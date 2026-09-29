"""SANITY (not a trial): no skill. Each month-end holds 15 names drawn
uniformly from those it may buy (eligible, else priced), equal weight. The draw
is seeded by the rebalance date, so it is deterministic and causal. It should
land mid-distribution in the random-selection null and near the equal-weight
pool."""

import numpy as np
import pandas as pd

STRATEGY = {"name": "sanity_random_selection", "family": "sanity",
            "hypothesis": "Random selection has no edge over the random-selection null."}
N = 15


def generate_weights(prices: pd.DataFrame, eligible: pd.DataFrame | None = None) -> pd.DataFrame:
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for dt in rebal:
        ok = prices.loc[dt].notna()
        if eligible is not None:
            ok &= eligible.loc[dt]
        pool = ok.index[ok.to_numpy()]
        if len(pool) < N:
            continue
        rng = np.random.default_rng(int(dt.strftime("%Y%m%d")))
        pick = rng.choice(pool, N, replace=False)
        rows[dt] = pd.Series(1.0 / N, index=pick)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
