"""Does the seated `liquidity-volume` lead's score mean anything for the 42% of
its book that is an ETF?

WHY THIS FILE EXISTS. `research/SUMMARY.md` #95 asked the lab to split every score
it owns into its region-mean `m(X)` and region-demeaned `dm(X)` halves, and named
two construction nodes to pre-commit — the minimum names per region, and **whether
ETFs enter the region mean at all**, "since a region mean containing that region's
own ETF reads the ETF's score back into itself". Tonight's pre-registration fixed
both. Measuring them then turned up something the note did not ask about and nobody
here had ever looked at: the seated lead does not merely put ETFs in its *mean*, it
puts them in its *book*. Over 260 train month-ends its top-20 holds **8.3 ETFs**,
and its single most-held name is **EWU, the UK country ETF, in the book on 87% of
month-ends**, ahead of BLK (84%) and SPGI (73%).

THE MECHANISM, STATED BEFORE THE MEASUREMENTS THAT FOLLOW. `ILLIQ` is
`mean(|return| / dollar_volume)` — Amihud's price-impact ratio, and its meaning is
that a security whose price moves a lot per dollar traded is one whose *own order
book* is thin. For an ETF that reading fails at the definition: creation and
redemption arbitrage ties the price to the basket, so the **numerator is inherited
from securities the ETF does not trade** while the denominator is set by the ETF's
own secondary-market activity. The two halves of the ratio refer to different
objects. This is the instrument-class analogue of the venue-unit account
`learnings.md` records for 2026-09-03 — that account says the *denominator's units*
are set by the listing venue; this one says that for one instrument class the
numerator and the denominator are not measuring the same security at all. Note the
two compound: the region demean is what makes ETFs *selectable* in the first place,
because it compares an ETF against its regional peers instead of against the
cross-section, and the `GLOBAL` bucket is nine ETFs and nothing else.

THE MEASUREMENTS, ALL FREE, ALL TRAIN, ALL RUN BEFORE THIS FILE WAS WRITTEN.
Top-20 excess over the scoreable pool, forward 21 days, region-demeaned throughout:

    score                    ETFs holdable      ETFs excluded        delta
    region-rel ILLIQ        +5.18%/yr(t=+3.90)  +10.29%/yr(t=+5.77)   +5.11pp
    seasonal same-other     +5.03%/yr(t=+3.66)   +4.23%/yr(t=+2.95)   -0.80pp
    21d reversal            +2.94%/yr(t=+1.49)   +2.43%/yr(t=+1.26)   -0.51pp
    12-1 momentum           +4.92%/yr(t=+2.31)   +2.21%/yr(t=+1.16)   -2.71pp
    [ctl] GK 21d vol        +6.35%/yr(t=+4.42)   +4.97%/yr(t=+2.93)   -1.38pp
    [ctl] placebo hash      +0.05%/yr(t=+0.04)   -0.46%/yr(t=-0.31)   -0.50pp

**The exclusion helps `ILLIQ` and hurts every other score in the repo**, including
this universe's identified survivorship artifact, which moves 1.38pp the *other*
way — the control that would have caught "this is just a stock/ETF survivorship
swap" and does not. The placebo puts the mechanical cost of shrinking a pool at
about -0.5pp, so the ILLIQ-specific content is nearer +5.6pp than +5.1pp.

TWO CONFOUNDS MEASURED AND BOUNDED RATHER THAN ASSERTED.

*(a) Screen on the statistic the trial is scored on.* At the seated lead's own
breadth (band 30/45, ~37 names) rather than at top-20, the same gap is **+2.14pp**,
not +5.11pp — less than half. That is the standing 2026-08-30 rule biting, and the
smaller number is the one this candidate is pre-registered against.

*(b) A volatility tilt in costume.* The ETF-free book sits at trailing-volatility
percentile **0.619** against the seated book's 0.496, and `learnings.md` prices the
train high-minus-low vol spread at +19.4%/yr — this universe's survivorship artifact
observed directly. Holding the volatility profile fixed by construction (equal draw
from each trailing-vol tercile, 36 names, profiles matched at 0.508 vs 0.517):

    unconstrained   seated +4.50%/yr(t=+3.99)   no ETFs +7.61%/yr(t=+6.16)   +3.11pp
    vol-NEUTRAL     seated +4.09%/yr(t=+3.69)   no ETFs +6.14%/yr(t=+5.45)   +2.06pp

**About a third of the raw gain is the volatility tilt and two thirds survives
neutralisation at t = +5.45.** The tilt is real and is a cost this candidate pays;
it is not the mechanism.

HOLDINGS-ONLY PRE-TRIAL PROFILE, train, at this candidate's own band:

    book                     names   annual L1 churn   vol pct   book excess
    seated (ETFs holdable)   36.87        0.62x         0.496    +4.80%/yr(t=+4.70)
    this candidate           38.12        0.43x         0.619    +6.94%/yr(t=+6.07)

Breadth is matched to 3.4% without being pinned, so the 2026-09-06 breadth confound
cannot carry this. Churn *falls*, which is a tailwind — but at 0.5x annual turnover
this is the cheapest book in the repo and the whole difference is worth about
0.06%/yr, so **the trial cannot be measuring the broker in either direction**, the
failure mode that swamped four consecutive non-`price-trend` trials.

ONE NODE, per `SUMMARY.md` #94. Everything else is bit-identical to
`lv_illiq_region_wide30`: the 63-day `ILLIQ` window, the region demean with
`MIN_REGION` = 4, band 30/45, equal weighting, the monthly grid, the warmup. ETFs
are still counted in the region mean — excluding them there as well is a *second*
node and the 2x2 prices it at +0.51pp, inside noise, so it is not taken.

PRE-REGISTERED POINT ESTIMATE: **0.99**, range **0.88 to 1.12**, against the seated
lead's 0.942. The arithmetic: +2.14pp of book excess on the seated book's 16.43%
annual return is +13% of return, against an expected volatility rise of order 10%
from the 0.496 -> 0.619 percentile shift, netting to roughly +0.05 of Sharpe — then
widened, in both directions, because the two calibrations this repo owns for
"screen to book" disagree by an order of magnitude (2026-08-30's designed pair turned
+3.35%/yr of screen into **-0.11** of validation Sharpe; 2026-09-03's region demean
turned +1.30%/yr into **+0.236**). This candidate is a *pool* change, and 2026-09-06
restored the over-prediction rule as the default after the intersection's
pool-changing operator over-predicted, so the low end of the range is the live risk
and I am not hiding it behind the point estimate.

**WHAT IS ESTABLISHED WILL NOT BE THE GAP.** Expected `rho` to the seated lead is
~0.85-0.9 on shared names, so `SE = 0.568*sqrt(1-rho)` puts one paired standard
error near 0.18-0.22 and **no outcome in the pre-registered range is resolvable**.
That is stated in advance and it is not a reason to skip the trial: what the trial
decides is whether the *seated family lead is misspecified* — whether the top
non-`price-trend` single sort on the board, the cheapest book in the repo, and the
leg every blend decline for ten sessions has been priced against, is holding 42% of
its capital in instruments its own score cannot describe. That is a statement about
the leaderboard, not a knob. The closest precedent is exact: `lv_illiq_region_relative`
(2026-09-03) was the same shape — a measurement-hygiene fix to this same score,
pre-registered at 0.72, landed 0.917 at t = +1.01, equally unresolvable, and
`learnings.md` records it as "the first leg improvement in this repo that came from a
stated mechanism rather than from a screened table".

SECOND PRE-REGISTRATION, per the standing instruction that every scout records its
train Sharpe as a prediction of its validation Sharpe. n = 28 outside `price-trend`.
The 2026-09-04 sample rule was checked prospectively rather than after the fact: this
book is scoreable on **215** train month-ends first reaching 2000-02 against the
seated lead's **227** first reaching 1999-02, a twelve-month offset on a
twenty-year window, so unlike the band bracket that rule was written for, **the two
train readings are comparable and this one is admissible.**

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from engine import data as D
from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_stocks_only",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Removing ETFs from the holdable set of the seated `liquidity-volume` lead — one "
        "node, with the 63-day ILLIQ window, the region demean at MIN_REGION=4, the 30/45 "
        "band, equal weighting and the monthly grid all bit-identical to "
        "`lv_illiq_region_wide30`, and ETFs still counted in the region mean — scores near "
        "0.99 on validation against that lead's 0.942, because ILLIQ is a price-impact "
        "ratio whose numerator an ETF inherits from a basket it does not trade while its "
        "denominator is the ETF's own secondary-market volume, so the ratio does not "
        "describe the 8.3 of 20 names the seated book currently draws from that class. "
        "The exclusion is worth +2.14pp/yr of train book excess at this candidate's own "
        "breadth (+5.11pp at top-20), and it is ILLIQ-specific rather than a pool effect: "
        "the same exclusion costs the seasonal leg 0.80pp, momentum 2.71pp, a placebo hash "
        "0.50pp and this universe's identified survivorship artifact 1.38pp, so the one "
        "control that would catch a stock-for-ETF survivorship swap points the other way. "
        "About a third of the gain is a volatility tilt — the book moves from percentile "
        "0.496 to 0.619 — and two thirds survives holding the volatility profile fixed by "
        "construction (+2.06pp, t = +5.45). Breadth is matched at 36.9 against 38.1 and "
        "churn falls 0.62x to 0.43x, worth 0.06%/yr on the cheapest book in the repo, so "
        "the trial cannot be measuring either breadth or the broker. No outcome in the "
        "0.88-1.12 range is resolvable against a paired SE near 0.18-0.22; what the trial "
        "decides is whether the seated family lead is misspecified, which is a statement "
        "about the leaderboard rather than a knob."
    ),
}

ILLIQ_WINDOW = 63     # bit-identical to the seated lead
CORE_N = 30
BAND_N = 45
WARMUP = 6
MIN_REGION = 4        # a region below this cannot supply a peer mean

# Instrument type is static metadata from `data/universe.yaml`, read through the
# sanctioned loader: no dates, no prices, nothing estimated from returns. Exactly
# the justification `strategies/lib/groups.py` gives for its region map, and it
# cannot leak the future in the way a fitted classification could. It *is* current
# metadata about a survivorship-selected universe, which is the standing caveat on
# every result in this repo and is not made worse by reading one more static field.
_ETFS = frozenset(
    rec["id"] for rec in D.load_universe()["instruments"] if rec["type"] == "etf"
)


def _region_relative(score: pd.Series) -> pd.Series:
    """Each name's score minus the mean score of its own region, dropping names
    whose region has fewer than `MIN_REGION` instruments scoreable on that date.

    Imported unchanged from `lv_illiq_region_wide30` so that this arm and the
    seated lead differ at exactly one node. ETFs are still counted in the mean.
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
        # The one node. Applied after the demean so the region means, and the
        # MIN_REGION filter that depends on them, are bit-identical to the seated
        # lead's; only the holdable set changes.
        score = score[[n for n in score.index if n not in _ETFS]]
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
