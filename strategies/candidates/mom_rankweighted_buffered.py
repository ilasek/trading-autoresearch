"""Buffered 12-1 momentum (the repo's best-yet challenger), but with capital
tilted toward the strongest names in the held basket instead of equal-weighted.

Every prior attempt to move capital *away* from the highest-momentum names
(inverse-vol weighting, low-vol double-sort) refuted itself by discarding the
pool's strongest compounders. This candidate tests the opposite direction:
does tilting *more* capital toward the strongest-ranked names in the buffer
band (rank-weighting instead of equal-weighting), while still holding the
same basket, improve on `mom_12m_buffered`'s 0.90 validation Sharpe? This
isolates the weighting-scheme change alone — buffer bands, lookback, and
universe are identical to `mom_12m_buffered`, so any Sharpe delta is
attributable to the weighting mechanism, not a different signal or basket.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_rankweighted_buffered",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Within the buffered 12-1 momentum basket (hold top 25, enter top "
        "15), weighting held names linearly by momentum rank (more capital "
        "to the strongest-ranked names, less to the weakest-ranked) improves "
        "validation Sharpe over equal weighting, net of 15 bps costs, "
        "because it concentrates capital in the pool's strongest compounders "
        "instead of diluting it equally across the full hold band."
    ),
}

LOOKBACK = 252
SKIP = 21
CORE_N = 15
BAND_N = 25


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK + SKIP + 1:
            continue
        past = hist.iloc[-(LOOKBACK + SKIP) - 1]
        recent = hist.iloc[-SKIP - 1]
        momentum = (recent / past - 1).dropna()
        if len(momentum) < CORE_N:
            continue

        ranked = momentum.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core  # both subsets of band, so |held| <= BAND_N

        held_ranked = momentum[list(held)].sort_values(ascending=False)
        k = len(held_ranked)
        raw = pd.Series(range(k, 0, -1), index=held_ranked.index, dtype=float)  # k..1

        w = pd.Series(0.0, index=prices.columns)
        w[raw.index] = raw / raw.sum()
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
