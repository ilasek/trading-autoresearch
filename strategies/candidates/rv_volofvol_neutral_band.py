"""Vol-of-vol: uncertainty ABOUT risk, held volatility-level-neutral.

THE CLAIM IN ONE LINE. The lab has measured the volatility LEVEL to null here
six times ("Sharpe is flat in beta on this panel"); it has never measured the
INSTABILITY of a name's volatility, which is a different quantity and is the one
range-variance object `program.md` names that no trial has touched.

WHY THE TWO ARE DIFFERENT, MEASURED BEFORE THIS FILE WAS WRITTEN. The score is
the trailing 252-day standard deviation of LOG 21-day Parkinson volatility, so
it is scale-free in the level by construction: its mean within-date Spearman
rank correlation to trailing 126-day volatility over 252 train month-ends is
**+0.132**. Demeaning it within volatility terciles takes that to -0.002 and
moves the score itself by almost nothing (rank correlation between the raw and
demeaned versions **+0.964**), which is why the demeaned version ships alone and
no "raw control" does -- an algebraically near-identical relative is not a
control. The volatility LEVEL in this identical harness ships instead, as
`pt_lowvol126_quota_band`, and that pair is the real test of whether this score
carries anything the level does not.

THE SIGN WAS FIXED FROM THE MECHANISM, BEFORE ANY NUMBER. Low vol-of-vol is
held. Uncertainty about an asset's risk is an ambiguity investors dislike and
therefore pay to avoid, so the ambiguous names should be the expensive ones;
this is the direction of the published vol-of-vol result (Baltussen-van
Bekkum-van der Grient). That paper is post-2018, so by `CLAUDE.md`'s rule its
novelty is discounted and **no performance expectation from it is imported
here** -- only the sign, which is also derivable from the mechanism alone.

WHY THE CONSTRUCTION IS WHAT IT IS, AND WHY IT IS NOT THE LEAD'S.
 (i) **Quota on (trailing-trading-calendar peer group x volatility tercile).**
     The peer half is the lab's standing geography control (2026-10-13/14: a
     whole-pool comparison welds the score to the region mix). The tercile half
     makes the de-risking-in-costume reading impossible by construction rather
     than by argument: the book holds the same share of each volatility tercile
     as the panel has, so it cannot be a low-beta bet in disguise.
 (ii) **Monthly with a 200-name retention band, and NOT the six overlapping
     sleeves the board lead uses.** The sleeve operator is refuted in advance for
     a score of this shape by the lab's own measurement: `learnings.md` F5 of
     2026-10-27/28 applied it to three slow RISK scores and watched it collapse
     the gross term (lowvol126 +0.057 -> +0.010), because the operator needs a
     score whose content is older than the holding period, and a 252-day
     statistic read five months late is a window shifted by half its own length.
     The band re-times nothing -- it only declines to sell a name whose score has
     decayed but not reversed -- and the record tells any new signal to carry it.
 (iii) **K = 100**, where the record measures the margin over the null gate to
     peak, and the equal-weight pool is emitted on dates before the score exists
     so the book is not scored in cash against a fully-invested benchmark.

NO TRAIN SIGNAL NUMBER IS OFFERED AS EVIDENCE FOR THIS BOOK, and that is a
deliberate break with the last twelve sessions. `learnings.md` 2026-11-16 puts
corr(train skill, validation skill) at -0.08 over 27 trials and 2026-11-19
measures the lab's own free forward-excess screen rejecting a true null 57% of
the time in its most-quoted cell, so a train sigma cannot qualify a candidate --
and the 2026-10-16/17 rule says a train screen may refute but may not qualify.
Tonight's screen was therefore used only for the arithmetic refusals it can
support (the +0.964 relabelling above), and the object is run rather than argued
into or out of existence. Train and validation numbers arrive together, from the
protocol, and the trial record is the result.

WHAT ARGUES AGAINST THE BOOK.
 (i) Vol-of-vol is estimated from 232 overlapping 21-day Parkinson windows, so
     neighbouring observations share 20 of 21 days and the standard deviation of
     the series is not the standard deviation of 12 independent quarters. It is a
     persistence-inflated estimate of volatility instability, which is a reason
     its cross-section may be noisier than its construction suggests.
 (ii) The score needs a high and a low for every day of a year, so its coverage
     is a question rather than an assumption: it is scored on 99% of eligible
     names per date over the train month-ends, which is reported here because
     the 2026-10-19/20 correction says to quote the per-date ratio.
 (iii) Instability of volatility is plausibly a *compensated* risk rather than an
     ambiguity premium, in which case the sign is the other one. The pre-signed
     direction is the one the mechanism gives and it is not hedged after the fact.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: 0.6-1.8x
one-way per year. A 252-day standard deviation is a persistent characteristic and
the band removes the marginal replacements, but this lab's validation churn has
run 29-49% above its train figure on this panel's wider split, and the range
carries that.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.features import parkinson_vol, realized_vol

K = 100
BAND = 200          # a held name is kept while it stays inside the top BAND
VV_WINDOW = 252     # days of log-Parkinson history the instability is measured over
VV_MIN = 180
PK_WINDOW = 21      # the range-volatility window whose instability is measured
VOL_WINDOW = 126    # the level the score is held neutral to
TERCILES = 3

STRATEGY = {
    "name": "rv_volofvol_neutral_band",
    "family": "range-variance",
    "hypothesis": (
        "Holding the 100 eligible names with the LOWEST trailing 252-day standard "
        "deviation of log 21-day Parkinson volatility -- vol-of-vol, demeaned within "
        "trailing-126-day volatility terciles and quota-allocated across "
        "(trailing-trading-calendar peer group x volatility tercile) cells, monthly with "
        "a 200-name retention band -- earns positive validation skill over the "
        "equal-weight eligible pool, because uncertainty about an asset's risk is an "
        "ambiguity investors pay to avoid and is therefore a priced characteristic "
        "distinct from the volatility LEVEL this panel has already measured to null six "
        "times, a distinctness established before the file was written by the score's "
        "mean within-date rank correlation of +0.132 to trailing 126-day volatility."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Low vol-of-vol, volatility-tercile and calendar-peer quota'd, monthly with a
    retention band. The pool is emitted on dates before the score exists.
    """
    high, low = aux["high"], aux["low"]
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    # Volatility of volatility. Ranges are a same-day ratio, so the stored back-adjustment
    # factor cancels exactly in high/low and the score reads no price LEVEL.
    pk = parkinson_vol(high, low, PK_WINDOW)
    logpk = np.log(pk.where(pk > 0))
    vv = logpk.rolling(VV_WINDOW, min_periods=VV_MIN).std()
    level = realized_vol(prices, VOL_WINDOW)

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = vv.loc[date].reindex(names)
        lv = level.loc[date].reindex(names)
        both = pd.concat([sc, lv], axis=1).dropna()
        both.columns = ["vv", "lvl"]
        if len(both) < 60:
            # Warm-up: hold the pool rather than cash, so the book is not scored against
            # a fully-invested benchmark while sitting out (2026-10-15/16). Once a book
            # exists, emit nothing and let it drift rather than trade on no score.
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        try:
            terc = pd.qcut(both["lvl"].rank(method="first"), TERCILES, labels=False)
        except ValueError:
            terc = pd.Series(0, index=both.index)

        # Low vol-of-vol is held; demeaned within volatility terciles so the ranking
        # cannot be a volatility-level ranking. Within a quota cell this subtracts a
        # constant, so it does not reorder the cell -- the neutralisation that bites is
        # the tercile half of the quota below.
        score = -(both["vv"] - both["vv"].groupby(terc).transform("mean"))

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()
        cells = groups.reindex(score.index).astype(str) + "|" + terc.reindex(score.index).astype(str)

        # The band: keep a held name while it is inside the top BAND, then fill to K.
        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        # If the band holds more than K, keep the best-ranked K of them rather than
        # whichever happened to be listed first.
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            room = K - len(keep)
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, cells.reindex(rest.index).dropna(), room)
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
