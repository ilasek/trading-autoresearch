---
title: "Linear vs. quadratic portfolio selection models with hard real-world constraints — the explicit K-name constraint as a construction object, the increasing-set operator that solves it, and the whole K-ladder for the price of one pass"
authors: Cesarone, Scozzari, Tardella
year: 2015 (working-paper version dated July 2010; arXiv:1105.3594)
venue: "Computational Management Science 12(3), 345–370 — peer-reviewed. An operations-research / management-science venue rather than a finance journal, so not one of the rubric's tier-1 names; graded tier 2 on venue."
url: https://doi.org/10.1007/s10287-014-0210-1
citations: 48 (Semantic Scholar by DOI, checked 2026-11-27); 31 (Crossref `is-referenced-by-count`, same date). Both resolved on the first call.
sample_period: "Two independent instance families. (a) Beasley OR-Library `indtrack1–8`: 290 weekly returns built from price data March 1992 – September 1997. (b) The authors' own five data sets: 263 weekly dividend-adjusted prices, March 2003 – March 2008, split into an in-sample window March 2003 – March 2007 and a single out-of-sample year April 2007 – March 2008."
markets: "Thirteen national-index constituent sets. OR-Library: Hang Seng (31), DAX 100 (85), FTSE 100 (89), S&P 100 (98), Nikkei (225), S&P 500 (457), Russell 2000 (1318), Russell 3000 (2151). Authors' own: EuroStoxx 50 (47), FTSE 100 (76), MIBTEL (221), S&P 500 (476), NASDAQ (2191)."
tier: "B. Peer-reviewed; the formulations and the algorithm are stated completely enough to re-implement; the instance set spans five markets and reaches 2,191 names, which is wider than this lab's own eligible cross-section. Held below A because the return evidence is one twelve-month hold after one estimation window, no transaction costs are charged in that evaluation, no significance test of any performance difference is reported, and the paper's own contribution and emphasis are computational rather than empirical."
validation_overlap: false
published_post_2018: false
read: "Full text of the authors' arXiv working-paper version, `arxiv.org/pdf/1105.3594.pdf`, HTTP 200 on the first request (622 KB PDF, 28 pages → 124 KB of text via `pdftotext -layout`, 509 instances of \" the \", no ASCII shift, `( )`-dropout check zero). Sections 1–7 intact including the Increasing Set Algorithm pseudocode and both theorem statements; the runtime tables extract cleanly. The published Computational Management Science version was not fetched (Springer closed for this DOI); section numbering below is the preprint's."
anti_lookahead_note: "The paper's ex-post section is a single dated window and its figures are cumulative portfolio-value paths. No level, no ratio and no directional claim tied to a calendar period is recorded here; the frontmatter's sample_period is the only date, as the note format requires. Nothing in the source is post-2023."
---

## Access

One request, no challenge. arXiv is the reliable channel for this group: `iris.uniroma1.it`,
`iris.uniroma3.it` and `flore.unifi.it` all hold records for the published version and were not
needed. Recorded as a positive, and as a reminder that for an Italian OR group the arXiv
working paper is usually the complete article rather than a stub.

Two negative channel results from the same session, both worth carrying:
**`bura.brunel.ac.uk`** (Brunel University Research Archive, which holds the theses behind the
Beasley index-tracking series) **failed twice with `HTTP 000 size=0`**, and the proxy named the
cause as `ws_closed_mid_exchange` — a **transport failure, not an origin refusal**, the same
signature `research/README.md` records for `web.archive.org` and `api.fatcat.wiki`.
**`core.ac.uk` is still Cloudflare-challenged** (403 with a ~5.4 KB body on two different
download ids), confirming the 2026-10-01 entry; it was the only route search surfaced to
Canakgoz–Beasley (2009) and Beasley–Meade–Chang (2003), so **both remain named-but-unobtained
secondaries**. Separately, Beasley's own Brunel pages
(`people.brunel.ac.uk/~mastjjb/jeb/{port,track,card,trackmip}.html`) are **abstract-only pages
that link to ScienceDirect and host no PDF** — the 2026-10-13 "author site as an abstract
channel" pattern, now confirmed on a second host.

## Mechanism

