"""THE MATCHED CONTROL FOR TONIGHT'S MAIN-EFFECT RESULT: THE SAME QUIETNESS, THE WRONG WINDOW.

WHAT THE FIRST ARM FOUND AND THE QUESTION IT LEAVES. `lv_volume_quiet_alone` (this session)
completed the 2026-11-25 2x2 by trading the purity filter's own quantity as the score with the
5/45 volume-shock sort entirely removed. It was pre-registered at gross validation skill
[-0.05, +0.05] if the in-window cut is an INTERACTION that cleans the shock score's baseline,
and above +0.08 if it is a MAIN EFFECT. It measured **gross +0.118 at the 98th percentile** of
200 region- and type-matched replicas -- the main-effect branch -- so the quantity #32's file
documents as hygiene carries a tradeable-sized selection term all by itself.

That leaves one reading ambiguous, and it is the reading the whole series turns on. Two very
different objects are consistent with +0.118:

  (A) QUIET NAMES ARE BETTER NAMES. Quietness is a slow property of the firm -- a stable
      shareholder base, no recent corporate action, no episodic attention -- and any reasonably
      recent reading of it selects the same kind of name. Then WHICH 50 days the statistic is
      read over barely matters.
  (B) QUIETNESS IN THE WINDOW THAT MATTERS. The term is about the name's state over the days
      immediately before the rebalance, not about the name. Then displacing the window kills it.

The 2026-11-25 session's own displaced arm bears on this and does not settle it: displacing
#32's cut to days -100..-51 took gross from +0.211 to +0.101, an in-window term of +0.145
against a displaced term of +0.035. But that measured the displaced cut as a FILTER on a shock
sort, where the baseline-cleaning channel is unavailable by construction. Nothing has measured
the displaced quantity as a SCORE.

ONE NODE CHANGES FROM `lv_volume_quiet_alone`: `.shift(50)` before the rolling maximum, the
identical displacement `lv_volume_shock_displaced_guard` (#41) used. K = 100, BAND = 200, the
monthly grid, the (calendar peer x instrument type) quota, the equal weighting and the warm-up
branch are byte-identical.

FREE PRE-TRIAL SCREEN, computed before this file was written, and it is why this is a trial
rather than a relabelling. No train Sharpe, skill or IC was computed.

    quantity                                    THIS FILE   in-window arm
    coverage of eligible names                     99.7%        99.9%
    rank rho, displaced score vs in-window         +0.274         --
    top-100 Jaccard vs the in-window book           0.274         --
    score rank phi, month to month                 +0.627       +0.627
    rank phi of the SCORED QUANTITY's LEVEL        +0.709       +0.705
    exit200                                        21.8%        22.1%
    ETF share of the quota'd book                   6.8%         6.9%
    US share of the quota'd book                   77.3%        77.2%

**This is the best-matched pair this lab has built.** Persistence (both the score's and the
scored level's), the exclusion-free coverage, the holdings schedule as forecast by exit200, the
instrument-type mix and the region mix agree to within a few tenths of a point, while the two
books share only 27% of their holdings. The only difference is which 50 days the statistic
reads. Note why the rho is +0.274 and not the +0.627 the monthly phi reports: the monthly phi
is measured between windows that OVERLAP by 29 days, and a 50-day displacement makes them
disjoint, so +0.274 is this quantity's genuine non-overlapping persistence. The 0.90
relabelling bar is not approached on either instrument.

PRE-REGISTERED PREDICTIONS, written before the run, and the two branches are disjoint.
 - GROSS skill **+0.05 to +0.12** is reading (A): the characteristic belongs to the NAME and a
   50-day-stale reading of it still selects the same kind of name, so most of the in-window
   arm's +0.118 survives.
 - GROSS skill **-0.03 to +0.04** is reading (B): window position is what carries the term, the
   displaced score is near-inert, and the result reconciles with the 2026-11-25 displaced
   FILTER arm's +0.035 displaced term on a different construction.
 - A reading between +0.04 and +0.05 does not discriminate and will be reported as such rather
   than argued into one branch.
 - NULL PERCENTILE: tracks the selection term by the 2026-11-26 identity, so **90-99%** under
   branch (A) and **50-85%** under branch (B).
 - CHURN: matched to the in-window arm on exit200 to within 0.3 points, and that arm was charged
   5.1x train / 10.2x validation, so train **3.5x to 8.0x**, validation **7.0x to 15.0x**. The
   node changes WHAT the book holds, so no bill is forecast from the churn (2026-11-26 rule).
 - TRAIN SKILL is not predicted and was not screened. The in-window arm failed that gate at
   -0.116 and this will probably join it; **the statistic under test is the GROSS skill and the
   null percentile, and the verdict is not the result.**
 - REFUSAL, pre-committed: whatever this reads, **no third window position is tried and no
   quietness knob is tuned** -- not K, not the band, not the window length. The pair settles the
   attribution and the thread closes tonight either way.

WHAT ARGUES AGAINST THE BOOK. Everything that argues against the in-window arm argues against
this one: 88% of that arm's gross was its own cost bill, its net skill was +0.014 with a 90% CI
of [-0.108, +0.141], the score carries a +0.264 rank rho to price-history depth, and share
volume keeps the split half of the as-of-fetch factor D_i(t) so a 2:1 split inside the window
registers as a log(2) jump and this book systematically avoids recent corporate actions. The
one thing this file adds is that a displacement cannot introduce a NEW confound: the two arms
are the same statistic on the same panel, matched on every screen above.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
WINDOW = 50         # the same 5 + 45 scoring window #32/#47's cut reads
DISPLACE = WINDOW   # read days -100..-51 instead, as #41 does

STRATEGY = {
    "name": "lv_volume_quiet_displaced",
    "family": "liquidity-volume",
    "hypothesis": (
        "Reading the quietness statistic over days -100..-51 instead of the 50 days before the "
        "rebalance -- one node changed from lv_volume_quiet_alone, a pair matched to within a "
        "few tenths of a point on score persistence (+0.627 both), scored-level persistence "
        "(+0.709 vs +0.705), coverage, exit200, ETF share and US share while sharing only 27% "
        "of its holdings -- reproduces that arm's GROSS validation skill of +0.118 to within "
        "+0.05 to +0.12, because a quiet-volume premium that is a property of the NAME survives "
        "a 50-day-stale reading of the same quantity; a reading of -0.03 to +0.04 instead says "
        "the term belongs to the window immediately before the rebalance rather than to the "
        "name, and reconciles tonight's main effect with the 2026-11-25 displaced FILTER arm's "
        "+0.035."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The 100 quietest eligible names by maximum |d log volume| over days -100..-51, quota'd
    across (calendar peer group x instrument type), monthly with a top-200 retention band.
    `lv_volume_quiet_alone` with the scoring window displaced by one window length.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    # The identical statistic, read one window length earlier. Negated, so that a HIGH score
    # is a name that was QUIET over days -100..-51.
    quiet = -lv.diff().abs().shift(DISPLACE).rolling(WINDOW, min_periods=25).max()

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
