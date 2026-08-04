"""Short-term (1-month) mean reversion on individual stocks, monthly rebalance.

Follow-up to `str_reversal_stocks`, which GATE_FAILed on turnover (83.9x
validation vs the 50x cap) because a weekly rebalance of a 5-day-return
ranking reshuffles most of the basket every week. This is a structurally
different version, not a parameter tweak: it moves to the champion's own
monthly cadence and a full 1-month (21-trading-day) lookback, the horizon
most associated with short-term reversal in the literature (Jegadeesh 1990)
— coincidentally exactly the SKIP window the champion's momentum signal
*excludes* to avoid this effect. Trading it directly, monthly, tests whether
that skipped month carries a genuine reversal premium of its own, at a
rebalance frequency the turnover gate can actually accommodate.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "str_reversal_monthly",
    "family": "short-term mean reversion",
    "hypothesis": (
        "Stocks with the worst trailing 1-month (21-trading-day) return "
        "outperform over the next month as the move mean-reverts, producing "
        "a better net Sharpe than the champion's 12-1 momentum, net of 15 "
        "bps costs, on a monthly-rebalanced long-only basket."
    ),
}

LOOKBACK = 21
BOTTOM_N = 15


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    stock_ids = [i["id"] for i in instruments(types=("stock",))]
    stock_cols = [c for c in stock_ids if c in prices.columns]
    stock_prices = prices[stock_cols]

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = stock_prices.loc[:dt]
        if len(hist) < LOOKBACK + 1:
            continue
        past = hist.iloc[-LOOKBACK - 1]
        recent = hist.iloc[-1]
        ret = (recent / past - 1).dropna()
        if len(ret) < BOTTOM_N:
            continue
        losers = ret.nsmallest(BOTTOM_N).index
        w = pd.Series(0.0, index=prices.columns)
        w[losers] = 1.0 / BOTTOM_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
