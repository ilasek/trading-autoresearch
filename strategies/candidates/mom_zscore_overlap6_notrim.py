"""Does the daily vol-spike trim still earn its keep once overlap has widened
the book?

Two established results collide here. Trial #30 showed the daily-reacting
vol-spike trim is a near no-op on baskets that are not vol-spiky in the first
place: applied to the plain equal-weight buffered basket it changed Sharpe,
maxDD and turnover by rounding error, because that basket's own 21d/252d
realised-vol ratio rarely crosses 1.6. Trial #34 then showed that the
overlapping-tranche construction works largely by widening *effective* book
breadth — and trial #35 pushed average positions to 34.2, more than double
the 15 the trim was originally designed around.

A 34-name, temporally-averaged book is much closer in character to the
diversified basket the trim was inert on than to the concentrated one it was
built for. So the current best challenger may be carrying an overlay that no
longer does anything — or worse, one that still fires occasionally and costs
turnover for it.

This candidate is `mom_zscore_overlap6_daily_trim` with the trim removed
entirely and nothing else changed: same 12-1/6-1 composite, same
hold-25/enter-15 buffer, same magnitude weighting, same six overlapping
monthly tranches, monthly rows only.

This is an ablation with real stakes rather than a search for a better
number. If Sharpe and maxDD are unchanged, the trim is dead weight and every
future candidate on this line should drop it — a simpler strategy at equal
performance is strictly preferable and removes a component that could be
overfit. If Sharpe or maxDD degrade materially, the trim is still live
despite the wider book, and the earlier "only works on vol-spiky baskets"
learning needs qualifying: overlap would then be widening name count without
actually damping the book's own vol spikes.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_notrim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Removing the daily-reacting vol-spike exposure trim from the "
        "six-tranche overlapping basket, with signal, buffer, weighting and "
        "tranche structure otherwise identical to trial #35, leaves "
        "validation Sharpe and maxDD statistically indistinguishable from "
        "that version's 1.11 and -29.1%, net of 15 bps costs, because a "
        "34-name temporally-averaged book is no longer vol-spiky enough for "
        "the 1.6x ratio trigger to fire meaningfully."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 6


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    recent_targets = []

    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK_LONG + SKIP + 1:
            continue
        mom_long = _momentum(hist, LOOKBACK_LONG)
        mom_short = _momentum(hist, LOOKBACK_SHORT)
        common = mom_long.index.intersection(mom_short.index)
        if len(common) < CORE_N:
            continue

        composite = _zscore(mom_long[common]) + _zscore(mom_short[common])
        ranked = composite.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core

        c_held = composite[list(held)]
        raw = c_held - c_held.min() + FLOOR
        target = raw / raw.sum()

        recent_targets.append(target)
        if len(recent_targets) > N_TRANCHES:
            recent_targets.pop(0)

        blended = pd.concat(recent_targets, axis=1).fillna(0.0).mean(axis=1)
        norm = blended / blended.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full

    return pd.DataFrame.from_dict(rows, orient="index")
