---
title: "Shrinking the Cross-Section — economically-motivated shrinkage, and why sparsity lives in PC space rather than characteristic space"
authors: Kozak, Nagel, Santosh
year: 2020
venue: Journal of Financial Economics 135(2), 271–292 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2019.06.008
citations: 776 (OpenAlex by DOI, checked 2026-09-03); Crossref `is-referenced-by-count` 719 (checked 2026-09-03); Semantic Scholar's DOI endpoint returns "not found" for this DOI
sample_period: daily — July 1926–December 2017 (FF25 warm-up application); November 1973–December 2017 (50 anomaly portfolios); September 1964–December 2017 (WRDS financial-ratio portfolios); the interaction data sets start slightly later
markets: US (CRSP), excluding stocks below 0.01% of aggregate market capitalisation
tier: A
validation_overlap: false
published_post_2018: true
---

Read **in full** from the authors' own PDF of the accepted manuscript, hosted on Stefan Nagel's
university page (`cpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/f/575/files/2020/07/SCS.pdf`, 56
pages, May 2019 version), for the paper published as JFE 135(2). The Internet Appendix is at the
same host (`.../SCSIA.pdf`) and was not needed for anything recorded here.

This is the source `research/README.md` asks for by name under `statistical-learning`: "how *few*
predictors actually matter". Its answer is not the one the question expects, and the correction is
the most useful thing in this note.

## Mechanism

The paper is about the **prior you have to hold** to estimate a return-forecasting model when the
number of candidate predictors is large relative to the sample, and about which space that prior
should be expressed in.

**Step 1 — the economic claim.** Absence of near-arbitrage implies that a factor earning a large
risk premium must either itself be a major source of return variance, or load heavily on something
that is. First and second moments are tied together. This holds in rational models where pervasive
risks are priced, and — under plausible restrictions — also in models where the cross-section of
expected returns comes from biased beliefs. Turned into a statement about a factor covariance
matrix: **most of the SDF's variance should be attributable to the high-eigenvalue principal
components of the candidate factor returns**, and an estimated model that puts large weight on a
low-variance PC is claiming a near-arbitrage, which is implausible and probably spurious.

**Step 2 — the prior implements that claim as unequal shrinkage.** With a conjugate normal prior
whose covariance is tied to the return covariance matrix, the posterior mean of the SDF coefficient
vector is `b̂ = (Σ + γI)⁻¹ μ̄`, where Σ is the factor covariance matrix, μ̄ the sample mean vector,
and γ the penalty. This *looks* like plain ridge, but it is not ridge on a return-prediction
regression: it is ridge applied to the mapping from **covariances to mean returns**. Because Σ's
eigenvalues sit inside the inverse, the estimator **shrinks coefficients on low-eigenvalue PCs far
harder than those on high-eigenvalue PCs**. The heterogeneity is the whole point; a uniform penalty
does not deliver it, and the authors show the unequal shrinkage is what buys the out-of-sample
improvement.

**Step 3 — the penalty has an economic unit.** With their prior parameterisation, γ maps one-to-one
to `κ`, the **root expected maximum squared Sharpe ratio** the prior considers plausible. So the
regularisation strength is not a free hyperparameter with no interpretation: choosing γ is choosing
how large a maximum Sharpe ratio you are willing to believe exists. Equivalently, the estimator
minimises the Hansen–Jagannathan distance subject to an L2 penalty on SDF coefficients, and maps
into L2-norm-constrained mean-variance weights of the Brandt–Santa-Clara–Valkanov /
DeMiguel–Garlappi–Nogales–Uppal kind.

**Step 4 — the sparsity result, which is the paper's headline and is two-sided.**

- In the space of **characteristics**, sparsity fails. An L1-only (lasso) selection of a few
  characteristics-based factors performs poorly out of sample, and even the dual L1+L2 estimator
  cannot compress the cross-section into a handful of characteristics without losing explanatory
  power. There is **not enough redundancy among known predictors** for a three-, four-, or
  five-characteristic model to summarise the cross-section. (With powers and interactions included,
  moderate sparsity becomes possible — of order a hundred surviving terms out of one to three
  thousand — but that is still not "a few characteristics".)
- In the space of **principal components** of those same factor returns, sparsity works. A model
  containing a small number of high-variance PCs, with the L2 penalty set at its optimum, delivers
  the paper's best out-of-sample cross-sectional fit; setting the coefficients of low-variance PCs
  to zero costs little. Very few PCs — in their tables, the first one carries the highest
  t-statistic and is the last survivor as the L1 penalty is strengthened — supply most of the
  explanatory power. Adding more PCs does not hurt provided the L2 penalty is strong, but it does
  not help much either.

