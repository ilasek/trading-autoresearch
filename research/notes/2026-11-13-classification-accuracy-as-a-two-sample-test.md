---
title: "Classification Accuracy as a Proxy for Two-Sample Testing"
authors: Kim, Ramdas, Singh, Wasserman
year: 2021
venue: The Annals of Statistics 49(1), 411–434 (peer-reviewed; the flagship theoretical-statistics journal, outside this rubric's finance tier-1 list)
url: https://doi.org/10.1214/20-AOS1962
citations: 33 (Crossref, checked 2026-11-13); 105 for the arXiv record (Semantic Scholar, checked 2026-11-13); the DOI itself returns `not found` from Semantic Scholar, which `research/README.md` records as that index's third failure mode
sample_period: none — analytic propositions with proofs, plus Monte Carlo over Gaussian and multivariate-t distributions
markets: n/a (statistical methodology; no financial data of any kind)
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

This is the source [2026-11-12] named as the primary aim for session 91, and it supplies the thing
`#438` left as a bare number: **a valid hypothesis test built on held-out classification accuracy,
with a null distribution, a consistency theorem, and an explicit price in power relative to a
purpose-built test.** `#438` told the lab to fit a logit predicting group membership and read its
AUC, with `0.5` meaning balance. It said nothing about what value is significantly above `0.5`,
nothing about computing it out of sample, and nothing about what the procedure costs. All three are
in this paper.

The framing is the one the lab needs. Two samples `X₁…X_{n₀} ~ P₀` and `Y₁…Y_{n₁} ~ P₁`; the null is
`H₀: P₀ = P₁`. Label the first sample `0` and the second `1`, train a classifier, and measure how
well it separates them. The **central identity** is that this common machine-learning practice —
"train a classifier and check whether its accuracy beats chance" — *is* a two-sample test, whether or
not the analyst calls it one, and so it can and should be graded on the currency of tests: power at a
fixed level `α`. The paper's question is stated as "what are the pros and cons of the classifier-based
approach to two-sample testing?", and its answer is that the approach is valid, consistent, and
**systematically but boundedly less powerful** than a test designed for the alternative at hand.

Two structural facts make the construction work and are worth stating before the recipe:

- **Chance level is exactly `1/2` under the null, regardless of the class sizes.** The error is
  defined as the *balanced* error `E = (E₀ + E₁)/2`, where `E₀` is the probability of calling a `P₀`
  point a `1` and `E₁` the reverse. Under `P₀ = P₁` this is `1/2` whatever the ratio `n₀ : n₁`, because
  predicting the dominant label also achieves balanced accuracy one half. This is the property that
  makes the diagnostic interpretable without a class-prior correction — and it is the reason the
  *balanced* error, not raw accuracy, is the statistic to use when the two groups are of different
  sizes.
- **Testing is easier than classification, and the gap is the whole point.** The paper's Remark 6.1
  isolates a regime in which the Bayes-optimal classifier's true accuracy converges to `1/2` — no
  classifier can predict better than a coin — and yet the *test* built on that classifier's accuracy
  has non-trivial power, strictly above `α`. A diagnostic can therefore report "the two groups are
  distinguishable" in a setting where no useful classifier of individual names exists. The converse
  reading matters more for this lab: **a low AUC is not evidence of balance** unless it has been run
  through a test, because the test is sensitive where the classifier is useless.

## Construction recipe

**The statistic.** Split the pooled, labelled data into a training part and a test part, with
`n_{0,tr}, n_{1,tr}` and `n_{0,te}, n_{1,te}` points of each class. Fit the classifier `Ĉ` on the
training part only. The **sample-splitting error** is

    Ê^S = (Ê₀^S + Ê₁^S)/2,
      Ê₀^S = (1/n_{0,te}) Σ_i I[Ĉ(X_{n_{0,tr}+i}) = 1],
      Ê₁^S = (1/n_{1,te}) Σ_i I[Ĉ(Y_{n_{1,tr}+i}) = 0].

Reject when `Ê^S` is significantly **below** `1/2`. (Equivalently, accuracy significantly above.)

**Decision rule 1 — the asymptotic test (Proposition 9.1).** Studentize the held-out error under the
null and compare to a normal quantile: reject when

    (2·Ê^S − 1) / sqrt( Ê₀^S(1−Ê₀^S)/n_{0,te} + Ê₁^S(1−Ê₁^S)/n_{1,te} )  <  −z_α.

Under mild regularity this has asymptotic type-1 error at most `α` as `n → ∞`, possibly with `d → ∞`
**at any relative rate**, and is **consistent** — power → 1 — whenever the classifier's limiting true
accuracy is `1/2 + ε` for any constant `ε > 0`. It is cheap: one classifier fit, one closed-form
quantile. It has **no finite-sample guarantee**.

**Decision rule 2 — the permutation test (Theorem 9.1).** Exact level `α` for every `n` and `d`. Two
variants, differing only in what gets permuted:

- *Method 1 (half-permutation).* Split into halves `(X¹,Y¹)` and `(X²,Y²)`. Train `f*` on the first
  half once; evaluate on the second to get `a*`. Then `P` times: pool the **second half only**,
  permute labels, re-split into parts of the same sizes, and evaluate the **already-fitted** `f*` on
  the permuted data to get `a_p`. Reject if `a*` exceeds the `⌈(1−α)(1+P)⌉`-th order statistic of
  `{a*, a₁,…,a_P}`.
- *Method 2 (full-permutation).* Same first step, but each replicate pools **all four** parts,
  permutes, re-splits, and **refits** a classifier on the permuted first half before evaluating it on
  the permuted second half.

Both are valid level-`α` tests. Method 2 is potentially more powerful because the permuted accuracies
can take more distinct values, so the threshold is less conservative; Method 1 is far cheaper,
needing no refit. **The number of permutations needed for consistency is `P > (1−α)/α` — about 20 at
`α = 0.05` — and is independent of the sample size.** That is a remarkably small number, and it is the
operational reason this diagnostic is cheap: consistency does not require hundreds of replicates. (The
paper's own simulations use 200 when it wants a fair power comparison, which is a different
objective from consistency.)

**Split ratio.** For the linear-classifier case the asymptotic power expression is explicitly
maximised at `λ = κ = 1/2` — a **balanced train/test split**, and balanced class proportions within
each. Use half the data to fit and half to score; do not hold out a token test set.

**The price in power, as a constant.** For Gaussian mean-shift alternatives with common covariance,
the held-out accuracy of (oracle, known-`Σ`) Fisher's LDA and Hotelling's `T²` have power expressions
that **match exactly in `n`, `d`, `δ` and `Σ`** and differ only in a constant. The asymptotic relative
efficiency is

    ARE ≤ 1/√π ≈ 0.564,

i.e. the classifier-accuracy test needs **about `√π ≈ 1.77` times as many observations** to reach the
power Hotelling's test reaches. The same `1/√π` reappears for unknown `Σ` with naive Bayes against the
Bai–Saranadasa and Srivastava–Du high-dimensional variants of Hotelling, and for elliptical
distributions up to an explicit factor (`√2` times the marginal density at zero) — with the side
observation that the classifier test becomes *relatively more* efficient as the tails get heavier
(lower `t` degrees of freedom). The authors' own recommendation follows directly: against a
well-specified alternative, use the purpose-built statistic.

**Two side results worth carrying.** (i) An explicit asymptotic minimax power expression for
high-dimensional two-sample mean testing, valid for any shared positive-definite `Σ` and unbalanced
class sizes. (ii) Hotelling's `T²` with unknown `Σ` is **asymptotically minimax optimal whenever
`d/n → 0`**, not merely for fixed `d` — a partial rehabilitation of a test the high-dimensional
literature had written off after Bai–Saranadasa showed it loses power when `d/n → c ∈ (0,1)`.

## Robustness evidence (qualitative only)

The results are theorems with stated assumptions, not estimates, so the usual replication questions
do not apply in their usual form; what matters is scope. The consistency results (Proposition 9.1,
Theorem 9.1) hold for **any** classifier in **any** dimension under mild conditions on the limiting
per-class errors, which is the broadest claim in the paper and the one the lab would lean on. The
power results are narrower: Gaussian or elliptical, mean-shift alternatives, linear classifiers, and
— the authors flag this themselves — **pointwise rather than uniform over a class of distributions**,
a weakness they note applies to essentially the whole high-dimensional two-sample literature, not
only to them.

Simulation confirms the theory in the paper's own experiments, including a direct comparison of
sample-splitting against resubstitution (training and scoring on the same data) with permutation
critical values for both, so the comparison is like-for-like. In the high-dimensional cells the
sample-splitting tests are **slightly more powerful** than resubstitution tests, but the authors
state explicitly that additional simulations not shown reverse this in low dimensions or small
samples, so **neither estimator dominates**. Hotelling and its high-dimensional variants beat both in
every cell shown. The same ordering — accuracy tests below Hotelling against Gaussian mean shift — is
reported independently by Rosenblatt et al. (see the companion note), which is the nearest thing to
replication this kind of result admits.

The idea's lineage is older than the paper and is set out in its related-work section: Friedman (2004)
proposed using a classifier to *reduce* a multivariate test to a univariate one (score every point,
then run Mann–Whitney or Kolmogorov–Smirnov on the scores) — a **different** construction from
held-out accuracy, and worth distinguishing if the lab ever reaches for "classifier-based test" as a
phrase. Geometric-graph tests (`k`-NN graph, minimum spanning tree, cross-matching) are a separate
family the authors name as an open comparison.

## Implementability here

**What it is for.** Not a strategy. This is a **diagnostic**, and it answers a question the lab's
existing null does not ask. The v3 random-selection null asks whether a *return difference* could
have arisen by chance from a book of the same size and region mix. A classifier two-sample test asks
the prior question: **are the names this candidate selects distinguishable, on their observable
characteristics, from the names it did not select?** If they are not, there is no mechanism to
explain and no return difference to defend. If they are, the test's by-product (which covariate the
classifier uses) says *on what* they differ — which is exactly the question the 2026-11-12/13
nightly's third finding ran into when a US `amihud126` reading at `t +2.80` inverted under the
within-region log-price control, Amihud being proportional to `1/price`.

