---
title: "Multiscale systematic risk"
authors: Gençay, Selçuk, Whitcher
year: 2005
venue: Journal of International Money and Finance 24(1), 55–70 (venue tier 1/2 — peer-reviewed Elsevier field journal)
url: https://doi.org/10.1016/j.jimonfin.2004.10.003
citations: 258 (Crossref `is-referenced-by-count`, checked 2026-10-27)
sample_period: 1973–2001 (US: S&P 500 constituents, 7263 market days ≈ 28 years; Germany: DAX30, 499 days; UK: FTSE 100, 491 days)
markets: US, Germany, UK large-cap equity
tier: B
validation_overlap: false
published_post_2018: false
---

> **Source read in full**, the typeset JIMF article with volume and page headers, from the
> **Bilkent University DSpace repository** (`repository.bilkent.edu.tr`). The route is worth
> reusing: the landing page is an Angular shell full of UUIDs, so go straight to the REST API —
> `/server/api/core/items/<item-uuid>/bundles` → the `ORIGINAL` bundle's `/bitstreams` → the
> bitstream's `_links.content.href`. 259 KB PDF → 52 KB of clean text, 363 instances of `" the "`,
> zero `( )` dropout. The item UUID came from a plain web search.

## Mechanism

**The economic claim.** Investors operate on different horizons (a market maker's horizon is
intraday, a pension fund's is years), so the covariance between an asset and the market need not
be the same object at every time scale. If horizons are heterogeneous, the CAPM's predictions are
scale-dependent and should be tested scale by scale rather than at whichever return interval the
data happen to arrive at. The paper situates this in the long-standing *intervalling-effect*
literature: estimated betas are known to depend on the return interval used (Levhari–Levy,
Hawawini, Handa et al., Cohen et al.), and a multiscale decomposition is the systematic version
of varying that interval.

**Why this is the construction half of the multi-scale vein.** The paper's real content for this
lab is not its CAPM finding but the **decomposition operator** and the exact arithmetic of what a
"scale" is.

**The arithmetic, and it is the result that decides the vein.** Using the Haar filter, the level-`j`
wavelet coefficient is *the difference of two averages, each formed from `2^{j−1}` consecutive
returns*, and the level-`j` scaling coefficient is *a simple average of `2^j` returns*. The paper
states this explicitly and adds that longer (Daubechies) filters "retain this interpretation as
the difference of **weighted** averages". So:

> **A wavelet multiresolution decomposition of a return series is a basis of
> moving-average-difference filters — a fixed, orthogonal, non-overlapping-passband
> re-parameterisation of exactly the moving-average family the lab already owns.**

Formally: `h = (1/√2, −1/√2)` (differencing, unit energy, orthogonal to even shifts),
`g = (1/√2, 1/√2)` (local averaging), applied in a cascade — filter the series to get
`(w̃_1, ṽ_1)`, re-filter `ṽ_1` to get `(w̃_2, ṽ_2)`, and so on to level `J ≤ log₂ T`, yielding
`w̃ = (w̃_1, …, w̃_J, ṽ_J)`. Level `j` captures frequencies `1/2^{j+1} < f ≤ 1/2^j`; on daily data
that is scale 1 ↔ 2–4 day dynamics, 2 ↔ 4–8, 3 ↔ 8–16, 4 ↔ 16–32, 5 ↔ 32–64, 6 ↔ 64–128 days. No
information is added or removed by the transform (unit energy), so **the decomposition itself
cannot create a signal; it can only re-sort one into passbands.**

## Construction recipe

Complete enough to implement without the paper:

1. **Inputs.** Daily log returns `r_{it} = log P_{it} − log P_{i,t−1}` per name, a market index
   return `r_{mt}` from the same, and a short rate `r_{0t}`. Work with premia `r_{it} − r_{0t}`
   and `r_{mt} − r_{0t}`.
2. **Transform.** Apply the maximal-overlap discrete wavelet transform with the **Daubechies
   least-asymmetric filter of length 8, LA(8)**, to each premium series, for scales `j = 1 … J`.
3. **Wavelet variance and covariance.** `σ²_{mj} = Var(w̃_{mj})` and `Cov(w̃_{mj}, w̃_{ij})`,
   computed from the coefficients at level `j`, **excluding coefficients affected by the
   boundary**.
4. **Scale-wise beta.** `β^w_{ij} = Cov(w̃_{mj}, w̃_{ij}) / σ²_{mj}` — the ordinary beta formula
   evaluated inside one passband.
5. **Books.** For each scale separately: estimate every name's `β^w_{ij}` on a **one-year**
   formation window, rank, form 10 (and 15) **equal-weighted** portfolios from low to high beta,
   hold for the **following year**, record each portfolio's realised return and its beta, then
   roll forward a year and repeat. Test the CAPM by regressing portfolio average return on
   portfolio beta and comparing the slope with the realised average market premium.
6. **Scale ceiling.** With annual re-formation, `J = 6` is the highest usable level on daily data,
   because scale 7 (128–256 days) is the length of the formation window itself.

**What the paper does *not* supply, and it is the thing the [2026-10-26] criterion asked for:**
there is **no recombination rule**. The `J` scales are never recombined into one signal; they are
used to form `J` separate rankings and `J` separate sets of portfolios.

## Robustness evidence (qualitative only)

- **Direction of the finding.** The relation between a portfolio's return and its beta is weak at
  the shortest scales and **strengthens monotonically as the wavelet scale increases**; the
  authors conclude CAPM predictions are "more relevant at medium- to long-run horizons".
- **Multi-market, but very unevenly.** The US evidence rests on ≈ 28 years of daily data across
  S&P 500 constituents with annual re-formation. The German (DAX30) and UK (FTSE 100) exercises
  each rest on **about two years of daily data (499 and 491 observations) with a single
  full-sample beta estimate**, not a rolling one — so they are an illustration of the method in
  two more markets, not independent multi-decade confirmation. Tier is B largely for this reason.
- **No cost treatment of any kind.** No transaction costs, no turnover figures, no execution
  assumptions appear. The annual re-formation makes turnover low by construction, but it is never
  quantified.
- **No multiple-testing acknowledgement.** Six scales × two bucket counts × three markets are
  reported without any adjustment for the number of specifications examined. This matters
  disproportionately here, because the method's defining act *is* to multiply the number of
  specifications by `J`.
- **No replication status to report.** The construction has been widely reused in later
  multiscale-beta work, but the folder found no independent replication of the scale-monotonicity
  finding at the standard of Hou–Xue–Zhang or Jensen–Kelly–Pedersen, and the paper itself is not
  in the anomaly-replication samples those studies cover.
- **Lineage of the method is solid even where this application is thin:** Ramsey and co-authors
  introduced wavelets to economics; Gençay–Selçuk–Whitcher's own 2001 text supplies the estimators
  for wavelet variance/covariance and the boundary treatment.

## Implementability here

**Verdict against the pre-committed criterion ([2026-10-26] open question): the vein fails the
construction test in the form this paper gives it, and the `O(1)` form that survives is a filter
the lab already owns.**

The criterion was: *a wavelet or long-memory proposal decomposes one series into `J` scales and
then needs a rule to recombine them, so ask of the first paper how many free parameters survive
the recombination. Admit it only if the answer is `O(1)` and the recombination weights are fixed
a priori.* The answer here is worse than `J` fitted weights: **there is no recombination at all.**
The paper's design multiplies one ranked book into `J` ranked books, which is a `J`-fold
specification expansion paid for out of the same 2018–2023 window the deflated-skill bar already
counts every trial against. Under the lab's own rules that is the most expensive possible shape.

What survives, and what to do with it:

- **The collapse, stated once so no later session re-derives it.** Fix the recombination weights a
  priori and a Haar multiresolution signal is `Σ_j c_j (MA_{2^{j−1}} − MA_{2^{j−1}, lagged})` with
  constants `c_j` — a weighted moving average of past returns. **Any fixed-weight recombination of
  Haar scales is a linear filter inside the family the lab's lookback sweeps already span**, and
  `notes/2026-08-17-moving-average-rules-anatomy.md` is the note that already characterises that
  family. This is the second consecutive session in which an admitted `O(1)` object turned out to
  be a smoother the lab owns (the first was the EWMA, [2026-10-26]).
- **The one genuinely new thing a wavelet basis buys is non-overlapping passbands.** A sweep over
  moving-average lookbacks produces signals that are heavily correlated with each other, because
  a 20-day and a 40-day mean share 20 days. The wavelet levels are orthogonal by construction. So
  the honest use is **diagnostic, not generative**: decompose a quantity the lab already has and
  read off which horizon band carries it.
- **The free diagnostic worth running, and it costs no trial.** Take an existing candidate's
  **active return against the equal-weight eligible pool**, decompose it by scale, and report the
  wavelet variance per scale. That says at which horizon the book's tracking error — and, with the
  co-decomposition against the pool, its skill — actually lives. Under v3 the gate is a difference
  against one portfolio, so "where in frequency does the difference sit" is directly about the
  statistic being graded. Pure measurement, no holdout, no new book.
- **Anti-candidate: do not rank this panel's book by a scale-wise beta, at any scale.** The lab
  measured on 2026-10-09/10 that **Sharpe is flat in beta here** — the bottom-GK-vol book carried
  beta 0.62 against the pool's 0.98 and earned proportionally less, at the 64th percentile of its
  own null. A scale-6 beta sort is a beta sort; a long-only fully-invested high-beta tilt buys
  return in proportion to risk and the gate scores Sharpe. The paper's finding, even taken at face
  value, is about the *cross-sectional slope of mean return on beta*, which is not skill under a
  pool benchmark.
- **Where it would otherwise fit the protocol well, which is worth recording because so little
  does.** The construction is **annual formation, annual holding, equal-weighted deciles** — about
  1× name turnover a year, squarely inside the cheap corner v3 leaves open (the lab priced a
  100-name book at 1.3× turnover at ≈ 14 bps/yr). If a scale-wise *non-beta* characteristic ever
  looked promising, this is the right cadence for it.
- **Protocol hazard, and it is specific.** Two distinct lookahead routes, both easy to miss:
  1. **Boundary coefficients.** The paper itself discards coefficients "affected by the boundary"
     when estimating wavelet variance. In a backtest the relevant boundary is the **present**: a
     MODWT computed on a window with circular boundary handling wraps the window's *end* into its
     *start*, so the early coefficients of each formation window are contaminated by its last
     observations. Use reflection-free, strictly trailing filtering, or drop the first `L_j − 1`
     coefficients of every window.
  2. **Phase alignment.** Least-asymmetric filters such as LA(8) are normally *circularly shifted*
     to align coefficients with features in the original series. That shift is forward in time:
     the aligned coefficient dated `t` then draws on observations after `t`. This is my inference
     from the filter mechanics, not a statement the paper makes — but it is exactly the class of
     thing `causality_check` fails, and the safe form is to treat level `j` as a **causal FIR
     filter of length `L_j`** applied to trailing data with no alignment step. With the Haar
     filter the question does not arise, which is a second reason to prefer Haar here.
  3. The **scale ceiling, the filter choice and `J` itself** are hyperparameters in item `#311`'s
     sense; fix them a priori.
- **Runtime.** A level-`J` cascade is `O(J · L · n)` per series — linear, trivially inside the
  ~60 s per-call budget even at the v2 panel's width. Cost is not the obstacle; the specification
  count is.

## Related

- `notes/2026-08-17-moving-average-rules-anatomy.md` — the family a fixed-weight wavelet
  recombination collapses into.
- `notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md` and SUMMARY `#312` — the
  previous instance of an admitted `O(1)` object turning out to be a smoother already owned.
- `notes/2026-10-27-modified-rescaled-range-and-the-long-memory-null.md`,
  `notes/2026-10-27-hurst-estimator-finite-sample-confidence-intervals.md`,
  `notes/2026-10-27-long-memory-and-regime-switching-identification.md` — the null side of the
  same multi-scale vein; this is its construction side.
- `notes/2026-09-21-har-rv-volatility-cascade.md` — the other "different horizons, one series"
  construction in the folder, and the one that *does* recombine with `O(1)` fixed structure
  (three fixed horizons, three fitted coefficients). Worth comparing: HAR is what a
  multiscale decomposition looks like when someone does impose a recombination rule.
- `experiments/learnings.md` 2026-10-09/10 — "Sharpe is flat in beta on this panel", which is what
  makes the paper's own book an anti-candidate here.
