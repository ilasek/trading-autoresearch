"""Does the max operator buy conviction, or the winner's curse? The k=2 control.

THE QUESTION THIS ANSWERS. `pl_maxleg_signal_blend` (#68, validation 1.008) is
the best non-`price-trend` result the lab has recorded, and its own file states
two mechanisms it could not separate:

  (a) *tail depth pays* — the book buys a deeper tail than any leg's own, and
      these signals are measured to pay only in their extreme tails;
  (b) *the max operator selects on noise* — the maximum of `n` noisy z-scores is
      the winner's curse in closed form, and a name with one spuriously extreme
      draw is selected on that draw alone.

#69 checked one incidental choice (z versus rank) and converted the headline
into a range, 0.88-1.01. It did not touch (a) versus (b), and every idea the
2026-08-31 session listed for raising this leg's own Sharpe assumes (a) is the
answer. Nothing has tested that. This file does, with the one control that is
parameter-free.

THE CONTROL, AND WHY IT IS NOT A KNOB. Score each name by the **second-largest**
of the same four leg z-scores rather than the largest. `k` indexes an order
statistic, not a threshold: k=1 is #68's max, k=4 is the min, and #67's mean is
off the ladder entirely. Moving k=1 -> k=2 changes exactly one thing — a name
now needs **two** legs to endorse it rather than one — which is (b)'s mechanism
stated as a construction. There is no constant to choose and nothing to tune.

THE TWO MECHANISMS PREDICT OPPOSITE SIGNS, which is what makes this worth a slot
rather than a decoration. Under (a) the k=2 book must lose: its tail is
shallower by construction. Under (b) it must win: it keeps the disjunctive
breadth that beat the mean while discarding the names held on a single lucky
draw.

PREMISE AND COST, MEASURED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN (325
month-ends, no returns scored):

    book        positions   turnover   depth on the max scale   overlap with #68
    k=1 (#68)     22.6       14.55x          +2.136                  --
    k=2 (here)    22.7       13.18x          +1.676                 0.435
    k=3           22.5       14.69x          +1.407                 0.294
    mean (#67)    22.5       15.15x          +1.783                 0.487

Two things that matter. Breadth is **bit-identical** (22.7 against 22.6) and
turnover is **lower, not higher** (13.18x against 14.55x), so this is the first
scout in this line that cannot be accused of measuring the broker — the standing
`learnings.md` rule after four consecutive trials in which a turnover difference
swamped the mechanism. And the book is genuinely re-drawn: 0.435 weight overlap
with #68, so the two operators select different names from bit-identical inputs.

PRE-REGISTERED, FALSIFIABLE. The one calibration the lab has for "depth pays" is
#67 -> #68: validation book depth +0.685 -> +2.210 moved validation Sharpe 0.635
-> 1.008, i.e. 0.245 Sharpe per unit of depth. At that rate k=2's measured depth
deficit of -0.460 predicts **0.895**, plus ~0.012 for the turnover it saves:
**this book scores 0.91**. Landing at or below that confirms (a) and refutes (b),
and #68's 1.008 survives as a conviction effect. Landing materially **above
1.008** confirms (b), and the lab's best non-`price-trend` result is partly a
winner's curse that a free construction change removes.

Stated honestly: the calibration rate is a **single point** spanning a 3.2x depth
change, used here on a 0.2x one, and `learnings.md` records repeatedly that a
constant measured on one construction is a property of that construction. The
number 0.91 is a stake in the ground, not a forecast; **the sign is what this
trial buys**, and the two mechanisms disagree about the sign.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. (The series stands at
n = 14 and unresolved; #67 was near-exact, #68 and #69 under-predicted by +0.39
and +0.26.)

SCOUT. It does not compete for the seat and cannot reach the holdout. The solved
required-leg-Sharpe bar for a resolvable blend is 1.34-1.42 against a 1.120
champion, and nothing on this board is near it — including, on either reading,
the leg this file is a control on.

WHY THE REDUCTION IS INLINE. `strategies/lib/signal_blend.py` was written for #67
and both #67 and #68 have been measured against it; adding a `reduce=` argument
would edit an existing lib file, which `CLAUDE.md` forbids because a promoted
candidate keeps importing it. `_integrate_kth` below is #68's `_integrate_max`
with the element-wise maximum replaced by the k-th largest, and nothing else. The
leg score functions are imported unchanged, so the two books share their inputs
exactly.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_second_best_leg",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Scoring each name by the SECOND-largest of the same four family-lead z-scores "
        "that trial #68 took the maximum of — Amihud illiquidity, same-calendar-month "
        "seasonality, sector-group 21-day lead-lag and 21-day reversal — and otherwise "
        "leaving that candidate bit-identical (same legs, same joint-coverage rule, same "
        "hold-30/enter-20 equal-weight monthly book, breadth matched holdings-only at "
        "22.7 against 22.6 names and turnover LOWER at 13.18x against 14.55x) scores at "
        "or below 0.91 on validation, because #68's advantage is tail depth rather than "
        "noise-robustness: the k=2 book's depth on the max scale is +1.676 against "
        "#68's +2.136, and the lab's one calibration of depth (0.245 Sharpe per unit, "
        "from #67 -> #68) prices that deficit at -0.113. Scoring materially above "
        "#68's 1.008 instead would show the max operator was selecting on single "
        "spuriously extreme draws — the winner's-curse mechanism #68 stated and could "
        "not test."
    ),
}

CORE_N = 20
BAND_N = 30
WARMUP = 60          # month-ends skipped; the seasonal leg needs the history
K = 2                # order statistic: 1 is #68's max, 4 would be the min


def _integrate_kth(scores: dict[str, pd.DataFrame], at: pd.Timestamp,
                   k: int = K, min_names: int = 20) -> pd.Series:
    """#68's `_integrate_max` with the maximum replaced by the k-th largest.

    Identical in every other respect: each leg is z-scored within its own
    cross-section at `at`, and the reduction is taken over the instruments every
    leg can score, so no name enters on a partial set of legs. Reads only rows at
    or before `at`.
    """
    zs: list[pd.Series] = []
    common: pd.Index | None = None
    for panel in scores.values():
        sub = panel.loc[:at]
        if sub.empty:
            return pd.Series(dtype=float)
        row = sub.iloc[-1].dropna()
        if len(row) < min_names:
            return pd.Series(dtype=float)
        sd = row.std(ddof=0)
        if not sd > 0:
            return pd.Series(dtype=float)
        z = (row - row.mean()) / sd
        zs.append(z)
        common = z.index if common is None else common.intersection(z.index)

    if common is None or len(common) < min_names:
        return pd.Series(dtype=float)
    frame = pd.concat([z.reindex(common) for z in zs], axis=1)
    ordered = np.sort(frame.to_numpy(), axis=1)[:, ::-1]      # descending
    return pd.Series(ordered[:, k - 1], index=common)


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "illiq": SB.illiquidity_score(prices, aux["dollar_volume"], 63),
        "seasonal": SB.seasonal_score(prices),
        "group_lead": SB.group_lead_score(prices, 21),
        "reversal": SB.reversal_score(prices, 21),
    }

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = _integrate_kth(legs, dt)
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
