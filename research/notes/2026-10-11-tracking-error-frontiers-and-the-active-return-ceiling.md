---
title: "Portfolio frontiers with restrictions to tracking error volatility and value at risk" (read as the Università Politecnica delle Marche working paper), carrying the geometry of Roll (1992) "A Mean/Variance Analysis of Tracking Error" and Jorion (2003) "Portfolio Optimization with Tracking-Error Constraints"
authors: Palomba, Riccetti (2012); the geometry restated is Roll (1992) and Jorion (2003)
year: 2012 (working paper 2011); Roll 1992; Jorion 2003
venue: Journal of Banking & Finance 36(9), 2604–2615 (venue tier 1, peer-reviewed; read as Quaderni di Ricerca n. 358, Dipartimento di Economia, Università Politecnica delle Marche, June 2011). Origins: Journal of Portfolio Management 18(4), 13–22 (tier 1 practitioner-academic) and Financial Analysts Journal 59(5), 70–82 (tier 1 practitioner-academic)
url: https://doi.org/10.1016/j.jbankfin.2012.05.014 · working paper read at https://docs.dises.univpm.it/web/quaderni/pdf/358.pdf · https://doi.org/10.3905/jpm.1992.701922 · https://doi.org/10.2469/faj.v59.n5.2565
citations: Palomba–Riccetti 13 (Crossref is-referenced-by, checked 2026-10-11), 22 (OpenAlex, checked 2026-10-11). Roll (1992) 561 (Crossref), 767 (OpenAlex), 758 (Semantic Scholar) — all checked 2026-10-11. Jorion (2003) 204 (Crossref), 250 (OpenAlex), checked 2026-10-11
sample_period: theory. The illustrative numerical example uses quarterly returns of DJ Eurostoxx 50 constituents, 2003Q1–2010Q4, grouped into ten asset classes
markets: theory, market-agnostic; the example is European large-cap equity with DJ Eurostoxx 50 and S&P 500 as the two benchmarks
tier: B — the geometry is Tier A by origin (two heavily cited tier-1 venues) and is algebra rather than an empirical claim, but the paper read here is a modestly cited single-author-pair contribution whose own sample is one illustrative example, costs are absent, and **short sales are allowed throughout**
validation_overlap: false
published_post_2018: false
---

## Access

**Both primaries are closed and neither was read first-hand.** Roll (1992) sits in the
*Journal of Portfolio Management*, whose publisher `pm-research.com` refuses an automated
client by redirecting into an OpenID flow (recorded in `research/README.md`, 2026-09-08);
OpenAlex and Semantic Scholar both report `oa_status: closed` with no repository copy.
Jorion (2003) sits in the *Financial Analysts Journal*; `rpc.cfainstitute.org` serves the
abstract page with no PDF endpoint, OpenAlex reports `closed`, and Jorion's current faculty
page (`faculty.sites.uci.edu/pjorion/publications/`) hosts only a résumé — the older
`merage.uci.edu/~jorion/` tree is 404, confirming the 2026-09-30 finding that it is gone.

What *is* readable is the Università Politecnica delle Marche working-paper version of
Palomba–Riccetti (2012), which **restates both results formally, with the equations, as its
section 2** before extending them. Every formula below is quoted from that paper. The
attribution convention in this note: results labelled *Roll* and *Jorion* are theirs as
reported by a peer-reviewed third party, not as read in their own words, and the extensions
(joint TEV–VaR frontiers) are Palomba–Riccetti's own. Access mechanics worth keeping: the
OpenAlex `locations` list named `docs.dises.univpm.it/web/quaderni/pdf/358.pdf` (fetch over
`https`, the listed `http` URL is refused by the proxy); `pdftotext -layout` gave 87 KB with
**zero `( )` dropout hits**, so the formula-bearing sections are intact.

## Mechanism

This is not a return mechanism. It is the **geometry of the objective the lab switched to on
2026-10-08**, and it exists because minimising risk *relative to a benchmark* is a different
optimisation from minimising risk, with a different solution.

Set notation as the paper does: `n` assets, mean vector `µ`, covariance `Ω`, and the three
data-only constants `a = ι'Ω⁻¹ι`, `b = ι'Ω⁻¹µ`, `c = µ'Ω⁻¹µ`, with `d = c − b²/a`. The
minimum-variance portfolio `C` has `µ_C = b/a`, `σ²_C = 1/a`. A benchmark `B ≡ (σ²_B, µ_B)`
is given, and two derived distances carry everything: `∆₁ = µ_B − µ_C` (how much more the
benchmark returns than the minimum-variance portfolio) and `∆₂ = σ²_B − σ²_C` (how much more
variance it carries).

**1. The mean-variance frontier.** `σ²_P = σ²_C + (µ_P − µ_C)²/d` — a parabola in
`(σ²_P, µ_P)` space, `√d` the slope of its asymptote in `(σ_P, µ_P)` space.

**2. Roll's mean-TEV frontier (MTF)** — the set of portfolios with the *smallest tracking
error* for each level of expected return:

```
σ²_P = σ²_B + (µ_P − µ_B)²/d + 2(∆₁/d)(µ_P − µ_B)
```

