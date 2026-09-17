"""Characteristic-sorted long-only sub-portfolios ("sleeves") and books over them.

Added 2026-09-17 for `research/SUMMARY.md` #114/#115 (factor momentum). The two
candidates that use it — `pl_factor_momentum_timed` and its untimed control — are
a designed pair and must differ at exactly one node, so the construction they
share lives here rather than being copied into both files.

Everything here is causal by construction: every frame handed in is already
truncated to the visible window by the protocol, `sleeve_members` reads one row
of an already-trailing characteristic, and `sleeve_returns` reads only realized
month-to-month price changes. Nothing indexes past the row it is asked about.

NOTE ON THE FILE-PERMISSION RULE: `strategies/lib/` may gain new files but no
existing one may ever be edited, because a promoted candidate keeps importing it.
This file is therefore frozen from the moment it is committed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import features as F
from . import walkforward as W

# The six characteristics, pre-registered in the journal under
# "Pre-registration — 2026-09-17 (nightly)" BEFORE any of them was profiled.
CHARACTERISTICS = ("trend", "reversal", "illiq", "gkvol", "volshock", "dvrank")

TOP_N = 20        # names per sleeve leg
LOOKBACK = 12     # months of own demeaned return the timing rule reads
WARMUP = 15       # month-end rows skipped so every characteristic is computable


def characteristic_frames(prices: pd.DataFrame, aux: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """The six pre-registered characteristic panels, all trailing."""
    return {
        "trend": F.trailing_return(prices, 252, skip=21),
        "reversal": F.trailing_return(prices, 21, skip=0),
        "illiq": F.amihud_illiquidity(prices, aux["dollar_volume"], 63),
        "gkvol": F.garman_klass_vol(aux["high"], aux["low"], prices, 21),
        "volshock": F.volume_shock(aux["volume"], 63),
        "dvrank": F.dollar_volume_rank(aux["dollar_volume"], 63),
    }


def build_sleeves(prices: pd.DataFrame, aux: dict[str, pd.DataFrame]):
    """Twelve sleeves — both legs of six characteristics.

    Returns `(dates, members, sleeve_returns, market)` where

      dates           month-end rows of the visible frame after WARMUP,
      members         {sleeve: {formation_date: [tickers]}},
      sleeve_returns  DataFrame (formation dates x sleeves) of the simple return
                      EARNED OVER THE MONTH ENDING ON THAT ROW, i.e. row `t` holds
                      the return of the book formed at `t - 1` month. Realized and
                      visible at `t`.
      market          equal-weighted universe monthly return on the same index.

    Both legs are kept because the source's construction is model-free: it takes
    the long side after the spread has been positive and the short side after it
    has been negative, and the long-only analogue of "take the short side" is to
    hold the other leg rather than to sit out.
    """
    chars = characteristic_frames(prices, aux)
    dates = list(W.rebalance_dates(prices, warmup=WARMUP))
    if len(dates) < LOOKBACK + 2:
        return dates, {}, pd.DataFrame(), pd.Series(dtype=float)

    mpx = prices.reindex(dates)
    mret = mpx.pct_change()

    members: dict[str, dict] = {}
    returns: dict[str, dict] = {}
    for cname, cframe in chars.items():
        cm = cframe.reindex(dates)
        for leg in ("hi", "lo"):
            key = f"{cname}_{leg}"
            members[key], returns[key] = {}, {}
            for i in range(len(dates) - 1):
                t, nxt = dates[i], dates[i + 1]
                score = cm.loc[t].dropna()
                fwd = mret.loc[nxt].reindex(score.index).dropna()
                score = score.reindex(fwd.index)
                if len(score) < 40:
                    continue
                sel = score.nlargest(TOP_N).index if leg == "hi" else score.nsmallest(TOP_N).index
                members[key][t] = list(sel)
                returns[key][nxt] = float(fwd.reindex(sel).mean())

    sleeve_returns = pd.DataFrame({k: pd.Series(v) for k, v in returns.items()}).sort_index()
    market = mret.mean(axis=1).reindex(sleeve_returns.index)
    return dates, members, sleeve_returns, market


def timing_signal(sleeve_returns: pd.DataFrame, market: pd.Series) -> pd.DataFrame:
    """Trailing `LOOKBACK`-month sum of each sleeve's DEMEANED monthly return.

    Demeaning against the equal-weighted universe is load-bearing, not cosmetic:
    an un-demeaned long-only sleeve return is mostly the market, so the sign of
    its trailing sum carries almost no cross-sleeve information. Row `t` reads
    only returns realized at or before `t`.
    """
    demeaned = sleeve_returns.sub(market, axis=0)
    return demeaned.rolling(LOOKBACK).sum()


def book_weights(members: dict, sleeve_returns: pd.DataFrame, columns,
                 selector) -> pd.DataFrame:
    """Equal weight across the selected sleeves, then equal weight inside each.

    `selector(formation_date) -> list[str]` names the sleeves live at that date.
    A name held by several selected sleeves accumulates their weights, which is
    what "equal weight across sub-portfolios" means for overlapping books.
    """
    rows: dict[pd.Timestamp, pd.Series] = {}
    all_sleeves = list(sleeve_returns.columns)
    if not all_sleeves:
        return pd.DataFrame(columns=columns, dtype=float)

    for i in range(LOOKBACK, len(sleeve_returns.index)):
        formation = sleeve_returns.index[i - 1]
        live = selector(formation) or all_sleeves
        acc: dict[str, float] = {}
        per_name = 1.0 / (len(live) * TOP_N)
        for sleeve in live:
            for name in members.get(sleeve, {}).get(formation, ()):  # noqa: B905
                acc[name] = acc.get(name, 0.0) + per_name
        if acc:
            rows[formation] = pd.Series(acc)

    if not rows:
        return pd.DataFrame(columns=columns, dtype=float)
    out = pd.DataFrame(rows).T.reindex(columns=columns).fillna(0.0)
    total = out.sum(axis=1)
    return out.div(total.where(total > 0), axis=0).fillna(0.0)


def sharpe(monthly: pd.Series) -> float:
    monthly = monthly.dropna()
    if len(monthly) < 2 or monthly.std() == 0:
        return float("nan")
    return float(np.sqrt(12) * monthly.mean() / monthly.std())
