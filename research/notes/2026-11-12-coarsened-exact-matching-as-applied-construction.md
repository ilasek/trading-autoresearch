---
title: "Causal Inference without Balance Checking: Coarsened Exact Matching"
authors: Iacus, King, Porro
year: 2012
venue: Political Analysis 20(1), 1–24 (peer-reviewed; the leading methodology journal of its field, outside this rubric's finance tier-1 list)
url: https://doi.org/10.1093/pan/mpr013
citations: 3082 (Crossref, checked 2026-11-12)
sample_period: none — analytic results, a measurement-error simulation, and one previously published non-financial observational dataset
markets: n/a (statistical methodology; no financial data of any kind)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The applied companion to `notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md`
(`#436`), by the same authors, and the source that answers the part of [2026-11-11]'s acceptance
criterion (iii) the JASA paper left thin: **how the coarsening is actually chosen.** It is also, at
3082 citations, the more-used of the pair, and its thesis is the one sentence this lab should take
from the vein:

> With a matching method whose tuning parameter bounds imbalance, the "arduous process … of balance
> checking, tweaking, and repeatedly rerunning the matching procedure is eliminated … **You get what
> you want rather than getting what you get.**"

The argument is the ex-ante/ex-post inversion `#436` establishes, now stated as a workflow claim.
Conventional matching produces a matched set and the analyst then *checks* balance; if the check
fails, the analyst tweaks the specification and re-matches. That loop is a search over
specifications conducted after seeing the data, and it is unnecessary when the construction's
parameter already bounds the imbalance — because the two MIB properties (the bound is determined by
the coarsening, and tightening one covariate's coarsening cannot loosen another's bound) between
them remove both the reason to check and the uncertainty the checking was there to resolve.

The paper is explicit about what this trade costs: fixing imbalance ex ante means the matched count
is an *output*, and the authors defend that on the ground that "bias is more crucial than variance
in observational data analyses" — while adding, in the same breath and against the obvious
objection, that "matching can sometimes even reduce variance by removing heterogeneity and model
dependent inferences." That second clause is the reconciliation `#436`'s note works out against
`#435`, stated here by the authors themselves.

Three further properties are new relative to `#436` and all three matter for how a lab uses the
method rather than for whether the method is sound.

**1. The congruence principle.** A method that projects the covariates out of the space in which
they were measured — into a propensity score, or into a Mahalanobis metric — operates in a space
neither the data producer nor the analyst understands. CEM does not: it works in the original
units, variable by variable, continuous or discrete or mixed. The practical payoff is that the
coarsening can be made to *respect meaningful thresholds in the variable itself* — their example is
coarsening years of education at the high-school, college and postgraduate boundaries, which caliper
matching cannot do because a caliper is a width, not a set of cut points. Nearest-neighbour caliper
matching on the orthogonalised covariates (Cochran–Rubin 1973) is neither MIB nor congruent; the
same caliper applied per variable *without* orthogonalisation is MIB, and congruent for genuinely
continuous variables only.

**2. Common support comes free.** Other approximate matching methods need a separate prior step
restricting the data to the region where treated and control units overlap, so that no
counterfactual is an extrapolation. CEM needs no such step: a coarsened cell is kept only if it
holds both a treated and a control unit, which is the definition of non-extrapolation. The authors
note CEM can therefore be used purely as a common-support restriction to improve *other* matching
methods.

**3. Approximate invariance to measurement error, with a stated condition.** If treatment is
ignorable given unobserved true covariates `X*` but matching is done on observed `X = X* + η`, then
balance on `X` does not imply balance on `X*`, the true propensity score on `X` is not a balancing
score for `X*`, and estimates are biased (citing Battistin–Chesher 2004). Under CEM, **if the
measurement error is smaller than the coarsening, `ε_j > max|η_j|`, and the error happens to respect
the stratum boundaries, the matched dataset is identical whether one matches on `X` or `X*`** — i.e.
exactly invariant. The first condition alone makes it *approximately* invariant, because the second
holds for most observations most of the time. Their simulation perturbs an earnings variable with
Gaussian noise over 5000 replications and measures the share of matched units surviving the
perturbation: CEM retains about 95% of treated and 98% of control units, against roughly 80% for
Mahalanobis and genetic matching and roughly 70% for propensity-score matching. This is the one
place in the vein where **coarsening is a defence rather than a concession**.

## Construction recipe

**Choosing the coarsening, substantively (the authors' recommendation).** Set `ε_j` from knowledge
of how `X_j` was measured and how much it plausibly matters to the outcome — the tolerance is a
statement about indifference, not a statistical estimate. The paper's position is that this is easy
and intuitive in most applications; everything below is offered as orientation when the scale of the
problem makes manual choice impractical.

**Automated route 1 — histogram bin-width rules.** Choosing `ε` is formally the same problem as
choosing a histogram bin width, and the paper names four rules its software implements:

- **Sturges**: `Δ_st = (x_n − x_1) / (log₂ n + 1)` — based on the range.
- **Scott**: `Δ_sc = 3.5 · s_n · n^(−1/3)` — based on an assumed underlying normal, `s_n` the sample
  standard deviation.
- **Freedman–Diaconis**: `Δ_fd = 2 · (Q₃ − Q₁) · n^(−1/3)` — based on the interquartile range, so
  robust to tails.
- **Shimazaki–Shinomoto (2007)**, derived from Poisson sampling in time-series spike recovery, which
  the authors report "works well".

For a panel whose covariates are heavy-tailed, the IQR-based rule is the one whose assumption this
lab's data would not immediately violate; Scott's normality assumption is the one it would.

**Automated route 2 — the SATT error bound, which also ranks the covariates.** Under a Lipschitz
restriction on the unknown outcome function `g₀` (Assumption 1: along each coordinate, `g₀` has
bounded sensitivity `L_j`), the estimation error of the sample average treatment effect on the
treated is bounded by `E₀ = max_j L_j ε_j`. So **finer coarsening directly lowers the maximum
possible estimation error** — the tuning parameter bounds not only imbalance and model dependence
but the effect-estimation error itself. The `L_j` are unknown, and the paper gives an estimator from
below:

```
L̂_j = max over pairs i₁ ≠ i₂ in the CONTROL group of  |Y_{i₁}(0) − Y_{i₂}(0)| / d_j(X_{i₁ j}, X_{i₂ j})
```

with `Ê₀ = max_j L̂_j ε_j`. The products `L̂_j ε_j` are then **a ranking of which covariate is
contributing most of the bound** — i.e. which coarsening to tighten first. Two cautions the paper
states itself: these are estimates from below, so `Ê₀` understates; and the estimator uses the
outcome variable, which is defensible **only because it uses control units alone** (as in Hansen
2008), so no selection bias is induced. Also note that when the `L_j` must be estimated they are
not independent and the bound then depends on `m_T` after all.

**Automated route 3 — progressive ("inductive") coarsening, for when the match leaves too few
units.** The authors are blunt that too few matches "reveals a feature of the data, not a problem
with the method", and that the real fix is more data — but they supply a search procedure for
rethinking `ε`:

1. Work in bin counts `h = (h₁,…,h_k)` rather than widths. Relax by *selectively increasing* `ε_j`,
   i.e. decreasing `h_j`.
2. Relax each `h_j` in decrements of 2 down to `h_j = 10`, then by 1, down to a user-set minimum
   tolerable interval count `h_j^min`. Then repeat for pairs `(h_i, h_j)`, then triples, and so on.
3. When two different relaxations yield the **same total matched count**, break the tie by
   **minimising `L₁`**. This is the one place the `#436` metric enters as an objective rather than a
   diagnostic.
4. Two bookkeeping rules that make the `L₁` values comparable across the search: setting `h_j = 1`
   is equivalent to dropping `X_j`, but **keep the variable at `h_j = 1` rather than dropping it**,
   because `L₁` depends on the number of covariates; and **hold the histogram bins used to compute
   `L₁` fixed** throughout.
5. Read the output as a plot: covariate relaxed on the horizontal axis (with the reduced interval
   count), percentage and absolute count of treated units matched on the vertical axes, each point
   labelled with its `L₁`. The largest vertical jumps identify **which covariate is hardest to match
   on in these data**; points joined by horizontal lines are solutions with equal matched counts and
   unequal `L₁`, i.e. free improvements. Thirty relaxations ran in about seven seconds on their
   illustrative dataset.

**The estimand, explicitly.** CEM discards treated units in cells with no control, so the matched
treated set defines a *local* SATT alongside the global one. The paper's framing is that the
estimand is then fixed ex ante with the two components separately estimated and identified, and
analysts may report the local SATT, the global one, or all three quantities — the point being that
which population is being described is a reported decision, not a side effect.

## Robustness evidence (qualitative only)

Peer-reviewed, 3082 citations (Crossref) — the most-cited source in this vein by a wide margin — and
the substantive claims are theorems proved in the companion JASA paper rather than estimates. Open
source implementations for R, Stata and SPSS accompany the article, which is the strongest form of
methodology honesty available and means the construction above is auditable rather than described.

The measurement-error comparison is the part that is evidence, and its design is reasonable: 5000
replications, a real dataset, a perturbation applied to a genuinely noisy variable, and the metric
(share of matched units surviving perturbation) is the right one for a claim about invariance rather
than about accuracy. Computational timings reported alongside show CEM and the propensity-score
methods at well under a tenth of a second against roughly two minutes for genetic matching, which
matters for anything run at every rebalance date.

Two honest limits. The claim that substantive coarsening choice "is relatively easy and intuitive in
most situations" is the authors' reported experience, not a result; this lab's covariates (trailing
volatility, illiquidity, nominal price) have no natural indifference thresholds of the kind "five
years of age" supplies, which makes the automated routes more load-bearing here than the paper
assumes. And the `L_j` ranking rests on a Lipschitz assumption about the outcome function that is
untestable and, on return data, questionable at the tails.

**The one claim that cuts against the lab's instinct, recorded as such.** The authors argue the
balance-checking loop should be *eliminated*, not improved. This lab's entire matched-control
practice is that loop. The honest reading is that eliminating the loop is licensed only by the MIB
bound — the loop is unnecessary *because* the parameter already bounds what the check would have
measured — so a lab that has not adopted an MIB construction may not adopt the conclusion. See also
`notes/2026-11-12-does-the-matching-paradox-bite-in-practice.md` (`#438`), whose independent authors
reach the opposite recommendation and "stress the importance of checking covariate balance" after
matching.

## Implementability here

This is the construction half of `#436`'s measurement half, and three items are directly actionable.
The `#418` constraint still governs everything below: strong ignorability is unavailable on this
panel, so a CEM-style control is a **balance diagnostic**, not an effect estimate.

1. **The coarsening choice for this panel now has four named defaults instead of none.** `#436`
   said the coarsening is the tolerance and recommended choosing it substantively; this panel's
   covariates do not have substantive indifference thresholds, so the automated rules are the
   realistic route. **Freedman–Diaconis is the one to reach for first** — `2 · IQR · n^(−1/3)` is
   computable per rebalance date from the panel's own cross-section, costs nothing, and its IQR base
   does not assume the normality that Scott's rule does and that return and volatility
   cross-sections violate. Sturges' range basis is the worst choice here for the same reason: this
   panel's ranges are set by its extremes. With roughly a thousand eligible names, `n^(−1/3) ≈ 0.1`,
   so the rule implies on the order of a dozen-ish buckets per covariate before the cell-space
   ceiling in `#436` binds at three or four covariates.

2. **Progressive coarsening is the right shape for the lab's recurring problem, and `L₁` is its
   tie-breaker.** The lab's matched controls fail in a characteristic way: the match is too tight,
   the control ends up thin, and the comparison becomes noise. The procedure above is exactly the
   search for *where to loosen*, it produces a readable plot of matched count against `L₁`, and the
   two bookkeeping rules (keep dropped covariates at one bin; hold the `L₁` bins fixed) are the ones
   a hand-rolled version would get wrong. This is a free diagnostic — no trial — and the output
   names which covariate is hardest to match on, which is itself a finding about the panel.

3. **The measurement-error invariance is the strongest argument in the vein for coarsening this
   lab's covariates rather than matching on them finely.** Several of the panel's matching variables
   are measured with known error: `#422` records a signed error in the volume-only liquidity tier,
   trailing volatility is an estimate with its own standard error, and the stored price level carries
   the back-adjustment problem the lab filed as an engine issue. The result says that if the
   coarsening exceeds the measurement error, the matched set is invariant to it. **So the lab's
   liquidity and volatility controls should be matched on coarse buckets wide enough to swallow their
   own measurement error, and the bucket width is therefore a quantity the lab can derive from its
   own error estimates rather than guess.** The `#406` volatility-tercile construction is already on
   the right side of this; a finer volatility match would be on the wrong side.

Pitfalls, beyond those in `#436`:

- **The `L̂_j` estimator uses the outcome, and on this panel "control units only" needs care.** It is
  safe in the paper because the maximum runs over control units alone. Transposed here, the control
  group is a set of *names*, and their forward returns over the same window the candidate is scored
  on are the outcome. Using them to rank which covariate to tighten is defensible by the paper's own
  argument, but it is an outcome-informed construction choice and belongs in the record as one. If
  in doubt, rank covariates by `ε_j` alone and skip the `L_j` half.
- **The "no balance checking" conclusion does not transfer to a non-MIB control.** Every matched
  control the lab has built so far fixed the count first, so none of them carries the bound that
  makes checking redundant. For those, checking is still mandatory — and `#438` argues it is
  mandatory in general.
- **The Lipschitz assumption is doing real work in the error bound.** `E₀ = max_j L_j ε_j` is a
  statement about a smooth outcome function. A cross-section of returns with a fat left tail is the
  case where `L_j` is effectively unbounded in the region that matters, and the bound then says
  nothing. Treat `Ê₀` as a covariate *ranking* device, which is how the paper actually uses it, not
  as a bound the lab can quote.
- **Timing claims are per match, not per rebalance date.** Sub-tenth-of-a-second figures are for one
  cross-section. The protocol calls `generate_weights` about seven times per trial over a long
  history, so a per-date CEM plus a per-date `L₁` is a loop over hundreds of month-ends; the `O(n)`
  tabulation in `#436` is what makes that affordable, and a nearest-neighbour or genetic alternative
  (two minutes per cross-section in their timings) is not.

## Related

- `notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md` (`#436`) — the companion;
  the MIB class, the propositions, and the `L₁` metric this paper uses as a tie-breaker.
- `notes/2026-11-12-does-the-matching-paradox-bite-in-practice.md` (`#438`) — the adversarial source
  for the vein; reaches the opposite conclusion about whether balance checking can be dropped, and
  supplies two cheaper imbalance metrics.
- `notes/2026-11-11-the-psm-paradox-and-random-pruning.md` (`#435`) — the refusal test that named
  this aim; this paper's "matching can reduce variance by removing heterogeneity" is the authors'
  own statement of the reconciliation.
- `notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md` (`#433`) — the scalar
  score; the congruence principle above is the argument against projecting into its space.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` and
  `notes/2026-11-08-committee-discretion-versus-the-published-admission-rule.md` — see this
  session's annotation.
