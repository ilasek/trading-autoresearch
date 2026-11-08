"""The TERM STRUCTURE of a name's own trend, priced as a linear SPAN -- the
momentum-shaped arm of tonight's paired test of the literature's category
prior. (`sl_trend_span_wf`, the same object with the column-axis leak the
causality check caught, is the recorded trial immediately above this one in the
journal; every number below is re-measured under masked ranks.)

=====================================================================
WHY THIS CANDIDATE EXISTS
=====================================================================

The 2026-11-06/07 handover states the lab's position: `corr(train skill,
validation skill)` is **+0.048** over nineteen trials, every pre-trial
instrument this lab owns **refuses usefully and qualifies not at all**, and so
"the only non-circular ordering left is the literature's category prior". Its
idea 3 recommends in as many words a session that selects on it.
`research/SUMMARY.md`'s `p0` subsection supplies the number: of the two
categories reachable from daily OHLCV, Hou-Xue-Zhang replicate **momentum at
63.2%** and **trading frictions at about 4%** (102 of 106 variables failing),
giving `p0 ~ 0.25-0.55` against `0.02-0.06`. **Almost every v3 trial so far has
been frictions-shaped.** This file is the momentum-shaped arm;
`sl_micro_span_masked.py` is the frictions-shaped arm, identical in machinery.

WHY A SPAN AND NOT A SCORE. `learnings.md` records this lab refuting one
functional of the own price path at a time -- the mean at three horizons, the
dispersion, the third moment, the maximum, the sign count, the within-day
location, the session split. Each closure is one direction in a space. A
walk-forward regression over a whole family prices the span at once, so an
empty answer closes every remaining direction inside it for one trial. It is
also the open cell of `statistical-learning`'s charter question: 2026-10-17/18
answered "which feature groups carry signal" with *none of them, linear or
nonlinear*, for ONE feature group (seven characteristic features, ridge and
boosting), and its own diagnosis -- **"it is the features"** -- names a
different FEATURE FAMILY under the same validated estimator as what is left.

THE FEATURES. `f_L = log(MA_L(P)/P)` at `L` in {5, 21, 63, 126, 252, 504}
days, ranked over the ELIGIBLE names (masked before ranking -- see the lesson
on the trial above, and `sl_ridge_six_masked`'s header). Six features. The span
nests 5- and 21-day reversal, the 63/126-day middle, 12-1 momentum at
`L = 252` and the mouth of the long-horizon reversal window at `L = 504`, with
the signs learned walk-forward: no single-horizon sort can express the
reversal between horizons, and every one of these horizons is refuted here on
its own.

=====================================================================
THE FREE BLOCK'S HEADLINE, AND IT IS A CORRECTION TO THE LAB'S
MOST-USED INSTRUMENT: THE REGION-MATCHED IC HARNESS SCORES A SIGNAL
AGAINST A RETURN v3's EXECUTION MODEL GIVES AWAY, AND THE GAP IS THE
FIRST DAY.
=====================================================================

The harness validated on 2026-11-04/05 scores a signal at `d` against
`P[d+21]/P[d]`. v3 fills a row emitted at `d` at each name's **next real
close**, so a book earns `P[d+22]/P[d+1]`. For a 756-day score the difference
is noise; for a 5-day score it is most of the signal. Region-matched, floor 50,
262 train month-ends, identical under masked and unmasked ranks (Spearman
inside the scored set is invariant to the rank denominator):

    feature   decision IC      t  |  TRADEABLE IC      t  | retained
    ma0005        +0.0484  +6.35  |       +0.0273  +3.64  |    56%
    ma0021        +0.0349  +3.82  |       +0.0290  +3.27  |    83%
    ma0063        +0.0245  +2.33  |       +0.0244  +2.30  |   100%
    ma0126        +0.0173  +1.53  |       +0.0183  +1.59  |   106%
    ma0252        +0.0019  +0.15  |       +0.0028  +0.22  |      --
    ma0504        -0.0029  -0.21  |       -0.0010  -0.07  |      --

**Monotone in horizon and gone beyond 63 days** -- the signature of a one-close
discount, not of a specification choice. This file therefore trains on the
tradeable target (`FILL_LAG = 1`), which is the protocol's own convention and
not a tuned knob. Refitted there the span reads **tradeable IC +0.0212 at
t +2.25** (decision IC +0.0311, t +3.24) over 188 month-ends at breadth 521,
with forecast rank rho to the features running +0.703 / +0.677 / +0.588 /
+0.482 / +0.222 / +0.155 from the 5-day to the 504-day scale.

=====================================================================
AND THE SECOND HALF, WHICH REFUSES THIS BOOK BEFORE ITS OWN TRAIN
SHEET DOES: COMPOSE THE FILL LAG WITH `#376`'s ONE-BIT TRUNCATION AND
THE REACHABLE IC IS +0.0076 AT t +1.18 -- A 4.1x OVERSTATEMENT.
=====================================================================

`research/SUMMARY.md` `#376` says a top-K long-only book expresses only
`in or out`, so the IC it can reach is the IC of `1[rank > 1-f]`, not the full
rank IC. Nobody had composed that with the fill lag. At `f = 0.10` (the lab's
own K/N), on the TRADEABLE target:

    object        full      t  |      BIT      t  |      bot      t  | bit/full
    ma0005     +0.0273  +3.64  |  +0.0124  +2.19  |  +0.0275  +3.66  |   +0.45
    ma0021     +0.0290  +3.27  |  +0.0071  +1.08  |  +0.0293  +3.32  |   +0.25
    ma0063     +0.0244  +2.30  |  +0.0041  +0.52  |  +0.0247  +2.33  |   +0.17
    ma0126     +0.0183  +1.59  |  +0.0069  +0.83  |  +0.0185  +1.61  |   +0.38
    SPAN       +0.0212  +2.25  |  +0.0076  +1.18  |  +0.0213  +2.26  |   +0.36

`bot` equals `full` to four decimals on every row, which is `#376`'s own
finding reproduced on a new object family: **the information is in the bottom,
and the long-only book cannot have it.** The composed chain for this span is

    decision full IC  +0.0311 (t +3.24)
      x0.68 fill lag -> +0.0212 (t +2.25)
      x0.36 one bit  -> +0.0076 (t +1.18)   <- the only IC this book can reach

i.e. **the lab's standard harness overstates the reachable quantity by 4.1x,
and what is left is not distinguishable from zero.** That is the first
pre-trial instrument in this lab's record with a *mechanism* attached rather
than a correlation, and it predicts a null book from the IC side alone.

=====================================================================
THE TRAIN SHEET AGREES, AND THE TRAIN GATE WILL REFUSE THIS CANDIDATE.
THE NEGATION IS BETTER THAN THE BOOK. BOTH FACTS ARE STATED FIRST.
=====================================================================

Through `protocol.evaluate_split` with the v3 execution model -- validated
tonight against three recorded figures (`dcorr_low` reproduced at skill
**+0.1020** / sharpe **+0.6260** / turnover **1.44** / 144.2 positions against
the recorded +0.102 / +0.626 / 1.44 / 144; `old_half_rev` at +0.052, the same
figure last night's harness read against #16's +0.058; and the engine's own
**gross pool at +0.535** against the recorded +0.5361). Gross is measured
DIRECTLY at `cost_multiplier = 0` with the pool re-priced under the same
stress, never inferred from the 2x column (2026-11-02/03), and the pool cache
is rebuilt for the stressed setup because `dataclasses.replace` shares it --
the same one-signed error that entry records, caught here before it was quoted.

    book                            skill   sharpe  turn   pos   volr  97-08   09-17
    SPAN trend, net (this file)   -0.0650  +0.4590  2.89  298.4 1.046 -0.040  -0.137
    SPAN trend, GROSS             -0.0440  +0.4920    --     --    --     --      --
    SPAN trend, negation (net)    -0.0330      --   2.84     --    --     --      --
    equal-weight pool, net            --   +0.5240
    equal-weight pool, GROSS          --   +0.5350

Ledger: reachable bit IC **+0.0076 (t +1.18)** -> gross skill **-0.0440** ->
cost **-0.0210** at 2.89x churn -> net **-0.0650**, both sub-periods negative,
-0.086 at 2x costs. `min_train_skill = 0.0` is a hard gate, so **the verdict is
GATE_FAIL before the run starts and this file says so rather than discovering
it.** And the negation invariant **fails**: the inverted book is better by
0.032, so the span's direction carries no sign content in the gate's statistic
even though its IC does. The 2026-11-05/06 method entry lists the negation
invariant as one of three things a pre-trial screen is entitled to refuse on;
that it is reported here rather than argued away is the point, and the reading
to carry is that a LEARNED sign failing the invariant is a statement about the
learner, not about a researcher's post-hoc choice.

ALSO MEASURED AND REFUTED FOR FREE, so it is not re-bought: the exchange rate
`train skill = 3.37 x rank IC` puts a +0.0212 tradeable IC at a ceiling of
**+0.0714**; realised gross is **-0.0440**, i.e. **-62% of ceiling** against
the 6%-65% band the rate was calibrated on. The band must now be quoted as
including large negative realisations, and the rate applied to the BIT IC
rather than the full one.

WHY IT IS SHIPPED ANYWAY, AND WHAT THE VERDICT ADDS THAT THE FREE SCREEN
CANNOT. The 2026-11-05/06 method entry settles the arithmetic: the deflator
clusters 136 records to roughly 36 effective, the best DSR on the board is
0.1635 against the 0.95 a challenge needs, and two more decorrelated trials
move a future candidate's DSR by about **0.004** -- three orders of magnitude
below the gap. Last night's `#25` was shipped at train skill -0.013 for exactly
this reason and its journal entry records the train gate refusing it. Three
things the verdict adds, none reachable for free:

 (i) **The paired category-prior test in the GATE'S OWN STATISTIC.** The prior
     is already confirmed in IC space (this span +0.0212 at t +2.25 against its
     frictions-shaped twin's -0.0030 at t -0.44). Settling it only there would
     repeat the lab's own most-recorded error -- eleven instances of "a
     positive slice excess with negative Sharpe skill is the rule on this
     panel". What the policy needs is whether the prior orders *validation
     skill*; n=1 pair cannot settle it and this is the first observation.
 (ii) **Validation skill, its 90% interval and its region-matched null
      percentile** for a span rather than a score.
 (iii) **Which mechanism it lands in.** Tonight's novelty screen -- the one
       surviving pre-trial instrument, refusal side only -- puts this book's
       train active-return rho at **+0.184** to falling share turnover,
       **+0.053** to the family lead's score, **-0.072** to `dcorr_low` and
       **-0.216** to the closed de-risking cluster: max |rho| **0.216**, the
       cleanest novelty profile this lab has priced. It PASSES, and
       2026-11-06/07 established the pass side has only ever been demonstrated
       **blind**. This is an observation on it.

NOT RUN, AND WHY. The matched-null LEVEL check: 2026-11-06/07 recorded it
setting the lab record (+6.07) on the board's second-worst result, and
2026-11-05/06 that it has failed to predict validation in both directions. The
engine runs its own region-matched null inside the trial, which is the one that
gates.

PRE-REGISTERED PREDICTIONS, to be scored:
 * **Turnover 3.5-4.3x.** Train 2.89x; this construction has gone +21% to +49%
   train-to-validation (+27% on the CLV trial). Eighth consecutive use of the
   2026-10-13/14 range method.
 * **Drawdown -40% to -47%, and the -45% gate may bind**, from volatility ratio
   **1.046**. The 2026-11-05/06 shape rule's four points: 0.865 -> -28.8%,
   0.954 -> -32.8%, 1.027 untested, 1.073 -> -46.1% and -47.5%.
 * **The region-matched null refuses it.** Nine of the last eleven v3 trials
   were refused by that gate rather than by cost, drawdown or turnover.
 * **#388's forecast floor is INERT**, and this is its mandatory accompaniment
   (`#388` requires reporting the share of dates on which the restriction is
   active): 324.0 names clear the floor on an average date, it binds on
   **0.0%** of 190 dates and empties the book on **0.0%**. A top-K book already
   expresses one bit, so flooring the forecast is the same restriction one step
   earlier and has nothing left to do -- `#376` seen from the forecast side,
   now measured rather than argued. `#388` is spent.
"""

