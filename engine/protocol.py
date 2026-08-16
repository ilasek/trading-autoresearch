"""The fixed experimental protocol. Agents never edit this file.

Owns: walk-forward splits, engine parameters, hard gates, the causality
(no-lookahead) check, trial recording, the champion-vs-candidate verdict, and
promotion (including the only permitted holdout evaluation).
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import metrics
from .backtest import run_backtest, sanitize_weights

ROOT = Path(__file__).resolve().parent.parent
CHAMPION_FILE = ROOT / "strategies" / "champion.py"
CHAMPION_CARD = ROOT / "strategies" / "champion_card.json"
ARCHIVE_DIR = ROOT / "strategies" / "archive"
TRIALS_FILE = ROOT / "experiments" / "trials.jsonl"
# Per-trial validation return series live in one Parquet per recorded trial,
# under the directory below. They are what makes it possible to measure how
# redundant the search has been (see `effective_n_trials`). The file name is
# derived from the trial's timestamp and name, so `trials.jsonl` stays
# append-only and is never rewritten to reference them.
TRIAL_RETURNS_DIRNAME = "trial_returns"


def trial_returns_dir() -> Path:
    """Resolved from ROOT on every call so that redirecting ROOT (as the test
    sandbox does) also redirects the returns store."""
    return ROOT / "experiments" / TRIAL_RETURNS_DIRNAME

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

# Two trials whose validation return series correlate at or above this level are
# counted as one effective trial. Tuning the 21st variant of an idea is not an
# independent shot at a high Sharpe; deflating as if it were punishes breadth
# and rewards fine-tuning the incumbent.
TRIAL_CLUSTER_RHO = 0.95


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
    champion_dsr: float | None = None  # incumbent re-deflated at today's bar
    dsr: float | None = None
    n_trials: int = 0
    n_effective_trials: float = 0.0
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


def returns_path(ts: str, name: str) -> Path:
    """Deterministic location of a trial's stored validation returns."""
    try:
        stamp = datetime.fromisoformat(ts).strftime("%Y%m%dT%H%M%SZ")
    except ValueError:
        stamp = re.sub(r"[^0-9A-Za-z]", "", ts)
    slug = re.sub(r"[^0-9A-Za-z_.-]", "_", name or "unnamed")
    return trial_returns_dir() / f"{stamp}_{slug}.parquet"


def store_trial_returns(ts: str, name: str, returns: pd.Series) -> Path:
    trial_returns_dir().mkdir(parents=True, exist_ok=True)
    path = returns_path(ts, name)
    returns.rename("ret").to_frame().to_parquet(path)
    return path


def load_trial_returns(ts: str, name: str) -> pd.Series | None:
    path = returns_path(ts, name)
    if not path.exists():
        return None
    return pd.read_parquet(path)["ret"]


def past_trial_sharpes() -> list[float]:
    """Daily-frequency validation Sharpes of every recorded trial."""
    return [sharpe for sharpe, _ in past_trials()]


def past_trials() -> list[tuple[float, pd.Series | None]]:
    """(daily validation Sharpe, validation returns) for every recorded trial.

    Returns are None for trials recorded before per-trial returns were stored
    and never backfilled; those count as fully independent trials."""
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
            if sd is None:
                continue
            out.append((float(sd), load_trial_returns(rec.get("ts", ""), rec.get("name", ""))))
    return out


def effective_n_trials(returns_list: list[pd.Series | None], rho: float = TRIAL_CLUSTER_RHO) -> float:
    """How many *independent* trials a set of trials is worth.

    Single-linkage clustering on the correlation of validation return series:
    trials that move together are one effective shot at a high Sharpe, however
    many parameter variants they were split into. Trials whose returns were not
    stored cannot be shown to be redundant, so each counts on its own.

    Deliberately conservative — single linkage only merges a variant into a
    cluster when it correlates at `rho` with something already in it, and the
    result is never below the number of distinct return series."""
    stored = [r for r in returns_list if r is not None and len(r) > 1]
    n_missing = len(returns_list) - len(stored)
    if not stored:
        return float(n_missing)

    mat = pd.concat(
        [r.rename(i) for i, r in enumerate(stored)], axis=1, join="outer"
    ).corr()  # pairwise-complete observations
    corr = mat.to_numpy()

    parent = list(range(len(stored)))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(len(stored)):
        for j in range(i + 1, len(stored)):
            r = corr[i, j]
            if np.isfinite(r) and r >= rho:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[ri] = rj

    n_clusters = len({find(i) for i in range(len(stored))})
    return float(n_clusters + n_missing)


