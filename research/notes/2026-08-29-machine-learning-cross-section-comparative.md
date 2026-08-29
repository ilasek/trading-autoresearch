---
title: "Empirical Asset Pricing via Machine Learning"
authors: Gu, Kelly, Xiu
year: 2020
venue: The Review of Financial Studies 33(5), 2223–2273 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhaa009
citations: 2323 (Crossref `is-referenced-by-count`, checked 2026-08-29); Semantic Scholar's DOI endpoint returns "not found" for `10.1093/rfs/hhaa009` — the same miss pattern this folder has recorded repeatedly for JF and RFS DOIs
sample_period: 1957–2016 (training 1957–1974, validation 1975–1986, out-of-sample test 1987–2016)
markets: ~30,000 US individual stocks (NYSE/AMEX/NASDAQ), monthly
tier: A
validation_overlap: false
published_post_2018: true
read: full text, NBER Working Paper 25398 (December 2018, revised September 2019), `nber.org/system/files/working_papers/w25398/w25398.pdf`
---

## Mechanism

This is not a strategy paper and has no economic mechanism of its own. It is the field's
reference **comparative-method** study: the same prediction problem — the conditional
expectation of next month's excess return given a high-dimensional feature set — run through
thirteen estimators from OLS to five-layer neural networks, on one dataset, with one honest
out-of-sample protocol. Its value to this lab is entirely methodological, and it answers three
questions the `statistical-learning` family will otherwise answer by trial and error.

**1. Which estimator class, and why.** The ranking is: OLS on the full feature set is worst
(it is actively harmful — its pooled out-of-sample R² is negative); penalised linear models
(elastic net) recover slightly positive predictive R²; **dimension reduction (PCR, PLS) beats
variable selection**; trees and neural networks beat both; and among neural networks, **three
hidden layers is the peak — four and five layers do not improve on it**. The authors attribute
the shallow-beats-deep result to "the comparative dearth of data and low signal-to-noise ratio
in asset pricing problems", explicitly contrasting it with computer vision.

**2. Where the nonlinear gain comes from — interactions, not curvature.** This is the paper's
sharpest diagnostic and the one most easily missed. A generalized linear model with a group-lasso
penalty over **spline expansions of individual features** — i.e. arbitrary univariate
nonlinearity, no interactions — **fails to improve on the purely linear models**, even though it
selects more features than elastic net. The entire advantage of trees and neural nets therefore
traces to *pairwise and higher-order predictor interactions*, not to bending any single feature's
response curve. A Monte Carlo in the appendix confirms the direction: on simulated data where
predictors enter linearly and additively, linear and generalized linear methods dominate; on
simulated data with nonlinear transformations and pairwise interactions, trees and neural
networks dominate. **If a candidate here has no interaction structure, the literature's own
evidence says a penalised linear model is the right estimator and a heavier learner will not
help.**

