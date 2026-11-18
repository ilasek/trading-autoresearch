---
title: "Consistent Covariance Matrix Estimation with Spatially Dependent Panel Data (read as: Spatial Correlations in Panel Data)"
authors: Driscoll, Kraay
year: 1998 (working-paper version 1995)
venue: The Review of Economics and Statistics 80(4), 549–560 (venue tier 1). Read in full from the World Bank Policy Research Working Paper 1553 version (December 1995, 28 pages), which carries the same theorem, the same examples and the same Monte Carlo design
url: https://doi.org/10.1162/003465398557825 — paywalled (MIT Press). Working paper read as the World Bank's own text rendition, https://documents1.worldbank.org/curated/en/944831468739460842/txt/multi0page.txt (58 KB of text, 299 instances of `" the "`), located via the World Bank documents API (`search.worldbank.org/api/v2/wds?qterm=...&fl=pdfurl,txturl`) after the RePEc-listed `www-wds.worldbank.org` path redirected to a landing page. WP DOI 10.1596/1813-9450-1553
citations: 6237 (Crossref `is-referenced-by-count`, checked 2026-11-18); 6941 (Semantic Scholar, checked 2026-11-18). The working-paper DOI separately carries 2
sample_period: theorems and Monte Carlo throughout. The simulation's cross-sectional covariance matrix was calibrated from two annual macro panels (20 US states, gross state product 1963–1986; 24 OECD economies). No part of the sample touches 2018–2023
markets: none traded. Macro output-growth panels are used only to supply a realistic dependence matrix to the simulator
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source the folder's standing primary aim asked for by description: **a covariance
estimator that requires no specification of the cross-sectional dependence — no cluster variable,
no spatial weights matrix, no assumed factor count — whose cost is paid in panel length.** It
meets all three acceptance criteria, and the mechanism is one idea.

**The idea: collapse the cross-section, then treat the result as a time series.** Write the
moment conditions of whatever estimator you are using, `h_it = ψ(θ, z_it)` (for OLS,
`h_it = x_it ε̂_it`). Define the **cross-sectional average at each date**,

> `h_t = Σ_i h_it`   (one vector per date, summed or averaged over the names alive that date)

and then apply the ordinary Newey–West HAC estimator to the univariate sequence `{h_t}`:

> `S_T = Ω̂_0 + Σ_{j=1..m(T)} w(j,m) [Ω̂_j + Ω̂_j']`,  `Ω̂_j = Σ_t h_t h_{t−j}'`,
> `w(j,m) = 1 − j/(m(T)+1)`,  `m(T) = O(T^{1/3})`

with `V_T = D_T^{-1} S_T D_T^{-1}` and, for OLS, `D_T = (X'X)/(NT)`. That is the whole estimator.
Driscoll and Kraay's own framing: their result "may be viewed as the case in which `N = 1`" of
Newey–West — i.e. **Newey–West applied to the time series of cross-sectional averages of the
moment conditions.**

**Why that works, and why it is the only direction that can work.** The decisive move is in the
*definition of mixing*, and it is deliberately **asymmetric between the two axes**. The standard
random-field literature requires dependence to die as Euclidean distance `((i−j)² + s²)^{1/2}`
grows, which would require (a) a cross-sectional *ordering* and (b) ruling out equal
contemporaneous cross-unit correlation, since that correlation does not decline in `|i−j|`.
Driscoll–Kraay instead require only that the dependence between `h_it` and `h_j,t−s` die **as the
time separation `s` grows, for any pair `i, j`** — the `i = j` case being the usual time-series
definition. The authors state the motivation explicitly: *"unlike in the time dimension, in most
cases there is no natural ordering in the cross-sectional dimension."*

The payoff is a property of exactly the right shape: a random field mixing in this asymmetric
sense has **cross-sectional averages `h_t` that form a univariate mixing sequence of the same
size, for any `N`, including `N → ∞`.** The cross-sectional dimension is averaged out of the
problem before any variance estimation happens, so no amount of cross-sectional dependence or
width can break it. Nothing about the dependence has to be named, parameterised, ordered or
grouped; it is *absorbed* rather than *modelled*.

**What the authors are explicit cannot be done, and it is the sharpest thing in the paper.** The
conclusion states that for **small `T`, or a single cross-section, the problem "appears much less
tractable"**: because there is no natural ordering in the cross-section, *"it is not possible to
construct the pure cross-sectional analogs of time-series HAC estimators"*, and inference on one
cross-section with spatial correlation *"will have to continue to rely on some knowledge of the
form of these spatial correlations."* The asymmetry that makes the estimator work is also the
reason it has no one-date version.

## Construction recipe

