---
title: "APT or \"AIPT\"? The Surprising Dominance of Large Factor Models"
authors: Didisheim, Ke, Kelly, Malamud
year: 2024 (NBER WP 33012, September 2024, revised August 2025; earlier circulated as "Complexity in Factor Pricing Models")
venue: NBER working paper (venue tier 2 — not peer-reviewed; the NBER series states this explicitly)
url: https://doi.org/10.3386/w33012
citations: 33 (Crossref, checked 2026-09-26); Semantic Scholar indexes the SSRN record at 5 (checked 2026-09-26)
sample_period: 1963–2023, out-of-sample evaluation beginning 1993 on a rolling 360-month training window
markets: US only — NYSE/AMEX/NASDAQ common stocks (CRSP share codes 10/11/12) excluding the smallest 1% of NYSE-percentile market cap, with 130 firm characteristics
tier: B
validation_overlap: true
published_post_2018: true
---

## Mechanism

This is the cross-sectional version of the complexity argument, and it is the one this lab would
actually build, because the lab predicts a cross-section rather than timing one index. Its
transferable content is **not** the headline that big models win. It is a theorem that names the
**pre-computable condition under which complexity can help at all**, and the condition is a property
of the universe, not of the model.

**The conjecture.** Ross's APT assumes a *low*-dimensional factor structure: a few common factors
drive returns, so exposures to a few factors determine expected returns. The paper's alternative
("AIPT") conjectures that returns are driven by a **large** number of factors, in which case a
pricing model should have many more factors than there are training observations or base assets.

**Limits to learning, and its two components (Theorem 3).** With `c = P/T > 0` — factor count over
training months — there are too many parameters and too few observations for the estimator to
converge to its population counterpart, which leaves a permanent wedge between the trained model's
out-of-sample behaviour and the true model's. The wedge has exactly two parts, and both are
quantifiable from the factors' *sample* covariance in the training data alone:

1. **Implicit shrinkage `Z*(z; q; c)`, monotone increasing in `c`.** A feasible high-complexity
   model with explicit ridge penalty `z` behaves out-of-sample like an *infeasible* model with a
   **larger** penalty `Z*` > `z`. The intuition is mechanical: holding `z` fixed and adding
   parameters, the ridge constraint on `‖λ‖²` can only continue to be satisfied by shrinking the
   coefficient vector further. So **complexity is itself a form of shrinkage** — you do not get to
   choose your effective shrinkage independently of your model size. Two consequences: expected
   return is highest at minimal shrinkage but cannot reach the infeasible benchmark, because `Z*`
   stays bounded away from zero in the high-complexity regime (`c > 1`) even in the ridgeless limit;
   and portfolio **variance falls** as complexity rises past `c = 1`, for the same reason.
2. **Complexity risk `G(z; q; c)`.** Sampling variation that survives even as `T → ∞`, because the
   parameter count grows with the data. It is a pure-variance term, independent of expected factor
   returns, depending only on the eigenvalue distribution of `E[F_t F_t']`, and it is zero exactly
   when `c = 0`.

**The condition that decides the sign, and it is the load-bearing result for this lab.** Raising
complexity has two opposing effects: more factors means better approximation of the true pricing
kernel, and also more severe limits to learning. Which wins is determined by **the eigenvalue
distribution of the factor second-moment matrix**:

- **Dispersed spectrum (many comparably-important factors)** → approximation gains dominate →
  complexity improves out-of-sample behaviour. The paper's AIPT calibration puts the **effective
  rank** at roughly 500.
- **Concentrated spectrum (a few dominant factors — the APT world)** → limits to learning dominate →
  **there are no benefits to complexity**, and with small ridge penalties high-complexity models are
  strictly *worse* than models near zero complexity. The APT calibration's effective rank is about
  2.5. One asymmetry the authors flag honestly: with *moderate* shrinkage there is also no great
  *cost* to complexity in this case, because the overfit cost of redundant parameters is offset by
  the implicit shrinkage that complexity brings with it.

Effective rank is defined as `EffRank(E[FF']) = (tr E[FF'])² / tr((E[FF'])²)` — the inverse-Herfindahl
(participation ratio) of the eigenvalues, i.e. the count of dominant principal components. The same
statistic appears in the theory's finite-asset error term, which is controlled solely by
`tr(Σ²)/(tr Σ)²`.

