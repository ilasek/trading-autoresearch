"""Peer-network momentum, acted on only where the peer relationship is estimable.

WHAT THIS FILE IS. `ll_peer_momentum` with **one function replaced** — `_eligible` —
and every other byte identical, including the neighbourhood constants, the band, the
floor, the cap and the dead-code-in-T1 `_hedgeable_fraction` that T1 computes and
discards precisely so that this file could use it without changing anything else.
That is the matched-pair design #96/#97 and #99/#100 got this repo's only resolvable
results from: the difference between the two books is the operator and nothing else.

THE OPERATOR, and it is a class this repo has never used. `research/SUMMARY.md` #150
observes that every score this lab computes is used at face value once computed, and
that nothing anywhere in the repo refuses to act on a per-name number because the
regression behind it is poorly determined. Yeo-Papanicolaou's screen is exactly that:
accept a name's signal only where the fit that produced it clears a cutoff, because a
badly-fit estimate generates trades whose costs are certain and whose edge is not.

WHY `E/Var` IS THE CORRECT CUTOFF VARIABLE HERE, AND IS NOT A KNOB ON THE SEAT.
`E/Var` *is* the `R^2` of a name against its four most-correlated substitutes — that
is its definition, not an analogy. So the `E/Var` of the very neighbourhood that
produced `peer_ret` is literally #150's "the `R^2` of the regression behind the
score", and the gate reads: **act on a peer signal only where the peers actually span
the name.** No `E/Var` constant is altered; `K`, the window and the lag are the seat's
and are chosen nowhere. The standing anti-candidate forbids choosing an `E/Var` knob,
and reusing the variable unchanged in a different role is the one use of it that
anti-candidate does not reach.

`eta` = the **cross-sectional median of `E/Var` on that date**, fixed in the journal's
pre-registration addendum before any curve existed, per #150's own instruction. A
cutoff chosen after seeing the curve is a fitted parameter; no curve was computed.

THE SIGN IS OPPOSITE TO THE SEAT'S AND THAT IS THE POINT. The champion scores
**`-E/Var`**: hold names the universe *cannot* replicate, a variance argument
(`learnings.md` 2026-09-23). This file gates on **high `E/Var`**: trust a peer signal
where the peers *do* span the name, an estimability argument. Same variable, opposite
direction, different reason — and the pair can falsify it. If T2 beats T1 the operator
is estimability. **If T2 loses, the honest first reading is that the seat's variance
channel is reasserting itself against the gate's own direction**, and the reversed
gate becomes the free next test rather than a new idea. Both readings were written in
the journal before either book was scored.

WHAT IT COSTS BY CONSTRUCTION. A median gate halves the eligible cross-section
(F6 measured a mean of 81.4 scoreable names per train month-end, so roughly 40 remain
against a 15-name core and a 25-name band). This repo's de-concentration price is
real and measured inside `price-trend` (~0.05 Sharpe per 30% of HHI) and `CLAUDE.md`
forbids carrying that constant into another family by analogy — so it is named here as
a mechanism and explicitly **not** priced.

PRE-REGISTERED: within **+-0.10 of T1**, for the breadth reason above. **No drawdown
call: F4 retired the diversification ratio as a drawdown predictor tonight**, on its
first test and by its own pre-registration.

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
    "name": "ll_peer_momentum_evargate",
    "family": "lead-lag-spillover",
    "track": "scout",
    "hypothesis": (
        "Restricting ll_peer_momentum's scoreable cross-section to the names whose E/Var — "
        "the hedgeable fraction against their own four most-correlated peers, i.e. the R^2 "
        "of the very regression that defines the peer neighbourhood — is at or above its "
        "cross-sectional median on that date, with every other byte of that file identical, "
        "moves validation Sharpe within +-0.10 of it, because SUMMARY.md #150's operator "
        "class says a signal should not be acted on where the regression behind it is poorly "
        "determined and a peer-transmission signal is exactly a signal whose premise is that "
        "the peers span the name. eta is the median, fixed in the journal before any curve "
        "existed. The gate's direction is the OPPOSITE of the seated champion's use of the "
        "same variable — the seat scores -E/Var to hold names the universe cannot replicate, "
        "a variance argument, while this gates on high E/Var to trust a signal where the "
        "peers do span the name, an estimability argument — so the pair separates the two "
        "readings: above T1 says estimate quality is a usable operator on this universe and "
        "the class generalises past this family, below T1 says the seat's variance channel "
        "dominates the estimability channel on the same variable and the reversed gate is "
        "the next free test rather than a new idea."
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
    """THE ONE NODE THIS FILE CHANGES. Keep only names whose peer neighbourhood
    actually spans them: `E/Var` at or above its own cross-sectional median on this
    date. `eta` is the median, fixed in the journal's pre-registration addendum
    before any curve existed, per `SUMMARY.md` #150.

    The median is taken over the names that are *scoreable on this date*, not over
    the whole universe, so the gate is a true half-split of the pool T1 holds from
    rather than a level threshold that drifts with universe composition."""
    common = score.index.intersection(evar.index)
    if len(common) == 0:
        return pd.Series(dtype=float)
    e = evar.reindex(common)
    eta = e.median()
    return score.reindex(common)[e >= eta]


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