def record_trial(result: TrialResult) -> None:
    TRIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    rets = (result.validation or {}).get("_returns")
    if rets is not None and len(rets):
        store_trial_returns(result.ts, result.name, rets)
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

    prior = past_trials()
    trial_sharpes = [s for s, _ in prior] + [result.validation["sharpe_daily"]]
    trial_returns = [r for _, r in prior] + [result.validation["_returns"]]
    result.n_trials = len(trial_sharpes)
    result.n_effective_trials = effective_n_trials(trial_returns)
    result.dsr = round(
        metrics.deflated_sharpe(
            result.validation["_returns"], trial_sharpes, result.n_effective_trials
        ),
        4,
    )
    bar = (
        f"{result.n_trials} trials, {result.n_effective_trials:g} effective "
        f"after clustering at rho {TRIAL_CLUSTER_RHO}"
    )

    if not CHAMPION_FILE.exists():
        # The first champion clears the same bar as every challenger after it.
        # Nothing holds the seat until something earns it.
        if result.dsr < DSR_THRESHOLD:
            result.verdict = "REJECT"
            result.reasons = [
                f"bootstrap: deflated sharpe prob {result.dsr} < {DSR_THRESHOLD} ({bar}) "
                f"— no champion is seated until a candidate clears the bar"
            ]
        else:
            result.verdict = "PROMOTE"
            result.reasons = [f"bootstrap: no champion exists; gates passed with DSR {result.dsr}"]
            promote(candidate_path, result, prices)
        record_trial(result)
        return result

    champ_mod, _ = load_strategy(CHAMPION_FILE)
    champ_val = evaluate_split(champ_mod.generate_weights, prices, "validation")
    result.champion_val_sharpe = champ_val["sharpe"]
    # Re-deflate the incumbent against exactly the bar the challenger faces. A
    # champion promoted when the trial count was low is not entitled to a seat it
    # could not win today; if it can no longer clear the threshold its tenure is
    # provisional and the best-deflated strategy holds the seat instead.
    result.champion_dsr = round(
        metrics.deflated_sharpe(
            champ_val["_returns"], trial_sharpes, result.n_effective_trials
        ),
        4,
    )
    champion_provisional = result.champion_dsr < DSR_THRESHOLD

    if result.validation["sharpe"] <= champ_val["sharpe"]:
        result.verdict = "REJECT"
        result.reasons = [
            f"validation sharpe {result.validation['sharpe']} <= champion {champ_val['sharpe']}"
        ]
    elif result.dsr >= DSR_THRESHOLD:
        result.verdict = "PROMOTE"
        result.reasons = [
            f"beats champion ({result.validation['sharpe']} > {champ_val['sharpe']}) "
            f"with DSR {result.dsr} ({bar})"
        ]
        promote(candidate_path, result, prices)
    elif champion_provisional and result.dsr > result.champion_dsr:
        result.verdict = "PROMOTE"
        result.reasons = [
            f"provisional champion: incumbent no longer clears the bar "
            f"(champion DSR {result.champion_dsr} < {DSR_THRESHOLD}), and this candidate "
            f"beats it on validation sharpe ({result.validation['sharpe']} > "
            f"{champ_val['sharpe']}) and on deflated sharpe ({result.dsr} > "
            f"{result.champion_dsr}) ({bar}). Still below {DSR_THRESHOLD} — not yet earned"
        ]
        promote(candidate_path, result, prices)
    else:
        result.verdict = "REJECT"
        result.reasons = [
            f"deflated sharpe prob {result.dsr} < {DSR_THRESHOLD} ({bar}); "
            f"champion DSR {result.champion_dsr}"
        ]

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
        "n_effective_trials_at_promotion": result.n_effective_trials,
        "dsr_at_promotion": result.dsr,
        "provisional": result.dsr is not None and result.dsr < DSR_THRESHOLD,
        "train": _public(result.train),
        "validation": _public(result.validation),
        "holdout": _public(result.holdout),
        "engine_params": ENGINE_PARAMS,
    }
    CHAMPION_CARD.write_text(json.dumps(card, indent=2) + "\n")
