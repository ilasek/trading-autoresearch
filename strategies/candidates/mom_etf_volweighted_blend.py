"""Capital blend of 12-1 momentum with the diversified ETF sleeve, weighted
by each sleeve's own trailing realized volatility instead of a fixed split.

`mom_etf_blend` (fixed 80/20) came within 0.015 Sharpe of the champion while
improving both train and validation max drawdown — the closest challenger so
far, and the first evidence that blending (not switching) the ETF sleeve
helps. Deliberately not chased by sweeping the 80/20 ratio (that's a knob,
not an idea). This instead uses a principled, date-varying weighting rule:
each month, weight the two sleeves inversely proportional to their own
trailing 126-day realized volatility (computed from each sleeve's own
constructed daily returns, using only data at or before the rebalance date),
so momentum gets less capital exactly when it's turbulent (e.g. entering a
momentum crash) and more when it's calm — without ever gating it off, which
is the mechanism that reliably backfired in three prior attempts.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_etf_volweighted_blend",
    "family": "combinations",
    "hypothesis": (
        "Blending 12-1 cross-sectional momentum with a static diversified "
        "ETF sleeve, weighted inversely by each sleeve's own trailing "
        "126-day realized volatility rather than a fixed 80/20 split, "
        "improves on the champion's validation Sharpe and/or drawdown net "
        "of costs, because it organically shifts capital toward the ETF "
        "sleeve exactly when momentum is turbulent."
    ),
}

LOOKBACK = 252
SKIP = 21
TOP_N = 15
VOL_LOOKBACK = 126
ETF_SLEEVE = ["SPY", "EFA", "VWO", "VNQ", "DBC", "GLD", "HYG", "TLT", "IEF", "LQD"]


def _sleeve_vol(returns: pd.DataFrame, members: list[str]) -> float:
    live = [c for c in members if c in returns.columns]
    if not live:
        return float("nan")
    sleeve_ret = returns[live].mean(axis=1)
    sleeve_ret = sleeve_ret.tail(VOL_LOOKBACK)
    if len(sleeve_ret) < VOL_LOOKBACK // 2:
        return float("nan")
    return float(sleeve_ret.std())


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    etfs = [c for c in ETF_SLEEVE if c in prices.columns]
    daily_returns = prices.pct_change()

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK + SKIP + 1:
            continue
        past = hist.iloc[-(LOOKBACK + SKIP) - 1]
        recent = hist.iloc[-SKIP - 1]
        momentum = (recent / past - 1).dropna()
        if len(momentum) < TOP_N:
            continue
        top = list(momentum.nlargest(TOP_N).index)

        last = hist.iloc[-1]
        avail_etfs = [e for e in etfs if pd.notna(last[e])]
        if not avail_etfs:
            continue

        hist_returns = daily_returns.loc[:dt]
        mom_vol = _sleeve_vol(hist_returns, top)
        etf_vol = _sleeve_vol(hist_returns, avail_etfs)
        if pd.isna(mom_vol) or pd.isna(etf_vol) or mom_vol <= 0 or etf_vol <= 0:
            mom_weight, etf_weight = 0.8, 0.2  # fall back to the known-decent fixed split
        else:
            inv_mom, inv_etf = 1.0 / mom_vol, 1.0 / etf_vol
            mom_weight = inv_mom / (inv_mom + inv_etf)
            etf_weight = 1.0 - mom_weight

        w = pd.Series(0.0, index=prices.columns)
        w[top] = mom_weight / TOP_N
        per = etf_weight / len(avail_etfs)
        for e in avail_etfs:
            w[e] = w.get(e, 0.0) + per
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
