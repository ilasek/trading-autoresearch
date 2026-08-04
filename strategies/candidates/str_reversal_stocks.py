"""Short-term (1-week) mean reversion on individual stocks, weekly rebalance.

First test of family #4 (short-term mean reversion) in this repo. Classic
result (Lehmann 1990, Jegadeesh 1990): stocks with the worst trailing
short-horizon return tend to bounce back over the following short horizon,
the opposite sign of the 12-1 momentum effect the champion trades. Restricted
to stocks only (not ETFs) since the effect is a single-name overreaction /
liquidity-provision story, not something a diversified basket should exhibit.
Weekly rebalance keeps the lookback short without daily rebalancing, which
would be needlessly expensive under the cost model; turnover is watched
against the 50x/year gate given the higher rebalance frequency.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "str_reversal_stocks",
    "family": "short-term mean reversion",
    "hypothesis": (
        "Stocks with the worst trailing 5-trading-day return outperform over "
        "the next week as the move mean-reverts, producing a better net "
        "Sharpe than the champion's 12-1 momentum, net of 15 bps costs, on a "
        "weekly-rebalanced long-only basket."
    ),
}

LOOKBACK = 5
BOTTOM_N = 15


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    stock_ids = [i["id"] for i in instruments(types=("stock",))]
    stock_cols = [c for c in stock_ids if c in prices.columns]
    stock_prices = prices[stock_cols]

    rebalance_dates = prices.groupby(pd.Grouper(freq="W")).tail(1).index
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