**Double ascent.** As a function of complexity the out-of-sample Sharpe ratio rises at low `c`,
collapses toward zero near the interpolation boundary `c = 1` as variance explodes, then rises again
for `c ≫ 1` as variance comes under control — "double ascent", the portfolio analogue of double
descent. With appropriate explicit shrinkage the collapse disappears and the curve is increasing
throughout. Pricing errors mirror the Sharpe curve and are bounded away from zero at every
complexity level.

## Construction recipe

**Characteristics.** Monthly US stock returns and characteristics from the Jensen–Kelly–Pedersen
panel; 153 reduced to `D = 130` by dropping those with the most missing values, and stock-months
with more than 30% of the 130 missing are discarded. Each characteristic is **cross-sectionally
rank-standardised and mapped to `[−0.5, 0.5]`** — the same single preprocessing step as the
comparative ML literature, and the only one.

**Factors are characteristic-managed portfolios.** For a random-feature map `S_p(·)`, factor `p`'s
return is `F_{p,t+1} = S_p(Z_t)' R_{t+1}` — i.e. the features *are* the portfolio weights, applied to
next period's returns. Random features are built by sine/cosine activations of random linear
combinations of the 130 ranked characteristics (robustness with `tanh` and `ReLU` activations is
reported).

**SDF fit.** Ridge on the mapping from factor moments to SDF coefficients, sweeping the penalty `z`
and the factor count `P`, with `P` from 36 to 360,000 against `T = 360` months, so `c = P/T` reaches
~1,000. Rolling out-of-sample: at each month use the most recent 360 months to estimate, then record
the next month's SDF portfolio return. Because random features are stochastic, the whole estimation
is **repeated 20 times with different seeds and metrics averaged** (the same caveat as in the
time-series paper applies — an average across seeds is not one implementable model).

**Evaluation.** Two metrics only: the SDF portfolio's out-of-sample Sharpe ratio, and out-of-sample
pricing error aggregated as a Hansen–Jagannathan distance over a large set of anomaly factors as
test assets.

**The screen worth extracting, stated as a procedure.** Before fitting anything large: build the
managed portfolios the candidate would use, form their second-moment matrix on the training window,
and compute its effective rank. A small effective rank places the universe in the source's own APT
calibration, where **its own theory predicts complexity does not pay** — no trial required to reach
that conclusion.

## Robustness evidence (qualitative only)

- **The theorem is proved and the calibrations are derived from it**, so the "which regime am I in"
  result does not depend on the empirical section being right. That is the part of this paper worth
  carrying.
- **The empirical half has three gaps and they are all rubric rows.** It is a working paper with no
  peer review (the NBER cover states this); it is a **single market**; and **transaction costs and
  turnover appear nowhere** — there is no cost model and no turnover accounting, while the object
  being evaluated is a monthly-rebalanced SDF portfolio built from up to 360,000 managed portfolios,
  which is the configuration most likely to trade heavily. Multiple testing is not addressed, though
  the design (one theory, two metrics, a complexity sweep) is not a specification search.
- **Its central empirical claim has a standing objection that is derived rather than measured.**
  A kernel representation of exactly this construction argues that when `P ≫ K` the implied
  mean-variance weights become kernel-smoothed averages of past stock returns — locality being
  similarity in characteristic space — so with short training windows the nearest neighbours of a
  stock are its own recent observations and the strategy acquires a momentum character mechanically,
  with a volatility-timing component from characteristic volatility. See
  `notes/2026-09-26-seemingly-virtuous-complexity-kernel-representation.md`. That objection also
  names a genuine mitigation specific to the panel case: smoothing runs across stocks *and* time, so
  a shorter time dimension may suffice here than in the single-asset case. **This paper uses a
  360-month window, not the 12-month window the objection is sharpest against** — which is the
  fairest statement of where the disagreement stands, and it is unresolved.
- Sample is multi-decade (1963–2023). `validation_overlap: true` — it covers the lab's validation
  window; `published_post_2018: true`. Discount novelty accordingly and import no performance
  expectation from it. The economic-interpretation result (complex models being markedly more
  sensitive to long-run macroeconomic activity than simple benchmarks) is recorded here as a
  direction only.

## Implementability here

