"""The closing-location-value (CLV) score and the book this lab prices it in.

WHAT THE SCORE IS. For each name and day, `(close - low) / (high - low)`: where
the close sits inside the day's own trading range, 0 at the low and 1 at the
high. Averaged over a trailing window and lagged, it measures how persistently a
name has been closing in the lower or upper part of its own range.

WHY IT IS A DIFFERENT OBJECT FROM EVERY PRICE SCORE ALREADY MEASURED HERE.

  (i) It is invariant to any same-day multiplicative price adjustment. All three
      inputs are that day's own quotes, so a split or dividend factor applied to
      the series cancels exactly in the ratio. `experiments/learnings.md`
      (2026-10-22, filed as an engine issue) records that the stored price and
      volume LEVELS embed future corporate actions and that neither
      `causality_check` nor the hindsight guard can see it; a within-day ratio
      cannot carry that contaminant at all. The measured residue is a rank rho of
      +0.202 to the log price level, which is the correlation of a real
      characteristic with price, not a channel for the adjustment.

  (ii) It is not a close-to-close return. It uses no information about where the
      previous close was, so it is not a horizon of the momentum / reversal
      lineage. Measured on train month-ends it nevertheless shares a rank rho of
      +0.439 with 12-1 momentum -- a name that trended up does close near its
      highs -- which is why the book below allocates its quota across momentum
      terciles. Inside those cells the rho falls to +0.063.

THE CONSTRUCTION, and each node has a reason recorded in `learnings.md`:

  - `calendar_peers` cells, so the claim is name selection within listing market
    rather than geography (2026-10-13/14: the skill statistic is against a pool
    that is 76% US on train, and only the null prices a region bet).
  - a second quota axis crossed with the peer group, so the book is neutral to it
    by construction. `cells="mom"` uses 12-1 momentum terciles (the axis CLV
    overlaps); `cells="depth"` uses price-history-depth terciles, the axis every
    recorded M3 trial uses and the control for whether neutralising momentum is
    what carries the book.
  - `peer_quota_select` at K=100, and K is NOT a knob here: it is the value every
    v3 trial of this lab has used (2026-10-28/29 makes K a standing
    anti-candidate at either holding period).
  - overlapping sleeves, `hold` of them, one reformed each month-end and carried
    `hold` months as shares, exactly as `pt_oldhalf_overlap6` does. The cost
    channel is the one operator channel this lab has measured as transferring
    (+0.008 to +0.013 of skill on all seven objects it was priced on, and +0.011
    on validation against train's +0.0096).
  - names that stop being eligible are pruned at every month-end, because the
    engine zeroes them anyway.

Causality: every input is a trailing rolling window, the score is shifted clear
of the decision date, the sleeve index is anchored on the calendar month rather
than on a position inside the visible window, and `calendar_peers` is passed
only the names eligible on the decision date.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
WINDOW = 756      # trading days of CLV averaged
LAG = 21          # days the average is shifted clear of the decision date
HOLD = 6          # overlapping sleeves
CELL_BINS = 3


def clv_score(prices: pd.DataFrame, aux: dict, window: int = WINDOW,
              lag: int = LAG, sign: float = 1.0) -> pd.DataFrame:
    """Minus the trailing mean closing location value: high where a name has
    persistently closed in the LOWER part of its own daily range."""
    rng = aux["high"] - aux["low"]
    clv = ((prices - aux["low"]) / rng).where(rng > 0)
    mean = clv.rolling(window, min_periods=int(window * 0.63)).mean().shift(lag)
    return sign * (-mean)


def _cell_values(prices: pd.DataFrame, cells: str) -> pd.DataFrame:
    if cells == "mom":
        return prices.pct_change(252, fill_method=None).shift(21)
    if cells == "depth":
        monthly = prices.resample("ME").last().pct_change(fill_method=None)
        return monthly.notna().cumsum().reindex(prices.index, method="ffill")
    raise ValueError(cells)


def clv_book(prices: pd.DataFrame, aux: dict, eligible=None, cells: str = "mom",
             k: int = K, hold: int = HOLD, window: int = WINDOW,
             sign: float = 1.0) -> pd.DataFrame:
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    volume = aux["volume"]
    px = prices.ffill()
    score = clv_score(prices, aux, window=window, sign=sign)
    cell_vals = _cell_values(prices, cells)

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
                # Warm-up: hold the pool rather than cash, so the book is not scored
                # against a fully-invested benchmark while sitting out (2026-10-15/16).
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
