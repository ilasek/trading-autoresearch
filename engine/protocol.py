"""The fixed experimental protocol. Agents never edit this file.

Owns: walk-forward splits, engine parameters, hard gates, the causality
(no-lookahead) check, trial recording, the champion-vs-candidate verdict, and
promotion (including the only permitted holdout evaluation).
"""

from __future__ import annotations

import importlib.util
import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from . import metrics
from .backtest import run_backtest, sanitize_weights

ROOT = Path(__file__).resolve().parent.parent
CHAMPION_FILE = ROOT / "strategies" / "champion.py"
CHAMPION_CARD = ROOT / "strategies" / "champion_card.json"
ARCHIVE_DIR = ROOT / "strategies" / "archive"
TRIALS_FILE = ROOT / "experiments" / "trials.jsonl"

# Walk-forward splits (inclusive bounds; holdout end = latest data).
SPLITS = {
    "train": (None, "2017-12-31"),
    "validation": ("2018-01-01", "2023-12-31"),
    "holdout": ("2024-01-01", None),
}

ENGINE_PARAMS = dict(
    cost_bps=10.0, slippage_bps=5.0, max_weight=0.25, max_leverage=1.0, allow_short=False,
)

GATES = dict(
    min_train_sharpe=0.0,      # must not lose money in-sample (sanity, not selection)
    max_drawdown=-0.45,        # validation drawdown must be better than this
    max_ann_turnover=50.0,     # ~2 full portfolio rotations per week is already extreme
    min_avg_positions=4.0,     # diversification floor
    min_active_days=126,       # must actually hold positions for ~6 months of validation
)

DSR_THRESHOLD = 0.95


