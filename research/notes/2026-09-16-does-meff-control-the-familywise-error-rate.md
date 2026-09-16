---
title: "Does a plug-in effective number of tests control the error rate? (Halle–Djurovic–Andreassen–Langaas; with Salyakina et al. and Moskvina–Schmidt)"
authors: Halle, Djurovic, Andreassen, Langaas (primary, read in full); Salyakina, Seaman, Browning, Dudbridge, Müller-Myhsok (abstract only); Moskvina, Schmidt (abstract only)
year: 2016; 2005; 2008
venue: "arXiv preprint stat.ME (Tier 4 by venue — no peer review, no citations); Human Heredity (Tier 1 for its field, peer-reviewed); Genetic Epidemiology (Tier 1 for its field, peer-reviewed)"
url: https://arxiv.org/abs/1612.04535 ; https://doi.org/10.1159/000087540 ; https://doi.org/10.1002/gepi.20331
citations: "Halle et al. — 0 (OpenAlex, checked 2026-09-16); Semantic Scholar arXiv endpoint returned HTTP 429 on two attempts, 20s apart. Salyakina et al. — 68 (Semantic Scholar by DOI, checked 2026-09-16), 54 (OpenAlex). Moskvina–Schmidt — 269 (Semantic Scholar), 272 (OpenAlex)"
sample_period: "No market data anywhere. Halle et al.: analytic/numerical study of compound-symmetry, AR(1) and tridiagonal correlation matrices, plus one genotype block from a published psychiatric-genetics cohort. Salyakina et al.: 291 genotyped markers in 31 genes. Moskvina–Schmidt: constructed examples plus genome scans."
markets: none — statistical genetics and multiple-testing methodology
tier: "B overall, and the components are graded separately on purpose. The **conclusion** — that substituting an estimated effective count into an independence formula does not reliably control the error rate — is carried by two peer-reviewed, independently-authored sources and is Tier B. The **head-to-head comparison table** is from an uncited preprint and is Tier C; treat its individual entries as indicative, not as established."
validation_overlap: false
published_post_2018: false
---

**Halle et al. read in full** (14-page arXiv PDF, v2, submitted December 2016; the compiled file
carries a later typesetting date). **Salyakina et al. and Moskvina–Schmidt recorded from their
published abstracts only** — both are closed-access and nothing below is taken from their bodies.
They are here because the preprint that was read has no citations and no peer review, and its central
claim needs support that does not come from its own authors. It has it: both peer-reviewed abstracts
state a version of the same finding independently and earlier.

**This is the companion to
`2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` and the reason that note
carries a warning in its header.** That note defines the estimator family. This one is the evidence
on what the family delivers.

## Mechanism

**The finding in one sentence, in the authors' own words:** *"the reviewed methods based on
estimating the effective number of independent tests in general do not control the familywise error
rate."*

**Why — and the argument is definitional before it is empirical.** The effective number of
independent tests is *defined* by inverting Šidák:

    M_eff  =  log(1 − α) / log(1 − α_loc)

where `α` is the target familywise error rate and `α_loc` the per-test cut-off. Read that equation
carefully, because it carries the whole note: **`M_eff` is a function of two error rates, not of a
correlation matrix.** The correlation structure enters only through the joint probability
`P(O_1 ∩ … ∩ O_m)` that gives the true `α_loc` for a target `α`. So a number computed from
eigenvalues alone is `M_eff` only if that functional happens to land on the value the inversion
requires — and there is no reason it should. The estimators in the companion note "are all based on
the eigenvalues of the genotype correlation matrix, and **are not related to the statistical test
used**". Nothing in their derivations mentions the familywise error rate at all, so nothing in them
can control it.

**Moskvina and Schmidt make the same point from the other end and it is the sharper form for this
repo**: the effective number of tests depends **nonlinearly on the per-test significance level**, a
dependence existing corrections do not take into account, "leading to widely overestimated results".
Two tests correlated at `ρ` are worth *more* independent tests deep in the tail than they are near
the centre of the distribution — the correlation of the statistics is not the correlation of the
tail events. **An effective count is therefore not a property of a set of strategies; it is a
property of a set of strategies at a stated significance level.**

