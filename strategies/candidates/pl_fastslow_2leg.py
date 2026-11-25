"""THE SUBTRACTION LAST NIGHT'S F3 ASKED FOR, RUN THE OTHER WAY -- drop the leg that
paid nothing and keep the two that paid, at matched size and matched construction.

WHY THIS FILE EXISTS. The 2026-11-24 session measured two things that only make sense
together. (a) `pl_ownscore_deconcentrate_3leg` (#35) -- a plain equal-allocation mix of
three independently-selected 90-name sleeves (long-horizon reversal, 12-1 momentum,
split-guarded 5/45 volume shock) -- scored validation skill +0.064, which is to inside any
error bar the AVERAGE of its three legs' individually recorded v3 skills (+0.124, a null,
+0.031 -> ~+0.05). (b) The night's F1 showed that the momentum leg is nearly ORTHOGONAL in
rank to the reversal leg on this panel at these windows (mean rank of one leg's selection
on the other: +0.500 to +0.529, i.e. the median), so it is not offsetting anything -- it is
simply a third of the book's allocation in a measured null.

If (a) is the right reading of the mix, then removing the null leg and splitting its
allocation between the two legs that are not nulls must raise the average, and the
prediction is arithmetic rather than hopeful:

    mean(+0.124, +0.031) = +0.078   against #35's measured +0.064

THAT IS THE HYPOTHESIS, AND IT IS FALSIFIABLE IN BOTH DIRECTIONS. If this book lands near
+0.078 the "a mix pays the average of its legs" reading of 2026-11-24 F2 survives a second,
independent test and becomes usable for planning: a mix's expected skill is computable from
its legs' records before it is built. If it lands at or below #35's +0.064, the reading is
refuted in its own family -- the mix's skill is not the average of its legs, and whatever
#35 earned was not attributable leg by leg.

ONE OPERATOR FROM #35 AND NOTHING ELSE. Same two surviving leg scores, imported
byte-identically from `strategies/lib/lead_scores.py`; same 90 names per leg; same
(trailing-trading-calendar peer group x instrument TYPE) quota; same equal weights inside a
leg; same equal allocation across legs; same monthly schedule; same population rule (every
leg is ranked on exactly the names every leg can score, so the arms select from the same
pool); same warm-up. The only change is that `LEGS` has two members instead of three.

WHAT ARGUES AGAINST THE BOOK.
 (i) Breiman's simplex bound still binds: an equal-allocation mix of finished long-only
     sleeves cannot beat its best member (+0.124), so the ceiling here is the board lead
     and this book cannot be a route to the seat. It is a measurement of an operator.
 (ii) Dropping a leg makes the book SMALLER -- 2 x 90 selections instead of 3 x 90 -- and a
     smaller book is further from the equal-weight pool, so its skill is mechanically less
     compressed toward zero than #35's. That cuts the same way as the +0.078 prediction and
     is stated here rather than discovered afterwards: a positive difference from #35 is
     consistent with both the arithmetic and the book-size change, and the two cannot be
     separated in one pair. The direction this does NOT confound is the refutation: if the
     skill falls, neither channel explains it.
 (iii) 2026-11-24 F2 also measured that the 100th-percentile null clearance of #35 came
     mostly from its FAST leg, and that an independent-selection mix buys gate clearance
     without buying skill. This book keeps the fast leg and should therefore keep the gate
     clearance; that half is a replication, not a new claim.
 (iv) Both surviving legs are coverage-restricted and the restriction is worse than the
     record says. Measured free on train tonight, as a share of eligible names: the
     long-horizon reversal is scorable on 59.6% (16.3% in 1997-2002, 81.3% in 2009-2017,
     because it needs 108 monthly observations) and the split-guarded volume shock on only
     **44.7%** -- the guard removes 55.3% of the panel, not the 0.57% its own file reports,
     because that figure is a share of DAYS and the guard is a rolling 50-day maximum. So
     this book, like #35, selects from the intersection of two thin panels. That is a
     coverage statement and not a tilt (price-history depth carries no signal here,
     2026-11-20), but it bounds what any mix of these two legs can be.

PRE-REGISTERED TURNOVER, WRITTEN BEFORE THE RUN: **train 3.5-7.0x** one-way (the charged
figures are 1.0x for the reversal leg alone and 9.0x for the volume shock alone, so an
equal-allocation pair sits near 5x), **validation 7-18x**. The 2026-11-24 entry put the
validation multiplier above 2x for any book carrying a near-zero-persistence leg; tonight's
`rv_range_shock_band` ran at 1.65x on a book that is ENTIRELY such a leg, so that claim is
already under question and this book is a second reading of it.

NO TRAIN SIGNAL STATISTIC was computed for this file, in either direction. The screens
quoted above are a coverage count, a rank-correlation relabelling test and a churn
prediction -- the three arithmetic grounds the 2026-11-22 rule permits.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.lead_scores import leg_scores, pct_rank

FINAL = 90                      # names per leg, matched to #34/#35
LEGS = ("rev", "vshock")        # the one change from #35: no momentum leg

STRATEGY = {
    "name": "pl_fastslow_2leg",
    "family": "portfolio-learning",
    "hypothesis": (
        "Blending two legs at equal allocation -- the 90 eligible names deepest on the "
        "board lead's long-horizon reversal score and the 90 deepest on the split-guarded "
        "5/45 volume shock, quota-allocated across (trailing-trading-calendar peer group x "
        "instrument type) cells and equal-weighted within each leg, monthly -- earns "
        "validation skill over the equal-weight eligible pool of about +0.078, the average "
        "of those two legs' individually recorded v3 skills (+0.124 and +0.031) and ABOVE "
        "the +0.064 the same construction scored with a third, measured-null momentum leg "
        "taking a third of the allocation, because 2026-11-24 F2 measured that a mix of "
        "independently-selected sleeves pays the average of its legs and nothing more -- so "
        "removing a null leg must raise that average, and a reading at or below +0.064 "
        "refutes the averaging rule in the family it was measured in."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Two legs, each selected on its own score alone; equal weights within a leg, equal
    allocation across legs, monthly. #35 with the momentum leg removed.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    scores = leg_scores(prices, volume)

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Identical population rule to #34/#35: rank every leg on exactly the names every
        # leg can score, so the arms select from the same pool.
        raw = {leg: scores[leg].loc[date].reindex(names).dropna() for leg in LEGS}
        idx = raw[LEGS[0]].index
        for leg in LEGS[1:]:
            idx = idx.intersection(raw[leg].index)
        if len(idx) < 200:
            if not rows:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, idx).dropna()
        if len(groups) < 100:
            continue
        idx = idx.intersection(groups.index)
        if len(idx) < 200:
            continue
        rank = {leg: pct_rank(raw[leg].reindex(idx)) for leg in LEGS}
        cells = (groups.reindex(idx).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in idx], index=idx))

        book = pd.Series(0.0, index=prices.columns, dtype=float)
        legs_filled = 0
        for leg in LEGS:
            own = rank[leg].dropna()
            if len(own) < 40:
                continue
            picked = peer_quota_select(own, cells.reindex(own.index), FINAL)
            if len(picked) < 20:
                continue
            book = book.add(pd.Series(1.0 / len(picked), index=picked)
                            .reindex(prices.columns).fillna(0.0), fill_value=0.0)
            legs_filled += 1

        if legs_filled == 0:
            continue
        total = float(book.sum())
        if total <= 0:
            continue
        rows[date] = book[book > 1e-12] / total

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
