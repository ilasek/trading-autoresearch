"""Daily-reacting vol-spike exposure trim on the repo's leading momentum basket.

Same base construction and same trigger *mechanism* as
`mom_zscore_volspike_trim` (trailing 21d vs 252d realized vol ratio of the
basket's own held constituents, cutting exposure to 0.6x above a 1.6x ratio)
— but that trial's diagnostic showed the monthly-rebalance cadence was the
actual problem, not the trigger itself: across 513 months of history it only
fired twice inside the whole validation window (2018-02, 2020-03), and by the
time a *month-end* row could react, most of the drawdown (e.g. most of the
2020-03 COVID crash) had already happened — a full month plus the engine's
1-day execution lag late. Basket *composition* (selection, buffering,
magnitude-weighting) still only updates monthly, exactly as in the
widebreadth base; this candidate only changes the exposure scalar to be
re-evaluated and (sparsely) re-emitted on every trading day the trim state
actually flips, so a crash-level vol spike can cut exposure within a day or
two instead of waiting for the next month-end. This isolates cadence as the
variable under test, not the trigger's sensitivity.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_daily_volspike_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "The same basket-own-vol-spike exposure trim as "
        "`mom_zscore_volspike_trim` (21d/252d realized-vol ratio > 1.6 -> "
        "0.6x exposure), re-evaluated daily instead of only at the monthly "
        "rebalance, reduces validation maxDD more effectively because it can "
        "react to a crash-level vol spike within days rather than waiting up "
        "to a month, net of 15 bps costs."
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

    # Daily exposure scale: for each period, compute trailing vol ratio of the
    # period's own held names, using only price data up to and including each
    # day (causal), and emit an extra sparse row only when the trim state flips.
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
                # month-end rebalance row already present; apply scale to it
                rows[dt2] = rows[dt2] * scale
                last_scale = scale
                continue
            if scale != last_scale:
                w_full = pd.Series(0.0, index=prices.columns)
                w_full[norm.index] = norm * scale
                rows[dt2] = w_full
                last_scale = scale

    return pd.DataFrame.from_dict(rows, orient="index")
