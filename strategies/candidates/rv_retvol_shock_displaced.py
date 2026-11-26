"""THE THIRD CHANNEL, DISPLACED ARM -- the control that separates baseline PURITY from a
cross-sectional STABILITY CHARACTERISTIC on a third data channel.

THE TWO READINGS THIS ARM SEPARATES. The in-window arm drops the names whose 50-row scoring
window contains the largest jumps. Two different things could explain any gain:
 (a) BASELINE PURITY -- a "recent minus baseline" score whose baseline contains a
     discontinuity measures a decaying baseline rather than a fresh event, so the defect is
     about the jump's POSITION inside the score's own window; or
 (b) a STABILITY CHARACTERISTIC -- jumpy names simply earn less, in which case the same
     criterion read ANYWHERE recent would pay the same.
Reading the identical criterion over days -100..-51 -- the 50 rows immediately BEFORE the
window the score reads -- is (b) with (a) removed. The recorded result on two channels:

    channel  in-window arm   displaced arm   no-filter arm   purity term   characteristic
    volume    +0.211 (#32)    +0.101 (#41)    +0.066 (#40)      +0.110        +0.035
    range     +0.119 (#42)    -0.009 (#43)    +0.010 (#38)      +0.109        -0.019

So the volume channel split about 76/24 purity-to-characteristic and the range channel 100/0.

THE MATCHING, measured free before this file was written, against the in-window arm:

    quantity                     in-window arm   THIS FILE   range-channel analogue
    scorable names kept              50.1%         50.1%        50.0% / 49.8%
    rank persistence phi            -0.014        -0.010       -0.007 / -0.012
    exit200                          38.5%         38.4%
    predicted train churn            12.2x         12.1x         7.4x / 7.4x
    ETF share of holdings            14.5%         14.2%         not measured
    top-100 Jaccard, the two arms            0.436              0.434

Matched to 0.0pp on exclusion rate, 0.004 on persistence, 0.1x on predicted churn and 0.3pp on
ETF share, while sharing only 44% of their holdings -- so the STRONG form of the
characteristic reading is the one under test, not a weaker version of it, and the ETF rider
that applies to the bare-versus-filtered contrast does not apply to this one.

PRE-REGISTERED PREDICTIONS, written before the run.
 - GROSS skill relative to the BARE arm: **+0.00 to +0.05**, reproducing the +0.035 and -0.019
   the two recorded channels gave. A reading at or above the in-window arm's would instead say
   the return channel's whole term is a jump-stability characteristic and that the three
   channels are not one mechanism.
 - NET skill: negative, -0.10 to -0.22.
 - NULL PERCENTILE: 55-90%, below the in-window arm's, by the 2026-11-25 monotone calibration.
 - CHURN: train 9-15x, validation 13-28x (predictor 12.1x).
 - The purity term reported for this channel is THIS ARM differenced against the in-window
   one, not against the bare one: the bare arm differs in exclusion rate, persistence and ETF
   share, and only these two arms are matched on all three.

WHAT ARGUES AGAINST THE BOOK.
 (i) `|r|` has essentially no persistence (phi -0.014), so the jump statistic read over
     -100..-51 carries little information about the jump statistic read over -50..-1. That
     makes this a CLEANER control for the position effect than the other two channels'
     displaced arms, and simultaneously a WEAKER test of (b): if jumpiness itself is not
     persistent, the characteristic reading has little to work with on this channel and a
     near-zero reading here is less informative than the range channel's was. This limit is
     stated rather than fixed; it is a property of the channel, not of the design.
 (ii) It is the third arm of a three-trial block in one family on one night. The justification
     is that the purity term is a DIFFERENCE and cannot be read without both controls; the
     night's breadth is carried by its other families.
 (iii) Same fast-book cost corner as its two siblings: net skill cannot be competitive and
     this is a scout measuring a construction rule, not a candidate for the seat.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5
SLOW = 45
WINDOW = FAST + SLOW
DISPLACE = WINDOW        # the jump statistic reads rows -100..-51

STRATEGY = {
    "name": "rv_retvol_shock_displaced",
    "family": "range-variance",
    "hypothesis": (
        "Displacing the 5/45 close-to-close return shock's median-jump exclusion from the "
        "50-row scoring window to the 50 rows immediately before it -- a rate-matched (50.1% "
        "vs 50.1% of scorable names kept), persistence-matched (phi -0.010 vs -0.014), "
        "churn-matched (12.1x vs 12.2x predicted) and ETF-matched (14.2% vs 14.5%) control "
        "that keeps substantially different names (top-100 Jaccard 0.436) -- recovers at most "
        "+0.05 of GROSS validation skill over the unfiltered arm, i.e. far less than the "
        "in-window arm, reproducing on a third data channel the purity-over-characteristic "
        "split the volume channel gave at 76/24 and the range channel at 100/0; a reading at "
        "or above the in-window arm's would instead say this channel's whole term is a "
        "jump-stability characteristic and that the three channels are not one mechanism."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """5/45 close-to-close return shock with the median-jump exclusion read over rows
    -100..-51. `rv_retvol_shock_pure` with one node changed.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    printed = volume.notna() & (volume > 0)
    absr = np.log(prices).diff().where(printed & printed.shift(1)).abs()

    fast = absr.rolling(FAST, min_periods=3).mean()
    slow = absr.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow
    jump = absr.diff().abs().shift(DISPLACE).rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        score = shock.loc[date].reindex(names).dropna()
        j = jump.loc[date].reindex(score.index).dropna()
        if len(j) < 60:
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue
        score = score.reindex(j.index)[j <= j.median()].dropna()
        if len(score) < 60:
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
