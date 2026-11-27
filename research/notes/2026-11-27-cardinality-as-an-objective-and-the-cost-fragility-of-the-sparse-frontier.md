---
title: "Efficient Cardinality/Mean-Variance Portfolios — the number of names treated as an OBJECTIVE rather than a constraint, the whole K ladder as a Pareto front, and the one source in this cluster that charges costs and reports what they do"
authors: Brito, Vicente
year: 2014 (conference version of 2013)
venue: "System Modeling and Optimization (IFIP TC7 conference volume), IFIP Advances in Information and Communication Technology, pp. 52–73, Springer. A peer-reviewed conference chapter in an optimisation series — venue tier 3 by this folder's rubric: below a journal, above a preprint."
url: https://doi.org/10.1007/978-3-662-45504-3_6
citations: 21 (Semantic Scholar by DOI, checked 2026-11-27); 12 (Crossref `is-referenced-by-count`, same date).
sample_period: "Two families. (a) FTSE 100 individual securities, daily, 01/2003–12/2007, with in-sample 01/2003–12/2006 and twelve monthly evaluation periods; a second pass extends the in-sample window to 12/2010 and uses fifteen daily evaluation periods. (b) Fama–French benchmark portfolios, monthly, 07/1971–06/2011, with in-sample 07/1971–06/1996 and fifteen annual evaluation periods."
markets: "UK (three nested FTSE 100 subsets of 12, 24 and 48 securities) and US (Fama–French industry sets FF10, FF17, FF48 and the 100 size/book-to-market portfolios). Both are small cross-sections; the FF sets are portfolios, not individual stocks."
tier: "C. Peer-reviewed and fully specified — the construction, the solver settings and the cost formula are all reproducible from the text, which is more than many tier-B sources give. Held at C on evidence, for four independent reasons: the cross-sections are 12–100 assets, the out-of-sample evaluation is twelve to fifteen periods from a single estimation window, the authors state outright that the Sharpe differences against the benchmark were NOT statistically significant, and the books are not long-only — the variable bounds are ±10, i.e. unlimited shorting and tenfold per-name leverage. Treated as hypothesis fodder and as a source of CONSTRUCTION facts, never as evidence for a level."
validation_overlap: false
published_post_2018: false
read: "Full text from the second author's own flat paper directory, `www.mat.uc.pt/~lnv/papers/cardMV.pdf`, HTTP 200 on the first request (570 KB PDF, 22 pages per `pdfinfo` → 57 KB of text via `pdftotext -layout`, 463 instances of \" the \", no ASCII shift, `( )`-dropout check zero). Sections 1–5, Appendix A (the solver settings) and the reference list intact. The paper's evidence is carried entirely by 34 figures, which do not extract; every claim recorded below is from the prose, and nothing is inferred from a figure."
anti_lookahead_note: "The source's results live in figures and in a discussion section that names calendar windows. No level, no ratio, no cumulative path and no 'worked in period Y' claim is recorded here. The one directional finding carried — that the cost charge reverses the comparison on individual securities but not on pre-aggregated portfolios — is a statement about two DATA TYPES, not about two periods, and is recorded that way deliberately. The paper's robustness pass over a longer in-sample window is recorded as a design fact only. Nothing in the source is post-2023."
---

## Access

One request, first try, from the pattern `research/README.md` keeps rediscovering: **a
methodologist's own site organised as a flat `/papers/<slug>.pdf` directory**. This is the
`robjhyndman.com/papers/` lesson (2026-10-13) and the `burns-stat.com` lesson (2026-10-15) on a
third host — a university mathematics department page, `www.mat.uc.pt/~lnv/papers/`, with short
derivative slugs (`cardMV.pdf`). The Springer chapter itself was never attempted. **For an
optimisation paper, try the applied-mathematician's own directory before the publisher**; the
finance-faculty-page lesson generalises to mathematics departments.

## Mechanism

Not a return mechanism. It is a reframing of the construction object, and the reframing is the
contribution: **stop treating the number of held names as a constraint and treat it as an
objective**.

The cardinality-constrained problem needs `K` supplied from outside and must be re-solved for each
value of it. Instead, minimise two things at once — a mean–variance score and the count:

    min  f₁(w) = −(μ'w)/(w'Qw)        [profit per unit of variance; parameter-free]
    min  f₂(w) = card(w) = ‖w‖₀
    s.t. e'w = 1,  Lᵢ ≤ wᵢ ≤ Uᵢ

