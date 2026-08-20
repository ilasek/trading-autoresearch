---
title: "Parametric Portfolio Policies: Exploiting Characteristics in the Cross Section of Equity Returns" + critique "An Empirical Assessment of Characteristics and Optimal Portfolios"
authors: Brandt, Santa-Clara, Valkanov (2009); Lamoureux, Zhang (2024)
year: 2009; 2024
venue: Review of Financial Studies 22(9), 3411–3447 (venue tier 1); Review of Asset Pricing Studies 14(3), 450–480 (venue tier 1/2, Oxford / Society for Financial Studies)
url: https://doi.org/10.1093/rfs/hhp003 (WP read in full at https://www.nber.org/system/files/working_papers/w10996/w10996.pdf) ; https://doi.org/10.1093/rapstu/raae006 (read in full at https://arxiv.org/pdf/2104.12975)
citations: BSV 434 (Semantic Scholar by DOI, checked 2026-08-20); Lamoureux–Zhang 0 (Crossref is-referenced-by-count, checked 2026-08-20 — not found on Semantic Scholar by DOI; a recently-published critique, so treat its weight as provisional)
sample_period: BSV 1964–2002; Lamoureux–Zhang data from 1961, fully out-of-sample evaluation 1990–2021
markets: US stocks (CRSP / CRSP-Compustat) in both
tier: BSV B+ (tier-1 venue, heavily cited, multi-decade, split-sample out-of-sample test — but single market, transaction costs not modelled, and the optimised book tilts small); Lamoureux–Zhang B− (tier-1 venue, full text read, but essentially uncited so far)
validation_overlap: BSV false; Lamoureux–Zhang **true** (evaluation window runs into 2021)
published_post_2018: BSV false; Lamoureux–Zhang true
---

## Mechanism

The second half of `SUMMARY.md` open question 6(a): *portfolio-choice work that optimises the
realised objective directly rather than a predictive loss.* This is that literature's founding
paper, and its most direct critique.

**BSV's move.** Do not model the joint distribution of returns and then optimise. Instead
write the portfolio weight itself as a fixed function of each asset's characteristics,

```
w_{i,t} = w̄_{i,t} + (1/N_t) · θᵀ x̂_{i,t}
```

where `w̄` is a benchmark weight (e.g. market cap), `x̂_{i,t}` are the asset's characteristics
**standardised cross-sectionally to zero mean and unit variance at each date**, and `θ` is a
short vector of coefficients that is **constant across assets and across time**. Then choose
`θ` by maximising the *sample average realised utility of the portfolio's return*:

```
max_θ  (1/T) Σ_t  u( Σ_i ( w̄_{i,t} + (1/N_t) θᵀ x̂_{i,t} ) · r_{i,t+1} )
```

Four properties follow from the construction, and they are the reason this framework is worth
knowing here:

1. **Dimensionality is decoupled from the universe.** The traditional route needs `N` means and
   `(N²+N)/2` second moments; this needs `|θ|` numbers regardless of `N`. Cost of the
   optimisation grows with the number of *characteristics*, not assets.
2. **Cross-sectional standardisation is load-bearing, for two stated reasons**: the standardised
   distribution is stationary through time where the raw one may not be, and it forces
   `Σ_i θᵀx̂_{i,t} = 0`, so the deviations from the benchmark sum to zero and the weights sum to
   one automatically. The `1/N_t` term is a normalisation so that doubling the universe without
   changing the cross-sectional distribution of characteristics does not double aggressiveness.
3. **The objective captures moments it never estimates.** Because `θ` is fitted to realised
   utility, the fit implicitly accounts for how characteristics relate to expected returns,
   variances, covariances *and higher moments*, each weighted by its actual impact on utility —
   without any of them being modelled.
4. **Any objective is admissible.** The authors name Sharpe ratio, information ratio,
   benchmark tracking, drawdown control and VaR alongside standard utilities; the empirical work
   uses CRRA.

Long-only is handled by truncation plus renormalisation, `w⁺_{i,t} = max[0, w_{i,t}] / Σ_j max[0, w_{j,t}]`,
with the authors noting the resulting non-differentiability at zero and smoothing it
polynomially only to compute standard errors. Nonlinearity is handled by putting nonlinear
transforms and cross-products of the base variables into `x` — the policy is linear in `x` but
`x` can be a polynomial basis in the underlying variables.

**Lamoureux–Zhang's critique, and it is a mechanism, not a data disagreement.** They analyse
overfitting in exactly this policy. The claim: *parsimony in `θ` does not protect you*, because
the utility being maximised depends on every property of an unspecified conditional return
distribution — so the effective dimensionality is not `|θ|`. Their diagnosis is specific and
portable: **overfitting — imprecision in weight estimation — is positively linked to the
variance of the resulting portfolio.** From which their remedy follows directly, and it is
unusual enough to be worth carrying: rather than penalising the parameters, **regularise by
fitting with a more concave loss than the one you care about.** For a power-utility investor
with relative risk aversion `γ`, estimate `θ` in-sample by maximising expected utility at
`γ* = γ + λ`, `λ > 0`, then hold the resulting policy as the `γ` investor. Raising the shadow
cost of variance in the *fitting* objective shrinks precisely the estimation noise that is
correlated with variance. They report the problem to be serious at low risk aversion and mild
at middling risk aversion — consistent with the mechanism, since a less risk-averse fit takes
more aggressive positions.

They also note two things about the alternatives: an L1 (lasso) penalty on the parameter space
does improve out-of-sample performance in this setting, but is criticised elsewhere for poor
statistical properties when the characteristics are correlated and for lacking economic
motivation; and because a parametric portfolio policy specifies no likelihood, Bayesian
shrinkage has no natural hook, which is why they reach for a decision-theoretic (maxmin over
bootstrapped configurations) criterion instead.

