"""Equal-weight diversified global ETF basket, monthly rebalance.

Simple diversification benchmark: should pass every gate, and tells us how much
of the champion's edge is just 'being in markets'.
"""

import pandas as pd

STRATEGY = {
    "name": "ew_global_etf",
    "family": "volatility targeting / risk parity",
    "hypothesis": (
        "A static equal-weight basket of global equity, bond, real-asset and "
        "EM ETFs achieves a better net Sharpe than cross-sectional momentum "
        "simply by avoiding momentum crashes and churn."
    ),
}

BASKET = ["SPY", "EFA", "EEM", "IEF", "TLT", "LQD", "GLD", "VNQ", "DBC", "TIP"]


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    basket = [c for c in BASKET if c in prices.columns]
    rows = {}
    for dt in rebalance_dates:
        live = [c for c in basket if pd.notna(prices.at[dt, c])]
        if len(live) < 6:
            continue
        w = pd.Series(0.0, index=prices.columns)
        w[live] = 1.0 / len(live)
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
