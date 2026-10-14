"""Arbitrage risk as a standalone selection score, region-neutralised.

Hypothesis (pre-registered, see the journal entry for this trial): the 100
eligible names with the *highest unhedgeable share* of return variance against
their four most-correlated substitutes earn positive skill over the
equal-weight eligible pool, because Wurgler-Zhuravskaya's arbitrage-risk
channel says mispricing persists where a name's variance is least hedgeable.

Why this is not one of the objects this lab has already refuted. The score's
rank correlation on train, measured over 32 month-ends before this file was
written, is +0.128 to 126-day close-to-close volatility, +0.155 to 126-day
Garman-Klass volatility and +0.168 to 126-day Amihud illiquidity -- all three
of which are refuted here (low volatility: journal 2026-10-09/10; illiquidity:
2026-10-13/14). It is also distinct from plain average peer correlation, which
this session measured as a region-matched null on both sides (-5.1 / -8.7
bps/63d): the unhedgeable *share* is a variance decomposition, not a level of
comovement, and the two disagree.

Construction notes that are protocol facts rather than taste:

- Entries are quota-allocated across trailing-trading-calendar peer groups
  (`strategies/lib/calendar_peers`), so the book's geography matches the
  benchmark's rather than being chosen by the score. v3's random-selection null
  is region-matched while the skill statistic is against the whole pool, so an
  un-neutralised sort mixes a geography bet into the measurement (journal
  F3/F4, 2026-10-13). The score here is region-neutral anyway -- its whole-pool
  and region-matched readings agree at +27.5 and +27.4 bps/63d -- so the quota
  is insurance, not the signal.
- The peer groups are derived from the names eligible on the decision date
  only, never from the visible frame's column set, which is the column-axis
  leak that cost trial #4 on 2026-10-07.
- No retention band. The band is this lab's one measured construction win, but
  on *this* score it lowers both the excess and the first sub-period's sign
  (K=100: no band +27.3 bps/63d at t +2.23 and 1.35x name churn; B=200 +25.3
  at t +2.35; B=300 +16.6 at t +1.66 with 1997-2008 going negative), so it is
  declined on its own arithmetic rather than carried over by analogy.
- Pre-registered turnover, as a range with the wider split's churn in it:
  train one-way name churn is 1.35x/yr, the engine's metric counts both sides,
  and validation name churn ran 68% above train's last time this was measured,
  so 2.0-5.5x annualised is the predicted band.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
CORR_WINDOW = 250
CORR_LAG = 20
N_PEERS = 4

STRATEGY = {
    "name": "rv_arbrisk_peer_neutral",
    "family": "range-variance",
    "hypothesis": (
        "Selecting the 100 eligible names with the highest unhedgeable share of return "
        "variance against their four most-correlated substitutes (250 trading days ending "
        "20 days back), with entries quota-allocated across trailing-trading-calendar peer "
        "groups so the book's geography matches the pool's, earns positive validation skill "
        "over the equal-weight eligible pool, because Wurgler-Zhuravskaya's arbitrage-risk "
        "channel says mispricing persists where a name's variance is least hedgeable -- a "
        "quantity measured here at rank correlation +0.13/+0.16/+0.17 to the realized-vol, "
        "Garman-Klass and Amihud scores this lab has already refuted, and therefore not a "
        "restatement of any of them."
    ),
    "track": "scout",
}


def _arb_risk(returns: pd.DataFrame) -> pd.Series:
    """Unhedgeable variance share: 1 - R^2 of each column on its `N_PEERS`
    most-correlated peers, over the window `returns` already covers.

    `returns` must already be restricted to the names eligible on the decision
    date, so neither the peer set nor the correlation matrix can depend on how
    many columns the visible frame happens to carry.
    """
    frame = returns.loc[:, returns.notna().sum().to_numpy() > CORR_WINDOW * 0.8]
    if frame.shape[1] <= N_PEERS + 1:
        return pd.Series(dtype=float)
    mat = frame.fillna(0.0).to_numpy(dtype=float)
    mat = mat - mat.mean(axis=0)
    sd = mat.std(axis=0)
    keep = sd > 0
    mat, cols = mat[:, keep], frame.columns[keep]
    if mat.shape[1] <= N_PEERS + 1:
        return pd.Series(dtype=float)

    corr = np.corrcoef(mat, rowvar=False)
    np.fill_diagonal(corr, -np.inf)
    order = np.argsort(-corr, axis=1)[:, :N_PEERS]          # names x peers

    # One batched least squares per name: X_i is the name's peer block, and the
    # columns are already demeaned so no intercept is needed.
    peers = mat[:, order]                                    # days x names x peers
    gram = np.einsum("tnk,tnl->nkl", peers, peers)
    rhs = np.einsum("tnk,tn->nk", peers, mat)
    gram = gram + np.eye(N_PEERS) * 1e-12
    coef = np.linalg.solve(gram, rhs[:, :, None])[:, :, 0]
    sst = (mat ** 2).sum(axis=0)
    sse = sst - (coef * rhs).sum(axis=1)
    share = np.clip(sse, 0.0, None) / np.where(sst > 0, sst, np.nan)
    return pd.Series(share, index=cols).dropna()


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K highest arbitrage-risk names, with
    entries quota-allocated across trailing-calendar peer groups."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    rets = prices.pct_change(fill_method=None)

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for date in month_ends:
        pos = prices.index.get_loc(date)
        if pos < CORR_WINDOW + CORR_LAG:
            continue
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 50:
            continue
        window = rets.loc[:date, names].iloc[-(CORR_WINDOW + CORR_LAG):-CORR_LAG]
        score = _arb_risk(window)
        if len(score) < 50:
            continue
        groups = calendar_peers(volume, date, names)
        picked = peer_quota_select(score, groups, K)
        if len(picked) < 20:
            continue
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
