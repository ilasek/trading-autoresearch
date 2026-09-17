"""The always-on control for `pl_factor_momentum_timed`. One node different.

THIS FILE IS THE OTHER HALF OF A DESIGNED PAIR and it exists to be subtracted.
It is `pl_factor_momentum_timed.py` with `_live_sleeves` replaced by "every
sleeve, always" and nothing else touched: same six pre-registered characteristics,
same twelve sleeves, same top-20 legs, same monthly grid, same warmup, same
equal-weight-across-sleeves-then-inside-sleeves construction, same shared library.
The two books differ at exactly one expression.

WHY A CONTROL IS WORTH A FULL TRIAL HERE, WHICH IS NOT OBVIOUS AND IS THE POINT.
`learnings.md` records, across four consecutive trials, that outside `price-trend`
a difference in turnover has dominated every mechanism comparison the lab tried to
run, and separately that a train advantage has ANTI-PREDICTED a validation
advantage three times out of three. Scoring only the timed book would produce a
level and no answer: a level cannot say whether the timing rule earned anything,
and this repo's own history says a train contrast is exactly the thing not to
extrapolate. The paired difference between two books this correlated is resolvable
on validation even though neither level is — which is the whole reason the pair is
worth two trials instead of one candidate and an argument.

Both outcomes are findings and both were written down before either book was
scored:

  * timed above untimed → the autocorrelation survives out of sample, and the
    lab has a mechanism that `learnings.md`'s five refuted vintage-averaging axes
    and its "blending beats switching" entry did not anticipate, because every
    overlay refuted here timed the book on an EXTERNAL state variable while this
    one times each component on its OWN past return.
  * untimed above timed → the published reexamination's central result is
    reproduced on this universe, `learnings.md`'s "blending beats switching"
    becomes stronger and more general (it now covers internal state too), and the
    train reading that motivated the pair joins the three-for-three
    anti-prediction record as a fourth instance. That is worth the trial.

PRE-REGISTERED, FALSIFIABLE: this book's train Sharpe, measured free before
either file existed, is **1.109** (against the timed book's 1.180 and the
equal-weighted universe's 1.045). Pre-registered validation Sharpe **0.75, range
0.45-1.10**, the same band as its partner because the pair differs only in which
sleeves are live and the sleeves are shared. Holdings-only pre-registration from
the train weight matrix: ~84 positions, mean top weight ~0.027, annual two-way
turnover ~3.5x. This is the LOWER-turnover half of the pair by construction, so
if it wins, the cost channel is the first thing to rule out and the gross
decomposition on train (+1.55%/yr to the timed book, against a ~0.36%/yr cost
difference) is already recorded in its partner's docstring for that purpose.

SCOUT, for the same reason as its partner: it never compares to the champion,
never reaches the holdout, and cannot end the session.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import sleeve_book as SB

STRATEGY = {
    "name": "pl_factor_momentum_untimed",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "The always-on control for `pl_factor_momentum_timed` — the same twelve "
        "characteristic sleeves (both legs of trend, reversal, Amihud illiquidity, "
        "Garman-Klass range volatility, volume shock and dollar-volume rank), equal "
        "weighted, every sleeve held every month — scores a validation Sharpe of 0.75 "
        "(range 0.45-1.10) and BELOW its timed partner, because a characteristic sort is "
        "positively autocorrelated in its own past return and dropping the sleeves whose "
        "own demeaned trailing 12-month return was negative is worth +1.55%/yr on train "
        "(t = +2.25) against a ~0.36%/yr cost difference; if this control wins instead, the "
        "published reexamination's result that timing does not beat buy-and-hold of the "
        "same factors is reproduced on this universe and `learnings.md`'s 'blending beats "
        "switching' extends from external state variables to a component's own past return."
    ),
}


def generate_weights(prices: pd.DataFrame, aux: dict[str, pd.DataFrame]) -> pd.DataFrame:
    _dates, members, sleeve_returns, _market = SB.build_sleeves(prices, aux)
    if sleeve_returns.empty:
        return pd.DataFrame(columns=prices.columns, dtype=float)

    all_sleeves = list(sleeve_returns.columns)
    return SB.book_weights(
        members,
        sleeve_returns,
        prices.columns,
        lambda _formation: all_sleeves,   # THE ONE NODE THAT DIFFERS
    )
