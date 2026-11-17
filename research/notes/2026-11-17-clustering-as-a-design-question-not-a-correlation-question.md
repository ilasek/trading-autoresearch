---
title: "When Should You Adjust Standard Errors for Clustering?"
authors: Abadie, Athey, Imbens, Wooldridge
year: 2023
venue: The Quarterly Journal of Economics 138(1), 1–35 (venue tier 1 — top-five general economics journal)
url: https://doi.org/10.1093/qje/qjac038 — read in full from arXiv 1710.02926v4 (79 pages, 286 KB of text, 947 instances of `" the "`, `( )`-dropout check zero, no ASCII shift); the v4 date matches the published version
citations: 1577 (Crossref `is-referenced-by-count`, checked 2026-11-17)
sample_period: a 2000 US Decennial Census cross-section (2,632,838 individuals) plus simulations. No financial data; no part of the sample touches 2018–2023
markets: none
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

The adversarial source of the session, and it attacks the premise under which the lab would use
anything in the companion note. Its claim: **the level at which to cluster is determined by the
sampling process and the treatment-assignment mechanism, and not by the presence of
cluster-level components in the outcome.** Once the estimand is an average treatment effect for
the *finite population at hand* rather than a parameter of an infinite super-population, "the
presence of cluster-level unobserved components of the outcome variable becomes irrelevant for
the choice of clustering level."

The paper names three misconceptions, and the first two are the lab's.

**Misconception 1 — that clustering is needed when within-cluster residual correlation is
non-zero.** False in both directions: "the presence of such correlation does not imply the need
to use cluster adjustments, and the absence of such correlation does not imply that clustering is
not required." The counterexample is a sample mean. If the population partitions into clusters
and outcomes are positively correlated within them, the cluster variance exceeds the robust
variance — yet if units were sampled **at random from the population**, standard sampling theory
says no clustering is needed. The correlation is real and the adjustment is still wrong.

**Misconception 2 — that clustering is free when unnecessary, so if it changes the answer you
should do it.** False: "the harm in clustering in this case is that confidence intervals will be
unnecessarily conservative, possibly by a wide margin." In their own application, clustering at
the state level inflates the standard error by **23–26×** over the robust one. An inflation of
that size is not caution, it is an inability to conclude anything.

**Misconception 3 — that the choice is binary.** False: a *combination* of the robust and
cluster variance estimators beats both.

**The design component, which is what the conventional frameworks lack.** Two distinct reasons
to cluster, which the paper separates:

- **Clustered sampling.** Clusters, not units, were drawn from the population. The correction
  shrinks as the sampled fraction of population clusters rises, because less of the population
  is being extrapolated to.
- **Clustered assignment.** Treatment takes a common value for all units in a cluster. "Clustered
  assignment to treatment is equivalent to clustered sampling of potential outcomes", so
  clustering is required here *even when individual units are sampled at random*.

The sharpest operational consequence, and it is a refusal: **"the data are not informative about
the need to adjust for clustering in the sampling process, but they are informative about the
need to adjust for clustering in the assignment process."** No measurement settles the
sampling-side half. It is a design judgement that must be stated, not estimated.

The paper also shows that **heterogeneity in treatment effects introduces additional variance
components** that change the need for clustering — so a specification that implicitly assumes a
constant effect has pre-judged its own standard error.

## Construction recipe

**Where the two conventional estimators sit.** Against the design-plus-sampling variance, robust
standard errors are "generally too small" and cluster standard errors are "unnecessarily
conservative". The truth is between them, and both are available.

**Causal Cluster Variance (CCV).** The construction, in words, because the ingredients are what
matter:

1. The estimator's error is a sum over units of products of regression errors and regressor
   values. The **robust** variance sums the squares of those products over units; the
   **cluster** variance sums the squares of the *within-cluster sums* of the same products.
2. The cluster variance is biased because, although the sum over all clusters of the expected
   within-cluster sum is zero, each cluster's own expectation is not. For each sampled cluster,
   that expectation can be estimated.
3. CCV uses those estimates to debias the cluster variance, then blends by the sampled fraction
   of population clusters `q̂`:

> `V̂^CCV = q̂ · V̂^CCV(1) + (1 − q̂) · V̂^cluster`.

At `q̂ → 0` (a vanishing fraction of clusters sampled) CCV collapses to the conventional cluster
variance and buys nothing; at `q̂` large the correction is substantial. **CCV requires
within-cluster variation in treatment assignment** — it estimates cluster-level treatment
effects — and is designed for many observations per cluster.

**Two-Stage Cluster Bootstrap (TSCB).** The resampling counterpart, and it is *not* either
conventional bootstrap (units, or whole clusters). Two stages: (i) draw each cluster's **fraction
treated** from the empirical distribution of cluster-specific treated fractions; (ii) sample
treated and control units from the cluster, their counts set by stage (i).

**Their application, as magnitudes with no effect claim attached.** For an individual-level
treatment: robust 0.0012, cluster 0.0269 (**22×**), CCV 0.0035 (**2.9×** robust, and
**0.13×** cluster), TSCB 0.0036. With fixed effects the CCV and TSCB standard errors come out at
0.0014, "in between robust and cluster but much closer to robust." So the honest answer was
nearer the robust one than the clustered one, and far from both.