**3. Why dimension reduction beats selection.** PCR and PLS outperform elastic net, which the
authors read as evidence that "characteristics are partially redundant and fundamentally noisy
signals. Combining them into low-dimension components averages out noise to better reveal their
correlated signals." This is the same averaging-beats-selecting result the folder already holds
from the forecast-combination literature
(`2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
`2026-08-19-bagging-averaging-unstable-predictors.md`), arriving here from a third direction and
now stated about *features* rather than about *models*. It is the strongest prior this note
supplies: on a noisy, redundant feature set, project before you select.

## Construction recipe

The protocol, in enough detail to copy:

- **Feature set.** 94 stock-level characteristics (61 updated annually, 13 quarterly, 20
  monthly), each interacted with 8 macroeconomic time-series predictors, plus 74 industry
  dummies: `94 × (8 + 1) + 74 = 920` covariates. The macro interaction is the device that lets a
  cross-sectional model carry time variation without a separate timing model.
- **Feature standardisation.** Every stock characteristic is **cross-sectionally ranked
  period-by-period and the ranks mapped into [−1, 1]**. This is the whole preprocessing step —
  no winsorising, no z-scoring on a trailing window, no unit-variance scaling. It makes every
  feature scale-free, outlier-insensitive and directly comparable across dates, and it is what
  makes a single pooled model across 30,000 heterogeneous stocks coherent.
- **Splitting.** A fixed three-way split into **training / validation / test**, with the
  validation block used only for hyperparameter tuning and never for evaluation. The authors
  state explicitly that they **do not use cross-validation, in order to maintain the temporal
  ordering of the data**.
- **Refit cadence.** Refit **once per year**, not every month, on the explicit grounds that most
  signals update annually and the algorithms are expensive. At each refit the training sample is
  **extended by one year** (expanding window) while the validation block keeps its size and
  **rolls forward** to the most recent twelve months.
- **Loss.** For OLS, elastic net, the GLM and boosted trees, the **Huber loss** version
  outperforms the squared-loss version. Heavy-tailed returns make the squared-loss objective chase
  outliers; the hybrid quadratic-near-zero / absolute-in-the-tails loss is the cheap fix. The
  appendix's simulation shows Huber loss improving matters most precisely where overfitting is
  worst.
- **Model complexity, observed rather than assumed.** Random forests select **shallow trees, one
  to five levels deep on average**. Boosted-tree ensembles use roughly **30 to 50 distinct
  characteristics** out of the 920. Neither is a model that reads the whole feature set.
- **Evaluation.** Out-of-sample R² is computed against a **zero** benchmark, not against the
  historical mean, on the grounds that historical-average stock returns are so noisy that
  benchmarking against them inflates R² (the authors put the inflation at roughly 3 percentage
  points). Pairwise **Diebold–Mariano tests** are used to compare methods rather than eyeballing
  R² differences.

## Robustness evidence (qualitative only)

- **All thirteen methods agree on which predictors matter, and the agreed set is small.** Two
  independent importance measures (reduction in R² from zeroing a predictor; the sum-of-squared-
  derivatives measure of Dimopoulos et al.) correlate 84%–98% within each model. The rank ordering
  of the top third of characteristics is described as remarkably stable across the thirty
  successive training samples.
- **The agreed ranking, in order.** (i) **Price trends** — five of the top seven overall:
  short-term reversal, twelve-month momentum, momentum change, industry momentum, recent maximum
  return, long-term reversal. (ii) **Liquidity** — share turnover and turnover volatility, log
  market equity, dollar volume, **Amihud illiquidity**, number of zero-trading days, bid-ask
  spread. (iii) **Risk** — total and idiosyncratic return volatility, market beta, beta squared.
  (iv) Valuation ratios and fundamental signals, last. The first three groups are the three
  `program.md` families `price-trend`, `liquidity-volume` and `range-variance`, in that order,
  and the fourth group is the one this repo cannot express at all.
- **Linear and nonlinear models weight that set differently.** Penalised linear and dimension-
  reduction models have importance "highly skewed toward momentum and reversal"; trees and neural
  networks are "more democratic, drawing predictive information from a broader set of
  characteristics". So a linear learner on a broad feature set will tend to *collapse onto the
  trend features*, which is a mechanical reason to expect high correlation with a trend incumbent.
- **The predictability is not a microcap artifact.** Splitting the fitted model's performance
  between the largest 1,000 and the smallest 1,000 stocks each month, tree and neural-network
  methods do **better among large stocks**, which the authors offer as reassurance that machine
  learning "is not merely picking up small scale inefficiencies driven by illiquidity". The
  conclusion states it flatly: machine learning is "most valuable for forecasting larger and more
  liquid stock returns and portfolios". For a survivorship-biased universe of large global names,
  this is the most favourable robustness result in the paper.
- **Costs.** Not modelled. The paper reports gross long-short decile spreads and notes only in
  passing that value-weighted portfolios are "less sensitive to trading cost considerations", with
  an appendix table excluding microcaps from the equal-weighted results. **There is no
  turnover accounting anywhere in it.** Treat every economic-gain claim in it as a gross number.
- **Multiple testing.** Acknowledged in the framing (the paper's stated motivation is partly the
  false-discovery problem in the characteristics literature) and handled at the method-comparison
  level with Diebold–Mariano tests and a Bonferroni adjustment, under which "neural networks
  become only marginally significant over penalized linear models". That is an unusually honest
  line and it should temper any expectation that the deep model is reliably the better one.
- **Replication status.** The paper is itself the reference point that later work replicates
  against rather than a claim awaiting replication, and it is a decade inside the McLean–Pontiff
  decay window for the characteristics it uses
  (`2026-08-17-mclean-pontiff-publication-decay.md`). Its `published_post_2018: true` flag is
  live: the out-of-sample window ends in 2016, so the *paper* cannot leak this lab's validation
  window, but the method choices it endorses were selected with knowledge of results through 2016.

## Implementability here

**In scope, and the constraints bind in a specific direction.**

- **Feature count.** The lab has ~145 instruments and no fundamentals. Of the four important
  groups above, group (iv) is unavailable and group (ii) is only partly available (turnover,
  dollar volume, Amihud illiquidity, zero-volume days are computable from the new `aux` panel;
  bid-ask spread and market equity are not). The reachable feature space is therefore groups
  (i)–(iii) minus a few members — a few dozen features at most, against 920 in the paper, on a
  cross-section 200× smaller. **This is the regime where the paper's own evidence says a
  penalised linear model or a dimension-reduction step is the right estimator**, which is what
  `CLAUDE.md` already tells a candidate to try first. This note supports that instruction rather
  than arguing against it.
- **The rank-to-[−1,1] transform is free and should probably be the default.** It costs nothing,
  is trivially causal (it uses only the current cross-section), removes the need for any trailing
  normalisation window, and is what makes a pooled model across regions and asset types
  (stocks *and* ETFs, 15 currencies) defensible. `strategies/lib/features.py` already has
  cross-sectional normalisation helpers.
- **Refit annually, not monthly, and say so.** The paper refits once a year with an expanding
  training window and a rolling validation block — and it is running a far larger model than
  anything possible here. `CLAUDE.md`'s clock budget (~60s per `generate_weights` call, called
  about seven times per trial) points the same way. The lab's first `statistical-learning` scout
  refit monthly and paid 15.4× annual turnover for it; an annual refit is both cheaper to run and
  closer to the reference protocol.
- **The direct warning about turnover, which the paper does not give.** GKX predicts *returns*
  and sorts on the prediction. Nothing in that objective asks the holdings to be stable, and the
  paper never pays for the instability because it never charges costs. `learnings.md` has already
  measured what that costs here (the ridge scout's monthly re-ranking of the whole cross-section
  cost roughly a third of its margin over the equal-weight floor). **Predicting returns well and
  holding a tradeable book are different objectives**; the folder's own
  `2026-08-20-parametric-portfolio-policies.md` and
  `2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` are the bridge, and this note
  should be read together with them rather than alone.
- **Feature redundancy with the incumbent is a design variable, not an accident.** The lab has
  already observed that feeding a learner the champion's own lookbacks reproduces the champion
  at higher correlation and lower Sharpe. GKX explains the mechanism: a penalised linear model on
  a feature set containing momentum will load on momentum, because that is where the marginal
  signal is. **If the point of a `statistical-learning` candidate is a decorrelated leg, the
  price-trend features have to be excluded or orthogonalised deliberately** — the estimator will
  not do it for you.
- **What the paper says is worth trying and this repo has not.** (a) **Huber loss instead of
  squared loss** — a one-line change in scikit-learn (`HuberRegressor`, or `loss="huber"`), with
  a documented tier-1 finding behind it. (b) **PCR/PLS on the feature block** rather than
  selection — `sklearn.cross_decomposition.PLSRegression` and `PCA` are both deterministic and
  cheap, and the paper's finding is that this specific step is where linear methods gain most.
  (c) **Macro-interaction structure** — a small number of slowly-moving global state variables
  (this repo cannot see the paper's eight, but it can construct market-level dispersion or
  aggregate volatility from its own panel) interacted with the stock features, which is the
  paper's device for time variation and is the closest available analogue to the regime-switching
  ideas `learnings.md` has already refuted in their binary form.

**Known pitfalls.** The out-of-sample R² values that separate these methods are *fractions of a
percent per month*. Do not expect a candidate here to separate estimators on this repo's much
smaller cross-section — the paper's own effect sizes say that comparison is underpowered at
n = 145, and a trial spent ranking estimators is a trial spent on noise. The reachable question
is which *feature groups* carry signal, which is also what `program.md` says the interesting
question is.

## Related

- `2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
  `2026-08-19-bagging-averaging-unstable-predictors.md`,
  `2026-08-19-model-averaging-mallows-weights.md` — the averaging-beats-selecting result, here
  restated about features rather than models.
- `2026-08-20-parametric-portfolio-policies.md` — the alternative to predict-then-sort: optimise
  the realised objective directly. The counterweight to this note's protocol.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md` — the liquidity block that ranks
  second in this paper's variable importance, and what a replication says about its best-known
  member.
- `2026-08-29-range-based-volatility-estimators.md` — the risk block that ranks third, and how to
  estimate it from the daily bar this repo now receives.
- `2026-08-24-multiple-testing-haircut.md`, `2026-08-24-deflated-sharpe-ratio.md` — why "thirteen
  methods, pick the best" is a multiple-testing problem, which this paper handles with
  Diebold–Mariano tests and this lab handles with the deflator.
