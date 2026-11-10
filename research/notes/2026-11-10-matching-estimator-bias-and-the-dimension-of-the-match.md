---
title: "Large Sample Properties of Matching Estimators for Average Treatment Effects; and Bias-Corrected Matching Estimators for Average Treatment Effects"
authors: Abadie, Imbens
year: 2006; 2011
venue: Econometrica 74(1), 235–267 (venue tier 1); Journal of Business & Economic Statistics 29(1), 1–11 (venue tier 1)
url: https://doi.org/10.1111/j.1468-0262.2006.00655.x ; https://doi.org/10.1198/jbes.2009.07333
citations: 2164 and 1126 (Crossref, checked 2026-11-10)
sample_period: none — asymptotic theory, simulation, and a 1970s US training-programme evaluation dataset
markets: n/a (econometric methodology; no financial data)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The second half of the [2026-11-09] acceptance criterion — *what the estimate means when the match
is imperfect in a known direction* — has a precise answer, and it is not reassuring. This pair of
papers derives the large-sample behaviour of exactly the estimator the three finance notes in
tonight's cluster use: match each treated unit to its nearest neighbours on observed covariates,
difference the outcomes, average.

Two results carry.

**(1) The bias of a matching estimator is governed by the number of CONTINUOUS matching variables,
and it does not vanish fast enough.** Write `k` for the number of continuously distributed
covariates matched on. The distance between a unit and its nearest neighbour in `k` dimensions
shrinks at rate `N^{−1/k}` as the sample grows — in one dimension the nearest match is very close,
in four it is far, because filling a `k`-dimensional space to a given density takes exponentially
more points. The estimator's **conditional bias inherits that rate**: the authors prove
`B_M = O_p(N^{−1/k})`, with the expected bias of order no better than `N^{−2/k}`.

The consequence is stated in their own abstract and conclusion: since the sampling error of the rest
of the estimator is `O_p(N^{−1/2})`, **for `k` large enough the bias dominates and the matching
estimator is not `√N`-consistent**. Standard confidence intervals around it are then not valid —
not "wide", *not valid*, because they are centred in the wrong place and the miscentring does not
shrink relative to the width. The one clean case is `k = 1`: with a single continuous matching
variable the bias is `O_p(N^{−1})`, the estimator is asymptotically normal, and the bias can simply
be ignored. **Discrete matching variables do not count toward `k`** — matching exactly on a
categorical is free in this accounting.

This is the formal content of the intuition Barber and Lyon reached empirically: their design that
was well specified *everywhere* matched on two variables and dropped industry, and their one failing
cell was the one where the match quality differed systematically between sample and control.

**(2) The bias is removable, by regression, without inflating the variance.** The companion paper's
bias-corrected estimator adjusts each matched pair's outcome difference by the *predicted* outcome
difference attributable to the covariate gap that the match failed to close. For a treated unit `i`
matched to control `j`, instead of imputing `Y_j` for the missing `Y_i(0)`, impute

```
Y_j + μ̂₀(X_i) − μ̂₀(X_j)
```

where `μ̂₀(·)` is an estimated regression of the control outcome on the covariates. Summed over the
sample, the correction is an estimated bias term `B̂` subtracted from the simple matching estimator.
They prove the correction removes the bias **without affecting the asymptotic variance**. The theory
is developed with a nonparametric series estimator for `μ̂₀`, but they note that series estimation
reintroduces the smoothing-parameter choice that matching exists to avoid, and in their own
applications they use a **plain linear regression** on the covariates to build the correction. The
intuition is the whole method: *the match handles the bulk, the regression handles the residual gap,
and each covers the other's weakness.*

Three further facts worth carrying:

- **Matching with replacement** is what the theory covers, and it is also what produces better
  matches — a control unit may serve as the match for several treated units. Matching *without*
  replacement forces worse matches as the pool is consumed.
- **Even when the bias is negligible, a fixed number of matches does not attain the semiparametric
  efficiency bound.** Matching is a convenience estimator, not an optimal one. For `k = 1` the
  efficiency loss can be made arbitrarily small by allowing enough matches.
- **The bootstrap is not valid for the simple matching estimator** (a separate result by the same
  authors). This is a genuine trap: the bootstrap is the default uncertainty tool everywhere else.
  They supply an analytic variance estimator that does not require nonparametric estimation of any
  unknown function.

## Construction recipe

A matched-control design, assembled from the two papers:

1. **Count your continuous matching variables.** If `k = 1`, the bias is ignorable and ordinary
   asymptotics apply. If `k ≥ 2`, assume the bias is *not* ignorable until shown otherwise.
2. **Match exactly on discrete variables** (region, market, sector-like groupings, calendar
   period). These are free — they do not enter `k`.
3. **Match with replacement**, a fixed small number `M` of neighbours per treated unit.
4. **Bias-correct.** Fit a regression of the control-group outcome on the matching covariates;
   adjust each imputed outcome by `μ̂₀(X_i) − μ̂₀(X_j)`. A linear specification is their own working
   choice.
