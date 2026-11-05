"""The paired control for `sc_overnight_drift_sleeves`: ONE node different.

WHAT THIS FILE IS FOR. The scout's score divides the overnight move by the day's
own trading range, which makes it a unit-free "what share of the travel was
overnight" quantity. The obvious alternative is to divide by the previous close,
which makes it a plain overnight RETURN -- and `experiments/learnings.md`
(2026-10-24/25) records the overnight leg of the short-horizon reversal as a
**pure null** on this panel, measured as a return.

This file is the scout with the normaliser swapped and every other node
identical: same 756-day window, same 21-day lag, same sign, same K=100, same
calendar-peer x momentum-tercile quota, same six overlapping sleeves, same
pruning, same warm-up handling. One node. So the pair measures on VALIDATION
whether the range normalisation is load-bearing, which is the design the lab has
used for #12/#13, #14/#15, #16/#17, #18/#19 and tonight's CLV pair.

TRAIN (free screen, 1997-2017 only, through `protocol.evaluate_split`; no
validation, holdout, forward or incubation number was read):

    book                                  net      gross    cost    turn   pos    volr   97-08   09-17
    range-normalised  (the scout)       +0.0310  +0.0370  -0.0060  1.34  138.1  0.954  +0.007  +0.022
    un-normalised RETURN  (this file)   +0.0250  +0.0320  -0.0070  1.39  140.7  0.947  -0.010  +0.021
    un-normalised RETURN, NEGATED       -0.0610  -0.0580  -0.0030  1.47  142.7  1.151  -0.023  -0.147

So on train the normalisation is worth **+0.006** of net skill and, more
interestingly, it is what makes 1997-2008 positive: the un-normalised version
reads **-0.010** there against the scout's +0.007, while 2009-2017 is the same to
0.001. That is the signature of a scale problem rather than a signal one -- an
un-normalised overnight return is dominated by whichever names were most volatile
in the window, and the panel's pre-2009 half is the thin, 97%-US half.

This control CLEARS the train-skill gate (+0.025 > 0), unlike tonight's CLV
control, so it is a live scout in its own right and not only a paired reading.
Its negation invariant passes as well (+0.025 against -0.061).

PRE-REGISTERED TURNOVER: train 1.39x, predicted validation band **1.6-2.1x**.
"""

from __future__ import annotations

from strategies.lib.session_split import session_book, session_return_score

STRATEGY = {
    "name": "sc_overnight_return_control",
    "family": "seasonality-calendar",
    "hypothesis": (
        "The identical lowest-overnight-session book with its normaliser changed from the "
        "day's own trading range to the previous close -- a plain overnight RETURN instead of "
        "a share of daily travel, every other node unchanged -- earns LOWER validation skill "
        "than the range-normalised version, because an un-normalised overnight return ranks "
        "names partly by their own volatility scale rather than by the share of their "
        "movement that happens out of hours, a defect already visible on train as a sign flip "
        "in the 1997-2008 sub-period (-0.010 against +0.007) while 2009-2017 is unchanged to "
        "0.001."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The scout's book with the range normaliser replaced by the previous close."""
    return session_book(prices, aux, eligible=eligible,
                        score_fn=session_return_score)
