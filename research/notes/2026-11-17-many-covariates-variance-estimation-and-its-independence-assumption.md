---
title: "Inference in Linear Regression Models with Many Covariates and Heteroscedasticity"
authors: Cattaneo, Jansson, Newey
year: 2018
venue: Journal of the American Statistical Association 113(523), 1350–1361 (venue tier 1 — top-tier statistics journal; the content used here is an impossibility result plus a closed-form variance estimator, so the replication and multi-market axes of this folder's rubric do not apply as they would to an empirical effect)
url: https://doi.org/10.1080/01621459.2017.1328360 — read in full from arXiv 1507.02493v2 (35 pages, 89 KB of text, 369 instances of `" the "`, `( )`-dropout check zero, no ASCII shift)
citations: 94 (Crossref `is-referenced-by-count`, checked 2026-11-17)
sample_period: none — a theory paper. Its single empirical illustration is a 1991 cross-section of US wages (white males aged 28–34), i.e. labour economics, with no financial data anywhere in the paper
markets: none
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source `#454` leans on, read for the one thing `#454` did not state: **what it
assumes about the rows.** The answer settles the blocker, and it settles it in the negative.

The paper's object is a linear regression `y = x'β + w'γ + u` in which the nuisance covariate
block `w` is **many** — `K` covariates with `K/n` not going to zero. Two results:

**The negative result.** Every standard Eicker–White heteroskedasticity-robust variance
estimator is **inconsistent** in this regime. The reason is structural rather than a small-sample
artifact. Writing `M` for the residual-maker (annihilator) matrix, the Eicker–White estimator
converges not to the target but to a *smeared* version of it,

> `Σ̂^EW = (1/n) Σᵢ Σⱼ M²ᵢⱼ v̂ᵢ v̂ᵢ' E[u²ⱼ | xⱼ, wⱼ] + oₚ(1)`,

against a target that needs `E[u²ᵢ]` paired with observation `i` alone. The off-diagonal
`M²ᵢⱼ` mass is what `K/n → 0` normally kills, and with many covariates it does not vanish. The
economic content: with many covariates each residual `ûᵢ` is a blend of many observations'
errors, so a per-observation variance cannot be recovered observation by observation — the curse
of dimensionality hits the *variance*, not the coefficient.

**The positive results.** Of the standard family, the paper grades each one:

| estimator | verdict under `K/n ↛ 0` |
|---|---|
| homoskedasticity-only (`HO`) | consistent **under homoskedasticity**, and that holds quite generally even with many covariates |
| `HC0` (= Eicker–White) | inconsistent; inference asymptotically invalid |
| `HC1` | inconsistent in general |
| `HC2` | inconsistent under heteroskedasticity |
| `HC3` | **asymptotically conservative** — the bias term is a sum of positive-semidefinite pieces, so it over-states the variance rather than under-stating it |
| `HC4` | reduces to `HC3` when leverages are equal, and is inconsistent in general |
| `HCK` (this paper) | consistent |

`HC3`'s status is the free lunch: *valid but wide*, obtainable "using standard linear methods
(and software)" with no new code. `HCK` is the consistent replacement.

## Construction recipe

**`HCK`.** Take the general class `Σ̂(κ) = (1/n) Σᵢ Σⱼ κᵢⱼ v̂ᵢ v̂ᵢ' û²ⱼ`. Consistency requires
`Σₖ κᵢₖ M²ₖⱼ = 1(i = j)`, i.e. `κ` must invert the **Hadamard square** of the annihilator
matrix. So:

1. Run the long regression; form `M = I − Z(Z'Z)⁻¹Z'` over the full design `Z = [x, w]`, and
   the residuals `û`.
2. Form `M ⊙ M` (elementwise square of `M`) and invert it: `κ^HC = (M ⊙ M)⁻¹`.
3. `Σ̂^HC = (1/n) Σᵢ Σⱼ κ^HC_{ij} v̂ᵢ v̂ᵢ' û²ⱼ`, where `v̂` is the residualised regressor of
   interest.

Every `HCk` in the table above is the special case where `κ` is **diagonal**, with
`κᵢᵢ = Υᵢ Mᵢᵢ^{−ξᵢ}`: `(Υ, ξ) = (1,0)` is `HC0`, `(n/(n−K), 0)` is `HC1`, `(1,1)` is `HC2`,
`(1,2)` is `HC3`, `(1, min(4, nMᵢᵢ/K))` is `HC4`. The paper's theorem is that **no diagonal
choice works** when `K/n ↛ 0`; the fix is necessarily non-diagonal.

**Existence condition.** `Σ̂^HC` is defined whenever `M ⊙ M` is invertible, and a sufficient
condition (via the Gershgorin circle theorem) is

> `𝓜 = 1 − min_i Mᵢᵢ < 1/2`,

i.e. **no observation has leverage at or above 1/2**. This is cheap to check and is the thing to
check *before* reporting anything. A slight strengthening of the same condition is what the
consistency theorem needs.

## Robustness evidence (qualitative only)

The paper reports a simulation study across designs and an empirical illustration (a wage
regression with county and cohort-by-county fixed effects, `K/n ≈ 0.28`, `𝓜 ≈ 0.42`). The
qualitative pattern: `HC3` intervals are "always quite conservative", and `HCK` intervals have
"close-to-correct empirical coverage". The illustration is the honest kind — the sign of the
conclusion *changes* with the estimator, with `HC0` giving a significant result and `HC3`/`HCK`
not, so the choice is not cosmetic. The framework is shown to cover three distinct cases:
parametric models with many covariates, panel models with many fixed effects, and
semiparametric models with many technical regressors (series/sieve terms).

Replication status in the folder's usual sense does not apply — these are theorems with proofs
in a supplemental appendix, not a measured effect.

## Implementability here

**This is the session's headline and it is a refusal.** `#454` instructs the lab, in the `p < n`
regime, to "run OLS with every control included and use the Cattaneo–Jansson–Newey variance
estimator". Read for its sampling assumption, that instruction **cannot be followed on this
lab's rows as written.** Assumption 1 (Sampling) requires

> `C[Uᵢ, Uⱼ | X, W] = 0` for `i ≠ j`, with `max_i #Tᵢ = O(1)`, the `Tᵢ` partitioning the sample
> into groups independent of one another,

and the authors say what that excludes in as many words: the assumption "generalizes classical
i.i.d. sampling by allowing for groups or 'clusters' of finite but possibly heterogeneous size
with arbitrary intra-group dependence… **As currently stated, this assumption does not allow for
dependence in the error terms across units, and therefore excludes clustered, spacial or time
series dependence in the sample.**" They conjecture the results extend and relegate it to future
work.

Two clauses bite, and the second is the fatal one:

- **Arbitrary within-group dependence is allowed** — so a cross-section of correlated names at a
  date is not automatically outside the theory, if a date is a group.
- **But group size must be `O(1)`** — bounded as `n` grows — and groups must be independent of
  each other. A date on this panel is a group of **~1,000 names**, and the whole point is that
  `n` grows by adding names to dates. Date-groups are also not independent of one another
  (returns are serially linked through slow-moving characteristics). So the partition the theorem
  needs does not exist here in either direction.

**What the lab can use today instead.** `HC3`. It is asymptotically conservative under many
covariates, it needs no new code, and it is the honest default for the one thing `#454` was
right about: at `K/n` of any size, the *default* robust standard error is not merely imprecise
but **inconsistent**, so a many-controls regression reported with `HC0`/`HC1` is wrong in a
direction that over-states significance. Report `HC3`, say it is conservative, and do not quote
`HCK` as if the lab had earned it. The leverage check `max_i(1 − Mᵢᵢ) < 1/2` is worth computing
anyway — it is one line and it flags a design in which a handful of names or dates carry the fit.

**Scale check.** At the widths the lab actually uses, none of this is computationally binding:
`#447`/`#452` put the control set at `d ≈ 3–6` against `n ≈ 1,000`, so `K/n ≈ 0.005` and the
many-covariate regime is not even entered — `HC0` would be fine *on the covariate count* and is
still wrong **on the dependence**, which is `#458`'s whole point. The many-covariate machinery
becomes relevant only if the lab ever runs the `#454` regression with hundreds of controls, and
by then the dependence problem has not gone away.

**Pitfall.** Do not read `HC3`'s conservativeness as a licence to ignore dependence. `HC3` is
conservative *with respect to the many-covariates problem only*, inside the same Assumption 1.
Against cross-sectional dependence it is as anti-conservative as `HC0` — the two failures are
independent and only one of them is fixed here.

## Related

- `research/notes/2026-11-16-omitted-variable-bias-of-lasso-based-inference.md` — the source of
  `#454`, which names this estimator as the `p < n` fallback and does not state its sampling
  assumption. That gap is what this note closes.
- `research/notes/2026-11-16-post-double-selection-inference-after-control-selection.md` —
  `#452`'s union rule, which also recommends these standard errors when `ŝ` is a non-trivial
  fraction of `n`; the same caveat applies to that recommendation.
- `research/notes/2026-11-17-which-dependence-structure-licenses-which-standard-error.md` — the
  estimator family that *does* admit cross-sectional dependence, and the price it charges.
- `research/notes/2026-11-17-clustering-as-a-design-question-not-a-correlation-question.md` — the
  argument that the lab must first say which question it is asking.
- `research/notes/2026-11-14-hotelling-t2-under-high-dimension.md` and
  `research/notes/2026-11-14-two-sample-location-test-without-a-dimension-condition.md` — `#445`,
  the same i.i.d. problem on the two-sample side, and the folder's permutation repair for it.
