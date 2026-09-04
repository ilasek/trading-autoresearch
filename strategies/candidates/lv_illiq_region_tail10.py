"""The seated `liquidity-volume` lead at the tail depth its own band was designed for.

WHY THIS FILE EXISTS, AND WHY IT IS NOT A BAND SWEEP. Every non-`price-trend`
book in this repo holds a hold-30/enter-20 band, inherited unexamined from the
books that first used it. Those were built on the **full ~140-name cross-section**,
where enter-20 buys the top ~14% — a tail, which is the whole reason
`learnings.md` (2026-08-30) can record a null 21-day IC coexisting with a
0.70-Sharpe book.

`lv_illiq_region_relative` (#78) then applied an operator that **narrows its own
pool**: region-demeaning drops every name whose region cannot supply four peers,
taking the scoreable pool from ~84 to **~77** names on train. The band was not
revisited. So the seated lead's enter-20 buys the top **26.1%** of its pool — a
quartile, not a tail, and roughly twice as shallow as the depth the construction
was designed around. There is exactly one non-arbitrary repair and it introduces
no new constant: pick the band that restores the **design quantile** on the
narrowed pool. enter-10 of ~77 is **13.0%**, against the 14% the same band buys
on 140 names. hold-15 keeps the band's 1.5x ratio to the core. Nothing here is
tuned against a performance number; the target is fixed by the operator's own
measured effect on the pool.

THE PREMISE, MEASURED FIRST (free, train, forward 21-day return, top-N book
excess over its own scoreable pool — the statistic a tail book is scored on,
per the standing rule not to screen on a quintile spread):

    top-5   ( 6.5% of pool)   +9.90 %/yr (t=+3.89)
    top-10  (13.0%)           +7.09 %/yr (t=+3.97)   <- the design quantile
    top-15  (19.6%)           +5.63 %/yr (t=+4.28)
    top-20  (26.1%)           +4.31 %/yr (t=+4.29)   <- the seated lead
    top-30  (39.1%)           +3.39 %/yr (t=+4.83)

Monotone in depth, and significant at every depth, so the signal is not a
knife-edge of the extreme tail.

THE CONTROL THAT COULD HAVE KILLED IT, RUN BEFORE THIS FILE WAS WRITTEN.
`ILLIQ` is |return| / dollar volume, so a narrower `ILLIQ` book could simply be
tilting further into the high-volatility tail that this universe's survivorship
bias inflates — the single cause behind `range-variance`'s eleven closed
mechanisms, worth +19.4%/yr high-minus-low on train. Weighted mean percentile of
the held book **within its own pool**:

    band                names   vol pct   log-ADV pct
    hold-45/enter-30    36.87    0.509      0.270
    hold-30/enter-20    25.23    0.515      0.287     <- seated lead
    hold-15/enter-10    12.44    0.549      0.194     <- this candidate
    hold-8 /enter-5      6.45    0.558      0.116

The book sits at its pool's **median volatility** at every depth (0.509 -> 0.558
across a 6x change in breadth), while a book that actually harvests the artifact
sits near the 0.9 percentile and earns +8.46%/yr (t=+3.96) on train. Narrowing
therefore does not buy volatility. What it does buy is **size**: log-ADV
percentile 0.287 -> 0.194. That is the one dimension on which this family has a
four-times-measured **null** (log ADV IC +0.0010, t = +0.11; `A_C` closed on its
0.993 rank correlation to it; region-demeaned log ADV top-20 +0.58%/yr,
t = +0.41), so the extra excess is not a disguised size premium either.

WHAT IT COSTS, AND WHY THE STANDING TURNOVER CONFOUND CANNOT BITE HERE.
`learnings.md` records four consecutive non-`price-trend` trials in which a
5-10x turnover difference swamped the mechanism under test. This pair is two
orders of magnitude away from that regime: holdings-only annualised L1 churn on
train is **0.58x** for the seated band against **0.96x** here, i.e. 0.06%/yr of
extra drag at 15 bps a side, worth ~0.006 of Sharpe. The trial cannot be
measuring the broker.

The real cost is concentration, and it is deliberately **not** priced from this
file's own prior: HHI 0.0398 -> 0.0809 (+103%) at breadth 25.2 -> 12.4 names.
`learnings.md`'s de-concentration constant (~0.05 Sharpe per 30% of HHI, which
would put this at -0.17) is a **`price-trend` constant** measured on one
construction, and `CLAUDE.md` forbids carrying it into a new family by analogy.
This trial is the first measurement of that price in `liquidity-volume`, which
is a second reason to run it: whichever way it lands, the family gets a
calibration it currently has to borrow or do without.

PRE-REGISTERED POINT ESTIMATE: **0.95**, against the seated lead's 0.917. The
train tail excess rises by a factor of 1.64 (+4.31 -> +7.09 %/yr) while breadth
halves, so the two effects are large and opposed; the estimate is deliberately
close to the incumbent because this repo has no measured exchange rate between
them outside `price-trend`. Both failure directions are informative and are named
in advance: **below 0.917** says the inherited band was already at or past the
right depth once the pool narrowed, and closes the tail-depth axis in this
family; **materially above 0.95** says the concentration price that dominates
`price-trend` does not transfer here, which is the more valuable of the two
because it is the constant `CLAUDE.md` requires re-measuring.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record
its train Sharpe as a prediction of its validation Sharpe. n = 24 outside
`price-trend`; the seated lead is the best reading ever recorded there (train
0.917 -> validation 0.917, exact to three decimals) and is also the only plain
single sort in the recent set, which is the hypothesis on record for why. This
candidate is the second plain single sort, so it is the first prospective test
of that hypothesis.

SCOUT. It does not compete for the seat and cannot reach the holdout. The solved
required-leg-Sharpe bar for a resolvable 20% blend is 1.34-1.42 against a 1.120
champion; nothing in this family is close, and this file does not pretend to be.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_region_tail10",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Holding the 10 instruments whose trailing-quarter Amihud ILLIQ is highest "
        "relative to their own region's mean — a hold-15/enter-10 band, everything else "
        "bit-identical to the seated family lead `lv_illiq_region_relative` (63-day "
        "window, equal weight, monthly grid, MIN_REGION=4) — scores near 0.95 on "
        "validation, above that lead's 0.917, because region-demeaning narrows the "
        "scoreable pool from ~84 to ~77 names and the inherited enter-20 therefore buys "
        "the top 26.1% of the pool rather than the ~14% tail the same band buys on the "
        "full 140-name cross-section the band was designed on; enter-10 restores that "
        "design quantile at 13.0% and raises the train top-N excess over the pool from "
        "+4.31%/yr (t = +4.29) to +7.09%/yr (t = +3.97). The book stays at its pool's "
        "median volatility throughout (vol percentile 0.515 -> 0.549 against ~0.9 for a "
        "book that harvests this universe's survivorship artifact), so the gain is not a "
        "volatility tilt, and it moves down a size ranking this family has measured as a "
        "null four times, so it is not a size premium. Against it, breadth halves "
        "(25.2 -> 12.4 names) and HHI doubles (0.0398 -> 0.0809); the de-concentration "
        "price that would make this lose is a `price-trend` constant that has never been "
        "measured in this family. A result below 0.917 says the inherited band was "
        "already deep enough once the pool narrowed and closes the tail-depth axis here."
    ),
}

ILLIQ_WINDOW = 63     # one quarter, as the seated lead
CORE_N = 10           # restores the ~13% design quantile on the narrowed pool
BAND_N = 15           # the seated lead's 1.5x core-to-band ratio, unchanged
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
