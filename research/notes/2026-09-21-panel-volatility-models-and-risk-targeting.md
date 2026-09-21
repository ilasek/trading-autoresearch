---
title: "Risk Everywhere: Modeling and Managing Volatility"
authors: Bollerslev, Hood, Huss, Pedersen
year: 2018
venue: The Review of Financial Studies 31(7), 2729–2773 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhy041
citations: 373 (OpenAlex, checked 2026-09-21); 353 (Crossref `is-referenced-by-count`, checked 2026-09-21). Semantic Scholar's DOI endpoint returns "not found" for this DOI — the documented index anomaly, not a low-impact paper.
sample_period: start varies by instrument (earliest early 1990s), all series end September 2014
markets: 58 instruments — 20 commodities, 21 global equity indices, 8 fixed-income futures, 9 currencies — intraday data across four asset classes and many countries
tier: A
validation_overlap: false
published_post_2018: true
read: full text (45 pages, typeset RFS article with volume/issue headers), from the first author's Duke faculty page — `public.econ.duke.edu/~boller/Published_Papers/rfs_18.pdf`. The article is CC-BY-NC-ND open access. The Internet Appendix was not read.
---

## Mechanism

Three separate claims, and they are worth keeping apart because only two of them survive this
repo's data constraints.

**1. Volatility dynamics are close to the same everywhere.** The raw volatility *levels* of a
commodity, a bond future, an equity index and a currency are obviously different. But normalise
each instrument's daily realized volatility by its own sample average, and the normalised series
have nearly identical unconditional distributions and nearly identical, highly persistent
autocorrelation functions — across instruments, across asset classes, and across countries. The
level is idiosyncratic; **the dynamics are common**. This is the paper's central empirical fact and
everything else follows from it.

**2. Therefore pool.** If the dynamic coefficients are the same object in every instrument, then
estimating them separately for each instrument is throwing away `N−1` samples' worth of
information and paying for it in estimation noise. A panel regression that constrains the dynamic
coefficients to be common — while letting each instrument keep its own level — is strictly more
efficient, and the paper's out-of-sample forecast improvements come mostly from this. **This is the
structural answer to the "140 instruments cannot support a learned model" objection in
`research/README.md`**: you do not fit 140 models, you fit one model on 140 instruments' worth of
rows. The obstacle to pooling is the level parameter, and §3.2 removes it (below).

**3. There is a common risk factor over and above the pooling.** Beyond sharing coefficients, a
*global* volatility factor — the cross-sectional average of normalised realized volatilities —
carries information about an individual instrument's future volatility that is **not** in that
instrument's own volatility history. Volatility spills over within and across asset classes and
regions. The authors do not claim to explain why volatility clusters; they report that the global
factor co-moves with aggregate risk-aversion and sentiment proxies and with macro news surprises,
and leave the structural question open. For this repo the relevant part is the reduced form: *your
neighbour's volatility predicts yours*.

A fourth contribution is methodological and, for this lab, possibly the most valuable single item
in the paper: **a way to score a volatility model that uses no return data at all** (§5, below).

## Construction recipe

### Centering — the trick that makes pooling legal

Write the general model as a distributed lag in past realized variances, `RV_{t+1} = b_0 + b(L) RV_t`.
The `b(L)` coefficients can reasonably be shared across instruments; the intercept `b_0` cannot,
because volatility levels differ by an order of magnitude. Replace the intercept with a **long-run
volatility factor** `RV_t^LR` — the *expanding-window* sample mean of that instrument's daily `RV`
from the start of its history to day `t` — and subtract it from every term including the left-hand
side:

    RV_{t+1} − RV_t^LR = b_1 (RV_t − RV_t^LR) + b_2 (RV_{t-1} − RV_t^LR) + ... + ε

Run in this form the coefficients are unconstrained, but collecting terms gives `RV_t^LR` an
implied coefficient of `1 − Σ b_i`, so **all implied coefficients sum to one by construction** and
the iterated long-run forecast converges to the day-`t` estimate of the unconditional volatility.
This is variance targeting (Engle–Mezrich) applied to a realized-volatility regression. Two
properties matter here: it is causal (an expanding mean uses only the past), and it eliminates the
level, which is exactly what allows the remaining coefficients to be estimated by panel regression
across instruments of wildly different volatility.

### HExp — smooth factors instead of HAR's step function

HAR (see `2026-09-21-har-rv-volatility-cascade.md`) imposes a step function on the lag weights, so
a forecast jumps abruptly when an unusually large daily `RV` drops out of the 5- or 22-day window.
The authors' preferred replacement mixes **exponentially weighted moving averages of past daily
`RV` at four fixed centers of mass**:

    ExpRV_t^{CoM} = Σ_{i=1..500} w_i · RV_{t+1-i},   w_i ∝ e^{-iλ},   CoM(λ) = e^{-λ}/(1 − e^{-λ})

