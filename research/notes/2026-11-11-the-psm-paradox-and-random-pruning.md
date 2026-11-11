---
title: "Why Propensity Scores Should Not Be Used for Matching"
authors: King, Nielsen
year: 2019
venue: Political Analysis 27(4), 435–454 (peer-reviewed; the leading methodology journal of its field, outside this rubric's finance tier-1 list)
url: https://doi.org/10.1017/pan.2019.11
citations: 1398 (Crossref, checked 2026-11-11)
sample_period: none — analytic argument, simulations, and reanalyses of previously published observational studies
markets: n/a (statistical methodology; no financial data)
tier: B
validation_overlap: false
published_post_2018: true
---

## Mechanism

The adversarial half of tonight's vein, and the reason the scalar-score aim should not be closed
with two approving notes. This paper accepts Rosenbaum–Rubin's Theorem 1 as "mathematically
correct" and argues that **the target it certifies is the wrong one**, with a specific failure mode
that gets worse the harder the method is applied.

**The core distinction is between two experimental ideals.**

- A **fully blocked** randomized design blocks treated and control units exactly on the observed
  covariates at the start. Imbalance in `X` is zero by construction.
- A **completely randomized** design assigns treatment by a scalar probability only, so assignment
  is random *with respect to* `X`. In any one sample, random does not mean balanced: imbalance is
  `≥ 0`, zero only by coincidence.

A fully blocked design has more power, more efficiency, less imbalance and — the authors' main
concern — **less model dependence**, meaning less scope for the analyst's choice of outcome model
to move the answer.

**The claim.** Matching methods that work in the space of `X` (Mahalanobis distance matching,
coarsened exact matching) have a tuning parameter that can be driven to exact matching, so they
**approximate full blocking**. A method that matches on a scalar probability **can only approximate
complete randomization**, because it is blind to all variation in `X` that is orthogonal to the
score. Formally, the exact-matching solution is contained in the set the score-matching condition
admits, so score matching's imbalance is bounded below by the other methods' and strictly worse
except in unusual cases.

The asymmetry is stated crisply and is the sentence to carry: **exact matching on `X` implies the
scores are matched, but equal scores do not imply matched covariates.** The theorem runs one way
only, and the direction that would make the method safe is false.

**The PSM Paradox.** Once score matching has achieved its own goal — a subset in which the scores
are approximately constant within strata, i.e. complete randomization has been approximated — any
**further** pruning is random with respect to `X` given the score. And random pruning **increases**
imbalance. So tightening the caliper, which is what a careful analyst does when balance looks poor,
makes balance *worse*. The paradox is therefore invisible to the instinct that would catch it.

**Why random pruning increases imbalance** — three arguments, given in ascending generality:

1. In `k` continuous dimensions, the expected distance from a point to its nearest opposite-arm
   neighbour grows as `n₁^{−1/k}` shrinks with `n₁` (they cite Abadie–Imbens 2006 for the general
   form — the **same `N^{−1/k}` rate** this folder recorded as `#429`). Prune at random, `n₁`
   falls, matching discrepancies grow, imbalance grows.
2. A discrete toy: a perfectly balanced two-by-two sample (one male and one female in each arm).
   Drop two of four observations at random and with probability 1/2 the survivors are a matched
   pair, with probability 1/2 they are maximally mismatched. Expected imbalance rises.
3. The continuous case: with randomly assigned `T` and fixed univariate `X`, the squared difference
   in group means — which *is* the squared standard error of that difference — is proportional to
   `1/n`. Pruning raises it mechanically.

The authors note the exception honestly: if **all** matching discrepancies are the same size,
random pruning changes nothing. The paradox needs dispersion in match quality, which real data has.

**The paradox is not unique to the score, it is just reached first there.** Any method that prunes
independently of the covariates can do this. For `X`-space methods the point arrives only after
full blocking has been approximated and all information in `X` is exhausted — at which point
further pruning is obviously pointless anyway. For score matching it arrives at the much earlier
point of complete randomization, and arrives *silently*.

## Construction recipe

This note's recipe is a **diagnostic and a method choice**, not a strategy.

**The diagnostic — the imbalance/pruning curve.** It is cheap and it is the thing to copy:

1. Choose an imbalance metric computed in the **space of `X`**, not in score space. They use the
   Mahalanobis discrepancy (and report the same conclusions under the `L₁` metric of Iacus–King–Porro
   and under the average absolute difference in means).
2. Start from the full sample and record imbalance.
3. Prune the single worst-matched pair by the **method's own distance metric** — for score matching,
   the largest `|π̂ᵢ − π̂ⱼ|`.
4. Recompute imbalance in `X`-space. Repeat to exhaustion.
5. Plot imbalance (vertical) against number of observations pruned (horizontal). Mark two reference
   points: the imbalance of the **original unpruned data**, and the imbalance that complete
   randomization would produce.

A curve that **rises** as pruning proceeds is the paradox, and the published applications they
reanalyse show it setting in immediately and continuing until no data is left. A method whose curve
falls monotonically is doing what matching is supposed to do.

**The method definitions, for the comparison.** With `δ` an adjustable parameter and `S` the sample
covariance of `X`:

- **MDM**: keep pairs with `√((Xᵢ − Xⱼ)' S⁻¹ (Xᵢ − Xⱼ)) < δ`. `δ = 0` is exact matching.
- **CEM**: coarsen each covariate (natural breakpoints for continuous variables, category merges
  for discrete ones) and keep pairs that match **exactly on the coarsened values**. `δ = 0` is fine
  enough to recover `X` itself. Faster than the alternatives and the natural choice for mixed
  continuous/discrete covariates.
- **Score matching**: keep pairs with `|π̂ᵢ − π̂ⱼ| < δ`, `π̂` fitted by logit. "Most important here
  is the reduction of the `k`-dimensional `Xᵢ` to the scalar `πᵢ` **before** measuring the
  distance."

**Three specific practices the paper argues are counterproductive**, each of which is standard
advice elsewhere:

- **The quarter-standard-deviation caliper** on the score — the most commonly recommended default —
  is pruning *past* the paradox point, and in their reanalyses leaves imbalance worse than, or no
  better than, plain one-to-one score matching.
- **Respecifying the score model after dropping non-overlapping observations** makes the second
  model less discriminating, hence closer to random pruning, hence worse.
- **Including every available pretreatment variable in the score logit**, including ones with small
  or no effect on the outcome, pushes the fitted score toward noise and the pruning toward random.
  This is the direct opposite of the usual recommendation.

**Their positive advice**, if the score is used anyway: scale the variables to represent their
prior importance (the score does *not* solve the scaling problem, it only hides it); report how
much imbalance is left relative to the original data; and prefer the method when the sample
remaining after matching is very large, so the gap between full blocking and complete randomization
matters less.

## Robustness evidence (qualitative only)

- **The analytic core is not in dispute.** The containment argument and the `n^{−1/k}` nearest-
  neighbour-distance result are proofs and borrowed theorems, the latter from the same
  Abadie–Imbens paper the folder already holds. The toy examples in §5.1 are arithmetic.
- **The empirical sweep is the authors' own.** They reanalyse two published observational studies
  (one in civic education, one in development/conflict) and report "more than 20" additional
  unpublished datasets obtained privately, all showing the same pattern. These are the authors'
  reanalyses, not independent replications, and the unpublished data cannot be checked by anyone.
- **The content analysis is a real finding about practice.** They sampled 1,000 JSTOR articles
  referencing the method, read the 230 that applied it to real data, and found **94% use the
  simplest one-to-one greedy form** (80% plain, 14% after exact matching on a few variables), with
  only 6% doing any iterative balance checking. So the critique is aimed at what is actually done,
  not at a straw man. They also re-ran their analyses with an automated iterative respecification
  procedure and report "almost imperceptible differences".
- **Why Tier B rather than A.** Peer-reviewed in its field's leading methods journal and heavily
  cited (1,398), with the analytic half solid. But: the central empirical claim rests on the
  authors' own reanalyses; the paper is a *contested* critique and this folder has **not read the
  published responses to it**, which exist; and the evidence base is one discipline's applied
  corpus, with no financial data anywhere in it. The rubric's "solid but with a gap
  (unreplicated, single market)" is the honest cell. Treat the analytic results as established and
  the sweeping practical conclusion as one side of a live argument.
- **An open question the authors themselves flag** and this folder should not pretend to answer:
  whether the paradox explains the difficulties other scholars have reported with the method.

## Implementability here

**This is a refusal test and a method substitution, and it costs no trial.**

**Refusal test (new).** Any cohort or matched-control diagnostic proposed on this panel must plot
its **imbalance/pruning curve in `X`-space before its result is read**. If imbalance rises as the
caliper tightens, the design is in the paradox and its output is not evidence. The curve is free:
it needs the covariates, the match distances the design already computes, and one imbalance metric.
Without it, a tight caliper is indistinguishable from a loose one plus noise, and the tighter one is
the one a careful analyst would wrongly prefer.

**Method substitution, and this panel is the easy case.** The paper's own recommendation — CEM for
mixed continuous/discrete covariates, Euclidean or Mahalanobis for purely continuous ones — maps
onto a construction this lab already runs. **Coarsened exact matching on this panel is a cell
sort**: coarsen prior-year return into quintiles, trailing dollar volume into quintiles, keep region
exact, and match within cells. That is `#431`'s characteristic-matched-benchmark grid with the
matching interpretation attached, and it is `#406`'s volatility-tercile conditioning in the same
shape. Both are already in the candidate list; this paper says they are the *better* matching
design, not merely a cheaper one.

**Where it collides with tonight's other two notes, stated rather than smoothed over.**
`notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md` proves the scalar score
is the only legitimate way to collapse `k` covariates to one, and `#429` says `k = 1` is the only
dimension at which a matching estimator's intervals are valid. Taken together with this paper, the
lab is caught: **the dimension reduction that fixes the interval is the one that caps the
achievable balance.** The resolution is not to pick a winner but to notice that the two sides are
about different estimators —

- `#429`'s `N^{−1/k}` problem is about a **matching estimator's bias and its confidence interval**;
- this paper's problem is about **imbalance and model dependence in the retained sample**.

— and that **subclassification sidesteps both**. Five quintile strata of the fitted score, every
name retained, a weighted average of within-stratum differences: nothing is pruned, so the paradox
cannot fire (it is a statement about pruning), and nothing is a nearest-neighbour matching
estimator, so the `N^{−1/k}` rate does not apply. That is the construction to prefer on this panel,
and the fact that it falls out of the *disagreement* between the two sources is the useful part.

**Specific transfers to this lab's existing practice.**

- **"Prune the worst matches" is the instinct to distrust.** The lab prunes constantly — eligibility
  screens, liquidity floors, volatility bands, trimming the score's tails (`#412`-cluster). This
  paper's §5.1 argument is that **pruning independent of the covariates raises imbalance**, and the
  continuous version of it is just `1/n`: the squared difference in group means *is* the squared
  standard error. Any screen that removes names for a reason uncorrelated with the comparison being
  made is making that comparison noisier, not cleaner. That generalises past matching, and it is
  free to check.
- **Do not include every available feature in a selection model.** Their argument — extra weak
  predictors push the fitted score toward noise and the pruning toward random — is the same
  conclusion the folder's `statistical-learning` cluster reaches from the other direction ("the
  dominant signals are few"), now with a mechanism for *why* it hurts rather than merely fails to
  help.
- **The scaling point applies to every composite score this lab builds.** "Some claim that [the
  score] automatically solves the problem of scaling when some variables have unknown importance,
  but this is untrue." A z-scored blend of signals makes an implicit importance claim; the score
  does not launder it.

