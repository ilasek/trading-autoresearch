---
title: "Optimization of Conditional Value-at-Risk" + "Conditional Value-at-Risk for General Loss Distributions" — the auxiliary-variable trick that makes a tail objective a linear program, and the proposition that under normality it changes nothing
authors: Rockafellar, Uryasev
year: 2000, 2002
venue: The Journal of Risk 2(3), 21–41 (2000; venue tier 2 — practitioner-academic journal, but the paper is the field's standard reference); Journal of Banking & Finance 26(7), 1443–1471 (2002; venue tier 1, peer-reviewed)
url: https://doi.org/10.21314/JOR.2000.038 and https://doi.org/10.1016/S0378-4266(02)00271-6
citations: 5550 for the 2000 paper and 3111 for the 2002 paper (Crossref `is-referenced-by-count`, both checked 2026-10-23, both resolved on the first call)
sample_period: neither paper has an empirical sample in the sense this folder means. Both are optimization-theory papers. The 2000 paper's illustrations are Monte Carlo draws from assumed distributions plus one dated instrument table, which is NOT recorded here (see the anti-lookahead note below); the 2002 paper is pure theory with no numerical section. Nothing in either can touch 2018–2023.
markets: not applicable (method papers); the 2000 paper's illustrations are on constructed three-instrument and option-portfolio examples
tier: A
validation_overlap: false
published_post_2018: false
read: full text of both, from Rockafellar's own flat paper directory at the University of Washington — `sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf` (200 KB, 26 pages, preprint dated 5 September 1999; 60 KB of text, 359 `" the "`) and `sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf` (321 KB, 34 pages; 77 KB of text, 483 `" the "`). Both `pdftotext -layout`, both clean, no ASCII shift, no `/xHH` escapes. The filenames came from the directory listing at `sites.math.washington.edu/~rtr/papers.html`, which prints every paper as `rtr<NNN>-<Slug>.pdf` — see the access note. The published versions were not obtained and are not needed; theorem numbering below is the preprints'.
anti_lookahead_note: the 2000 preprint contains a dated instrument table (a NIKKEI butterfly spread, with a stated as-of date in 1997) and several figures of loss distributions. No number, position, price or date from that table or those figures is recorded in this note, and none of it bears on the mechanism. The only thing taken from §5 is the authors' structural observation that an option book's loss distribution can be far from normal, which is a statement about option payoffs, not about a period.
---

## Mechanism

The previous note ends with a problem. Artzner et al. show that the coherent tail measure is an
average over the tail rather than a quantile, and propose "worst conditional expectation" — but they
describe it as impractical to compute, and their own "tail conditional expectation" is the computable
one and is not coherent. This pair of papers closes that gap, and the closing device is a single
variational identity that is the whole mechanism.

Write the loss as `f(x, y)`, `x` the decision (a portfolio) in a set `X`, `y` the random vector. For a
confidence level `β`, `β`-VaR is `α_β(x) = min{α : Ψ(x, α) ≥ β}` and `β`-CVaR is the conditional
expectation of loss given that loss is at least `α_β(x)`. CVaR is defined *through* VaR, so minimising
it looks like it requires computing a quantile inside an optimisation loop — and a quantile is a
non-convex, locally-flat, multi-local-minimum function of the weights.

**The identity.** Define

```
F_β(x, α) = α + (1−β)^{-1} · E[ (f(x,y) − α)^+ ]
```

**Theorem 1 (2000).** As a function of `α`, `F_β(x, α)` is convex and continuously differentiable, and

```
φ_β(x) = min_α F_β(x, α)
```

i.e. **minimising this auxiliary function over the scalar `α` returns CVaR itself**, and the argmin set
`A_β(x)` is a non-empty closed bounded interval whose **left endpoint is VaR**. So `α` is not a
parameter to be estimated and plugged in — it is a free variable of the optimisation, and the
optimisation recovers VaR as a by-product of computing CVaR.

**Theorem 2 (2000).** Minimising CVaR over `x ∈ X` is equivalent to minimising `F_β(x, α)` jointly over
`(x, α) ∈ X × ℝ`, with the same optimal `x` and with `α*` giving that portfolio's VaR. Furthermore
`F_β(x, α)` is **convex in `(x, α)` jointly** whenever `f(x, y)` is convex in `x`. For a portfolio the
loss `f(x, y) = −xᵀy` is *linear* in `x`, so `F_β` is convex in `(x, α)` and, on a convex `X`, the whole
problem is convex programming.

Why this works is worth stating in one line, because it is the reusable idea: `(f − α)^+` is the
**shortfall beyond a threshold**, and `α + (1−β)^{-1}E[(f−α)^+]` is a function whose minimiser over the
threshold is the threshold that makes the tail mass exactly `1−β`. The quantile is the *solution* to a
convex problem rather than an input to one. (The same device is the pinball/quantile-regression loss;
the folder's quantile-regression notes are the forecasting-side cousin of this.)

**What the 2002 paper adds, and it is not cosmetic.** The 2000 paper assumes the loss distribution has
no atoms. The 2002 paper removes that assumption, and in doing so repairs exactly the defect Artzner
et al.'s Proposition 5.1 exposed. With atoms there are three distinct functionals:

- **CVaR⁻** ("lower CVaR"), the expectation of losses *strictly* above VaR;
- **CVaR⁺** ("upper CVaR"), the expectation of losses `≥` VaR; and
- **CVaR**, defined as the **mean of the `α`-tail distribution**, where the tail distribution is
  constructed by *splitting the atom at the quantile* — taking only the part of its mass needed to
  make the tail weigh exactly `1−α`.

**CVaR is coherent; CVaR⁺ and CVaR⁻ are not.** The authors are explicit that `CVaR⁻` is the functional
Artzner et al. had in hand when they found the coherence failure, and that WCE was their remedy —
"impractical" in Rockafellar–Uryasev's word — whereas CVaR-with-the-atom-split is both coherent and
minimisable by the identity above.

**Proposition 6 (2002)** makes the splitting concrete: with `λ_α(x) = [Ψ(x, ζ_α(x)) − α]/[1 − α]`,

```
CVaR = λ·VaR + (1 − λ)·CVaR⁺
```

a weighted average of two functionals **neither of which is coherent**, whose particular weighting is.
The authors call the formula "surprising" themselves. **Proposition 8** gives the discrete-sample
formula directly: with ordered losses `z₁ < … < z_N` of probabilities `p_k` and `k_α` the index where
cumulative probability first reaches `α`,

```
CVaR = (1−α)^{-1} [ (Σ_{k≤k_α} p_k − α)·z_{k_α} + Σ_{k>k_α} p_k z_k ]
```

— the partial weight on the boundary observation is the atom-splitting, written out.

**Corollary 9 is a trap and is the single most practically important line in the pair.** If the worst
loss `z_N` has probability `p_N > 1 − α`, then `CVaR = VaR = z_N`: the measure collapses onto the
single worst observation. On an equally-weighted empirical sample of `T` days, `p_N = 1/T`, so this
triggers whenever `α > 1 − 1/T`. More generally the effective number of observations entering CVaR at
level `α` is about `T(1−α)`, and the estimator is an average of that many points. **A tail level chosen
without reference to the sample length silently turns a tail average into a single-observation
statistic.**

## Construction recipe

**The linear program, exactly as the 2000 paper gives it (§3).** Sample the return distribution to get
scenarios `y₁, …, y_q` (for this lab: the historical daily return rows in the visible window, equally
weighted). Minimise, over `x` and the scalar `α` and auxiliary variables `u_k`:

```
minimise    α + (1 / (q(1−β))) · Σ_k u_k
subject to  u_k ≥ 0                     for k = 1..q
            xᵀy_k + α + u_k ≥ 0         for k = 1..q      [i.e. u_k ≥ −xᵀy_k − α = loss − α]
            x_j ≥ 0,  Σ_j x_j = 1                        [long-only, fully invested]
            −xᵀm ≤ −R                                    [optional expected-return floor]
```

Note what the paper's own illustrative constraint set is: `x_j ≥ 0` with `Σ x_j = 1`. **The paper's
worked constraint set is exactly this lab's constraint set** (long-only, gross 1.0), which is unusual
for a risk-measure paper and means nothing has to be adapted on that axis. The authors note explicitly
that the reduction to linear programming "does not depend on `y` having a special distribution."

Sizes: `q` scenarios and `n` instruments give `n + q + 1` variables and about `2q` constraints, so the
LP grows with the *scenario count*, not just the instrument count. The authors mention that
non-smooth optimisation on the original `n`-dimensional problem can beat the LP when few instruments
are being adjusted, because it adds no auxiliary variables — relevant if a candidate ever rebalances a
small sleeve rather than a whole book.

**The three problems to keep apart**, in the paper's own numbering: (P1) minimise CVaR, (P2) minimise
VaR, (P3) minimise variance. The method solves (P1) and returns (P2)'s objective value at (P1)'s
solution, which is *not* solving (P2). The authors' judgement is that "(P1) is a better problem to be
solving for risk management than (P2)" — and their reason is the previous note's: (P2) is non-convex
in the weights with multiple local extrema.

**The result that bounds what any of this can buy.** The 2000 paper's Proposition (§3, proved via
symbolic algebra under normality) states: if the loss is normally distributed and `β ≥ 0.5` and the
expected-return constraint is active, then **the solutions to any two of (P1), (P2), (P3) are the
same portfolio.** The closed forms are

```
VaR_β(x)  = µ(x) + c₁(β)·σ(x),     c₁(β) = √2 · erf⁻¹(2β − 1)
CVaR_β(x) = µ(x) + c₂(β)·σ(x),     c₂(β) = √(2π) · exp(erf⁻¹(2β−1)²) · (1−β)⁻¹   [as printed]
```

Both are **affine in `(µ, σ)`** with a `β`-dependent slope. So under normality, choosing `β` chooses a
point on the mean–variance frontier and nothing more: **CVaR optimisation is minimum-variance
optimisation with a reparameterised risk aversion.** Every bit of value in a CVaR objective comes from
the loss distribution's departure from normality, and the authors' own illustration of where that
departure comes from is an option book — a payoff nonlinearity — not an equity portfolio.

**Mixed-level CVaR.** Not in these two papers but in the companion note's Example 4: a convex
combination `Σᵢ λᵢ CVaR_{αᵢ}` is again coherent and still an LP (one `α` variable and one `u` block per
level). This is the right way to express "care about the whole tail, not one level" and it removes the
`β`-choice degree of freedom that Corollary 9 makes dangerous.

## Robustness evidence (qualitative only)

The theorems are theorems and are not in dispute; the identity in Theorem 1 is now standard and is the
basis of essentially all practical CVaR computation, of the regulatory move from VaR to expected
shortfall, and of the quantile-regression-style formulations in machine learning. 5550 and 3111
Crossref citations between them. Pflug's coherence proof for CVaR, Acerbi–Nordio–Sirtori's independent
proof, and the authors' own §3 of the 2002 paper are three separate routes to the same coherence
result, so that claim is replicated in the only sense a mathematical claim can be.

What is *not* established by either paper, and the authors do not claim it, is that a CVaR-optimal
portfolio performs better out of sample than a variance-optimal one. The 2000 paper's comparison of
(P1) and (P3) is a comparison of *in-sample optima under an assumed distribution*, plus the normality
proposition showing the two coincide when the assumption is Gaussian. **There is no out-of-sample
evidence in this pair at all**, and the literature that supplies it points the other way — see the
noise-sensitivity note, whose finding is that the estimation error of a tail objective is larger than
that of variance at the same panel dimensions, and that this gap grows as the tail level deepens.

The honest summary of the pair's standing: a complete and settled solution to the *computational*
problem of minimising a coherent tail measure, with the *statistical* problem of whether you should
left open and answered unfavourably elsewhere.

## Implementability here

**Runtime, computed rather than guessed, and this is the first binding constraint.** The protocol calls
`generate_weights` about seven times per trial and wants a call under ~60s. A CVaR LP over the full
eligible panel at a single rebalance date has `n ≈ 1,000` and, with a trailing window of `T` daily
rows as scenarios, `q = T`. A two-year window is `q ≈ 500`, giving ~1,500 variables and ~1,000
inequality constraints — a dense LP of that size is solvable by `scipy.optimize.linprog`'s HiGHS
backend in roughly a second, but it must be re-solved **at every rebalance date**. Over a 2018–2023
validation span that is ~72 month-end solves per call and ~500 per trial. That is plausible at
month-end cadence and **not** plausible at daily cadence. Any candidate built from this must be
month-end or slower, which the protocol supports directly (sparse rows are rebalance instructions).

**The second constraint is the one that should stop most such candidates before they are written, and
it is arithmetic, not opinion.** The tail average at level `β` on a trailing window of `q` days is an
average of about `q(1−β)` observations. At `q = 500` and `β = 0.95` that is **25 days**; at `β = 0.99`
it is **5 days**; and Corollary 9 says at `β > 1 − 1/q` it is **one day**. A long-only book over ~1,000
names whose weights are chosen to minimise a 25-observation average is fitting the identity of 25
particular days. The lab has an existing, measured verdict on this shape of construction — see
`SUMMARY.md`'s sections on what a selected maximum is worth and on where a long-only book's risk
actually lives — and nothing in these papers argues against it. **The tail level and the window length
are not independent choices and a candidate must state `q(1−β)` explicitly.**

**Where the vein is nonetheless live, and it is not in the weights.** Three uses survive both
constraints:

1. **As a diagnostic, not an objective — free, no trial, no holdout.** Compute CVaR (by Proposition
   8's discrete formula, which needs no optimisation at all — it is a weighted sum of sorted returns)
   of the champion's and the equal-weight pool's *realised* validation returns, and report the
   difference alongside the skill number. This is a property of series the lab already has, costs
   nothing, reads nothing it should not, and answers a question the Sharpe-based gate cannot: whether
   a lead's skill is accompanied by a worse tail than the benchmark's. It composes with the folder's
   existing free-diagnostic queue rather than competing with it.
2. **Mixed-CVaR as a *scaling* rather than a *selection* device.** Instead of optimising weights,
   use `CVaR_β` of a name's own trailing returns in place of trailing volatility in an
   inverse-risk weighting on an *already-chosen* selection. This changes `n` from 1,000 to 1 — each
   name's CVaR is a univariate sorted average, no LP, no covariance, no `N/T` problem at all — and it
   is a one-line swap in an existing long-only weighting helper. The honest prior from the previous
   note is that it will track inverse-volatility weighting closely, so **the informative version of
   this is to measure the cross-sectional rank correlation between a name's trailing `CVaR_β` and its
   trailing `σ` on this panel before writing any candidate.** If that correlation is near one, the
   vein is closed for weighting and the measurement cost was a handful of lines.
3. **The expected-return floor as the live constraint, not the risk term.** In the LP above the only
   place a *forecast* enters is `−xᵀm ≤ −R`. Everything else is risk. The 2000 paper's own normality
   proposition requires that constraint to be *active* for (P1) and (P3) to coincide — i.e. the
   interesting portfolios are the ones where the return constraint binds. A candidate whose selection
   signal enters as `m` and whose risk term is CVaR is making two bets; the folder's standing
   construction-versus-idea question applies, and the signal should be measured in a simpler wrapper
   first.

**Three pitfalls specific to this repo.**

- **Costs are outside the LP and are heterogeneous under v3.** The program above has no turnover term.
  Under v3 each name carries a liquidity-tier cost (15/20/30/40 bps per side) plus the listing market's
  transaction tax, so a cost-blind re-optimisation at each rebalance will churn across *differently
  priced* names. A turnover or `L1`-deviation-from-current-weights term keeps the problem an LP (it is
  piecewise linear) and should be in it from the start, not added after a cost failure.
- **The 25%-per-position cap and the eligibility boundary are both just rows in `X`.** `x_j ≤ 0.25`
  and `x_j = 0` for non-eligible `j` are linear, so they cost nothing to impose and must be imposed
  *inside* the optimisation rather than by clipping afterwards — clipping a weight vector after
  optimisation returns a point that solves no problem.
- **Determinism.** The causality check compares holdings at `1e-6`. An LP with a degenerate optimum
  (and this LP is degenerate whenever the argmin interval `A_β(x)` is non-trivial, which Theorem 1
  says can happen) can return different vertices on different runs or different platforms. Pin the
  solver and method explicitly, and prefer a formulation with a unique optimum (a strictly convex
  turnover penalty does this) over one that relies on tie-breaking.

**What is not implementable:** nothing in this pair needs fundamentals, intraday data, options or
short interest. The method is fully reachable from daily closes. The obstacle is dimension and tail
sample size, not data availability.

## Related

- **`2026-10-23-coherent-measures-of-risk-axioms.md`** is the prior note and the reason this one
  matters: it supplies the axioms, the VaR non-subadditivity counterexamples, and the TCE-vs-WCE gap
  that the 2002 paper's atom-splitting closes. It also carries the normality remark that this note's
  §3 Proposition turns into an exact statement.
- **`2026-10-23-generalized-deviation-measures.md`** generalises the objective from CVaR to the whole
  sublinear deviation family (lower semideviation, mixed CVaR, worst-case mixed CVaR) and gives the
  optimality conditions under constraints, which is the right reference if a candidate wants a
  long-only-aware first-order condition rather than a solver call.
- **`2026-10-23-noise-sensitivity-of-risk-measures.md`** is the counterweight and should be read
  before anything here is implemented. It supplies the `N/T` arithmetic that bounds use (1) above and
  rules out the full-panel weight optimisation.
- Folder sections this composes with: "Estimating the book instead of forecasting it — the precision
  matrix, what is computable at this panel's width" (the same `N/T` problem for the covariance route);
  "What a selected maximum is worth" (the `q(1−β)`-observation problem is a selected-extreme problem);
  "The objective itself — growth, utility, and the gate's own statistic"; and the quantile-regression
  notes, whose asymmetric loss is the same variational device used to forecast rather than to allocate.
- **No tension with `experiments/learnings.md`.** Nothing in this folder or that file has measured a
  CVaR or deviation objective on this panel under any protocol version, so there is no refutation to
  contradict and no constant to carry. The learnings file's standing warning about risk-overlay
  constructions backfiring is about *timing* overlays on a signal; a CVaR weighting is a
  cross-sectional weighting, a different object, and is untested here.
