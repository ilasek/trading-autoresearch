---
title: "Bayes-Stein and empirical-Bayes shrinkage of an estimated mean vector"
authors: Jorion (1986); Frost & Savarino (1986); Bock (2018, horserace and recipe source)
year: 1986
venue: Journal of Financial and Quantitative Analysis (Tier 1, both 1986 papers); Bock 2018 is an uncited Warwick Business School working paper on arXiv (Tier 4 on the rubric — see Robustness)
url: https://doi.org/10.2307/2331042 (Jorion) · https://doi.org/10.2307/2331043 (Frost–Savarino) · https://arxiv.org/abs/1811.08255 (Bock)
citations: Jorion 989 (Semantic Scholar, checked 2026-09-30) / 1013 (OpenAlex, checked 2026-09-30); Frost–Savarino 410 (Semantic Scholar, checked 2026-09-30) / 411 (OpenAlex, checked 2026-09-30); Bock **0** (Semantic Scholar, checked 2026-09-30; OpenAlex daily budget was exhausted, so unconfirmed there)
sample_period: Jorion and Frost–Savarino — not established, primaries not read (see Access). Bock's six datasets run 06/1963–03/2018 and 02/1995–03/2018.
markets: Jorion/Frost–Savarino not established; Bock — US portfolio-level and stock-level datasets
tier: A for the estimator (Tier-1 venue, ~1000 citations, universally re-implemented) / C for the tradable claim that it beats naive diversification (see Robustness)
validation_overlap: true (Bock's datasets end 03/2018, so they touch the first quarter of the lab's validation window; the two 1986 primaries cannot overlap it)
published_post_2018: false (1986; Bock is September 2018)
---

## Access — what was and was not read

**Neither 1986 primary was read.** Both are closed: OpenAlex reports no open-access location for
either DOI (two locations each, both `is_oa: false`), Semantic Scholar reports
`openAccessPdf: CLOSED`, and `cambridge.org/core` returned an 860 KB **HTML bot page** in place of
its PDF endpoint — the refusal mode this folder recorded on 2026-09-18, confirmed again today.
Routes tried and failed, recorded so the next session does not repeat them:

- `merage.uci.edu/~jorion/` — **HTTP 404**; the whole `~jorion` tree is gone from the Merage
  school's site, so the 2026-09-18 faculty-page trick does not work for this author.
- `publikationen.ub.uni-frankfurt.de` — **HTTP 200 with a 7.4 KB Anubis proof-of-work challenge**
  (`within.website/x/xess` stylesheet, title "Making sure you're not a bot!"). This is a **tenth
  distinct refusal shape** for this folder's records, and like the Incapsula case of 2026-09-18 it
  **returns 200**, so the careless reading is "the file is small" rather than "blocked". Check the
  body before parsing.
- `www-2.rotman.utoronto.ca/~kan/papers/` — **HTTP 200 serving a 1.6 KB Rotman 404 handler** for
  every path tried. Kan's paper directory is gone; this matters beyond tonight, because that
  directory is the standard open route to the Kan–Zhou estimation-risk papers.
- A `.edu`/`.ac.uk` targeted search returned only third-party papers that cite Jorion, no hosted copy.

**What was read in full:** Bock (2018), from arXiv, which states Jorion's estimator in full
(its Eq. 6–8) and runs it in a sixteen-strategy horserace. The README permits this substitution
provided the note says the primary was not read. It does. **Nothing below is attributed to Jorion's
own argument, only to his estimator as a third party states it**, and Frost–Savarino's construction
is reported from their published abstract alone — which is thin, and flagged as such.

## Mechanism

An estimated mean vector is the noisiest input to any portfolio rule, and the noise is not
symmetric in its consequences: an optimiser **maximises over** the estimates, so it systematically
loads on whichever names had the luckiest sample mean. The estimation error is therefore converted
into position size rather than averaged away, and it gets worse as the number of assets grows
relative to the sample length.

Stein's insight is that when you estimate many means at once, the *vector* of sample means is
inadmissible under quadratic loss even though each component is individually unbiased: pulling every
component toward a common target reduces total expected loss, because the variance you remove
exceeds the bias you add. The finance version makes the target a portfolio-relevant central value
rather than zero, and makes the pull strength a function of how dispersed the estimates actually are
— if the cross-section of estimated means is tightly clustered, almost all of its spread is noise
and the estimator shrinks hard; if it is genuinely dispersed relative to sampling error, it shrinks
little. **The intensity is data-determined; there is no tuning constant.** That is the property that
makes this class interesting for a lab that is trying not to add free parameters.

