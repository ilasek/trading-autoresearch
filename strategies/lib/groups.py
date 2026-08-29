"""Static group labels for the universe: sector-ish buckets and regions.

Why this is a library file rather than a per-candidate constant. The sector map
below was first written inside `strategies/candidates/mom_multihorizon_zscore_
sectorneutral.py`; the `lead-lag-spillover` family needs exactly the same map,
and copying it a second time invites the two copies to drift. The map is static
metadata about instruments, not a signal: it contains no dates, no prices and
nothing estimated from returns, so it cannot leak the future in the way a
fitted grouping could. It *is* current metadata about a survivorship-selected
universe, which is the standing caveat on every result in this repo and is not
made worse by writing the grouping down.

The completeness assertion at import time is the point of the module: a group
map that silently misses an instrument turns "the group's return" into "the
return of whichever members happened to be mapped".
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent.parent
UNIVERSE_FILE = ROOT / "data" / "universe.yaml"


SECTOR_GROUPS: dict[str, list[str]] = {
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

SECTOR_OF: dict[str, str] = {
    t: sector for sector, members in SECTOR_GROUPS.items() for t in members
}


def _universe_records() -> list[dict]:
    return yaml.safe_load(UNIVERSE_FILE.read_text())["instruments"]


REGION_OF: dict[str, str] = {r["id"]: r["region"] for r in _universe_records()}
TYPE_OF: dict[str, str] = {r["id"]: r["type"] for r in _universe_records()}

_missing = set(REGION_OF) - set(SECTOR_OF)
assert not _missing, f"sector map missing tickers: {sorted(_missing)}"


def labels(columns, mapping: dict[str, str]) -> pd.Series:
    """Group label per column, as a Series aligned to `columns`."""
    return pd.Series([mapping.get(c) for c in columns], index=list(columns))


def group_members(mapping: dict[str, str], min_size: int = 1) -> dict[str, list[str]]:
    """Inverse of a label mapping, dropping groups below `min_size`."""
    out: dict[str, list[str]] = {}
    for ticker, group in mapping.items():
        out.setdefault(group, []).append(ticker)
    return {g: sorted(m) for g, m in out.items() if len(m) >= min_size}
