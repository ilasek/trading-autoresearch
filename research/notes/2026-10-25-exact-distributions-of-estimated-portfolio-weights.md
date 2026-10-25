---
title: "Distributional properties of portfolio weights — the GMV weight estimator is exactly multivariate-t and unbiased, the expected-utility one is biased by exactly (n−1)/(n−k−1), and the Sharpe-ratio-optimal one has NO finite moments at all"
authors: Okhrin, Schmid
year: 2006
venue: "Journal of Econometrics 134(1), 235–256 (venue tier 1 — top-five econometrics journal)."
url: "https://doi.org/10.1016/j.jeconom.2005.06.022 ; read at https://opus.bibliothek.uni-augsburg.de/opus4/files/47551/47551.pdf (CC BY-NC-ND 4.0 author deposit of the published article)"
citations: "184 (Crossref `is-referenced-by-count`, checked 2026-10-25). Semantic Scholar's title-search endpoint returned HTTP 429 on this session's first unauthenticated call and was not retried, per `research/README.md`; Crossref answered every lookup tonight on the first attempt."
sample_period: "None. The paper is entirely theory — exact finite-sample moments and densities, plus asymptotic distributions. There is no market data anywhere in it; the simulation study referenced in the conclusion is in Okhrin's 2004 thesis and is not reproduced. Nothing in it can touch any evaluation window."
markets: "Not applicable (theory). The asset model is `k` risky assets with returns `X_t ~ N_k(µ, Σ)`, independent across `t`."
tier: "A. Tier-1 econometrics venue, 184 citations, closed-form exact results with full proofs in the appendix, and the central negative result (non-existence of moments for the Sharpe-ratio-optimal weights) is a proof rather than a simulation. The one axis on which it is weaker than its venue suggests: the exact results all assume independent multivariate-normal returns, and the relaxation in Section 3 (weak stationarity, serial correlation permitted) buys only asymptotics."
validation_overlap: false
published_post_2018: false
read: "In full — the Augsburg institutional deposit of the published article, 935 KB PDF, `pdftotext -layout` into 73 KB of clean text, 301 instances of `\" the \"`, zero `( )` dropout, pagination and journal citation line intact (the deposit's cover page carries the Elsevier citation and the CC licence). Sections 1–4 read closely; the appendix proofs (Section 5) were skimmed for structure and the Muirhead (1982) results they lean on were noted but not checked."
access_note: "The Augsburg repository (`opus.bibliothek.uni-augsburg.de/opus4/files/<docId>/<docId>.pdf`) served the **published** article on the first try under a CC BY-NC-ND licence, where the Elsevier DOI is closed — a new working channel of the 2026-10-04 'enumerate the co-authors' institutions' shape, reached here from a plain web search rather than from an OpenAlex locations list. The file path is simply the numeric `docId` repeated, which is derivable from the `opus4/frontdoor/index/index/.../docId/<n>` landing URL. `-w 'size=%{size_download}'` on the fetch, per the README."
anti_lookahead_note: "Nothing to withhold: the paper contains no data, no dates after its own publication, and no performance figures of any kind. Every number quoted below is a function of `n` (observations) and `k` (assets) only."
---

## Mechanism

Four estimated portfolios, one question: what is the sampling distribution of the **weight vector**?
The answer splits the four cleanly, and the split is the content.

Write `µ̂` and `Σ̂` for the usual sample mean and (unbiased) sample covariance from `n` independent
draws of `X_t ~ N_k(µ, Σ)`, and define

```
ŵ_GMV = Σ̂⁻¹1 / (1ᵀΣ̂⁻¹1)                                  (global minimum variance)
ŵ_EU  = Σ̂⁻¹1/(1ᵀΣ̂⁻¹1) + α⁻¹ R̂ µ̂,  R̂ = Σ̂⁻¹ − Σ̂⁻¹11ᵀΣ̂⁻¹/(1ᵀΣ̂⁻¹1)   (quadratic-utility optimum, risk aversion α)
ŵ_SR  = Σ̂⁻¹µ̂ / (1ᵀΣ̂⁻¹µ̂)                                  (Sharpe-ratio optimum, fully invested)
ŵ_TP  = α⁻¹ Σ̂⁻¹(µ̂ − r_f 1)                                (tangency, with a risk-free asset)
```

