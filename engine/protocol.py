"""The fixed experimental protocol. Agents never edit this file.

Owns: walk-forward splits, engine parameters, hard gates, the causality
(no-lookahead) check, trial recording, the champion-vs-candidate verdict, the
holdout veto, and promotion.

The holdout split is read in exactly one place — `holdout_gate` — and only for
candidates that have already won on validation and cleared the deflated-Sharpe
bar. It can veto a promotion; it is never scored, ranked or maximized.

Two tracks share this protocol. A `challenge` candidate (the default) competes
for the champion seat exactly as it always has. A `scout` candidate explores a
family the lab has not established: it runs the same causality check, the same
splits and the same hard gates, and it counts as a full trial in the
deflated-Sharpe deflator — but it never compares against the champion, so it
never reaches the holdout gate. It earns `FAMILY_LEAD` by being the best result
yet recorded in its own family. The seat is unchanged and unreachable from the
scout track; a family's lead reaches it, if at all, through a `challenge`
candidate that builds on it.
"""

from __future__ import annotations

import importlib.util
import inspect
import json
import math
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from . import data, metrics
from .backtest import run_backtest, sanitize_weights

ROOT = Path(__file__).resolve().parent.parent
CHAMPION_FILE = ROOT / "strategies" / "champion.py"
LEADERBOARD_FILE = ROOT / "experiments" / "leaderboard.json"
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

# The holdout veto. A candidate that has already won on validation is refused the
# seat if it is worse than the incumbent on holdout by more than this many paired
# standard errors (`metrics.sharpe_diff_se`).
#
# Why a veto and not a second objective. Scoring holdout would make it a selection
# set, and there is no third split held in reserve; a one-sided veto leaks roughly
# one bit per trial where maximizing it would leak the whole ranking. The gate is
# also placed last, after causality, the hard gates, the champion comparison and
# DSR, so it reads holdout only for candidates that would have been promoted
# outright before it existed — the number of candidate holdout reads is unchanged.
#
# Why it exists. Validation and holdout stopped agreeing at trial #43, and the
# gate could not see it: four consecutive promotions raised validation Sharpe
# 1.120 -> 1.229 while holdout fell 1.377 -> 0.691. On the closed-form paired SE
# no promotion in this repo's history ever cleared |t| = 2 on validation, while
# five of six superseded champions beat the incumbent on holdout at |t| > 2. The
# gate was breaking ties on the split with no resolving power. At 2.0 the veto
# fires only on a loss the data can actually resolve; a tie still promotes, so
# the burden of proof stays on the challenger without holdout becoming a target.
HOLDOUT_VETO_T = 2.0

# Tracks. `challenge` is the historical behaviour and stays the default, so
# every candidate written before this existed is a challenger. `scout` trades
# the champion comparison (and with it any access to the holdout) for a verdict
# that can record progress inside a family the lab has not yet established.
TRACKS = ("challenge", "scout")
DEFAULT_TRACK = "challenge"


@dataclass
class TrialResult:
    candidate: str
    name: str
    family: str
    hypothesis: str
    verdict: str                      # PROMOTE | REJECT | GATE_FAIL | HOLDOUT_VETO
                                      # | FAMILY_LEAD | SCOUT
    reasons: list[str]
    train: dict = field(default_factory=dict)
    validation: dict = field(default_factory=dict)
    holdout: dict | None = None       # filled only when the holdout gate is reached
    champion_val_sharpe: float | None = None
    champion_dsr: float | None = None  # incumbent re-deflated at today's bar
    dsr: float | None = None
    n_trials: int = 0
    n_effective_trials: float = 0.0
    track: str = DEFAULT_TRACK
    family_best_sharpe: float | None = None   # best prior validation sharpe in this family
    # The holdout gate's arithmetic, recorded whether it vetoed or let the
    # candidate through, so every reading of the split leaves an audit trail.
    champion_holdout_sharpe: float | None = None
    holdout_delta: float | None = None   # candidate minus champion, annualized
    holdout_se: float | None = None      # paired SE of that difference
    holdout_rho: float | None = None     # correlation of the two holdout series
    holdout_t: float | None = None       # delta / se
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
    track = str(meta.get("track", DEFAULT_TRACK)).strip().lower()
    if track not in TRACKS:
        raise ValueError(f"{path}: STRATEGY['track'] must be one of {TRACKS}, got {track!r}")
    return mod, {
        "name": meta.get("name", path.stem),
        "family": meta.get("family", "unknown"),
        "hypothesis": meta.get("hypothesis", ""),
        "track": track,
    }


def normalize_family(family: str) -> str:
    """Family labels are free text; the leaderboard groups on this."""
    return " ".join(str(family or "unknown").strip().lower().split())


