"""Integrated score-level blending of four family-lead signals.

WHY THIS TRIAL EXISTS, AND WHY THE FAMILY IS NOT ALREADY CLOSED.
`experiments/learnings.md` closed `portfolio-learning` on 2026-08-30 without a
trial: equal-weight ensembles of the eight recorded legs' stored validation
return series, cherry-picked ex post over every subset, ran 0.834 / 0.829 /
0.819 / ... monotone *decreasing* in leg count against the best single member's
0.820, so "an allocator over these allocates over one thing".

`research/SUMMARY.md` #60 identifies the step that argument takes one wider than
its measurement supports, and this file is the test. Two objections, both
checked free before it was written:

(a) THE BOUND IS ABOUT THE WRONG OBJECT. Mixing finished *books* is bounded
    between its components by construction. The integrated build — average the
    legs' cross-sectional *scores*, then construct one long-only book in a
    single step — is not subject to that bound, because a name that is jointly
    attractive on several legs while top-decile on none is unreachable by any
    capital mix of the legs' books, and is exactly what an integrated score
    buys.

(b) THE CLOSURE'S KEY STATISTIC IS CONFOUNDED. The 0.68-0.98 correlations were
    measured on the legs' realised *return series*, i.e. on long-only books over
    one ~140-name universe that all carry the same market beta. The quantity
    that governs an integrated build is the cross-sectional correlation of the
    **signals**. Measured (2026-08-31 journal entry, holdings-only, no returns
    scored) on identical instruments and month-ends, the four legs below
    correlate at a mean |rho| of **0.054 on train and 0.070 on validation** —
    an order of magnitude below the return-series figure. The single material
    pair is group-lead against 21-day reversal at **-0.448**, which is
    mechanical: both read the same 21-day window with opposite signs, one at
    group level and one at name level. So the legs disagree in the cross-section
    almost completely, and the aggregation bound this repo keeps rediscovering —
    *the gain is bounded by the components' disagreement* — is not binding here
    on the statistic that actually governs it.

WHICH LEGS, BY A RULE STATED IN ADVANCE. One leg per `program.md` family that
has a recorded lead, taking that family's best recorded mechanism, and excluding
two on stated grounds: `statistical-learning`'s lead correlates 0.976-0.98 with
the Amihud sort (it is the same object, twice measured), and
`statistical-arbitrage`'s lead is the only recorded result *below* the 0.49
equal-weight floor. That leaves illiquidity, seasonality, group lead-lag and
short-horizon reversal. Choosing the subset by ex-post performance is exactly
the cherry-picking the closure's own arithmetic warns about, so it is not done.

EQUAL WEIGHTS, AND THAT IS LOAD-BEARING. `SUMMARY.md` #1's parameter-counting
screen forbids estimating leg weights; a ~140-name monthly cross-section cannot
fit four of them honestly, and `learnings.md` records equal leg weights as
load-bearing on the one axis where it measured them.

THE MANDATORY SCREEN #60 ATTACHES, RUN BEFORE THIS FILE WAS WRITTEN, PASSED.
The peer-reviewed rebuttal #60 cites finds that integration's apparent edge is a
low-risk tilt in disguise — averaging scores mechanically de-extremes a book —
and this repo has already refuted low-vol tilts twice. Measured holdings-only:
`spearman(integrated score, -trailing 252d vol)` is **-0.076 on train and -0.142
on validation**, i.e. the integrated score tilts mildly toward *high* volatility,
and the 20 held names sit at trailing-vol percentile **0.583 / 0.620** against
0.50 for no tilt. The tilt is the opposite sign to the one that would make this a
disguised low-vol book, so the rebuttal's mechanism is ruled out here rather than
assumed away.

TURNOVER IS MATCHED BY DESIGN, NOT ARGUED CLEAN AFTERWARDS. `learnings.md`
records from four consecutive trials that outside `price-trend` a turnover
difference swamps every mechanism comparison. The core-20 / band-30 equal-weight
monthly construction is copied unchanged from `lv_amihud_illiquidity_tilt`,
`pt_raw_reversal_control` and `lv_trading_time_reversal`, which ran 1.0x, 17.6x
and 16.7x; the integrated selection was measured holdings-only at ~13.9x (train)
and ~17.8x (validation) annual *before* the band, so it sits inside the range its
comparators occupy and the comparison is not a broker measurement.

PRE-REGISTERED, FALSIFIABLE. The four legs scored validation 0.681 (illiq),
0.747 (seasonal), 0.688 (group-lead) and 0.701 (reversal). The claim is that the
integrated book beats the best of them, **0.747**. Landing at or below 0.747
falsifies it and closes `portfolio-learning` a second time on the statistic
#60 says the first closure should have used — which is a real result, not a
failure, because it would mean near-zero signal correlation is *not* sufficient
and the long-only constraint is what binds.

SECOND PRE-REGISTRATION, per the 2026-08-30 session's standing instruction that
every scout record its train Sharpe as a prediction of its validation Sharpe, so
the n=11 train/validation-disagreement sample grows: whatever train Sharpe this
book records is hereby the prediction for its validation Sharpe.

THREE DISCOUNTS CARRIED FROM THE SOURCE, none imported as an expectation.
Integration's gain goes to zero as signal correlation goes to +1 (not binding
here) and as active risk goes to zero; breadth enters directly and a ~140-name
cross-section holds few of the jointly-attractive names integration exists to
find; and the solved required-leg-Sharpe bar (1.34-1.42 against a 1.120
champion) is a separate constraint that none of this relaxes — so this is a
scout, it does not compete for the seat, and it will not reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_integrated_signal_blend",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Averaging the cross-sectional z-scores of four family-lead signals — Amihud "
        "illiquidity, same-calendar-month seasonality, sector-group 21-day lead-lag and "
        "21-day name-level reversal, equal-weighted because the parameter-counting "
        "screen forbids estimating leg weights — and constructing ONE long-only "
        "hold-30/enter-20 equal-weight monthly book from the averaged score scores a "
        "validation Sharpe above the best single leg's 0.747, because the aggregation "
        "bound that closed this family was measured on the legs' realised return series "
        "(rho 0.68-0.98, dominated by a common long-only market component) while the "
        "quantity governing an integrated build is the cross-sectional correlation of "
        "the signals themselves, measured here at a mean |rho| of 0.054 on train and "
        "0.070 on validation."
    ),
}

CORE_N = 20
BAND_N = 30
WARMUP = 60          # month-ends skipped; the seasonal leg needs the history


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
        score = SB.integrate(legs, dt)
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        # Hysteresis on membership, identical to the three comparator books.
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