with the decay solved from the center of mass as `λ = log(1 + 1/CoM)`, and **CoM ∈ {1, 5, 25, 125}
days** (roughly daily, weekly, monthly, semi-annual). The model, centered as above:

    RV_{t+h}^h − RV_t^LR = Σ_{j ∈ {1,5,25,125}} β_j (ExpRV_t^j − RV_t^LR) + ε        [HExp]

This has **no tuning parameters** — the four centers of mass are pre-specified, not fitted — so it
estimates by plain OLS asset-by-asset or by panel regression, exactly like HAR. The authors also
tried MIDAS beta-polynomial lag shapes and linear/hyperbolic decay mixtures and report that at a
monthly forecast horizon none of them systematically beat HExp. That is a useful negative: **the
smoothing family does not need to be searched.**

### HExpGl — adding the global factor

Define the global factor `GlRV_t` as the cross-sectional average of *normalised* `RV`s, rescaled
back to the target instrument's own volatility level, and constructed **per instrument** so that
today's global factor never uses data overlapping the target's next trading session — any
instrument whose hours would overlap is lagged one extra day. Then:

    RV_{t+h}^h − RV_t^LR = Σ_j β_j (ExpRV_t^j − RV_t^LR) + β_Gl (ExpGlRV_t^5 − RV_t^LR) + ε

where `ExpGlRV_t^5` is a 5-day-CoM EWMA of the global factor. The time-zone lagging convention is
not a detail — in a global universe it is the difference between a forecast and a look-ahead.

### Risk targeting, and the return-free way to score a forecast

A mean–variance investor with relative risk aversion `γ` facing a constant conditional Sharpe ratio
`SR` holds

    x*_t = SR / ( γ · sqrt( E_t[RV_{t+1}] ) )

i.e. **targets a constant volatility of `SR/γ`**, scaling exposure down when predicted volatility
is above target and up when below. The paper's calibration (from the broad-asset literature, not
fitted): `SR = 0.4`, `γ = 2`, giving a 20% annualised volatility target.

The payoff item is §5.1's **realized utility**. With that calibration, an investor using risk model
`θ` to set `x_t^θ = 20%/sqrt(E_t^θ[RV_{t+1}])` earns, per unit of wealth,

    UoW^θ = (1/T) Σ_t [ 8% · sqrt(RV_{t+1}) / sqrt(E_t^θ[RV_{t+1}])  −  4% · RV_{t+1} / E_t^θ[RV_{t+1}] ]

**Expected returns do not enter this expression.** It depends only on the realized variance and the
forecast, so it ranks volatility models without any exposure to the noise of realised returns, and
a model with a perfect forecast scores the theoretical maximum (4% of wealth under this
calibration) while any forecast error scores less. Transaction costs subtract directly, because the
metric is already in return units: charge `cost × |x_t^θ − x_{t-1}^θ|`.

Costs change the ranking of models, not just their level. A static model trades nothing; a fast
daily model trades most; the smoother models sit in between, and the smoothest responds slowest and
therefore cheapest. The authors' mitigation is Gårleanu–Pedersen **partial adjustment** — move only
a fixed fraction of the way (they use 15% per day) toward the zero-cost optimal position — and
under that policy the smooth models recover much of the utility that trading all the way to target
destroys.

## Robustness evidence (qualitative only)

- **58 instruments, four asset classes, many countries, two-plus decades.** The commonality result
  is not an equity or a US result; it is weakest for commodities, which co-move with each other
  about as much as they co-move with everything else.
- **Out-of-sample throughout** — rolling forecasts, not in-sample fits — and the economic
  evaluation is run on the same rolling forecasts as the statistical one, which is the right
  discipline and is not universal in this literature.
- **Costs are modeled** using measured bid–ask spreads, and the authors deliberately use the full
  spread rather than the half spread to stay conservative about market impact. They also report the
  ranking of models *net* of cost and note that it differs from the gross ranking — honest about
  the thing that most often reverses a volatility-timing result.
- Method honesty is otherwise good: the Jensen's-inequality biases from forecasting variance and
  then taking a square root or a reciprocal are flagged explicitly with the Taylor expansions, and
  alternative lag-shape families that did *not* help are reported rather than buried.
- **Caveats.** Three of four authors are at AQR and the fourth consults for it; the paper says so.
  The utility framework assumes a constant conditional Sharpe ratio — deliberately, to isolate the
  risk model — so it cannot speak to whether risk-targeting helps when expected returns co-move
  with volatility, which is precisely what the volatility-targeting debate is about (see the
  companion note). And the whole paper is built on intraday `RV`; the accuracy claims are not
  claims about daily-bar proxies.

