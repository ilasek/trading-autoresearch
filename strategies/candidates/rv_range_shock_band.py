"""THE ATTENTION EVENT MEASURED ON THE RANGE PANEL -- a one-operator pair against
`lv_volume_shock_gkm_band` (#32), the only object in 35 recorded v3 trials to clear the
region- and type-matched random-selection null.

THE CLAIM IN ONE LINE. A name whose recent daily trading RANGE is unusually wide relative
to its own recent norm has had a visibility or attention shock, and Merton's
investor-recognition channel -- the same channel Gervais-Kaniel-Mingelgrin invoke for the
high-volume return premium, and Barber-Odean's attention argument alongside it -- says such
names earn higher returns over the following weeks as the shareholder base broadens. The
sign is fixed from that mechanism and from nothing else. Both sources are pre-2018, so no
post-2018 novelty discount applies.

WHY THIS IS THE ONE PAIR WORTH BUYING TONIGHT, AND IT IS THE HANDOVER'S OWN IDEA (ii).
The v3 board carries exactly ONE fast object (`vol_shock_5_45`, month-to-month rank
persistence phi -0.022) and exactly one object that has ever cleared the null gate -- the
same one. `learnings.md` (2026-11-22) records that a score whose ordering is near-random is
decorrelated from this board almost by construction because everything else on it is slow,
and the 2026-11-24 handover put "a second FAST mechanism" first among the night's ideas for
that reason. This file changes ONE node of #32 -- the score -- and holds K = 100,
BAND = 200, the (trailing-trading-calendar peer group x instrument type) quota, the monthly
schedule, the warm-up rule and the equal weighting byte-identical in intent.

WHY THE SCORE NEEDS NO SPLIT GUARD, AND WHY THAT IS THE POINT RATHER THAN A CONVENIENCE.
`log(high / low)` is a ratio of two quotes from the SAME day on the same adjusted series,
so the as-of-fetch back-adjustment factor `D_i(t)` -- the product of every distribution
factor after `t`, which `learnings.md` records as dominating the stored LEVEL and as the
source of this lab's six contaminated dollar-volume scores -- cancels exactly, splits
included, and so does the day's FX rate. `learnings.md` (2026-11-05/06) calls the within-day
ratio the first score class structurally immune to the contaminant. #32 had to buy its
cleanliness with a causal guard that drops any name whose daily |log volume change| exceeds
log(3) anywhere in a 50-day window; this score needs no guard at all.

AND THE GUARD IS NOT CHEAP -- MEASURED TONIGHT, FREE, ON TRAIN, AND IT IS A FACT ABOUT THE
BOARD'S ONE LIVE OBJECT RATHER THAN ABOUT THIS FILE. The share of eligible names carrying a
scorable 5/45 volume shock, by era:

    era          volume prints   raw 5/45 shock   AFTER the split guard
    1997-2002        97.2%            99.7%             34.1%
    2003-2008        98.6%            99.9%             47.1%
    2009-2017        96.1%            99.7%             50.1%

The guard removes **55.3%** of the eligible panel, not the 0.57% #32's docstring reports --
that figure is the share of DAYS exceeding the threshold, and the guard is a rolling 50-day
MAXIMUM, so the per-day rate compounds over the window. #32 therefore selected its 100 names
from about half the panel, and the half it kept was selected on VOLUME STABILITY, a
cross-sectional screen nobody measured; `random_null_v3` draws its replicas from the full
region- and type-matched eligible pool, so part of #32's recorded selection term is the
guard's own selection and not the volume shock's. This score is scorable on **99.7% of
eligible names in every era** (0.3% of prints have high == low and are dropped), so it is
the same event mechanism read on the whole panel.

WHAT IT IS NOT A RELABELLING OF -- measured before this file was written, 252 train
month-ends, mean within-date Spearman rank correlation:

    vs the 5/45 volume shock (#32's score)   +0.395
    vs trailing 126-day volatility            -0.019
    vs 12-1 momentum                          +0.025
    vs the board lead's long-horizon reversal  +0.010

The second number is the load-bearing one and it is the opposite of what a reader would
guess: a range SHOCK is not a volatility-LEVEL sort, so this object does not enter the
six-measurement series behind "Sharpe is flat in beta on this panel", and it is not
`rv_volofvol_neutral_band` in costume either (that score is a 252-day standard deviation at
phi +0.920; this one is at phi -0.009). The first number is well below the 0.90 the
relabelling test refuses at, and research `#519`, filed last night, says it cannot be read as
a membership statement anyway: the two scores' top-100 sets overlap at Jaccard **0.202**
(prefix-weighted intersection metric delta^(w) **0.763**) despite that +0.395. This is the
first measured instance in this lab of the paper's separation between a full-cross-section
rank correlation and a top-K agreement measure.

PRE-REGISTERED, IN WRITING, BEFORE THE RUN -- and the cost side is registered as a problem
rather than hidden. Train exit-from-top-200 is **44.9%**, so the 2026-11-22 predictor
(`train one-way churn ~ 1.0 + 0.29 x exit200%`) puts train churn at **14.0x**; registered
**10-18x train and 20-36x validation** (the >2x validation multiplier is a property of
books holding a near-zero-persistence leg, 2026-11-24). At the 10-19 bps per 1x of churn the
record now brackets, that is a bill of **0.15-0.35 of Sharpe**. The largest GROSS skill ever
recorded here is ~+0.21. **So net skill is expected NEGATIVE, and the statistic that tests
the claim is the null PERCENTILE together with the gross skill (skill plus the bill implied
by skill minus skill-at-2x-costs), exactly as #37's docstring pre-registered the null
percentile as the statistic for an all-fund book.** Saying this before the run is the whole
discipline: a positive net reading would be a surprise, and a negative one is not a refutation
of the mechanism.

THERE IS NO CHEAPER CONSTRUCTION FOR THIS OBJECT AND THAT IS ARITHMETIC. The band is inert
at this persistence (2026-11-22: a retention band controls churn only against a score whose
ORDERING is persistent, above ~0.97; phi here is -0.009, so B = 200 is carried to match #32
and not because it is expected to save anything). Holding longer dilutes a 1-4 week premium
proportionally, so the net/gross ratio does not improve (2026-11-22 (iii)); overlapping
sleeves are the same arithmetic in a different shape. A deeper K would trade less and dilute
the tail by the same factor. Per the 2026-11-24 rule, any proposal to cheapen this book must
first write down the gross skill the cheapening removes alongside the bill it saves -- which
is why none is offered here.

WHAT ARGUES AGAINST THE BOOK.
 (i) The bill above, which is most of the plausible prize. This is the same corner #32
     found: on this panel the CLEAN corner of the event-shock space and the CHEAP corner of
     the cost model do not overlap.
 (ii) GKM's premium is strongest in smaller names and this panel is nine countries' large
     caps, so research `#506`'s reading rule applies to the attention channel too: the
     unconditional claim overstates what a long-only book here can collect. `learnings.md`
     prices this lab's long leg at roughly a third of any object's spread.
 (iii) A wide range is mechanically a large |return| day, so part of this score is the
     short-horizon reversal's own conditioning variable unsigned. The reversal is refuted
     here as a traded book; an unsigned magnitude is a different object, but the overlap is
     real and is the reason the pre-signed direction rests on recognition rather than on
     any price-continuation argument.
 (iv) High/low are forward-filled on a 10-day cap like the close, so a non-printing day
     would repeat the previous day's range. The score is taken only on days with a volume
     print, which is the panel's own print indicator (volume is never forward-filled).

NO TRAIN SIGNAL NUMBER IS OFFERED AS EVIDENCE FOR THIS BOOK. Every screen above is used
only for the arithmetic refusals it can support -- a relabelling correlation, a coverage
count, a churn prediction -- because corr(train skill, validation skill) is -0.08 over 27
recorded trials and the 2026-10-16/17 rule, as corrected on 2026-11-22, permits a train
screen to refute but never to qualify and equally forbids declining an object because a
train statistic fell short of a bar.
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

STRATEGY = {
    "name": "rv_range_shock_band",
    "family": "range-variance",
    "hypothesis": (
        "Holding the 100 eligible names with the HIGHEST range shock -- mean log(high/low) "
        "over the last 5 printing days minus the median over the preceding 45, taken only on "
        "days with a volume print, quota-allocated across (trailing-trading-calendar peer "
        "group x instrument type) cells, monthly with a 200-name retention band -- earns a "
        "validation Sharpe above the 90% quantile of its region- and type-matched random "
        "selection null and positive GROSS skill over the equal-weight eligible pool, because "
        "an unusually wide trading range is a visibility shock that broadens a name's "
        "shareholder base over the following weeks (Merton recognition, the channel "
        "Gervais-Kaniel-Mingelgrin invoke for the high-volume premium), and because a "
        "within-day high/low ratio is the one score class on this panel from which the "
        "as-of-fetch back-adjustment factor cancels exactly -- so unlike the volume shock it "
        "needs no split guard, and is scorable on 99.7% of eligible names instead of 44.7%."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """High short-window range shock, quota'd across (calendar peer group x instrument
    type), monthly with a retention band. #32 with one node changed: the score.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    # Only days with a volume print carry a real bar: high/low are forward-filled on the
    # same 10-day cap as the close, so a holiday would otherwise repeat yesterday's range.
    printed = volume.notna() & (volume > 0)
    lrange = np.log(aux["high"].where(printed) / aux["low"].where(printed))
    lrange = lrange.where(lrange > 0)          # high == low is a non-range, not a zero range

    fast = lrange.rolling(FAST, min_periods=3).mean()
    slow = lrange.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        score = shock.loc[date].reindex(names).dropna()
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
