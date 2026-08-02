"""Capital blend of the champion's 12-1 momentum basket with a static
diversified ETF sleeve — an ensemble of decorrelated signals rather than a
switch between them.

Three prior attempts to fix the momentum-crash weakness by *modifying* the
momentum sleeve (inverse-vol weighting, binary regime switching) or by
*replacing* it with an ETF sleeve (trend-filtered, risk-parity) all failed:
either momentum's return premium was diluted, or the standalone ETF sleeve's
own Sharpe was too low (~0.35-0.71) to carry the blend. This instead keeps
momentum at 80% capital and adds a fixed, low-turnover 20% allocation to a
diversified asset-class ETF sleeve every month, so the diversification only
needs to reduce portfolio-level *drawdown correlation* — it doesn't need a
good standalone Sharpe to help the blend.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_etf_blend",
    "family": "combinations",
    "hypothesis": (
        "An 80/20 capital blend of 12-1 cross-sectional momentum with a "
        "static diversified ETF sleeve improves the champion's Sharpe "
        "and/or drawdown net of costs, because the low-turnover ETF sleeve "
        "is only weakly correlated with momentum's crash periods even "
        "though it has a much lower standalone Sharpe."
    ),
}

LOOKBACK = 252
SKIP = 21
TOP_N = 15
MOM_WEIGHT = 0.8
ETF_SLEEVE = ["SPY", "EFA", "VWO", "VNQ", "DBC", "GLD", "HYG", "TLT", "IEF", "LQD"]
ETF_WEIGHT = 0.2


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    etfs = [c for c in ETF_SLEEVE if c in prices.columns]
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
        top = momentum.nlargest(TOP_N).index

        w = pd.Series(0.0, index=prices.columns)
        w[top] = MOM_WEIGHT / TOP_N

        last = hist.iloc[-1]
        avail_etfs = [e for e in etfs if pd.notna(last[e])]
        if avail_etfs:
            per = ETF_WEIGHT / len(avail_etfs)
            for e in avail_etfs:
                w[e] = w.get(e, 0.0) + per
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
