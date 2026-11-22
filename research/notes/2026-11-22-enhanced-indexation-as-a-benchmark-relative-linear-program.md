---
title: "Enhanced index tracking with CVaR-based ratio measures — the benchmark-relative long-only book as a linear program, and the rebalance-frequency finding that is measured gross of costs"
authors: Guastaroba, Mansini, Ogryczak, Speranza
year: 2020
venue: "Annals of Operations Research 292, 883–931 — peer-reviewed, gold open access (CC-BY). Operations-research venue rather than a finance journal, so **not** one of the tier-1 names in this folder's rubric; graded tier 2 on venue."
url: https://doi.org/10.1007/s10479-020-03518-7
citations: 37 (Semantic Scholar by DOI, checked 2026-11-22); 32 (Crossref `is-referenced-by-count`, checked 2026-11-22)
sample_period: "weekly returns; the dated instances run in-sample 1992-03 to 1994-02 with out-of-sample 1994-03 to 1995-02 (the five OR-Library instances of Beasley, Meade & Chang). The four FTSE-100 instances and three further OR-Library instances carry no stated dates in the paper — the authors say explicitly of the latter that the originating paper 'did not provide any detail regarding the time frame the data refer to'."
markets: "nine national-index constituent sets — Hang Seng (HK), DAX 100 (DE), FTSE 100 (UK) twice over, S&P 100, Nikkei 225 (JP), S&P 500, Russell 2000, Russell 3000 — with constituent counts from 31 to 2151"
tier: "B. Peer-reviewed and open, the formulations are stated completely enough to re-implement, and the instance design deliberately spans four benchmark-trend combinations. Held below A because: citations are modest for its age, **transaction costs are never charged** (turnover is reported, not priced), the empirical comparison is against one earlier model by the same group rather than against a naive or equal-weight benchmark, and the conclusions overstate one of the paper's own ranking tables (see Robustness)."
validation_overlap: false
published_post_2018: true
read: "Full text, gold open access from `link.springer.com/content/pdf/10.1007/s10479-020-03518-7.pdf`, HTTP 200 on the first request (2.9 MB PDF → 189 KB of text via `pdftotext -layout`, 788 instances of `\" the \"`, no character shift, `( )` dropout check zero). Sections 1–5 and both appendices intact; the numeric tables extract but are not quoted here."
---

## Access

One request, no challenge: a Springer **gold open-access** article is fetched directly from
`link.springer.com/content/pdf/<doi>.pdf`. Worth recording as a positive channel, because this
folder's Springer experience so far has been with closed articles. Two cautions from the same
fetch. `file -b` reported this 49-page article as **"10 page(s)"** — the page-count tell again,
under-reporting, exactly as the [2026-11-21] entry recorded; the extracted-text checks are the
only reliable verification. And the search that found it was a **topic** search, not a title
search: the paper surfaced on the phrase `enhanced index tracking` + `linear programming`, which
is how an OR-journal treatment of a finance problem gets found at all.

Three channels failed first and are recorded in `SUMMARY.md`'s channel notes: the two canonical
enhanced-indexation papers (Canakgoz–Beasley 2009, Beasley–Meade–Chang 2003) are ScienceDirect-only
with no OA location in OpenAlex, and `palomar.home.ece.ust.hk` — which hosts the author copy of a
peer-reviewed IEEE paper on sparse index tracking — **fails TLS verification even with
`--cacert /root/.ccr/ca-bundle.crt`**, a new instance of the `orbilu.uni.lu` class.

## Mechanism

**There is no return-predicting mechanism in this source, and that is why it is here.** It is a
*construction* source. Its subject is the object this lab's own objective already is: a long-only,
fully-invested book whose success is defined **relative to a benchmark portfolio**, not in absolute
terms.

