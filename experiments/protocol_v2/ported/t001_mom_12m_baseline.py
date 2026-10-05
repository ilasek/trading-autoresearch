# PORT of trial #1 (mom_12m_baseline) as run at commit 639ad648eb1e, for the protocol v2
# re-scoring only (not a trial). The one change: the ranking step considers only names
# that are point-in-time eligible on the rebalance date (lines marked PORT).
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


def generate_weights(prices: pd.DataFrame, eligible: pd.DataFrame | None = None) -> pd.DataFrame:
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
        if eligible is not None:   # PORT (protocol v2): rank only point-in-time eligible names
            momentum = momentum[eligible.loc[dt].reindex(momentum.index, fill_value=False).to_numpy(dtype=bool)]
        top = momentum.nlargest(TOP_N).index
        w = pd.Series(0.0, index=prices.columns)
        w[top] = 1.0 / TOP_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
