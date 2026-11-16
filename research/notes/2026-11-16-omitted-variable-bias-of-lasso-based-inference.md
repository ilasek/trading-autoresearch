---
title: "Omitted Variable Bias of Lasso-Based Inference Methods: A Finite Sample Analysis" — the asymptotic licence for a selected control set is not a finite-sample licence, the harmful regime has a computable boundary, and where p < n the honest answer is not to select at all
authors: Wüthrich, Zhu
year: 2023
venue: Review of Economics and Statistics 105(4), 982–997 (venue tier 1 — peer-reviewed)
url: https://doi.org/10.1162/rest_a_01128
citations: 29 (Crossref `is-referenced-by-count`, checked 2026-11-16)
sample_period: n/a — a methods paper. Theory plus simulations; the two re-analyses use a US household survey from the early 1990s and a US school-cohort study from the late 1990s
markets: none (methodology; no financial application)
tier: B
validation_overlap: false
published_post_2018: true
read: full text of `arxiv.org/pdf/1903.08704` (1.2 MB → 278 KB of clean text via `pdftotext -layout`, no ASCII shift; the deposit is labelled the final author version accepted at the journal). Title, authors, journal, volume, issue and pages verified against the Crossref record for the published DOI.
---

## Mechanism

This is tonight's adversarial source, and it is adversarial to the two notes written beside it
rather than to anything the lab believes. Post-double selection and debiased lasso both come with
a theorem saying the interval afterwards is valid. This paper asks what that theorem is worth at
a finite `n`, and the answer is: **less than it looks, and the gap is computable.**

The object is **double under-selection** — a relevant control missed by *both* lasso steps. The
union rule gives each confounder two chances; this paper prices the event that both chances fail.
Its contribution is a **non-asymptotic lower bound** on the resulting omitted-variable bias, with
explicit universal constants, built from an explicit lower bound on the probability of
under-selection at fixed `n`. (The authors distinguish their result from asymptotic
necessary-conditions work on lasso selection consistency, whose arguments do not straightforwardly
yield a constant-bearing finite-sample bound.)

The headline is a comparison of two quantities that the literature never puts side by side: the
**OVB lower bound** against `σ_α̃ = n^{−1/2}·(σ_η/σ_v)`, the standard deviation implied by the
*asymptotic* distribution. At a configuration drawn from a published application — `n = 14238`,
`p = 384`, all relevant coefficients equal at `0.07` — the ratio `OVB/σ_α̃` is **0.27 when `k = 1`
and 2.4 when `k = 10`**, where `k` is the number of relevant controls. Ten relevant controls is
not a pathological design, and `n` here is 37 times `p`. So:

- The bias can exceed **twice** the standard deviation the confidence interval is built from,
  which means under-coverage rather than a widened interval.
- This happens with **sparse** coefficient vectors and with **`n` much larger than `p`**, i.e.
  inside the conditions the asymptotic theory is stated under.
- The requirement on `k` for the bias to be negligible is, in the authors' word, "quite
  stringent" — and `k` is unknown.

The authors are careful about what this does and does not say, and so is this note: it does **not**
contradict the asymptotic result. It says the asymptotic zero-mean approximation to
`√n(α̃ − α*)` can be inaccurate at sample sizes people actually have. The connection they draw is
to Leeb and Pötscher: non-asymptotically, post-double selection "cannot avoid the post-selection
inference issues" that literature raised.

## Construction recipe

There is no new estimator here. What is constructible is a **boundary, a diagnostic, and a
fallback.**

**1. The three regimes, as a function of the relevant coefficients' magnitude.**

- **Regime (iii), no bias — the beta-min condition, and it is the computable object.** All relevant
  controls are selected with probability at least `1 − 1/p^τ` if, for each relevant `j`,
  **either**

      |β*_j| ≥ a·φ⁻¹·σ_η·√( 2(1+τ)·log p / n )    (outcome equation)
      |γ*_j| ≥ b·φ⁻¹·σ_v ·√( 2(1+τ)·log p / n )    (treatment equation)

  with `a, b > 3`, where `φ` is a restricted-eigenvalue-type constant and `τ > 0` sets the
  confidence level. Then `Î₁ ∪ Î₂ = K` with high probability and the OVB is exactly zero. **Note
  the "either":** one large coefficient on either side suffices — this is the union rule's
  two-chances property turned into an inequality, and it is the precise sense in which double
  selection beats single selection.
- **Regime (ii), negligible bias.** Coefficients so small that omitting the control costs almost
  nothing; the relevant controls are "essentially irrelevant". Normality centred at zero holds
  even when `(k·log p)/√n` is bounded away from zero.
