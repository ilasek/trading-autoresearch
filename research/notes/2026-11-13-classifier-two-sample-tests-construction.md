---
title: "Revisiting Classifier Two-Sample Tests (C2ST)"
authors: Lopez-Paz, Oquab
year: 2017
venue: International Conference on Learning Representations (ICLR) — a top-tier refereed machine-learning conference; venue tier 2 under this rubric's finance-shaped ladder, but the archival venue of record in its own field
url: https://arxiv.org/abs/1610.06545
citations: 666 (Semantic Scholar, checked 2026-11-13); no registered DOI for the conference version, so Crossref holds no count
sample_period: none — synthetic distributions (Gaussian, Student-t, sinusoid) and image benchmarks; no time series of any kind
markets: n/a (machine-learning methodology; no financial data)
tier: B
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the construction complement [2026-11-12] named alongside the primary aim, and its value here
is entirely operational: it is the paper that writes the classifier two-sample test down as **five
numbered steps with a closed-form null**, in a form a person can implement in an afternoon. Where
Kim–Ramdas–Singh–Wasserman give the theory (consistency, permutation validity, the `1/√π` price), this
gives the procedure, the simple Gaussian null, and the one design trade-off that decides whether the
test has any power at all.

The mechanism is the same reduction: build a labelled dataset by tagging every point of sample `S_P`
with `0` and every point of `S_Q` with `1`; if `P = Q` the labelling is pure noise and no classifier
can beat chance on held-out data; if `P ≠ Q` a classifier that finds the difference will beat chance,
and **by how much** is the effect size. The paper's framing claim — that this is worth doing rather
than merely possible — rests on four properties it argues the approach has and kernel or
moment-based tests do not:

1. It **learns a representation of the data on the fly**, so the analyst does not have to specify in
   advance which direction the two distributions differ in. This is the honest statement of when the
   method earns its power discount.
2. The statistic is in **interpretable units**: a held-out accuracy is "the fraction of points
   distinguishable", a number a reader can argue about, unlike a kernel discrepancy in arbitrary
   units.
3. It has a **simple null distribution** — binomial, with no kernel bandwidth or spectrum to
   estimate.
4. Its **per-point predicted probabilities localise the difference**: the points the classifier gets
   right with the most confidence are the ones where the two distributions differ most, and whatever
   feature-importance machinery the classifier carries (linear-model coefficients, random-forest
   importances) says *on which variables* they differ. This is the property the lab should want most,
   because a balance diagnostic that says only "imbalanced" leaves the next step undetermined.

## Construction recipe

Assume `m = n` for simplicity (the paper does). Five steps:

1. **Build** `D = {(x_i, 0)}_{i=1..n} ∪ {(y_i, 1)}_{i=1..n} =: {(z_i, l_i)}_{i=1..2n}`.
2. **Shuffle and split** `D` into disjoint `D_tr` and `D_te`, with `n_te = |D_te|`.
3. **Train** a binary classifier `f : X → [0,1]` on `D_tr` only, where `f(z)` estimates
   `p(l = 1 | z)`. Model selection — cross-validation, hyper-parameter search — may be run **inside
   `D_tr`** without invalidating anything.
4. **Score** on the held-out part:

       t̂ = (1/n_te) · Σ_{(z_i,l_i) ∈ D_te} I[ I(f(z_i) > 1/2) = l_i ].

5. **Decide** against the null distribution below.

**The null.** Each held-out term is an independent Bernoulli. Under `H₀: P = Q` the classification
problem is impossible, so `n_te · t̂ ~ Binomial(n_te, 1/2)` exactly, and for large `n_te` the central
limit theorem gives

    t̂ ~ N( 1/2 , 1/(4·n_te) )   under H₀.

That is the whole calibration: **a `z` statistic of `(t̂ − 1/2) / sqrt(1/(4·n_te))`**, no permutation
needed, no nuisance parameter. Under the alternative `n_te·t̂` is Poisson-binomial (the per-point
success probabilities differ), approximated by `Binomial(n_te, p̄)` with `p̄` the average, giving
`t̂ ~ N(p̄, p̄(1−p̄)/n_te)`.

**Power (Theorem 1).** With effect size `ε ∈ (0, 1/2)` defined by true accuracy `1/2 + ε` under the
alternative, the approximate power at level `α` is

    Φ( ( √n_te · ε − Φ⁻¹(1−α)/2 ) / sqrt( 1/4 − ε² ) ).

