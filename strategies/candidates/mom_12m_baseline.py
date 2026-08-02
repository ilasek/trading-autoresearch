"""Baseline: classic 12-1 cross-sectional momentum, monthly rebalance.

The first champion. Deliberately vanilla — its job is to set an honest bar.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_12m_baseline",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Instruments with the highest 12-month return (skipping the most recent "
        "month) continue to outperform over the next month, net of 15 bps costs."
    ),
}

LOOKBACK = 252   # ~12 months
SKIP = 21        # skip most recent month (short-term reversal)
TOP_N = 15


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
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
        w[top] = 1.0 / TOP_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
