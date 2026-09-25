---
title: "Deep Learning Statistical Arbitrage"
authors: Guijarro-Ordonez, Pelger, Zanotti
year: 2022 (working paper draft read); published in Management Science
venue: Management Science — Tier 1 (peer-reviewed); read as the arXiv/SSRN working paper
url: https://arxiv.org/abs/2106.04028 (published version DOI https://doi.org/10.1287/mnsc.2022.03132)
citations: 32 (Semantic Scholar, SSRN record `10.2139/ssrn.3862004`, checked 2026-09-25); 13 (Crossref, same SSRN record) and 3 (Crossref, the Management Science DOI) — the usual split-record undercount, see Robustness below
sample_period: residuals 1998–2016; out-of-sample trading evaluated 2002–2016
markets: US equities — the ~550 largest and most liquid names (market cap above 0.01% of total, the Kozak–Nagel–Santosh screen), roughly S&P 500 scale
tier: B
validation_overlap: false
published_post_2018: true
---

**Text read**: the 41-page arXiv working paper (v2, draft dated September 2022), in full —
the conceptual framework of Section II, the factor-model and signal specifications of Section III,
and the market-frictions extension. The Management Science version of record was not read.

## Mechanism

The paper's durable contribution is a **decomposition of what a statistical-arbitrage strategy
is**, into three separately-choosable functions. Almost every construction in this family is a
particular choice of each, and naming them separately is what makes the design space searchable:

1. **Arbitrage portfolio** — a *residual*. For each name `n`, fit a factor model and take the
   residual `eps_n,t`. Economically this is a relative trade: long the name, short a
   **mimicking portfolio** with the same factor loadings. The choice of factor model *is* the
   choice of what "similar" means — PCA factors make the mimicking portfolio the combination of
   names with the most correlated return history (which is why PCA residuals and a clustering
   approach are close to the same idea); characteristic-based factors make it the combination with
   the most similar fundamentals. The asset-pricing argument for why residuals should revert at
   all: under a correct factor model, residual portfolios earn no risk premium, so their
   unconditional mean is zero and any deviation must be temporary. The authors note the strategy
   does not *depend* on the model being correct — with an omitted factor the trade simply exploits
   deviations from the factors that were captured.
2. **Arbitrage signal** — a function of the **last `L` residual returns**, i.e. of the *path* of
   the cumulative residual, not of its current level alone. This is the paper's sharpest framing
   point: the classical Ornstein–Uhlenbeck-plus-threshold rule (Avellaneda–Lee) is a signal
   function that compresses that whole path into essentially **two numbers** — the current
   deviation from the fitted long-run mean, and a goodness-of-fit measure — and every other
   feature of the path is discarded before the trading decision is made. The signal is a
   *sufficient statistic* for the policy: two residuals with the same signal must get the same
   weight, so whatever the signal throws away is unrecoverable downstream.
3. **Trading policy** — a map from signal to weight, solving a utility maximisation with the
   constraints and frictions written **into the objective**. This is where leverage, turnover
   penalties and short-sale penalties live.

The empirical part replaces (2) with progressively richer time-series models — a Fourier
decomposition feeding a feed-forward net, then a convolutional network with a transformer
attention layer — while holding (1) and (3) fixed, which is a clean ablation design.

## Construction recipe

Implementable pieces, stripped of the network architecture:

- **PCA residuals (the branch reachable without fundamentals).** At each date, estimate the
  correlation matrix from the **last 252 trading days**; extract the top `K` eigenvectors; form
  eigen-portfolio weights as `v_m^i / sigma_i` (the Avellaneda–Lee volatility rescaling); then
  regress each name's returns on those factors over the **last 60 days** to get loadings, and
  compute the residual for the current day out of sample. `K` swept over {1, 3, 5, 8, 10, 15}.
- **Fama–French-style residuals**: loadings by OLS on the **last 60 days** (the Carhart
  procedure), `K` ∈ {1, 3, 5, 8}.
