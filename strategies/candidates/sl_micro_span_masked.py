"""The TERM STRUCTURE of a name's own return AUTOCORRELATION, priced as a
linear SPAN -- the frictions-shaped arm of tonight's paired test of the
literature's category prior, and the twin of `sl_trend_span_masked.py`.

=====================================================================
THE DESIGN: ONE PAIR, TWO CATEGORIES, EVERYTHING ELSE HELD FIXED
=====================================================================

`research/SUMMARY.md`'s `p0` subsection prices the two categories reachable
from daily OHLCV an order of magnitude apart -- Hou-Xue-Zhang replicate
**momentum at 63.2%** against **trading frictions at about 4%** (102 of 106
variables failing), giving `p0 ~ 0.25-0.55` against `0.02-0.06` -- and the
2026-11-06/07 handover's idea 3 recommends a session that selects on that
prior, because `corr(train skill, validation skill)` is +0.048 over nineteen
trials and every other instrument this lab owns qualifies not at all.

A prior that orders two categories is testable only with one candidate from
each, matched. This pair is matched on every node that is not the category:

    shared          six features; 504 days of required own history (so the
                    price-history-length confound of 2026-10-26/27 is the same
                    for both); row-wise ranks taken over the ELIGIBLE names
                    (masked before ranking); the same closed-form ridge at the
                    same alpha and the same 12000-row release floor; the same
                    monthly grid; the same cross-sectional rank target measured
                    FROM THE FILL; `#388`'s zero floor; and `moment_book`'s
                    K=100 calendar-peer x momentum-tercile quota in six
                    overlapping monthly sleeves, byte-identical to #24/#25.

    differs ONLY   `sl_trend_span_masked`: `log(MA_L/P)` at L = 5..504 days,
                   the MOMENTUM category.
                   this file: `rho_k = corr(r_t, r_{t-k})` for k = 1..6 over a
                   504-day window lagged 21 days, the FRICTIONS category.

The two feature sets share no member and no window convention, so this is not
the same-score pair 2026-11-06/07 made an anti-candidate (same-score pairs
correlate at active-return rho +0.909); measured, these two books correlate at
**+0.193** on train active returns.

WHY THIS PARTICULAR FRICTIONS OBJECT. It is unit-free, which on this panel is
a design requirement rather than an aesthetic: a correlation between two
returns of the same name cannot carry the multiplicative back-adjustment factor
the 2026-10-18 / 2026-10-22 engine issues record in stored price and volume
LEVELS, and it divides the volatility level out of the score rather than
controlling for it afterwards. `rho_1` **nests Roll's implied effective
spread** -- a wide spread shows up as negative first-order autocorrelation --
which is the frictions axis this lab has closed on the Amihud LEVEL
(2026-10-24/25) and the share-turnover TREND (2026-10-28/29) but never on the
serial-correlation form; `rho_2..rho_6` are the slow-diffusion half, and no
object in the v3 record touches them. Returns are masked to days the name
actually PRINTED (`volume` is not forward-filled, so a NaN is a shut listing
market); without that mask a run of forward-filled holiday zeros would put the
listing calendar straight into `rho_1`, which is the `%zero` artifact
`learnings.md` records on 2026-09-28. The calendar-peer quota is the designed
second line of defence on the same axis.

=====================================================================
THE FREE BLOCK ANSWERS THE CATEGORY PRIOR IN IC SPACE BEFORE EITHER
TRIAL RUNS, AND IT ANSWERS IT IN THE PRIOR'S FAVOUR: THIS SPAN IS
EMPTY AND ITS TWIN IS NOT.
=====================================================================

Region-matched, floor 50, 261 train month-ends, on the TRADEABLE target
(`P[d+22]/P[d+1]`, the return a v3 book actually earns -- see the twin's header
for the fill-gap table that motivates it):

    feature    full IC      t  |     BIT IC      t  |  bit/full
    rho1       +0.0003  +0.05  |    -0.0047  -0.90  |     --
    rho2       -0.0066  -1.26  |    -0.0015  -0.31  |   +0.23
    rho3       +0.0071  +1.37  |    +0.0019  +0.42  |   +0.26
    rho4       +0.0017  +0.31  |    -0.0017  -0.38  |     --
    rho5       -0.0008  -0.15  |    +0.0034  +0.77  |     --
    rho6       -0.0032  -0.58  |    -0.0027  -0.58  |   +0.85
    SPAN       -0.0030  -0.44  |    -0.0055  -1.14  |   +1.87
    ---------------------------------------------------------------
    twin SPAN  +0.0212  +2.25  |    +0.0076  +1.18  |   +0.36

**Not one lag clears |t| = 1.4, and the learned combination is mildly
ANTI-predictive** (-0.0030, t -0.44; one-bit -0.0055, t -1.14). Against the
momentum-shaped twin's +0.0212 at t +2.25 that is the category prior behaving
exactly as `research/SUMMARY.md` says it should: **the span in the 63%-replication
category carries a measurable IC and the span in the 4% category does not.**
`rho_1` in particular reads +0.0003 at t +0.05, so Roll's spread form of the
frictions axis is a null here on the same terms as its level and trend forms --
the third independent closure of that axis, and the first on a quantity with no
scale in it.

=====================================================================
THE TRAIN SHEET, AND THE TRAIN GATE WILL REFUSE THIS CANDIDATE.
=====================================================================

Through `protocol.evaluate_split`, the instrument validated 2026-10-25/26 and
re-validated tonight against three recorded figures (`dcorr_low` at skill
**+0.1020** / sharpe **+0.6260** / turnover **1.44** / 144.2 positions against
the recorded +0.102 / +0.626 / 1.44 / 144; `old_half_rev` at +0.052 against
#16's +0.058; the engine's own **gross pool at +0.535** against +0.5361).
Gross measured directly at `cost_multiplier = 0` with the pool re-priced under
the same stress and a rebuilt pool cache (2026-11-02/03).

    book                            skill   sharpe  turn   pos   volr  97-08   09-17
    SPAN micro, net (this file)   -0.0570  +0.4660  2.03  186.3 1.002 +0.009  -0.201
    SPAN micro, GROSS             -0.0450  +0.4910    --     --    --     --      --
    SPAN micro, negation (net)    -0.0230      --   2.03     --    --     --      --
    equal-weight pool, net            --   +0.5240
    equal-weight pool, GROSS          --   +0.5350

`min_train_skill = 0.0` is a hard gate, so **the verdict is GATE_FAIL before
the run starts and this file says so first.** Three further facts against the
book, all reported rather than argued away: the negation is better by 0.034, so
the learned sign carries no content; the two sub-periods disagree (+0.009 then
-0.201), which 2026-11-04's `#390` reads as instability rather than low power;
and gross is -0.0450, so cost (-0.0120 at 2.03x churn) is not what refuses it.

WHY IT IS SHIPPED ANYWAY. Last night's `#25` was shipped at train skill -0.013
and its entry records the train gate refusing it, for the reason the
2026-11-05/06 method entry gives: the deflator clusters 137 records to roughly
36 effective, the best DSR on the board is 0.1635 against the 0.95 a challenge
needs, and two more decorrelated trials move a future candidate's DSR by about
**0.004**. What this verdict adds that no free screen can:

 (i) **It is the second half of the pair**, and without it tonight's category
     test exists only in IC space -- which is precisely the space this lab has
     eleven recorded instances of being misled by ("a positive slice excess
     with negative Sharpe skill is the rule on this panel"). The question the
     recommended policy needs answered is whether the prior orders *validation
     skill*, and a single arm cannot answer it.
 (ii) **The validation skill, its interval and its region-matched null
      percentile** for the frictions span.
 (iii) **The mechanism it lands in.** The novelty screen (refusal side only)
       puts this book's train active-return rho at **+0.224** to `dcorr_low`,
       +0.198 to falling share turnover, +0.169 to the de-risking cluster and
       +0.149 to the family lead's score -- max **0.224**, a clean pass, and
       2026-11-06/07 established the pass side has only ever been demonstrated
       blind.

PRE-REGISTERED PREDICTIONS, to be scored:
 * **Turnover 2.4-3.0x** (train 2.03x; +21% to +49% is this construction's
   recorded train-to-validation range).
 * **Drawdown -33% to -41%** from volatility ratio **1.002**, interpolating the
   2026-11-05/06 shape rule's points (0.954 -> -32.8%; 1.046 -> -39.0%, scored
   tonight on the twin; 1.073 -> -46.1% and -47.5%). The -45% gate should not
   bind.
 * **The region-matched null refuses it**, as it has nine of the last eleven.
 * **#388's floor is inert**: 387.1 names clear it on an average date, it binds
   on **0.0%** of 195 dates and empties the book on **0.0%** -- the twin's
   measurement reproduced on an unrelated feature family, which is what makes
   `#388` spent rather than untested.
"""

