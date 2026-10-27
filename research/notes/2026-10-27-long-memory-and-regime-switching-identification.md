---
title: "Long memory and regime switching"
authors: Diebold, Inoue
year: 2001
venue: Journal of Econometrics 105(1), 131–159 (venue tier 1)
url: https://doi.org/10.1016/S0304-4076(01)00073-2
citations: 865 (Crossref `is-referenced-by-count`, checked 2026-10-27)
sample_period: none — analytic results plus Monte Carlo (10,000 replications, T from 100 to 5000)
markets: none (no empirical application)
tier: A
validation_overlap: false
published_post_2018: false
---

> **Source read in full** as the working-paper version: **PIER Working Paper 01-006, "Long Memory
> and Structural Change"** (May 1999, this draft November 1999), Diebold and Inoue, at
> `economics.sas.upenn.edu/sites/default/files/filevault/working-papers/01-006.pdf` — 402 KB,
> `pdftotext -layout` into 96 KB of clean text, no `( )` dropout, no ASCII shift. The title
> changed between working paper and journal version ("Structural Change" → "Regime Switching");
> the abstract, the two propositions, the Monte Carlo design and the concluding comparison with
> Granger–Hyung read below are all present in the draft. The published version was not obtained,
> so **section and table numbering here are the working paper's** and anything added in revision
> is not reflected. A `penn` department PDF is the channel; `papers.ssrn.com` was not tried,
> being already recorded as dark.

## Mechanism

**The claim: long memory and structural change are not two phenomena but, under a small amount of
regime switching, two labels for the same one — and the confusion is asymptotic, not a
small-sample artifact.**

The working definition the paper adopts, because it is the most general and the one its proofs
use, is the **variance of partial sums**: a series is `I(d)` if `var(Σ_{t≤T} x_t) = O(T^{2d+1})`.
This is equivalent to the familiar hyperbolic-autocorrelation definition `ρ(τ) ~ cτ^{2d−1}` and
to the low-frequency spectral definition `f(ω) ~ gω^{−2d}` under standard conditions, and it is
what makes the results below one-line proofs.