**Step 5 — the asymmetry between the two spaces is the mechanism, not a numerical accident.** There
is no economic reason a few *characteristics* should suffice: present-value or q-theory arguments
motivate why book-to-market and expected profitability jointly matter, but expected profitability is
unobservable and dozens of observable characteristics could each help predict it. There *is* an
economic reason a few *high-variance PCs* should suffice — step 1. So the failure of characteristic
sparsity and the success of PC sparsity are the same statement viewed twice.

A fifth result worth carrying separately: **uncertainty about means dominates uncertainty about
covariances.** They estimate Σ from daily returns, treat it as known, and shrink only the means;
when they allow uncertainty in both, covariance uncertainty has negligible impact on the
coefficients once mean uncertainty is accounted for. The shrinkage that matters is on expected
returns, not on the covariance matrix.

## Construction recipe

Enough detail to build it without re-reading:

1. **Turn each characteristic into a zero-investment managed portfolio.** For characteristic *i* and
   stock *s* at date *t*: cross-sectionally rank `cᵢ,ₛ,ₜ` from 1 to `nₜ` (ties get the average rank),
   divide by `nₜ + 1` to get `rcᵢ,ₛ,ₜ`, then centre and normalise by the sum of absolute deviations:
   `zᵢ,ₛ,ₜ = (rcᵢ,ₛ,ₜ − mean_s rcᵢ,ₛ,ₜ) / Σ_s |rcᵢ,ₛ,ₜ − mean_s rcᵢ,ₛ,ₜ|`. Missing values are replaced
   by the cross-sectional mean, i.e. zero. This makes gross exposure invariant to the number of
   names, and makes the factor insensitive to outliers in the raw characteristic.
2. **Factor returns are `Fₜ = Z′ₜ₋₁ Rₜ`** — one factor per characteristic, rebalanced monthly, with
   daily weights inside the month adjusted so the position behaves as a monthly-rebalanced
   buy-and-hold.
3. **Estimate Σ from daily returns of those factors** (precision here is why they use daily data),
   and μ̄ as their sample mean.
4. **Estimate `b̂ = (Σ + γI)⁻¹ μ̄`.** For factor *selection*, add an L1 penalty and solve the dual-penalty
   (elastic-net-shaped) problem; the L2 half is the economic prior, the L1 half is what produces
   exact zeros.
5. **Choose γ (and the L1 strength) by K-fold cross-validation on the cross-sectional out-of-sample
   R², defined as `1 − (μ̄₂ − Σ₂b̂)′(μ̄₂ − Σ₂b̂)/(μ̄₂′μ̄₂)`** on the withheld fold. They use K = 3, chosen
   as a compromise: larger K makes `b̂` better estimated but leaves too short a withheld sample for
   Σ₂ to be well behaved. With very high-dimensional interaction sets they drop to K = 2 for
   numerical stability of the covariance inverse.
6. **For the PC version, rotate first**: take PCs of the factor return matrix, then run the same
   dual-penalty estimator on the PC portfolios.
7. **Interactions and powers**, if wanted, are built by multiplying two rank-transformed
   characteristics elementwise and re-normalising with the same absolute-deviation rule — without
   re-ranking, so a cube is a genuinely different characteristic with stronger exposure to extremes
   but the same gross leverage.

**The one part that must not be copied here.** Their K-fold CV splits the *whole* historical sample
and therefore uses future information to pick the penalty; the authors say so and are explicit that
the resulting CV R² is upward biased, which is why they add a separately withheld terminal sample
for the final test. That design is illegal under this repo's causality check. Any implementation
here must select γ walk-forward — on data released before the forecast date — or fix it a priori
from the economic prior (step 3 of the mechanism gives a defensible way to do that without any
tuning at all).

## Robustness evidence (qualitative only)

Multi-decade daily US data under three portfolio sets of very different construction (a classic
size/value grid, a 50-anomaly set, an 80-ratio WRDS set), plus two extremely high-dimensional sets
built from powers and interactions; the sparsity conclusions are reported as holding across all of
them. The method is first validated on a case where the answer is known — applied to the 25 ME/BM
portfolios it recovers an SDF resembling the one built by hand in Fama–French (1993) — which is the
right way to earn trust in an estimator. The authors close with a genuinely withheld terminal
sample, not merely cross-validated numbers. Top-tier venue, three authors with track records in
exactly this area, public data and code. Known limits: single market (US), and the paper is about
*explaining* the cross-section rather than about net-of-cost tradeability — transaction costs are
not modelled anywhere in it, and the managed portfolios are long-short by construction.

## Implementability here

The universe is ~145 large-cap names plus 42 ETFs, long-only at gross ≤ 1.0, with 15 bps/side costs
and a walk-forward requirement. Under those constraints:

