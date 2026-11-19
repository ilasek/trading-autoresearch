---
title: "Detecting p-Hacking"
authors: Elliott, Kudrin, Wüthrich
year: 2022
venue: "Econometrica 90(2), 887–906 (Tier 1). Read in full from the arXiv version (arXiv:1906.06711v5, 25 May 2021)."
url: "https://doi.org/10.3982/ECTA18583 (read from https://arxiv.org/pdf/1906.06711)"
citations: "66 (Crossref, checked 2026-11-19)"
sample_period: "No market estimation window. The paper is theory plus two reanalyses of LITERATURE CORPORA: 49,838 t-tests from 640 papers in the AER/QJE/JPE (Brodeur et al. 2016 collection, articles published 2005–2011), and text-mined p-values from open-access PubMed papers across 21 disciplines (Head et al. 2015/2016 collection)."
markets: "None. The object is a set of test statistics, not an asset panel."
tier: "A — Tier-1 venue, theorems with proofs, two independent corpora, dependence explicitly handled, and the authors state plainly where their own restrictions fail (non-similar tests, rounding, joint-test confounding with publication bias)."
validation_overlap: false
published_post_2018: true
---

## Access

`arxiv.org/pdf/1906.06711` served the complete paper first try (HTTP 200, 664 KB, `pdftotext -layout`
into 76 KB of clean text, 357 `" the "`, zero `( )` dropouts, right title on line 1). **Fourth
consecutive session in which arXiv has been the working channel.** Note that `file -b` reported
"2 page(s)" for a ~20-page article — another instance of the 2026-10-07 lesson that the page count is
not a completeness check.

## Mechanism

This is the source the folder's standing aim asked for: **a formal treatment of what the
distribution of a set of `p`-values looks like when nobody has gamed it**, so that a deviation from
that shape is evidence about the search rather than about the world.

The setup is exactly the lab's own situation written in general notation. A test statistic `T` has
distribution `F_h`, where `h` indexes the true effect; researchers test `H0: h ∈ H0` against
`H1: h ∈ H1`; the critical value for a level-`p` test is `cv(p) = F^{-1}(1-p)`; and the **power
function** is `β(p,h) = Pr(T > cv(p) | h)`. Across many studies the true effects are themselves
drawn from a distribution `Π` (the "distribution of true effects"), so the CDF of the observed
`p`-values is `G(p) = ∫ β(p,h) dΠ(h)` and the **`p`-curve** is its density
`g(p) = ∫ ∂β(p,h)/∂p dΠ(h)`.

The whole contribution is that **`Π` is never known**, so a usable null has to hold *for every* `Π`.
The authors say in as many words why the prior literature's numerical examples are not enough:
"such analyses are not sufficient for guaranteeing size control of statistical tests for p-hacking
since the true effect distribution is never known." What is needed, and what they supply, is a
characterisation of the shape of `g` for general tests **and all effect distributions**.

The economic reading for this lab: a set of one's own test statistics has a *shape* that is pinned
down by the geometry of the power function alone, independently of how much true skill is out there.
That is why the shape can be used as a diagnostic of the selection process. It is also why the
diagnostic is fragile — the pinning-down depends on properties of the test, and the lab's test does
not have all of them (`#480`).

## Construction recipe

**The null set, in three nested layers of strength.**

1. **General tests → non-increasing and continuously differentiable (Theorem 1).** Under
   Assumption 1 (regularity: `F`, `F_h` twice continuously differentiable with bounded derivatives,
   `f > 0` on the critical-value range, common support) and Assumption 2 (the sufficient condition
   `f'_h(x) f(x) ≥ f'(x) f_h(x)` for all `x ∈ {cv(p)}` and all `h ∈ H`), the `p`-curve satisfies
   `g'(p) ≤ 0` on `(0,1)` for **any** `Π`. Assumption 2 is a monotone-likelihood-ratio-type
   restriction on how power moves with the critical value. Lemma 1 verifies it for (i) the similar
   one-sided t-test (`F = Φ`, `F_h = Φ(·-h)`, `H0 = {0}`, `H1 ⊆ (0,∞)`), (ii) the two-sided t-test
   (half-normal null, folded-normal alternative, `H0 = {0}`), and (iii) the Wald/chi-square test
   (central vs non-central `χ²_d`, `H0 = {0}`). The paper states this is the first *general* formal
   justification for the existing non-increasingness tests, which had rested on examples.

