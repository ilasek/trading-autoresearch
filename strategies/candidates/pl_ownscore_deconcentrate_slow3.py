"""THE NIGHT'S LIVE OBJECT WITH ITS FAST LEG REMOVED -- was the null clearance the BLEND,
or was it inherited from the one leg that had already cleared the null alone?

WHERE THIS COMES FROM. Tonight's paired trial settled the operator question and raised a
different one. `pl_ownscore_deconcentrate_3leg` (trial #35) -- three legs selected on their
own scores, equal-weighted within a leg, blended at equal allocation -- cleared the
region- and type-matched random-selection null at the **100th percentile** (candidate
+0.40 against a null median +0.28 and a 90% quantile +0.33), the strongest null-gate
result recorded in 34 v3 trials, with validation skill **+0.064** [90% CI -0.118, +0.218]
and an information ratio against the pool of **+0.19**. Its filtered twin (#34, research
`#513`'s operator) scored -0.026 at the 99th percentile, so the composite FILTER is worth
about **-0.09 of skill** here and is not the source of the clearance.

THE QUESTION THIS FILE ANSWERS, AND IT IS THE ONLY ONE LEFT ON THAT OBJECT. Both arms
share the split-guarded 5/45 volume-shock leg, and that leg's own parent book
(`lv_volume_shock_gkm_band`, trial #32) had ALREADY cleared the same null at the 99th
percentile by itself. So #35's clearance has exactly two candidate sources:

    (a) the THREE-LEG BLEND -- a ~220-name book assembled from three mechanically
        unrelated selections is something the matched null cannot imitate; or
    (b) the FAST LEG -- #35 inherited the clearance from the one leg already known to
        clear it alone, and the blend contributed nothing.

This file is #35 with the fast leg REPLACED by a slow one and nothing else changed. Under
(a) the clearance survives; under (b) it does not. No other trial on the board can
separate them, because no other trial holds the blend fixed while changing the leg.

THE SECOND THING IT BUYS, AND IT IS ARITHMETIC RATHER THAN A FORECAST. The fast leg is
where the whole cost bill sits. #35's skill goes from +0.064 to **-0.071 at 2x liquidity
costs**, so its bill is ~**0.135 of Sharpe** on 4.7x train / 11.8x validation one-way
churn. The 2026-11-22 predictor puts the volume shock at 14.7x train against 1.1x and 1.9x
for the two slow legs, and the same entry measures a volume shock at ~**19 bps per 1x** of
churn -- not the record's ~11 -- because it selects exactly the names the liquidity tiers
and the UK/HK/FR/IT/ES transaction taxes punish. Replacing it with a slow leg is therefore
predicted by arithmetic to take churn to ~1.4x and the bill to ~0.03.

**The handover's own named cheapening axis was declined tonight on D1, which is why this is
the cheapening axis that got the trial.** Both the 2026-11-22 and 2026-11-23 handovers put
"the volume-shock premium at matched tail depth in the cheapest cost tier" first. A
liquidity tier is a cross-sectional comparison of `dollar_volume` LEVELS, and
`learnings.md`'s standing operating rule since 2026-10-21/22 is that a candidate may use
ratios, returns and trends of the stored panels but NOT their levels -- `dollar_volume`
keeps the dividend half of the as-of-fetch back-adjustment factor, which is what accounted
for Amihud's entire measured IC here. So that axis is closed by the lab's own contamination
rule, and the reachable form of the same idea is to change the LEG, not the universe.

THE THIRD LEG, AND WHY IT IS THIS ONE. Minus trailing 126-day close-to-close volatility --
the score behind `pt_lowvol126_*` (#30/#31) and `pt_lowvol_gk_quarterly` (#1). It is a
measured NULL here and that is deliberate: the hypothesis is about the blend, and a blend
that only clears the gate when one leg already clears it alone is not a blend result. It is
slow (rank persistence +0.970, exit-from-top-180 0.4%), it is clean (a dispersion of
returns, no level anywhere), and its one known defect is already handled -- 2026-11-22's F3
finding is that a volatility-LEVEL sort is the one score family that buys ETFs (24.7% and
20.8% share in the two recorded low-volatility books against a 5.5% panel share), and the
(peer x type) quota this file carries unchanged is exactly the correction that moved that
book's selection term +0.056.

WHAT MAKES EACH VERDICT INFORMATIVE.
 - Clears the null with positive train skill: the first object in 35 v3 trials to pass both
   binding gates, and the blend is the reason.
 - Clears the null, train skill still negative: #35's clearance was (a), the blend, and it
   survives at a tenth of the cost bill -- which makes the blend the lab's first reproducible
   way past the gate that refused 22 of 24 candidates.
 - Fails the null: #35's clearance was (b), inherited from the volume-shock leg, and the
   three-leg blend is worth nothing on its own. `portfolio-learning`'s "ensembles of
   decorrelated signals" clause would then be closed on four trials rather than on analogy.

NO TRAIN SIGNAL STATISTIC WAS COMPUTED OR READ for this file. The pre-registered rule
(scratchpad `PREREG.md`, fixed before the night's first screen) permits a decline only on
arithmetic grounds, and no threshold on a train signal statistic may decline an object in
either direction (2026-11-22).

PRE-REGISTERED TURNOVER: all three legs are slow (exit-from-top-180 of 0.3%, 3.2%, 0.4%,
giving 1.1x / 1.9x / 1.1x from the 2026-11-22 predictor, leg average ~1.4x). #35 charged
4.7x train against a leg average of 5.9x, so the blend ran slightly BELOW its legs.
**Registered: train 1.1-2.5x, validation 1.5-5.5x.** The validation band is widened at the
top because tonight's two trials came in at 2.58x and 2.51x the train figure, ABOVE the
1.30-2.00x band the 2026-11-22 entry set -- recorded as a miss of that band by both arms.

WHAT ARGUES AGAINST THE BOOK.
 (i) All three legs are now slow, and 2026-11-22's finding is that a score whose rank
     persistence is near zero is decorrelated from this board almost by construction
     "because everything on the board is slow". Removing the fast leg is predicted to make
     this book CORRELATED with the board's M1/M3 clusters -- a cost in breadth even if the
     clearance survives.
 (ii) Two of three legs are measured nulls and the third's 90% interval contains zero.
     Breiman's simplex bound says a mix of finished long-only books cannot beat its best
     member, and #35 landed at +0.064 against a leg average of roughly +0.05, i.e. the bound
     held almost exactly. The honest prior for this file is therefore the average of
     +0.124, a null and a negative -- near zero, and possibly below #35.
 (iii) Low volatility and long-horizon reversal are both in the board's M1/M3 neighbourhood,
     so this book's three legs are less mechanically independent than #35's were, which is
     the opposite of the property that made #35 interesting.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.features import realized_vol
from strategies.lib.lead_scores import momentum_score, pct_rank, reversal_score

FINAL = 90       # names per leg, matched to trials #34 and #35
VOL_WINDOW = 126
LEGS = ("rev", "mom", "lowvol")

STRATEGY = {
    "name": "pl_ownscore_deconcentrate_slow3",
    "family": "portfolio-learning",
    "hypothesis": (
        "Trial #35's three-leg mix with its fast leg replaced by a slow one -- three legs "
        "(long-horizon reversal, 12-1 momentum, minus trailing 126-day volatility), each "
        "taking the 90 eligible names highest on its OWN rank, quota-allocated across "
        "(trailing-trading-calendar peer group x instrument type) cells, equal-weighted within "
        "a leg and blended at equal allocation -- still beats the 90% quantile of its own "
        "region- and type-matched random-selection null, because #35's clearance of that null "
        "at the 100th percentile was produced by assembling three mechanically unrelated "
        "selections into one book and not inherited from the volume-shock leg whose own parent "
        "book had already cleared the same null alone."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Three slow legs, each selected on its own score alone; equal weights within a leg,
    equal allocation across legs, monthly. Trial #35 with the fast leg swapped out.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    scores = {
        "rev": reversal_score(prices),
        "mom": momentum_score(prices),
        # A dispersion of returns, not a level: no stored level enters this anywhere.
        "lowvol": -realized_vol(prices, window=VOL_WINDOW),
    }

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Identical population rule to #34/#35: rank every leg on exactly the names every
        # leg can score, so the three arms select from the same pool.
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