which is the *same curve horizontally translated*. Two consequences fall straight out and
they are the reason this note exists. The MTF's own minimum sits at `(σ²_B − ∆₁²/d, µ_C)` —
i.e. a TEV-minimising book's least-variance point is still at the minimum-variance
portfolio's *return*, but at a higher *variance*. And subtracting (1) from (2) gives the
horizontal gap between the two frontiers:

```
δ_B = ∆₂ − ∆₁²/d                     (the efficiency loss)
```

**`δ_B` does not depend on `µ_P`.** The penalty for optimising against a benchmark instead of
in absolute terms is a *constant* excess variance, set entirely by where the benchmark sits
relative to the minimum-variance portfolio — not by how aggressive the active book is, not by
how much tracking error it takes. It is zero only if the benchmark itself lies on the
mean-variance frontier. This is Roll's result that benchmark-relative optimisation is
"generally overly risky": every point on the MTF lies to the right of the MVF by the same
`δ_B`. His own suggested remedy is to constrain the portfolio's **beta** against the
benchmark.

**3. Jorion's constrained-TEV frontier (CTF)** — impose `TEV = T₀` (a variance budget) on the
Markowitz problem and the feasible set becomes a closed, bounded **ellipse** in
`(σ²_P, µ_P)`:

```
d(σ²_P − σ²_B − T₀)² + 4∆₂(µ_P − µ_B)² − 4∆₁(σ²_P − σ²_B − T₀)(µ_P − µ_B) − 4dδ_B T₀ = 0
```

centred horizontally at `σ²_B + T₀`, with its axis sloping up when `∆₁ > 0` and down when
`∆₁ < 0`, and its area growing with `T₀`. Three readings of this ellipse matter more than the
equation:

- **Whether it touches the efficient frontier at all** is decided by
  `Ψ = dT₀ − d∆₂ + ∆₁²`. `Ψ < 0`: no intersection — *no portfolio inside the tracking-error
  budget is mean-variance efficient*. `Ψ = 0`: tangency, at a budget exactly equal to the
  efficiency loss, `T_H = δ_B`. `Ψ > 0`: two intersections, and the ellipse's **left arc
  coincides with the mean-variance frontier** while the right arc is the merely
  TEV-constrained one. So the TEV budget has a threshold, and it is the efficiency loss:
  below `δ_B` there is nothing efficient to buy.
- **The ceiling on active return.** The ellipse's extreme-return points are
  `J₁ = (σ²_B + T₀ + 2∆₁√(T₀/d), µ_B + √(dT₀))` and its mirror
  `J₂ = (σ²_B + T₀ − 2∆₁√(T₀/d), µ_B − √(dT₀))`. Read `J₁` as a rate:
  **`(µ₁ − µ_B)/√T₀ = √d`.** The maximum ex-ante active return per unit of tracking error is
  `√d` — the asymptotic slope of the universe's own mean-variance frontier — and it does
  **not depend on which benchmark was chosen**. The benchmark decides the efficiency loss;
  the opportunity set decides the information-ratio ceiling.
- **The trade-off is explicit in both directions.** On the joint TEV–VaR boundary the paper
  constructs, for a fixed expected return a manager can *lower relative risk by raising
  absolute risk, or lower absolute risk by raising relative risk* — which is Roll's point
  restated as a menu, and the paper names the principal-agent problem this creates.

Jorion's own remedy, as reported here: a TEV constraint alone ignores total risk, so add a
**total-volatility constraint** alongside it.

## Construction recipe

Not a signal, a sizing discipline. What is implementable from the algebra:

1. **Compute `d` for the opportunity set** (`d = c − b²/a` from `µ`, `Ω` on the eligible
   panel) and read `√d` as the ceiling on active return per unit of tracking error. Any
   candidate claiming more is claiming an estimate of `µ` and `Ω` the data does not support.
2. **Compute `δ_B = ∆₂ − ∆₁²/d` for the benchmark actually used.** It is the standing variance
   penalty of a benchmark-relative mandate and the minimum TEV budget at which anything
   efficient becomes reachable (`T_H = δ_B`).
3. **Never minimise tracking error as the objective.** The MTF is the wrong curve: it is the
   MVF shifted right by `δ_B` for every return level. If a book is to be anchored near the
   benchmark, anchor it with a *constraint* (`TEV ≤ T₀`) and optimise total risk-return
   inside the ellipse, which is Jorion's construction; the efficient part of the feasible set
   is the **left arc** between `J₁` and `J₂`.
4. **If a TEV constraint is kept, add a total-volatility cap** (Jorion) or a beta constraint
   against the benchmark (Roll). Either one re-attaches the objective to absolute risk.
5. Diagnostics to carry with any benchmark-relative result: realised TEV, the implied
   information ratio against `√d`, and the book's beta against the benchmark.

## Robustness evidence (qualitative only)

- The content is **algebra under the standard Markowitz assumptions** (quadratic utility /
  normal returns, one period, known moments), not an empirical regularity, so "robustness"
  means the assumptions, not sub-periods. No replication question arises for the identities;
  the two threats are estimation error in `µ, Ω` (which is the subject of the companion note
  on combining with the naive rule) and the constraint set.
