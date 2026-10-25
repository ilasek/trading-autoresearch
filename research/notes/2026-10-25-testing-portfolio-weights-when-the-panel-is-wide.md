---
title: "Tests for the weights of the global minimum variance portfolio in a high-dimensional setting — the exact F-test on a weight vector, what happens to it as p/n → c, and the discovery that ignoring a rank-deficient covariance matrix drives every such test's power to ZERO"
authors: "Bodnar, Dmytriv, Parolya, Schmid (the exact test they generalise is Bodnar & Schmid 2008)"
year: 2019 (Bodnar–Schmid 2008 for the exact test)
venue: "IEEE Transactions on Signal Processing 67(17), 4479–4493 (venue tier 2 for this rubric — a top signal-processing journal, peer-reviewed, but not a finance or econometrics outlet). The exact test generalised is in Metrika 67, 127–143."
url: "https://doi.org/10.1109/tsp.2019.2929964 ; read at https://arxiv.org/pdf/1710.09587v3 . Bodnar–Schmid 2008: https://doi.org/10.1007/s00184-007-0126-7"
citations: "28 (Crossref `is-referenced-by-count` for 10.1109/tsp.2019.2929964, checked 2026-10-25). Bodnar–Schmid 2008: 58 (Crossref, checked 2026-10-25). Both counts are modest; the tier below reflects that."
sample_period: "None. Theory plus Monte-Carlo simulation. There is no market data in the paper — no empirical application section exists, and the covariance matrices in the comparison study are constructed by hand (one-ninth of non-zero eigenvalues at 2, four-ninths at 5, the rest at 10). Nothing in it can touch any evaluation window."
markets: "Not applicable (theory + simulation). Parameterised by `p` (assets), `n` (observations), `c = p/n`, and `rank(Σ) = q`."
tier: "B. The mathematics is sound, proved in an appendix, and the central negative finding is demonstrated cleanly. Held at B rather than A on three counts: a tier-2 venue for this rubric with only 28 citations; everything assumes independent (and for most results normally distributed) returns; and the headline comparisons are simulation results under a hand-chosen eigenvalue spectrum, so the ranking of tests is demonstrated rather than proved. The exact-test result it builds on (Bodnar–Schmid 2008) is itself a proof and is the more durable half."
validation_overlap: false
published_post_2018: true
read: "In full — arXiv:1710.09587v3 (1 July 2019, marked 'IEEE Transactions of Signal Processing, 2019 forthcoming'), 802 KB PDF, `pdftotext -layout` into 227 KB of clean text, 593 instances of `\" the \"`, zero `( )` dropout. Sections I–V, Theorems 1–4, Propositions 1 and the whole comparison-study discussion read closely; the appendix proofs were not followed. Several displayed equations in the two-column layout extract out of reading order, so equations (5), (9) and (23) were re-extracted page-by-page without `-layout` to confirm their structure. Bodnar–Schmid (2008), *Metrika*, was NOT obtained — closed at Springer; its test statistic and exact null distribution are recorded here **as this paper restates them** (Section III.A, equations 5–8), which is a primary source that generalises the result and reproduces its statement, not a search snippet."
access_note: "`arxiv.org/pdf/<id>v3` served the accepted version of a closed IEEE article on the first try, carrying the journal's own running head — the README's standing arXiv channel, confirmed again. Worth noting the two-column-with-floats layout defeats `pdftotext -layout` for displayed equations specifically while leaving the prose perfect: the `\" the \"` count and the `( )` check both pass, so **neither of the README's integrity tests detects equation re-ordering**. Re-extracting the single page without `-layout` fixed it. That is a fourteenth 'looks like an answer' mode of a milder kind: the document is complete and correct, and only the *order* of the mathematics is wrong."
anti_lookahead_note: "Published 2019, so `published_post_2018` is true and the flag should be read as a novelty discount — but the paper contains no data at all, so there is no sample to overlap this lab's validation window and nothing period-specific to withhold. All quantities below are functions of `p`, `n`, `c` and `rank(Σ)`."
---

## Mechanism

This note is the boundary condition on the other three in tonight's set. They supply exact inference
on an estimated weight vector; this one says when that inference still works on a panel of this
lab's width, and what the failure looks like when it does not.

**The exact test (Bodnar–Schmid 2008, restated here as equations 5–8).** The hypothesis is the one a
lab grading against a benchmark actually wants:

```
H0 : w_GMVP = r          against        H1 : w_GMVP ≠ r
```

