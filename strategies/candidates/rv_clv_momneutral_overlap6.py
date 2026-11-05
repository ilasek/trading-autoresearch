"""Where the close sits inside the day's own range, as a selection score.

THE MECHANISM, AND WHY IT IS NOT ONE THIS LAB HAS ALREADY PRICED. Every price
score the v3 record holds is a function of close-to-close returns: momentum at
every horizon, residual momentum, the decade and five-year reversals, short-term
reversal, the overnight/intraday split, close-to-close and range VOLATILITY,
skewness, the variance ratio, 52-week-high proximity. The closing location value
`(close - low) / (high - low)` is a function of a single day's own three quotes
and of nothing else. It says where in the day's travel the day ended, not how
far the day moved or in which direction. A name whose closes sit persistently in
the lower part of its range has been met by end-of-day supply day after day
without that showing up as a distinctive return path.

HYPOTHESIS, PRE-SIGNED AND FALSIFIABLE (one sentence, in STRATEGY below): the low
end earns a positive peer-relative return, because persistent closing weakness is
price PRESSURE rather than information, and pressure abates while information
does not. The published direction for order-imbalance / closing-pressure
measures is the one taken here; the negation was run as a control before the
file was written and reads -0.087 against this book's +0.007, so the sign is the
pre-signed one and not a sign chosen because the number came out that way (the
2026-11-02/03 refusal rule).

TWO PROPERTIES THAT MADE IT WORTH A TRIAL, BOTH MEASURED TONIGHT ON TRAIN ONLY.

*Novelty.* Mean rank rho over 252 train month-ends against every refuted or
contaminated object on the board:

    old_half  decade_mean  mom252  lowvol126  amihud_neg  vol_trend_down  log_price  dollar_vol
     +0.113     -0.039     +0.439    +0.277      +0.062      -0.014        +0.202     -0.013

Only one of those is large, and it is the one the construction answers: inside
(calendar-peer x 12-1-momentum-tercile) cells the momentum rho falls to **+0.063**.
So the shipped book is a CLV claim and not a momentum relabelling, which the
+0.439 raw figure would have made it.

*Adjustment invariance.* The 2026-10-22 engine issue records that the stored price
and volume LEVELS embed future corporate actions invisibly to both
`causality_check` and the hindsight guard. A ratio of three quotes from the same
day cannot carry that contaminant: any multiplicative factor cancels in it. This
is the first score in the v3 record with that property by construction rather
than by argument.

TONIGHT'S FREE SCREENS (TRAIN 1997-2017 ONLY, through `protocol.evaluate_split`
with the v3 execution model -- the instrument validated 2026-10-25/26. No
validation, holdout, forward or incubation number was read; no such file was
opened.)

*The churn lever, and the ship rule was declared before the grid ran.* The
252-day CLV at the lab's standard monthly hold-1 rule reads gross +0.028 and a
cost term of **-0.052** at 5.76x churn -- the cost bill eats a positive gross
selection term whole. Pre-declared rule: price window in {252, 504, 756} days
crossed with rule in {hold-1, overlap/H6}, and ship the cell with the SMALLEST
cost term that clears the train-skill gate; net train LEVEL does not rank the
cells, because `corr(train skill, validation skill)` is +0.048 over the nineteen
v3 trials and is not evidence.

    cell                     net      gross    cost    turn   pos     97-08   09-17
    clv252  hold-1         -0.0240  +0.0280  -0.0520   5.76   100.0  +0.011  -0.091
    clv252  overlap/H6     +0.0210  +0.0320  -0.0110   2.09   172.5  +0.052  -0.047
    clv504  hold-1         -0.0210  +0.0170  -0.0380   4.56    99.8  -0.005  -0.065
    clv504  overlap/H6     -0.0090  -0.0020  -0.0070   1.70   153.4  +0.014  -0.072
    clv756  hold-1         -0.0240  +0.0090  -0.0330   4.13    99.8  +0.015  -0.099
    clv756  overlap/H6     +0.0070  +0.0120  -0.0050   1.50   145.1  +0.050  -0.090   <- ships

The rule selects `clv756 / overlap/H6` on cost (-0.005, the smallest in the
grid) and it also happens to be the only cell that satisfies the operator's
stated precondition (2026-10-27/28: the score's content must be older than the
holding period -- a three-year window lagged 21 days read five months late is
shifted by one seventh of its own length, where the 252-day window would be
shifted by two fifths). Note for the record that the precondition was NOT
necessary on this object: the 252-day cell's gross term went UP under the
operator (+0.028 to +0.032), which is the second exception after #16 to the
reading that the operator preserves gross only where the precondition holds.

*The negation invariant.* +0.0070 shipped against **-0.0870** negated, gross
+0.012 against -0.080. Not both positive, and the gap is 0.094 -- the sign is
real and it is the pre-signed one.

*The LEVEL null for the whole construction, and THIS IS THE ARGUMENT AGAINST THE
BOOK.* Six AR(1) scores at this score's own measured month-to-month Spearman
rank persistence (phi = **0.9894**), masked to its own scorable set, pushed
through the identical construction:

    null net: mean -0.0132  sd 0.0201  min -0.0530  max +0.0010
    book     +0.0070   ->   z +1.00

**The book's train level is one standard deviation above a meaningless score of
the same persistence, against the z +5.2 the lab's one positive object (#16)
reads on the same instrument.** Pre-registered, per the 2026-10-27/28 standing
rule, that this hypothesis rests on the LEVEL rather than on the operator's
delta -- so this is the null NOT agreeing with the hypothesis, and it is
reported as the main thing arguing against the trial rather than buried.

WHY THE TRIAL IS STILL WORTH ITS PLACE IN THE BAR, STATED AS ARITHMETIC. The
instrument that reads z +1.00 is a train instrument, and this lab has measured
what train instruments are worth here: `corr(train skill, validation skill)` is
+0.048 over nineteen trials (Spearman +0.135), the same correlation ran -0.345
at n=7 and -0.074 at n=17, and the one object that DID read a high matched-null
z on train (`vol_trend_down`, z +4.21) landed at the 55th and 66th percentile of
its validation null. A low train z is therefore not evidence of a bad validation
result any more than a high one was evidence of a good one; what the z +1.00
licenses is the statement that *train gives no reason to believe the score has
content*, which is reported above and is not the same claim. Against that, the
marginal cost is small and countable: the deflator clusters 129 recorded trials
of all versions to roughly 36 effective, the best DSR on the board is 0.1635
against the 0.95 a challenge needs, and two more decorrelated trials move a
candidate's DSR by about 0.002. Six consecutive nightly sessions have now
recorded zero trials on reasoning of this shape.

WHAT ELSE ARGUES AGAINST IT.
 (i) 2009-2017 reads **-0.090** against 1997-2008's +0.050, so the half of train
     nearest validation is the negative half. That sub-period is also this lab's
     worst predictor of validation skill (-0.134 at n=19, after -0.355 at n=15),
     so it is reported and not leant on in either direction.
 (ii) The volatility ratio to the pool is 1.073, so this is NOT the de-risking
      axis trial #1 closed -- but it is slightly MORE volatile than the pool,
      which the gate judges as a ratio.
 (iii) `range-variance` is the family with the worst recorded v3 result
       (`rv_arbrisk_peer_neutral`, skill -0.233), and its one trial was a risk
       construction. Nothing about that trial transfers to this one, which is
       the point of running it, but the family prior is poor.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train
comes in at 1.50x, and this lab's validation churn has run 21-49% above its
train figure on the recorded trials of the sleeve construction, so **1.7-2.3x**
is the predicted band.
"""

