"""Tail-preserving integration: score each name by its BEST leg, not its mean leg.

THE DESIGNED PAIR. This file is `pl_integrated_signal_blend` (trial #67) with
**one operator changed** — `mean` becomes `max` over the same four legs'
cross-sectional z-scores. Same four legs, same z-scoring, same joint-coverage
rule, same core-20 / band-30 equal-weight monthly construction, same warmup,
same universe. Everything that is not the aggregation operator is bit-identical,
which is the design template `learnings.md` prescribes after four consecutive
trials in which a turnover difference swamped the mechanism being tested.

WHAT #67 MEASURED, AND WHY IT POINTS HERE. #67 confirmed `SUMMARY.md` #60's
premise (the legs' cross-sectional signal ranks correlate at mean |rho| 0.054
train / 0.070 validation, an order of magnitude below the 0.68-0.98 the family's
closure was measured on) and still scored **0.635**, below all four of its legs.
A free post-hoc diagnostic found the reason: averaging `n` near-orthogonal
z-scores shrinks the composite's cross-sectional dispersion by ~`1/sqrt(n)`, so
#67's top-20 sat at mean z **+0.491 (train) / +0.685 (validation)** on its own
score against each leg's own top-20 at **+1.096 / +1.476** — ratios of 0.45 and
0.46 against the 0.50 exact orthogonality predicts. It bought a tail less than
half as deep as any leg's, and this repo has already established that these
signals pay *only* in their extreme tails (`pt_raw_reversal_control` scores
validation 0.701 on a 21-day reversal whose cross-sectional IC is a null,
+0.0102 at t = +0.97).

THE PREMISE, VERIFIED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN. The max
operator restores tail depth and then some, because the maximum of four draws is
more extreme than any one of them: mean z of the held top-20 on its own score is
**+1.948 (train) / +2.210 (validation)**, against each leg's own +1.096 / +1.476
and #67's +0.491 / +0.685 — a ~4x move in the intended direction. Turnover is
matched by prior measurement rather than argued clean afterwards: monthly core-20
churn 0.571 against #67's 0.580 on train and 0.715 against 0.744 on validation,
i.e. ~13.7x vs ~13.9x and ~17.2x vs ~17.8x annual before the band. The books are
genuinely different (top-20 overlap with #67 of 0.614 / 0.469), and no single leg
dominates the selection — the share of held names supplied by each leg's argmax
runs 0.206 / 0.240 / 0.331 / 0.224 on train and 0.178 / 0.294 / 0.270 / 0.258 on
validation — so this is not one leg's book wearing four labels.

TWO COMPETING MECHANISMS, STATED IN ADVANCE, AND THE TRIAL SUPPLIES THE SIGN.
*(a) Tail depth pays.* If #67's deficit is tail dilution, restoring depth should
recover it, and this book should beat 0.635 and plausibly the best single leg's
0.747, since its tail is deeper than any leg's own.
*(b) The max operator selects on noise.* The maximum of `n` noisy z-scores is the
winner's curse in closed form: a name with one spuriously extreme draw is
selected on that draw alone, and the more orthogonal the legs the more
independent bites at a false extreme each name gets. Under this reading the
deeper tail is deeper *noise* and the book loses.
These predict opposite signs from the same measured premise, which is what makes
the trial worth its slot rather than a knob-turn.

PRE-REGISTERED, FALSIFIABLE: this book beats #67's **0.635**. Landing at or below
falsifies (a), and the family then closes on all three aggregation objects — the
capital mix (bounded by arithmetic, 2026-08-30), the mean-score integration
(#67), and the tail-preserving integration (here) — which is a complete negative
rather than a partial one.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe: whatever train Sharpe this
book records is the prediction for its validation Sharpe. (#67's call was
0.636 -> 0.635, the closest agreement in the series so far.)

BOUNDARY STATED HONESTLY. Max-integration sits *between* #67 and the capital mix
the 2026-08-30 arithmetic already bounded: "hold a name if any leg loves it" is
closer to a union of the legs' tails than a mean-score book is. It is not the
same object — the operator lets whichever leg has the deeper tail on a given date
supply more names, which no fixed capital allocation does, and the measured leg
shares vary by date — but if it loses, part of the reason may be that bound
reasserting itself rather than mechanism (b), and the two are not separable by
this trial alone.

SCOUT. It does not compete for the seat and will not reach the holdout: the
solved required-leg-Sharpe bar is 1.34-1.42 against a 1.120 champion, and nothing
on this board is near it.

WHY THE REDUCTION IS INLINE RATHER THAN A PARAMETER ON `signal_blend.integrate`.
`strategies/lib/signal_blend.py` was written for #67 and #67 has now been
measured against it and recorded in `trials.jsonl`. Adding a `reduce=` argument
would be editing an existing lib file, which `CLAUDE.md` forbids for exactly this
reason — a lib edit silently changes an already-measured strategy. `_integrate_max`
below is a verbatim copy of `signal_blend.integrate` with `sum(...)/len(...)`
replaced by an element-wise maximum, and nothing else; the leg score functions are
imported unchanged, so the two books really do share their inputs.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_maxleg_signal_blend",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Scoring each name by the MAXIMUM of the same four family-lead z-scores that "
        "trial #67 averaged — Amihud illiquidity, same-calendar-month seasonality, "
        "sector-group 21-day lead-lag and 21-day reversal — and otherwise leaving that "
        "candidate bit-identical (same legs, same joint-coverage rule, same "
        "hold-30/enter-20 equal-weight monthly book, turnover matched holdings-only at "
        "13.7x against 13.9x on train) scores a validation Sharpe above its 0.635, "
        "because #67's deficit was tail dilution — averaging four near-orthogonal "
        "z-scores cut the held book's own-score depth to +0.491 against each leg's "
        "+1.096, and the max operator restores it to +1.948 — and these signals are "
        "measured to pay only in their extreme tails."
    ),
}

CORE_N = 20
BAND_N = 30
WARMUP = 60          # month-ends skipped; the seasonal leg needs the history


def _integrate_max(scores: dict[str, pd.DataFrame], at: pd.Timestamp,
                   min_names: int = 20) -> pd.Series:
    """`signal_blend.integrate` with the mean replaced by an element-wise max.

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
    return pd.concat([z.reindex(common) for z in zs], axis=1).max(axis=1)


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
        score = _integrate_max(legs, dt)
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
