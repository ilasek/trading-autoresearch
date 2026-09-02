"""Is the max operator a union of tails, or a conditional allocator over them?

WHY THIS FILE EXISTS. Trial #70 refuted the winner's-curse account of
`pl_maxleg_signal_blend` (#68, validation 1.008) and then a free follow-up screen
refuted the account #68 itself gave. The lab had explained the operator ladder —
max 1.008 > max-of-rank 0.877 > k=2 0.753 > mean 0.635 — by "tail depth pays",
measured as the held book's mean score in its own raw units. Standardized, that
statistic is **flat**: over 325 month-ends the three z-based books all reach
1.46-1.56 cross-sectional SDs into their own score distribution, and its
correlation with Sharpe is **-0.053**. It has to be flat — all four books hold
the top ~20 of ~140 names, so they buy the same *quantile* by construction and
cannot differ in depth. `max-of-rank` settles it: shallowest standardized depth
of the four (1.127 SDs) and second-best Sharpe.

So the operators do not differ in how deep a tail they buy. They differ in
**which names the same quantile contains**, and the ladder still has to be
explained. This file tests the one account that survives the screen.

THE ACCOUNT. With legs that are near-orthogonal in the cross-section (mean |rho|
0.054 train / 0.070 validation, measured for #67), `max` holds a name if **any**
leg ranks it extreme — a union of the legs' own tails — and, crucially, the
number of names each leg contributes is **not fixed**: it varies month to month
with how extreme that leg's tail happens to be. Measured holdings-only over the
same 325 month-ends, the argmax share of the core-20 by leg is

    leg          illiq   seasonal   group_lead   reversal
    mean share   0.199     0.252       0.317       0.232
    sd of share  0.099     0.105       0.184       0.109

with a mean absolute deviation from an equal quarter of **0.104** and a single
leg reaching **0.850** of the book in one month. That date-conditioning is an
allocation rule with no estimated parameters, and nothing has tested whether it
is worth anything.

THE CONTROL. Take the **top 5 names from each leg** every month — a fixed 25%
share by name count, never varying — and hold the union. Same four legs, same
z-scoring, same joint-coverage rule, same hysteresis band (the union of each
leg's top 7), same equal weight, same monthly grid, same warmup. The *only*
thing removed is the conditioning: this book is the union of the legs' tails
with the per-leg quota frozen.

PREMISE AND COST, MEASURED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN:

    book              positions   turnover   HHI      overlap with #68
    max (#68)           22.6       14.55x   0.0446         --
    fixed share          20.4       14.14x   0.0492        0.745

Turnover is **matched and slightly lower** (14.14x against 14.55x) and breadth is
close (20.4 against 22.6), so this pair cannot be accused of measuring the
broker — the standing `learnings.md` rule after four consecutive trials in which
a turnover difference swamped the mechanism. A quarter of the book is re-drawn,
which is enough to score differently and correlated enough to resolve: at ~0.75
weight overlap the closed-form paired SE should run near 0.10.

PRE-REGISTERED, FALSIFIABLE, AND THE TWO OUTCOMES MEAN DIFFERENT THINGS.
*If the conditioning is the mechanism*, this book loses materially — it should
fall toward the 0.834 that the 2026-08-30 arithmetic bounds an ex-post-optimal
capital mix of these legs at, and well below 1.008.
*If the mechanism is simply "hold the union of the legs' tails"*, this book lands
near 1.008, the conditioning is decoration, and the lab gains a **simpler**
construction with no operator to overfit and one fewer arbitrary choice — which
after #69 (z versus rank, indistinguishable at t = +1.31) is worth more than the
0.02 of Sharpe it might cost.

**Pre-registered point estimate: 0.88.** That is the midpoint of the two
accounts, and it is deliberately not derived from a rate — the only rate the lab
had for this family was the depth rate #70 just voided, and inventing a
replacement from a single new pair would repeat the error. The trial buys the
sign and the size; it is not being asked to confirm an arithmetic.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. (n = 15 and unresolved;
the three `portfolio-learning` books that differ only by operator under-predicted
by +0.39, +0.26 and +0.15, while #67 was near-exact.)

SCOUT. It does not compete for the seat and cannot reach the holdout. The solved
required-leg-Sharpe bar for a resolvable blend is 1.34-1.42 against a 1.120
champion, and nothing on this board is near it.

WHY THE SELECTION IS INLINE. `strategies/lib/signal_blend.py` was written for #67
and #67, #68 and #70 have all been measured against it; adding a selection mode
would edit an existing lib file, which `CLAUDE.md` forbids because a promoted
candidate keeps importing it. The z-scoring and joint-coverage rule below are a
verbatim copy of #68's `_integrate_max` up to the point where the reduction
happens; the leg score functions are imported unchanged, so the books share their
inputs exactly.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_fixed_share_tails",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Holding the union of the top 5 names from each of the same four family-lead "
        "z-scores that trial #68 took the maximum of — a fixed 25% share per leg by name "
        "count — rather than letting the max operator vary each leg's contribution by "
        "date (measured argmax shares 0.199/0.252/0.317/0.232 with per-leg sd 0.10-0.18 "
        "and one leg reaching 0.850 of the book in a single month), and otherwise leaving "
        "that candidate bit-identical (same legs, same z-scoring, same joint-coverage "
        "rule, same hysteresis band, same equal weight, same monthly grid; turnover "
        "matched holdings-only at 14.14x against 14.55x and breadth at 20.4 against 22.6 "
        "names) scores near 0.88 on validation, materially below #68's 1.008, because the "
        "max operator's edge is the date-conditioning of the per-leg quota rather than the "
        "union of tails as such — the tail-depth account that had been credited with it is "
        "refuted by trial #70's follow-up screen, in which standardized book depth is flat "
        "at 1.46-1.56 SDs across every operator and correlates -0.053 with Sharpe."
    ),
}

CORE_N = 20
BAND_N = 30
WARMUP = 60                      # month-ends skipped; the seasonal leg needs the history
PER_LEG_CORE = CORE_N // 4       # 5 — the fixed quota this file exists to impose
PER_LEG_BAND = BAND_N // 4       # 7 — the same hysteresis, applied per leg


def _leg_zscores(scores: dict[str, pd.DataFrame], at: pd.Timestamp,
                 min_names: int = 20) -> pd.DataFrame | None:
    """#68's `_integrate_max` up to (but not including) its reduction.

    Each leg is z-scored within its own cross-section at `at`, and the frame is
    restricted to the instruments every leg can score, so no name enters on a
    partial set of legs. Reads only rows at or before `at`.

    One deviation from the copy, forced by needing the legs individually rather
    than reduced: the columns are keyed by leg name. `_integrate_max` concatenates
    unkeyed, which leaves all four columns labelled with the same rebalance date —
    harmless under `.max(axis=1)`, but this file selects columns by name.
    """
    zs: list[pd.Series] = []
    common: pd.Index | None = None
    for panel in scores.values():
        sub = panel.loc[:at]
        if sub.empty:
            return None
        row = sub.iloc[-1].dropna()
        if len(row) < min_names:
            return None
        sd = row.std(ddof=0)
        if not sd > 0:
            return None
        z = (row - row.mean()) / sd
        zs.append(z)
        common = z.index if common is None else common.intersection(z.index)

    if common is None or len(common) < min_names:
        return None
    return pd.concat([z.reindex(common) for z in zs], axis=1, keys=list(scores))


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
        frame = _leg_zscores(legs, dt)
        if frame is None or len(frame) < BAND_N:
            continue

        core: set[str] = set()
        band: set[str] = set()
        for col in frame.columns:
            ordered = frame[col].sort_values(ascending=False)
            core |= set(ordered.index[:PER_LEG_CORE])
            band |= set(ordered.index[:PER_LEG_BAND])

        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