- **A `K = 0` control**: run the identical signal and policy on *raw* excess returns rather than
  residuals. This is the single most valuable design element in the paper for a lab that has to
  justify residualisation at all — it prices the residualisation node in isolation.
- **Signal window** `L = 30` trading days of cumulative residual returns; checked at `L = 60`.
- **Pool rule**: only names with no missing observations inside the rolling window, which on a
  large-cap screen removes at most ~2% of names.
- **Frictions, written into the training objective**, not applied afterwards:
  ```
  cost(w_t, w_t-1) = 0.0005 * ||w_t - w_t-1||_1  +  0.0001 * || min(w_t, 0) ||_1
  ```
  i.e. 5 bps per unit of turnover plus **1 bp per unit of short exposure**. Weights are
  normalised to sum to one in absolute value, which is the leverage constraint.
- Model re-estimation on a rolling **four-year** window; daily rebalancing at the close.

## Robustness evidence (qualitative only)

Stated as orderings and shapes, with no period-specific magnitudes:

- **Residuals beat raw returns for every signal model and every factor family.** The `K = 0`
  control is the worst configuration in each column. This is the paper's own first-stated
  conclusion and it is a direct contradiction of what this lab measured on its own universe (see
  Implementability).
- **The number of factors has an interior optimum for PCA residuals**: performance rises with `K`
  over the low range and falls again once too much variation is removed. This independently
  reproduces the shape Avellaneda–Lee report and this folder already records — remove too little
  and the residual still carries common variation; remove too much and it is noise. For the
  *conditional characteristic-based* factors the shape is flatter, which is consistent with
  conditional loadings extracting the same structure with fewer factors.
- **The signal-extraction function matters more than the residual definition.** Holding the
  residual fixed and swapping the OU-plus-threshold rule for a richer time-series model moves the
  result far more than any factor-model choice does. The authors state explicitly that their
  benchmark models are robust to the choice of factor model *as long as it contains sufficiently
  many factors*. The transferable claim: the information the classical rule discards when it
  compresses a 30-day residual path into a deviation and an R² is large.
- **Constraints trained into the objective change the strategy, not just its returns.** When the
  turnover penalty is added, the learned policy reduces its own turnover rather than simply
  paying the cost — the allocation adapts. A post-hoc filter on a signal computed without the cost
  cannot do this.