@dataclass
class TrialResult:
    candidate: str
    name: str
    family: str
    hypothesis: str
    verdict: str                      # PROMOTE | REJECT | GATE_FAIL
    reasons: list[str]
    train: dict = field(default_factory=dict)
    validation: dict = field(default_factory=dict)
    holdout: dict | None = None       # filled only on promotion
    champion_val_sharpe: float | None = None
    dsr: float | None = None
    n_trials: int = 0
    ts: str = ""

    def to_record(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


# ---------------------------------------------------------------------------
# Strategy loading & evaluation
# ---------------------------------------------------------------------------

def load_strategy(path: Path):
    """Import a strategy module from a file path; validate the contract."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "generate_weights"):
        raise ValueError(f"{path} does not define generate_weights(prices)")
    meta = getattr(mod, "STRATEGY", {})
    return mod, {
        "name": meta.get("name", path.stem),
        "family": meta.get("family", "unknown"),
        "hypothesis": meta.get("hypothesis", ""),
    }


def evaluate_split(generate_weights, prices: pd.DataFrame, split: str) -> dict:
    """Run the strategy with data visible up to the split's end; score only the
    returns inside the split window."""
    start, end = SPLITS[split]
    visible = prices.loc[:end] if end else prices
    weights = generate_weights(visible)
    res = run_backtest(weights, visible, **ENGINE_PARAMS)
    window = res.returns.loc[start:end] if start else res.returns.loc[:end]
    w_window = res.weights.loc[window.index]
    turnover = res.turnover.loc[window.index]
    active_days = int((w_window.abs().sum(axis=1) > 1e-6).sum())
    out = metrics.summary(window)
    out.update({
        "ann_turnover": round(float(turnover.mean() * 252), 2),
        "avg_positions": round(float((w_window.abs() > 1e-6).sum(axis=1).mean()), 2),
        "active_days": active_days,
        "sharpe_daily": round(
            float(window.mean() / window.std(ddof=1)) if window.std(ddof=1) > 0 else 0.0, 6
        ),
        "_returns": window,  # stripped before serialization
    })
    return out


def _public(d: dict | None) -> dict | None:
    if d is None:
        return None
    return {k: v for k, v in d.items() if not k.startswith("_")}


# ---------------------------------------------------------------------------
# Causality (no-lookahead) check
# ---------------------------------------------------------------------------

def causality_check(
    generate_weights, prices: pd.DataFrame, cuts=(63, 252), tail_buffer=5
) -> str | None:
    """Recompute weights on truncated histories: a causal strategy produces
    identical *effective daily holdings* for the dates both runs can see.

    We compare post-sanitize, forward-filled holdings rather than raw weight
    frames so that sparse rebalance schedules (whose final partial-period
    rebalance shifts with the truncation point) don't false-positive; the last
    `tail_buffer` shared days are excluded for the same reason. Returns an
    error string on failure, None if causal."""

    def effective(w, px):
        p = ENGINE_PARAMS
        return sanitize_weights(w, px, p["max_weight"], p["max_leverage"], p["allow_short"])

    end = SPLITS["validation"][1]
    visible = prices.loc[:end]
    w_full = effective(generate_weights(visible), visible)
    # Always include a deep truncation: shallow cuts can miss strategies whose
    # future-dependent selection happens to be stable over short horizons.
    for cut in (*cuts, len(visible) // 2):
        if len(visible) <= cut + 300:
            continue
        truncated = visible.iloc[:-cut]
        w_trunc = effective(generate_weights(truncated), truncated)
        common = w_trunc.index[:-tail_buffer]
        diff = (w_full.loc[common] - w_trunc.loc[common]).abs().max().max()
        if diff > 1e-6:
            return (
                f"holdings change when future data is hidden (max diff {diff:.2e} "
                f"with last {cut} days removed) — strategy is peeking ahead"
            )
    return None


# ---------------------------------------------------------------------------
# Gates & verdict
# ---------------------------------------------------------------------------

def apply_gates(train: dict, validation: dict) -> list[str]:
    fails = []
    if train["sharpe"] <= GATES["min_train_sharpe"]:
        fails.append(f"train sharpe {train['sharpe']} <= {GATES['min_train_sharpe']}")
    if validation["max_drawdown"] < GATES["max_drawdown"]:
        fails.append(
            f"validation drawdown {validation['max_drawdown']} worse than {GATES['max_drawdown']}"
        )
    if validation["ann_turnover"] > GATES["max_ann_turnover"]:
        fails.append(
            f"annual turnover {validation['ann_turnover']} > {GATES['max_ann_turnover']}"
        )
    if validation["avg_positions"] < GATES["min_avg_positions"]:
        fails.append(
            f"avg positions {validation['avg_positions']} < {GATES['min_avg_positions']}"
        )
    if validation["active_days"] < GATES["min_active_days"]:
        fails.append(
            f"active days {validation['active_days']} < {GATES['min_active_days']}"
        )
    return fails


def past_trial_sharpes() -> list[float]:
    """Daily-frequency validation Sharpes of every recorded trial."""
    if not TRIALS_FILE.exists():
        return []
    out = []
    with open(TRIALS_FILE) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            sd = rec.get("validation", {}).get("sharpe_daily")
            if sd is not None:
                out.append(float(sd))
    return out


def record_trial(result: TrialResult) -> None:
    TRIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    rec = result.to_record()
    rec["train"] = _public(rec["train"])
    rec["validation"] = _public(rec["validation"])
    rec["holdout"] = _public(rec["holdout"])
    with open(TRIALS_FILE, "a") as f:
        f.write(json.dumps(rec) + "\n")


def run_trial(candidate_path: Path, prices: pd.DataFrame) -> TrialResult:
    """The one entry point for judging a candidate. Never bypass this."""
    mod, meta = load_strategy(candidate_path)
    result = TrialResult(
        candidate=str(candidate_path.relative_to(ROOT)),
        name=meta["name"], family=meta["family"], hypothesis=meta["hypothesis"],
        verdict="GATE_FAIL", reasons=[],
        ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    causality_error = causality_check(mod.generate_weights, prices)
    if causality_error:
        result.reasons = [f"causality: {causality_error}"]
        record_trial(result)
        return result

    result.train = evaluate_split(mod.generate_weights, prices, "train")
    result.validation = evaluate_split(mod.generate_weights, prices, "validation")

    gate_fails = apply_gates(result.train, result.validation)
    if gate_fails:
        result.reasons = gate_fails
        record_trial(result)
        return result

    trial_sharpes = past_trial_sharpes() + [result.validation["sharpe_daily"]]
    result.n_trials = len(trial_sharpes)
    result.dsr = round(
        metrics.deflated_sharpe(result.validation["_returns"], trial_sharpes), 4
    )

    if not CHAMPION_FILE.exists():
        result.verdict = "PROMOTE"
        result.reasons = ["bootstrap: no champion exists; gates passed"]
        promote(candidate_path, result, prices)
        record_trial(result)
        return result

    champ_mod, _ = load_strategy(CHAMPION_FILE)
    champ_val = evaluate_split(champ_mod.generate_weights, prices, "validation")
    result.champion_val_sharpe = champ_val["sharpe"]

    if result.validation["sharpe"] <= champ_val["sharpe"]:
        result.verdict = "REJECT"
        result.reasons = [
            f"validation sharpe {result.validation['sharpe']} <= champion {champ_val['sharpe']}"
        ]
    elif result.dsr < DSR_THRESHOLD:
        result.verdict = "REJECT"
        result.reasons = [
            f"deflated sharpe prob {result.dsr} < {DSR_THRESHOLD} "
            f"(bar set by {result.n_trials} total trials)"
        ]
    else:
        result.verdict = "PROMOTE"
        result.reasons = [
            f"beats champion ({result.validation['sharpe']} > {champ_val['sharpe']}) "
            f"with DSR {result.dsr}"
        ]
        promote(candidate_path, result, prices)

    record_trial(result)
    return result


# ---------------------------------------------------------------------------
# Promotion — the only place holdout is ever evaluated
# ---------------------------------------------------------------------------

def promote(candidate_path: Path, result: TrialResult, prices: pd.DataFrame) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    if CHAMPION_FILE.exists():
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        old_name = "champion"
        if CHAMPION_CARD.exists():
            old_name = json.loads(CHAMPION_CARD.read_text()).get("name", old_name)
        shutil.copy2(CHAMPION_FILE, ARCHIVE_DIR / f"{stamp}_{old_name}.py")
        if CHAMPION_CARD.exists():
            shutil.copy2(CHAMPION_CARD, ARCHIVE_DIR / f"{stamp}_{old_name}_card.json")

    shutil.copy2(candidate_path, CHAMPION_FILE)

    mod, _ = load_strategy(CHAMPION_FILE)
    result.holdout = evaluate_split(mod.generate_weights, prices, "holdout")

    card = {
        "name": result.name,
        "family": result.family,
        "hypothesis": result.hypothesis,
        "promoted_at": result.ts,
        "source_candidate": result.candidate,
        "n_trials_at_promotion": result.n_trials,
        "train": _public(result.train),
        "validation": _public(result.validation),
        "holdout": _public(result.holdout),
        "engine_params": ENGINE_PARAMS,
    }
    CHAMPION_CARD.write_text(json.dumps(card, indent=2) + "\n")
