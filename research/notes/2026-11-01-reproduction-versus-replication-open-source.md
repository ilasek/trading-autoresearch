---
title: "Open Source Cross-Sectional Asset Pricing"
authors: Chen, Zimmermann
year: 2022
venue: Critical Finance Review 11(2), 207–264 (Tier 2 — a peer-reviewed journal, but not one of the rubric's named Tier-1 outlets; the authors' track record in this exact area is Tier-1, see Related)
url: https://doi.org/10.1561/104.00000112 · full text read from https://cfr.ivo-welch.info/published/papers/chen2021open.pdf
citations: 384 (Crossref `is-referenced-by-count`, checked 2026-11-01). Semantic Scholar's DOI endpoint returns `Paper with id DOI:10.1561/104.00000112 not found` (checked 2026-11-01) — a real, heavily-cited article, so this is that API's known clean-`not found` failure mode, not an indexing fact. OpenAlex not consulted (budget spent on locating a different source's green copy).
sample_period: "No single estimation window. Every reproduction test is run on **the original paper's own sample period** for that predictor — earliest start in the 1920s, most original samples ending in the 1980s–2000s. The released dataset itself extends to the project's data vintage, but none of the evidence this note records comes from the extension."
markets: US common stocks (CRSP/Compustat, plus IBES and OptionMetrics for some signals); 319 firm-level characteristics drawn from the prior meta-studies, 205 of them classified as testable predictors
tier: B+ — a genuine large-scale reproduction with fully public code and data, hand-collected original t-statistics open to inspection, and candid about its own residual errors; held below A only on venue and because it deliberately does **not** address net-of-cost profitability (it says so, and names the paper that does).
validation_overlap: false
published_post_2018: true
---

## Access

Read in full from **`cfr.ivo-welch.info/published/papers/chen2021open.pdf`** — the *Critical
Finance Review*'s own editor-hosted copy of its published articles, served on the first try
(3.2 MB; `pdftotext -layout` → 186 KB of clean text, 615 instances of `" the "`, zero `( )`
dropout, no ASCII shift). This is a **new channel of a shape this folder keeps rediscovering**:
the journal's editor runs a flat `/published/papers/<author><year><slug>.pdf` directory, so for a
*Critical Finance Review* article try the editor's site before the publisher's. `papers.ssrn.com`
and the Now Publishers / Emerald endpoints were not attempted, both being on this file's dark list.

## Mechanism

This is not a note about a strategy. It is a note about **a distinction the replication debate
turns on**, and about **the elasticity of a measured cross-sectional result to three construction
knobs**. It is the third corner of a triangle this folder already holds two corners of:
`2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` (the pessimistic reading) and
`2026-08-25-hierarchical-bayesian-factor-replication.md` (the optimistic one).

**The distinction: reproduction is not replication.** Following Welch's terminology, the authors
separate (i) **reproduction** — same data, same sample, same method as the original paper — from
(ii) **scientific replication** — a different sample, population, or a uniform method applied to
everything. The two questions have different answers, and conflating them is how a literature can
be reported as 35%-replicable and 100%-reproducible at the same time without anyone lying.
Reproduction asks *did the original authors compute what they said they computed*; replication asks
*does the effect exist under a construction I chose*. **Only the second is relevant to a research
lab deciding what to build, and only the first is relevant to whether a paper is honest.**

**The reproduction answer is near-unanimous.** Writing code from the text and exhibits of the
original papers (not from author-supplied code), the authors reproduce 319 characteristics. Of the
161 they classify as **clear predictors** — the original paper showed unambiguous significant
long-short predictability — 158 clear `|t| > 1.96` on the original sample, and one of the three
misses reaches 1.93. A regression of reproduced t-statistics on hand-collected original
t-statistics has a **slope of 0.88 and an R² of 82%**: the reproductions do not merely clear a
threshold, they land near the original *magnitudes*. Mean returns are near-monotonic in the
signal decile (the probability that decile *k* beats decile *k−2* is roughly 96%).

**The misclassification mechanism — why the pessimistic count is large.** The authors trace their
disagreement with the pessimistic study not to construction but to **what counts as a claim**. That
study analyses 452 "anomalies" which derive from only **240 characteristics** (212 of the 452 are
the same strategy at a different rebalancing frequency), and of those 240 only **118 showed clear
long-short significance in the original paper at all**. The authors reproduce 117 of those 118
above 1.96. So a large part of a headline "replication failure" rate is **arithmetic on a
denominator that includes claims nobody made**: variables the original study reported as
insignificant, variables never tested for return predictability, and duplicate holding periods.
The general lesson is about **how a denominator is built**, and it transfers to any count of
"how many of our ideas worked".

**The construction elasticity — the part this lab can use.** Three knobs, each measured as a
cross-predictor distribution rather than as one number:

1. **A liquidity screen costs about one third of the gross.** Imposing *any* of a
   large-exchange-only screen, a market-equity floor at the 20th percentile of NYSE size, or
   value-weighting in place of equal-weighting moves the typical in-sample long-short mean return
   from roughly 60 bps/month to roughly 40 bps/month. The authors stress that the three very
   different-looking adjustments have **near-identical effects** — they are all the same
   intervention, which is *removing the small and illiquid tail from the sort*. A share-price floor
   is the one soft version.
2. **Costs cost about another third, independently.** The authors decline to claim implementable
   profits and name the cost study instead: effective bid-ask spreads remove roughly another third
   of in-sample mean return, even after cost mitigation.
3. **Performance declines monotonically as the rebalance interval lengthens** from 1 to 3 to 6 to
   12 months, with the mechanism stated plainly — less frequent re-assignment means less exposure
   to the signal. Monthly re-sorting beats the original specifications because many originals
   follow the annual-June convention.

**The timing convention, which is the one place this paper is behind this repo.** The portfolios
"implicitly assume data at the end of month *t* can be used to make trades in closing auctions on
the last day of month *t*", and a footnote concedes that the hypothetical traders would themselves
add demand to those closing auctions, raising the buy price. **This is exactly the convention
protocol v3 abolished.** A careful, fully-open reproduction of the entire literature is built on a
same-close fill — which is evidence that the convention is the literature's default rather than
one study's slip, and therefore that *every* gross magnitude quoted from this literature is quoted
under a fill this repo does not get.

## Construction recipe

Not a strategy recipe; a **measurement** recipe, and the pieces worth copying are the defaults:

1. **Sign the portfolio, not the characteristic.** Keep raw characteristics unsigned and apply the
   original study's claimed direction at the portfolio step, stored as data. This keeps the sign
   convention auditable and separable from the signal.
2. **Delay every screen to the portfolio-formation step, not the signal step.** Build the signal
   from all names, then apply the liquidity screen, the weighting and the quantile cut when forming
   portfolios. This is what makes a screen's price measurable at all — with the screen baked into
   the signal there is no counterfactual.
3. **Default construction**: quantile sort (the original paper's quantile where stated, otherwise
   quintiles/deciles), monthly re-assignment, the original paper's weighting, long-short.
4. **Hand-collect the target.** For every signal, record the original paper's key table, the exact
   test, the claimed sign, the claimed t-statistic and the sample window — *before* reproducing it.
   The comparison that carries the paper's weight (slope 0.88, R² 82%) is only possible because the
   target was written down first. **This is a pre-registration discipline in replication clothing.**
5. **Classify claims by the strength of the original evidence** into clear predictors, likely
   predictors (borderline or multivariate-only evidence), not-predictors (the original found
   nothing), and indirect signals (variations someone else constructed). Apply the `|t| > 1.96`
   test only to the first class. A single threshold applied across all four is what produces an
   uninterpretable rate.

## Robustness evidence (qualitative only)

The strongest robustness claim here is **procedural rather than statistical**: the code and the
hand-collected targets are public and the whole exercise is re-runnable by anyone with the data
vendors, so the finding is falsifiable by construction, which almost nothing else in this debate
is. The authors also report finding and fixing a coding error that had flipped one predictor's
verdict in an earlier draft — the right signal about a project of this size, and a reminder that a
handful of their residual failures are probably theirs rather than the original authors'.

Corroboration across neighbouring designs: their reproduced decay profile is consistent with the
independent post-publication-decay study (returns decay after publication but stay positive, and
decay more for predictors that were stronger in sample), and with that study's own numbers on the
subset of predictors the two share. Cross-market and multi-decade evidence is **absent by design**
— this is a US-only, same-sample exercise.

Honest weaknesses, stated by the authors: reproduction success says nothing about whether an effect
is *real* (p-hacking survives reproduction perfectly); they do not address net-of-cost
profitability and point at the study that finds the answer is unfavourable; a few of their
likely-predictor reproductions deviate materially from the originals' methods (controls dropped,
two-stage estimators simplified to one stage), and they say which.

