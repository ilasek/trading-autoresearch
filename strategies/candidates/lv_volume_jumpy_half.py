"""THE COMPLEMENT OF #50: THE JUMPY HALF, AND THE OBJECT A CORRECTED D2 ADMITS.

WHY THIS FILE EXISTS. `#50 lv_volume_quiet_alone` held the 100 eligible names with the
SMALLEST maximum one-day |d log share volume| in a 50-day window and recorded validation
gross skill +0.118 at the 98th percentile of its region- and type-matched null -- the
fourth object in 49 v3 trials to clear that gate, and the first near-orthogonal to every
reference object the lab holds. `#51` displaced the same window by 50 days and recorded
-0.017 at the 62nd percentile, which the 2026-11-27 session read as: recent share-volume
quietness is a short-lived STATE, worth an in-window term of +0.135.

That session also declined the complement of its own score -- the JUMPY half -- to honour
a pre-registration whose relabelling clause was written with an absolute value, and
flagged the clause as wrong in the same entry: a score at rank rho **+1** to another is
the same ordering, but a score at **-1** holds DISJOINT names and is a different book.
The corrected rule is `rho >= +0.90` plus a separate top-K Jaccard test. Measured tonight
on the train split, this object sits at rho **-1.000** to `#50`'s score and top-100
Jaccard **0.022** to `#50`'s book: it is a complement, not a relabelling, and it is the
one object the corrected rule unblocks.

ONE NODE CHANGES FROM #50: the sign of the score. Everything else -- K = 100, BAND = 200,
WINDOW = 50, the monthly grid, the (calendar peer x instrument type) quota, the equal
weighting, the warm-up branch -- is byte-identical.

FREE PRE-TRIAL SCREEN (train 1997-2017, 252 month-ends; rank and composition statistics
only. **No train Sharpe, train skill or train IC was computed for this object.**)

    quantity                                 value      #50 for reference
    month-to-month rank phi                  +0.6252    +0.6252  (equal under reversal)
    rank rho to the 5/45 volume shock        +0.0435    -0.042
    rank rho to 12-1 momentum                -0.0546    +0.060
    rank rho to 21-day reversal              +0.0310    +0.002
    rank rho to 126-day volatility           +0.0420    -0.048
    rank rho to amihud126                    +0.2875    -0.294
    rank rho to log mean dollar volume       -0.2841    +0.287
    rank rho to seasoning (history depth)    -0.2571    +0.264
    rank rho to #50's score                  -1.0000      --
    top-100 Jaccard to #50's book             0.022       --
    coverage of eligible names                99.9%      99.9%
    exit200 (top-200 retention band)          16.9%      19.7% (22.1% recorded)
    fund share / US share                    13.2% / 68.3%   3.9% / 82.3%
    transaction-tax-region share             13.5%       4.5%
    share in the >=$100M liquidity tier      17.8%      37.5%

The four rhos at or below 0.055 in absolute value say this is near-orthogonal to the
volume shock, momentum, reversal and the volatility axis, exactly as `#50` is; the three
slow confounds are carried at the mirror of `#50`'s loadings, which is what a complement
must do and is why the pair is matched on everything except which names it holds.

PRE-REGISTERED PREDICTIONS, written before the run (full text in the session's
pre-registration). Three disjoint branches on validation GROSS skill:
 (A) SYMMETRIC STATE -- the state is symmetric across the cross-section and the complement
     mirrors #50: **-0.16 to -0.08**, null percentile below 40%.
 (B) TAIL-ONLY / option-like -- the premium lives only in the quiet tail and this side
     carries nothing: **-0.05 to +0.05**, null percentile 40-75%. (2026-11-04/05's |b|/|t|
     instrument reads five of eight scores on this panel as carrying as much in the bottom
     as the top, which is what keeps both (A) and (B) live.)
 (C) WINDOW-REGIME -- the in-window term belongs to the 2018-2023 window rather than to a
     state, so both sides of the sort are positive in it: **above +0.05**, null percentile
     above 80%.
 CHURN by the corrected `24 x exit200%` arithmetic: train **3.0x-5.5x** (point 4.06x),
 validation **6.0x-11.0x** (point 8.0x, using #50's measured train->validation ratio 1.97).
 BILL per 1x **above #50's 10.2 bps**, because this book holds a less liquid and more
 taxed set (17.8% vs 37.5% in the top tier, 13.5% vs 4.5% taxed) and the per-1x constant
 is a property of holdings (2026-11-24).
 TRAIN SKILL is not predicted and was not screened; 44 of 47 recorded v3 trials fail that
 gate. **The statistic under test is the validation gross skill and the null percentile.
 The verdict is not the result.**

WHAT ARGUES AGAINST THE BOOK.
 (i) It has no source behind it. `#50`'s positive branch was already the alternative to
     the record's stated mechanism rather than a literature prior, and this is its
     complement; the hypothesis is an attribution claim about the lab's own 2x2, not an
     economic one.
 (ii) Share volume carries the split half of the as-of-fetch adjustment factor, so a split
     inside the window steps log volume by log(2) and makes a name look jumpy. Where `#50`
     systematically AVOIDED recent corporate actions, this book systematically SELECTS
     them. That is causal and is a real selection, but it is not the economics the title
     claims, and it is the single largest reservation about this arm.
 (iii) The composition screen says this is the expensive half of the panel. The bill is
     forecast above #50's and the gross has to clear it to leave anything.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
WINDOW = 50         # the same 5 + 45 scoring window #32/#47's cut and #50's score read

STRATEGY = {
    "name": "lv_volume_jumpy_half",
    "family": "liquidity-volume",
    "hypothesis": (
        "Holding the complement of #50's book -- the 100 eligible names with the LARGEST "
        "maximum one-day |d log share volume| anywhere in the 50-day window, every other "
        "node byte-identical to lv_volume_quiet_alone and only the sign of the score "
        "changed -- earns validation GROSS skill of -0.16 to -0.08 if the share-volume "
        "quietness state is SYMMETRIC across the cross-section and this side is the mirror "
        "of #50's +0.118; inside [-0.05, +0.05] if the premium is TAIL-ONLY and lives in "
        "the quiet extreme alone; and above +0.05 if the in-window term measured on "
        "2018-2023 belongs to that WINDOW rather than to a state, in which case both sides "
        "of the sort are positive in it. The object is admitted by the corrected "
        "relabelling rule (rho -1.000 but top-100 Jaccard 0.022 to #50's book: a complement "
        "holds disjoint names and is a different book), and it is the only reading of #50 "
        "that its own 2x2 never priced."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The 100 JUMPIEST eligible names by in-window maximum |d log volume|, quota'd across
    (calendar peer group x instrument type), monthly with a top-200 retention band.
    `lv_volume_quiet_alone` with the sign of the score reversed and nothing else changed.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    # #50's statistic with the sign reversed: the largest one-day move in log volume
    # anywhere in the scoring window, NOT negated, so a HIGH score is a JUMPY name.
    jumpy = lv.diff().abs().rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken (the
        # 2026-10-07 column-axis leak).
        score = jumpy.loc[date].reindex(names).dropna()
        if len(score) < 60:
            # Warm-up: hold the pool rather than cash (2026-10-15/16).
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()
        cells = (groups.reindex(score.index).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in score.index],
                             index=score.index))

        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, cells.reindex(rest.index).dropna(), K - len(keep))
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