This is not a return mechanism. It is the **construction object this folder named as open and
then left open**: the 2026-11-22 enhanced-indexation note recorded that a cardinality cap
"requires binary variables and turns the LP into a MILP, which is where tractability stops being
free", and stopped there. This paper is about exactly that constraint, and it supplies three
things the folder did not have.

**1. What the cardinality constraint does to the frontier — it stops being a frontier.** Write
the long-only mean–variance problem as `min x'Σx s.t. μ'x = ρ, e'x = 1, x ≥ 0`, with optimal
value `φ(ρ)`. Convexity gives two properties the lab uses without noticing: `φ` is increasing and
convex on `[ρ_min, ρ_max]`, and the equality constraint `μ'x = ρ` can be replaced by `μ'x ≥ ρ`
without changing the solution. Add `|supp(x)| ≤ K` and **both properties fail**: the feasible
region is non-convex, `φ_K(ρ)` need not be increasing or convex, and `φ_K(ρ) ≠ φ̃_K(ρ)` (the
inequality-constrained value) at any `ρ` whose point is **not** on the efficient frontier — which
is how you detect the gaps: where the two values differ, there is **no** efficient portfolio at
that return level at all. The paper's operational consequence is sharp and is the part to carry:
**tracing a cardinality-constrained frontier by scalarising — a convex combination of risk and
return — is incorrect**, because the set being optimised over is not convex. Any "sweep the
risk-aversion knob" procedure silently skips the gaps.

**2. Why the constraint is combinatorial at all, and which constraint is to blame.** The
cardinality cap alone is a restriction to the faces of the simplex of dimension at most `K`. What
makes it bite in practice is its companion, the **quantity constraint** (buy-in threshold):
`x_i = 0 or ℓ_i ≤ x_i ≤ u_i`. A *minimum* position size is a disjunction, and it is the
disjunction, not the count, that forbids a convex reformulation.

**3. The economic motive the authors state, which is the lab's motive too**: administering a book
with many very small holdings is undesirable "because of transaction costs, minimum lot sizes,
complexity of management, or policy of the asset management companies". Under protocol v3 the
first of those is literal — drift is charged and each name carries 15–40 bps plus statutory tax.

## Construction recipe

