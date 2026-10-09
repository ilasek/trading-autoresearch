---
title: "Do Demand Curves for Stocks Slope Down? — with: Price and Volume Effects Associated with Changes in the S&P 500 List: New Evidence for the Existence of Price Pressures"
authors: Shleifer; Harris & Gurel
year: 1986; 1986
venue: Journal of Finance 41(3), 579–590 (venue tier 1); Journal of Finance 41(4), 815–829 (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.1986.tb04518.x ; https://doi.org/10.1111/j.1540-6261.1986.tb04550.x
citations: "Shleifer: 1187 (Crossref is-referenced-by-count, checked 2026-10-09); 1453 (Semantic Scholar, same date). Harris–Gurel: 587 (Crossref, checked 2026-10-09)"
sample_period: "Shleifer: S&P 500 additions 1966–1983, with the event tests run on the post-September-1976 subsample (246 firms after exclusions). Harris–Gurel: all S&P 500 list changes 1973–1983 (228 additions, 194 usable), with the price tests concentrated on the 84 additions of the sample's second half"
markets: US equities (S&P 500 index changes), CRSP daily
tier: A for both — top-tier venue, four-figure and high-three-figure citation counts, the founding pair of a literature with dozens of independent replications in other indices and other countries
validation_overlap: false
published_post_2018: false
---

## Mechanism

Both papers ask one question with one experiment, and they are the reason the question is
interesting: **does a purely mechanical, publicly-announced, information-free shift in demand
for a share move its price?** Index membership is the clean instrument, because the index
provider states that investment appeal plays no part in selection — Harris and Gurel quote
S&P's own line, *"Judgements as to the investment appeal of the stocks do not enter into the
selection process"* — while index funds are obliged to buy the added name and sell the deleted
one regardless of what they think of it.

Three hypotheses are on the table, and the two papers separate them the same way:

- **Horizontal demand (the EMH corollary).** Stocks are close substitutes; a large uninformed
  purchase moves nothing. Predicts **no price effect at all**.
- **Imperfect substitutes / downward-sloping demand (the "DS" or "ISH" hypothesis).** Long-run
  demand for an individual share is not perfectly elastic, so an outward shift in demand clears
  at a **permanently** higher price. Predicts a price rise with **no reversal**.
- **Price pressure (the "PPH").** Long-run demand *is* elastic, but the investors who
  accommodate an immediate demand shock must be paid for the inventory risk and transaction
  costs of trading when they otherwise would not. Predicts a price rise that is **fully
  reversed** once the liquidity suppliers have re-established their positions.

The distinguishing test is therefore not the jump — all three parties agree there is a jump —
but **what happens over the following weeks**. That is the whole fight, and the two papers,
published three months apart in the same journal on overlapping samples of the same event, came
to opposite answers.

**Shleifer's answer: it persists.** Abnormal returns on the announcement date average close to
+3%, and the cumulative abnormal return starting at the announcement is still ~1.9% after ten
trading days and ~1.8% after twenty, with the point estimates showing no continuing decline past
day eleven; the cumulative measures lose significance only because their standard error grows,
not because the mean reverts. He reads this as supporting downward-sloping demand.

**Harris and Gurel's answer: it reverses.** The day-1 excess return is +3.13% (t = 13.95, with
96% of names positive), and the cumulative excess return from day 2 onward is −1.74% by day 11
and −2.49% by day 21, each individually significant and negative for roughly two-thirds of
names. Two tests — a t-test of "cumulative reversal equals minus the day-1 return" and a
Bayesian posterior-odds comparison of *no reversal* against *full reversal* — both favour full
reversal; the posterior odds on no-correction fall below 0.07 for every horizon past fifteen
days. They read this as supporting price pressure and as inconsistent with both the EMH and the
imperfect-substitutes story.

**Why both are Tier A and the tension is live.** This is not one careful paper against one
sloppy one. The samples overlap but are not identical (Shleifer 1966–1983 with event tests from
September 1976; Harris–Gurel 1973–1983 with price tests on the 1978–1983 half), the event-study
machinery is the same Fama–Fisher–Jensen–Roll market-model residual in both, and each paper
anticipates the other's objection. The honest summary of what the pair establishes jointly is
the part they agree on: **a publicly pre-announced, information-free demand shock of a few
percent of shares outstanding moves a large-cap share price by about three percent on the day.**
Whether that is a new equilibrium price or a rent paid to liquidity suppliers is the part they
do not settle, and later work (see the two companion notes) finds that the answer is not a
constant.

