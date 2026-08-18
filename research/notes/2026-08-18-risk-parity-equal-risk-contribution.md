---
title: "On the Properties of Equally-Weighted Risk Contributions Portfolios" (published as "The Properties of Equally Weighted Risk Contribution Portfolios")
authors: Maillard, Roncalli, Teiletche
year: 2010 (working paper June 2008, this version May 2009)
venue: Journal of Portfolio Management 36(4), 60–70 (venue tier 1 by the rubric's JPM listing; the content is closer to tier-2 quantitative practitioner research)
url: https://doi.org/10.3905/jpm.2010.36.4.060 ; working paper http://www.thierry-roncalli.com/download/erc.pdf
citations: 512 (Semantic Scholar by DOI, checked 2026-08-18)
sample_period: theory is sample-free; empirical illustrations use January 1973 – December 2008 (US sector indices), January 1979 – March 2008 (commodities), January 1995 – December 2008 (global multi-asset)
markets: 10 US industry sector indices; a commodity panel; a 13-instrument global multi-asset set (equity indices, government and credit bonds, EM debt, commodities)
tier: A on the theory (closed-form results that cannot decay), B on the empirical illustrations (single set of backtests, no multiple-testing control, practitioner framing)
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source `SUMMARY.md` has flagged for two sessions as the largest uncovered axis:
the **risk-parity half of family 3**, and specifically the question of what a sound
risk-weighting scheme requires. The paper's value here is almost entirely in its closed-form
results, which settle the lab's two inverse-vol refutations at the level of *what the
objective is*, not at the level of whether an estimate was noisy.

The construction: choose weights so that every component contributes **the same share of
total portfolio risk**. Component `i`'s risk contribution is `σ_i(x) = x_i · ∂_{x_i} σ(x)`,
and these are set equal across `i`. The motivation is a middle path between two
return-free constructions — 1/N (balanced in *weights*, but not in risk, so one volatile
component can dominate the portfolio's variance) and minimum variance (balanced in
*marginal* risk, but typically concentrated in a handful of low-volatility names).

Four analytic results do all the work for this repo:

**(1) Two components: ERC is exactly inverse-volatility, independent of correlation.**
For `n = 2` the solution is

```
x* = ( σ₁⁻¹ / (σ₁⁻¹ + σ₂⁻¹) ,  σ₂⁻¹ / (σ₁⁻¹ + σ₂⁻¹) )
```

and the paper states explicitly that this does not depend on `ρ`.

**(2) Many components: inverse-vol is ERC only under a constant correlation matrix.** If
`ρ_ij = ρ` for all `i ≠ j`, then

```
x_i = σ_i⁻¹ / Σ_j σ_j⁻¹
```

— each weight is the inverse of its volatility over the harmonic average of volatilities.
Away from constant correlation this is **not** the ERC portfolio.

**(3) The general solution is inverse-beta, not inverse-volatility.** Writing `β_i` for
component `i`'s beta *to the portfolio itself*,

```
x_i = β_i⁻¹ / Σ_j β_j⁻¹ = β_i⁻¹ / n
```

so the penalty falls on components with high volatility **or** high correlation with the
rest of the book. The solution is endogenous (`x` depends on `β`, which depends on `x`), so
in general it needs numerical optimisation — the paper is explicit that this is
computationally heavy relative to 1/N and even to minimum variance.

**(4) The optimality condition, which is the finding that matters most here.** ERC coincides
with the maximum-Sharpe (tangency) portfolio **if and only if two conditions hold together:
a constant correlation matrix, and all components having the same Sharpe ratio.** The
authors state the converse directly: when correlations differ *or* assets have different
Sharpe ratios, ERC is not the maximum-Sharpe portfolio.

Two structural results round it out: the volatility ordering

```
σ_mv ≤ σ_erc ≤ σ_1/N
```

and an equivalent optimisation formulation — ERC is the minimum-variance portfolio subject
to a diversification floor `Σ ln x_i ≥ c`, where `c = −∞` recovers minimum variance and
`c = −n ln n` recovers 1/N. That formulation is the cleanest statement of what risk parity
*is*: a variance minimiser with a concentration brake, not a return-seeking construction.

## Construction recipe

- **Inputs:** a covariance matrix only. No expected returns anywhere — this is the family's
  entire claim to robustness, and it is the same claim 1/N makes more cheaply.
- **Estimation as run in the paper:** covariance from **daily returns over a rolling
  one-year window**, portfolios rebalanced **monthly** on the last trading day.
- **Solve:** closed form via `x_i ∝ σ_i⁻¹` only in the two-component case or under constant
  correlation; otherwise numerically, minimising the dispersion of risk contributions (or
  equivalently minimising variance subject to `Σ ln x_i ≥ c`), long-only with weights
  summing to 1.
- **A ready-made shortcut for sleeve aggregation:** rescale each sleeve to a common ex ante
  volatility target and equal-weight the rescaled sleeves. (This is the "equal risk weight"
  aggregation Asness–Frazzini–Pedersen use across industry sub-factors; it equals ERC
  exactly when the sleeves' pairwise correlations are equal.)
- **Diagnostics the paper reports and the lab could reuse for free:** Herfindahl and Gini
  indices computed on **both the weight vector and the risk-contribution vector**. The
  weight-side statistics are already in the lab's holdings-only diagnostic toolkit; the
  risk-contribution versions are the natural extension and, like the rest of that toolkit,
  score no returns and cost no trial.

## Robustness evidence (qualitative only)

- The core results are **algebra**, not estimates. They cannot decay, cannot fail to
  replicate, and carry no publication-bias discount. This is the same epistemic status as
  the moving-average weighting identity already in this folder, and it is why the note is
  tiered A on the theory despite a practitioner framing.
- The empirical illustrations are three backtests on sector, commodity and global
  multi-asset panels, with turnover and concentration statistics reported alongside
  performance — better disclosure than most practitioner work. But they are a single set of
  backtests with no multiple-testing control and no out-of-sample discipline, so the
  performance ordering they report is weak evidence, tier B.
- The paper's own account of when ERC and 1/N diverge is a **heterogeneity** condition: the
  two coincide when volatilities are equal, and the gap between them grows with dispersion
  in volatilities and correlations. On panels where components look alike, ERC is close to
  1/N by construction.
- **Tension to record explicitly, in two directions.** (a) The illustrations report ERC
  dominating 1/N on Sharpe; DeMiguel–Garlappi–Uppal (already in this folder) report that no
  optimisation-based scheme consistently beats 1/N out of sample across seven datasets and
  fourteen models. (b) The lab measured the opposite of the illustrations on its own
  ~10-ETF sleeve — true inverse-vol risk parity at 0.35 Sharpe versus static equal weight at
  0.49. The reconciliation is in result (4) below, and it is not "the data disagree": ERC's
  optimality requires equal component Sharpe ratios, a condition none of these three
  settings guarantees and which the lab's sleeve visibly violates.

## Implementability here

**Verdict: the family stays closed, but the reason is now precise, and the note upgrades
the lab's refutation from an empirical result to a screen that can be applied before any
future trial.**

The lab has refuted inverse-vol weighting twice: `risk_parity_multi_asset` (0.35 Sharpe
across a 10-ETF sleeve) and `mom_etf_volweighted_blend` (inverse-vol between the momentum
basket and the ETF sleeve, cutting the fixed-80/20 blend from 0.85 to 0.76).
`learnings.md` diagnoses both as "inverse-vol between sleeves of unequal diversification
always favors the more-diversified leg". This source sharpens that on three points, one of
which corrects it:

1. **The between-sleeve implementation was not a mis-approximation — it was exact.** For two
   components, ERC *is* inverse-volatility, and result (1) says correlation does not enter.
   So `mom_etf_volweighted_blend` implemented textbook risk parity correctly. That closes an
   escape route the lab never actually took but might have: there is no "proper" risk-parity
   version of that blend that would have done better. **The refutation is of the objective,
   not of the estimator.**
2. **The objective is provably wrong when component Sharpes differ, and the lab's do.**
   Result (4) is the free screen this axis has been missing. Equalising risk contributions
   is the maximum-Sharpe answer only under constant correlation *and equal Sharpe ratios*.
   The lab's two components are a momentum basket around 1.1 validation Sharpe and a
   diversified ETF sleeve around 0.5 — roughly a factor of two apart. Under that condition
   the paper's own theory says ERC is *not* the tangency portfolio, and the direction of the
   error is exactly what the lab measured: the low-volatility, low-Sharpe leg is handed
   capital in proportion to its calmness rather than its earning power. This also explains
   the `learnings.md` finding that fixed-ratio blending beat every vol-based reweighting
   tried: a fixed ratio at least encodes a judgement about relative return, which risk
   parity structurally refuses to look at.
3. **Within a sleeve, the "unequal diversification" framing needs restating as a
   correlation statement.** Result (3) gives the general rule: ERC penalises a component for
   high volatility *or* high correlation with the rest of the portfolio, `x_i ∝ 1/β_i`. So
   the honest generalisation of the lab's learning is not about diversification per se but
   about **portfolio beta**: any risk-balancing scheme systematically overweights whatever
   is least correlated with the book, and a diversified sleeve is least correlated with the
   book almost by definition, regardless of whether it earns anything. Correcting a naive
   inverse-vol scheme to a full ERC scheme would push *further* in the refuted direction,
   not back from it.

**The leverage constraint independently forecloses the family's actual selling point.** The
volatility ordering `σ_mv ≤ σ_erc ≤ σ_1/N` says risk parity's product is a portfolio with
*lower volatility* than equal weight. In the practitioner literature that is the first half
of a two-step argument — de-risk by balancing contributions, then **lever back up** to the
target return. Gross leverage ≤ 1.0 truncates the second step, leaving only the de-risking
half. That is structurally the same one-sided-scalar problem already recorded for
volatility timing in this family, arriving now from the cross-sectional side. Note this is
the lab's inference from the paper's ordering result, not a claim the paper makes.

**What is worth taking, and it is diagnostic rather than strategic.** The
**risk-contribution vector** — `σ_i(x) = x_i · ∂_{x_i}σ(x)`, or equivalently `x_i β_i σ(x)`
— is a holdings-only statistic computable from the weight matrix and a covariance estimate.
It scores no returns, is not a backtest, and therefore costs no trial, which puts it in the
category `learnings.md` says keeps killing ideas cheaply. Its natural use is descriptive:
the champion's magnitude weighting concentrates *weight* in the strongest names, and the
open standing question is whether its monotonically widening validation drawdown is a
concentration artifact. The risk-contribution decomposition answers "how much of the book's
variance does the top name actually explain?" — which the existing top-weight and HHI
statistics only proxy. **Recommended as a diagnostic; explicitly not recommended as an
objective to optimise, for the reasons above.**

**Pitfall for a future session.** Do not read Asness–Frazzini–Pedersen's use of "equal risk
weight" aggregation as literature support for risk-weighting the lab's sleeves. They apply
it across ~49–70 industry sub-factors that are constructed identically and are plausibly
close to equal in both correlation structure and Sharpe — the exact conditions under which
result (4) says ERC is optimal. The lab's application was two sleeves that fail both
conditions. Same formula, opposite verdict, and the condition that separates them is
checkable in advance without spending a trial.

## Related

- `2026-08-17-naive-vs-optimized-weighting.md` — 1/N versus optimisation; ERC is the
  intermediate case, and the parameter-count triage rule in that note ranks it as expensive
  (a full covariance matrix) except in the two-component case where it collapses to a
  single volatility ratio.
- `2026-08-17-volatility-timing-managed-portfolios.md` — the vol-targeting half of family 3;
  the one-sided-scalar problem under a leverage cap is common to both halves.
- `2026-08-18-low-risk-investing-industry-neutral.md` — the equal-risk-weight aggregation in
  its favourable setting.
- `experiments/learnings.md` — "Inverse-vol / risk-weighting between sleeves of unequal
  diversification always favors the more-diversified (lower-return) leg" (two trials), and
  "Standalone diversified ETF sleeves cap out well below the champion".