## Robustness evidence (qualitative only)

Central limit theorems and large-sample variances are derived for the least-squares and
fixed-effects estimators under the combined sampling-plus-assignment framework, with the robust
and cluster variances recovered as limit cases, so the comparison is analytic rather than
asserted. Simulation evidence across designs supports CCV and TSCB over both conventional
estimators; the paper reports a design in which the conventional cluster standard error is more
than seven times the estimator's actual normalized standard deviation. The framework builds on
the authors' earlier design-based regression work and nests clustered sampling and clustered
experimental assignment as special cases. Four referees are acknowledged; the empirical
illustration uses a public census extract.

The limitation to carry: the estimand is a **finite-population average treatment effect**.
Everything gentler about these standard errors flows from that choice, and a researcher who
genuinely wants a super-population parameter is not entitled to the smaller interval.

## Implementability here

**The lab's position under this framework is unusual and the paper's logic cuts both ways.** Two
of the lab's questions have different answers, and the lab has never distinguished them.

**(a) Balance and descriptive screens — the design-based reading applies, and it vindicates what
the folder already does.** When the lab asks "did this book's selected names differ from the
pool on `log P` and `vol126` *on this panel*", the population of interest **is** the panel: all
index members on all dates are observed, `q̂ = 1`, nothing is being extrapolated to an unobserved
super-population. There is no clustered *sampling*. The relevant variability is the
**assignment** — which names the book held — and that is exactly what the folder's existing
repair randomizes: `#439`/`#445`'s **within-date permutation of the hold/not-hold labels**. That
permutation is a randomization-inference calibration under a finite-population design, which is
to say it is this paper's framework rather than a patch on the i.i.d. one. **So the folder's
screens do not need a cluster-robust standard error at all; they need the permutation they
already have, and the conventional cluster SE would be the "unnecessarily conservative" choice
Misconception 2 warns about.** This is the session's most reassuring output and it should stop
the lab from reaching for a heavier instrument.

**(b) Forecast claims — the design-based reading does not apply, and the companion note's
correction stands.** When the lab asks "will this signal earn skill on data it has not seen", the
estimand is a parameter of a data-generating process that will produce future dates. The panel
is a *sample* from that process, the sampled fraction of relevant dates is effectively zero, and
clustering by date is required. Nothing in this paper softens that. The 2026-11-17 nightly's
board regression is in this category.

**The rule to adopt, stated in one line:** before quoting any standard error, say whether the
claim is **about this panel** (permutation, finite-population, no clustering) or **about the
process that will generate the next dates** (cluster or block-resample by date, and pay the
companion note's inflation factor). The lab currently writes both kinds of claim in the same
units with the same error bars.

**CCV and TSCB are mostly not usable here, and it is worth saying why rather than filing them as
available.** CCV needs within-cluster variation in treatment assignment — satisfied, since a
book holds some names and not others within a date — but its gain is proportional to `q̂`, the
sampled fraction of population clusters. For the balance screens `q̂ = 1` and the right
instrument is the permutation (a); for the forecast claims `q̂ ≈ 0` and CCV reduces to the
conventional cluster variance, buying nothing. So CCV is an estimator whose regime of usefulness
the lab sits outside on both sides. TSCB's first stage — resampling the fraction treated per
date — is, however, a *construction worth borrowing*: it is close to a null in which the book's
date-by-date position count is preserved and its name choices are not, which is a strictly
stronger null than permuting labels at a fixed count.

**The treatment-effect-heterogeneity point has a direct analogue.** A book's "effect" is not
constant across dates; the paper's result that heterogeneity adds variance components means that
any instrument assuming one constant per-date effect understates uncertainty. The folder's
regime-conditioning notes bear on the same thing from the other side.

**Pitfall.** Do not read this note as a licence to drop dependence corrections generally. It
narrows *when* clustering is the right tool; it does not claim the i.i.d. interval is correct. In
case (b) the i.i.d. interval remains wrong by the companion note's factor.

## Related

- `research/notes/2026-11-17-which-dependence-structure-licenses-which-standard-error.md` — the
  direct adversary, and the stated tension: Petersen's `ρ_X ρ_ε` bracket is a **decision rule**
  ("cluster iff both correlations are non-zero") that this paper says is not a decision rule at
  all, while conceding nothing about the **magnitude** when clustering *is* called for. The
  resolution carried in `SUMMARY.md` is that the two frameworks answer different questions and
  the lab must say which it is asking.
- `research/notes/2026-11-17-many-covariates-variance-estimation-and-its-independence-assumption.md`
  — `#458`, the estimator `#454` names and the dependence it excludes.
- `research/notes/2026-11-14-hotelling-t2-under-high-dimension.md` — `#445` and the within-date
  permutation, which this note reclassifies from "a patch for a broken asymptotic reference" to
  "the correct finite-population instrument".
- `research/notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — `#446`'s
  selection-space/return-space two-by-two; TSCB's first stage belongs on the selection-space side
  of it.
- `research/notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` — the
  folder's own selection-as-treatment framing, which this paper supplies the inference theory for.
