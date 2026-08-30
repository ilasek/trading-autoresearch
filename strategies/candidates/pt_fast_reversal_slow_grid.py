"""Signal horizon and rebalance frequency are separate choices, and the lab's
standing "reversal is untradeable here" conclusion conflates them.

THE CLAIM BEING TESTED. The 2026-08-29 session closed on: "the strongest signal
measurable on this universe sits exactly at the horizon the cost model
structurally forbids" — raw 5-10 day reversal, IC +0.0455 at 5 days, decaying to
a null by 21. `SUMMARY.md` #18's mechanism (the short-horizon premium pays
liquidity *providers*, and a book paying 15 bps a side is on the other side of
it) is about the *trading* horizon. The measurement behind "forbidden" is about
the *scoring* horizon. Those are not the same quantity, and nothing forces them
to be equal: a 5-day reversal score can be sampled on a monthly grid, in which
case the book pays monthly turnover while betting on a 5-day signal.

THE PREMISE, VERIFIED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN. On the
identical 20-enter/30-hold monthly book, changing only the score's lookback:

    score horizon   avg names   annual turnover   train Q5-universe (t)
     5d              24.3        11.82x            +7.23%/yr (3.83)
    10d              24.3        11.93x            +5.55%/yr (2.98)
    21d              24.3        11.93x            +2.50%/yr (1.27)

Turnover is flat because at ~21 trading days of spacing a 5-day, a 10-day and a
21-day window are all **fully disjoint** from their predecessor, so the book's
churn is set by the rebalance grid and not by the lookback. The cost objection to
the short horizon therefore does not apply to this construction at all.

WHAT IT DOES. `pt_raw_reversal_control` (trial #65, validation 0.701) with one
expression changed: the score is the negative 5-day return instead of the
negative 21-day return. Same band, same equal weight, same monthly grid, same
warmup, same universe. The pair is turnover-matched by measurement, not by
argument.

PRE-REGISTERED EFFECT, AND AN HONEST DISCOUNT ON IT. The train screen puts the
5-day score +4.72%/yr of Q5-universe spread ahead of the 21-day one. Tonight's
own trial #64/#65 pair calibrated that exchange rate for the first time and it is
brutal: +3.35%/yr of Q5 spread bought **+0.03** of train Sharpe and **-0.11** of
validation Sharpe, because a 20-name book with a hysteresis band holds a tail,
not a quintile. Applying that calibration here predicts roughly **+0.04** of
Sharpe — inside this construction's resolution floor. So the point estimate is
not the reason to run this; the reason is that the pair adjudicates a headline
conclusion in the journal, and both outcomes are informative:

  - lands materially above 0.701 → "the strongest signal is untradeable" is
    refuted, and it was a statement about the rebalance grid all along;
  - lands at or below 0.701 → the premium genuinely does require fast trading,
    because the excursion reverts inside the holding month and a monthly book
    collects only its front. That sharpens the standing claim rather than
    overturning it, and it is the first evidence for it that is not a cost
    argument.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below `pt_raw_reversal_control`'s
0.701.

CAVEATS RECORDED IN ADVANCE. (a) The margin is pre-registered as unresolvable
against this family's paired standard error; the trial is being spent on the
*sign* and on the mechanism question, which is the only condition
`learnings.md`'s own screening rule allows. (b) This is the session's second and
last `price-trend` slot under `program.md`'s cap. (c) It will correlate highly
with trial #65 and cluster with it in the deflator, so its marginal cost to the
bar is small — but it is a real trial and is recorded as one. (d) Equal weight
throughout, per `CLAUDE.md`'s prohibition on importing the magnitude-weighting
result across families — and, here, across mechanisms.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pt_fast_reversal_slow_grid",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "Fading the raw 5-day return on a monthly rebalance grid — the identical "
        "20-name hold-30/enter-20 equal-weight book as trial #65, which fades the "
        "21-day return — scores a validation Sharpe above that trial's 0.701 at "
        "the same annual turnover (11.82x against 11.93x, verified holdings-only "
        "on train, because at monthly spacing both lookback windows are fully "
        "disjoint from their predecessor), i.e. the short-horizon reversal premium "
        "the lab recorded as structurally untradeable is reachable once the "
        "scoring horizon is decoupled from the rebalance frequency."
    ),
}

REVERSAL_WIN = 5
CORE_N = 20
BAND_N = 30
WARMUP = 6


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    score = -(prices / prices.shift(REVERSAL_WIN) - 1.0)
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        row = score.loc[:dt].iloc[-1].dropna()
        if len(row) < BAND_N:
            continue
        ranked = row.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
