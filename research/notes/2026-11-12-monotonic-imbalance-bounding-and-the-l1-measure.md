---
title: "Multivariate Matching Methods That Are Monotonic Imbalance Bounding"
authors: Iacus, King, Porro
year: 2011
venue: Journal of the American Statistical Association 106(493), 345–361 (peer-reviewed; the flagship journal of its discipline, outside this rubric's finance tier-1 list)
url: https://doi.org/10.1198/jasa.2011.tm09599
citations: 839 (Crossref, checked 2026-11-12)
sample_period: none — analytic class definition, propositions with proofs, Monte Carlo, and two previously published non-financial observational datasets
markets: n/a (statistical methodology; no financial data of any kind)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source [2026-11-11] named as the primary aim for session 90, and it supplies the object
`#435`'s refusal test requires and the folder did not hold: **a definition of multivariate
imbalance, computable from the two groups' empirical distributions alone, plus a class of matching
methods whose guarantee is stated in that metric rather than in a matched-sample size.**

The paper's organising claim is that the existing theory of matching — the Equal Percent Bias
Reducing (EPBR) class — makes the wrong thing the user's choice. Under EPBR (Definition 1) the
matched control count `m_C` is **fixed ex ante** and the balance achieved, the scalar `γ` in
`E[X̄_mT − X̄_mC] = γ(µ₁ − µ₀)`, is **computed ex post**. Three things follow, and all three are
properties this lab's own matched designs inherit:

1. **EPBR's guarantee is in expectation, not in sample.** It is a statement about the population
   that generated the data, whereas the efficiency of the estimate actually produced is a function
   of the *in-sample* imbalance. The authors note in passing that this is what explains the
   otherwise counter-intuitive result that matching on the *estimated* propensity score is more
   efficient than matching on the true one (citing Hirano–Imbens–Ridder 2003) — the same direction
   `#434` records from Abadie–Imbens, now with a reason attached.
2. **EPBR's guarantee is about means only.** The `γ` is a scalar precisely because the property
   asserts that balance improves *proportionally on every covariate and every linear combination of
   them at once*. It says nothing about variances, covariances, quantiles, interactions or
   nonlinearities, except for terms the analyst explicitly adds to `X`. And the proportionality
   itself is conditional on data assumptions (ellipsoidal symmetry and a proportional covariance
   structure) that "rarely hold, and are almost never known to hold".
3. **Balancing means is not balancing distributions, and the paper demonstrates the gap
   constructively.** Propensity-score *weighting* with `w_i = 1 − p̂_i` on treated and `p̂_i` on
   controls eliminates **all** mean imbalance by construction — every difference in means goes to
   zero — while the multivariate imbalance of the joint distribution is left essentially unchanged.
   A design can therefore pass every per-variable balance check it is given and be exactly as
   imbalanced as it started.

The replacement class inverts the user's choice. **Monotonic Imbalance Bounding (MIB)**
(Definition 3) asks the analyst to fix the **maximum tolerable imbalance** ex ante, as a vector
`π = (π₁,…,π_k)` of one tuning parameter per covariate, and lets the matched counts `m_T(π)`,
`m_C(π)` fall out of the algorithm. Its guarantee is the monotonicity in the name: there exists a
monotonically increasing `γ_{f,D}(·)` with `D(f(X_mT(π)), f(X_mC(π))) ≤ γ_{f,D}(π)`, and — this is
the operative clause — when the method satisfies the per-variable form `γ_j(π_j)`, **tightening one
covariate's tuning parameter leaves every other covariate's imbalance bound unchanged.** The bound
depends on `π` only; it does not depend on `m_T` or `m_C`, so it is a worst case rather than an
average. The contrast the paper draws is exact: with extra data assumptions, EPBR means imbalance
changes on all variables proportionally at once; without any data assumptions, MIB means changing
one variable's knob does not disturb the others' maxima.

Neither class can deliver both a bound on imbalance and a prescribed matched-sample size — the
paper states this as a limitation of matching itself, not of either class. The authors argue the MIB
side of the trade is the right one in observational work, "where data is typically plentiful but is
not under control of the investigator."

The reason the monotonicity matters practically is the failure mode it rules out: *improving balance
on one variable while silently worsening it on others*, which both classes exist to avoid and which
is "a serious practical problem in real applications." Under MIB the analyst can set each covariate's
tolerance as **the largest measurement error they are willing to accept in it** — the paper's own
examples are two pounds of body weight, five years of age in middle age, a year or two of education
away from a credential threshold — and know those maxima will hold no matter how the other knobs
are turned.

## Construction recipe

**The imbalance measure `L₁` (Definition 5), and the bin choice that makes it a single number.**

1. Choose a set of bins for each covariate. `H(X_j)` is the set of intervals the support of `X_j` is
   cut into; the multidimensional histogram is the cells of the Cartesian product
   `H(X₁) × ⋯ × H(X_k) = H`.
2. Cross-tabulate treated and control units into those cells and take **relative** frequencies
   `f_{ℓ₁⋯ℓ_k}` (treated) and `g_{ℓ₁⋯ℓ_k}` (control). Using relative frequencies is what makes the
   measure insensitive to the two groups having different sizes. Observation weights, if a matching
   method emits them, enter here.
3. `L₁(f, g; H) = ½ Σ_{cells} |f_{ℓ₁⋯ℓ_k} − g_{ℓ₁⋯ℓ_k}|`.

Properties worth having in hand: `L₁ = 0` iff the two empirical distributions coincide, `L₁ = 1` iff
they are completely separated (up to the bin resolution), and the reading is directly interpretable
as overlap — `L₁ = 0.6` means 40% of the area under the two histograms overlaps. Empty cells
contribute nothing, so the sum has at most `n` nonzero terms however large the cell space is. A
matching method is doing its job when `L₁(f^m, g^m) ≤ L₁(f, g)` **with the bins `H` held fixed** —
comparing two methods under two different bin definitions is not a comparison.

**Choosing the bins `H` for the metric** (criterion (iii) for the metric itself). `L₁(H)` depends on
`H` the way a kernel density estimate depends on bandwidth: bins too fine force `L₁ = 1` (everything
separates in high dimension), bins too coarse force `L₁ = 0` (nothing discriminates). The paper's
device is the **`L₁`-profile**: the distribution of `L₁(H)` over the set of all possible bin
definitions, sampled by drawing random `H` (they use 250 draws). Plot `L₁(H)` against `H` with `H`
sorted by the *raw* data's `L₁`, and compare methods as curves rather than at a point. The
recommended summary statistic for general use is

> **`L̄₁ ≡ L₁(H̄)` where `H̄` is the bin set at the _median_ of the `L₁`-profile of the raw data.**

The empirical regularity they report across the datasets they have analysed — and they flag it as
"worth checking for in specific applications" rather than assuming it — is that the **rank order** of
methods by imbalance reduction is approximately invariant across almost the whole range of `H`, so
the bin choice usually does not decide which method wins. On the non-financial benchmark dataset they
illustrate with, the ordering has coarsened exact matching ahead of propensity-score matching ahead
of Mahalanobis matching, with the latter two only slightly better than the raw data.

**Coarsened Exact Matching (CEM), the MIB member to build (Section 3).** Three steps:

1. **Coarsen** each variable in `X` as much as the analyst is willing, giving `C(X)`. For a
   continuous variable, cut the range into equal intervals of length `ε_j` (if substance suggests
   unequal intervals, `ε_j` is the maximum length). For a categorical variable, group levels.
2. **Exact-match on `C(X)`**: sort observations into strata `s ∈ S`, one per unique value of `C(X)`.
3. **Keep strata holding both treated and control units.** Strata with only controls are discarded;
   strata with only treated units are the ones that would require extrapolation.

`ε_j` **is the MIB tuning parameter** — `π_j = ε_j`, `D(x,y) = |x − y|` — so the coarsening is not a
nuisance choice, it *is* the imbalance tolerance, and the paper's propositions say what each value of
it buys. With `R_j` the range of `X_j` and `θ_j ≈ ⌈R_j/ε_j⌉` the implied bin count:

- **Proposition 2** — means: `|X̄^w_{m_T,j} − X̄^w_{m_C,j}| ≤ ε_j`.
- **Proposition 3** — centered absolute `k`th moments: `|µ̄^k_{T,j} − µ̄^k_{C,j}| ≤ ε_j^k (θ_j + 1)^k`.
- **Propositions 4 and 5** — quantiles: `|X^q_{m_T,j} − X^q_{m_C,j}| ≤ ε_j` for empirical quantiles
  under one-to-one matching, and the same bound for weighted quantiles when the support is cut into
  subintervals of exact length `ε_j`.

So the bound on the mean, on every centered moment, and on every quantile is a *function of the one
number the analyst chose*, with no assumption about the data at all. That is the whole content of
"monotonic imbalance bounding" in a usable form.

**How the coarsening is chosen** (criterion (iii)). Two routes, and the paper is explicit that it
prefers the first: (a) **substantively** — set `ε_j` to the largest imbalance in `X_j` that is
tolerable, treating it as an acceptable measurement error, which the authors report analysts have
"little trouble" doing; (b) **automatically** — standard automated histogram bin-width rules, with
more elaborate alternatives, shipped in their R and Stata packages. The paper does **not** claim a
single optimal coarsening exists, and it is worth noting that the automated route is the one it
describes least.

**Other MIB members, and how to compose one.** Nearest-neighbour matching *with a caliper*, and full
optimal matching, are MIB provided the tuning parameter is on the scale of the covariate and defined
for every `j`. Non-MIB methods applied **inside** CEM strata or inside variable-by-variable calipers
yield methods that are still MIB — e.g. coarsen with wide bins, apply CEM, then prune further within
each cell by propensity score or Mahalanobis distance. Note the converse, which is the paper's stated
reason for excluding full optimal matching from MIB in general: a method that works from **a scalar
imbalance metric** is not MIB.

**Two mechanics that matter at panel scale.** The cell space is `m^k` and so unusable directly (their
example: `k = 20` covariates at `m = 6` bins is `6²⁰ ≈ 3.7 × 10¹⁵` cells), but CEM produces **at most
`n` non-empty strata**, so the implementation never enumerates the space: represent each coarsened
observation as an integer feature vector, concatenate it into a key string, and tabulate.
**CEM is then `O(n)` — the complexity of a frequency tabulation** — and expressible as a SQL-style
group-by. Separately, a **nonparametric propensity-score estimate is free from a CEM solution**: the
proportion treated within each stratum. The authors expect it to balance better than a logit score,
which optimises fit rather than balance — though they note CEM does not need it, since the matches
are already determined.

**On strata that hold only treated units.** The curse of dimensionality is real — with independent
covariates in 20 dimensions, even two bins per variable leaves almost every cell without both a
treated and a control unit. Their answers: real data are far more correlated than independent draws,
so in practice CEM matches enough; the remedy for too many discarded treated units is to **relax the
chosen maximum imbalance**, i.e. coarsen more; and following Abadie–Imbens, the number of cells
holding only unmatched treated units goes to zero exponentially in `n_T` provided the control
reservoir grows at `n_C = O(n_T^{1/r})` with `r ≥ k` for `k` continuous covariates.

## Robustness evidence (qualitative only)

Peer-reviewed in the flagship journal of statistics, heavily cited (839, Crossref) for its age, and
the propositions are proved in the paper's appendix rather than asserted — the core claims are
theorems about an algorithm, not estimates from a sample, so there is nothing in them to decay.
Replication software for R and Stata accompanies the article, and the empirical section is an explicit
replication of a previously published study rather than a fresh analysis.

The Monte Carlo evidence is the part that is evidence rather than algebra, and its design is honest in
a way worth recording: the data are generated **to satisfy EPBR's own requirements**, which is the
setting most favourable to the comparison method, and the target is the population-level estimand
rather than the sample one, which the authors state also favours the comparison method. Six outcome
functions spanning constant, linear and several nonlinear treatment effects, 1000 replications,
coarsenings swept across 2–11 equal intervals. In that setting CEM has lower root-mean-square error
than logit-score nearest-neighbour matching in 59 of 60 experiments and ties in the last. A
five-covariate Gaussian case with propensity-score model selection is run as well.

Two limits on the evidence. First, the `L₁`-profile rank-invariance claim is an empirical regularity
across the datasets these authors happen to have analysed, offered with an instruction to check it
rather than a proof — and the mechanism by which it could fail (different bin definitions ranking
methods differently) is stated in the paper itself. Second, a broader data-collection exercise
supporting the practical-matchability claim is described as forthcoming work and is **not** in this
paper, so that claim rests on the authors' reported experience.

**Tension with `#435`, and it resolves rather than stands.** `notes/2026-11-11-the-psm-paradox-and-random-pruning.md`
(King–Nielsen, Tier B) establishes that pruning observations raises the variance of the comparison
being made, and that a design whose imbalance/pruning curve *rises* should be rejected. This paper —
same middle author — reports the opposite-looking result that CEM's RMSE **falls as it coarsens more
and drops more units**. The two are not in conflict, and the reconciliation is given in this paper's
own sentence: the variance of the estimate is a function of `n` **and of the heterogeneity of the
units being compared**, and matching in covariate space reduces the second while shrinking the first.
`#435`'s result is about pruning that is *uncorrelated with the comparison* — random pruning, which
buys no heterogeneity reduction and pays the `1/n` cost in full. So the two notes together say:
**pruning is justified exactly to the extent that it removes heterogeneity in covariate space, and
`#435`'s rising-curve test is the diagnostic that tells you whether it did.** This is also why `#435`
endorses the *shape* of a cell sort over nearest-neighbour matching on a scalar score; this paper
supplies the reason, in that a method reasoning from a scalar imbalance metric is excluded from MIB
by definition.

**A third claim that changes what a matched comparison is allowed to say.** In the replication, CEM
raised the point estimate of the effect by a substantial fraction *and* collapsed the spread of
estimates across alternative regression specifications — but the matched treated units are a visibly
narrower population than the full treated group, differing on several covariates. The authors are
explicit that this is **a different estimand** (a local rather than a population average effect over
the treated), reported as such and defended on the ground that an inference about the narrower group
is reliable where one about the whole group is not. Matching did not make the same number more
precise; it changed which number was being estimated.

## Implementability here

Nothing here is a strategy. It is the measurement layer under the lab's matched controls, and it
bears on them in four specific places. Note first the constraint that decides how much of it is
reachable: `#418` establishes that strong ignorability is unavailable on this panel by construction,
so **everything below is a balance diagnostic, not an effect estimate** — exactly the status
`#433`/`#434` are recorded with.

1. **`L̄₁` is computable here, cheaply, and the lab has no multivariate imbalance number at all.**
   Every matched control the lab has built (region matching, sector matching, the `recent_half`
   control, the `-vol126` control, the volatility-tercile conditioning of `#406`) is checked, when
   it is checked, one variable at a time against the thing being matched on. `L₁` needs only a
   cross-tabulation of the candidate's selected names against the control's selected names over a
   few coarsened covariates the panel already holds — trailing volatility, liquidity tier, region,
   price level, eligibility vintage — and it is a `groupby` plus an absolute difference of relative
   frequencies. The `O(n)` tabulation trick means panel width is not an obstacle. Rebalance-date
   handling is the one design question the paper does not answer for us: `L̄₁` is defined for one
   pair of groups, so a panel version is either per-date (a time series of imbalance) or pooled
   across dates, and the two answer different questions.

2. **The ex-ante/ex-post inversion is the actionable recommendation, and it reverses how this lab
   builds controls.** The lab's habit is to fix the control's size — typically to match the
   candidate's name count — and then look at how balanced it came out. MIB says fix the tolerance
   per covariate (how much trailing-volatility difference, how much liquidity-tier difference, is
   acceptable) and let the count fall out. Under the paper's propositions that choice then bounds
   the mean, the moments and the quantiles of every matched covariate, with no distributional
   assumption. A control whose count was fixed first carries no such bound.

3. **The propensity-score-weighting demonstration is a refusal test the lab can apply to its own
   screens immediately.** A control that equalises per-covariate *means* can leave the joint
   distribution untouched. Any lab control validated by "the means of the matched covariates agree"
   is therefore **unvalidated**, and the check that would settle it is `L̄₁` before versus after. This
   joins `#427`/`#429`'s matched-design refusals and is strictly cheaper than either.

4. **CEM is the construction to prefer, and its parameter is the one the lab is already implicitly
   choosing.** `#435` recommended subclassification over pruning and said nothing about the
   coarsening; the answer here is that the coarsening is the tolerance, chosen substantively. For
   this panel that is a readable question — how many trailing-volatility buckets, how many liquidity
   tiers, whether region is coarsened to developed/Asia or left at nine index memberships — and the
   bin count `θ_j = ⌈R_j/ε_j⌉` converts a tolerance into a bucket count directly. The `#406`
   volatility-tercile construction is already a one-covariate CEM with `θ = 3`; the propositions say
   what widening or narrowing that buys, and that adding a second coarsened covariate does not
   disturb the first's bound.

Four pitfalls, stated plainly.

- **The cell space grows as `m^k` and this panel's covariates are correlated but not that
  correlated.** The paper's own 20-dimensional example produces almost no matched cells. With
  roughly a thousand eligible names on a validation date, three or four coarsened covariates at three
  to five buckets each is the realistic ceiling; beyond that most cells hold one side only, and the
  honest response is to coarsen harder, not to add covariates.
- **A matched control changes the estimand, and the lab's gate does not know that.** The
  replication's matched set was a narrower population and the paper reports a *local* effect
  accordingly. A matched control built on this panel selects a subpopulation of names, so the
  difference it licenses is a statement about that subpopulation — which is the same caveat `#434`
  attaches to the population-versus-treated-cohort distinction, now arriving from the construction
  side rather than the inference side.
- **Bins must be held fixed across any comparison.** Comparing a candidate's `L̄₁` against a
  control's under different coarsenings is not a comparison. If the lab ever reports `L̄₁`, the bin
  set belongs in the record beside it.
- **The `L₁`-profile's rank-invariance is not guaranteed here.** It is an empirical regularity from
  non-financial datasets. A panel of returns is not those datasets, and the paper's own instruction
  is to check the profile rather than to assume it — which costs a sweep over random bin definitions,
  not a trial.

## Related

- `notes/2026-11-11-the-psm-paradox-and-random-pruning.md` (`#435`) — the source whose refusal test
  named this aim; the pruning/variance tension is reconciled above, and this note supplies the
  reason its recommended cell sort is preferred to a scalar-score match.
- `notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md` (`#433`) — the scalar
  score; this paper's CEM-strata proportion is the nonparametric alternative to fitting it, and its
  Section 3 names Cochran (1968) as the first formal analysis of any subclassification method.
- `notes/2026-11-11-matching-on-the-estimated-score-and-its-variance.md` (`#434`) — the
  estimated-score variance result; this paper attributes the same direction to Hirano–Imbens–Ridder
  and explains it as an in-sample versus expected-balance distinction.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` and
  `notes/2026-11-08-committee-discretion-versus-the-published-admission-rule.md` — the admission-rule
  cluster this methodology is about; see the annotation added this session.
- `experiments/learnings.md` — the lab's matched controls, including the case where a matched control
  inverted a positive reading and the refusal it corroborated.