## Construction recipe

**Jorion's Bayes-Stein estimator** (as stated by Bock 2018, Eq. 6–8; `N` assets, `M` observations):

```
mu_bs   = (1 - phi) * mu_hat + phi * mu_min * 1
phi     = (N + 2) / [ (N + 2) + M * (mu_hat - mu_min*1)' * Sigma_inv * (mu_hat - mu_min*1) ]
mu_min  = mu_hat' w_min            # mean of the minimum-variance portfolio
```

Four details that are easy to get wrong and that matter more than the headline:

1. **The shrinkage target is not the equal-weighted grand mean.** It is `mu_min`, the *expected
   return of the minimum-variance portfolio* — a scalar, but a covariance-weighted one. A great deal
   of casual secondary writing says "shrink toward the grand mean"; the estimator says otherwise.
2. **The distance in the denominator is Mahalanobis, not Euclidean.** The pull depends on
   `(mu - target)' Sigma_inv (mu - target)`, so two score vectors with identical cross-sectional
   spread can get very different intensities depending on whether their dispersion lies along
   high-variance or low-variance directions of the covariance.
3. **`phi` falls as `M` rises and rises with `N`.** More data shrinks less; more assets shrink more.
   With `N` large relative to `M`, `phi` approaches 1 and the estimator approaches the target.
4. Jorion additionally recommends the scaled covariance `Sigma_hat * M / (M - N - 2)` rather than the
   raw sample covariance (Bock 2018, footnote 2).

**Frost–Savarino's empirical-Bayes estimator** is the same idea under a fuller conjugate prior: the
prior asserts that **all securities are identical** — same expected return, same variance, same
pairwise correlation — so the posterior draws the estimates toward the **average return, the average
variance, and the average correlation** of the population simultaneously. Jorion shrinks the mean
only; Frost–Savarino shrink all three moments toward their cross-sectional averages. *This paragraph
is from the published abstract; the paper was not read, and no intensity formula is claimed for it.*

## Robustness evidence (qualitative only)

**Grade the claim, not the paper** — the 2026-09-29 rule, and this cluster is a second clean
instance of it.

The *estimator* is Tier A in every sense: a Tier-1 venue, roughly a thousand citations, and it is
re-implemented as a standard benchmark in essentially every subsequent horserace, which is as close
to routine replication as a statistical construction gets.

The *tradable claim* — that shrinking the estimated mean makes an optimised portfolio beat naive
diversification out of sample — does not survive. Bock (2018) tests sixteen strategies across six
datasets, including plain Bayes-Stein, Bayes-Stein with short-sale constraints, and norm-constrained
Bayes-Stein, and reports that **none of them consistently outperforms 1/N or minimum-variance** on
Sharpe ratio, certainty-equivalent return or turnover. This corroborates rather than contradicts
DeMiguel–Garlappi–Uppal (2009), which the folder already holds
(`2026-08-17-naive-vs-optimized-weighting.md`).

The diagnosis both give is the one worth carrying: **shrinking the mean is not enough, because the
residual estimation error in expected returns still dominates the optimisation.** Bock's own stated
implication is that research effort should go either into better estimation of expected returns, or
into **diversification rules that do not require estimating expected returns directly** and instead
use other stock characteristics. Note that this is a verdict on *mean-variance optimisation with a
shrunk mean*, not on shrinkage as an operator — the lab does not run an optimiser at all, which is
exactly why the transfer below has to be argued rather than assumed.

**Weight Bock correctly, and that means barely.** Semantic Scholar returns **zero citations**
(checked 2026-09-30) for a paper from 2018 — a single-author working paper that the literature has
not taken up, which the rubric puts at Tier 4 (credible only with fully reproducible methodology),
not Tier 2. **The verdict above therefore rests on DeMiguel–Garlappi–Uppal (2009), which is Tier 1
and already in this folder; Bock is corroboration from an independent hand, not evidence in its own
right.** Its load-bearing use here is narrower and safer than its horserace: it is a *transcription
source* for a famous estimator, and a transcription can be checked against the estimator's known
structure, which this one passes. Nothing in this note depends on a number Bock computed.

## Implementability here

The lab does not solve a mean-variance problem, so the estimator cannot be imported as written.
What can be imported is the operator: **shrink a cross-sectional score vector toward a target with a
data-determined intensity.** Here is the part that decides whether that is worth a trial, and it is
algebra on the lab's own weighting function, not a measurement.

