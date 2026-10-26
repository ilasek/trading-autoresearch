"""Paired validation control for trial #14: the same exclusion at the WRONG PHASE.

WHAT THIS EXISTS TO SEPARATE. Trial #14 drops the five lags of months -120..-61 that
share the calendar month the book is about to hold, and scored validation skill
**+0.021** against trial #12's +0.070 for the same window undropped. So the exclusion
operator cost 0.049 of validation skill. Two readings of that are still open and they
have opposite consequences:

  (a) **The operator costs and the phase is irrelevant.** A 12-periodic exclusion set
      shifts phase every month, so 12 of 55 months change status per step against 2 of
      60 for a plain rolling mean; that raises churn 2.40x -> 4.29x on train and 3.4x ->
      6.4x on validation, and the cost is the whole story. Under this reading the
      twelve-phase train permutation (#14's F5: phase 0 first of twelve, z +3.50 on
      selection) carried no information about validation whatsoever.

  (b) **The operator costs MORE than 0.049 and the phase recovers part of it.** Under
      this reading the anniversary content is real out of sample and the right lesson
      is that it is worth less than the churn it buys.

Only a wrong-phase control separates them, and it has to be paired: identical window,
identical availability rule, identical K, identical peer-group x depth-tercile quota,
identical warm-up operator, identical five-of-sixty exclusion structure. The ONLY
difference between this file and `pt_old_half_ex_anniversary.py` is `PHASE`.

THE CONTROL PHASE WAS CHOSEN STRUCTURALLY, NOT BY ITS TRAIN NUMBER. Phase +6 is the
antipode — six months opposite the anniversary on the calendar — which is the control
a reader would name before seeing any table. It is also, as it happens, the weakest of
the eleven placebos on train (net -0.015, 2009-2017 -0.158, both last of twelve), and
that coincidence is recorded here rather than relied on.

PRE-REGISTERED DIRECTION, written before this was run. Validation skill **below** trial
#14's +0.021. On train the gap is 0.061 of selection (+0.027 against +0.088) and 0.190
of the 2009-2017 sub-period (-0.158 against +0.032) at the same 4.28x churn and the
same -0.042 cost. **If this control instead ties or beats #14, then the twelve-phase
permutation is a train-only object and the calendar phase carries nothing out of
sample** — which is the alternative this file exists to expose, and would be the eighth
instance in a row of a clean train screen failing to qualify anything.

Train figures for this exact book, through `protocol.evaluate_split(..., "train",
setup=setup_v3)`: net skill **-0.015**, selection +0.027, cost -0.042, turnover 4.28x,
volatility ratio 0.989, 1997-2008 +0.058, 2009-2017 -0.158. It fails
`min_train_skill = 0.0`, so a GATE_FAIL on the train gate is expected and is not
informative; the validation skill and the null percentile are what this trial is for.

PRE-REGISTERED TURNOVER: 4.0-7.5x, the same band as #14, which charged 6.4x.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
LO, HI = 61, 120      # the old half of the decade window, in months back
PHASE = 5             # k % 12 == 5 is the ANTIPODE of the anniversary phase (11)
MIN_MONTHS = 44       # of the 55 kept
DEPTH_BINS = 3

KEPT_LAGS = [k for k in range(LO, HI + 1) if k % 12 != PHASE]

STRATEGY = {
    "name": "pt_old_half_ex_phase6_control",
    "family": "price-trend",
    "hypothesis": (
        "Replacing trial #14's excluded calendar phase with its antipode -- dropping the "
        "five lags of months -120..-61 that sit six months opposite the holding month's "
        "calendar month, and leaving every other node of that candidate byte-identical -- "
        "scores validation skill BELOW #14's +0.021, because the exclusion operator is "
        "held fixed by construction (same five-of-sixty structure, same 4.3x train churn, "
        "same -0.042 cost) so only the calendar phase differs, and on train this phase is "
        "last of all twelve on net skill (-0.015 against +0.046) and on the 2009-2017 "
        "sub-period (-0.158 against +0.032); if it does not, the twelve-phase train "
        "permutation that motivated #14 carries no information about validation and the "
        "anniversary phase is a train-only object."
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
    """Monthly, equal-weight over the K lowest phase-6-excluded old-half means,
    quota-allocated across peer-group x depth-tercile cells. Byte-identical to
    `pt_old_half_ex_anniversary.generate_weights` apart from `PHASE`."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)

    score = (-_lagged_mean(mret)).reindex(prices.index, method="ffill")
    depth = mret.notna().cumsum().reindex(prices.index, method="ffill")

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 50:
            continue
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < 50:
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