from __future__ import annotations

from strategies.lib.learned_span import learned_score
from strategies.lib.third_moment import moment_book

STRATEGY = {
    "name": "sl_trend_span_masked",
    "family": "statistical-learning",
    "hypothesis": (
        "A walk-forward ridge over the six moving-average-to-price ratios log(MA_L/P) at "
        "L = 5, 21, 63, 126, 252 and 504 days -- the term structure of a name's own trend, "
        "ranked over the eligible names only, with the sign at each horizon learned monthly "
        "from realized forward returns measured FROM THE FILL rather than from the decision "
        "date, the forecast floored at zero, and the hundred highest forecasts "
        "quota-allocated across (trailing-trading-calendar peer group x 12-1-momentum "
        "tercile) cells and held in six overlapping monthly sleeves -- earns positive "
        "validation skill against the equal-weight eligible pool, because the momentum "
        "category is the one reachable from daily closes that the external replication "
        "literature puts at a 63.2% hit rate against trading frictions' 4%, and because "
        "the linear span of multi-horizon own-trend can express the sign reversal between "
        "horizons that no single-horizon sort refuted here could express."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the top-100 walk-forward trend-span forecast,
    quota-allocated across calendar-peer x momentum-tercile cells."""
    return moment_book(prices, aux, eligible=eligible,
                       score_fn=learned_score("trend"), cells="mom")
