---
title: "Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps"
authors: Jagannathan, Ma
year: 2003
venue: Journal of Finance (tier 1, peer-reviewed)
url: https://doi.org/10.1111/1540-6261.00580
citations: 1652 (Semantic Scholar, DOI endpoint, checked 2026-08-21); 1210 (Crossref is-referenced-by-count, checked 2026-08-21)
sample_period: 1968–1999 (portfolios formed each April 1968–1998, post-formation returns to April 1999; covariance estimated on the preceding 60 months, so estimation data reaches back to 1963)
markets: US only — 500 stocks drawn each year from NYSE/AMEX common stocks above the 80th NYSE size percentile and above $5
tier: A
validation_overlap: false
published_post_2018: false
---

Full text read directly: NBER Working Paper 8922 (May 2002), the working-paper version of the
published article, `nber.org/system/files/working_papers/w8922/w8922.pdf`. A published erratum
exists (`afajof.org/wp-content/uploads/Risk-reduction-Jagannathan-erratum.pdf`, "A Note on
'Risk reduction in large portfolios…'"); it was not read this session, so treat the algebra
below as read from the working paper rather than as the final published statement.

## Mechanism

The paper's object is the **global minimum-variance portfolio** built from an estimated
covariance matrix `S`, under two constraints practitioners impose anyway: no short sales
(`ω_i ≥ 0`) and a per-position upper bound (`ω_i ≤ ω̄`).

The starting puzzle is a genuine contradiction in the prior literature. Green–Hollifield argue
that the extreme long/short weights of sample-efficient portfolios are **not** mostly
estimation error: with one dominant factor and little cross-sectional dispersion in betas, the
minimum-variance solution genuinely wants to short a high-beta basket against a low-beta one,
so the weights are large for a real reason. If that is right, forbidding shorts should *cost*
efficiency. Empirically it usually helps. The paper reconciles the two.

**Proposition 1 (the whole idea).** Let `λ` be the Kuhn–Tucker multipliers on the
non-negativity constraints and `δ` the multipliers on the upper bounds. Define

```
S̃ = S + (δ1' + 1δ') − (λ1' + 1λ')
```

Then `S̃` is symmetric positive semi-definite and the *constrained* minimum-variance portfolio
from `S` is an *unconstrained* minimum-variance portfolio from `S̃`. Reading off the entries:

- Wherever the **no-short** constraint binds for asset `i`, that asset's covariance with every
  other asset `j` is **reduced** by `λ_i + λ_j`, and its own variance by `2λ_i`.
- Wherever the **upper bound** binds for asset `i`, its covariance with `j` is **raised** by
  `δ_i + δ_j`, and its variance by `2δ_i`.

The economics is in which assets those constraints bind for. At the unconstrained optimum every
asset's marginal contribution to portfolio variance is equalised, so an asset with unusually
large covariances with the rest of the book gets pushed down and, if the covariances are large
enough, goes negative — meaning **the no-short constraint binds precisely on the assets with
the largest estimated covariances**. Those are the estimates most likely to be *upward*-biased
by sampling error. So the constraint shrinks exactly the elements that are most likely
overstated. Symmetrically, the upper bound binds on assets with unusually *low* estimated
covariances, which are the estimates most likely *downward*-biased, and the constraint raises
them. Both moves are shrinkage toward the average, applied where estimation error is expected
to be worst — which is why a constraint that is **false in the population** can still improve
out-of-sample risk.

**Proposition 2** upgrades this from an equivalence to an estimator. Under iid joint normality
with `S` the unconstrained MLE, `S̃` (with the upper-bound multipliers rescaled by `1 − ω̄`)
satisfies the first-order conditions of the **constrained maximum-likelihood problem** —
maximise the likelihood of `Ω` subject to the requirement that the minimum-variance portfolio
implied by `Ω` obey the weight constraints. In the authors' words: you may impose the
constraints at the *estimation* stage instead of the *optimisation* stage and get the same
answer. The constraint is not a restriction bolted onto an estimate; it **is** an estimator.

## Construction recipe

Not a strategy — a re-derivation and a diagnostic. The reusable procedure:

1. For any binding weight constraint, its **shadow price is the size of the implicit covariance
   edit** it performs: `λ_i + λ_j` off the `(i,j)` covariance for a binding floor, `δ_i + δ_j`
   onto it for a binding cap. A constraint that never binds performs no edit and is inert.
2. The direction of the edit is fixed by the constraint's side: floors shrink large covariances
   downward, caps push small covariances upward. Both are toward the mean.
3. Therefore, when comparing "constrain the weights" against "shrink the covariance matrix",
   they are not alternatives on different axes — the first is a zero-parameter special case of
   the second.

Their empirical design, for reference: each April 1968–1998, draw 500 stocks from large,
liquid NYSE/AMEX names with 60 months of prior returns; estimate the covariance nine ways
(monthly sample covariance; Sharpe one-factor; Ledoit's optimal shrinkage; Fama–French
three-factor; Connor–Korajczyk three- and five-factor; and daily-data versions of each, with
and without Scholes–Williams / Dimson / Cohen-et-al microstructure corrections); form three
portfolios per estimator (unconstrained, no-short, no-short *plus* a 2% cap); hold one year;
repeat. Compare realised standard deviation. A parallel exercise minimises tracking error
against the S&P 500.

## Robustness evidence (qualitative only)

- **Multi-estimator, not multi-market.** Three decades of US data, one country, large caps
  only, with the universe redrawn at random each year — a design that guards against
  cherry-picked stock sets but says nothing about non-US markets.
- The headline qualitative findings, stated without dated performance numbers:
  - Once the **no-short constraint is imposed**, the plain monthly sample covariance matrix
    produces minimum-variance portfolios about as good as those from factor models, from
    Ledoit shrinkage, and from daily data. The constraint substitutes for the estimator.
  - Adding a **2% upper bound on top of** no-short changes realised out-of-sample variance
    essentially not at all. The authors conclude that caps are there to make the solution
    *implementable*, not to reduce risk further.
  - Imposing no-short on **factor-model** covariance estimates modestly *hurt* them — which is
    the expected sign if the constraint is false in the population, and is therefore read as
    supporting Green–Hollifield rather than refuting them.
  - Optimisation still beats naive diversification on realised volatility: a minimum-variance
    portfolio subject to no-short had materially lower realised volatility than randomly picked
    equal-weight baskets of similar size, and than the equal- and value-weighted 500.
  - In tracking-error minimisation the constraints are largely *not binding* under a one-factor
    covariance — direct support for the claim that the extreme weights come from the single
    dominant factor, which differencing against a benchmark removes.
- **Aside worth more than it looks**: the authors note that a plain 50/50 average of the
  one-factor and sample covariance matrices performed close to Ledoit's *optimally* weighted
  average of the same two, and suspect large sampling error in the estimated shrinkage
  intensity. That is this folder's "averaging beats estimated-optimal weighting" law appearing
  inside a covariance-estimation paper, from authors not making that argument.
- **Methodology honesty**: multiple estimators reported side by side including the ones that
  lose; no transaction costs modelled anywhere (the exercise is variance, not net return); no
  multiple-testing discussion, but also nothing being data-mined — the propositions are algebra.

## Implementability here

**What does not transfer, stated first.** Propositions 1 and 2 are about the *global
minimum-variance problem*. The champion is not an optimiser: its weights are a monotone
transform of a cross-sectional score, and its 25% cap and long-only constraint bind on
whichever names the *signal* likes, not on whichever names have the largest estimated
covariances. The equivalence `constrained-on-S = unconstrained-on-S̃` therefore has **no bite
on the champion's actual weights**, and this note must not be cited as evidence that the repo's
caps improve its returns. The multipliers `λ`, `δ` in the theorem are the shadow prices of a
variance minimisation that this repo never runs.

**What does transfer, and it is a correction to a standing folder position.**

1. **The folder has recorded the long-only constraint only as a leak, and that is one-sided.**
   `SUMMARY.md` prices constraints through the transfer coefficient (`IR ≈ TC · IC · √BR`,
   `TC ≈ 0.3–0.8`), and three separate sources are logged as reporting their constrained variant
   as materially weaker. Every one of those is a claim about **signal transfer given a correct
   alpha**. Jagannathan–Ma is a claim about **estimation error given a noisy input**, and it has
   the opposite sign: the same constraint that leaks signal also suppresses the input errors
   that would otherwise be amplified. Both are true simultaneously, and which dominates depends
   entirely on whether the binding constraint is standing between the book and a *good* estimate
   or a *noisy* one. Record the tension; do not resolve it by picking a side.
2. **A sharper statement of screen #1.** The folder's first screen grades a weighting scheme by
   how many noisily-estimated parameters it needs. This source adds the complementary half:
   **a hard constraint is a zero-parameter way of buying part of what an estimated shrinkage
   would buy**, which is exactly why constraints keep beating estimators out-of-sample. It is
   the same law as 1/N-beats-optimisation and simple-mean-beats-optimal-combination, arriving
   from a third direction.
3. **A boundary on screen #1, honestly stated.** Screen #1 says avoid schemes that need a
   covariance matrix. Jagannathan–Ma report that *once no-short is imposed*, the sophistication
   of the covariance estimator stops mattering much. That does not license covariance-based
   *objectives* here (those remain closed by the ERC theorem and by both inverse-vol trials),
   but it does mean that for any covariance-based **diagnostic** the lab already runs — the
   risk-contribution vector, and the effective-bets statistic in this session's companion note —
   there is no reason to reach for a factor model or a shrinkage estimator. A plain trailing
   sample covariance on a long-only book is the case where the literature says the fancy
   estimators stop earning their keep.
4. **A free screen against one shape of future proposal.** "Relax the 25% cap so more of the
   signal reaches the weights" is a transfer-coefficient argument. Before spending a trial on
   it, note that the cap is doing double duty — it is also the only thing in the construction
   that pushes back on the covariance elements most likely to be understated. Note equally, so
   this is not over-claimed in the other direction: the paper's own finding is that upper bounds
   added **little** on top of no-short. The honest prior is that cap-relaxation is a small
   effect of ambiguous sign, i.e. not worth a trial.

**Known pitfalls.** The objective is variance, with no expected returns anywhere in the paper —
nothing here speaks to Sharpe or to net return. The result is derived for iid normal returns.
And the shrinkage story depends on the constraint binding on the *high-covariance* names; in a
long-only book every short is forbidden regardless of covariance, so most of the constraint is
not binding in the paper's sense at all.

## Related

- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the estimation-error law this extends;
  the 50/50-vs-Ledoit aside is that note's principle inside a covariance paper.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the transfer-coefficient
  framing this note puts under tension.
- `notes/2026-08-18-risk-parity-equal-risk-contribution.md` — the closed direction that this
  note does *not* reopen: constraints as estimators is not licence for covariance objectives.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the companion
  diagnostic that benefits from point 3.
- `experiments/learnings.md`, "Weight concentration is not risk concentration" — the lab's
  existing trailing-covariance diagnostic, which point 3 says needs no fancier estimator.
