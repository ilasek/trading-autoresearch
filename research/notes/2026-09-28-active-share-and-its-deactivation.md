---
title: "Active Share — the weight-space distance measure, and its deactivation"
authors: Cremers, Petajisto (2009); Frazzini, Friedman, Pomorski (2016)
year: 2009; 2016
venue: "Review of Financial Studies 22(9), 3329–3365 (Tier 1); Financial Analysts Journal
  72(2), 14–21 (peer-reviewed practitioner journal, Tier 1 by this folder's rubric row for
  JPM-class outlets; authors are AQR principals and the article carries the journal's own
  conflict-of-interest note)"
url: https://doi.org/10.1093/rfs/hhp057 ; https://doi.org/10.2469/faj.v72.n2.2
citations: "Cremers–Petajisto: 1325 (Crossref by DOI, checked 2026-09-28); 1608 (OpenAlex by
  DOI, checked 2026-09-28); Semantic Scholar's DOI endpoint returns **not found** for
  `10.1093/rfs/hhp057` and resolves only a separate record — third consecutive session in which
  Semantic Scholar fails on an RFS DOI. Frazzini–Friedman–Pomorski: 58 (Crossref by DOI,
  checked 2026-09-28); 61 (Semantic Scholar by DOI, checked 2026-09-28)."
sample_period: "Cremers–Petajisto: 1980–2003. Frazzini–Friedman–Pomorski: 1990–2009, the same
  sample and methodology as the paper it re-examines."
markets: US domestic equity mutual funds (holdings from Thomson Reuters, returns from CRSP)
tier: A
validation_overlap: false
published_post_2018: false
---

**Version warning, stated up front.** The Cremers–Petajisto text read here is the **August 7,
2006 working-paper draft** (served by `content.money.com`), not the 2009 RFS version of record;
the definition and the two-dimensional framing are identical across versions, but no claim
below should be attributed to the published text's exact wording. Frazzini–Friedman–Pomorski
was read in full from AQR's own hosted PDF of the FAJ "ahead of print" typesetting.

Tier A for the **pair**, and the pair is the point. Taken alone the first paper is a Tier A
measure with a contested empirical claim; the second is a same-sample, same-method
re-examination by authors with a declared commercial interest, which is exactly the
combination the replication row of this folder's rubric exists to grade. Neither paper is
about a trading signal. They are filed here because the lab's chronic blocker is **how to tell
whether two long-only books are actually different**, and this is the literature that owns
that question — including the part where the obvious answer fails.

## Mechanism

**The measure.** For a portfolio with weights `w_fund,i` and a reference portfolio with weights
`w_bench,i`, over the union of all assets:

    ActiveShare = ½ · Σᵢ |w_fund,i − w_bench,i|

It is 0 when the two portfolios coincide, 1 when they share no holdings, and for a long-only
fund benchmarked against a long-only index it is bounded in [0, 1]. The halving makes it read
as "the fraction of the portfolio that differs", because every overweight is matched by an
equal-sized underweight.

**The framing that is the actual contribution.** Cremers–Petajisto argue a single number cannot
classify active management, and that a portfolio must be located in **two** dimensions:
Active Share (a *holdings*-space distance from the reference) and tracking error (a *return*-
space distance). The two are not redundant: a diversified stock-picker holding many small
active bets can carry high Active Share with modest tracking error, while a factor-timing book
holding few names close to index weights can carry low Active Share with large tracking error.
Their empirical claim, which the second paper attacks, is that funds in the top Active-Share
group beat their stated benchmarks and funds in the bottom group lag, with the bottom group
characterised as "closet indexers" charging active fees for index-like exposure.

**The deactivation, and its mechanism is the transferable part.** Frazzini–Friedman–Pomorski
replicate the baseline on the same sample and then show that the sort is confounded:

1. **Sorting funds on Active Share is close to sorting funds on benchmark type.** High-Active-
   Share funds are predominantly benchmarked to small- and mid-cap indices; low-Active-Share
   funds to large-cap indices. The "active" ranking is, to a first approximation, a ranking of
   *which index a fund is measured against*.
2. **Total returns of high- and low-Active-Share funds are not reliably distinguishable.** The
   benchmark-adjusted gap arises because the two groups' benchmarks differed, not because the
   funds did.
3. **Within a single benchmark, the relationship is as likely to be positive as negative.**
   Conditioning on the reference removes the result.

Their one-sentence explanation is the rule worth carrying: **Active Share is a measure of
active *risk*, and taking more risk is not by itself a source of return.** They extend it by
analogy — tracking error is another concentration/distance measure and does not predict
performance either, and Amihud–Goyenko's `R²`-based distance-from-index does not predict
performance on its own. What does appear in their reading is an *interaction*: managers
independently more likely to be skilled do better when they take more risk. Distance is a
multiplier on skill, never a substitute for it.

Their concession is equally useful: Active Share remains a reasonable instrument for judging
**whether a fee is proportionate to the active risk delivered** — a cost-side use, not a
return-side one.

