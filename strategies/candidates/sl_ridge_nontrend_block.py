"""Does a learner do better once the incumbent's own features are taken away?

THE QUESTION. Trial #56 (`sl_ridge_xs_walkforward`) gave a ridge eleven features,
three of which were the champion's own lookbacks (12-1, 6-1, 3-1). It scored
validation 0.601 at **rho 0.774** — the highest correlation to the champion of
any non-`price-trend` result on the board — and the journal's reading was that a
learner fed the incumbent's features rediscovers the incumbent, worse.
`research/SUMMARY.md` #50 says the same thing from the literature: penalised
linear models' variable importance is "highly skewed toward momentum and
reversal", so if the point of a learned candidate is a *decorrelated* leg, the
trend features have to be removed deliberately, because the estimator will not
do it for you. This candidate removes them and nothing else that matters.

THE FEATURE BLOCK IS MEASURED, NOT LISTED. Every candidate feature was screened
on the train split tonight (free, holdings-only, no returns scored): rank-IC
against the 21-day forward return, averaged over ~310 month-ends. What the
screen found, in order:

    market residual reversal 21d   IC +0.0175  t=+1.75
    same-calendar-month seasonal   IC +0.0208  t=+2.27
    volume shock 63d               IC -0.0159  t=-2.01   (enters negated)
    Amihud ILLIQ 63d               IC +0.0118  t=+1.18
    --- dropped, with reasons ---
    momentum 12-1 / 6-1 / 3-1      IC +0.0204 / +0.0039 / +0.0027  (the incumbent's)
    Garman-Klass vol 21d / 252d    IC -0.0438 / -0.0439, t <= -2.9
    GK vol compression             IC -0.0014  t=-0.15   (null)
    dollar-volume rank             IC +0.0010  t=+0.11   (null)

Two of those drops are judgement calls and are stated as such. The **volatility
level** has by far the largest |IC| in the whole screen, and its sign says high
volatility *wins* by ~7.5%/yr on train. That is the survivorship signature read
directly — this universe contains the volatile names that survived — so giving
it to a learner would buy a book that harvests the bias and calls it alpha. It
is excluded on that reasoning, not on its statistics, and the reasoning is
falsifiable by anyone who wants to include it. The **5-10 day residual
reversal** is the strongest genuine signal measured tonight (IC +0.0400,
t = +4.22 at 10 days) and is also excluded: at that horizon the premium is
compensation for *providing* liquidity, and a book paying 15 bps a side is on
the other side of that trade (`SUMMARY.md` #18). The 21-day residual is kept
because it is the horizon at which the effect is weak enough to be about
something else and slow enough to trade monthly.

THE TURNOVER FIX, WHICH IS THE OTHER HALF OF THE TRIAL. #56 paid ~2.3%/yr —
about a third of its whole margin over the equal-weight floor — to a monthly
re-rank of the entire cross-section, because nothing in its construction asked
its holdings to be stable. Two changes here, both cheap: the model is fitted
against the rank of the **63-day** forward return rather than the 21-day one,
so the target itself moves more slowly, and the book carries an enter-20 /
hold-35 hysteresis band with equal weights instead of re-deriving magnitude
weights from a fresh score every month.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below #56's recorded **0.601**.
That is a deliberately harder bar than the 0.49 equal-weight floor: the claim is
not "a learner finds something" — #56 already established that — but "the
incumbent's features were subtracting from the learner". A second reading is
pre-registered and is worth as much: **rho to the champion should fall well
below 0.774.** If Sharpe rises and rho falls, the family has an ensemble leg
worth developing. If Sharpe falls and rho falls, the trend features were
carrying the result and this family's independent content is thin. If rho stays
near 0.774 with the trend features gone, then the remaining features are
themselves trend in disguise, which would be the most interesting outcome of
the three.

CAVEATS. (a) The feature block was chosen on the train split, which is what the
train split is for, but it does mean this is a *selected* four-tuple and its
validation number carries that. (b) The seasonal feature uses the corrected
target-month alignment established in trial #60, not the one shipped in
`strategies/lib/features.py`. (c) Ridge, single-threaded, closed-form, no seed
to forget — deterministic by construction, per `CLAUDE.md`'s causality note.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sl_ridge_nontrend_block",
    "family": "statistical-learning",
    "track": "scout",
    "hypothesis": (
        "A ridge over four causal NON-trend features — same-calendar-month seasonal, "
        "Amihud illiquidity, volume shock and 21-day market-residual reversal, each "
        "measured on the train split to carry independent univariate information — "
        "refitted monthly walk-forward against a 63-day forward-return rank and traded "
        "as a banded equal-weight top-20 book, beats the 0.601 recorded by the "
        "eleven-feature ridge that included the champion's own 12-1/6-1/3-1 lookbacks, "
        "at a materially lower correlation than that trial's rho 0.774 — i.e. the "
        "incumbent's features were subtracting from the learner rather than adding."
    ),
}

HORIZON = 63          # forward-return rank the model is fitted against
CORE_N = 20
BAND_N = 35
ALPHA = 10.0
MIN_TRAIN_ROWS = 2000
WARMUP = 60           # month-ends skipped; the seasonal feature needs the history

ANN_YEARS = 20
NON_MONTHS = 240
MIN_SAME = 5


def _seasonal_panel(prices: pd.DataFrame) -> pd.DataFrame:
    """Same-calendar-month return minus other-month return, for the month about
    to start, published on each month-end rebalance row.

    Alignment note: the target month is taken with `MonthBegin(1)`, because a
    rebalance date is the last *trading* day of a month and `MonthEnd(1)` would
    return the month that has just ended on ~30% of them (trial #59/#60)."""
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    month_pos = {p: i for i, p in enumerate(monthly.index.to_period("M"))}

    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in W.rebalance_dates(prices):
        i = month_pos.get(dt.to_period("M"))
        if i is None or i < MIN_SAME * 12:
            continue
        past = mret.iloc[:i]                       # strictly before the current month
        target = (dt + pd.offsets.MonthBegin(1)).month
        same = past[past.index.month == target].tail(ANN_YEARS)
        other = past[past.index.month != target].tail(NON_MONTHS)
        if len(same) < MIN_SAME or len(other) < 24:
            continue
        score = same.mean() - other.mean()
        rows[dt] = score.where(same.notna().sum() >= MIN_SAME)

    if not rows:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    frame = pd.DataFrame(rows).T
    return frame.reindex(index=prices.index, columns=prices.columns).ffill()


def _feature_panels(prices: pd.DataFrame, aux: dict) -> dict[str, pd.DataFrame]:
    raw = {
        "seasonal": _seasonal_panel(prices),
        "illiq_63": F.amihud_illiquidity(prices, aux["dollar_volume"], 63),
        "vshock_63": -F.volume_shock(aux["volume"], 63),
        "resid_21": -F.market_residual_return(prices, 252, 21),
    }
    return {name: F.xs_rank(frame) - 0.5 for name, frame in raw.items()}


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    dates = W.rebalance_dates(prices, warmup=WARMUP)
    scores = W.walk_forward_scores(
        feature_panels=_feature_panels(prices, aux),
        target=W.rank_target(prices, HORIZON),
        dates=dates,
        horizon=HORIZON,
        fit_predict=W.ridge_fit_predict(ALPHA),
        min_train_rows=MIN_TRAIN_ROWS,
    )

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()
    for dt, row in scores.iterrows():
        s = row.dropna()
        if len(s) < BAND_N:
            continue
        ranked = s.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