- **Weaknesses, and they are why this is Tier B not A.** Single market. No independent
  replication (the work is recent, and the published version post-dates both Hou–Xue–Zhang's
  sweep and Jensen–Kelly–Pedersen's). Multiple testing is not formally addressed, although the
  ablation design mitigates it. The cost model is deliberately simple — proportional, constant
  across names and time, no market impact — and the authors say so. The `published_post_2018` flag
  is **true** and should be applied as the usual novelty discount.
- Index note: Semantic Scholar resolves only the SSRN working-paper record; the Management Science
  DOI returns *not found* there and carries a near-zero Crossref count because it is newly
  registered. Per the rubric no tier adjustment was made on that basis — the count recorded above
  is the SSRN record's, which is the one that reflects the literature's actual use of the work.

## Implementability here

**What is reachable.** The PCA branch needs nothing but daily closes: correlation matrix on 252
days, eigen-portfolios with the `1/sigma_i` rescaling, 60-day loading regressions, residual for
the current day. On ~145 instruments that is cheap — well inside the ~60s-per-call budget, and
walk-forward by construction (every estimate uses only the trailing window, so
`causality_check` should pass without special handling). `scikit-learn`'s `PCA` and a linear
regression are the only tools needed. The `K = 0` control is free and should be run in the same
candidate.

**What is not.** The IPCA branch needs 46 firm characteristics from accounting data — out of
scope, and it is also the branch that performs best, so the reachable half of this paper is its
weaker half. Say so in any hypothesis line rather than citing the paper's headline.

**The cost gap is the binding constraint and it is a factor of six.** The paper trades **daily**
at **5 bps** per unit of turnover. This repo pays **15 bps per side** with a 1-day execution lag.
A daily-rebalanced residual book is therefore not merely more expensive here — it is a different
strategy. The honest adaptation is to move the rebalance out (weekly or monthly) and accept that
the 30-day residual path signal is being sampled far more coarsely than the paper samples it, or
to apply the signal as a **membership** rule over a slow-moving held set rather than as a
continuously re-struck weight.

**The long-only problem, stated precisely — and this paper is the best available text on it
because it is the only one in this vein that prices shorting explicitly.** Each arbitrage
portfolio is "long the name, short its mimicking portfolio". Under a fully-invested long-only
book the mimicking legs cannot be held. Two consequences the lab should write down before
proposing anything here:

1. **The market leg is free, the others are not.** In a fully-invested book the weights sum to
   one, so an implicit unit of market exposure is always held; the `K = 1` residual's short leg is
   therefore financed by the budget constraint *automatically* — a long-only book that overweights
   high-residual names against an equal-weight baseline **is** the long half of a market-residual
   trade. For `K > 1` no such accident occurs: the second and later factor legs are not
   neutralised at all, so a long-only "PCA `K = 5` residual" book holds four unhedged factor bets
   it did not choose. This is the same mechanism Blitz et al. derive for the contrarian sort
   (`notes/2026-09-25-short-term-residual-reversal.md`), arriving from the other direction.
2. **The 1 bp short-holding penalty is the literature's own estimate of what shorting costs, and
   it is small.** The gap between this paper's book and a long-only one is therefore *not* mostly
   a financing cost — it is the loss of the hedge and of half the cross-section. That squares with
   `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`: the reachable effect size is the
   minority share, and the reason is the constraint, not the fee.

**Tension with this lab's own measurement, recorded rather than resolved.**
`experiments/learnings.md` [2026-08-30] found residualisation *monotonically harmful* to 5-day
reversal on this universe (raw IC +0.0455 > 1-factor +0.0375 > PCA k=3 +0.0331 ≈ k=5 +0.0336).
This paper's `K = 0` control finds the opposite ordering on every one of its configurations. Three
differences that are not excuses but are testable: (i) the lab compared **unconditional
cross-sectional ICs**, this paper compares **traded strategies whose policy is optimised under the
residual definition** — an IC comparison cannot see a gain that lives in the signal-extraction
function; (ii) the lab's PCA used a single lookback and no `1/sigma_i` eigen-portfolio rescaling,
which on a universe where the volatility level is a known survivorship artifact is precisely the
node that decides which names dominate the factors; (iii) the lab's `k` range sits inside the
region both this paper and Avellaneda–Lee find worst. The cheap discriminating test is the
`1/sigma_i` rescaling: re-run the same IC ladder with eigen-portfolios built from the correlation
matrix and volatility-rescaled weights, train only. If the ordering flips, the lab's refutation
was about its PCA construction; if it does not, the refutation stands and is about the universe.

## Related

- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` — Avellaneda–Lee: the
  classical OU-plus-threshold rule that this paper treats as the benchmark signal function, and
  the source of the eigen-portfolio and factor-count material.
- `notes/2026-09-25-mean-reversion-time-screening-statarb.md` — Yeo–Papanicolaou, whom this paper
  cites as the other classical benchmark; the two together define "the signal function this paper
  is arguing against".
- `notes/2026-09-25-short-term-residual-reversal.md` — the same residualisation idea at monthly
  horizon, with the factor-exposure algebra written out.
- `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md` — how much of a long-short effect the
  long leg can reach.
- `notes/2026-09-03-machine-learning-economic-restrictions.md` — the same author (Pelger) on why
  economic restrictions beat unrestricted learners on this kind of panel.
