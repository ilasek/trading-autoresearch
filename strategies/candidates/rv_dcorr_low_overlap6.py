"""Downside CORRELATION, with the volatility term divided out of the score.

THE OBJECT, AND WHY IT IS THE ONE RESEARCH NAMED. Ang-Chen-Xing's
disappointment-aversion story is about downside BETA. `research/SUMMARY.md`
`#116` records that sort as REFUTED -- Hou-Xue-Zhang read the high-minus-low
spread as negative in all three holding horizons and all eight specifications
-- and names the reason through the identity

    beta_minus = rho_minus * sigma_minus_i / sigma_minus_m

i.e. a high downside beta comes either from high downside CORRELATION, which is
the priced content, or from the asset's own downside VOLATILITY, which carries
the opposite-signed volatility effect and dominates the extreme bucket. The
note's own sentence: *"the raw beta_minus sort is a refuted construction and
must not be proposed here; what has never been measured is the correlation with
the volatility term divided out."* This file measures exactly that object:

    rho_minus(i) = corr(r_i, r_m) over the days in a trailing 756-day window on
                   which r_m was below its own window mean, lagged 21 days,

with `r_m` the equal-weight eligible panel's return. `sigma_minus_i` is divided
out by construction; `sigma_minus_m` is common to every name on a date and so
drops out of any cross-sectional rank. The book buys the hundred eligible names
with the LOWEST `rho_minus`.

HYPOTHESIS, PRE-SIGNED BEFORE THE FIRST BOOK WAS PRICED (one sentence in
STRATEGY below): the low end earns positive skill, because a name that comoves
LESS with the market when the market falls is the one that does not fail you
when diversification is worth most, and disappointment aversion says that
service is paid for. The negation was priced as the control before this file
was written and reads **-0.120** against this book's **+0.102**, a margin of
**0.222** -- the largest negation-invariant margin in this lab's v3 record
(previous best 0.125) -- so the sign is the pre-signed one and not a sign
chosen because the number came out that way (the 2026-11-02/03 rule).

=====================================================================
THE SCREEN REFUSED THIS BOOK, AND THE FILE SAYS SO BEFORE IT SAYS
ANYTHING ELSE. THE TRIAL IS SHIPPED TO TEST THE SCREEN AS WELL AS
THE OBJECT.
=====================================================================

Tonight's free block built the instrument the 2026-11-05/06 handover asked
for -- correlate a candidate's TRAIN active-return stream against the train
streams of the recorded board, all in one matched construction -- and ran this
book through it:

    train active-return rho to          lowvol_gk_neg  +0.592   <-- REFUSED
                                        mom252         +0.337
                                        ndrift756      +0.331
                                        vol_trend_down +0.319
                                        decade_rev     +0.291
                                        amihud126_neg  +0.249
                                        old_half_rev   +0.240
                                        clv756         +0.094

`lowvol_gk_neg` is the M1 de-risking cluster that trial #1 closed ("Sharpe is
flat in beta on this panel"), and +0.592 is above the ~0.5 the handover set.
**Three further facts make the refusal stronger, not weaker, and all three are
recorded here rather than argued away.** (i) The rank correlation of this score
to the same object is **-0.123** -- opposite sign, five times smaller -- which
is the third instance of the 2026-11-05/06 sign inversion and the first caught
before a trial was spent. (ii) The book's volatility ratio to the pool is
**0.865**, i.e. it really is a lower-risk book. (iii) Research `#406`'s "design
the confound out" operator was tried free and is a **no-op here**: crossing the
peer quota with a volatility tercile instead of a momentum tercile leaves the
book at rho **+0.953** to this one, skill unchanged at +0.102, and the overlap
with `lowvol_gk_neg` RISES to +0.631. So the low-volatility character is
intrinsic to `rho_minus` and is not removable by the cell choice.

**WHY IT IS SHIPPED ANYWAY, STATED AS ARITHMETIC.** Tonight's F4 validated the
screen's two sides separately against the recorded validation streams, over the
21 score-pairs for which both a matched-construction train rho and a recorded
validation rho exist:

    instrument                       -> validation rho      R2      p
    pairwise RANK rho                                      0.056   0.670
    pairwise TRAIN active-return rho                       0.146   0.119

Neither is significant. **A 0.5 train screen passes 4 of the 5 pairs that
validation put above |0.5|**, including the handover's own headline case
(`clv756`/`old_half_rev`: train **+0.069**, validation **+0.525**). The single
pair that the train screen DID refuse (`decade_rev`/`old_half_rev`, +0.536) came
in at +0.591 on validation. So the instrument is one-sided -- blind when it
passes, 1-for-1 when it refuses -- and its refusal side rests on **one**
observation. This trial is that side's second observation, and it is the only
way to get one.

The second thing the verdict adds that the free screen cannot: the de-risking
axis was closed twice, both times through a quantity with a SCALE -- trial #1
selected on GK volatility (slice beta 0.623), trial #10 on the cointegrating
slope. Nobody has tested it through a pure CORRELATION with the scale divided
out, and `#116` names that gap in as many words. If this book lands inside M1
on validation active returns, the axis is closed from the correlation side too
and `#116` is answered; if it does not, the screen's refusal side is wrong and
the lab's only working novelty instrument is gone. **Both answers are worth a
trial and neither is reachable for free.**

TRAIN SHEET (1997-2017 only, through `protocol.evaluate_split` with the v3
execution model -- the instrument validated 2026-10-25/26, and re-validated
tonight against three recorded figures: `clv756` reproduced at skill +0.007 and
volatility ratio 1.073 against the recorded +0.007 / 1.073, `ndrift756` at
+0.031 / 0.954 against +0.031 / 0.954, `old_half_rev` at +0.052 against #16's
+0.058. No validation, holdout, forward or incubation number was read; no such
file was opened.)

    book                              skill   sharpe  turn   pos   volr   97-08   09-17
    rho_minus LOW   (this file)      +0.102   +0.626  1.44x  144  0.865  +0.083  +0.167
    rho_minus HIGH  (negation)       -0.120   +0.404  1.30x  145  1.161  -0.079  -0.217
    rho_minus LOW, vol-tercile cells +0.102   +0.625  1.40x  137  0.859  +0.089  +0.146
    equal-weight eligible pool          --    +0.524    --    --   1.000     --      --

**Both train sub-periods positive (+0.083 / +0.167)**, which only one other
object on this board has managed, and skill at 2x liquidity costs is **+0.093**
against +0.102 -- so the 0.009 cost bill is not what is carrying it.

*The matched-null LEVEL check* (2026-10-27/28 standing rule, since this
hypothesis rests on the LEVEL and not on an operator's delta). Six AR(1) scores
at this score's own measured month-to-month Spearman rank persistence
(phi = **0.9913**), masked to its own scorable set, through the identical
construction:

    null net: mean -0.0187  sd 0.0199  min -0.0410  max +0.0110
    book     +0.1020   ->   z +6.07

That is the highest reading this lab has recorded (previous best #16's +5.2),
and it is quoted here as exactly what the lab has measured it to be worth and
no more: **evidence that the train number is not construction arithmetic.**
The same instrument read z +4.21 on `vol_trend_down`, which landed at the
55th-66th validation percentile, and z +1.00 on the CLV book, which came in at
validation +0.012 -- it has now failed to predict validation in both
directions, and six draws give its sd five degrees of freedom.

WHAT ARGUES AGAINST THE BOOK, BEYOND THE SCREEN.
 (i) Train skill is not evidence. This lab has measured `corr(train skill,
     validation skill)` at **+0.048** over nineteen trials. +0.102 is the
     highest train skill priced tonight and that fact carries no weight.
 (ii) The volatility ratio 0.865 is **0.135 away from parity**, and the
      2026-10-20/21 entry found that every object clearing |t| = 2 in bps
      carried a ratio at least 0.14 from 1.00 with Sharpe skill inside the
      noise floor or negative. This book sits just inside that line.
 (iii) `rho_minus` carries rank rho **-0.236 to the log price level**, the
       back-adjustment contaminant of the 2026-10-18 / 2026-10-22 engine
       issues. That is larger than the +0.070 the share-turnover trend carried
       (worth about -0.006 of IC there), so scale it to roughly -0.02 of IC
       here. Not negligible, and stated rather than buried.
 (iv) The train drawdown is **-49.6%**, worse than the -45% the VALIDATION gate
      uses. Train drawdown is not gated, and the 2026-11-05/06 reading is that
      the volatility ratio predicts the validation drawdown (0.954 -> -32.8%;
      1.073 -> -46.1% and -47.5%), so a ratio of 0.865 should land well inside
      the gate. That is a prediction, and it is recorded here to be scored.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train
comes in at 1.44x, and the same construction went 1.50x train to 1.9x
validation (+27%) on the CLV trial, so **1.6-2.1x** is the predicted band.
"""

