"""Low Garman-Klass volatility, 100 names, equal weight, rebalanced quarterly.

WHY THIS IS THE FIRST v3 TRIAL. Protocol v3's re-measurement of the v2 board
(`reports/protocol-v3-methodology.md`) is a single finding stated five times: every
scored v2 trial was a 20-22x-turnover book, every one of them beat its own random
null at the 98th-100th percentile, and not one of them beat simply holding the
equal-weight eligible pool (skill -0.01 to -0.26, all negative at 2x costs, all
negative on train). The pool is at 0.452 on validation. So the binding constraint
under v3 is not signal, it is **cost**: a book that trades 22x a year pays 3-6%/yr
of liquidity tier plus stamp duty and must out-earn that before it earns anything.
The arithmetic says the first thing to try under v3 is the opposite corner of the
design space -- the lowest-turnover construction that can still plausibly carry a
Sharpe edge over the pool.

THE MECHANISM, AND WHY IT IS A SHARPE CLAIM AND NOT A RETURN CLAIM. The
low-volatility anomaly is the observation that the cross-section of realized
volatility is flat in mean return while steep in risk, so the low-volatility end
earns the same money with much less variance. That is a claim about the *ratio*,
which is exactly what v3 scores, and it is why the two previous readings in this
repo cannot settle it:

  - the v2 cross-sectional IC screen (`learnings.md`, 2026-10-07) priced low-vol and
    low-idiosyncratic-vol as "one object (rho +0.82) and both nulls" -- but an IC
    against the forward 21-day *return* measures the numerator only. A signal that is
    deliberately flat in mean return and steep in volatility scores exactly zero on
    that screen whether or not it raises Sharpe. The screen was pointed at the wrong
    moment of the distribution.
  - v1's fifteen `range-variance` screens and the three de-risking overlays in
    `learnings.md` measured low-vol as a *conditioner on a momentum book* on 140
    surviving names under v1 execution. None of them measured it standalone, on the
    point-in-time panel, as a book of its own.

WHAT THE FREE SCREENS MEASURED TONIGHT (train split 1997-2017 only, 252 month-ends,
no portfolio formed and no return or Sharpe computed outside `run_experiment.py`;
journal entries F1-F3):

    quantity                                           value
    IC(-GK vol 252d, forward 63d return), all names   +0.0005  (t +0.04, n 220)
    IC(-GK vol 252d, forward 21d return), all names   +0.0007  (t +0.04, n 222)
    IC(-GK vol 252d, forward 63d return), stocks only -0.0017  (t -0.11, n 243)
    mean GK vol of the bottom 100 / pool mean          0.614
    mean 252d beta to the pool, bottom 100             +0.623
    mean 252d beta to the pool, all eligible           +0.983
    => beta ratio                                      0.633
    bottom-100 name overlap at 3 months                0.873
    => one-way turnover at a quarterly rebalance       0.51x/yr

**The two columns together are the hypothesis.** The mean is a flat null on this panel
(t +0.04, i.e. the low-vol end earns neither more nor less per dollar than the
high-vol end), while the systematic risk the money is earned on is a third lower
(beta 0.62 against 0.98). A ratio whose numerator is unchanged and whose denominator
falls by a third rises. Nothing else in the table is doing the work, and the flat IC
is what makes the claim *testable*: if the mean were positive this would be a return
anomaly dressed as a risk one.

WHY THE TURNOVER NUMBER IS THE SECOND HALF OF THE ARGUMENT. 0.51x a year one-way
against the v2 board's 22x is a factor of 43. At v3's 15-40 bps per side that is
roughly 13 bps/yr of cost against the 3-6%/yr the v2 leads paid, so this book's
quoted Sharpe is almost entirely insensitive to the cost model -- which is precisely
the sensitivity that destroyed the v2 board. The 2x-cost stress recorded with this
trial should therefore come back nearly unchanged, and that is the clean, falsifiable
reading: if this candidate's skill collapses at 2x costs, the turnover arithmetic
above is wrong and I want to know it.

WHY GARMAN-KLASS AND NOT CLOSE-TO-CLOSE. The range estimator extracts several times
more information per observation, which matters at a 252-day window across a panel
where many names are thinly traded. The two are nearly the same object here
(cross-sectional rho +0.909 on train), so this is an efficiency choice and not a
mechanism choice -- which is also why the family slug below is `price-trend` and not
`range-variance`. `program.md` files "low-vol / quality" under `price-trend`, and
feeding a low-vol sort a range-based estimator instead of a close-to-close one does
not make it a different family. Calling this `range-variance` would be spending an
untouched family slug on a relabelling, which is the trap `learnings.md` 2026-10-07
caught at rho +0.98 and the reason that entry exists. This trial is therefore counted
against `price-trend`'s cap of 2.

WHAT THE BOOK WILL LOOK LIKE, PRE-REGISTERED SO THE COMPOSITION IS NOT A SURPRISE.
The candidate cannot see instrument types, so it does not restrict to stocks, and on
train the bottom-100 selection ran **27% ETFs against the pool's 7%** -- low-volatility
selection on a mixed panel naturally prefers diversified baskets to volatile single
names. The random-selection null matches type and (for stocks) listing region, so the
ETF share and the region mix are both neutralised in the null and the gate tests
low-vol selection against random-of-the-same-kind, which is the comparison that should
decide this. Region spread: 1 region (all US) before 2009, ~6 after, tracking the pool.

PRE-REGISTERED PREDICTION. Validation Sharpe **+0.55 to +0.75** against the pool's
0.452, i.e. skill **+0.10 to +0.30**, from the beta ratio 0.633 discounted for the
idiosyncratic variance a 100-name book keeps and for the fact that a flat IC is not a
*positive* IC. Train skill **positive in both sub-periods**: 1997-2008 contains two
regimes (2000-02, 2008) in which the low-volatility end is where the money stayed, and
the beta ratio is 0.72 and 0.54 in the two halves respectively. Note that by this
repo's own anti-prediction rule a confident train story is a bearish signal for
validation, and it is recorded as such rather than left out.

FALSIFIERS, all three informative.
  - Skill at or below zero on validation with the beta ratio intact says the
    low-volatility anomaly does not survive on this point-in-time panel under
    realistic execution, which would be the cleanest negative result the lab has: it
    would mean the pool's extra variance is compensated after all.
  - Positive validation skill with *negative* train skill fails the gate and says the
    effect is a 2018-2023 artifact -- the exact pattern `GATES_V3["min_train_skill"]`
    was added to refuse.
  - A null percentile below 90% says the Sharpe gain is what any 100-name book of the
    same types and regions would have got, i.e. de-concentration rather than
    low-volatility selection. That is the single most likely way this fails and the
    reason the book is 100 names rather than 30: a 30-name low-vol book would confound
    the two, and the null's 90% quantile is nearly flat in K (`learnings.md`
    2026-10-07), so nothing is given up by widening it.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F

STRATEGY = {
    "name": "pt_lowvol_gk_quarterly",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "Holding the 100 eligible names with the lowest trailing 252-day "
        "Garman-Klass range volatility, equal weight, rebalanced only at "
        "quarter-ends, beats the equal-weight eligible pool's validation Sharpe "
        "of 0.452 by at least 0.10, because on the train split that selection's "
        "cross-sectional IC against the forward 63-day return is a flat null "
        "(+0.0005, t +0.04) while its mean 252-day beta to the pool is 0.633 of "
        "the pool's own (0.623 against 0.983) -- an unchanged numerator over a "
        "denominator a third smaller -- and because at 0.51x one-way turnover a "
        "year, 43 times less than every scored v2 trial, the cost model that "
        "destroyed the v2 board cannot reach it; skill at or below zero says the "
        "pool's extra variance is compensated after all, and a null percentile "
        "below 90% says the gain was de-concentration rather than low-volatility "
        "selection."
    ),
}

VOL_WINDOW = 252
TOP_N = 100
MIN_NAMES = 150
MIN_COVERAGE = 0.8


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    # Quarter-ends only: the whole point of the construction is that it almost
    # never trades. Drift between rows is deliberate and is what a no-trade
    # region buys under proportional costs.
    rebalance_dates = prices.groupby(pd.Grouper(freq="QE")).tail(1).index

    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)

    # Per-column rolling estimator: causal in the time axis, and it involves no
    # cross-sectional normalisation at all, so the column-axis look-ahead of
    # `learnings.md` 2026-10-07 cannot arise here. The mask is applied to the
    # values before any selection, never after.
    vol = F.garman_klass_vol(aux["open"], aux["high"], aux["low"], prices, window=VOL_WINDOW)
    covered = prices.notna().rolling(VOL_WINDOW, min_periods=1).mean()

    rows = {}
    for dt in rebalance_dates:
        if dt not in vol.index:
            continue
        v = vol.loc[dt].where(elig.loc[dt] & (covered.loc[dt] > MIN_COVERAGE))
        v = v[v > 0].dropna()
        if len(v) < MIN_NAMES:
            continue
        picked = v.nsmallest(min(TOP_N, len(v))).index
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
