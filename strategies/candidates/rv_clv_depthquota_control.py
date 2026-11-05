"""The paired control for `rv_clv_momneutral_overlap6`: ONE node different.

WHAT THIS FILE IS FOR. The CLV score shares a mean rank rho of **+0.439** with
12-1 momentum over 252 train month-ends -- a name that trended up closes near
its highs. The shipped scout answers that by crossing its quota with momentum
terciles, inside which the rho falls to +0.063. That makes the scout a CLV claim
rather than a momentum relabelling *by construction*, but it leaves the
interesting question untested: is the momentum-neutralisation the thing carrying
the book, or is it incidental?

This file is byte-identical to the scout except for the second quota axis:
price-history-DEPTH terciles -- the axis every recorded M3 trial of this lab uses
-- instead of momentum terciles. Same score, same window, same lag, same K, same
peer grouping, same sleeve rule, same pruning, same warm-up handling. One node.

So the pair measures the momentum-neutralisation node on VALIDATION rather than
asserting it from a train table, which is the design the lab has used for
#12/#13, #14/#15, #16/#17 and #18/#19.

TRAIN (free screen, 1997-2017 only, through `protocol.evaluate_split`; no
validation, holdout, forward or incubation number was read):

    book                                      net      gross    cost    turn    pos
    peer x momentum tercile  (the scout)    +0.0070  +0.0120  -0.0050   1.50   145.1
    peer x depth tercile     (this file)    -0.0170  -0.0150  -0.0020   1.35   129.5
    peer x depth tercile, score NEGATED     -0.0860  -0.0810  -0.0050   1.25   131.1

**This file is EXPECTED TO GATE_FAIL and that is not a defect.** Train skill is
-0.017, below `min_train_skill = 0.0`, so the verdict is a foregone conclusion
and the trial's value is entirely in the validation and null columns it records
alongside its pair. It is shipped as a control, declared as one before it ran,
and its recorded verdict should be read that way.

WHAT THE TRAIN TABLE ALREADY SAYS, pending the paired validation reading. The
depth-quota book is 0.024 of net and 0.027 of gross WORSE than the
momentum-quota book on the identical score, so on train the momentum content
inside CLV is a DRAG rather than the source of the result -- which is what the
rest of this lab's record predicts, since momentum's own top-100 slice loses
11-20 bps per 63 days at every horizon from 21 to 252 days on this panel
(2026-10-09/10). The negation invariant passes on this axis too (-0.017 against
-0.086), so the sign of the CLV score does not depend on which second axis the
quota uses.

PRE-REGISTERED TURNOVER: train 1.35x, predicted validation band **1.6-2.0x**.
"""

from __future__ import annotations

from strategies.lib.clv_book import clv_book

STRATEGY = {
    "name": "rv_clv_depthquota_control",
    "family": "range-variance",
    "hypothesis": (
        "The identical low-closing-location-value top-100 book, with its quota crossed "
        "against price-history-depth terciles instead of 12-1-momentum terciles and every "
        "other node unchanged, earns LOWER validation skill than the momentum-neutral "
        "version, because leaving the score's +0.439 rank correlation to 12-1 momentum "
        "un-neutralised imports a momentum tilt whose own top-100 slice loses 11-20 bps "
        "per 63 days at every horizon on this panel -- a drag already visible on train at "
        "-0.017 against +0.007, which this pair tests for transfer rather than assuming."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The scout's book with the second quota axis changed to price-history depth."""
    return clv_book(prices, aux, eligible=eligible, cells="depth")
