"""IS THE INTERIOR OPTIMUM AN ALLOCATION OR A LEG COUNT? -- the one cell of the grid the three
recorded mixes bracket but none occupies.

WHAT 2026-11-25's F5 MEASURED, AND THE AMBIGUITY IT LEFT. Three recorded books, with GROSS
skill taken as net skill plus the skill-minus-2x-cost bill:

    book                          legs  fast share   net skill   bill    GROSS skill
    #36 rev + mom + lowvol          3        0          -0.003   0.059      +0.056
    #35 rev + mom + vshock          3       1/3         +0.064   0.135      +0.199
    #39 rev + vshock                2       1/2         +0.061   0.153      +0.214

Marginal gross per unit of bill is **1.9** from 0 to a third and **0.83** from a third to a
half, which is where the "interior optimum near a third" reading comes from. But the fast share
and the LEG COUNT move together across those three books: every 1/3 cell has three legs and
every 1/2 cell has two. So two different mechanisms fit the same numbers:
 (a) an ALLOCATION effect -- a third of the book in the fast leg is the efficient share, and
     the leg count is incidental; or
 (b) a LEG-COUNT effect -- three legs dilute the fast leg's churn better than two do (the slow
     legs' low train churn is the denominator, which is the 2026-11-25 reading of the >2x
     validation multiplier), and the fast share is incidental.
**This file is the missing cell: two legs at a one-third fast share.** It differs from `#39` in
exactly one node -- the allocation vector, (1/2, 1/2) -> (2/3 rev, 1/3 vshock) -- and from `#35`
in exactly one node, the presence of the momentum leg. So:

    (this file - #39) at fixed leg set and construction  =  the ALLOCATION effect
    (this file - #35) at fixed fast share                =  the LEG-COUNT effect

and the two readings are separated for the first time. The legs, `FINAL = 90` names each, the
(trailing-trading-calendar peer group x instrument type) quota, the common-population rule, the
monthly grid and the within-leg equal weighting are byte-identical to `#39`.

WHY THE COMPLEMENTARY ARM IS NOT RUN. The natural fourth cell is the fast-share-zero point for
this leg set -- the reversal leg alone in this construction. It is REFUSED under tonight's
pre-registered decision rule on **D2**: `leg_scores.reversal_score` is the board lead's own
score, so a single-leg book on it has score-level rank correlation **1.000** to a recorded
object, which is the relabelling bar whatever its holdings do. `#36` is the recorded
fast-share-zero point and is used as such, with its different slow legs stated as the caveat.

PRE-REGISTERED PREDICTIONS, written before the run.
 - BILL: **0.10 to 0.14**, from linear interpolation between `#36` (0.059 at fast share 0) and
   `#39` (0.153 at 1/2); `#35` landed at 0.135 at this share with three legs.
 - GROSS skill: **+0.15 to +0.21**, interpolating the same two anchors (+0.161) with `#35`'s
   +0.199 at this share as the upper end.
 - NET skill: **+0.05 to +0.10**. The reading that decides between (a) and (b): a net skill
   **above `#39`'s +0.061 and `#35`'s +0.064** supports the ALLOCATION reading and confirms the
   interior optimum; a net skill **at or below both** supports the LEG-COUNT reading and says
   F5's optimum was an artefact of three legs being cheaper than two, not of a third being the
   right share.
 - A third outcome is live and is named here so it cannot be claimed as a prediction
   afterwards: all three cells inside 0.02 of each other, which would say the allocation surface
   is FLAT between a third and a half and that F5's 1.9-versus-0.83 marginal ratio was reading
   noise in the bill rather than a curve. Given the board's skill intervals are about +-0.17
   wide this is the most likely outcome of the three, and it would be reported as such.
 - CHURN: train **4-8x**, validation **9-18x**. `#39` was charged 5.3x / 13.6x at a 1/2 fast
   share and `#35` 5.3x / 13.6x-ish at 1/3 with three legs; a 2/3 weight on the slowest leg on
   this board (phi +0.980, 1.0x/1.3x standalone) should pull the train figure down.
 - NULL PERCENTILE: **100%**, as both `#35` and `#39` recorded. Per tonight's correction entry
   the percentile is near-exactly a monotone transform of the SELECTION term and is not a test
   of skill over the pool, so it is reported here as a gate and not as a result.
 - TRAIN SKILL stays negative (`#35` -0.140, `#39` -0.140), so this is a GATE_FAIL whatever
   happens. The verdict is not the result.
 - REFUSAL, pre-committed: no third allocation is tried. One interior point either confirms the
   curve, refutes it, or shows the surface flat, and all three close the axis.

WHAT ARGUES AGAINST THE BOOK.
 (i) `#36` is an imperfect fast-share-zero anchor: its slow legs are rev + mom + lowvol, not
     rev alone, and lowvol is a measured null on this panel. Both interpolations above inherit
     that, so the bill and gross predictions are softer than their ranges suggest.
 (ii) An allocation is the closest thing to a knob this file could be, and the record is
     explicit that knob sweeps waste shared budget. The defence is that this is the single
     interior point that separates two stated mechanisms, the refusal above forbids a second,
     and the prediction is signed in both directions.
 (iii) The fast leg is `#32`'s volume shock, whose gross is ~86% its own cost bill and whose
     premium `research/#506` localises toward smaller names than this panel holds. Nothing
     about reallocating it fixes either limit.
 (iv) 2026-11-25 already refuted the idea that a mix's skill is computable from its legs'
     records (`#39` was registered at +0.078 and scored +0.061), so the interpolations here are
     stated as interpolations of the three recorded MIXES, not of their legs.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.lead_scores import leg_scores, pct_rank

FINAL = 90                              # names per leg, matched to #34/#35/#39
LEGS = ("rev", "vshock")                # the same two legs as #39
ALLOC = {"rev": 2.0 / 3.0, "vshock": 1.0 / 3.0}   # the one change from #39

STRATEGY = {
    "name": "pl_third_fast_2leg",
    "family": "portfolio-learning",
    "hypothesis": (
        "Giving the fast leg one third of a TWO-leg mix rather than one half -- the 90 eligible "
        "names deepest on the board lead's long-horizon reversal score at 2/3 of the book and "
        "the 90 deepest on the split-guarded 5/45 volume shock at 1/3, quota-allocated across "
        "(trailing-trading-calendar peer group x instrument type) cells, equal-weighted within "
        "each leg, monthly, every other node byte-identical to pl_fastslow_2leg -- earns "
        "validation skill above both the 1/2-fast two-leg book's +0.061 and the 1/3-fast "
        "THREE-leg book's +0.064, because 2026-11-25 measured marginal gross per unit of cost "
        "bill at 1.9 below a third and 0.83 above it and this is the one cell that separates "
        "that ALLOCATION reading from the alternative that three legs simply dilute a fast "
        "leg's churn better than two; a reading at or below both instead attributes the "
        "apparent optimum to the leg count, and all three cells within 0.02 says the surface "
        "is flat and the marginal ratio was noise in the bill."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Two legs, each selected on its own score alone; equal weights within a leg, 2/3 of the
    book to the slow leg and 1/3 to the fast one, monthly. #39 with one node changed: the
    allocation vector.
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

        # Identical population rule to #34/#35/#39: rank every leg on exactly the names every
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
            book = book.add(pd.Series(ALLOC[leg] / len(picked), index=picked)
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
