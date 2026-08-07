"""Wider-breadth variant of the repo's strongest challenger to date
(`mom_multihorizon_zscore_buffered`, val Sharpe 1.03, DSR 0.9333, unpromoted).

Tonight's first trial (`mom_multihorizon_zscore_sectorneutral`) tested whether
the validation maxDD growth across the weighting-intensity escalation
(-30.2% -> -36.0% over three trials, per learnings.md) was a sector-
concentration artifact — it wasn't: sector-neutralizing the composite score
cost far more Sharpe than the drawdown it saved and even raised turnover,
implying global top-momentum names already span sectors reasonably well and
the risk is coming from somewhere else.

The more obvious remaining candidate is plain basket breadth: the winning
basket still only ever holds 15-25 names out of a 140-instrument universe.
This candidate holds everything about `mom_multihorizon_zscore_buffered`
fixed — same two-horizon composite z-score, same buffering mechanism, same
weighting-by-magnitude — and only widens the core/band counts (15/25 ->
20/35, same ~1.67x band-to-core ratio), i.e. de-escalates concentration via
a lever nobody has swept yet, the mirror image of the (now-closed)
weighting-intensity escalation line. More names means any single name's
z-score swing moves less of the portfolio, which should directly reduce
maxDD and (per the standard momentum-turnover-vs-breadth tradeoff) also cut
turnover, at some cost to Sharpe from including weaker-conviction names.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_multihorizon_zscore_widebreadth",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Widening the buffered momentum basket from hold-25/enter-15 to "
        "hold-35/enter-20 (same composite 6-1/12-1 z-score ranking and "
        "magnitude-weighting as `mom_multihorizon_zscore_buffered`) reduces "
        "validation maxDD and turnover versus the narrower basket, at some "
        "Sharpe cost, because diluting single-name concentration is a "
        "structurally different risk-reduction lever than the (already "
        "explored and refuted) options of dampening the weight spread or "
        "sector-neutralizing the score, net of 15 bps costs."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 20
BAND_N = 35
MAX_WEIGHT = 0.25
FLOOR = 0.05


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
        norm = raw / raw.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w = pd.Series(0.0, index=prices.columns)
        w[norm.index] = norm
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
