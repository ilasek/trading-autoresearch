"""The falling-turnover book held in six overlapping sleeves — the paired control
that measures the sleeve operator's channel on a SECOND, independent score.

WHAT THIS FILE IS. It differs from `lv_vol_trend_hold1` (trial #18) in **one
integer**: `HOLD = 6` instead of 1. Same score, same K, same quota, same
availability rule, same pruning, same warm-up, same geography. Everything said
about the score in that file stands here and is not restated; this file's
hypothesis is about the OPERATOR.

WHY IT IS WORTH A TRIAL RATHER THAN A FREE MEASUREMENT. The 2026-10-27/28
session shipped the same pair on the decade reversal (#12 hold-1 → #16
overlap/H6) and read the +0.054 validation gain as two channels: a COST term
(fewer trading events cost less money) and a VARIANCE-REDUCTION term (averaging
six correlated top-K draws), both called construction arithmetic and therefore
the first quantities in this lab's record with a claim to transfer. **Tonight's
F3 shows that only half of that is right, and the half that is wrong is the
bigger half.** Seven objects pushed through both constructions on train:

    object                       hold-1 net  overlap net   d net    d gross   d cost
    old half (#12/#16's score)     +0.0256     +0.0580    +0.0324   +0.0198  +0.0126
    decade mean (#5's score)       +0.0983     +0.0766    -0.0217   -0.0342  +0.0125
    decade return / decade risk    +0.0540     +0.0276    -0.0264   -0.0380  +0.0116
    fraction of positive months    +0.0252     +0.0159    -0.0093   -0.0211  +0.0118
    decade skewness, low           +0.0105     +0.0065    -0.0040   -0.0118  +0.0078
    volume trend down 24/36        +0.0175     +0.0241    +0.0066   -0.0031  +0.0097
    volume trend up 24/36          -0.0453     -0.0588    -0.0135   -0.0216  +0.0081

**The COST rebate is universal and tightly bounded** (+0.008 to +0.013 on all
seven, exactly as "arithmetic" predicts). **The GROSS term is object-specific
and NEGATIVE on six of seven** — including the decade mean, a 120-month window
whose content is maximally older than a six-month hold and which therefore
satisfies the stated precondition as well as any object can. So the operator's
gross half is not construction arithmetic, the precondition does not predict it,
and #16's gross gain is an exception rather than a rule.

THE HYPOTHESIS, AND IT IS ONE-SIDED ON PURPOSE. On the shipped score the two
channels nearly cancel on train (`cost +0.0096`, `gross -0.0185`, `net
-0.0089`), so this pair is the cleanest available test of the one channel with a
transfer claim. Trial #18 charged **2.1x** on validation against its own 1.81x
on train; this book charges 1.07x on train, so its validation churn should land
near 1.25x and the cost gap it removes is **larger** on validation than on
train. The cost rebate therefore predicts this file ABOVE trial #18's +0.012 by
roughly +0.010; the gross term is a selection term and this lab has nine
instances of those not transferring, so it is forecast as noise of either sign.
A result below trial #18 by more than the cost rebate refutes the claim that the
cost channel is the transferable one.

TRAIN SHEET (train only, engine backtest with `setup.execution`; instrument
re-validated tonight against two recorded figures. No validation, holdout,
forward or incubation number was read when this file was written. Journal F1-F9
of 2026-10-28/29.)

    book                   net     gross    cost    2x cost  turn   pos    97-08   09-17
    hold-1   [trial #18]  +0.0504 +0.0622 -0.0118  +0.0386   1.81   102.0  +0.030  +0.122
    overlap/H6 [this]     +0.0415 +0.0437 -0.0022  +0.0393   1.07   120.0  +0.025  +0.079

1.07x is the cheapest book this lab has priced that holds a score at all — the
equal-weight pool itself churns 0.89x.

THE OPERATOR'S OWN NULL, and the pre-registration it forces. Six random AR(1)
scores at this score's measured rank persistence (phi 0.9953), masked to its own
scorable set, through both constructions: null hold-1 net **-0.0220** (sd
0.0172), null overlap net **-0.0161** (sd 0.0194), null **DELTA +0.0059** (sd
0.0098). So this book's level is **z +2.97** and its delta is **z -1.51**. Read
both, as the 2026-10-27/28 standing rule requires: the level says the score has
content, and the delta says the operator found none of it — which is this file's
claim, not a hole in it, since the claim is that the operator moves money and
not information.

WHAT ARGUES AGAINST IT.
 (i) Trial #18 has already returned +0.012 at the 55th percentile of its null,
     so the score this operator is applied to is a measured near-null. A
     cost rebate on a null is a null.
 (ii) The operator costs this score -0.0089 of net skill on train. Shipping the
     *worse* train number is deliberate — the cost half is the half with a
     transfer claim and the train gross term is the half without one — but it
     is a train-sheet regression and is recorded as such.
 (iii) Six overlapping sleeves can carry a name that leaves its index inside the
     holding period. Those names are pruned at every month-end and the sheet
     above was screened with the pruning in place.
 (iv) `H = 6` is NOT swept here. It was fixed at 6 by the 2026-10-27/28 session
     from a flat-region argument made before any overlapping book was run, and
     1/3/6/12 are all priced in that session's F2. Re-choosing it on this score
     would be the knob-picking this lab has twice recorded as its own mistake.

PRE-REGISTERED TURNOVER: train 1.07x; trial #18's validation churn ran 16% above
its train figure and the lab's last four trials ran 29-49% above, so **1.2-1.6x**
is the predicted band.
"""

from __future__ import annotations

from strategies.lib.vol_trend_book import vol_trend_book

K = 100
HOLD = 6          # the one integer that differs from lv_vol_trend_hold1

STRATEGY = {
    "name": "lv_vol_trend_overlap6",
    "family": "liquidity-volume",
    "hypothesis": (
        "Holding trial #18's book -- the 100 eligible names with the most negative multi-year "
        "share-turnover trend under the (calendar peer group x price-history-depth tercile) "
        "quota -- in six overlapping monthly sleeves instead of one, earns HIGHER validation "
        "skill than trial #18's single-sleeve version of the byte-identical score, because the "
        "sleeve operator's cost channel is arithmetic and universal (+0.008 to +0.013 of train "
        "net skill on all seven objects measured through both constructions tonight) while its "
        "gross channel is object-specific and was negative on six of those seven, so on a score "
        "where the two nearly cancel on train (cost +0.0096, gross -0.0185) the cost half should "
        "dominate on validation, where churn runs higher and the gap the operator removes is "
        "therefore larger: trial #18 charged 2.1x against its own train 1.81x, and this book "
        "charges 1.07x on train. A result below trial #18 by more than the cost rebate refutes "
        "the claim that the cost term is the transferable one."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The falling-turnover top-K book, held in HOLD overlapping monthly
    sleeves: one is reformed each month-end and carried HOLD months as shares,
    so the emitted row is the drifted book plus the reformed sleeve."""
    return vol_trend_book(prices, aux, eligible=eligible, k=K, hold=HOLD)