from __future__ import annotations

from strategies.lib.third_moment import downside_correlation_score, moment_book

STRATEGY = {
    "name": "rv_dcorr_low_overlap6",
    "family": "range-variance",
    "hypothesis": (
        "The 100 eligible names with the LOWEST downside correlation -- corr(r_i, r_m) over "
        "the days in a trailing 756-day window on which the equal-weight eligible panel's "
        "return was below its own window mean, lagged 21 days -- quota-allocated across "
        "(trailing-trading-calendar peer group x 12-1-momentum tercile) cells and held in "
        "six overlapping monthly sleeves, earn positive validation skill against the "
        "equal-weight eligible pool, because a name that comoves less with the market when "
        "the market falls does not fail its holder when diversification is worth most and "
        "disappointment aversion says that service is paid for, and because dividing the "
        "name's own downside volatility out of the loading is the one form of the "
        "Ang-Chen-Xing sort that research #116 records as never measured -- the raw "
        "downside-beta version being refuted precisely because the volatility term "
        "dominates its extreme bucket."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the lowest-downside-correlation top-100 pick,
    quota-allocated across calendar-peer x momentum-tercile cells; one sleeve
    reformed each month-end, ineligible names pruned at every month-end."""
    return moment_book(prices, aux, eligible=eligible,
                       score_fn=downside_correlation_score, cells="mom")
