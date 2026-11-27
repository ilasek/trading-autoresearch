---
title: "A Scalable Algorithm for Sparse Portfolio Selection — the K-name long-only book solved to certified optimality at index scale, the ridge term that makes it tractable, and a support rule that is a RANKING of dual multipliers"
authors: Bertsimas, Cory-Wright
year: 2022 (arXiv:1811.00138, v5 dated 2021-03-28; first submitted 2018-10-31)
venue: "INFORMS Journal on Computing 34(3), 1489–1511 — peer-reviewed, the flagship computational journal of INFORMS. Venue tier 1 for operations research; outside this folder's finance-journal list, as with the other optimisation sources on the shelf."
url: https://doi.org/10.1287/ijoc.2021.1127
citations: 86 (Semantic Scholar by DOI, checked 2026-11-27); 52 (Crossref `is-referenced-by-count`, same date). Both resolved on the first call.
sample_period: "Daily closing prices 2007-01-03 to 2017-12-29, rescaled to a one-month holding period, used ONLY to produce realistic `(μ, Σ)` inputs for timing experiments. There is no backtest, no rolling evaluation and no return series in the paper. Earlier sections use synthetic data and the Frangioni–Gentile and Chang et al. instance libraries."
markets: "US equities: the constituent sets of the S&P 500, Russell 1000 and Wilshire 5000 (the last ~3,200 frequently traded names), plus synthetic instances and two published benchmark libraries."
tier: "A on what it claims — peer-reviewed tier-1 OR venue, healthy citation velocity for its age, all proofs given, reference implementation published (`github.com/ryancorywright/SparsePortfolioSelection.jl`), and the central objects are theorems that cannot decay. The grade carries an explicit caveat rather than a deduction: the paper makes NO empirical return claim of any kind, so it satisfies none of the evidential criteria a return mechanism would face. It is admitted as a CONSTRUCTION source, on the same footing as `2026-10-24-uncertainty-sets-as-dual-norm-penalties.md`."
validation_overlap: false
published_post_2018: true
read: "Full text of arXiv v5, `arxiv.org/pdf/1811.00138v5`, HTTP 200 on the first request (945 KB PDF, 47 pages → 181 KB of text via `pdftotext -layout`, 606 instances of \" the \", no ASCII shift, `( )`-dropout check zero). All five sections, the appendix pseudocode and the theorem/corollary statements intact; runtime tables extract. Note `file -b` reported '16 page(s)' against `pdfinfo`'s 47 — another instance of the 2026-10-07 lesson that `file`'s page count is not a completeness check."
anti_lookahead_note: "Nothing to withhold. The paper contains no performance figures, no return comparison and no market narrative; its data is used only to make solver timings realistic. The 2007–2017 window stops before this lab's validation split, so no part of the source touches 2018–2023, and nothing in it is post-2023."
---

## Access

One request, no challenge. The authors' own GitHub implementation is linked in the paper and was
**not fetched** — `research/README.md` records that this session's GitHub search API is closed, and
the repository was not needed because the algorithm is stated completely in the text. Recorded so a
later session does not re-derive the pointer: `github.com/ryancorywright/SparsePortfolioSelection.jl`
is the published reference implementation, and the 2026-09-07 lesson (read the author's code when
the contribution *is* an algorithm) would apply if the pseudocode were ever ambiguous. It is not.

## Mechanism

No return mechanism — this is the **tractability half of the cardinality-constrained construction**,
and it answers the question the companion note
(`2026-11-27-limited-asset-markowitz-cardinality-and-quantity-constraints.md`) leaves open: can a
`K`-name long-only book be *optimised* rather than *ranked*, at the width of a real index?

The problem is the one every long-only sorted book is an instance of:

    min_{x ≥ 0}  (σ/2)·x'Σx − μ'x     s.t.  l ≤ Ax ≤ u,  e'x = 1,  ‖x‖₀ ≤ k

NP-hard even with no linear inequalities at all (the authors cite Gao–Li 2013 for this). The
authors' stated motive for `k ≪ n` is worth recording because it is not a cost argument: managers
incur a **monitoring cost per non-zero position**, and investors suspect a manager who does not
control the number of positions of index-tracking while charging active fees. The second is the
*active-share* objection, and it is the mirror image of this lab's own problem — a book that holds
a thousand names at eligible weights **is** the benchmark.

The contribution is two moves.

**Move 1 — add a ridge term and the problem becomes tractable.** Replace the objective with

    (σ/2)·x'Σx + (1/2γ)·‖x‖₂² − μ'x

for fixed `γ > 0`. Three consequences, all proved:

- the **duality gap** between the regularised problem and its second-order-cone relaxation
  **decreases as `γ` decreases and reaches exactly zero at some finite `γ > 0`** (the value is
  data-dependent). Below that threshold the combinatorial problem has a *convex* certificate;
- any optimal solution of the regularised problem is a `1/(2γ)`-optimal solution of the
  unregularised one — so the ridge term is a bounded, quantified approximation, not a different
  problem;
