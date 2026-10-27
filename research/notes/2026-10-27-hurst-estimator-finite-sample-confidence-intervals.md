---
title: "Estimating long-range dependence: finite sample properties and confidence intervals"
authors: Weron
year: 2002
venue: Physica A 312(1–2), 285–299 (venue tier 2 — peer-reviewed, outside the finance tier-1 set)
url: https://doi.org/10.1016/S0378-4371(02)00961-5
citations: 357 (Crossref `is-referenced-by-count`, checked 2026-10-27)
sample_period: simulation study (Gaussian white noise, sample lengths 256 … 65536, 10,000 replications each); illustrative application to pre-2001 daily series
markets: none for the main result — the evidence is Monte Carlo under a known null
tier: B
validation_overlap: false
published_post_2018: false
---

> **Source read in full** from the author's arXiv preprint `arXiv:cond-mat/0103510v2`
> (174 KB → 49 KB of clean text via `pdftotext -layout`, no `( )` dropout, no ASCII shift). The
> published DOI, volume, pages and citation count were resolved by **Crossref journal-year
> enumeration** on ISSN 0378-4371 for 2002 after a direct title lookup was not attempted — the
> 2026-10-07 "a journal's year is a much better key than an article's title" rule, used first
> rather than as a fallback.

## Mechanism

No market mechanism. This is the **price list** for the long-memory vein: it reports, under a
known white-noise null, how much a Hurst-exponent estimate moves from pure sampling noise at each
sample length a researcher is likely to have. Everything that follows is a statement about
estimators, not about markets, which is why it transfers to this repo's panel unchanged.

The logic the paper makes concrete: all three standard `H` estimators are **slopes of a log-log
regression** (or, for GPH, of a log-periodogram regression). A slope fitted over a handful of
aggregation levels on a finite series has a wide sampling distribution, and that distribution is
not centred on the heuristic bands practitioners quote.

## Construction recipe

Three estimators, each defined completely enough to implement:

**1. R/S analysis (Mandelbrot–Wallis, after Hurst).** Split a length-`L` return series into `d`
subseries of length `n`. For each subseries: take the mean `E_m` and standard deviation `S_m`;
demean, `X_{i,m} = Z_{i,m} − E_m`; cumulate, `Y_{i,m} = Σ_{j≤i} X_{j,m}`; take the range
`R_m = max Y − min Y`; rescale `R_m/S_m`. Average over subseries to get `(R/S)_n`. Then
`(R/S)_n ~ c n^H`, so `H` is the slope of `log(R/S)_n` on `log n`.
*Mandatory correction:* for small `n` the expected value under the null is **not** `0.5`. Use the
**Anis–Lloyd** expectation, which the paper writes as

```
E(R/S)_n = ( (n − ½)/n ) · ( Γ((n−1)/2) / (√π Γ(n/2)) ) · Σ_{i=1..n−1} √((n−i)/i)      for n ≤ 340
         = ( (n − ½)/n ) · ( 1/√(nπ/2) )              · Σ_{i=1..n−1} √((n−i)/i)        for n > 340
```

and regress the *corrected* statistic. Without this correction the estimator **systematically
overestimates `H` to a large extent** — it is the single biggest avoidable error in the family.

**2. Detrended Fluctuation Analysis (Peng et al.).** Same subseries split. For each subseries:
cumulate `Y_{i,m} = Σ_{j≤i} X_{j,m}`; fit a least-squares line `a_m i + b_m` to it; take the RMS
of the residual, `F(m) = √( (1/n) Σ_i (Y_{i,m} − a_m i − b_m)² )`. Average to `F̄(n)`; `H` is the
slope of `log F̄(n)` on `log n`.

**3. Periodogram (GPH) regression.** Periodogram `I_L(ω_k) = (1/L)|Σ_t x_t e^{−2πi(t−1)ω_k}|²` at
`ω_k = k/L`; regress `log I_L(ω_k)` on `log(4 sin²(ω_k/2))` over the lowest `K` frequencies; minus
the slope is `d̂`, and `H = d̂ + 0.5`. Standard choice `K = [L^{0.5}]`. **This is the only one of
the three with a known asymptotic distribution:** `d̂` is asymptotically normal with variance
`π² / (6 Σ_{k≤K} (x_k − x̄)²)` where `x_k = log(4 sin²(ω_k/2))`.

**Subseries-length floor.** The paper reports every result for a minimum `n`, because very short
subseries dominate the regression and bias the slope. `n > 50` is the setting that wins for
`L > 500`; `n > 10` is better only at `L = 256`, and then only because 256 has just three divisors
above 50 and a three-point regression is unstable.

## Robustness evidence (qualitative only)

The headline table — 10,000 independent Gaussian white-noise realisations per length, true
`H = 0.5`, **standard deviation of `Ĥ`**:

| `L` | R/S–AL (`n>50`) | DFA (`n>10`) | DFA (`n>50`) | GPH |
|---|---|---|---|---|
| 256 | 0.1739 | 0.0972 | 0.1222 | 0.2205 |
| 512 | 0.1043 | 0.0724 | 0.0716 | 0.1705 |
| 1024 | 0.0739 | 0.0559 | 0.0497 | 0.1401 |
| 2048 | 0.0535 | 0.0436 | 0.0355 | 0.1085 |
| 4096 | 0.0422 | 0.0359 | 0.0278 | 0.0898 |
| 8192 | 0.0332 | 0.0293 | 0.0217 | 0.0727 |
| 16384 | 0.0277 | 0.0254 | 0.0181 | 0.0622 |
| 65536 | 0.0193 | 0.0184 | 0.0125 | 0.0424 |

