"""DOES BASELINE PURITY GENERALISE OFF THE VOLUME PANEL? -- the same operator tonight
measured to carry three quarters of the board's best gross skill, transplanted onto a score
that has just been measured a null without it.

THE THREE ARMS TONIGHT ESTABLISHED, ON THE VOLUME PANEL. Identical books, one node apart:

    arm                                val sharpe   net skill   @2x cost   bill   GROSS skill   null
    #32 guard INSIDE the 50-day window   +0.368       +0.031      -0.149   0.180    ~+0.211      99%
    guard DISPLACED to days -100..-51    +0.250       -0.085      -0.271   0.186    ~+0.101      97%
    NO guard                             +0.200       -0.138      -0.342   0.204    ~+0.066      95%

The bill is flat across the three (0.180 / 0.186 / 0.204) and the churn of the two guarded
arms is matched to 0.2x, so the whole difference is GROSS skill. Of the guard's ~+0.145, the
rate-matched displaced version recovers ~+0.035 and the IN-WINDOW position carries ~+0.110 --
about three quarters. **So the term is mostly baseline PURITY** (a 5/45 shock whose 45-day
baseline contains a jump is measuring a decaying baseline, not a fresh event) **and about a
quarter a cross-sectional stability characteristic.**

WHY THAT CLAIM NEEDS A SECOND PANEL, AND WHY THIS IS THE RIGHT ONE. Purity, if it is real, is
a property of SHOCK SCORES and not of volume: any statistic of the form "recent window minus
baseline window" is corrupted the same way when the baseline is not a baseline. Tonight's
`rv_range_shock_band` is exactly such a score -- mean log(high/low) over 5 printing days
minus the median over the preceding 45 -- and it was run with NO purity filter at all. It
scored validation skill **-0.154** at the 79th percentile of its null, bill ~0.164, so
**GROSS skill ~+0.010**: a null. If purity generalises, adding the filter should move that
gross figure toward the +0.11 the in-window position carried on the volume panel; if it does
not move, purity is a property of the volume series and not of shock scores, and tonight's
headline shrinks to one panel.

THE FILTER, AND IT HAS NO TUNED PARAMETER. The volume guard's log(3) threshold is in log-volume
units and is inert on the range panel -- daily log(high/low) lives in roughly [0.005, 0.15],
so |d log range| above log(3) = 1.099 occurs on **0.00%** of eligible printing day-names and a
literal transplant leaves the book byte-identical (top-100 Jaccard **1.000** against the
unfiltered arm, i.e. refused as a relabelling before it was written). The parameter-free
restatement is used instead: a name is dropped if its largest daily |d log range| inside the
50-day scoring window exceeds the **cross-sectional median** of that quantity among the names
scorable on that date. The median is the one choice that is not a knob, and it lands the
exclusion rate on the volume guard's by construction. Measured on train, before this file was
written, the two filters are structural twins:

    filter                               coverage of eligible   phi      exit200   pred churn   Jaccard vs own raw
    #32's volume guard (log 3, in-window)       44.7%         -0.022     25.6%       8.4x            0.274
    this file (median jump, in-window)          50.0%         -0.007     22.0%       7.4x            0.248

and the filtered score's rank correlation to trailing 126-day volatility is **-0.044**, so
this is not a volatility sort in costume -- the concern the record raises about every
range-class object. The guard also cuts the predicted churn nearly in half (14.0x -> 7.4x),
which is the first construction on this board to reduce a fast score's bill without diluting
its horizon, because it removes names rather than slowing the schedule.

PRE-REGISTERED PREDICTIONS, WRITTEN BEFORE THE RUN.
 - GROSS skill: if purity generalises, **+0.08 to +0.15**; if it is volume-specific, within
   noise of the unfiltered arm's ~+0.010.
 - A reading in between, or a gross rise smaller than the volume panel's +0.110, is the
   honest third answer and would say purity is real but panel-dependent in size.
 - NET skill is still expected negative or near zero: the bill falls with the churn (predicted
   ~0.09-0.13 of Sharpe at 10-19 bps per 1x of a ~10-16x validation figure), so a gross of
   +0.10 would land net near zero. The statistic that tests the claim is the GROSS skill and
   the null percentile, as for all three volume arms.
 - CHURN: **train 6-11x, validation 10-22x** (predictor 7.4x; the volume analogue predicted
   8.4x and was charged 9.0x/16.6x).
 - REFUSAL: if the filter raises gross skill by less than the displaced arm's +0.035 recovered
   on the volume panel, the purity rule is reported as volume-specific and is NOT re-knobbed
   onto a third threshold -- the exclusion rate is already matched and the only remaining
   parameter is the one the median removes.

WHAT ARGUES AGAINST THE BOOK.
 (i) The underlying score was measured a null tonight (gross ~+0.010, 79th percentile), so
     this arm is a filter applied to nothing. If the filter has to create the signal rather
     than clean it, the purity story is wrong. That is the point of running it on a measured
     null rather than on the one object that worked.
 (ii) Selecting on the median of a within-window jump statistic is one step from the
     "second moment of the series" class the record lists as an anti-candidate (`vchurn252`,
     refuted with the wrong sign). Tonight's displaced-guard arm is what separates the two
     readings, and it put only a quarter of the volume term on the characteristic; this arm
     is exposed to that quarter.
 (iii) A wide range is mechanically a large |return| day, so part of this score remains the
     short-horizon reversal's conditioning variable unsigned. The pre-signed direction rests
     on Merton recognition / Barber-Odean attention, not on any price-continuation argument.
 (iv) The same cost corner as every fast object here, though less of it: the filter is the
     one cheapening this lab has found that does not dilute the signal's horizon, so the
     2026-11-24 rule ("write down the gross the cheapening removes alongside the bill it
     saves") is satisfied with a predicted gross INCREASE rather than a decrease.

NO TRAIN SIGNAL STATISTIC was computed for this file. Every number above is a coverage count,
a jump rate, a rank persistence, a holdings Jaccard, a churn prediction, or a validation
figure already recorded in `trials.jsonl` tonight.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5            # printing days of recent range
SLOW = 45           # printing days of baseline, ending FAST+1 days ago
WINDOW = FAST + SLOW

STRATEGY = {
    "name": "rv_range_shock_pure",
    "family": "range-variance",
    "hypothesis": (
        "Adding a parameter-free baseline-purity filter to the 5/45 log-range shock -- drop "
        "any name whose largest daily |change in log(high/low)| inside the 50-day scoring "
        "window exceeds the cross-sectional median of that quantity on the date, which lands "
        "the exclusion rate on the 55% the volume shock's log(3) guard was measured to use -- "
        "raises that score's GROSS validation skill from the ~+0.010 it recorded unfiltered "
        "toward the ~+0.110 the in-window guard position was measured to carry on the volume "
        "panel tonight, because a shock score whose baseline window itself contains a jump is "
        "measuring a decaying baseline rather than a fresh event and that defect is a property "
        "of shock scores rather than of the volume series; a gross reading within noise of "
        "+0.010 instead confines tonight's purity finding to the volume panel."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """5/45 log-range shock with an in-window baseline-purity filter at the cross-sectional
    median jump. `rv_range_shock_band` with one node added.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    printed = volume.notna() & (volume > 0)
    lrange = np.log(aux["high"].where(printed) / aux["low"].where(printed))
    lrange = lrange.where(lrange > 0)

    fast = lrange.rolling(FAST, min_periods=3).mean()
    slow = lrange.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow
    jump = lrange.diff().abs().rolling(WINDOW, min_periods=25).max()

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
        j = jump.loc[date].reindex(score.index).dropna()
        if len(j) < 60:
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