- **the two-stage recipe that follows is the single most transferable thing in the paper**: solve
  the regularised problem, take its **support**, then re-solve a plain convex QP restricted to that
  support with the *unregularised* objective. Because there are finitely many `k`-sparse supports,
  for large enough `γ` this returns the exact optimum of the unregularised problem. Regularise to
  *select*; drop the regulariser to *weight*.

**Move 2 — a reformulation that makes the relaxation strong.** The standard modelling of
"`x_i = 0` if `z_i = 0`" is the big-M inequality `x_i ≤ M·z_i`. The authors substitute `x_i z_i` for
`x_i`, use `z_i² = z_i` and strong duality to obtain a convex mixed-integer quadratic problem whose
continuous relaxation is far tighter, then solve it by outer approximation (cutting planes on the
binary support vector, with an in-out method at the root node and a heuristic warm start). The
lesson generalises past this paper: **big-M is the reason cardinality-constrained books are
reported as intractable**, not the cardinality constraint itself.

## Construction recipe

**The pieces a candidate here would actually use, in order of cheapness.**

1. **Corollary 4 — support recovery by RANKING a dual vector.** The relaxation's dual solution
   carries a vector `w*`. Let `|w*|_[k]` be its `k`-th largest entry in absolute magnitude. If
   `|w*|_[k] > |w*|_[k+1]` (a strict gap at the cut) and a stated complementarity condition holds
   — `γ·Σᵢ zᵢwᵢ* = 1`, `l ≤ γ·Σᵢ Aᵢwᵢ*zᵢ ≤ u`, `zᵢwᵢ ≥ 0`, and `vᵢ* = 0` wherever `zᵢ = 0` — then
   setting `zᵢ = 1` for the `k` largest `|wᵢ*|` and `0` elsewhere is **provably optimal**, and the
   relaxation's bound is exact. This is remarkable for this lab specifically: the optimal `K`-name
   support is, under a checkable condition, **the top `K` of a ranking** — of a dual multiplier
   rather than of a return score, but a ranking. It is also the cheapest possible operator: one
   convex solve plus an argsort, with a *certificate* attached.
2. **Closed form in the degenerate case.** If `Σ` is diagonal, `μ` is a multiple of the ones
   vector and there are no side inequalities, the regularised problem is solvable in closed form.
   Useful as a unit test, and as a reminder that all the difficulty lives in the off-diagonal.
3. **Low-rank covariance as a first-class input.** Their index-scale runs take an SVD of the
   correlation matrix, keep a low-rank estimate (ranks of order 200–300 for `n` in the thousands)
   and rescale by each asset's variance. Runtime depends strongly on `rank(Σ)`, and the authors'
   own experiments vary it as a knob. For a ~1,000-name panel with ~250 trading days of history,
   a full-rank sample covariance is rank-deficient anyway, so the low-rank input is not an
   approximation imposed by the solver — it is the honest estimate.
4. **Minimum-investment constraints**, written `xᵢ ≥ zᵢ·x_i,min`, are handled directly and are the
   expensive constraint class: they slow the method materially while leaving it competitive. This
   is the same diagnosis as the companion note — the *disjunction*, not the count, is what costs.
5. **Hyperparameters.** `κ` weights the return term (they run `κ = 1`, or `κ = 0` with an explicit
   minimum-return constraint whose level is set from the min-variance-with-ridge portfolio's own
   expected return); `γ` is the ridge; `k` is the cardinality budget.

**One data-handling rule copied verbatim because it is causal, cheap and this lab's panel has the
same problem**: when computing means and covariances for the two widest universes they **omit days
with a greater than 20% change in closing price**, on the stated grounds that such moves occur on
low-volume trading and typically reverse the next day. That is a trailing-window estimation filter,
not a selection rule, so it is implementable without lookahead.

## Robustness evidence (qualitative only)

- **Scalability is the claim and it is demonstrated across three universe widths.** Prior
  certifiably-optimal approaches had not been shown to converge in practical time beyond about
  400 securities; this method solves instances drawn from universes of hundreds to roughly three
  thousand names to **provable optimality**, and the authors are explicit that ~3,200 (the widest
  index they know of) is the practical upper bound they are aiming at. In the absence of side
  constraints the method solved every constraint-free instance they considered in under a second,
  and they are careful to attribute part of that to the particular problem data.
- **Honesty markers.** They flag that comparisons against other published methods are imperfect
  because those ran on different machines with unavailable source code; they note the in-out root
  technique "can do more harm than good for easier problems"; they report that market data made
  the problem *easier* than their own synthetic data, i.e. that synthetic instances were the harder
  test; and they publish the code. Multiple-testing is not relevant — nothing is tested.
