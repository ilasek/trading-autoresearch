---
title: "Parametric Portfolio Policies: Exploiting Characteristics in the Cross-Section of Equity Returns" — read for what cross-sectional standardization assumes, and for the one construction shape that ranks nothing and holds no band
authors: Brandt, Santa-Clara, Valkanov
year: 2009
venue: The Review of Financial Studies (venue tier 1)
url: https://doi.org/10.1093/rfs/hhp003
citations: 492 (OpenAlex, checked 2026-09-11); 434 (Semantic Scholar DOI endpoint, same date); 415 (Crossref `is-referenced-by-count`, same date). Three indices within ~15% of each other — the unusual case in this folder, and worth recording as such.
sample_period: 1964–2002, monthly
markets: all CRSP/Compustat US common stocks (average 3,680 firms per month; 1,033 at the sample's thinnest), plus a 500-largest-stocks subset reported separately
tier: A
validation_overlap: false
published_post_2018: false
read: full text of NBER Working Paper 10996 (December 2004), `nber.org/system/files/working_papers/w10996/w10996.pdf`, 51pp, served first try and text-extractable. The published RFS article was not read; the working paper's sample (1964–2002) and its three characteristics match the published abstract. Nothing below is taken from the published tables.
---

## Mechanism

This note is filed against a coverage gap this file named itself. The 2026-09-10 entry proposed a
checklist — *for every operator the lab applies to a score (demean, rank, winsorize, standardize,
neutralize, blend, band), is there a note on what that operator assumes?* — and answered that it
was "not obviously yes for cross-sectional standardization or winsorization". A grep across all 88
prior notes confirms it: `standardi` appears in 12 notes, always incidentally, and in none of them
is the operator the subject. Meanwhile the lab's own champion family is literally named
`mom_zscore_*`, and `learnings.md` records that moving from equal weight to rank weight to
**z-score-magnitude weight** was the single largest within-basket lever it ever found. The lab has
been standing on this operator for its entire history without a note on what it assumes.

This paper is the right primary because standardization is not decoration in it — it is load-bearing,
and the authors say exactly what it buys them.

**The construction.** Instead of forecasting returns and then optimizing, model the portfolio
weight itself as a function of characteristics:

    w_{i,t}  =  wbar_{i,t}  +  (1/N_t) · θᵀ · xhat_{i,t}

where `wbar_{i,t}` is the stock's weight in a benchmark (e.g. the value-weighted market, or here
equal weight), `xhat_{i,t}` is the vector of that stock's characteristics **standardized
cross-sectionally at date `t` to zero mean and unit standard deviation**, and `θ` is a short vector
of coefficients that is **constant across stocks and constant through time**. Estimate `θ` by
maximizing the sample average of the investor's utility of the realized portfolio return. That is
the whole method.

**The three things standardization is doing, in the authors' own words.** This is the part that
transfers, and it is worth separating because the lab's single boolean bundles all three:

1. **Stationarity.** The cross-sectional distribution of the *standardized* characteristic is
   stationary through time, while the distribution of the raw characteristic may not be. A constant
   `θ` is only coherent if the thing it multiplies means the same thing in every period.
2. **Budget.** Zero cross-sectional mean implies the deviations `θᵀ·xhat` sum to zero across
   stocks, which implies the weights sum to one **for free**, with no renormalization step and no
   constraint imposed in the optimizer.
3. **Breadth invariance — and this one is a separate operator, not part of the z-score.** The
   `1/N_t` term is what makes the policy portable across a changing number of assets. Without it,
   *doubling the number of stocks without otherwise changing the cross-sectional distribution of
   the characteristics results in twice as aggressive allocations, even though the investment
   opportunities are fundamentally unchanged.*

