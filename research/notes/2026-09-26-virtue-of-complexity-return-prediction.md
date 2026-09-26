---
title: "The Virtue of Complexity in Return Prediction"
authors: Kelly, Malamud, Zhou
year: 2024
venue: Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/jofi.13298
citations: 215 (Crossref, checked 2026-09-26); Semantic Scholar returns *not found* for the JF DOI and indexes only the NBER/SSRN stub record at 1 (checked 2026-09-26)
sample_period: 1926–2020 (estimation sample begins 1930 after a 36-month standardisation warm-up)
markets: one asset — the CRSP value-weighted US equity index — predicted from 15 monthly Goyal–Welch variables
tier: B
validation_overlap: true
published_post_2018: true
---

## Mechanism

The claim is about the **relationship between a model's parameter count and its out-of-sample
portfolio performance**, not about any particular predictor. Conventional reasoning says that as
the number of regressors `P` approaches the number of training observations `T`, the regressor
covariance matrix becomes unstable, its inverse explodes, forecasts vary wildly, expected
out-of-sample `R²` tends to negative infinity, and a portfolio built on those forecasts has
divergent variance and a Sharpe ratio collapsing to zero. This is the standard overfitting story
and the paper confirms it *at* `P ≈ T`, which it calls the **interpolation boundary**.

The paper's result is about what happens **past** that boundary. When `P > T` the inverse
covariance matrix does not exist but the pseudo-inverse does, and it coincides with ridge
regression in the limit of infinitesimal shrinkage (the **"ridgeless"** estimator). Using random
matrix theory in the limit `T → ∞`, `P/T → c > 0`, the authors prove that timing strategies built
on ridgeless least-squares forecasts earn positive Sharpe-ratio improvements at arbitrarily high
complexity `c`, and that performance **recovers** past the boundary rather than degrading
monotonically. The statistics literature calls the underlying phenomenon *benign overfit* or
*double descent*; the economic content here is that a model fitting its training data exactly can
still produce a profitable position rule. The mechanism for the recovery is that the ridgeless
solution, among the many that interpolate the training data, selects the **minimum-norm** one, so
`z → 0` still regularises: the constraint moves from the penalty to the solution set.

Three secondary results carry more transferable content than the headline:

1. **Out-of-sample `R²` is an incomplete measure of a forecast's economic value, and its failure
   mode is one-directional.** Mean squared forecast error decomposes into a scale-free
   (correlation) component and a scale-dependent one; trading performance depends on the
   scale-free part. A coefficient estimate many times too large drives `R²` deeply negative
   without changing the correlation between fitted and true conditional expectations. The
   properties of least squares make the timing strategy's *expected* return always positive, so a
   substantial Sharpe ratio is compatible with a negative `R²` — the `R²` is negative because the
   variance of the fits is wrong, and only the variance is fixable by shrinkage.
2. **Shrinkage and complexity are complements, and the boundary is where shrinkage matters most.**
   Heavier ridge shrinkage biases forecasts downward, which lowers expected timing return, but
   reins in variance by more; the Sharpe ratio typically improves. The gain is largest near
   `P ≈ T`, which is exactly where the ridgeless estimator is most vulnerable.
3. **Expected return and "leverage" are the two objects that recur throughout the analysis.** The
   strategy's position *is* the forecast (`π_t = S_t'β`), so a forecast whose scale is wrong is a
   position whose size is wrong. The paper tracks `E[π_t R_{t+1}]` and the expected magnitude of
   positions as separate quantities, and the Sharpe ratio is their ratio in the limit.

## Construction recipe

**Features (random Fourier features, RFF).** Take a `K`-vector of raw predictors `G_t` (here
`K = 15`). Draw `ω_i ~ i.i.d. N(0, I_K)` and form pairs
`S_i,t = [sin(γ ω_i' G_t), cos(γ ω_i' G_t)]'` with bandwidth `γ = 2`. Each draw yields two
features, so any `P` is reachable from a fixed `K` by drawing `P/2` weight vectors. This is
algebraically a wide two-layer network whose first layer is *random and fixed* and whose second
layer is the linear regression — no first-layer training, hence no optimiser, no seeds beyond the
feature draw, and a closed-form fit.