**The reformulation (Section 3).** Fold the return target into the objective with a quadratic
penalty and you get a *Standard Quadratic Program* — a quadratic form over the simplex:

    min  f_M(x) = x'Σx + M·[μ'x − ρ]²     s.t.  x ∈ Δ = {x ≥ 0, e'x = 1}

No binary variables anywhere. Any quadratic `x'Px + 2q'x` coincides on `Δ` with the pure form
`x'Qx` for `Q = P + e q' + q e'`, so linear terms are free. Adding `|supp(x)| ≤ K` means
"minimise `f_M` over the faces of `Δ` of dimension ≤ `K`"; adding `ℓ_i ≤ x_i ≤ u_i` on the support
gives the full Limited Asset Markowitz (LAM) model.

**The operator (Section 4) — this is the transferable piece.** It rests on a structural theorem
(Scozzari–Tardella): if `x*` minimises a quadratic on a polyhedron `P`, there is a **nested
sequence of faces** `F¹ ⊂ F² ⊂ … ⊂ F^k` on which `f` is strictly convex, each with an interior
minimiser, and `x*` is the interior minimiser of the last. Therefore an optimal support of size
`h` **contains** an optimal support of every smaller size along that chain, and supports can be
grown one name at a time:

```
Increasing Set Algorithm
  C¹ ← all singletons {i};  MIN(1) ← min_i q_ii
  for j = 1 … K:
      C^{j+1} ← every element of C^j extended by one admissible asset
      if C^{j+1} is empty:  MIN(h) ← MIN(j) for all h > j;  stop
      MIN(j+1) ← min{ MIN(j),  min_{I ∈ C^{j+1}} w(I) }
  return MIN(K)
```

`w(I) = (e'Q_I^{-1} e)^{-1}` for the unconstrained-face case, and a convex QP of dimension `|I|`
once bounds are present. Four properties matter here:

- **It is exact** as written (by the nested-faces theorem), and **exponential** in the worst case.
- **Truncating the beam makes it polynomial**: at each level keep only a limited number of the
  best-valued supports. Optimality is no longer guaranteed — and *in every real-world instance
  that CPLEX could also solve, the truncated version returned the same solution to numerical
  precision*. That is the paper's strongest practical claim and it is a claim about a **greedy
  beam search over supports**, not about an exact solver.
- **`MIN(j)` is the optimum at cardinality ≤ `j`.** One pass therefore returns the *entire*
  optimal-book-versus-`K` ladder, `K = 1 … K_max`, not a single book. The `K` ladder is free.
- **Pre-assignment is a speed-up, not a cost.** Forcing a named subset `J` into the book starts
  the algorithm at `C^{|J|} = {J}` and *shortens* it. A construction that insists on holding the
  top-scoring names and optimises only the remainder is **cheaper** than one that does not.

**Bounds used in their experiments**: `K ∈ {5, 10}`, `ℓ_i = 0.01`, `u_i = 1`, long-only
throughout, one fixed `ρ` per experiment, no rebalancing inside the hold.

**The linear siblings.** The same cardinality-plus-quantity constraints over mean-absolute
deviation (LAMAD) and CVaR (LACVaR) give mixed-integer *linear* programs. The paper's most
counter-intuitive computational result: CPLEX needed **more** time on those MILPs than the
increasing-set algorithm needed on the MIQP. A linear risk measure is not automatically the
cheaper construction.

## Robustness evidence (qualitative only)

- **Computational breadth is the strong part.** Thirteen instance sets across five markets and up
  to 2,191 names, with the optimal or best-known LAM solutions published for all of them —
  including, in the authors' own words, filling the gap that Beasley's widely-reused data sets had
  no known optima. The method reaches instance sizes where the exact MIQP solver returns nothing
  at all.
- **Return evidence is thin and the paper does not oversell it.** One estimation window, one
  twelve-month hold, five markets, a fixed return target at two risk levels, and the comparison is
  against the unconstrained models and the official index. The authors report the limited-asset
  books doing at least as well as the unconstrained ones, and the books in general doing better
  than the index at the longer horizons examined. **No transaction costs are charged anywhere in
  that evaluation** and no standard error or test is reported, so the evidence is a single draw.
  Read it as "the K-name restriction did not obviously cost anything", not as evidence for it.
- **One mechanism-level observation inside the return section that is worth more than the
  comparison itself**: at the low-risk target the asset limitation changed composition materially
  for all three risk measures, while at the higher target it mattered much less for the *linear*
  models and still mattered for mean–variance — the authors attribute this to mean–variance
  producing a more diversified book than MAD or CVaR at the same target. The risk measure, not
  only the cardinality cap, decides how concentrated the unconstrained optimum already was.
- **No replication status.** This is a method paper in an OR venue; it is not in the scope of
  Hou–Xue–Zhang or Jensen–Kelly–Pedersen, and no independent replication was located. The
  *algorithm* is deterministic arithmetic and cannot decay; the one-window return comparison has
  no replication standing at all.

## Implementability here

**Why this object is admissible at all, against the `#507` audit.** The thirty-five filed-or-
refused named objects of `program.md` are signals and risk measures. This is neither: it is the
**selection operator** that turns a score into a held set, and the audit's own conclusion was that
the remaining room is in the construction clauses. The lab has run a cardinality-`K` long-only
book in every trial it has ever scored — *top-`K` of a sorted score* is `|supp(x)| ≤ K` chosen by
rank — and has never once asked what the optimal `K`-subset looks like. That is the gap.

**The binding constraint is the lab's clock, and the arithmetic is unforgiving.** `generate_weights`
is called about seven times per trial and must stay near 60 s per call. A monthly book over the
lab's visible window is roughly 320 rebalance dates, so the per-rebalance budget is of order
**0.2 s**. The paper's own runtimes for 500 return values on a 2,151-name instance run to tens of
thousands of seconds. **Any exact or beam-search cardinality solve over the full ~1,000-name
eligible panel is out of reach by three or four orders of magnitude**, and a candidate that tries
it will time out rather than fail honestly. Three affordable adaptations survive:

1. **Screen first, optimise small.** Pre-screen the eligible panel to 30–60 names by the score the
   lab already computes (cheap, one argsort), then run the increasing-set beam on that subset with
   `K` of order 10–25 and a beam of a few hundred. At `n = 50` the paper's own runtimes are
   seconds-to-sub-second territory. This is precisely the shape of `#513`'s
   filter-then-deconcentrate, with the deconcentration step replaced by an operator with a
   stated optimality property instead of a rule of thumb.
2. **Take the `K` ladder, since it is free.** One pass returns the optimum at every `K ≤ K_max`.
   The lab's standing open question of *how many names a long-only book should hold* has been
   answered so far only by varying `K` across whole trials, which spends the trial count. Inside
   one candidate the ladder costs nothing extra — though note that **choosing `K` by looking at
   the ladder's in-sample values is in-sample objective maximisation**, which is the failure mode
   the deflated-Sharpe gate exists to punish (the same objection
   `2026-08-20-parametric-portfolio-policies.md` raises against fitting `θ`). `K` must be fixed by
   a rule stated before the run, or walk-forward.
3. **Use pre-assignment deliberately.** Forcing the top-scoring names in and optimising only the
   remaining slots is *faster* than free selection and is the natural way to keep the score in
   charge of the book while letting the covariance decide the tail of it.

**What does not transfer.**

- **`μ` is required.** Both the LAM objective and the return target need expected returns, and
  this folder's accumulated position is that estimated means are the expensive input. The
  **cardinality-constrained minimum-variance** variant — drop `μ'x = ρ`, keep `|supp| ≤ K` — needs
  no mean at all, and is the honest first version to write; but it is a **de-risking construction**,
  which the standing exclusions bar, so it belongs in the note and not in a candidate.
- **The quantity constraint is backwards for this lab.** Their binding side is a *minimum*
  position (`ℓ_i = 0.01`); v3's is a *maximum* (25% cap). Dropping `ℓ` removes the disjunction and
  makes the problem strictly easier — which is also why the runtime tables here are a pessimistic
  bound on what the lab would pay, not an optimistic one.
- **Costs are absent from their evaluation.** v3 charges 15–40 bps per side plus UK/HK/FR/IT/ES
  statutory taxes and charges drift between rebalance rows. A `K`-name optimised book re-solved at
  each month-end can churn its whole support when the covariance estimate moves, and the frontier
  gaps documented above are exactly the mechanism by which a small change in target jumps the
  composition. **Turnover is derivable from the construction but is not reported by the source**,
  so any candidate must measure it, and the paper's silence on costs is the reason this is tier B.
- **Weekly returns, not daily.** Their covariance inputs are weekly; the lab's are daily. Nothing
  in the algorithm cares, but the estimation-error profile differs.

**The OR-Library data sets are not usable here.** `indtrack1–8` are external market data; fetching
them is barred by the lab's own rules (`research/README.md` §5, and `CLAUDE.md`'s no-download rule).
They are noted only because their index coverage — Hang Seng, DAX, FTSE 100, Nikkei, S&P 500 —
overlaps this panel's own markets, so the published optima are a *qualitative* sanity reference for
anyone who wonders whether `K = 10` books on such indices are even solvable. They are not a data
source.

## Related

- `2026-11-22-enhanced-indexation-as-a-benchmark-relative-linear-program.md` — named this exact gap
  ("a cardinality cap … is where tractability stops being free") and shares the OR-Library instance
  family. This note fills it.
- `2026-11-27-sparse-portfolio-selection-at-index-scale-ridge-and-outer-approximation.md` — the same
  object solved to certified optimality at index scale, and a relaxation-then-rank support rule that
  is far cheaper than the beam search here.
- `2026-11-27-cardinality-as-an-objective-and-the-cost-fragility-of-the-sparse-frontier.md` — the
  same `K` ladder obtained as a Pareto front rather than a constraint sweep, and the one source in
  tonight's cluster that charges transaction costs and reports what they do.
- `2026-08-22-long-only-as-l1-regularization.md` and the Brodie et al. ℓ1 construction it records —
  the *continuous* route to sparsity. The difference is control: an ℓ1 penalty produces a support as
  a by-product of a tuning parameter; a cardinality constraint names `K` directly.
- `2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` (`#513`) — the live
  `portfolio-learning` construction this operator is a drop-in for.
- `2026-08-20-parametric-portfolio-policies.md` — the standing warning against fitting a
  construction parameter to in-sample utility, which applies to choosing `K` off the ladder.
