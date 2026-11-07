"""The TERM STRUCTURE of a name's own trend, priced as a linear SPAN rather
than as one more horizon -- the momentum-shaped half of tonight's paired test
of the literature's category prior.

=====================================================================
WHY THIS CANDIDATE EXISTS: THE LAB HAS NO ORDERING INSTRUMENT LEFT
EXCEPT THE LITERATURE'S CATEGORY PRIOR, AND THIS IS THE FIRST TRIAL
SELECTED ON IT.
=====================================================================

`experiments/journal.md`'s 2026-11-06/07 handover states the position
plainly: `corr(train skill, validation skill)` is **+0.048** over nineteen
trials; every pre-trial instrument this lab has built -- the train level, the
train delta, the rank IC screen, the appraisal ratio, the matched-null z, the
relabelling rho and both correlation spaces -- **refuses usefully and
qualifies not at all**; so "the only non-circular ordering left is the
literature's category prior", and that handover's idea 3 recommends in as many
words a session that selects candidates on it. `research/SUMMARY.md`'s `p0`
subsection supplies the number: of the two categories reachable from daily
OHLCV without fundamentals, Hou-Xue-Zhang replicate **momentum at 63.2%** and
**trading frictions at about 4%** (102 of 106 variables failing at |t| >= 1.96
under NYSE breakpoints and value weights), which the folder converts to
`p0 ~ 0.25-0.55` against `0.02-0.06` -- an order of magnitude, and the single
most decision-relevant output of that exercise. **Almost every v3 trial so far
has been frictions-shaped.** This file is the momentum-shaped arm; its twin
`sl_micro_span_wf.py` is the frictions-shaped arm, identical in machinery, and
the two are a matched pair across the prior.

WHY A SPAN AND NOT A SCORE. `experiments/learnings.md` records this lab
refuting one functional of the own price path at a time -- the mean at three
horizons, the dispersion, the third moment, the maximum, the sign count, the
within-day location, the session split. Each closure is one direction in a
space. A walk-forward cross-sectional regression over a whole family of path
functionals prices the entire linear span at once, so an empty answer closes
every remaining direction inside it for one trial instead of twenty. It is
also the open cell of `statistical-learning`'s charter question: 2026-10-17/18
answered "which feature groups carry signal" with *none of them, linear or
nonlinear*, but it answered it for ONE feature group (seven characteristic
features, under ridge and under boosting), and its own diagnosis -- **"it is
the features"** -- names a different FEATURE FAMILY under the same validated
estimator as the other uncovered cell.

THE FEATURES. Han-Zhou-Zhu's moving-average-to-price ratios,
`f_L = log(MA_L(P)/P)` at `L` in {5, 21, 63, 126, 252, 504} days, each
cross-sectionally ranked (row-wise, so causal in the time axis per
2026-10-07). Six features. The span nests 5- and 21-day reversal, the 63- and
126-day middle, 12-1 momentum at `L = 252` and the mouth of the long-horizon
reversal window at `L = 504`, with the **signs learned walk-forward rather
than assumed**: a single-horizon sort cannot express the reconciliation, and
every one of these horizons has been refuted here on its own.

=====================================================================
THE FREE SCREEN'S HEADLINE, AND IT IS A CORRECTION TO THE LAB'S
MOST-USED INSTRUMENT: THE REGION-MATCHED IC HARNESS MEASURES A
QUANTITY v3's EXECUTION MODEL CANNOT TRADE, AND THE GAP IS THE
FIRST DAY'S RETURN.
=====================================================================

The harness `learnings.md` validated on 2026-11-04/05 scores a signal at date
`d` against `P[d+21]/P[d]`. v3 fills a row emitted at `d` at each name's
**next real close**, so the return a book actually earns is
`P[d+22]/P[d+1]`. For a 756-day score the difference is noise; for a 5-day
score it is most of the signal. Measured, region-matched, floor 50, 263 train
month-ends:

    feature     decision IC      t  |  TRADEABLE IC      t  | retained
    ma0005          +0.0484  +6.35  |       +0.0273  +3.64  |    56%
    ma0021          +0.0349  +3.82  |       +0.0290  +3.27  |    83%
    ma0063          +0.0245  +2.33  |       +0.0244  +2.30  |   100%
    ma0126          +0.0173  +1.53  |       +0.0183  +1.59  |   106%
    ma0252          +0.0019  +0.15  |       +0.0028  +0.22  |     --
    ma0504          -0.0029  -0.21  |       -0.0010  -0.07  |     --

**Monotone in horizon and zero beyond 63 days**, which is the signature of a
one-close discount and not of a specification choice. Two standing
consequences, both recorded in the journal: the lab's IC harness overstates a
fast score's reachable content by up to **1.8x**, and the exchange rate
`train skill = 3.37 x rank IC` -- calibrated entirely on slow scores -- must
be applied to the TRADEABLE IC. This file therefore trains the learner on the
tradeable target (`FILL_LAG = 1` in `strategies/lib/learned_span.py`), which
is the protocol's own convention rather than a tuned knob.

Refitted on that target the span reads **tradeable IC +0.0250 at t +2.57**
(decision IC +0.0362, t +3.69) over 221 month-ends, and its forecast's rank
rho to the individual features runs +0.707 / +0.622 / +0.386 / +0.311 / +0.058
/ +0.074 from the 5-day to the 504-day scale -- i.e. the learner moved weight
off the 5-day scale once the untradeable close was removed from its target,
which is the retargeting doing exactly what it was imposed to do.

=====================================================================
AND HERE IS THE RESULT THAT MATTERS, STATED BEFORE ANYTHING FAVOURABLE:
A +0.0250 TRADEABLE IC AT t +2.57 CONVERTS TO **NEGATIVE GROSS** SHARPE
SKILL. THE TRAIN GATE WILL REFUSE THIS CANDIDATE.
=====================================================================

Train sheet through `protocol.evaluate_split` with the v3 execution model --
the instrument validated 2026-10-25/26 and re-validated tonight against three
recorded figures (`dcorr_low` reproduced at skill **+0.1020** / sharpe
**+0.6260** / turnover **1.44** / 144.2 positions against the recorded +0.102 /
+0.626 / 1.44 / 144; `old_half_rev` at +0.052, the same figure last night's
harness read against #16's +0.058; and the engine's own **gross pool at
+0.535** against the recorded +0.5361). Gross is measured DIRECTLY at
`cost_multiplier = 0` with the pool re-priced under the same stress, never
inferred from the 2x column (2026-11-02/03).

    book                           skill   sharpe  turn   pos   volr  97-08   09-17
    SPAN trend, net (this file)   -0.0430  +0.4810 3.01  298.9 1.027 -0.014  -0.111
    SPAN trend, GROSS             -0.0200  +0.5160   --     --    --     --      --
    SPAN trend, negation (net)    -0.0570  --      3.01  302.0    --     --      --
    equal-weight pool, net           --    +0.5240
    equal-weight pool, GROSS         --    +0.5350

So the ledger is: tradeable IC **+0.0250 (t +2.57)** -> gross skill
**-0.0200** -> cost **-0.0230** at 3.01x churn -> net **-0.0430**.
`min_train_skill = 0.0` is a hard gate, so the verdict is **GATE_FAIL before
the run starts, and this file says so rather than discovering it.** The
negation is *worse* (-0.0570 against -0.0430), so the learned sign is the
right one; the book is simply worse than the pool.

WHY IT IS SHIPPED ANYWAY, AND WHAT THE VERDICT ADDS THAT THE FREE SCREEN
CANNOT. The 2026-11-05/06 method entry settles the first half: a screen this
lab has measured as uninformative cannot be the thing that vetoes a trial, the
deflator clusters 135 records to roughly 36 effective, the best DSR on the
board is 0.1635 against the 0.95 a challenge needs, and two more decorrelated
trials move a future candidate's DSR by about **0.004** -- three orders of
magnitude smaller than the gap. The rule it states is to ship for the
information the verdict adds and to say which that is. Here it is three
things, none of them reachable for free:

 (i) **The paired category-prior test in the GATE'S OWN STATISTIC.** The prior
     is already confirmed in IC space (this span +0.0250 at t +2.57 against
     its frictions-shaped twin's -0.0061 at t -1.04). Settling it only there
     would repeat precisely the error this lab keeps making -- eleven recorded
     instances of "a positive slice excess with negative Sharpe skill is the
     rule on this panel". The question the policy actually needs answered is
     whether the category prior orders *validation skill*, and n=1 pair cannot
     settle it but it is the first observation ever taken.
 (ii) **The validation skill, its 90% interval and its region-matched null
      percentile** for a span rather than a score. Nineteen trials of evidence
      say train carries +0.048 of correlation with it, so -0.0430 on train is
      not a prediction of anything.
 (iii) **Which mechanism it lands in.** Tonight's novelty screen -- the one
       surviving pre-trial instrument, refusal side only -- puts this book's
       maximum train active-return rho to any recorded cluster at **+0.272**
       (falling share turnover), with +0.161 to the family lead's score,
       +0.129 to `dcorr_low` and **-0.070** to the closed de-risking cluster.
       That is the cleanest novelty profile this lab has priced, it PASSES the
       refusal threshold, and 2026-11-06/07 established that the pass side has
       only ever been demonstrated **blind**. This is an observation on it.

WHAT WAS NOT RUN, AND WHY. The matched-null LEVEL check was deliberately not
run: 2026-11-06/07 recorded it setting the lab record (+6.07) on the board's
second-worst result, and 2026-11-05/06 that it has now failed to predict
validation in both directions. The engine runs its own region-matched null
inside the trial, which is the one that gates.

PRE-REGISTERED PREDICTIONS, to be scored rather than quoted:
 * **Turnover** 3.6-4.5x. Train is 3.01x and this construction has gone
   +21% to +49% train-to-validation (+27% on the CLV trial); eighth
   consecutive use of the 2026-10-13/14 range method.
 * **Drawdown** -38% to -46%, from the volatility ratio **1.027**. The
   2026-11-05/06 shape rule has three confirmations (0.865 -> -28.8%;
   0.954 -> -32.8%; 1.073 -> -46.1% and -47.5%), and at 1.027 the -45% gate
   is expected to be close to binding or to bind.
 * **The null gate refuses it.** Nine of the last eleven v3 trials were
   refused by the region-matched null rather than by cost, drawdown or
   turnover.
 * **#388's forecast floor is INERT here**, and this is its mandatory
   accompaniment (`research/SUMMARY.md` `#388` requires reporting the fraction
   of dates on which the restriction is active): 448.3 names clear the floor
   on an average date, it binds on **0.0%** of 223 dates and empties the book
   on **0.0%**. A one-bit top-K book already expresses "in or out", so
   flooring the forecast is the same restriction one step earlier and has
   nothing left to do -- `#376`'s one-bit truncation seen from the forecast
   side, now measured rather than argued.
"""

