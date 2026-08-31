"""Integrated (score-level) blending of family-lead signals.

WHY THIS IS A SEPARATE FILE FROM `blend.py`. `blend.py` combines finished
*books*: it takes weight matrices and mixes capital between them. That is the
"portfolio mix", and `experiments/learnings.md` records (2026-08-30) that it is
bounded between its components by construction — an equal-weight mix of the
eight recorded legs is monotone *decreasing* in leg count against the best
single member, so the family closed on arithmetic.

`research/SUMMARY.md` #60 names the gap in that closure: the bound applies to
the mix, not to the **integrated** construction — average the legs'
cross-sectional *scores* first, then build one long-only book in a single step.
The two differ because a name that is jointly attractive on several legs, but
top-decile on none, is unreachable by any mix of the legs' books and is exactly
what an integrated score selects. This module is that second function.

The gap between the two is governed by the **cross-sectional correlation of the
signals**, which is not the quantity the closure was measured on: that used the
correlation of the legs' realised return series (0.68-0.98), which shares a
large common long-only market component. Measured on cross-sectional signal
ranks over the same instruments and dates, the four leads below correlate at a
mean |rho| of 0.054 on train and 0.070 on validation (max 0.448, the
mechanically-related group-lead / 21-day-reversal pair). See the 2026-08-31
journal entry.

WEIGHTS ARE EQUAL AND THAT IS LOAD-BEARING. `SUMMARY.md` #1's parameter-counting
screen forbids estimating them: a scheme that estimates nothing carries no
estimation error, and this universe's cross-section (~140 names) is nowhere near
long enough to fit four leg weights honestly. `learnings.md` reaches the same
conclusion from the other side — "equal weights between legs are load-bearing".

EVERY LEG IS CAUSAL. Each function below reads only rows at or before the date
it is asked about; none uses a forward return, and none is fitted. The panels
are published on month-end rebalance rows and never forward-filled past the
next rebalance, so a truncated frame reproduces its own history exactly.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

# Same-calendar-month seasonal, matching `sc_same_month_seasonal_aligned`.
ANN_YEARS = 20        # same-month observations averaged
NON_MONTHS = 240      # other-month observations averaged
MIN_SAME = 5          # need at least this many same-month observations


def seasonal_score(prices: pd.DataFrame) -> pd.DataFrame:
    """Average return in the calendar month about to start minus the average
    over all other months, published on each month-end row.

    `MonthBegin(1)`, not `MonthEnd(1)`: rebalance dates are the last *trading*
    day of a month, which on 29.8% of train months is not the last calendar day,
    and `MonthEnd(1)` then names the month that has just ended (trials #59/#60).
    `strategies/lib/features.seasonal_same_month_return` still carries that bug
    and may not be edited, so the corrected version lives here.
    """
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    month_pos = {p: i for i, p in enumerate(monthly.index.to_period("M"))}

    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in W.rebalance_dates(prices):
        i = month_pos.get(dt.to_period("M"))
        if i is None or i < MIN_SAME * 12:
            continue
        past = mret.iloc[:i]                    # strictly before the current month
        target = (dt + pd.offsets.MonthBegin(1)).month
        same = past[past.index.month == target].tail(ANN_YEARS)
        other = past[past.index.month != target].tail(NON_MONTHS)
        if len(same) < MIN_SAME or len(other) < 24:
            continue
        rows[dt] = (same.mean() - other.mean()).where(same.notna().sum() >= MIN_SAME)

    if not rows:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns)


def group_lead_score(
    prices: pd.DataFrame, lookback: int = 21, min_group: int = 4
) -> pd.DataFrame:
    """Each name scored by the median trailing `lookback`-day return of its own
    sector group — the group-level continuation `ll_group_lastmonth_lead` found,
    broadcast back to members so it can be averaged with name-level scores."""
    members = G.group_members(G.SECTOR_OF, min_size=min_group)
    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in W.rebalance_dates(prices, warmup=2):
        hist = prices.loc[:dt]
        if len(hist) < lookback + 2:
            continue
        ret = hist.iloc[-1] / hist.iloc[-1 - lookback] - 1.0
        out: dict[str, float] = {}
        for group, mem in members.items():
            present = [m for m in mem if m in ret.index and pd.notna(ret[m])]
            if len(present) < min_group:
                continue
            med = float(ret[present].median())
            for name in present:
                out[name] = med
        if out:
            rows[dt] = pd.Series(out)

    if not rows:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns)


def reversal_score(prices: pd.DataFrame, lookback: int = 21) -> pd.DataFrame:
    """Negative trailing `lookback`-day return — `pt_raw_reversal_control`."""
    return -(prices / prices.shift(lookback) - 1.0)


def illiquidity_score(
    prices: pd.DataFrame, dollar_volume: pd.DataFrame, window: int = 63
) -> pd.DataFrame:
    """Amihud ILLIQ — `lv_amihud_illiquidity_tilt`."""
    return F.amihud_illiquidity(prices, dollar_volume, window)


def integrate(scores: dict[str, pd.DataFrame], at: pd.Timestamp,
              min_names: int = 20) -> pd.Series:
    """Equal-weighted average of each leg's cross-sectional z-score at `at`.

    Every leg is z-scored *within its own cross-section first*, so legs
    denominated in different units (a return, an illiquidity ratio, a seasonal
    mean) contribute on one scale. The average is taken over the instruments
    every leg can score, so no name enters on a partial set of legs — a name
    scored by two legs and NaN on the other two would otherwise receive a
    different, quieter signal than its neighbours.

    Returns an empty Series when the legs do not jointly cover enough names.
    """
    zs: list[pd.Series] = []
    common: pd.Index | None = None
    for panel in scores.values():
        sub = panel.loc[:at]
        if sub.empty:
            return pd.Series(dtype=float)
        row = sub.iloc[-1].dropna()
        if len(row) < min_names:
            return pd.Series(dtype=float)
        sd = row.std(ddof=0)
        if not sd > 0:
            return pd.Series(dtype=float)
        z = (row - row.mean()) / sd
        zs.append(z)
        common = z.index if common is None else common.intersection(z.index)

    if common is None or len(common) < min_names:
        return pd.Series(dtype=float)
    total = sum(z.reindex(common) for z in zs)
    return total / len(zs)