**Concrete construction on this panel.** On a rebalance date, label each eligible name `1` if the
candidate holds it and `0` otherwise. Features: the handful of covariates the lab already computes and
already worries about — trailing realised volatility, log dollar volume (or the liquidity tier),
region, log price level (`#420`–`#426`), and whatever the candidate's own score is *not*. Fit on a
random half of the names, score the other half, read the balanced held-out error, and calibrate with
Method 1 permutations. `n` is of order a thousand eligible names per date and `d` is a handful, so
`d/n → 0` — **the regime in which this paper says Hotelling's `T²` is minimax optimal**, and therefore
the regime in which the accuracy test is paying its `1.77×` sample-size premium for nothing if the
alternative is a mean shift. The honest recommendation that falls out: **if the lab's question is
"do the selected names differ in mean on these covariates", use Hotelling's `T²`, not an AUC.** Use
the classifier version when the suspected difference is an interaction or a nonlinearity the lab
cannot write down — which is precisely the authors' own takeaway rule (structured or abundant data
with an unspecifiable difference → flexible classifier; specifiable alternative → tailored statistic).

**Cost.** Method 1 with `P = 20` is twenty evaluations of one already-fitted classifier — trivially
free by the lab's standards, and free in the protocol's sense too, since it scores no returns and
records no trial. A single logistic regression on five features and a thousand rows is milliseconds.
There is no reason this cannot run on every candidate before the candidate file is written, which is
where `#413`'s composed pre-trial rule already sits.

