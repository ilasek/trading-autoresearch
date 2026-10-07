"""The v2 panel's first recorded trial: short-horizon residual reversal.

WHY THIS IS THE FIRST THING TO MEASURE UNDER PROTOCOL v2. The lab has 104 v1
trials and zero v2 trials. Every constant in `experiments/learnings.md` was
measured on 140 survivors, the v1 champion scores 0.19 on the point-in-time
panel, and the v1-vs-v2 rank agreement across all 104 trials is +0.43. So the
board is empty and the first job is to find out which mechanism, if any, has
content on ~960 point-in-time names rather than on today's winners.

WHAT THE FREE SCREEN SAID (train split 1997-01-01..2017-12-31, 251 month-ends,
cross-sectional Spearman of nine causal scores against the forward 21-day
return, no portfolio formed and no returns scored; written up in the journal
under "Free measurements — 2026-10-07"):

    score         IC        t        rank-corr to this file's score
    rev1m      +0.0282   +3.07       1.00
    mom12_1    +0.0128   +0.96       0.02
    lowidio    +0.0088   +0.78       0.02
    consistency+0.0043   +0.41      -0.18
    volshock   +0.0012   +0.21      -0.04
    size_dv    -0.0021   -0.25       0.02
    lowvol_pk  -0.0028   -0.20       0.01
    seas       -0.0142   -2.01      -0.03

Residual reversal is the only score of the nine that clears |t| = 2 with the
sign its mechanism predicts, it is the largest in magnitude by a factor of two,
and it is decorrelated from every other score on the list (|rho| <= 0.18). The
screen is also the reason this file is not a momentum file: 12-1 momentum --
the mechanism that produced all seven v1 promotions -- reads +0.0128 at t =
+0.96 on the point-in-time panel, statistically indistinguishable from the
+0.0102 / t = +0.97 the same screen gave it on the v1 universe.

WHAT THE SCREEN DOES **NOT** LICENSE, STATED BEFORE THE TRIAL. `learnings.md`
[2026-08-30] records exactly this trap from the other direction: a plain 21-day
reversal book scored 0.701 validation under v1 while its train IC was a null
(+0.0102, t = +0.97), "because the book buys the extreme tail, not the quintile
mean". An IC is a statement about the whole cross-section and a book is a
statement about its tail, so the ordering above is weak evidence about book
Sharpes and strong evidence about *decorrelation*. The IC is the reason this
file is tested; it is not a prediction of what it will score.

CONSTRUCTION, AND WHY EACH CHOICE IS THE PLAIN ONE. Equal weight, because
`learnings.md` [2026-09-08] says a rank-slice screen prices an equal-weight book
and this trial's job is to price the mechanism, not a weighting scheme. K = 30,
because the random-selection null's 90% quantile is flat in book size on train
(0.566 at K=10, 0.570 at 20, 0.585 at 30, 0.565 at 50, 0.603 at 100, 0.636 at
200 -- measured, journal F1), so K buys nothing against the gate and 30 is the
diversification the drawdown gate wants: v1 reversal books ran -38% on
validation against a -45% gate. Monthly rebalance, no skip -- the engine's
one-day execution lag is the microstructure protection, and a skip would be a
different mechanism. The market leg is the equal-weight mean of the *eligible*
names only, so the residual is taken against the pool the book can actually buy.

FALSIFIER. If this lands below the random-selection null's 90% quantile, the
strongest screened score on the v2 panel does not survive 15 bps a side at
monthly turnover, and the honest reading is that the point-in-time panel has no
cheap cross-sectional reversal premium -- not that the book was built wrong.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "pt_resid_reversal_v2",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "A long-only equal-weight book of the 30 eligible names with the most "
        "negative 21-day return measured against the equal-weight eligible "
        "pool, re-formed monthly, beats the 90% quantile of the "
        "survivorship-matched random-selection null on validation net of 15 "
        "bps a side, because the one score of nine that clears |t| = 2 on the "
        "train-split forward-return screen on the point-in-time panel is "
        "residual reversal (+0.0282, t = +3.07) and it is decorrelated from "
        "every other screened score (|rho| <= 0.18), including the 12-1 "
        "momentum that produced all seven v1 promotions and that the same "
        "screen reads as a null here (+0.0128, t = +0.96); landing at or below "
        "the null's 90% quantile falsifies the claim that the point-in-time "
        "panel carries a cross-sectional reversal premium net of costs."
    ),
}

HORIZON = 21
TOP_N = 30
MIN_NAMES = 50


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)

    # 21-day simple return ending at each row; NaN where either endpoint is missing.
    past = prices.shift(HORIZON)
    horizon_return = prices / past - 1.0

    rows = {}
    for dt in rebalance_dates:
        if dt not in horizon_return.index:
            continue
        r = horizon_return.loc[dt]
        ok = elig.loc[dt].to_numpy() & r.notna().to_numpy()
        if ok.sum() < MIN_NAMES:
            continue
        r = r[ok]
        score = -(r - r.mean())          # revert the move against the eligible pool
        picked = score.nlargest(min(TOP_N, len(score))).index
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
