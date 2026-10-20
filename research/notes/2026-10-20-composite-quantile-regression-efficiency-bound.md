---
title: "Composite Quantile Regression and the Oracle Model Selection Theory" — a family of check-function losses that estimates the *same* slope as least squares, survives an infinite error variance, and whose relative efficiency against least squares is bounded below by 70.26%
authors: Zou, Yuan
year: 2008
venue: The Annals of Statistics 36(3), 1108–1126 (venue tier 1 — the discipline's flagship theoretical-statistics journal)
url: https://doi.org/10.1214/07-AOS507
citations: 487 (Crossref `is-referenced-by-count`, checked 2026-10-20); 619 (Semantic Scholar by DOI, same date). Both indices resolved on the first call.
sample_period: none — estimator theory plus a synthetic simulation study. No market data of any period appears anywhere in it.
markets: none
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the IMS electronic reprint, `arxiv.org/pdf/0806.2905` (19 pp., 296 KB → 58 KB of clean text, 298 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). The reprint is the published article and says so in its own header ("This is an electronic reprint of the original article published by the Institute of Mathematical Statistics"); it differs from the journal version only in pagination. Project Euclid's own `.pdf` endpoint for the DOI returned **HTTP 200 with a 1,155-byte body that `file` identifies as HTML** — the same "looks like an answer" shape this folder records for several publishers — so the arXiv copy is the one relied on.
---

## Mechanism

No economic mechanism. This is the **estimator-theory layer** directly under
`notes/2026-10-19-consistent-scoring-functions-and-elicitability.md`, and it answers the question
that note leaves open.

Last night's chain established the theorem: a loss function does not measure accuracy, it *names a
functional*. Squared error is consistent for the conditional mean and the Bregman class is exactly
the set of losses that are; the pinball loss is consistent for a quantile and the generalised
piecewise-linear class is exactly the set that is. The immediate and obvious inference — and it is
wrong — is that **if the decision wants something mean-like, the loss must be squared error**. It
need not be. There is a whole family of check-function losses that recovers the *same slope vector*
as least squares, and it has strictly better worst-case behaviour.

The construction. Write the linear model `y = Σ_j x_j β*_j + ε` with centred predictors. The
conditional `100τ%` quantile of `y | x` is `x'β* + b*_τ` where `b*_τ` is the `τ`-quantile of `ε`:
that is, **the slope is the same at every quantile level and only the intercept moves**. A single
quantile regression at level `τ` estimates `(b_τ, β)` jointly. Composite quantile regression (CQR)
fits `K` quantile levels **at once**, with `K` free intercepts and **one shared slope**:

    (b̂_1, …, b̂_K, β̂^CQR) = argmin  Σ_{k=1..K} Σ_{i=1..n} ρ_{τ_k}( y_i − b_k − x_i'β )

with `ρ_τ(t) = τ·t₊ + (1−τ)·t₋` the check function and, typically, equally spaced levels
`τ_k = k/(K+1)`. The objective is a *mixture of the objective functions of K quantile regressions*
sharing their slope — hence "composite". Nothing is averaged after the fact: the sharing is imposed
inside one convex program.

**Why the sharing is the whole point, and why a single quantile is not a safe substitute.** The
paper is explicit about the trap. A single quantile regression — the median / least-absolute-value
regression included — is root-`n` consistent and asymptotically normal even when `ε` has infinite
variance, which least squares is not; so it looks like the robust choice. But *its asymptotic
relative efficiency against least squares can be arbitrarily small*. The authors say in as many
words that they "do not consider it as a safe alternative to the least squares". Combining levels is
what buys a floor: it is the `K`-fold aggregation, not the check function, that makes the estimator
safe.

## Construction recipe

**Limiting distribution (Theorem 2.1).** Under the two standard regularity conditions for quantile
regression asymptotics (`n⁻¹X'X → C` positive definite; a density condition on `ε`),

    √n (β̂^CQR − β*)  →d  N(0, Σ_CQR),
    Σ_CQR = C⁻¹ · [ Σ_{k,k'} min(τ_k,τ_k')·(1 − max(τ_k,τ_k')) ] / ( Σ_k f(b*_{τ_k}) )²

**Asymptotic relative efficiency (Section 3).** Against least squares, whose asymptotic variance is
`σ²C⁻¹` when `σ² < ∞`,

    ARE(τ_1,…,τ_K, f) = σ² ( Σ_k f(b*_{τ_k}) )² / Σ_{k,k'} min(τ_k,τ_k')(1 − max(τ_k,τ_k'))

**The universal lower bound (Theorem 3.1), which is the result to carry.** With `τ_k = k/(K+1)`,
`ARE(K,f)` converges as `K → ∞` to

    δ(f) = 12 σ² ( E_ε[f(ε)] )²

and over the class `F` of all densities satisfying the regularity condition with finite variance,

    inf_{f ∈ F} δ(f) > 6/(eπ) = 0.7026.

`δ` is scale-invariant despite its explicit `σ²`. So **the worst-case cost of using the composite
check-function loss instead of squared error is under 30% of the variance, for every finite-variance
error distribution there is**, and the bound is described by the authors as conservative. The upside
is not bounded at all. Their worked values:

| error density | `δ` (CQR efficiency vs least squares) |
|---|---|
| Normal | 0.955 — least squares is optimal here and CQR gives up 4.5% |
| Logistic | 1.097 — and CQR attains the Fisher information bound exactly |
| Double exponential | 1.5 |
| Student `t`, 3 df | 1.9; `δ → 0.955` as df → ∞ |
| `(1−r)·N(0,1) + r·N(0, r⁶)` | arbitrarily large, with the error variance held bounded |
| any infinite-variance density (e.g. Cauchy) | least squares is not root-`n` consistent at all; CQR still is |

The last two rows are the paper's Examples 5 and the motivating case: a *slight* perturbation of a
normal, leaving the variance finite and bounded, is enough to make CQR arbitrarily more efficient.
The failure of least squares here is not exotic — it is a contaminated normal.

**Variable selection (Section 4).** The adaptively-penalised CQR (ACQR) adds an adaptive-lasso
penalty built from a first-pass CQR fit:

    argmin  Σ_k Σ_i ρ_{τ_k}(y_i − b_k − x_i'β)  +  λ Σ_j |β_j| / |β̂_j^CQR|²

Theorem 4.1: if `λ/√n → 0` and `λ → ∞`, ACQR is **consistent in selection** and attains
`Σ_CQRoracle`, i.e. it performs as well as an oracle that knew the true sparse support — including
when the error variance is infinite, which is exactly where the least-squares oracle theory (SCAD,
adaptive lasso) breaks down, because those estimators mimic a least-squares oracle that is no longer
root-`n` consistent. The relative-efficiency results carry over verbatim to the oracle comparison.
The authors note the SCAD penalty would work too and that they chose the adaptive lasso **for
computational reasons: with it, computing ACQR is a linear program** solvable by a standard LP
solver. The concluding remarks also record the associate editor's generalisation, a weighted
integral `∫₀¹ Σ_i ρ_t(y_i − b_t − x_i'β) w(t) dt`, which makes the level set a design choice rather
than a grid.

## Robustness evidence (qualitative only)

The content is theorems, so "robustness" means the scope of the assumptions rather than a sample.
What is proved: the limiting distribution, the universal lower bound, and the oracle properties of
the penalised version. What is assumed, and these are the live constraints:

- **One shared slope across quantile levels.** This is a *pure location-shift* model for `y | x`:
  the predictors may move the centre of the conditional distribution and nothing else. If the shape
  or scale of the conditional distribution varies with `x`, CQR is a misspecified model of the
  conditional quantiles — it remains a legitimate and well-behaved estimator of a location slope,
  but it is not then a distributional forecast. The paper does not claim otherwise and does not
  study the misspecified case. This is the precise boundary between this note and
  `notes/2026-10-20-forecasting-the-return-distribution-in-the-cross-section.md`, whose entire
  method exists because the shape does vary.
- **`n⁻¹X'X → C` positive definite** — a fixed-`p`, large-`n` asymptotic. There is no
  high-dimensional (`p` growing with `n`) result here, and the oracle theory is about a sparse
  support within a fixed `p`, not about `p > n`.
- **Finite variance for the comparison, not for the estimator.** The efficiency statement needs
  `σ² < ∞` to have something to divide by; the consistency and normality of CQR itself do not.
- Independent replication is not the right category for a 2008 *Annals of Statistics* theorem with
  several hundred citations; the results are proved in the paper and the surrounding literature
  (local CQR, penalised CQR variants) builds on them rather than contesting them. No market claim
  is made anywhere, so there is nothing here for Hou–Xue–Zhang or McLean–Pontiff to decay.

## Implementability here

**What is installed and what is not.** `scikit-learn 1.9.1` ships
`sklearn.linear_model.QuantileRegressor(quantile=…, alpha=…, solver=…)` — an L1-penalised *single*
quantile regression solved as a linear program — and `scipy 1.17.1` ships `optimize.linprog`. So:

- **Single-`τ` quantile regression: directly available, one call.**
- **Exact CQR (one shared slope, `K` intercepts, one objective): not available off the shelf.** It is
  one linear program and `scipy.optimize.linprog` can express it — the design is `K` stacked copies
  of `X` plus `K` intercept dummies, with the per-block check weights differing by `τ_k` — but it has
  to be written, and writing it is the only way to get the theorems' guarantees as stated.
- **The cheap approximation is to fit `K` separate `QuantileRegressor`s and average their slope
  vectors.** Say so plainly if it is used: averaging the slopes of separately-fitted quantile
  regressions is *not* the Zou–Yuan estimator, which imposes the shared slope inside the objective.
  In the location-shift model the two are closely related and the averaged version is the standard
  practical stand-in, but the lower bound of 0.7026 is proved for the composite program, not for the
  average of unconstrained fits.

**Runtime is the binding constraint and it should be measured before anything is designed around
it.** A ridge has a closed form; a quantile regression is an LP whose cost grows badly in the number
of rows, and CQR's program is `K` times the size. `program.md` allows ~60 s per `generate_weights`
call and the protocol makes about seven calls per trial, on a panel where ~1,000 names are eligible
on a typical date. A full-train-split fit is on the order of 10⁵–10⁶ rows before the composite
factor. Three ways out, in order of preference: subsample rows per rebalance date; fit on a reduced
set of rebalance dates (`program.md`'s own advice — "give a model fewer rebalance dates rather than
a cached fit nobody can audit"); reduce `K` (the bound is a `K → ∞` limit but `ARE(K,f)` converges
quickly in `K`, so a handful of levels captures most of it). **Measure one call first.**

**Determinism, which this lab needs at `1e-6`.** An LP solution is deterministic given the data and
the solver, with no `random_state` to fix and no threading to pin — which is a real advantage over
every stochastic learner for passing `causality_check`. The one hazard is **non-uniqueness**: the
check-function objective is piecewise linear and can have a non-unique argmin, in which case the
reported solution is a solver artifact and two runs on a truncated window may differ in a way that
reads as a peek. Keeping a small L1 penalty on, as ACQR does anyway, is the cheap guard.

**The honest size of the prize, and it is a ceiling rather than a promise.** The efficiency result
is a statement about the *variance of the estimator*, not about the existence of signal. A `t`
statistic scales as the inverse standard error, so swapping squared error for a composite check loss
can improve a `t` by at most a factor `√δ` — which is `≈1.38` at `t(3)` errors, `≈1.22` at a double
exponential, and *below* 1 at a Gaussian. That factor is the whole prize available from this
direction, and it should be compared against the lab's own already-recorded numbers before anybody
builds the LP: `learnings.md` [2026-10-19/20] records within-region rank ICs of `+0.0066` (`t +0.28`)
for a pointwise ridge and `−0.0110` (`t −1.08`) for a pairwise-logistic ranker on the lab's free-OHLCV
feature sets. **A 1.38× ceiling on a `t` of `+0.28` does not reach anywhere, so this is an
estimator-efficiency argument that arrives too late to rescue those features** — see
[Related](#related) for why that is the right reading rather than a reason to try it. Where it is
genuinely free: *any* penalised linear fit this lab runs on a heavy-tailed panel could be reported
alongside its `δ̂` — a one-line plug-in from the residual density at the fitted quantiles,
`12·σ̂²·(mean of f̂ at the K fitted intercepts)²` — which says whether squared error was costing
anything on that panel at all. That diagnostic answers an open question for free and costs no trial.

## Related

- **Directly underneath** `notes/2026-10-19-consistent-scoring-functions-and-elicitability.md`. That
  note's theorem says the loss names the functional. This one says the map from functionals to losses
  is not a bijection in the direction that matters: the *slope* of a location model is reachable from
  an entire family of check-function losses, with a worst case of −30% variance and an unbounded best
  case. Both notes are needed to state the whole claim, and together they close a question rather
  than open one.
- **Tension with a measured refutation, stated explicitly as `research/README.md` requires.**
  `learnings.md` [2026-10-19/20] closed the objective-function branch of `statistical-learning` for
  zero trials, on the structural ground that "an ordinal loss cannot create ordering information the
  features do not carry" and that the lab's rank-IC screens were already ordinal. **This note does
  not contradict that and in fact strengthens it**, which is worth recording because the superficial
  reading goes the other way. CQR is not an ordinal loss and the lab's refutation does not apply to
  it verbatim: it is a *location-slope* estimator, in the same equivalence class as the ridge the lab
  fitted, and the thing it changes is estimator variance. But the theorem *bounds* that change —
  `√δ`, at most ~1.38 on the lab's own panels — so the refutation survives the one route around it
  with room to spare, and now survives it with a number rather than an argument. The transferable
  form: **a loss swap inside the same functional class buys variance, never signal, and the ARE gives
  the exact ceiling on the variance it can buy.**
- **Boundary against** `notes/2026-10-20-forecasting-the-return-distribution-in-the-cross-section.md`
  (shape varies with `x`, so the shared-slope assumption is the thing that paper discards) and
  `notes/2026-10-20-distributional-conformal-prediction.md` (what a predicted distribution is worth
  when the model is wrong, which is the case CQR's theorems do not cover).
- Adjacent on method, not on object: `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md`
  (lasso-based estimation at panel width, and the same "guarantees attach to the mean-free half"
  caution), and `notes/2026-08-29-machine-learning-cross-section-comparative.md` (the lab's standing
  "penalised linear model first" source).
