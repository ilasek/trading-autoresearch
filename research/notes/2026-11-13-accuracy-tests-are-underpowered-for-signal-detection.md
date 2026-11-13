---
title: "Better-Than-Chance Classification for Signal Detection"
authors: Rosenblatt, Benjamini, Gilron, Mukamel, Goeman
year: 2021
venue: Biostatistics 22(2) (peer-reviewed; a leading applied-statistics journal, outside this rubric's finance tier-1 list). Published online 2019-10-14
url: https://doi.org/10.1093/biostatistics/kxz035
citations: 14 (Crossref, checked 2026-11-13); read from the authors' arXiv version, arXiv:1608.08873v2 (2017-12-14), so section numbers cited here are the preprint's
sample_period: none — Monte Carlo under varied covariance structures, plus one previously published fMRI dataset
markets: n/a (statistical methodology; no financial data)
tier: B
validation_overlap: false
published_post_2018: true
---

## Mechanism

This is the adversarial request the detector's standing rule budgets for every vein — *the source that
says the vein is a mistake* — and it does its job: it agrees with the companion Annals paper on the
ordering of the tests, disagrees with it about **why**, and the disagreement changes what the lab
should build. Where Kim–Ramdas–Singh–Wasserman price the classifier-accuracy test at a clean
asymptotic constant (`ARE ≤ 1/√π`, i.e. `≈1.77×` the sample size), these authors run finite-sample
simulations and argue the practical gap is larger and comes from a source asymptotics cannot see.

Their thesis, stated plainly: **using a classifier's accuracy as a test statistic is an underpowered
way to detect a difference between two populations, and it is more computationally demanding than a
test.** The workflow they attack — fit a classifier, cross-validate, ask whether accuracy beats
chance — is standard in neuroimaging and genetics, and is exactly the workflow `#438` recommends to
this lab as a balance diagnostic.

**Where the power goes (their §5.1), four causes:**

(a) **Discretization.** An accuracy statistic takes a bounded number of values — at most the number
of held-out points. A discrete statistic cannot exhaust the permissible false-positive rate, so it is
*conservative*, and conservative means less powerful. The degree of discretization is governed by the
sample size, so **an asymptotic analysis cannot see this cause at all**; the authors name the
companion paper explicitly on this point, and note the consequence: an asymptotic argument may bless
resubstitution accuracy as a reasonable statistic while it suffers severe finite-sample power loss.
The canonical fix — a randomized test that rejects with probability
`max{(α − P{T_π > T}) / P{T_π = T}, 0}` when the permutation `p`-value exceeds `α` — was implemented
and gave **only a minor improvement**, so the discreteness is not an artefact of ties alone.

(b) **Shift alternatives.** Their simulations use mean-shift alternatives, where a location test is
expected to win by a Neyman–Pearson argument. This is an honest concession and it bounds the claim —
it is also the point at which this source and the C2ST construction note agree rather than conflict,
since the C2ST paper's wins are on non-shift alternatives.

(c) **Inefficient use of the data when validating with a holdout set.**

(d) **Inappropriate regularization**, with the striking formulation: **testing requires less
regularization than predicting.** A classifier tuned to predict well is not tuned to test well.

Their summary sentence is worth carrying verbatim as a prior: *"we dare argue that an accuracy test
will rarely have more power than a high-dimensional location test."*

**The one thing everyone agrees on: level is controlled.** Across every simulation, under the null,
all statistics — location tests and accuracy tests alike — kept the false-positive rate at or below
`0.05`. So the dispute is **entirely about power**, never about validity. For a lab that wants a
*refusal* test rather than a discovery test, that distinction matters more than the headline.

## Construction recipe

This source's contribution to construction is a set of design choices for the accuracy estimate, each
argued from simulation. Their framing is the right one for a diagnostic: **we are not trying to
estimate accuracy without bias, we are trying to detect departure from chance**, and those are
different objectives.

- **Cross-validate or not?** Bias in the accuracy estimate is *not a problem for testing*, provided
  it does not break the error guarantee — the intuition being that a bias introduced identically in
  every permutation cancels in the permutation null. So resubstitution accuracy is admissible as a
  test statistic, calibrated by permutation.
- **Resubstitution is for high signal-to-noise only.** When `n ≫ p`, resubstitution avoids the cost
  of cross-validation without losing power. In low SNR the loss is considerable, which they attribute
  to discretization compounding with concentration: the sampling distributions of the resubstitution
  accuracy under null and alternative become indistinguishable.
- **`V`-fold cross-validation is dominated and is never recommended.** They fix `V = 4` and decline
  to study the effect of `V` precisely because the whole family loses to the alternative below.
- **Use the leave-one-out bootstrap (bLOO) instead.** The discreteness of the statistic is governed
  by the number of distinct held-out points; resampling test sets **with replacement** smooths it.
  bLOO is the average accuracy of the held-out observations over all bootstrap samples:

      Ê_A^bLOO = (1/n) Σ_{i=1..n} (1/|C^(i)|) Σ_{b ∈ C^(i)} I{A_{S^b}(x_i) = y_i},

  where `S^b` is a bootstrap sample of size `n` drawn with replacement and `C^(i)` indexes the
  bootstrap samples **not** containing observation `i`; equivalently, average over bootstrap
  replicates of the accuracy on each replicate's out-of-bag set. Its derivatives (`0.632`, `0.632+`)
  are the same idea. **This is their headline construction recommendation.**
- **Regularize the classifier, and regularize it for testing.** In low-SNR regimes — `n` of the order
  of `p`, or strong correlations — regularization is crucial to detection power. They single out
  **shrinkage-based diagonal LDA** (Pang et al. 2009) as a good performer, while saying more research
  is needed, in particular on regularizing in directions orthogonal to the mean difference.
- **Permutation mechanics.** The neuroimaging convention is to permute labels and **refold** the data
  after each permutation, because permuting labels unbalances a stratified folding. They follow it
  for comparability while noting it is computationally cheaper to **permute features instead of
  labels** (Golland et al.), which fixes the label-to-fold assignment.
- **Sample size is the cure for conservativeness.** The conservativeness caused by discretization
  decreases with sample size — the one lever that reliably works.

**When an accuracy test cannot be replaced.** Their §5.7 concedes the case: when the question is not
"is there a difference" but "can *this particular predictor* extract it" — brain–computer interfaces,
clinical diagnostics — no location test substitutes. The above list is what to do in that case.

**On interpretation.** They reject the common defence that accuracy is attractive because it is a
sample-size-invariant effect size: the multivariate-statistics literature supplies effect-size
estimators generalising Cohen's `d` that do not suffer discretization. And they cite work showing
practitioners find the signal type captured by accuracy tests *less* interpretable than that captured
by location tests — the direct contrary of the C2ST paper's interpretability claim, and a genuine,
unresolved disagreement between two of tonight's three sources.

## Robustness evidence (qualitative only)

Simulation-based, with the battery varied systematically along the axes that matter: departures from
Gaussianity, from sphericity, from homoskedasticity, a long-memory Brownian correlation structure,
and the high-dimensional cell (`n = 40`, `p = 23`, so `p/n` is not small). The ordering — location
tests above accuracy tests — holds across all of them. The comparison set is strong and includes the
regularized high-dimensional location tests that matter (`Hotelling.shrink` with the
Schäfer–Strimmer covariance, Goeman's test, Srivastava's `sd`), not just classical Hotelling, so the
result is not an artefact of comparing against a statistic known to fail when `p/n → c`. A real fMRI
example accompanies the simulations.

Tier **B** rather than A, for three reasons recorded rather than glossed: the evidence is simulation
plus one application, not a multi-sample replication record; the alternatives studied are
predominantly **shift** alternatives, which the authors themselves flag as favourable to their
conclusion; and the citation count is modest. What raises confidence is agreement from outside the
authorship — the companion Annals paper independently reports the same ordering in its own
simulations and cites this work as reaching the same conclusion — and the fact that the two papers'
*mechanisms* for the gap are different and additive rather than competing: a constant-factor
asymptotic efficiency loss, plus a finite-sample discreteness loss on top of it.

## Implementability here

**The decisive consequence for this lab, and it is a refusal.** `#438` proposed the C statistic as the
cheapest balance diagnostic in the matched-control vein. These three sources together say: **if the
imbalance you are looking for is a difference in means on covariates you can name, do not use a
classifier for it — use a regularized high-dimensional location test on those covariates.** The lab's
balance questions are overwhelmingly of that shape (is the selected set shifted in volatility, in
liquidity, in log price, in region mix?), the covariate count is a handful against ~1,000 eligible
names so `d/n → 0`, and the companion note establishes that **Hotelling's `T²` is asymptotically
minimax optimal in exactly that regime**. Paying `1.77×` in sample size plus a discreteness penalty,
for flexibility against nonlinear alternatives nobody has hypothesised, is a bad trade.

**Where the classifier version still earns its place here**, on their own §5.7 logic: when the
question is *can anything at all tell the two sets apart*, with no named direction — which is the
genuinely open-ended version of `#438`'s question and the one a location test cannot answer. In that
case this note's construction list applies:

- prefer **bLOO** over a single split or `V`-fold (and note this **conflicts** with the companion
  note's single balanced split, which is optimal within the split family only — the comparison these
  authors run is across families);
- **regularize** — a penalised logistic or shrinkage diagonal LDA, not an unregularized fit, since
  with correlated covariates (volatility and liquidity are correlated on this panel; `#422` documents
  a signed error in the liquidity tier that is itself price-driven) the low-SNR regime is the
  realistic one;
- expect the statistic to be **conservative**, and say so when reporting a non-rejection — a
  `C` near `0.5` is even weaker evidence of balance than the companion note's ARE already implies;
- with a small held book the smaller class is tiny, discreteness is severe, and the test is close to
  uninformative. **Book size, not panel size, governs this diagnostic's power.**

**One further transfer, outside the balance vein.** The caution *"testing requires less regularization
than predicting"* generalises to the lab's screens. A score built to *forecast* returns well is not
the score that best *detects* whether a relationship exists; the lab's free screens (`#376`'s one-bit
truncation test, `#389`'s cumulative-curve test, `#381`'s `σ_IC`) are detection instruments, and
tuning them with prediction-shaped choices — more shrinkage, more features, finer buckets — can cost
detection power. This is the same asymmetry `#437`'s measurement-error result reaches from the
matching side.

