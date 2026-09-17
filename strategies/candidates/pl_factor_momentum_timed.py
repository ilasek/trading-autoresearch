"""`research/SUMMARY.md` #115 — timing twelve long-only sleeves on their own past return.

ONE HALF OF A DESIGNED PAIR. Its partner `pl_factor_momentum_untimed.py` is this
file with `_live_sleeves` replaced by "always on" and NOTHING else changed. The
pair exists because the object under test is a CONTRAST, not a level, and because
`learnings.md` records that outside `price-trend` a train advantage has
anti-predicted a validation advantage three times out of three — the only way to
find out whether tonight's train contrast is the fourth is to score both books on
validation and read the paired difference, which is resolvable even where neither
level is.

THE MECHANISM (Ehsani-Linnainmaa via `SUMMARY.md` #114/#115). A characteristic
sort's own return series is positively autocorrelated, so a sub-portfolio can be
timed on its own trailing return without any belief about which leg is supposed
to pay. That model-freeness is the appeal: no expectation about the sign of any
of the six sorts enters this file. The long-only analogue of "take the short side
after the spread has been negative" is to hold the OTHER LEG, which is why there
are twelve sleeves and not six.

THE SCREEN, RUN FREE ON TRAIN BEFORE THIS FILE EXISTED, AND ITS PLACEBO. All
nodes below were pre-registered in `experiments/journal.md` under
"Pre-registration — 2026-09-17 (nightly)" before a single number was computed,
including the six-characteristic list, the twelve-sleeve construction, the
demeaning step and the two-sided decision rule. Train split only, gross, monthly:

    (a) untimed equal-weight 12            +18.13%/yr   sharpe +1.109
    (b) TIMED on own demeaned trailing 12m +19.68%/yr   sharpe +1.180
        paired (b) - (a)                    +1.55%/yr   t = +2.25
    CONTROL: identical rule, UN-demeaned   +17.42%/yr   sharpe +1.047

The control is the pre-registered rider and it behaves exactly as #114 predicts:
an un-demeaned long-only sleeve return is mostly the market, so timing on its
sign carries no cross-sleeve information and reads BELOW the untimed book. The
demeaning is the load-bearing step, not a cosmetic one.

    placebo (hash of (date, sleeve), hold rate matched at 0.521): -0.00%/yr,
    t = -0.01; over 40 independent draws mean +0.07%/yr, sd 0.49%/yr, and the
    observed +1.55%/yr sits at the 100th percentile. Clean.

    leave-one-characteristic-out, all six drops, timed minus untimed:
      trend +1.95 (t=+2.98) | reversal +1.96 (+2.53) | illiq +0.99 (+1.38)
      gkvol +1.32 (+1.68)   | volshock +1.63 (+2.22) | dvrank +1.37 (+1.85)

Every drop keeps the sign. That matters more than the headline: the published
reexamination's central complaint is that roughly a QUARTER OF FACTORS carry
essentially all of the effect, which is the selection the model-free claim has to
survive. Here no single characteristic carries it.

WHAT THE SCREEN DOES **NOT** SAY, STATED BEFORE THE NUMBER ARRIVES. The source's
peer-reviewed reexamination reports that the timed book does NOT beat buy-and-hold
of the same factors, on mean or Sharpe, in either of two samples. Tonight's train
reading disagrees with it. No performance expectation is imported from either
paper in either direction — the ordering was re-measured here and only the
ordering is at issue. `SUMMARY.md` flags the reexamination `validation_overlap:
true` (its sample runs to Dec 2020), which is a discount on its novelty, not a
reason to prefer this reading.

PRE-REGISTERED, FALSIFIABLE, AND RECORDED AS THIS SESSION'S TRAIN-AS-PREDICTION
ENTRY (`learnings.md`, 2026-08-30: every scout writes its train Sharpe down as a
prediction of its validation Sharpe, so the sign becomes readable at n ~ 25):

  * train Sharpe of this construction, measured free above: **1.18**.
  * pre-registered validation Sharpe **0.75, range 0.45-1.10**. The level is
    expected near the diversified floor rather than near the champion because
    this is a ~65-name book at a ~0.036 mean top weight — `learnings.md` prices
    breadth of that kind at the low end of the board, and no non-`price-trend`
    scout here has cleared 1.01. A reading above 1.10 should be treated as
    suspicious rather than as a win.
  * the quantity that actually matters: **validation Sharpe ABOVE its untimed
    partner**. Falsified if the paired difference is negative.
  * holdings-only pre-registration, from the train weight matrices: ~65
    positions (untimed ~84), mean top weight ~0.036 (untimed ~0.027), annual
    two-way turnover ~5.9x (untimed ~3.5x). A profile far from that means the
    file is not building the book the screen measured.

COST ARITHMETIC, STATED BECAUSE `learnings.md` RECORDS THAT OUTSIDE `price-trend`
TURNOVER DIFFERENCES HAVE DOMINATED EVERY MECHANISM COMPARISON THE LAB HAS RUN
(four consecutive trials, four times). The timing rule costs 2.4x of extra annual
turnover against its partner, which at 15 bps/side is ~0.36%/yr, against a gross
train gain of +1.55%/yr. The contrast therefore survives its own cost difference
by roughly 4:1 on train — but the pair is scored net by the engine, so the
decomposition is stated here rather than discovered afterwards.

SCOUT. `learnings.md`'s blend board is exhaustive and closed — no seated lead
reaches a third of a standard error against the champion — so a challenger needs
its own reason and this does not have one yet. As a scout it never compares to
the champion, never reaches the holdout, and cannot end the session.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import sleeve_book as SB

STRATEGY = {
    "name": "pl_factor_momentum_timed",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "A long-only book that equal-weights twelve characteristic sleeves (both legs of "
        "trend, reversal, Amihud illiquidity, Garman-Klass range volatility, volume shock "
        "and dollar-volume rank) but holds only those whose OWN trailing 12-month return, "
        "demeaned against the equal-weighted universe, was positive at formation scores a "
        "validation Sharpe of 0.75 (range 0.45-1.10) and, decisively, scores ABOVE its "
        "otherwise bit-identical always-on partner `pl_factor_momentum_untimed`, because a "
        "characteristic sort is positively autocorrelated in its own past return: on train "
        "the timed book beats the untimed one by +1.55%/yr (t = +2.25, Sharpe 1.180 vs "
        "1.109) with a hash placebo at the 100th percentile of 40 draws, the sign surviving "
        "all six leave-one-characteristic-out drops, and the pre-registered un-demeaned "
        "control reading BELOW the untimed book as the mechanism requires."
    ),
}


def _live_sleeves(signal: pd.DataFrame, formation: pd.Timestamp) -> list[str]:
    """Sleeves whose own demeaned trailing 12-month return was positive at `formation`.

    THE ONE NODE THAT DIFFERS FROM THE UNTIMED PARTNER. An empty selection falls
    back to the full sleeve set (handled by `book_weights`), so the book is never
    in cash and `min_active_days` is never at risk.
    """
    if formation not in signal.index:
        return []
    row = signal.loc[formation]
    return [s for s in signal.columns if pd.notna(row[s]) and row[s] > 0]


def generate_weights(prices: pd.DataFrame, aux: dict[str, pd.DataFrame]) -> pd.DataFrame:
    _dates, members, sleeve_returns, market = SB.build_sleeves(prices, aux)
    if sleeve_returns.empty:
        return pd.DataFrame(columns=prices.columns, dtype=float)

    signal = SB.timing_signal(sleeve_returns, market)
    return SB.book_weights(
        members,
        sleeve_returns,
        prices.columns,
        lambda formation: _live_sleeves(signal, formation),
    )
