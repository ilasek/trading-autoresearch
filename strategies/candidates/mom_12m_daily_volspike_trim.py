"""The champion's own plain equal-weight buffered 12-1 basket, plus the
daily-reacting basket-own vol-spike exposure trim that worked on the
composite z-score-weighted baskets.

Trials #27-28 established that a basket-own realized-vol-spike exposure trim
(21d/252d trailing vol ratio > 1.6 -> 0.6x exposure), re-evaluated on every
trading day rather than only at the monthly rebalance, improves validation
Sharpe *and* cuts maxDD when applied to the composite 6-1/12-1 z-score
weighted basket (widebreadth: 1.03 -> 1.05 Sharpe, -35.6% -> -29.5% maxDD;
narrow: 1.03 -> 1.07 Sharpe, -36.0% -> -30.3% maxDD). Both prior trims were
layered on the magnitude-weighted basket. This candidate isolates whether the
trim's benefit is a property of *any* concentrated momentum basket reacting
to its own vol regime, or specific to the return-magnitude weighting scheme,
by applying the identical trim mechanism to the plain equal-weight buffered
12-1 basket (`mom_12m_buffered`, champion's own signal, val Sharpe 0.865
untrimmed) instead.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_12m_daily_volspike_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Applying the same daily-reacting basket-own vol-spike exposure trim "
        "(21d/252d realized-vol ratio > 1.6 -> 0.6x exposure) to the plain "
        "equal-weight buffered 12-1 basket (the champion's own signal, "
        "hold-25/enter-15) improves its validation Sharpe and reduces its "
        "maxDD versus the untrimmed champion, net of 15 bps costs, because "
        "the trim's benefit comes from reacting to the basket's own vol "
        "regime, not from the return-magnitude weighting scheme it was "
        "previously tested on."
    ),
}

LOOKBACK = 252
SKIP = 21
CORE_N = 15
BAND_N = 25

VOL_SHORT = 21
VOL_LONG = 252
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    base_periods = []  # (start_idx_pos, end_idx_pos_exclusive, norm)

    all_dates = prices.index
    for i, dt in enumerate(rebalance_dates):
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
        held = (held & band) | core

        norm = pd.Series(1.0 / len(held), index=list(held))
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