- **Stability in the regulariser.** Over the whole range of `γ` examined at `k = 10` on a
  ~1,000-name universe, the optimal support changed **once**. So the selected names are not an
  artefact of the ridge level, which is exactly the fragility one would fear from a sparse
  optimiser. Solve times are essentially non-decreasing in `γ`, and below a finite `γ` every
  instance solved with a single cut.
- **The gap in the evidence, stated plainly.** There is **no out-of-sample study, no Sharpe, no
  turnover and no comparison to equal weight**. The paper establishes that the optimal `K`-name
  book is *computable*; it offers no evidence that it is *better than a ranked one*. A session
  that reads this note as support for optimised selection has misread it. The evidence on that
  question is in the two companion notes, and it is weak and cost-fragile.

## Implementability here

**What it settles.** The 2026-11-22 note's worry — that a cardinality cap makes the construction
intractable — is **false as a matter of optimisation** at this panel's width. A `K`-name long-only
book over ~1,000 eligible names with a 25% cap (`l ≤ Ax ≤ u` covers the cap exactly) is solvable
to certified optimality in seconds-to-minutes with a low-rank `Σ` and no minimum-position
constraint, which is the lab's configuration.

**What it does not settle, and this is the binding objection.** The lab's clock, not the solver's.
`generate_weights` runs about seven times per trial under ~60 s per call, and a monthly book over
the visible window is of order 320 rebalances — a budget near **0.2 s per rebalance**. A
per-month-end convex MIQP solve is one to three orders of magnitude over that even at the fast end
of the paper's timings, and the lab has no Mosek, no CPLEX and no Julia: `scipy` and
`scikit-learn` are what is installed, and neither solves a mixed-integer SOCP. So the full method
is **not implementable as a candidate here**, and a note that pretended otherwise would be
useless. Three things are implementable:

1. **The relaxation-then-rank operator (Corollary 4) without the certificate.** Solve the
   *continuous* ridge-regularised long-only problem — a convex QP that `scipy.optimize` handles at
   a few hundred names — rank the resulting weights (or the dual vector where available), take the
   top `K`, and re-solve the unregularised QP on that support. This is the paper's own two-stage
   recipe with the integer search deleted, it is affordable if the pre-screen keeps `n` modest, and
   the gap test `|w*|_[K] > |w*|_[K+1]` is a free diagnostic of whether the cut is even well
   defined. **The honest framing is that this is a heuristic the paper's corollary explains, not
   the optimum the paper computes.**
2. **The ridge level as the one knob worth exposing.** `1/(2γ)` is both the approximation bound and
   the conditioning fix; small `γ` is tractable and heavily shrunk toward equal-ish weights, large
   `γ` approaches the unregularised optimum. Given the folder's accumulated position on estimation
   error, the small-`γ` end is where a long-only book should live, and the source's stability
   finding says the chosen *support* barely moves with it.
3. **The low-rank covariance input**, which the lab needs anyway at ~1,000 names and ~250 days.

**What to measure, free, before writing any candidate.** (a) On stored lead scores, check whether a
strict gap exists at the lab's own cut depth — `|score|_[K] > |score|_[K+1]` with a margin — because
Corollary 4's condition is exactly the statement that the cut is not inside a tie, and `#530` has
already priced what a cut costs in correlation terms. (b) Time one continuous ridge-QP solve at the
panel's eligible width and at a screened width of 50; the 0.2 s budget decides between them before
any strategy is written.

**Two cautions specific to v3.** The paper charges no transaction cost and models no rebalancing,
so it says nothing about how often an optimised support flips; and the companion note's frontier
result implies it can flip discontinuously. And the minimum-investment constraint — the one the
authors find expensive — is the natural way to express "do not hold a name at a weight too small to
be worth its 15–40 bps plus stamp duty", so the version of this construction that is most *correct*
under v3 costs is also the version that is most expensive to solve.

## Related

- `2026-11-27-limited-asset-markowitz-cardinality-and-quantity-constraints.md` — the same object with
  a greedy beam-search operator, actual (thin) return evidence, and the frontier-gap result this note
  does not duplicate.
- `2026-11-27-cardinality-as-an-objective-and-the-cost-fragility-of-the-sparse-frontier.md` — what
  happens to a sparse book's apparent edge once 50 bps per side is charged.
- `2026-10-24-uncertainty-sets-as-dual-norm-penalties.md` — the same authorship lineage and the
  general theorem that a robustness set is a norm penalty; the ridge term here is that theorem's
  simplest instance, used for tractability rather than for robustness.
- `2026-08-22-long-only-as-l1-regularization.md` — the ℓ1 route to sparsity, and the standing
  observation that `x ≥ 0` is itself a regulariser.
- `2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` (`#513`) — the construction
  whose selection step this operator could replace.
- `2026-08-17-naive-vs-optimized-weighting.md` — the folder's standing position that estimated means
  are the expensive input and that equal weight is hard to beat once they enter. Both this paper's
  `μ` and its minimum-return variant inherit that problem; the min-variance-with-ridge special case
  avoids it at the price of being a de-risking construction the standing exclusions bar.
