---
title: "A Simple Approximate Long-Memory Model of Realized Volatility (HAR-RV)"
authors: Corsi
year: 2009
venue: Journal of Financial Econometrics 7(2), 174–196 (venue tier 1 for econometrics; Oxford UP)
url: https://doi.org/10.1093/jjfinec/nbp001
citations: 2500 (Semantic Scholar, checked 2026-09-21; its record dates the paper 2008, the working-paper year); 1850 (Crossref `is-referenced-by-count`, checked 2026-09-21)
sample_period: USD/CHF December 1989 – December 2003; S&P 500 futures January 1990 – July 2007; 30-year US T-Bond futures January 1990 – October 2003
markets: one FX rate, one equity-index future, one fixed-income future — tick-by-tick, three long series
tier: A
validation_overlap: false
published_post_2018: false
read: full text, from a university course reading-list directory (`statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/`), the typeset JFEC article complete with volume, issue and page headers.
---

## Mechanism

This is a **forecasting** result about volatility, not a return premium. It belongs here because
it names the one quantity in this repo's data that is known to be strongly predictable, and gives
the cheapest good model of it.

The economic story is the **Heterogeneous Market Hypothesis** (Müller et al. 1993): market
participants differ in their trading horizon — intraday dealers and market makers at one end,
weekly-rebalancing intermediaries in the middle, monthly-or-slower institutions at the other — and
agents at different horizons *perceive, react to, and cause different volatility components*. The
non-obvious part is that the coupling is **asymmetric**. Long-horizon volatility matters to
short-horizon traders, because it sets the expected size of future trends and therefore their risk;
short-horizon volatility does not enter a long-horizon trader's decisions at all. The result is a
one-way **cascade from low frequencies to high frequencies** — the same shape as an energy cascade
in turbulence, which is where the analogy in this literature comes from.

Corsi's move is to take that story literally and write volatility as an **additive cascade of
three partial volatilities** (daily, weekly, monthly), each an almost-AR(1) in its own realized
volatility plus the expectation of the next longer component. Recursive substitution collapses the
cascade into a single linear regression. The payoff is that a model with **three** free
coefficients reproduces the stylised facts that motivate long-memory models — slowly decaying
volatility autocorrelation, fat-tailed returns, self-similarity — without being a long-memory
process at all. It is a step-function approximation to a hyperbolic decay, and the approximation is
good enough that the exact long-memory machinery (ARFIMA, fractional differencing) buys little.

The second thing worth taking from the mechanism: the fitted coefficients are a **direct read on
which horizon carries the information**, because they are the weights on the three market
components. Where a series' daily realized volatility is noisily measured, the daily coefficient
collapses and the weekly and monthly components absorb the weight — Corsi observes exactly this for
the instrument with the sparsest tick arrival, and explains it as measurement noise in the daily
term rather than as an absence of daily dynamics. **A near-zero short-horizon coefficient is
evidence about your volatility proxy, not about the market.** That is a directly usable diagnostic
here, where the proxy is a daily bar rather than a tick stream.

## Construction recipe

Let `RV_t^(d)` be the realized volatility for day `t`. Aggregate to longer horizons as a **simple
average of the daily values**, not a sum:

    RV_t^(w) = (1/5)  · (RV_t + RV_{t-1} + ... + RV_{t-4})
    RV_t^(m) = (1/22) · (RV_t + RV_{t-1} + ... + RV_{t-21})

(Corsi notes that by Jensen's inequality the averaged quantity is not literally the realized
volatility of the longer interval; the difference is immaterial empirically and the averaging is
what makes the model readable as a restricted AR(22).) Annualise everything so the three horizons
are on one scale.

The model, **HAR(3)-RV**, is then one OLS regression:

    RV_{t+1}^(d) = c + β_d · RV_t^(d) + β_w · RV_t^(w) + β_m · RV_t^(m) + ω_{t+1}

- **Estimation is plain least squares.** Coefficients are consistent and asymptotically normal;
  use Newey–West standard errors (Corsi uses order 5) because the aggregated regressors overlap.
- **Volatility, not variance.** The paper is written in the square-root (volatility) form. The
  variance form and the log form are both stated as legitimate alternatives — the log form is the
  usual way to guarantee positivity.
- **Multi-step forecasts**: for an `h`-day horizon, forecast the *aggregate*, i.e. regress
  `Σ_{j=0..h} RV_{t+j}` directly on the same three regressors (a "direct" forecast), rather than
  iterating the one-day model forward.
- **Out-of-sample protocol in the paper**: re-estimate daily on a rolling window of 1,000
  observations. Nothing is fitted once over the whole sample — the model is cheap enough to refit
  every day, which is why it survives a walk-forward discipline.
