"""Multi-horizon z-score buffered momentum, with a square-root dampening
transform on the weighting spread.

Three consecutive trials tonight escalated capital concentration into the
strongest-momentum names (equal -> rank -> z-score magnitude -> two-horizon
composite z-score), each lifting validation Sharpe further but also
widening validation maxDD (-30.2% -> -32.4% -> -36.0%) and turnover (4.4x ->
6.1x -> 7.0x) in lockstep — and the DSR gain per trial started shrinking on
the last step. This candidate keeps the exact same selection signal and
buffer-band ranking as `mom_multihorizon_zscore_buffered` (so basket
membership is identical) and only applies a concave (square-root) transform
to the within-basket weight spread, compressing how much extra capital the
most extreme names receive relative to the rest of the held basket. This
tests a genuinely different lever — moderating concentration to reduce
variance/turnover — rather than a further escalation of it.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_multihorizon_zscore_damped_buffered",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Applying a square-root dampening transform to the within-basket "
        "weight spread of the two-horizon z-score-weighted buffered "
        "momentum basket (same selection and ranking as "
        "`mom_multihorizon_zscore_buffered`) achieves a higher deflated-"
        "Sharpe probability than the undamped version, net of 15 bps costs, "
        "because compressing (not eliminating) the tail of the weighting "
        "distribution reduces return variance and month-to-month turnover "
        "without discarding the magnitude-weighting benefit."
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
        damped = np.sqrt(raw)
        norm = damped / damped.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w = pd.Series(0.0, index=prices.columns)
        w[norm.index] = norm
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