2. **t-tests → completely monotone (Theorem 2).** For the one-sided case the `p`-curve has the
   closed form `g1(p) = ∫_{[0,∞)} exp(h·cv1(p) - h²/2) dΠ(h)` with `cv1(p) = Φ^{-1}(1-p)`; for the
   two-sided case `g2(p) = ∫_R ½[exp(h·cv2(p) - h²/2) + exp(-h·cv2(p) - h²/2)] dΠ(h)` with
   `cv2(p) = Φ^{-1}(1-p/2)`. A function `ξ` is completely monotone on `I` if
   `0 ≤ (-1)^k ξ^{(k)}(x)` for all `x ∈ I` and all `k = 0,1,2,…`. **`g1` is completely monotone on
   `(0,½]` and `g2` on `(0,1)`.** This is strictly more than non-increasingness: every derivative
   alternates in sign. The authors note complete monotonicity can **fail** for `χ²` tests with more
   than two degrees of freedom, so it is a t-test-specific restriction, not a general one.

3. **t-tests → explicit upper bounds on the curve and all its derivatives (Theorem 3).**
   `g1(p) ≤ 1{p≤½} exp(cv1(p)²/2) + 1{p>½}`, and for the two-sided case
   `g2(p) ≤ 1{p < 2(1-Φ(1))} B̃2^{(0)}(p) + 1{p ≥ 2(1-Φ(1))}` where the sharper (implicit)
   `B̃2^{(0)}(p) = ½[exp(h*cv2(p) - h*²/2) + exp(-h*cv2(p) - h*²/2)]` uses the non-zero root `h*(p)`
   of `(cv2 - h)e^{cv2·h} - (cv2 + h)e^{-cv2·h} = 0`, and is itself bounded by the simple explicit
   `exp(cv2(p)²/2)`. Derivative bounds `(-1)^k g_s^{(k)}(p) ≤ B_s^{(k)}(p)` are in their Appendix B.3.
   The bounds restrict the magnitude of the curve **near zero** as well as ruling out humps at 0.01,
   0.05, 0.10 — which is what makes them the only restriction with power against pure
   smallest-`p`-value selection.

**The tests built on these restrictions.** The implementable versions bin the `p`-values into `J`
histogram bins with proportions `π`, and test the moment inequalities `A q ≤ b` implied by the
restrictions using the Cox–Shi (2020) conditional chi-square statistic
`T = inf_{q: Aq ≤ b} n(π̂_{-J} - q)' Ω̂^{-1} (π̂_{-J} - q)`, compared to a `χ²` critical value with
`rank(Â)` degrees of freedom, where `Â` collects the rows of `A` for the **active** inequalities and
`Ω = diag{π_1,…,π_{J-1}} - π_{-J} π'_{-J}`. The paper's named tests: **CS1** (non-increasingness
only), **CS2B** (2-monotonicity plus bounds on the curve and its first two derivatives), **LCM**
(least-concave-majorant), a **Binomial** test on `[0.04,0.05]` split at 0.045, **Fisher's** test, and
a **density discontinuity** test at 0.05 (Cattaneo et al.). They use 30 bins (15–60 depending on
sample size) and restrict attention to `p < 0.15` or `p < 0.1`.

**How dependence is handled — the criterion the aim called binding.** Two separate devices, both
stated explicitly because the corpora have multiple `p`-values per paper:

- **A cluster-robust variance estimator of the sample proportions** `π̂` feeding the Cox–Shi
  statistic, clustering on the paper. This is a correction to `Ω̂`, not to the restrictions.
- **Random subsamples with one `p`-value per paper**, which "allow[s] us to use exact tests in the
  presence of within-paper correlation." This is the finite-sample-clean route: it buys exactness by
  spending the sample down to the number of clusters.

## Robustness evidence (qualitative only)

- **Two independent corpora**, one hand-collected from three economics journals and one text-mined
  across six scientific disciplines, with the same battery of tests applied to both.
- **The restrictions are derived, not calibrated.** Theorems 1–3 hold for every `Π`, which is the
  property the authors argue the earlier example-based justifications lacked.
- **The authors state three places their own machinery breaks**, and all three are the useful part:
  1. **Non-similar tests.** Assumption 2, and with it Theorem 1, **fails** when the null is
     composite on one side. Their own worked example: testing `H0: h ≤ 0` against `H1: h > 0` with a
     one-sided t-test gives `f'(x)/f(x) = -x` and `f'_h(x)/f_h(x) = -(x-h)`, so Assumption 2 holds
     for `h ≥ 0` and is **violated for `h < 0`**. If `Π` puts enough weight on `h < 0`, the `p`-curve
     can be non-monotonic or increasing **with no p-hacking at all**. They illustrate with
     `Π = N(μ,1)`: non-increasing at `μ = 0`, non-monotonic at `μ = -2.5`.
  2. **Rounding.** Rounded `p`-values (mass points at 0.01, 0.02, …) make the curve non-monotonic
     and discontinuous absent any p-hacking and therefore "invalidate[] the testable restrictions in
     Theorem 1." They re-run everything on de-rounded data (adding `U[u, 0.5]·10^{-k}` noise,
     `u = 0` for zero and `u = -0.5` for non-zero `p`-values) and the conclusions change materially:
     rejections on the raw data turn into non-rejections on the de-rounded data in several
     disciplines. They also note density-discontinuity tests are "poorly suited" where rounding is
     present, because discontinuities survive de-rounding.
  3. **Publication bias is not separable.** Their characterisation is of the `p`-curve under "no
     p-hacking **and** no publication bias", so the tests "become joint tests for p-hacking and
     publication bias." A rejection does not say which.
- **Honest about power.** On the one-`p`-value-per-paper subsamples of the economics corpus there
  are **no rejections**, and the authors write that this "suggest[s] that the tests may be
  underpowered in small samples." The companion paper (`notes/2026-11-19-the-power-of-those-tests-and-the-selection-function-this-lab-runs.md`)
  makes that the whole subject.
- The restrictions compose: the paper notes they extend to nuisance parameters, to a sub-interval
  `I ⊂ (0,1)` via `g_I(p) = g(p)/∫_I g`, and to a finite aggregation of different qualifying tests.

## Implementability here

This is an instrument for the lab's own board, not a strategy. Nothing in it touches the panel, the
universe or costs. Four consequences, in decreasing order of how much they bind.

- **`#480` — the lab's own test is the one Theorem 1 does not cover, and this is the binding
  finding.** Every restriction above requires a **similar** test, `H0 = {0}`. The lab's gate tests
  `skill ≤ 0` against `skill > 0`, a one-sided **composite** null, and the lab has measured real mass
  on negative skill (the v3 learnings record negative train skill in both subperiods for the residual
  reversion lineage, and the low-vol book at −0.03). That is precisely the authors' counterexample:
  with weight on `h < 0`, a non-monotone or increasing curve is what **no** p-hacking produces. So
  **a monotonicity or hump-shape reading of this lab's statistics is not licensed**, and had the
  2026-11-16 nightly found left-skew it would not have been evidence of a gamed search. The
  restriction that survives a composite null is **none of the three** as stated; the honest move is
  to re-derive the null for the actual test or to use a diagnostic that does not rest on the shape.
