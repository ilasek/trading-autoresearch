---
title: "Noise sensitivity of portfolio selection under various risk measures" — the closed-form estimation-error multiplier 1/√(1−N/T), the critical N/T at which each risk measure's optimisation diverges, and why the coherent tail measures are the fragile ones
authors: Kondor, Pafka, Nagy
year: 2007
venue: Journal of Banking & Finance 31(5), 1545–1573 (venue tier 1, peer-reviewed)
url: https://doi.org/10.1016/j.jbankfin.2006.12.003
citations: 105 (Crossref `is-referenced-by-count`, checked 2026-10-23). Modest in absolute terms next to the other sources in tonight's cluster, and that is a fair signal to record rather than explain away — but the paper's central formula predates it and is attributed in the text to Pafka–Kondor (2003), Burda et al. (2003) and Papp et al. (2005), so the result's citation mass sits across that cluster rather than in this one paper. Tier is set on venue, on the fact that the headline result is an exact random-matrix computation confirmed by simulation, and on the authors' unusual candour about their own simplifying assumptions.
sample_period: no empirical sample. Every number in the paper comes from Monte Carlo simulation of synthetic Gaussian return series with a known "true" covariance matrix; the point of the design is that the truth is known, which no historical sample permits. Nothing in it can touch 2018–2023.
markets: none — synthetic portfolios of N assets, parameterised by N and the series length T
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the arXiv version, `arxiv.org/pdf/physics/0611027` (379 KB, 33 pages, `physics.soc-ph`, v1 dated 2 November 2006, internal version line "This version: 29 September 2005"; `pdftotext -layout` to 81 KB of clean text, 638 `" the "`, no ASCII shift). Figure contents were not read as images; all numerical results quoted below are from the body text and the conclusions, both of which state them explicitly. First-try fetch, no refusal.
---

## Mechanism

The three preceding notes build a case: a coherent tail measure is axiomatically better behaved than
variance, and minimising it is a linear program. This note is the counterweight, and it is the reason
the vein should probably not be entered on the weighting side at all. Its subject is not whether a risk
measure is coherent but **how much of the optimised portfolio is noise**, and the finding is that the
ordering is close to reversed: the better a measure's axioms, the worse its estimation behaviour.

The design is the one that makes the question answerable. Rather than optimise on historical data —
where the true optimum is unknown and so the error is unmeasurable — the authors *simulate* returns
from a known covariance matrix, optimise on a finite sample of length `T`, and compare the **true** risk
of the sample-optimal portfolio to the **true** risk of the truly-optimal portfolio. Their sensitivity
measure is the relative sub-optimality

```
q₀² = (w* ᵀ σ⁽⁰⁾ w*) / (w⁽⁰⁾* ᵀ σ⁽⁰⁾ w⁽⁰⁾*)
```

with `σ⁽⁰⁾` the true covariance, `w*` the weights chosen on the sample and `w⁽⁰⁾*` the weights that
would be chosen with full information. `q₀ − 1` is the fraction by which realised risk exceeds the
attainable minimum purely because the inputs were estimated. `q₀` is itself a random variable over
samples, and both its mean and its distribution are studied.

**Result 1 — the closed form, for variance.** For `N/T < 1`, random-matrix theory gives exactly

```
q̄₀ = 1 / √(1 − N/T)
```

The authors stress two things about it. First, it depends on `N` and `T` **only through the ratio
`N/T`** — error scales in `N/T`, so doubling both the panel width and the history length leaves the
problem exactly as hard. Second, it **diverges as `N/T → 1`**, which is the point at which the sample
covariance matrix becomes singular; and the asymptotic formula is already accurate at moderate `N` and
`T`. This is not a bound or an approximation: it is the mean relative risk inflation.

**Result 2 — the phase transition, and the ranking it induces.** The divergence is not special to
variance. The authors optimise under four measures — variance, mean absolute deviation (MAD), expected
shortfall (ES, i.e. CVaR) and maximal loss (ML) — and find that each has a **critical value of `N/T`**
at which `q̄₀` diverges, with critical exponent `−1/2`, and that the critical value depends on the
measure:

| Risk measure | Critical `N/T` |
|---|---|
| variance | 1 |
| mean absolute deviation | 1 |
| maximal loss | 1/2 |
| expected shortfall (CVaR) | **below 1/2**, depending on the tail level `β` |

So **a tail measure needs strictly more data than variance** to reach the same estimation accuracy on
the same panel, under the same (Gaussian) returns.

**Result 3 — the one the authors themselves call unexpected, and it inverts the obvious intuition.**
For ES the critical `N/T` *decreases* as `β` decreases. Lowering `β` means averaging over *more* tail
observations, which ought to help; instead the feasibility boundary bends downward, so "for a fixed
`N` we need longer and longer time series to have the same chance of finding a solution." They
describe this as ES becoming "in a sense, more sensitive to noise as `β` decreases" and note the result
"is quite unexpected." The boundary must terminate at the origin, because as `β → 0` the objective
becomes linear in the weights and is then always unbounded.

**Result 4 — the feasibility problem, which is a different failure from inaccuracy.** Variance and MAD
optimisation is **always feasible** below the critical ratio. ES and ML instead exhibit a
*probabilistic* feasibility problem: the objective can be **unbounded from below**, in which case **no
solution to the optimisation exists at all**. In the `N, T → ∞` limit the probability of a solution
existing drops discontinuously from one to zero across the boundary; at finite `N, T` the transition is
smooth, and they map the iso-probability contours. The mechanism is that a tail objective computed on
finitely many scenarios can be driven to `−∞` by a weight direction that no observed scenario
penalises.

**Result 5 — weight instability, and a warning about how it is usually hidden.** Beyond the aggregate
`q₀`, the authors measure the sample-to-sample fluctuation of the individual weights, and find it large
already for variance and **stronger still for the other three measures**. They attach a methodological
warning that is worth more here than the result: the instability "is conspicuous if we use
non-overlapping samples; whereas **overlapping samples generate autocorrelations and apparent structure
in data that are uncorrelated by construction.**" A rolling-window study of weight stability on data
with no structure at all will show structure.

Their own closing gloss: "for normally distributed returns and under the sensitivity measure `q₀`,
variance is the best risk measure from the point of view of noise tolerance", and filtering methods
(shrinkage, eigenvalue cleaning) exist for variance and "hardly any" exist for the alternatives.

## Construction recipe

There is no strategy here. What is constructible is a **feasibility arithmetic to run before writing
any risk-optimising candidate**, and it is three lines:

1. Count the cross-section `N` the optimisation will actually see at a rebalance date, and the number
   of scenario rows `T` the trailing window supplies.
2. Form `N/T`. Compare against the measure's critical value: 1 for variance or MAD, 1/2 for maximal
   loss, below 1/2 for CVaR at a usable `β`.
3. If using variance, read the expected risk inflation straight off `q̄₀ = 1/√(1 − N/T)` and decide
   whether that much inflation is acceptable before spending a trial. If the ratio is near or above the
   critical value, the optimisation is not a measurement of the idea — it is a measurement of the
   sample.

The authors' two routes out, in their own framing: **reduce `N`** (the problem scales in the ratio, so
grouping the cross-section is as good as lengthening the history), or **filter the inputs** — and they
note filtering is well developed for covariance and essentially absent for the tail measures, which
makes "reduce `N`" the only route available for a CVaR objective.

## Robustness evidence (qualitative only)

The central formula is an exact result from random-matrix theory, independently published in three
prior papers the authors cite, and confirmed here by simulation at moderate `N` and `T`. The phase
transitions for ML and ES are numerical rather than analytic — the authors are explicit that the
precise shape of the ES boundary is hard to pin down for small `N/T` because "the simulations slow down
tremendously", and that they could not follow it below `β ≈ 0.3`. The qualitative claim (a critical
ratio exists, it is below 1/2 for ES, it bends down with `β`) is well supported; a precise critical
value for a given `β` is not available from this paper.

**The authors' own three stated limitations, all of which matter here and one of which is decisive:**

- **Gaussian returns.** They used Gaussian data to make the truth knowable, and argue the phase
  transition "is ultimately due to information deficit" and so should not depend on the distribution,
  while conceding that fat tails may change the universality class. Their judgement on direction is
  explicit: "the effect of estimation error on real life portfolio selection can only be **worse** than
  in our artificial world." Treat the numbers as a floor on the error, not an estimate of it.