The paper's framing is that enhanced indexation (the EITP) is intrinsically **bi-objective** —
maximise the mean of the excess return over the benchmark, minimise the dispersion of that excess
return — and that the literature's disagreements are mostly disagreements about which scalarisation
of those two objectives to solve. The economic content is a modelling claim rather than a market
claim: if you are graded on a difference of two return series, then the object to optimise is the
*distribution of that difference*, and a risk measure applied to the difference series is a
different thing from the same measure applied to the portfolio's own returns.

The specific proposal is to measure the risk side with the **Weighted Conditional Value-at-Risk**
(WCVaR): a weighted combination of several CVaR measures at different tail probabilities, rather
than one CVaR at a single chosen tail. The motivation is that a single tail level encodes a single,
arbitrary risk-aversion point, while a weighted combination of levels traces a coarse risk-aversion
*profile* and still collapses to a linear program. The theoretical pay-off the authors claim for
this is a **second-order stochastic dominance (SSD) consistency** property: their Corollary 1 states
that an optimal solution of the ratio model, when it satisfies a stated sign condition on
mean-minus-deviation, is SSD-nondominated up to ties in mean and deviation.

## Construction recipe

Notation: `n` assets, `T` historical scenarios (here, weeks) with probabilities `p_t`, asset
returns `r_jt`, benchmark return `r_t^α`, portfolio weights `x_j`, portfolio return
`y_t = Σ_j r_jt x_j`, and `μ_α` the benchmark's mean.

**The model (EWCVaR).** Minimise the ratio of a CVaR-based deviation measure of the *excess*
return series to the mean of that excess return:

    min   [ Δ_w^(m)(R_x − R_α) + ε₂ ] / μ(R_x − R_α)
    s.t.  μ(R_x − R_α) ≥ ε₁
          Σ_j x_j = 1,  x_j ≥ 0

where `Δ_w^(m)` is the WCVaR deviation built from `m` tail levels `β_k` with weights `w_k`. Two
tolerance parameters: `ε₁ > 0` forces the denominator positive (the book must beat the benchmark
in-sample by at least `ε₁`), and `ε₂ > 0` keeps the objective well-posed.

**Linearisation.** The quasi-linear objective is linearised by the **Charnes–Cooper (1962)**
transformation: substitute `v₀ = 1/(z − μ_α)` and rescale every variable by the same factor
(`x̃_j = x_j/(z − μ_α)`, and likewise for the shortfall and threshold variables), divide all
constraints through, and add the transformation's own constraint. After eliminating the variables
that equations define, the compact LP is

    min_{x̃, d̃, η̃}  Σ_j (μ_j − μ_α + ε₂) x̃_j − Σ_k w_k η̃_k + Σ_k (w_k/β_k) Σ_t p_t d̃_tk
    s.t.  Σ_j (μ_j − μ_α) x̃_j = 1
          Σ_j x̃_j ≤ 1/ε₁,   x̃_j ≥ 0
          d̃_tk ≥ η̃_k − Σ_j (r_jt − r_t^α) x̃_j,   d̃_tk ≥ 0   for all t, k

and the actual weights are recovered as `x_j = x̃_j / Σ_i x̃_i`. Note what the constraint matrix
is made of: **one shortfall variable per scenario per tail level**, and the only market input is
the matrix of asset-minus-benchmark excess returns. Size is `O(nm + Tm)` variables.

**Parameterisation the paper actually used.** Four tail-level choices were compared:
`{.05, .25}`, `{.05, .25, .50}`, `{.05}` alone and `{.50}` alone. Scenarios were **104 weekly
in-sample observations** (two years); evaluation ran over the following 52 weeks.

**Rebalancing.** A rolling-window variant re-solves the LP on the trailing 104 weeks at a fixed
cadence; three cadences were compared — every 4, 12 and 24 weeks. Between solves the weights are
left alone.

**Side constraints.** Upper and lower weight bounds and a **cardinality** cap are both available,
but the authors are explicit that a cardinality cap requires binary variables and turns the LP into
a MILP, which is where tractability stops being free.

