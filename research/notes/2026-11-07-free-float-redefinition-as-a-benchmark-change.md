---
title: "Global versus Local Asset Pricing: A New Test of Market Integration"
authors: Hau
year: 2011
venue: Review of Financial Studies 24(12), 3891–3940 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhr094
citations: 42 (Crossref `is-referenced-by-count`, checked 2026-11-07)
sample_period: event windows around December 2000, with two years of prior weekly returns for covariance estimation; the staged implementation ran to 2002
markets: 2,291 stocks across developed and emerging markets worldwide (from 2,566 in the old or new MSCI ACWI), excluding Argentina and Turkey
tier: A — tier-1 venue, published version of record read in full, identification from a rule change rather than from a discretionary event, and the paper builds and tests an explicit alternative (speculative front-running) against its own hypothesis
validation_overlap: false (event is 2000–2002)
published_post_2018: false
read: full text, published version of record (517 KB PDF, 51 pages → 189 KB of clean text, 1,050 instances of `" the "`, zero `( )` dropout)
---

## Access

Read from the **University of Geneva's Archive ouverte** (`archive-ouverte.unige.ch`), which holds
this closed RFS article as a **published version** under the publisher's policy. The mechanic worth
copying: the record page is a **661 KB Angular shell** with no `.pdf` href in it, exactly the
2026-10-10 `repository.arizona.edu` shape — but the file path is sitting in the page's
**`<meta name="citation_pdf_url">`** tag, pointing at
`access.archive-ouverte.unige.ch/access/metadata/<uuid>/download`. So for a DSpace-era repository,
**grep the landing page's citation meta tags before grepping for bitstream UUIDs**: the page also
contained ten bare UUIDs, only one of which was the document. This generalises the 2026-10-13
EDHEC lesson (read a landing page's meta tags before concluding it holds nothing) from *abstracts*
to *files*.

OpenAlex named this location in its `locations[]` list and reported `oa_status: green` with
`oa_url` pointing at **SSRN**, a known refusal. Reading the `locations` list rather than the
`oa_url` is what worked — the third confirmation of the 2026-10-10 lesson.

## Mechanism

This paper is in this folder for a reason one step removed from its own title. Its subject is global
versus local risk pricing; its **instrument** is an index provider's weighting rule changing, and
the chain of reasoning from "the rule changed" to "betas moved" is the cleanest statement this
folder has of *why an index rule is an asset-pricing object at all*.

The argument runs:

1. **Index capital is not optimising.** Some capital tracks fixed index weights and does not
   re-optimise. The remaining capital — the actively managed residual — is what the market
   benchmark actually consists of.
2. **So an index revision is a shock to the benchmark itself.** When index-tracking capital
   reallocates, the residual supply held by optimising investors changes. The benchmark change is
   proportional to the **weight change vector** `w_new − w_old`, which is observable.
3. **A benchmark change moves every beta.** A stock's CAPM beta is proportional to the covariance of
   its return with the benchmark return, so changing the benchmark changes betas mechanically, with
   no change in cash flows.
4. **Moved betas move prices.** A beta change moves the discount rate, so with expectations held
   fixed, stocks whose beta rises should take a negative announcement return and vice versa.

That makes the test an asset-pricing test **"in differences"**: it needs only the benchmark
*change*, never a specification of the benchmark level, which sidesteps the joint-hypothesis problem
of testing a pricing model and a benchmark choice at once.

The rule itself. MSCI's December 2000 redefinition of the All Country World Index did two things,
both **rule-based and involving no judgment about a company's prospects**, which is precisely why
the weight changes were computable in advance by anyone who anticipated the rule:

- **Weights moved from market capitalisation to free float.** MSCI defines free float as the share
  of outstanding stock available to international investors, and — because disclosure does not
  identify "strategic" holdings — implements it by **classifying holders**: households, investment
  and mutual funds, unit trusts, pension funds, insurers, social-security funds and brokers count as
  free-floating; governments, corporates, banks excluding trusts, principal officers, board members
  and employees do not. So the operative variable is **ownership concentration**, driven mostly by
  long-term family and state stakes.
- **Market representation was raised**, from a 60% capitalisation-based target to an **85%
  free-float-adjusted target within each country and industry**.

Together these added 489 stocks, removed 298, and changed weights for thousands, with a **median
absolute country-level weight change of about 42%**.

The paper's second mechanism is the one that makes it methodologically useful: **the announcement
is anticipated, and the anticipation leaves its own footprint in the cross-section.** MSCI ran a
public consultation before announcing, and a competitor had already adopted float weights, so
speculators could and did build positions in advance. A mean–variance speculator trades off
expected return against arbitrage risk, and the optimal arbitrage portfolio decomposes into a
**return-seeking** component and a **risk-hedging** component. The hedging leg generates a *second*,
transitory, correlated return pattern across names — one that has nothing to do with the beta
change being tested. Identification therefore requires controlling for the hedging footprint, and
the paper reports that the speculative model including hedging demand fits the cross-section
materially better than the alternatives, with both components significant in the run-up.

## Construction recipe

The reusable parts are two, and neither is a trading signal:

**(a) Turning a rule change into predicted beta changes.** Given the old and new weight vectors and
a return covariance matrix estimated over a prior window (here two years of weekly returns across
all index stocks), compute each stock's beta against the old and the new benchmark and take the
difference. Separately compute the beta change against *alternative* candidate benchmarks — the
global index, the national market, developed versus emerging partitions — and let the cross-section
of event returns decide which benchmark's beta change explains them. Requirements the paper is
explicit about: two years of prior price history per name, and enough weekly observations (its
threshold was 80, loosened to 40 as a robustness check) for the covariance matrix.

**(b) Separating the pricing effect from the front-running effect.** Define *two* event windows, not
one: a **position-buildup window** ending at the first announcement (tried at 5, 10, 15 and 20
trading days) and a **hedge-liquidation window** starting after it (3, 5, 7 days). The buildup
window carries the arbitrageurs' entry; the second carries their unwind. Both the return-seeking and
the risk-hedging components enter the cross-sectional regression. The lesson that transfers: when a
*known, dated, rule-driven* flow is coming, the cross-section around it contains an arbitrage
footprint that is **not** the effect of interest, and its sign and timing are different from the
effect's.

## Robustness evidence (qualitative only)

- **Four segmentation hypotheses tested, not one.** National-market segmentation is rejected;
  global integration cannot be rejected. Developed/emerging segmentation also fails — weight changes
  of *developed*-market stocks have a significant return impact on *emerging*-market stocks, in line
  with their global beta changes.
- **Where segmentation does survive.** Emerging-market stocks that are **neither cross-listed nor
  liquid** do show segmentation; cross-listing (in the US or UK) and higher liquidity each go with
  global pricing. So the headline "priced globally" is a **developed-market and liquid-stock**
  statement, and the paper says so.
- **Sample-construction robustness.** Reinstating the two excluded currency-peg countries, and
  loosening the minimum-observation threshold, each expand the sample and are reported as
  qualitatively unchanged. Event-window boundaries are varied and reported as not qualitatively
  decisive.
- **Honest about what the design cannot do.** The whole result rests on the index revision being
  uncorrelated with other risk factors — defensible over short windows, and stated as the assumption
  it is.
- **Citation caveat.** 42 Crossref citations is modest for a tier-1 article of this vintage; the
  venue, the published-version read and the alternative-hypothesis discipline carry the A, not the
  count.

## Implementability here

**No candidate can be built from this.** The weight vectors, the free-float classification and the
announcement dates are all outside the contract, and there is no index-revision event in this
repo's visible panel to trade. What it changes is how two things the lab already does should be
read.

**1. It is evidence against country-grouping as a risk-pricing device — and that sits in tension
with a measured result in `experiments/learnings.md`, so state the tension rather than pick a
side.** Hau rejects segmentation along national markets for developed-market stocks: a global
benchmark's beta change explains the cross-section, a national one's does not. This repo's panel is
eight developed-market national indices plus the S&P 500 — exactly the population the finding
covers. But `experiments/learnings.md` records the lab *measuring* region-relative scoring beating
sector-relative scoring on an illiquidity score, with the stated mechanism that venue properties
(tick size, lot size, settlement, listed float) set a score's regional level.

These are compatible, and the resolution is worth writing down because it is a reusable
distinction: Hau is about **where risk is priced** (which benchmark's covariance earns a premium);
the lab's finding is about **where a characteristic's measurement units live** (which grouping to
demean a score by so that the score means the same thing for every name). Region-demeaning an
*illiquidity* score is a units correction and Hau says nothing against it. Region-demeaning an
*expected-return* or *beta* estimate is a segmentation assumption, and Hau is evidence against it
for developed-market names. A candidate that country-neutralises its **risk model** is making the
claim Hau rejects; one that country-neutralises its **signal construction** is not. Note also the
blunter constraint: under protocol v2 a candidate cannot read `data/universe.yaml`, so the region
labels those learnings were measured with are not available to new code in any case.

**2. It gives a mechanism for why "newly eligible" is not a clean event in this panel.** The
`eligible` panel's first `True` for a column is an index addition, and this paper says such a change
moves the name's beta against the benchmark through the residual-supply channel, with an
**anticipatory arbitrage footprint before the date and an unwind after it**. Any candidate
conditioning on time-since-first-eligible is sampling a window that contains a transitory
front-running pattern on top of whatever persistent effect it hopes to capture. The practical
instruction, which is cheap: if a candidate keys on newly-eligible names, **skip a window around the
eligibility date rather than trading into it**, and state the skip length as a design choice. This
is the skip-month logic the momentum literature already imposes, arriving for an unrelated reason.

**3. Liquidity and cross-listing are the moderators, and one of them is observable.** Hau's
segmentation survives only among illiquid, non-cross-listed emerging names. This panel holds
**large-cap developed-market index members**, so by construction it sits on the globally-priced side
— which is a reason to expect **less** cross-sectional payoff from region conditioning here than the
international-asset-pricing literature's full-universe results would suggest. Dollar volume is in
`aux` and is the one moderator a candidate can actually measure.

**Pitfall.** Do not read "markets are globally integrated" as "a global factor model will fit this
panel well". The finding is about which benchmark's *beta change* prices a *rule-driven* shock over
days. It is not a claim about the `R²` of a global model at monthly horizons, and the
counting-factors notes in this folder are the right place for that question.

## Related

- `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` — the same object with
  the rule held fixed instead of changing; Greenwood's conjecture that arbitrary weighting is costly
  is what float adjustment was a response to.
- `2026-11-07-index-addition-comovement-across-forty-national-indices.md` — the third side: what
  admission to a non-US national index does, across six of this panel's nine indices.
- `2026-09-10-country-demeaned-versus-country-mean-characteristics.md`,
  `2026-09-10-country-industry-global-return-decomposition.md`,
  `2026-08-28-local-versus-global-factor-construction.md`,
  `2026-11-01-anomalies-across-the-globe-country-neutral.md` — the folder's existing country-grouping
  cluster, which this note qualifies rather than overturns.
- `2026-10-09-index-inclusion-demand-curves-vs-price-pressure.md`,
  `2026-10-09-index-premium-and-the-index-turnover-cost.md` — the demand-curve side of index events.
- `2026-09-22-limits-of-arbitrage-performance-based.md`,
  `2026-09-22-arbitrage-risk-substitute-portfolios.md` — the arbitrage-risk trade-off the hedging
  component here is an instance of.
- `2026-10-27`'s long-memory cluster and the counting-factors notes
  (`2026-09-27-counting-factors-eigenvalue-estimators.md`) — where the "does a global model fit"
  question actually belongs.
