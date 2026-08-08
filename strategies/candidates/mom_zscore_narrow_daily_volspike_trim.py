"""Daily-reacting vol-spike exposure trim applied to the narrower, higher-
conviction 15/25 buffered basket instead of the 20/35 widebreadth one.

`mom_zscore_daily_volspike_trim_fixed` (trial #27) showed that re-evaluating
a basket-own realized-vol-spike exposure trim daily (instead of only at the
monthly rebalance) fixes the cadence problem that made the same trigger a
no-op at monthly frequency (trial #25): applied to the 20/35 widebreadth
basket it lifted validation Sharpe to 1.05 (from 1.03) while *also* cutting
maxDD to -29.5% (from -35.6%, and better than the champion's own -29.9%) —
the first challenger ever to improve both axes at once.

That trial used the widebreadth (hold-35/enter-20) basket. The repo's
single highest raw validation Sharpe before this line of work was actually
the narrower hold-25/enter-15 basket (`mom_multihorizon_zscore_buffered`,
val Sharpe 1.03, but with the worse -36.0% maxDD that widebreadth was
designed to dilute). This candidate holds the fast daily trim mechanism
completely fixed and only swaps back to the narrower core/band counts, to
test whether the trim's drawdown fix generalizes to a higher-conviction,
more concentrated basket too — i.e. whether the trim and the concentration
level are independent, additive levers, or whether the trim's benefit was
itself dependent on the extra breadth.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_narrow_daily_volspike_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Applying the same daily-reacting basket-own vol-spike exposure trim "
        "(21d/252d realized-vol ratio > 1.6 -> 0.6x exposure) to the "
        "narrower hold-25/enter-15 buffered z-score basket, instead of the "
        "hold-35/enter-20 widebreadth basket used in trial #27, improves "
        "validation Sharpe further (starting from a higher base of 1.03 vs "
        "1.03) while still meaningfully reducing that basket's maxDD from "
        "-36.0%, net of 15 bps costs, because the trim and the "
        "concentration level are independent levers."
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
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    base_periods = []  # (start_idx_pos, end_idx_pos_exclusive, norm)

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
        sub = prices.iloc[: end_pos][names]
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
