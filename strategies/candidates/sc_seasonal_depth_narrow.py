"""The depth-profile mechanism's first PROSPECTIVE test, in a third family.

WHAT IS BEING TESTED, AND WHY IT IS NOT A BAND SWEEP. 2026-09-08 found the
mechanism behind a puzzle two sessions had left open: a concentration
calibration is "a property of a construction, not of a family or a score"
(widening monotonically GOOD in `liquidity-volume`, 0.874/0.917/0.942 across a
3x breadth span; every HHI-lowering axis LOSING in `price-trend`). The proposed
mechanism is each score's own depth profile — marginal excess by rank slice —
with the rule **breadth beyond where a score's marginal slices go flat is
dilution**. It was fitted on the two families whose brackets already existed.
It has never been asked to predict one.

`seasonality-calendar` is the clean prospective case, because its seated lead
`sc_seasonal_matched_control` (val 0.782, 21.14 names) did not choose its band
at all: CORE_N=20/BAND_N=30 was **inherited verbatim from the union book's
machinery**, where the file's own docstring says it was adopted "not [this
signal's] recorded 25/45". That is exactly the situation `learnings.md`
2026-09-04 warns about — "any book here whose operator restricts its pool should
have its band re-bracketed rather than inherited" — and the band has never been
re-bracketed since.

PREMISE, MEASURED FREE BEFORE THIS FILE WAS WRITTEN (train, forward 21d,
equal-weight slice excess over **the seated book's own union-joint pool**, not
the full cross-section the 2026-09-08 table used; the placebo is a hash of
(rebalance date, ticker) reading no market data):

    score                     1-10        11-15       16-20       21-30       31-45       46-62
    same-minus-other month  +11.48(5.75) +1.70(0.81) -0.08(-0.04) -3.77(-2.05) +0.17(0.13) -1.62(-1.25)
    [ctl] placebo hash       -0.89(-.59) -2.49(-1.12) +4.07(1.74) +1.44(0.87) +0.08(0.06) -2.24(-1.77)

**The content is over by rank 15, and the 21-30 slice — which the seated band
reaches into — is significantly NEGATIVE.** The placebo shows no ordered
structure, which is what licenses reading the seasonal row as a shape. This is a
sharper profile than the 2026-09-08 full-pool reading (+4.54/-0.78/-0.87/-1.74)
because the joint pool is smaller and the tail is correspondingly deeper.

THIS CANDIDATE is `sc_seasonal_matched_control` with **one pair of constants
changed** — CORE_N 20 -> 10, BAND_N 30 -> 15 — and nothing else: same signal
imported unchanged from `strategies/lib/signal_blend.py`, same union-joint
coverage test, same warmup, same equal weighting. Its wide-arm twin
`sc_seasonal_depth_wide` (30/45) is the other side of the bracket. Per
`SUMMARY.md` #94 the two arms differ from the seated book at a single node.

BREADTH AND CHURN, PINNED ON VALIDATION — the split the comparison will be read
on, per the 2026-09-08 rule that #85 cost a trial to learn:

    core/band   val names   val turnover      (train names / turnover)
       10/15      10.41        20.70x            10.99 / 17.12x
       20/30      21.16        18.97x   seated   23.66 / 13.74x
       30/45      32.96        17.03x            36.07 / 12.44x

Narrowing therefore carries a **cost handicap of +1.73x annual turnover, ~0.52%/yr
at 15 bps, ~0.026 of Sharpe**, working against the hypothesis. Reported rather
than designed away, per the standing rule.

PRE-REGISTERED, FALSIFIABLE: **0.89** (range 0.80-0.98). Arithmetic, stated so it
can be wrong in a legible way. Cumulative top-k excess on train runs +11.48%/yr
at k=10 against +6.14 at k=20, so narrowing buys ~+5.4%/yr of gross mean, ~+4.9
net of the churn handicap, worth ~+0.26 of Sharpe at this book's ~0.19 validation
vol. Against that, `liquidity-volume`'s own bracket prices the pure concentration
penalty of narrowing at roughly **-0.23 Sharpe per 3x** (there, a 3x narrowing
lost 0.068 while GAINING ~3.1%/yr of mean); a 2.03x narrowing here is ~-0.15.
Net +0.11 on the seated 0.782.

**What the trial is actually asked for is the SIGN, and the claim is the ordering
narrow > seated > wide** — deliberately the OPPOSITE ordering to the one measured
in `liquidity-volume` across the same axis, predicted in advance from nothing but
the two scores' depth profiles. No single gap here will be resolvable: band
variants of one score correlate 0.96-0.99, and at `rho` 0.96 the closed-form
paired SE is 0.114, so +0.11 is ~1 SE. `learnings.md` 2026-09-04 states the
reading rule for exactly this design: **read the shape, never the levels.**

TRAIN SHARPE IS NOT RECORDED AS A PREDICTION, and the reason is prospective
rather than discovered afterwards. A band change silently changes the train
sample here (2026-09-04): the joint pool averages 73.1 names on train against
133.8 on validation, so month-ends scoreable at each band run **318 / 253 / 202**
for band 15 / 30 / 45 — the three arms are measured on three different train
windows. Validation is **72 of 72 at every band**, which is why the bracket is
quoted there alone and why the train-as-prediction record is held at n = 28.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sc_seasonal_depth_narrow",
    "family": "seasonality-calendar",
    "track": "scout",
    "hypothesis": (
        "Narrowing the seated seasonal lead's inherited band from core-20/band-30 to "
        "core-10/band-15, with the signal, the union-joint coverage test, the warmup and the "
        "equal weighting all bit-identical, scores ABOVE its 0.782 on validation (registered "
        "at 0.89), because a free train depth profile on that book's own pool puts the "
        "score's marginal excess at +11.48%/yr in ranks 1-10, +1.70 in 11-15, -0.08 in 16-20 "
        "and -3.77 (t = -2.05) in 21-30 — so the inherited band reaches into slices that "
        "subtract — and this is the first prospective test of the 2026-09-08 rule that "
        "breadth beyond where a score's marginal slices go flat is dilution, predicting here "
        "the OPPOSITE bracket ordering to the one that rule was fitted on in "
        "`liquidity-volume`, despite a +1.73x turnover handicap against the hypothesis."
    ),
}

CORE_N = 10          # seated book: 20. The one node this arm moves.
BAND_N = 15          # seated book: 30. The one node this arm moves.
WARMUP = 60          # unchanged
MIN_NAMES = 20       # unchanged — the union book's joint-coverage minimum per leg


def _score_from(legs: dict[str, pd.DataFrame], at: pd.Timestamp) -> pd.Series:
    """The seasonal leg's score at `at`, restricted to the names EVERY leg of the
    union book can score on that date.

    Imported unchanged from `sc_seasonal_matched_control` so that this arm and
    the seated book differ in nothing but CORE_N/BAND_N. Reads only rows at or
    before `at`.
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