The solution is not a portfolio but a **Pareto front in (cardinality, mean–variance) space**: for
every attainable `K`, the best achievable score, and the weights that achieve it. An investor with
a score target reads off the *lowest* cardinality that attains it; an investor with a cardinality
budget reads off the best score available at that budget. Three structural points follow.

- **The objective is parameter-free.** `−μ'w / w'Qw` needs no risk-aversion coefficient and no
  return target, which removes the knob whose sweep the companion note shows is *invalid* on a
  non-convex feasible set. That is a real advantage and it is why the biobjective framing is worth
  recording rather than dismissing as a repackaging.
- **`card(·)` is discontinuous**, so gradient methods are unavailable; the authors use a
  **derivative-free multiobjective** method (direct multisearch, polling-based), which only needs
  function values and tolerates discontinuity. They state explicitly that **the Pareto fronts
  themselves are discontinuous** — independent confirmation, from the other side of the problem, of
  the frontier-gap result in `2026-11-27-limited-asset-markowitz-cardinality-and-quantity-constraints.md`.
- **The literature gap they claim is the one this folder cares about.** Prior tri-objective work
  (minimise variance, maximise return, minimise cardinality) existed; the authors say those authors
  "did not investigate the effects of cardinality constraints on portfolio models in terms of
  out-of-sample performance, a subject still poorly analyzed in the literature". That is a direct
  statement that the *evidence* on whether optimised sparse selection pays out of sample is thin —
  consistent with what the other two notes in tonight's cluster found.

## Construction recipe

**What is actually fed to the solver** (Appendix A, and this is where the implementability
problems are):

- `card(w)` is replaced by `Σᵢ 1{|wᵢ| > ε}` with `ε = 10⁻⁸`. A tolerance is unavoidable, and its
  level is a construction choice nobody reports: too small and numerical dust counts as a position,
  too large and genuinely held names vanish.
- The variable bounds are made **symmetric, `Lᵢ = −b`, `Uᵢ = +b`, with `b = 10`**. So the books are
  long–short with up to tenfold per-name leverage. This is the single most important fact about the
  source and it governs everything below.
- The budget equality `e'w = 1` is **eliminated** (direct-search methods cope badly with
  equalities) by substituting `w_N = 1 − Σ_{i<N} wᵢ` and bounding the substituted expression. Worth
  copying as a technique whenever a derivative-free solver meets a budget constraint.
- Solver settings that actually mattered: raise the function-evaluation budget to ~2×10⁶ for
  `N ≤ 50` (and ~10⁷ for the 100-asset set), tighten the step tolerance from 10⁻³ to 10⁻⁷, turn the
  evaluation cache off for speed, and **initialise the nondominated list with a single point rather
  than the default ~`N` points** — which they found worked better.

**Cost accounting, which is the part the other two sources in this cluster do not have.**
Proportional cost of 50 bps per transaction, charged on the full rebalance:

    TC = Σ_t Σ_i 0.5% · |w_{i,t+1} − w_{i,t}|

and then a **net Sharpe**, `(m − TC − r_f)/σ`, with a real short-rate series as `r_f` (3-month UK
T-bills for the UK sets, 90-day US T-bills for the FF sets). Two reference books are marked
throughout for comparison: the unconstrained maximum-profit-per-variance portfolio (the
maximum-cardinality endpoint of the same front) and the **no-short minimum-variance** portfolio.

**Three cost facts worth carrying, none of them dated.**

1. **The sparse efficient books' turnover sits between the two reference books** — cheaper than the
   max-score portfolio, dearer than the long-only minimum-variance one. The authors attribute the
   minimum-variance book's cheapness directly to **the no-short constraint limiting the weights at
   the outset**, which is this folder's `long-only as ℓ1 regularisation` result arriving from the
   turnover side rather than the estimation side.
2. **Cost rises with cardinality, and only moderately.** More names means more lines to trade, but
   the marginal cost of an extra name is small. So the `K` knob is a weak lever on turnover — the
   lever is *how much the support and the weights move between rebalances*, not how many names
   there are.
3. **The cardinality-constrained minimum-variance MIQP beat the authors' own mean–variance Pareto
   books on net-of-cost Sharpe**, and their own explanation is that its costs are lower *because it
   does not estimate expected returns*. The estimated mean is charged twice: once in error, once in
   turnover.

## Robustness evidence (qualitative only)

- **The central negative, and it is the reason this note exists.** Gross of costs, a large number of
  the sparse efficient books beat the equal-weight benchmark on both data families. **Net of 50 bps
  per side, they did not beat equal weight on the individual-security sets at all; they still did on
  the Fama–French sets.** The authors state this plainly. The difference between the two families is
  not a period and not a market — it is that the FF "assets" are *already diversified portfolios*,
  so the optimiser's weight changes move slower and cost less, while on individual securities the
  same construction's turnover eats the edge. **Recorded as a claim about data type.** For a lab
  whose panel is individual large-cap stocks, that is the relevant half.
