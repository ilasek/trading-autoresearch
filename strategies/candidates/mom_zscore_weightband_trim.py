"""No-trade band on weights: the untested counterpart to membership buffering.

Trial #17 (`mom_12m_buffered`) produced the largest single improvement in this
repo's history by refusing to trade on small signal moves — replacing a hard
top-15 cutoff with a hold-25/enter-15 hysteresis band cut turnover from 5.8x
to 4.4x *and* raised Sharpe. But that buffer only governs *membership*. Once a
name is in the basket, every subsequent rebalance resets its magnitude weight
to the new target in full, however little its composite z-score moved. On the
current best challenger (`mom_zscore_narrow_daily_volspike_trim`, trial #28)
turnover is 7.3x — noticeably higher than the equal-weight buffered basket's
4.4x — and the difference is precisely this weight churn among names that
never left the basket. At 15 bps per side that is roughly 2.2% of annual
return spent on rebalancing, against a +27.0% gross-of-nothing result.

This candidate applies the same hysteresis logic one level down. At each
monthly rebalance the previous target weights are drifted forward by realized
price moves and renormalized (an approximation of where the book actually sits
before trading). A held name's weight is only moved to its new target if the
gap exceeds BAND; otherwise the drifted weight is left alone. Entries and
exits are unaffected — membership is still governed by the existing 25/15
buffer, and the daily vol-spike exposure trim is unchanged.

Everything else is identical to trial #28, so the comparison isolates one
mechanism. The band is set at 2 percentage points of portfolio weight, roughly
a third of the average position size in an ~18-name basket: large enough to
absorb ordinary month-to-month z-score jitter, small enough that a name whose
signal genuinely strengthens still gets re-weighted within a rebalance or two.

The bull case is that most weight churn is noise in the z-score rather than
information, so suppressing it recovers cost with little signal loss. The bear
case is that magnitude weighting is exactly where four prior trials found the
return comes from (0.90 -> 0.93 -> 0.98 -> 1.03 as capital tilted harder toward
the strongest names), so damping its responsiveness may cost more signal than
it saves in cost — a close cousin of the refuted square-root weight dampening,
though that one flattened the weight *spread* permanently while this only
slows the *rate* at which weights track their targets.

Falsifiable: if weight churn is mostly information rather than noise,
turnover falls but validation Sharpe lands at or below trial #28's 1.07.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_weightband_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Adding a 2-percentage-point no-trade band on the magnitude weights of "
        "already-held names — leaving a position at its drifted weight unless "
        "its new target differs by more than the band, with membership and the "
        "daily vol-spike trim unchanged — cuts turnover below trial #28's 7.3x "
        "and raises validation Sharpe above its 1.07 net of 15 bps costs, "
        "because most month-to-month movement in the composite z-score of a "
        "name that never left the basket is jitter rather than information, "
        "and trading on it is a pure cost."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

BAND = 0.02

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
    prev_norm = None
    prev_dt = None

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

        if prev_norm is not None:
            # Where the book sits before trading: last targets, drifted by
            # realized price moves since the previous rebalance.
            names = prev_norm.index
            px_then = prices.loc[prev_dt, names]
            px_now = prices.loc[dt, names]
            growth = (px_now / px_then).replace([float("inf")], float("nan"))
            drifted = (prev_norm * growth).dropna()
            if drifted.sum() > 0:
                drifted = drifted / drifted.sum()
                keep = drifted.index.intersection(norm.index)
                stay = keep[(norm[keep] - drifted[keep]).abs() <= BAND]
                if len(stay) > 0:
                    norm = norm.copy()
                    norm[stay] = drifted[stay]
                    norm = norm.clip(upper=MAX_WEIGHT)
                    norm = norm / norm.sum()

        prev_norm, prev_dt = norm, dt

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
