---
title: "Forecasting stock return distributions around the globe with quantile neural networks" — a 37-quantile forecast of each name's next-month return distribution, and the finding that only the *centre* of that distribution is priced in the cross-section
authors: Baruník, Hronec, Tobek
year: 2026
venue: International Journal of Forecasting (venue tier 2 by this folder's rubric — a well-regarded peer-reviewed forecasting journal, not one of the finance tier-1 list; refereed, with the editor and two referees acknowledged in the paper)
url: https://doi.org/10.1016/j.ijforecast.2026.04.004
citations: 1 (Crossref `is-referenced-by-count`, checked 2026-10-20); 1 (Semantic Scholar by DOI, same date). Essentially uncited — the article is newly published and the count carries no information yet, which is itself a reason the tier below is not higher.
sample_period: 1963–2018 US (training from 1973), 1990–2018 international; out-of-sample predictions 1995–2018, with an appendix extending the US exercise to 2019–2023
markets: US, Europe, Japan, Asia-Pacific — 23 developed countries. Reported separately for a "full sample" (all names above a penny-price screen, thousands per region) and a "liquid sample" (top-95% market cap AND top-95% dollar volume within region, hundreds per region)
tier: B
validation_overlap: true
published_post_2018: true
read: full text of `arxiv.org/pdf/2408.07497` (v2, dated 2025-08-02; 2.5 MB → 258 KB of clean text, 1,425 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). arXiv on the first try, which is the channel this folder's 2026-10-19 access note says to prefer for a methods paper. The preprint carries the abstract, all of Sections 1–4, Tables 1–9 and the appendix list of 153 characteristics; the published version's own figures were not needed because the prose restates the table contents. **The appendix's 2019–2023 US exercise was deliberately not read beyond the sentence announcing it**, since this folder may not carry post-2023 information and has no use for dated performance from any window.
---

## Mechanism

No new economic mechanism is claimed, and that matters for how to read the paper. The mechanism
question it answers is **structural**: given that a cross-sectional selection rule reduces a
predictive *distribution* to a single number and sorts on it, which feature of that distribution
should the number be?

The standard answer is the conditional mean, because squared-error training elicits the mean
(`notes/2026-10-19-consistent-scoring-functions-and-elicitability.md`). The distributional
alternative is to forecast many conditional quantiles, interpolate them into a smooth CDF, and then
read *whatever* functional the decision wants out of that CDF — the mean by numerical integration,
or the median, or a variance, skewness or kurtosis. This paper builds that object at scale, on four
regions, and then asks the only question that decides whether the extra machinery earns anything:
**are the predicted quantiles, and the predicted higher moments, actually priced in the
cross-section — or is the mean still the only thing a sort can use?**

Its answers are the reason to file the note, and two of the three are negative:

1. **Only the central quantiles are priced.** Sorting names on a predicted `τ`-quantile and holding
   the extreme deciles produces a spread that is largest at the **centre** of the distribution
   (levels near the median and modestly above it) and **decays monotonically toward both tails**,
   becoming statistically indistinguishable from zero well before the extreme levels are reached.
   The authors' own summary: "the tail `τ`-quantiles in isolation are not priced into the
   cross-section of stock returns." The same pattern appears in the international evidence.
2. **The decay is much sharper in the liquid sample, where the significant band is narrow.** In the
   full sample the spread stays significant across a broad band of central levels. In the liquid
   sample — large-cap, high-dollar-volume names only — the spread falls away far faster as one moves
   off the centre, and the band that remains significant is correspondingly narrow. This is the
   single most transferable fact in the paper for this lab, because the lab's panel is nine
   large-cap national indices and is the liquid sample's analogue, not the full sample's.
3. **No higher moment is monotonically priced, in either sample.** Long–short deciles sorted on the
   distribution-derived volatility, skewness and kurtosis forecasts are mostly indistinguishable
   from zero; there are scattered regional exceptions in the full sample only (volatility and
   skewness in two regions), and the value-weighted versions agree with the equal-weighted ones. The
   predicted-volatility relation is *negative but insignificant* in the liquid sample, which the
   authors attribute to the large-cap focus: "volatility effects are typically weaker" there.
4. **What the distributional route does buy is a better mean.** The mean obtained by numerically
   integrating the interpolated CDF produces a larger cross-sectional spread than a direct
   mean forecast from an otherwise-comparable network trained on squared error, and than the
   quantile model's own *median*. In the full sample the mean beats the median significantly in
   every region; **in the liquid sample the mean and the median are statistically
   indistinguishable**, which the authors tie to the conditional distribution being less asymmetric
   among large caps. So the gain from "predict the distribution" is a *mean-estimation* gain, of the
   same kind the composite-quantile theorem predicts
   (`notes/2026-10-20-composite-quantile-regression-efficiency-bound.md`), and it too shrinks as the
   universe becomes liquid.

Read together: the distributional apparatus pays for itself through the centre of the distribution
and through a more robustly estimated mean, and both of those payments get smaller exactly as the
universe moves toward the large-cap panel this lab trades. The tails, the variance and the shape pay
nothing.

## Construction recipe

**Target.** For each name `i` and month `t`, the conditional quantiles
`Q_{r_{i,t+1}}(τ | F_t)` of the *next* month's raw return, at **37 levels** spanning
`τ ∈ {0.00005, 0.0001, 0.001, 0.005, 0.01 … 0.05, 0.075, 0.1, 0.15, 0.2 … 0.8, 0.85, 0.9, 0.925,
0.95 … 0.99995}` — dense in the tails and on a 0.05 grid through the middle. The forecast horizon is
a 22-day-ahead return.

**The two-stage architecture, and the reason for it.** Cross-sectional standardisation of returns is
the usual way to strip out market-wide time-series noise before a cross-sectional fit, but it
destroys the scale of the thing being forecast; here the output has to be a quantile of a *raw*
return. So:

- *Stage I* forecasts quantiles of a **standardised** return
  `r̃_{i,t+1} = r_{i,t+1} / σ̄_t`, where `σ̄_t` is the **cross-sectional average** of stock-level
  volatilities at `t` (not the stock's own volatility — the averaging is deliberate, to avoid
  injecting the noise of an individual volatility estimate; and `σ̄_t`, not `σ̄_{t+1}`, because the
  latter is not known when the forecast is made). Returns are divided but **not** demeaned, on the
  stated ground that average returns are not persistent.
- *Stage II* is a second sub-network that predicts a **multiplicative adjustment factor** to `σ̄_t`
  from market-level volatility inputs, rescaling Stage I's standardised quantiles back to raw ones.
  It forecasts the adjustment, not market volatility itself.

**Loss.** One multi-output network for all 37 levels at once, with the pinball losses summed over
levels and over both output heads (standardised and raw) and averaged:

    L = (1/B)(1/K) Σ_{τ∈T} Σ_i [ ρ_τ( r_{i,t} − Q̂_{r_{i,t}}(τ) ) + ρ_τ( r̃_{i,t} − Q̂_{r̃_{i,t}}(τ) ) ]

with equal weight on every name and every level. Joint training across levels is both cheaper than
`K` separate models and, the authors report, enough on its own to keep the predicted quantiles
monotone — **no quantile-crossing penalty was needed and no crossing occurred**.

**Quantiles → CDF → moments.** Cubic B-spline interpolation of the `(τ_j, Q̂_j)` pairs, on a denser
grid built by inserting one hundred equally spaced points between each adjacent pair of predicted
quantiles (excluding the outermost), gives a smooth CDF on `[−1, ∞)`; differentiating the spline
gives a density; the mean, variance, skewness and kurtosis follow by numerical integration. The
paper also adjusts the higher moments for the absence of extreme observations in the tails.

**Features (194 in total, and far beyond this lab's reach — see Implementability).** 153 published
anomaly characteristics (93 fundamental, 49 market-friction, 11 analyst-estimate), plus 18
stock-level volatility estimates, plus 23 market-level variables. The volatility block is the only
part reachable from a daily OHLCV panel and is specified usefully: **EWMAs of squared returns at
decay factors `α ∈ {0.8, 0.9, 0.94, 0.96, 0.98, 0.99}`; EWMAs of *negative* returns only at
`α ∈ {0.8, 0.9, 0.94}` as an asymmetric-volatility proxy; total volatility over 3, 6 and 12 months;
and Parkinson (1980) high–low range volatility.** Every stock-level volatility is divided by its own
cross-sectional mean, so that it enters as a relative quantity like the rank-normalised
characteristics. The market block is EWMA cross-sectional mean returns at
`α ∈ {0.9, 0.94, 0.96, 0.99, 0.999}` plus 18 cross-sectional averages of the stock volatilities.
Missing characteristics are imputed by the cross-sectional median.

**Fitting discipline, which is careful and worth copying.** Hyperparameters are chosen once on an
early block and then frozen. The model is retrained **annually on an expanding window**, with the
final forecast date in each year restricted so that the 22-day forward target lands inside the same
calendar year — explicitly to prevent both label and feature leakage across the retrain boundary.
Subsequent retrains **fine-tune from the previous period's weights** rather than reinitialising.
Regularisation is dropout 0.2, L1 on the first-stage weights, L2 on the market sub-network's first
layer, early stopping with patience 2 on a 20% validation slice, and an **ensemble of 20 networks**.
Optimiser Adam, lr 3e-4, batch 8192, Leaky-ReLU, batch normalisation.

**Portfolio construction used for the pricing tests.** Monthly rebalance; sort all names on the
forecast; long the top decile, short the bottom decile, **equal-weighted**; value-weighted variants
reported as a robustness check. Inference is Newey–West with 12 lags.

## Robustness evidence (qualitative only)

**For it.** Four regions and 23 developed countries, reported separately rather than pooled, with
the international results qualitatively matching the US on the central-quantile finding. Two
universe definitions (full and liquid) reported side by side throughout, which is what makes the
liquidity discount above visible at all. Equal- and value-weighted portfolio variants. A
simulation study under a known data-generating process, and comparisons against a linear model,
one- and two-hidden-layer networks, GARCH and tree-based learners. Models trained on US data only
are applied to international markets as an additional out-of-sample test. The leakage discipline at
the retrain boundary is stated explicitly and is stricter than much of this literature.

**Against it, and this is why the tier is B rather than A.**

- **No transaction costs anywhere.** A grep of the full text finds "turnover" only as the name of
  input characteristics; no cost model, no turnover report, no net-of-cost table. The strategies are
  monthly decile long–shorts over a universe including thousands of names per region, i.e. high
  turnover by construction, and none of it is charged.
- **No multiple-testing treatment.** The features are 153 published anomalies and the pricing tests
  run 13 quantile levels × 4 regions × 2 samples × 2 weighting schemes; the paper acknowledges the
  multiple-testing literature in its reference list (Harvey et al.) but applies no correction, and
  the `t` statistics are read individually.
- **Essentially uncited and unreplicated.** One citation at the date checked. No independent group
  has rebuilt this.
- **The headline pricing results are a difference of two deciles**, i.e. long–short, which is not
  the object this lab can trade; see below.
- `validation_overlap: true`. The main out-of-sample window ends in 2018 and so does not touch the
  lab's 2018–2023 validation split in bulk, **but an appendix extends the US exercise into
  2019–2023, which does.** The novelty discount applies, and the appendix was not read.

## Implementability here

**The method as published is out of reach, and not marginally.** 153 of its 194 features are
fundamentals, analyst estimates and friction measures from CRSP/Compustat and I/B/E/S; this lab has
daily OHLCV and nothing else. A 20-network ensemble of multi-output deep nets, retrained annually
with fine-tuning, is also far outside `program.md`'s ~60 s per call and its determinism requirement
at `1e-6` — a fine-tuned, early-stopped, dropout-regularised ensemble is not reproducible to that
tolerance, and `program.md`'s own guidance ("prefer few features and a penalised linear model
first") points the other way. **Do not propose a trial that is this paper's architecture.** What
transfers is the paper's *findings*, which are mostly prohibitions, plus two reachable fragments.

**The prohibitions, which are free and are the valuable part.**

- **Do not build a candidate that sorts on a predicted tail quantile, a predicted variance, a
  predicted skewness or a predicted kurtosis.** This paper's own distribution-derived versions of
  all four are unpriced, in the sample closest to this lab's panel, with multi-region evidence and
  a long sample behind the null. That is a published null on four candidate signals at once, and it
  is independent of anything this lab has measured — unlike the lab's own volatility and
  dispersion nulls, which were measured on this panel and could have been panel artifacts. The two
  now agree from different directions, which is the strongest form the evidence comes in.
- **Discount any distributional-forecast proposal by the liquidity gap before costing it.** The
  spread decays faster off-centre in the liquid sample, and the mean-over-median advantage vanishes
  there entirely. Both of the paper's gains are substantially weaker in the subsample that resembles
  nine large-cap national indices. A proposal justified by the full-sample result is justified by a
  universe this lab does not have.
- **If a distributional candidate is ever written, the functional to read off the CDF is the mean,
  not a quantile.** That is the paper's one positive finding and it is also what
  `notes/2026-10-20-composite-quantile-regression-efficiency-bound.md` predicts from theory. The
  median is not the thing to sort on, which is a non-obvious correction to the naive "quantile
  regression is robust, use the median" instinct.

**The two reachable fragments.**

1. **The volatility feature block is fully specified and entirely free-OHLCV.** Six EWMA variances
   at named decay factors, three negative-return-only EWMAs as an asymmetry proxy, 3/6/12-month
   total volatility, and Parkinson range volatility — thirteen causal features computable from
   `prices` and `aux` with `strategies/lib/features.py`, each **divided by its own cross-sectional
   mean**, which is the construction detail that makes them comparable to rank-normalised scores.
   This is a ready-made feature set for the `range-variance` family, with the paper's own caution
   attached: in its liquid sample these inputs did not deliver a priced volatility sort.
2. **The two-stage standardisation is a pattern, not a signal, and it is cheap.** Dividing returns
   by the *cross-sectional average* of stock-level volatilities — rather than by each name's own —
   is a one-line de-noising step with a stated rationale, and the `σ̄_t`-not-`σ̄_{t+1}` point is
   exactly the kind of causality trap `causality_check` exists to catch. Note the contrast with
   `notes/2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md`, where the
   pool-level cross-sectional *variance* is the object; here the pool-level average *volatility* is
   a scale, which is that note's own estimator/signal/scale distinction appearing again.

**Long-only is a real constraint on importing the headline.** Every pricing result is a top-decile
minus bottom-decile spread. The paper does report the legs separately for the quantile sorts, and
the qualitative shape of the long leg alone is not the same as the shape of the spread — so a
long-only reading of these results requires the long leg's column, and anybody citing this paper for
a long-only candidate should say which column they are citing. Under v3 the comparison that matters
is against the equal-weight eligible pool, which is not a column this paper prints at all.

## Related

- **Second member of tonight's chain**, between the theory
  (`notes/2026-10-20-composite-quantile-regression-efficiency-bound.md`: a family of check-function
  losses recovers the location slope with a bounded efficiency cost) and the calibration layer
  (`notes/2026-10-20-distributional-conformal-prediction.md`: what a predicted CDF is worth when the
  model is misspecified). This note is the empirical middle: on a real global cross-section, the
  quantile machinery's payoff is a better mean and the shape is unpriced.
- **Consistent with a measured refutation rather than against it.** `learnings.md` [2026-10-19/20]
  closed the objective-function branch of `statistical-learning` — an ordinal loss cannot create
  ordering information absent from the features. This paper changes the *loss* (pinball over 37
  levels) and the *functional* (a whole CDF) while keeping a rich feature set, and still finds the
  tails and the shape unpriced and the mean the only usable read. That is the same conclusion from
  the opposite end of the feature-richness scale, and it is why tonight's session should be read as
  closing the distributional branch too rather than opening it.
- **Supersedes nothing but qualifies** `notes/2026-08-29-machine-learning-cross-section-comparative.md`
  (the lab's standing ML comparative source, which holds the squared-error objective fixed) and
  `notes/2026-10-19-learning-to-rank-cross-sectional-selection.md` (which varies the loss toward an
  ordinal one). Those two plus this one span the three available moves — vary the estimator, vary
  the loss, vary the predicted object — and all three land on the features.
- Volatility and higher-moment nulls on this panel:
  `notes/2026-10-18-dispersion-beta-and-the-cross-section.md`,
  `notes/2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md`.
- The unobtained pointer this note partly replaces: Ma–Pohlman (2008, *EJF*), named in `SUMMARY.md`'s
  [2026-10-19] open-questions entry as the standard primary on quantile-regression return forecasts
  feeding portfolio construction, closed at Taylor & Francis with only an SSRN location. Still
  unobtained; the empirical calibration it would have supplied is now supplied by a newer source on a
  wider panel.
