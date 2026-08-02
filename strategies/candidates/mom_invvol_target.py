"""Volatility-managed cross-sectional momentum.

Same 12-1 momentum selection as the champion, but (1) weights the basket by
inverse trailing volatility instead of equal weight, and (2) scales total
exposure down (never up — long-only, leverage capped at 1.0) when the
basket's own trailing realized vol is elevated. Both aim directly at the
champion's documented weakness: the -50.7% train max drawdown from the
2008-09 momentum crash, which is a vol-spike phenomenon.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_invvol_target",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Inverse-volatility basket weighting plus a portfolio-level volatility "
        "target (scaling down only) on top of 12-1 momentum reduces the "
        "champion's momentum-crash drawdown while keeping validation Sharpe "
        "at or above the champion's, net of 15 bps costs."
    ),
}

LOOKBACK = 252
SKIP = 21
TOP_N = 15
VOL_LOOKBACK = 63
TARGET_VOL = 0.15


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

        basket_rets = hist[top].pct_change().tail(VOL_LOOKBACK)
        vol = basket_rets.std()
        mean_vol = vol.replace(0, np.nan).mean()
        vol = vol.replace(0, np.nan).fillna(mean_vol if pd.notna(mean_vol) else 1.0)
        inv_vol = 1.0 / vol
        basket_w = inv_vol / inv_vol.sum()

        port_proxy = basket_rets.mean(axis=1)
        realized_vol = float(port_proxy.std() * np.sqrt(252)) if len(port_proxy) > 1 else np.nan
        scale = min(1.0, TARGET_VOL / realized_vol) if realized_vol and realized_vol > 0 else 1.0

        w = pd.Series(0.0, index=prices.columns)
        w[top] = basket_w * scale
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