**The known routes to long memory, for contrast.** (i) *Cross-sectional aggregation*
(Granger 1980): aggregate `N` independent `AR(1)`s whose coefficients are drawn from a Beta
distribution and the aggregate is `I(1 − q/2)`, where `q` is a Beta parameter. (ii) *Heavy-tailed
durations* (Mandelbrot–Taqqu; Parke's error-duration model): superimpose many on/off sources whose
on- and off-durations have power-law tails with infinite variance and the aggregate converges to
fractional Brownian motion. Both tie long memory to **aggregation** and, in (ii), to heavy tails.

**The paper's route is different and much more ordinary.** Take a mixture model in which the mean
occasionally jumps:

```
v_t = 0      with probability 1 − p
    = w_t    with probability p ,      w_t ~ iid N(0, σ²_w)
```

Then `var(Σ_{t≤T} v_t) = p T σ²_w`. **Proposition 1:** if `p = O(T^{2d−2})` with `0 < d < 1`, then
`v_t` is `I(d − 1)` — immediately, from the partial-sum definition. Let the level accumulate those
shocks, `μ_t = μ_{t−1} + v_t`, and `μ_t` is `I(d)`; add observation noise, `y_t = μ_t + ε_t`, and
the **mean-plus-noise state-space model has the same long-memory property**.

The key device, and the reason this is not a technicality: **`p` is allowed to shrink with sample
size, so that however long the sample, a realisation contains only a few breaks.** That is exactly
the empirical situation of a two-decade equity panel.

**Proposition 2** extends the result to Engle–Smith's STOPBREAK model
`μ_t = μ_{t−1} + (ε²_{t−1}/(α_T + ε²_{t−1})) ε_{t−1}` — bigger innovations have more permanent
effects — giving `y ~ I(1 − η)` when `α_T = O(T^η)`, `η > 0`. Engle and Smith themselves note
STOPBREAK is an approximation to the mean-plus-noise model and a better one than **an exponential
smoother, which is the best *linear* approximation**.

**The conclusion the authors insist on, and it is not the naive one.** They explicitly refuse the
reading "structural change produces *spurious* inferences of long memory": "even if the 'truth' is
structural change, long memory may be a convenient shorthand description, which may remain very
useful for tasks such as prediction… 'structural change' and 'long memory' are effectively
different labels for the same phenomenon, in which case attempts to label one as 'true' and the
other as 'spurious' are of dubious value."

## Construction recipe

There is no portfolio construction here. What is implementable is the **generating process** — the
thing to simulate as a null when any long-memory or regime claim is made:

```
ε_t ~ iid N(0,1);  w_t ~ iid N(0,1)
v_t = w_t  w.p. p,  else 0
μ_t = μ_{t−1} + v_t
y_t = μ_t + ε_t
```

with `p` small (the Monte Carlo sweeps `p ∈ {0.0001, …, 0.1}` and `T ∈ {100 … 5000}`,
10,000 replications per cell). Estimate `d` by the **GPH log-periodogram regression**:
`log I(ω_j) = β_0 + β_1 log(ω_j) + u_j` over `j = 1 … m`, `d̂ = −½ β̂_1`, with the rule of thumb
`m ≈ √T`, and theoretical standard error `π · (24m)^{−½}` depending only on `m`. The paper uses
all of the first `m` ordinates (following Hurvich–Beltrao's finding that dropping the lowest ones
raises MSE).

## Robustness evidence (qualitative only)

- **Finite samples behave as the asymptotics predict.** Rejection frequencies of `d = 0` rise in
  both `T` and `p`; rejection frequencies of `d = 1` (tested as `d = 0` on differences) fall in
  both. On a single realisation with a handful of breaks the fitted log-periodogram slope implies
  `d̂ ≈ 0.79` for the mean-plus-noise model and `d̂ ≈ 0.67` for STOPBREAK — large fractional
  integration estimates produced by a process with **no fractional integration in it at all**.
- **The density of `d̂` is bimodal at small `p`**, and the authors identify the mixture: one mode is
  the distribution of `d̂` when no break happened in the realisation, the other when at least one
  did. So a single `d̂` from a single series is a draw from a mixture whose components correspond
  to different *histories*, not different parameters.
- **Independent and contemporaneous corroboration.** Granger–Hyung (1999) derive the `p = O(1/T)`
  case for the mean-plus-noise process and find very slowly decaying autocorrelations; that is the
  special case `d = 0.5` of Proposition 1. Granger–Teräsvirta's `y_t = sign(y_{t−1}) + ε_t`
  example shows apparent long memory emerging as switches become rare, without theory. Mikosch and
  Stărică reach the same conclusion from the asset-return side. Earlier warnings in hydrology
  (Klemeš), econometrics (Hidalgo–Robinson; Lobato–Savin) and mathematical statistics
  (Bhattacharya–Gupta–Waymire; Künsch; Teverovsky–Taqqu) are catalogued and the authors note they
  "have had little impact".
- **What this does not say.** It is not a claim that long-memory estimates in asset returns *are*
  breaks. It is an identification result: the two classes generate indistinguishable second-order
  behaviour at realistic break frequencies, so the data cannot choose between them. The
  Monte Carlo covers GPH only; whether the same confusion afflicts R/S-type or wavelet-based
  estimators is not tested here (it is implied, since all are functionals of the same low-frequency
  behaviour, but that is inference and not the paper's result).

## Implementability here

**This is an interpretation rule and a null generator. It produces no book and costs no trial.**

- **The first consequence is a refusal.** Any candidate whose motivation is "this series has long
  memory / a Hurst exponent above a half / slowly decaying autocorrelation, therefore a
  long-horizon signal should work" is unidentified at the outset: the same evidence is produced by
  a handful of level shifts, and the two imply **opposite** trading prescriptions — genuine
  fractional integration implies a smoothly decaying predictable component at every horizon, while
  a few breaks imply a series that is unpredictable except across the break dates nobody knows ex
  ante. Writing the candidate anyway buys a trial on a hypothesis the data cannot adjudicate.
- **The second consequence is a free null the lab can actually run.** Before reading anything into
  a long-horizon dependence measurement, simulate the mean-plus-noise process at the lab's own `T`
  and at a `p` implying a plausible number of regime changes over the window, and report the
  distribution of the statistic under it. This is the same discipline as `benchmarks.random_null_v3`
  — compare against a null that shares the nuisance structure, not against zero.
- **The direct tie to the lab's own 60-month result, and it is a tension to record rather than
  resolve.** The 2026-10-26/27 measurement found the cross-sectional rank correlation of
  market-demeaned returns over `[−2h, −h]` against `[−h, 0]` to be 4–9× larger at `h = 60` months
  than at any other horizon, and flagged that at `h = 60` adjacent monthly decision dates share 59
  of 60 months so the `t` is an upper bound. Diebold–Inoue add a second, independent reason for
  caution that the overlap rider does not cover: **over a two-decade train window, a handful of
  level shifts in relative valuation across a cross-section would produce exactly a long-horizon
  reversal at the scale of the window and nothing at shorter scales.** That is not a refutation —
  the lab's object is cross-sectional and theirs is univariate — but it is the alternative that a
  5-year-reversal candidate is implicitly betting against, and the paper's own position is that
  the bet may be unresolvable. The cheap discriminator is **stability across disjoint sub-periods
  of train**, which the lab already computes for every trial (1997–2008 vs 2009–2017): a
  fractional-integration story predicts the effect in both halves, a few-breaks story does not
  predict it anywhere in particular.
- **A sharper, free version of the same discriminator.** The lab's changepoint material
  (`notes/2026-10-22-multiple-changepoint-estimation-bai-perron-pelt.md`) supplies the estimator:
  date the breaks in the pool-relative series directly and ask whether the measured long-horizon
  reversal survives conditioning on them. If it is the breaks, it does not.
- **The STOPBREAK observation is reusable on its own.** "An exponential smoother is the best
  *linear* approximation to the mean-plus-noise model" is the same equivalence the folder reached
  from the filtering side (`#312`, `notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md`),
  arrived at independently. The addition here is the **nonlinear** improvement: weight an
  innovation's permanence by `ε²/(α + ε²)`, i.e. let large moves update the level more than small
  ones, with **one** scalar `α` for the whole panel. That is an `O(1)`, causal, zero-per-name-
  parameter alternative to an EWMA wherever the lab currently smooths a level, and it is the right
  side of item 1's triage rule.
- **Protocol hazard.** `p`, `α` and GPH's `m` are hyperparameters in `#311`'s sense. `m = √T` is a
  rule, not a fit, and is safe; `α` chosen by likelihood over the sample is not.

## Related

- `notes/2026-10-27-modified-rescaled-range-and-the-long-memory-null.md` — Lo removes short-range
  contamination from the test; Diebold–Inoue show that what survives still does not identify a
  mechanism. Read the two together: they close the vein from opposite ends.
- `notes/2026-10-27-hurst-estimator-finite-sample-confidence-intervals.md` — the third defect,
  estimation noise, independent of both.
- `notes/2026-10-22-multiple-changepoint-estimation-bai-perron-pelt.md` and
  `notes/2026-10-22-regime-switching-financial-markets.md` — the structural-change side of the
  same coin; this note is the reason those two and a long-memory claim are not separate agendas.
  The [2026-10-22] standing criterion (*admit a regime or timing vein only if it yields something
  that is NOT a timing overlay*) applies here and is satisfied only by the free screens above.
- `notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md`,
  `notes/2026-10-26-optimal-exponential-weights-signal-to-noise.md` — the mean-plus-noise model is
  literally the same state-space object those notes analyse; this one perturbs it by making the
  innovation intermittent.
- `experiments/learnings.md` 2026-10-26/27 — the 60-month cross-sectional reversal measurement
  this note qualifies.
