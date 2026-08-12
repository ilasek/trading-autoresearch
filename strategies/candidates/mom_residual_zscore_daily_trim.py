"""Residual (market-neutralised) momentum in place of total-return momentum,
inside the repo's best-performing mechanism.

Every scoring signal tried so far ranks names by *total* trailing return. That
means a large part of each name's score is simply its loading on the global
market's own trailing move: in a long bull stretch the top of the ranking fills
with high-beta names, and the basket's magnitude weighting then concentrates
capital into exactly those. The documented residual-momentum result (Blitz,
Huij & Martens 2011) is that stripping the market component out of the return
before measuring momentum raises the signal's information ratio and softens its
crash behaviour, because what remains is stock-specific drift rather than
leveraged market direction.

This candidate changes exactly ONE thing versus the repo's strongest challenger
`mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07, maxDD
-30.3%, DSR 0.9326): the two horizon scores fed into the composite z-score are
cumulative *residual* returns (name return minus beta x equal-weight-universe
return, beta estimated over a longer 756d window ending at the same skip point)
instead of cumulative total returns. Buffer band (hold-25/enter-15),
magnitude weighting, the 25% cap, monthly rebalance cadence and the
daily-reacting basket-own vol-spike trim are all held identical.

Note this is deliberately the *unnormalised* residual sum — the literature's
version divides by residual volatility, which would also re-introduce a
low-vol-style tilt (an axis this repo has refuted as a capital-weighting
mechanism). Keeping it unnormalised isolates market-neutralisation as the
single change; signal-level risk normalisation is a separate hypothesis.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_residual_zscore_daily_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Ranking and magnitude-weighting the buffered basket by a composite "
        "z-score of cumulative *residual* return (total return minus "
        "beta-times-market return, beta estimated over a trailing 756d window) "
        "instead of cumulative total return raises validation Sharpe above the "
        "1.07 of the otherwise-identical total-return version, net of 15 bps "
        "costs, because removing the market-beta component of each name's "
        "trailing move leaves a higher signal-to-noise, less crash-prone "
        "stock-specific momentum signal."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
BETA_WINDOW = 756
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

VOL_SHORT = 21
VOL_LONG = 252
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6


def _residual_scores(hist: pd.DataFrame) -> tuple[pd.Series, pd.Series] | None:
    """Cumulative residual return over the long and short horizons.

    Uses only rows of `hist` at or before its last date, and skips the most
    recent SKIP days (the standard momentum skip-month).
    """
    window = hist.iloc[-(BETA_WINDOW + SKIP): len(hist) - SKIP]
    if len(window) < BETA_WINDOW:
        return None
    rets = window.pct_change().iloc[1:]
    ok = rets.notna().all(axis=0) & np.isfinite(rets).all(axis=0)
    rets = rets.loc[:, ok]
    if rets.shape[1] < CORE_N:
        return None

    r = rets.to_numpy(dtype=float)
    market = r.mean(axis=1)
    m_dev = market - market.mean()
    m_var = float(m_dev @ m_dev)
    if m_var <= 0:
        return None
    beta = ((r - r.mean(axis=0)).T @ m_dev) / m_var
    resid = r - np.outer(market, beta)

    out = []
    for lookback in (LOOKBACK_LONG, LOOKBACK_SHORT):
        tail = resid[-lookback:]
        out.append(pd.Series(tail.sum(axis=0), index=rets.columns))
    return out[0], out[1]


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    base_periods = []

    all_dates = prices.index
    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < BETA_WINDOW + SKIP + 1:
            continue
        scores = _residual_scores(hist)
        if scores is None:
            continue
        res_long, res_short = scores

        composite = _zscore(res_long) + _zscore(res_short)
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
