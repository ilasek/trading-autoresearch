"""Low volatility with the ASSET CLASS held to the panel's own share.

THE ONE-OPERATOR PAIR. `pt_lowvol126_quota_band` ran tonight and landed at
validation skill -0.141, at the **0th** percentile of its own null, with a
selection term of **-0.150** -- the worst on the v3 board bar two. A free
holdings-only measurement on train then found why: that book is **20.8% ETFs**
on average (26.1% after 2009) against an eligible panel that is **5.5%** ETFs.
On a panel carrying 42 ETFs the lowest-volatility instruments are ETFs, so a
volatility sort is substantially an asset-class sort, and `random_null_v3`
replaces each entered name with one of the same TYPE but -- for ETFs -- with no
matching inside the type. A fifth of that book's replicas are therefore *random*
ETFs, mostly equity ones, while the book itself bought the quietest ETFs it could
find. Its null median sits at the pool's Sharpe for that reason.

This file changes exactly one thing: the quota cells become (trailing-trading-
calendar peer group x instrument TYPE) instead of the peer group alone. Same
score, same K, same band, same monthly grid, same warm-up rule, same masking,
same everything else, byte-for-byte. So the book holds the panel's own share of
each asset class and the comparison is a true one-operator pair, which the
previous one was not and said so.

WHAT THE PAIR SETTLES. If the selection term moves materially toward zero, this
lab's low-volatility results have been measuring an uncontrolled asset-class bet
and the equity-only version of the question is still open -- which would put a
rider on the six-fold "Sharpe is flat in beta on this panel" convergence rather
than overturn it, since none of those six measurements is re-run here. If the
selection term does not move, the asset-class channel is not the explanation, the
previous book's 20.8% was incidental, and low volatility is a null on this panel
for the reason the record already gives. Both readings are results and the
hypothesis is signed for the first.

WHY READING THE INSTRUMENT TYPE IS NOT HINDSIGHT. Type is static and
survivorship-free: an ETF is an ETF on every date, and nothing about which names
later won is encoded in it. It is also the protocol's own primitive -- the
random-selection null matches on exactly this axis -- so quota'ing on it makes
the book *more* comparable to its benchmark, not less. `CLAUDE.md` permits ETF
ids outright; this reads the same fact without naming any instrument, and types
are queried only for names the book already ranks.

THE SIGN is low volatility held, carried unchanged from the previous file and not
re-derived after seeing its number.

NO TRAIN NUMBER IS OFFERED AS EVIDENCE: corr(train skill, validation skill) is
-0.08 over 27 recorded trials, so a train sheet cannot qualify a candidate.

PRE-REGISTERED TURNOVER: **0.8-2.6x** one-way per year. The previous book charged
0.9x on train and 1.8x on validation; forcing the ETF share down from ~21% to
~5% replaces a fifth of the book with stocks, whose volatility ranks are less
stable than a fund's, so the range is shifted up from that measured pair rather
than guessed. This is the only number in this file revised after a run, and it is
revised from the pair's own measured churn, not from its result.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.features import realized_vol

K = 100
BAND = 200
VOL_WINDOW = 126

STRATEGY = {
    "name": "pt_lowvol126_typequota_band",
    "family": "price-trend",
    "hypothesis": (
        "Holding the 100 eligible names with the LOWEST trailing 126-day volatility, "
        "quota-allocated across (trailing-trading-calendar peer group x instrument type) "
        "cells so that the book carries the eligible panel's own ~5% ETF share instead of "
        "the ~21% an unconstrained volatility sort takes, earns a validation SELECTION "
        "term (candidate Sharpe minus its null median) materially above the -0.150 the "
        "peer-quota-only version earned tonight, because that book's null replaced a "
        "fifth of its holdings with random same-type ETFs while it had itself bought the "
        "lowest-volatility ETFs on the panel, making its selection statistic an "
        "asset-class bet rather than a measurement of the volatility cross-section."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Low trailing volatility, quota'd across (calendar peer group x instrument type),
    monthly with a retention band. One operator away from `pt_lowvol126_quota_band`.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    # Static, survivorship-free instrument type; the protocol's null matches on it.
    kinds = data.instrument_types("pit")

    level = realized_vol(prices, VOL_WINDOW)

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        score = (-level.loc[date].reindex(names)).dropna()
        if len(score) < 60:
            # Warm-up: hold the pool rather than cash (2026-10-15/16).
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()
        cells = (groups.reindex(score.index).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in score.index],
                             index=score.index))

        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, cells.reindex(rest.index).dropna(), K - len(keep))
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
