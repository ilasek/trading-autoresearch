"""Illiquidity, neutralised on the trading-calendar peer axis, 100 names,
monthly grid, held through a top-200 retention band.

THE QUESTION THIS IS AIMED AT. The 2026-10-10 session left one live question:
"is the equal-weight eligible pool beatable by cross-sectional selection on free
daily data under v3 execution?" Two v3 trials say no so far, and both failed the
same two gates (train skill, random-selection null). This is the first v3 trial
in `liquidity-volume`.

THE MEASUREMENT THAT MOTIVATES IT, AND IT IS A METHOD FINDING FIRST. Protocol
v3's random-selection null is region-matched; the skill statistic is not -- it is
against the whole equal-weight pool, which is 76% US over the train split (97%
before 2009, 48% after, because the eight non-US indices join in 2009). So a
score correlated with listing region produces a book whose excess over the pool
is geography, and only the null can see it. Screening the same score both ways
separates the two, and on the train split it reverses two conclusions
(journal F3/F4, 211-222 month-ends, excess of the top-100 slice's forward 63-day
return over the eligible pool's, in bps):

    score (top-100 slice)        vs whole pool      vs a region-matched pool    US%
    days since first eligible     +43.2 (t +3.12)        +5.3 (t +0.66)        100%
    126d Amihud illiquidity       +18.3 (t +0.93)       +46.8 (t +3.23)         50%

The first row is the kill: "hold the longest-standing index members" looks like
the best signal this lab has screened under v3 and is **entirely** a US tilt --
the slice is 100% US on every one of 222 dates, because the S&P 500 is eligible
from 1996 and everything else from 2009. It was declined on this arithmetic and
is not what is being run. The second row is the inverse error: the illiquidity
premium is *hidden* by the whole-pool comparison, because an unconstrained
illiquidity sort is half non-US against a pool that is three-quarters US, so a
real within-market premium is paid for with a geography bet of the opposite sign.

WHY THIS IS NOT A RE-TEST OF A REFUTED IDEA. `learnings.md` records two readings
on Amihud and neither measures this object. (i) v2's screen is a *rank IC*
against the forward 21-day return (-0.0024, t -0.29) and concludes the tilt "adds
no level effect, only a location" -- but the same file's 2026-10-10 entry then
establishes that a rank IC cannot screen a magnitude hypothesis at all, which is
the methodological reason that screen is not binding here. (ii) v3's F7 cut the
*residual-reversion* book by liquidity and found restricting it to the liquid
half deletes 91% of its gross excess -- a result about conditioning a reversal
book, and its own conclusion was that "a liquidity split on a fixed book size is
confounded with tail depth". Neither measured illiquidity standalone, at a 63-day
horizon, region-neutral, as a book. The stated reason to re-open it is that the
region-matched screen is a different measurement, not a re-run of the same one.

THE CONSTRUCTION, PRE-REGISTERED BEFORE RUNNING (journal F7; every number below
is train-split only).

  - Score: 126-day log Amihud, `features.amihud_illiquidity`. Higher = more
    price impact per dollar. No other input, no conditioner, no tilt.
  - Peer groups: `lib/calendar_peers.calendar_peers` on the trailing 252 days of
    the raw volume panel, over **only the names eligible on the decision date**.
    Volume is not forward-filled, so a name's non-print days are its listing
    market's holidays; grouping on that pattern recovers the region axis at a
    name-weighted purity of 0.96 / 0.94 / 0.95 in 2005 / 2012 / 2017, with 1, 7
    and 7 groups. Masking to the eligible set first is required, not tidiness:
    anchors derived from the whole visible frame would depend on its column
    count, which differs between the truncated and untruncated causality runs
    (`learnings.md` 2026-10-07 -- the leak that cost trial #4). Groups are
    re-estimated once a calendar year, which is also what keeps the call cheap.
  - Selection: `peer_quota_select` takes the highest-Amihud names group by group,
    with each group's quota proportional to its share of the eligible panel. The
    book's geography therefore matches the pool's by construction (measured 79%
    US against the pool's 76%) and what is left to measure is selection.
  - K = 100, retention band B = 200: a held name is kept while it is still
    inside the peer-neutral top 200. The band is this lab's one measured
    construction win (`learnings.md` 2026-10-10: at K=100 a top-200 band cut name
    turnover 42% and *raised* the held book's train excess) and it reproduces
    here, independently: +82.3 bps -> +94.2 bps while name turnover falls from
    0.81x to 0.23x a year.
  - Equal weight inside the book, monthly grid. Equal weighting needs no defence
    under this benchmark -- the pool *is* that operator at its limit, so a book
    that equal-weights its selection is long the tilt over its names and short it
    over the complement, and its measured skill is about selection
    (`research/SUMMARY.md` #246).

Pre-registered train screen for the chosen cell (K=100, B=200), and the
alternatives that were not chosen, so the choice is on the record rather than in
a sweep:

    K    B      exc bps/63d        t     name turn/yr   1997-2008      2009-2017
    100  none        +82.3     +3.92         0.81      +34.6/+1.6    +130.5/+3.7
    100  200         +94.2     +5.75         0.23      +44.5/+2.6    +144.5/+5.3   <- run
    100  300         +90.7     +5.17         0.14      +30.8/+1.7    +151.3/+5.1
    200  none        +48.5     +4.62         0.49      +14.0/+1.8     +83.3/+4.4
    200  400         +44.3     +4.03         0.12       -7.1/-1.2     +96.1/+4.8

K=100/B=200 is taken because it is the only cell that is both the strongest and
positive in both train sub-periods; the two widest cells buy lower turnover by
giving up 1997-2008, which is the half of train the gate cannot be fitted to.

TURNOVER, PRE-REGISTERED AS A RANGE. The name-overlap screen says 0.23x/yr, and
`learnings.md` records that such a screen is a **lower bound** -- it missed by
1.6x on train and 3.2x on validation last time, because validation name churn
ran 68% above train's. So the honest pre-registration is **0.2x to 1.5x a year**,
and anything inside that is not a surprise. At the illiquid slice's measured
trailing median dollar volume ($18-28M/day, 10th percentile $6.6M, i.e. v3's 20
and 30 bps tiers rather than the 40 bps floor) this is a cost bill of order 10-30
bps a year against a gross excess of order 300 bps, so unlike every v2 lead this
book is not a bet on the cost model. The equal-weight pool itself pays 0.22%/yr
at 0.89x turnover (journal F2), so the comparison is close to cost-neutral.

WHAT WOULD FALSIFY IT, AND THE THREE WAYS IT CAN STILL BE AN ARTIFACT. The
hypothesis is directional and the magnitudes above are **not** imported as
expectations: the train excess is ~1.3 bps/day and flat in horizon (+25.9 at
h=21, +81.7 at h=63, +164.8 at h=126 before the band), which is the signature of
a level premium rather than a forecast, and a level premium is exactly what a
Sharpe statistic can refuse -- an illiquid book can earn more and still score
worse. Three named risks. (1) **Delisting.** An illiquidity-tilted book is the
most exposed thing in this lab to the delisting bias that remains in a
Yahoo-priced universe; the pre-screen shows 0.000% of selected names' series end
within 63 days on train, so the screen itself is not survivorship-inflated, but
`skill_delist30` is the number that decides it and it has not been seen.
(2) **Regime.** 2009-2017 does roughly three times 1997-2008's excess, and
1997-2008 is the half with 40-66% Yahoo coverage of index members. (3) **Purity.**
The peer grouping is 0.94, not 1.0, so a residual geography bet survives
neutralisation; the region-matched null is the gate that prices it.

Scout track: the v3 deflator already counts 36 effective trials across all
versions, so no single-mechanism candidate can reach the seat on its own, and a
scout spends no holdout look.
"""