1. **This source corrects a screen the lab has already run and drawn a general conclusion from.**
   `learnings.md` (2026-08-29) fed eleven features to a penalised linear combiner on the 140-name
   monthly cross-section, got back `rho` 0.774 to the champion at a lower Sharpe, and again with a
   four-feature block got `rho` 0.976 to a single one of its inputs — concluding that a learned
   combiner "reproduces its own best input, worse". That trial regressed **returns on features**
   with a **uniform** L2 penalty. This paper's estimator does something structurally different: it
   maps **mean returns onto covariances**, so the penalty's effect is unequal across PC directions
   by construction. The lab's result is evidence about ridge-on-features at this cross-section size;
   it is *not* evidence about the KNS estimator, and the design rule derived from it ("a learned
   candidate is worth a trial only if its feature block contains no single member that already works
   on its own") is aimed at the wrong failure. **This is a live correction, not a re-import of a
   refuted idea.**
2. **The free screen to run before any of it — and it is the paper's own identifying prediction.**
   Build the lab's existing legs as managed portfolios by step 1 of the recipe, take the daily
   covariance matrix of their factor returns, and check whether **mean returns line up with
   high-variance PCs**: regress each PC's mean return on its eigenvalue rank, or simply report the
   eigenvalue spectrum alongside the PC means and t-statistics. If the lab's leg factors show mean
   returns concentrated in the top PCs, the prior transfers and a KNS-form combiner is worth a
   trial. If the means are unrelated to the eigenvalue ordering — which on a 140-name universe whose
   first PC is likely to be the market and whose legs correlate 0.75–0.85 is a real possibility —
   the prior does not transfer, and that is a finding that closes the idea without spending a trial.
   Costs nothing, uses only train data, and it is the same free-diagnostic shape that has settled
   most of this folder's recent candidates.
3. **The penalty-as-Sharpe-prior is the transferable half even if nothing else is.** The lab has no
   principled way to set a regularisation constant and cannot cross-validate over the whole sample.
   `κ` gives one: pick the largest maximum Sharpe ratio you are willing to assert exists on this
   universe, and it pins γ. That converts a hyperparameter this repo cannot legally tune into a
   stated prior — which is exactly the form `CLAUDE.md` wants a modelling choice to take.
4. **The PC-sparsity result predicts what the lab's own correlation structure already shows.** Five
   long-only family leads correlating 0.75–0.85 with each other is a book-level statement that one
   direction dominates. This paper says that is the *expected* shape, and that the right response is
   to model in the rotated space rather than to hunt for a fifth characteristic. It is also the
   natural formal language for the live `portfolio-learning` question — the leg-count ladder is
   asking, in effect, how many independent directions the lab's leg set actually spans, which is an
   eigenvalue question with a free answer.
5. **Two adaptations forced by the constraints.** (a) The managed portfolios are long-short; the
   book here is long-only, so what is estimable is a *score* and what is tradeable is its top slice.
   The folder's standing framing for `statistical-arbitrage` applies unchanged: removing factor
   structure from the signal does not remove it from the book. (b) With ~8–15 candidate legs rather
   than 50–3400 factors, the high-dimensional problem this estimator was built for barely exists
   here — which cuts both ways. The regularisation matters less, but so does the whole apparatus;
   an honest version of this candidate should say in advance which it expects.
6. **What it does not license.** No performance expectation of any kind — the paper models no costs
   and its portfolios are unconstrained. And "few PCs suffice" is not "few characteristics suffice":
   quoting this source in support of a small hand-picked feature block would invert its central
   finding.

## Related

- `notes/2026-08-29-machine-learning-cross-section-comparative.md` (Gu–Kelly–Xiu) and
  `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` (Freyberger et al.) —
  the folder's other two `statistical-learning` readings; this one disagrees with the second about
  whether characteristic-space sparsity is attainable, and the disagreement is about the *space*,
  not the data.
- `notes/2026-09-03-machine-learning-economic-restrictions.md` — the same night's companion, which
  uses this paper's estimator on portfolios and asks where the profitability of learned signals
  actually lives. Read the two together: this note says what to estimate, that one says how much of
  the estimate survives on a big-stock, cost-paying universe.
- `notes/2026-08-20-parametric-portfolio-policies.md` and
  `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — the L2-constrained
  mean-variance and constraints-as-shrinkage results the estimator maps into; the second explains
  why the long-only cap is itself a shrinkage device.
- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` — the other PC-rotation source
  in this folder, with the opposite use (residuals rather than the leading components).
- `experiments/learnings.md` 2026-08-29 (the penalised linear combiner) — point 1 argues that
  result does not bind here.