from __future__ import annotations

from strategies.lib.learned_span import learned_score
from strategies.lib.third_moment import moment_book

STRATEGY = {
    "name": "sl_micro_span_masked",
    "family": "statistical-learning",
    "hypothesis": (
        "A walk-forward ridge over the six own-return autocorrelations "
        "rho_k = corr(r_t, r_{t-k}) for k = 1..6, estimated over a 504-day window of the "
        "name's own PRINTED daily returns lagged 21 days and ranked over the eligible "
        "names only -- the term structure of a name's own serial dependence, which nests "
        "Roll's implied effective spread at k = 1 and the slow-diffusion half at k = 2..6, "
        "with signs learned monthly against forward returns measured from the fill, the "
        "forecast floored at zero, and the hundred highest forecasts quota-allocated across "
        "(trailing-trading-calendar peer group x 12-1-momentum tercile) cells held in six "
        "overlapping monthly sleeves -- earns LOWER validation skill than its "
        "momentum-shaped twin sl_trend_span_masked, because the external replication "
        "literature puts the trading-frictions category at a 4% hit rate against momentum's "
        "63.2%, and this pair is matched on every node except which of those two categories "
        "its features live in."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the top-100 walk-forward autocorrelation-span
    forecast, quota-allocated across calendar-peer x momentum-tercile cells."""
    return moment_book(prices, aux, eligible=eligible,
                       score_fn=learned_score("micro"), cells="mom")
