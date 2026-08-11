"""Nearness-to-52-week-high cross-sectional signal, in place of return-
magnitude momentum, using the same buffer + z-score-magnitude weighting
mechanism as the repo's strongest untrimmed challenger.

Every prior escalation on this basket (buffering, magnitude weighting, wide
breadth, sector-neutral scoring) reused the same underlying signal: a
composite z-score of trailing total returns over two horizons. The learnings
file explicitly flags that "a completely different signal source... has not
been tried." Nearness to the 52-week high (price / trailing-252d rolling
max) is a well-documented alternative momentum proxy (George & Hwang 2004)
that is structurally different from return magnitude: it is bounded, driven
by the *distance from a reference price* rather than the *size of the past
return*, and empirically captures slow information diffusion in a way that
sometimes dominates plain return momentum, especially around continuation
after consolidation near highs.

This candidate swaps the composite return z-score for a composite z-score of
52-week-high proximity (long: 252d window, short: 126d window, mirroring the
existing long/short structure) while keeping every other mechanism —
buffer band, z-score-magnitude weighting, skip-month — identical to
`mom_multihorizon_zscore_buffered` (val Sharpe 1.03 untrimmed). No vol-spike
trim is applied here: this trial isolates whether the new signal is
competitive as a base signal before combining it with any overlay.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_52wkhigh_zscore_buffered",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Ranking and magnitude-weighting the buffered basket (hold-25/"
        "enter-15) by a composite z-score of nearness-to-52-week-high "
        "(252d and 126d trailing windows) instead of trailing total return "
        "achieves validation Sharpe competitive with the return-based "
        "composite z-score basket (1.03), net of 15 bps costs, because "
        "52-week-high proximity is a documented alternative momentum proxy "
        "distinct from return magnitude."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05


def _high_proximity(hist: pd.DataFrame, lookback: int) -> pd.Series:
    recent = hist.iloc[-SKIP - 1]
    window = hist.iloc[-(lookback + SKIP) - 1 : -SKIP]
    high = window.max()
    return (recent / high).dropna()


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
        prox_long = _high_proximity(hist, LOOKBACK_LONG)
        prox_short = _high_proximity(hist, LOOKBACK_SHORT)
        common = prox_long.index.intersection(prox_short.index)
        if len(common) < CORE_N:
            continue

        composite = _zscore(prox_long[common]) + _zscore(prox_short[common])
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

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full

    return pd.DataFrame.from_dict(rows, orient="index")
