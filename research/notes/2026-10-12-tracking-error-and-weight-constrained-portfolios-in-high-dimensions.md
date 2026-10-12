---
title: "Portfolio Analysis in High Dimensions with TE and Weight Constraints" (the CROWN method)
authors: Caner, Fan
year: 2024 (first posted); version read dated October 2025
venue: arXiv working paper, q-fin.PM (venue tier 2 at best — unpublished preprint; the version read acknowledges a co-editor and two referees, so it is under review somewhere, which is not a venue)
url: https://arxiv.org/abs/2402.17523 · read as https://arxiv.org/pdf/2402.17523 (v2) · https://doi.org/10.48550/arXiv.2402.17523
citations: 0 (OpenAlex, checked 2026-10-12). Crossref holds no record for the arXiv DOI; Semantic Scholar returned HTTP 429 and OpenAlex's free daily budget was exhausted after this one call, so no second index was reachable tonight
sample_period: theory plus simulations (synthetic, e.g. p = 80/160/320 with p/T = 0.8 and 2.0). The empirical section uses monthly S&P 500 component returns against three S&P indices; **its window was deliberately not looked up and the section was not read**, because a 2025-vintage empirical sample would breach this folder's post-2023 ban
markets: US large-cap equity in the unread empirical section; the theory is market-agnostic
tier: C — an uncited preprint by this folder's rubric, however competent. It is noted anyway because its content is a *limit theorem and an explicit impossibility*, not a performance claim: what it says cannot be inflated by a lucky sample, and the part the lab needs is the part the authors concede
validation_overlap: true (assumed, not verified — the empirical section was left unread; discount accordingly, though nothing numeric from it enters this note)
published_post_2018: true
---

## Access

Read first-hand from arXiv (v2). The `( )` math-dropout check returned zero hits; the
extract was not ASCII-shifted. **Sections 6 (simulations, in part) and 7 (empirics) were
deliberately skipped**: this note takes only the problem statements, the closed forms, the
theorems' conditions and the authors' own statement of what the method cannot do.
Bajeux-Besnainou, Belhaj, Maillard and Portait (2011, *Journal of Financial Research* 34(2),
295–330, DOI `10.1111/j.1475-6803.2011.01292.x`, 13 Crossref citations checked 2026-10-12),
the paper that first wrote down the TE-plus-weight-constrained weight formula, is **closed and
was not read**: OpenAlex reports `oa_status: closed` with no repository copy, and SSRN refuses
an automated client (Cloudflare 403, and the `autopapers.ssrn.com` host OpenAlex names as the
green location failed at the transport layer with a 502 CONNECT). Everything attributed to it
below is attributed *as Caner–Fan describe it*, and nothing is claimed from its own words.

## Mechanism

Not a return mechanism. This is the **constrained** sequel to
`notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md`: the same
factor-plus-nodewise machinery (named CROWN here — Constrained Residual Nodewise Optimal
Weight Regression), applied to the three problems a benchmarked manager actually faces, with
`p` allowed to exceed `T`. Three things in it matter to a lab whose grading statistic just
became benchmark-relative.

**1. The tracking-error-constrained optimum has a closed form, and the active part of it does
not depend on the benchmark.** Maximising `µ'w_d − (Ξ/2)w_d'Σ w_d` over active weights `w_d`
(the deviation from benchmark holdings `m`) subject to the budget `1'w_d = 0` gives

    w*_d = κ · ( Θµ / 1'Θµ  −  Θ1 / 1'Θ1 ),        w* = m + w*_d,

i.e. the optimal **active overlay is a scalar multiple of (tangency portfolio − global
minimum-variance portfolio)**, with `κ` a risk-tolerance scalar the investor supplies rather
than estimates. The benchmark enters only as the anchor `m`. This is the estimation-side
twin of the geometry result already in the folder
(`notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md`): there, the
attainable active-return-per-unit-tracking-error ceiling `√d` was benchmark-independent; here,
the *direction* of the optimal tilt is benchmark-independent too. Only its size is a choice.