Note the structure of `ŵ_EU`: a **GMV core plus a mean-driven tilt**, with `R̂` the covariance
inverse projected off the budget direction. That decomposition is what makes the results readable.

**1. The GMV estimator is the well-behaved one.** Proposition 1 gives its exact multivariate density;
Corollary 1 the marginals. Deleting one component (the weights sum to one, so only `k−1` are free),

```
ŵ*_GMV  ~  t_{k−1}( n − k + 1 ,  w*_GMV ,  Ω* )        with    Ω = (1/(n − k − 1)) · Q/(1ᵀΣ⁻¹1),
                                                               Q = Σ⁻¹ − Σ⁻¹11ᵀΣ⁻¹/(1ᵀΣ⁻¹1)
E(ŵ_GMV) = w_GMV        (exactly unbiased)
```

and each individual weight is a **scaled Student `t` with `n − k + 1` degrees of freedom**:
`√(1ᵀΣ⁻¹1) · √(n−k+1) · (ŵ_GMV,i − w_GMV,i)/√(e_iᵀΣe_i)  ~  t_{n−k+1}`. Exact `t`-tests on single
weights, exact joint tests on subsets, no asymptotics. This is the same law
`notes/2026-10-25-gmv-weights-as-regression-coefficients.md` reaches from OLS, derived independently
from Wishart algebra — two routes to one result.

**2. The expected-utility estimator is biased, and the bias is a pure parameter-count factor.**
Theorem 1(a): for `α = 1, n ≥ k+1, k ≥ 2`, or `α < 1, n ≥ k+2, k ≥ 3`,

```
E(ŵ_EU)  =  Σ⁻¹1/(1ᵀΣ⁻¹1)  +  ((n − 1)/(n − k − 1)) · α⁻¹ R µ
```

**The GMV core is unbiased; the mean-driven tilt is inflated by exactly `(n − 1)/(n − k − 1)`.** At
`k = 100, n = 252` that factor is 1.66 — the estimated active tilt is systematically 66% too large,
in expectation, before anything is said about its variance. The factor diverges as `k → n`.

Theorem 1(b) gives the exact variance, which exists only for `n ≥ k + 4` and is built from

```
c_1 = (n−1)²(n−k+1) / [(n−k)(n−k−1)²(n−k−3)] ,   c_2 = (n−1)² / [(n−k)(n−k−1)(n−k−3)]
```

— note `(n−k−3)` in both denominators: **the variance of the estimated weights blows up as the number
of assets approaches the number of observations**, and ceases to exist three observations before the
estimator itself does.

**3. De-biasing makes it worse.** The paper states the obvious correction,
`w̃_EU = Σ̂⁻¹1/(1ᵀΣ̂⁻¹1) + ((n−k−1)/(n−1)) α⁻¹ R̂ µ̂`, which is unbiased by construction, and then shows
`MSE(ŵ_EU) ≤ MSE(w̃_EU)` in the matrix sense (`B − A` non-negative definite). **Removing the known
bias strictly increases mean squared error.** This is the same lesson Frahm–Memmel reach from the
other side (the plug-in estimator is best *unbiased*, so improvements must be biased) and it is a
general warning against "correcting" an estimator because its bias is known in closed form.

**4. The Sharpe-ratio-optimal weights have no moments.** Proposition 2 gives the exact conditional
density of `ŵ_SR,i` given `µ̂`, and then — this is the paper's sharpest result —

```
all moments of ŵ_SR,i of order β ≥ 1 do not exist;  moments of order β ∈ [0,1) do exist.
```

The mechanism is visible in the density: one term behaves like `1/[(x −1)H_11(x −1)ᵀ]`, whose `β`-th
moment integral diverges for `β ≥ 1`. **The estimated Sharpe-optimal weight vector has no mean and no
variance** — its tail index is 1, i.e. it matches a Cauchy in exactly this respect: moments exist
below order 1 and at no order at or above it. The authors flag the practical
consequence explicitly: "estimating the variance by the sample variance obtained from a Monte-Carlo
simulation would lead to misleading results." A simulation study of such an estimator will always
return a finite number, and that number is not converging to anything.

Section 3 relaxes independence to weak stationarity (serial and cross-serial correlation allowed) and
delivers asymptotic normality with explicit sandwich variances (Theorem 3) for `ŵ_EU`, `ŵ_GMV` and
`ŵ_TP` — and notes that for `ŵ_SR` the asymptotic variance exists while the finite-sample one does
not, so **the asymptotic approximation for that estimator is describing something the exact
distribution does not have.** The conclusion also records that the exact and asymptotic covariance
matrices can differ substantially even for `ŵ_GMV` and `ŵ_EU`, i.e. leaning on the asymptotics is
not free.

