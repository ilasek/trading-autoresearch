"""Low-volatility equity tilt: monthly rebalance into the lowest trailing-
realized-volatility stocks, equal weighted.

Tests the low-volatility anomaly (low-risk stocks earn better risk-adjusted,
sometimes even raw, returns than the market) directly against the champion.
Single-stock strategy on a survivorship-biased universe, per the standing
data caveat in experiments/learnings.md — treated with extra skepticism, but
still worth one honest trial since it's next in program.md's family list.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "lowvol_equity_tilt",
    "family": "low-volatility / quality tilts",
    "hypothesis": (
        "Stocks with the lowest trailing 126-day realized volatility "
        "outperform the champion's high-momentum basket on a risk-adjusted "
        "(Sharpe) basis, net of 15 bps costs, because low-vol names carry "
        "less drawdown risk per unit of turnover."
    ),
}

VOL_LOOKBACK = 126
BOTTOM_N = 20


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    stock_ids = [i["id"] for i in instruments(types=("stock",))]
    stock_cols = [c for c in stock_ids if c in prices.columns]

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = prices.loc[:dt, stock_cols]
        if len(hist) < VOL_LOOKBACK + 1:
            continue
        window = hist.tail(VOL_LOOKBACK + 1)
        rets = window.pct_change().iloc[1:]
        # require a fully populated volatility window (listed for the whole lookback)
        vol = rets.std()
        vol = vol[rets.notna().all()]
        if len(vol) < BOTTOM_N:
            continue
        bottom = vol.nsmallest(BOTTOM_N).index
        w = pd.Series(0.0, index=prices.columns)
        w[bottom] = 1.0 / BOTTOM_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
