"""Buffered 12-1 momentum, weighted by cross-sectional momentum z-score
magnitude instead of ordinal rank.

`mom_rankweighted_buffered` showed that tilting capital toward the
strongest-ranked names in the buffered basket (instead of equal-weighting)
lifted validation Sharpe from 0.90 to 0.93 — the repo's best result so far.
But ordinal rank weighting treats a runaway winner and a name that barely
edged out its neighbor identically (both just move one rank). This
candidate keeps the same buffer band, lookback, and universe, and only
swaps the weighting *basis*: weight by how far above the cross-sectional
mean each held name's momentum z-score is, so a name with an unusually
large momentum lead gets proportionally more capital than one that merely
ranks higher by a hair. This isolates whether magnitude (not just order)
carries additional signal.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_weighted_buffered",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Within the buffered 12-1 momentum basket (hold top 25, enter top "
        "15), weighting held names by cross-sectional momentum z-score "
        "magnitude (rather than ordinal rank) improves validation Sharpe "
        "over rank-weighting, net of 15 bps costs, because it gives "
        "proportionally more capital to names with an unusually large "
        "momentum lead instead of treating all rank gaps as equal."
    ),
}

LOOKBACK = 252
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05  # minimum z-shift above the weakest held name, keeps it non-zero


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

        mu, sigma = momentum.mean(), momentum.std(ddof=0)
        z = (momentum - mu) / sigma if sigma > 0 else momentum * 0.0

        ranked = momentum.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core  # both subsets of band, so |held| <= BAND_N

        z_held = z[list(held)]
        raw = z_held - z_held.min() + FLOOR
        norm = raw / raw.sum()
        # one cap-and-renormalize pass; held-set sizes here never concentrate
        # enough to need iterating
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w = pd.Series(0.0, index=prices.columns)
        w[norm.index] = norm
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