**Four pitfalls, and the first is fatal if ignored.**

1. **Exchangeability.** The permutation test's exactness comes from the labels being exchangeable
   under the null. Across a *panel* — the same names on many dates — they are not: a name held in
   January is likely held in February, and names within a region move together. Permuting
   name-dates would therefore give an invalid null. **Run the test one rebalance date at a time**,
   where the unit is a name and the permutation is over names within that date's cross-section, and
   treat the sequence of dates as a sequence of separate tests (which then meets the lab's own
   multiple-testing apparatus, `#328`–`#342`). The paper does not discuss dependence at all; this
   caveat is the lab's, not the authors'.
2. **The split is not optional.** The asymptotic test's validity is derived from the held-out error
   being a sum of independent terms *given the training set*. Scoring on the data the classifier was
   fitted on breaks that, and the resubstitution null distribution is unknown — which is why the
   paper's own resubstitution comparison has to be calibrated by permutation.
3. **Read it, never optimise it.** `#438`'s warning survives this paper intact and is reinforced by
   it: tuning the classifier to maximise AUC is a specification search, and the permutation null
   calibrates only the test as specified, not the search that produced it. Fix the feature set and
   the classifier in advance.
4. **A `C` near `0.5` is weak evidence of balance, not strong.** The ARE result says this test is
   less powerful than a tailored one; Remark 6.1 says the classifier can be useless while the test is
   not. Failing to reject is therefore cheap to achieve and should be reported as "not detectably
   imbalanced at this `n`", with `#393`–`#400`'s detectability framing attached.

## Related

- `notes/2026-11-12-does-the-matching-paradox-bite-in-practice.md` — the source of `#438`'s C
  statistic, which this note turns into a test. That note's recommendation ("read it, never optimise
  it") is unchanged; what is added is a null distribution and a price.
- `notes/2026-11-13-classifier-two-sample-tests-construction.md` — the construction complement
  (Lopez-Paz & Oquab), which gives the explicit five-step recipe, the binomial null, and the
  classifier-flexibility / test-set-size trade-off this paper does not discuss.
- `notes/2026-11-13-accuracy-tests-are-underpowered-for-signal-detection.md` — the adversarial side
  (Rosenblatt et al.), which agrees on the ordering and attributes the gap to causes this paper's
  asymptotic framing cannot see, principally the **discreteness** of an accuracy statistic.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — same first two authors (Kim,
  Ramdas), different problem; the minimax-separation vocabulary there is the one used here.
- `notes/2026-11-11-the-psm-paradox-and-random-pruning.md` and
  `notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md` — the balance-diagnostic vein
  this test joins. `L̄₁` and the C statistic answer the same question with different machinery; this
  note supplies the inference for the second of them.
- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — where a per-date sequence of
  these tests would have to be accounted for.