**What it does not say.** It does not say propensity scores are useless — the authors explicitly
note "propensity scores have other productive uses" (weighting, stratification, overlap
diagnostics). The target is specifically **matching-with-pruning on the score**. Do not carry this
note as a refutation of the previous two; carry it as the boundary on how their construction may be
used.

## Related

- `notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md` — the paper this one
  attacks, and whose Theorem 1 it accepts. Read in that order.
- `notes/2026-11-11-matching-on-the-estimated-score-and-its-variance.md` — improves *inference*
  given the design; this note attacks the design. Note the uncomfortable pairing: that paper says
  the fitted score's sampling variance is **smaller** than the true score's because `θ̂` adapts to
  the sample, and this one says the fitted score throws away the `X`-space information that would
  have bounded imbalance. Both can hold — they are statements about different quantities.
- `notes/2026-11-10-matching-estimator-bias-and-the-dimension-of-the-match.md` — `#429`'s
  `N^{−1/k}` rate, which this paper borrows for its own argument (its §5.1 cites the same source).
- `notes/2026-11-10-characteristic-matched-benchmark-portfolios.md` (`#431`) and
  `notes/2026-11-06-illiquidity-premium-and-where-the-size-screen-sits.md` (`#406`) — the cell-sort
  constructions already in the candidate list that this paper endorses as the better matching
  design.
- `experiments/learnings.md` — the de-concentration and screening results, all measured under v1/v2
  and none of them re-measured against an imbalance curve.
- `research/SUMMARY.md` candidate ideas #433–#435.
