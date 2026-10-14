"""Ten-year mean reversion: this panel's only reachable proxy for a low price
relative to fundamentals, region-neutralised.

Hypothesis (pre-registered, see the journal entry for this trial): the 100
eligible names with the *lowest* trailing ten-year mean monthly return earn
positive skill over the equal-weight eligible pool, because a decade of flat
prices in a name that is still a large-cap index member is the cheapest thing
this panel can say about price relative to fundamentals, and no fundamental
data is available here.

Why this is a new object rather than a known one in costume. Measured on train
over 42 month-ends before this file was written, the score's rank correlation
is +0.345 to the three-year reversal this lab screened as a null
(`ret756_skip21`, journal F3/F4 2026-10-13), +0.055 to index seasoning (the
score that turned out to be a pure US tilt the same night), +0.014 to 21-day
reversal and +0.126 to 126-day Amihud illiquidity. The ten- and twenty-year
windows are one object (rank rho +0.872); the ten-year window is taken because
it is the stronger and the *more balanced across the train sub-periods* of the
two, which is the whole of the window search that was run.

What the screen said, and the two things in it that argue against the book:

    region-matched excess, fwd 63d, K=100, no band   +81.3 bps  (t +3.16)
    1997-2008 / 2009-2017                            +60.6/+2.14  +102.5/+2.36
    unconstrained sort, whole-pool reading           +31.4 bps  (t +1.42)
    one-way name churn                               0.87x/yr
    slice beta / slice vol vs pool                   0.87 / 0.97
    appraisal ratio vs pool (train, gross)           +0.20, SR - rho*SR_pool +0.088

Neutralising region *doubles* the excess (+31.4 -> +81.3), the same sign as the
illiquidity case: the unconstrained sort is 53% US against a 72% US pool and
pays for its selection with an opposite-signed geography bet. Against the book:
the excess is flat in bps per day across 21/63/126/252-day horizons (1.4, 1.2,
1.1, 1.3), which `experiments/learnings.md` (2026-10-13) names as the signature
of a risk premium rather than a forecast -- though the paired condition that
made that a refusal last time (earns more *and* risks more) does not hold here,
since the slice carries 0.97x the pool's volatility at 0.87 beta. And a
loser-buying book is exactly what v3's delisting haircut exists to price: on
train, 0.000% of the selected names' series end within the horizon, same as the
pool's, so the stress is expected to move nothing, but the stress is the test.

No retention band: one-way churn is already 0.87x/yr against the pool's own
0.89x, so the book competes cost-neutrally and there is nothing for a band to
cut. A band at B=300 did raise the t-statistic (+79.3 at t +3.75) while cutting
churn to 0.14x/yr, and that is declined on this lab's own rider -- a near-static
book's monthly observations are one draw repeated and its t is an upper bound
(learnings, 2026-10-10).

Pre-registered turnover, as a range with the wider split's churn in it: the
engine's metric counts both sides and validation name churn ran 68% above
train's last time it was measured, so 1.3-3.5x annualised is the predicted band.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
MONTHS = 120
MIN_MONTHS = 60

STRATEGY = {
    "name": "pt_decade_reversal_peer_neutral",
    "family": "price-trend",
    "hypothesis": (
        "Selecting the 100 eligible names with the lowest trailing ten-year mean monthly "
        "return, with entries quota-allocated across trailing-trading-calendar peer groups "
        "so the book's geography matches the pool's, earns positive validation skill over "
        "the equal-weight eligible pool, because a decade of flat prices in a name that is "
        "still a large-cap index member is this panel's only reachable proxy for a low price "
        "relative to fundamentals -- distinct from the three-year reversal this lab measured "
        "as a null (rank rho +0.35) and from index seasoning (+0.06)."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K lowest ten-year mean monthly returns,
    with entries quota-allocated across trailing-calendar peer groups."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    # Monthly returns, then the trailing mean. Every value published on a month
    # label uses only returns realized at or before that label, and the daily
    # reindex forward-fills, so a decision date reads the latest label at or
    # before it.
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    decade = mret.rolling(MONTHS, min_periods=MIN_MONTHS).mean()
    score = (-decade).reindex(prices.index, method="ffill")

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for date in month_ends:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 50:
            continue
        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < 50:
            continue
        groups = calendar_peers(volume, date, names)
        picked = peer_quota_select(sc, groups, K)
        if len(picked) < 20:
            continue
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
