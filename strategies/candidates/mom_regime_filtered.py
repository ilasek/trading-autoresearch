"""Cross-sectional momentum gated by a market-trend regime filter.

Identical 12-1 momentum basket to the champion when the market (SPY) is
above its 200-day moving average; when SPY is below its 200dma, rotates
fully into a diversified bond sleeve instead. Distinct mechanism from the
already-rejected `mom_invvol_target` (which reweighted/scaled inside the
momentum sleeve every month) — this is a binary market-level regime switch,
aimed at sidestepping momentum-crash periods (which cluster around broad
market downtrends/reversals) rather than damping them from within.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_regime_filtered",
    "family": "regime switching",
    "hypothesis": (
        "Switching fully out of 12-1 cross-sectional momentum into a "
        "diversified bond sleeve whenever SPY is below its 200-day moving "
        "average reduces the champion's momentum-crash drawdown while "
        "keeping validation Sharpe at or above the champion's, net of costs."
    ),
}

LOOKBACK = 252
SKIP = 21
TOP_N = 15
MA_WINDOW = 200
DEFENSIVE = ["IEF", "SHY", "AGG", "LQD"]


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    defensive = [c for c in DEFENSIVE if c in prices.columns]
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK + SKIP + 1:
            continue
        spy_hist = hist["SPY"].dropna()
        if len(spy_hist) < MA_WINDOW + 1:
            continue
        spy_ma = spy_hist.tail(MA_WINDOW).mean()
        spy_last = spy_hist.iloc[-1]
        risk_on = spy_last > spy_ma

        w = pd.Series(0.0, index=prices.columns)
        if risk_on:
            past = hist.iloc[-(LOOKBACK + SKIP) - 1]
            recent = hist.iloc[-SKIP - 1]
            momentum = (recent / past - 1).dropna()
            if len(momentum) < TOP_N:
                continue
            top = momentum.nlargest(TOP_N).index
            w[top] = 1.0 / TOP_N
        elif defensive:
            w[defensive] = 1.0 / len(defensive)
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
