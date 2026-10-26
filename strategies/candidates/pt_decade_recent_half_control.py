"""The paired control for trial #12: the identical construction carrying the window
the screen says is a null.

WHY THIS TRIAL EXISTS. Trial #12 (`pt_decade_old_half_depth_neutral`) is the first v3
trial with positive validation skill (+0.070) and the first to clear the
random-selection null gate (97th percentile against a 90% bar). Three things changed at
once relative to the two trials that traded the same mechanism before it: the score was
cut back to the OLD half of the ten-year window, the entry quota gained a
price-history-depth axis, and the availability rule got stricter (48 of the 60 months
from ten to five years back, so a name needs about nine years of history). Any one of
them could be carrying the result, and no amount of further train measurement can tell
them apart -- `learnings.md` has five instances of train skill carrying no usable
information about validation, this trial's own train skill (+0.026) being the latest.

So: hold every node of trial #12 byte-identical and change the score to the window the
free screen pre-signs as a NULL -- the RECENT half, months -60 to -1, whose train
selection measured +0.012 against the old half's +0.135 (journal F2, 2026-10-26/27).
The recent-half score is masked to exactly the old half's scorable set, so the two books
run the identical schedule over the identical name universe and differ by the score and
nothing else.

PRE-REGISTERED PREDICTION, stated before the run. Validation skill near zero and below
trial #12's +0.070, and a null percentile below its 97%. If instead this control scores
about what trial #12 scored, then the old/recent decomposition is NOT what pays and the
depth-neutral quota or the stricter availability rule is -- which would be the larger
finding of the two and would redirect the next session. Train skill may fail the
`min_train_skill` gate; the validation reading is recorded either way, which is the
point of running it.

Pre-registered turnover: trial #12 charged 2.4x on train and 3.4x on validation against
a 2.5-4.0x pre-registration. A faster score on the same schedule should sit at or above
that, so 3.0-5.0x is the predicted validation band.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
SPAN = 60
MIN_MONTHS = 48
REF_LAG = 60      # the old half's lag, used only to reproduce its availability rule
DEPTH_BINS = 3

STRATEGY = {
    "name": "pt_decade_recent_half_control",
    "family": "price-trend",
    "hypothesis": (
        "Replacing trial #12's score with the RECENT half of the ten-year window (the mean "
        "monthly return of months -60 to -1), masked to trial #12's own scorable set and "
        "leaving every other node of that candidate byte-identical, scores validation skill "
        "near zero and below trial #12's +0.070, because the recent half's train selection "
        "term is +0.012 against the old half's +0.135 -- and if it does not, then trial #12's "
        "result is the depth-neutral quota or the nine-year availability rule rather than the "
        "old/recent decomposition, which is the alternative this control exists to expose."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K lowest mean monthly returns of months -60..-1,
    on trial #12's schedule, name universe and peer-group x depth-tercile quota."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)

    recent = mret.rolling(SPAN, min_periods=MIN_MONTHS).mean()
    # The old half's availability rule, reused verbatim so the two books share a schedule
    # and a name universe and differ only in which window the score is taken over.
    old = mret.shift(REF_LAG).rolling(SPAN, min_periods=MIN_MONTHS).mean()
    score = (-recent.where(old.notna())).reindex(prices.index, method="ffill")

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