5. **Do not bootstrap the simple matching estimator.** Use the analytic variance estimator, or at
   minimum do not treat bootstrap intervals as valid.

## Robustness evidence (qualitative only)

- These are theorems with stated regularity conditions (Lipschitz or bounded-third-derivative
  regression functions, overlap, a compactly supported covariate density), not empirical claims, so
  "robustness" means the conditions are checkable rather than that the result replicated. The rate
  result is a property of nearest-neighbour distances in `k` dimensions and is as general as that.
- Both papers were published in tier-1 methodology venues, are heavily cited, and the methods ship
  as reference implementations in three statistical environments, which is the strongest available
  form of independent use.
- The simulation evidence in the bias-correction paper is on simulated and training-programme data,
  not markets, and no finding from it is imported here.
- The bias-rate result is corroborated by its own restatement elsewhere in the literature, and the
  `k = 1` exception is stated identically in the abstract, the theorem and the conclusion of the
  Econometrica paper — so it is not a reading artifact.

## Implementability here

**This is a constraint on experimental design, not a strategy.** It costs nothing to apply and it
rules out a class of designs before they are written.

**The binding translation.** A matched-control scout on this panel (see
`2026-11-10-performance-matched-controls-and-mean-reversion.md`) would naturally want to match a
cohort on past return, trailing volatility, dollar-volume rank *and* region. Under this result that
is `k = 3` continuous variables plus one discrete — and at `k = 3` the bias is `O_p(N^{−1/3})`
against sampling error of `O_p(N^{−1/2})`, so **the bias dominates**. With roughly a thousand names
eligible on a typical date and a cohort that is a fraction of them, `N` is in the hundreds, not the
millions; the asymptotics are a warning about the regime the lab actually operates in, not a remote
limit.

Three consequences, all free:

1. **Prefer one continuous matching variable, and make it the selection variable.** The design with
   the best statistical properties here is: match exactly on region (discrete, free), match on
   **past return alone** among continuous variables, and *control* for the rest by regression rather
   than by matching. This is also what the finance literature converged on empirically — the
   Barber–Lyon design that worked everywhere used a wide window on one variable and a
   nearest-neighbour on the second, and `#424`'s decisive comovement test matched on a size *decile*
   (discrete) plus past return.
2. **Bias-correct rather than add a matching dimension.** Adding a fourth characteristic to the match
   makes the match *worse* in this accounting, while adding the same characteristic as a regressor in
   `μ̂₀` costs nothing asymptotically. The folder's instinct — more matching variables is a better
   control — is wrong in a way that has a rate attached.
3. **Do not bootstrap the matched difference.** The lab's standard uncertainty machinery is a paired
   block bootstrap, and it is the right tool for the *trial* statistic. It is explicitly **not**
   valid for a simple nearest-neighbour matching estimator, and a scout that reports bootstrap
   intervals around a matched cohort difference would be reporting intervals with no coverage
   guarantee. Report the analytic variance, or report the difference without an interval and say so.

**What this does not supply.** It gives the bias's *order*, not its sign. "Imperfect in a known
direction" is answered structurally — the bias is whatever the regression function's gap across the
unclosed covariate distance is — and the *direction* has to come from the domain. For this lab the
direction is supplied by the finance notes in the cluster: the unclosed gap is in past return, and
past return's relationship to future return is the thing under test, which is precisely why the
bias-correction regression (`μ̂₀` fitted **on the control group only**) is the right instrument and
why fitting it on the pooled sample would be circular.

**Pitfall.** `μ̂₀` must be fitted causally and walk-forward, like any model in this lab — a
bias-correction regression fitted over the whole visible window and applied backwards is the
standard lookahead, and `CLAUDE.md`'s machine-learning rules apply to it in full. The regression is
small (a handful of covariates), so `strategies/lib/walkforward.py` carries it cheaply.

## Related

- `notes/2026-11-10-performance-matched-controls-and-mean-reversion.md` — the design this constrains;
  its ±10%/±30% two-window scheme is a `k = 2` match and therefore in the regime where the bias is
  not ignorable.
- `notes/2026-11-10-control-firm-versus-reference-portfolio-biases.md` — its two-stage match (window
  then nearest-neighbour) is also `k = 2`; the paper's finding that the *order* of the two stages
  changes specification is the empirical shadow of this result.
- `notes/2026-11-10-characteristic-matched-benchmark-portfolios.md` — a 3-characteristic grid, but
  matched on **quintile cells** rather than on continuous distances, which is exactly the
  discretisation that keeps `k` at zero. That is an argument for cell-based benchmarking over
  nearest-neighbour matching on this panel, and it is not an argument the finance papers make.
- `SUMMARY.md`, "Inference on the weight vector itself" and the online multiple-testing cluster —
  the folder's existing inference notes; this one is about a different object (a treatment-effect
  estimator), not another hurdle for the gate.
