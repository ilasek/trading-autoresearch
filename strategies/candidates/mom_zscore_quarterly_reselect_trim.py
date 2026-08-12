"""Quarterly (instead of monthly) re-evaluation of basket membership and
weights — the slower half of the selection-cadence question opened by trial #33.

Trial #33 moved the selection grid the *fast* way (weekly) and lost on both
axes: turnover more than doubled, but about half the return damage was a worse
gross signal rather than costs — near the buffer edges a weekly ranking of a
6-12 month trend is dominated by short-horizon price noise. If sampling the
signal more often adds variance without information, sampling it less often
should reduce that variance, and it also directly attacks the biggest remaining
inefficiency in the best challenger: its 7.3x annual validation turnover, worth
roughly 1.1pp of annual return at 15 bps/side.

This candidate changes exactly ONE thing versus
`mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07, maxDD
-30.3%, turnover 7.3x, DSR 0.9326): the rebalance grid is quarter-end rather
than month-end. The composite 12-1/6-1 z-score signal, the hold-25/enter-15
buffer band, the magnitude weighting, the 25% cap and the daily-reacting
vol-spike trim are all identical — note in particular that the trim still
reacts daily, so slowing the *selection* down does not slow down the
crash-response mechanism, which is what made a slow-reacting overlay fail in
earlier sessions.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_quarterly_reselect_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Re-evaluating the buffered composite-z-score basket's membership and "
        "magnitude weights quarterly instead of monthly — every other element "
        "of trial #28 held identical, including the daily-reacting vol-spike "
        "trim — raises validation Sharpe above its 1.07, net of 15 bps costs, "
        "because a 6-12 month trend signal is sampled with less noise at a "
        "slower grid (the mechanism that made weekly reselection lose gross "
        "return in trial #33) while annual turnover falls well below 7.3x."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
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


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="QE")).tail(1).index
    rows = {}
    held = set()
    base_periods = []

    all_dates = prices.index
    for i, dt in enumerate(rebalance_dates):
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

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full

        start_pos = all_dates.get_loc(dt)
        next_dt = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else None
        end_pos = all_dates.get_loc(next_dt) if next_dt is not None else len(all_dates)
        base_periods.append((start_pos, end_pos, norm))

    if not base_periods:
        return pd.DataFrame.from_dict(rows, orient="index")

    last_scale = 1.0
    for start_pos, end_pos, norm in base_periods:
        names = list(norm.index)
        sub = prices.iloc[:end_pos][names]
        avail = sub.dropna(axis=1, how="any").columns
        if len(avail) == 0:
            continue
        rets = sub[avail].pct_change()
        basket_ret = rets.mean(axis=1)
        vol_short = basket_ret.rolling(VOL_SHORT).std(ddof=0)
        vol_long = basket_ret.rolling(VOL_LONG).std(ddof=0)
        ratio = vol_short / vol_long
        scale_series = (ratio > SPIKE_RATIO).map({True: TRIM_SCALE, False: 1.0})
        scale_series = scale_series.where(vol_long > 0, 1.0)

        day_scales = scale_series.iloc[start_pos:end_pos]
        for dt2, scale in day_scales.items():
            if pd.isna(scale):
                scale = 1.0
            if dt2 in rows:
                rows[dt2] = rows[dt2] * scale
                last_scale = scale
                continue
            if scale != last_scale:
                w_full = pd.Series(0.0, index=prices.columns)
                w_full[norm.index] = norm * scale
                rows[dt2] = w_full
                last_scale = scale

    return pd.DataFrame.from_dict(rows, orient="index")