**2. Constraints do not change the hard part.** Caner–Fan prove the same convergence rate —
`O_p(s̄ l_T K^{3/2})` for weights in `ℓ₁`, and a slower `O_p(s̄ l_T K⁴)` for portfolio variance,
tracking error and squared Sharpe ratio — for the TE-only problem, the TE-plus-equality-weight
problem and the TE-plus-inequality-weight problem alike. Their explanation is that every rate
is driven by estimating the unconstrained maximum-Sharpe weights `Θµ/1'Θµ`; the constraints
ride along for free. Two side-results fall out of this. The benchmark-relative problem can be
*easier* in finite samples than the unconstrained one, because the benchmark's own weights are
given rather than estimated (their Remark 6), while asymptotically the two are the same. And
whether a weight constraint binds can be decided **from the data**: the inequality constraint
`1'_R w_d ≤ ω` binds exactly when `κŵ_u > ω`, so the estimator switches between the TE-only
and the jointly-constrained solution by an estimated indicator, and stays consistent either
way (their Theorem 3). That binding test is the piece they claim as new relative to
Bajeux-Besnainou et al.

**3. The `p > T` guarantee rests on an assumption that is easy to miss, and the long-only
constraint is not covered at all.** Consistency with more assets than observations is proved
under a **diverging** maximum Sharpe ratio (`µ'Θµ → ∞` as `p` grows) — a technical device
inherited from Caner et al. (2023). Their Appendix B shows that if one instead assumes a
*bounded* maximum Sharpe ratio, which is the economically modest assumption, consistency is
recovered only for `p < T`. And on short selling the authors are explicit: a no-short
constraint `w_j ≥ 0` is a floor on each weight, their method handles it in exactly two
sub-cases — a floor on **one** asset, or a joint floor on the **summed** weight of a group of
assets — and it "cannot cover a short sales constraint for each asset in a portfolio."

That last sentence is the most valuable line in the paper for this lab, and it generalises:
when this literature says "weight constraints" it means a small number of **linear group
budgets** (a sector cap, a country floor, a prospectus limit), not `p` simultaneous
non-negativity constraints. The long-only version of the tracking-error problem at this
panel's width is, on the evidence of the most recent paper in the vein, **an open problem**.

## Construction recipe

1. Estimate `Θ̂` by the factor-model-plus-residual-nodewise route of the companion note
   (observed factors, OLS loadings, Lasso nodewise on residuals, Woodbury reassembly).
2. Fix `κ` (risk tolerance) and the benchmark weights `m`. `κ` can be mapped to a
   tracking-error budget analytically (their Appendix A.3) or estimated consistently
   (their Appendix B.3) — but it is an input, not something to scan.
