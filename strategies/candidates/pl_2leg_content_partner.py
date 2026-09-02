"""Does a union leg earn its place by independence alone, or does it also need
content? Arm A: the partner leg HAS a tail.

WHY THIS FILE EXISTS. `experiments/learnings.md` (2026-09-01) records the lab's
most generalisable recent result: "a leg earns its place in a union book by being
independent, not by being individually significant". Its evidence is one
retrospective reading — the four-leg fixed-quota union (#71, validation 0.958)
against the same machinery running the strongest leg alone (#72, 0.782): gap
+0.175, `rho` 0.9119, SE 0.169, **t = +1.04**. The supporting free screen points
the *other* way at leg level: on train, `seasonal`'s decile-10 excess is
+10.59%/yr (t = +4.16) while the other three legs sit at +3.37 / +2.85 / +1.90,
none reliable. So three legs with no individually significant cross-sectional
content appear to add ~0.18 to a book built on the one leg that has it.

The claim as stated is untested in the direction that matters. "Not individually
significant" is not the same as "empty": measured tonight on train against the
forward 21-day return, the three weak legs' top-20 excesses are +3.87%/yr
(t = +2.92), +3.25 (t = +1.26) and +2.31 (t = +1.29) — weak, but all positive and
all in the same direction. Nothing has ever added a leg with **no tail at all**.
Until that is done, "independence, not significance" and "several weak but real
tails, realised in different months" are the same evidence read two ways, and the
lab has been generalising the first.

THE DESIGNED PAIR. Two 2-leg fixed-quota union books, both `seasonal` plus one
partner, differing in exactly one property of the partner:

    arm  partner    train top20-uni      cross-sectional rho to seasonal
    A    reversal   +2.31%/yr (t=+1.29)            -0.006
    B    suv        +0.09%/yr (t=+0.08)            +0.001

Independence is held fixed — both partners are orthogonal to `seasonal` to
within 0.006 — and only the partner's own tail varies. This file is arm A.

MATCHED HOLDINGS-ONLY BEFORE EITHER FILE WAS WRITTEN, per the standing rule that
a scout changing selection and turnover at once cannot answer a mechanism
question:

    book                    months   positions   ann_turnover   joint pool
    A  seasonal+reversal      350       20.6         13.01x       49.3
    B  seasonal+suv           350       20.9         13.44x       49.2
    #72 seasonal alone        350       24.7         11.68x       49.3
    #71 four legs             253       20.1         11.93x       46.7

A and B are matched to 3.3% on turnover (~0.003 Sharpe) and 1.5% on breadth, run
the same 350 months from the same first date, and lose nothing in joint coverage.
`reversal` was chosen over `illiq` as the content partner precisely for this:
`illiq` is a 63-day Amihud average and its 2-leg book runs 7.52x, which would have
put a 5.9x turnover difference (~0.9%/yr, ~0.04 Sharpe) inside a ~0.1 effect.

PRE-REGISTERED. Under either account this book should beat #72's 0.782, because
it adds an orthogonal partner with a real tail: **0.87**, taking the recorded
1-leg -> 4-leg climb of +0.175 and allocating roughly half of it to the first leg
added. The discriminating quantity is not this number but **A minus B**: the
independence account predicts ~0 (content is irrelevant, only orthogonality
pays), the competing account predicts ~+0.2 (half the book's slots in arm B are
filled by a leg that ranks names at random with respect to forward returns, so
arm B should decay toward the equal-weight floor).

STATED HONESTLY: the pair is at the edge of what this window resolves. The two
arms share their `seasonal` half, so `rho` should run near 0.93-0.95 and the
closed-form paired SE `0.568*sqrt(1-rho)` near 0.13-0.14; a +0.2 gap is t ~ 1.4
and a null gap is t ~ 0. What makes the trial worth its place in the deflator
anyway is that the two accounts predict **different signs of a difference**, not
different point estimates of one, and that two independent anchors (#71, #72) are
already on the board at the ends of the same ladder.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. Outside `price-trend` the
last six readings all under-predicted (n = 17), so this is recorded, not relied on.

SCOUT. It does not compete for the seat and cannot reach the holdout. The solved
required-leg-Sharpe bar for a resolvable blend is 1.34-1.42 against a 1.120
champion, and nothing on this board is near it.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import union_legs as UL

STRATEGY = {
    "name": "pl_2leg_content_partner",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "A two-leg fixed-quota union book holding the top 10 names of the same-calendar-month "
        "seasonal score and the top 10 of the 21-day reversal score — a partner that is "
        "orthogonal to the seasonal leg in the cross-section (rho -0.006) AND carries a real "
        "tail of its own (+2.31%/yr top-20 excess on train, t = +1.29) — scores near 0.87 on "
        "validation, above trial #72's single-leg 0.782 under bit-identical machinery, and "
        "materially above its matched twin `pl_2leg_null_partner`, which substitutes a "
        "partner of equal orthogonality (rho +0.001) but no tail whatever (+0.09%/yr, "
        "t = +0.08); because a union leg pays through the interaction of independence with "
        "its own tail content rather than through independence alone, which is the untested "
        "half of the 2026-09-01 finding that legs earn their place by independence rather "
        "than by individual significance. Breadth, churn and joint coverage are matched "
        "holdings-only in advance (20.6 against 20.9 names, 13.01x against 13.44x annual "
        "turnover, 49.3 against 49.2 names of joint pool, same 350 months)."
    ),
}


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "seasonal": SB.seasonal_score(prices),
        "reversal": SB.reversal_score(prices, 21),
    }
    return UL.fixed_quota_union(prices, legs)
