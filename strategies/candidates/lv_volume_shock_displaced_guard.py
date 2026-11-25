"""THE DISCRIMINATOR FOR TONIGHT'S HEADLINE -- the same guard criterion, the same exclusion
rate, the same churn, read on a window the score never touches.

WHAT TONIGHT ESTABLISHED, AND WHY ONE MORE ARM IS NEEDED TO READ IT. Two arms of the
split-guarded 5/45 volume shock are now recorded, identical in every node but the guard:

    arm                            val sharpe   net skill   @2x cost   bill   GROSS skill   null pctile
    #32 lv_volume_shock_gkm_band     +0.368       +0.031      -0.149    0.180    ~+0.211        99%
    lv_volume_shock_unguarded        +0.200       -0.138      -0.342    0.204    ~+0.066        95%

The guard -- "drop any name whose daily |log share volume change| exceeds log(3) anywhere in
the 50-day scoring window" -- is worth **+0.169 of net and ~+0.145 of GROSS validation
skill**, i.e. about two thirds of the whole prize the record attributes to the high-volume
return premium. The null gate is cleared by BOTH arms, so that part of the record survives:
the gate clearance belongs to the shock. The skill does not.

TWO READINGS OF THAT +0.145, AND THEY PREDICT OPPOSITE THINGS HERE.
 (A) **Baseline purity.** A 5/45 shock compares the last five days to a 45-day baseline. If
     the baseline window itself contains a volume explosion, the "shock" is measuring a
     decaying baseline rather than a fresh event, and excluding those names makes the score
     mean what it says. On this reading the guard is a SIGNAL-PURITY filter whose value is
     tied to the window the score reads, and it should generalise to every short-window
     shock score in the lab.
 (B) **A volume-stability characteristic.** The guard keeps names whose daily volume never
     tripled in 50 days, which is a cross-sectional screen on volume instability -- the class
     `learnings.md` (2026-11-20) put on its by-name anti-candidate list as "any second moment
     of the volume series at any window or sign", after `vchurn252` was refuted with the
     wrong sign. On this reading any 55%-rate volume-stability screen is worth about the
     same, and nothing about the scoring window matters.

THIS FILE IS THE ONE-OPERATOR TEST. It is #32 with the guard's test window DISPLACED: the
same log(3) threshold on the same daily |log volume change|, but taken over days -100..-51 --
the 50 days immediately BEFORE the scoring window, which the score itself never reads.
Measured on train before this file was written, the displacement is rate- and churn-matched
almost exactly:

    arm            coverage of eligible   phi      exit200   predicted train churn
    #32 guarded          44.7%          -0.022     25.6%            8.4x
    this arm             45.6%          -0.028     25.9%            8.5x
    unguarded            99.8%          -0.025     45.8%           14.3x

so the two guarded arms exclude the same share of the panel at the same persistence and the
same churn, and differ only in WHICH window the exclusion reads. They keep different names:
top-100 Jaccard between them is **0.344** (and 0.274 / 0.320 against the unguarded arm), well
below the 0.90 a relabelling is refused at.

PRE-REGISTERED PREDICTIONS, WRITTEN BEFORE THE RUN, ONE PER READING:
 - If (A) baseline purity is the mechanism, this arm lands near the UNGUARDED arm: gross
   skill ~+0.07, net skill negative, because the score's own baseline is left unprotected.
 - If (B) a stability characteristic is the mechanism, this arm lands near **#32**: gross
   skill ~+0.21, net skill near zero or positive, because any 55%-rate volume-stability
   screen buys the same thing.
Either outcome is a result and neither is a refutation of the other arm. A landing in the
middle is the honest third answer and would say the two channels share the term.

WHAT ARGUES AGAINST THE BOOK.
 (i) It is a construction node and not a new bet. Like the unguarded arm it is bought for
     the rider it places on a recorded result; by the breadth mandate's own standard
     (2026-11-22: read the ACTIVE-return rho, not the label) it will cluster with the
     volume-shock mechanism and `distinct_mechanisms` will not move.
 (ii) The displacement is NOT a perfectly clean experiment: a Jaccard of 0.344 between the
     two guarded arms says volume instability is not persistent enough across adjacent
     50-day windows for this to be "the same screen on a different window". So reading (B)
     is tested in its strong form -- *any* rate-matched stability screen is worth the same --
     and not in a weaker "the same names" form. Said here rather than afterwards.
 (iii) Displacing the guard costs 50 more days of required volume history, so the book starts
     later in the warm-up and holds no name with under ~100 printing days. Price-history
     depth carries no signal on this panel (2026-11-20), so this is a coverage restriction.
 (iv) Same cost corner as both other arms: a near-zero-persistence score has no cheaper
     construction here (the band is inert below phi ~0.97; holding longer dilutes a 1-4 week
     premium proportionally), so the bill is structural.

PRE-REGISTERED TURNOVER: **train 7-13x** one-way (predictor 8.5x, #32 charged 9.0x at an
identical 25.6% exit rate), **validation 12-24x** (#32 charged 16.6x). The statistic that
tests the claim is the GROSS skill -- net skill plus the bill implied by skill minus
skill-at-2x-costs -- read against the two bracketing arms above, together with the null
percentile.

NO TRAIN SIGNAL STATISTIC was computed for this file. Every number quoted is a coverage
count, a jump rate, a rank persistence, a holdings Jaccard, a churn prediction, or a
validation figure already recorded in `trials.jsonl` for an earlier arm.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5            # printing days of recent volume
SLOW = 45           # printing days of baseline, ending FAST+1 days ago
GUARD = np.log(3.0)
WINDOW = FAST + SLOW     # 50: the span the score reads
DISPLACE = WINDOW        # the guard reads days -100..-51 instead

STRATEGY = {
    "name": "lv_volume_shock_displaced_guard",
    "family": "liquidity-volume",
    "hypothesis": (
        "Taking lv_volume_shock_gkm_band and displacing its log(3) volume-jump guard from "
        "the 50-day scoring window to the 50 days immediately before it -- a rate-matched "
        "(45.6% vs 44.7% of eligible names kept), persistence-matched (phi -0.028 vs -0.022) "
        "and churn-matched (predicted 8.5x vs 8.4x) exclusion that the score itself never "
        "reads -- recovers only a small part of the ~+0.145 of GROSS validation skill that "
        "guard was measured to carry tonight, because that value is baseline PURITY (a 5/45 "
        "shock whose 45-day baseline contains a volume explosion is measuring a decaying "
        "baseline, not a fresh event) rather than a cross-sectional volume-stability "
        "characteristic; a landing near #32's ~+0.21 instead would say any rate-matched "
        "stability screen buys the same thing and would put the term back on the "
        "second-moment-of-volume class the record has on its anti-candidate list."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """#32 with the guard's test window displaced to days -100..-51. One node changed."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    fast = lv.rolling(FAST, min_periods=3).mean()
    slow = lv.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow

    # The operator under test: the same jump criterion, read on the 50 days BEFORE the
    # window the score reads. Causal — it looks further back, never forward.
    step = lv.diff().abs().shift(DISPLACE).rolling(WINDOW, min_periods=25).max()
    shock = shock.where(step < GUARD)

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        score = shock.loc[date].reindex(names).dropna()
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