Mean absolute error follows the same ordering. Findings:

- **DFA with `n > 50` is the unanimous winner for `L > 500`**, and it has **no asymptotic
  distribution theory** — so the better estimator is also the one with no analytic test, which is
  why the paper builds empirical intervals.
- **Uncorrected R/S overestimates `H` badly**; all the other methods carry a slight *negative*
  bias.
- **GPH is the worst of the three at every length** — roughly 2–3× the standard deviation of DFA —
  despite being the only one with a textbook standard error.
- **The commonly quoted heuristic band `1/√L` rejects far too often.** Compared against the
  simulated quantiles, it over-rejects relative even to a 90% interval, let alone 95%.
- **Fitted confidence bands.** The simulated quantiles fit well as
  `0.5 ± exp(a · log(log₂ L) + b)` for R/S–AL (e.g. 95%:
  lower `0.5 − exp(−7.33 log(log₂ L) + 4.21)`, upper `0.5 + exp(−7.20 log(log₂ L) + 4.04)`;
  `R² ≈ 0.998`) and as `0.5 ± exp(a · log₂ L + b)` for DFA. For GPH the empirical and the
  theoretical asymptotic intervals agree closely, which is the one favourable thing the paper says
  about it.
- **A worked width, and this is the number to remember.** At `L ≈ 2500` daily observations (about
  ten years of daily data), the **90%** no-memory intervals are R/S–AL `(0.414, 0.581)`,
  DFA `(0.439, 0.554)`, GPH `(0.318, 0.665)`. At 99% the GPH interval runs `(0.207, 0.758)`.
- Applied to daily index series, the paper's own qualitative reading — consistent with the
  references it cites — is that **returns show essentially no detectable long-range dependence**
  while the **absolute value of returns does**, significantly at the two-sided 99% level by all
  three methods. (A separate, non-equity series showed `H` significantly *below* 0.5, i.e.
  anti-persistence; recorded only to note that the methods do reject in both directions when
  something is there.)
- **Limits of the study, stated by the author.** The null simulated is *Gaussian white noise*, not
  a short-range-dependent process. So these intervals price **estimation noise**, not the
  short-memory contamination Lo's modified R/S is built to remove — the two defects are
  independent and both apply. The study also fixes `H = 0.5`; power against specific `H > 0.5`
  alternatives is not mapped.

## Implementability here

**Zero trials, zero holdout, and it is a gate on the whole vein rather than a signal.**

- **The arithmetic for this panel.** A per-name Hurst estimate on one year of daily data
  (`L ≈ 252`) has a null standard deviation of roughly **0.10–0.17** depending on method — wider
  than the entire plausible range of true `H` for equity returns. On the full train window
  (`L ≈ 5,300`) it is still about **0.025–0.08**. On validation alone (`L ≈ 1,500`) about
  **0.04–0.12**.
- **The screen this licenses, and it should be run before any `Hurst`-ranked book is written.**
  Compute `Ĥ` per eligible name over the train window with DFA (`n > 50`), then compare the
  **cross-sectional standard deviation of `Ĥ`** against the table's null standard deviation at the
  same `L`. If the cross-sectional dispersion is not materially larger than the null dispersion,
  the ranking is a ranking of estimation noise and the sort has nothing in it. This is four lines
  of pandas and it costs no trial. The same comparison is the honest version of "names differ in
  persistence".
- **Which estimator to use here.** DFA with `n > 50`, because it is the lowest-variance of the
  three at every length above 512 and because the empirical bands above are supplied. Do **not**
  use raw R/S (the Anis–Lloyd correction is not optional), and do not prefer GPH merely because it
  has a closed-form standard error — its sampling variance is 2–3× DFA's.
- **Interaction with the `eligible` panel.** Index membership is point-in-time, so per-name series
  have different and often short usable lengths; the null band must be read at **each name's own
  `L`**, not at the panel's. A cross-sectional sort on `Ĥ` therefore mixes names whose null
  dispersion differs by a factor of two or more — which is a confound of the same shape as the
  2026-10-09/10 "liquidity split on a fixed book size is confounded with tail depth" finding, and
  it is avoided by requiring a common minimum `L`.
- **Protocol hazard.** The subseries-length floor, the set of `n` used in the regression, and `K`
  for GPH are all hyperparameters in item `#311`'s sense. Fix them a priori (`n > 50`,
  `K = [L^{0.5}]`) rather than choosing them from the data.
- **What it cannot do.** This prices noise under a *white-noise* null. A series with short-range
  dependence will produce a biased `Ĥ` on top of this noise, and that bias is Lo's subject, not
  Weron's. Both corrections are needed before any `Ĥ` is believed.

## Related

- `notes/2026-10-27-modified-rescaled-range-and-the-long-memory-null.md` — the short-range-bias
  half of the same problem, and the reason the raw R/S slope is not to be trusted.
- `notes/2026-10-27-long-memory-and-regime-switching-identification.md` — even an `Ĥ` that clears
  both corrections does not identify a mechanism.
- `notes/2026-09-21-har-rv-volatility-cascade.md` — the "absolute returns are persistent, returns
  are not" split is the same fact the HAR note records from the volatility-modelling side.
- `notes/2026-08-24-deflated-sharpe-ratio.md` and `scripts/rank_trials.py` — the folder's standing
  rule that a point estimate without an error bar is not a ranking. This note is that rule applied
  to a Hurst exponent, and the table above is the error bar.
- SUMMARY `#306`/`#310`/`#312` — the parameter-count and precondition-first family of screens;
  this is the same shape, with the precondition being "is the dispersion larger than the noise".
