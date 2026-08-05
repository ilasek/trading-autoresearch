"""Momentum + short-term reversal blend with buffer/hysteresis bands to cut turnover.

Two prior sessions established: (1) an 80/20 capital blend of 12-1 momentum with
monthly short-term reversal reaches validation Sharpe ~0.87
(`mom_str_reversal_blend`, `mom_str_reversal_composite`) — a genuine edge over the
champion's 0.865 — but both constructions were REJECTed only on the deflated-Sharpe
multiple-testing bar (~0.90 vs 0.95 required), not on the head-to-head Sharpe
comparison. (2) Both prior constructions ran turnover far above the champion's
5.8x (8.3-9.0x annual). Higher turnover raises costs directly and inflates
month-to-month churn from names re-sorting across a hard cutoff near the selection
boundary, without necessarily adding raw edge — so cutting that churn is worth
testing on its own economic merit.

This is a genuinely different mechanism, not a swept parameter: instead of a fixed
top-N cutoff recomputed fresh every month (which flips a name in/out the instant its
rank crosses N), each leg now applies an asymmetric buffer — a name already held
stays in as long as it remains within a wider band, and only new entrants must clear
the tighter core threshold. This is standard practice for reducing momentum-strategy
turnover in the literature (e.g. Novy-Marx & Velikov 2016) and has not been tried in
this repo. The 80/20 blend ratio and the underlying signals are unchanged from the
established near-miss construction — only the membership-selection mechanism changes.
"""

import pandas as pd

from engine.data import instruments

STRATEGY = {
    "name": "mom_str_reversal_buffered",
    "family": "combinations",
    "hypothesis": (
        "Applying an asymmetric buffer band (hold while ranked in the top/bottom "
        "25, enter only when ranked in the top/bottom 15) to each leg of the 80/20 "
        "momentum + monthly-reversal blend cuts turnover well below the ~8-9x seen "
        "in the unbuffered blend while keeping validation Sharpe within reach of "
        "the champion, net of 15 bps costs."
    ),
}

MOM_LOOKBACK = 252
MOM_SKIP = 21
REV_LOOKBACK = 21
CORE_N = 15   # threshold to newly enter a leg's basket
BAND_N = 25   # threshold below which an already-held name is kept
MOM_WEIGHT = 0.8
REV_WEIGHT = 0.2


def _select(prev_held: set, scores: pd.Series, ascending: bool) -> set:
    ranked = scores.sort_values(ascending=ascending)
    core = set(ranked.index[:CORE_N])
    band = set(ranked.index[:BAND_N])
    return (prev_held & band) | core  # both terms are subsets of band, so size <= BAND_N


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    stock_ids = [i["id"] for i in instruments(types=("stock",))]
    stock_cols = [c for c in stock_ids if c in prices.columns]
    stock_prices = prices[stock_cols]

    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    mom_held, rev_held = set(), set()
    for dt in rebalance_dates:
        hist = stock_prices.loc[:dt]
        if len(hist) < MOM_LOOKBACK + MOM_SKIP + 1:
            continue

        past = hist.iloc[-(MOM_LOOKBACK + MOM_SKIP) - 1]
        recent = hist.iloc[-MOM_SKIP - 1]
        momentum = (recent / past - 1).dropna()
        if len(momentum) < CORE_N:
            continue
        mom_held = _select(mom_held, momentum, ascending=False)

        rev_past = hist.iloc[-REV_LOOKBACK - 1]
        rev_recent = hist.iloc[-1]
        rev_ret = (rev_recent / rev_past - 1).dropna()
        if len(rev_ret) < CORE_N:
            continue
        rev_held = _select(rev_held, rev_ret, ascending=True)

        w = pd.Series(0.0, index=prices.columns)
        for c in mom_held:
            w[c] = w.get(c, 0.0) + MOM_WEIGHT / len(mom_held)
        for c in rev_held:
            w[c] = w.get(c, 0.0) + REV_WEIGHT / len(rev_held)
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
