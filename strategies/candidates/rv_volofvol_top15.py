"""`range-variance`'s first recorded trial, on the object fifteen screens never ranked.

THIS FILE CHOOSES NOTHING. Every node below — family, track, slug, score, sign,
band, weighting, pool, expected range and falsifier — was fixed in
`experiments/journal.md` under "Pre-registration for the NEXT session —
2026-09-13, the `range-variance` trial, fully specified", written before this
session existed and explicitly so that the session running it would not revisit
it. The value of that block is entirely in not reopening it, so nothing here is
re-derived, re-profiled or re-tuned.

WHY THE FAMILY REOPENED. Thirteen consecutive sessions declined `range-variance`
on fifteen mechanism screens, one identified cause (a current-constituents
universe in which the high-volatility survivors did well) and four robustness
statistics that all flatter that cause. Every one of those readings is a
statement about ranking names by a volatility **LEVEL** — the same bet as the
refuted high-vol side of `low-volatility / quality tilts`. 2026-09-13 asked what
object the screens had actually ranked and profiled two unit-free alternatives
on train. A unit-free *ratio* of two estimators (`RVR` = Parkinson(21)/RV(21))
is empty at 21 and 63 days — a content null, with its own hash placebo more
structured than it is — and is closed. A unit-free *second moment* of one
estimator is not.

THE PREMISE, MEASURED FREE BEFORE THE PRE-REGISTRATION WAS WRITTEN (train,
forward 21d, equal-weight marginal excess by rank slice over the scoreable pool;
the placebo is a hash of (rebalance date, ticker) reading no market data):

    vol-of-vol (CV of RV21        1-15         16-30        31-45        46-60        61-80
      over 252d), LONG HIGH    +4.85(+2.46) -1.19(-0.73) +0.00(+0.00) -2.05(-1.45) -0.51(-0.42)
      LONG LOW                 -3.10(-1.60) +0.93(+0.60) +0.82(+0.56) -0.11(-0.08) -1.46(-1.21)

Content in the top slice, nothing past rank 15, placebo clean. The cumulative
series falls in **both** mean and t past the band (top-5 +9.10 t=+2.64, top-10
+8.45 t=+3.33, top-15 +4.85 t=+2.46, top-20 +3.28 t=+1.94, top-25 +2.78
t=+1.80) rather than the t rising under dilution — which is 2026-09-12's test
for a band that is real rather than an artifact of a shrinking standard error.
**The band is read off the MARGINAL profile at ~15 regardless, per the house
rule**, and that is where this file's `TOP_N` comes from.

THE DECISIVE CONTROL, AND IT IS THE ONE THIS FAMILY HAS NEVER PASSED. Vol-of-vol
is not the level: `spearman(vol-of-vol, GK 21d level)` = **+0.0915** at a top-15
name overlap of **0.216**, and measured INSIDE the high-GK half — where the
survivorship artifact is differenced out — the effect does not merely survive,
it strengthens to **+5.59%/yr (t = +2.75)** against the placebo's -1.93
(t = -1.14) on the identical restriction. Nor is it a re-labelling of anything
seated: `spearman` **-0.0935** to `ILLIQ` 63d, **+0.0039** to 12-1 momentum (the
lowest any live characteristic here has posted against the incumbent), **+0.0769**
to the 21-day volatility level; top-15 overlap with momentum's top-15 is 0.164;
and it holds +3.96%/yr (t = +2.11) inside the high-`ILLIQ` half.

TWO WEAKNESSES, CARRIED FORWARD FROM THE SCREEN RATHER THAN DISCOVERED AFTER IT.
On the stock sleeve alone it reads +4.40%/yr at **t = +1.79** — same magnitude,
n falls 164 -> 127, so it is not an ETF artifact, but that sleeve does not clear
|t| = 2 on its own. And inside the high-momentum half it fades to +1.29%/yr
(t = +0.84), so the effect is weaker among past winners. The pre-registration
makes both of these *diagnostics for a later night*, not nodes of this file.

SIGN. **LONG HIGH**, taken from the train profile above and declared as such
rather than imported: `SUMMARY.md` #106's contested-sign rule applies to
vol-of-vol as the literature leaves it, and the repair for a contested sign is to
measure it on train. A train-set sign applied to a validation-scored book is the
same operation as a train-set band, which this repo does everywhere.

THE HOUSE CONSTRUCTION (`learnings.md`, 2026-09-10), varied at no node:
rebalance grid `walkforward.rebalance_dates` with warmup 6, last TRADING day of
each month; pool every instrument scoreable on the date, **ETFs included**;
equal weight, which is the house default everywhere outside `price-trend`; no
group demeaning (2026-09-10's `m`/`dm` split indicates the region operator
exactly where the lab applies it and contra-indicates it elsewhere). Closes only,
so the one-argument contract suffices and no aux panel is read. The only node
NOT inherited is the band, which the house table says must never be inherited and
which the marginal profile above sets.

PRE-REGISTERED, FALSIFIABLE: **validation Sharpe 0.55, range 0.30-0.90.** No
non-`price-trend` scout in this repo has cleared 1.01, and this is a
single-characteristic equal-weight book on a weakly-priced score, so **a reading
above 1.01 should be treated as suspicious rather than as a win**. Falsified by a
validation Sharpe below 0.30, or by an `avg_positions`/turnover profile far from
the ~15 names and ~4.3x annual two-way turnover the train screen implies (~2.7 of
15 names replaced per month, pool ~131 at rebalance).

WHAT IT MUST NOT BECOME: no second band, no second window, no magnitude
weighting, no demean, no blend with a seated lead. Each is a second object and
needs its own night.

SCOUT. It does not compete for the seat, the champion is not compared, and the
holdout is unreachable from this track — so this trial cannot end the session.
It discharges `program.md`'s cold-family allocation rule, unmet for fourteen
sessions, and it is this family's first recorded trial.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "rv_volofvol_top15",
    "family": "range-variance",
    "track": "scout",
    "hypothesis": (
        "An equal-weight monthly book holding the top 15 names by vol-of-vol — the "
        "coefficient of variation of 21-day realized volatility over a trailing 252 days, "
        "long HIGH — scores a validation Sharpe of 0.55 (range 0.30-0.90), above the 0.49 "
        "equal-weight floor, because vol-of-vol is the first `range-variance` object that is "
        "not the volatility LEVEL the family's fifteen previous screens all ranked: it "
        "correlates only +0.0915 with the 21-day Garman-Klass level at 0.216 top-15 name "
        "overlap, carries +4.85%/yr (t = +2.46) over train ranks 1-15 with nothing past rank "
        "15 and a clean placebo, and STRENGTHENS to +5.59%/yr (t = +2.75) when measured "
        "inside the high-Garman-Klass half where the survivorship artifact is differenced "
        "away — which is the control every previous object in this family failed."
    ),
}

RV_WINDOW = 21        # short-horizon realized volatility, the object whose variation is scored
VOV_WINDOW = 252      # trailing window over which that volatility's own CV is taken
VOV_MIN_PERIODS = 126 # pre-registered
TOP_N = 15            # from the MARGINAL depth profile, not inherited
WARMUP = 6            # house default


def _vol_of_vol(prices: pd.DataFrame) -> pd.DataFrame:
    """Coefficient of variation of trailing realized volatility.

    `std(RV21, 252) / mean(RV21, 252)`. Unit-free by construction — the scale of
    each name's own volatility divides out — which is the entire reason this
    object is not the level that fifteen screens identified as this universe's
    survivorship artifact.

    Every input is backward-looking: `realized_vol` is a trailing rolling std of
    past returns and both outer rollings are trailing, so the value on row `t`
    reads nothing after `t`.
    """
    rv = F.realized_vol(prices, RV_WINDOW)
    roll = rv.rolling(VOV_WINDOW, min_periods=VOV_MIN_PERIODS)
    mean = roll.mean()
    std = roll.std()
    return std / mean.where(mean > 0)


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    vov = _vol_of_vol(prices)

    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        sub = vov.loc[:dt]
        if sub.empty:
            continue
        score = sub.iloc[-1].dropna()          # pool: every name scoreable on the date
        if len(score) < TOP_N:
            continue
        names = sorted(score.nlargest(TOP_N).index)   # LONG HIGH, hard cut, no hysteresis
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