## Construction recipe

This is a diagnostic toolkit rather than a strategy, and every item is arithmetic in `n` and `k`.

1. **Classify the proposal before building it.** Does the weighting rule use estimated *means*? If
   not (GMV, risk parity, inverse-variance, equal weight), you are in case 1 and exact inference
   exists. If yes, you are in case 2 at best and case 4 at worst.
2. **For a mean-free covariance weighting**, test individual weights with
   `t_{n−k+1}` and the joint hypothesis `w* = r*` with the `F` statistic of
   `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md`. Degrees of freedom
   `n − k + 1` is the honest sample size, not `n`.
3. **For any rule with a mean-driven tilt**, deflate the tilt by `(n − k − 1)/(n − 1)` *only* if you
   accept the MSE cost the paper proves — otherwise leave it, and read the un-deflated tilt as an
   over-estimate by that factor when judging whether it is economically large.
4. **Refuse the normalised-Sharpe form.** Any rule of the shape `Σ̂⁻¹µ̂ / (1ᵀΣ̂⁻¹µ̂)` — i.e. "put
   everything in the estimated maximum-Sharpe portfolio, scaled to be fully invested" — has an
   estimator with no mean. No standard error, no confidence interval and no Monte-Carlo dispersion
   figure for it means anything. The fix is not a better estimator of the same object; it is a
   different objective (drop the mean, or shrink hard toward a fixed reference).
5. **Check `n ≥ k + 4` for a variance, `n ≥ k + 1` for a point estimate.** Below those, the quantity
   you are about to report does not exist.

## Robustness evidence (qualitative only)

- **These are theorems with proofs, not estimates.** There is no replication question and no decay
  question: they hold exactly whenever the stated assumptions hold, and they are checkable algebra.
  What replication *would* bear on is the realism of the assumptions.
- **The assumptions are strong and the paper admits it.** Exact results need independent,
  multivariate-normal returns; the paper devotes a paragraph to the evidence against normality for
  daily data (citing Osborne, Fama, Mittnik–Rachev) and defends normality as a modelling convenience
  consistent with mean-variance analysis rather than as a fact. Section 3 drops independence for
  asymptotics only.
- **The non-existence result is the most robust part.** Non-existence of moments comes from the
  *shape* of the density near the singularity of `1ᵀΣ̂⁻¹µ̂`, i.e. from the ratio structure of the
  estimator. Heavier-tailed return distributions make that worse, not better. A reader who rejects
  normality should expect the Sharpe-optimal weight estimator to be worse behaved than the paper
  proves, not better.
- **Independently corroborated where it overlaps.** Kempf–Memmel (2006) reach the same GMV weight
  law by OLS; Bodnar–Schmid (2008) build an exact linear-hypothesis test on top of it and extend it
  to the elliptical class; Bodnar–Dmytriv–Parolya–Schmid (2019) restate `E(ŵ_n) = w_GMV` and
  `Cov(ŵ_n) = Q/[(n−p−1)·1ᵀΣ⁻¹1]` verbatim as their starting point. Three independent uses of the
  same result, two of them in tier-1 or tier-2 venues.
- **Known gap.** Case 4's density is derived only for the `i`-th component conditional on `µ̂`, and the
  tangency density (Proposition 3) only for `k = 1`. The authors say generalising the tangency case
  "seems difficult". So the toolkit is complete for GMV, partial for the mean-using portfolios.

## Implementability here

**The direct reading: this closes a class of candidate, cheaply.** `program.md`'s
`portfolio-learning` family invites "ensembles of decorrelated signals" and clustering-based
allocation; the natural sophisticated move inside it is some version of "estimate the covariance of
the family leads' active returns and hold their maximum-Sharpe combination". Result 4 says the
fully-invested maximum-Sharpe weight estimator **has no first moment**. Whatever such a candidate
scores, the score is a draw from a distribution with no centre, and re-running it on a different
window is not sampling noise around a value — there is no value. That is a stronger objection than
"it is noisy", and it costs nothing to apply.

**The screen, with this panel's numbers.** The bias factor `(n − 1)/(n − k − 1)` on any mean-driven
tilt, at daily frequency:

