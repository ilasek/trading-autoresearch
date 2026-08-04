"""Capital blend of 12-1 momentum with monthly short-term reversal — two
stock-level signals on structurally opposite horizons, not asset classes.

Two independent findings this session motivate this: (1) `str_reversal_monthly`
(buying last month's worst performers) reached validation Sharpe 0.82, the
second-closest standalone challenger in the repo after momentum itself, with
a different (worse) drawdown profile — a sign its return stream isn't simply
a weaker copy of momentum's. (2) The one established near-miss mechanism in
this repo is a fixed-ratio capital *blend* (not switch, not vol-weighting —
that failed twice: `mom_invvol_target` and `mom_etf_volweighted_blend`), and
80/20 is the one ratio already shown to work best here (`mom_etf_blend`, val
Sharpe 0.85). This applies that same proven ratio to a second sleeve chosen
for a structural reason: momentum's SKIP=21 window exists specifically to
exclude the short-term reversal effect, so the two signals are selecting on
literally disjoint, opposite-signed return horizons of the same stocks.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "mom_str_reversal_blend",
    "family": "combinations",
    "hypothesis": (
        "An 80/20 capital blend of 12-1 cross-sectional momentum with "
        "monthly (21-day) short-term reversal improves the champion's "
        "validation Sharpe and/or drawdown net of costs, because the two "
        "signals select on disjoint, structurally anti-correlated return "
        "horizons of the same stock universe."
    ),
}

MOM_LOOKBACK = 252
MOM_SKIP = 21
REV_LOOKBACK = 21
TOP_N = 15
MOM_WEIGHT = 0.8
REV_WEIGHT = 0.2


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    stock_ids = [i["id"] for i in instruments(types=("stock",))]
    stock_cols = [c for c in stock_ids if c in prices.columns]
    stock_prices = prices[stock_cols]

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebalance_dates:
        hist = stock_prices.loc[:dt]
        if len(hist) < MOM_LOOKBACK + MOM_SKIP + 1:
            continue

        past = hist.iloc[-(MOM_LOOKBACK + MOM_SKIP) - 1]
        recent = hist.iloc[-MOM_SKIP - 1]
        momentum = (recent / past - 1).dropna()
        if len(momentum) < TOP_N:
            continue
        winners = momentum.nlargest(TOP_N).index

        rev_past = hist.iloc[-REV_LOOKBACK - 1]
        rev_recent = hist.iloc[-1]
        rev_ret = (rev_recent / rev_past - 1).dropna()
        if len(rev_ret) < TOP_N:
            continue
        losers = rev_ret.nsmallest(TOP_N).index

        w = pd.Series(0.0, index=prices.columns)
        w[winners] = MOM_WEIGHT / TOP_N
        for c in losers:
            w[c] = w.get(c, 0.0) + REV_WEIGHT / TOP_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