**Reported diagnostics worth copying.** A **diversification index** defined as the complement of
the Herfindahl index of the weights (1 = perfectly spread, 0 = one name), portfolio cardinality,
min and max weight, and a **turnover index** `TI = (1/L) Σ_l Σ_j |x_{j,l+1} − x_{j,l}|` averaged
over rebalances. The turnover index counts only model-generated trades and explicitly **excludes**
weight changes caused by price drift.

## Robustness evidence (qualitative only)

- **Instance design is the honest part.** The FTSE-100 instance set was deliberately constructed to
  span the four combinations of benchmark direction in-sample × out-of-sample (up/up, up/down,
  down/up, down/down). That is a subperiod-stability design rather than a single sample, and it is
  the right shape of robustness check for a benchmark-relative objective.
- **No model choice dominates.** Across their twelve instances the authors state plainly that *no
  optimization model clearly dominates all the others* out of sample. The ranking tables are close,
  and the model-choice axis is therefore weak evidence — which is the same conclusion this folder
  has reached repeatedly about objective-function variants.
- **An internal inconsistency to read around.** The conclusions assert that *adding further CVaR
  measures within a WCVaR framework tends to produce better performance*, but the paper's own
  single-period ranking table puts the **two**-level variant ahead of the three-level variant on
  average position, with the single deep-tail variant last. The defensible reading is narrower than
  the authors': **one very deep tail level alone is the worst choice, and two levels are enough**.
  Treat the "more measures is better" sentence as unsupported by the table beneath it.
- **The rebalance-frequency result, and it is the transferable one.** Rebalancing **every 24 weeks
  beat every 12 weeks, which beat every 4 weeks**, out of sample, in their rolling-window
  experiments. This is measured **with no transaction costs charged at all** — turnover is reported
  but never priced — so it is a *gross* finding. A cost model can only widen the gap. The mechanism
  is presumably estimation error: re-solving the LP on a largely-overlapping trailing window
  reshuffles weights in response to noise, and the reshuffle is not free even when it is costless.
- **Costs, and multiple testing.** Costs: absent. Multiple testing: not acknowledged at all — the
  four tail-level configurations are compared on the same instances with no correction, which in
  this folder's terms is a four-way search reported at face value.
- **Scenario generation.** The authors note the models accept any scenario set, not just historical
  returns, and warn in their own words that using historical data "might affect the performance of
  any strategy" and that out-of-sample results "must be interpreted with care, since they might
  contain noise that is difficult to separate from the intrinsic performance" of the method. That
  caveat is unusually forthright for this literature and is worth quoting back at any source that
  omits it.
- **Replication status: none.** No independent replication of this specific model class is known to
  this folder, and the comparison inside the paper is against a model by the same four-author group.

## Implementability here

**What maps cleanly, and it is more than usual.** This lab's promotion statistic *is* a
benchmark-relative one — Sharpe minus the equal-weight eligible pool's on the same days — so the
paper's object and the lab's objective are the same object. Everything the LP needs is a matrix of
`asset return − benchmark return` over a trailing window, which is computable from the `prices`
panel and an equal-weight pool return series with no new data. Long-only (`x_j ≥ 0`) and
fully-invested (`Σ x_j = 1`) are the paper's own constraints, not adaptations. The **25%-per-name
cap is a linear upper bound** and goes in for free. `scipy.optimize.linprog` is available and this
folder already holds a note on an LP-shaped risk objective
(`notes/2026-10-23-cvar-optimization-as-a-linear-program.md`), so the machinery is not new here.

**What does not map, in descending order of seriousness.**

1. **Panel width versus scenario count.** The LP has `O(nm + Tm)` variables and `O(Tm)`
   constraints; with roughly a thousand eligible names and a trailing window of a few hundred daily
   observations, the constraint matrix is large but the *estimation* problem is worse than the
   solver problem — `n ≫ T` is precisely the regime where this folder's own precision-matrix and
   weight-estimation notes say an optimised long-only book is noise. The paper's largest instance
   has 2151 assets against **104** scenarios and the authors report solve times as negligible; they
   never ask whether the solution is estimable, only whether it is computable. That gap is the
   whole risk.