## Construction recipe

- Choose a benchmark weight vector `w̄` (equal weight or market cap; `w̄ = 0` gives a pure
  long-short characteristic portfolio).
- Standardise each characteristic **cross-sectionally at each rebalance date** to zero mean and
  unit standard deviation.
- Set `w = w̄ + (1/N)·θᵀx̂`; truncate at zero and renormalise for long-only.
- Fit `θ` by maximising average realised utility over the fitting sample; for regularisation,
  fit at `γ* = γ + λ` and evaluate at `γ`, selecting `λ` out-of-sample.
- Test individual and joint significance of characteristics from the first-order conditions
  (the estimator is a maximum-expected-utility estimator, so standard GMM-style inference
  applies).

## Robustness evidence (qualitative only)

- BSV run a two-way split-sample experiment (fit on one half, hold in the other, then reverse)
  and report the in- and out-of-sample portfolios to be closely similar in weight distribution
  and in average characteristics, with a modest loss in certainty equivalent. That is a real
  out-of-sample test and better than most of its vintage.
- **But costs are essentially unmodelled.** The only cost discussion is an assertion that the
  optimised portfolio's turnover is low enough that trading costs are unlikely to matter much.
  Under `SUMMARY.md` screen 4(b), that is an unpaid bill, not a finding.
- The optimised portfolio tilts substantially small — the authors say so plainly, in both
  sub-samples and with and without short-sale constraints. That is McLean–Pontiff's "surviving
  predictability lives in small, illiquid names" showing up again, and it is the corner of the
  market this repo does not trade.
- The framework has been independently adopted rather than merely cited: Lamoureux–Zhang list
  applications to option-implied moments, option portfolios, and currency strategies, and
  `notes/2026-08-20-trading-diversification-combining-signals.md` (DeMiguel et al., RFS 2020) is
  a tier-1 paper a decade later built on it. Methodological durability is genuine; the
  *empirical* claims are the part under challenge.
- Lamoureux–Zhang is the challenge, and it is essentially uncited so far. Its mechanism claim
  is checkable on paper and is the part recorded here; its empirical conclusions are not carried
  into this folder, both because of its citation status and because its evaluation window
  overlaps this repo's validation split.

## Implementability here

**The champion is already a parametric portfolio policy with `θ` fixed rather than fitted.**
Magnitude weighting from a cross-sectionally standardised composite momentum z-score is exactly
`w ∝ x̂` with a hard-coded coefficient, plus a threshold. Reading it that way is the useful
part, because it locates precisely which door the lab has kept shut: BSV's contribution is
*fitting* `θ` to realised in-sample utility, and the lab's protocol treats in-sample objective
maximisation as the thing the deflated-Sharpe gate exists to punish. **So this framework is
not a candidate to import — it is the named form of the failure mode the protocol guards
against.** Anyone proposing to "fit the weighting coefficients on the training split" is
proposing BSV, and the honest prior on that is Lamoureux–Zhang's.

**What is genuinely usable, and it is one idea.** Lamoureux–Zhang's regularisation principle —
*fit with a more concave objective than the one you care about, because estimation noise is
correlated with the fitted portfolio's variance* — is a general statement about selecting a
strategy on an in-sample statistic, not a statement about `θ`. It applies to any procedure that
picks a book by maximising a sample objective, which includes **selecting candidates on
validation Sharpe**. `learnings.md` carries a standing ⚠ protocol concern that validation Sharpe
has risen monotonically across recent promotions while the holdout has fallen monotonically,
and records the shape of the winners: more concentrated, faster-rotating. Lamoureux–Zhang's
mechanism predicts exactly that shape — a selection criterion with too little curvature picks
the high-variance member of the candidate set, and the imprecision travels with the variance.
This does not fix anything the lab can touch (the gate lives in a frozen file), but it gives
the human reviewing that concern a literature-grounded name for it and a stated remedy:
*select on a more risk-averse criterion than the one you ultimately care about.* Recorded for
the human, not as a candidate.

**Three secondary yields, all free.**
1. *Cross-sectional standardisation is not cosmetic.* Two specific properties depend on it —
   stationarity of the score distribution across dates, and weights that sum to one without a
   renormalisation step. The champion already standardises; recorded so it is not "simplified"
   to raw returns.
2. *The `1/N_t` normalisation.* Without it, aggressiveness scales with universe size for no
   economic reason. This repo's instrument count is roughly fixed, so it does not bite — but any
   future candidate whose weights are built from an unnormalised sum over held names inherits
   the defect.
3. *Long-only is truncate-and-renormalise, and it is not free.* BSV state that the constrained
   version yields materially smaller gains than the unconstrained one and that they cannot
   reject the optimality of the plain market portfolio once it is imposed. That is a third
   independent instance of this folder's "long-short results do not transfer by default" rule,
   arriving from portfolio construction rather than from a momentum or a beta mechanism.

**What does not transfer at all:** the characteristics are size, book-to-market and lagged
return; two of the three need fundamentals this repo does not have.

## Related

- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — the same crossing from
  the theory side; there the parameters are known, here they are fitted, and the two notes
  bracket the answer to open question 6(a).
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal; BSV is the
  designed response to that estimation-error problem, and Lamoureux–Zhang is the report that
  the response does not fully escape it.
- `notes/2026-08-19-model-averaging-mallows-weights.md` — the other source in this folder that
  says *when* estimated weights are safe; its four conditions and this note's critique are the
  same argument in two vocabularies.
- `notes/2026-08-20-trading-diversification-combining-signals.md` — the same machinery with
  transaction costs made central.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the small-tilt caveat.