def call_strategy(generate_weights, prices: pd.DataFrame, aux: dict | None = None):
    """Call a strategy under whichever contract it declares.

    `generate_weights(prices)` is the original contract and still the whole of
    what most candidates need. A strategy that also declares a second positional
    parameter receives the auxiliary OHLCV panels — already narrowed to exactly
    the rows of `prices`, because a panel that outran the prices it accompanies
    would hand the strategy the future while the causality check watched the
    wrong frame."""
    params = [
        p for p in inspect.signature(generate_weights).parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    if len(params) >= 2:
        return generate_weights(prices, data.slice_panels(aux, prices.index))
    return generate_weights(prices)


def evaluate_split(
    generate_weights, prices: pd.DataFrame, split: str, aux: dict | None = None
) -> dict:
    """Run the strategy with data visible up to the split's end; score only the
    returns inside the split window."""
    start, end = SPLITS[split]
    visible = prices.loc[:end] if end else prices
    weights = call_strategy(generate_weights, visible, aux)
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
    generate_weights, prices: pd.DataFrame, cuts=(63, 252), tail_buffer=5,
    aux: dict | None = None,
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
    w_full = effective(call_strategy(generate_weights, visible, aux), visible)
    # Always include a deep truncation: shallow cuts can miss strategies whose
    # future-dependent selection happens to be stable over short horizons.
    for cut in (*cuts, len(visible) // 2):
        if len(visible) <= cut + 300:
            continue
        truncated = visible.iloc[:-cut]
        w_trunc = effective(call_strategy(generate_weights, truncated, aux), truncated)
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


def recorded_trials() -> list[dict]:
    """Every trial record, oldest first. Read-only; `trials.jsonl` is append-only."""
    if not TRIALS_FILE.exists():
        return []
    out = []
    with open(TRIALS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def family_best_sharpe(family: str, records: list[dict] | None = None) -> float | None:
    """Best validation Sharpe yet recorded in `family`, or None if it has none.

    Only trials that reached the validation split count — a candidate killed by
    the causality check or the hard gates has no number to be best with."""
    fam = normalize_family(family)
    best = None
    for rec in (recorded_trials() if records is None else records):
        if normalize_family(rec.get("family", "")) != fam:
            continue
        sharpe = (rec.get("validation") or {}).get("sharpe")
        if sharpe is None:
            continue
        best = float(sharpe) if best is None else max(best, float(sharpe))
    return best


def champion_trial_returns(records: list[dict]) -> pd.Series | None:
    """The seated champion's stored validation returns, for correlation only.

    Found from the champion card's name, falling back to the last PROMOTE. Used
    to report how decorrelated each family's lead is from the incumbent — the
    quantity an ensemble challenger has to argue from. Costs no re-run."""
    name = None
    if CHAMPION_CARD.exists():
        try:
            name = json.loads(CHAMPION_CARD.read_text()).get("name")
        except (json.JSONDecodeError, OSError):
            name = None
    matches = [r for r in records if name and r.get("name") == name]
    if not matches:
        matches = [r for r in records if r.get("verdict") == "PROMOTE"]
    for rec in reversed(matches):
        rets = load_trial_returns(rec.get("ts", ""), rec.get("name", ""))
        if rets is not None and len(rets) > 1:
            return rets
    return None


def write_leaderboard() -> dict:
    """Regenerate `experiments/leaderboard.json` from the recorded trials.

    One row per family: its best validation result, and that result's return
    correlation with the seated champion. Derived entirely from `trials.jsonl`
    and the stored per-trial returns — no strategy is re-run, no split is read,
    and nothing here feeds a gate. It exists so that a family the champion
    comparison would score as a plain REJECT still leaves a legible record of
    how far it got and how decorrelated it is."""
    records = recorded_trials()
    champ_rets = champion_trial_returns(records)
    rows: dict[str, dict] = {}
    for rec in records:
        val = rec.get("validation") or {}
        if val.get("sharpe") is None:
            continue
        fam = normalize_family(rec.get("family", ""))
        row = rows.get(fam)
        if row is not None and float(val["sharpe"]) <= row["validation"]["sharpe"]:
            rows[fam] = {**row, "n_trials": row["n_trials"] + 1}
            continue
        rho = None
        rets = load_trial_returns(rec.get("ts", ""), rec.get("name", ""))
        if champ_rets is not None and rets is not None and len(rets) > 1:
            r = float(rets.corr(champ_rets))
            rho = None if not math.isfinite(r) else round(r, 4)
        rows[fam] = {
            "name": rec.get("name"),
            "candidate": rec.get("candidate"),
            "track": rec.get("track", DEFAULT_TRACK),
            "verdict": rec.get("verdict"),
            "ts": rec.get("ts"),
            "n_trials": (row["n_trials"] + 1) if row else 1,
            "rho_to_champion": rho,
            "validation": {
                k: val.get(k) for k in
                ("sharpe", "ann_return", "max_drawdown", "ann_turnover", "avg_positions")
            },
            "train_sharpe": (rec.get("train") or {}).get("sharpe"),
        }
    board = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "champion": (
            json.loads(CHAMPION_CARD.read_text()).get("name")
            if CHAMPION_CARD.exists() else None
        ),
        "families": dict(sorted(rows.items(), key=lambda kv: -kv[1]["validation"]["sharpe"])),
    }
    LEADERBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEADERBOARD_FILE.write_text(json.dumps(board, indent=2) + "\n")
    return board


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


def run_trial(
    candidate_path: Path, prices: pd.DataFrame, aux: dict | None = None
) -> TrialResult:
    """The one entry point for judging a candidate. Never bypass this."""
    mod, meta = load_strategy(candidate_path)
    result = TrialResult(
        candidate=str(candidate_path.relative_to(ROOT)),
        name=meta["name"], family=meta["family"], hypothesis=meta["hypothesis"],
        verdict="GATE_FAIL", reasons=[], track=meta["track"],
        ts=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    causality_error = causality_check(mod.generate_weights, prices, aux=aux)
    if causality_error:
        result.reasons = [f"causality: {causality_error}"]
        record_trial(result)
        write_leaderboard()
        return result

    result.train = evaluate_split(mod.generate_weights, prices, "train", aux)
    result.validation = evaluate_split(mod.generate_weights, prices, "validation", aux)

    gate_fails = apply_gates(result.train, result.validation)
    if gate_fails:
        result.reasons = gate_fails
        record_trial(result)
        write_leaderboard()
        return result

    prior_records = recorded_trials()
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

    if result.track == "scout":
        # A scout is not competing for the seat, so the champion is never loaded
        # and `holdout_gate` is unreachable from here: a scouting session spends
        # no look at the holdout and never has to stop. It is still a full trial
        # in the deflator above — exploring is cheap, but it is not free, and
        # pretending otherwise would understate the bar for everyone after.
        result.family_best_sharpe = family_best_sharpe(result.family, prior_records)
        if result.family_best_sharpe is None:
            result.verdict = "FAMILY_LEAD"
            result.reasons = [
                f"first recorded result in family '{normalize_family(result.family)}': "
                f"validation sharpe {result.validation['sharpe']}, DSR {result.dsr} ({bar})"
            ]
        elif result.validation["sharpe"] > result.family_best_sharpe:
            result.verdict = "FAMILY_LEAD"
            result.reasons = [
                f"best result yet in family '{normalize_family(result.family)}': "
                f"validation sharpe {result.validation['sharpe']} > "
                f"{result.family_best_sharpe} (DSR {result.dsr}, {bar})"
            ]
        else:
            result.verdict = "SCOUT"
            result.reasons = [
                f"scouted family '{normalize_family(result.family)}': validation sharpe "
                f"{result.validation['sharpe']} <= the family's best "
                f"{result.family_best_sharpe} (DSR {result.dsr}, {bar})"
            ]
        record_trial(result)
        write_leaderboard()
        return result

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
            promote(candidate_path, result, prices, aux=aux)
        record_trial(result)
        write_leaderboard()
        return result

    champ_mod, _ = load_strategy(CHAMPION_FILE)
    champ_val = evaluate_split(champ_mod.generate_weights, prices, "validation", aux)
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

    # Each branch either rejects outright or states the case for promotion. Nothing
    # is promoted here — every winner still has to clear the holdout gate below.
    promote_reasons: list[str] | None = None

    if result.validation["sharpe"] <= champ_val["sharpe"]:
        result.verdict = "REJECT"
        result.reasons = [
            f"validation sharpe {result.validation['sharpe']} <= champion {champ_val['sharpe']}"
        ]
    elif result.dsr >= DSR_THRESHOLD:
        promote_reasons = [
            f"beats champion ({result.validation['sharpe']} > {champ_val['sharpe']}) "
            f"with DSR {result.dsr} ({bar})"
        ]
    elif champion_provisional and result.dsr > result.champion_dsr:
        promote_reasons = [
            f"provisional champion: incumbent no longer clears the bar "
            f"(champion DSR {result.champion_dsr} < {DSR_THRESHOLD}), and this candidate "
            f"beats it on validation sharpe ({result.validation['sharpe']} > "
            f"{champ_val['sharpe']}) and on deflated sharpe ({result.dsr} > "
            f"{result.champion_dsr}) ({bar}). Still below {DSR_THRESHOLD} — not yet earned"
        ]
    else:
        result.verdict = "REJECT"
        result.reasons = [
            f"deflated sharpe prob {result.dsr} < {DSR_THRESHOLD} ({bar}); "
            f"champion DSR {result.champion_dsr}"
        ]

    if promote_reasons is not None:
        result.verdict = holdout_gate(
            mod, champ_mod, prices, result, promote_reasons, candidate_path, aux=aux
        )

    record_trial(result)
    write_leaderboard()
    return result


# ---------------------------------------------------------------------------
# The holdout gate — the last word on a promotion
# ---------------------------------------------------------------------------

def holdout_gate(
    mod,
    champ_mod,
    prices: pd.DataFrame,
    result: TrialResult,
    promote_reasons: list[str],
    candidate_path: Path,
    aux: dict | None = None,
) -> str:
    """Final gate: refuse the seat to a candidate the holdout says is worse.

    Reached only by candidates that have already won on validation and cleared
    the deflated-Sharpe bar — i.e. exactly the set that was promoted outright
    before this gate existed, so it reads no candidate's holdout that the old
    protocol would not have read anyway. The incumbent is re-scored on the same
    window for a paired comparison; its holdout is already public in the card
    and in `trials.jsonl`, so that costs no new information.

    The test is one-sided. A candidate that ties, or wins, on holdout is
    promoted; only a loss large enough to resolve against the paired standard
    error (`t < -HOLDOUT_VETO_T`) is refused. Holdout is never scored, ranked or
    maximized here — it can only ever say no.

    Returns the verdict and, on a veto, leaves the champion untouched.
    """
    cand_hold = evaluate_split(mod.generate_weights, prices, "holdout", aux)
    champ_hold = evaluate_split(champ_mod.generate_weights, prices, "holdout", aux)

    se, rho = metrics.sharpe_diff_se(cand_hold["_returns"], champ_hold["_returns"])
    delta = cand_hold["sharpe"] - champ_hold["sharpe"]
    # A degenerate comparison returns se = inf, so t = 0.0 and nothing is vetoed.
    t = delta / se if se else 0.0

    result.holdout = cand_hold
    result.champion_holdout_sharpe = champ_hold["sharpe"]
    result.holdout_delta = round(float(delta), 4)
    result.holdout_se = None if not math.isfinite(se) else round(float(se), 4)
    result.holdout_rho = None if not math.isfinite(rho) else round(float(rho), 4)
    result.holdout_t = round(float(t), 3)

    arith = (
        f"holdout {cand_hold['sharpe']} vs champion {champ_hold['sharpe']} "
        f"(delta {delta:+.3f}, paired SE {se:.3f} at rho {rho:.3f}, t {t:+.2f})"
    )

    if t < -HOLDOUT_VETO_T:
        result.reasons = [
            f"holdout veto: {arith} — worse than the incumbent by more than "
            f"{HOLDOUT_VETO_T} paired standard errors. It won validation "
            f"({result.validation['sharpe']} > {result.champion_val_sharpe}), but the "
            f"two splits disagree and the seat is not transferred on a split the "
            f"comparison cannot resolve"
        ]
        return "HOLDOUT_VETO"

    result.reasons = promote_reasons + [f"holdout gate passed: {arith}"]
    promote(candidate_path, result, prices, holdout=cand_hold, aux=aux)
    return "PROMOTE"


# ---------------------------------------------------------------------------
# Promotion — the only place holdout is ever evaluated
# ---------------------------------------------------------------------------

def promote(
    candidate_path: Path,
    result: TrialResult,
    prices: pd.DataFrame,
    holdout: dict | None = None,
    aux: dict | None = None,
) -> None:
    """Seat the candidate as champion.

    `holdout` may carry the metrics the holdout gate has already computed, so a
    promotion reads the split once rather than twice. The gate scores the
    candidate module and this scores the freshly-copied champion file, which is
    a byte-for-byte copy of it — the two are the same measurement.
    """
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

    if holdout is None:
        mod, _ = load_strategy(CHAMPION_FILE)
        holdout = evaluate_split(mod.generate_weights, prices, "holdout", aux)
    result.holdout = holdout

    card = {
        "name": result.name,
        "family": result.family,
        "hypothesis": result.hypothesis,
        "track": result.track,
        "promoted_at": result.ts,
        "source_candidate": result.candidate,
        "n_trials_at_promotion": result.n_trials,
        "n_effective_trials_at_promotion": result.n_effective_trials,
        "dsr_at_promotion": result.dsr,
        "provisional": result.dsr is not None and result.dsr < DSR_THRESHOLD,
        "train": _public(result.train),
        "validation": _public(result.validation),
        "holdout": _public(result.holdout),
        "holdout_gate": {
            "champion_holdout_sharpe": result.champion_holdout_sharpe,
            "delta": result.holdout_delta,
            "se": result.holdout_se,
            "rho": result.holdout_rho,
            "t": result.holdout_t,
            "veto_t": HOLDOUT_VETO_T,
        },
        "engine_params": ENGINE_PARAMS,
    }
    CHAMPION_CARD.write_text(json.dumps(card, indent=2) + "\n")