- **Extension point the author names**: the model is a linear regression, so extra regressors
  (jump components, signed/asymmetric terms, other assets' volatility) drop straight in. That hook
  is what the panel and global-factor extensions in
  `2026-09-21-panel-volatility-models-and-risk-targeting.md` use.

Qualitatively, all three horizon coefficients come out individually significant, none dominates,
and they are of broadly similar size — the information is genuinely spread across horizons rather
than concentrated at the shortest lag. That is the fact a single trailing-window estimate throws
away.

## Robustness evidence (qualitative only)

- **Three series in three different asset classes** (FX, equity index, fixed income), each with
  more than a decade of tick data, and the qualitative conclusion is the same in all three.
- Against an unrestricted **AR(22)** — the model HAR(3) is a restricted version of — the
  restrictions are formally rejected by an F-test, but the Bayesian information criterion
  nevertheless prefers HAR(3), i.e. the extra 19 parameters do not pay for themselves. Corsi is
  candid about the rejection and diagnoses it per series (a missing two-day and biweekly frequency
  in one, a five-lag periodicity in another, coefficient instability beyond three weeks in the
  third). This is unusually honest reporting of a fit statistic that goes against the author.
- Against **ARFIMA**, the genuine long-memory competitor: performance is comparable, with the
  advantage alternating by horizon. Corsi's argument for HAR is therefore *not* accuracy, it is
  that ARFIMA is fragile — its results depend on the Taylor-expansion cutoff of the fractional
  difference operator and on the GPH frequency cutoff, and re-estimating it on a rolling window is
  painful. **Parsimony and estimation stability are the claim, not a forecasting win.**
- HAR has since become the standard benchmark that later realized-volatility models are judged
  against (Bollerslev–Hood–Huss–Pedersen say so explicitly), which is replication by adoption
  rather than by a formal replication study. Note the limit: the effect being "replicated" is a
  *forecasting* regularity in volatility, not a tradeable anomaly, so the McLean–Pontiff
  publication-decay logic in `2026-08-17-mclean-pontiff-publication-decay.md` does not obviously
  apply — nobody arbitrages away the persistence of variance.

## Implementability here

**The blocking issue is the input, and it is not fatal.** `RV` in this paper is built from tick
data. This repo has one daily bar per instrument. Two substitutions are available and both are
already characterised in this folder:

1. **Range-based daily variance as the RV proxy** — Parkinson, Garman–Klass or Rogers–Satchell
   from `2026-08-29-range-based-volatility-estimators.md`. These are the right input: the log range
   has roughly a quarter the noise of the log absolute return as an estimator of log volatility, and
   it is nearly Gaussian, which is what makes it behave under a linear model. Corsi's own diagnostic
   applies directly — **if `β_d` collapses when you fit HAR on a range proxy, that is the proxy's
   noise, not the absence of daily dynamics**, and the honest response is to lean on the weekly and
   monthly terms rather than to add parameters.
2. **Squared daily close-to-close returns** as the crudest proxy. Strictly worse per the
   efficiency result above, but it is the null model any range-based version must beat, and the
   comparison is free.

Fit against the rest of the constraints:

- **Walk-forward is native.** The paper's own out-of-sample protocol is a rolling 1,000-day
  re-estimation, which is exactly what `strategies/lib/walkforward.py` does and what
  `causality_check` demands. A HAR fit is three OLS coefficients — it will refit at every month-end
  far inside the ~60s per-call budget, and OLS on fixed regressors is deterministic.
- **Few features.** `research/README.md` warns that a 140-instrument universe cannot support a
  900-feature model. HAR is a three-regressor model whose regressors are specified in advance, with
  no tuning parameters. It is the extreme end of the "penalised linear model first" advice.
- **It is not a return signal.** Nothing here predicts returns, and nothing here should be sorted
  on cross-sectionally as if it did. Note the lab's standing warning in `experiments/learnings.md`
  (2026-09-08): 21-day Garman–Klass volatility has the **largest |IC| of any score in this repo**,
  with high volatility predicting high forward return, and fourteen mechanism screens identify that
  as this universe's survivorship artifact. **A better volatility forecast is a better estimate of
  the artifact-carrying variable.** The only honest use of a HAR forecast here is as a *risk*
  input — a denominator, a covariance input, a scaling — never as a cross-sectional score.
- **What it changes, concretely:** everywhere this repo currently uses a trailing 21-day or 252-day
  volatility, that is an equal-weight window, i.e. the one restriction HAR says is wrong. The
  substitution is a drop-in and the question of whether it matters here is answerable without a
  trial (see the realized-utility metric in
  `2026-09-21-panel-volatility-models-and-risk-targeting.md`).

**Pitfalls.**

- The `h`/`l`/`c` in the range estimators are measured **from the open**, not from the previous
  close (see the pitfalls section of the range-estimators note). Getting this wrong quietly
  mis-specifies the RV input — and `strategies/lib/sleeve_book.py:41`'s mis-specified
  `garman_klass_vol` call, flagged 2026-09-18 and still open, is the instance of exactly this
  failure mode already present in the repo.
- Volume and therefore some bar fields are NaN on foreign holidays in this universe; a 22-day
  average of a range proxy needs an explicit missing-data convention, and the convention must not
  peek forward.
- The aggregation is an **average**, not a sum. A sum changes the scale of `β_w` and `β_m` and will
  read as a fitting problem when it is an arithmetic one.

## Related

- `2026-08-29-range-based-volatility-estimators.md` — supplies the daily RV proxy this model needs
  and the efficiency argument for preferring the range to the squared close-to-close return.
- `2026-09-21-panel-volatility-models-and-risk-targeting.md` — the modern successor: centering,
  panel estimation across instruments, smooth EWMA factors in place of HAR's step function, a
  global volatility factor, and a return-free way to score a volatility forecast.
- `2026-09-21-volatility-targeting-impact-and-the-momentum-overlay.md` — what a volatility forecast
  is worth once it is turned into position sizes, and the warning that on equities such an overlay
  is partly a trend overlay.
- `2026-08-17-volatility-timing-managed-portfolios.md` — the portfolio rule (`1/σ²` scaling) whose
  input this note is about. That note's central asymmetry — volatility is forecastable, returns at
  the same horizon are not — is the reason this literature is worth reading at all.
- `experiments/learnings.md` (2026-09-06 onward) — the repo's own finding that trailing
  Garman–Klass volatility is the most monotone, most phase-stable, highest-|IC| score here, and is
  the survivorship artifact. Read before any construction that ranks names by volatility.
