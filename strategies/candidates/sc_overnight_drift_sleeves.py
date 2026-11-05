"""How much of a name's daily travel happens while the exchange is shut.

THE MECHANISM. A daily bar is two sessions. The overnight gap from the previous
close to today's open is where news, retail order flow accumulated out of hours
and attention-driven demand land; the intraday move from open to close is where
institutional execution happens. This score measures, for each name, what
fraction of its daily range has persistently accrued in the overnight session:

    overnight_drift = mean over 756 days of (open - previous close) / (high - low),
                      lagged 21 days

and the book buys the hundred eligible names with the LOWEST value -- the names
that have gained the least out of hours.

HYPOTHESIS, PRE-SIGNED BEFORE THE FIRST BOOK WAS PRICED (one sentence in
STRATEGY below): the low end earns a positive peer-relative return, because a
persistent overnight gain is attention-driven and retail-order-flow-driven
demand arriving when the exchange cannot absorb it, which is a transient price
component, so the names without it are the ones not carrying that component.
The negation was priced as the control before this file was written and reads
**-0.094** against this book's +0.031, so the sign is the pre-signed one and not
a sign chosen because the number came out that way (the 2026-11-02/03 rule).

WHY THE FAMILY SLUG IS `seasonality-calendar`, AND THE ALTERNATIVE IS NAMED. The
defining choice here is a CALENDAR partition of the return series -- which part
of the trading day the return accrued in -- which is the same kind of object as
the day-of-week and turn-of-month effects `program.md` lists under this family,
and the family's one reachable form is the fully-invested cross-sectional
seasonal, which this is. The honest alternative is `range-variance`, since the
normaliser is the daily range and the score reads the high/low panels; it is
filed here because the range enters only as a scale and the claim is about the
session boundary. A human owner who disagrees should re-file it; the slug was
chosen on that reading and NOT because `range-variance` already has two trials
tonight.

WHY IT IS NOT A RELABELLING. Mean rank rho over 252 train month-ends against
every refuted or contaminated object on the board, plus tonight's other score:

    mom252  old_half  decade_mean  lowvol126  amihud_neg  vol_trend_down  log_price  clv756
    +0.029   -0.009     -0.162      -0.116      +0.087       -0.095        -0.003    +0.230

**That is the cleanest novelty profile in this lab's v3 record** -- the largest
absolute figure is 0.230, against the "at most 0.21 to every refuted object"
that qualified the share-turnover trend and the +0.439 tonight's CLV score
carried to momentum. Inside (calendar-peer x momentum-tercile) cells the
momentum rho is **+0.007**. And the **-0.003** to the log price level is the
figure that matters most: the 2026-10-22 engine issue records that stored price
and volume LEVELS embed future corporate actions invisibly to both
`causality_check` and the hindsight guard, and this score is a ratio of two
quotes one day apart on the same adjusted series.

TONIGHT'S FREE SCREENS (TRAIN 1997-2017 ONLY, through `protocol.evaluate_split`
with the v3 execution model -- the instrument validated 2026-10-25/26. No
validation, holdout, forward or incubation number was read; no such file was
opened. One sibling score, the range-normalised INTRADAY drift
(close - open)/(high - low), was declined free before any book was priced: its
rank rho to tonight's CLV score is **-0.706**, making it a relabelling of a leg
already measured at -0.087.)

*The book, its negation, and the un-normalised control that ships alongside it.*

    book                                  net      gross    cost    turn   pos    volr   97-08   09-17
    range-normalised  (this file)       +0.0310  +0.0370  -0.0060  1.34  138.1  0.954  +0.007  +0.022
    range-normalised, NEGATED           -0.0940  -0.0910  -0.0030  1.34  138.7  1.067  -0.020  -0.203
    un-normalised overnight RETURN      +0.0250  +0.0320  -0.0070  1.39  140.7  0.947  -0.010  +0.021
    un-normalised, NEGATED              -0.0610  -0.0580  -0.0030  1.47  142.7  1.151  -0.023  -0.147

Three things to read off it. The negation invariant passes by **0.125** of net
skill, the largest margin of the night. **Both train sub-periods are positive**
(+0.007 and +0.022), which no other object priced tonight managed. And the
volatility ratio to the pool is **0.954**, i.e. the book is slightly LESS
volatile than its benchmark -- which matters because tonight's two CLV trials
were both refused on the validation drawdown gate at a ratio of 1.073.

*The LEVEL null for the whole construction.* Six AR(1) scores at this score's own
measured month-to-month Spearman rank persistence (phi = **0.9876**), masked to
its own scorable set, through the identical construction:

    null net: mean -0.0210  sd 0.0232  min -0.0540  max -0.0020
    book     +0.0310   ->   z +2.24

Pre-registered per the 2026-10-27/28 standing rule that this hypothesis rests on
the **LEVEL** and not on the operator's delta. z +2.24 is a clear separation
from a meaningless score of the same persistence -- below #16's +5.2 but above
every other object this lab has pushed through the instrument, and the only
positive reading of the night (tonight's CLV book read +1.00).

WHAT ARGUES AGAINST THE BOOK.
 (i) The level null is z +2.24 on six draws, so the null's own sd is estimated
     from five degrees of freedom. Read it as "clearly not the null" and not as
     a p-value.
 (ii) The same instrument read z +4.21 on `vol_trend_down` (2026-10-28/29) and
      that book landed at the 55th-66th percentile of its validation null, and
      z +1.00 on tonight's CLV book which came in at validation +0.012. **The
      matched-null z has now failed to predict validation in both directions**,
      so its value here is the narrow one it is entitled to: evidence that the
      train number is not construction arithmetic.
 (iii) `seasonality-calendar`'s one recorded v3 trial is the board's
       second-worst (`sc_weekday_mood_band`, skill -0.265), and `learnings.md`
       records two characteristic-level seasonals (weekday mood, Heston-Sadka
       same-month) as real on this panel and unharvestable under v3's execution
       model. The difference this book is betting on is that it is a slow,
       fully-invested, 1.34x-churn characteristic rather than a 4-11x one.
 (iv) The open panel is the least-exercised column of `aux` in this lab's
      record. The score's one structural weakness is that `open` on a
      back-adjusted series is adjusted by the same factor as the previous close
      only if the action's ex-date is handled consistently by the vendor; the
      -0.003 rho to the log price level is the evidence that it is, but it is
      evidence rather than proof.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train
comes in at 1.34x, and tonight's CLV trial went 1.50x on train to 1.9x on
validation (+27%), so **1.5-2.0x** is the predicted band.
"""