**The second structural finding, on additivity.** `M_eff` *is* additive over independent blocks —
but only if a common local significance level is imposed on every block and solved for
simultaneously. Compute `M_eff` block by block and sum, and you are implicitly using a different
`α_loc` per block. The authors show this is not a technicality: the same estimator that was
conservative on the full matrix exceeded its nominal error rate when its own per-block estimates
were summed. **A "total effective count" assembled from parts is not the effective count of the
whole.**

## Construction recipe

There is no new estimator to implement here. What there is, is a **validation procedure** for any
effective-count estimator, and it is the transferable content:

1. **Fix a dependence structure you can compute the truth for.** Halle et al. use three: compound
   symmetry (every pair correlated at `ρ` — the analogue of a homogeneous family of variants),
   AR(1) (correlation decaying with distance — the analogue of a research programme drifting over
   time), and tridiagonal (neighbours only).
2. **Compute the true per-test cut-off.** For compound symmetry the `m`-dimensional integral
   factorises into a one-dimensional integral over the common factor; otherwise use numerical
   integration of the multivariate normal orthant probability (they use Genz's algorithm with
   absolute error tolerance `1e-9`, feasible to `m ≤ 1000`). This gives the `α_loc` that actually
   delivers `FWER = α`.
3. **Compute each estimator's `α_loc`** by its own route — eigenvalues → `M_eff` → Šidák.
4. **Feed each estimator's `α_loc` back through the exact calculation** to get the FWER it really
   delivers, and compare against nominal. *Not* against the true `α_loc` — against the realised error
   rate, which is the thing anyone cares about.
5. **Sweep `ρ`.** An estimator whose curve crosses the truth is not "slightly off"; it is
   conservative in one regime and anti-conservative in another, and knowing which regime you are in
   requires knowing the answer you were trying to estimate.

**The reference standard throughout this literature is permutation** (Westfall–Young max-T, which
gives strong FWER control under the subset-pivotality condition), and every `M_eff` paper positions
itself as a cheap approximation to it. Salyakina's conclusion on Nyholt's method is the blunt
statement of the trade: *"Although Nyholt's approach may be useful as an exploratory tool, it is not
an adequate substitute for permutation tests."*

## Robustness evidence (qualitative only)

These are properties of estimators on known correlation structures — no market data, no dated
performance, nothing that could contaminate a return-based evaluation.

- **No estimator in the family was conservative everywhere.** Under compound symmetry, the
  Cheverud/Nyholt and Gao estimators came in below nominal for every `ρ` examined, while Li–Ji and
  Galwey came in *above* nominal. Under AR(1) the ordering held and widened: Li–Ji and Galwey drifted
  progressively past nominal as `ρ` rose — at nominal 5% the realised familywise error reached
  roughly 7–8% at high `ρ` — while Cheverud grew steeply conservative over the same range. Under the
  tridiagonal structure it was Galwey and Gao that failed. **Which estimator is safe depends on the
  dependence structure, and you do not know the dependence structure.**
- **The conservative estimators are conservative by a lot.** Cheverud's realised error fell to
  roughly a third of nominal at the highest correlations examined. That is the price of the one
  member of the family that never overshot, and it is the same trade-off the whole literature is
  trying to escape.
- **Block-wise summation broke the one estimator that was otherwise safe.** Summing per-block
  estimates over a hundred correlated blocks pushed Cheverud's realised error rate above nominal,
  where the same estimator on the full matrix was conservative. Li–Ji's summed estimate was the worst
  in the comparison. This is the concrete instance of the additivity result above.
- **Independent, earlier, peer-reviewed support for the same conclusion.** Salyakina et al. tested
  Nyholt's procedure against permutation on real genotype data and found the realised type-I error at
  a nominal 5% ranged from under 3% to over 7% depending on the correlation structure, with
  additional theory showing the method "can be very conservative in the presence of haplotype block
  structure". Moskvina and Schmidt report that ignoring the significance-level dependence leads to
  "widely overestimated" effective counts. **Three independent groups, two of them peer-reviewed,
  reach the same verdict: the shortcut is a shortcut.**
- **What is *not* claimed, and the note should not be read as claiming it.** Nobody here says
  `M_eff` is useless or that the correlation among tests should be ignored. The direction is not in
  dispute — correlated tests *are* worth fewer independent tests, every method agrees, and Bonferroni
  on the raw count *is* conservative under dependence. What is disputed is whether a plug-in count
  buys you a *guarantee*. It does not.

## Implementability here

