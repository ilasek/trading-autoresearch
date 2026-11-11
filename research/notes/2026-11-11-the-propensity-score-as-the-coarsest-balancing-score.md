---
title: "The Central Role of the Propensity Score in Observational Studies for Causal Effects"
authors: Rosenbaum, Rubin
year: 1983
venue: Biometrika 70(1), 41–55 (venue tier 1 — top peer-reviewed statistics journal)
url: https://doi.org/10.1093/biomet/70.1.41
citations: 26586 (Crossref, checked 2026-11-11)
sample_period: none — statistical theory, plus one simulation study and one clinical observational dataset
markets: n/a (statistical methodology; no financial data)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the named primary the [2026-11-10] handover asked for, and it answers the question
`#429` created. That note established that a matching estimator built on `k ≥ 2` **continuous**
covariates has a bias of order `N^{−1/k}`, which does not shrink fast enough relative to the
`N^{−1/2}` sampling error, so its confidence intervals are not valid; only `k = 1` is clean. The
standard device for collapsing `k` covariates to one is a **scalar summary**, and this paper is
where that device comes from and where its justification is proved.

The object is defined in two steps.

**A balancing score** `b(x)` is *any* function of the observed covariates `x` such that the
conditional distribution of `x` given `b(x)` is the same in the treated and control groups:

```
x ⊥ z | b(x)
```

where `z ∈ {0,1}` is the treatment indicator. The trivial balancing score is `b(x) = x` itself —
matching exactly on every covariate obviously balances every covariate. The interesting ones are
many-to-one functions.

**The propensity score** is the conditional probability of treatment given the covariates:

```
e(x) = pr(z = 1 | x)
```

