"""Peer-network momentum: score a name by what its four closest peers just did.

WHY THIS FILE EXISTS. `program.md` names five sub-mechanisms under
`lead-lag-spillover` and the lab has measured three of them. ETF-versus-constituent
was screened to a null (`learnings.md` 2026-08-31). Region-leading-region is closed
on a rejection (2026-09-16), and the surviving West -> JP/HK pairs turn out to be
filled by the engine's own 1-day execution lag. Sector-group lead-lag is the
family's seated lead (`ll_group_lastmonth_lead`, 0.688). **Network momentum has
never been run here**, and the family has two recorded trials in total, which makes
it the coldest reachable object on the board after tonight's screens closed
`statistical-arbitrage`'s residual-reversal vein (journal, F1/F2).

THE OBJECT, and every constant in it comes from somewhere else.

    peer_ret[i,t] = mean over i's K=4 most-correlated names of their
                    trailing 21-day return

`K = 4`, the 250-day correlation window and the 20-day lag are **inherited verbatim
from the seated champion's `E/Var` neighbourhood** (`pt_mom_evar_arbrisk`:
`EVAR_K`, `EVAR_WINDOW`, `EVAR_LAG`). Nothing about the neighbourhood is chosen
here, and no curve in `K` was computed. That is deliberate: `learnings.md`
2026-09-24 established that locality is a single monotone dial along which a
co-movement score turns into a low-beta bet, and it carries a standing
anti-candidate against reading a `K` off that curve. The cheapest way to honour it
is not to choose.

THE HYPOTHESIS'S DIRECTION WAS FIXED BEFORE IT WAS MEASURED. The 21-day horizon is
the month every momentum construction in this repo throws away because it reverses
at the name level. The transmission claim is that it does **not** reverse when it
arrives from a neighbour: the peers' move is news about a shared exposure that the
focal name has not finished repricing. So the sign is positive — hold names whose
peers just rose — and that was written in the journal's pre-registration addendum
before F6 ran.

WHAT F6 MEASURED, TRAIN ONLY, BEFORE THIS FILE WAS WRITTEN (397 month-ends,
mean 81.4 names per date; all three gates pre-registered at the house 0.50 bar):

    |spearman(peer_ret, own trailing 21d return)|   +0.328   PASS
    |spearman(peer_ret, own 4-horizon momentum z)|  +0.004   PASS
    |spearman(peer_ret, 250d realised vol level)|   +0.027   PASS
    IC(peer_ret, forward 21d return)                +0.0118  (t = +1.04)
    IC(peer_ret residualised on own momentum)       +0.0142  (t = +1.36)

The gates say this is a genuinely separate object rather than own reversal, own
momentum or the volatility artifact in costume — the +0.004 against the champion's
own momentum score is the striking one. **The IC says the signal is weak and
unresolved at t = +1.04, and the pre-registration fixed in advance that the IC
gates nothing**, because the purpose of a scout is to map a family and a null is
the result. This is stated here rather than discovered later.

CONSTRUCTION. The house name-level rank-and-band with hysteresis, transcribed from
the seat (`CORE_N = 15`, `BAND_N = 25`, `FLOOR = 0.05`, magnitude weighting off a
fixed anchor). Nothing about the construction is new, so that T2's one-node
difference is the only thing either file is testing.

PRE-REGISTERED: validation **near the family's 0.688 lead, range 0.45-0.85**. The
over-prediction rule has been the default since 2026-09-06, a peer-mean signal is a
smoothed object, and the IC behind it does not clear t = 2. **No drawdown call is
made: F4 retired the diversification ratio as a drawdown predictor tonight, and the
risk-contribution count's scatter makes a call here unfalsifiable rather than
small.**

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# --- transcribed from the seated champion's E/Var neighbourhood, not re-swept ---
PEER_WINDOW = 250
PEER_LAG = 20
PEER_K = 4

# --- transcribed from the seated champion's band, not re-swept ---
CORE_N = 15
BAND_N = 25
FLOOR = 0.05
MAX_WEIGHT = 0.25

PEER_HORIZON = 21      # the month the name-level signal throws away
MIN_NAMES = 30         # a cross-section below this is not scored

STRATEGY = {
    "name": "ll_peer_momentum",
    "family": "lead-lag-spillover",
    "track": "scout",
    "hypothesis": (
        "Holding the 15 names (25-name hold band) whose four most-correlated peers had "
        "the highest mean trailing 21-day return — the neighbourhood estimated on a "
        "250-day window lagged 20 days, K, window and lag all inherited verbatim from the "
        "seated champion's E/Var term and chosen nowhere here — scores a validation Sharpe "
        "near the lead-lag-spillover family's 0.688 lead (range 0.45-0.85), because the "
        "most recent month reverses at the name level but the transmission claim is that it "
        "continues when it arrives from a neighbour, and on 397 train month-ends peer_ret "
        "clears all three pre-registered orthogonality gates at the house 0.50 bar "
        "(+0.328 against the name's own trailing 21-day return, +0.004 against the "
        "champion's own four-horizon momentum score, +0.027 against the 250-day volatility "
        "level) while carrying a weak and unresolved IC of +0.0118 at t = +1.04, rising only "
        "to +0.0142 at t = +1.36 once own momentum is projected out. Network momentum is the "
        "one program.md sub-mechanism in this family with no measurement against it and the "
        "family has two recorded trials in total; above 0.85 says peer transmission is a "
        "real and separable object on this universe and the family's lead moves to a "
        "name-level construction, below 0.45 says a t = +1.04 IC does not survive a "
        "long-only book and the sub-mechanism is closed on a measurement rather than left "
        "open on a slug."
    ),
}


def _peer_scores(block: np.ndarray, names: list, own21: pd.Series) -> pd.Series:
    """Mean trailing 21-day return of each name's `PEER_K` most-correlated peers.

    The correlation matrix is built on the same de-meaned, standardized window the
    seat's `_hedgeable_fraction` uses, so "peer" means exactly what it means there.
    """
    v = block - block.mean(axis=0)
    sd = v.std(axis=0, ddof=1)
    ok = sd > 0
    if ok.sum() <= PEER_K + 1:
        return pd.Series(dtype=float)
    v, sd = v[:, ok], sd[ok]
    cols = [n for n, keep in zip(names, ok) if keep]
    n = len(cols)

    corr = (v.T @ v) / (len(v) - 1) / np.outer(sd, sd)
    np.fill_diagonal(corr, -np.inf)          # a name is not its own peer
    top = np.argpartition(-corr, PEER_K - 1, axis=1)[:, :PEER_K]

    r = own21.reindex(cols).to_numpy(dtype=float)
    with np.errstate(invalid="ignore"):
        scores = np.nanmean(r[top], axis=1)
    return pd.Series(scores, index=cols).replace([np.inf, -np.inf], np.nan).dropna()


def _band_target(score: pd.Series, held: set) -> tuple[pd.Series, set]:
    """House rank-and-band with hysteresis, transcribed from the seat.

    The floor is a fixed constant rather than an anchor on the weakest held name,
    which is the artifact `learnings.md`'s fixed-anchor entries spent four trials
    tracing."""
    ranked = score.sort_values(ascending=False)
    core = set(ranked.index[:CORE_N])
    band = set(ranked.index[:BAND_N])
    held = (held & band) | core
    chosen = score[list(held)]
    raw = chosen - chosen.min() + FLOOR
    w = raw / raw.sum()
    for _ in range(8):                        # cap to a fixed point, as the engine would
        if w.max() <= MAX_WEIGHT + 1e-12:
            break
        w = (w.clip(upper=MAX_WEIGHT))
        w = w / w.sum()
    return w, held


def _eligible(score: pd.Series, evar: pd.Series) -> pd.Series:
    """T1 holds the whole scoreable cross-section. `ll_peer_momentum_evargate` is
    this file with this one function replaced, and nothing else."""
    return score


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rets = prices.pct_change(fill_method=None)
    ret_values = rets.to_numpy()
    all_names = list(prices.columns)
    positions = {dt: i for i, dt in enumerate(prices.index)}

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in rebalance_dates:
        end = positions[dt] - PEER_LAG + 1
        start = end - PEER_WINDOW
        if start < 1:
            continue
        block = ret_values[start:end]
        finite = np.isfinite(block).all(axis=0)
        if finite.sum() <= PEER_K + 1:
            continue
        names = [n for n, keep in zip(all_names, finite) if keep]

        hist = prices.loc[:dt]
        if len(hist) < PEER_HORIZON + 2:
            continue
        own21 = (hist.iloc[-1] / hist.iloc[-1 - PEER_HORIZON] - 1.0)

        score = _peer_scores(block[:, finite], names, own21)
        if score.empty:
            continue
        evar = _hedgeable_fraction(block[:, finite], names)
        score = _eligible(score, evar)
        if len(score) < MIN_NAMES:
            continue

        target, held = _band_target(score, held)
        rows[dt] = target

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)


def _hedgeable_fraction(block: np.ndarray, names: list) -> pd.Series:
    """E/Var = corr(name, its top-K substitute basket)^2, in closed form.

    Transcribed from the seat. T1 computes it and does not use it, so that T1 and
    T2 differ in exactly one function (`_eligible`) and in nothing else — the
    matched-pair design #99/#100 and #96/#97 got their resolvable results from.
    """
    v = block - block.mean(axis=0)
    sd = v.std(axis=0, ddof=1)
    ok = sd > 0
    if ok.sum() <= PEER_K + 1:
        return pd.Series(dtype=float)
    v, sd = v[:, ok], sd[ok]
    cols = [n for n, keep in zip(names, ok) if keep]
    n = len(cols)

    corr = (v.T @ v) / (len(v) - 1) / np.outer(sd, sd)
    np.fill_diagonal(corr, -np.inf)
    top = np.argpartition(-corr, PEER_K - 1, axis=1)[:, :PEER_K]
    sel = np.zeros((n, n))
    sel[np.arange(n)[:, None], top] = 1.0 / PEER_K
    baskets = v @ sel.T
    b_sd = baskets.std(axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        rho = (v * baskets).sum(axis=0) / (len(v) - 1) / (sd * b_sd)
    return pd.Series(np.square(np.clip(rho, -1.0, 1.0)), index=cols).replace(
        [np.inf, -np.inf], np.nan
    ).dropna()