Two things to read off it. First, power depends on `n_te` and `ε` and **not on the dimension `d`**,
which is the optimal order of magnitude for fixed-`d`, `n → ∞` problems; the authors explicitly leave
the `n/d → c` regime to future work and point at Ramdas et al. for it (that regime is the companion
note's subject). Second, and this is the design rule:

> **Maximising power is a trade-off between the classifier's accuracy `ε` and the test-set size
> `n_te`, and the two pull against each other.** A simple classifier misses nonlinear structure
> (smaller `ε`) but needs little training data (larger `n_te`); a flexible classifier finds more
> (larger `ε`) but needs more training data (smaller `n_te`). Formally this is the VC-dimension
> bias–variance trade-off wearing a different hat.

**Remark 2 (worth carrying).** The zero-one loss makes `t̂` a mean of Bernoullis, which is a
**high-variance** statistic. The construction extends unchanged to real-valued binary classification
losses, whose lower variance enters the power expression directly and can be tuned as a
power-maximising hyper-parameter in the manner of Gretton et al.'s optimal-kernel work. This is the
same weakness the adversarial companion note diagnoses as *discretization*, arriving from the
construction side.

**Independence testing, free.** Because independence testing is a special case, the same machinery
tests `H₀ : P(X,Y) = P(X)P(Y)` by comparing the paired sample to one in which `Y` has been randomly
permuted against `X`. Worth knowing: the lab's "is this score related to that one" questions are of
this shape.

## Robustness evidence (qualitative only)

The paper's evidence is simulation and image benchmarks, not a multi-decade multi-market sample, and
that is the main reason it is graded **tier B** here rather than A: a conference paper whose empirical
section is about evaluating generative models carries no replication record of the kind this rubric
asks for, and its headline claim ("a new state of the art") is a claim about benchmark tables that
this folder's anti-lookahead rules would not let it record anyway. What *is* robust is the part that
is arithmetic — the binomial null and the power expression follow from the construction, and the
companion Annals paper proves the corresponding consistency statements under far weaker assumptions.

Its own comparisons are against kernel (MMD), mean-embedding (ME), and classical univariate tests
(Kolmogorov–Smirnov, Kuiper, Wilcoxon) across Gaussian-vs-Gaussian, Student-t-vs-Gaussian and
sinusoidal-dependence settings, with type-I error reported alongside power — which is the right
sanity check and confirms level control for the classifier variants. The qualitative pattern that
transfers: the classifier test wins where the difference is **not** a mean shift (the sinusoid, the
heavy-tail contrast) and does not win where it is. That is consistent, from the opposite direction,
with the ARE result in the companion note and with Rosenblatt et al.'s simulations.

The prior-uses section is the useful bibliographic map: the reduction originates with Friedman (2003),
was studied information-theoretically by Pérez-Cruz (2009) and Reid–Williamson (2011), and is
implicit in any method that discriminates data from noise — noise-contrastive estimation, negative
sampling, GANs. The authors also note that `#438`'s C-statistic-as-AUC usage is common in
neuroscience, where this folder's adversarial source lives.

## Implementability here

This is the note to implement from. The procedure is five lines of code against `sklearn`, which
`program.md` confirms is installed, and the null needs no permutation at all — `N(1/2, 1/(4 n_te))`
is a closed form. Concretely, for a candidate's selection on one rebalance date:

- `z_i` = the covariate vector for eligible name `i` (trailing volatility, log dollar volume, region
  one-hot, log price level — the lab's standing control set, `#406`/`#422`/`#423`);
- `l_i` = 1 if the candidate holds the name, 0 otherwise;
- split names at random into halves, fit a logistic regression on one, score the other;
- `z = (t̂ − 1/2)/sqrt(1/(4 n_te))`, two-sided or one-sided as preferred.

With roughly a thousand eligible names, `n_te ≈ 500`, so the null standard deviation of `t̂` is about
`0.022` — meaning **a held-out accuracy below roughly `0.54` is not distinguishable from chance at
`α = 0.05` on a single date.** That number is pure arithmetic from `n_te`, carries no market
information, and is the single most useful thing in this note: it tells the lab in advance how big an
imbalance a one-date test can even see, which is `#393`–`#400`'s detectability question asked of a
balance check.

**Four adaptations and cautions specific to this panel.**

1. **Class imbalance.** A candidate holding 25 of 1,000 names gives a 2.5% positive rate, and the
   paper's `m = n` assumption does not hold. The binomial null above is for *raw* accuracy on a
   balanced set; with unequal classes, predicting "never hold" scores 97.5%. Use the **balanced**
   error from the companion note (the average of the two per-class error rates), whose chance level
   is `1/2` regardless of the ratio, and let `n_te` in the variance be driven by the **smaller** class
   — with 25 held names the test is weak, which is a true statement about what a 25-name book's
   selection can be shown to be.
2. **Prefer the simple classifier.** Theorem 1's trade-off is decided here by the covariate count
   being small (a handful) and the structure being plausibly monotone: a penalised logistic
   regression gets nearly all of the available `ε` while leaving `n_te` at its maximum. A gradient
   booster would cost test-set size for interaction structure the lab has no prior reason to expect,
   and would reintroduce exactly the hyper-parameter search `#437` exists to remove.
3. **The null is asymptotic in `n_te`, and the statistic is discrete.** With a small held-out set the
   normal approximation to a binomial is poor in the tail that matters. Use the exact binomial, or
   the companion note's permutation calibration, whenever the smaller class has fewer than a few
   dozen names.
4. **Model selection inside `D_tr` is permitted; feature selection across the whole sample is not.**
   The paper's licence is explicit and narrow — cross-validate within the training split. Choosing
   which covariates to include after seeing which ones separate is the specification search, and no
   null here calibrates it.

**What it does not do.** It is not a strategy, it scores no returns, and it cannot be promoted. It is
a free pre-trial diagnostic in the sense `#413` uses the phrase, and its output is a statement about
*names*, never about *returns*.

## Related

- `notes/2026-11-13-classification-accuracy-as-a-two-sample-test.md` — the theory for this
  construction: consistency for any classifier, exact permutation validity, the balanced-error
  definition that fixes this note's class-imbalance problem, and the `1/√π` power price. Read that
  note for *whether* to use the method; read this one for *how*.
- `notes/2026-11-13-accuracy-tests-are-underpowered-for-signal-detection.md` — the adversarial side,
  which identifies the discreteness this note's Remark 2 anticipates as the leading cause of lost
  power, and prefers a leave-one-out bootstrap to a single split or `V`-fold.
- `notes/2026-11-12-does-the-matching-paradox-bite-in-practice.md` — `#438`, the source of the C
  statistic this note calibrates.
- `notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md` — `L̄₁`, the other
  distribution-free balance measure. `L̄₁` needs a binning choice and no fitting; this needs a fitting
  choice and no binning. They are substitutes, and disagreement between them is informative.
