"""THE SECOND HALF OF THE CROSS-PANEL TEST -- the range panel's rate-matched DISPLACED
control, which turns "the purity rule generalises" into a claim about its DECOMPOSITION.

WHERE THIS SITS. Four arms are now recorded tonight, two per panel, one operator apart
within each panel. Bill = net skill minus skill at 2x liquidity costs; gross = net + bill:

    panel   arm                                   val sharpe  net skill   @2x     bill   GROSS   null  churn tr/val
    volume  guard IN the 50-day window (#32)        +0.368     +0.031   -0.149  0.180  +0.211   99%   9.0/16.6
    volume  guard DISPLACED to days -100..-51       +0.250     -0.085   -0.271  0.186  +0.101   97%   9.2/16.9
    volume  no guard                                +0.200     -0.138   -0.342  0.204  +0.066   95%  11.2/19.0
    range   no filter                               +0.183     -0.154   -0.318  0.164  +0.010   79%  11.0/18.2
    range   purity filter IN the window (median)    +0.250     -0.084   -0.287  0.203  +0.119   95%   9.1/16.4

The volume panel gives the full decomposition: of the guard's +0.145 of gross skill, a
rate-matched guard displaced OUTSIDE the scoring window recovers +0.035 and the IN-window
position carries +0.110. The range panel so far gives only the total: +0.109, which is the
volume panel's in-window term to within 0.001 and was pre-registered at +0.08 to +0.15. **What
is missing is the range panel's displaced control, and without it the range result is
consistent with two different stories** -- baseline purity (the mechanism), or any
rate-matched exclusion on a within-window jump statistic (a characteristic).

THIS FILE IS THAT CONTROL, AND IT IS ONE OPERATOR FROM `rv_range_shock_pure`. Same 5/45
log-range shock, same parameter-free median-jump threshold, same K = 100, same BAND = 200,
same (peer x type) quota, same monthly schedule -- the jump statistic is simply read over days
-100..-51, the 50 days immediately before the window the score reads. Measured on train
before this file was written, the displacement is rate-, persistence- and churn-matched to
the purity arm almost exactly, which is what makes the comparison a one-operator one:

    arm                        coverage of eligible   phi      exit200   pred churn   Jaccard vs raw
    purity filter (in-window)         50.0%         -0.007     22.0%       7.4x           0.248
    this file (displaced)             49.8%         -0.012     22.0%       7.4x           0.296

and the two keep substantially different names (Jaccard between them **0.434**), so this is
the strong form of the characteristic reading -- *any* rate-matched jump-stability screen is
worth the same -- and not a "same names, different window" restatement. Its filtered score's
rank correlation to trailing 126-day volatility is **+0.014**, against -0.044 for the purity
arm and -0.019 unfiltered, so neither arm is a volatility sort.

PRE-REGISTERED PREDICTIONS, WRITTEN BEFORE THE RUN.
 - If the range panel reproduces the volume panel's decomposition, this arm's GROSS skill
   lands near **+0.04** -- the unfiltered arm's +0.010 plus about a quarter of the +0.109 --
   and the purity rule is confirmed as a property of the scoring window on both panels.
 - If it lands near the purity arm's **+0.119**, then on the range panel the whole term is a
   jump-stability characteristic and the volume panel's 3:1 split does NOT generalise, which
   would mean tonight's headline is two different effects wearing one name.
 - NET skill expected negative in either case; the statistic that tests the claim is GROSS
   skill and the null percentile.
 - CHURN: **train 6-11x, validation 10-22x** (predictor 7.4x; the purity arm predicted 7.4x
   and was charged 9.1x/16.4x).
 - REFUSAL / NO-KNOB CLAUSE: whichever way this lands, the exclusion rate is already matched
   and the median removes the only free parameter, so no third threshold is tried on either
   panel. If the two panels disagree, the finding is reported as panel-dependent and the
   operator is NOT carried into a further candidate tonight.

WHAT ARGUES AGAINST THE BOOK.
 (i) It is a construction node, not a new bet; it is bought for the rider it places on the
     night's own finding, and it will cluster with the range-shock mechanism.
 (ii) Displacing the jump window costs 50 more printing days of history, so the book starts
     later in the warm-up. Price-history depth carries no signal here (2026-11-20), so this
     is a coverage restriction and not a tilt.
 (iii) On the volume panel the bill was flat across all three arms (0.180/0.186/0.204) while
     on the range panel it ROSE with the filter (0.164 -> 0.203) even though churn FELL
     (11.0x -> 9.1x train): 9.0 bps per 1x of churn unfiltered against 12.4 filtered. So the
     range purity filter moves the book into a more expensive liquidity tier, which is the
     2026-11-24 "the cost-per-turn constant is set by what a book holds" rule firing again,
     and it means this arm's bill is not predictable from its churn alone.
 (iv) The underlying score is a measured null unfiltered (gross ~+0.010 at the 79th
     percentile), so both range arms are filters applied to a null; that is deliberate -- it
     is the only way to attribute the whole of an effect to the operator.

NO TRAIN SIGNAL STATISTIC was computed for this file. Every number above is a coverage count,
a rank persistence, a holdings Jaccard, a rank correlation used as a relabelling test, a churn
prediction, or a validation figure already recorded in `trials.jsonl` tonight.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5
SLOW = 45
WINDOW = FAST + SLOW
DISPLACE = WINDOW        # the jump statistic reads days -100..-51

STRATEGY = {
    "name": "rv_range_shock_displaced",
    "family": "range-variance",
    "hypothesis": (
        "Displacing the 5/45 log-range shock's median-jump exclusion from the 50-day scoring "
        "window to the 50 days immediately before it -- a rate-matched (49.8% vs 50.0% of "
        "scorable names kept), persistence-matched (phi -0.012 vs -0.007) and churn-matched "
        "(predicted 7.4x in both) control that keeps substantially different names (Jaccard "
        "0.434) -- recovers only about a quarter of the +0.109 of GROSS validation skill the "
        "in-window filter was measured to add tonight, i.e. GROSS skill near +0.04, "
        "reproducing on the range panel the 3-to-1 purity-versus-characteristic split the "
        "volume panel gave (+0.110 in-window against +0.035 displaced); a reading near "
        "+0.119 instead would say the range panel's whole term is a jump-stability "
        "characteristic and that the two panels' effects are not the same mechanism."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """5/45 log-range shock with the median-jump exclusion read over days -100..-51.
    `rv_range_shock_pure` with one node changed.
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
    jump = lrange.diff().abs().shift(DISPLACE).rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

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