- The origins are heavily cited in two tier-1 practitioner-academic venues and the result is
  standard textbook material in the active-management literature; the paper read here is one
  of several that extend it (it names El-Hassan–Kofman 2003 for the no-short-sales case,
  Alexander–Baptista 2008/2010 for VaR and ex-ante-alpha frontiers, and Riccetti 2010 for
  commissions).
- **Known gaps, all of which bite here.** *(i)* **Short sales are allowed throughout**, and
  the paper's own closing sentence names "disallowing short sales" as the natural extension —
  so every statement above describes a *superset* of what a long-only book can reach. *(ii)*
  **No transaction costs**, and the frontier geometry says nothing about turnover. *(iii)* The
  moments are treated as known; nothing here is a finite-sample result. *(iv)* The empirical
  section is one illustrative allocation, not evidence.

## Implementability here

This folder has covered how to build a score, how to weight it, how to grade it and what the
sample does to it. It had not, in 177 notes, covered **what changes when the objective itself
is defined relative to a specific portfolio** — which is what protocol v3 did on 2026-10-08
by deflating *skill* (validation Sharpe minus the equal-weight eligible pool's on the same
days) instead of Sharpe. Four concrete consequences, carefully separated from what the source
actually proves:

1. **v3's statistic is a Sharpe difference, not the TEV-constrained active-return objective —
   and that is a good thing by Roll's own argument.** A Sharpe difference rewards *total*
   risk-adjusted return; Roll's pathology is precisely what happens when you reward active
   return at minimum relative risk. So a candidate that tries to beat the pool by hugging it
   and tilting is optimising the wrong curve: the lab's statistic does not pay for a small
   tracking error, it pays for the total Sharpe, and the right target inside Jorion's ellipse
   is the **left arc that coincides with the mean-variance frontier**, not the maximum-active-
   return vertex `J₁`.
2. **The information-ratio ceiling `√d` is a sanity check the lab can run for free, and it is
   the honest frame for "the 90% skill interval is ±0.33".** Skill is a Sharpe difference
   rather than an information ratio, so `√d` is not a bound on it — but the two are tied
   through the same opportunity set, and an estimate of `√d` on the eligible panel (train
   only) says how much active return a given tracking error can possibly buy before costs.
   Compute it from the sample moments of the eligible panel; expect the estimate to be
   wildly optimistic (that is the standing message of the folder's estimation-error notes),
   which makes the comparison conservative in the useful direction.
3. **`δ_B` makes "the pool is hard to beat" a measurable statement rather than a mood.** The
   efficiency loss of the *pool as benchmark* is `∆₂ − ∆₁²/d`: it is large exactly when the
   equal-weight pool sits far from the panel's minimum-variance portfolio in variance terms
   without being paid for it in return terms. This is pure accounting on the train split, it
   needs no candidate, and it composes with the open engine questions about what the pool is
   obliged to do — if `δ_B` is small, the pool is nearly efficient and there is little room
   for *any* benchmark-relative construction; if it is large, the room exists and the question
   becomes whether a long-only book can reach it.
4. **The long-only correction is not in this source and must not be smuggled in.** Every
   number above is computed on an unconstrained (short-selling) opportunity set, so `√d` and
   the shape of the ellipse are *upper bounds* on the long-only case. The folder's existing
   transfer-coefficient material already prices long-only at a linear 0.3–0.8 haircut on the
   information ratio under realistic constraints; the honest composition is "ceiling `√d`,
   times something well below one". Do not quote `√d` as an attainable number for this lab.

Pitfalls: *(a)* `T₀` is a **variance**, not a volatility, throughout — `TEV = T₀` enters the
ellipse as `σ²_P − σ²_B − T₀`; getting that wrong squares the budget. *(b)* `∆₁ < 0`
(benchmark returns less than the minimum-variance portfolio) flips the ellipse's axis slope
and is a perfectly normal case in-sample. *(c)* All of this is single-period and
cost-free — v3 charges per-name costs and charges the trades that undo drift, so the feasible
set the lab actually faces is smaller again, in a way the no-trade-band material in this
folder describes and this source does not.

## Related

- `notes/2026-10-08-benchmark-portfolios-have-alpha-of-their-own.md` — what the benchmark
  itself is; this note is what its *being* the benchmark does to the optimum.
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` — the
  finite-sample half of the same question: given estimation error, how much of the active
  rule to hold against the naive benchmark. Tu–Zhou's footnote makes the bridge explicit:
  benchmark-relative mandates are handled by treating the benchmark's return in the role of
  the riskless rate.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the transfer coefficient:
  the long-only haircut this source does not price.
- `notes/2026-08-17-naive-vs-optimized-weighting.md`,
  `notes/2026-09-30-shrinking-portfolio-weights-toward-a-target.md` — `1/N` as a shrinkage
  target; here it is the thing being *measured against* instead.
- `notes/2026-10-08-no-trade-bands-under-proportional-costs.md` — the cost geometry this
  frontier analysis omits entirely.
