---
title: "Technical Note—A Robust Perspective on Transaction Costs in Portfolio Optimization — the cost term in the objective IS a regularizer, and the right coefficient is not the true cost"
authors: Olivares-Nadal, DeMiguel
year: 2018
venue: Operations Research 66(3), 733–739 (venue tier 1 — INFORMS flagship, peer-reviewed)
url: https://doi.org/10.1287/opre.2017.1699
citations: 82 (Crossref `is-referenced-by-count`, checked 2026-10-24, resolved on the first call)
sample_period: "1963-07 – 2013-12 for the four Ken French datasets; 1968-04 – 2005-04 for the CRSP individual-stock dataset. Nothing in the paper touches 2018–2023. The theoretical contribution (Proposition 1) has no sample at all."
markets: US only — 10 and 48 industry portfolios, 6 and 25 size/book-to-market portfolios, and a rolling random draw of 25 CRSP stocks. Monthly returns throughout.
tier: A
validation_overlap: false
published_post_2018: false
read: "full text, from the London Business School institutional repository — `lbsresearch.london.edu/id/eprint/920/1/VDM%20Robust%20Perspective%20on%20Transaction%20Costs.pdf` (526 KB, 22 pages incl. the repository cover sheet; `pdftotext -layout` gave 66 KB of clean text, 247 `\" the \"`, no ASCII shift, no `/xHH` escapes). This is the accepted manuscript, so section and proposition numbering match the published version but page numbers do not. The Online Companion (proofs in Appendix A, supplementary tables in Appendix B) was NOT obtained; everything below comes from the main text, and where the main text only summarises an appendix table that is said explicitly."
anti_lookahead_note: "The paper's Tables 1 and 2 report dataset-by-dataset Sharpe ratios and turnovers over the samples above. No Sharpe ratio from Table 1 is recorded here, and the Sharpe-improvement percentages the authors quote are deliberately omitted — they are performance figures attached to a sample. The turnover contrasts in `Robustness evidence` are recorded because turnover is a construction diagnostic, not a return, and because the *shape* of the contrast (all-or-nothing versus intermediate) is the mechanism. Nothing after 2013 appears in the paper."
---

## Mechanism

The lab already has two notes on what costs do to *trading*: `2026-10-08-no-trade-bands-under-proportional-costs.md`
(how far a holding may drift before correcting it is worth paying for) and
`2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` (trade partway toward a
forward-looking aim portfolio). Both treat the cost coefficient as a *known physical constant* and
ask what the optimal policy is given it. This paper asks a different question, and the answer
changes how the constant itself should be chosen.

**The problem.** Mean-variance with a `p`-norm cost term:

```
min_w   (γ/2)·wᵀΣw  −  µᵀw  +  κ·‖Λ(w − w₀)‖_p^p
s.t.    1ᵀw = 1
```

`w₀` is the starting portfolio, `κ` the cost coefficient, and — the piece that matters most here —
`Λ` is a non-singular **transaction-cost matrix** applied to the trade vector before the norm is
taken. For `p = 1` and diagonal `Λ = diag(λ₁ … λ_N)` the term is `κ·Σᵢ λᵢ·|wᵢ − w₀ᵢ|`: per-name
proportional costs with a different rate for every name. That is exactly protocol v3's cost
structure.

**Proposition 1 — the same problem, written three other ways.** For every `γ > 0` and `κ ≥ 0` there
exist `δ, κ′ ≥ 0`, `α > 0` and `µ₀` such that the problem above is equivalent to:

*(i) a robust portfolio problem.* Replace the cost term with a worst case over the mean:

```
min_w  (γ/2)·wᵀΣw − µᵀw  +  max_{µ̂ ∈ U(δ)} (µ − µ̂)ᵀ(w − w₀)
U(δ) = { µ̂ : ‖µ − µ̂‖_{q,Λ^{-T}} ≤ δ },     1/p + 1/q = 1
```

The uncertainty set is a ball in the **dual** norm. The identity underneath is

