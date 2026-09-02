"""Does a union leg earn its place by independence alone, or does it also need
content? Arm B: the partner leg has NO tail.

READ `pl_2leg_content_partner.py` FIRST — it states the pair's design in full and
is arm A. This file changes exactly one thing: the partner leg.

    arm  partner    train top20-uni      cross-sectional rho to seasonal
    A    reversal   +2.31%/yr (t=+1.29)            -0.006
    B    suv        +0.09%/yr (t=+0.08)            +0.001

Independence is held fixed to within 0.006 and only the partner's own tail
varies, so the difference between the two arms is the value of a leg's content at
constant orthogonality — the untested half of the 2026-09-01 finding that legs
earn their place in a union book "by being independent, not by being individually
significant".

WHAT ARM A ALREADY CHANGED. Arm A ran first and landed **0.786** against a
pre-registered 0.87 and against #72's single-leg **0.782**: `rho` 0.9416, SE
0.1373, **d = +0.0037, t = +0.03**. A partner with a real tail added nothing, so
the per-leg linear reading of the independence account is already refuted. That
sharpens what this arm is for rather than removing the need for it: the ladder is
now flat from one leg to two and jumps only by four (0.782 → 0.786 → 0.958), and
the two live explanations — a **breadth threshold** that needs several legs before
it pays, versus **the partner's identity mattering** — make opposite predictions
about a partner with no content at all.

THE SUV LEG, AND WHY IT IS NOT THE ONE THE LAST SESSION MEASURED. `research/
SUMMARY.md` #62 proposes standardized unexplained volume, and the 2026-09-01
session screened it to the recipe "log volume on a constant plus |positive| and
|negative| returns as separate regressors over 21 days, residual sum
standardized". **Read literally that recipe is identically zero** — an OLS with an
intercept has residual sum exactly zero on its own fitting sample. Measured
directly over 416 name-dates, the largest |sum of residuals| is 1.6e-11 and the
mean 2.4e-13, i.e. the rounding error of the linear solve; an independent
reimplementation of the stated recipe reproduces that session's IC at 21 days to
four decimals (+0.0102 against its +0.0101), which is what two implementations of
one degenerate formula do. That also explains the property it was selected for —
"the most orthogonal signal ever measured against these legs", |rho| 0.002-0.107:
**an object with no content is orthogonal to everything by construction.**

`strategies/lib/union_legs.py` implements the literature's two-window version
instead (estimation window t-63..t-11 fits `log volume ~ 1 + |r|_+ + |r|_-`; the
event window t-10..t is scored against those coefficients and standardized by the
estimation residual SD). That object is real, non-degenerate and well-behaved
(median -0.025, quartiles ±1.42, 99.96% of values inside ±10 after a units floor
on the estimation residual SD guards a degenerate fit). Measured on train against
the forward 21-day return it is a **clean null on the statistic a book is scored
on**: top-20 excess **+0.09%/yr (t = +0.08)**, top-10 **+0.73%/yr (t = +0.40)**,
IC -0.0062 (t = -0.90). That null is the point — it is what makes it the control.

MATCHED HOLDINGS-ONLY BEFORE EITHER FILE WAS WRITTEN:

    book                    months   positions   ann_turnover   joint pool
    A  seasonal+reversal      350       20.6         13.01x       49.3
    B  seasonal+suv           350       20.9         13.44x       49.2
    #72 seasonal alone        350       24.7         11.68x       49.3

3.3% apart on turnover, 1.5% on breadth, same 350 months from the same first
date, no loss of joint coverage — SUV is NaN on 59% of cells but the `seasonal`
leg's own 20-year warmup binds first, so the pool is unchanged.

PRE-REGISTERED: **0.72.** Half this book's slots are filled by a leg that orders
names at random with respect to forward returns, so it should sit *below* the
single-leg 0.782 by roughly the dilution of ten of twenty positions toward the
universe — bounded below by the equal-weight floor this repo records at ~0.49 and
above by 0.782. Landing at or above 0.786 instead would mean the union book's
slots are close to interchangeable and that what the extra legs supply is breadth
of *holdings* rather than breadth of *signal*, which would be a stronger and much
less comfortable result than the independence account as currently written.

The A-minus-B difference is the quantity of interest. Expect `rho` near 0.93-0.95
and a closed-form paired SE near 0.13-0.14, so a 0.07 gap is not resolvable on its
own; what the pair buys is the **sign**, read against two anchors already on the
board (#72 at 0.782, #71 at 0.958).

SECOND PRE-REGISTRATION, per the standing instruction: train Sharpe as a
prediction of validation Sharpe. Arm A broke a six-reading streak of
under-prediction (train 0.81, validation 0.79); this arm extends the sample either
way.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import union_legs as UL

STRATEGY = {
    "name": "pl_2leg_null_partner",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "A two-leg fixed-quota union book holding the top 10 names of the same-calendar-month "
        "seasonal score and the top 10 of standardized unexplained volume — a partner as "
        "orthogonal to the seasonal leg as arm A's (rho +0.001 against -0.006) but carrying "
        "no tail content whatever (+0.09%/yr top-20 excess on train, t = +0.08, against arm "
        "A's +2.31%/yr) — scores near 0.72 on validation, below both trial #72's single-leg "
        "0.782 and arm A's 0.786, because a union leg pays through its own tail and not "
        "through orthogonality as such, so filling half the book's slots with a leg that "
        "orders names at random with respect to forward returns dilutes it toward the "
        "equal-weight floor. Landing at or above 0.786 would instead show the book's slots "
        "are near-interchangeable and that extra legs supply breadth of holdings rather than "
        "breadth of signal. Breadth, churn and joint coverage are matched holdings-only in "
        "advance (20.9 against 20.6 names, 13.44x against 13.01x annual turnover, 49.2 "
        "against 49.3 names of joint pool, same 350 months). The SUV leg is the two-window "
        "construction in strategies/lib/union_legs.py, not the single-window recipe screened "
        "on 2026-09-01, which is identically zero because an OLS with an intercept has "
        "residual sum zero on its own fitting sample."
    ),
}


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "seasonal": SB.seasonal_score(prices),
        "suv": UL.standardized_unexplained_volume(aux["volume"], prices),
    }
    return UL.fixed_quota_union(prices, legs)