2. **Costs absent, and the lab's cost wall is the binding constraint.** Under v3 the per-side cost
   is 15–40 bps plus transaction taxes, and drift between rows is charged. An objective that is
   indifferent to turnover will produce a book whose gross edge is spent. Any implementation must
   either add an explicit turnover penalty (an `ℓ₁` term in weight changes, which stays linear with
   auxiliary variables) or a no-trade band — and this folder already holds both ideas
   (`notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`,
   `notes/2026-10-08-no-trade-bands-under-proportional-costs.md`).
3. **Weekly, not daily.** Every scenario here is a week. On a daily panel the same `T` spans a fifth
   of the history, and daily excess returns are noisier per observation. The rebalance cadences the
   paper compares (4 / 12 / 24 weeks) translate to roughly 20 / 60 / 120 trading days — all at or
   beyond the lab's 21-day cost wall, and the **slowest** was the best.
4. **`ε₁` is a hindsight knob.** Forcing `μ(R_x − R_α) ≥ ε₁` in-sample means the LP is *required*
   to find an in-sample excess return. There is always a feasible point that does so on a wide
   panel, and nothing in the formulation distinguishes a real tilt from an in-sample fit. The
   companion note on stochastic dominance
   (`notes/2026-11-22-stochastic-dominance-over-the-benchmark-and-the-shortfall-lp.md`) makes the
   sharper version of this point: an in-sample book that *never* trails the benchmark is an
   arbitrage, so its existence is evidence of fitting, not of edge.
5. **Walk-forward is mandatory and the paper's own design already is one.** The rolling-window
   variant re-solves on trailing data only, so it is causal as written. It must be implemented that
   way here: one solve per rebalance date on the visible window, nothing cached.

**The concrete adaptation, stated so a session can take it or leave it.** On a monthly or
quarterly grid, solve the compact LP on the trailing window of daily excess returns against the
equal-weight pool, with `x_j ≥ 0`, `Σ x_j = 1`, `x_j ≤ 0.25`, two tail levels `{0.05, 0.25}`, and
an `ℓ₁` turnover penalty against the previous weights. Restrict the asset set before solving —
`n ≫ T` is the failure mode, so a pre-screen to a few hundred names is part of the construction,
not a shortcut. Expect the honest result to be a **null**, and note what makes it informative: a
null here is a statement about *optimisation on this panel*, which is a different and more general
claim than a null on any one signal.

**The free pre-trial measurement this source suggests.** Before building the book, solve the LP
once on the trailing window and once on the *first half* of it, and measure the rank correlation
of the two weight vectors. If an optimised long-only benchmark-relative book is not stable to
halving its own estimation window, the trial is measuring estimation noise and can be skipped at
zero cost. This is the weight-stability counterpart of the screens numbered `#501`–`#503`.

## Related

- `notes/2026-10-23-cvar-optimization-as-a-linear-program.md` — the same linearisation machinery
  (shortfall variables per scenario) applied to absolute rather than benchmark-relative risk.
- `notes/2026-11-22-stochastic-dominance-over-the-benchmark-and-the-shortfall-lp.md` — the
  companion construction, which reaches a *strictly simpler* LP for the same job and supplies the
  no-arbitrage argument against requiring in-sample out-performance.
- `notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md` and
  `notes/2026-10-12-tracking-error-and-weight-constrained-portfolios-in-high-dimensions.md` — the geometry of benchmark-relative optimisation, i.e. why
  minimising tracking error alone produces a systematically wrong total-risk position. This source
  is the LP-side literature that geometry never meets.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal. The standing prior
  against which any optimised book on a wide panel must be read; this paper never tests against a
  naive rule.
- `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md` and
  `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` — the `n ≫ T` problem the
  paper computes through without addressing.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the cost layer this source
  omits; its finding and this paper's gross rebalance-frequency result point the same way.
- `experiments/learnings.md` — the de-concentration and turnover lessons there were measured under
  v1/v2 on `price-trend` constructions and must not be imported into a cost model for this one.
