---
title: "Robust Standard Errors for Panel Regressions with Cross-Sectional Dependence"
authors: Hoechle
year: 2007
venue: The Stata Journal 7(3), 281–312 (venue tier 3 by this folder's rubric — a software journal — but carrying its own theorem-free derivation and its own Monte Carlo study, and cited at a Tier-1 rate)
url: https://doi.org/10.1177/1536867X0700700301 — read in full from the free AgEcon Search copy, https://ageconsearch.umn.edu/record/119278/files/sjart_st0128.pdf (385 KB; `pdftotext -layout` → 97 KB of text, 411 instances of `" the "`, no ASCII shift)
citations: 2773 (Crossref `is-referenced-by-count`, checked 2026-11-18)
sample_period: Monte Carlo throughout (1,000 replications per parameter setting). One empirical illustration uses a monthly panel of 219 European stocks over Stata months 491–551, i.e. roughly end-2000 to end-2005. No part of the sample touches 2018–2023
markets: simulated panels; the illustration is European large-cap equities
tier: B
validation_overlap: false
published_post_2018: false
---

## Mechanism

Nominated in the folder's open question as *"the construction half"* of the primary aim, to be
*"admitted and graded honestly"*. It earns more than that, because it supplies three things the
original does not: the **formula for an unbalanced panel** (the lab's exact case), an
**operational bandwidth default**, and a **pre-test plus decision rule** for whether to use the
estimator at all.

**1. The unbalanced-panel adjustment, and it is one symbol.** Driscoll–Kraay's original
formulation assumes a balanced panel. Hoechle's modification is to let the inner sum run over the
names actually present on that date:

> `Ω̂_j = Σ_{t=j+1..T} h_t(θ̂) h_{t−j}(θ̂)'`,  with  `h_t(θ̂) = Σ_{i=1..N(t)} h_it(θ̂)`

— *"the sum of the individual time-`t` moment conditions runs from 1 to `N(t)`, where `N` is
allowed to vary with `t`. This small adjustment to Driscoll and Kraay's (1998) original estimator
suffices to make their estimator ready for use with unbalanced panels."* Everything else is
unchanged: `V̂(θ̂) = (X'X)^{-1} S_T (X'X)^{-1}`, Bartlett weights `w(j,m) = 1 − j/(m(T)+1)`, and
for pooled OLS `h_it(θ̂) = x_it ε̂_it = x_it (y_it − x_it'θ̂)`. The panel may also contain **gaps**
(a name present, then absent, then present again), and missing values are handled.

**2. The operational bandwidth.** The theorem only gives a rate (`m(T) = O(T^{1/3})`). The
implemented default is the standard Newey–West plug-in,

> `m(T) = floor[ 4 (T/100)^{2/9} ]`

which is a *lag length*, chosen from `T` alone and from nothing about the data. Note what this
means: at `T = 100` it is 4; the rule is extremely flat in `T`, so the bandwidth is effectively a
small constant over any panel length the lab will ever have. Whether that is adequate is exactly
what tonight's third source attacks.

**3. The decision rule, and the price of using the estimator when you did not need to.** This is
the finding that makes the note worth more than its venue tier. Hoechle's Monte Carlo includes a
**reference scenario with no cross-sectional dependence at all**, and there the Driscoll–Kraay
standard errors are *"slightly worse"* calibrated than the conventional alternatives — clustered
("Rogers") standard errors on pooled OLS are the ones that hit nominal coverage. So robustness is
**not free**, and the article's own conclusion is a conditional, not a blanket recommendation:

> *"To ensure that statistical inference is valid, testing whether the residuals of a linear panel
> model are cross-sectionally dependent is therefore important. If they are, then statistical
> inference should be based on the Driscoll–Kraay estimator. However, when the residuals are
> believed to be spatially uncorrelated, then Rogers standard errors are preferred."*

The named pre-test is **Pesaran's CD test** (null: residuals cross-sectionally uncorrelated),
which the article notes is *"suitable for panels with `N` and `T` tending to infinity in any
order"* and is the only one of the three implemented cross-sectional-independence tests
**adequate for unbalanced panels**. The test output also reports the **average absolute
off-diagonal residual correlation**, which is the magnitude `#460`'s inflation factor needs as an
input and which the lab currently has no instrument for.

## Construction recipe

1. Fit the pooled OLS (or within-transformed fixed-effects) regression normally.
2. **Pre-test**: compute Pesaran's CD statistic on the residuals, and read off the average
   absolute off-diagonal correlation. Reject ⇒ step 3. Fail to reject ⇒ use clustered standard
   errors, which are better calibrated in that case.
3. Form `h_it = x_it ε̂_it`; sum within date over the `N(t)` names present.
4. Newey–West the `{h_t}` sequence with lag `m(T) = floor[4(T/100)^{2/9}]` (or a stated
   alternative) and Bartlett weights; sandwich with `(X'X)^{-1}`.
5. For fixed effects, within-transform first: `z̃_it = z_it − z̄_i + z̄`, where `z̄_i` is the unit
   mean over that unit's `T_i` present dates and `z̄` the grand mean weighted by `T_i`. Then run
   steps 3–4 on the transformed data.
6. **Reference implementation exists**: the Stata `xtscc` command, itself based in part on
   Driscoll's own GAUSS code. Useful as an unambiguous primary for the construction, not as a
   dependency.

## Robustness evidence (qualitative only)

The Monte Carlo is designed around a two-component error, `ε_it = ε̄_i + λ_i f_t + ϑ_it` with
`f_t` an AR(1) common factor and `λ_i ~ U[ι₁, ι₂]` heterogeneous loadings — i.e. exactly the
"arbitrary loadings on a common factor" case Driscoll–Kraay identified as the one that **survives
time dummies**. Six dependence scenarios span expected between-subject correlations of
0, 0.125, 0.25 and 0.64, crossed with autocorrelation 0, 0.25, 0.5, at 1,000 replications each.

**The simulation's scale is the single most relevant fact about it for this lab: `N = 1,000`
subjects with `T = 40`, and a second set at `N = 2,500` with `T = 5, 10, 15, 25`.** The lab's
eligible cross-section is ~1,000 names. The published findings (the coverage numbers themselves
live only in chart form and are **not** restated in the prose, so they are not carried here):

- With **no** cross-sectional dependence, conventional and clustered standard errors are well
  calibrated and Driscoll–Kraay is slightly worse. Clustered standard errors on pooled OLS are
  the best-calibrated estimator in that case.
- With dependence present, OLS, White, clustered and Newey–West standard errors give coverage
  *"far below"* nominal for both pooled OLS and fixed effects, and the shortfall is **monotone in
  the degree of cross-sectional dependence**. Driscoll–Kraay standard errors are also slightly
  optimistic but *"much better calibrated"* and — the key property — their coverage is *"almost
  invariant to changes in the level of cross-sectional and temporal correlation."*
- **Dependence in the regressor matters separately from dependence in the residual.** Comparing
  the scenario pair that holds residual correlation at 0.125 and raises regressor correlation from
  0.125 to 0.64, *"an increase in the cross-sectional dependence of the explanatory variable `x_it`
  exacerbates underestimation of the standard errors."* This is an **independent corroboration of
  Petersen's product form** `1 + (m−1)ρ_X ρ_ε` (`#460`) on the cross-sectional axis: both
  correlations enter, and either one at zero removes the problem.
- **Once cross-sectional dependence is present, the extra damage from serial correlation is
  "relatively small."** The highest average autocorrelation simulated is `0.5 · 0.8² = 0.32`.
- **Fixed effects do not help and can hurt**: *"although the true model contains
  individual-specific FE, the coverage rates of the within regressions are actually lower than
  those of the pooled OLS estimation."*
- **The unbalanced-panel results are "qualitatively similar" to the balanced ones**, so the `N(t)`
  adjustment works. The unbalanced design drops names progressively from a full start, ending with
  about half the observations.
- **The small-`T` sweep is the honest part.** At `N = 2,500` and `T = 5, 10, 15, 25`,
  Driscoll–Kraay still dominates OLS and clustered standard errors whenever dependence is present,
  and the conventional estimators' failure holds *"irrespective of the panel's time dimension
  `T`"* — but *"the longer the time dimension `T` of a panel is, the better calibrated are the
  Driscoll–Kraay standard errors."* So short `T` degrades the robust estimator without rescuing
  the conventional ones: the choice at short `T` is between a biased estimator and a worse one.
- **Grading.** Tier **B**, not A: the venue is a software journal, the derivation is a restatement
  rather than a new theorem, and the Monte Carlo is the author's own and unreplicated. Against
  that, it is cited at a Tier-1 rate (2,773), its simulation design is explicitly built to break
  the alternatives it tests, and the finding that **matters most to this lab** — that the robust
  estimator costs calibration when there is nothing to be robust to — runs *against* the
  article's own advocacy, which is the honesty signal the rubric asks for.

## Implementability here

**The `N(t)` line is the whole reason this note exists.** Protocol v2's panel is point-in-time:
roughly a thousand names are eligible on a typical validation date, the set turns over, and
columns appear only once a name has been eligible. That is an unbalanced panel with gaps, which
is the case the original estimator does not cover and this one does, at the cost of one index
change. Any dependence-robust standard error the lab computes on its own panel must use this
form.

**The pre-test is a free measurement the lab has never made, and it answers a question the record
has been arguing about.** Pesaran's CD test on the residuals of a pooled predictive regression
costs one pass over stored validation frames, needs no holdout, and returns two things the lab
wants: whether cross-sectional dependence is present at all, and the **average absolute
off-diagonal residual correlation** — which is the one unmeasured input to `#460`'s inflation
table. The lab currently has `rho = +0.0888` as the mean pairwise **cross-trial** active-return
correlation (2026-11-18 nightly); that is a different object from the mean pairwise
**cross-name within-date residual** correlation, and nothing in the record has measured the
latter. If it comes back near zero, `#460`'s bracket collapses and the i.i.d. standard error is
defensible on the forecast side too — a cheaper outcome than adopting a new estimator. If it comes
back at the level the article's own equity illustration found, the bracket is large and the
estimator is needed.

**Bandwidth, concretely.** At the lab's daily validation grid (`T = 1,562`) the default rule gives
`floor[4·(15.62)^{2/9}] = 7` lags; at ~251 month-ends it gives 4; at 72 month-ends, 3. The rule is
nearly flat, which is convenient and is also the thing to be suspicious of — see the companion
note, where a misspecified lag length is shown to be the binding error rather than the panel
length.

**Pitfalls.**

1. **Do not adopt the estimator unconditionally.** The article's own simulation says it is the
   *worse* choice when the cross-section is independent. The lab should run the pre-test first and
   record the answer, exactly as `#453` made an audit free rather than optional.
2. **Do not read fixed effects as a safety margin.** Within-transformation lowered coverage
   relative to pooled OLS in the simulation even when the true model had unit fixed effects.
3. **Do not carry the illustration's magnitude as a prior.** Its equity panel reported an average
   absolute residual correlation of 0.160 between two stocks, but that is 219 European large-caps
   on monthly bid–ask spreads over ~2001–2005 — a different dependent variable, a different
   frequency and a narrower panel than this lab's. Measure it here; do not assume it.
4. **The reference implementation is Stata.** The formula above is complete and the lab should
   implement it directly; nothing here requires the package.

## Related

- `notes/2026-11-18-covariance-estimation-without-specifying-cross-sectional-dependence.md`
  (this session) — the original estimator, its conditions, and its cost stated as a required `T`.
- `notes/2026-11-18-inference-without-a-bandwidth-and-the-distortion-that-does-not-shrink.md`
  (this session) — the adversarial third, which attacks the bandwidth default this note supplies.
- `notes/2026-11-17-which-dependence-structure-licenses-which-standard-error.md` — Petersen's
  product form, which this article independently corroborates on the cross-sectional axis.
- `notes/2026-11-17-clustering-as-a-design-question-not-a-correlation-question.md` — the standing
  warning that this article's test-then-choose rule is a *correlation* criterion, which `#464`
  holds is not the right criterion for a sampling-and-assignment decision. The tension is explicit
  and is carried, not resolved.
