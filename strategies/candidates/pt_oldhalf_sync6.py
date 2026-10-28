"""The paired control for `pt_oldhalf_overlap6`: the same names, rebalanced.

WHY THIS FILE EXISTS. `pt_oldhalf_overlap6` changes two things about trial #12
at once, and tonight's train decomposition says they are not the same size:

    book                        gross    cost     net     turn    pos   97-08   09-17
    hold-1  (= trial #12)      +0.045  -0.019  +0.026    2.36   140.4  +0.051  -0.020
    sync/H6   (THIS FILE)      +0.055  -0.007  +0.048    1.44   164.4  +0.057  +0.030
    overlap/H6                 +0.063  -0.005  +0.058    1.30   164.4  +0.062  +0.053

SYNC holds exactly the names the overlapping book holds -- the union of the six
most recent monthly top-100 picks, each leg weighted 1/(6*K) -- but re-forms all
six legs at every month-end, so the drift is undone every month and the whole
book trades. OVERLAP reforms one leg and lets the other five drift.

  OVERLAP minus SYNC isolates the DRIFT channel (+0.010 on train).
  SYNC minus trial #12 isolates the WEIGHT-SMOOTHING channel (+0.022 on train):
  averaging six lagged picks makes a name enter at 1/600 and grow to 6/600 over
  six months instead of jumping to 1/100, which cuts boundary churn from 2.36x
  to 1.44x WITHOUT deferring any trade. That matters because the only
  churn-cutting operator this lab had was a retention band, and the 2026-10-25/26
  paired trial closed the band as a validation operator on this very mechanism
  (+0.080 of train skill for -0.049 of validation skill). Smoothing is not
  deferral: it changes what the target vector is, not when it is reached.

WHAT THIS PAIR CAN AND CANNOT RESOLVE. Trial #12 is already on validation at
skill +0.070, so the three books form a ladder on the same split with one node
changing between each rung. The lab's resolution floor is 0.03-0.08 of Sharpe,
so SYNC minus #12 (+0.022 on train) sits at its bottom edge and OVERLAP minus
SYNC (+0.010) sits below it: **this pair is pre-registered as a test of the
operator's SIGN, not of the decomposition's magnitudes.** It is shipped together
with its partner rather than after seeing its partner's validation number, so
neither file was designed on the other's result.

AND IT IS THE FIRST TEST OF AN ARITHMETIC CHANNEL. Every operator this lab has
taken to validation was argued from a train selection number, and
`corr(train skill, validation skill)` across fifteen v3 trials is -0.074. The
cost half of this pair is different in kind: fewer trading events cost less
money by arithmetic, not by a property of 2018-2023 that might not hold. If both
rungs still come in below trial #12, the finding is that a cost-channel argument
fails to transfer too -- which would be the more valuable of the two outcomes
and is the reason the control is worth a trial.

THE OPERATOR'S NULL SAYS THE CHANNEL IS MECHANICAL, WHICH IS THE POINT. Six
random AR(1) scores at the real score's own rank persistence (phi = 0.9803),
masked to its scorable set, gain **+0.0167** of net skill (sd 0.0153) from the
overlapping rule alone — against this mechanism's +0.032. So the delta is z +1.0
against its own null: the operator is cost arithmetic, not a discovery about the
score. The LEVEL is a different matter — +0.058 against a null overlap mean of
-0.0210 at sd 0.0151 is z +5.2. Both rungs of this ladder therefore test the
same single question: **does a gain whose source is arithmetic transfer, where
every selection-argued operator this lab has shipped has not?**

PRE-REGISTERED SHIPPING RULE FOR THIS FILE, written before its partner ran: ship
it if and only if `pt_oldhalf_overlap6`'s validation skill moves more than
0.010 (the smaller of the two channels' train deltas) away from trial #12's
+0.070. If the operator leaves validation skill inside +/-0.010 of #12 it is a
validation null and the decomposition has nothing to decompose, so the trial is
not bought. Recorded in the journal's free-measurement block before either trial
ran so that neither file was designed on the other's result.

TONIGHT'S FREE SCREENS: journal F1-F7 of 2026-10-27/28, train 1997-2017 only,
through `protocol.evaluate_split` with the v3 execution model. The sheet above is
this file's own row (F4). No validation, holdout, forward or incubation number
was read.

PRE-REGISTERED TURNOVER: train 1.44x, and this mechanism's validation churn has
run 29-49% above train, so **1.7-2.4x** is the predicted band.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
LAG = 60          # months skipped before the score window starts
SPAN = 60         # length of the score window, in months
MIN_MONTHS = 48   # of SPAN
DEPTH_BINS = 3
LEGS = 6          # the six most recent monthly picks, averaged

STRATEGY = {
    "name": "pt_oldhalf_sync6",
    "family": "price-trend",
    "hypothesis": (
        "Equal-weighting the union of the six most recent monthly top-100 picks of the "
        "old-half reversal score -- each leg 1/(6*100), re-formed in full at every "
        "month-end -- earns higher validation skill than trial #12's single-leg version "
        "of the identical score, quota and K, because averaging six lagged picks smooths "
        "the target weight vector (a name enters at 1/600 and grows to 6/600 rather than "
        "jumping to 1/100) and that alone cuts engine-counted churn from 2.36x to 1.44x "
        "and the cost term from -0.019 to -0.007 while deferring no trade, which is a "
        "different operator from the retention band the 2026-10-25/26 paired trial "
        "refused; shipped as the control that separates this smoothing channel from the "
        "drift channel in `pt_oldhalf_overlap6`."
    ),
    "track": "scout",
}


def _picker(prices, aux, elig):
    """The top-K peer/depth-quota pick of the old-half reversal score, memoised
    per month-end so the six legs cost one pass rather than six."""
    volume = aux["volume"]
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    old = mret.shift(LAG).rolling(SPAN, min_periods=MIN_MONTHS).mean()
    score = (-old).reindex(prices.index, method="ffill")
    depth = mret.notna().cumsum().reindex(prices.index, method="ffill")
    memo: dict = {}

    def pick(date):
        if date in memo:
            return memo[date]
        out = None
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) >= 50:
            # Mask to the eligible names BEFORE anything cross-sectional is taken.
            sc = score.loc[date].reindex(names).dropna()
            if len(sc) >= 50:
                groups = calendar_peers(volume, date, sc.index).dropna()
                if len(groups) >= 50:
                    sc = sc.reindex(groups.index)
                    dep = depth.loc[date].reindex(groups.index)
                    try:
                        bins = pd.qcut(dep.rank(method="first"), DEPTH_BINS, labels=False)
                    except ValueError:
                        bins = pd.Series(0, index=dep.index)
                    cells = groups.astype(str) + "|" + bins.astype(str)
                    cand = peer_quota_select(sc, cells, K)
                    if len(cand) >= 20:
                        out = cand
        memo[date] = out
        return out

    return pick


def generate_weights(prices, aux, eligible=None):
    """Monthly. Equal weight over the union of the six most recent monthly picks,
    each leg carrying 1/LEGS of the book; every leg re-formed each month."""
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    pick = _picker(prices, aux, elig)

    month_ends = list(prices.groupby(pd.Grouper(freq="ME")).tail(1).index)
    rows = {}
    for i, date in enumerate(month_ends):
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 50:
            continue
        legs = [pick(month_ends[i - j]) for j in range(LEGS) if i - j >= 0]
        legs = [leg for leg in legs if leg is not None]
        if not legs:
            # Warm-up: hold the pool rather than cash (operator of 2026-10-15/16).
            rows[date] = pd.Series(1.0 / len(names), index=names)
            continue
        w = pd.Series(0.0, index=prices.columns, dtype=float)
        for leg in legs:
            w = w.add(pd.Series(1.0 / (len(legs) * len(leg)), index=leg)
                      .reindex(prices.columns).fillna(0.0), fill_value=0.0)
        rows[date] = w[w > 1e-12]

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
