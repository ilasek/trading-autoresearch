"""PRICING THE GUARD -- the one node of the board's only null-gate-clearing object that
nobody measured, and the arithmetic says it cannot do the job it was written for.

WHAT IS BEING MEASURED. `lv_volume_shock_gkm_band` (#32) is the only object in 36 recorded
v3 trials to clear the region- and type-matched random-selection null (p = 0.010, 99th
percentile), and the record treats that reading as evidence about the high-volume return
premium. One node of it is a "causal split guard": drop any name whose daily |log share
volume change| exceeds log(3) anywhere in the 50-day scoring window. Its own file reports
that guard as costing **0.57%** of eligible printing days -- i.e. as hygiene. This file is
#32 with that guard REMOVED and every other node byte-identical in intent: the same 5/45
log-volume shock, the same K = 100, the same BAND = 200, the same (trailing-trading-calendar
peer group x instrument TYPE) quota, the same monthly schedule, the same warm-up, the same
equal weighting. **The difference between the two arms is the guard and nothing else.**

WHY THE GUARD HAS TO BE PRICED -- THREE MEASUREMENTS AND ONE PIECE OF ARITHMETIC, ALL FREE,
ALL ON TRAIN, ALL TAKEN BEFORE THIS FILE WAS WRITTEN.

 (1) **The quoted cost is the wrong threshold's cost.** Over 2,545,241 eligible printing
     day-names, the share with |d log V| above log(3) is **2.34%**, not 0.57%; 0.57% is the
     rate at log(5), and 0.15% at log(10). The guard is a rolling 50-day MAXIMUM, so the
     per-day rate compounds: 1-(1-0.0234)^50 = 69% of names would be dropped if the
     exceedances were independent.

 (2) **Measured, it removes 55.3% of the eligible panel** -- 34.1% scorable in 1997-2002,
     47.1% in 2003-2008, 50.1% in 2009-2017, against 99.7% for the raw 5/45 shock. So #32
     selected its 100 names from about half the panel, and the half it kept was selected on
     VOLUME STABILITY: a name that ever tripled its daily volume inside 50 days is excluded,
     and an earnings day does that routinely. That is a cross-sectional screen, not hygiene.

 (3) **It moves three quarters of the book.** The two scores' top-100 sets overlap at
     Jaccard **0.274** over 215 common train month-ends. A node that changes 73% of the
     holdings is a first-order operator in the construction.

 (4) **And it cannot catch the split it was written for.** The contaminant is the as-of-fetch
     back-adjustment factor `D_i(t)`, the product of every distribution factor after `t`;
     `learnings.md` records that volume carries the split half of it (which is why it cancels
     in `dollar_volume = close x volume`). A window spanning a split therefore carries a STEP
     equal to the split ratio -- **log(2) = 0.693 for a 2:1 split, which is the modal split
     and sits BELOW the guard's log(3) = 1.099 threshold.** The guard fires only on ratios of
     3 or more. So its D1 benefit is confined to a rare subset of splits while its cost is a
     55% universe selection, and removing it is D1-NEUTRAL rather than a D1 regression. That
     is the argument this trial rests on, and it is arithmetic, not a forecast.

WHAT THE TWO POSSIBLE OUTCOMES MEAN, WRITTEN BEFORE THE RUN. If this arm clears the null
gate as #32 did, the high-volume premium reading survives on the whole panel and the guard
was costing coverage for nothing. **If it does not, then #32's 99th-percentile reading was
substantially its guard's selection rather than its score's** -- because `random_null_v3`
draws replicas from the full region- and type-matched eligible pool, never from a
candidate's own guarded sub-panel, so any selection the guard performs is scored as the
candidate's selection term. That second outcome would put a rider on the record's single
most-quoted v3 result, and it is the reason this trial is worth more than another score.

WHAT ARGUES AGAINST THE BOOK.
 (i) It is a construction node, not a new bet: by the breadth mandate's own standard
     (2026-11-22: check the ACTIVE-return rho, not the label) this book will correlate highly
     with #32 and adds no mechanism. It is bought for the rider it can place on a recorded
     result, not for the board.
 (ii) The guard's removal admits the residual split step on roughly 0.6% of name-dates at
     ratios of 3 or more, and splits follow price run-ups, so the residual contaminant is
     SIGNED toward past winners. That is a real cost of this arm and the reason the guard
     existed; point (4) is the claim that it was mispriced, not that it was pointless.
 (iii) The same cost corner as #32 and tonight's `rv_range_shock_band`: on this panel the
     clean corner of the event-shock space and the cheap corner of the cost model do not
     overlap, and a near-zero-persistence score has no cheaper construction (the band is
     inert below phi ~0.97, holding longer dilutes a 1-4 week premium proportionally).

PRE-REGISTERED BEFORE THE RUN. Train exit-from-top-200 is **45.8%** unguarded against 25.6%
guarded, so the 2026-11-22 predictor puts train churn at **14.3x** against #32's charged
9.0x; registered **11-18x train, 20-36x validation**. Month-to-month rank persistence phi
**-0.025** (guarded: -0.022), so this is the lab's third fast object and the band is carried
only to match #32. Expected bill 0.17-0.35 of Sharpe at the 10-19 bps per 1x the record
brackets, so as with tonight's first trial **the statistic that tests the claim is the null
PERCENTILE and the gross skill, not net skill.**

NO TRAIN SIGNAL STATISTIC was computed for this file. Every number above is a coverage
count, a jump rate, a holdings-overlap Jaccard, a rank persistence or a churn prediction --
arithmetic grounds only, per the 2026-11-22 rule.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5            # printing days of recent volume
SLOW = 45           # printing days of baseline, ending FAST+1 days ago

STRATEGY = {
    "name": "lv_volume_shock_unguarded",
    "family": "liquidity-volume",
    "hypothesis": (
        "Holding the 100 eligible names with the highest 5/45 log share-volume shock -- "
        "identical to lv_volume_shock_gkm_band in every node except that the log(3) "
        "rolling-50-day volume-jump guard is removed -- clears the 90% quantile of its "
        "region- and type-matched random-selection null as that book did, because the guard "
        "cannot catch the contaminant it was written for (a 2:1 split, the modal split, "
        "steps the series by log(2) = 0.693, below the guard's log(3) = 1.099 threshold) "
        "while measurably removing 55.3% of the eligible panel on ordinary earnings-day "
        "volume spikes and changing 73% of the holdings; if instead the null clearance does "
        "NOT survive the guard's removal, then that book's 99th-percentile reading was "
        "substantially its guard's volume-stability selection and not the volume shock's, "
        "because the null draws replicas from the full eligible pool and never from a "
        "candidate's own sub-panel."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """High short-window volume shock, UNGUARDED, quota'd across (calendar peer group x
    instrument type), monthly with a retention band. #32 with one node removed.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    fast = lv.rolling(FAST, min_periods=3).mean()
    slow = lv.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow          # no guard: that is the operator under test

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        score = shock.loc[date].reindex(names).dropna()
        if len(score) < 60:
            # Warm-up: hold the pool rather than cash (2026-10-15/16).
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()
        cells = (groups.reindex(score.index).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in score.index],
                             index=score.index))

        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, cells.reindex(rest.index).dropna(), K - len(keep))
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