Point 3 is the one this lab most needs and is the least likely to have. A z-score is invariant to
the scale of the score but **not** to the size of the cross-section it is computed over: `N` names
each `z` standard deviations from the mean is a bigger bet than `N/2` such names. The lab changes
its pool size routinely — `learnings.md` (2026-09-04) records region-demeaning narrowing the
scoreable pool from ~84 to ~77 names and `MIN_REGION=4` gating which names are scoreable at all —
and the `1/N` term is precisely the correction for that.

**Why constant `θ` is the substantive assumption, not a convenience.** Constant across stocks means
a stock's weight depends only on its characteristics and never on its own return history: two
stocks with the same characteristics get the same weight even if their realized returns differ
wildly. The authors are explicit that this *is* an assumption — the characteristics are being
asked to capture everything about the joint return distribution that matters for the allocation.
Constant through time means the coefficients that maximize conditional expected utility at each
date also maximize unconditional expected utility, which is what licenses estimating one `θ` from
the pooled sample.

**What the objective buys.** Because `θ` is chosen to maximize utility of the *portfolio's* return
rather than to forecast individual returns, the optimization automatically accounts for the
relation between characteristics and variances, covariances and higher moments — to the extent
those affect expected utility. A characteristic that predicts returns but loads on the same risk as
everything else earns a smaller coefficient than its return predictability alone would justify.
That is a genuinely different object from an IC, which is the statistic this lab grades scores on.

## Construction recipe

**Base policy.**

- Characteristics per name per date; the paper uses three: log market equity, book-to-market, and
  the lagged one-year return (with the standard skip and reporting-lag conventions).
- Standardize each characteristic cross-sectionally at each date to mean 0, SD 1.
- `w_{i,t} = wbar_{i,t} + (1/N_t)·θᵀ·xhat_{i,t}`.
- Choose `θ` to maximize `(1/T)·Σ_t u(r_{p,t+1})` for a pre-specified utility (they use CRRA;
  quadratic, minimum-variance and maximum-Sharpe variants are also reported).
- Rebalance monthly.

**Long-only version — equation (13), and it is three lines.** Truncate at zero and renormalize:

    w⁺_{i,t}  =  max(0, w_{i,t}) / Σ_j max(0, w_{j,t})

The authors flag the one wrinkle: after truncation the weights no longer sum to one (zeroing the
negatives leaves a sum greater than one), hence the renormalization; and `max(0, ·)` is
non-differentiable at zero, which matters for their analytic standard errors and is handled by
splining `max(0, y)` between `y = 0` and a small `y = α > 0`. **For a numerical optimizer that does
not need the gradient, the plain `max` is fine and the spline is unnecessary.**

**Nonlinearity for free.** Linearity in `x` is not restrictive because `x` may itself contain
nonlinear transforms and cross-products of more basic variables `y`; the policy is then
`w = wbar + g(y; θ)` for any `g` spanned by a polynomial expansion. Cross-products are the
interesting case because they encode interactions between characteristics — the paper's own example
is momentum being concentrated in low-book-to-market names.

**Conditioning.** An extension lets `θ` itself depend on a state variable (they use the term
spread), i.e. `θ_t = θ₀ + θ₁·z_t`. This is the paper's version of regime switching and it costs one
extra parameter per characteristic.

**Parameter count.** `θ` has one entry per characteristic. Computational burden grows with the
number of *characteristics*, not the number of *assets*. Three characteristics is a three-parameter
model over thousands of stocks.

**Turnover (a construction statistic, not a performance figure).** The optimized policy turns over
about 50% per year, against about 12% per year for the value-weighted market — whose own turnover
comes only from listings, delistings and issuance. Roughly a 4× ratio over a benchmark that is
doing nothing. The reason is structural and the lab should note it: `θ` is constant, so turnover
comes only from the standardized characteristics moving, and standardization damps the
period-to-period drift that raw characteristics have.

## Robustness evidence (qualitative only)

- Multi-decade US sample across the full CRSP/Compustat cross-section, with the number of firms
  varying by a factor of six across the sample — which is what makes the `1/N` breadth term
  testable rather than cosmetic.
