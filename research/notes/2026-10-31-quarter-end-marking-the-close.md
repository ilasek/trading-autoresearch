---
title: "Quarter-end price inflation and marking the close — the leaning-for-the-tape hypothesis"
authors: Carhart, Kaniel, Musto, Reed
year: 2002
venue: Journal of Finance (Tier 1)
url: https://doi.org/10.1111/1540-6261.00438
citations: 362 (Semantic Scholar by DOI, checked 2026-10-31; Crossref `is-referenced-by-count` 321 for the same DOI, same date)
sample_period: 1985–1999 (daily fund returns Jan 1985 – Aug 1997; TAQ intraday 1993–1999; CDA disclosed holdings 1989–1995)
markets: US only — NYSE/AMEX/Nasdaq equities and US domestic equity mutual funds
tier: A
validation_overlap: false
published_post_2018: false
---

Read **in full** from the author-hosted PDF (`johnhcochrane.com/s/carhart_leaning_for_tape_JF.pdf`,
519 KB; `pdftotext -layout` → 100 KB of clean text, `" the "` count 609, no shift artifact, no
`( )` dropout).

This note opens the **quarter boundary**, which `SUMMARY.md`'s [2026-10-30] entry named as the
session's target: the folder has had the *month* boundary since 2026-09-02 and had never written
down the *quarter* one, which is the boundary the lab's own 2026-10-09/10 nightly measured a flow
concentration at. Per the folder's anti-lookahead rule, performance magnitudes below are recorded
as **cross-sectional ratios and orders of magnitude against this repo's cost floor**, never as
dated levels.

## Mechanism

A fund's net asset value is computed from the **closing** prices of its holdings. A manager who
buys, late in the session, stocks the fund already owns can therefore move measured performance
from the next period into this one without changing the portfolio. The practice is called *painting
the tape*, *marking up* or *portfolio pumping*; regulators treat it as illegal. The economic driver
is that **reporting dates are quarterly, not monthly**: quarterly and annual performance figures
are what investors, rankings and incentive pay respond to, and the flow–performance relation is
convex, so the manager with the strongest quarter has the most to gain from one more basis point.

The authors test two incentive stories and keep one.

- **Benchmark-beating** (mark up to finish above the index) is **rejected**: manipulation aimed at
  a threshold should dent the empirical distribution of annual fund returns just above the index
  return and just above zero, and no such distortion appears.
- **Leaning for the tape** (mark up to improve an already-good ranking, and to harvest the convex
  flow response) is **supported**: the period's *best-performing* funds show the largest period-end
  run-up and the largest next-day reversal.

So the cross-sectional conditioner is **who holds the stock**, not what the stock itself has done.
That distinction is the whole implementability question here, and section IV.C of the paper settles
it in the unfavourable direction: stocks in the disclosed portfolios of the top-decile funds are
more inflated at the period end **after controlling for capitalisation and recent return** — i.e.
the two price-only proxies a repo like this one could compute are explicitly partialled out of the
result, and the signal survives in the holdings residual.

Three further mechanism facts, all of which narrow the effect:

1. **It is an end-of-the-last-day effect, not a last-day effect.** Equity-price inflation is
   localised in the final half-hour before the close, with excess trade counts peaking in the last
   five minutes.
2. **It is monotone decreasing in capitalisation.** The smallest capitalisation quintile runs up by
   roughly an order of magnitude more than the largest, which is down to *a few basis points* at
   quarter ends — below one side of this repo's cheapest cost tier. Small stocks are cheaper to
   move, so they are the targets.
3. **The month boundary is not the quarter boundary.** The authors state it directly: there is
   "little or no effect at month-ends that are not quarter-ends", in the Lipper indices, in their
   own fund database, and in the fraction of funds beating the index. The quarter dummy and the
   month dummy are estimated jointly, so this is a contrast and not two separate regressions.
   Excess last-half-hour trading is large at quarter ends and insignificant at other month ends.

## Construction recipe

The paper's own design, stated so it can be reused rather than re-read:

- **Index time by period-end indicators, estimated jointly.** Regress the return series on
  `YEND`, `YBEG`, `QEND`, `QBEG`, `MEND`, `MBEG` — last and first trading day of year, of quarter
  other than the fourth, and of month other than a quarter-end. Estimating the three boundaries in
  one regression, with the month dummy *excluding* quarter-ends, is what makes the quarter-versus-
  month claim a contrast. The second specification they report replaces the three with
  `YEND`, `QEND` and `YEND+QEND+MEND`, which reads off the quarter's *incremental* effect over
  being a month-end at all. **Any quarter-boundary test should be built this way**, since a bare
  quarter dummy is confounded with the month effect the folder already has a note on.
- **Define the inflation statistic as a round trip, not a level**: a stock's inflation at a period
  end is its return on the last day of the period *minus* its return on the first day of the next.
  That differences out whatever drift is common to the two days and is twice the average one-way
  inflation. It is also the right object to price against costs, because capturing it requires
  both legs.
- **Control cross-sectionally before attributing.** Their holdings test sorts into 5×5
  capitalisation × past-six-month-return groups and goes long the top-fund-held names against the
  rest *within* each group, then standardises each group-year statistic by its own distribution
  over all other non-overlapping two-day windows in that year. The null is built from the rest of
  the same year, not from a model — a cheap and transferable device.
- **Breadth, not just mean.** They re-run the same regression with the *fraction* of funds beating
  the index as the dependent variable. A period-end claim that holds on the mean but not on the
  fraction is a tail story; checking both is cheap.

## Robustness evidence (qualitative only)

