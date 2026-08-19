---
title: "Least Squares Model Averaging"
authors: Hansen
year: 2007
venue: Econometrica 75(4), 1175–1189 (venue tier 1)
url: https://doi.org/10.1111/j.1468-0262.2007.00785.x
citations: 856 (Semantic Scholar by DOI, checked 2026-08-19)
sample_period: n/a — theory plus a Monte Carlo experiment (100,000 draws per parameterisation); no market data
markets: none (econometric methodology)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the model-averaging literature `SUMMARY.md` asked for — the strand outside the
break-detection framing — and its contribution to this lab is a **boundary condition**: it
identifies exactly when averaging with *estimated* weights is provably better than selecting,
which sharpens the folder's standing "averaging beats selecting, equal weights are
load-bearing" principle from a taboo into a rule with a stated precondition.

Setup: a linear regression `y_i = μ_i + e_i` with `μ_i = Σ_j θ_j x_ji` a countably infinite
series, and a sequence of nested approximating models where model `m` uses the first `k_m`
regressors. A **model average estimator** is a convex combination `Θ̂ = Σ_m w_m Θ̂_m` of the
least-squares estimates from those models, weights on the unit simplex. Hansen's framing of
the objective is worth quoting because it is exactly the lab's situation one level over:
"the goal in model averaging is to **reduce estimation variance while controlling omitted
variable bias**."

Three results matter here.

**1. Averaging over nested models *is* shrinkage.** With orthogonal regressors, the `j`th
element of the model-average estimator equals the `j`th element of the largest unconstrained
estimator multiplied by `Σ_{m ≥ j} w_m`. Because that sum is decreasing in `j`, coefficients
on later (higher-order, further-out) regressors are shrunk hardest. Averaging across a nested
ladder of models is therefore not a separate technique from shrinkage — it is a particular,
data-ordered shrinkage profile.

**2. Weights chosen to minimise a Mallows criterion are asymptotically optimal.** The Mallows
criterion is an *estimate of the average squared error* of the averaged fit (fit plus a
penalty term in the effective number of parameters and the error variance). Hansen shows this
criterion is asymptotically equivalent to the squared error itself, so the empirically
minimising weight vector is asymptotically equivalent to the infeasible optimal one, and the
resulting MMA estimator "asymptotically achieves the lowest possible squared error in the
class of model average estimators". The proof is an application of Li (1987).

**3. Averaging can beat the best single model even when the best single model is known.** In
the Monte Carlo, risk is normalised by that of the **infeasible optimal least squares
estimator** — the single best-fitting model, chosen with oracle knowledge. MMA's normalised
risk is *below 1 in many cases*. Separately, smoothed-AIC beats AIC *selection* throughout,
which the author notes is consistent with earlier literature. The claim "pick the right model
and you do as well as any average" is therefore false in this setting, not merely
impractical.

Hansen states two limitations himself, both load-bearing for anyone importing the result:

- **Conditional homoskedasticity is required.** Mallows-criterion selection is not optimal
  under heteroskedasticity (Andrews 1991b), and MMA's optimality "will similarly fail".
- **The weights are restricted to a discrete set** in the asymptotic theory, because
  uniformity over an unbounded-dimension continuous weight vector could not be established.

And one empirical caveat from the simulation: the ranking of MMA against smoothed-BIC
"depends strongly on sample size", with smoothed-BIC winning at small `n` and MMA improving
as `n` grows. The good behaviour of estimated weights is an asymptotic property that arrives
gradually.

## Construction recipe

For the record, since it is the object the lab must *not* naively copy:

1. Order the regressors and form a nested ladder of `M` approximating models.
2. Estimate each by least squares; obtain `σ̂²` from the largest model.
3. Choose weights `w` on the simplex minimising the Mallows criterion — the averaged
   residual sum of squares plus `2σ̂²` times the weighted effective parameter count.
4. Form the averaged coefficient vector.

The single design ingredient that makes step 3 legitimate is that the criterion being
minimised is an (asymptotically) unbiased estimate of *the very loss you care about*, computed
from the same sample. Without that, minimising an in-sample criterion over weights is just
in-sample fitting of the weights.

## Robustness evidence (qualitative only)

- Econometrica, heavily cited, and the core optimality result is a theorem rather than an
  empirical regularity — it cannot decay.
