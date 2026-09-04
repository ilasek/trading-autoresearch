"""The third point of the bracket: is the seated band an interior optimum?

WHY THIS FILE EXISTS, AND WHY IT IS THE LAST ONE ON THIS AXIS. Tonight's two
trials both moved the seated `liquidity-volume` lead in the **concentrating**
direction and both lost:

    #80  hold-15/enter-10, equal weight      breadth 25.2 -> 12.4   HHI +103%   -0.043
    #81  hold-30/enter-20, rank weight       breadth 25.2 -> 25.2   HHI  +31%   -0.049

Two points on one side of the incumbent is an observation, not a closed axis.
`learnings.md` records the difference between the two explicitly — the horizon
kernel was "closed by a bracket rather than an assertion", while a one-sided
reading left the trim axis open for six trials. This file supplies the missing
side: hold-45/enter-30, the same band ratio, everything else bit-identical.
**Whatever it returns, no fourth point will be taken** — a fourth would be the
sweep the manual forbids, and three points already determine whether the
incumbent sits at an interior optimum or on a slope.

THE PREMISE, MEASURED FREE ON TRAIN (top-N book excess over its own scoreable
pool, forward 21-day return — the statistic the book is scored on):

    top-10  (13.0% of a 77-name pool)   +7.09 %/yr (t=+3.97)   -> #80, lost
    top-20  (26.1%)                     +4.31 %/yr (t=+4.29)   -> seated lead
    top-30  (39.1%)                     +3.39 %/yr (t=+4.83)   -> this candidate

So the mean moves against this candidate — it gives up 0.92%/yr of tail excess,
about -0.048 of Sharpe if it were delivered one-for-one at this book's
volatility. The question is entirely whether the variance saving covers it. That
is the same trade #80 took in reverse and lost, which is the reason to expect a
gain here and the reason it is not a foregone conclusion: diversification gains
are strongly concave, and 25 names is already past the steep part.

HOLDINGS-ONLY PROFILE, MEASURED BEFORE THIS FILE WAS WRITTEN:

    band                names    HHI      vol pct   log-ADV pct   annual L1 churn
    hold-45/enter-30    36.87   0.0273     0.509       0.270           ~0.5x
    hold-30/enter-20    25.23   0.0398     0.515       0.287            0.58x
    hold-15/enter-10    12.44   0.0809     0.549       0.194            0.96x

HHI -31%, which is almost exactly the mirror of #81's +31% at the *other*
channel, so the two together also bracket the concentration price symmetrically
in size while differing in channel. The book stays at its pool's median
volatility (0.509), so this is not a low-volatility tilt in disguise — which
matters, because `learnings.md` closes the low-vol family on this universe and a
widening book drifting down the volatility ranking would be that result arriving
unlabelled. Churn falls, so the standing turnover confound cannot bite in the
candidate's favour either.

PRE-REGISTERED POINT ESTIMATE: **0.94**, against the seated lead's 0.917 — the
same number #81 pre-registered and missed, and stated with that in mind. The
decomposition behind it: -0.048 from the lost tail excess, against a variance
saving inferred from #80 running the trade backwards (halving breadth cost
-0.043 *net* of a +2.78%/yr mean gain, so the pure breadth term there was worth
roughly -0.18; a +46% breadth increase should return a concave fraction of that,
call it +0.05 to +0.09).

**Both outcomes close the axis, and I am naming them in advance.** Above ~0.94:
the seated lead is on a slope, the family wants a wider book than every
non-`price-trend` scout has used, and the inherited hold-30/enter-20 is too
narrow rather than too wide — the single most transferable thing tonight could
produce, since twenty-five books share that band. Between 0.90 and 0.94: the
incumbent is an interior optimum, the axis is closed by a three-point bracket,
and equal-weighted enter-20 stands as measured rather than inherited. Below
0.90: concentration and de-concentration both lose, which would mean the
incumbent sits at a local peak sharp enough to be suspicious of, and the honest
reading is that all three books are one object inside the family's resolution
floor — in which case the right conclusion is that this axis cannot be resolved
here at all, and I will record that rather than the ranking.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. n = 27 outside
`price-trend`. Tonight's two readings both over-predicted (1.13 -> 0.874,
0.97 -> 0.868), which killed the 2026-09-03 hypothesis that the seated lead's
exact reading belonged to its being a plain single sort.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_region_wide30",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Widening the seated family lead's band from hold-30/enter-20 to hold-45/enter-30 "
        "— the same 1.5x band ratio, and window, weighting, grid, pool and region operator "
        "bit-identical to `lv_illiq_region_relative` — scores near 0.94 on validation "
        "against that lead's 0.917, because tonight's two trials show both concentrating "
        "channels lose in this family (cutting breadth -0.043 at +103% HHI, re-weighting "
        "at fixed breadth -0.049 at +31% HHI) and this is the same trade in reverse: "
        "breadth 25.2 -> 36.9 names and HHI -31%, bought by giving up 0.92%/yr of train "
        "tail excess (+4.31 -> +3.39%/yr, both t > 4) worth about -0.048 of Sharpe if "
        "delivered one-for-one. The book holds its pool's median volatility (0.515 -> "
        "0.509) so this is not the closed low-vol tilt in disguise, and its churn falls, "
        "so the standing turnover confound cannot bite in the candidate's favour. This is "
        "the third and final point of a bracket: above ~0.94 says the hold-30/enter-20 "
        "band that twenty-five non-`price-trend` books inherited is too narrow; between "
        "0.90 and 0.94 says the incumbent is an interior optimum and the axis is closed; "
        "below 0.90 says both directions lose and the three books are one object inside "
        "the family's resolution floor, which would be a statement about what this split "
        "can resolve rather than about the band."
    ),
}

ILLIQ_WINDOW = 63     # one quarter, as the seated lead
CORE_N = 30           # the bracket's wide arm; band ratio held at the seated 1.5x
BAND_N = 45
WARMUP = 6
MIN_REGION = 4        # a region below this cannot supply a peer mean


def _region_relative(score: pd.Series) -> pd.Series:
    """Each name's score minus the mean score of its own region, dropping names
    whose region has fewer than `MIN_REGION` instruments scoreable on that date.

    `groups.REGION_OF` is static instrument metadata read from `data/universe.yaml`
    — no dates, no prices, nothing estimated from returns — so this reads only
    the cross-section it is handed. Identical to the seated lead's helper.
    """
    labels = pd.Series({name: G.REGION_OF.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= MIN_REGION).dropna()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = _region_relative(illiq.loc[:dt].iloc[-1].dropna())
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
