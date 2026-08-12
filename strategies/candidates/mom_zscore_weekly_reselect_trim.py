"""Weekly (instead of monthly) re-evaluation of basket membership and weights,
holding every other element of the repo's strongest challenger fixed.

The most general lesson this repo has produced so far came from the vol-spike
trim: an identical trigger was a near no-op at monthly cadence and decisive at
daily cadence, purely because of reaction lag. That lesson was established for
the *exposure overlay*. Its untested counterpart is the selection itself — the
basket's composition and its magnitude weights are still recomputed only at
month-end, so a name whose momentum has collapsed keeps its (possibly large)
weight for up to 21 trading days before the buffer can drop it, and a newly
strong name waits just as long to be added.

This candidate changes exactly ONE thing versus
`mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07, maxDD
-30.3%, DSR 0.9326): the rebalance grid is weekly rather than monthly. The
composite 12-1/6-1 z-score signal, the hold-25/enter-15 buffer band, the
magnitude weighting, the 25% cap and the daily-reacting vol-spike trim are all
identical. The buffer band is what makes this affordable: membership only
changes when a name leaves the top 25 or enters the top 15, so a weekly grid
should mostly buy faster *exits* rather than wholesale churn.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_weekly_reselect_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Re-evaluating the buffered composite-z-score basket's membership and "
        "magnitude weights weekly instead of monthly — every other element of "
        "trial #28 held identical — raises validation Sharpe above its 1.07, "
        "net of 15 bps costs, because the buffer band keeps the extra turnover "
        "small while cutting up to three weeks of reaction lag out of the "
        "basket's exits from names whose momentum has already broken down."
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
    rebalance_dates = prices.groupby(pd.Grouper(freq="W")).tail(1).index
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
