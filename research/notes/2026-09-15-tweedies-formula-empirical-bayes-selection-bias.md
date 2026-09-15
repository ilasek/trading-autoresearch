---
title: "Tweedie's Formula and Selection Bias"
authors: Efron
year: 2011
venue: Journal of the American Statistical Association (Tier 1)
url: https://doi.org/10.1198/jasa.2011.tm11181 ; working paper read at https://stacks.stanford.edu/file/druid:vc631wx1024/BIO%20256.pdf
citations: 1015 (Semantic Scholar by DOI, checked 2026-09-15); 418 (OpenAlex, same date); 393 (Crossref, same date)
sample_period: n/a — statistical theory. Its worked examples are a simulation and a genomics copy-number-variation dataset; **no market data in the paper**
markets: none (methods paper)
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full** as Stanford Division of Biostatistics Technical Report 256 (March 2011), 24 pages,
complete and text-extractable. Access note: the author's own page
(`efron.ckirby.su.domains/papers/2011TweediesFormula.pdf`) **could not be reached from this
environment** — three attempts, each failing at the transport layer with the agent proxy reporting
`ws_closed_mid_exchange` rather than any HTTP status. That is a **fourth distinct refusal mode** for
this folder's records, after the Cloudflare 403 challenge, OpenAlex's metered budget and
`pm-research.com`'s OpenID redirect: a tunnel that dies with no status at all. It should be reported
as a transport failure against one host, not as a paywall and not as an egress block — the Stanford
`stacks` mirror of the same content served it instantly on the first try. **Generalise: when an
author page dies without an HTTP code, look for the institutional repository's copy of the same
technical report before concluding anything about access.**

This is the second of this session's two corrections for a selected maximum. The first
(`2026-09-15-inference-on-winners-post-selection-estimation.md`) assumes nothing about the
distribution of true effects and conditions on the selection event. This one goes the other way: it
**estimates the distribution of true effects from the ensemble itself** and uses it to shrink. The
two are not substitutes, and the first note records exactly when this one fails.

## Mechanism

Observe `N` possibly correlated normal estimates, each with its own unknown mean:

    z_i ~ N(µ_i, σ²),  i = 1 … N

Attention then falls on the extremes — the largest few `z_i`. Those are large for **two** reasons:
their `µ_i` really are large, *and* they got lucky. The paper's phrase for why this creates bias is
the one to carry: **"the evanescence of the luck factor"**. The luck does not persist into the next
sample; the `µ_i` does. So the selected `z_i` overstate their `µ_i`, and the selected `µ_i` lie
closer to the centre of the observed distribution than the selected `z_i` do. Efron names this
plainly as **regression to the mean**, which is the oldest description of the effect and the one
this folder had no note on at all.

**Tweedie's formula** (Robbins 1956, crediting Tweedie) gives the posterior mean in closed form.
With `µ ~ g(·)` and `z | µ ~ N(µ, σ²)`, and `f(z)` the *marginal* density of `z`:

    E{ µ | z } = z + σ² · l'(z),    where  l(z) = log f(z)

The correction is the derivative of the log marginal density at the observed value. **The crucial
advantage is that it needs only `f`, never `g`.** There is no deconvolution: you never have to
estimate the prior distribution of true effects, only the observed distribution of estimates, which
you have in front of you. Where the log-density is falling steeply — i.e. out in a thin tail — `l'`
is large and negative and the shrinkage is large. Where the density is flat, there is nothing to
shrink toward and the correction is small. That is the entire mechanism, and it is why the formula
does the right thing automatically: **an estimate is shrunk in proportion to how unusual it is
relative to the population it was selected from.**

## Construction recipe

**The empirical-Bayes version.** All `N` observations are used to fit a smooth estimate of
`log f(z)`, and the correction is its derivative:

    µ̂_i = z_i + σ² · l̂'(z_i)

Efron's implementation:

1. Bin the `N` observed `z` values into a histogram.
2. Fit the **log of the bin counts** by Poisson regression on a smooth basis in `z` — he uses a
   natural spline with `J = 5` degrees of freedom, and reports that a polynomial form of the same
   order made little difference.
