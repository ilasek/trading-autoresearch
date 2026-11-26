"""THE THIRD CHANNEL, IN-WINDOW ARM -- the one trial that turns baseline purity into a law or
confines it to two channels.

THE RULE UNDER TEST, as the record left it on 2026-11-25. A score of the form "recent window
minus baseline window" is corrupted when its BASELINE window itself contains a discontinuity:
it is then measuring a DECAYING BASELINE rather than a fresh event. Excluding the names whose
scoring window contains the largest jumps was measured to carry, in GROSS validation skill:

    channel  in-window minus displaced   in-window arm   displaced arm   no-filter arm
    volume        +0.110                   +0.211 (#32)    +0.101 (#41)    +0.066 (#40)
    range         +0.109                   +0.119 (#42)    -0.009 (#43)    +0.010 (#38)

Two channels, the same +0.11, with the bill flat across all six books so none of it is cost.
The displaced arm is what separates the two readings: if the term were a cross-sectional
STABILITY CHARACTERISTIC (quiet names do better) the same criterion read over the 50 days
BEFORE the scoring window would pay the same; it recovered a quarter of the term on the volume
channel and none of it on the range channel. This file is the in-window arm on a third channel.

THE CHANNEL. Close-to-close `|log return|`, masked to days where both the day and the previous
day printed a volume. It is a ratio of two stored prices inside the visible window, so the
split half of the as-of-fetch factor `D_i(t)` cancels exactly and the dividend half is the
distribution itself -- an adjusted-close return IS the total return. It is in the same units as
`log(high/low)`, so the operator transplants with no rescaling and no new parameter.
`dollar_volume` cannot host this test (it keeps the dividend half of `D_i(t)`), which is why
the recorded `lv_vol_trend_*` family is not the third channel.

THE FILTER, AND IT HAS NO TUNED PARAMETER. A name is dropped if the largest daily change in
its absolute return inside the 50-row scoring window exceeds the CROSS-SECTIONAL MEDIAN of
that quantity among the names scorable on that date -- the same parameter-free restatement
`rv_range_shock_pure` used, for the same reason: the volume channel's log(3) threshold is in
log-volume units and is inert everywhere else (a literal transplant onto the range channel
returned top-100 Jaccard 1.000 and was declined as a relabelling before it cost a trial). The
median is the one choice that is not a knob and it lands the exclusion rate on the other two
channels' by construction.

FREE PRE-TRIAL SCREEN, measured before this file was written. The three arms are matched:

    arm                         keeps   phi      exit200  pred churn  Jaccard vs bare  ETF share
    bare (#44 tonight)           100%   -0.014    45.2%     14.1x         --             7.1%
    THIS FILE, in-window        50.1%   -0.014    38.5%     12.2x        0.224          14.5%
    displaced to -100..-51      50.1%   -0.010    38.4%     12.1x        0.261          14.2%
    in-window vs displaced                                             Jaccard 0.436

This is the best-matched purity triple in the record -- the two filtered arms agree on
exclusion rate to 0.0pp, on rank persistence to 0.004, on predicted churn to 0.1x and on ETF
share to 0.3pp while sharing only 44% of their holdings (the range channel's analogue was
50.0/49.8%, phi -0.007/-0.012, 7.4x/7.4x, Jaccard 0.434). Coverage of eligible names 98.7%.
The filtered score's rank rho to trailing 126-day volatility is +0.013, so this is not a
volatility-level sort in costume -- the standing concern about every variance-class object here.

RIDER THAT MUST TRAVEL WITH THE RESULT. The filter DOUBLES the ETF share of the book, 7.1% ->
14.5%, because a fund's daily absolute return is compressed and so survives a
largest-jump-in-window criterion. Per the 2026-11-22 finding, an ETF-overweight book is
mismatched against its own type-matched null, and exactly two recorded objects carried that
confound (both low-volatility books, at 24.7% and 20.8%). **The two filtered arms are
ETF-matched to 0.3pp, so the in-window-minus-displaced contrast -- the statistic that tests
purity -- is clean of it. The bare-versus-filtered contrast is NOT, and will be reported with
that caveat.** This is the first time in the three-channel series that the ETF share of the
arms was measured before the runs rather than after.

PRE-REGISTERED PREDICTIONS, written before the run.
 - THIS ARM minus the BARE arm, in GROSS skill: **+0.08 to +0.14** if purity is a property of
   shock scores. **Within noise of zero (|.| < 0.035)** if it belongs to the volume and range
   channels only.
 - THIS ARM minus the DISPLACED arm, the purity term proper: **+0.08 to +0.14**.
 - NET skill: negative, -0.10 to -0.22. The statistic that tests the claim is the GROSS skill
   and the null percentile, as for all six recorded arms.
 - NULL PERCENTILE: 93-99% if the gross lands in range, using the 2026-11-25 monotone
   calibration (gross +0.12 read 95% on the range channel, +0.21 read 99% on the volume one).
 - CHURN: train 9-15x, validation 13-28x (predictor 12.2x; the 2026-11-22 fit and the
   1.30-2.00x validation multiplier).
 - REFUSAL, pre-committed: if the in-window term lands below +0.035, the purity rule is
   reported as channel-specific and CLOSED. No third threshold is tried, no knob is turned,
   and no fourth channel is sought -- the exclusion rate is already matched and the median has
   removed the only free parameter.

WHAT ARGUES AGAINST THE BOOK.
 (i) The underlying score is being run tonight as a control and is predicted to be a null, so
     this is a filter applied to nothing. If the filter has to CREATE the signal rather than
     clean it, the purity story is wrong -- which is exactly why it is run on a measured null,
     as #42 was.
 (ii) `|r|` is the spikiest of the three channels, so `max |d|r||` over 50 rows is driven
     largely by the single largest absolute return in the window. The filter is therefore
     closer to "exclude names with a jump event in the window" than on the other two
     channels, where the scored quantity is persistent. That is a fair reading of purity but
     it is a WEAKER instrument, and it is the honest reason the in-window term could come in
     below the other two channels' +0.11 without the rule being wrong.
 (iii) Selecting on a within-window jump statistic is one step from the "second moment of the
     series" anti-candidate class (`vchurn252`, refuted with the wrong sign). The displaced
     arm is the control that separates them.
 (iv) A large absolute return is the short-horizon reversal's conditioning variable with its
     sign discarded, so the book's returns are exposed to reversal; no signed control is run
     tonight and that limit is stated rather than fixed.
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

STRATEGY = {
    "name": "rv_retvol_shock_pure",
    "family": "range-variance",
    "hypothesis": (
        "Adding a parameter-free baseline-purity filter to the 5/45 close-to-close return "
        "shock -- drop any name whose largest daily change in |log return| inside the 50-row "
        "scoring window exceeds the cross-sectional median of that quantity on the date, "
        "which keeps 50.1% of scorable names and so lands on the 44.7% and 50.0% the volume "
        "and range channels' filters were measured to keep -- raises that score's GROSS "
        "validation skill by +0.08 to +0.14 over both the unfiltered arm and the "
        "rate-, persistence-, churn- and ETF-matched arm that reads the same criterion over "
        "days -100..-51, because a shock score whose baseline window itself contains a "
        "discontinuity is measuring a decaying baseline rather than a fresh event and that "
        "defect is a property of shock scores rather than of share volume or the intraday "
        "range; an in-window term below +0.035 instead confines the rule to those two "
        "channels and closes it."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """5/45 close-to-close return shock with an in-window baseline-purity filter at the
    cross-sectional median jump. `rv_retvol_shock_band` with one node added.
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
    jump = absr.diff().abs().rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken — the median
        # is computed inside the set the engine will actually let this book buy.
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
