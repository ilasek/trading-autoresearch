"""THE PAIRED CONTROL FOR `pl_filter_deconcentrate_3leg` -- the same book with the
composite FILTER removed and nothing else changed.

WHY THIS FILE EXISTS, AND IT IS THE POINT OF THE PAIR RATHER THAN A SECOND GUESS.
Research `#513`'s claim is about a COMBINATION OPERATOR: filter each lead's broad
selection by the composite rank of the OTHER leads, then deconcentrate. An operator can
only be measured against the same book without it. This file is `pl_filter_deconcentrate_3leg`
with exactly one operator changed:

    filtered arm   top 150 on the leg's own score  ->  the 90 with the BEST composite
                                                       rank across the other two legs
    this arm       the 90 deepest on the leg's own score

Everything else is byte-identical in intent and shares the same imported leg scores:
the same three legs (long-horizon reversal, 12-1 momentum, split-guarded 5/45 volume
shock, all from `strategies/lib/lead_scores.py`), the same 90 names per leg, the same
(trailing-trading-calendar peer group x instrument type) quota, the same equal weights
within a leg, the same equal allocation across legs, the same monthly schedule, the same
warm-up rule. **The difference between the two arms' validation skill is the value of the
filter nonlinearity and nothing else.**

WHAT THIS ARM IS IN ITS OWN RIGHT. It is the MIX -- three independently-selected
long-only sleeves blended at equal allocation -- which is the construction research
`#517` says wins at LOW active risk and loses at high, with the crossover unsettled in
either direction. It is also the arm both of the folder's ensemble-killing bounds apply
to: Breiman's simplex bound binds on any reweighting of finished long-only books, and an
equal-allocation mix of three sleeves is such a reweighting. So this arm is predicted by
those bounds to be at best the average of its legs, and two of its three legs are
measured nulls here. **That prediction is itself testable and is the second thing the
pair measures**: if this arm lands near the average of its legs' recorded skills and the
filtered arm does not, the bound held and the nonlinearity is where the value is; if
both land in the same place, the operator is worth nothing on this panel and research
`#513` is closed for this lab.

NO NEW SCREEN WAS RUN FOR THIS FILE and none was needed: the free screens in the
filtered arm's docstring were computed on BOTH arms' holdings at once (that is what
`#514`'s screen is -- a comparison of the two arms), and the D2 refusal test it reports
(per-leg Jaccard 0.425) is a statement about the pair. No train skill, IC or signal
statistic was computed for either arm, per the 2026-11-22 rule.

PRE-REGISTERED TURNOVER: strictly fewer boundary crossings than the filtered arm,
because this arm's membership moves only when a leg's OWN ordering moves while the
filtered arm's moves when any of the three do. Registered before the trial at
**train 2.0-6.0x, validation 3.0-10.0x** (the filtered arm: 2.5-7.0x / 3.5-12.0x). The
fast leg still carries the bill: `exit`-from-top-180 is 47.1% for the volume shock
against 0.3% and 3.2% for the two slow legs, and the 2026-11-22 predictor puts that leg
alone at ~14.7x train.

WHAT ARGUES AGAINST THE BOOK.
 (i) It is a mix of three sleeves, two of which are measured nulls, and Breiman's bound
     says a mix cannot beat its best member. The honest expected value of this arm on its
     own is the average of +0.124, a null, and +0.031 -- i.e. near zero -- and it is run
     as a CONTROL, not as a candidate for the board.
 (ii) Its book is LARGER than the filtered arm's (202 names against 142 at the same 90
     per leg, measured on train month-ends), because the filter makes the three legs
     converge. A larger book is closer to the equal-weight pool, so this arm's skill is
     mechanically compressed toward zero relative to the filtered arm's. That cuts
     against reading a small difference between the arms as the operator's value, and it
     is stated here rather than discovered afterwards.
 (iii) Requiring all three legs to be defined means requiring ~9 years of monthly returns
     (leg rev needs 108 monthly observations), so the book never holds a recently-admitted
     name. Price-history depth carries no information here (2026-11-20), so this is a
     coverage restriction rather than a tilt.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.lead_scores import leg_scores, pct_rank

FINAL = 90       # names per leg, matched to the filtered arm
LEGS = ("rev", "mom", "vshock")

STRATEGY = {
    "name": "pl_ownscore_deconcentrate_3leg",
    "family": "portfolio-learning",
    "hypothesis": (
        "Blending three legs at equal allocation, where each leg takes the 90 eligible "
        "names with the highest rank on its OWN score (long-horizon reversal, 12-1 "
        "momentum, split-guarded 5/45 volume shock), quota-allocated across "
        "(trailing-trading-calendar peer group x instrument type) cells and equal-weighted "
        "within each leg, earns validation skill over the equal-weight eligible pool no "
        "higher than the average of its three legs' individually recorded skills, because "
        "an equal-allocation mix of finished long-only sleeves is a reweighting of long-only "
        "books and Breiman's simplex bound binds on exactly that -- which makes this arm the "
        "control that prices the filter nonlinearity in `pl_filter_deconcentrate_3leg`."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Three legs, each selected on its own score alone; equal weights within a leg,
    equal allocation across legs, monthly. The filtered arm's twin, one operator apart.
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

        # Identical population rule to the filtered arm: rank every leg on exactly the
        # names every leg can score, so the two arms select from the same pool.
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
