"""The multi-year share-volume trend, and the overlapping-sleeve book on it.

Shared by `lv_vol_trend_overlap6` and `lv_vol_trend_hold1`, which differ in the
single integer `HOLD` passed to `vol_trend_book`.

THE SCORE. For each (recent, older) month-pair in `CELLS`, the log ratio of a
name's mean daily share volume over the last `recent` months to its mean over
the `older` months before that, converted to a cross-sectional normal score
**within the names eligible on the decision date**, and averaged over the cells.
Negated, so the book buys the names whose turnover is falling.

Two deliberate properties:

  * **Share counts only, never a level.** The store holds back-adjusted bars, so
    the price LEVEL and the volume LEVEL embed future corporate actions
    (`learnings.md`, 2026-10-22, filed as an engine issue). The standing rule
    there is that a candidate may use ratios and trends of the stored panels and
    may not use their levels. A ratio of two share-volume means for the same
    name is scale-free in share counts, so the contaminant cannot enter: the
    measured rank rho of this score to the log price level is +0.056.
  * **The knob is averaged away, not chosen.** Every (recent, older) pair whose
    recent window is at least 24 months is included, which is every pair the
    sleeve operator's own precondition admits at a six-month hold (the score's
    content must be older than the holding period). The three excluded pairs
    have a 12-month recent window and were excluded by that precondition before
    their scores were read.

THE BOOK. `K` names by a (trailing-trading-calendar peer group x price-history-
depth tercile) quota, re-picked every month-end, held in `HOLD` overlapping
sleeves: one sleeve is reformed each month and carried `HOLD` months as shares,
so the emitted row is the drifted book plus the reformed sleeve and only that
sleeve trades. `HOLD = 1` is the ordinary monthly top-K book.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

# Every (recent, older) month-pair with a recent window of at least 24 months.
CELLS = ((24, 24), (24, 36), (24, 60), (36, 36), (36, 60), (60, 60))
DEPTH_BINS = 3


def trend_frames(volume: pd.DataFrame, cells=CELLS) -> list[pd.DataFrame]:
    """One monthly-indexed log-volume-ratio frame per cell. A value on a month
    label uses only daily volume at or before that label."""
    mv = volume.resample("ME").mean()
    out = []
    for recent, older in cells:
        r = mv.rolling(recent, min_periods=max(6, recent // 2)).mean()
        o = mv.shift(recent).rolling(older, min_periods=max(6, older // 2)).mean()
        out.append(np.log(r.where(r > 0) / o.where(o > 0)))
    return out


def falling_turnover_score(frames: list[pd.DataFrame], date, names) -> pd.Series:
    """The averaged score on `names`, read at the latest month label at or
    before `date`. Each cell is normal-scored WITHIN `names` before averaging --
    pooling ranks formed on a wider set would make the average depend on names
    the book cannot buy (`learnings.md`, method, 2026-10-20/21)."""
    acc = None
    n = 0
    for f in frames:
        labels = f.index[f.index <= date]
        if not len(labels):
            continue
        v = f.loc[labels[-1]].reindex(names).dropna()
        if len(v) < 50:
            continue
        q = v.rank() / (len(v) + 1)
        z = pd.Series(norm.ppf(q.to_numpy()), index=v.index)
        acc = z if acc is None else acc.add(z, fill_value=np.nan)
        n += 1
    if acc is None or n == 0:
        return pd.Series(dtype=float)
    return -(acc.dropna() / n)


def vol_trend_book(prices, aux, eligible=None, k: int = 100, hold: int = 6):
    """The book. `hold` sleeves, one reformed per month-end and carried `hold`
    months as shares."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    px = prices.ffill()
    frames = trend_frames(volume)

    # History depth, as a candidate can count it: months of realized monthly
    # return in the visible window. Neutralised below, never sorted on
    # (`learnings.md`, 2026-10-26/27: depth is the panel's largest confound).
    mret = prices.resample("ME").last().pct_change(fill_method=None)
    depth = mret.notna().cumsum().reindex(prices.index, method="ffill")

    sleeves: dict[int, pd.Series] = {}
    formed: set[int] = set()
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Hold only names still eligible: the engine zeroes the rest, so a sleeve
        # carrying a leaver would be asking for a book it does not get.
        if sleeves:
            ok = set(names)
            sleeves = {s: sh[[n in ok for n in sh.index]] for s, sh in sleeves.items()}
            sleeves = {s: sh for s, sh in sleeves.items() if len(sh)}

        p = px.loc[date]
        vals = {s: float((sh * p.reindex(sh.index)).fillna(0.0).sum())
                for s, sh in sleeves.items()}
        value = float(sum(vals.values()))

        sc = falling_turnover_score(frames, date, names)
        picked = None
        if len(sc) >= 50:
            groups = calendar_peers(volume, date, sc.index).dropna()
            if len(groups) >= 50:
                sc = sc.reindex(groups.index)
                dep = depth.loc[date].reindex(groups.index)
                try:
                    bins = pd.qcut(dep.rank(method="first"), DEPTH_BINS, labels=False)
                except ValueError:
                    bins = pd.Series(0, index=dep.index)
                cells = groups.astype(str) + "|" + bins.astype(str)
                cand = peer_quota_select(sc, cells, k)
                if len(cand) >= 20:
                    picked = cand

        if picked is None:
            if value == 0.0:
                # Warm-up: hold the pool rather than cash, so the book is not
                # scored against a fully-invested benchmark while sitting out
                # (`learnings.md`, 2026-10-15/16).
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        # Which sleeve is due. Anchored on the CALENDAR month, not on the date's
        # position in the visible window, so truncation cannot move it.
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
