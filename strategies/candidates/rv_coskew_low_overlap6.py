"""Coskewness with the market, at the long estimation window.

THE OBJECT.  beta_skd(i) = E[e_i * e_m^2] / sqrt( E[e_i^2] * E[e_m^2] ),

with `e_i` name i's market-model residual and `e_m` the demeaned return of the
equal-weight eligible panel, both over a trailing 756-day window lagged 21 days
(`research/SUMMARY.md` `#118`; Harvey-Siddique). It is unit-free by
construction and built from residuals orthogonal to the market, so it is not
the beta axis this lab closed from the weighting side on 2026-10-09/10 and from
the selection side on 2026-10-20/21: those are second-moment objects and this
is a third co-moment.

Extend utility to the third moment and an asset that makes a diversified
portfolio's distribution more left-skewed must be PAID for, so the premium on
coskewness is NEGATIVE and the tradeable long bucket is the most-negative
third. The book buys the hundred eligible names with the LOWEST `beta_skd`.

THE ESTIMATION WINDOW IS THE LIVE DISAGREEMENT AND IT IS WHY THIS IS WORTH A
TRIAL RATHER THAN A CITATION. `#118` records the replication chain refusing to
point one way: independent reproductions recover the premium in sample,
Jensen-Kelly-Pedersen find it in developed-ex-US and marginally at best in the
US, and Hou-Xue-Zhang read it as **right-signed but insignificant in all eight
specifications**. The note's most parsimonious reconciliation -- an inference
from the two papers' methods, not a claim either makes -- is that HXZ estimate
the third moment from **one month of daily returns**, where Harvey-Siddique are
explicit that odd moments are not persistent and that noise in a third moment
is amplified by a cube rather than a square. This file therefore uses 756 days,
the short end of Harvey-Siddique's own 36-72 month grid. The falsifiable
content is whether the long window rescues an object the short window reads as
a null.

WHY IT IS SHIPPED ON A NEGATIVE TRAIN NUMBER, STATED PLAINLY. The train sheet
below reads skill **-0.013** for the pre-signed direction. That is not a
reason to decline here and the arithmetic is the lab's own: `corr(train skill,
validation skill)` is **+0.048** over nineteen v3 trials, and the 2026-11-05/06
method entry states that a screen measured as uninformative cannot be the thing
that vetoes a trial. What a pre-trial screen is entitled to do is refuse
relabellings, check the gates are mechanically reachable, and check the
negation invariant. This candidate passes all three, and on the first it has
**the cleanest profile of anything priced tonight**:

    train active-return rho to     mom252         +0.306   <-- max
                                   old_half_rev   +0.228
                                   amihud126_neg  +0.152
                                   decade_rev     +0.131
                                   lowvol_gk_neg  +0.097
                                   clv756         +0.074
                                   ndrift756      +0.039
                                   vol_trend_down +0.034

Max |rho| **+0.306**, against +0.592 for tonight's other object, and the screen's
refusal side is the only side tonight's F4 found evidence for. Rank rho to the
board is at most **0.115** (to `amihud126_neg`), and to the log price level
**-0.065** -- so this score carries almost none of the back-adjustment
contaminant the 2026-10-18 / 2026-10-22 engine issues record. It is
rank-orthogonal to tonight's other new object at **+0.009**, so the two are
separate bets rather than one.

TRAIN SHEET (1997-2017 only, through `protocol.evaluate_split` with the v3
execution model; the harness was re-validated tonight against three recorded
figures -- `clv756` at skill +0.007 / volatility ratio 1.073 against the
recorded +0.007 / 1.073, `ndrift756` at +0.031 / 0.954 against +0.031 / 0.954,
`old_half_rev` at +0.052 against #16's +0.058. No validation, holdout, forward
or incubation number was read; no such file was opened.)

    book                              skill   sharpe  turn   pos   volr   97-08   09-17   skew
    beta_skd LOW    (this file)      -0.013   +0.511  1.67x  154  1.020  -0.069  +0.032  +0.03
    beta_skd HIGH   (negation)       -0.067   +0.457  1.60x  153  1.052  +0.019  -0.210  -0.08
    beta_skd LOW, vol-tercile cells  -0.010   +0.513  1.64x  149  1.025  -0.077  +0.066  +0.02
    equal-weight eligible pool          --    +0.524    --    --   1.000     --      --     --

**The negation invariant holds and holds in the direction that matters**: the
pre-signed, published direction (-0.013) is the better of the two (-0.067), by
0.054. That margin is thin and is reported as thin. **The volatility ratio is
1.020** -- the closest to parity of any book priced tonight, and parity is the
narrow band the 2026-11-05/06 entry found the gate set admits, after the CLV
pair was refused twice at 1.073 and the drawdown gate turned out to be a shape
gate. Research `#406`'s "design the volatility confound out" operator was tried
free and is a **no-op on this panel**: crossing the quota with a volatility
tercile moves skill from -0.013 to -0.010 and the maximum board overlap from
+0.306 to +0.301, so it is not shipped as a node.

WHAT ARGUES AGAINST THE BOOK.
 (i) The train level is NEGATIVE and the two sub-periods disagree in sign
     (-0.069 / +0.032), which is the same split-sample instability the
     2026-10-09/10 entry used to decline common idiosyncratic volatility. The
     honest reading is that this ships on the lab's measured indifference to
     train numbers, not on a train case.
 (ii) `#118`'s own most transferable remark cuts against the whole exercise and
      is Harvey-Siddique's: *the highest-Sharpe styles often have the most
      negative skew, which is part of why their Sharpe ratios are high.* This
      lab's objective IS Sharpe and Sharpe does not penalise left skew, so a
      positive reading here would be partly a skew risk premium being counted
      as selection. The train book's own daily-return skewness is **+0.03**
      against the negation's -0.08, which is the cheapest available control and
      says the effect is not showing up as a skew bet on train. It must be read
      again on validation before any positive verdict is believed.
 (iii) Harvey-Siddique's own follow-up specification curve moves the premium
       estimate by roughly a factor of two across weighting scheme, window
       length (36/48/60/72) and the maximum missing months allowed -- with the
       missing-value limit among the more influential knobs. This file fixes
       all three before measuring (756 days, equal weight inside the selected
       slice, `min_periods` at 400 usable market days) and does not tune them.
 (iv) `seasonality-calendar`, `lead-lag-spillover` and `statistical-arbitrage`
      have each been closed on measurement after a single-digit number of
      trials, and three of the four trials run on 2026-11-05/06 were refused by
      the random-selection null at the 59th-68th percentile against the 90th
      the gate wants. A near-tie is the modal outcome on this board and is the
      most likely outcome here.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train
comes in at 1.67x, and the same construction went 1.50x train to 1.9x
validation (+27%) on the CLV trial, so **1.8-2.4x** is the predicted band.
"""

