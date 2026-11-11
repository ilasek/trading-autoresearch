---
title: "Matching on the Estimated Propensity Score"
authors: Abadie, Imbens
year: 2016
venue: Econometrica 84(2), 781–807 (venue tier 1)
url: https://doi.org/10.3982/ECTA11293
citations: 708 (Crossref, checked 2026-11-11)
sample_period: none — asymptotic theory plus a Monte Carlo exercise
markets: n/a (econometric methodology; no financial data)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the third leg of the [2026-11-10] acceptance criterion: **what changes when the balancing
score is estimated rather than known.** `notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md`
proves a scalar `e(x) = pr(z = 1 | x)` can replace a `k`-dimensional match; that paper's own
simulation says estimating `ê(x)` costs little *bias*. This paper asks the other question — what
estimating it does to the **sampling distribution** — and the answer is counter-intuitive enough
that the authors note "these results were previously unavailable in the literature" despite the
method's thirty-year popularity.

Setup. Potential outcomes `Y(1), Y(0)`, binary treatment `W`, covariates `X`, target
`τ = E[Y(1) − Y(0)]`. Strong ignorability (`Y(1), Y(0) ⊥ W | X` and `0 < p(X) < 1`) is assumed —
this paper takes Rosenbaum–Rubin's identification result as given and works on inference. The
propensity score is given a generalized linear form `p(X) = F(x'θ)` with `F` logit or probit, and
`θ̂_N` is its maximum-likelihood estimate. The estimator matches each unit, **with replacement**,
to the `M` nearest units in the opposite treatment arm *by distance in the fitted score*, and
averages the signed outcome differences.

Three results carry, and the second is the one worth the night.

**(1) First-step estimation changes the large-sample distribution, and the obvious treatment of it
is wrong.** Matching estimators are "highly non-smooth functionals of the distribution of the
matching variables", so the standard two-step-estimator expansions (Newey–McFadden) do not apply;
this is why the result took so long. Treating `θ̂_N` as if it were the true `θ` is not a harmless
approximation.

**(2) THE SIGN IS BACKWARDS FROM THE NAIVE EXPECTATION. Matching on the ESTIMATED score has a
SMALLER asymptotic variance than matching on the TRUE score.** Their Theorem 1:

```
√N (τ̂_N − τ)  →  N(0, σ² − c' I_θ⁻¹ c)
```

where `σ²` is the asymptotic variance of the estimator that matches on the **true** score (the
Abadie–Imbens 2006 result), `I_θ` is the Fisher information matrix of the propensity-score model,
and `c` is a vector depending on the covariance between the covariates and the outcome,
conditional on the propensity score and on treatment. The adjustment term `−c'I_θ⁻¹c` is a
**quadratic form in an inverse information matrix and is therefore non-positive**: estimating the
nuisance parameter *reduces* the variance. The intuition the formula encodes is that `θ̂_N` adapts
to the realised sample, so matching on the fitted score balances the realised covariates better
than matching on the true probability would have.

**Scope restriction, stated by the authors in the same breath and easy to miss**: "This need not
be the case for matching estimators of other treatment parameters, **such as the average treatment
effect on the treated**." The sign is a property of this estimand, not of propensity-score
matching in general. Any design that targets the effect *on the treated cohort* — which is the
natural target whenever the "treatment" is an event that happens to a few names — is outside the
guarantee and must be treated as sign-unknown.

**(3) The practical consequence is that the naive standard error is too BIG, so the naive interval
is CONSERVATIVE rather than anti-conservative.** The estimator `σ̂²_N(θ̂_N)` that plugs the fitted
score in and ignores its estimation is biased **upward**; confidence intervals built on it have
**larger than nominal coverage**. This is the opposite of the usual two-step problem, where
ignoring first-step estimation understates uncertainty. It is also a rare case where the lazy
procedure is safe in the direction that matters for a research lab: it loses power rather than
manufacturing significance — **for this estimand only**, per (2).

**Bootstrap remains unavailable.** The paper's own motivating remark: bootstrap standard errors
have been used for propensity-score matching estimators precisely because the analytic
distribution was unknown, "however, recently it has been shown that the bootstrap is not in
general valid for matching estimators (Abadie and Imbens, 2008)". This re-confirms `#429`'s
refusal from a second direction.

## Construction recipe

