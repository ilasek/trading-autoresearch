---
title: "Approximate stochastic dominance over a benchmark — the cumulative rule collapses to 'minimise expected shortfall below the benchmark', an LP in n+T variables; and exact dominance is ruled out by no-arbitrage"
authors: Bruni, Cesarone, Scozzari, Tardella
year: 2017
venue: "European Journal of Operational Research 259(1), 322–329 — peer-reviewed, top operations-research journal. Not one of the tier-1 finance names in this folder's rubric; graded tier 2 on venue."
url: https://doi.org/10.1016/j.ejor.2016.10.006
citations: 88 (OpenAlex `cited_by_count`, checked 2026-11-22); 75 (Crossref `is-referenced-by-count`, checked 2026-11-22)
sample_period: "weekly returns computed from daily prices. DJIA 1990-02 to 2016-04; FTSE 100 2002-07 to 2016-04; NASDAQ 100 and S&P 500 2004-11 to 2016-04; Fama–French 49 industry portfolios 1969-07 to 2015-07. **Ends before 2018 on every dataset.**"
markets: "four national-index constituent sets — DJIA (28 names), NASDAQ 100 (82), FTSE 100 (83), S&P 500 (442) — from Datastream, plus the 49 Fama–French industry portfolios. Stocks required to have at least ten years of observations."
tier: "B. Peer-reviewed, the model is proved and stated completely, the datasets are published for reuse, five of the six competing models are independent third-party formulations, and the sample is multi-decade and multi-market. Held below A for: no transaction costs charged (turnover reported only), no multiple-testing treatment, and the ten-year-history filter is a survivorship screen the authors do not discuss."
validation_overlap: false
published_post_2018: false
read: "Full text of the author preprint (322 KB PDF → 53 KB of text via `pdftotext -layout`, 244 instances of `\" the \"`, no character shift, `( )` dropout check zero), served first-try at HTTP 200 by Sapienza's IRIS repository at `iris.uniroma1.it/bitstream/11573/1091776/6/Bruni_preprint_exact%20-approximate-stochastic_2017.pdf`. Sections 1–5 and the reference list intact; the numeric result tables extract but are not quoted here."
---

## Access