## Construction recipe

Nothing to build — the measure is one line — so the recipe here is the *protocol* the two
papers jointly imply for comparing two books:

1. Compute the weight-space distance `½ Σ |w_A,i − w_B,i|` over the union of holdings, on
   aligned dates, against an explicitly named reference `B`.
2. Compute a return-space distance for the same pair (tracking error of `A − B`, or its
   correlation).
3. **Report both, and never substitute one for the other.** The papers' two-dimensional
   argument and the critique's benchmark confound are the same point seen from either side:
   the weight-space number is not a function of the return-space number.
4. Before comparing any two books on a distance measure, **condition on the reference they are
   measured against**. A cross-group comparison of distances is a comparison of references.

## Robustness evidence (qualitative only)

- The measure itself is definitional and cannot decay; only the performance claim is at issue.
- The critique is the strongest available form: **same data, same method, same sample window**,
  reaching the opposite conclusion by adding one control. That is the replication row of this
  folder's rubric being exercised properly, and it is why the pair is Tier A while either half
  alone would not be.
- The critique's own conflict of interest is declared by the journal and should be weighed; its
  argument, however, is a controlled comparison that can be checked rather than an assertion,
  and Cremers–Petajisto themselves are quoted in it as having noted the benchmark-alpha
  asymmetry.
- Both papers are US-only, mutual-fund-only, holdings-disclosure-based, single-market. Neither
  models transaction costs. Neither addresses multiple testing.
- A third-party strand cited by the critique (five measures of active management, examined
  independently, none predictive) points the same way, and is not read here.

## Implementability here

**Not a signal. A free diagnostic, and a correction to one the lab already uses.**

`experiments/learnings.md` [2026-09-27] established the quantity that makes this relevant: the
seat holds ~61% of gross in its ten largest weights and ~1.4% in its ten smallest of ~48, ratio
**0.023**. The lab's existing holdings-space diagnostics — month-to-month **Jaccard**, holdings
overlap, "42% of names deleted" — are **unweighted membership** statistics, and on a book with
that weight profile they are dominated by names carrying a fortieth of the risk each. A Jaccard
of 0.0611 and a holdings overlap of 0.963 are both, on this weighting function, nearly
uninformative about what the book will earn.

`½ Σ |w_A,i − w_B,i|` is the **weighted** version of exactly those statistics, costs one line,
is computable from emitted validation rows with no trial, and is dominated by the same ten
weights that dominate `rho`. **Concrete suggestion: replace (or at minimum accompany) Jaccard
and raw holdings overlap with Active Share against the seated champion, computed per rebalance
date and summarised with the summary statistic named in advance** (`learnings.md` [2026-09-27]
on thresholds over per-date distributions).

**And the pre-registered expectation must be the critique's, not the original's.** This
literature's own verdict is that a weight-space distance **does not predict the return
difference**. So:

- Active Share to the incumbent is a legitimate *description* of what a candidate changed, and
  a legitimate *falsifier*: a candidate whose Active Share to the seat is near zero cannot
  produce a resolvable return difference, whatever its `rho` says, and can be declined before
  it costs a trial.
- It is **not** evidence of decorrelation, and a high Active Share must never be read as a
  reason to expect a blend gain. The required-gain table is read off `rho`, a return-space
  quantity, and nothing here changes that. This is the citable anchor for the lab's own
  standing rule from 2026-09-10 — *do not infer a book's return-space distance from its
  holdings-space distance* — which until now was a warning with a measured quantity (0.023)
  but no external support. It now has a same-sample controlled replication behind it.
- The critique's benchmark-confound has a direct analogue: **comparing Active Share across
  families is comparing families, not signals.** A `seasonality-calendar` book and a
  `price-trend` book will differ in Active Share because of what their universes and turnover
  profiles are. Compare within family, or state the confound.

**Fit against constraints.** No data requirement beyond weights the engine already emits;
long-only bounds the measure to [0,1]; the 25% cap and gross ≤ 1.0 mean the measure behaves as
in the source. Cost: zero. This is a reporting change, not a candidate.

## Related

- The quantity this note is about: `experiments/learnings.md` [2026-09-27] (the ~10-name book,
  ratio 0.023) and [2026-09-27] (a cost remedy needs retainable holdings — the Jaccard 0.0611
  measurement whose *weighted* analogue is Active Share).
- Return-space distance and what it is worth here:
  `notes/2026-09-23-mean-variance-spanning-and-intersection.md`,
  `notes/2026-09-23-spanning-test-power-and-step-down.md`,
  `notes/2026-08-24-testing-differences-of-sharpe-ratios.md`.
- Other distance/concentration measures already filed:
  `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`,
  `notes/2026-09-24-diversification-ratio-most-diversified-portfolio.md`.
- Companion filed the same night, arguing the *opposite* side of the concentration question
  from inside the same literature: `notes/2026-09-28-best-ideas-and-the-cost-of-overdiversification.md`.
