"""The champion's own 12-1 momentum signal, with a buffer/hysteresis band on
basket membership instead of a hard top-15 cutoff.

This session's `mom_str_reversal_buffered` trial showed the buffer mechanism
(hold while ranked in the top 25, enter only in the top 15) cuts turnover
substantially — 8.3-9.0x down to 6.5x on the momentum+reversal blend — while
*improving* validation Sharpe slightly, not costing anything for the reduced
churn. That trial mixed the mechanism change with the reversal leg, so it
couldn't isolate how much of the gain was the buffer itself. This candidate
applies the same buffer mechanism to the champion's own signal in isolation
(no reversal leg, no blend) to test whether it makes the incumbent cheaper to
run without hurting its edge — a mechanism-level change to the exact signal
that already works, not a new signal or a swept parameter.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_12m_buffered",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Replacing the champion's hard top-15 monthly cutoff with an "
        "asymmetric buffer band (hold while ranked in the top 25, enter only "
        "when ranked in the top 15) reduces annual turnover below the "
        "champion's 5.8x while keeping validation Sharpe at or above the "
        "champion's, net of 15 bps costs."
    ),
}

LOOKBACK = 252
SKIP = 21
CORE_N = 15
BAND_N = 25


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK + SKIP + 1:
            continue
        past = hist.iloc[-(LOOKBACK + SKIP) - 1]
        recent = hist.iloc[-SKIP - 1]
        momentum = (recent / past - 1).dropna()
        if len(momentum) < CORE_N:
            continue

        ranked = momentum.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core  # both subsets of band, so |held| <= BAND_N

        w = pd.Series(0.0, index=prices.columns)
        w[list(held)] = 1.0 / len(held)
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