for any known `r` with `1ᵀr = 1` — the equal-weight pool, the incumbent champion's weight vector, the
book you are currently holding. Drop one component (the weights sum to one) and write `ŵ*` for the
first `p−1` estimated weights, `Q̂ = Σ̂⁻¹ − Σ̂⁻¹11ᵀΣ̂⁻¹/(1ᵀΣ̂⁻¹1)`, `Q̂*` its leading `(p−1)×(p−1)`
block. Then

```
T_n  =  ((n − p)/(p − 1)) · (1ᵀΣ̂⁻¹1) · (ŵ* − r*)ᵀ (Q̂*)⁻¹ (ŵ* − r*)        ~  F_{p−1, n−p}   under H0
```

**exactly** — not asymptotically — for fixed `p`, `n > p`, independent returns, and in fact for the
whole matrix-variate elliptically-contoured class, not just the normal. It is a Mahalanobis distance
between the estimated and hypothesised weight vectors in the metric `Q̂*`, scaled by the degrees of
freedom. Its exact density under the alternative is also known (equation 6, a hypergeometric
`₂F₁`), with non-centrality

```
λ  =  (1ᵀΣ⁻¹1) · (w*_GMVP − r*)ᵀ (Q*)⁻¹ (w*_GMVP − r*)
```

so the **exact power function** is available (equation 8) — which is unusual and valuable: you can
compute, before running anything, how large a weight deviation this test could detect at your `(p, n)`.

**What `p/n` does to it.** The size is exact whenever `n > p`, so dimension does not break the test's
calibration. What dimension does is change the *scale* of the statistic. Theorem 1: under
`p/n → c ∈ (0,1)`,

```
√(p−1) · ( T_n − 1 − λ_n/(p−1) ) / C_n  →  N(0,1),      C²_n = 2 + 2λ²_n/c + 4λ_n/c + 2(c/(1−c))(1 + λ_n/c)²
```

and under `H0` (`λ_n = 0`) this collapses to `√(p−1)(T_n − 1) → N(0, 2/(1−c))`. **The null
distribution's dispersion grows as `2/(1−c)`**, so as the panel widens toward the sample length the
statistic becomes a noisier measurement of the same deviation. Equation (9) gives the asymptotic power
in closed form, and the simulations show the approximation is already good at `n = 500` with
`p ∈ {50, 250, 350, 450}` — so for a wide panel the practical move is to use the normal critical value
rather than the exact `F` quantile, since the exact power function's `₂F₁` is numerically hostile at
large `p` and `n`.

**The shrinkage-based test, and why it exists.** The second test replaces the sample weights with the
shrinkage estimator `ŵ_GSE = α_n Σ̂⁻¹1/(1ᵀΣ̂⁻¹1) + (1 − α_n) b_n` (Bodnar–Parolya–Schmid 2018), whose
optimal intensity `α̂_n = (b_n − ŵ_n)ᵀΣb_n / (b_n − ŵ_n)ᵀΣ(b_n − ŵ_n)` is almost surely asymptotically
equivalent to a deterministic `α̃_n ∈ [0,1]`. The trick is an **identity**: with the target set to the
hypothesised vector, `b_n = r`,

```
w_GMVP = r     ⟺     α̃_n = 0
```

so the weight hypothesis becomes `H0 : α̃_n = 0` against `H1 : α̃_n > 0` — a one-sided test on a single
scalar, the shrinkage intensity, whose asymptotic law follows from the same relative-loss quantity
`R_{b_n} = (1ᵀΣ⁻¹1)(b_nᵀΣb_n) − 1` that Frahm–Memmel call `τ_R`. This is, as far as the authors know,
the first use of a shrinkage estimator inside test theory rather than point estimation.

**The finding that matters most, and it is a negative one.** When `Σ` is **singular** —
`rank(Σ) = q < p`, which is what a panel wider than its history gives you — and the test ignores that
singularity, the simulations show **all three non-singular tests (Bodnar–Schmid's, Glombeck's, and
the shrinkage one) have power functions and ROC curves very close to zero in every case considered.**
The reason is mechanical: the asymptotic variances derived under non-singularity are far too large
when the true `Σ` is rank-deficient, so the standardised statistic never reaches its critical value.
**This is not reduced power. It is a test that cannot reject anything, while reporting a p-value.**
The paper's Section III.C supplies Moore–Penrose versions (`Σ̂⁺` in place of `Σ̂⁻¹`, degrees of freedom
driven by `q` and `c̃ = q/n`) that do work, and among those the singularity-aware shrinkage test
dominates on both power and ROC in almost every configuration.

