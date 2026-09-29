"""SANITY (not a trial): textbook cross-sectional momentum. Each month-end
holds the 15 names (of those it may buy) with the highest 12-1 month return,
equal weight. Momentum is among the best-documented anomalies in point-in-time
data, so a sound protocol should still see *some* edge here."""

import pandas as pd

STRATEGY = {"name": "sanity_momentum_12_1", "family": "sanity",
            "hypothesis": "Plain 12-1 momentum keeps an edge on a point-in-time universe."}
N, LB, SKIP = 15, 252, 21


def generate_weights(prices: pd.DataFrame, eligible: pd.DataFrame | None = None) -> pd.DataFrame:
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    pos = {d: i for i, d in enumerate(prices.index)}
    rows = {}
    for dt in rebal:
        i = pos[dt]
        if i < LB + SKIP:
            continue
        mom = (prices.iloc[i - SKIP] / prices.iloc[i - SKIP - LB] - 1)
        ok = mom.notna() & prices.loc[dt].notna()
        if eligible is not None:
            ok &= eligible.loc[dt]
        mom = mom[ok]
        if len(mom) < N:
            continue
        rows[dt] = pd.Series(1.0 / N, index=mom.nlargest(N).index)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
