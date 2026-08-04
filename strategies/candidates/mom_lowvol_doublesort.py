"""Momentum-qualified low-volatility double sort: among the top momentum
decile of stocks, hold the lowest-volatility names. Monthly rebalance.

Standalone low-vol stock selection is refuted in this repo (val Sharpe 0.69,
see `lowvol_equity_tilt`): low-vol names on this survivorship-biased,
sector-concentrated large-cap universe just don't carry a return premium on
their own. `experiments/learnings.md` flags this as needing a return/quality
overlay to be worth retesting, rather than a standalone signal. This
double-sorts instead of blending: first screen to the top-momentum quintile
(same universe the champion trades), then within that pool pick the lowest
trailing-vol names — testing whether low-vol adds anything as a *risk filter
on top of* a real return signal, rather than being expected to carry returns
by itself.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "mom_lowvol_doublesort",
    "family": "low-volatility / quality tilts",
    "hypothesis": (
        "Among stocks in the top momentum quintile (12-1 return), those "
        "with the lowest trailing 126-day realized volatility produce a "
        "better net Sharpe than the champion's plain top-N momentum "
        "selection, because low-vol acts as a quality filter that avoids "
        "the most crash-prone high-momentum names."
    ),
}

LOOKBACK = 252
SKIP = 21
VOL_LOOKBACK = 126
MOM_POOL_FRACTION = 0.20   # top quintile by momentum
FINAL_N = 15               # same basket size as the champion


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    stock_ids = [i["id"] for i in instruments(types=("stock",))]
    stock_cols = [c for c in stock_ids if c in prices.columns]
    stock_prices = prices[stock_cols]

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = stock_prices.loc[:dt]
        if len(hist) < LOOKBACK + SKIP + 1:
            continue
        past = hist.iloc[-(LOOKBACK + SKIP) - 1]
        recent = hist.iloc[-SKIP - 1]
        momentum = (recent / past - 1).dropna()
        pool_size = max(FINAL_N, int(len(momentum) * MOM_POOL_FRACTION))
        if len(momentum) < pool_size:
            continue
        pool = momentum.nlargest(pool_size).index

        vol_hist = hist[pool].tail(VOL_LOOKBACK + 1)
        if len(vol_hist) < VOL_LOOKBACK + 1:
            continue
        rets = vol_hist.pct_change().iloc[1:]
        vol = rets.std()
        vol = vol[rets.notna().all()]
        if len(vol) < FINAL_N:
            continue
        picks = vol.nsmallest(FINAL_N).index

        w = pd.Series(0.0, index=prices.columns)
        w[picks] = 1.0 / FINAL_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
