"""The ten-year reversal with its null half removed and its one large confound
neutralised.

THE CLAIM IN ONE LINE. The score trial #5 and trial #11 traded -- the mean monthly
return over the trailing ten years -- is the average of two halves that do not
contribute equally: measured on train tonight, the OLD half (months -120 to -61)
carries a selection term of +0.135 and the RECENT half (months -60 to -1) is a pure
null at +0.012. The traded score therefore averaged a signal with noise. This
candidate holds the old half alone, and neutralises price-history depth as well as
region because tonight's screen found depth to be the largest single confound on this
panel.

TONIGHT'S FREE SCREENS (train 1997-2017 only, the engine's own backtest through
`protocol.evaluate_split(..., "train")` -- the instrument validated on 2026-10-25/26,
which reproduces trial #5's recorded train sharpe +0.5560 and train skill +0.0330 to
four decimals. No validation, holdout, forward or incubation number was read, and no
book outside this sheet was scored. Journal F2-F14 of 2026-10-26/27.)

*F2 -- the decade window's two halves are not equal contributors.* K=100, calendar-peer
quota, monthly, pool held through warm-up; SELECTION is gross skill over the gross pool:

    score                               net skill  selection    cost   turn   volratio
    decade mean (months -120..-1)  [#5]   +0.104     +0.120   -0.016   2.20    1.037
    OLD half   (months -120..-61)         +0.112     +0.135   -0.023   2.53    0.952
    RECENT half(months  -60..-1)          -0.010     +0.012   -0.022   2.83    1.111

Five further leak-free decade-path objects were priced the same way (decade return per
unit decade risk +0.073, fraction of positive months +0.054, decade skewness +0.031,
distance below the decade peak -0.044, low market correlation +0.008).

*F9/F10 -- why this book neutralises DEPTH and not only region.* A naive lag profile
said a deeper window selects better and churns less, monotonically. Holding the
candidate name universe fixed to the names a 15-year score can be computed for destroys
it: the profile goes flat and the deepest lag becomes the worst. The cause, priced with
no return score at all: **selecting the 100 eligible names with the deepest monthly
price history, peer-quota'd, earns +0.047 of selection at 0.99x turnover** (+0.075 at a
15-year threshold). It is not avoided delistings -- zero eligible series terminate within
1 or 3 years anywhere on train, in any depth group -- and it is confined to 2009-2017,
the half of train on which the panel's coverage depth is heterogeneous.

*F10a/F12 -- the confound is in SORTING on depth, not in requiring it, and this score
survives.* Requiring >= 60 months and equal-weighting everything that qualifies is worth
+0.002; requiring >= 120 months, -0.005. Re-quota'd across (calendar peer group x depth
tercile) cells so neither axis can supply the excess:

    book                               net skill  selection    cost   turn   97-08    09-17
    decade mean, region+depth neutral    +0.098     +0.116   -0.018   2.29  +0.092  +0.031
    OLD half,    region+depth neutral    +0.103     +0.127   -0.024   2.63  +0.134  +0.027
    decade skew, region+depth neutral    +0.010     +0.019   -0.009   1.65  -0.008  +0.025

The old half loses 0.008 of selection to depth neutralisation and keeps the rest, so the
+0.135 is not the depth premium wearing a reversal's clothes. Both train sub-periods are
positive and the volatility ratio is 0.948, so this is not the de-risking construction
trial #1 closed.

*F13 -- the selection-bias null for "best of eight objects priced tonight".* Six AR(1)
random scores at this score's own measured rank persistence (phi = 0.983), masked to its
own scorable set and pushed through the identical construction: net skill mean -0.0477
(sd 0.0253, max -0.0120), selection mean -0.0217 (sd 0.0260, max +0.0160). This book is
**z +5.9 on net and z +5.7 on selection** against that null, and churns 2.63x against the
random scores' 2.86-3.04x.

*F14 -- the gate's own region-matched null, measured on train (40 replicas).* Candidate
0.627 against a null median 0.514, sd 0.024, p90 0.542 -- a margin of +0.085 over where
the gate sits. **This is consistency, not a prediction**: trial #6 carried a train margin
of +0.100 and still failed on validation, and `learnings.md` records four instances of
the operator with the largest train gain decaying fastest.

WHAT ARGUES AGAINST THE BOOK. (i) Rank rho to the already-traded decade mean is +0.777,
so this is mechanism M4 again, not a new one -- the honest description is the same bet
with a null component removed, and M4's two validation readings are -0.006 and -0.055.
(ii) The parent score's within-region IC alternates sign across five-year buckets of the
decision date (2026-10-25/26 F12), so its decade-to-decade stability is poor and much of
the train result sits in the 2000-2004 value rebound. (iii) The 09-17 sub-period term
(+0.027) is five times smaller than the 97-08 one (+0.134), and 2009-2017 is the half of
train closest to validation.

No retention band: the 2026-10-25/26 paired validation measurement closed the band as a
validation operator on this very mechanism (+0.080 of train skill for -0.049 of
validation skill), and nothing here reopens it.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train comes in at
2.63x annualised and trial #5's validation churn ran 34% above its train figure
(2.02x -> 2.71x), so **2.5-4.0x** is the predicted band.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
LAG = 60          # months skipped before the window starts
SPAN = 60         # length of the window, in months
MIN_MONTHS = 48   # of SPAN
DEPTH_BINS = 3

STRATEGY = {
    "name": "pt_decade_old_half_depth_neutral",
    "family": "price-trend",
    "hypothesis": (
        "Selecting the 100 eligible names with the lowest mean monthly return over the "
        "window from ten to five years before the decision date -- the OLD half of the "
        "ten-year reversal the lab already traded -- with entries quota-allocated across "
        "(trailing-trading-calendar peer group x price-history-depth tercile) cells, earns "
        "positive validation skill over the equal-weight eligible pool, because the recent "
        "half of that ten-year window is a pure null on train (selection +0.012 against the "
        "old half's +0.135) so the traded score averaged a signal with noise, and because "
        "neutralising history depth removes the only confound measured large enough to "
        "account for it (sorting on depth alone earns +0.047 with no return score at all)."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K lowest mean monthly returns of the window
    [-LAG-SPAN, -LAG-1], quota-allocated across peer-group x depth-tercile cells."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    # Monthly returns. A value published on a month label uses only returns realized at
    # or before that label; the daily reindex forward-fills, so a decision date reads the
    # latest label at or before it.
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)

    # The old half of the decade window: shifted clear of the most recent LAG months.
    old = mret.shift(LAG).rolling(SPAN, min_periods=MIN_MONTHS).mean()
    score = (-old).reindex(prices.index, method="ffill")

    # History depth, as a candidate can count it: months of realized monthly return in
    # the visible window. A function of the window's start, not its end.
    depth = mret.notna().cumsum().reindex(prices.index, method="ffill")

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 50:
            continue
        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < 50:
            # Warm-up: hold the pool rather than cash, so the book is not scored against
            # a fully-invested benchmark while sitting out (operator of 2026-10-15/16).
            rows[date] = pd.Series(1.0 / len(names), index=names)
            continue
        groups = calendar_peers(volume, date, sc.index).dropna()
        if len(groups) < 50:
            continue
        sc = sc.reindex(groups.index)
        dep = depth.loc[date].reindex(groups.index)
        try:
            bins = pd.qcut(dep.rank(method="first"), DEPTH_BINS, labels=False)
        except ValueError:
            bins = pd.Series(0, index=dep.index)
        cells = groups.astype(str) + "|" + bins.astype(str)
        picked = peer_quota_select(sc, cells, K)
        if len(picked) < 20:
            continue
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