**The estimator.** For each unit `i`, let `J_M(i, θ)` be the set of `M` units in the opposite
treatment arm with the closest fitted scores `|F(X_i'θ) − F(X_j'θ)|`. Then

```
τ̂_N(θ) = (1/N) Σ_i (2W_i − 1) [ Y_i − (1/M) Σ_{j ∈ J_M(i,θ)} Y_j ]
```

Matching is **with replacement**, so a control may be used many times; the equivalent weighted
form is `τ̂_N(θ) = (1/N) Σ_i (2W_i − 1)(1 + K_{N,i}(θ)/M) Y_i`, where `K_{N,i}` counts how often
unit `i` was used as a match. That weighted form is the one to implement — it is a single pass
over the panel once the match counts are known.

**The variance, in three estimated pieces.** Fix `J` (the number of same-arm neighbours used for
the local variance) and let `H_J(i, θ)` be the `J` units with the **same** treatment status and
closest fitted scores to `i`.

- Local outcome variance: `σ̂²_{N,i} = (1/J) Σ_{j ∈ {i} ∪ H_J(i,θ)} (Y_j − Ȳ_i)²`, with `Ȳ_i` the
  mean outcome over `{i} ∪ H_J(i, θ)`. Feed it into the Abadie–Imbens (2006) estimator
  `σ̂²_N(θ) = (1/N) Σ_i [ (K_{N,i}/M)² + ((2M−1)/M)(K_{N,i}/M) ] σ̂²_{N,i}`.
- The correction vector: using the same same-arm neighbourhoods, estimate
  `cov(X_i, Y_i | F(X_i'θ), W_i)` as the local cross-moment
  `(1/J) Σ_{j ∈ {i} ∪ H_J(i,θ)} (X_j − X̄_i)(Y_j − Ȳ_i)`, then
  `ĉ = (1/N) Σ_i côv(X_i, Y_i | ·) f(X_i'θ̂)[ W_i / F(X_i'θ̂)² + (1 − W_i) / (1 − F(X_i'θ̂))² ]`,
  where `f` is the derivative of the link `F`.
- The information matrix:
  `Î_θ = (1/N) Σ_i f(X_i'θ̂)² / [F(X_i'θ̂)(1 − F(X_i'θ̂))] · X_i X_i'` — the usual MLE sandwich
  ingredient, no extra machinery.

**The adjusted variance is then** `σ̂²_adj = σ̂²_N(θ̂_N) − ĉ' Î_θ⁻¹ ĉ`, and it is consistent. Every
ingredient is a local average over nearest neighbours in the fitted score plus one logit
information matrix: no new tuning parameter beyond `J`, and no resampling.

**Assumptions to check before quoting the interval** (their Assumptions 1–4): strong ignorability;
the generalized-linear score model is **correctly specified** (`θ̂` is the MLE for the true `θ`);
`F` has a continuous derivative, satisfied by logit and probit; and the score is bounded away from
0 and 1 on the support of `X`. The correct-specification requirement is not cosmetic — the whole
`−c'I_θ⁻¹c` term is computed *inside* the parametric model.

## Robustness evidence (qualitative only)

- **Theory first, simulation as illustration.** The paper is a proof; the Monte Carlo (two uniform
  covariates, a logistic score, a linear outcome, single nearest-neighbour matching, large `N`)
  exists to show the approximation is accurate at a realistic sample size. Its qualitative
  findings, which are what transfer: the estimator matching on the estimated score has **lower
  variance** than the one matching on the true score, exactly as the theorem says; the unadjusted
  variance estimator is **biased upward on average** and its intervals **over-cover**; and the
  adjusted estimator is approximately unbiased with coverage close to nominal. No design constants
  are carried here.
- **Venue and provenance.** *Econometrica*, 708 Crossref citations. The companion results it leans
  on (Abadie–Imbens 2006 large-sample theory, 2008 bootstrap failure) are the same pair already in
  the folder at `notes/2026-11-10-matching-estimator-bias-and-the-dimension-of-the-match.md`, so
  this is a coherent body rather than an isolated claim.
- **Honest limits the authors state themselves**: the proof of Theorem 1 requires a
  **discretization of the first-step estimator**, with the result arising in the limit as the
  discretization is refined; the results are derived for generalized-linear score models (they say
  the extension to more general parametric models is easy, but it is not done); and the sign of the
  adjustment is **established for the average treatment effect only**.