**Not a strategy.** Nothing here scores a return or proposes a book. Everything above is free in the
protocol's sense.

## Related

- `notes/2026-11-13-classification-accuracy-as-a-two-sample-test.md` — the companion that this note
  argues with. Agreement: the ordering, and that level is controlled. Disagreement: whether the gap
  is a clean constant (there) or a constant plus an unbounded finite-sample discreteness penalty
  (here), and whether sample splitting or resampling-with-replacement is the right estimator.
- `notes/2026-11-13-classifier-two-sample-tests-construction.md` — this note's direct antagonist on
  interpretability, and the source of the closed-form binomial null these authors would say is too
  coarse in the tail when the held-out set is small. That note's own Remark 2 (zero-one loss is a
  high-variance statistic; real-valued losses are better) anticipates this note's cause (a).
- `notes/2026-11-12-does-the-matching-paradox-bite-in-practice.md` — `#438`, whose C statistic this
  note is the strongest argument against using as the *primary* balance check.
- `notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md` — `L̄₁`, which is not a test
  statistic and therefore sidesteps this entire dispute; it bounds imbalance rather than testing for
  it, which is why `#436`'s bound is worth more than any of tonight's `p`-values.
- `notes/2026-10-21-sure-independence-screening-marginal-vs-joint.md` — where the
  "testing ≠ predicting" asymmetry lands on the lab's own screens.
