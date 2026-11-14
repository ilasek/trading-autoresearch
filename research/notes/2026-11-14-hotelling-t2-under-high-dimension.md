---
title: "Effect of High Dimension: By an Example of a Two Sample Problem"
authors: Bai, Saranadasa
year: 1996
venue: Statistica Sinica 6(2), 311–329 (peer-reviewed; a respected theoretical-statistics journal, outside this rubric's finance tier-1 list)
url: https://www3.stat.sinica.edu.tw/statistica/oldpdf/A6n21.pdf
citations: not resolved (Crossref journal-year enumeration for Statistica Sinica 1996 under ISSN 1017-0405 returns **zero deposits** — the journal registered no DOIs that far back; OpenAlex returned HTTP 429 `Insufficient budget` and Semantic Scholar's title endpoint HTTP 429 on two attempts, which are **rate limits, not clean negatives**; checked 2026-11-14). Per `research/README.md` the tier is not downgraded on this basis. Indirect evidence of standing: it is the named reference point of every later paper in this vein, and Chen & Qin (2010) call it "an important work".
sample_period: none — analytic asymptotics (random-matrix theory) plus Monte Carlo
markets: n/a (statistical methodology; no financial data of any kind)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the paper `#440` leaned on without having read, and it is the one that makes the refusal
quantitative rather than rhetorical. [2026-11-13] told the lab **not** to use a classifier AUC to
test a named difference, on the ground that a location test is minimax optimal when `d/n → 0`, and
then left the lab with no construction and — more importantly — **no way to know when its own cell
stops being that cell**. This paper supplies both halves: the exact mechanism by which Hotelling's
`T²` degrades as the dimension grows toward the sample size, and the arithmetic for *how far along
that curve a given `(d, n)` sits*.

The setting is the plain one. Two independent samples `x_{ij} ~ N_p(μ_i, Σ)`, `j = 1…N_i`, `i = 1, 2`;
test `H₀: μ₁ = μ₂`. Hotelling's statistic is

    T² = τ⁻¹ (x̄₁ − x̄₂)' A⁻¹ (x̄₁ − x̄₂),   A = Σᵢ Σⱼ (x_{ij} − x̄ᵢ)(x_{ij} − x̄ᵢ)',   τ = (N₁+N₂)/(N₁N₂),

with `n = N₁ + N₂ − 2` the within-sample degrees of freedom, and under `H₀` the exact result
`((n − p + 1)/(np)) T² ~ F(p, n − p + 1)`. Its three classical virtues are affine invariance, an
exact null distribution, and good power **when `p` is small relative to `n`**. Its one structural
defect is stated in one line: `T²` is **undefined when `p` exceeds `n`**, because `A` is singular.

The paper's contribution is to show that the defect is not a cliff at `p = n` but a **slope that
starts immediately**, and to name the quantity that governs it. Write `y = lim p/n`. Then

- **Hotelling's asymptotic power** (Theorem 2.1, under `y ∈ (0,1)`, `N₁/(N₁+N₂) → κ ∈ (0,1)`,
  `‖δ‖² = o(1)`):

        β_H(μ) − Φ( −ξ_α + √( n(1−y) / (2y) ) · κ(1−κ) · ‖δ‖² ) → 0,     δ = Σ^(−1/2)(μ₁ − μ₂).

The non-centrality carries the factor `√(1−y)`, which **vanishes as `y → 1`**. That single factor is
the "effect of high dimension" of the title: with the mean separation held fixed in Mahalanobis
terms, Hotelling's power is multiplied by `√((1−y)/2y)` relative to what a `y → 0` analysis would
predict.

The *cause* is spelled out and is the part worth carrying. It is not that the mean estimate degrades
— `x̄₁ − x̄₂` is fine. It is that **`A⁻¹` is a bad estimate of `Σ⁻¹` in a specific, quantifiable
way.** When `p/n → y`, the empirical spectrum of the sample covariance spreads over the
Marčenko–Pastur support `[(1−√y)², (1+√y)²]` rather than concentrating at the population
eigenvalues, so the ratio of largest to smallest sample eigenvalue tends to

        (1 + √y)² / (1 − √y)².

The authors make the consequence concrete with three values of that ratio, and these are the most
useful numbers in the paper because they are pure functions of `y`:

| `y = p/n` | limiting condition number of the sample covariance |
|---|---|
| 0.01 | **1.494** |
| 0.1 | **3.705** |
| 0.93 | **≈ 3039** |

Their own emphasis: *"it is not necessary to require the dimension of data to be very close to the
degrees of freedom to make the effect of high dimension visible"* — and their simulations show it
at `p = 4`. Inverting a sample covariance always costs something; the table says how much.

The second contribution is the replacement statistic, which founds the whole later literature. Drop
the inverse:

        M_n = (x̄₁ − x̄₂)'(x̄₁ − x̄₂) − τ · tr(S_n),     S_n = A/n,

whose expectation under `H₀` is zero (the `tr S_n` subtraction removes the bias in the squared
norm). Standardized by a ratio-consistent estimator of `tr Σ²` it is asymptotically standard normal,
and its power (Theorem 4.1) is

        β_BS(μ) − Φ( −ξ_α + n κ(1−κ) ‖μ‖² / √(2 tr Σ²) ) → 0,     μ = μ₁ − μ₂,

identical to Dempster's non-exact test and **free of the `√(1−y)` factor**. Hence the headline: when
`y` is close to one, the non-inverting tests dominate Hotelling.

**The trade that the headline hides, and which decides the lab's case.** Hotelling's non-centrality
is in `‖δ‖² = ‖Σ^(−1/2)μ‖²`, the *Mahalanobis* norm; the replacement's is in `‖μ‖²/√(tr Σ²)`, the
*Euclidean* norm of the raw mean difference. These are different functionals of the same alternative.
The authors say exactly when the swap is safe: the non-exact tests win *"when the underlying
covariance structure is reasonably regular, i.e., the structure of `Σ` does not cause too large a
difference between `μ'Σ⁻¹μ` and `√n‖μ‖²/√tr(Σ²)`."* **Giving up the inverse means giving up affine
invariance.** A mean difference that lies along a low-variance direction is loud in Mahalanobis
terms and quiet in Euclidean terms, and against such an alternative Hotelling is the better test at
any `y` for which it is defined.

## Construction recipe

**Hotelling's `T²`, as the baseline (`p < n`).**
1. Pool: `A = Σ_{i=1,2} Σ_{j=1}^{N_i} (x_{ij} − x̄_i)(x_{ij} − x̄_i)'`, `n = N₁+N₂−2`, `S_n = A/n`.
2. `T² = (N₁N₂/(N₁+N₂)) (x̄₁ − x̄₂)' S_n⁻¹ (x̄₁ − x̄₂)`.
3. Refer `((n − p + 1)/(np)) · T²` to `F(p, n − p + 1)`. This is **exact** under normality, not
   asymptotic — no large-`n` appeal is needed for the level.
4. Read the degradation off `y = p/n` via the condition-number table above before trusting the power.

**The Bai–Saranadasa statistic (valid for `p` comparable to or exceeding `n`).**
1. `M_n = (x̄₁ − x̄₂)'(x̄₁ − x̄₂) − τ tr(S_n)`, with `τ = (N₁+N₂)/(N₁N₂)`.
2. Estimate `tr Σ²` by the **bias-corrected** estimator — the naive `tr S_n²` is neither unbiased
   nor ratio-consistent once `p` is not fixed:

        B_n² = n²/((n+2)(n−1)) · ( tr S_n² − (1/n)(tr S_n)² ).

   The bracket is non-negative by Cauchy–Schwarz.
3. `Z = M_n / √( 2(n+1)/n · τ² B_n² ) → N(0,1)` under `H₀`; reject at level `α` if `Z > ξ_α`
   (one-sided — the statistic is a squared norm, so all departures push it up).
4. **Standardize the coordinates first.** The statistic is a raw Euclidean norm and is therefore
   *not* scale-invariant: a covariate measured in different units changes the answer. With
   heterogeneous covariates, convert each to a common scale (z-score or rank) before step 1, and say
   that you did.

**Conditions required (and worth checking, not assuming).**
- (a) A factor representation `x_{ij} = Γ z_{ij} + μ_j` with `ΓΓ' = Σ` and i.i.d. `z` of unit
  variance, fourth moment `3 + Δ < ∞` and a pseudo-independence condition on mixed moments up to
  order 4. **Normality is not required** for the `Z` statistic — this is its advantage over
  Dempster's test, which needs it.
- (b) `p/n → y > 0` and `N₁/(N₁+N₂) → κ ∈ (0,1)`.
- (c) **`μ'Σμ = o(τ · tr Σ²)`** (3.7) — a local-alternative condition, automatic under `H₀`; and
  **`λ_max = o(√(tr Σ²))`** (3.8) — *no single eigenvalue may dominate the spectrum*.

Condition (3.8) deserves naming because it is the one a financial cross-section is most likely to
break. Since `tr Σ² = Σᵢ λᵢ²`, the condition says `λ_max / √(Σᵢ λᵢ²) → 0`: the top eigenvalue must be
asymptotically negligible against the whole spectrum. A panel dominated by one common factor is
precisely the configuration in which it fails.

## Robustness evidence (qualitative only)

Evidence is **analytic plus Monte Carlo**; there is no empirical application and no replication
record in the sense this rubric usually means. What carries the tier is that the asymptotic machinery
is the mature random-matrix theory of the sample covariance (Marčenko–Pastur, Yin–Bai–Krishnaiah,
Silverstein, Wachter — all cited and all independent of this paper), and that the paper's central
claims have since been re-derived and extended rather than contradicted: Chen & Qin (2010) rebuild
the statistic on the same model and reproduce the power formula as a special case, and Cai, Liu &
Xia (2014) take the `T²`-degradation result as settled background. The `(1+√y)²/(1−√y)²` spread is a
theorem about Wishart spectra, not a finding about a dataset.

Simulations cover normal and non-normal (moving-average gamma) innovations, identity, banded and
equicorrelated covariances, at `p = 40` against `N₁ = 25, N₂ = 20`, and also at `p = 4`. All three
tests held their nominal size; the two non-exact tests tracked each other closely and the new one was
consistently a shade above Dempster's; Hotelling's power rose slowly with the non-centrality in the
high-dimension cells. **The honest limit of the evidence**: the mean shifts were parameterized by
`η = ‖μ₁−μ₂‖²/√(tr Σ²)` — i.e. by the *Euclidean* functional the new test is built around — so the
design does not probe the adversarial case where the shift hides in a small-eigenvalue direction, and
nothing here contradicts Hotelling's superiority there.

## Implementability here

**This is a measurement instrument, not a strategy.** It proposes no book and costs no trial. Its
place in the lab is the one `#440` left vacant: the test to run when asking whether a candidate's
selected names differ from the names it passed over, on named covariates.

**The decisive calculation, and it goes against importing the high-dimensional machinery.** The lab's
balance question has `d ≈ 3–6` covariates (trailing volatility, log dollar volume or liquidity tier,
region, log price level per `#420`–`#426`) against `n ≈ 1,000` eligible names on a validation date.
So `y = d/n ≈ 0.003–0.006`. Put that into the table above and the limiting condition number of the
sample covariance is **below 1.3** — less inflation than the `y = 0.01` row, which is already
benign. The `√(1−y)` power factor is `0.998`. **On the lab's actual cell, Hotelling's `T²` loses
essentially nothing, and the Bai–Saranadasa statistic buys nothing while giving up affine
invariance.** This is the quantitative confirmation of `#440`'s claim, now with the threshold
attached: the high-dimensional replacements become the right instrument only if the covariate count
rises into the hundreds against the same thousand names, and the lab is two orders of magnitude from
that.

So the operational reading is **use `T²`, with the exact `F` reference**, which has the further
advantage over every asymptotic alternative that its level is exact at finite `n` under normality
rather than approached as `p → ∞`.

**Three pitfalls, in descending order of how likely they are to bite.**

1. **The observations are not independent, and no version of this theory tolerates that.** Every
   result above assumes `N₁ + N₂` i.i.d. draws. The lab's "observations" are *names in a single
   cross-section*, which are correlated — strongly, within region and within the common factor. The
   effective sample size is far below the name count, so the `F` reference (and every asymptotic
   normal reference in this vein) will be **anti-conservative**: it will reject too often. The fix
   that costs nothing and needs no theory is `#439`'s: **calibrate by permuting the selection labels
   within the date's cross-section**, which preserves the cross-sectional dependence exactly and
   makes the reference distribution correct by construction. Use `T²` as the *statistic* and the
   permutation as the *null*. Do not report an `F` p-value from a cross-section of correlated names.
2. **Do not confuse the two dimensions.** Here `p` is the **covariate count** and `n` the **name
   count**; `Σ` is the `d × d` covariance *of the covariates*, inverted at covariate width. `#438`
   already recorded the name-width inversion as the error to avoid, and this paper's whole subject is
   what goes wrong when you invert something too wide relative to your sample.
3. **Condition (3.8) is the one to state rather than verify.** Should the lab ever move to a
   wide-covariate regime where the replacement statistics matter, a cross-section with a dominant
   common factor can violate `λ_max = o(√tr Σ²)` outright, which voids the asymptotic normality that
   is the replacement's entire claim. Record it as a precondition before computing, not as a
   footnote after.

**What this does not do.** It is a test of a *joint* mean difference: a rejection says the selected
set differs somewhere in the covariate vector, and names no coordinate. Attribution needs the
per-coordinate statistics afterwards, under `#328`–`#342`'s multiplicity accounting. And a
non-rejection is `#441`'s reading — *not detectably different at this `n`* — never balance.

## Related

- `notes/2026-11-13-accuracy-tests-are-underpowered-for-signal-detection.md` and
  `notes/2026-11-13-classification-accuracy-as-a-two-sample-test.md` — the source of the refusal
  (`#440`) this note supplies the construction for; the former names `Hotelling.shrink`, Goeman's
  test and Srivastava's `sd` as the regularized location tests that beat classifier accuracy.
- `notes/2026-11-14-two-sample-location-test-without-a-dimension-condition.md` — Chen & Qin's
  rebuild of this statistic, which removes the `p/n → c` restriction and the equal-covariance
  assumption.
- `notes/2026-11-14-sparse-alternatives-and-the-precision-transformed-test.md` — the adversarial
  companion: against a *sparse* alternative, the whole sum-of-squares family here is the wrong
  choice.
- `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — the lab's existing null, which
  reasons in return space; this is the prior question in selection space.
- `notes/2026-09-27-nonlinear-shrinkage-instead-of-counting.md` and
  `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — the folder's existing
  covariance-estimation notes; the Marčenko–Pastur spread quantified here is the same phenomenon
  those shrinkage methods exist to repair.
