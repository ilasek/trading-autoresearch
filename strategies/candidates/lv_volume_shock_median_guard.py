"""THE ONE POSITIVE RESULT ON THIS BOARD, RE-RUN WITH ITS ONE FREE PARAMETER REMOVED.

WHY THIS IS THE MOST VALUABLE SINGLE TRIAL AVAILABLE TONIGHT. `lv_volume_shock_gkm_band`
(trial #32) is the only object in 43 recorded v3 trials to clear the region- and type-matched
random-selection null (99th percentile, MC p = 0.010), and the 2026-11-25 session measured that
**two thirds of its gross skill lives in one node its own file documents as hygiene** -- a
"causal split guard" that drops any name whose daily |d log volume| exceeds log(3) anywhere in
the 50-day scoring window. Removing the guard took gross skill +0.211 -> +0.066 and displacing
it to days -100..-51 gave +0.101. Nothing on this board has ever been replicated. The single
most informative thing that can be asked of it is whether its headline survives the removal of
its only tuned number.

THE FREE MEASUREMENT THAT MOTIVATES THIS FILE, AND IT IS A CORRECTION TO THE RECORD. Measured
over 252 train month-ends on the eligible panel, before this file was written:

    **log(3) = 1.099 sits at the 44.8th percentile of the cross-sectional distribution of
    the in-window maximum |d log volume|.**

So the threshold the record has been calling a "split guard" is, empirically, a MEDIAN-LIKE
CUT of the cross-section -- not an outlier cut. That sharpens the 2026-11-25 correction (iv),
which established only that the guard cannot catch the split it was written for (a 2:1 split,
the modal split, steps log volume by log(2) = 0.693, BELOW log(3)). The two statements
together say the guard is a cross-sectional median selection wearing a corporate-action label.

THE RESTATEMENT. Replace the fixed log(3) with the cross-sectional MEDIAN of that same
quantity among the names scorable on the date -- the parameter-free operator
`rv_range_shock_pure` introduced, and the same one tonight's three return-channel arms used.
One node changes; K = 100, BAND = 200, the monthly grid, the (calendar peer x instrument type)
quota, the equal weighting and the warm-up branch are byte-identical to #32.

FREE PRE-TRIAL SCREEN, before this file was written. No train signal statistic was computed.

    quantity                         #32 (log 3)    THIS FILE (median)
    scorable names kept                 44.8%            50.1%
    month-ends the book trades on        215              252
    ETF share of holdings                4.2%             3.9%
    top-100 Jaccard, the two books               0.687

Jaccard 0.687 is the number that makes this a trial rather than a relabelling: the two rules
agree on the threshold's LOCATION (44.8% vs 50.1% of the cross-section) yet disagree about a
third of the book, because log(3) is a FIXED cut of a distribution whose width moves through
time while the median is a cut of its rank. The 0.90 relabelling bar is not approached. The
median rule also scores every month-end rather than 215 of 252: a fixed threshold in log units
leaves early, thin months with too few survivors to fill a quota.

PRE-REGISTERED PREDICTIONS, written before the run.
 - GROSS skill (net skill plus the skill-minus-2x-cost bill, the arithmetic every arm of this
   series uses): **+0.15 to +0.25**, i.e. within noise of #32's +0.211, if the OPERATOR rather
   than the threshold is what carries the term. A reading near the unguarded arm's +0.066 would
   say log(3) was doing something a median cut does not, and would make #32's headline a
   property of one number.
 - NULL PERCENTILE: **95-99%**, by the 2026-11-25 monotone calibration -- with tonight's new
   rider that the calibration cannot resolve gross differences below about 0.02-0.05 because
   each book's percentile is set against its own replicas' median.
 - NET skill: around **+0.00 to +0.06** (#32 scored +0.031). This is the one book on the board
   where a positive net skill is a live possibility rather than an arithmetic impossibility.
 - CHURN: train **7-12x**, validation **11-22x** (#32 was charged 9.0x / 16.6x and keeps a
   slightly smaller fraction of the panel than this file does).
 - TRAIN SKILL will remain negative, so this will be a GATE_FAIL whatever happens: #32 failed
   that gate at -0.124 and nothing here addresses it. **The statistic under test is the GROSS
   skill and the null percentile, and the verdict is not the result.**
 - REFUSAL, pre-committed: whatever this reads, no third threshold is tried on this channel.
   Either the operator replicates or #32's headline is reported as threshold-specific.

WHY THIS IS NOT THE RE-KNOB TONIGHT'S REFUSAL FORBIDS. Tonight's return-channel triple closed
the purity rule as channel-specific (it pays only where the scored quantity is persistent in
level; `|r|` is not, and the filter was inert there in both positions). That refusal forbids
seeking a fourth channel or a new threshold for the refused claim. This file is on the FIRST
channel, where the rule was measured to work, and it REMOVES a parameter rather than adding
one. It was named as arm A5 in tonight's pre-registration before any result was read.

WHAT ARGUES AGAINST THE BOOK.
 (i) Share volume carries the split half of the as-of-fetch factor `D_i(t)`, so the score's
     level is contaminated in principle; the 50-day ratio window is the record's reason for
     believing the contamination is small, and neither rule is a defence against it, since
     log(3) cannot catch a 2:1 split and the median catches only the jumpiest half.
 (ii) Replacing a fixed cut with a rank cut makes the exclusion rate constant through time by
     construction, which removes a source of variation #32 had; if #32's term came partly from
     excluding MORE names in volatile periods, this file gives it up.
 (iii) The 2026-11-22 rider from `research/#506` still stands: the source localises the
     high-volume premium toward smaller names and this panel is nine countries' large caps, so
     #32's +0.21 gross is an upper bound on what any book here could have collected.
 (iv) It is a fast book on a panel whose binding constraint is turnover, and the
     2026-11-22 arithmetic that there is no cheaper construction for this object -- holding
     longer dilutes a 1-4 week premium proportionally -- applies unchanged.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5            # days of recent volume
SLOW = 45           # days of baseline, ending FAST+1 days ago
WINDOW = FAST + SLOW

STRATEGY = {
    "name": "lv_volume_shock_median_guard",
    "family": "liquidity-volume",
    "hypothesis": (
        "Replacing the fixed log(3) threshold in the board's only null-gate-clearing object "
        "with the cross-sectional MEDIAN of the same in-window maximum |log volume change| -- "
        "a parameter-free restatement that keeps 50.1% of scorable names against log(3)'s "
        "44.8%, carries the same 4% ETF share, scores all 252 train month-ends against 215, "
        "and yet shares only 69% of its holdings because a fixed cut of a time-varying "
        "distribution is not a cut of its rank -- reproduces that object's GROSS validation "
        "skill of +0.211 to within noise (+0.15 to +0.25) and its null percentile of 95-99%, "
        "because the term belongs to the baseline-purity OPERATOR and not to the particular "
        "number; a reading near the unguarded arm's +0.066 instead makes the board's one "
        "positive result a property of one tuned threshold."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """High short-window volume shock, guarded at the cross-sectional median in-window jump,
    quota'd across (calendar peer group x instrument type), monthly with a retention band.
    `lv_volume_shock_gkm_band` with one node changed: the threshold becomes a rank cut.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    fast = lv.rolling(FAST, min_periods=3).mean()
    slow = lv.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow

    # The same causal statistic #32 thresholds at log(3): the largest one-day move in log
    # volume anywhere in the scoring window. Cut at the cross-section's median instead.
    step = lv.diff().abs().rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken — the median
        # is computed inside the set the engine will actually let this book buy.
        score = shock.loc[date].reindex(names).dropna()
        j = step.loc[date].reindex(score.index).dropna()
        if len(j) < 60:
            # Warm-up: hold the pool rather than cash (2026-10-15/16).
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue
        score = score.reindex(j.index)[j <= j.median()].dropna()
        if len(score) < 60:
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
