"""The three already-measured lead scores tonight's `portfolio-learning` pair blends.

WHY THIS FILE EXISTS. Research `#513` ("filter, then deconcentrate") is a statement
about a COMBINATION OPERATOR, not about a signal: per lead, keep a broad selection on
that lead's own score, then inside each selection drop the names with the worst
composite rank across the OTHER leads, then equal-weight and blend the legs. Testing
an operator needs the legs held fixed across both arms of a paired trial, so the leg
scores live here and are imported byte-identically by both candidates.

WHY THESE THREE LEGS.
  rev -- LONG-HORIZON REVERSAL. `-mean(monthly return)` over months -120..-61, i.e. the
      score behind `pt_oldhalf_overlap6`, the board lead under v3 (skill +0.124) and the
      slowest object recorded here (month-to-month rank persistence phi +0.980).
  mom -- 12-1 MOMENTUM. The most-studied cross-sectional characteristic there is, measured
      a null on this panel, and MECHANICALLY OPPOSED to R: a name in the top half on
      long-horizon reversal and the bottom half on recent momentum is exactly the
      "offsetting scores" case research `#514` names as the mechanism of the
      mix-versus-composite crossover. Including it is what gives the filter work to do.
  vshock -- VOLUME SHOCK. Mean log share volume over the last 5 printing days minus the
      median over the preceding 45, split-guarded, i.e. the score behind
      `lv_volume_shock_gkm_band` -- the ONLY object in 31 recorded v3 trials to clear the
      random-selection null (p = 0.010) and the most decorrelated one on the board
      (max |rho| +0.265 in active returns). phi -0.022: the fast leg.

EVERY SCORE IS A RATIO, A RETURN OR A DIFFERENCE OF LOGS. `learnings.md` (2026-10-21/22,
filed as an engine issue) records that the stored price and volume LEVELS are not causal
-- Yahoo's bars carry the product of every distribution factor after each date, which
cancels in a ratio inside the visible window and dominates a level (log price level scores
a within-region rank IC of -0.0878). `dollar_volume = close x volume` keeps the dividend
half of that factor and is therefore not used anywhere in this file.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# --- leg rev: long-horizon reversal (the board lead's score) -------------------
REV_LAG = 60          # months skipped before the window starts
REV_SPAN = 60         # window length, in months
REV_MIN = 48          # of REV_SPAN

# --- leg mom: 12-1 momentum ----------------------------------------------------
MOM_LOOKBACK = 252
MOM_SKIP = 21

# --- leg vshock: volume shock (the one object that cleared the null gate) ---------
VS_FAST = 5          # printing days of recent volume
VS_SLOW = 45         # printing days of baseline, ending VS_FAST+1 days ago
VS_SPLIT_GUARD = np.log(3.0)


def reversal_score(prices: pd.DataFrame) -> pd.DataFrame:
    """Leg R, daily-indexed: minus the mean monthly return over months -120..-61.

    A value published on a month label uses only returns realized at or before that
    label; the daily reindex forward-fills, so a decision date reads the latest label
    at or before it.
    """
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    old = mret.shift(REV_LAG).rolling(REV_SPAN, min_periods=REV_MIN).mean()
    return (-old).reindex(prices.index, method="ffill")


def momentum_score(prices: pd.DataFrame) -> pd.DataFrame:
    """Leg M, daily-indexed: the 12-month return skipping the most recent month."""
    px = prices.ffill()
    return px.shift(MOM_SKIP) / px.shift(MOM_SKIP + MOM_LOOKBACK) - 1.0


def volume_shock_score(volume: pd.DataFrame) -> pd.DataFrame:
    """Leg V, daily-indexed: mean log volume over the last VS_FAST printing days minus
    the median over the preceding VS_SLOW, with a causal split guard.

    The guard drops any name showing a daily |log volume change| above log(3) anywhere
    in the window, so a split's as-of-fetch step cannot enter the score. Volume is not
    forward-filled, so a NaN is a non-print and the score is taken over prints only.
    """
    lv = np.log(volume.where(volume > 0))
    fast = lv.rolling(VS_FAST, min_periods=3).mean()
    slow = lv.shift(VS_FAST).rolling(VS_SLOW, min_periods=25).median()
    shock = fast - slow
    step = lv.diff().abs().rolling(VS_FAST + VS_SLOW, min_periods=25).max()
    return shock.where(step < VS_SPLIT_GUARD)


def leg_scores(prices: pd.DataFrame, volume: pd.DataFrame) -> dict:
    """All three legs, daily-indexed on `prices.index`."""
    return {
        "rev": reversal_score(prices),
        "mom": momentum_score(prices),
        "vshock": volume_shock_score(volume),
    }


def pct_rank(s: pd.Series) -> pd.Series:
    """Cross-sectional percentile rank in [0, 1], high score = high rank.

    Taken AFTER masking to the names eligible on the decision date -- never pooled
    across groups (`learnings.md`, 2026-10-20/21).
    """
    s = s.dropna()
    if len(s) < 2:
        return pd.Series(dtype=float)
    return s.rank(method="average") / float(len(s))