Five theorems then do the work (the paper's own summary, §2.1):

1. **Theorem 1 — the propensity score is a balancing score**: `x ⊥ z | e(x)`. Cochran and Rubin
   had proved this for multivariate normal `x`; here it holds **regardless of the distribution of
   `x`**.
2. **Theorem 2 — `e(x)` is the COARSEST balancing score, and `x` is the finest.** Formally,
   `b(x)` is a balancing score **if and only if** `b(x)` is finer than `e(x)`, in the sense that
   `e(x) = f{b(x)}` for some function `f`. This is the theorem that licenses the dimension
   reduction: nothing coarser than a scalar probability can balance the covariates, and nothing
   needs to be finer.
3. **Theorem 3 — ignorability transfers.** If treatment assignment is *strongly ignorable* given
   `x` — that is, `(r₁, r₀) ⊥ z | x` and `0 < pr(z = 1|x) < 1` for all `x`, where `r₁, r₀` are the
   two potential responses — then it is strongly ignorable given **any** balancing score.
4. **Theorem 4 — the estimate at a score value is unbiased.** Under strong ignorability, at any
   value of a balancing score the expected difference in observed responses between treated and
   control equals the average treatment effect at that value:
   `E{r₁|b(x), z=1} − E{r₀|b(x), z=0} = E{r₁ − r₀ | b(x)}`. Units with the same balancing score
   but different treatments "can act as controls for each other".
5. **Theorem 5 / Corollary 5.1 — sample estimates of the score produce sample balance**, not
   merely population balance.

The economic content for this lab is the second theorem, and it is a licence with a condition
attached. The licence: a `k`-dimensional match can legitimately be replaced by a **one-dimensional
match on a probability**, which is exactly the `k = 1` case `#429` says is the only clean one. The
condition: the scalar that does this is specifically the probability of *selection into the
treated group*, not any other scalar summary. A one-dimensional index that is not (a monotone
function of) `pr(treated | x)` is not a balancing score and Theorem 2 says so.

Three structural points the paper is explicit about, all of which bite here:

- **Strong ignorability is an assumption about unobservables and is not testable.** Theorem 3
  transfers it; nothing establishes it. The paper notes that in a randomized trial `x` is *known*
  to contain all variables used to assign treatment, and that "this condition is usually not known
  to hold in a nonrandomized experiment."
- **`e(x)` is known in a randomized experiment and unknown everywhere else**, so in observational
  data it must be modelled — the paper suggests a logit model or a discriminant score.
- **Discriminant matching is a special case.** If `pr(x|z=t)` is multivariate normal with common
  covariance `Ω`, then `e(x)` is a monotone function of the linear discriminant
  `xᵀΩ⁻¹(μ₁ − μ₂)`, so matching on the discriminant *is* matching on the propensity score. Under
  a polynomial exponential family, `e(x)` obeys a polynomial logit model. The scalar score is
  therefore the general form of a family of ad-hoc one-dimensional indices.

## Construction recipe

Enough to implement without re-reading the paper. The paper gives three distinct uses of the same
scalar, all covered by Corollaries 4.1–4.3.

**Step 0 — model the score.** Fit `ê(x)` by a logit (or probit, or discriminant) regression of the
treatment indicator `z` on the covariates `x`. The paper's worked example selects covariates *and
interactions among them* by a stepwise procedure. The exact non-parametric estimator
`ê(a) = prop{z = 1 | x = a}` exists only when `x` takes few values; with any continuous covariate
it is 0 or 1 almost everywhere, so "some modelling will be required".

**Use A — pair matching on the score (Corollary 4.1).** Sample a value of `b(x)`, then one treated
and one control unit at that value; the mean of matched-pair differences is unbiased for the
average treatment effect. In practice exact matches on a scalar are "often impossible to obtain",
so use **nearest available matching** on `ê(x)` from a reservoir of controls. The relevant
construction property is **equal per cent bias reduction (EPBR)**: a method is EPBR if the bias in
*each* coordinate of `x` is reduced by the same percentage, i.e. `B_m = γB` for a scalar
`0 < γ < 1`. Theorem 6 gives the reduction in bias for any method that matches on `b` alone, and
**Corollary 6.1** gives the condition: if `E(x|b) = α + βf(b)` for vectors `α, β` and a
scalar-valued `f`, matching on `b` alone is EPBR. **Corollary 6.2** extends it within
subpopulations: if `d(x)` is constant inside each subpopulation, propensity matching within
subpopulations is EPBR in each. A method that is *not* EPBR has the explicitly undesirable
property that it **increases** the bias for some linear function of `x`.

**Use B — subclassification on the score (Corollary 4.2).** Divide all units into subclasses at
the **quintiles of the sample distribution of `ê(x)`** — five subclasses, following Cochran's
observation that five strata remove at least 90% of the bias for many continuous distributions —
then take the difference in treatment means within each subclass and combine them by direct
adjustment with subclass-total weights. This is unbiased for the average treatment effect under
strong ignorability **without modelling assumptions such as parallel linear response surfaces**.
The paper's stated motivation for doing it on the score rather than on `x`: subclassifying on `P`
covariates with even two categories each gives `2^P` cells, "most of which will not contain both
treated and control units". Subclassification on the propensity score is "a natural way to avoid
this problem".

**Use C — covariance adjustment on the score (Corollary 4.3).** If `E{r_t | z=t, b(x)} = α_t +
β_t b(x)` is linear, then `(α̂₁ − α̂₀) + (β̂₁ − β̂₀)b̄` is unbiased for the average treatment
effect, where `b̄` is the sample mean of the score. The paper's warning here is sharp and is the
one most likely to be ignored: **covariance adjustment on `x` cannot be relied upon unless the
linear discriminant is highly correlated with the propensity score.** When the two groups'
covariance matrices differ — so that the discriminant is *not* a monotone function of `e(x)` —
covariance adjustment can "either increase the bias or overcorrect for bias dramatically". The
authors note the subset receiving a new treatment is often *more homogeneous* than the general
population, so unequal covariances are not unusual.

**Diagnostics.** The paper's own balance check is the one to copy: for each covariate, compute the
`F` statistic for the treatment main effect **before** subclassification, then the `F` for the
treatment main effect and for the **treatment-by-subclass interaction** in a 2 × (number of
subclasses) analysis of variance **after**. Balance has been achieved when the post-subclassification
statistics collapse toward their null distribution while the pre-subclassification ones do not. It
also recommends plotting responses and residuals **against `ê(x)`** rather than against the
discriminant, because by Corollary 4.3 the expected response difference at each `e(x)` equals the
treatment effect there — a property that "does not generally hold for other functions of `x`".

## Robustness evidence (qualitative only)

- **The theory is distribution-free.** Theorems 1–4 assume nothing about the distribution of `x`.
  This is the paper's own stated improvement over the earlier normal-theory discriminant-matching
  results.
- **Estimating the score costs little in the matching application.** The paper reports a
  simulation (bivariate normal covariates with a common covariance matrix, nearest-available
  matching, control reservoirs of 2×, 3× and 4× the treated group) comparing matching on the
  **sample** score against matching on the **population** score across a range of initial
  imbalance. Its qualitative conclusion, in the authors' words: the two are "approximately equally
  effective in removing bias, so that **no substantial loss is incurred by having to estimate the
  propensity score**", and matching alone removes most of the initial bias when the reservoir is
  relatively large. Per cent-reduction figures are not carried here — they are simulation design
  constants, and the qualitative statement is what transfers.
- **The paper flags the gap between its own theorem and its own simulation**: nearest-available
  matching with imperfect matches "provides only a partial adjustment for the propensity score",
  so the conditions underlying the simulation differ from those underlying Theorem 1. The theorem
  is about exact matching on the score; practice never achieves it.
- **Propensity matching beats Mahalanobis matching specifically when `x` is markedly
  non-spherical**, and specifically when `x` contains a coordinate representing a **rare binary
  event** — the quadratic metric "may try too hard to match that coordinate exactly, thereby
  reducing the quality of the matches on the other coordinates".
- **Replication status**: this is one of the most-cited papers in statistics (26,586 Crossref
  references) and its theorems are proofs rather than empirical findings, so "replication" in the
  Hou–Xue–Zhang sense does not apply. What *is* contested is whether the method should be used for
  **matching** in practice — see `notes/2026-11-11-the-psm-paradox-and-random-pruning.md`, which
  accepts Theorem 1 as "mathematically correct" and argues it is the wrong target. Read the two
  together.

## Implementability here

**What this licenses.** `#429` says a matched-control design on this panel must have `k = 1`
continuous matching variable or its intervals are invalid. Theorem 2 says the one scalar that can
stand in for several covariates is `pr(eligible-event | x)` — the probability of the selection
event itself, estimated from the covariates. On protocol v2's panel the candidate "treatments" are
exactly the selections `#410`/`#411` identify: a name **becoming `eligible`** (index admission), a
name entering a liquidity band, a name entering a volatility band. For the admission event the
covariates available here are the ones the panel actually holds — trailing return over several
horizons, trailing realised or range volatility, trailing dollar volume and its trend, and
region/market as a **discrete** covariate. Discrete covariates are free under `#429`'s accounting,
so **region and market should be matched on exactly and left out of the score**, which is also
Corollary 6.2's construction (EPBR within subpopulations).

**The logit must be walk-forward.** `CLAUDE.md` requires it and `causality_check` enforces it: the
score model is fitted on information available at the rebalance date, never once over the visible
window. This is the same constraint `#429` put on `μ̂₀` and it binds harder here, because the
score is fitted on *every* name rather than on controls only.

**Prefer subclassification to matching on this panel, and the reason is arithmetic, not taste.**
Five quintile subclasses of `ê(x)` against ~1,000 eligible names gives ~200 names per subclass —
large enough for a within-subclass mean to mean something. One-to-one matching throws away the
unmatched majority of a 1,000-name cross-section, and `#429` has already said the bootstrap is not
valid for the resulting estimator at any `k`. Subclassification keeps every name, needs no caliper,
estimates no covariance, and is a **direct-adjustment weighted average** rather than a matching
estimator, so it sidesteps the `N^{−1/k}` machinery entirely. It is also a construction this lab
already knows how to run: a quintile sort with weights, i.e. the same object as `#431`'s cells with
a different sorting variable.

**What it does NOT license.** Three refusals, all from the paper's own text:

- **A scalar index that is not a treatment probability is not a balancing score.** A composite
  "selection likelihood" built by averaging z-scores, or a first principal component of the
  covariates, fails Theorem 2 unless it happens to be a monotone function of `e(x)`. If a candidate
  wants dimension reduction, the reduction must be a fitted `pr(z = 1 | x)`.
- **Covariance adjustment on the raw covariates is the dangerous one**, and this lab's instinct —
  regress the outcome on the covariates and read the treatment dummy — is exactly that method. The
  paper says it can *increase* bias when the two groups' covariance matrices differ. Newly eligible
  names are plausibly a more homogeneous subset than the pool, which is the condition it warns
  about. Note the tension with `#430`'s "regress, don't match" rule: `#430` is about correcting a
  *matched* estimator's residual covariate gap, which the paper endorses as Use C **on the score**;
  it is not a licence for raw-covariate covariance adjustment in place of balancing.
- **Strong ignorability cannot be established on this panel, so no causal claim may be attached to
  the output.** A committee decides index admission (`#418`), on criteria that are partly
  unpublished and partly discretionary (`#416`-cluster), so `x` demonstrably does not contain
  everything that drove selection. Everything built on this score is a **descriptive balance
  diagnostic** — "the eligible cohort differs from the matched non-event cohort by this much on
  the outcome, after balancing on observable selection probability" — and never an estimate of an
  effect.

**Runtime.** A logit on a handful of features over ~1,000 names per rebalance date is trivially
inside the ~60 s/call budget; `sklearn.linear_model.LogisticRegression` with a fixed
`random_state` and `n_jobs=1` satisfies the determinism rule. The cost is in the walk-forward
bookkeeping, not the fit.

**Pitfall specific to this lab.** The paper's balance diagnostic is an `F` statistic per covariate,
and this folder holds ten notes on what happens when many statistics are computed and the best is
read. A balance table over `k` covariates × 5 subclasses is a multiple-testing surface. Report it
as a *description* of balance, not as a sequence of tests with a decision attached — the online
error-budget machinery (`#328`–`#342`) is for the gate, not for a diagnostic.

## Related

- `notes/2026-11-10-matching-estimator-bias-and-the-dimension-of-the-match.md` — `#429`/`#430`,
  the note that creates the question this one answers. Its `k = 1` carve-out is the reason the
  scalar score matters at all, and its bias-correction regression is this paper's Use C.
- `notes/2026-11-11-matching-on-the-estimated-score-and-its-variance.md` — the modern complement:
  what changes in the **large-sample variance** when `ê(x)` is estimated rather than known. This
  paper's simulation says estimating the score costs little in *bias*; that note says it changes
  the *variance*, and in a direction most practitioners get wrong.
- `notes/2026-11-11-the-psm-paradox-and-random-pruning.md` — the adversarial reading. It accepts
  Theorem 1 and argues that approximating a *completely randomized* experiment, which is all a
  balancing score can do, is the wrong target when a *fully blocked* one is reachable. Read before
  building anything that prunes.
- `notes/2026-11-10-performance-matched-controls-and-mean-reversion.md`,
  `notes/2026-11-10-control-firm-versus-reference-portfolio-biases.md`,
  `notes/2026-11-10-characteristic-matched-benchmark-portfolios.md` — the three finance notes the
  matched-control vein was built on; all match on covariates directly, none uses a scalar score.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` (`#401`/`#411`) —
  why index admission is the natural "treatment" on this panel, and why its selection is not
  ignorable.
- `research/SUMMARY.md` candidate ideas #427–#432.