1. **Estimate `θ` as usual.** OLS (or GMM) coefficients are consistent under cross-sectional
   dependence; only the standard errors are wrong, so no re-estimation is needed.
2. **Form residuals, then the per-date moment conditions** `h_it = x_it ε̂_it`.
3. **Sum over names within each date** to get one `h_t` per date. This is where the width goes.
4. **Newey–West the `{h_t}` series** with Bartlett weights `w(j,m) = 1 − j/(m(T)+1)` and
   bandwidth of order `T^{1/3}` (the theorem's rate; an operational default is in the companion
   note).
5. **Sandwich**: `V̂ = D̂_T^{-1} S_T D̂_T^{-1}`; standard errors are the square roots of the
   diagonal. For a fixed-effects specification, within-transform the data first (subtract unit
   means) and then run the same recipe.
6. **Conditions to assert, not test** (the theorem's Assumption 1 is the only substantive one):
   arbitrary **contemporaneous** cross-sectional correlation is allowed; **lagged**
   cross-sectional correlation must decay as the time separation grows; `T → ∞`; `N` is
   unrestricted and may exceed `T` or diverge at any rate relative to it.
7. **A sufficient condition that is checkable by construction.** Because the mixing-random-field
   assumption is hard to verify directly, the paper proves that a **factor structure**
   `ε_it = λ_i' f_t + v_it` satisfies it — for any number of factors `M`, any loadings `λ_i`, and
   (per their footnote) even with the `v_it` arbitrarily cross-sectionally correlated. Three
   nested cases are worked: equal loadings (time dummies would suffice); group-wise equal
   loadings (a region/sector block structure); and **arbitrary loadings on a common factor, where
   spatial correlation survives even after time dummies are included**. Lagged dependence is
   obtained by giving the factors their own autocovariance. So "does my dependence satisfy the
   assumption?" reduces in practice to "is it representable as a factor structure plus noise?",
   which for an equity panel it is.

## Robustness evidence (qualitative only)

- **The comparison is against two named alternatives and both are shown to fail in the lab's own
  regime.** *Time dummies* are the correct correction only if contemporaneous cross-unit
  correlations are **equal for every pair** and lagged cross-unit correlations are **zero**; under
  heterogeneous loadings on a common factor, or lagged spillover, the resulting estimator's
  properties are *"in general unknown"*. *SUR/FGLS* must estimate `N(N+1)/2` free parameters from
  `NT` observations, so it needs `T ≫ (N+1)/2` — infeasible whenever the cross-section is wide.
- **Monte Carlo coverage, the paper's own headline (simulation numbers, not market performance).**
  With the dependence matrix calibrated from observed macro panels, coverage of nominal-95%
  intervals at `T = 25` and `T = 50`: OLS-with-time-dummies never above **.694**, SUR never above
  **.679**, the HAC estimator in the range **.818–.903**. SUR is poor *even when correctly
  specified* (the `ρ = 0` column), because the covariance matrix it needs is estimated too
  imprecisely.
- **An earlier draft's parameter sweep, reported in a footnote**, found: time dummies perform
  poorly under heterogeneous response to a common factor and under lagged cross-sectional
  correlation; SUR performs well only when `N` is very small relative to `T`; and the HAC
  estimator performs well **in all cases, even at `T` as low as 25, with performance that does not
  depend on the size of the cross-section, which may be arbitrarily large.**
- **The cost, stated as a required `T`.** Consistency rests entirely on large-`T` asymptotics, and
  the authors name the operational floor themselves: *"our Monte Carlo simulations suggest that a
  value of `T = 20` or `T = 25` is the minimum."* Coverage at that floor is **.82–.90** against a
  nominal .95 — i.e. the estimator is **anticonservative** in finite samples, not conservative.
- **Replication status.** The estimator is extremely heavily cited and has a published independent
  implementation plus independent Monte Carlo evidence (Hoechle, companion note), and its
  conditions were later given **primitive** form by a separate literature (Hidalgo–Schafgans,
  companion note) — which is also where its finite-sample behaviour is challenged. The dependence
  calibration used in the simulations is macroeconomic, not equity; the magnitudes it implies
  should not be carried over.

## Implementability here

**What this is for.** It is not a strategy. It is the instrument for the `#465` *forecast* side:
a claim of the form "this score predicts next month's cross-sectional returns", estimated on the
protocol-v2 panel where **~1,000 names are eligible on a typical date** and the dependence across
them within a date is of **unknown form, with no cluster metric and no natural grouping**. This is
precisely the case `#458` closed off (the many-covariates estimator excludes this panel's
dependence by its authors' own statement), `#460` priced (the i.i.d. inflation factor
`1 + (m−1)ρ_X ρ_ε`, which at a date of ~1,000 names is 1.41×–15.8× across dependence products
0.001–0.25) and `#461` left without a repair (the clustered correction is itself biased at few
clusters). Driscoll–Kraay is the estimator for it, and the reason it fits is structural: the lab
**has** the axis the method charges on. Validation is **1,562 daily dates** (`2018-01-01 ..
2023-12-29`) and ~251 month-ends counted as dates — against DK's own `T ≥ 20–25` floor, both are
far above it, and the daily grid is two orders of magnitude above it.

**Concrete adaptation.**

- **The regression to run it on** is a pooled predictive panel: next-period name return on the
  candidate score (plus whatever controls `#456`/`#457` call for), one row per name-date, with no
  cluster variable. The estimator wants exactly what the lab has — many dates, a wide and
  dependent cross-section.
- **The cheap implementation is a `groupby(date)` and a 1-D HAC.** Compute `h_it = x_it ε̂_it`,
  sum within date to get a `T × (K+1)` matrix of `h_t`, and Newey–West that. The cross-sectional
  width costs nothing beyond the groupby: no `N × N` matrix is ever formed. This is strictly
  cheaper than the within-date permutation the lab already runs.
- **Use it for the forecast claim, not for the balance screens.** `#465` split the lab's practice
  in two: for a claim about the panel the lab *holds*, the sampled-cluster fraction is 1 and
  `#439`/`#445`'s within-date permutation is the correct finite-population instrument. This note
  does not touch that half and must not be read as replacing it.

**Known pitfalls, in the order they will bite.**

1. **It is anticonservative in finite samples, not conservative.** At DK's own floor coverage is
   .82–.90 against .95. Anything derived from it is a *less* severe discount than it looks, and
   the folder's third source tonight quantifies how much worse that gets (see `#475`/`#476`); read
   the companion notes before quoting a `t`.
2. **Two knobs remain, and they are the ones the aim did not eliminate**: the **bandwidth** `m(T)`
   and the implicit assumption that **temporal dependence is homogeneous across names**. The
   estimator is bandwidth-free in the *cross-section* only.
3. **There is no single-date version, by the authors' own conclusion.** A per-date cross-sectional
   regression — a Fama–MacBeth first stage, a one-date IC, a one-date balance test — **cannot** be
   made robust to cross-sectional dependence nonparametrically. The repair is to aggregate over
   dates and charge the dependence on the time axis, or to supply knowledge of the dependence's
   form. This is a refusal the lab should hold, because it rules out a whole class of
   "fix the standard error on this date's cross-section" moves.
4. **`N(t)` varies here.** Point-in-time eligibility means the number of names alive differs by
   date; DK's original formulation assumes a balanced panel. The adjustment is one line and is in
   the companion note.
5. **Do not import the calibration.** The simulations' dependence matrices come from macro output
   growth (the paper reports average cross-sectional correlations of ~0.19 for US states and ~0.31
   for OECD economies, with maxima ~0.63 and ~0.76, as *simulator inputs*). The lab's own measured
   cross-trial active-return `rho` of **+0.0888** is a different object on a different axis and the
   two must not be equated.

## Related

- `notes/2026-11-17-which-dependence-structure-licenses-which-standard-error.md` — Petersen's
  `1 + (m−1)ρ_X ρ_ε`: the price list for ignoring dependence (`#460`) and the few-cluster bias of
  the clustered correction (`#461`) that left this gap open.
- `notes/2026-11-17-many-covariates-variance-estimation-and-its-independence-assumption.md` —
  `#458`: the many-covariates estimator whose own authors exclude clustered, spatial and
  time-series dependence, which is what made this aim binding.
- `notes/2026-11-17-clustering-as-a-design-question-not-a-correlation-question.md` — `#464`/`#465`:
  the design-versus-correlation rule that splits the lab's practice, and the half this note serves.
- `notes/2026-11-18-the-unbalanced-panel-formula-and-when-not-to-use-it.md` (this session) — the
  computable unbalanced-panel formula, the operational bandwidth default, and the pre-test that
  decides whether to use this estimator at all.
- `notes/2026-11-18-inference-without-a-bandwidth-and-the-distortion-that-does-not-shrink.md`
  (this session) — the adversarial third: this estimator's asymptotic `t`-test is oversized at
  every simulated `T`, and under heterogeneous temporal dependence the distortion **does not
  shrink in `T`**.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the folder's only prior HAC
  entry, and it is on the **time** axis (Bartlett long-run variance for overlapping returns);
  the pre-download grep found `Driscoll` and `spatial correlation` at **0** across 300 notes.
