"""THE AGGREGATE INSTRUMENT AS THE TRADED UNIT -- the one object this panel holds and has
never ranked.

THE CLAIM IN ONE LINE. Sorting the eligible NON-STOCK instruments (the panel's 42 funds)
on their own previous month's return and holding the top fifth, long-only, equal-weighted,
earns a validation Sharpe above the 90% quantile of a random selection built the same way
from the same pool -- because at the AGGREGATE level the short-horizon cross-sectional
signal is CONTINUATION, where at the single-name level it is REVERSAL.

WHY THIS IS A DIFFERENT MECHANISM AND NOT MOMENTUM RELABELLED -- THE SIGN FLIP IS THE
WHOLE ARGUMENT. The lab's leaderboard clusters mechanisms, so "momentum also works on
indices" would be one mechanism with two labels and would deserve no trial. The literature
reports the opposite: Cakici-Fieberg-Neszveda-Piljak-Zaremba define the country-level
previous-month sort High-minus-Low and state it is momentum "rather than reversal", and
Chan-Hameed-Tong find index CONTINUATION strongest at 2-4 weeks -- while the single-name
one-month signal is the reversal this lab has itself measured. A signal that changes SIGN
when the unit of aggregation changes is a different mechanism, not a different label.

WHY THE HORIZON IS ONE MONTH AND NOT SWEPT. Fixed from the two sources before the file was
written and not varied: Chan-Hameed-Tong put index-momentum alphas near zero and jointly
insignificant at 1 week, significant at the 1% level at 2 and 4 weeks, and GONE at 12 and
26 weeks; the multiverse paper's one price-computable signal surviving its design sweep,
a block bootstrap and out-of-sample design selection is the one-month sort. One horizon,
taken from the sources. The long-horizon (~3-year) country reversal is refused outright on
window width -- a 3-year ranking against a six-year validation split is two non-overlapping
test periods.

WHY THE LAB THROWS THIS BET AWAY BY CONSTRUCTION, WHICH IS WHY IT HAS NEVER BEEN MEASURED.
Every quota'd candidate on this board allocates across (trailing-trading-calendar peer
group x ...) cells precisely to remove the region axis, because v3's null is region-matched
while its skill statistic is against the whole pool, so an un-neutralised region tilt is a
geography claim wearing a selection costume. That control is correct for a single-name
book and it deletes the object tested here. **This file therefore carries NO peer quota, by
design, and the object it buys is the region/asset bet itself.**

WHAT THIS OBJECT IS NOT, STATED PLAINLY BECAUSE IT LIMITS THE READING. It is not a
country-index book. The panel's non-stock sleeve is a SUPERSET of country and region funds
-- it also holds sector, bond and commodity funds -- and separating the country subset
needs a fund-to-country mapping that exists nowhere a candidate may read: the membership
files are refused outright and naming the funds individually would be a hindsight
selection of which aggregate units to rank. So the unit tested is "aggregate instrument",
not "country", and the sources' claim transfers to it only as far as aggregation itself is
the mechanism. That is a discount on how directly this trial speaks to them, and it is
recorded as one.

THE THREE DISCOUNTS FROM THE SOURCES THEMSELVES, NONE OF THEM REMOVABLE HERE.
 (i) NO SOURCE IN THIS VEIN MODELS TRANSACTION COSTS. A full-text grep of the multiverse
     paper returns zero mentions of transaction or trading cost; Chan-Hameed-Tong's
     economic-significance measure is an explicitly frictionless zero-cost arbitrage
     return; Richards' contrarian portfolio is zero-net-investment. **Every magnitude in
     this vein is gross, including the near-zero developed-market result, which is itself
     a pre-cost near-zero.** No performance expectation is imported from any of them.
 (ii) THE INSTRUMENT IS THE WORSE END OF THE PAPER'S MOST INFLUENTIAL DESIGN NODE.
     Representing an aggregate by a FUND rather than by a full-market aggregate cuts spread
     payoffs by roughly 0.13-0.16 pp/month -- two to three times lower -- because funds hold
     the large liquid names while the aggregates include the small and micro-cap names the
     authors call the primary source of return predictability. Fund-based designs also carry
     higher nonstandard errors: lower payoff AND noisier.
 (iii) RESTRICTING TO DEVELOPED MARKETS GIVES SPREAD RETURNS STATISTICALLY INDISTINGUISHABLE
     FROM ZERO, and this panel is nine developed indices. **Why that is not a D4 refusal:**
     the multiverse paper's unit is a long-SHORT spread, and Chan-Hameed-Tong find the effect
     lives almost entirely in the LONG leg -- "buying winner portfolios yields significant
     profits consistently, but selling loser portfolios creates either insignificant profits
     or losses". A spread can be near zero while its long half is not, and nothing in the
     multiverse paper measures the long leg. The discount refuses the spread; it cannot by
     itself refuse a long-only construction. Note that this INVERTS `program.md`'s standing
     caveat that long-only is a real constraint because only the cheap side is tradeable --
     here the tradeable side is the side the evidence is on, and that is the single best
     reason this object is worth one of tonight's trials.
 Also carried: the smaller-market gradient is confirmed twice 29 years apart, but Richards'
 eight-largest subgroup (close in composition to this panel) still shows a positive
 contrarian return at ~60% of the small-market one and the difference is NOT significant, so
 the correct statement is "the gradient runs against this panel", not "the effect is absent
 from it".

WHY THE CURRENCY CHANNEL IS NOT THE BET, AT THIS HORIZON SPECIFICALLY. The panel is
USD-converted and unhedged, so a USD aggregate score could be a currency sort. The USD
decomposition says it is not at short horizons: the equity-on-past-equity term is above 90%
of total profit at 1 week and above 80% at 2 and 26 weeks, with the currency-on-past-currency
and currency-on-past-equity terms small. The transferable rule is that a USD-denominated
aggregate score is cleanest at SHORT horizons and increasingly self-contaminating as the
horizon lengthens -- which independently explains why the one-month sort is the robust one.

FAMILY SLUG, AND IT IS DELIBERATELY THE CAPPED ONE. This is a cross-sectional momentum
sort, so it is `price-trend`, even though the research note that motivated it also tags
`lead-lag-spillover` and that family has one trial against `price-trend`'s eleven. Filing a
cross-sectional momentum book under a thinner family to dodge the 2-trial cap would be
gaming `program.md`'s allocation rule rather than following it. This is trial 1 of the
night's 2 permitted in `price-trend`, and no second one is planned.

CONSTRUCTION, AND EVERY INPUT IS A RATIO. Score = the 21-day price ratio, lagged one day so
the row emitted at a month-end uses only returns realized at or before it. No level, no
`dollar_volume`, nothing carrying the as-of-fetch back-adjustment factor. Funds are eligible
from their first price, so the sleeve grows from 5 eligible in 1997 to 42 by 2012; below 15
eligible funds the book holds the equal-weight eligible POOL rather than cash, per the
2026-10-15/16 rule that a candidate must not be scored against a fully-invested benchmark
while sitting out.

PRE-REGISTERED TURNOVER: a one-month sort over ~40 units with a top-fifth cut rotates most
of the book most months. At K = 8 of ~42 that is up to 8 replacements a month, i.e. of order
**train 4.0-9.0x and validation 5.0-14.0x** one-way. Funds sit in the cheapest liquidity
tier and carry no UK/HK/FR/IT/ES purchase tax if US-listed, so the ~19 bps-per-1x constant
measured on volume-shock books should NOT apply here and the ~11 bps-per-1x slow-book
constant is the better prior -- but both were measured on single-name books and neither is
imported as a forecast. D3 was evaluated on this basis and did not fire.

NO TRAIN SIGNAL STATISTIC WAS COMPUTED OR READ for this file; the only free screen run was
the count of eligible funds per year, which is a coverage measurement and decided the
warm-up threshold.
"""

