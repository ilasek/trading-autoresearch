"""True inverse-volatility risk parity across asset-class ETFs, with a
portfolio-level volatility target (scale down only).

Distinct from the already-rejected `ew_global_etf` (static equal weight,
val Sharpe 0.49): here weights equalize each asset's risk contribution
(inverse trailing vol) rather than capital, and total exposure is scaled to
a fixed annualized vol target. Naive risk parity's actual thesis — balance
risk, not capital — hasn't been tested yet in this repo.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "risk_parity_multi_asset",
    "family": "volatility targeting / risk parity",
    "hypothesis": (
        "Inverse-volatility weighting across a diversified asset-class ETF "
        "sleeve, scaled to a 10% annualized vol target, achieves a better "
        "net Sharpe than the champion by balancing risk contribution rather "
        "than capital across uncorrelated asset classes."
    ),
}

ASSETS = ["SPY", "EFA", "VWO", "VNQ", "DBC", "GLD", "HYG", "TLT", "IEF", "LQD"]
VOL_LOOKBACK = 63
TARGET_VOL = 0.10
MIN_ASSETS = 4


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    assets = [c for c in ASSETS if c in prices.columns]
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = prices.loc[:dt, assets]
        if len(hist) < VOL_LOOKBACK + 1:
            continue
        window = hist.tail(VOL_LOOKBACK + 1)
        rets = window.pct_change().iloc[1:]
        fully_available = rets.columns[rets.notna().all()]
        if len(fully_available) < MIN_ASSETS:
            continue
        vol = rets[fully_available].std()
        vol = vol[vol > 0]
        if len(vol) < MIN_ASSETS:
            continue

        inv_vol = 1.0 / vol
        w_rp = inv_vol / inv_vol.sum()

        port_proxy = (rets[vol.index] * w_rp).sum(axis=1)
        realized_vol = float(port_proxy.std() * np.sqrt(252)) if len(port_proxy) > 1 else np.nan
        scale = min(1.0, TARGET_VOL / realized_vol) if realized_vol and realized_vol > 0 else 1.0

        w = pd.Series(0.0, index=prices.columns)
        w[vol.index] = w_rp * scale
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