**The co-author-institution procedure recorded on [2026-10-04] worked exactly as written, and
OpenAlex's `locations[]` list was again the key rather than a guessed hostname.** ScienceDirect
holds the article closed; OpenAlex listed **`iris.uniroma1.it`** (Sapienza's IRIS instance) as an
OA location with a direct `bitstream` PDF URL, and that URL returned the author preprint on the
first request. `iris.uniroma1.it` is nominated as a working channel; IRIS is the standard Italian
university repository platform, so the same route should reach the large Italian OR-and-finance
literature that is otherwise Elsevier-closed.

One method note that cost a call and is worth recording: **four guessed Elsevier DOIs for this
paper and its siblings all failed**, as the [2026-10-07] entry warns. The DOI was recovered from
**Crossref's `query.bibliographic` endpoint** with the full author list and title, which returned
it first with its citation count attached — that is the cheap, reliable route and should be the
default rather than DOI-pattern guessing.

## Mechanism

**No return-predicting mechanism; this is a construction source, and its contribution is a
reduction.** The subject is enhanced indexation stated as a *dominance* problem rather than a
mean-risk problem: find a long-only portfolio whose return distribution stochastically dominates
the benchmark's.

Three obstacles make exact dominance useless in practice, and the paper is unusually clear about
all three:

1. **Exact stochastic dominance frequently fails to order two distributions at all** — so the
   constraint set is often empty and the criterion yields no portfolio.
2. **The lowest-order exact relation conflicts with no-arbitrage.** Zero-order stochastic
   dominance of the portfolio over the benchmark means `δ_t(x) = R_t(x) − r_t^I ≥ 0` for *every*
   period: a book that never trails the benchmark. That is an arbitrage, so it cannot exist in a
   market without one. **This is the load-bearing idea in the paper for this lab's purposes** — it
   converts "my construction beat the benchmark in every in-sample period" from a strong result
   into a *diagnosis of fitting*.
3. **The SSD formulations in the literature are too large to solve** on real universes.

The fix is to relax dominance by a tolerance `ε` and then *minimise the tolerance*: instead of
asking for a portfolio that never underperforms, ask for the one whose worst admissible
underperformance is smallest. The authors define **Cumulative Zero-order ε-Stochastic Dominance
(CZεSD)**: the portfolio is preferred to the benchmark if, for *every subset* `S` of the in-sample
periods, `Σ_{t∈S} δ_t(x) ≥ −ε`. Bounding every subset's cumulative shortfall, not merely every
single period's, is what makes the rule stronger than the per-period relaxation — a book can have
small individual shortfalls that accumulate into a large one, and the per-period rule does not see
that.

**The reduction, which is the result.** Because
`min_{S⊆T} Σ_{t∈S} δ_t(x) = Σ_{t∈T} min{0, δ_t(x)} = −Σ_{t∈T} max{0, −δ_t(x)}`, the exponentially
constrained problem is *identical* to minimising the **expected shortfall of the portfolio below
the benchmark**. The economically meaningful quantity and the combinatorially defined one are the
same object. The authors also prove the rule implies the earlier Lizyayev–Ruszczyński approximate-SSD
rule, so it sits at the strong end of the approximate-dominance family rather than being another
incomparable variant.

## Construction recipe

Notation: `n` assets, `m = |T|` in-sample periods, asset returns `r_it`, benchmark return `r_t^I`,
weights `x`, portfolio return `R_t(x) = Σ_i x_i r_it`, excess return `δ_t(x) = R_t(x) − r_t^I`.

**The model, in its final form.** With one auxiliary variable `y_t` per period:

    min_{x, y}   Σ_{t∈T} y_t
    s.t.         y_t + δ_t(x) ≥ 0        for all t ∈ T
                 Σ_i x_i = 1
                 x ∈ C                   (any further linear constraints)
                 x ≥ 0,  y ≥ 0

That is the whole thing: **n + m variables and m + 1 constraints** beyond `C`. At the optimum
`y_t = max{0, −δ_t(x)}`, so the objective is the total (equivalently, mean) shortfall of the book
below the benchmark. It is a linear program; it needs no tail-probability parameter, no
risk-aversion parameter, and no tolerance to be chosen in advance — `ε` is an *output*.

**What goes in `C`.** The paper names an expected-return floor as the typical example. Weight caps,
group caps and turnover penalties are all linear and belong here.

**Evaluation protocol the authors used.** A rolling time window with a **52-week in-sample window,
a 12-week out-of-sample window, and rebalancing every 12 weeks** — the in-sample length chosen with
reference to Jegadeesh–Titman (2001) and a preliminary calibration. Benchmark is the market index
for the four index datasets and, for the industry-portfolio dataset, **the equally-weighted
portfolio**.

**Comparison set.** Six models, five of them other people's: their CZεSD model; exact SSD by
cutting planes (Roman et al.); the Lizyayev–Ruszczyński approximate-SSD model; Luedtke's linearised
SSD; the Kopa–Post SSD model with a fixed power weight; and plain Markowitz mean-variance.

**Reported measures.** Sharpe, Sortino, Rachev (a CVaR-ratio at 5%/5%), information ratio against
the benchmark, Jensen's alpha against the benchmark, average return, and a **turnover** measure —
mean over rebalances of `Σ_i |x_{j,i} − x_{j−1,i}|`, explicitly counting only model-generated
trades and **not** drift, and offered as an approximation to transaction costs rather than a
charge against returns.

## Robustness evidence (qualitative only)

- **Multi-decade and multi-market.** Five datasets, two countries plus an industry cross-section,
  the longest spanning more than four decades, all ending before this lab's validation window
  opens. The `validation_overlap: false` flag is unusually clean here.
- **The comparison is against third-party models, not against the authors' own earlier variant** —
  materially stronger than the single-group comparison in the companion Annals of OR source, and
  it includes mean-variance as the reference everybody recognises.
- **Published data.** The weekly return series for all five datasets were released as a separate
  Data-in-Brief paper for reuse. Reproducibility at the data level is therefore better than this
  literature's norm, and the model is simple enough to re-implement from the paper alone.
- **The theoretical claim is proved, not asserted.** The implication chain (CZεSD ⟹ ZεSD, and
  CZεSD ⟹ LR-ASSD) and the shortfall equivalence are derivations, so the construction's
  justification does not rest on its own empirical table.
- **Costs: not charged.** Turnover is reported and described as an approximation to costs. No
  result in the paper is net of anything.
- **Multiple testing: not addressed.** Six models on five datasets with seven performance measures,
  reported at face value.
- **An undiscussed screen.** Requiring at least ten years of observations per stock is a
  survivorship filter, and on index-constituent data it also selects for names that stayed listed.
  The authors do not raise it. This folder has the relevant notes
  (`notes/2026-10-02-delisting-returns-the-other-half-of-survivorship.md`,
  `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md`), and the right discount is to
  treat the in-sample feasibility of a low-`ε` portfolio as optimistic.
- **Replication status: none known** for this specific rule. The broader SSD-portfolio literature it
  competes with is active and the five rival models are independently published, which is the
  nearest thing to replication available.

## Implementability here

**This is the most directly usable construction this folder has filed for the lab's own objective,
and the reason is the shape of the objective rather than any claim about returns.** The lab grades
a candidate on Sharpe minus the equal-weight eligible pool's. The model above minimises the mean
shortfall of a long-only book below exactly that kind of benchmark, takes nothing but a matrix of
excess returns, and is a linear program with no tuning parameters. Long-only and
fully-invested are the paper's constraints as written; `x_j ≤ 0.25` is one more linear bound;
`scipy.optimize.linprog` solves it.

**Four things to get right, and one argument for not running it at all.**

1. **`n ≫ T` is the whole risk, and it is worse here than in the paper.** Their largest case is 442
   assets against 52 in-sample weeks, and even there the LP has far more freedom than data. On this
   panel — roughly a thousand eligible names — an unrestricted solve will drive the in-sample
   shortfall to near zero by construction. **The paper's own no-arbitrage argument is the reason to
   distrust that**: a near-zero `ε` is the signature of fitting, because a genuinely dominant book
   cannot exist. Treat the fitted `ε` as a *diagnostic*, not an achievement: if it comes out near
   zero on the training window, the solve has not found an edge, it has found the panel's width.
2. **Pre-screen the asset set before solving.** Some restriction to a few hundred names (by
   liquidity tier, or by a prior score) is part of the construction. Choosing that screen *after*
   seeing which solve worked is the hindsight this lab's rules forbid, so the screen must be fixed
   before the first solve and stated in the hypothesis.
3. **Costs must be added, because the objective is indifferent to them.** Minimising shortfall
   below a benchmark has no reason to produce a stable book. An `ℓ₁` penalty on weight changes
   against the previous row stays linear with auxiliary variables and is the natural fix; the
   companion note's gross finding — slower rebalancing beat faster rebalancing *before* costs —
   argues for a quarterly or semi-annual grid rather than monthly.
4. **Walk-forward as written.** Their rolling scheme (fit on trailing 52 weeks, hold 12 weeks,
   re-solve) is already causal and maps onto roughly a 250-day window with a 60-day hold on daily
   data. One solve per emitted row, nothing cached, per `strategies/lib/walkforward.py`'s
   discipline.

**One asymmetry worth noticing, because it is the reason this is not simply "optimise the active
return".** The objective is **one-sided**: it penalises periods where the book trails the benchmark
and gives no credit for periods where it leads. For a lab graded on a *Sharpe* difference, that is
not the same objective — it is closer to minimising the downside tracking error. Whether one-sided
is better than two-sided here is an empirical question this source cannot answer, but the one-sided
form is the one with the stochastic-dominance justification, and it is also the form that does not
reward a lucky large lead. The two-sided alternative is the companion note's ratio model.

**The free pre-trial measurement.** Solve the LP once on the trailing window with the equal-weight
pool as benchmark and record the optimal `ε` (the mean in-sample shortfall) as a function of the
number of names allowed in. If `ε` falls towards zero as names are added, the curve *is* the
overfitting, and it is measurable before a single return is scored. Combined with the weight-stability
check in the companion note, two LP solves decide whether a trial here is worth spending.

## Related

- `notes/2026-11-22-enhanced-indexation-as-a-benchmark-relative-linear-program.md` — the companion
  construction: a two-sided ratio objective with tail parameters, versus this one-sided
  parameter-free one. Read together, they bracket the enhanced-indexation design space, and both
  omit costs.
- `notes/2026-10-23-cvar-optimization-as-a-linear-program.md` — the same per-scenario shortfall
  variables; this paper's objective is that construction with the benchmark subtracted and the tail
  probability set to one.
- `notes/2026-10-14-which-alpha-the-sufficient-statistic-for-beating-a-benchmark.md`
  and
  `notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md` — what statistic
  actually decides that a book beat its benchmark, which is the question this model answers with a
  shortfall rather than a mean.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the standing prior against optimised books on
  wide panels; the `n ≫ T` caution above is that note applied to this one.
- `notes/2026-10-02-delisting-returns-the-other-half-of-survivorship.md`,
  `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the ten-year-history screen
  the authors leave undiscussed.
- `notes/2026-11-22-cointegration-tracking-and-its-price-level-tilt.md` — the third construction in
  this family, and the one this folder refuses on the lab's own measurement.
