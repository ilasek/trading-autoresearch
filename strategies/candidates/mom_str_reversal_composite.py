"""Composite z-score ranking of 12-1 momentum and monthly short-term
reversal into a single basket, instead of blending two separate baskets.

`mom_str_reversal_blend` (two 15-name baskets, 80/20 capital split) beat the
champion's raw validation Sharpe for the first time in the repo (0.87 vs
0.865) but was rejected on the deflated-Sharpe multiple-testing bar, and ran
a high 8.3x validation turnover from managing two overlapping-but-distinct
basket memberships every month. This tests the same "buy strong 12-month
trend that has pulled back over the last month" idea through a different,
single-basket construction: cross-sectionally z-score both signals each
month and rank stocks on one composite score (same 80/20 weighting already
validated as the good blend ratio), then hold the top 15. One ranked list
should need to replace fewer names per month than reconciling two separate
lists, which may cut turnover enough — combined with the same raw edge — to
actually clear the DSR bar.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "mom_str_reversal_composite",
    "family": "combinations",
    "hypothesis": (
        "Ranking stocks on a single composite z-score of 12-1 momentum "
        "(80% weight) and negative 1-month return (20% weight) and holding "
        "the top 15 achieves a better net validation Sharpe than both the "
        "champion and the two-basket `mom_str_reversal_blend`, because a "
        "single ranked list has lower name turnover than reconciling two "
        "separate baskets."
    ),
}

MOM_LOOKBACK = 252
MOM_SKIP = 21
REV_LOOKBACK = 21
TOP_N = 15
MOM_WEIGHT = 0.8
REV_WEIGHT = 0.2


def _zscore(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()


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

        rev_past = hist.iloc[-REV_LOOKBACK - 1]
        rev_recent = hist.iloc[-1]
        rev_ret = (rev_recent / rev_past - 1).dropna()

        common = momentum.index.intersection(rev_ret.index)
        if len(common) < TOP_N:
            continue

        mom_z = _zscore(momentum.loc[common])
        rev_z = _zscore(-rev_ret.loc[common])  # higher = worse recent return
        score = MOM_WEIGHT * mom_z + REV_WEIGHT * rev_z
        score = score.dropna()
        if len(score) < TOP_N:
            continue

        picks = score.nlargest(TOP_N).index
        w = pd.Series(0.0, index=prices.columns)
        w[picks] = 1.0 / TOP_N
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
