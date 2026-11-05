"""The session boundary inside the daily bar, as a cross-sectional characteristic.

WHAT THE SCORE IS. A daily bar is two sessions: the overnight gap from the
previous close to today's open, and the intraday move from the open to the close.
For each name and day,

    overnight_drift = (open - previous close) / (high - low)

is the overnight move expressed in units of that day's own trading range.
Averaged over a trailing window and lagged, it says how much of a name's daily
travel has persistently happened while the exchange was shut. The shipped score
is its NEGATIVE, so the book buys the names with the LEAST persistent overnight
gain.

WHY THE RANGE NORMALISATION IS THE DESIGN, NOT A DETAIL. Dividing by the close
would give a plain overnight return, and `experiments/learnings.md` (2026-10-24/25)
records the overnight leg of the short-horizon reversal as a pure null on this
panel. Dividing by the day's own range instead makes the quantity unit-free and
scale-free in the one dimension that differs across names and regimes: it asks
what FRACTION of the day's movement was overnight, not how many basis points it
was. `session_return_score` below is the un-normalised version, kept so the
normalisation can be tested as one node of a pair rather than asserted.

WHY IT IS A DIFFERENT OBJECT FROM EVERY SCORE ON THE v3 BOARD. Mean rank rho over
252 train month-ends: 12-1 momentum **+0.029**, the decade mean -0.162, the old
half -0.009, 126-day volatility -0.116, Amihud +0.087, the share-turnover trend
-0.095, the log price level **-0.003**, tonight's CLV score +0.230. Inside
(calendar-peer x momentum-tercile) cells the momentum rho is **+0.007**. That is
the cleanest novelty profile in this lab's v3 record, and the -0.003 to the log
price level matters specifically: the 2026-10-22 engine issue records that stored
price and volume LEVELS embed future corporate actions invisibly to both
`causality_check` and the hindsight guard, and a ratio whose numerator and
denominator are quotes one day apart on the same adjusted series carries almost
none of it.

THE CONSTRUCTION is the one `strategies/lib/clv_book.py` documents, node for
node: `calendar_peers` cells crossed with momentum terciles, `peer_quota_select`
at K=100, six overlapping monthly sleeves with one reformed each month-end, and
ineligible names pruned at every month-end. It is reproduced here rather than
imported with a different score because `clv_book.py` is already the source of a
recorded trial and must not change.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
WINDOW = 756
LAG = 21
HOLD = 6
CELL_BINS = 3


def overnight_drift_score(prices: pd.DataFrame, aux: dict, window: int = WINDOW,
                          lag: int = LAG, sign: float = 1.0) -> pd.DataFrame:
    """Minus the trailing mean of (open - previous close) / (high - low): high
    where a name has persistently gained the LEAST overnight, as a share of its
    own daily range."""
    rng = aux["high"] - aux["low"]
    x = ((aux["open"] - prices.shift(1)) / rng).where(rng > 0)
    return sign * (-x.rolling(window, min_periods=int(window * 0.63)).mean().shift(lag))


def session_return_score(prices: pd.DataFrame, aux: dict, window: int = WINDOW,
                         lag: int = LAG, sign: float = 1.0) -> pd.DataFrame:
    """The same quantity with the range normalisation removed: minus the trailing
    mean overnight RETURN, (open - previous close) / previous close."""
    prev = prices.shift(1)
    x = ((aux["open"] - prev) / prev.where(prev > 0))
    return sign * (-x.rolling(window, min_periods=int(window * 0.63)).mean().shift(lag))


def _cell_values(prices: pd.DataFrame) -> pd.DataFrame:
    return prices.pct_change(252, fill_method=None).shift(21)


def session_book(prices: pd.DataFrame, aux: dict, eligible=None, score_fn=None,
                 k: int = K, hold: int = HOLD, window: int = WINDOW,
                 sign: float = 1.0) -> pd.DataFrame:
    score_fn = score_fn or overnight_drift_score
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    volume = aux["volume"]
    px = prices.ffill()
    score = score_fn(prices, aux, window=window, sign=sign)
    cell_vals = _cell_values(prices)

    sleeves: dict[int, pd.Series] = {}
    formed: set[int] = set()
    rows: dict = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue
        if sleeves:
            ok = set(names)
            sleeves = {s: sh[[n in ok for n in sh.index]] for s, sh in sleeves.items()}
            sleeves = {s: sh for s, sh in sleeves.items() if len(sh)}
        p = px.loc[date]
        vals = {s: float((sh * p.reindex(sh.index)).fillna(0.0).sum())
                for s, sh in sleeves.items()}
        value = float(sum(vals.values()))

        sc = score.loc[date].reindex(names)
        sc = sc[np.isfinite(sc)].dropna()
        picked = None
        if len(sc) >= 50:
            groups = calendar_peers(volume, date, sc.index).dropna()
            if len(groups) >= 50:
                sc = sc.reindex(groups.index)
                cv = cell_vals.loc[date].reindex(groups.index)
                try:
                    bins = pd.qcut(cv.rank(method="first"), CELL_BINS, labels=False)
                except ValueError:
                    bins = pd.Series(0, index=cv.index)
                cell = groups.astype(str) + "|" + bins.fillna(0).astype(int).astype(str)
                cand = peer_quota_select(sc, cell, k)
                if len(cand) >= 20:
                    picked = cand

        if picked is None:
            if value == 0.0:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        sleeve = (date.year * 12 + date.month - 1) % hold
        if value == 0.0:
            target = 1.0
        elif sleeve not in formed:
            target = value / hold
            sleeves = {s: sh * ((value - target) / value) for s, sh in sleeves.items()}
        else:
            target = vals.get(sleeve, 0.0)

        pp = p.reindex(picked)
        pp = pp[pp > 0].dropna()
        if len(pp) < 20 or target <= 0:
            continue
        sleeves[sleeve] = (target / len(pp)) / pp
        formed.add(sleeve)

        held = pd.Series(0.0, index=prices.columns, dtype=float)
        for sh in sleeves.values():
            held = held.add((sh * p.reindex(sh.index)).reindex(prices.columns).fillna(0.0),
                            fill_value=0.0)
        total = float(held.sum())
        if total > 0:
            rows[date] = held[held > 1e-12] / total

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0).sort_index()