Both papers also supply the same corroborating fact, and it is the one that makes the
demand-side reading hard to escape: **the effect is absent in the early part of each sample and
present in the later part, tracking the growth of indexed assets.** Shleifer splits his
post-1976 window and finds the announcement return rising across the halves (2.27% then 3.19%,
with a one-sided test rejecting equality at 98%); Harris and Gurel find the day-1 volume ratio
rising from 1.21 (t = 0.81) in the first half of their sample to 2.81 (t = 7.16) in the second,
and the price effect present only in the second half. An information story has no reason to
depend on how much money tracks the index; a demand story must.

## Construction recipe

Neither paper is a strategy, but both hand over measurement machinery that is directly reusable:

**The event definition.** The event is the **announcement**, not the effective date. Shleifer is
explicit that the usable sample begins in September 1976 only because that is when S&P started a
notification service with a datable announcement; before that he has to use newsletter mailing
dates and treats the earlier results as unreliable. The lesson transfers: *the date a membership
change becomes public is a different date from the date it takes effect, and a membership panel
usually records the latter.*

**The volume-shock statistic (Harris–Gurel).** Their volume ratio is a clean, fully causal,
scale-free measure of abnormal turnover that needs nothing but a volume panel:

    VR_it = (V_it / V_mt) · (V_m· / V_i·)

where `V_it` is name *i*'s volume in event period *t*, `V_mt` is total market volume in the same
period, and the dotted terms are the corresponding averages **over the eight weeks preceding the
event window**. It is a per-name volume divided by its own trailing norm, with the market's
contemporaneous volume divided out, so its expected value is 1 under no change. The market
division is what makes it usable in a panel: it removes market-wide volume regimes without
estimating anything. The eight-week trailing window is their choice, not a derived optimum.

**Control for the event's own risk change.** Shleifer estimates the market model *separately
before and after* the inclusion rather than pooling, on the grounds that index membership may
itself change a name's beta. He reports that pooling made little difference in his sample, but
the construction is the right default when the event is suspected of changing comovement.

**Sample hygiene that matters more than it looks.** Shleifer drops 13 firms whose inclusion was
"perfectly anticipated" (regional telephone companies added in 1983, re-inclusions after a name
change following a merger) and 17 added in a single bulk index revision. Harris and Gurel drop
additions that were mergers with a deleted firm, and treat their deletions sample as
uninterpretable because six of the few usable deletions were utilities clustered on one date.
**Bulk revisions, index-internal reshuffles and re-entries are not the same event as an ordinary
addition**, and a panel built from membership files contains all of them undistinguished.

## Robustness evidence (qualitative only)

- **Replication breadth is the strongest part of this literature's case.** The same event study
  has been run on other US indices, on index families outside the US, and on index changes with
  different selection rules, and a price effect at the announcement is found in the great
  majority of them. The founding result is not a single-sample artifact.
- **The two primaries disagree on permanence on overlapping data**, which is the single most
  important qualitative fact here and the reason no number from either should be carried as a
  prior for "the permanent part". Later work treats both short-run and long-run components as
  real but of different sizes, and finds the split varies with the index, the name and the level
  of indexation.
- **Both papers' own subsample evidence says the effect is a function of how much mechanical
  money tracks the index** — it is not a constant of nature, it is a function of market
  structure, and market structure moves.
- **The deletion side is far weaker evidenced than the addition side in both papers.** Harris and
  Gurel say so outright (small sample, clustered, dominated by names leaving because of merger or
  bankruptcy rather than by an index decision). Any symmetry assumption between additions and
  deletions is an assumption, not a finding — and the companion note on the asymmetry debate
  records that it is still contested.
- **Shleifer's own discrimination against the rival stories is partial and he says so.** His
  certification test (do added names without S&P bond ratings, or with low ones, earn more?)
  finds nothing; his liquidity test (do less-known names — non-Fortune-500 entrants — earn more?)
  finds nothing. These are two specific informational stories rejected, not the information
  hypothesis as a class.

## Implementability here