from __future__ import annotations

from strategies.lib.clv_book import clv_book

STRATEGY = {
    "name": "rv_clv_momneutral_overlap6",
    "family": "range-variance",
    "hypothesis": (
        "The 100 eligible names with the lowest mean closing location value -- "
        "(close - low) / (high - low), averaged over 756 trading days and lagged 21 -- "
        "quota-allocated across (trailing-trading-calendar peer group x 12-1-momentum "
        "tercile) cells and held in six overlapping monthly sleeves, earn positive "
        "validation skill against the equal-weight eligible pool, because persistent "
        "closing weakness inside a name's own daily range is end-of-day price PRESSURE "
        "rather than information and pressure abates, and because the score is a "
        "within-day ratio and therefore the first object in the v3 record that cannot "
        "carry either the close-to-close return path (rank rho +0.063 to 12-1 momentum "
        "inside the quota cells, against +0.439 outside them) or the back-adjusted "
        "price level the 2026-10-22 engine issue records."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the low-CLV top-100 pick, quota-allocated across
    calendar-peer x momentum-tercile cells. One sleeve is reformed each month-end
    and carried six months as shares, so only that sleeve trades; names that stop
    being eligible are pruned at every month-end."""
    return clv_book(prices, aux, eligible=eligible, cells="mom")