**The free screen first, because it can close the question without a trial.** The lab has never
measured whether this universe is in the dispersed-spectrum regime where complexity is predicted to
pay. It can: compute `EffRank = (tr A)² / tr(A²)` for `A` the training-window second-moment matrix
of whatever managed portfolios a proposed learned candidate would use (for a cheap first pass, the
ranked-characteristic sorts the lab already builds; the instrument return covariance is a *different*
matrix and is not the object the theory refers to — say which one was computed). Pre-register the
branch: **a small effective rank puts this universe in the source's APT calibration, where its own
theorem says a large model buys nothing**; a large one is the first positive evidence this lab would
have for spending a trial on a big model. This is a train-only measurement and costs no trial,
though it scores returns, so it is not covered by the folder's holdings-only diagnostic exemption.

**The prior this lab should hold going in, stated so the screen can contradict it.** Three
independent things point at the concentrated-spectrum regime here. This folder's own
effective-number-of-bets note measures that the count of correlation eigenvalues ≥ 1 saturates long
before the instrument count does. `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`
records that sparsity works in the space of *high-variance principal components* precisely because
near-arbitrage logic puts the premium in a few high-eigenvalue directions — which is the
concentrated case by construction. And the lab's universe is ~145 large survivors, where an
independent source predicts most characteristics stop working at all. **So the honest expected
reading is that complexity does not pay here**, and the value of the screen is that it makes that a
measurement instead of an inherited belief. Note the one comfort in the same theorem: in the
concentrated regime with moderate shrinkage there is predicted to be no great *cost* either, so a
complexity result near zero is genuinely uninformative rather than evidence against learning — which
is a reason to run the screen instead of a trial.

**What is structurally unreachable, and it is the same taxonomy as the statistical-arbitrage vein.**
The object here is an **SDF portfolio** — the mean-variance-efficient combination of characteristic-
managed long-short portfolios. Managed portfolios take signed weights by construction, and the
tangency combination of them is unconstrained in sign and scale. Under this repo's long-only,
gross ≤ 1.0, 25%-cap budget that object does not exist, and there is no partial version of it: the
*hedging* half dies and only the **membership** half survives, exactly as this folder's 2026-09-25
constraint taxonomy states. A long-only book built from the top of an SDF-implied score is not the
paper's portfolio and must not be described as one.

**Three further hard limits.**
- **130 characteristics are not available here** — most are fundamentals. The reachable feature set
  is price/volume/range-derived and numbers in the handful, so `K` is small. That is not fatal to the
  construction (random features manufacture `P` from any `K`), but it changes what "many factors"
  can mean: `P` large from `K` tiny is a statement about functional form, not about breadth of
  information.
- **`c = P/T` is bounded by the history, not by ambition.** This repo's monthly rebalance and its
  usable history put `T` in the low hundreds at best, so a model past the interpolation boundary is
  easy to reach and a model at `c ≈ 1` is easy to reach *by accident*. Count parameters against
  training rows before writing the file, and stay away from `c ≈ 1` deliberately.
- **20-seed averaging is not implementable here.** One candidate file, one weight path; fix a seed,
  expect single-draw noise, and do not compare against a seed-averaged number from the literature.

**What the theory buys even if no big model is ever built here.** "Complexity is itself shrinkage"
is a reading rule for the lab's existing results: the 2026-08-29 ridge that "reproduced its own best
input, worse" was, under `Z*`, running at a heavier effective penalty than its nominal one — so its
null is evidence about the estimator's *effective* shrinkage, not about its feature block, and a
re-run with the nominal penalty lowered is a different experiment from a re-run with fewer features.

## Related

- `notes/2026-09-26-virtue-of-complexity-return-prediction.md` — the single-asset predecessor whose
  theory this generalises to the panel.
- `notes/2026-09-26-seemingly-virtuous-complexity-kernel-representation.md` — the standing objection,
  and the weight-vector diagnostic that any candidate built from this recipe should carry.
- `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md` — the low-dimensional counterpart:
  ridge from covariances to means, sparsity in PC space, shrinkage with an economic unit. Its
  concentrated-spectrum premise is this paper's APT calibration.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the same
  inverse-Herfindahl-of-eigenvalues statistic, reached from the diversification literature. The
  screen above is that note's statistic applied to a new question.
- `notes/2026-08-29-machine-learning-cross-section-comparative.md`,
  `notes/2026-09-03-machine-learning-economic-restrictions.md` — the comparative and deflationary
  halves of this family; the second's finding that the *incremental value of nonlinearity* lives in
  hard-to-arbitrage names is the economic version of the spectrum condition.
- `experiments/learnings.md` [2026-08-29] (ridge reproducing its best input) and [2026-09-11] (the
  `statistical-learning` lead, an affine long-only policy, and what the clip did to its breadth).