**One honest wrinkle in the comparison.** In the *non-singular* case with small `c` the ordering flips
depending on the criterion: Bodnar–Schmid's and Glombeck's tests have higher raw power than the
shrinkage test, while the shrinkage test wins on ROC — because it is **undersized** at small `c`.
Power comparisons between tests that do not hold their nominal size are not comparisons; the ROC is
the criterion that survives that.

## Construction recipe

1. **Decide which régime you are in, from two numbers.** `p` = names entering the covariance estimate,
   `n` = independent return observations. Then `c = p/n`, and `q = rank(Σ̂)` — in practice
   `q = min(p, n − 1)` for a sample covariance, so `q < p` whenever `n ≤ p`.
2. **If `n > p` and `c` is small** (say under 0.1): use the exact statistic `T_n` above against
   `F_{p−1, n−p}` quantiles. Compute the exact power at your `(p, n)` from equation (8) before
   trusting a non-rejection.
3. **If `n > p` but `c` is large**: use the same `T_n` with the normal critical value from Theorem 1,
   i.e. reject when `√(p−1)(T_n − 1)/√(2/(1−c)) > z_{1−α}`. Expect the detectable deviation to grow
   with `c`.
4. **If `q < p` — the singular case — do NOT run any of the above.** Use the Moore–Penrose versions:
   replace `Σ̂⁻¹` with `Σ̂⁺`, `Q̂` with `Q̃ = LΣ̂⁺Lᵀ − LΣ̂⁺11ᵀΣ̂⁺Lᵀ/(1ᵀΣ̂⁺1)` for an `L` selecting `k ≤ q`
   components, and test sub-vectors of the weight vector with `T̃_n`, Bonferroni-adjusting across the
   sub-vectors needed to cover the whole book. The singularity-aware shrinkage test is the one to
   prefer.
5. **Pick the target `r` before looking at the data.** It is a hypothesis, and under the shrinkage
   formulation it is literally the shrinkage target.

## Robustness evidence (qualitative only)

- **The exact `F` result is a theorem** and holds for the matrix-variate elliptically-contoured class,
  not only the normal — so heavy tails do not invalidate it, as long as returns are independent across
  time. Independence is the binding assumption, not normality.
- **Theorems 1–4 are proved**, in an appendix not followed here. The *rankings* of tests are
  simulation findings under one hand-built eigenvalue spectrum (chosen so the spectrum's shape is
  invariant to `p`), so they are demonstrations rather than theorems, and the authors say so: "these
  results could not be considered as a general statement to the problem and further investigation in
  this direction should be done."
- **The singular-case collapse is the most robust empirical claim in the paper** — it appears across
  two ranks (`q ∈ {100, 300}`), both `p = 450` and `p = 600`, and both criteria, with a mechanical
  explanation (over-large asymptotic variances) rather than a curve-fitting one.
- **Modest citation counts** (28 and 58) and a non-finance venue. The results have not been
  independently replicated in the finance literature as far as this note's sources show. Weigh the
  *exact* test (Bodnar–Schmid, 58 cites, and corroborated by Okhrin–Schmid's independently derived
  distribution for the same estimator) more heavily than the high-dimensional extensions.
- **No empirical study.** Like Frahm–Memmel, this paper never touches market data, so its asymptotic
  régimes have not been checked against the serial dependence, conditional heteroskedasticity and
  structural breaks real panels show.

## Implementability here

**The one-line consequence for this lab: the exact weight tests in tonight's other notes are usable on
a selected book of a few dozen to a few hundred names on daily data, and are NOT usable on the
eligible panel, where they will silently never reject.**

Concretely, with `n` = independent daily observations in the estimation window:

| what is being tested | `p` | `n` | `c = p/n` | régime |
|---|---|---|---|---|
| a 25-name book, 1yr daily | 25 | 252 | 0.10 | exact `F`, comfortable |
| a 100-name book, 1yr daily | 100 | 252 | 0.40 | `n > p`; use the normal limit, expect weak power |
| a 100-name book, monthly over validation | 100 | ~70 | — | **singular**: `q = 69 < p`. Moore–Penrose only |
| the ~1,000-name eligible panel, 6yr daily | ~1000 | ~1512 | 0.66 | `n > p` but `2/(1−c) ≈ 5.9`: very weak power |
| the ~1,000-name eligible panel, monthly | ~1000 | ~70 | — | **singular**: `q = 69 ≪ p`. Nothing non-singular applies |

