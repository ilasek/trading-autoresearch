"""Trend-gated global asset allocation on ETFs (GTAA-style).

ETF-only deliberately: least exposed to the universe's survivorship bias.
"""

import pandas as pd

STRATEGY = {
    "name": "gtaa_trend_etf",
    "family": "time-series momentum / trend following",
    "hypothesis": (
        "Holding a diversified ETF sleeve only while each ETF trades above its "
        "200-day moving average (parking de-risked sleeves in 7-10y Treasuries) "
        "beats cross-sectional stock momentum on risk-adjusted returns."
    ),
}

RISK_SLEEVES = ["SPY", "EFA", "EEM", "VNQ", "GLD"]
SAFE = "IEF"
MA_WINDOW = 200


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    sleeves = [c for c in RISK_SLEEVES if c in prices.columns]
    ma = prices[sleeves].rolling(MA_WINDOW).mean()
    rows = {}
    for dt in rebalance_dates:
        # A sleeve participates only once it has a full MA window of history.
        live = [s for s in sleeves if pd.notna(ma.at[dt, s])]
        if len(live) < 3:
            continue
        w = pd.Series(0.0, index=prices.columns)
        per_sleeve = 1.0 / len(live)
        safe_total = 0.0
        for s in live:
            if prices.at[dt, s] > ma.at[dt, s]:
                w[s] = per_sleeve
            else:
                safe_total += per_sleeve
        if SAFE in prices.columns and pd.notna(prices.at[dt, SAFE]):
            w[SAFE] = safe_total
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