```
κ‖Λ(w − w₀)‖_p^p  =  max_{ µ̂ : ‖µ−µ̂‖_{q,Λ^{-T}} ≤ δ }  (µ − µ̂)ᵀ(w − w₀)
```

so the cost term is *literally* the worst-case expected-return regret of trading from `w₀` to `w`,
given that the true mean lies in `U(δ)`.

*(ii) a regularized regression problem.* Using Britten-Jones' (1999) regression form of
mean-variance:

```
min_w  ‖1_T − Rw‖₂²  +  κ′·‖Λ(w − w₀)‖_p^p      s.t.  wᵀµ = µ₀,  1ᵀw = 1
```

with `R` the `T × N` matrix of historical returns. For `p = 1` the cost term is a **lasso** penalty;
for `p = 2` a **ridge** penalty. Note the penalty is on `w − w₀`, not on `w` — it shrinks toward the
*current holdings*, not toward zero.

*(iii) a Bayesian portfolio problem*, where the investor's prior over the weight vector is a
Multivariate Exponential Power density `π(w) ∝ exp(−‖Λ(w − w₀)‖_p^p / αᵖ)` — a distribution the
authors define for this purpose. `p = 2, Λ = Σ^{1/2}` is a multivariate normal prior; `p = 1, Λ = I`
is a Laplace prior.

All three extend unchanged when further constraints (long-only, position caps) are added: put the
same constraints in all four formulations.

**The two readings that matter.**

*Charging yourself for trading buys estimation-error protection for free.* Because the cost term
*is* a dual-norm penalty, a portfolio that pays attention to costs is already robust and already
regularized, whether or not it was designed to be. This is the theoretical explanation for the
practitioner observation that robust portfolios have low turnover: robustifying and charging a
trading cost are the same operation.

*Which `p` you charge encodes which uncertainty you fear.* `p = 1` (proportional costs) ⇒ `q = ∞` ⇒
a **box** uncertainty set. `p = 2` with `Λ = Σ^{1/2}` (the quadratic cost Gârleanu–Pedersen argue
is realistic) ⇒ an **ellipsoid** `‖µ − µ̂‖_{2,Σ^{-1/2}} ≤ δ`, which the authors point out *coincides
with the statistical confidence region for the sample mean* under i.i.d. normal returns with
covariance `Σ`. So of the two common cost shapes, only the quadratic one implies an uncertainty set
that matches the actual sampling distribution of the thing being estimated. That is the paper's
statistical argument for preferring a quadratic penalty over a proportional one *when the goal is
fighting estimation error* — even if the real-world costs are proportional.

**And the consequence the paper draws from all this: the cost coefficient becomes a hyperparameter.**
If `κ` is a regularization strength, it should be *calibrated*, not set to the broker's number. The
authors calibrate it by cross-validation and treat the true cost as the thing you are *evaluated*
against, not the thing you put in the objective.

## Construction recipe

1. **Pick the penalty geometry.** `p = 1, Λ = I` for a plain turnover penalty; `p = 1` with diagonal
   `Λ` holding per-name cost rates for a cost-weighted turnover penalty; `p = 2, Λ = Σ^{1/2}` for
   the estimation-error-matched quadratic penalty. `p = 1.5` is the square-root market-impact shape
   (Almgren et al.; Frazzini et al.) and is covered by the same proposition.
2. **Reparameterise the penalty as a trading budget, so the two geometries are comparable.** `κ` is
   not comparable across `p`. For proportional costs the penalty has an exact constrained twin,
   `‖w − w₀‖₁ ≤ τ`; for quadratic costs the authors invoke Kourtis (2015), whose result is that the
   mean-variance optimum under quadratic costs is a **convex combination of the starting portfolio
   and the cost-free optimum**, so it too is indexed by a single trading volume. Calibrate `τ` (a
   percentage of wealth traded per rebalance), not `κ`.
