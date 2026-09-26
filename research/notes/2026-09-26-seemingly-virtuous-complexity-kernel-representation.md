---
title: "Seemingly Virtuous Complexity in Return Prediction"
authors: Nagel
year: 2025
venue: NBER working paper w34104 / SSRN (venue tier 2 — working paper, Tier-1 author)
url: https://doi.org/10.3386/w34104
citations: 14 (Crossref, NBER record `10.3386/w34104`, checked 2026-09-26); the two SSRN records for the same work read 1 and 0 (Crossref, same date); Semantic Scholar's title endpoint returned HTTP 429 and was not retried
sample_period: 1926–2020 (the replication data of the paper it examines), plus artificial data built from it
markets: one asset — the US equity index — from 15 monthly predictors; a cross-sectional extension is derived but not estimated
tier: B
validation_overlap: true
published_post_2018: true
---

## Mechanism

This is the note to read before building anything complex. It is an **identity**, not an
estimate: it says what a high-complexity ridgeless regression *is*, and the answer is that it is a
weighted average of the training window's realised returns, with weights that are mostly decided
before any return is seen.

**The general statement, which is not specific to random features.** For a predictive regression
with `P > T`, training-window returns `r_t` and predictor matrix `Z_{t−1}` (`T × P`), the ridgeless
forecast is

    r̂_{t+1|t} = w_t' r_t ,    w_t' = z_t' Z_{t−1}' (Z_{t−1} Z_{t−1}')^{−1}

so the forecast — and therefore the position, when the position is the forecast — is a **weighted
average of the `T` returns in the training window**. The weights are the coefficients of a
regression of the *current* predictor vector on the *lagged* predictor vectors: they measure how
similar each past predictor vector is to today's, and **greater similarity means higher weight**.
Nothing in `w_t` depends on the returns. This holds for any overparameterised predictive
regression, whatever the features are.

**What the weights then look like, and why it is mechanical.** With random Fourier features and
`P ≫ K`, dot products of feature vectors converge to a Gaussian kernel of the original `K`
predictors, `k(x_t, x_{t−k}) = exp(−(γ²/2)‖x_t − x_{t−k}‖²)`, so the ridgeless RFF forecast
approximates kernel ridgeless regression,
`r̂_{t+1|t} ≈ k(x_t, X_{t−1}) K(X_{t−1}, X_{t−1})^{−1} r_t`. Two properties of real predictors then
fix the shape of the weights:

1. **Persistence ⇒ momentum.** If predictors are persistent, the predictor vector most similar to
   today's is usually **last month's**, the next most similar the month before, and so on. So
   similarity is, in a short window, mostly *temporal proximity*, weights decline with lag, and the
   forecast is a recency-weighted average of recent returns — a **momentum rule**, arrived at with
   no evidence that momentum exists.
2. **Heteroskedasticity ⇒ volatility timing.** Distances between predictor vectors are larger when
   predictor innovations are more volatile, so similarity and hence the *magnitude* of all the
   weights falls when predictor volatility rises. The position therefore scales roughly with the
   reciprocal of predictor volatility: the rule **de-risks when predictor volatility rises**, with
   no forward-looking content whatsoever.

Combined: a high-complexity ridgeless regression on persistent, heteroskedastic predictors and a
short window is a **volatility-timed momentum strategy by construction**. The author's summary of
his own finding is that the method's strong historical showing "reflects fortunate coincidence" —
the mechanically-produced strategy happened to work in the sample — rather than learning.

**The geometric reason complexity cannot rescue a short window.** With `T ≪ P` the fitted model
projects onto a `T`-dimensional *random* subspace of the `P`-dimensional predictor space. What can
be learned is bounded by `T`, not by `P`; most of the predictor space is never examined, so signal
variation is small while noise is not. The author draws the general lesson that in asset pricing the
ratio of sample size to model complexity is far lower than in the machine-learning applications
this method was imported from.

**The nuance, recorded because it is easy to overstate this paper.** The author explicitly does
*not* claim complexity is generally harmful: a complex model will often beat an ad hoc sparse
misspecified one. What he rejects is that complexity **enables discovery of predictability from
very small training samples**. The target is `T`, not `P`.

## Construction recipe

There is no strategy to implement here — the recipe is a set of **diagnostics**, and they are what
makes this note worth more to this lab than the paper it critiques.

**Diagnostic 1 — print the implied weight vector on past returns.** For any linear-in-parameters
forecast (ridge, ridgeless, kernel ridge, PCR, a linear stack) the forecast can be written
`r̂ = Σ_k w_k r_{t−k+1}` with `w` computable in closed form and **independent of the realised
returns**. Plot the time-series mean of `w` against lag, and separately plot the mean of `w` over
time. The first plot says which past-return pattern the estimator holds (declining in lag ⇒
momentum); the second says whether the position's scale is being timed by something, and against
what.

**Diagnostic 2 — the sign-flipped synthetic placebo.** Build artificial returns by adding a
simulated MA(2) component with strong negative autocorrelation to the real return series, so the
artificial series **reverses** where the real one trends. Refit the same estimator on the
artificial data and look at the weights again. If the estimator is learning, the weights should
change sign; if the weights are unchanged, the estimator is imposing a structure rather than
finding one. In the source's hands the weights are unchanged and the resulting strategy earns
*negative* abnormal returns on the artificial data — which is the stronger version of the argument,
since a learning estimator would have to be shown to *mis*learn in exactly the wrong direction.

**Diagnostic 3 — the predictor wild bootstrap.** Wild-bootstrap the `K` raw predictors to destroy
predictive content while preserving their persistence and the time path of their innovation
volatilities. This removes predictive information in linear combinations, first-order interactions
and odd powers of the innovations, while preserving the *similarity structure* that sets the
weights. If out-of-sample performance survives the bootstrap essentially intact, the performance
was coming from the mechanical weighting, not the predictors.

**Diagnostic 4 — the hand-built mechanical benchmark.** Write down the simple rule the mechanism
predicts and check whether it spans the complex one. Here that rule is a **linearly-declining-weight
momentum signal scaled by inverse predictor variance**:

    r̂_volmom = 0.05 × (1 / σ̂²_{x,t−1}) × Σ_{k=0..11} ((12 − k)/78) · r_{t−k+1}

where `σ̂²_{x,t−1}` is the average variance of the `K` predictors over the 12-month window and 78
normalises the lag weights to sum to one (the 0.05 only matches position scale and affects no
t-statistic). Then regress the complex strategy's returns on this one. In the source the simple
rule's positions closely resemble the complex rule's and absorb most of its abnormal return.

**Method note worth copying independently of all the above.** The critique isolates one
construction choice at a time: the target's volatility standardisation is *removed* rather than
argued about (the author works with unstandardised returns because standardising the dependent
variable by trailing volatility can itself generate predictability absent from raw returns), and
the feature standardisation is added back in a separate step so its effect on the weights is
visible on its own.

## Robustness evidence (qualitative only)

- **The core claim is algebra plus a kernel convergence result from the machine-learning
  literature, so it does not need replication in the way an empirical anomaly does** — the identity
  `w_t' = z_t' Z_{t−1}'(Z_{t−1}Z_{t−1}')^{−1}` can be verified on paper, and the similarity
  interpretation follows from it directly. That is why this note is graded B rather than C despite
  being an unrefereed working paper: the load-bearing part is checkable without the author's data.
- The empirical half uses the criticised paper's **own replication data**, which is the right
  design for a critique and removes data-choice as an explanation of the disagreement.
- It converges with at least three independent critiques reaching compatible conclusions by
  different routes — an attainability objection about averaging across random-feature draws (Berk),
  an implementation objection about the zero-intercept restriction and the cross-draw aggregation
  (Buncic, with a published reply from the original authors), a measurement-error limit (Cartea, Jin
  and Shi) and information-theoretic impossibility bounds for windows this short (Fallahgoul).
  **None of these four was read here** — they are recorded as the source describes them, and nothing
  above rests on them.
- The **cross-sectional extension is derived, not estimated.** The author shows the same logic
  applies "at least in part" to an SDF built from random-feature factors of firm characteristics:
  the implied mean-variance weights become kernel-smoothed averages of past stock returns, where
  locality is similarity in characteristic space, so with a short window the closest matches to a
  stock are that same stock's recent observations — imparting a momentum character — and lower
  characteristic volatility again tightens clustering and raises weights. He states one genuine
  mitigation: because smoothing runs across **both** stocks and time, a shorter time dimension may
  suffice in the panel than in the pure time-series case. Treat the cross-sectional version as a
  derivation awaiting evidence, not as a measured result.
- Costs and turnover are not modeled; they are not relevant to the argument, but it means nothing
  here speaks to net performance.
- `validation_overlap: true` via the inherited sample. No period-specific figure is recorded above.

## Implementability here

This note costs no trial and it changes what a learned candidate in this repo has to prove.

1. **New free screen, and the folder has no instance of it: any learned candidate must print the
   implied weight vector on past returns before it is run.** `learnings.md`'s existing design rule
   (2026-08-29) screens the *feature block* — a learned candidate earns a trial only if no single
   feature already works alone, or if the model is asked for something a sort cannot express. That
   rule would **pass** an estimator that mechanically rebuilds momentum from features containing no
   trend at all, because persistence plus a short fitting window is enough. The weight-vector print
   catches it and costs nothing: it is holdings-side algebra, reads no returns, and is available in
   closed form for every estimator this repo can fit. **This is the direct extension of
   `notes/2026-08-17-moving-average-rules-anatomy.md`'s screen from linear filters to learners**, and
   it is more decisive here because the weights are provably return-independent.
2. **It supplies the mechanism for a result the lab has already measured and filed as a puzzle.**
   `learnings.md` [2026-08-29]: a ridge over eleven features returned `rho = 0.774` to a momentum
   champion, and a version with trend features deliberately removed returned `rho = 0.976` to a
   single sort on one of its own inputs. The folder recorded this as "feed a learner the incumbent's
   features and it rediscovers the incumbent, worse". This note says the rediscovery **need not come
   through the features at all** — a short-window fit on persistent predictors builds a
   recency-weighted return average regardless — so the lab's rule should be stated on the estimator's
   implied weights rather than on its inputs. Note honestly that the lab's ridge was fitted with
   `P < T`, not `P > T`, so the exact identity above does not apply to it; the *similarity-weighting
   intuition* is what carries, and the weight print is how to test whether it does.
3. **A pre-registrable placebo design this repo can run without new machinery.** Diagnostic 2 is
   the sign-flipped synthetic target, and this lab already has the habit (placebos on region
   labels, on vintages, on characteristics that read no market data). For a learned candidate the
   placebo is stronger than usual because the prediction is exact: **the implied weights must not
   move** when the DGP's autocorrelation is reversed, if the estimator is not learning. That is a
   pass/fail branch statable before the number exists, which is what this lab's protocol rewards.
4. **It predicts, rather than merely explains, where this repo's learned candidates will fail.**
   This universe's features (volatility levels, illiquidity, valuation-free price aggregates) are
   persistent and heteroskedastic, which is exactly the configuration that makes the mechanical
   momentum artifact appear. Combined with a monthly rebalance and a training window measured in
   tens-to-hundreds of months, any kernel-like learner here should be *expected* to produce a
   vol-scaled trend book correlated with the incumbent. The honest consequence is that
   **`statistical-learning`'s correlation-to-champion problem is structural, not a feature-selection
   bug**, and a decorrelated learned leg needs an estimator whose implied weights are *not* a
   decaying function of lag — which is a constraint on the estimator class, not on the feature list.
5. **One caution against over-reading it.** The paper does not say complex models are bad; it says
   small training windows cannot support them. This repo has a long monthly history available for
   training, so the reachable response is **a longer training window with heavier shrinkage**, not
   abandonment of the family. What is refuted is the appealing idea that a 12-month window plus a
   huge feature count is a shortcut around the sample-size problem.
6. **What is *not* reachable**: the market-timing position rule (signed, unbounded leverage) and
   anything requiring the strategy to short. As with this folder's statistical-arbitrage taxonomy,
   the reachable half of an imported learned construction is the part that decides **membership**.

## Related

- `notes/2026-09-26-virtue-of-complexity-return-prediction.md` — the source under examination. The
  construction recipe there should not be used without the weight print here.
- `notes/2026-09-26-large-factor-models-aipt-complexity.md` — the cross-sectional complexity claim;
  this note's section on the panel case is the standing objection to it, and the two together give
  a pre-registrable pair of readings.
- `notes/2026-08-17-moving-average-rules-anatomy.md` — the original weight-vector screen, for linear
  trend filters. This note generalises it.
- `notes/2026-08-29-machine-learning-cross-section-comparative.md` — the comparative study's
  "shallow beats deep, dearth of data, low signal-to-noise" conclusion is the same sample-size
  argument reached empirically rather than geometrically.
- `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` — the other source that
  predicts *this* universe in particular will produce nulls.
- `experiments/learnings.md` [2026-08-29] (the ridge that rediscovered the incumbent) and
  [2026-09-11] (the long-only clip that took breadth out of a policy's control).