- **Regime (i), the harmful one.** The coefficients are **too small to be reliably selected but
  large enough to bias** — and `(k·log p)/√n` is not small. This is the interval *between* the two
  safe regimes, and nothing about the data announces that you are in it. Roughly, the bound grows
  about linearly in `(k·log p)/n` in the relevant range.

**2. The diagnostic — a stress test, read in the counter-intuitive direction.** Re-run post-double
selection with **both** penalties increased, and a **50% increase over the theory-driven penalty
is the paper's simulation-calibrated rule of thumb.** Increasing `λ` *aggravates* under-selection,
so:

- if `α̃` barely moves → the design is in Regime (ii) or (iii), and the estimate is trustworthy
  **and** efficient;
- if `α̃` moves materially → Regime (i) cannot be ruled out, and the interval should not be
  believed.

The rationale is that the final step is just an OLS on the selected union, so varying what gets
selected varies the only thing that can be wrong. The authors liken it to a bandwidth robustness
check in a regression discontinuity design.

**3. What does NOT work, and it is the tempting move.** *Lowering* `λ` to force more controls in
"does not work in general and can lead to rather poor performance". Their comparison of
`0.5·λ_BCCH`, `λ_BCCH` and `1.5·λ_BCCH` shows `0.5·λ_BCCH` over-selects at every `n` and `R²`
tried; cross-validated `λ_min` selects the most controls and gives the smallest bias-to-SD ratio
in some designs while being poor in others. Their flat statement: **"there is no simple
recommendation for how to choose the regularization parameters"**, and "no single choice
outperforms the others across all designs". A method whose answer depends materially on a tuning
constant with no principled setting is a method to be stress-tested, not trusted.

**4. The fallback, for `p < n`.** Where `p` is comparable to but smaller than `n`, run **OLS with
every control included** and use a variance estimator built to be robust to many controls — the
authors find the Cattaneo–Jansson–Newey estimator gives "excellent coverage accuracy across all
our simulation designs". Two properties make this the honest default in that regime: it needs
**no sparsity assumption at all**, and there is no selection event to invalidate anything. The
price is wider intervals — an explicit trade between coverage accuracy and interval length.

**5. The amelioration set, endorsed from the other side.** They repeat the predecessor's advice as
their own second recommendation: **always** augment the selected union with controls motivated by
theory and prior knowledge. Here it is a bias-mitigation device, not a convenience.

## Robustness evidence (qualitative only)

- **Three independent legs.** A theorem (the non-asymptotic lower bound, with constants), extensive
  simulations across designs, `n`, `p` and `R²`, and two re-analyses of published applications in
  which subsamples of varying size are drawn from a large original dataset and compared against
  the full-data estimate. In both re-analyses the biases are substantial "even when `n` is
  considerably larger than `p`", and their magnitude varies substantially with the regularisation
  choice. The three legs agree, which is what makes the finding hard to dismiss as a simulation
  artefact.
- **Why tier B rather than A.** Top venue, a theorem rather than a calibration, and an honest
  statement of what it does not claim — but the citation count is modest, and the paper's own
  result has not been independently replicated. Its *mechanism* (lasso under-selection when
  coefficients sit near the selection threshold) is corroborated by the independent
  selection-consistency literature it builds on; its **constants and the 50% rule of thumb are
  properties of its own designs**. Carry the mechanism and the beta-min inequality; treat the
  50% figure as a starting point for a stress test rather than a law, and treat `OVB/σ_α̃ = 2.4`
  as a demonstration that the ratio *can* exceed one, not as a number for any other design.
- **The scope is wider than post-double lasso.** The analysis covers debiased lasso as well, so it
  bears on the whole family in tonight's other two notes, including the lasso-based members of
  the DML family.

## Implementability here

**This is the note that settles what the lab should actually do, and the answer is deflationary in
a useful direction.**

1. **The lab is in the `p < n` regime, so the recommendation is: do not select controls at all —
   include them all.** The lab's candidate control list is of the order of ten variables (log `P`,
   `vol126`, `vol756`, `mom12-1`, Amihud illiquidity, region, type, liquidity tier) against ~251
   train month-ends; `p/n` is small. In that regime this paper's own guidance is OLS on the full
   control set with a many-controls-robust variance estimator, because it assumes no sparsity and
   creates no selection event. **This is the cheapest possible resolution of `#447`'s third veto**
   ("a data-chosen control set costs the validity of the interval that follows it"): if nothing is
   chosen, nothing is invalidated. It is also strictly simpler than what the lab does now, which
   is to admit controls one at a time on judgement.
