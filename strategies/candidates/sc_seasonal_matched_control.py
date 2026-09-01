"""Is the union book four legs, or one leg and three passengers?

WHY THIS CONTROL IS THE ONE WORTH RUNNING. `portfolio-learning`'s result rests on
a comparison the lab has never run cleanly. The union books — #68's max-of-z at
1.008 and #71's fixed-share at 0.958 — are quoted as beating "every one of their
four legs (0.681 / 0.747 / 0.688 / 0.701)". But those four leg numbers come from
four candidate files with four *different* constructions: different band widths,
different warmups, and — decisively — a different eligible universe, because a
union book restricts itself to the names **all four legs can score** on each date
while a standalone leg book does not. So "the union beats its best leg by +0.21"
is confounded with machinery, and `SUMMARY.md` #63 asks exactly the question the
confound blocks: which legs are carrying this, and would any survive being priced
against the others?

The return-series version of that audit was run free tonight and is
uninformative in the direction that matters: on stored validation series each
leg's marginal alpha against the other three is +0.23% to +0.93%/yr at t = +0.07
to +0.35 — no leg is distinguishable — while the max-of-z book priced against all
four legs carries **+5.20%/yr at t = +2.10**. That says the integration is not
decoration; it does not say the *level* is not one leg's.

WHAT MAKES THE SUSPICION CONCRETE. A free train-split decile screen run tonight
puts almost all of the cross-sectional content in one leg, and puts it exactly
where a top-quantile cut buys:

    leg          decile-10 excess return     decile-10 t     best decile
    seasonal          +10.59%/yr                +4.16             10
    illiq              +3.37%/yr                +1.68              6
    group_lead         +2.85%/yr                +0.76              3
    reversal           +1.90%/yr                +0.54              1

One leg has a top decile worth three times any other's and the only `t` above 2.
If the union book is really a `seasonal` book wearing four labels, the same-leg
book built on the union's own machinery will reproduce the union's Sharpe.

THIS CANDIDATE. `sc_same_month_seasonal_aligned`'s signal — the corrected
`MonthBegin` same-calendar-month seasonal, imported unchanged from
`strategies/lib/signal_blend.py` so it is bit-identical to the leg the union
books actually use — selected and held with the **union book's machinery** rather
than its own: core-20 / band-30 (not 25/45), warmup 60 month-ends, and the
cross-section restricted to the names all four legs can score, which is the
restriction that makes the eligible pool identical. It is not a re-run of the
recorded candidate: that book holds 28.4 names from an unrestricted pool, this
one holds 21.2 from the union's pool.

PREMISE AND COST, MEASURED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN:

    book                     positions   turnover
    fixed-share union (#71)     20.4       14.14x
    seasonal, matched (here)    21.2       19.60x
    seasonal, recorded          28.4       17.08x

**The one confound, stated rather than hidden, because it cannot be designed
away.** This control trades *more* than the union it is a control for — 19.60x
against 14.14x, worth ~0.82%/yr or ~0.05 Sharpe at 15 bps. That gap is not an
implementation choice: it is the 1/N churn damping across disagreeing legs that
`learnings.md` records ("do not reason about a book's turnover from its legs'
turnover"), i.e. it is part of the mechanism under test. Holding it fixed would
mean removing the thing being measured. So it is reported instead, per the
standing rule, and it handicaps this control by about **0.05** — a quarter of the
0.211 gap the trial is asked about, and in the direction that flatters the union.

PRE-REGISTERED, FALSIFIABLE: **0.80.** That is the recorded 0.747 nudged up for a
narrower, deeper book (21.2 names against 28.4, buying more of the one decile
worth +10.59%/yr) and down for the extra turnover. The two readings the trial
separates:
  - landing near **0.96** — the four-leg apparatus adds nothing, the family's
    headline is one leg plus machinery, and `SUMMARY.md` #63's warning that the
    edge may collapse onto a single leg is confirmed;
  - landing near **0.75-0.85** — the union is real, worth +0.11 to +0.21 gross
    and +0.06 to +0.16 after handing back the cost handicap, and the three weak
    legs earn their place by timing diversification rather than by
    cross-sectional signal.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. (n = 16; the four
`portfolio-learning` books all under-predicted, by +0.15 to +0.39.)

SCOUT, and filed under `seasonality-calendar` because that is the mechanism it
runs on — a same-calendar-month seasonal sort — not the family whose claim it
adjudicates. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sc_seasonal_matched_control",
    "family": "seasonality-calendar",
    "track": "scout",
    "hypothesis": (
        "Holding the top 20 names of the same-calendar-month seasonal score alone — the "
        "identical leg the union books of trials #68 and #71 use, imported unchanged — "
        "under those books' own machinery rather than its own (core-20/band-30 instead of "
        "25/45, warmup 60, and the cross-section restricted to the names all four legs can "
        "score, so the eligible pool is identical) scores near 0.80 on validation, "
        "materially below the fixed-share union's 0.958, because the union's margin over "
        "its legs is a real four-leg effect and not one leg plus machinery — even though "
        "the free train decile screen puts the only significant cross-sectional content in "
        "this leg (decile-10 excess +10.59%/yr at t = +4.16, against +3.37 / +2.85 / +1.90 "
        "for the other three) and even though this control is handicapped ~0.05 Sharpe by "
        "trading 19.60x against the union's 14.14x."
    ),
}

CORE_N = 20          # the union book's core, not this signal's recorded 25
BAND_N = 30          # the union book's band, not its recorded 45
WARMUP = 60          # the union book's warmup
MIN_NAMES = 20       # the union book's joint-coverage minimum per leg


def _score_from(legs: dict[str, pd.DataFrame], at: pd.Timestamp) -> pd.Series:
    """The seasonal leg's score at `at`, restricted to the names EVERY leg of the
    union book can score on that date.

    The restriction is the point of the control: a union book can only ever hold
    a name all four legs cover, so a single-leg control drawn from an
    unrestricted pool is comparing two different universes as well as two
    different constructions. The coverage test is #68's, unchanged — same legs,
    same `min_names`, same non-degenerate-spread requirement. Reads only rows at
    or before `at`.
    """
    common: pd.Index | None = None
    seasonal: pd.Series | None = None
    for key, panel in legs.items():
        sub = panel.loc[:at]
        if sub.empty:
            return pd.Series(dtype=float)
        row = sub.iloc[-1].dropna()
        if len(row) < MIN_NAMES or not row.std(ddof=0) > 0:
            return pd.Series(dtype=float)
        if key == "seasonal":
            seasonal = row
        common = row.index if common is None else common.intersection(row.index)

    if common is None or seasonal is None or len(common) < MIN_NAMES:
        return pd.Series(dtype=float)
    return seasonal.reindex(common)


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "illiq": SB.illiquidity_score(prices, aux["dollar_volume"], 63),
        "seasonal": SB.seasonal_score(prices),
        "group_lead": SB.group_lead_score(prices, 21),
        "reversal": SB.reversal_score(prices, 21),
    }

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = _score_from(legs, dt)
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
