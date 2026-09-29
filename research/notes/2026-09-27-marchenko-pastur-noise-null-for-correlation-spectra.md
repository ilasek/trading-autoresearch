---
title: "Noise Dressing of Financial Correlation Matrices — the random-matrix null for an estimated spectrum"
authors: Laloux, Cizeau, Bouchaud, Potters
year: 1999
venue: Physical Review Letters 83(7), 1467–1470 (Tier 1 for its field — peer-reviewed, heavily cited; it is physics rather than finance, which is the only discount)
url: https://doi.org/10.1103/PhysRevLett.83.1467
citations: 1189 (Semantic Scholar by DOI, checked 2026-09-27); 1077 (Crossref, checked 2026-09-27)
sample_period: 1991–1996
markets: 406 S&P 500 constituents, daily (T = 1309); the analysis is stated to have been repeated on other major markets (Paris named) with "very similar results", and on a matrix of intraday-estimated volatilities rather than returns
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full**, from the arXiv preprint (`cond-mat/9810255`, 20 Oct 1998 — three pages, the
whole Letter). The published PRL version was not fetched; `journals.aps.org` was not tried. One
internal discrepancy in the version read, recorded because it is the sort of thing to check before
quoting: the body says the largest eigenvalue is "25 times larger than the predicted `λmax`" and the
figure caption says "30 times greater". Nothing below rests on either number.

**Why this folder is reading a 1999 physics Letter.** The 2026-09-26 nightly ran this file's
highest-ranked screen — the inverse-Herfindahl effective rank `EffRank = (tr A)²/tr(A²)` of a
characteristic-managed-portfolio second-moment matrix — and found that it **reads anything you like
depending on which columns go in** (0.208·P to 0.638·P on four defensible versions of the same
fourteen characteristics), because near-duplicate columns concentrate a spectrum mechanically. The
session then did the right thing by hand: it ran the statistic on an i.i.d. control and on a placebo,
got 0.775·P and 0.875·P, and concluded that the *placebo* rather than `P` is the ceiling. That is an
ad-hoc, simulated version of a question this literature answered in closed form in 1999 — **what does
the spectrum of an estimated covariance matrix look like when there is nothing in it?** — and the
answer comes with a second, parameter-free test attached.

## Mechanism

There is no effect here to believe in; the content is an estimation fact. A correlation matrix over
`N` series has `N(N−1)/2` distinct entries and is estimated from `N` series of length `T`. When `T`
is not large relative to `N`, the estimate is *mostly noise*, and the noise is not diffuse — it has a
known shape.

Write `C = MM'/T` with `M` the `N × T` matrix of standardized observations. Under the null that the
entries of `M` are i.i.d. with variance `σ²`, the density of eigenvalues of `C` converges, as
`N, T → ∞` with `Q = T/N ≥ 1` fixed, to

```
ρ(λ) = (Q / 2πσ²) · sqrt((λmax − λ)(λ − λmin)) / λ ,     λ ∈ [λmin, λmax]
λmax, λmin = σ² · (1 + 1/Q ± 2·sqrt(1/Q))
```

(the Marchenko–Pastur law; the source cites Sengupta–Mitra). Three features carry all the content:

- **The bulk has two hard edges.** In particular the *lower* edge is strictly positive for `Q > 1`:
  under pure noise there are **no** eigenvalues between 0 and `λmin`. The density has a sharp maximum
  near that lower edge, diverging as `1/sqrt(λ)` in the limit `Q = 1`.
- **The upper edge is where "information" starts.** Eigenvalues above `λmax` are the ones the null
  cannot produce. Fitting the bulk and counting what sticks out above it is the whole procedure.
- **The smallest eigenvalues are the noisiest, and they are exactly the ones a minimum-variance
  optimizer loads on.** This is the paper's punchline and it is a statement about *construction*, not
  about any period: the least-risky-portfolio directions of a Markowitz problem are the
  bottom of the spectrum, which is where the estimate is least trustworthy. The authors' own
  conclusion is that "Markowitz's portfolio optimisation scheme based on a purely historical
  determination of the correlation matrix is not adequate".

Even when the *true* correlation matrix is the identity, its finite-sample estimate has nontrivial
eigenvalues and eigenvectors. The null is not "the matrix is the identity"; it is "the matrix is an
estimate of the identity from `T` points".

## Construction recipe

**The spectral test.**

1. Standardize each series to zero mean and unit variance over the window (the derivation assumes
   it; skipping it makes `σ²` meaningless).
2. Compute `Q = T/N` and the eigenvalues `λ₁ ≥ … ≥ λ_N` of the sample correlation matrix.
3. The naive null sets `σ² = 1`. It will usually be rejected immediately by `λ₁`, which on equity
   data is the market direction and sits far above `λmax`. That is not a refutation of the method; it
   is the first eigenvalue being real.
4. **Remove the known direction and re-set the null's variance.** Having attributed `λ₁` to a market
   factor, the variance left for the noise part is `σ² = 1 − λ₁/N`. Refit.
5. **Or treat `σ²` as a free parameter** and fit the bulk, which is the version the source prefers;
   it reports the best fit at `σ² = 0.74` on its sample, with the bulk then accounting for the large
   majority of the spectrum and the top few percent still clear of the edge. Allowing a slightly
   smaller effective `Q` fits better still, which the authors attribute to volatility clustering.
6. For finite `N` the edges are blurred, so a small number of eigenvalues just outside
   `[λmin, λmax]` is expected under the null and is not evidence of anything.