- The simulation is a Monte Carlo over an infinite-order regression design with 100,000 draws
  per parameterisation, across sample sizes and population `R²`; the qualitative rankings
  (averaging beats selecting; MMA's advantage grows with `n`) are stable across the grid.
- The limitations are stated by the author rather than discovered by critics, which is a
  methodology-honesty point in the source's favour.
- Scope weakness for this repo: homoskedastic linear regression with i.i.d. sampling. Daily
  asset returns are strongly heteroskedastic and serially dependent in variance, so the
  headline optimality result is out of scope here by the author's own condition, not by
  interpretation.

## Implementability here

**1. It resolves an apparent contradiction with the folder's own top-ranked screen.** The
folder records "averaging beats selecting, whenever the selection would have to be estimated",
and separately warns that estimating weights is the mistake three literatures agree on. A
tier-1 result showing *estimated* weights are asymptotically optimal looks like a
counterexample. It is not, and the reconciliation is a checkable list of conditions rather
than a judgement call. Estimated averaging weights are justified when:

  (a) there is an **unbiased in-sample estimate of the loss being minimised** (Mallows/`C_p`
      given `σ̂²`);
  (b) the components are **nested and ordered**, so the weight vector has low effective
      dimension and a shrinkage interpretation;
  (c) errors are **conditionally homoskedastic**;
  (d) the sample is **large relative to the number of weights** — the advantage grows with `n`
      and reverses at small `n`.

  This repo's setting fails all four. Its loss is a deflated Sharpe over ~6 years of daily
  returns, and there is *no* unbiased in-sample estimator of it — the deflation machinery
  exists precisely because in-sample Sharpe is upward-biased under selection. Returns are
  heteroskedastic. The components being averaged (formation vintages, lookback windows,
  sleeves) are not a single nested ladder with a natural order. And the effective sample is
  short. **So equal weights remain correct here — but now for four stated reasons rather than
  as a rule of thumb, and the rule is falsifiable: if a future setting meets all four, the
  prohibition does not apply to it.**

**2. The strongest transferable claim is about the question, not the answer.** Averaging beat
the *infeasible optimal* single model in many parameterisations. So "which formation vintage
/ which lookback window is best?" is not merely an unanswerable question in a short sample —
it is the **wrong question**, because the best single member need not be as good as the
average. That is a stronger statement than the folder currently records (which is the weaker
"the selection would have to be estimated, and estimation is noisy"), and it should raise, not
lower, confidence in the equal-weighted multi-vintage construction.

**3. A reading of what the four-horizon average actually is, offered as interpretation.** The
lab's four lookback windows (roughly 63/126/189/252 days, all ending at the skip-month) are
**nested**: each shorter window's data is contained in each longer one. Under Hansen's
orthogonal-regressor identity, equal-weight averaging across a nested ladder is a shrinkage
profile that downweights the increments only the longest windows can see — monotonically,
with no parameter estimated. That is a concrete description of what `#42` does to the *score*,
and it connects two existing candidate entries: the construction has a definite weighting
shape over past returns, which is exactly the object candidate #3's closed-form triage rule
(write any trend/MA signal as its weight vector over past price changes) operates on. **Two
boundaries on this reading, both real:** the identity holds for orthogonal regressors and the
lab's nested return windows are not orthogonal; and the lab averages *portfolios*, not scores
— the per-window buffered selection is nonlinear, which is precisely the difference the
bagging note says is where the gain lives. So the shrinkage picture describes the score
ladder, not the realised book, and it is offered as a lens rather than a result.

**4. What not to do with this.** Do not build a Mallows-weighted or otherwise criterion-fitted
blend of vintages, sleeves or horizons. Condition (a) is the one that cannot be repaired here,
and the folder already has the empirical instance of what happens when weights are fitted to
something noisy: two inverse-vol reweighting refutations and a spacing-correction null.

## Related

- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the combination
  puzzle (simple mean beats estimated-optimal weights) is the *other* side of the same
  boundary; this note explains what has to be true for the estimated weights to win instead.
- `notes/2026-08-17-averaging-over-estimation-windows.md` — averaging over estimation windows,
  the break-framing strand.
- `notes/2026-08-19-bagging-averaging-unstable-predictors.md` — why averaging portfolios and
  averaging scores are different operations, which bounds how far the shrinkage reading in (3)
  can be pushed.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the parameter-counting screen this note
  gives a precise exception to.
- `notes/2026-08-17-moving-average-rules-anatomy.md` — candidate #3's weight-shape triage rule,
  which point (3) above says now applies to the champion's own horizon ladder.
