"""The ladder's intercept: what does this book score when NONE of its legs
reads market data?

WHY THIS FILE EXISTS. Tonight's trial #76 completed the union leg-count ladder,
and the completed ladder is the reason for this control:

    legs   book                                    validation
    1      seasonal alone                (#72)        0.782
    2      + reversal / suv / placebo (#73-#75)   0.786 / 0.913 / 0.799   (mean 0.833)
    3      + illiq + group_lead          (#76)        0.889
    4      all four                      (#71)        0.958

Monotone on all four rungs, and a straight line through the rung means fits at
**slope +0.0582 per leg with a maximum residual of 0.0052**. That looks like a
leg-count effect. But every adjacent step is unresolvable — #76 vs #72 is
t = +0.56, #71 vs #76 is t = +0.56, #71 vs #72 is t = +1.04 — and the 2-leg rung
is an average over three partners whose spread (0.127) exceeds the whole
1-leg-to-4-leg gap's own standard error, with a **placebo partner that reads no
market data buying +0.017 against a real-content partner's +0.004**.

That last fact is what this file is about. If the arms of the 2-leg rung cannot
tell a real leg from a hash of the date and the ticker, then the ladder's slope
may not be measuring signal combination at all. There is a competing account
that predicts the same monotone shape:

  * **Signal.** Each added leg contributes a real, weak, independently-timed
    tail; more legs, more of it; the intercept at zero legs is far below 0.782.
  * **Selection is worth nothing here.** The book is ~20 equally-weighted names
    drawn from a ~47-name joint-coverage pool of large global instruments over a
    strong validation window, and *any* draw from that pool scores in this band.
    Then the four rungs are four draws from one distribution and the line through
    them is a line through noise.

**Nothing in this family distinguishes those two accounts, and one trial does.**
Replace all four scores with pseudo-random orderings and hold the machinery
otherwise bit-identical. The ladder's own linear fit puts the zero-leg intercept
at **0.720**; the second account puts this book among the rungs.

WHAT IS AND IS NOT HELD FIXED. The four real legs still define the **joint
coverage pool** — each placebo is masked to exactly the names its corresponding
real leg can score at that date — so the pool, the month window and the warmup
are identical to #71's and only the *within-leg ordering* is replaced. This
matters: `learnings.md` (2026-09-01) measured the machinery-and-coverage
confound at +0.036, so leaving coverage free would put a known effect inside an
unknown one.

CHURN, MATCHED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN. A placebo redrawn
every month churns 16.23x against #71's 11.98x; redrawn every second month,
staggered across the four legs, it churns 9.19x. Measured grid:

    redraw          months  first        positions  turnover
    #71 real legs     253   1996-12-31     20.10     11.98x
    every month       253   1996-12-31     19.53     16.23x
    every 2, aligned  253   1996-12-31     19.46      8.04x
    every 2, staggered253   1996-12-31     19.11      9.19x   <- THIS
    every 3           253   1996-12-31     19.12      6.40x

The staggered two-month redraw is the closest reachable match (2.79x away
against the monthly draw's 4.25x) and it is chosen on that criterion alone. It
leaves the placebo a **cost advantage of about 0.42%/yr, ~0.024 of Sharpe**,
which is stated here rather than netted out, and which runs in the direction
that makes a *low* score for this book the decisive result.

PRE-REGISTERED POINT ESTIMATE: **0.75** — the ladder's own fitted intercept of
0.720 plus the 0.024 the churn match hands the placebo. This is the signal
account's prediction, and it is what the trial is set up to falsify. A book
landing at or above ~0.85 would sit inside the rungs it is supposed to lie below,
and would say that the span from one leg to four is not attributable to the legs:
the whole `portfolio-learning` result — including the 1.008 that is the best
non-`price-trend` number this lab has ever recorded — would then have to be
re-read as what a ~20-name equal-weight draw from this pool does over this
window, and the family should be closed rather than extended.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. n = 21 outside
`price-trend`, still unresolved. This candidate is the one case where the two
splits' disagreement would be especially informative, since a contentless book
has no reason to prefer either.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import hashlib

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import union_legs as UL
from strategies.lib import walkforward as W

REDRAW_MONTHS = 2                       # matched on churn, see the grid above
OFFSETS = {"seasonal": 0, "illiq": 1, "group_lead": 2, "reversal": 3}

STRATEGY = {
    "name": "pl_zeroleg_all_placebo",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "A four-leg fixed-quota union book in which every one of the four family-lead "
        "scores is replaced by a deterministic pseudo-random ordering that reads no market "
        "data — while the real legs still define the joint-coverage pool, so the month "
        "window (253 months from 1996-12-31), warmup, band, equal weighting and monthly grid "
        "are bit-identical to trial #71 and only the within-leg ordering changes, with churn "
        "matched holdings-only in advance at 9.19x against 11.98x and breadth at 19.11 "
        "against 20.10 names — scores near 0.75 on validation, at the zero-leg intercept of "
        "the completed leg-count ladder (0.782/0.833/0.889/0.958 at one to four legs, a "
        "straight line of slope +0.0582 per leg with maximum residual 0.0052 and fitted "
        "intercept 0.720, plus the 0.024 of Sharpe the churn match hands the placebo), "
        "because the ladder's slope reflects real if individually unresolvable content in "
        "the legs. Landing at or above roughly 0.85 instead would place a book with no "
        "signal whatever inside the rungs it should lie below, and would mean the family's "
        "entire one-leg-to-four-leg span — and the 1.008 that is this lab's best "
        "non-price-trend result — is not attributable to the legs but to what any ~20-name "
        "equal-weight draw from this pool earns over this window."
    ),
}


def _placebo(prices: pd.DataFrame, salt: str, offset: int) -> pd.DataFrame:
    """Pseudo-random cross-sectional ordering, redrawn every `REDRAW_MONTHS`.

    Reads no market data: the value for (bucket, name) is a hash of those two
    strings mapped into [0, 1). Causal by construction (there is nothing to peek
    at) and exactly reproducible under the protocol's truncated re-runs, since
    the bucket is a function of the calendar month alone and not of the frame.
    `hashlib` rather than `numpy.random` so the value depends only on the key and
    not on any global stream state or draw order.
    """
    rows: dict[pd.Timestamp, pd.Series] = {}
    cols = list(prices.columns)
    for dt in W.rebalance_dates(prices):
        bucket = (dt.year * 12 + dt.month - 1 + offset) // REDRAW_MONTHS
        key = f"{salt}|{bucket}"
        rows[dt] = pd.Series(
            [int(hashlib.sha256(f"{key}|{c}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
             for c in cols],
            index=cols,
        )
    if not rows:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    real = {
        "seasonal": SB.seasonal_score(prices),
        "illiq": SB.illiquidity_score(prices, aux["dollar_volume"], 63),
        "group_lead": SB.group_lead_score(prices, 21),
        "reversal": SB.reversal_score(prices, 21),
    }
    legs = {}
    for name, panel in real.items():
        p = _placebo(prices, name, OFFSETS[name])
        # Coverage — and only coverage — is inherited from the real leg, so the
        # joint pool this book selects within is #71's own.
        legs[name] = p.where(panel.reindex_like(p).notna())
    return UL.fixed_quota_union(prices, legs)