**Nothing to implement; one thing to stop doing, and one number to reinterpret.** This note's value
to the lab is entirely in what it forbids.

- **The lab's 1.56 is an effective-dimension statistic, not an `M_eff` for any error rate.** The
  2026-09-15 nightly measured a participation ratio of 1.56 on 90 stored trial-return series (4.12
  with the market component removed) against the engine's clustered count of 24. That is a correct
  and useful measurement of *how concentrated the spectrum is*. It is **not** the number of
  independent tests at the repo's operating significance level, and this literature is the reason:
  the effective count depends on `α` and `α_loc`, and a spectrum functional has no argument for
  either. Report it as what it is — a dispersion measure on the trial ensemble.
- **The direction of the error is not determined.** The 2026-09-15 entry reasons that a smaller
  effective `N` lowers `expected_max_sharpe` and therefore that counting 24 where the structure says
  1.6 means the engine over-deflates. The *arithmetic* of that is right and is not contested here.
  What this literature adds is that **the premise — that the structural number is the right `N` —
  is exactly what fails**: Moskvina–Schmidt's nonlinearity says the effective count at a deep tail
  cut-off is larger than the effective count implied by the bulk correlation, and the repo's deflator
  operates in the tail. So the gap between 24 and 1.6 overstates the over-deflation by an unknown
  amount, in the conservative direction. **This strengthens the 2026-09-15 conclusion that a low
  effective-`N` reading is not a licence to relax anything, and it strengthens it for a reason
  independent of the Sullivan–Timmermann–White universe argument already recorded there.** Two
  independent reasons, same direction.
- **The lab now has three candidate `K`s and must not choose among them by convenience.** The engine's
  single-linkage count, the participation ratio, and (if the companion note's diagnostic is run) five
  more from the eigenvalue family. This literature's finding is that the spread between them is the
  honest state of knowledge, not a menu. Pre-commit before computing, or report the spread and select
  nothing.
- **The one route that does carry a guarantee is already in this folder, and it is not free.** Strong
  FWER control comes from permutation / max-statistic resampling, which in this repo's vocabulary is
  White's Bootstrap Reality Check on the stored trial return series — `O(l)` storage, one pass,
  reproducible from a seed. The honest summary of both notes together: **the eigenvalue shortcut buys
  a three-orders-of-magnitude speed-up and gives up the guarantee, and in this repo the permutation
  route is affordable.** `m ≈ 90`, not 700,000. The computational argument that justifies `M_eff` in
  genomics does not apply here.

**Pitfalls.**

- **Do not port the sign of any estimator's bias from this note into a finance application.** The
  comparisons above are on compound-symmetry, AR(1) and tridiagonal matrices. A repo's trial
  correlation matrix is none of those — it is closer to one dominant factor plus a hierarchy of
  variant clusters. `CLAUDE.md`'s rule against carrying constants across families is the same rule
  and it applies with more force across *fields*.
- **The `M_eff` results are about a Šidák/Bonferroni cut-off; the repo's deflator is an extreme-value
  expectation.** The shared structure is the plug-in, not the calibration. A finding that Li–Ji
  overshoots a Šidák target says nothing quantitative about what it would do inside `E[max SR]`.
- **This is not an engine bug report and must not become one.** Nothing here says the engine computes
  anything incorrectly. It says a *calibration* question has no clean answer in the literature
  either, which if anything supports the 2026-09-15 decision to hand `TRIAL_CLUSTER_RHO` to a human
  rather than to reinterpret it.
- **No trial, no candidate file, no holdout read** is implied by anything in this note.

## Related

- `2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` — the estimators this
  note evaluates. Read that one first, then this one; reading it alone is the error this note exists
  to prevent.
- `2026-09-16-clustering-trials-onc-effective-number-of-trials.md` — the finance-side plug-in, which
  inherits this critique in full and has never been tested against a realised error rate.
- `2026-09-15-reality-check-max-statistic-under-dependence.md` — the resampling route that does carry
  a guarantee, and the note whose scree diagnostic produced the lab's 1.56.
- `2026-08-24-deflated-sharpe-ratio.md` — the formula whose `N` is at issue.
- `2026-08-24-multiple-testing-haircut.md` — Harvey–Liu's constant-average-correlation route, which
  is a *third* way of pricing dependence and shares the plug-in structure critiqued here.
