"""Arm C of the union-partner triple: the partner leg is a coin flip.

READ `pl_2leg_content_partner.py` (arm A) AND `pl_2leg_null_partner.py` (arm B)
FIRST. This file changes one thing again: the partner is a deterministic
pseudo-random score derived from a hash of (rebalance date, instrument name) and
reading **no market data at all**.

WHY A THIRD ARM. The pair inverted its pre-registration. Arm A's partner carried
a real tail (+2.31%/yr top-20 on train, t = +1.29) and added **+0.004** over the
single-leg book (#72, 0.782); arm B's partner had none (+0.09%/yr, t = +0.08) and
added **+0.131**. Two free diagnostics then removed the comfortable explanations
and left one:

  * arm B's gain is **not** a defensive or size tilt in costume — SUV's picks sit
    at 1.140x the pool's 21-day volatility (above it, not below), at pool-average
    log dollar volume (-0.029) and slightly *below* pool ETF share (0.127 vs
    0.149);
  * SUV has no content at the depth the book actually buys it either — its
    top-10-of-joint-pool forward-21-day excess on train is **-0.77%/yr
    (t = -0.51)**, if anything mildly negative;
  * and on the **train split, which is 9.1x longer, the two arms tie exactly**:
    0.806 against 0.810, against a validation gap of +0.127.

What survives is a quantity that orders the three books the way their Sharpes are
ordered, and it is not content. It is **the volatility of what the partner puts in
the other half of the book**:

    arm  partner    picks' 21d vol / pool   partner top-10 content   validation
    A    reversal          1.230              +1.23%/yr (t=+0.57)       0.786
    B    suv               1.140              -0.77%/yr (t=-0.51)       0.913
    C    placebo           1.005               0 by construction         ?

Arm C is the neutral point of that axis and the zero point of the content axis at
the same time. It is also the control this family has never had: if a book whose
second half is filled **at random** matches or beats one filled by a measured
signal, then what the union operator buys is not the union of the legs' tails at
all — it is a **deeper draw on the one leg that works** (`seasonal`'s top-10
train excess is +12.21%/yr at t = +6.86 against its top-20's +6.94%/yr), with the
remaining slots serving only to dilute month-specific idiosyncratic risk.

MATCHED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN — the closest match in the
family's history:

    book                 months   positions   ann_turnover   partner stay rate
    B  seasonal+suv        350       20.9         13.44x           0.173
    C  seasonal+placebo    350       21.0         13.42x           0.185

0.5% apart on breadth and 0.1% on turnover, so this pair cannot be accused of
measuring the broker.

PRE-REGISTERED: **0.95.** Arm C should land at or slightly above arm B's 0.913,
because it holds the volatility axis one step further toward the pool average
while changing nothing else. Landing near arm A's 0.786 instead would mean SUV
carried something real that the tail statistic could not see, and would restore
content as the operative variable.

WHAT EACH OUTCOME MEANS, STATED BEFORE THE RUN.
  * C >= B: the second slot is content-insensitive; the 2026-09-01 "legs earn
    their place by independence" finding should be restated as "a union book
    concentrates its best leg into a deeper tail and the rest of the book is
    filler whose only job is to be uncorrelated and not too volatile".
  * C ~ A: the volatility reading is wrong and SUV is doing something the
    diagnostics missed.
  * C well below A: filler is costly and both A and B were flattered by their
    partners' content after all.

THE RESOLUTION CAVEAT, REPEATED. Expect `rho` near 0.94 to arm B and a
closed-form paired SE near 0.14, so a 0.04 gap is not resolvable. This arm is
being spent on a **sign against a construction-zero baseline**, which is the one
thing the two recorded arms cannot supply, and on the fact that a placebo is
the cheapest possible falsification of a mechanism claim.

SECOND PRE-REGISTRATION: train Sharpe as a prediction of validation Sharpe. Both
recorded arms landed at train 0.81; this one is predicted to land there too,
since the train split has said the partner does not matter.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import hashlib

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import union_legs as UL
from strategies.lib import walkforward as W


def _placebo_score(prices: pd.DataFrame) -> pd.DataFrame:
    """A deterministic pseudo-random cross-sectional score.

    Reads no market data: the value for (date, name) is a hash of those two
    strings mapped into [0, 1). That makes it causal by construction (there is
    nothing to peek at), exactly reproducible under the protocol's truncated
    re-runs, and free of any style loading — the three properties a placebo leg
    needs. `hashlib` rather than `numpy.random` so the value depends only on the
    key and not on any global stream state or draw order.
    """
    rows: dict[pd.Timestamp, pd.Series] = {}
    cols = list(prices.columns)
    for dt in W.rebalance_dates(prices):
        key = dt.strftime("%Y%m%d")
        vals = [
            int(hashlib.sha256(f"{key}|{c}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            for c in cols
        ]
        rows[dt] = pd.Series(vals, index=cols)
    if not rows:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T


STRATEGY = {
    "name": "pl_2leg_placebo_partner",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "A two-leg fixed-quota union book holding the top 10 names of the same-calendar-month "
        "seasonal score and the top 10 of a deterministic pseudo-random score that reads no "
        "market data at all scores near 0.95 on validation — at or above trial #74's 0.913, "
        "whose partner was a measured but contentless signal, and well above trial #73's "
        "0.786, whose partner carried a real tail — because the union book's second slot is "
        "content-insensitive and what orders these books is the volatility of whatever fills "
        "it (partner picks at 1.005x, 1.140x and 1.230x the pool's 21-day volatility for the "
        "placebo, SUV and reversal partners respectively), the operative mechanism being that "
        "a second leg lets the book draw the working leg's own deeper tail (seasonal's top-10 "
        "train excess is +12.21%/yr at t = +6.86 against its top-20's +6.94%/yr) while the "
        "remaining slots merely dilute month-specific idiosyncratic risk. Landing near 0.786 "
        "instead would restore the partner's content as the operative variable. Breadth and "
        "churn are matched holdings-only in advance to within 0.5% and 0.1% of trial #74 "
        "(21.0 against 20.9 names, 13.42x against 13.44x annual turnover, same 350 months)."
    ),
}


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "seasonal": SB.seasonal_score(prices),
        "placebo": _placebo_score(prices),
    }
    return UL.fixed_quota_union(prices, legs)
