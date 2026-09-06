---
title: "Characteristic-Sorted Portfolios: Estimation and Inference"
authors: Cattaneo, Crump, Farrell, Schaumburg
year: 2020
venue: The Review of Economics and Statistics 102(3), 531–551 (venue tier 1 — top-five general economics journal; the content used here is a theorem plus a mean-square-error expansion, not an anomaly claim, so the replication and multi-market axes of this folder's rubric score it differently than they would an empirical effect)
url: https://doi.org/10.1162/rest_a_00883 — the typeset REStat article read in full from the third author's own page, https://maxhfarrell.com/research/Cattaneo-Crump-Farrell-Schaumburg2020_REStat.pdf
citations: 40 (Crossref `is-referenced-by-count`, checked 2026-09-06); 35 (Semantic Scholar DOI endpoint, same date, whose record dates the paper to the 2018 arXiv version); 19 (OpenAlex, same date). Three indexes, three counts, the usual spread — the Crossref number is the one used below
sample_period: January 1926 – December 2015 (empirical illustration only; the theory is asymptotic in both n and T)
markets: US equities (CRSP; NYSE, AMEX, Nasdaq common shares), single market
tier: A
validation_overlap: false
published_post_2018: true
---

**Read in full**: the published 21-page article, including the estimator definition, the two
rate conditions, the MSE expansion, both optimal-`J` formulas, the feasible grid-search
implementation and remark 9 on factor construction. The supplemental appendix (which carries the
explicit `B`, `V⁽¹⁾`, `V⁽²⁾` expressions) was **not** read; the recipe below is stated at the
level of detail the article itself gives.

First note in this folder on **how many portfolios a sort should cut the cross-section into**.
The folder has covered breadth in the fundamental-law sense (how many independent bets),
weighting schemes, and buffer bands; it has never covered the number of bins as an
*estimation* choice, which is what the lab's own 2026-09-05 result — breadth monotone across a
3x span, arrows pointing the opposite way to `price-trend` — put on the table.

## Mechanism

There is no economic mechanism here. The claim is statistical, and its force comes from
re-describing something the lab does every night as an estimator with a tuning parameter.

Sorting `n` assets into `J` quantile-spaced portfolios and averaging returns within a portfolio
is **partition regression** — a nonparametric estimator of the conditional mean function
`μ(z) = E[return | characteristic = z]`, evaluated at the point `z*` you care about. `J` is its
**bandwidth**, exactly as in kernel regression:

- **Small `J` (wide bins, many names)** → low variance, because a large share of the
  cross-section is averaged into each bin — and **bias**, because the bin also contains assets
  whose characteristic is far from `z*`. The estimate of "the return at the top of the ranking"
  is contaminated by the middle of the ranking.
- **Large `J` (narrow bins, few names)** → low bias, high variance.

The estimand every long-short sort reports, `μ(z_H) − μ(z_L)`, is the difference of two such
estimates. So the customary "deciles, always" is a bandwidth chosen once in the 1970s and never
revisited, and — the authors' central practical point — **`J` should depend on the data**: on
the cross-sectional size `n`, on the length of the time series `T`, on how steep the
characteristic-return relation is, and on how noisy returns are.

The intuition that transfers most directly to this lab comes from their homoskedastic linear
special case (`μ(z) = bz`, constant `σ²`):

> **a steeper relation (larger `|b|`) calls for more portfolios; more idiosyncratic noise
> (larger `σ²`) calls for fewer.**

A strong signal justifies cutting finely, because there is real curvature to resolve; a weak
signal in noisy returns justifies wide bins, because everything you gain in bias you lose twice
over in variance. Note what this says about a score that is *not* a forecast: `b ≈ 0` sends the
optimal number of portfolios toward its lower limit, i.e. toward holding a wide slice.

## Construction recipe

**The estimator.** At each date `t`, sort on `z`, form `J` portfolios at estimated quantiles
(each holding ≈ `n/J` names), take the within-portfolio average return; then average that
time series over `t = 1 … T`. The article insists the portfolios be re-formed from *estimated*
quantiles each period — that randomness is part of the asymptotics, not a nuisance to condition
away. Value-weighting is accommodated as weighted least squares.

**The two rate conditions** for asymptotic normality of the sorted estimator (`d` = number of
sorting characteristics, `d = 1` for a univariate sort):

    J·log(max(J, T)) / n → 0      (bins must not be so many that each is thin)
    n·T / J³ → 0                  (bins must not be so wide that bias dominates)

**The MSE-optimal choices.** Two different objectives give two different rates:

    testing  H₀: μ(z_H) − μ(z_L) = 0        J*  ∝ n^(1/2) · T^(1/4)
    point estimation / factor construction  J** ∝ n^(1/3) · T^(1/3)

with `J** = o(J*)` whenever the cross-section is much larger than the time series — so
**you should cut more finely to test a spread than to build a portfolio from it.** The authors
note the empirical literature already does this informally (Fama–French use few portfolios to
build factors, ten to test).

**The feasible version**, which is what an implementer runs: search a grid of `J` minimising the
sample MSE expansion

    MSE(J) = V̂⁽²⁾ · J^(2d) / (n²T) + B̂² / J²            (testing)
    MSE(J) = V̂⁽¹⁾ · J^d   / (nT)  + B̂² / J²            (construction, remark 9)

where `B̂` and `V̂` are themselves computed at each candidate `J`. No pilot bandwidth is
required and no undersmoothing fudge is used — the authors argue explicitly against the usual
ad hoc undersmoothing, since `J*` is already inference-valid.

**Standard errors.** Two valid estimators are given: a new plug-in, and the ordinary
Fama–MacBeth variance `V̂_FM(z) = T⁻² Σ_t (μ̂_t(z) − μ̂(z))²` — the first proof this folder has
seen that the omnipresent Fama–MacBeth standard error is actually valid in the sorted-portfolio
setting with estimated quantiles. `V̂(z) ≍ J/(nT)`: **the variance of a bin's estimated mean is
linear in `J`**, which is the cleanest statement of what narrowing a band costs.

**Extension worth knowing about.** The framework allows additive linear-in-parameters controls
alongside the sort, which is how they separate a candidate characteristic from an already-known
one (their example includes industry momentum, plus its square and cube, as controls in a
momentum sort). This is the bridge between a sort and a cross-sectional regression, and it is a
way to ask "is this new score anything more than a re-labelling of one I already hold?" inside
the sorting framework rather than by correlating two books' returns.

## Robustness evidence (qualitative only)

The core results are theorems (consistency, asymptotic normality, validity of two variance
estimators, higher-order MSE expansions), so "replication" is not the relevant axis; the proofs
are in the article and its supplement and were refereed at a top-five economics journal.

The empirical illustrations are US-only and are used to demonstrate that the choice bites: for
the two anomalies they revisit, the MSE-optimal number of portfolios **varies substantially with
the cross-sectional sample size**, is generally **well above ten**, and — the finding an
implementer should take — **substantive conclusions change with `J`**. In their data the
cross-section ranges from about 500 to nearly 8,000 names and the optimal `J` for one of the
two anomalies ranges from 13 to 52. Reported subperiod stability is a property of `J`, not of
returns, so nothing dated is imported here.

What is *not* established: nothing about costs, turnover, or the tradability of any bin. The
objective throughout is estimating a conditional mean, never maximising a portfolio's Sharpe
ratio. That gap is the main adaptation risk below.

## Implementability here

**The scaling laws are computable on this repo's constants with no data access at all**, and
this is where the note earns its place. The universe is ~140 instruments; the region-relative
operator the lab's current family lead uses narrows the scoreable pool to ~77; train runs to 666
month-ends. Taking those as `n` and `T`:

1. **The lab's inherited band corresponds to a very small `J`.** `enter-20` out of 140 is
   `J ≈ 7`; out of a ~77-name region pool it is `J ≈ 4`. The 2026-09-05 wide arm (`enter-30`
   of ~77) is `J ≈ 2.6`. So the entire bracket the lab ran lives between `J ≈ 2.6` and
   `J ≈ 7.7` — a range the empirical-finance default (`J = 10`) sits *above*, and the CCFS
   optimum in a 500–8,000-name cross-section sits far above.
2. **Scaling their range down to this universe supports the lab's own direction.** For
   construction, `J** ∝ n^(1/3)T^(1/3)`: moving from `n = 500` to `n = 140` multiplies `J` by
   `(140/500)^(1/3) ≈ 0.65`; for testing, `J* ∝ n^(1/2)`, a factor of `≈ 0.53`. A universe this
   small wants **fewer, wider portfolios** than the literature's defaults, in the same direction
   the lab's breadth bracket found empirically. This is a rate argument with an unknown
   constant, so it is a direction, not a number.
3. **The honest finding is that the asymptotic regime does not exist at `n ≈ 140`.** Plug the
   repo's magnitudes into the two rate conditions: `J·log(T)/n → 0` with `log 666 ≈ 6.5` wants
   `J ≪ 140/6.5 ≈ 21`, while `nT/J³ → 0` wants `J ≫ (140 × 666)^(1/3) ≈ 45`. **The two windows
   do not overlap.** These are limit conditions and not finite-sample inequalities, so this is a
   heuristic reading and is flagged as one — but the direction of the tension is unambiguous:
   with a cross-section this small and a time series this long, there is no `J` that is
   simultaneously fine enough to kill bias and coarse enough to control variance. The practical
   consequence is a *design* rule rather than a tuning rule: **this lab's band width should be
   chosen on economic grounds and held fixed, and the top-bin estimate should be assumed
   bias-contaminated by the middle of the ranking** — which is exactly what a monotone,
   wrong-signed breadth axis looks like when the score is not a forecast.
4. **The feasible MSE grid is runnable here and costs no trial.** `MSE(J) = V̂⁽¹⁾J/(nT) + B̂²/J²`
   needs train-split returns and a score — the same inputs the lab already uses for its
   free top-`k` excess and IC diagnostics — and returns a pre-registered band width per score
   instead of the `hold-30/enter-20` that roughly twenty-five books inherited unexamined. The
   lab's own next-idea list asks for exactly this screen.

**Pitfalls.**

- **The objective is wrong for a trader, in a knowable direction.** CCFS minimise the MSE of an
  estimated conditional mean. A book's Sharpe penalises variance differently, and cost and
  turnover are absent from the expansion entirely. Use the MSE-optimal `J` as a *prior* on band
  width, not as a target to optimise toward.
- **`d > 1` shrinks the feasible window fast.** The rate conditions require `B·d < 2` for
  `T ≍ n^B`; a two-characteristic sort on 140 names is far outside anything the theory covers.
  Single sorts only.
- **The bias term is within-bin heterogeneity**, so it is largest precisely where the
  conditional mean is steepest. If a score's relation to returns is concentrated in a small
  extreme tail, wide bins do not merely dilute — they estimate the wrong thing.
- Nothing in this paper licenses reading a holdout. Every quantity above is a train-split
  computation on a score and its own past returns.

## Related

- The shape question this note cannot answer — *is the relation across bins monotone at all, or
  is the top-minus-bottom spread coming from one end?* — is the subject of
  `notes/2026-09-06-monotonicity-tests-for-portfolio-sorts.md`. CCFS explicitly describe the
  top-minus-bottom test as an *informal* test of monotonicity; Patton–Timmermann is the formal
  one. The two notes are a pair: `J` says how finely to cut, the MR test says whether the cuts
  agree with each other.
- Which end of the ranking a long-only book can use is
  `notes/2026-09-06-long-side-share-of-anomaly-profits.md`.
- Breadth in the fundamental-law sense (`IR ≈ TC · IC · √BR`) is
  `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`. That note's breadth is a
  count of independent bets; this note's `J` is a bandwidth. They are different objects and
  should not be conflated: widening a band raises names held (nominal breadth) *and* raises
  estimator bias, and the fundamental law is silent on the second.
- The lab's own bracket (2026-09-05, three trials across a 3x breadth span in
  `liquidity-volume`, wider strictly better on validation) is the empirical counterpart of the
  "noisy signal calls for fewer portfolios" intuition. The note does **not** import that result;
  it supplies a reason why the sign came out the way it did, and predicts the same sign for any
  other family whose score is closer to a risk ranking than to a forecast.
- Weighting-scheme grading (how many noisily-estimated parameters a scheme needs) is
  `SUMMARY.md`'s cross-family screen #1; the MSE grid adds *one* estimated quantity (`J`) and
  the theory for it, which is the cheapest possible thing to add under that screen.