from __future__ import annotations

import pandas as pd

from engine import data

K = 8                # top fifth of a ~42-unit sleeve
LOOKBACK = 21        # one month, the horizon both sources converge on
LAG = 1              # the score uses only returns realized at or before the row's date
MIN_UNITS = 15       # below this the sleeve is too thin to sort; hold the pool instead

STRATEGY = {
    "name": "pt_aggregate_unit_stmom",
    "family": "price-trend",
    "hypothesis": (
        "Holding the 8 eligible NON-STOCK instruments with the highest trailing 21-day "
        "return (lagged one day), equal-weighted and reformed monthly, with no peer quota so "
        "the region and asset-class bet is kept rather than neutralised, earns a validation "
        "Sharpe above the 90% quantile of 200 random selections built exactly like it from the "
        "same point-in-time pool, because at the AGGREGATE level the short-horizon "
        "cross-sectional signal is continuation while at the single-name level it is reversal "
        "-- a sign flip under change of aggregation unit, which makes it a different mechanism "
        "rather than the stock-level momentum this lab has already measured to null."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Top-K previous-month return among the eligible non-stock instruments, equal-weighted,
    monthly, un-neutralised. The aggregate unit is the point: no peer quota.
    """
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    # The aggregate sleeve, identified by instrument TYPE and never by id: no fund is named
    # anywhere in this file, so no hindsight selection of which units to rank is possible.
    units = pd.Index([c for c in prices.columns if str(kinds.get(c, "stock")) != "stock"])

    px = prices.ffill()
    score = px.shift(LAG) / px.shift(LAG + LOOKBACK) - 1.0

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible aggregate units BEFORE the cross-sectional sort.
        sc = score.loc[date].reindex(units.intersection(names)).dropna()
        if len(sc) < MIN_UNITS:
            # Warm-up: hold the pool rather than cash (2026-10-15/16).
            if not rows:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        picked = sc.nlargest(min(K, len(sc))).index
        if len(picked) < 4:
            continue
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