- **No statistical significance.** §4.4 says the p-values for the Sharpe differences against the
  naive benchmark were computed and are not reported "because they are not statistically
  significant". That the authors say so is methodology honesty; that it is true is a reason to take
  no level from this source at all.
- **Breadth.** Two markets, 12–100 assets, one estimation window per family, twelve to fifteen
  evaluation periods. A second pass with a longer in-sample window and daily rather than monthly
  evaluation periods is reported by the authors as leaving their conclusions unchanged. There is no
  replication by other authors and none of the standard replication audits covers this venue.
- **The method claim is better supported than the return claim.** Derivative-free multisearch
  recovered the whole front in tens of seconds at ~50 assets, and the authors note the structure of
  the problem (`f₁` smooth with known derivatives, the poll step parallelisable) was deliberately
  *not* exploited — so the runtime is an upper bound for a naive implementation, not a limit.

## Implementability here

**Scale is the first wall, and it is lower than the other two sources'.** Tens of seconds for a
single front at ~50 assets, and ~10⁷ function evaluations at 100 assets, against a per-rebalance
budget here of order 0.2 s (seven `generate_weights` calls per trial, ~60 s each, ~320 monthly
rebalances). A derivative-free multiobjective search over ~1,000 eligible names at every month-end
is **not merely slow, it is the wrong order of magnitude by six or more**. The biobjective framing
is therefore a **diagnostic to run once on a screened subset**, never a rebalance-time operator.

**What survives, and what it is good for.**

1. **The `K` ladder as a shape, not a book.** Run the front once, offline, on a *small screened*
   subset — the kind `#513`'s filter step already produces — and look at where the Pareto front
   flattens. The flattening cardinality is the first non-arbitrary answer this lab would have to
   "how many names", and it costs no trial. The same caution as in the companion note applies with
   full force: **choosing `K` by reading an in-sample front is in-sample objective maximisation**,
   the exact behaviour the deflated-Sharpe bar punishes, so a ladder read this way licenses a
   *pre-registered* `K`, not a tuned one.
2. **The discontinuity warning.** Two independent sources now say the cardinality-constrained
   frontier has gaps. For v3 this is a **turnover** warning before it is an optimisation warning: a
   construction whose support can jump discontinuously when a target or an estimate moves slightly
   will churn, and churn is charged at 15–40 bps plus stamp duty, plus the drift trades it implies.
3. **The cost finding, used as a prior rather than a number.** The one cost-aware source in this
   cluster says the sparse-optimised book's edge over equal weight **did not survive 50 bps per side
   on individual stocks**. The lab's own costs are 15–40 bps per side plus statutory taxes, with UK
   names — of which this panel holds many — among the dearest. So the prior on "optimised `K`-name
   selection beats the lab's existing top-`K`-by-score book after v3 costs" should be **low**, and a
   candidate in this family should be written to measure turnover first and skill second.

**What explicitly does not transfer.** The ±10 bounds. Everything the source reports is a book that
can short and lever, which inflates both its gross score and its turnover; the long-only
minimum-variance reference book inside the same paper is cheaper precisely because it cannot. A
long-only, 25%-capped version of their construction is a *different* object whose cost profile this
source does not measure, and the direction of the difference is favourable — which is the one honest
reason to not treat the negative above as decisive.

## Related

- `2026-11-27-limited-asset-markowitz-cardinality-and-quantity-constraints.md` — the same `K` ladder
  obtained as a by-product of an exact increasing-set search rather than a derivative-free Pareto
  sweep, and the formal version of the frontier-gap result.
- `2026-11-27-sparse-portfolio-selection-at-index-scale-ridge-and-outer-approximation.md` — the
  tractable end of the same object, and the reason the biobjective sweep is not the way to get the
  ladder at panel width.
- `2026-08-22-long-only-as-l1-regularization.md` — the no-short constraint as a regulariser; this
  source adds that it is also a *turnover* reducer, which that note does not claim.
- `2026-08-17-naive-vs-optimized-weighting.md` — the equal-weight benchmark this source uses and
  mostly fails to beat net of costs. The lab's own gate measures skill against an equal-weight
  eligible pool, so the comparison is the same one.
- `2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` (`#513`) and `#530`'s price
  for the selection step — the live construction this cluster is evidence about.
