"""Is the union book sensitive to the quality of the leg you put in it?

WHY THIS FILE EXISTS. Tonight produced two results that only mean something
together.

**One.** The union leg-count ladder was completed and then given its intercept:

    legs   book                                    validation
    0      all four scores replaced by hashes  (#77)   0.759
    1      seasonal alone                      (#72)   0.782
    2      + reversal / suv / placebo      (#73-#75)   0.786 / 0.913 / 0.799
    3      + illiq + group_lead                (#76)   0.889
    4      all four                            (#71)   0.958

Monotone on five rungs, R^2 0.974, slope +0.0505 per leg, fitted intercept
0.7433 — against a zero-leg rung *pre-registered at 0.75* and landing at 0.759.
The shape survived its hardest control. But the same table says the seasonal leg
— the only leg in this repo with significant cross-sectional content on train
(decile-10 excess +10.59%/yr, t = +4.16) — is worth **+0.023 over a hash of the
date and the ticker** (t = +0.13), and even the four-leg book beats that hash by
only +0.199 at t = +1.11. Not one rung is individually distinguishable from a
book that reads no market data.

**Two.** Trial #78 built a leg that is genuinely better, in a different family
and on a mechanism argument rather than a fitted one: Amihud `ILLIQ` scored
against the mean `ILLIQ` of the name's own **region**, because `ILLIQ` is a
price-impact ratio whose cross-region level is partly a venue artifact. It scores
validation **0.917** against the unconditional sort's 0.681 (d = +0.236,
`rho` 0.8323, SE 0.2329, t = +1.01) at **1.2x** annual turnover.

So the union family now has, for the first time, a leg whose standalone quality
moved by a measured amount. **The question the ladder cannot answer and this file
can: does that reach the book?**

THE DESIGNED SWAP. Trial #71 with one expression changed — the `illiq` leg
becomes its region-relative version. The other three legs, the z-scoring, the
fixed per-leg quota, the joint-coverage rule, the hysteresis band, the equal
weighting, the monthly grid and the warmup are bit-identical.

MEASURED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN:

    book                    months  first        positions  turnover  joint pool
    #71 unconditional         253   1996-12-31     20.10     11.98x      85.2
    this, region-relative     247   1997-06-30     19.84     11.51x      78.0

    holdings overlap between the two books: 0.762

Churn is matched to 3.9% (~0.07%/yr of cost) and breadth to 1.3%, so this pair
cannot be accused of measuring the broker. One thing is **not** matched and is
stated rather than hidden: regions with fewer than four scoreable instruments
cannot supply a peer mean, so the joint pool narrows from 85.2 to 78.0 names
(-8.5%) and the book starts six months later. `learnings.md` (2026-09-01) priced
the machinery-and-coverage confound at +0.036, and this coverage change runs
**against** the swap — a smaller pool to select 20 names from. The swap therefore
has to beat #71 through leg quality while paying for a narrower pool.

PRE-REGISTERED POINT ESTIMATE: **1.02**, i.e. +0.06 on #71's 0.958. That is the
ladder's own slope of +0.0505 per leg applied once: the swap does not add a leg,
it upgrades one from roughly placebo-grade to the best standalone leg on the
board, which is the same move in leg-quality units. The two accounts are:

  * **Content-sensitive.** The union transmits leg quality and this lands near
    1.02 — which would also make it the best non-`price-trend` result on record
    and, more usefully, would mean the ladder measures signal rather than breadth.
  * **Content-insensitive.** It lands at 0.958 or below. Combined with #77's
    placebo intercept and the 2-leg triple's coin flip, that would say the union
    machinery responds to the *number* of orderings it is given and not to what
    is in them — a breadth effect wearing a signal's clothes — and the family
    should be closed rather than extended, because nothing the lab can do to a
    leg would then reach the book.

Note that the resolution is better here than anywhere else in this family: at
0.762 holdings overlap the paired SE should run near 0.10-0.12, so a +0.06 effect
is t ~ 0.5-0.6. Still not resolvable on its own, and said so in advance — but the
two accounts differ in **sign of the difference** against a well-measured
anchor, which is what makes the trial worth its place in the deflator.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. Tonight's three readings
were 0.696 -> 0.889 (under), 0.471 -> 0.759 (under) and 0.920 -> 0.917 (near
exact). n = 23 outside `price-trend`, still unresolved.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import groups as G
from strategies.lib import signal_blend as SB
from strategies.lib import union_legs as UL
from strategies.lib import walkforward as W

MIN_REGION = 4        # a region below this cannot supply a peer mean

STRATEGY = {
    "name": "pl_union_region_relative_illiq",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Trial #71's four-leg fixed-quota union book with its Amihud illiquidity leg replaced "
        "by the region-relative version — the one expression that changed, every other leg, "
        "the z-scoring, the per-leg quota, the joint-coverage rule, the hysteresis band, the "
        "equal weighting and the monthly grid left bit-identical, churn matched holdings-only "
        "in advance at 11.51x against 11.98x and breadth at 19.84 against 20.10 names — "
        "scores near 1.02 on validation, about +0.06 above #71's 0.958, because the union "
        "book transmits the standalone quality of its legs and this swap upgrades one leg by "
        "a measured +0.236 (trial #78: 0.917 against 0.681, t = +1.01). Landing at or below "
        "0.958 instead would say the machinery responds to the NUMBER of orderings it is "
        "given rather than to their content — which the completed leg-count ladder already "
        "hints at, since its zero-leg rung built entirely from hashes scores 0.759 and the "
        "best single leg beats that hash by only +0.023 (t = +0.13) — and would close the "
        "family rather than extend it, since no improvement to a leg could then reach a book. "
        "The swap also pays a narrower joint pool (78.0 against 85.2 names) for the regions "
        "too small to supply a peer mean, so the coverage change runs against it."
    ),
}


def _region_relative(panel: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    """`panel` scored against each name's own region mean, published on the same
    rebalance rows the union book reads.

    `groups.REGION_OF` is static instrument metadata read from `data/universe.yaml`
    — no dates, no prices, nothing estimated from returns — so each row reads only
    the cross-section of that row. Rows are built at or before their own date, so
    a truncated frame reproduces its own history exactly.
    """
    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in W.rebalance_dates(prices):
        sub = panel.loc[:dt]
        if sub.empty:
            continue
        row = sub.iloc[-1].dropna()
        if row.empty:
            continue
        labels = pd.Series({name: G.REGION_OF.get(name) for name in row.index})
        grouped = row.groupby(labels)
        rows[dt] = (row - grouped.transform("mean")).where(
            grouped.transform("size") >= MIN_REGION
        )
    if not rows:
        return pd.DataFrame(index=prices.index, columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns)


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    illiq = SB.illiquidity_score(prices, aux["dollar_volume"], 63)
    legs = {
        "seasonal": SB.seasonal_score(prices),
        "illiq": _region_relative(illiq, prices),
        "group_lead": SB.group_lead_score(prices, 21),
        "reversal": SB.reversal_score(prices, 21),
    }
    return UL.fixed_quota_union(prices, legs)