- **The large-cap subset is reported separately and it weakens the paper's own result**, which is
  the robustness fact that matters most here: on the 500 largest stocks the book-to-market
  coefficient stays positive and significant but is **about half as large** as on the full
  cross-section. Recorded as a ratio; no levels, no dates. This is the same direction as
  `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` and
  `notes/2026-09-02-anomalies-by-size-group.md`, and it is a third independent arrival at the same
  discount: **this repo's universe is the subset where characteristics work least.**
- The out-of-sample design is a **split-half swap**: estimate `θ` on subsample 1, apply to
  subsample 2, then flip. The authors report the in- and out-of-sample portfolios as similar in
  composition and average characteristics. This is an honest design and it is *not* walk-forward —
  see the pitfall below.
- The authors argue the stability of the optimized portfolio's average characteristics is itself
  evidence the result is not driven by a few outlying periods.
- Parsimony as a stated overfitting defence: with a handful of parameters over thousands of assets,
  a coefficient only moves away from zero if the characteristic pays *consistently across stocks
  and through time*. This is an argument, not a replication, and should be graded as one.
- Not, as far as this note establishes, the subject of an independent replication study. Its tier
  rests on venue, sample length, the internally-reported large-cap weakening, and a citation count
  that three indices agree on.

## Implementability here

**This is the most directly buildable thing this folder has recorded in some time, and it is also
the first construction shape that is not a sorted band.** The 2026-09-06 session observed that
*every strategy this repo has ever run ranks a score and holds a band*. A parametric portfolio
policy ranks nothing and holds no band: every name gets a weight that is a continuous function of
its standardized characteristics, clipped at zero. That is a structurally new object for this lab,
not another parameterisation of the existing one.

1. **The `1/N_t` breadth term is the cheapest thing on this list and it is free.** It is one
   multiplication. The lab's pool size moves — region-demeaning narrows it, `MIN_REGION` gates it,
   ETF/stock splits change it — and every z-score-magnitude book in this repo is, as far as this
   note can tell from `learnings.md`, implicitly assuming breadth is constant. A train-split
   measurement of how much the effective bet size moves with pool size scores no returns and costs
   no trial.
2. **The long-only recipe is given exactly** (eq. 13) and needs only `max(0, ·)` and a
   renormalization — no optimizer constraint, no projection step. The 25% position cap sits on top
   as a second clip-and-renormalize.
3. **A three-to-four characteristic policy is within budget.** The lab has more than enough
   daily-computable characteristics with recorded standing: a momentum z-score (the champion's own
   input), region-relative Amihud `ILLIQ` (the family lead, and the lab's only leg improvement from
   a stated measurement mechanism), a range-volatility measure, a seasonal score. `θ` would be a
   3–4 vector. Under the `CLAUDE.md` ML guidance — *prefer few features and a penalised linear model
   first* — this is about as few-parameter as a learned model gets, and it is the one shape where
   the fit is over the **portfolio's** utility rather than over 140 noisy return series.
4. **It is a `portfolio-learning` candidate, and it is a different operator from the four that
   family has already closed.** Those closures (mean, max, union, intersection of family leads) are
   all *signal-aggregation* operators over books. This is a *weighting function* estimated against
   an objective — the same distinction that made HRP worth a separate note on 2026-09-07. It could
   equally be filed `statistical-learning`; the family choice should be made deliberately and
   stated, because it affects which cap binds.
5. **The natural first version is the one that cannot overfit: fix `θ` by hand.** Setting
   `θ = (1, 0, 0, …)` and running it reproduces a magnitude-weighted single-signal book with a
   breadth correction — which makes it a *control* for the estimated version rather than a new bet.
   Running the hand-set version first is the cheap way to find out whether the gain comes from the
   policy shape or from the estimation.

**Pitfalls, and the first one is fatal if ignored.**