3. **Calibrate `τ` by k-fold cross-validation inside the estimation window.** Split the `M`-month
   estimation window into 10 contiguous blocks. For each held-out block `j`, compute the portfolio
   from the other nine for every candidate `τ` on a grid, and record that portfolio's return on
   block `j` **net of the true costs**. Pool the `M` held-out returns per `τ` and pick the `τ` whose
   pooled series has the smallest variance. (The authors report that using net-of-cost Sharpe
   instead, and jointly cross-validating `τ` and the cost shape, give qualitatively similar answers.)
   Their grid was `τ ∈ {0, 0.5, 1, 2.5, 5, 10}%` per month.
4. **Re-calibrate at every rebalance**, rolling with the estimation window.
5. **Evaluate net of the true cost schedule** regardless of what `κ` the construction used. The
   calibrated coefficient and the charged coefficient are two different numbers with two different
   jobs.

## Robustness evidence (qualitative only)

- **The central empirical claim is about the *shape* of the trading pattern, and it is the most
  transferable thing in the paper.** A penalty set to the *true* proportional cost drives turnover
  almost to zero: the `ℓ1` term is non-differentiable at `w₀`, which creates a no-trade region whose
  width grows with `κ`, and at the honest cost level that region swallows nearly every trade. The
  authors describe this as "an all-or-nothing trading pattern". The cross-validated penalty instead
  selects *intermediate* turnover, typically one to two orders of magnitude higher than the
  honest-cost penalty allows and one to two orders below the unpenalised optimum. Net-of-cost
  out-of-sample Sharpe followed the intermediate setting.
- **The optimal penalty depends on how noisy the target portfolio is, and a single rule gets it
  wrong in both directions.** Mean-variance portfolios (which need `µ`) are helped by charging the
  nominal cost, because they need the regularization badly. Minimum-variance portfolios (which do
  not need `µ`) are *hurt* by it — the authors call the nominal coefficient "too conservative" for
  them. So "charge yourself the real cost" over-regularizes an already-stable construction and
  under-regularizes an unstable one.
- **Quadratic beat proportional for the minimum-variance portfolios on four of the five datasets**,
  consistent with the ellipsoid/confidence-region argument above.
- **Where the gain came from.** The authors state (from Online Companion tables not read here) that
  cost-aware construction did *not* reduce return variance; the improvement was in the out-of-sample
  **mean**. Tail risk behaved like variance. So this is not a risk-reduction device dressed up as a
  performance device.
- **Limits.** Single country, monthly data, portfolios-as-assets for four of five datasets, and
  `N ≤ 48` except in the CRSP draw (`N = 25`, robustness at 50 and 100). Costs assumed a flat 50 bps
  proportional for every name — the heterogeneous-`Λ` case the theory permits is never exercised
  empirically. The theory is exact and sample-free; the calibration result is one paper's evidence
  on small universes.

## Implementability here

**Status: the theory applies directly and is free; the empirical recipe is a trial.**

- **The direct and free consequence, and it is a correction to how this lab reads its own protocol.**
  Protocol v3 charges per-name costs *in the evaluation*. That is an accounting fact. It says nothing
  about what cost coefficient a candidate should use *in its own construction*, and this paper's
  result is that the two numbers should generally differ — the evaluation coefficient is the truth,
  the construction coefficient is a regularization strength. A candidate that tries to be clever by
  simulating v3's exact cost schedule inside its own weighting rule is, by Proposition 1, choosing a
  specific and probably wrong prior. **Any candidate with a cost-aware construction step should be
  able to say which number it used and why.**
