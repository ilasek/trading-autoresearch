"""Beta-removed momentum WITHOUT idiosyncratic-vol normalization — the
disentangling half of trial #32.

Trial #32 (`mom_residual_zscore_daily_volspike_trim`) swapped the raw-return
composite for a residual-momentum *t-statistic* and produced a split result:
the best validation drawdown in the repo's history (-24.5%, vs -30.3% for the
raw-return version and -29.9% for the champion) but a much lower annualized
return (+16.0% vs +27.0%), netting a worse Sharpe (0.96 vs 1.07).

That construction changed two things at once:
  (a) numerator — score the market-model residual instead of the total
      return, removing the part of trailing performance that is just loaded
      market beta;
  (b) denominator — divide by residual volatility, expressing the remainder
      per unit of stock-specific risk.

This repo's established learnings predict opposite signs for the two. Tilting
capital *toward* the strongest-momentum names has raised Sharpe at every step
(0.90 -> 0.93 -> 0.98 -> 1.03); every construction that tilted capital *away*
from higher-vol names has cost Sharpe (`lowvol_equity_tilt`,
`mom_lowvol_doublesort`, `mom_etf_volweighted_blend`, `risk_parity_multi_asset`).
Half (b) is structurally the latter — dividing by vol systematically demotes
exactly the high-conviction, higher-idiosyncratic-vol compounders that the
magnitude-weighting mechanism has been shown to profit from.

This candidate keeps (a) and drops (b): the score is the mean daily *residual
return* over each window, with no risk normalization. Everything else —
hold-25/enter-15 buffer, composite of 252d and 126d windows skipping the most
recent month, magnitude weighting, 25% cap, and the daily-reacting basket-own
vol-spike exposure trim — is identical to trials #28 and #32, so the
comparison isolates exactly one change.

Falsifiable: if trial #32's drawdown improvement came from the vol
normalization rather than the beta removal, this candidate's validation maxDD
reverts toward the raw-return version's -30.3% instead of staying near -24.5%.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_residual_raw_zscore_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Scoring the same buffered magnitude-weighted basket by cumulative "
        "market-model residual return (beta removed) WITHOUT dividing by "
        "residual volatility retains trial #32's best-ever validation maxDD "
        "(-24.5%) while restoring the annualized return that the vol "
        "normalization destroyed (+16.0% vs +27.0%), lifting validation "
        "Sharpe above 1.07 net of 15 bps costs, because the beta removal and "
        "the risk normalization are separable and only the latter tilts "
        "capital away from the high-conviction compounders this repo has "
        "repeatedly found to carry the return."
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
    """Mean daily market-model residual return over `lookback` days, skipping
    the last SKIP. No division by residual vol — that is the point of this trial."""
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
    return resid.mean().dropna()


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
