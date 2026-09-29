"""SANITY (not a trial): pure hindsight. Holds, equal-weight, the 15 legacy-
universe stocks with the highest 2010-2023 total return — a list only knowable
at the end of 2023. It passes the causality check (the list is a constant) and
is exactly the selection the legacy universe bakes in. A protocol that is
robust to survivorship bias must not reward it."""

import pandas as pd

STRATEGY = {"name": "sanity_hindsight_winners", "family": "sanity",
            "hypothesis": "Hindsight selection must not pass a survivorship-robust protocol."}

WINNERS = ["NVDA", "AVGO", "NFLX", "AAPL", "LLY", "ASML", "AMZN", "NVO", "UNH", "MA",
           "HD", "SPGI", "ADBE", "MSFT", "COST"]


def generate_weights(prices: pd.DataFrame, eligible: pd.DataFrame | None = None) -> pd.DataFrame:
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    names = [c for c in WINNERS if c in prices.columns]
    ok = prices.loc[rebal, names].notna()
    if eligible is not None:
        ok &= eligible.loc[rebal, names]
    w = ok.astype(float)
    w = w.div(w.sum(axis=1).replace(0, float("nan")), axis=0).fillna(0.0)
    return w.reindex(columns=prices.columns, fill_value=0.0)