| assets `k` | `n = 252` | `n = 756` | `n = 1512` |
|---|---|---|---|
| 10 | 1.04 | 1.01 | 1.01 |
| 50 | 1.25 | 1.07 | 1.03 |
| 100 | **1.66** | 1.15 | 1.07 |
| 200 | 4.92 | 1.36 | 1.15 |
| 500 | — (`n < k+2`) | 2.96 | 1.49 |

And the variance exists only for `n ≥ k + 4`, with `(n−k−3)` in the denominator, so the 200-name /
one-year cell is not merely biased by a factor of five — its sampling variance is already in the
régime where it is dominated by that denominator. Combined with the previous note's
`(N−1)/(T−N−1)` variance penalty, **two independent closed forms now say the same thing about this
panel: at the widths this lab works at, an estimated weight vector is mostly an estimate of noise.**

**Where it bites on existing lab practice.**

- `experiments/learnings.md` (2026-10-09/10, corrected 2026-10-15) establishes that a **pool-plus-tilt
  blend is a legal, gradable candidate** under v3's null, because a non-uniform weight vector has a
  non-degenerate permutation null. This note prices the tilt: if the tilt is driven by estimated
  means, its magnitude is inflated by the table above, so a tilt weight `κ` calibrated on train is
  measuring `κ · (n−1)/(n−k−1)` of intended tilt. The lab's measured null-dispersion ladder
  (`κ = 0.1 / 0.3 / 0.6`) is a *construction* parameter and is unaffected; what is affected is any
  claim that an estimated tilt is the right size.
- **Prefer the mean-free side of the family.** The lab has repeatedly found means unestimable here
  (momentum's top-100 slice losing 11–20 bps per 63 days at every horizon; the CIV-beta sign
  inverting across train sub-periods). This note says the statistical cost of using estimated means
  in a *weighting* rule is categorically worse than the cost of using an estimated covariance: the
  former can destroy the existence of the estimator's moments, the latter only inflates its variance
  by a computable factor.
- **It does not license a GMV strategy.** Case 1's good behaviour is a statement about *inference*,
  not about returns. The lab's v3 measurement that Sharpe is flat in beta on this panel stands, and
  nothing here contradicts it.

**Pitfalls.**

- **`k` is the number of names in the estimation, not the number held.** A rule that scores 1,000
  eligible names and holds 100 has `k = 1000` in the covariance step unless the covariance is
  estimated on the 100 — and if it is estimated on the 100 *selected at the rebalance date*, the
  selection is inside the estimate and none of these exact distributions apply.
- **Overlapping windows and drift.** Exactness needs independent draws. The lab's own warning that a
  near-static book's monthly observations are "one draw repeated" applies here with full force:
  degrees of freedom `n − k + 1` is an upper bound.
- **The `(n−1)/(n−k−1)` factor is not a correction to apply.** The paper proves that applying it
  raises MSE. It is a *reading* of the tilt's magnitude, not a patch.
- **Nothing here is about costs.** Every result is on the weight vector. v3 charges per name per side
  plus taxes, and `learnings.md` prices the lab's own residual-reversion gross alpha at exactly its
  cost bill. A weighting rule that survives this note's arithmetic still has to survive that.

## Related

- `notes/2026-10-25-gmv-weights-as-regression-coefficients.md` — the same GMV weight law from OLS,
  plus the exact `(N−1)/(T−N−1)` estimation-risk formula and the restricted-regression `F`-test.
- `notes/2026-10-25-dominating-estimators-and-the-naive-diversification-test.md` — the constructive
  answer to result 3: since de-biasing hurts and the plug-in is best unbiased, go deliberately
  biased, and here is the shrinkage intensity and the test that decides whether it is worth it.
- `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` — this paper's `Cov(ŵ_n)`
  is the input to the exact `F`-test for a weight hypothesis; that note covers what happens to the
  test when `k/n` is not small or `Σ` is singular.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — Ledoit–Wolf on the *performance*
  statistic. Complementary axis: that note tests the realised Sharpe difference, this one tests the
  weights that produced it.
- `notes/2026-09-27-nonlinear-shrinkage-instead-of-counting.md` and
  `notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md` — the spectral view of the
  same `k/n` problem.
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` — Tu–Zhou combine
  the naive rule with an estimated one; result 4 is the reason the estimated component has to be
  shrunk rather than merely scaled.