- **Only the budget constraint.** They impose `Σwᵢ = 1` and nothing else — **no non-negativity, no
  position cap** — and they flag the omission, noting it "will be interesting to see how the
  re-introduction of the constraint on the expected return will modify the conclusions."
- **No return constraint** in the main experiments.

The second limitation is the one that must be worked through rather than quoted, because it changes
which of the five results transfers. **The feasibility transition (Result 4) does not survive a
long-only constraint, and this is provable in a line.** Take the CVaR program from the companion note:
minimise `α + (q(1−β))⁻¹ Σ u_k` subject to `u_k ≥ 0`, `u_k ≥ −xᵀy_k − α`, with `x` on the simplex
(`x ≥ 0`, `Σx = 1`). As `α → +∞` the `u_k` go to zero and the objective is `α → +∞`. As `α → −∞` every
`u_k ≈ −xᵀy_k − α`, so the objective behaves like `α(1 − (1−β)⁻¹) + const`, and since `(1−β)⁻¹ > 1` the
coefficient on `α` is negative and the objective again `→ +∞`. The weights live in a compact set, so
the program is **bounded below and feasible for every sample**. Unboundedness in the paper comes from
weights being free to run to infinity in a direction no scenario penalises; the simplex forecloses it.

**So the honest split is:** Results 1–3 and 5 (error scaling in `N/T`, divergence at a critical ratio,
the tail measures needing more data, weight instability) transfer to this lab qualitatively and are the
part to act on. Result 4 (no solution exists) does **not** transfer — long-only is doing real work
here, and a candidate that cited this paper as a reason a CVaR program "may have no solution" on this
panel would be wrong. What long-only does *not* fix is accuracy: a bounded program can still return a
weight vector that is mostly noise, and the simplex's own boundary makes it worse in a specific way, in
that the optimiser expresses its noise by piling onto a handful of names at the `x ≥ 0` boundary.

## Implementability here

**The arithmetic for this repo, done.** Under protocol v2/v3 roughly 1,000 names are eligible on a
typical validation date. Validation is 2018–2023, about 1,510 trading days; a trailing estimation window
is shorter still — two years is `T ≈ 500`, three years `T ≈ 755`.

| Construction | `N` | `T` | `N/T` | Verdict |
|---|---|---|---|---|
| Full-panel covariance, 2y window | ~1,000 | ~500 | **2.0** | singular; meaningless |
| Full-panel covariance, full validation span | ~1,000 | ~1,510 | **0.66** | feasible, `q̄₀ ≈ 1.71` — **71% risk inflation** |
| Full-panel CVaR, any window | ~1,000 | ≤1,510 | ≥0.66 | **above ES's critical ratio (<0.5)** — divergent regime |
| 50 sector/region buckets, 2y window | 50 | ~500 | 0.10 | `q̄₀ ≈ 1.05` — 5% inflation, comfortable |
| 20 buckets, 2y window | 20 | ~500 | 0.04 | `q̄₀ ≈ 1.02` |

Two conclusions, and they are quantitative rather than stylistic:

1. **A full-panel risk optimisation of any kind is not implementable on this universe, and a full-panel
   CVaR optimisation is not implementable at all.** Even using the *entire* validation span as the
   estimation window — which a causal candidate cannot do anyway, since it may only use data at or
   before each rebalance date — variance optimisation carries a 71% expected inflation of realised
   risk, and CVaR sits past its own critical ratio. The causality requirement makes `T` smaller than
   the table's best case, so the real numbers are worse. **This closes the "minimise CVaR over the
   eligible panel" candidate before it is written, on arithmetic, with no trial spent.** It is the same
   verdict the folder's precision-matrix section reached for the covariance route, arriving
   independently and with a closed form attached.
2. **The route that survives is to collapse `N`.** Because the error scales in the *ratio*, reducing
   the optimisation's dimension is exactly as good as lengthening history, and history cannot be
   lengthened. Optimising over a few dozen groups (and distributing within a group by a rule that is
   not optimised) moves `N/T` from 2.0 to 0.1 and the inflation from "undefined" to ~5%. This is the
   dimensional argument *for* clustering-based allocation, arriving from estimation error rather than
   from the hierarchical-risk-parity literature's own motivation, and it is the strongest
   quantitative support in tonight's cluster for anything in the `portfolio-learning` family.