- **The paper's estimation is a single full-sample fit and would fail this lab's causality check
  outright.** `θ` is chosen to maximize average utility over the whole sample; the split-half swap
  is an *evaluation* design, not an estimation design. Here `θ` must be refit walk-forward via
  `strategies/lib/walkforward.py`, with a training row released only once its forward-return target
  was realized. This is not a technicality — a full-sample `θ` applied backwards is exactly the
  lookahead `causality_check` recomputes truncated weights to catch.
- **A walk-forward `θ` makes the turnover claim unsafe to inherit.** The paper's low turnover rests
  on `θ` being *constant*; a refit `θ` moves every rebalance and adds turnover the paper never
  measured. The 50%-per-year figure is a property of their construction, not a prediction about a
  walk-forward one, and importing it would be the "carry a constant into a new family by analogy"
  error `CLAUDE.md` forbids. Measure it here.
- **Standardization is not free under a long-only constraint**, and this is worth stating plainly
  because the paper's own justification quietly stops applying. Property 2 above — zero mean ⇒
  deviations sum to zero ⇒ weights sum to one — is destroyed the moment `max(0, ·)` truncates the
  negatives. Under long-only it is the **renormalization** that enforces the budget, not the
  standardization. What standardization still buys is stationarity (property 1). The lab should not
  claim more for it than that.
- **A z-score is unbounded and the tails set the weights.** This is the hinge between this note and
  its two companions tonight: in a magnitude-weighted book, the extreme observations of the score
  *are* the portfolio. `learnings.md` already carries the mirror-image finding — the 52-week-high
  proximity signal failed partly because a bounded `(0,1]` score clusters names near 1.0 and has no
  tail to weight on. Distribution shape is doing work here that nobody has measured.
- **Utility choice is a construction node, and an undeclared one.** CRRA with a chosen risk
  aversion, quadratic, minimum-variance and maximum-Sharpe give different `θ`. This is precisely a
  node for the `#93` house-convention list and for `#92`'s specification curve; adding a policy like
  this without fixing the utility in writing first adds a fork the lab cannot see.
- **The paper's characteristics are two-thirds unavailable here.** Market equity and book-to-market
  need fundamentals. Only momentum transfers directly. That is fine — the method is agnostic about
  which characteristics enter — but it means **none of this paper's coefficients, signs or
  magnitudes may be imported**, only the policy shape.
- **Survivorship.** The paper's cross-section includes delisted firms; this universe is current
  constituents. A policy fitted to maximize utility on a survivorship-biased panel will learn the
  bias. This is the standing caveat, but it bites harder here than for a ranked band because the
  objective is fitted rather than imposed.

## Related

- `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md` — the sorted-band alternative, and
  the finding that its asymptotic regime does not exist at `n ≈ 140`. A parametric policy sidesteps
  the binning question entirely, which is its main structural attraction.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the standing case for `1/N` over optimization;
  a parametric policy is the middle object, optimizing a handful of parameters rather than `N`.
- `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md` — the other few-parameter answer to
  the same problem, in PC space rather than weight space.
- `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` and
  `notes/2026-09-02-anomalies-by-size-group.md` — the two prior arrivals at the large-cap discount
  this paper reaches independently in its 500-largest subset.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — the other weighting-function
  object in `portfolio-learning`, declined by the lab on 2026-09-08; the contrast worth drawing is
  that HRP uses no characteristics and fits no objective, while this fits an objective over
  characteristics.
- `notes/2026-09-11-influential-observations-winsorization-versus-robust-regression.md` and
  `notes/2026-09-11-trimming-and-the-size-premium.md` — tonight's other two notes, on the operator
  that decides what those unbounded standardized tails contain.
- `experiments/learnings.md` — the equal → rank → z-score-magnitude weighting ladder, and the
  2026-09-01 retraction establishing that "depth" measured in raw score units is not scale-free.