- **The sharp lab-specific reading of `Λ`, and the caution that goes with it.** v3's cost schedule is
  per-name and highly dispersed: 15/20/30/40 bps per side by liquidity tier, plus UK stamp duty
  (0.5% on purchases), HK stamp duty (both sides) and French/Italian/Spanish FTTs (purchases). Set
  `Λ = diag(λᵢ)` with `λᵢ` that name's round-trip rate and the cost term is `κΣᵢλᵢ|Δwᵢ|`. Proposition
  1(i) with `p = 1, q = ∞` then makes the implied uncertainty set a box with **per-name half-widths
  `δ·λᵢ`**: minimising cost-aware mean-variance is behaving as though each name's expected return
  could be wrong by an amount *proportional to that name's trading cost*. **That correspondence is
  algebra, not economics, and the direction of the implication is worth stating plainly: a UK
  large-cap's stamp duty is a fact about HMRC, not evidence that its mean return is badly estimated.**
  Real estimation error in a name's mean scales with its return volatility and the length of its
  history. So the free regularization that comes with charging honest v3 costs is **mis-weighted** —
  it over-shrinks expensive-but-well-measured names (UK/HK large caps) and under-shrinks
  cheap-but-noisy ones. A candidate that wants the regularization should choose `Λ` for the
  estimation-error job (e.g. `Σ^{1/2}`, or per-name trailing volatility) and let the engine charge
  the real schedule separately.
- **The cross-validation step is the part that needs care here, and the folder already has the
  warning.** Step 3 is k-fold CV on contiguous blocks of a return panel.
  `2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` is about exactly this hazard, and
  anything built from this recipe should use that note's purging/embargo discipline rather than the
  plain 10-fold split the authors use. Separately, the calibration must happen **inside** each
  rebalance's visible window or `causality_check` will fail it — this is the walk-forward requirement
  in `CLAUDE.md`, and the CV grid is small enough (six values) that the cost is tolerable.
- **What is cheap to build.** A long-only ranked book with a cost-weighted turnover budget: rank on
  whatever signal, form the target equal-weighted top-`k` book, then move from `w₀` toward the target
  only as far as a per-rebalance budget `Σᵢλᵢ|Δwᵢ| ≤ τ` allows, spending the budget on the trades
  with the largest score change per unit of cost. `τ` calibrated on the visible window. No covariance
  matrix, no optimizer — the paper's Kourtis reparameterisation says the quadratic-penalty solution
  is a convex combination of old and target book, which for a long-only ranked book is just partial
  movement toward the target.
- **What to avoid.** The paper's own empirical constructions are minimum-variance and mean-variance
  optimizations, which need `Σ` or `µ` at this panel's width. Candidate-list item 1's triage rule
  (count the noisily-estimated parameters) applies with full force and is the reason to take the
  *penalty* from this paper and not the *portfolio*.

## Related

- `2026-08-22-long-only-as-l1-regularization.md` — Brodie et al.'s result that a long-only
  constraint is itself an `ℓ1` regularizer. Tonight's paper is the trade-side twin: that one
  regularizes the *level* of the weights, this one the *change* in them. The DGNU (2009,
  *Management Science*, 921 Crossref cites checked 2026-10-24) norm-constraint result is cited in
  passing in that note; Proposition 1(iii) here generalises DGNU's Bayesian interpretation from the
  1-, 2- and A-norms to all `p ∈ [1,2]` with an arbitrary `Λ`.
- `2026-10-08-no-trade-bands-under-proportional-costs.md` — the asymptotic no-trade band. This paper
  explains *why* the honest-cost band is too wide to be the performance-maximising band: the band's
  job is partly regularization, and the honest cost is not the right regularization strength.
- `2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — Gârleanu–Pedersen, whose
  `Λ = Σ^{1/2}` quadratic cost is the exact case Proposition 1(i) maps to the Gaussian confidence
  region. Reading the two together is the point: their realism argument and this paper's statistical
  argument land on the same matrix for different reasons.
- `2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` — the hazard in step 3.
- `2026-10-24-uncertainty-sets-as-dual-norm-penalties.md` — the general optimization theorem behind
  Proposition 1(i), stated for arbitrary norms and uncertainty sets.
- `2026-10-24-equal-weight-as-the-maximal-ambiguity-optimum.md` — the same dual-norm algebra applied
  to *distributional* rather than parameter uncertainty, with the equal-weight portfolio as its limit.
- `experiments/learnings.md` — the de-concentration-price and required-gain tables there are v1/v2
  `price-trend` measurements and are explicitly not to be carried into v3 by analogy; nothing in this
  note licenses doing so.
