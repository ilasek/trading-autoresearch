"""Vol-spike exposure trim on the repo's leading momentum basket.

Base construction is unchanged from `mom_multihorizon_zscore_widebreadth`
(composite 6-1/12-1 z-score, buffered hold-35/enter-20 basket, magnitude
weighting) — val Sharpe 1.03, DSR 0.9277 at trial #24, matching the narrower
`mom_multihorizon_zscore_buffered`'s Sharpe (1.03, DSR 0.9333 at trial #21)
at lower turnover. Two prior sessions closed the sector-concentration and
name-breadth axes as explanations for this basket's rising validation maxDD
(-36.0% / -35.6% vs the champion's -29.9%): neither sector-neutralizing nor
widening the basket materially reduced it, pointing at the weighting
mechanism's tail behavior in a crash rather than insufficient diversification.

Every de-risking overlay tried before this was an *external trend* signal
(200dma on an ETF sleeve, a binary SPY-trend switch) that whipsawed in calm
markets because trend flips are frequent — that's why they all lost more
Sharpe to whipsaw than they saved in drawdown. This candidate uses a
structurally different, rarer trigger: the *basket's own* realized-volatility
regime. It measures the trailing 21-day realized vol of the basket's own
(already-selected) constituents against their trailing 252-day realized vol,
purely from price history up to each rebalance date, and only cuts gross
exposure when short-term vol has spiked well above its own long-run level —
the hallmark of an actual crash (e.g. 2008-09), not an ordinary trend
reversal. Selection, buffering, and within-basket weighting are all held
identical to the widebreadth base; only a single exposure scalar is added.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_volspike_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Scaling total exposure down (to 0.6x) only when the momentum "
        "basket's own trailing 21-day realized volatility exceeds 1.6x its "
        "trailing 252-day realized volatility — leaving exposure at 1.0x "
        "otherwise — reduces validation maxDD versus the unscaled "
        "`mom_multihorizon_zscore_widebreadth` basket without materially "
        "hurting validation Sharpe, net of 15 bps costs, because it targets "
        "genuine crash-level vol spikes rather than the frequent trend "
        "reversals that made every prior external-trend overlay whipsaw."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 20
BAND_N = 35
MAX_WEIGHT = 0.25
FLOOR = 0.05

VOL_SHORT = 21
VOL_LONG = 252
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def _exposure_scale(hist: pd.DataFrame, names: list) -> float:
    """Ratio of the basket's own trailing short-vs-long realized vol,
    using only price history up to and including the current row."""
    if len(hist) < VOL_LONG + 2:
        return 1.0
    sub = hist[names].dropna(axis=1, how="any")
    if sub.shape[1] == 0:
        return 1.0
    rets = sub.pct_change().dropna(how="all").mean(axis=1)
    if len(rets) < VOL_LONG:
        return 1.0
    vol_short = rets.iloc[-VOL_SHORT:].std(ddof=0)
    vol_long = rets.iloc[-VOL_LONG:].std(ddof=0)
    if vol_long <= 0:
        return 1.0
    ratio = vol_short / vol_long
    return TRIM_SCALE if ratio > SPIKE_RATIO else 1.0


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

        scale = _exposure_scale(hist, list(held))
        norm = norm * scale

        w = pd.Series(0.0, index=prices.columns)
        w[norm.index] = norm
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