**The eigenvector test, which has no adjustable parameters at all and is the more valuable half for
this repo.** Normalise an eigenvector so that `Σᵢ v²_{α,i} = N`. Under the no-information null the
distribution of its components, taken across `i` for fixed `α`, is the maximum-entropy distribution
with `E[u²] = 1` — i.e. standard normal (the Porter–Thomas distribution in the random-matrix
literature). The source reports this fitting the empirical component histograms of eigenvectors
inside the bulk "extremely well, with no adjustable parameters", and failing visibly for the top
eigenvector. **So an eigenvector can be tested for emptiness without fitting `σ²`, without choosing
`kmax`, and without believing the bulk fit.**

## Robustness evidence (qualitative only)

- The bulk fit is reported as reproducing across markets (a second major market is named) and, in a
  separate matrix, across *volatilities* rather than returns — i.e. the phenomenon is a property of
  estimating a correlation matrix, not of any one panel.
- It is a limit theorem, so the evidence that matters is mathematical rather than empirical:
  Marchenko–Pastur is not an anomaly that can decay. What *is* period- and panel-specific is the
  number of eigenvalues found above the edge, and this note records none of the kind.
- Known limits the source states itself: the law is an `N → ∞` result and the edges are blurred at
  finite `N`; volatility clustering biases the effective `Q`; and the fitted `σ²` is a free parameter
  in the version that fits best, which is exactly the kind of knob this folder has learned to
  distrust — hence the eigenvector test as the parameter-free fallback.
- The wider random-matrix-in-finance literature is enormous and only one Letter was read here; nothing
  below rests on the follow-up work (eigenvalue clipping, Marchenko–Pastur-based cleaning schemes),
  which is covered from a different angle in the nonlinear-shrinkage note filed the same day.

## Implementability here

**This is a diagnostic, not a strategy, and that is the point — it is free.** No trial, no candidate
file, no holdout.

- **The direct use is the one the lab already needed.** Any "is this universe's spectrum concentrated
  or dispersed" reading needs a reference distribution, and the lab built one by simulation. The
  closed form is cheaper and, more importantly, *states its own assumptions*: `Q = T/N`,
  standardized columns, i.i.d. entries. The lab's discovery that its i.i.d. control read 0.775·P
  rather than `P` "because it inherits the real panel's unequal column SDs" is precisely the
  standardization step of this recipe being skipped — with columns standardized the control should
  land much closer to the analytic value. That is a **checkable prediction about the lab's own
  control**, and it costs one re-run of a screen it has already written.
- **Dimensions here.** For the instrument panel: `N ≈ 145`, and a 250-day estimation window gives
  `Q = 1.724`, `1/Q = 0.580`, `2·sqrt(1/Q) = 1.523`, hence `λmax = 3.103·σ²` and
  `λmin = 0.057·σ²`. So with a one-year window **the pure-noise bulk alone spans a
  fifty-fold range of eigenvalues**, from near zero to three times the average. Any statement of the form "the top three PCs hold
  78% of variance, therefore the universe is low-dimensional" has to be read against that, and the
  lab's seated `E/Var` construction uses exactly a 250-day window on ≥45 names.
- **The eigenvector test is the part worth adopting as standing discipline.** It converts "is this
  PC real?" into a one-line Shapiro/Anderson–Darling-style comparison of the PC's *loading*
  distribution against `N(0,1)`, using no returns, no thresholds, and no free parameters. It is
  available for every `K` in every PCA-residual construction this repo has run, and it answers a
  different question from the variance share: a direction can hold 8% of variance and still have
  Gaussian loadings, i.e. be empty.
- **What it does not license.** It says nothing about *returns*. The `SUMMARY.md` #70 screen — that
  eigenvalue ordering should line up with mean returns — was refuted by the lab on 2026-09-03 (the
  statistic was a product of Sharpe and PC volatility; scale-free it read +0.367 against an n = 14
  critical value). **Nothing here revives it.** A direction being above the noise edge means it is
  not measurement error; it does not mean it is paid.
- **Pitfall, and it is the one that matters most on this universe.** The null is i.i.d. entries.
  Duplicated or near-duplicated columns violate it, and so does serial dependence in volatility. On a
  *feature* panel where the columns are three nested momentum legs and four volatility estimators,
  the Marchenko–Pastur bulk is the wrong null and the test is uninformative — which is the same
  conclusion the lab reached by hand, and the companion note filed today shows it is an
  *identification* failure that no eigenvalue-counting method escapes.
- Costs, turnover and the long-only constraint never enter, because nothing is traded.

## Related

- `notes/2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` — names
  Marchenko–Pastur spread as the pitfall that inflates every `M_eff` estimator, and prescribes the
  same i.i.d. control. This note is the closed form behind that pitfall.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the eigenvalue-based
  diversification functional this repo already uses, and the source of its eigenvalue-saturation
  measurement.
- `notes/2026-09-27-counting-factors-eigenvalue-estimators.md` — what to do when you want a *number*
  rather than a picture, and why the number is not identified when the idiosyncratic part is
  cross-correlated.
- `notes/2026-09-27-nonlinear-shrinkage-instead-of-counting.md` — the decision-theoretic alternative:
  do not count eigenvalues, correct them.
- `notes/2026-09-24-long-only-minimum-variance-composition.md`,
  `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — the minimum-variance
  constructions this note's punchline is about.
- `experiments/learnings.md` [2026-09-03] — the refuted #70 eigenvalue/mean-return screen.
- `experiments/learnings.md` [2026-09-26] — `EffRank`'s free parameter, the 0.775·P i.i.d. control
  and the 0.875·P placebo, which this note reinterprets as an un-standardized bulk.
