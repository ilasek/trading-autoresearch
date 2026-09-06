"""The same intersection operator with its breadth held fixed by construction.

WHY THIS FILE EXISTS. Trial #83 (`pl_signal_intersection`) scored validation
**0.804** against a pre-registered 1.00, and the run reported `avg_pos` **9.1**
against the **13.9** the band was profiled at. The two moved together, and
`learnings.md` is explicit that a scout changing selection and breadth at the same
time cannot answer a mechanism question. This file changes nothing but the band
rule, so the operator can be read.

THE FAULT, MEASURED AND MECHANICAL. An intersection of two orthogonal scores, each
keeping the top `m` of a pool of `n`, holds about `m^2/n` names. Every book in this
repo uses an **absolute** band (top-20, top-30) because for a single sort book size
is `m`, independent of `n`. For an intersection it is not: breadth is quadratic in
the band and **inverse in the pool**, so an absolute band silently de-broadens as
the universe grows. Measured on the realised pool, holdings only:

    period ending   mean pool   mean core   30*30/pool
      2000            55.4        14.0        16.2
      2005            76.7        12.2        11.7
      2010           114.8         8.7         7.8
      2015           123.6         7.7         7.3
      2020           125.2         8.2         7.2
      2025           126.0         6.3         7.1

    train split      104.5         9.88        8.61
    validation       125.7         6.67        7.16

The core tracks `m^2/n` closely, and the pool grows 55 -> 126 across the sample.
So #83's band was profiled on a train split averaging 104 names and then traded on
a validation split averaging 126, where the identical band buys a **third fewer
names**. Its 0.804 is the operator and a breadth collapse together, and the
liquidity-volume half of this book sits in the one family where de-concentration
has been measured to *help* monotonically across a 3x span (2026-09-04).

THE REPAIR, AND IT IS THE ONLY CHANGE. Each leg keeps the top
`m = round(sqrt(TARGET * n))` of the joint pool, so the expected intersection is
`m^2/n = TARGET` names at **any** pool size. `TARGET = 14`, the size at which the
2026-09-06 screen was run and passed its placebo, and the size #83 was designed
for and missed.

The buffer is set on the same arithmetic rather than inherited, which is the
second thing the quadratic scaling changes. The family's standing hysteresis is a
1.5x band-to-core ratio at **book** level. Applying 1.5x per leg would give an
intersection band of `2.25 * TARGET`, because the ratio squares through the
operator. So the band leg keeps `round(sqrt(1.5 * TARGET * n))`, which lands the
band intersection at `1.5 * TARGET` -- the same book-level hysteresis every other
book in this repo runs, expressed correctly for an intersection.

WHAT IS HELD BIT-IDENTICAL TO #83: both legs and every parameter inside them (the
champion's four lookbacks and skip-month, the 63-day ILLIQ window, the region
operator and its `MIN_REGION = 4`), the warmup, the equal weighting, and the
**pool floor of 45 names**. The floor is deliberately not re-tuned even though the
repair no longer needs it, so the two trials run on exactly the same set of
scoreable month-ends and the comparison is paired rather than a comparison of
samples -- the 2026-09-04 lesson that a band change silently changes the train
sample, applied prospectively for the first time.

PRE-REGISTERED POINT ESTIMATE: **0.90**, against #83's 0.804. The decomposition:
validation breadth 6.7 -> 14 names is a +109% change, and the only calibration
this repo has for that axis outside `price-trend` is the liquidity-volume bracket
(12.4 -> 25.2 -> 36.9 names scoring 0.874 -> 0.917 -> 0.942), which is worth about
+0.04 per doubling in the region of interest. `CLAUDE.md` forbids carrying a
constant into a new family by analogy, and this book is only half that family, so
+0.10 is stated as a deliberately generous allowance rather than a reading of that
table. The falsifying branches, named in advance:

  - **>= 1.008**: the intersection takes the `portfolio-learning` lead and the
    operator is real; #83 measured its band, not its operator. I do not expect this.
  - **0.942 to 1.008**: beats the ILLIQ leg but not the max operator, so the
    intersection is a third live operator without headroom.
  - **0.85 to 0.942**: the breadth account is directionally right and the operator
    still does not beat its own better leg. `portfolio-learning` then closes on all
    three aggregation operators, with the intersection's failure attributed to
    breadth rather than to content -- a different epitaph from the union's.
  - **<= 0.804**: the breadth account is **wrong**, #83's number was the operator,
    and the intersection is refuted on its own terms with no confound left to
    blame. This is the branch that makes the pair worth two trials rather than one.

Either of the last two closes the family. Both are informative, which is why the
repair is worth running rather than assuming.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import math

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_intersection_fixed_breadth",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Holding the intersection book's breadth fixed by construction -- each leg keeping the "
        "top round(sqrt(14*n)) of a joint pool of n, so the expected intersection is 14 names at "
        "any pool size, with the buffer band at round(sqrt(1.5*14*n)) so the book-level "
        "hysteresis is the family's usual 1.5x rather than the 2.25x an inherited per-leg ratio "
        "squares into -- scores near 0.90 on validation against trial #83's 0.804, with both "
        "legs, the region operator, the warmup, the equal weighting and the 45-name pool floor "
        "bit-identical so the two trials run on the same scoreable month-ends. #83 reported "
        "avg_pos 9.1 against the 13.9 its band was profiled at, because an intersection holds "
        "about m^2/n names: breadth is quadratic in the band and inverse in the pool, and this "
        "repo's pool grows from 55 to 126 names across the sample, so an absolute band buys a "
        "third fewer names on validation (mean pool 125.7) than on the train split it was "
        "profiled on (104.5). Above 0.942 the operator beats its own better leg and is real; "
        "between 0.85 and 0.942 the breadth account is right and `portfolio-learning` closes on "
        "all three aggregation operators with the intersection failing on breadth rather than "
        "on content; at or below 0.804 the breadth account is wrong and the intersection is "
        "refuted on its own terms with no confound left to blame."
    ),
}

MOM_LOOKBACKS = (252, 189, 126, 63)   # the champion's four horizons, as #83
SKIP = 21
ILLIQ_WINDOW = 63
TARGET_N = 14                         # target book size, held at any pool size
BUFFER_RATIO = 1.5                    # book-level hysteresis, as every other book here
MIN_POOL = 45                         # #83's floor, kept so the two trials are paired
WARMUP = 6
MIN_REGION = 4


def _region_relative(score: pd.Series) -> pd.Series:
    """Each name's score minus the mean score of its own region, dropping names
    whose region has fewer than `MIN_REGION` instruments scoreable on that date.

    `groups.REGION_OF` is static instrument metadata read from `data/universe.yaml`
    -- no dates, no prices, nothing estimated from returns. Identical to #83's.
    """
    labels = pd.Series({name: G.REGION_OF.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= MIN_REGION).dropna()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = [F.xs_zscore(F.trailing_return(prices, lb, skip=SKIP)) for lb in MOM_LOOKBACKS]
    momentum = sum(legs) / float(len(legs))
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        mom = momentum.loc[dt].dropna()
        liq = _region_relative(illiq.loc[:dt].iloc[-1].dropna())
        pool = mom.index.intersection(liq.index)
        n = len(pool)
        if n < MIN_POOL:
            continue

        # Each leg's band, sized so the intersection lands on TARGET_N names
        # whatever the pool size. `m^2 / n = TARGET_N`  =>  `m = sqrt(TARGET_N*n)`.
        core_m = min(n, int(round(math.sqrt(TARGET_N * n))))
        band_m = min(n, int(round(math.sqrt(BUFFER_RATIO * TARGET_N * n))))

        mom_rank = mom.reindex(pool).sort_values(ascending=False).index
        liq_rank = liq.reindex(pool).sort_values(ascending=False).index

        core = set(mom_rank[:core_m]) & set(liq_rank[:core_m])
        band = set(mom_rank[:band_m]) & set(liq_rank[:band_m])
        held = (held & band) | core
        if len(held) < 4:
            held = set(core)
            if len(held) < 4:
                continue

        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