**The methodological warning is the most broadly useful thing in the paper and it is free.** The
observation that **overlapping samples manufacture apparent structure in data that is uncorrelated by
construction** applies directly to any weight-stability or signal-stability diagnostic the lab runs on
rolling windows — which is most of them. A rolling-window picture of a statistic's stability is partly
a picture of the window overlap. The correction is the authors': check stability on
**non-overlapping** samples, and treat a rolling-window stability plot as an upper bound on
genuine persistence. This composes with the folder's existing block-resampling items rather than
duplicating them: block resampling fixes the *error bar*; this fixes the *picture*.

**Three further points for a candidate.**

- **`q̄₀ = 1/√(1 − N/T)` is a pre-registerable kill condition, not just a diagnostic.** A candidate
  proposing any estimated-risk construction can state its `N`, its `T` and the implied inflation in its
  hypothesis line, before running. If the implied inflation exceeds the skill the candidate hopes to
  show, the trial is not worth spending.
- **It is a floor, not an estimate.** The authors' own judgement is that real data can only be worse
  than their Gaussian world. Any margin a candidate claims against this threshold should be generous.
- **Do not cite the feasibility transition here.** As worked through above, long-only removes it. The
  transferable claims are about *accuracy* and *weight instability*.

**Universe fit.** The paper needs no data from this repo and proposes no signal; its content is a
constraint on construction, available free to every candidate, and the one piece of arithmetic in
tonight's four notes that changes what should be built rather than how it should be judged.

## Related

- **`2026-10-23-cvar-optimization-as-a-linear-program.md`** is the paper this one answers. Read
  together: Rockafellar–Uryasev show minimising CVaR is a tractable convex program; this shows the
  program's *input requirements* are stricter than variance's, and that at this panel's width neither
  is satisfiable on the full cross-section. The `q(1−β)` tail-sample arithmetic in that note and the
  `N/T` arithmetic here are two faces of the same information deficit — one counts observations in the
  tail, the other counts observations per parameter.
- **`2026-10-23-coherent-measures-of-risk-axioms.md`** — the inversion is the point of the pairing.
  Artzner et al. rank the measures by axiom: CVaR coherent, VaR and mean-variance not. This paper ranks
  them by noise tolerance and the order roughly reverses. The authors' own conclusion is that
  "the requirement of robustness (noise-tolerance) should be given special attention when considering
  the theoretical and practical criteria to be imposed on a risk measure" — i.e. coherence is a
  criterion on the functional, and estimability is a criterion on the estimator, and a measure can pass
  one while failing the other.
- **`2026-10-23-generalized-deviation-measures.md`** — this note is why that one steers toward the
  *per-name* tail beta (a univariate conditional mean, no joint estimation, immune to the `N/T`
  problem) rather than toward the joint deviation-measure optimisation.
- Folder sections: "Estimating the book instead of forecasting it — the precision matrix, what is
  computable at this panel's width, and the one anchoring operator that is" reaches the same verdict
  for the covariance route and should be read with this; `q̄₀ = 1/√(1−N/T)` is the closed form that
  section's argument wants. Also "Where a long-only book's risk actually lives — weight-space distance,
  revealed alpha, and concentration"; "What a selected maximum is worth — post-selection estimation";
  and the `portfolio-learning` family's hierarchical-risk-parity material, for which Result 1 above is
  independent dimensional support.
- **`experiments/learnings.md`:** no contradiction, and one alignment worth naming. The learnings file
  records, from the lab's own measurements, that de-concentration and risk-overlay constructions have
  repeatedly cost more than they returned. Those constants were measured on `price-trend` under v1/v2
  and `CLAUDE.md` forbids carrying them into v3 or another family — they are not carried here. But this
  paper supplies an *independent, external, mechanism-level* reason to expect estimated-risk machinery
  to disappoint on a wide panel with short history, which is a different kind of evidence for a
  compatible conclusion. That is worth recording precisely because it is not a re-import: the lab
  measured an outcome, this paper explains a cause.
