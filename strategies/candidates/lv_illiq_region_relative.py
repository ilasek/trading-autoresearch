"""Amihud ILLIQ scored against the name's own region, not against the world.

WHY THIS FILE EXISTS. `research/SUMMARY.md` #71 (Avramov-Cheng-Metzker) makes a
claim the lab has never tested separately: the content of a cross-sectional
signal is in **peer-relative** ranking, not in picking groups. Note carefully
what that is *not*. `experiments/learnings.md` closed regional neutralisation by
a bracket, but that was about **weights** — neutralising the book's regional
exposure. This is about the **scoring benchmark**: what each name's score is
measured relative to, before any book exists. Different operator, never tested.

Run for free on train tonight over all four family-lead scores, against the
forward 21-day return, on the tail statistic a 20-of-140 book is actually scored
on (`learnings.md` 2026-08-30: screen on the statistic the trial will be scored
on, not on a quintile spread):

    leg          benchmark        top-20 excess        IC
    seasonal     unconditional   +6.73%/yr (t=+4.35)  +0.0387 (t=+3.77)
    seasonal     sector-rel.     +5.09     (t=+3.54)  +0.0278 (t=+2.96)
    seasonal     region-rel.     +5.03     (t=+3.66)  +0.0317 (t=+2.90)
    reversal     unconditional   +2.70     (t=+1.22)  +0.0095 (t=+0.71)
    reversal     sector-rel.     +4.52     (t=+2.61)  +0.0116 (t=+1.28)
    reversal     region-rel.     +2.89     (t=+1.38)  +0.0146 (t=+1.13)
    illiq        unconditional   +4.25     (t=+2.69)  +0.0186 (t=+1.78)
    illiq        sector-rel.     +5.28     (t=+3.72)  +0.0145 (t=+1.59)
    illiq        region-rel.     +5.55     (t=+3.98)  +0.0347 (t=+4.47)

(`group_lead` is omitted from that table on purpose: it IS the sector median
broadcast to its members, so sector-demeaning it is identically zero — measured
median cross-sectional SD 0.0e+00, largest |value| 2.8e-17. Its apparently strong
"+6.14%/yr, t = +3.76" row is a rank over exact ties broken by column order. That
is the sixth instance of this repo's oldest failure mode and it was caught by the
standing detector `learnings.md` added last session: print the object's own
dispersion before believing a suspiciously good screen.)

WHY ILLIQUIDITY AND WHY REGION, CHOSEN ON MECHANISM RATHER THAN ON THE TABLE.
`ILLIQ` is |return| / dollar volume — a **price-impact ratio whose units are set
by the venue**. Tick size, lot size, settlement, market-maker structure and
listed float differ across the exchanges in this universe, so the cross-region
level of `ILLIQ` is partly a measurement artifact of where a name trades rather
than a statement about its liquidity premium. Region-demeaning removes that
artifact. This is the one cell in the table with an argument that does not depend
on the table: it predicts the improvement should be larger for **region** than
for **sector** (venue is a regional property, not an industry one), and that is
what the two rows show — IC +0.0347 (t = +4.47) against +0.0145 (t = +1.59), from
an unconditional +0.0186.

It also sharpens a result the lab already has. `learnings.md` (2026-08-29)
checked that this leg is not a disguised volatility tilt (`ILLIQ` within
trailing-volatility terciles, +2.01%/yr against the unconditional +1.72%/yr).
Region was never the control that was run, and it is the one the construction
argues for.

CHURN, MATCHED HOLDINGS-ONLY BEFORE THIS FILE WAS WRITTEN. This is the rare
comparison where the standing confound is absent by construction — a
trailing-quarter illiquidity ranking is slow-moving whatever it is benchmarked
against:

    benchmark        annual turnover   avg positions
    unconditional         0.77x            24.6
    sector-relative       0.75x            24.2
    region-relative       0.81x            24.9

0.04x of turnover is ~0.006%/yr of cost. `learnings.md` records four consecutive
non-`price-trend` trials in which a turnover difference swamped the mechanism;
this pair cannot be one of them.

WHAT IT COSTS. Regions with fewer than four instruments present cannot supply a
peer mean and are dropped, taking the scoreable pool from 114 to 102 names on
train. That is a real narrowing and it is why the comparison is run as a book
rather than argued from the IC.

PRE-REGISTERED POINT ESTIMATE: **0.72**, against the seated family lead
`lv_amihud_illiquidity_tilt`'s 0.681. The train tail excess improves by
+1.30%/yr, which at this book's volatility is worth roughly +0.06 of Sharpe if it
transferred one-for-one — and the standing rule is that a cross-sectional screen
**over-predicts the book it motivates**, so the estimate is deliberately below
that. A result at or below 0.681 says the peer benchmark is a train-split
artifact and closes #71 for this family.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. The unconditional version
is the largest over-prediction on the board (train 1.001 against validation
0.681), so this leg is the one where the question is sharpest. n = 22 outside
`price-trend`, unresolved.

SCOUT. It does not compete for the seat and cannot reach the holdout. The solved
required-leg-Sharpe bar for a resolvable 20% blend is 1.34-1.42 against a 1.120
champion, and nothing in this family is close.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_region_relative",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Holding the 20 instruments whose trailing-quarter Amihud ILLIQ is highest "
        "relative to the mean ILLIQ of their own region — equal-weighted with the same "
        "hold-30/enter-20 band, the same 63-day window and the same monthly grid as the "
        "seated family lead `lv_amihud_illiquidity_tilt`, with churn matched holdings-only "
        "in advance at 0.81x against 0.77x annual turnover and 24.9 against 24.6 names — "
        "scores near 0.72 on validation, above that lead's 0.681, because ILLIQ is a "
        "price-impact ratio whose cross-region level is partly a venue artifact (tick size, "
        "lot size, settlement and listed float differ by exchange) rather than a liquidity "
        "premium, so removing the region mean removes measurement noise rather than signal; "
        "measured on train the region-relative score raises the top-20 excess from "
        "+4.25%/yr (t = +2.69) to +5.55%/yr (t = +3.98) and the cross-sectional IC from "
        "+0.0186 (t = +1.78) to +0.0347 (t = +4.47), and does so more strongly than the "
        "sector-relative benchmark (+0.0145, t = +1.59) exactly as a venue account predicts "
        "and an industry account does not. A result at or below 0.681 says the peer "
        "benchmark is a train-split artifact."
    ),
}

ILLIQ_WINDOW = 63     # one quarter, as the seated lead
CORE_N = 20
BAND_N = 30
WARMUP = 6
MIN_REGION = 4        # a region below this cannot supply a peer mean


def _region_relative(score: pd.Series) -> pd.Series:
    """Each name's score minus the mean score of its own region, dropping names
    whose region has fewer than `MIN_REGION` instruments scoreable on that date.

    `groups.REGION_OF` is static instrument metadata read from `data/universe.yaml`
    — no dates, no prices, nothing estimated from returns — so this reads only
    the cross-section it is handed.
    """
    labels = pd.Series({name: G.REGION_OF.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= MIN_REGION).dropna()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = _region_relative(illiq.loc[:dt].iloc[-1].dropna())
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