3. Differentiate the fitted `l̂(z)` analytically and evaluate at each selected `z_i`.
4. The same fit gives the posterior variance: `σ²·[1 + σ²·l̂''(z_i)]`. A concave `l̂` implies a
   posterior variance *smaller* than `σ²`.

**The `J = 2` case is the James–Stein estimator**, and this is the part to implement first when `N`
is small. If the prior is normal, `µ ~ N(0, A)` and `z | µ ~ N(µ, 1)`, the marginal is `N(0, V)`
with `V = A + 1`, so `l'(z) = −z/V` and Tweedie's formula collapses to a pure multiplicative
shrink:

    E{ µ | z } = ( 1 − 1/V ) · z

James–Stein substitutes the unbiased estimator `(N − 2)/Σ z_j²` for `1/V`:

    µ̂_i = ( 1 − (N − 2)/Σ z_j² ) · z_i

Efron's recipe differs only in using the MLE `N/Σ z_j²` instead. **So the whole apparatus, at its
simplest, is one scalar: shrink every estimate toward the ensemble mean by a factor estimated from
the ensemble's own spread.** A fancier `J` only lets the shrinkage vary with `z` — which is what
you want when the marginal distribution is not normal (Efron's genomics example is bimodal and a
sixth-degree polynomial fits it).

**Relevance — the modification that decides whether any of this is legitimate.** A hidden
assumption above is that all `N` other cases are *relevant* to estimating any particular `µ_i`.
Efron devotes a section to relaxing it. Introduce a covariate `x` on which the prior depends, a
target value `x_0`, and a relevance function `ρ(x_0, x)` giving the probability that case `x`'s
prior equals the target's. The corrected formula gains a second term:

    correction = σ²·l'(z)  +  σ²·( log ρ(x_0 | z) )'

and `ρ̂` is fitted the same way `l̂'` was. The practical form of the warning is simpler than the
algebra: in his genomics example, restricting the "relevant" set from all 5000 cases to various
subsets **moved the corrected estimate around by an amount comparable to the correction itself** —
he calls those differences "not drastic", and then says in terms that *other data sets might make
relevance considerations more crucial*. **Which ensemble you shrink toward is a modelling choice,
not a detail.**

## Robustness evidence (qualitative only)

- The formula is exact Bayes, not an approximation: if `g` were known, `E{µ|z}` would be right and
  the whole problem would be over — Efron notes that "Bayes rule is immune to selection bias". All
  the risk is in the *empirical* step of estimating `l'` from finitely many observations.
- Efron's simulation check is a fair one: 100 replications, correcting the 20 largest and 20
  smallest in each. The corrected differences are much more tightly centred on zero than the
  uncorrected ones, in **both** tails — so the method is not a one-sided fudge. He also reports that
  bias correction usually costs variance but did not here, the corrected differences being if
  anything *less* variable.
- **Correlation does not break it.** The algorithm does not require independence; fitting methods
  like the Poisson-regression one still give nearly unbiased estimates of `l̂` for correlated `z_i`,
  with **increased variability** relative to the independent case. Efron's framing: the "empirical
  Bayes information per other observation is reduced by correlation". This matters enormously for
  the intended use here and is the single most important robustness fact in the paper for this repo.
- **The binding limit is `N`.** Every worked example has `N` in the thousands (5000 simulated
  values; 5000 genomic markers). The method's whole premise is that the marginal density can be
  estimated well from the ensemble, and a spline fit to a few hundred points in a tail cannot be.
  Efron's own accuracy section is built around defining how much information each "other"
  observation carries.
- **The external limit, from the other note in this session.** Andrews–Kitagawa–McCloskey find that
  empirical-Bayes corrections of this family **reduce but do not eliminate** selection bias, and
  give the reason: a standard empirical-Bayes correction amounts to a normal prior on the effects,
  which corrects the winner's curse when that prior matches the truth and not in general otherwise.
  Read together with the `J = 2` result above, this is a sharp statement: **the James–Stein form is
  exactly the case whose implicit prior is normal, so it is exactly the case that inherits that
  limitation.** The escape is a larger `J` — which needs a larger `N`, which is the limit above.

