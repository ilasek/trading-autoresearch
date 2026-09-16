---
title: "The effective number of independent tests, M_eff — the eigenvalue estimator family (Cheverud; Nyholt; Li–Ji; Gao et al.; Galwey)"
authors: Cheverud; Nyholt; Li, Ji; Gao, Starmer, Martin; Galwey
year: 2001; 2004; 2005; 2008; 2009
venue: Heredity (Tier 1 for its field); American Journal of Human Genetics (Tier 1); Heredity (Tier 1); Genetic Epidemiology (Tier 1); Genetic Epidemiology (Tier 1) — all peer-reviewed, none in finance
url: https://doi.org/10.1046/j.1365-2540.2001.00901.x ; https://doi.org/10.1086/383251 ; https://doi.org/10.1038/sj.hdy.6800717 ; https://doi.org/10.1002/gepi.20310 ; https://doi.org/10.1002/gepi.20408
citations: "Cheverud 435 (Semantic Scholar by DOI, checked 2026-09-16), 426 (OpenAlex). Nyholt 1767 (Semantic Scholar), 1747 (OpenAlex). Li–Ji 1489 (Semantic Scholar), 1530 (OpenAlex). Gao et al. 808 (Semantic Scholar), 753 (Crossref). Galwey 186 (Semantic Scholar), 196 (OpenAlex); all checked 2026-09-16"
sample_period: "No market data anywhere in this cluster. Li–Ji: simulated genotypes plus a published case/control panel. Galwey: a genotyped case/control sample at ~85,000 loci in 2,000 genes. Nyholt and Cheverud: genotype/haplotype panels. Dates are irrelevant to the content, which is algebra on a correlation matrix."
markets: none — statistical genetics
tier: A (five peer-reviewed sources, three of them heavily cited, the family repeatedly re-evaluated by independent groups; the discount is that it is a *different field's* literature and nothing here was ever tested on financial data)
validation_overlap: false
published_post_2018: false
---

**Li–Ji read in full** (the typeset *Heredity* article, from the publisher's own open PDF endpoint).
**Cheverud, Nyholt, Gao et al. and Galwey were not read in their original form**; their estimator
definitions are taken from two independent restatements — Li–Ji's own restatement of Cheverud, and
the review section of Halle–Djurovic–Andreassen–Langaas, read in full and noted separately in
`2026-09-16-does-meff-control-the-familywise-error-rate.md` — plus Galwey's and Gao's published
abstracts. The two restatements agree with each other on every formula below, which is why they are
recorded as reliable; **no claim in this note rests on the unread papers' arguments**, only on their
definitions. `cell.com` and Europe PMC both refused an automated client for the Nyholt AJHG PDF
(HTTP 403 and an HTTP 500 from the REST full-text endpoint respectively).

**Why this folder is reading statistical genetics.** This is the literature that asked the lab's
current question first and in the same form: *given `m` correlated tests, how many independent tests
is that worth, and can you just substitute the answer into a formula derived for independent tests?*
The vocabulary is `M_eff`. The lab has just computed a number of exactly this shape
(a participation ratio of the eigenvalues of its 90 stored trial-return series), and this cluster is
where the estimator family it belongs to is defined. **What the family is worth is the subject of
the companion note, and this note should not be used without it.**

## Mechanism

**The problem.** Bonferroni (`α_loc = α/m`) is valid under any dependence but conservative when tests
are correlated. Šidák (`α_loc = 1 − (1−α)^(1/m)`) assumes independence outright. Permutation is the
reference answer but costs a full re-test per shuffle. The `M_eff` idea, due to Cheverud, is a
shortcut: **estimate from the correlation matrix alone a number `M_eff ≤ m` of "independent
equivalents", then correct as though you had run `M_eff` independent tests.**

**The interpolation that generates the first two estimators.** Take `R̂`, the `m × m` correlation
matrix of the test statistics, with eigenvalues `λ_1 … λ_m` summing to `m`. Two extremes anchor it:

- tests completely independent → `R̂ = I` → every `λ_i = 1` → `Var(λ) = 0` → want `M_eff = m`;
- tests completely identical → one eigenvalue `m`, the rest zero → `Var(λ) = m` → want `M_eff = 1`.

Cheverud's estimator is the straight line between those two anchors in `Var(λ)`. Everything else in
the family is an attempt to do better *between* the anchors, because the line is where the anchoring
argument gives no guidance at all.

**Why the interpolation is wrong in the middle, stated exactly** (Li–Ji's argument, and the sharpest
thing in this cluster). Suppose the `m` tests are `c` identical copies of `m/c` genuinely independent
tests. The spectrum is then `c` repeated `m/c` times, and zeros elsewhere; the truth is
`M_eff = m/c`. Cheverud's formula returns `m + 1 − c`, so its ratio to the truth is

    r = c(m + 1 − c) / m  ≥ 1

which for large `m` and moderate `c` is *much* larger than one. **The failure mode is specific and it
is the one that matters here: a large number of moderately correlated tests.** That is precisely the
regime a research lab's accumulated trial history sits in.

**The repair, and its own assumption.** Li–Ji's observation is that an eigenvalue can be split: the
integer part counts identical tests that should collapse to one, the fractional part counts a
partially-correlated test that should count as a fraction. Hence count each eigenvalue as
`I(λ ≥ 1) + frac(λ)`. This is exact when the spectrum is integer-valued (`c_1 … c_t`, then zeros) —
i.e. when the tests really are blocks of exact copies — and is an approximation otherwise.

## Construction recipe

All five run the same three steps: **(1)** form the correlation matrix of the test statistics;
**(2)** take its eigenvalues and map them to `M_eff`; **(3)** substitute `M_eff` for `m` in Šidák (or
Bonferroni) to get the per-test cut-off `α_loc`. Only step (2) differs.

| Estimator | `M_eff` from the eigenvalues `λ_1 … λ_m` of `R̂` |
|---|---|
| **Cheverud (2001)** | `m · (1 − (m−1)·Var(λ)/m²)` |
| **Nyholt (2004)** | `1 + (m−1)·(1 − Var(λ)/m)` — an algebraic rewrite of Cheverud |
| **Li–Ji (2005)** | `Σ_i f(\|λ_i\|)`, with `f(x) = I(x ≥ 1) + (x − ⌊x⌋)` |
| **Gao et al. (2008)** | the smallest `k` with `(1/m)·Σ_{i≤k} λ_i ≥ c`, eigenvalues sorted descending; `c = 0.995` as published |
| **Galwey (2009)** | `(Σ_i √λ_i)² / (Σ_i λ_i)` |

`Var(λ)` is the empirical variance of the eigenvalues (Li–Ji write it with denominator `m−1`).
Galwey's form tolerates a non-positive-semidefinite `R̂` — the case that arises when correlations are
estimated pairwise on incomplete data — by setting small negative eigenvalues to zero.

**Three properties of the table worth carrying, because they are easy to get wrong.**

- **Cheverud and Nyholt are the same estimator.** Do not treat a disagreement between two papers
  citing "Nyholt's method" and "Cheverud's method" as two data points.
- **Every one of these is a functional of the spectrum only.** Two correlation matrices with the same
  eigenvalues get the same `M_eff` regardless of what is correlated with what.
- **`M_eff` is not scale-free across the family: the functionals genuinely disagree.** Galwey's
  `(Σ√λ)²/Σλ` and the **participation ratio** `(Σλ)²/Σλ²` — the statistic this lab computed
  overnight — are *both* standard effective-dimension functionals of the same spectrum and are *not*
  equal. Since `Σλ = m` for a correlation matrix, Galwey is `(Σ√λ)²/m` and the participation ratio is
  `m²/Σλ²`. They coincide at the two anchors and differ everywhere between. **A number from one is
  not a number from the other, and neither is "the" effective count.**

**Blockwise computation, and the caveat that comes with it.** Li–Ji propose the obvious speed-up:
when `R̂` is block diagonal (independent groups), compute `M_eff` per block and sum. This is what
makes the method tractable at genome scale. It is also where the family breaks in a way the
companion note documents — **the additivity is not free**, and summing block-wise estimates gave
materially different (and worse) error control than running the same estimator on the full matrix.

**Cost.** The whole method is one eigendecomposition, `O(m³)`. Li–Ji's own comparison against
permutation is the reason anyone uses it: for ~1,000 tests they report the eigen route finishing in
seconds against hours for a permutation test of the same family — a factor of roughly a thousand.
**Speed is the entire argument for `M_eff`.** It is not claimed to be more accurate than permutation
anywhere in this literature; it is claimed to be nearly as accurate and vastly cheaper.

## Robustness evidence (qualitative only)

- **The family has been re-evaluated repeatedly by independent groups**, which is why it is Tier A
  despite being a shortcut: Nyholt evaluated Cheverud against permutation; Li–Ji identified
  Cheverud's over-estimation analytically and proposed the repair; Galwey benchmarked his own and
  Li–Ji's refinements against random permutation on a large genotyped sample and reported close
  agreement for *combining* p-values; Gao's variance-explained variant and all of the above were
  compared head to head by the Halle group. This is a well-worked vein, not a single untested idea.
- **The known direction of each estimator's error is structure-dependent, not universal.**
  Cheverud/Nyholt over-estimate `M_eff` (→ conservative) in the "many moderately correlated tests"
  regime, by an amount Li–Ji derive in closed form. Li–Ji and Galwey correct that and thereby *lose*
  conservatism. Gao's estimator depends on an arbitrary cut-off `c` that has **no derived connection
  to the target error rate at all**, and an independent re-analysis found it highly sensitive to the
  block size used when `m` exceeds the sample size.
- **Nothing in this cluster was tested on financial data, on return series, or on a Sharpe-ratio
  statistic.** The dependence structures it was tuned against are genetic-marker correlation
  matrices. Carrying a *sign* of error from there to here is an analogy, not evidence — the same
  mistake `CLAUDE.md` forbids when carrying `price-trend` constants into a new family.
- **Galwey's own framing is the fair summary of the family's ambition**: the effective number of
  tests is "a valid approximation that allows p-values to be combined in a highly informative way".
  An approximation that is informative — not a guarantee.

## Implementability here

**Directly and cheaply implementable, and the lab has in effect already implemented one member of
the family.** The inputs are the stored validation return series of recorded trials; the correlation
matrix of those series stands in for the correlation matrix of the test statistics, exactly as in
this literature (where the correlation of score-test statistics is shown to reduce to the correlation
of the underlying data when the tests are of the same form). One `numpy.linalg.eigvalsh` call gives
the whole table above. No trial, no candidate file, no holdout read, no new machinery.

**What it would be for.** The repo's deflated-Sharpe bar takes a number of trials `K`. The engine
currently obtains that number by **single-linkage clustering of validation return series at
`ρ ≥ 0.95`** (per the 2026-09-15 journal entry; `engine/` is frozen and was not read for this note),
which is a *threshold* method with no member in the table above. Computing Cheverud/Nyholt, Li–Ji,
Gao and Galwey on the same correlation matrix, alongside the participation ratio already measured,
would put the engine's number inside a family with a published literature instead of beside it —
and, more usefully, would show **how wide the spread across estimators is on this repo's own
matrix.** That spread is the honest error bar on any statement of the form "the repo has run `K`
independent trials".

**Concrete, free, pre-registrable diagnostic.** On the stored series: report `m`, the five estimators
above, the participation ratio, and the engine's own cluster count, as one table. Pre-commit in the
journal that **no estimator will be selected after seeing the table** — the point is the spread, and
picking the member that gives the most convenient `K` is exactly the specification-search the repo
measures elsewhere.

**Pitfalls, and the first one is live here.**

- **Sampling noise in the spectrum inflates every one of these estimators.** The eigenvalues are of
  an *estimated* correlation matrix from `T` observations on `m` series; when `m` is not small
  relative to `T`, Marchenko–Pastur spread alone produces eigenvalue dispersion with no structure
  behind it. Li–Ji's estimator is the most exposed, because it counts any `λ ≥ 1` as a full
  independent test and noise pushes roughly half the spectrum above 1. **The lab has already met this
  failure mode from the other side**: its pre-registered control disqualified the Kaiser rule for
  returning 44 on 90 genuinely independent series. Every estimator here needs the same control — run
  it on `m` i.i.d. series of the same length and report what it says there.
- **`M_eff` is not additive over blocks for free.** See the companion note before summing anything.
- **These are corrections for a Šidák/Bonferroni cut-off, not for an extreme-value expectation.** The
  repo's deflator uses `K` inside `E[max SR]`, a different formula with a different derivation. The
  *plug-in* structure is shared; the estimator's calibration is not transferable between them.
- **Do not read a low `M_eff` as licence to lower a bar.** The companion note gives the statistical
  reason; the 2026-09-15 journal entry gives the repo-specific one (the correction must also span the
  literature universe, per Sullivan–Timmermann–White), and they point in opposite directions.

## Related

- `2026-09-16-does-meff-control-the-familywise-error-rate.md` — **the companion, and this note is
  incomplete without it.** It is the evidence on whether substituting `M_eff` into an
  independence formula controls anything.
- `2026-09-16-clustering-trials-onc-effective-number-of-trials.md` — the finance-side estimator of
  the same quantity, by clustering rather than by eigenvalues.
- `2026-08-21-effective-number-of-bets-diversification-measurement.md` — the **other** effective
  number, and the two must not be confused: that one counts *bets in a portfolio* (a functional of
  weights and covariance, answering "how diversified is this book"), this one counts *tests in a
  search* (a functional of the correlation of test statistics, answering "how many shots did I
  take"). They share an algebraic ancestry — Meucci's diversification distribution and the
  participation ratio are both entropy-like functionals of a spectrum — and nothing else.
- `2026-08-24-deflated-sharpe-ratio.md` — the formula the repo actually deflates with, whose `N` is
  the quantity estimated here.
- `2026-09-15-reality-check-max-statistic-under-dependence.md` — the permutation/bootstrap route that
  this whole family exists as a cheap substitute for, and which this literature treats as the
  reference answer.