from __future__ import annotations

from strategies.lib.learned_span import learned_score
from strategies.lib.third_moment import moment_book

STRATEGY = {
    "name": "sl_trend_span_wf",
    "family": "statistical-learning",
    "hypothesis": (
        "A walk-forward ridge over the six moving-average-to-price ratios "
        "log(MA_L/P) at L = 5, 21, 63, 126, 252 and 504 days -- the term structure of a "
        "name's own trend, with the sign at each horizon learned monthly from realized "
        "forward returns measured FROM THE FILL rather than from the decision date, the "
        "forecast floored at zero, and the hundred highest forecasts quota-allocated "
        "across (trailing-trading-calendar peer group x 12-1-momentum tercile) cells and "
        "held in six overlapping monthly sleeves -- earns positive validation skill "
        "against the equal-weight eligible pool, because the momentum category is the one "
        "reachable from daily closes that the external replication literature puts at a "
        "63.2% hit rate against trading frictions' 4%, and because the linear span of "
        "multi-horizon own-trend can express the sign reversal between horizons that every "
        "single-horizon sort refuted here could not."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the top-100 walk-forward trend-span forecast,
    quota-allocated across calendar-peer x momentum-tercile cells."""
    return moment_book(prices, aux, eligible=eligible,
                       score_fn=learned_score("trend"), cells="mom")
