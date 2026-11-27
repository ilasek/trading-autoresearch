"""THE MISSING CELL OF THE 2026-11-25 2x2: THE PURITY FILTER'S OWN QUANTITY AS THE SCORE.

WHAT THE RECORD SAYS AND WHAT IT DOES NOT. `lv_volume_shock_gkm_band` (#32) and its
parameter-free replication `lv_volume_shock_median_guard` (#47) are the only objects in 47
recorded v3 trials to clear the region- and type-matched random-selection null, and the
2026-11-25 session measured that TWO THIRDS of #32's gross skill lives in one node its own
file documents as hygiene -- a cut on the largest one-day |d log share volume| anywhere in
the 50-day scoring window. That session ran three arms and the 2026-11-26 session added the
fourth channel:

    arm                                      gross skill
    bare 5/45 volume shock, no cut              +0.066
    shock + the cut read IN the window          +0.211      <- #32
    shock + the cut DISPLACED to -100..-51      +0.101
    (the same operator on the return channel)   +0.009      <- inert; closed as channel-specific

The in-window TERM is +0.145 and the standing explanation is BASELINE PURITY: a "last 5 days
minus the preceding 45" score whose 45-day baseline itself contains an explosion is measuring
a decaying baseline rather than a fresh event, so excluding those names CLEANS THE SCORE. That
explanation makes the term an INTERACTION between the cut and the shock sort.

**The 2x2 was never completed.** No arm has ever traded the cut's own quantity with the shock
sort REMOVED. If baseline purity is the mechanism, that book carries nothing: there is no
baseline left to clean. If instead the +0.145 is a MAIN EFFECT -- names whose share volume has
been quiet are simply better names to hold on this panel -- then the board has a selection it
has never priced, and the 2026-11-25 attribution of #32 is wrong in kind rather than in size.
This file is the one trial that separates those two readings, and the direction is pre-signed
in both branches.

ONE NODE CHANGES FROM #47. The score becomes the NEGATED in-window maximum jump (high score =
quiet name) and the separate median cut disappears, because the cut and the score are now the
same quantity. K = 100, BAND = 200, the monthly grid, the (calendar peer x instrument type)
quota, the equal weighting and the warm-up branch are byte-identical to #47.

WHY THIS IS A SLOW BOOK WHERE #32/#47 ARE FAST, AND WHY THAT IS THE POINT. The shock score's
own rank persistence is -0.009 to -0.028 -- a signal with no persistence, which is why #32
is charged 16.6x of validation churn and pays a 0.180 cost bill for a +0.211 gross. The
quantity under test here is the opposite: a LEVEL that persists (phi +0.705) producing a score
that persists (phi +0.627). Tonight's free F1 measurement puts this lab's cost bill at
+0.0111 of Sharpe per 1x of annual churn (R2 0.974 over all 47 recorded v3 books), so a book
in the 3-8x range pays 0.03-0.09 rather than 0.18. **Net skill is gross minus that bill, and
no slow object on this board has gross skill above +0.124.**

FREE PRE-TRIAL SCREEN, computed before this file was written. No train Sharpe, skill or IC
was computed for this object.

    quantity                                        value      reference
    coverage of eligible names                      99.9%      #47 keeps 50.1%, #32 44.8%
    month-ends scorable                             264/264    #32 scores 215 of 252
    rank phi of the SCORE, month to month           +0.627     the shock score: -0.009
    rank phi of the SCORED QUANTITY's LEVEL         +0.705     the 2026-11-26 screen; PASSES
    rank rho to the 5/45 volume shock score         -0.042
    rank rho to 12-1 momentum                       +0.060
    rank rho to the board lead's reversal score     +0.002
    rank rho to trailing 126-day volatility         -0.048     <- NOT low-vol in costume
    rank rho to seasoning (price-history depth)     +0.264     <- the one rider, see below
    top-100 Jaccard to #47's book                   0.411
    ETF share of the quota'd book                   6.9%       panel 5.5%
    US share of the quota'd book                    77.2%      eligible pool 76.7%

The four rhos at or below 0.06 in absolute value are the unusual line: this is the first score
in the v3 record that is near-orthogonal to EVERY reference object the lab holds, and the
-0.048 against 126-day volatility is what distinguishes it from the dead risk axis (six
measurements of "Sharpe is flat in beta on this panel"). The 0.90 relabelling bar is not
approached on either instrument.

PRE-REGISTERED PREDICTIONS, written before the run.
 - GROSS skill (net skill plus the skill-minus-2x-cost bill): **-0.05 to +0.05** if the
   baseline-purity mechanism is right. **Above +0.08** re-attributes the 2026-11-25 in-window
   term from an interaction to a main effect.
 - NULL PERCENTILE: **40-80%**, by the coarse 2026-11-25 calibration at its stated 0.02-0.05
   resolution limit; above 90% only if gross exceeds +0.08.
 - CHURN: this node changes WHAT the book holds rather than how often it trades, so per the
   2026-11-26 rule the exit200 predictor is the wrong instrument and the range is widened:
   train **2.5x to 9.0x**, validation **4.0x to 18.0x**. exit200 is 22.1%, which gives 2.65x
   of name churn mechanically; the 2026-11-22 predictor gives 7.4x and is calibrated on
   near-zero-persistence books. **No bill is forecast from the churn** (2026-11-26 rule).
 - TRAIN SKILL is not predicted and was not screened; 44 of 47 recorded v3 trials fail that
   gate and this will probably join them. **The statistic under test is the GROSS skill and
   the null percentile. The verdict is not the result.**
 - REFUSAL, pre-committed before the run: a gross reading inside [-0.05, +0.05] refuses the
   main-effect reading, and no further quietness construction is written tonight -- no K, no
   band, no window, no threshold variant.

WHAT ARGUES AGAINST THE BOOK.
 (i) The +0.264 rank rho to seasoning. Quiet names are somewhat longer-listed, and
     price-history depth is this panel's largest single confound (2026-10-26/27) -- though
     2026-11-20 measured it as a necessary condition carrying no signal of its own. It is
     reported rather than controlled, because a seasoning control would be a second node and
     would destroy the one-operator reading this file exists to deliver.
 (ii) Share volume carries the split half of the as-of-fetch adjustment factor D_i(t), so a
     split inside the window steps log volume by log(2) = 0.693 and makes that name look
     jumpy. This book therefore systematically avoids names with a recent corporate action,
     which is a real selection and is causal, but is not the economics the title claims.
 (iii) A quiet-volume premium has no source behind it. The 2026-11-25 session's own
     explanation of the +0.145 is the interaction, and this file's positive branch is the
     alternative to the record's stated mechanism, not a literature prior.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
WINDOW = 50         # the same 5 + 45 scoring window #32/#47's cut reads

STRATEGY = {
    "name": "lv_volume_quiet_alone",
    "family": "liquidity-volume",
    "hypothesis": (
        "Trading the purity filter's own quantity as the score -- the 100 eligible names with "
        "the SMALLEST maximum one-day |d log share volume| anywhere in the 50-day window, "
        "quota-allocated across (trailing-trading-calendar peer group x instrument type), "
        "equal-weighted, monthly, with a top-200 retention band, every other node "
        "byte-identical to lv_volume_shock_median_guard and the shock sort removed -- earns "
        "GROSS validation skill above +0.08, because the 2026-11-25 session's +0.145 "
        "in-window term would then be a main-effect quiet-volume characteristic premium "
        "rather than the baseline-cleaning INTERACTION that session attributed it to; a gross "
        "reading inside [-0.05, +0.05] instead confirms baseline purity as the mechanism, "
        "since with the shock sort removed there is no baseline left to clean, and closes the "
        "quietness characteristic as a tradeable object."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The 100 quietest eligible names by in-window maximum |d log volume|, quota'd across
    (calendar peer group x instrument type), monthly with a top-200 retention band.
    `lv_volume_shock_median_guard` with the shock sort replaced by the cut's own quantity.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    # The identical causal statistic #32 thresholds at log(3) and #47 cuts at its
    # cross-sectional median: the largest one-day move in log volume anywhere in the
    # scoring window. Negated, so that a HIGH score is a QUIET name.
    quiet = -lv.diff().abs().rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken (the
        # 2026-10-07 column-axis leak).
        score = quiet.loc[date].reindex(names).dropna()
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