3. Unconstrained-in-weights case: `ŵ = m + κ(Θ̂µ̂/1'Θ̂µ̂ − Θ̂1/1'Θ̂1)`.
4. Group-constrained case: pick the restricted index set `R` and the group budget `ω`
   (expressed as a deviation from the benchmark's own weight on that group), test
   `κŵ_u > ω` on the data, and use the jointly-constrained solution when it binds and the
   TE-only solution when it does not.
5. Report tracking error as `√(ŵ_d'Σ̂ŵ_d)`, and remember that variance and Sharpe converge
   more slowly than the weights do — an apparently well-estimated book can still have a
   badly estimated Sharpe ratio.

## Robustness evidence (qualitative only)

- **Proof-based, not sample-based.** The content is theorems with stated conditions:
  stationary weakly dependent returns, an approximate factor model with observed factors
  growing more slowly than `T`, sparsity of the **residual** precision matrix, and either a
  diverging maximum Sharpe ratio (for `p > T`) or `p < T` (for a bounded one).
- **No replication, no citations yet** (0 in OpenAlex tonight). By the rubric this is Tier C
  and may not be leaned on for any magnitude. Its negative statements are the durable part.
- **Simulation design is honest about the hard regime** — they simulate `p/T = 2` as well as
  `p/T = 0.8`, and compare against POET, nonlinear shrinkage and single-factor shrinkage
  rather than only against a naive baseline. The empirical section reports turnover,
  maximum/minimum weights and total short exposure, and a Sharpe-ratio test p-value, which is
  the right furniture; it was not read here.
- **Lineage check.** The paper's own account of its relation to Caner et al. (2023) is that
  the earlier paper's out-of-sample maximum-Sharpe consistency needed `p < T` because its
  proof went through the largest eigenvalue of `Σ`, which diverges at rate `p`; this one
  replaces that step with a sup-norm bound that grows more slowly. That is a real technical
  improvement and also a reminder that both results are statements about proof technique, not
  about markets.

## Implementability here

- **The headline is a closure, not a candidate.** If the lab wanted to build its active book
  by estimating the tracking-error-optimal overlay on the eligible panel, there is no theory
  covering it: the one method that handles `p > T` with constraints concedes it cannot impose
  non-negativity name by name, and the lab's hard constraint is exactly that (long-only, max
  25% per name, gross ≤ 1). Truncating a signed optimum at zero and renormalising is a
  different estimator with no guarantees attached — permissible as a heuristic, but it must be
  declared as such and not justified by this literature.
- **What *is* usable, and cheaply.** The group-budget form is a genuine fit for this panel:
  "the eligible book may deviate from the pool's weight on a region (or on the ETF sleeve) by
  at most `ω`" is precisely `1'_R w_d ≤ ω`, and the binding test is a two-line computation
  once `Θ̂` exists. A region-budget overlay on top of the equal-weight pool is the version of
  this idea the lab could actually submit.
- **The direction result argues against scanning.** Since the optimal active direction is
  `(tangency − GMV)` and only `κ` is free, a candidate in this vein has exactly one knob, and
  the deflator charges for knobs. Pre-register `κ` (or the tracking-error budget it implies)
  before the run.
- **Use the pool as the anchor `m`, because v3 already does.** The engine grades against the
  equal-weight eligible pool, so `m` = pool weights is the one anchor for which the measured
  statistic and the construction agree. This does *not* make an anchored book a good idea —
  see the tension below — it only means that if one is built, the anchor is not a free
  parameter.
- **Cost model mismatch.** Nothing in this literature charges per-name liquidity tiers,
  transaction taxes, or the cost of undoing drift. A `(tangency − GMV)` overlay re-estimated
  monthly on ~1,000 names is a high-turnover object by construction; under v3's cost model
  that is where it would die, and the paper's turnover figures say nothing about it.
- **Runtime.** Same gate as the companion note: `p` Lasso fits per rebalance is not feasible
  at `p ≈ 1,000` inside the protocol's time budget. Sleeves or fewer rebalance dates.

**Tension to record, not to resolve.** This paper's whole frame is that the manager's problem
is *constrained by a tracking-error budget*, while this folder's own reading of the lab's new
objective (`#234`, `#238`) is that **nothing** rewards proximity to the pool under a Sharpe
*difference* statistic, and that a minimum-tracking-error or enhanced-index book is dominated.
Both can be true: the closed form above is the solution to a problem the lab does not have.
What transfers is the algebra and the impossibility statement; what does not transfer is the
motivation.

## Related

- `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md` — the
  unconstrained parent, and the source of every rate condition quoted here.
- `notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md` — the geometry
  of the same problem without estimation error; the `√d` ceiling and `δ_B` efficiency loss.
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` — the rival
  response to a panel too wide to estimate on: mix with the naive rule rather than estimate
  the optimum.
- `notes/2026-10-12-black-litterman-benchmark-anchored-tilting.md` — the practitioner answer
  to the same anchoring problem, with a confidence knob instead of a tracking-error budget.
- `research/SUMMARY.md`, candidate ideas #234 and #238 — the standing reasons not to build a
  benchmark-hugging book here.