import numpy as np
import pandas as pd

from strategies.lib import features
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

STRATEGY = {
    "name": "lv_illiq_peer_neutral_band",
    "family": "liquidity-volume",
    "hypothesis": (
        "Selecting the 100 highest-Amihud-illiquidity eligible names group by group across "
        "trailing-trading-calendar peer groups, in quotas proportional to each group's share of "
        "the eligible panel, and holding them through a peer-neutral top-200 retention band on a "
        "monthly grid, earns positive train and validation skill against the equal-weight "
        "eligible pool under v3 execution, because the price-impact premium is a within-market "
        "effect whose whole-pool excess is cancelled by the opposite-signed geography bet an "
        "unconstrained illiquidity sort carries (train: +18.3 bps/63d against the whole pool at "
        "50% US, +46.8 against a region-matched pool), and neutralising the geography axis rather "
        "than the score is what makes the comparison a selection claim."
    ),
    "track": "scout",
}

AMIHUD_WINDOW = 126        # days of |return| / dollar volume
CALENDAR_LOOKBACK = 252    # days of trading-calendar fingerprint
K = 100                    # names held
BAND = 200                 # a holding is kept while inside the peer-neutral top BAND
MIN_SCORED = 200           # too few scored names to form peer quotas -> emit nothing


def generate_weights(prices, aux, eligible=None):
    volume = aux["volume"]
    dollar_volume = aux["dollar_volume"]
    illiq = features.amihud_illiquidity(prices, dollar_volume, window=AMIHUD_WINDOW)

    elig = (
        pd.DataFrame(True, index=prices.index, columns=prices.columns)
        if eligible is None
        else eligible.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    )

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows: dict = {}
    peers_by_year: dict = {}
    held = pd.Index([])

    for date in month_ends:
        live = elig.loc[date]
        eligible_names = live[live.to_numpy()].index
        if len(eligible_names) < MIN_SCORED:
            continue

        # Peer groups are re-estimated once a calendar year, over the names
        # eligible on that date only (see the module docstring in calendar_peers).
        year = date.year
        if year not in peers_by_year:
            peers_by_year[year] = calendar_peers(
                volume, date, eligible_names, lookback=CALENDAR_LOOKBACK
            )
        groups = peers_by_year[year].reindex(eligible_names).dropna()

        score = illiq.loc[date].reindex(groups.index).dropna()
        if len(score) < MIN_SCORED:
            continue
        groups = groups.reindex(score.index)

        target = peer_quota_select(score, groups, K)
        if len(held):
            inside = peer_quota_select(score, groups, BAND)
            keep = held.intersection(inside)
            room = K - len(keep)
            additions = [c for c in target if c not in keep][: max(room, 0)]
            selected = pd.Index(list(keep) + list(additions))
        else:
            selected = target
        if not len(selected):
            continue

        rows[date] = pd.Series(1.0 / len(selected), index=selected)
        held = selected

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