2. **It converts tonight's primary rule from "adopt the procedure" to "adopt the rule about
   sides".** Post-double selection's transferable content for this lab is that a control's claim to
   inclusion can come from **either** side — its association with the score or its association with
   the forward return — and the beta-min inequality above is the quantitative version: a
   confounder is safe if it is strongly related to *one* of the two. The lab currently judges on
   the score side only (`#448`). Under the "include them all" recommendation the question of which
   side to judge on mostly dissolves, which is the cleanest possible resolution of `#451`'s
   tension.
3. **The stress test transfers even without any lasso, and the lab should run it in the form it
   can.** The lab's instrument is a joint rank-space residualisation on a hand-picked set. The
   analogue of "increase `λ` and see if the reading moves" is **vary the control set and report the
   spread** — read the association under the full set, under each control dropped, and under the
   set augmented by the next-most-plausible candidate, and report the range rather than one
   number. The 2026-11-10/11 entry is exactly this measurement taken once (raw `+0.0193`, `−24%`
   under log `P` alone, `−34%` under volatility alone, `−83%` under both) and it is the reason the
   lab declined a trial. **Make it standing practice and report the range, not the point.** Free;
   no trial, no holdout.
4. **It sharpens `#450` rather than contradicting it.** `#450` refuses "add another control and see
   if the reading survives" as a robustness move, because a control that *raises* a reading is
   unresolved rather than corroborating. That refusal is about **interpreting the direction** of a
   change. This paper licenses the **variation itself as a sensitivity diagnostic** whose output is
   a width, not a verdict: if the reading is stable across the control set, the selection is not
   the thing you have to worry about; if it is unstable, you cannot read an interval at all. The
   two are compatible exactly because this one refuses to attach a sign to the movement. Stated
   explicitly so a later session does not read a contradiction: **vary the set and report the
   spread; never read a direction off the variation.**
5. **A number the lab can compute and has never computed.** The beta-min threshold
   `aφ⁻¹σ√(2(1+τ)log p/n)` is, in the lab's units, the association magnitude a control must have
   to be reliably caught by any selection procedure at the lab's `n` and `p`. With
   `n ≈ 251` month-ends, `p ≈ 10`, `τ = 0.5`, `a = 3`, `√(2·1.5·log 10/251) ≈ 0.13` before the
   `φ⁻¹σ` scaling — i.e. of the order of several tenths of a standardised unit. **Controls weaker
   than that are in Regime (i) territory for any selection rule**, which is a further argument for
   item 1: at this `n` the lab cannot reliably *select* controls even if it wanted to, so it
   should include them.
6. **The i.i.d. assumption is unrelieved here too.** `#445`'s caution applies: the paper's `n` is a
   count of independent observations, and the lab's panel rows are not independent within a date.
   Counting `n` as name-months would make the beta-min threshold look about thirty times smaller
   than it is. **Count dates.**

**Pitfalls.** Reading `OVB/σ_α̃ = 2.4` as a calibration for anything other than its own design.
Lowering a penalty to "include more" (explicitly refuted). Treating the 50% increase as the only
stress test, rather than as one point on a sensitivity curve. And concluding from this note that
double selection is unsound — the correct conclusion is that it is an asymptotic result whose
finite-sample behaviour needs checking, and that at this lab's `p/n` there is a simpler procedure
with no sparsity assumption at all.

## Related

- `notes/2026-11-16-post-double-selection-inference-after-control-selection.md` — the method this
  bounds; its amelioration set is endorsed here as bias mitigation.
- `notes/2026-11-16-double-debiased-ml-neyman-orthogonality-cross-fitting.md` — the family this
  also covers through the debiased-lasso member.
- `notes/2026-11-15-the-modified-disjunctive-cause-criterion.md` (`#447`) — the third veto, which
  the `p < n` fallback resolves by removing the selection event.
- `notes/2026-11-15-covariate-selection-for-the-propensity-score.md` (`#448`) — the per-covariate
  variance price, which is the cost side of "include them all".
- `notes/2026-10-21-illusion-of-sparsity-selection-versus-shrinkage.md` — the dense-design
  tension; this paper's fallback is the one recommendation in the vein that does not need sparsity
  to hold.
- `notes/2026-09-15-inference-on-winners-post-selection-estimation.md` — the other selection event
  the lab faces, and the Leeb–Pötscher impossibility results this paper connects to.
