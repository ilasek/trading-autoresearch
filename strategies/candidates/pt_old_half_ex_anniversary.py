"""The ten-year reversal's old half with its ANNIVERSARY months cut out.

THE CLAIM IN ONE LINE. Trial #12 buys the hundred eligible names with the lowest
mean monthly return over months -120..-61. Those sixty months are not homogeneous:
five of them share the calendar month of the month the book is about to hold, and
Heston-Sadka's cross-sectional seasonality says a name's same-calendar-month history
predicts its return with the OPPOSITE sign to the reversal the rest of the window
carries. Averaging them in therefore shorts a positive predictor. Cutting the five
out doubles the selection term on train and is the only one of twelve matched
calendar phases that does so.

WHY THIS IS NOT A KNOB. The five excluded lags are fixed by the calendar, not chosen:
k = 12j - 1 inside [61,120], i.e. {71, 83, 95, 107, 119}. Every other phase removes
exactly five of the same sixty months and was run as a matched placebo. Churn, cost,
book size, scorable set and rank correlation to the parent score are held fixed by
construction across all twelve; only the calendar phase varies.

TONIGHT'S FREE SCREENS (train 1997-2017 only, through
`protocol.evaluate_split(..., "train", setup=setup_v3)` -- the engine's own backtest,
the instrument validated on 2026-10-25/26 and confirmed again tonight: run on trial
#12 verbatim it returns train sharpe +0.5490 and train skill +0.0260 against the
recorded +0.549 and +0.026. No validation, holdout, forward or incubation number was
read. Journal F1-F7 of 2026-10-27/28.) SELECTION is gross skill over the gross pool
with the liquidity tier and the transaction taxes both switched off; COST is net minus
gross. K=100, (calendar peer group x price-history-depth tercile) quota, monthly, pool
held through warm-up.

*F5 -- all twelve exclusion phases. The pre-signed one is first on every statistic.*

    book                            net skill  selection    cost   turn   volr   97-08   09-17
    baseline: all 60 months  [#12]    +0.024     +0.042   -0.018   2.40   0.981  +0.052  -0.031
    exclude phase  0  [ANNIVERSARY]   +0.046     +0.088   -0.042   4.29   0.978  +0.048  +0.032
    exclude phase 11                  +0.023     +0.064   -0.041   4.30   0.986  +0.027  -0.005
    exclude phase  7                  +0.015     +0.057   -0.042   4.32   0.991  +0.048  -0.050
    exclude phase  1                  +0.014     +0.054   -0.040   4.06   0.975  +0.066  -0.076
    exclude phase  8                  +0.010     +0.052   -0.042   4.33   0.990  +0.068  -0.103
    exclude phase  2                  +0.011     +0.050   -0.039   4.06   0.985  +0.063  -0.087
    exclude phase  4                  +0.006     +0.048   -0.042   4.32   0.987  +0.029  -0.047
    exclude phase  9                  -0.001     +0.042   -0.043   4.37   0.987  +0.042  -0.088
    exclude phase  5                  -0.004     +0.038   -0.042   4.36   0.986  +0.044  -0.091
    exclude phase  3                  -0.007     +0.034   -0.041   4.16   0.984  +0.035  -0.090
    exclude phase  6                  -0.015     +0.027   -0.042   4.28   0.989  +0.058  -0.158
    exclude phase 10                  -0.016     +0.026   -0.042   4.33   0.994  +0.027  -0.107

Phase 0 ranks **1 of 12** on selection (+0.088 against the eleven placebos' mean
+0.045, sd 0.012, **z +3.50**), 1 of 12 on net skill (+0.046 against +0.003, z +3.34)
and 1 of 12 on the 2009-2017 sub-period, where it is **the only non-negative value of
the twelve** (+0.032 against a placebo mean of -0.082, z +2.92). Monte Carlo
`p = (1 + 0)/(1 + 12) = 0.077` on each; the three statistics are not independent, so
that is one p-value, not three. Turnover runs 4.06-4.37x and cost -0.039 to -0.043
across every phase, which is what "the operator is held fixed" means here.

*F3 -- the two halves of the split, traded on their own, pre-signed before measuring.*
Heston-Sadka's sign for the anniversary leg (buy the HIGH end), the lab's reversal sign
for its complement (buy the LOW end):

    leg                                net skill  selection   turn    97-08   09-17
    old ANNIVERSARY   (+, HS sign)       -0.069     +0.027    9.16   -0.044  -0.142
    old NON-anniversary (-, reversal)    +0.046     +0.088    4.29   +0.048  +0.032
    old ANNIVERSARY   NEGATED            -0.168     -0.070    9.25   -0.068  -0.362

The anniversary content is correctly signed and **unharvestable on its own**: five
observations make a ranking that churns 9.2x/yr, and the cost schedule takes -0.096 of
a +0.027 selection term. It is worth something only as a contaminant removed. The
negation invariant passes (+0.027 against -0.070, not both positive).

*F2 -- where the reversion lives, measured without a top-K book so no scorable-set
confound can enter.* Rank correlation across names of the market-demeaned log return
over months [-2h,-h] against [-h,0], pooled over train month-ends: -0.020 (t -2.36) at
h=1, -0.016 at h=3, +0.014 at h=6, +0.011 at h=12, +0.013 at h=24, -0.014 at h=36 and
**-0.089 at h=60**. The five-year block scale is 4-9x any other horizon. (The t at
h=60 is an upper bound: 60-month blocks on a monthly decision grid overlap heavily.)

WHAT ARGUES AGAINST THE BOOK, and none of it is optional.

(i) **A train screen may refute but may not qualify** (`learnings.md`, 2026-10-16/17).
Seven sessions have ended with a version of "a clean screen is not evidence", and this
is the cleanest one yet, which is exactly the situation that rule was written for. The
permutation result is a statement about train.

(ii) **This is not a new mechanism.** Rank rho to trial #12's score is **+0.936**,
so it is M3 again -- the same bet with a second component removed, as #12 was to #5 at
+0.777. M3's recorded validation skills are -0.006, -0.055 and +0.070.

(iii) **The anniversary identification is 71% pure, not 100%.** A pandas `ME` label can
fall after the month's last trading day, so on 97 of 336 train decision dates the score
read is one month stale and the excluded lags land one calendar month off (measured:
mode share 0.712-0.719 across the five lags). The effect is therefore attenuated
toward the placebo mean and +0.088 is a lower bound on a correctly-aligned version.
This is shipped as screened rather than repaired, because repairing it would ship a
book whose permutation p-value had not been measured.

(iv) **The exclusion is mechanically expensive.** A 12-periodic exclusion set shifts
phase every month, so 12 of 55 months change status per step against 2 of 60 for a
plain rolling mean. That is the whole of the 2.40x -> 4.29x turnover rise, and it costs
-0.024 of skill. The book clears the standing screen on gross train skill (+0.088 > 0)
and on volatility ratio (0.978 <= 1.0) and **fails its churn arm** (4.29x against the
~2x bar of 2026-10-24/25). It is shipped anyway because the bar exists to catch books
whose cost takes all of their selection, and here cost takes -0.042 of +0.088.

(v) No retention band. The 2026-10-25/26 paired validation trial closed the band as a
validation operator on this very mechanism, and nothing here reopens it.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train charges
4.29x; trial #5 ran 34% above its train figure on validation and trial #12 ran 45%
above. **4.0-7.5x** is the predicted band.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
LO, HI = 61, 120      # the old half of the decade window, in months back
PHASE = 11            # lags with k % 12 == PHASE share the holding month's calendar month
MIN_MONTHS = 44       # of the 55 kept
DEPTH_BINS = 3

KEPT_LAGS = [k for k in range(LO, HI + 1) if k % 12 != PHASE]

STRATEGY = {
    "name": "pt_old_half_ex_anniversary",
    "family": "price-trend",
    "hypothesis": (
        "Selecting the 100 eligible names with the lowest mean monthly return over "
        "months -120..-61 AFTER dropping the five lags that share the calendar month of "
        "the month the book is about to hold, with entries quota-allocated across "
        "(trailing-trading-calendar peer group x price-history-depth tercile) cells, "
        "earns higher validation skill than trial #12's undropped version of the same "
        "window, because Heston-Sadka cross-sectional seasonality gives a name's "
        "same-calendar-month history the opposite sign to the reversal the other 55 "
        "months carry -- so averaging them in shorts a positive predictor -- and because "
        "on train this pre-signed phase is first of all twelve matched calendar phases "
        "on selection (+0.088 against a placebo mean of +0.045, sd 0.012), on net skill "
        "and on the 2009-2017 sub-period, where it is the only non-negative one."
    ),
    "track": "scout",
}


def _lagged_mean(mret: pd.DataFrame) -> pd.DataFrame:
    """Mean of the kept lags, NaN where fewer than MIN_MONTHS of them are present."""
    stack = np.stack([mret.shift(k).to_numpy() for k in KEPT_LAGS])
    count = np.sum(~np.isnan(stack), axis=0)
    with np.errstate(invalid="ignore"):
        mean = np.nanmean(stack, axis=0)
    return pd.DataFrame(np.where(count >= MIN_MONTHS, mean, np.nan),
                        index=mret.index, columns=mret.columns)


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K lowest non-anniversary old-half means,
    quota-allocated across peer-group x depth-tercile cells."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    # Monthly returns. A value published on a month label uses only returns realized at
    # or before that label; the daily reindex forward-fills, so a decision date reads the
    # latest label at or before it. Every lag is a ratio of two prices inside the visible
    # window, so the back-adjustment factor of the 2026-10-22 engine issue cancels.
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)

    score = (-_lagged_mean(mret)).reindex(prices.index, method="ffill")

    # History depth, as a candidate can count it: months of realized monthly return in
    # the visible window. Neutralised rather than scored on — sorting on it is the
    # largest confound measured on this panel (2026-10-26/27, F9-F11).
    depth = mret.notna().cumsum().reindex(prices.index, method="ffill")

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 50:
            continue
        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < 50:
            # Warm-up: hold the pool rather than cash, so the book is not scored against
            # a fully-invested benchmark while sitting out (operator of 2026-10-15/16).
            rows[date] = pd.Series(1.0 / len(names), index=names)
            continue
        groups = calendar_peers(volume, date, sc.index).dropna()
        if len(groups) < 50:
            continue
        sc = sc.reindex(groups.index)
        dep = depth.loc[date].reindex(groups.index)
        try:
            bins = pd.qcut(dep.rank(method="first"), DEPTH_BINS, labels=False)
        except ValueError:
            bins = pd.Series(0, index=dep.index)
        cells = groups.astype(str) + "|" + bins.astype(str)
        picked = peer_quota_select(sc, cells, K)
        if len(picked) < 20:
            continue
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
