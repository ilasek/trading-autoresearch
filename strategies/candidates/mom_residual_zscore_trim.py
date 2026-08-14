"""Residual (market-beta-neutralized) momentum in place of total-return
momentum, inside the otherwise-unchanged trial-#28 mechanism.

Background. Every momentum signal tried in this repo so far ranks names by
*total* trailing return. Blitz, Huij & Martens (2011) show that momentum
computed on returns *residual to the market factor* has materially higher
risk-adjusted performance than total-return momentum, and — the part that
matters most here — far milder crash behaviour. Their mechanism: a total-return
momentum basket accumulates a large unintended market-beta bet, because after a
sustained rally the highest-return names are disproportionately the highest-beta
names. When the market turns, that concentrated beta is what produces the
momentum crash. Residualizing strips the beta bet out and leaves the
stock-specific trend, which is what the momentum anomaly is actually about.

Why this is a genuinely open direction here, not a re-tread:
- It is not the refuted sector-neutral scoring (trial #23). That demeaned the
  score *within coarse groups*, a cross-sectional operation that only reshuffles
  ranks between peers. This residualizes each name's own *time series* against
  the market, which changes what the score measures rather than who it is
  compared against.
- It is not the refuted low-vol family. Nothing here selects or weights by
  volatility level; a high-vol name with a strong stock-specific trend still
  scores highly, and a low-vol name that merely drifted with the market scores
  near zero. The signal is deliberately left as an unstandardized residual
  cumulative return (not Blitz's residual t-stat) precisely so that no vol
  normalization sneaks in — that keeps this trial a clean one-change test and
  avoids brushing against the refuted vol-tilt axis.
- It is not the refuted 52-week-high proximity signal (trial #31), which failed
  on turnover because it is a bounded ratio that clusters names near 1.0. A
  residual cumulative log return is unbounded and spreads names out on the same
  kind of scale as the total-return signal it replaces, so it should inherit the
  buffer band's stickiness rather than fighting it.

Exactly one thing changes versus `mom_zscore_narrow_daily_volspike_trim`
(trial #28, val Sharpe 1.07, maxDD -30.3%, DSR 0.9326): the per-name score fed
into the composite z-score is the market-residual log return over each lookback
window instead of the raw total return. Horizons (252d and 126d, skip 21d),
hold-25/enter-15 buffer, magnitude weighting off the composite, 0.25 cap, and
the daily-evaluated binary vol-spike trim (21d/252d ratio > 1.6 -> 0.6x) are all
held identical.

Market factor: the equal-weighted cross-sectional mean of daily log returns
across all instruments available on each date. This is used rather than a
single index ETF so the factor exists over the full history (VT/ACWI start only
in the late 2000s) and so it reflects the actual global stock+ETF universe being
traded. Betas are estimated on the same window the momentum is measured over,
which keeps the construction causal and free of a second lookback parameter.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_residual_zscore_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Ranking and magnitude-weighting the buffered hold-25/enter-15 basket "
        "by a composite z-score of market-beta-residual cumulative return "
        "(252d and 126d windows, skip 21d), instead of total return, raises "
        "validation Sharpe above the total-return version's 1.07 net of 15 bps "
        "costs, because residualizing removes the unintended market-beta bet "
        "that total-return momentum accumulates and that drives its crashes."
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


def _residual_momentum(
    logret: pd.DataFrame, market: pd.Series, end_pos: int, lookback: int
) -> pd.Series:
    """Cumulative log return of each name net of its market-beta component,
    measured over `lookback` days ending SKIP days before `end_pos`."""
    stop = end_pos - SKIP + 1          # exclusive; leaves the skip month out
    start = stop - lookback
    if start < 1:
        return pd.Series(dtype=float)

    win = logret.iloc[start:stop]
    mkt = market.iloc[start:stop]
    win = win.dropna(axis=1, how="any")
    if win.shape[1] == 0 or len(mkt) < 2:
        return pd.Series(dtype=float)

    mkt_dev = mkt - mkt.mean()
    mkt_var = float((mkt_dev**2).sum())
    if mkt_var <= 0:
        return pd.Series(dtype=float)

    dev = win - win.mean()
    beta = dev.mul(mkt_dev, axis=0).sum() / mkt_var
    return win.sum() - beta * float(mkt.sum())


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    logret = np.log(prices).diff()
    market = logret.mean(axis=1, skipna=True)

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    all_dates = prices.index
    rows = {}
    held = set()
    base_periods = []

    for i, dt in enumerate(rebalance_dates):
        pos = all_dates.get_loc(dt)
        if pos < LOOKBACK_LONG + SKIP + 1:
            continue

        res_long = _residual_momentum(logret, market, pos, LOOKBACK_LONG)
        res_short = _residual_momentum(logret, market, pos, LOOKBACK_SHORT)
        common = res_long.index.intersection(res_short.index)
        if len(common) < CORE_N:
            continue

        composite = _zscore(res_long[common]) + _zscore(res_short[common])
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

        next_dt = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else None
        end_pos = all_dates.get_loc(next_dt) if next_dt is not None else len(all_dates)
        base_periods.append((pos, end_pos, norm))

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
