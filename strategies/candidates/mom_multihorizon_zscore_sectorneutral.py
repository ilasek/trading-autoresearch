"""Sector-neutral variant of the repo's strongest challenger to date
(`mom_multihorizon_zscore_buffered`, val Sharpe 1.03, DSR 0.9333, unpromoted).

Three consecutive trials escalating within-basket weighting *intensity* (equal
-> rank -> z-score magnitude -> two-horizon z-score magnitude) each raised
validation Sharpe but also walked validation maxDD out in lockstep (-30.2% ->
-32.4% -> -36.0%), and a follow-up dampening trial confirmed the effect is
real signal, not a variance artifact of concentration (see learnings.md).
learnings.md's open question for a future session: is a *structurally
different* lever available that trims risk without fighting the signal
itself? This candidate tests one: the winning basket's composite z-score is
computed globally, so if momentum is being driven by a handful of correlated
sectors/asset-classes at once (a textbook mechanism behind momentum-crash
drawdowns), the basket can end up concentrated in that one bloc even though
membership/weighting look diversified by name count. Neutralizing the
6-1/12-1 composite z-score *within* a coarse sector/asset-class grouping
before ranking and weighting should, if that mechanism is real, spread the
basket's exposure across blocs and reduce validation maxDD relative to
`mom_multihorizon_zscore_buffered`, while giving up only a modest amount of
Sharpe (not fighting the within-bloc magnitude-weighting edge, which prior
trials established is real).

Sector/asset-class groups below are a coarse, hand-curated, GICS-like
classification of this repo's 140-instrument universe (by ticker only, no
external data) — good enough to test the neutralization mechanism, not meant
to be authoritative. Every price column must map to exactly one group; a
compile-time assertion checks full coverage against `data/universe.yaml` so
a silently-mis-bucketed name can't slip through.
"""

import pandas as pd
import yaml
from pathlib import Path

STRATEGY = {
    "name": "mom_multihorizon_zscore_sectorneutral",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Neutralizing the composite 6-1/12-1 momentum z-score within coarse "
        "sector/asset-class groups before ranking and weighting the buffered "
        "momentum basket (hold top 25, enter top 15) reduces validation "
        "maxDD relative to the globally-ranked `mom_multihorizon_zscore_"
        "buffered` (val Sharpe 1.03, maxDD -36.0%), because it prevents a "
        "handful of correlated sectors from dominating basket exposure even "
        "when name-level diversification looks adequate, net of 15 bps costs."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

_SECTOR_GROUPS = {
    "tech": [
        "AAPL", "MSFT", "NVDA", "AVGO", "ORCL", "CRM", "AMD", "ADBE", "CSCO",
        "ACN", "INTC", "IBM", "QCOM", "TXN", "TSM", "ASML", "SAP_DE", "IFX_DE",
        "8035_JP", "INFY", "XLK",
    ],
    "communication": [
        "GOOGL", "META", "NFLX", "DIS", "VZ", "DTE_DE", "9432_JP", "0941_HK",
        "9984_JP", "0700_HK", "7974_JP",
    ],
    "consumer_discretionary": [
        "AMZN", "TSLA", "HD", "NKE", "MCD", "BABA", "VOW3_DE", "BMW_DE",
        "ADS_DE", "7203_JP", "6758_JP", "3690_HK", "XLY",
    ],
    "consumer_staples": [
        "WMT", "PG", "KO", "PEP", "COST", "UL", "BATS_UK", "DGE_UK", "XLP",
    ],
    "financials": [
        "JPM", "V", "MA", "BAC", "GS", "MS", "BLK", "SPGI", "ALV_DE",
        "MUV2_DE", "DBK_DE", "HSBA_UK", "LLOY_UK", "BARC_UK", "LSEG_UK",
        "8306_JP", "1299_HK", "1398_HK", "0388_HK", "XLF",
    ],
    "healthcare": [
        "UNH", "JNJ", "MRK", "ABBV", "LLY", "TMO", "PFE", "NVO", "AZN_UK",
        "GSK_UK", "BAYN_DE", "XLV",
    ],
    "energy": ["XOM", "CVX", "SHEL", "TTE", "BP_UK", "XLE"],
    "industrials": [
        "CAT", "GE", "HON", "UPS", "SIE_DE", "REL_UK", "6501_JP", "6954_JP",
        "XLI",
    ],
    "materials": ["BHP", "RIO", "BAS_DE", "4063_JP", "XLB"],
    "utilities": ["XLU"],
    "real_estate": ["VNQ"],
    "broad_market_etf": [
        "SPY", "QQQ", "IWM", "DIA", "VTI", "VEA", "VWO", "EEM", "EFA", "VT",
        "ACWI",
    ],
    "country_etf": [
        "EWJ", "EWG", "EWU", "FXI", "INDA", "EWZ", "EWY", "EWT", "EWA", "MCHI",
    ],
    "bonds": ["AGG", "BND", "TLT", "IEF", "SHY", "LQD", "HYG", "TIP"],
    "commodities": ["GLD", "SLV", "DBC"],
}

_TICKER_SECTOR = {t: sec for sec, tickers in _SECTOR_GROUPS.items() for t in tickers}

_UNIVERSE_IDS = {
    i["id"]
    for i in yaml.safe_load(
        (Path(__file__).resolve().parent.parent.parent / "data" / "universe.yaml").read_text()
    )["instruments"]
}
_missing = _UNIVERSE_IDS - set(_TICKER_SECTOR)
assert not _missing, f"sector map missing tickers: {sorted(_missing)}"


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def _sector_neutral_zscore(s: pd.Series) -> pd.Series:
    groups = s.index.to_series().map(_TICKER_SECTOR)
    return s.groupby(groups).transform(_zscore)


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK_LONG + SKIP + 1:
            continue
        mom_long = _momentum(hist, LOOKBACK_LONG)
        mom_short = _momentum(hist, LOOKBACK_SHORT)
        common = mom_long.index.intersection(mom_short.index)
        if len(common) < CORE_N:
            continue

        composite = _sector_neutral_zscore(mom_long[common]) + _sector_neutral_zscore(
            mom_short[common]
        )

        ranked = composite.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core

        c_held = composite[list(held)]
        raw = c_held - c_held.min() + FLOOR
        norm = raw / raw.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w = pd.Series(0.0, index=prices.columns)
        w[norm.index] = norm
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