**Preprocessing.** Returns are volatility-standardised by a trailing 12-month standard deviation
computed from the uncentered second moment; predictors by an expanding-window standard deviation
(they are far more persistent); RFFs by their **training-window** standard deviations. All three
are backward-looking. A 36-month warm-up is required before the first predictor standardisation is
considered stable. The regression has **no intercept** (footnote 35 states that adding a constant
leaves the results unchanged because the intercept is shrunk very heavily).

**Fit and forecast.** Rolling window `T ∈ {12, 60, 120}` months. For each `t`, fit ridge with
penalty `log₁₀(z) ∈ [−3, 3]` on `{(R_s, S_{s−1})}` inside the window, forecast `β̂'S_t`, and take
the position `π_t = β̂'S_t` — i.e. the position equals the predicted return, which is the
conditional Markowitz solution under the paper's homoskedastic normalisation and differs from the
unconditional mean-variance optimum only at third order.

**Complexity sweep.** `P` from 2 to 12,000, so `c = P/T` reaches ~1,000 at `T = 12`. Because low-`P`
results depend on which random features were drawn, the entire pipeline is repeated **1,000 times**
with independent RFF draws and performance statistics are **averaged across repetitions**.

**The one parameter that is not swept**: `γ`. Set to 2, with robustness asserted in the text.

## Robustness evidence (qualitative only)

- The sample is multi-decade and the data set is the field's most-used predictor panel, so the
  inputs are not the weak point.