Lookahead status: `validation_overlap: false` — every reproduction test uses the original study's
own window, and the latest of those end before this lab's validation period. `published_post_2018:
true`. No performance figure tied to any calendar window appears above; the three magnitudes
recorded are **cross-predictor elasticities to construction choices**, each measured on each
predictor's own original sample.

## Implementability here

**The paper is explanatory, not a book.** Nearly all 319 characteristics need fundamentals,
analyst data or options data. But three of its findings bind hard on what this repo should expect
from *any* cross-sectional construction, and one of them changes an arithmetic the lab does
routinely.

1. **This repo's universe IS the liquidity screen, so the one-third haircut is already paid before
   a candidate is written.** The panel is nine large-cap national indices plus ETFs; relative to
   the pool a published cross-sectional result was measured in, it imposes *simultaneously* a
   large-exchange screen, a market-equity floor well above the 20th NYSE percentile, and (through
   index membership) a de facto capitalisation filter. This source's measurement says each of those
   three alone costs roughly a third of gross long-short mean return, and that they are largely the
   same intervention rather than three additive ones. **The usable form is a prior, not a
   constant:** expect a published cross-sectional gross edge to arrive here at order two-thirds of
   its published size *before* v3's cost schedule, and treat the shortfall as predicted rather
   than as a failed replication. `research/README.md`'s own clause — that a null on a mechanism
   the literature localises to small or thin names is *uninformative* here — now has a magnitude
   attached to its general case, not only to its extreme case.
2. **The second third is the cost schedule, and under v3 it is worse than the source's number.**
   The cost study this paper defers to measures effective spreads on US stocks. Protocol v3 charges
   15/20/30/40 bps per side by liquidity tier **plus** statutory transaction taxes — UK stamp duty
   0.5% on purchases, HK stamp duty both sides, French/Italian/Spanish FTTs on purchases — on a
   panel where several of the nine markets carry one. Two independent one-third haircuts compound
   to roughly 4/9 of the published gross surviving, before anything specific to this lab's
   execution. That is an order-of-magnitude frame for the lab's recurring finding that a real,
   correctly-signed mechanism is out of reach at this cost schedule; it is the *expected* outcome,
   not an anomaly of this repo.
3. **The rebalance-frequency monotonicity runs the opposite way to the cost gradient, and that is
   the trade this lab keeps re-deriving.** Gross content falls monotonically as the re-sort
   interval lengthens, because exposure to the signal falls; cost falls too. There is no free
   lunch at either end, and the only honest way to pick an interval is to price both sides on the
   same construction. Worth stating because this folder's cost-mitigation note argues from the cost
   side alone, and this source supplies the gross side's shape.
4. **The denominator lesson applies directly to `experiments/leaderboard.json` and to this
   folder.** The pessimistic replication rate was inflated by counting duplicate holding periods as
   separate claims and by counting variables whose original papers claimed nothing. The lab's own
   trial count — which sets the deflated-skill bar — has the same hazard in mirror image: trials
   that were knob-sweeps of one idea, and trials testing a hypothesis nobody held, both raise the
   bar as if they were independent claims. `distinct_mechanisms` in the leaderboard is the right
   object; this source is the argument for why counting at the *claim* level rather than the *run*
   level is a substantive methodological choice and not bookkeeping.
5. **Two free disciplines, each costing nothing.** (i) **Write the target down before measuring
   it** — this source's headline evidence exists only because the original t-statistic was
   hand-collected first, which is the pre-registration the lab already practises on its own
   hypotheses and could extend to any literature-derived expectation. (ii) **Apply screens at
   portfolio formation, not at signal construction**, so the price of a screen stays measurable;
   the eligible panel already forces this, but a candidate that narrows its own universe before
   computing its signal destroys the counterfactual.

**The one pitfall to flag.** The reproduction success rate must not be read as evidence that a
mechanism will work here. Reproduction is same-sample, same-method, and this source says so twice.
Its transferable content is entirely in the **elasticities and the denominator discipline**, not in
the 98% figure.

## Related

- `notes/2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md` — the pessimistic corner of
  the same triangle, and the study whose denominator this source dissects. The two are not in
  conflict about any number; they disagree about **what to count** and about **which sort to run**.
  Both agree the cross-sectional dispersion of anomaly variables is largest in the smallest names,
  which is the structural fact behind elasticity (1).
- `notes/2026-08-25-hierarchical-bayesian-factor-replication.md` — the optimistic corner, which
  cites this paper as the "pure reproduction" complement to its own "scientific replication". That
  note's 2026-11-01 addendum carries the theme-level and size-group breakouts.
- `notes/2026-10-01-limits-of-p-hacking-publication-bias.md` — the **same first author** on the
  two related questions (can p-hacking generate the observed t-distribution; how much to shrink a
  published t-statistic). That note is the statistical argument; this one is the data project the
  argument is estimated on.
- `notes/2026-10-14-net-expected-returns-of-the-anomaly-zoo.md` — the cost study this paper defers
  to for net profitability, and where elasticity (2)'s first third comes from.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — argues the rebalance-
  interval trade from the cost side; finding (3) here supplies the gross side.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the decay study this source reconciles
  itself against, including why 12% of that study's portfolios read as weak without being failures.
- `experiments/learnings.md`: the standing entry that this universe's edge dies below ~30 bps
  round-trip, and the v3 entries recording zero skill for both re-measured family leads, are what
  elasticities (1) and (2) predict for a panel of this composition — read them as corroboration of
  the frame, not as separate bad news.
