"""Time-series trend following on a multi-asset ETF sleeve, with a diversified
defensive parking basket (fixes the min-positions gate failure of the earlier
`gtaa_trend_etf` trial, which parked all risk-off capital in a single
Treasury ETF and averaged only 3.84 positions in validation).

Each risk asset is held at an equal target weight while priced above its own
200-day moving average; whenever it is below, its target weight is
redistributed equally across four investment-grade bond ETFs instead of one,
so the portfolio never collapses below ~4 held positions even if every risk
asset is simultaneously in a downtrend.
"""

import pandas as pd

STRATEGY = {
    "name": "gtaa_trend_diversified",
    "family": "time-series momentum / trend following",
    "hypothesis": (
        "An equal-weight multi-asset-class ETF sleeve that de-risks each "
        "asset individually below its 200-day moving average, parking "
        "de-risked capital across a diversified bond basket instead of one "
        "instrument, beats cross-sectional stock momentum on risk-adjusted "
        "terms while satisfying the diversification gate."
    ),
}

RISK_ON = ["SPY", "EFA", "VWO", "VNQ", "DBC", "GLD", "HYG", "TLT"]
DEFENSIVE = ["IEF", "SHY", "AGG", "LQD"]
MA_WINDOW = 200


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    risk_on = [c for c in RISK_ON if c in prices.columns]
    defensive = [c for c in DEFENSIVE if c in prices.columns]
    base_w = 1.0 / len(risk_on)

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = prices.loc[:dt, risk_on]
        if len(hist) < MA_WINDOW + 1:
            continue
        ma = hist.rolling(MA_WINDOW).mean().iloc[-1]
        last = hist.iloc[-1]
        valid = ma.notna() & last.notna()
        if not valid.any():
            continue

        w = pd.Series(0.0, index=prices.columns)
        risk_off_weight = 0.0
        for a in risk_on:
            if not valid[a]:
                continue
            if last[a] > ma[a]:
                w[a] = base_w
            else:
                risk_off_weight += base_w

        if risk_off_weight > 0 and defensive:
            per = risk_off_weight / len(defensive)
            for d in defensive:
                w[d] = w.get(d, 0.0) + per

        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