## Implementability here

The honest assessment is **"the mechanism transfers, the estimator mostly does not — at one
ensemble size, and in one form."**

- **Where it works: within one specification curve, and only in the James–Stein form.** The
  2026-09-14 nightly produced 178 train Sharpes of a single construction. That is a genuine
  ensemble of exchangeable-ish estimates, and the `J = 2` shrink is one line: compute the spread of
  the 178 values about their mean, form the shrink factor, apply it. The interesting output is not
  the shrunk argmax but **the shrinkage factor itself**, which says what fraction of the curve's
  spread the ensemble thinks is noise rather than real construction differences. That is a
  decomposition of the 0.079 NSE the lab has no other way to get, and it costs nothing.
- **Where it does not work: across the trial history.** The repo has ~91 trials, not 5000, and — far
  more damaging — they are **not exchangeable**. They span eight families, two tracks, several
  universes and six weeks of deliberate design changes. Efron's relevance section is precisely about
  this, and the answer it gives is that shrinking a `statistical-learning` result toward a pool
  dominated by `price-trend` variants is a modelling assertion, not a correction. **The lab should
  not shrink its leaderboard.** If it ever does, the relevance set must be argued and stated first.
- **The complementarity with the session's other note is the practical point.** The conditional
  method needs the covariance `Σ` and the selection rule but makes no distributional assumption; the
  Tweedie method needs neither `Σ` nor the selection rule but needs a large, exchangeable ensemble.
  For 178 correlated variants of one construction, the ensemble exists but `Σ` is also computable,
  and the conditional method is the better-founded of the two. For a case where the selection rule
  is murky (a construction chosen partly by judgement), Tweedie is the one that still applies —
  because it never conditions on how the winner was picked.
- **A diagnostic the lab can read for free even if it never applies either correction.** Efron's
  formula says the shrinkage at `z` is `σ²·d/dz log f(z)`. Fit the log-density of *any* score
  distribution the lab already computes and the derivative at the top of the range says how fast the
  density is thinning there — i.e. how much of a top-band selection is luck. This is the same
  statement as "the correction is governed by the winner-to-runner-up gap" from the other note,
  arrived at from the density side, and it applies to the lab's **cross-sectional** rankings
  (which name is best this month) as readily as to its construction curves. That connection is
  unexplored and is the most interesting thing this note opens.

**Pitfalls.**

- `σ²` is assumed known and constant. For Sharpe estimates it is neither — see
  `2026-08-23-statistics-of-sharpe-ratios.md`. Efron has a remark on non-constant `σ`; it is an
  extension, not a free pass.
- The correction is only as good as the marginal-density fit, and a spline fit is worst exactly
  where it is needed most: in the tail, where the counts are smallest.
- Shrinking a maximum and then comparing it to an *unshrunk* incumbent is worse than shrinking
  nothing. Any application must apply the same operator to both sides.
- **No trial, no candidate, no holdout.** Everything here is arithmetic on numbers already computed.

## Related

- `2026-09-15-inference-on-winners-post-selection-estimation.md` — the session's other correction,
  which conditions rather than shrinks, and which supplies this note's binding external caveat.
- `2026-09-15-reality-check-max-statistic-under-dependence.md` — the testing complement to both.
- `2026-08-25-hierarchical-bayesian-factor-replication.md` — the folder's existing empirical-Bayes
  coverage, which fits a prior to a published literature; this note supplies the estimator that
  work rests on, and the reason the *source* of the ensemble is the whole argument.
- `2026-08-24-deflated-sharpe-ratio.md` — the folder's existing winner's-curse coverage, whose
  closed form assumes independence; Efron's algorithm explicitly does not.
- `2026-09-11-parametric-portfolio-policies-standardized-characteristics.md` and
  `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the other two
  notes about what an operator does to a cross-section of scores. Shrinkage is a third such
  operator and, unlike winsorizing, it is not undone by a subsequent rank.