- The theory is a proof, not an estimate: it needs no replication, and its statements about the
  interpolation boundary and the shrinkage–complexity interaction hold for any data satisfying its
  assumptions. **The empirical claim is a different object and is actively contested.** At least
  four independent lines of work dispute either the interpretation or the implementation: a kernel
  representation showing the high-complexity estimator reduces mechanically to a
  volatility-timed momentum rule (see
  `notes/2026-09-26-seemingly-virtuous-complexity-kernel-representation.md`); an argument that the
  reported performance is not attainable because it averages across 1,000 random-feature draws
  rather than describing one implementable model (Berk 2023, **not read here**, known only from
  that paper's description); an implementation critique attributing the result to the zero-intercept
  restriction and the cross-draw aggregation scheme, with a published reply arguing that
  pre-aggregating across draws itself constructs a complex model (Buncic 2025 and Kelly–Malamud
  2025, **neither read here** — SSRN returned HTTP 403 to an automated client and no mirror was
  found in four attempts); and information-theoretic bounds arguing that learning relationships of
  this complexity from windows this short is impossible (Fallahgoul 2025, **not read here**). The
  tier reflects this: a Tier-1 venue and a healthy citation count, but **no independent
  replication that survived scrutiny**, one market, one asset, and no costs.
- **Costs are not modeled anywhere.** There is no turnover accounting and no transaction-cost
  model; every performance statement is gross. The strategy's position size is the forecast itself,
  so leverage is unbounded and strongly time-varying, and the paper treats that magnitude as a
  quantity to measure rather than to constrain.
- `validation_overlap: true` — the sample runs to 2020 and so touches the lab's validation window.
  Nothing period-specific is recorded here, but the flag should discount novelty on any hypothesis
  that leans on this source's empirics.

## Implementability here

**What transfers, and it is free.**

- **Do not grade a learned candidate by out-of-sample `R²`, in either direction.** A negative `R²`
  is not disqualifying (it may be pure scale error, which the position-sizing step can absorb), and
  a positive one is not evidence of tradeable content. This lab is scored on net Sharpe, which is
  the right target under the paper's own decomposition — the point is only that an `R²` gate added
  as a screen would reject good candidates and pass bad ones.
- **Never operate a learned candidate near `P ≈ T`.** This is a *design* rule, checkable before any
  data is touched: count the fitted parameters and the training rows. The boundary is the one place
  where the estimator is provably at its worst, and a candidate that lands there will look like
  evidence against learned models when it is only evidence about the boundary. Either stay clearly
  below it (a handful of parameters, which is what `learnings.md`'s own design rule already
  prefers) or go far past it with real shrinkage.
- **The RFF construction is cheap enough to run inside this repo's time budget**, which is unusual
  for a learned candidate: the first layer is random and never fitted, so each rebalance is one
  ridge solve on a `T × P` matrix. It is deterministic given the feature draw's seed, which the
  causality check requires. `CLAUDE.md`'s ~60s-per-call budget is the binding constraint on `P`, not
  the estimator.

**What does not transfer, and the gap is structural.**

- **The theory is single-asset market timing, and the paper says so.** Its own footnote 2 states
  that applying the analysis to a panel is complicated by the covariances of returns and signals
  across stocks. This lab's `statistical-learning` candidates are cross-sectional; the cross-
  sectional version of the argument is a separate paper with a separate theorem
  (`notes/2026-09-26-large-factor-models-aipt-complexity.md`).
- **The position rule is unreachable here.** `π_t = forecast` is a signed, unbounded, time-varying
  leverage rule. This repo is long-only with gross leverage ≤ 1.0 and a 25% position cap, so the
  mapping from forecast to position must be replaced by a rank or weight rule — and that
  replacement is exactly where the source's Sharpe statements stop applying, because its Sharpe is
  a property of the *unconstrained* affine map. `learnings.md` (2026-09-11) has already measured
  what a long-only clip does to an affine policy: it becomes a band whose width you do not control.
- **Averaging 1,000 independent draws is not a strategy**, and this repo cannot even pretend
  otherwise: `run_experiment.py` evaluates one candidate file producing one weight path. If an RFF
  candidate is ever built here, it must fix **one** draw (seeded), and the honest expectation is the
  performance of a single draw, which the source's own text says is noisy at low `P`.
- **The target-standardisation step needs care.** Dividing returns by a trailing volatility before
  fitting is a construction choice, not a neutral normalisation, and an independent analysis
  (the kernel note) argues it can *generate* predictability absent from the raw returns. If a
  candidate here standardises its target, that choice must be stated and ideally tested both ways.

## Related

- `notes/2026-09-26-seemingly-virtuous-complexity-kernel-representation.md` — the critique that
  supplies the mechanical account of what this estimator actually holds. Read the two together;
  the construction recipe above is only safe to use with that note's diagnostic attached.
- `notes/2026-09-26-large-factor-models-aipt-complexity.md` — the cross-sectional version, and the
  one whose theorem names a *pre-computable* condition for whether complexity can help at all.
- `notes/2026-08-29-machine-learning-cross-section-comparative.md` — the comparative study whose
  finding is nearly the opposite emphasis (shallow beats deep, few features, dimension reduction
  beats selection). Both cannot be the whole story; the eigenvalue condition in the AIPT note is
  the variable that decides between them.
- `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md` — the same shrinkage-with-an-
  economic-unit idea, reached from a low-dimensional direction, and the source of this folder's
  standing "sparsity in PC space, not characteristic space" result.
- `notes/2026-08-17-moving-average-rules-anatomy.md` — the "write the rule as its weight vector
  over past returns" screen. The kernel note extends that screen from linear filters to this
  estimator, which is the single most useful thing in this cluster for this lab.
- `experiments/learnings.md` [2026-08-29] — "feed a learner the incumbent's features and it
  rediscovers the incumbent, worse" (ridge, `rho = 0.774`). The kernel note argues this can happen
  **even with no trend feature in the block**, which strengthens the lab's design rule rather than
  contradicting it.