- **`#482` — the discreteness objection applies directly to `null_pctile`, and it is cheap to state.**
  The lab's `null_pctile` is reported as integer percentiles (the v3 learnings carry "64%", "80%",
  "99th–100th percentile"), and it is *constructed* by ranking against a finite set of random draws,
  so it is discrete by construction, not merely rounded in reporting. Theorem 1's restrictions are
  invalidated by exactly this. The 2026-11-16 nightly's reading of 27 `null_pctile` values as a
  sample from `U(0,1)` (KS `p` 0.041) inherits the problem: a KS test against a continuous reference
  distribution applied to values on a coarse grid is mis-sized, and the direction of the error
  depends on the grid. **If that reading is to be kept, de-round the percentiles the way this paper
  does — add `U[-0.5, 0.5]·10^{-k}` noise at the reporting resolution — and report both.** This is
  free and needs no holdout.
- **`#483` — the dependence correction the lab can actually afford is the one that costs the most
  observations.** Of the paper's two devices, the cluster-robust `Ω̂` needs a cluster variable; the
  lab has one in the folder's own audit (7–12 independent bets among 27 trials), so it is available.
  The one-per-cluster exact route would leave the lab with **7–12 observations**, and the paper's own
  experience is that this route produced **no rejections** on a corpus of 640 clusters. At 7–12 it is
  arithmetically hopeless. **The lab cannot buy exactness under dependence at its current board
  size**, and that is a statement about the design, not about the result.
- **`#484` — a rejection would be uninterpretable here for a second reason.** The lab both searches
  (p-hacks, in this literature's neutral sense) *and* selects what it records (the `FAMILY_LEAD` /
  `SCOUT` verdict structure is a reporting rule). Any rejection is a joint rejection of "no search
  effect" and "no selective recording", and the folder has no way to separate them.

**What is worth taking.** The explicit bound `g1(p) ≤ exp(cv1(p)²/2)` is a closed-form,
assumption-light ceiling on how much mass a set of honest one-sided t-statistics can put near any
`p`. Even where the composite-null problem kills the monotonicity reading, **the bound is a
one-line arithmetic check** the lab can run on its own recorded `t`-statistics at zero cost: compute
the empirical density of the recorded `p`-values in a bin and compare it to `exp(cv1(p)²/2)`. It
will not be a valid *test* here (the bound is also derived under `H0 = {0}`), but it is the right
order-of-magnitude yardstick and it is the restriction the companion paper identifies as the only
one with power against the lab's own style of search.

**Pitfall, stated plainly.** This source makes the folder's standing diagnostic *weaker*, not
stronger. Three sessions declined to take this aim on the grounds that applying a `p`-curve test to
27 statistics the lab's own audit calls 7–12 independent bets would be a misuse. **That judgement
was right, and this paper is the authority for it** — not because of the dependence (which it
corrects for) but because of the composite null, which it shows invalidates the restriction itself.

## Related

- Companion and the other half of the aim:
  `notes/2026-11-19-the-power-of-those-tests-and-the-selection-function-this-lab-runs.md`.
- The dispersion half of the aim (`#489`–`#491`):
  `notes/2026-11-19-dependence-robust-inference-on-a-set-of-estimates.md`.
- The nearest adjacent note, and explicitly a *different* object: `notes/2026-10-01-limits-of-p-hacking-publication-bias.md`
  fits a publication-probability function to the *published literature's* t-statistics; this paper
  tests the shape of a set of statistics against a null that holds for every effect distribution.
- `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md`, `notes/2026-08-24-multiple-testing-haircut.md`,
  `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — the haircut veins, which this does not
  duplicate: they adjust a threshold, this reads a distribution.
- **Named and unobtained**: Cattaneo, Jansson & Ma's density-discontinuity test, Cox & Shi (2020)'s
  conditional chi-square inference for moment inequalities, and Head et al. (2015) — all used here,
  none read. Do not re-hunt them unless a later aim needs the test's own derivation.