The two singular rows are the common cases in this repo — a monthly rebalance grid over a six-year
validation window gives about 70 observations against hundreds or thousands of names — and they are
exactly the cases where the paper shows a non-singular test has power near zero. **A weight test run
there would return "cannot distinguish this book from the pool" for every book, including books that
are nothing like the pool**, and the output would be indistinguishable from a genuine non-rejection.
That is a trap worth naming before anyone builds the screen that tonight's other two notes invite.

**Three usable moves.**

1. **Run the weight test on the held book, not the panel.** `p` is the number of names whose
   covariance you estimate. A candidate that holds `K = 100` names and wants to ask "is my weight
   vector distinguishable from equal weight over these names?" has `p = 100`, not 1,000 — and on
   daily data that is a legal, if low-powered, question. Selecting the 100 at the rebalance date puts
   the selection inside the statistic, so this is a *post hoc* diagnostic on a fixed book, not a
   pre-registered test.
2. **Report the detectable deviation, not just the p-value.** Equation (8) gives the exact power as a
   function of the non-centrality `λ`. Stating "at this `(p, n)` the test detects a weight deviation of
   at least `λ*` with 80% probability" is far more informative than a non-rejection, and it is the
   same discipline the lab already applies when it reports skill intervals rather than point Sharpes.
3. **Check `rank(Σ̂)` before running any covariance-based screen.** One line of linear algebra. If
   `q < p`, the non-singular machinery is not merely imprecise, it is inert. This generalises past
   weight tests: any statistic whose null distribution was derived assuming `Σ̂` is invertible is
   suspect on a panel where it is not.

**Pitfalls.**

- **`published_post_2018: true`.** Discount the novelty of the high-dimensional half accordingly, per
  `research/README.md`. The exact-`F` half dates from 2008 and is not affected.
- **`n` is independent observations, not rows.** Overlapping formation windows, forward-filled
  holiday prices and near-static books all inflate the nominal row count. `learnings.md`'s own warning
  that a wide band produces "one draw repeated" is the same caution. Use the smaller, honest `n`.
- **The shrinkage test needs `Σ` in its intensity formula.** `α̂_n`'s definition involves the true `Σ`;
  the paper supplies a consistent estimator (`α̃⁺_n` from `R̂⁺_{b_n}`), so use that, not the
  population expression.
- **Nothing here is about returns.** Every result is second-moment inference on a weight vector. A
  book that is statistically distinguishable from the pool on its weights may still have zero skill,
  and the lab has measured precisely that outcome more than once.
- **Bonferroni across sub-vectors costs power.** Testing a 100-name book via sub-vectors of size
  `k ≤ q` with a Bonferroni adjustment, on a test that is already weak, will not reject. Prefer a
  single test on a book small enough that `k ≤ q` holds in one go.

## Related

- `notes/2026-10-25-exact-distributions-of-estimated-portfolio-weights.md` — Okhrin–Schmid supply the
  `E(ŵ) = w_GMVP`, `Cov(ŵ) = Q/[(n−p−1)·1ᵀΣ⁻¹1]` and multivariate-`t` results this paper quotes
  verbatim as its starting point, and independently confirm them.
- `notes/2026-10-25-gmv-weights-as-regression-coefficients.md` — the same hypothesis tested by
  restricted-regression `F` instead; that route makes the `n > p` requirement visible as "a regression
  needs more rows than regressors", which is the same wall.
- `notes/2026-10-25-dominating-estimators-and-the-naive-diversification-test.md` — Frahm–Memmel's
  relative loss `τ_R` is this paper's `R_{b_n}`; the two give a *test on the intensity* and a *test on
  the loss* of the same shrinkage idea, and Frahm–Memmel's `q = n/d → 1⁺` warning is the mirror of this
  paper's `c → 1` one.
- `notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md` and
  `notes/2026-09-27-nonlinear-shrinkage-instead-of-counting.md` — the random-matrix background for why
  `Σ̂` stops being a good estimator at `c` bounded away from zero (the eigenvalues spread over
  `[(1−√c)², (1+√c)²]`), which this paper cites as its motivation.
- `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md` — the other
  route to inference on a wide panel's precision matrix.
- `notes/2026-09-23-mean-variance-spanning-and-intersection.md` and
  `notes/2026-09-23-spanning-test-power-and-step-down.md` — the adjacent question ("does adding this
  asset expand the frontier?") and its own power problem; Gibbons–Ross–Shanken's `F`-test, which this
  paper names as the classical antecedent, lives there.