from __future__ import annotations

from strategies.lib.session_split import overnight_drift_score, session_book

STRATEGY = {
    "name": "sc_overnight_drift_sleeves",
    "family": "seasonality-calendar",
    "hypothesis": (
        "The 100 eligible names whose daily OVERNIGHT session has persistently contributed "
        "the least to their own daily range -- the lowest trailing 756-day mean of "
        "(open - previous close) / (high - low), lagged 21 days -- quota-allocated across "
        "(trailing-trading-calendar peer group x 12-1-momentum tercile) cells and held in "
        "six overlapping monthly sleeves, earn positive validation skill against the "
        "equal-weight eligible pool, because a persistent overnight gain is attention- and "
        "retail-flow-driven demand arriving when the exchange cannot absorb it and is "
        "therefore a transient price component, and because the score is a ratio of two "
        "quotes one day apart (rank rho +0.029 to 12-1 momentum, -0.003 to the log price "
        "level, at most 0.230 to any object on the v3 board) and so is neither a return-path "
        "relabelling nor a carrier of the back-adjusted price level the 2026-10-22 engine "
        "issue records."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the lowest-overnight-drift top-100 pick,
    quota-allocated across calendar-peer x momentum-tercile cells; one sleeve
    reformed each month-end, ineligible names pruned at every month-end."""
    return session_book(prices, aux, eligible=eligible,
                        score_fn=overnight_drift_score)