**Read this section as a statement about the panel, not about a trade.** Under protocol v2/v3
this repo's universe *is* point-in-time membership of nine maintained indices, so index additions
and deletions are not an exotic event for the lab to go looking for — they are the mechanism that
creates and destroys the columns of the `eligible` panel. Every entry into the panel is one of
these events, and so is every exit.

**What is reachable.** The `eligible` frame is dates × names and boolean, so a candidate can
compute, with no extra data and no hindsight, each name's **first eligible date** and hence its
*seasoning* — how long it has been in the panel as of the rebalance date. That is the only piece
of the event the panel contains, and it is free.

**What is not reachable, and this kills the event trade outright.**
1. **The announcement date is not in the panel.** Both papers are emphatic that the event is the
   announcement and that mis-dating it destroys the result — Shleifer throws away his entire
   pre-1976 sample over exactly this. An eligibility flag records when a name *became tradeable
   in the index*, i.e. something at or after the effective date. By then the announcement window
   both papers measure has already passed.
2. **Protocol v3 fills at each name's next real close.** The effect both papers measure is a
   one-day move, and Harris and Gurel's own footnote reports that much of it accrues between the
   announcement and the next open. A signal that can first see the event on the effective date
   and then fills a day later is two fills late on a one-day event.
3. **Shares outstanding are not in the data.** The demand shock in both papers is sized as a
   percentage of shares outstanding; this repo has price and volume, not share count. Any
   "size of the shock" conditioner here must be proxied (trailing dollar volume is the obvious
   one) and the proxy is not the quantity the papers model.

**What *is* worth building, and it is a screen rather than a signal.** If a freshly eligible name
has, on average, just experienced a positive abnormal move of a few percent — whether that move
persists or reverses — then the set of names in their first weeks of eligibility is not a random
sample of the panel, and **any cross-sectional score the lab computes is being computed partly on
that non-random set**. Two consequences, both measurable on train for zero trials:

- A **seasoning screen** (exclude names eligible for fewer than *k* months from the selection
  set) is a one-line, hindsight-free change to any existing construction. Under the price-pressure
  reading it avoids buying into a rent that is about to be paid back; under the downward-sloping
  reading it costs nothing but a handful of names. It is cheap precisely because the two Tier-A
  sides disagree about the sign of what it avoids but agree it is not a reason to *buy*.
- The **mirror case cannot be screened**: the engine zeroes weight on a name the day it stops
  being eligible, so every holding that leaves the panel is sold at whatever the deletion
  mechanism did to it. A candidate cannot opt out of that, and neither can the equal-weight pool.

**The pitfall to flag loudest.** Harris and Gurel's sample-hygiene step — dropping bulk index
revisions and index-internal reshuffles — is unavailable here, because the panel does not say
*why* a name became eligible. Nine indices with staggered start dates (S&P 500 from 1996, the
other eight from 2009) means the panel's early years contain large synthetic entry cohorts that
are an artifact of when data coverage begins, not index events at all. **A seasoning variable
computed near a tracked index's coverage start date is measuring the data vendor, not the
market.** Any train-period use of it has to exclude the first year or two after each index's
start, and `program.md` already warns that pre-2009 coverage is the thin part of the panel.

## Related

- `2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the other half of the index-
  membership story, and the complement to this one. That note is about selecting a universe on
  **end-of-period** membership, which protocol v2 fixed. This note is about the **flow of entries
  and exits inside** a correctly point-in-time universe, which v2 did *not* fix and cannot: the
  index effect is a property of how the real index is maintained, not of how the data was
  sampled. Cai–Houge's long-horizon Russell result in that note is the closest prior pointer to
  the present one.
- `2026-10-09-index-premium-and-the-index-turnover-cost.md` — the magnitude, the cross-sectional
  determinants, and the closed-form cost this imposes on a mechanical index tracker, which is
  what the v3 equal-weight eligible pool is.
- `2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — what happened to the
  Shleifer/Harris–Gurel effect as indexation grew, and why the answer is not the one either paper
  would have predicted.
- `2026-09-07-high-volume-return-premium.md`, `2026-08-31-amihud-volume-component-decomposition.md`
  — Harris and Gurel's volume ratio is an earlier and simpler member of the same family of
  trailing-normalised volume shocks these notes cover.
- `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — index deletion and delisting
  are different events that both end a column; a deleted name usually keeps trading, a delisted
  one does not. The lab's v3 delisting stress (30% haircut on a series that ends) is calibrated
  for the second and is not a model of the first.