from __future__ import annotations

from strategies.lib.third_moment import coskewness_score, moment_book

STRATEGY = {
    "name": "rv_coskew_low_overlap6",
    "family": "range-variance",
    "hypothesis": (
        "The 100 eligible names with the most NEGATIVE coskewness with the equal-weight "
        "eligible panel -- E[e_i e_m^2] / sqrt(E[e_i^2] E[e_m^2]) over a trailing 756-day "
        "window lagged 21 days, with e_i the market-model residual and e_m the demeaned "
        "panel return -- quota-allocated across (trailing-trading-calendar peer group x "
        "12-1-momentum tercile) cells and held in six overlapping monthly sleeves, earn "
        "positive validation skill against that pool, because an asset that makes a "
        "diversified portfolio more left-skewed must be paid for so the premium on "
        "coskewness is negative and its most-negative third is the long-only tradeable "
        "bucket, and because the one reconciliation research #118 offers for the "
        "literature's disagreement is that the sceptical replication estimates this third "
        "moment from a single month of daily returns while odd moments are not persistent "
        "and cubed noise is larger than squared noise -- which the 756-day window tests."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the most-negative-coskewness top-100 pick,
    quota-allocated across calendar-peer x momentum-tercile cells; one sleeve
    reformed each month-end, ineligible names pruned at every month-end."""
    return moment_book(prices, aux, eligible=eligible,
                       score_fn=coskewness_score, cells="mom")
