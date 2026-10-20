---
title: "Distributional conformal prediction" — prediction intervals built by permuting the *probability-integral-transform ranks* of a conditional-CDF model, which are independent of the predictors and therefore stay valid under heteroskedasticity where residual-based intervals cannot
authors: Chernozhukov, Wüthrich, Zhu
year: 2021
venue: Proceedings of the National Academy of Sciences 118(48), e2107794118 (venue tier 1 — refereed, with an editor and two referees acknowledged; not a finance journal, so the rubric's finance tier-1 list does not apply, but the venue is unambiguously top-tier)
url: https://doi.org/10.1073/pnas.2107794118
citations: 74 (Crossref `is-referenced-by-count`, checked 2026-10-20); 211 (Semantic Scholar by DOI, same date). The usual direction of the gap for a paper with a long preprint life — first arXiv version 2019.
sample_period: the method is distribution-free and has no sample. Its two empirical illustrations use daily returns of a value-weighted US market portfolio, 1926-07-01 to 2021-06-30, and a 2012 cross-section of US wages.
markets: one aggregate US equity index (market portfolio, daily) and one US labour-market cross-section. No individual stocks, no non-US markets.
tier: A
validation_overlap: true
published_post_2018: true
read: full text of `arxiv.org/pdf/1909.07889` (v3, dated 2021-08-21; 977 KB → 141 KB of clean text, 466 instances of `" the "`, three `( )` dropouts all inside running prose rather than inside a definition, no ASCII shift, title line verified). The v3 preprint is the accepted version — it acknowledges the editor and two referees — and carries the abstract, Sections 1–5, Theorems 1–3, Lemmas 1–2 and Algorithms 1–2. The **SI Appendix** (Algorithm S1, the β-mixing conditions, the distribution-regression details and the optimal-DCP implementation) is referenced throughout and was **not** read; claims that live only there are flagged below as such.
---

## Mechanism

No economic mechanism — this is inference machinery. It belongs in this folder because it answers a
question none of the 204 prior notes touches (`conformal` returns zero across all of them), and
because the question is one the lab's own gating already has an opinion about: **how wide is the
uncertainty around a prediction, and is that width allowed to depend on the state?**

The setting: data `{(Y_t, X_t)}`, predict `Y_{T+1}` given `X_{T+1}`, and report an interval. Two
notions of validity:

- **Unconditional validity**: `P(Y_{T+1} ∈ Ĉ) ≥ 1 − α`, coverage correct *on average over* `X`.
- **Conditional validity**: `P(Y_{T+1} ∈ Ĉ(X_{T+1}) | X_{T+1}) ≥ 1 − α`, coverage correct *at every
  value* of the predictors.

Standard conformal prediction built on a conditional-*mean* model delivers the first and not the
second, and the paper's analytical example shows exactly why in two lines. Take
`Y_t = X_t + X_t·ε_t` with `X_t ~ U(0,1)` and `ε_t ~ N(0,1)` — a pure location-scale model, the
textbook shape of a return panel. A mean-based conformal interval is built from residuals
`R_t = Y_t − E(Y_t|X_t) = X_t·ε_t`, giving

    C_reg(x) = [ x − Q_{|R|}(1−α),  x + Q_{|R|}(1−α) ]

whose **length `2·Q_{|R|}(1−α)` does not depend on `x` at all**. A constant-width interval in a
heteroskedastic model cannot be conditionally valid: it over-covers where the conditional dispersion
is small and under-covers where it is large, by construction, no matter how much data there is.
Distributional conformal prediction (DCP) is instead built from the **probability-integral-transform
rank** `U_t = F(Y_t, X_t)` — here `Φ(ε_t)` — giving

    C_dcp(x) = [ x − x·Q_{|ε|}(1−α),  x + x·Q_{|ε|}(1−α) ]

whose length scales with `x` automatically and is conditionally valid.

**The structural reason, which is the one line worth carrying out of the paper.** Residuals are
*not* independent of the predictors under heteroskedasticity, so permuting them mixes observations
drawn from differently-scaled conditional distributions. **Ranks under the true conditional CDF are
exactly uniform and exactly independent of `X` by construction**, whatever the shape of the
conditional distribution. Permutation inference is legitimate on them and illegitimate on residuals.
Everything else in the paper follows from that substitution.

## Construction recipe

**The conformity score.** With `F̂(·, x)` any estimate of the conditional CDF — quantile regression,
distribution regression, quantile random forests, quantile neural networks; the method is agnostic —
define ranks `Û_t = F̂(Y_t, X_t)` and the score `V̂_t = ψ(Û_t)` with the baseline choice

    ψ(u) = |u − 1/2|

i.e. **distance of the rank from the median rank**. If `F̂(·, x)` comes out non-monotone it is
rearranged first.

**Split DCP (Algorithm 2) — the version to use, because the full version needs a grid search.**

1. Split `{1,…,T}` into `T₁ = {1,…,T₀}` and `T₂ = {T₀+1,…,T}`.
2. Estimate `F̂` on `T₁` only.
3. On the held-out half `T₂`, compute `Û_t = F̂(Y_t, X_t)` and `V̂_t = ψ(Û_t)`.
4. Let `Q̂` be the `(1−α)(1 + 1/|T₂|)` empirical quantile of `{V̂_t}_{t∈T₂}` — note the finite-sample
   inflation factor.
5. Report `Ĉ(X_{T+1}) = { y : ψ(F̂(y, X_{T+1})) ≤ Q̂ }`, which is an interval because `F̂(·,x)` is
   monotone. Equivalently, invert: the interval runs from the `(α/2)`-quantile to the
   `(1−α/2)`-quantile of `F̂(·, X_{T+1})`, with the level adjusted by `Q̂`.

**Full DCP (Algorithm 1)** augments the data with each trial value `y` on a grid, re-estimates `F̂`
on the augmented sample, and keeps the `y` whose permutation `p`-value exceeds `α`. It is what buys
*exact finite-sample* validity, because the augmentation is what makes the sample exchangeable
including the test point; the paper is explicit that without augmentation the intervals are not
exactly valid "not even with correct specification and iid data". The cost is one full refit per grid
point.

**Optimal DCP (Section 4), for skewed conditional distributions.** The baseline `ψ(u) = |u − 1/2|`
gives the *equal-tailed* interval, which is shortest only when the conditional density is symmetric
and unimodal. The shortest interval at coverage `1−α` is `[Q(b, x), Q(b + 1 − α, x)]` where

    b(x, α) ∈ argmin_{z ∈ [0, α]}  Q(z + 1 − α, x) − Q(z, x)

and Lemma 2 shows the score `ψ*(y,x) = |F(y,x) − b(x,α) − (1−α)/2|` attains it. So the whole
correction for asymmetry is a **single scalar shift of the target rank per prediction point**: find
the `α`-wide window of probability mass whose quantile span is narrowest, and centre the score on
it. Under symmetry `b = α/2` and optimal DCP reduces to the baseline.

**The guarantees, in the paper's own enumeration.** (i) Asymptotic *conditional* validity when `F̂`
is consistent for `F` (Theorem 3). (ii) *Unconditional* validity under arbitrary misspecification —
finite-sample and exact with iid or exchangeable data (Theorem 1, requiring only that the CDF
estimator be permutation-invariant, which quantile and distribution regression are), and asymptotic
with time-series data (Theorem 2). (iii) For optimal DCP, asymptotic conditional validity plus
shortest length under weak conditions. The consistency requirement in Assumption 1 is **weak and
rate-free**: an averaged `L^q` closeness of `F̂` to some non-random `F*`, with `q = 2` verifiable for
many estimators. Note the honest division of labour: conditional validity needs `F* = F`, i.e. a
correctly specified model; **misspecification costs you conditional validity but not unconditional
validity.**

## Robustness evidence (qualitative only)

**For it.** The core claims are theorems with explicitly stated, weak assumptions. The time-series
extension is proved under β-mixing, and the paper notes that standard stochastic-volatility and
GARCH-type models for asset returns are β-mixing in the existing literature — so the dependence
condition is satisfied by the data-generating processes this domain actually uses. (The β-mixing
details live in the SI Appendix, which was not read; the statement that the condition is what is
assumed comes from the main text.) The equity illustration spans nine decades of daily data and
the method is compared against seven alternatives, including conformalized quantile regression and a
location-scale conformal method.

**The empirical finding, stated at mechanism level because that is all this folder may record.**
Coverage is examined across twenty bins of the conditioning variable (lagged realised volatility,
computed as the square root of the sum of squared returns over the previous 22 days). The
**quantile-based conformal methods — DCP-QR, optimal DCP-QR, and the conformalized-quantile-regression
family — hold coverage essentially flat across all bins, close to nominal.** The **mean-based
conformal method (CP-OLS) over-covers in the low-dispersion bins and substantially under-covers in
the high-dispersion bins**, with interval lengths nearly constant across bins — exactly the failure
the analytical example predicts, now measured. The distribution-regression variant under-covers in
the high-dispersion bins. One further qualitative result worth keeping: because the quantile-based
methods and the location-scale method perform alike, the authors conclude that **a location-scale
model is a good approximation of the conditional distribution of these returns** — which is a direct,
independently-arrived-at statement about the restriction that
`notes/2026-10-20-composite-quantile-regression-efficiency-bound.md` requires.

**Against it, and why the tier is still A but the *finance* evidence inside it is thin.** The
equity application is a single aggregate index, a single conditioning variable, and one country; it
is an illustration of a statistical method, not a study of returns. Nothing cross-sectional is
tested. No costs, no portfolios, no trading. `validation_overlap: true` because the return sample
runs to mid-2021 — but the overlap is nearly irrelevant here, since nothing in the paper is a signal
and the method is distribution-free. Replication in the Hou–Xue–Zhang sense does not apply; the
relevant check is that the theorems are proved and the surrounding conformal-inference literature
(cited in the paper: Vovk, Lei, Romano, Candès, Barber) extends rather than contests them, with the
authors noting that a later paper generalises their Theorem 3 to `F* ≈ F`.

## Implementability here

**A naming collision to get out of the way first.** In *this* paper "CQR" means **conformalized
quantile regression** (Romano–Patterson–Candès), one of the benchmark methods. In
`notes/2026-10-20-composite-quantile-regression-efficiency-bound.md` "CQR" means **composite quantile
regression** (Zou–Yuan). Two different objects, same three letters, both in tonight's reading. Spell
it out wherever either appears.

**What this is not.** It is not a signal, not a family, and not a candidate. Nothing here predicts a
return or orders a cross-section, and a wider or narrower interval does not select a name. Any
proposal of the form "use conformal prediction to pick stocks" is a category error:
`notes/2026-10-19-consistent-scoring-functions-and-elicitability.md` says the decision consumes an
ordering, and an interval is not one. Resist it.

**What it is, and the one place it earns its keep.** The lab's measurement chain already reports
bootstrap intervals on skill, and `scripts/rank_trials.py` currently cannot separate any v3 trial
from the best — i.e. the lab's binding problem is interval *width* and interval *honesty*, not point
estimates. DCP's transferable content for that problem is one prohibition and one construction:

- **The prohibition, and it is free.** Any interval or band whose width is computed from the
  dispersion of a *mean* model's residuals, pooled across states, has a width that does not depend on
  the state and therefore mis-covers systematically as a function of cross-sectional dispersion — too
  wide when the panel is calm, too narrow when it is not. This is the analytical example above, and
  it is a property of the construction rather than of any sample. It applies directly to anything
  this lab builds that pools residuals to get an error bar on a conditional prediction, and it is a
  second, independent route to the same warning as
  `notes/2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md`'s "is the
  statistic an estimator, a signal or a scale" distinction — here the dispersion is being used as a
  *scale*, and a pooled scale is the wrong one.
- **The construction, which is cheap and uses what is installed.** Split DCP needs only a
  conditional-CDF estimate plus one empirical quantile of held-out ranks.
  `sklearn.linear_model.QuantileRegressor` (present, 1.9.1) at a handful of levels gives the CDF
  estimate; steps 3–5 are four lines of pandas. There is no optimiser, no `random_state`, no
  threading — so it is deterministic at the `1e-6` tolerance `causality_check` applies, and the
  `T₁`/`T₂` split is a *time* split, which is the shape the lab's walk-forward bookkeeping already
  enforces. The honest caveat: **a split costs half the fitting sample**, and the exact
  finite-sample guarantee belongs to full DCP, which needs a refit per grid point and is therefore
  out of budget at ~60 s per call.
- **If it is ever used on a diagnostic, use the optimal-DCP shift.** Return distributions are
  skewed, and the baseline score silently assumes symmetry; the correction is one scalar per
  prediction point and is specified in full above.

**Where this would be read rather than built.** The natural use is not inside a candidate at all but
inside a *report*: a conditionally-valid interval for a next-period return, or for a next-period
skill number, conditioned on the panel's current dispersion, is a more honest error bar than a pooled
bootstrap — and the paper's own equity exercise is precisely the "interval for a return given lagged
realised volatility" problem. That is a `reports/`-side improvement and is not a trial. **It also
touches the engine's own machinery, which this folder does not write to; nothing here licenses
changing a protocol threshold or a gate.**

## Related

- **Third member of tonight's chain.** Theory
  (`notes/2026-10-20-composite-quantile-regression-efficiency-bound.md`) → empirics
  (`notes/2026-10-20-forecasting-the-return-distribution-in-the-cross-section.md`) → **what a
  predicted distribution is worth when the model is wrong**. The third step is also the one that
  survives the other two's negative findings, because it never needed the distribution to be priced.
- **The cross-link worth noticing.** This paper's equity exercise concludes that a *location-scale*
  model approximates the conditional return distribution well. Zou–Yuan's composite quantile
  regression assumes a *location-shift* model (one slope, `K` intercepts) — one restriction tighter.
  Whether the "scale" half matters is therefore an empirical question with a partial answer in this
  paper, arrived at independently and on an aggregate series rather than a cross-section, and
  recorded here as a pointer rather than a finding: **a demonstrated need for the scale term is a
  demonstrated misspecification of the location-shift model.**
- Measurement-chain neighbours from sessions 58–62, which this note extends by one object (the
  interval): `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md`,
  `notes/2026-10-14-which-alpha-the-sufficient-statistic-for-beating-a-benchmark.md`,
  `notes/2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` (the closest prior note on
  honest out-of-sample machinery under dependence).
- The elicitability layer that says why an interval is not a selection rule:
  `notes/2026-10-19-consistent-scoring-functions-and-elicitability.md`.