The champion weights names by `c - c.min() + FLOOR` (normalised). Apply a scalar-target linear
shrink `c' = (1-phi)*c + phi*m` for any scalar `m`. Then:

```
c' - c'.min() = (1-phi)*c - (1-phi)*c.min() = (1-phi) * (c - c.min())
w_i           ∝ (1-phi)*d_i + FLOOR ,   where d_i = c_i - c.min() >= 0
              ∝ d_i + FLOOR/(1-phi)
```

**So shrinking the score toward any scalar target is exactly equivalent to raising `FLOOR` to
`FLOOR/(1-phi)`, and changes nothing else.** As `phi -> 1` the book goes to equal weight; as
`phi -> 0` it is unchanged. A Jorion-style candidate built on a scalar target is therefore **a
reparametrisation of a knob the lab already has**, not a new mechanism, and the whole family it spans
has already been swept whenever `FLOOR` was swept. **This is a free kill: it should cost zero
trials.** It also says something the lab may not have noticed — `FLOOR` *is* a mean-shrinkage
intensity, and the seat's concentration (61.41% of gross in ten names, ratio 0.023, [2026-09-27]) is
a statement about where on that shrinkage path the book already sits.

What is **not** spanned by `FLOOR`, and is therefore where any real content lives:

- **A vector-valued target.** If `mu_0` is not proportional to `1` — shrink each name toward its
  **region or sector mean** rather than toward a global scalar — the algebra above breaks and the
  operator genuinely re-ranks. The folder already holds the `phi = 1` endpoint of exactly this map
  (`2026-09-10-country-demeaned-versus-country-mean-characteristics.md`, full demeaning) and the
  `phi = 0` endpoint (the raw score). **Bayes-Stein supplies the missing middle with a
  data-determined intensity and no new free parameter** — that is the one candidate shape in this
  note, and it is a partial, estimated demean rather than a new signal.
- **The Mahalanobis metric.** The intensity uses `Sigma_inv`, so it is not a per-name scalar
  operation; on a 140-name universe with a daily panel, `Sigma_hat` is estimable but ill-conditioned,
  and the folder's own shrinkage/eigenvalue notes ([2026-09-27]) are the right prerequisite. A
  candidate that swaps in a Euclidean distance has changed the estimator and should say so.
- **A non-convex combination.** See the companion note
  (`2026-09-30-optimal-shrinkage-of-a-high-dimensional-mean-vector.md`): the asymptotically optimal
  linear shrinkage is `alpha*mu_hat + beta*mu_0` with **`alpha + beta` not constrained to 1**, which
  is strictly more general than the convex `phi` form and is not a `FLOOR` reparametrisation even for
  a scalar target.

Pitfalls. (i) `phi` depends on `N` and `M`; at a monthly rebalance with a multi-year window,
`N = 140` against `M` of a few dozen to a few hundred months puts this estimator in precisely the
regime where the sample covariance is unusable — prefer the daily panel or a shrunk covariance.
(ii) Everything here must be recomputed inside the walk-forward loop; a `Sigma_inv` or a `phi` fitted
once over the visible window is the classic lookahead the causality check is built to catch.
(iii) The horserace verdict above is a real prior: two independent studies say this operator class
does not rescue an optimiser. The lab is not an optimiser, but nobody has shown it helps a
magnitude-weighted long-only book either, and this note does not claim it does.

## Related

- `2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal (2009); the Tier-1 statement
  of the same negative, and the reason the tradable claim here is graded C.
- `2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — the `phi = 1` endpoint of
  the group-mean-target version proposed above.
- `2026-09-30-optimal-shrinkage-of-a-high-dimensional-mean-vector.md` — the modern, distribution-free
  version of this estimator, and the reason the convex form is not the general one.
- `2026-09-30-shrinking-portfolio-weights-toward-a-target.md` — the same operator applied in weight
  space instead of score space.
- `2026-09-27-nonlinear-shrinkage-instead-of-counting.md`, `2026-08-21-weight-constraints-as-covariance-shrinkage.md`
  — the folder's covariance-side shrinkage notes; this is the mean-side gap they left.
- `2026-09-15-tweedies-formula-empirical-bayes-selection-bias.md` — empirical Bayes applied to a
  *selected* maximum rather than to the whole vector; a different use of the same machinery.
