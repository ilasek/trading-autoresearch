"""The high-volume return premium, at the only window where it is COMPUTABLE here.

THE CLAIM IN ONE LINE. A name whose recent trading volume is unusually high
relative to its own recent norm has had a visibility or recognition shock, and
the published finding (Gervais-Kaniel-Mingelgrin, pre-2018, so no post-2018
novelty discount applies) is that such names earn higher returns over the
following weeks. The sign is fixed from that mechanism and nothing else.

WHY THE WINDOW IS 5 DAYS AGAINST 45 AND NOT A YEAR -- THIS IS THE WHOLE DESIGN
AND IT IS A D1 ARGUMENT, NOT A PREFERENCE. `learnings.md` records that the
stored volume LEVEL is not causal: this panel's bars are adjusted as of the
fetch date, so a name's stored volume carries the product of every split factor
*after* each date. That factor cancels in a ratio of two volumes only when no
split falls between them. A long-window within-name volume ratio therefore
carries a STEP wherever a split lands inside the window -- and because splits
follow price run-ups, the step is correlated with past returns, which is the
contaminant this lab has now reproduced six times through `dollar_volume`.

Tonight's first attempt at a fix was worse than the problem and is recorded as
such: winsorising daily log-volume changes at +/- log(1.5) and cumulating them
clips **7.16%** of eligible printing days (the median daily |log volume change|
is 0.254, so that clip sits at only 1.6x a typical day's move), and since the
index is a cumulative sum every clipped day shifts its level permanently. The
result correlates **+0.126** with the plain log-volume shock -- it is an
accumulated random walk of clipping residuals, not a volume shock.

The window is the fix. Over a ~50-day total span the chance a split falls inside
is about 50/252 of a ~3%/yr rate, i.e. ~0.6% of name-dates, and an explicit
causal guard drops any name showing a daily |log volume change| above log(3)
anywhere in the window (0.57% of eligible printing days). A median, not a mean,
sets the baseline, because volume is heavy-tailed and one earnings day would
otherwise define the norm. That window is also the literature's own: the source
measures a day or a week of volume against the preceding fifty.

THE STRUCTURAL FACT THIS DESIGN EXPOSES, WORTH MORE THAN THE TRIAL: **on this
panel the CLEAN corner of the volume panel and the CHEAP corner of the cost
model do not overlap.** Long-window within-name volume ratios are cheap to hold
and carry the split step; short-window ones are clean and churn. There is no
construction that is both, so every volume candidate here pays for its cleanliness
in turnover. That is why this book is pre-registered at 2.0-6.0x rather than in
the free corner the record prefers.

WHAT IT IS NOT A RELABELLING OF, measured before the file was written. Mean
within-date Spearman rank correlation over 252 train month-ends: **+0.086** to
the dollar-volume trend that is this family's recorded lead (`lv_vol_trend_*`),
**-0.209** to trailing 126-day volatility, **+0.026** to 12-1 momentum, **-0.034**
to 126-day Amihud illiquidity, **+0.023** to the board lead's score. The first
number is the one that matters: a volume SHOCK and a volume TREND are different
objects here, so this is not the family's lead in a shorter costume. The second
discharges research `#502`'s free screen, which says to measure how much of a
volume score is a volatility sort before spending a trial on it: a fifth of a
rank, in the direction that makes high-volume names the *less* volatile ones.

THE QUOTA CARRIES TONIGHT'S OWN CORRECTION. Cells are (trailing-trading-calendar
peer group x instrument TYPE). The peer half is the standing geography control.
The type half is tonight's finding: a book that does not hold the panel's ~5.5%
ETF share buys an asset-class bet that `random_null_v3` prices as selection
failure, because it matches type but matches nothing inside the ETF type. A
volume-shock score has no obvious reason to tilt toward funds, which is exactly
why the quota is cheap insurance rather than a correction being applied twice.

NO TRAIN SIGNAL NUMBER IS OFFERED AS EVIDENCE for this book either. The screens
above are used only for the arithmetic refusals they can support -- a relabelling
correlation and a contaminated construction -- because corr(train skill,
validation skill) is -0.08 over 27 recorded trials and the 2026-10-16/17 rule
permits a train screen to refute but never to qualify.

WHAT ARGUES AGAINST THE BOOK.
 (i) The source's effect is strongest in smaller names, and this panel is the top
     of the capitalisation distribution in nine countries. That is a discount on
     the expected size, and by research `#506`'s reading rule it is the kind of
     conditioning structure that makes an unconditional claim overstate what a
     long-only book here can collect. It is not the outright refusal research
     `#505` applied to price delay, whose source localises to 0.02% of market
     value; the high-volume premium was documented in large caps too.
 (ii) `learnings.md` prices this lab's long leg at roughly a third of any
     object's spread, so the prize has to be three times what a long-short study
     would need -- against a cost bill this construction cannot avoid.
 (iii) Volume is not forward-filled, so a NaN is a non-print. The score is taken
     over prints only and its per-date coverage is 99% of eligible names, which
     is reported because the 2026-10-19/20 correction says to quote the ratio
     rather than compare a median count to a mean one.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it:
**2.0-6.0x** one-way per year. A 5-day signal reshuffles the top of the sort every
month and the band only declines to sell inside the top 200; this lab's validation
churn has run 73-100% above its train figure on tonight's books, and the range
carries that rather than assuming the band rescues it.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5            # days of recent volume
SLOW = 45           # days of baseline, ending FAST+1 days ago
SPLIT_GUARD = np.log(3.0)

STRATEGY = {
    "name": "lv_volume_shock_gkm_band",
    "family": "liquidity-volume",
    "hypothesis": (
        "Holding the 100 eligible names with the HIGHEST volume shock -- mean log share "
        "volume over the last 5 printing days minus the median over the preceding 45, "
        "dropping any name with a daily |log volume change| above log(3) anywhere in the "
        "window so a split's as-of-fetch step cannot enter the score, quota-allocated "
        "across (trailing-trading-calendar peer group x instrument type) cells, monthly "
        "with a 200-name retention band -- earns positive validation skill over the "
        "equal-weight eligible pool, because unusually heavy trading is a visibility "
        "shock that draws in buyers over the following weeks, and because a ~50-day "
        "window is the only span on this panel over which a within-name volume ratio is "
        "free of the back-adjustment step that has contaminated six dollar-volume scores."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """High short-window volume shock, split-guarded, quota'd across (calendar peer
    group x instrument type), monthly with a retention band.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    fast = lv.rolling(FAST, min_periods=3).mean()
    slow = lv.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow

    # Causal split guard: the largest one-day move in log volume anywhere in the window.
    step = lv.diff().abs().rolling(FAST + SLOW, min_periods=25).max()
    shock = shock.where(step < SPLIT_GUARD)

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        score = shock.loc[date].reindex(names).dropna()
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
