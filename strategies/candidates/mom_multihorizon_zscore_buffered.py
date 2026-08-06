"""Z-score-weighted buffered momentum (tonight's best-yet result), but
ranking and weighting on a composite of two momentum horizons instead of
12-1 alone.

Every trial tonight has held the *selection signal* fixed (raw 12-1
momentum) and only changed how held names are weighted (equal -> rank ->
z-score magnitude), each an improvement. This candidate holds the
z-score-weighting mechanism fixed and instead changes the signal itself:
average the cross-sectional z-scores of 6-1 and 12-1 momentum into a single
composite score, used both for buffer-band ranking and for weighting.
Combining two lookback horizons is standard practice in the momentum
literature specifically to reduce horizon-specific noise (a name can look
strong on 12-1 momentum purely because of one now-stale quarter); the
hypothesis is that a steadier composite signal reduces false-positive
entries into the basket without giving up the return premium.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_multihorizon_zscore_buffered",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Ranking and weighting the buffered momentum basket (hold top 25, "
        "enter top 15) by a composite of 6-1 and 12-1 momentum z-scores, "
        "instead of 12-1 momentum alone, improves validation Sharpe over "
        "`mom_zscore_weighted_buffered`, net of 15 bps costs, because "
        "averaging two independent lookback horizons reduces horizon-"
        "specific noise in which names qualify for the basket."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
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
        held = (held & band) | core  # both subsets of band, so |held| <= BAND_N

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
