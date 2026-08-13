"""Residual (idiosyncratic) momentum in place of raw-return momentum, inside
the repo's best-performing mechanism.

Everything here is held identical to `mom_zscore_narrow_daily_volspike_trim`
(trial #28, val Sharpe 1.07, maxDD -30.3%, DSR 0.9326 — the strongest
challenger in the repo's history): hold-25/enter-15 buffered membership,
magnitude weighting by composite z-score, 25% cap, and the daily-reacting
basket-own vol-spike exposure trim. The ONLY change is what the composite
z-score ranks on.

Instead of z(12-1 raw return) + z(6-1 raw return), each name is scored by the
t-statistic of its market-model alpha over the same two windows: regress the
name's daily returns on the equal-weight universe return over the formation
window, then score = mean(residual) / std(residual). This is the classic
residual-momentum construction (Blitz, Huij & Martens 2011 / Gutierrez &
Prior): it removes the part of trailing performance that is just loaded
market beta, and expresses the remainder per unit of idiosyncratic risk.

Why this is not a re-test of the refuted low-vol direction: those trials
(`lowvol_equity_tilt`, `mom_lowvol_doublesort`) used raw trailing *total*
volatility as a separate screen or weight applied on top of an unchanged
momentum ranking, and failed because the screen discarded the momentum
pool's strongest compounders. Here there is no separate screen — the
denominator is residual (beta-removed) vol and it is intrinsic to the signal
definition, so a high-total-vol name with strong, steady stock-specific
outperformance still ranks at the top. The primary novelty is the beta
removal, which is also the documented reason residual momentum suffers
smaller crash drawdowns than total-return momentum.

Falsifiable: if residual momentum is merely a noisier repackaging of the
same information on this universe, validation Sharpe lands at or below the
1.07 of the identical raw-return mechanism.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_residual_zscore_daily_volspike_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Scoring the buffered hold-25/enter-15 magnitude-weighted basket by a "
        "composite z-score of residual-momentum t-statistics (market-model "
        "alpha over 252d and 126d formation windows, skipping the most recent "
        "month, divided by residual volatility) instead of raw trailing "
        "returns raises validation Sharpe above the 1.07 of the otherwise "
        "identical raw-return version, net of 15 bps costs, because removing "
        "loaded market beta isolates the stock-specific continuation that "
        "drives momentum and drops the factor exposure that drives its crashes."
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


def _residual_score(hist: pd.DataFrame, lookback: int) -> pd.Series:
    """t-stat of market-model alpha over `lookback` days, skipping the last SKIP."""
    px = hist.iloc[-(lookback + SKIP) - 1 : len(hist) - SKIP]
    px = px.dropna(axis=1, how="any")
    if px.shape[1] < 2 or len(px) < lookback:
        return pd.Series(dtype=float)

    rets = px.pct_change().iloc[1:]
    mkt = rets.mean(axis=1)
    mkt_dev = mkt - mkt.mean()
    var_m = float((mkt_dev**2).mean())
    if var_m <= 0:
        return pd.Series(dtype=float)

    dev = rets.sub(rets.mean(), axis=1)
    beta = dev.mul(mkt_dev, axis=0).mean() / var_m
    resid = rets - np.outer(mkt, beta)
    sd = resid.std(ddof=0)
    score = resid.mean() / sd.where(sd > 0)
    return score.dropna()


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
        score_long = _residual_score(hist, LOOKBACK_LONG)
        score_short = _residual_score(hist, LOOKBACK_SHORT)
        common = score_long.index.intersection(score_short.index)
        if len(common) < CORE_N:
            continue

        composite = _zscore(score_long[common]) + _zscore(score_short[common])
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
