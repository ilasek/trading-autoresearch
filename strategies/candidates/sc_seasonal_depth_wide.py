"""The wide arm. Without it the narrow arm is a point, not a bracket.

`learnings.md` records the reading rule for a concentration axis explicitly —
**read the shape, never the levels** — because band variants of one score
correlate 0.96-0.99 and no single gap between them is resolvable. The
`liquidity-volume` bracket (0.874 / 0.917 / 0.942 across a 3x breadth span) is
quoted for its monotone ordering and for nothing else. This arm supplies the
third point that makes tonight's reading the same kind of object.

THE CLAIM UNDER TEST, restated from `sc_seasonal_depth_narrow`. 2026-09-08
proposed each score's own depth profile as the mechanism deciding whether
breadth helps, with the rule **breadth beyond where a score's marginal slices go
flat is dilution**. It was fitted on the two brackets that already existed
(`liquidity-volume` monotone up, `price-trend` monotone down) and had never
predicted one. Measured free on the seated seasonal book's own union-joint pool
before either file was written (train, forward 21d, equal-weight slice excess,
placebo = hash of (rebalance date, ticker) reading no market data):

    score                     1-10        11-15       16-20       21-30       31-45       46-62
    same-minus-other month  +11.48(5.75) +1.70(0.81) -0.08(-0.04) -3.77(-2.05) +0.17(0.13) -1.62(-1.25)
    [ctl] placebo hash       -0.89(-.59) -2.49(-1.12) +4.07(1.74) +1.44(0.87) +0.08(0.06) -2.24(-1.77)

The narrow arm has since landed **0.846** against the seated **0.782**, so the
"narrowing helps" half is in. The prediction that can still fail — and the half
that distinguishes a real profile from a one-sided lucky draw — is that pushing
the band the *other* way, into slices measured at -3.77 and +0.17 and -1.62,
**loses**.

THIS CANDIDATE is `sc_seasonal_matched_control` with the identical single node
moved in the opposite direction: CORE_N 20 -> 30, BAND_N 30 -> 45. Signal,
union-joint coverage test, warmup and equal weighting all bit-identical, exactly
as in the narrow arm.

BREADTH AND CHURN, PINNED ON VALIDATION (2026-09-08 rule), all measured
holdings-only before this file was written:

    core/band   val names   val turnover
       10/15      10.41        20.70x    narrow arm, landed 0.846
       20/30      21.16        18.97x    seated,            0.782
       30/45      32.96        17.03x    this arm

Note the direction of the cost handicap **reverses** between the arms: widening
*saves* 1.94x of annual turnover (~0.58%/yr, ~0.03 Sharpe) where narrowing paid
1.73x. Both arms therefore have costs working against the hypothesis, which is
the useful design property — the bracket cannot be a turnover artifact in either
direction, and `learnings.md` records four consecutive non-`price-trend` trials
where turnover differences swamped the mechanism under test.

PRE-REGISTERED, FALSIFIABLE: **0.72** (range 0.65-0.80). Arithmetic: cumulative
top-k train excess falls +6.14%/yr at k=20 to ~+3.0%/yr at k=33, so widening
gives back ~-3.1%/yr of gross mean, ~-2.5 net of the churn saving, worth ~-0.13
of Sharpe at this book's ~0.19 validation vol; against that, the concentration
credit for a 1.56x widening is ~+0.08 at the `liquidity-volume` bracket's
implied rate. Net -0.06 on the seated 0.782.

**The falsification is sharp and is the point of running this.** If this arm
lands at or above 0.782 the ordering is not monotone, the seasonal book has no
depth-driven optimum, and tonight's narrow result becomes a single draw inside a
standard error rather than a bracket — in which case the 2026-09-08 mechanism has
failed its first prospective test and must be recorded as failing it. The lab's
own record says this matters: five "live" averaging axes lost after passing their
screens, and `learnings.md` states flatly that a screen should be used to kill,
never to promote.

TRAIN SHARPE IS AGAIN NOT RECORDED AS A PREDICTION, prospectively and for the
same measured reason as the narrow arm: the joint pool averages 73.1 names on
train against 133.8 on validation, so month-ends scoreable at band 15 / 30 / 45
are **318 / 253 / 202**. This arm's train Sharpe sits on the shortest and latest
of the three windows and is not comparable to the others (2026-09-04). Validation
is **72 of 72 at every band**, which is why the whole bracket is quoted there.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sc_seasonal_depth_wide",
    "family": "seasonality-calendar",
    "track": "scout",
    "hypothesis": (
        "Widening the seated seasonal lead's inherited band from core-20/band-30 to "
        "core-30/band-45 — the identical single node the narrow arm moved, in the opposite "
        "direction, with signal, union-joint coverage test, warmup and equal weighting "
        "bit-identical — scores BELOW its 0.782 on validation (registered at 0.72), because "
        "the free train depth profile on that book's own pool puts the marginal excess of the "
        "slices this arm adds at -3.77%/yr (t = -2.05, ranks 21-30), +0.17 (31-45) and -1.62 "
        "(46-62), so the added names subtract mean the concentration credit cannot repay; a "
        "landing at or above 0.782 would break the bracket's monotonicity and record the "
        "2026-09-08 depth-profile mechanism as having failed its first prospective test."
    ),
}

CORE_N = 30          # seated book: 20. The one node this arm moves.
BAND_N = 45          # seated book: 30. The one node this arm moves.
WARMUP = 60          # unchanged
MIN_NAMES = 20       # unchanged — the union book's joint-coverage minimum per leg


def _score_from(legs: dict[str, pd.DataFrame], at: pd.Timestamp) -> pd.Series:
    """The seasonal leg's score at `at`, restricted to the names EVERY leg of the
    union book can score on that date.

    Imported unchanged from `sc_seasonal_matched_control`, so this arm, the
    narrow arm and the seated book differ in nothing but CORE_N/BAND_N. Reads
    only rows at or before `at`.
    """
    common: pd.Index | None = None
    seasonal: pd.Series | None = None
    for key, panel in legs.items():
        sub = panel.loc[:at]
        if sub.empty:
            return pd.Series(dtype=float)
        row = sub.iloc[-1].dropna()
        if len(row) < MIN_NAMES or not row.std(ddof=0) > 0:
            return pd.Series(dtype=float)
        if key == "seasonal":
            seasonal = row
        common = row.index if common is None else common.intersection(row.index)

    if common is None or seasonal is None or len(common) < MIN_NAMES:
        return pd.Series(dtype=float)
    return seasonal.reindex(common)


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
        score = _score_from(legs, dt)
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