Multi-source rather than multi-market: the NAV pattern appears in two independent fund databases
and in the cross-sectional breadth measure; the price pattern appears in intraday transaction data;
the trading pattern appears in trade counts; and the holdings test ties it to specific funds. The
authors note the quarter-end result was novel at the time and is not a projection of the
pre-existing year-end literature. Against that: **the sample is a single market** (US) and ends in
the 1990s, there is acknowledged survivor bias in the early years of one fund database, and the
paper is not a replication study in the Hou–Xue–Zhang or Jensen–Kelly–Pedersen sense. The
mechanism is a *regulated* one, which is the strongest reason to expect decay — a practice that is
illegal and detectable can be deterred, and the companion note
(`2026-10-31-tape-painting-buying-versus-selling.md`) documents exactly that: the composition of
the behaviour shifted from the easily detected form toward a harder-to-detect one. Treat any claim
about the effect's *current* size as unsupported by this source.

## Implementability here

**Verdict: this channel fails this repo's pre-committed admission criterion on two of its three
clauses, and the failure is structural rather than a matter of degree.** The criterion
(`SUMMARY.md` [2026-10-30]) asked for (a) a quarter effect distinct from the month effect, (b) a
*cross-sectional* construction, (c) a mechanism whose signal needs no fundamentals, holdings, flow
or short-interest data.

- **(a) passes, and passes cleanly.** This is the source the folder was missing: the quarter
  boundary is a different object from the month boundary, demonstrated as a joint contrast in two
  databases. The institutional reason — reporting and ranking dates are quarterly — is different in
  kind from the month-end payment-and-settlement cycle in
  `notes/2026-09-02-turn-of-month-payment-cycle.md`, not a relabelling of it.
- **(b) fails as published, and this is the decisive one.** The cross-section the effect lives on is
  *funds*, and the stock-level version is identified **only** in the holdings residual, with
  capitalisation and recent return controlled out by construction. A price-only tilt toward
  "small, high-past-return names at quarter ends" is precisely the variation the paper removes
  before finding its result.
- **(c) fails with (b)**: the signal is disclosed holdings, which this repo does not have and
  cannot construct.
- **Protocol v3 closes the remaining crack independently.** The effect is in the last half-hour
  before the close and reverses the next day. Under v3 a row emitted on date `d` fills at each
  name's **next real close**, so a close-to-close book cannot be inside the final half-hour of the
  quarter at all; it can only buy *after* the run-up has printed and sell into the reversal. This is
  the sign-inverted version of the trade. The folder's 2026-08-30 finding that the execution lag
  costs a daily effect most and a monthly effect least bites at its maximum here.
- **The panel objection, which the criterion asked to be checked, is confirmed.** The inflation is
  monotone decreasing in capitalisation and reaches a few basis points in the largest quintile.
  This repo's nine indices (S&P 500, DAX, CAC 40, FTSE 100, SMI, AEX, Euro Stoxx 50, Nikkei 225,
  Hang Seng) are **all large-cap**, so the panel sits where the source itself measures the effect
  as smallest — and a few basis points of two-day round trip is below a single side of the 15 bps
  cheapest cost tier, before the UK and Hong Kong stamp duties that v3 charges on exactly two of
  these nine markets. The criterion's abandonment clause is met: the effect is concentrated in a
  segment this panel excludes by construction, so a null here would be **uninformative**, not
  evidence against the literature.

**What is worth keeping is free and methodological, not a book:**

1. **The joint-dummy specification** (`YEND`, `QEND`, `MEND` with the month dummy excluding
   quarter-ends, plus the `YEND+QEND+MEND` re-parameterisation). Any future calendar screen in this
   lab should use it, because it is the only form in which "the quarter boundary matters" is
   separable from "the month boundary matters". The lab's own 2026-10-09/10 measurement compared
   the month after a quarter-end against *other months* — a pooled contrast that cannot tell the
   two boundaries apart.
2. **The round-trip inflation statistic** (last day of period minus first day of next) as the unit
   of any period-end measurement, in place of a one-sided window return.
3. **The within-year empirical null** (standardise a two-day statistic by its own distribution over
   all other non-overlapping two-day windows of the same year). This is a cheap, assumption-light
   alternative to a bootstrap for any short-window calendar claim, and it is computable on train
   without a trial.

**Do not spend a trial on this.** If a human later wants the vein tested anyway, the only form that
is both legal under the hindsight guard and reachable under v3 is a *fully-invested cross-sectional*
tilt at quarter ends built from price and volume alone — and this source is evidence that such a
tilt is the part of the variation that was controlled away. Price the depth loss first, per the
lab's standing secondary-selection screen.

## Related

- `notes/2026-09-02-turn-of-month-payment-cycle.md` — the **month** boundary, and the contrast this
  note's joint specification is designed to draw against it. Ogden's payment cycle and this paper's
  reporting cycle are different mechanisms with different periodicity; the folder now has both.
- `notes/2026-10-31-tape-painting-buying-versus-selling.md` — the trade-level decomposition of the
  same behaviour, which both corroborates it and removes the price-only proxy.
- `notes/2026-10-31-quarter-ending-month-momentum-seasonality.md` — the one source that proposes a
  *price-only, fully-invested* construction on this boundary, and which is in direct tension with
  the companion note's window-dressing test.
- `notes/2026-10-31-nav-inflation-outside-the-us-china.md` — a second-market test of this exact
  design, including the quarter-versus-month contrast.
- `experiments/learnings.md` 2026-10-09/10 — the lab's own quarter-boundary flow measurement, and
  its reason for declining it (a timing construction forfeits the equity premium under v3);
  2026-10-15/16 — the fully-invested version of that timing idea, measured and closed on turnover.
- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` — the execution-lag asymmetry that makes
  a last-half-hour effect unreachable here.