## Implementability here

**What transfers directly, and cheaply:**

- **Centering.** The expanding-window mean as a level factor is causal, trivial, and is the
  precondition for anything pooled. It also generalises: any cross-instrument panel model in this
  repo that has to cope with a level parameter can use the same trick.
- **Panel estimation of common dynamic coefficients.** This is the paper's most transferable idea
  for a 140-instrument universe with short-ish histories. One model, `N × T` rows, a handful of
  coefficients, plain OLS, deterministic, walk-forward by construction. It is well inside the
  causality check and the time budget, and it is the opposite of the over-parameterised learner
  `research/README.md` warns against.
- **HExp's four fixed centers of mass.** No tuning parameters means no specification curve, which
  given `experiments/learnings.md`'s post-selection findings (2026-09-15) is worth more here than a
  marginally better lag shape. If a session wants a smooth multi-horizon volatility estimate, take
  `{1, 5, 25, 125}` from the paper and do not search around it.
- **The global volatility factor.** This repo has ~145 instruments across 15 regions and can build
  the cross-sectional average of normalised daily range-variance immediately. The time-zone lagging
  convention is directly relevant: a global universe with Asian, European and US sessions in it
  will otherwise leak. **The lab has already measured one version of a cross-sectional
  volatility-spillover claim** — see the 2026-08-31 ETF-versus-constituent lead-lag null in
  `experiments/learnings.md` — but that was a *return* lead-lag, and this is a *volatility*
  lead-lag. They are different claims and the null on one does not settle the other.
- **The realized-utility metric, and this is the item to use first.** It requires no returns, no
  champion comparison, no `run_experiment.py` trial — only the repo's own realized variance series
  and two competing forecasts. It answers the question "is a HAR/HExp/panel forecast better than
  the trailing 21-day window this repo already uses, *on this universe's data*" as a free
  measurement. If the answer is no, nothing downstream is worth building and no trial has been
  spent finding that out.

**What does not transfer:**

- **`RV` from intraday data.** This repo has one daily bar. The substitute is a range-based daily
  variance (see `2026-08-29-range-based-volatility-estimators.md`), which is noisier than intraday
  `RV` and, per Corsi's own diagnostic, will depress the shortest-horizon coefficient. Expect the
  1-day CoM factor to carry less weight here than in the paper, and do not read that as a bug.
- **Leverage.** `x*_t = target/σ̂_t` is a *two-sided* rule; this repo's gross leverage cap of 1.0
  means only the de-levering half is reachable. A risk-targeting overlay here can hold cash when
  predicted volatility is high but cannot lean in when it is low, which removes roughly half of the
  mechanism. Any adaptation should say which half it is claiming.
- **The 15%-per-day partial adjustment** is calibrated to costs an order of magnitude below this
  repo's 15 bps per side. The *idea* — trade partially toward target — transfers; the constant does
  not, and per the standing rule in `CLAUDE.md` about carrying constants across families it must be
  re-measured rather than imported.
- **`SR = 0.4`, `γ = 2`, 20% target.** These are the paper's calibration for a broad multi-asset
  futures universe. Using them to *score forecasts* is fine — the ranking is mostly insensitive to
  them and the metric is comparative. Using them as a performance expectation for a long-only
  equity book here is not, and `research/SUMMARY.md`'s standing rule against importing performance
  expectations applies.

**A pitfall specific to this repo.** Everything above makes the *risk* estimate better. It does not
make returns predictable, and it must not be turned into a cross-sectional score: trailing
volatility is this universe's identified survivorship artifact (`experiments/learnings.md`,
2026-09-06 onward), and a better forecast of it is a better estimate of the artifact.

## Related

- `2026-09-21-har-rv-volatility-cascade.md` — the benchmark this paper extends, and the source of
  the multi-horizon cascade idea that HExp smooths.
- `2026-09-21-volatility-targeting-impact-and-the-momentum-overlay.md` — the other side: what
  happens when you *use* the forecast to size positions in equities, and why that is partly a trend
  overlay.
- `2026-08-29-range-based-volatility-estimators.md` — the daily-bar substitute for intraday `RV`.
- `2026-08-17-volatility-timing-managed-portfolios.md` — the `1/σ²` portfolio rule and its
  replication challenge; this paper supplies the forecast, that note supplies the argument about
  whether the forecast is worth anything.
- `2026-08-21-weight-constraints-as-covariance-shrinkage.md` and the risk-parity note — the other
  places in this folder where a covariance estimate turns into weights.
