"""Peer groups recovered from the trailing trading calendar.

Why this exists. Protocol v3's random-selection null is **region-matched**: a
replacement for a stock is drawn from the same listing region. The skill
statistic, by contrast, is measured against the *whole* equal-weight eligible
pool. So a score that happens to correlate with listing region produces a book
whose apparent excess over the pool is a region and FX bet, and the null is the
only gate that can see it. Neutralising the region axis inside a candidate is
therefore not a refinement: it is the difference between a selection claim and a
geography claim.

A candidate cannot read the region table -- `engine.data.instrument_regions` is
engine state, and the membership files are refused outright by the hindsight
guard. It can, however, recover the axis from the panel it is handed: `volume`
is not forward-filled, so the days on which a name has no print are the days its
*listing market* was shut. That pattern is a holiday calendar, and a holiday
calendar is very nearly a country.

Measured on the train split (journal F6/F7, 2026-10-13): grouping the eligible
names this way gives 1 group in 2005 (only the S&P 500 is eligible then), 7 in
2012 and 7 in 2017, at a name-weighted purity against the true listing region of
0.960 / 0.937 / 0.946. It collapses the European markets into a few clusters
rather than resolving all 19 regions, which is enough for the axis that matters
here (US vs Europe vs Japan vs Hong Kong).

Causality note, and it is the reason the signature takes `names`. The anchor set
is derived from the patterns of the names passed in, so passing the *whole*
visible frame would make the grouping depend on how many columns the frame has
-- and `protocol.visible_frame` deliberately drops columns that have not been
eligible yet, so that count differs between the truncated and untruncated runs.
That is the column-axis leak `experiments/learnings.md` (2026-10-07) records as
having cost a trial. **Pass only the names eligible on the decision date.**
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def calendar_peers(
    volume: pd.DataFrame,
    date: pd.Timestamp,
    names,
    lookback: int = 252,
    min_anchor: int = 15,
    min_prints: int = 40,
) -> pd.Series:
    """Label each of `names` with a trailing-trading-calendar peer group.

    `volume` is the raw (not forward-filled) share-volume panel; a NaN means the
    name had no print that day. Only rows at or before `date` are read. The
    exact non-print patterns held by at least `min_anchor` names become anchors,
    and every remaining name joins the anchor whose pattern it agrees with on
    the most days. Deterministic, and independent of the frame's column count.

    Returns a Series of opaque group labels indexed by name (names with fewer
    than `min_prints` prints in the window are dropped).
    """
    names = pd.Index(names)
    have = volume.columns.intersection(names)
    if not len(have):
        return pd.Series(dtype=object)
    window = volume.loc[:date, have].iloc[-lookback:]
    present = window.notna()
    present = present.loc[:, present.sum(axis=0).to_numpy() > min_prints]
    if not present.shape[1]:
        return pd.Series(dtype=object)

    pattern = present.T.to_numpy()                       # names x days, bool
    keys = pd.Series([hash(row.tobytes()) for row in pattern], index=present.columns)
    counts = keys.value_counts()
    anchor_keys = counts[counts >= min_anchor].index
    if not len(anchor_keys):
        anchor_keys = counts.index[:1]
    anchors = np.stack([pattern[(keys == k).to_numpy()][0] for k in anchor_keys])

    pos, neg = pattern.astype(np.int16), (~pattern).astype(np.int16)
    agreement = pos @ anchors.astype(np.int16).T + neg @ (~anchors).astype(np.int16).T
    return pd.Series(np.asarray(anchor_keys)[agreement.argmax(axis=1)], index=present.columns)


def peer_quota_select(score: pd.Series, groups: pd.Series, k: int) -> pd.Index:
    """The `k` highest scores, allotted across `groups` in proportion to each
    group's share of the scored names.

    This is what makes the book's geography match the benchmark's instead of
    being chosen by the score. Quotas are rounded, so the selection can come
    out a name or two away from `k`; the caller equal-weights whatever it gets.
    """
    score = score.dropna()
    groups = groups.reindex(score.index).dropna()
    score = score.reindex(groups.index)
    if score.empty:
        return pd.Index([])
    quota = (groups.value_counts() / len(groups) * k).round().astype(int)
    picked: list = []
    for group, n in quota.items():
        if n < 1:
            continue
        in_group = score[(groups == group).to_numpy()]
        picked.extend(in_group.nlargest(int(n)).index)
    return pd.Index(picked)
