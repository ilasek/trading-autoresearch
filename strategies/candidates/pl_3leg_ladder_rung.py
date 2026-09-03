"""The missing rung: is the union book's 1-leg -> 4-leg gap a threshold in leg
count, or is it noise?

WHY THIS FILE EXISTS. The whole `portfolio-learning` story rests on one number.
Trial #71 (four legs, fixed quota) scored validation 0.958; trial #72 (the same
machinery running the strongest leg alone) scored 0.782. Gap +0.175, `rho`
0.9119, closed-form paired SE 0.169, **t = +1.04**. Everything the lab has said
about union books is an interpretation of that single gap.

The 2026-09-02 session tested the obvious reading of it — that each added leg
buys about +0.175/3 — and **refuted it**. Three two-leg books, each `seasonal`
plus one partner, matched holdings-only on breadth, churn, warmup and joint pool,
varying only what the partner is:

    arm  partner    partner's own tail        d vs #72    SE      t     train   val
    A    reversal   +2.31%/yr (t=+1.29)         +0.004   0.1373  +0.03   0.806  0.786
    B    suv        +0.09%/yr (t=+0.08)         +0.131   0.1360  +0.96   0.810  0.913
    C    placebo    zero by construction        +0.017   0.1139  +0.15   0.834  0.799

Arm C's partner is a hash of the rebalance date and the ticker and reads no
market data at all. Not one arm is distinguishable from the single-leg baseline,
the entire spread across all three partners (0.127) sits inside one paired SE,
and the coin flip won the longer split. **The first added leg buys nothing
measurable, whatever it is.**

That leaves exactly two live accounts of the +0.175, and they are the reason for
this file:

  * **Threshold.** The gap is real but is not delivered per leg — a union needs
    enough legs before the union-of-tails does anything, and two is not enough.
    Then three legs should sit near the 2-leg cluster (~0.83) and four is where
    it appears.
  * **Noise.** There is no leg-count effect; #71 and #72 are one draw apart at
    t = +1.04 and the 2-leg triple is what that looks like from inside. Then
    three legs lands anywhere in the band and the family's four-leg advantage
    should be recorded as **unreproduced**.

Three legs is the only rung never measured, and it is the only one whose
predicted effect is not already inside the resolution floor.

WHICH THREE LEGS, AND WHY THE CHOICE IS NOT A FREE PARAMETER. The 2-leg triple
established that partner identity is not resolvable here (spread 0.127 against
SE ~0.13, with the placebo winning on train), which licenses one a-priori subset
rather than all three. The subset is then fixed by the standing matching rule —
a scout that changes selection and turnover at once cannot answer a mechanism
question — and measured holdings-only on train BEFORE this file was written:

    rung                                    months  first        positions  turnover
    1  seasonal                               350   1988-11-30      24.70    11.72x
    2  seasonal+illiq                         350   1988-11-30      21.52     7.54x
    2  seasonal+group_lead                    253   1996-12-31      20.77    15.11x
    2  seasonal+reversal        (arm A)       350   1988-11-30      20.63    13.04x
    3  seasonal+illiq+group_lead  <- THIS     253   1996-12-31      19.68    10.59x
    3  seasonal+illiq+reversal                350   1988-11-30      19.26     9.25x
    3  seasonal+group_lead+reversal           253   1996-12-31      19.33    14.35x
    4  seasonal+illiq+group_lead+reversal     253   1996-12-31      20.10    11.98x

`seasonal+illiq+group_lead` is the only 3-leg subset that reproduces the 4-leg
rung's **exact month window** (253 months from 1996-12-31 — `group_lead` is what
sets that start date, so any subset omitting it runs a 97-month-longer train
sample than the rung it is being compared to) and it is simultaneously the
closest of the three on turnover (10.59x against 11.98x) and on breadth (19.68
against 20.10). The comparison that matters most is 3-against-4, and this is the
subset that makes it clean.

PRE-REGISTERED POINT ESTIMATE: **0.89** — the midpoint of the two live accounts
(the 2-leg cluster at ~0.83 against #71's 0.958). It is deliberately not read off
a rate: the only per-leg rate the lab had was refuted last session, and inventing
a replacement from the same data would repeat the error.

STATED PLAINLY, BECAUSE IT DECIDES WHAT THE TRIAL IS WORTH. This rung shares its
`seasonal` and `illiq` halves with #71, so `rho` should run high and the paired
SE near 0.13-0.15 — and the two accounts are 0.128 apart, i.e. about **one** SE.
A single rung therefore cannot resolve them, and this file does not claim it
will. What it can do is put the last missing point on a four-point ladder whose
other three are already recorded, and the ladder is read as a shape rather than
as a test: 0.782 / ~0.833 / X / 0.958. If X sits at or below the 2-leg cluster,
the threshold account has nowhere left to live and the lab should **stop building
union books** — which is the decision this trial exists to inform, and it is a
decision that saves trials in every later session.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. n = 20 outside
`price-trend` and still unresolved; the streak of under-prediction broke last
session (two of three over-predicted). Recorded, not relied on.

SCOUT. It does not compete for the seat and cannot reach the holdout. The solved
required-leg-Sharpe bar for a resolvable 20% blend is 1.34-1.42 against a 1.120
champion, and the best object on this board is 0.958-1.008.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import union_legs as UL

STRATEGY = {
    "name": "pl_3leg_ladder_rung",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "A three-leg fixed-quota union book holding the union of the top 6 names of each of "
        "the same-calendar-month seasonal score, the 63-day Amihud illiquidity score and the "
        "21-day sector-median group-lead score — bit-identical to trials #71 and #73-#75 in "
        "z-scoring, joint-coverage rule, hysteresis band, equal weighting, monthly grid and "
        "warmup, and matched to the four-leg rung holdings-only in advance on month window "
        "(253 months from 1996-12-31, identical), breadth (19.68 against 20.10 names) and "
        "churn (10.59x against 11.98x annual turnover) — scores near 0.89 on validation, "
        "between the two-leg cluster's 0.786/0.799/0.913 and the four-leg 0.958, because the "
        "recorded one-leg-to-four-leg gap of +0.175 is a threshold in leg count rather than a "
        "per-leg increment; the per-leg reading was refuted last session when a placebo "
        "partner that reads no market data bought +0.017 against the single-leg baseline and "
        "the whole spread across three different partners fell inside one paired standard "
        "error. A rung at or below the two-leg cluster leaves the threshold account nowhere "
        "to live and records the four-leg advantage as unreproduced."
    ),
}


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "seasonal": SB.seasonal_score(prices),
        "illiq": SB.illiquidity_score(prices, aux["dollar_volume"], 63),
        "group_lead": SB.group_lead_score(prices, 21),
    }
    return UL.fixed_quota_union(prices, legs)