- **What was read.** The NBER working-paper version (w15301, August 2009, revised December 2009),
  obtained at `nber.org/system/files/working_papers/w15301/w15301.pdf` — 22 pages, extracted
  cleanly, no ASCII shift and no `( )` dropout. OpenAlex lists that same PDF as a location for the
  published work and its stored abstract is **verbatim identical** to the working paper's, so the
  theorem statements above are the published ones. The typeset *Econometrica* article was not
  fetched; page numbers in the frontmatter come from Crossref.

## Implementability here

**This is the inference layer for anything built on the previous note's scalar score, and it is
mostly good news with one trap.**

- **If a cohort diagnostic on this panel matches on a fitted score and reports the naive interval,
  that interval is too wide, not too narrow — provided the estimand is the average effect over the
  whole panel.** For the lab, that means a wide-and-null cohort result is **weak evidence of
  nothing**, because some of the width is the unadjusted variance. Before concluding "no
  difference", compute `σ̂²_adj`; the ingredients are three local averages that cost one pass each.
- **The trap, and it is the likely case here.** The natural question on this panel is almost always
  about the **treated** cohort — what happens to names that *become* eligible, not what would
  happen to an average name if it became eligible. That is the average effect on the treated, and
  the authors explicitly withhold the sign of the adjustment for it. **Refusal test: a cohort
  design on this panel must state whether its estimand is over the whole panel or over the treated
  cohort; if the latter, the naive interval cannot be called conservative** and the adjustment's
  direction is unknown without doing the derivation this paper does not do.
- **It kills the obvious escape hatch from `#429` for a second time.** `#429` said the bootstrap is
  not valid for a matching estimator at any `k`; this paper's own motivation re-states it. Between
  them, the only route to a valid interval on a matching estimator here is an analytic variance,
  which means the `σ̂²_adj` recipe above or nothing. The lab's standing bootstrap interval, which
  `engine/protocol.py` computes for *skill*, is a different object on a different estimator and is
  untouched by this — but it must not be borrowed for a matched-cohort number.
- **Cost of computing it on this panel.** ~1,000 eligible names per date; the expensive step is
  nearest-neighbour search in a **one-dimensional** fitted score, which is a sort plus a merge, not
  a `k`-d tree. `Î_θ` is a `p × p` outer-product sum for a handful of features. All of it is
  comfortably inside the ~60 s/call budget, and none of it needs an estimated covariance matrix —
  so the `#1` parameter-counting screen does not fire on the *variance* calculation, only on the
  score model's feature count.
- **Specification risk is the binding constraint, not arithmetic.** The adjustment is computed
  inside the assumed logit. On this panel the "treatment" is an index committee's decision
  (`#418`), so a correctly specified assignment model is not available in principle. The honest
  framing: report `σ̂²_adj` as the interval **under an assumed selection model**, name the model,
  and do not present the resulting number as a causal effect. This is the same discipline the
  previous note imposes for the same reason.
- **One free diagnostic that falls out of the construction.** `ĉ` is built from
  `cov(X, Y | score, W)` — the covariance between the covariates and the outcome *after*
  conditioning on the score. If that is near zero, the whole adjustment is near zero and the naive
  variance is already right. Computing `ĉ` therefore tells you whether any of this matters before
  you build the rest, and a near-zero `ĉ` is itself the informative statement that **the covariates
  carry no outcome information beyond the score** on this panel.

## Related

- `notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md` — the primary this one
  completes. Rosenbaum–Rubin's simulation says estimating the score costs little **bias**; this
  paper says what it does to the **variance**, and the two together are the full answer to
  [2026-11-10]'s criterion (iii).
- `notes/2026-11-10-matching-estimator-bias-and-the-dimension-of-the-match.md` — `#429`/`#430`,
  the same authors' 2006/2011 pair. The `N^{−1/k}` bias result and the bootstrap refusal both live
  there; this note is the `k = 1`-after-score-reduction case of it.
- `notes/2026-11-11-the-psm-paradox-and-random-pruning.md` — the critique that says the
  score-matched design should not be built at all. Note the asymmetry: this paper improves
  *inference* conditional on the design; that one attacks the design.
- `notes/2026-11-05-minimum-track-record-length-and-the-probabilistic-sharpe-ratio.md` and the
  inference cluster — where the lab's own intervals come from, and why a conservative interval is
  not a free lunch when the decision is "keep searching or stop".
- `research/SUMMARY.md` candidate ideas #429–#433.
