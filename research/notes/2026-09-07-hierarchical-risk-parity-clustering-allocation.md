---
title: "Building Diversified Portfolios that Outperform Out of Sample" (with Hierarchical Clustering-Based Asset Allocation; Schur Complementary Allocation; and Can Machine Learning-Based Portfolios Outperform Traditional Risk-Based Portfolios?)
authors: López de Prado; Raffinot; Cotton; Jain, Jain
year: 2016; 2017; 2024; 2019
venue: Journal of Portfolio Management 42(4), 59–69 (venue tier 1 by the rubric's list, practitioner-facing); Journal of Portfolio Management 44(2), 89–99 (tier 1 list); arXiv preprint (tier 4); Risks 7(3), 74 (peer-reviewed, minor venue — tier 3 in effect)
url: https://doi.org/10.3905/jpm.2016.42.4.059 (closed; algorithm read from the author's own reference implementation, https://www.quantresearch.org/HRP.py.txt, header dated 20151227) · https://doi.org/10.3905/jpm.2018.44.2.089 (closed, metadata only) · https://arxiv.org/abs/2411.05807 (read in full) · https://doi.org/10.3390/risks7030074 (read in full via EconStor, https://www.econstor.eu/bitstream/10419/257912/1/risks-07-00074.pdf)
citations: López de Prado 225 (Semantic Scholar DOI endpoint) / 292 (OpenAlex) / 222 (Crossref), checked 2026-09-07 — a three-way spread of the kind this folder now expects. Raffinot 110 (S2) / 111 (OpenAlex). Cotton 5 (S2, `arXiv:2411.05807`). Jain–Jain 30 (S2) / 36 (OpenAlex)
sample_period: López de Prado — **no historical sample; the out-of-sample evidence is a Monte Carlo experiment on generated data**. Cotton — simulation study, no historical sample. Jain–Jain — estimation November 2010 – December 2016, evaluation the following calendar year. Raffinot — not verified
markets: López de Prado and Cotton — synthetic. Jain–Jain — five 10-asset sub-universes drawn from the NIFTY 50 (India). Raffinot — not verified
tier: B
validation_overlap: false
published_post_2018: true
---

**Read in full**: Cotton's preprint (the Schur-complement construction, the HRP/MVO limits, the
simulation design) and Jain–Jain (covariance forecast models, the five universes, the superior
predictive ability test, the conclusions). **The HRP algorithm itself was read from López de
Prado's own published reference implementation**, which is complete and unambiguous; the JPM
article's prose is closed access and is not summarised here. Raffinot is metadata only.

This note exists because `program.md` names "hierarchical risk parity, clustering-based
allocation" as sub-mechanisms of `portfolio-learning`, and `research/README.md` has carried them
as a standing search area since 2026-08-29, while the folder had **zero** coverage of either.
The lab has since closed `portfolio-learning` three times — on the mean, max and intersection
operators — but all three are **signal-aggregation** operators over rank scores. HRP is a
different object: a **weighting** scheme over a correlation structure, with no signal in it at
all. The family's named sub-mechanism was therefore still open. This note closes it on the
literature, and the recommendation is not to spend a trial.

## Mechanism

The problem HRP is built for is real and is stated cleanly: a Markowitz optimizer must invert an
estimated covariance matrix, and the condition number of that matrix rises with the correlations
among the assets. So the more the assets co-move — precisely when diversification is most needed
— the more a small estimation error in `Σ` is amplified into a large, unstable swing in weights.
Constraining or shrinking helps; inverting a badly conditioned estimate of an object you only
observe with noise remains the weak point.

HRP's answer is to **not invert anything**. It replaces the flat "every asset against every other
asset" problem with a **hierarchy**: assets that co-move are grouped into a tree, and capital is
split top-down between groups rather than solved for jointly. The economic claim is that a
hierarchy is closer to how correlation structure actually arises (an asset competes for capital
with its close substitutes first, and only then with distant ones) and that a top-down split is
far more stable under estimation error than a joint solve.

**Cotton's result is the one that should govern how this lab reads HRP, and it is analytical
rather than empirical.** Within each bisection step, HRP consults the variances of the two
sub-clusters and *never consults the covariance block between them*. Restoring that block via
Schur complements — replacing each sub-covariance matrix by a version corrected for the
information in the off-diagonal block — produces a family of allocators that interpolates
continuously from HRP at one end to full minimum variance at the other. So:

> HRP is not a different objective from mean-variance. It is **approximate hierarchical variance
> minimisation with the cross-cluster covariances discarded**, and the discarding is the
> approximation.

That reframing matters because it says HRP's stability is bought by *throwing information away*,
which is a shrinkage argument — and this folder already holds a sharper version of the same
argument (see *Implementability*). It also says HRP has no separate economic mechanism to test:
there is no return prediction anywhere in it.

## Construction recipe

From the author's own reference implementation, which is short enough to state exactly:

1. **Correlation to distance.** `d[i,j] = sqrt((1 - corr[i,j]) / 2)`, a proper metric bounded in
   `[0,1]`.
2. **Tree clustering.** `scipy.cluster.hierarchy.linkage(d, 'single')` — **single linkage** in the
   reference code. (The paper's fuller version applies a second-order distance, the Euclidean
   distance between columns of the distance matrix, before linkage.)
3. **Quasi-diagonalisation.** Reorder the rows and columns of the covariance matrix into the
   dendrogram's leaf order, so similar assets sit adjacent and the largest covariances end up
   near the diagonal.
4. **Recursive bisection.** Start with the whole ordered list as one cluster. Repeatedly:
   - split each cluster **into two halves by count** — note this splits the *sorted list*, not
     the dendrogram's own cluster boundaries, which is the step Raffinot's later work replaces;
   - for each half, compute its cluster variance `V = w' Σ w`, where `w` is that half's
     **inverse-variance** portfolio;
   - set `alpha = 1 - V0 / (V0 + V1)`, multiply the first half's weights by `alpha` and the
     second's by `1 - alpha`;
   - recurse until every cluster is a single asset.

Structural properties, which are the reason it is attractive at all:

- **Long-only and fully invested by construction.** Every weight is a product of factors in
  `(0,1)` and the weights sum to one. No constraint machinery, no solver, no failure mode where
  the optimizer returns a short position.
- **No matrix inversion**, so it is well defined when the number of assets exceeds the number of
  observations.
- **No expected-return input at all.** It is a pure risk allocator; it cannot express a view.
- **Deterministic** given the input matrix.

## Robustness evidence (qualitative only)

This is where the source cluster earns its tier, and the honest reading is that **the evidence
for HRP is much weaker than its citation count suggests**.

- **The original paper's out-of-sample evidence is simulated, not historical.** The author's own
  reference implementation generates its data (`generateData(nObs, size0, size1, sigma1)`, a
  synthetic block-correlation structure) and runs the comparison on that. The benchmarks are the
  critical line algorithm and inverse-variance weighting. **1/N is not among them, and no
  historical price series is used**, in a paper titled "Building Diversified Portfolios that
  Outperform Out of Sample". A Monte Carlo experiment can establish that one estimator is more
  stable than another under an assumed data-generating process; it cannot establish that the
  more stable one earns more in a market.
- **Independent evaluation is mixed and, where it is negative, it is negative against the
  simplest benchmark.** Jain–Jain make the point that HRP, despite not inverting the covariance
  matrix, is still entirely a *function* of it, so any comparison must specify a covariance
  forecast model. Under a formal test for superior predictive ability, they find that **when
  covariance estimates are crude, inverse-volatility weighting is the most robust, with the
  hierarchical portfolios behind it**. Their design is honest (bootstrapped SPA test, three
  covariance models, three rebalance frequencies) and their sample is weak: five 10-asset
  sub-universes of a single national index, one market, and an evaluation window of one year.
  Treat it as a tier-C datapoint that happens to be carefully executed.
- **An unread pointer, recorded as a pointer and not as evidence.** Deković and Šimović,
  *Future Generation Computer Systems* 167 (2025), `10.1016/j.future.2025.107744`, is reported
  by secondary summaries to compare HRP against 1/N on S&P 500 constituents and to find 1/N ahead
  in every experimental setup. The article is closed access, OpenAlex reports no repository full
  text, and Crossref carries no abstract, so **the finding above is a search-engine paraphrase
  and nothing in this folder should be built on it.** It is recorded so a future session does not
  re-discover it and mistake it for a read source. It is also the only evaluation found with a
  multi-decade sample, and its sample reaches years inside this lab's validation window.
- **No cost or turnover accounting anywhere in the primary literature.** None of the sources read
  charges the turnover that a rolling dendrogram refit generates. Single linkage is the least
  stable of the standard linkages under small perturbations of the distance matrix (the chaining
  effect), so a rolling HRP refit produces a *moving* tree and therefore moving weights, at a cost
  nobody in this literature has measured.
- **Post-publication decay is not documented** for HRP either way, because there is no historical
  event study to decay. Note the rubric's usual replication anchors (Hou–Xue–Zhang,
  Jensen–Kelly–Pedersen) do not cover it at all: it is not an anomaly, it is an estimator.

## Implementability here

It is implementable — `scipy` is installed, the algorithm is ~40 lines, it is deterministic, and
it returns long-only weights that sum to one, so it clears the engine's contract without any
adaptation. **The reason not to build it is not feasibility. It is that this folder and this lab
already hold the results that decide the question.**

1. **The constraint set this engine imposes is already the shrinkage HRP is selling.**
   `2026-08-21-weight-constraints-as-covariance-shrinkage` (Jagannathan–Ma) establishes that a
   long-only constraint plus a position cap is *equivalent* to shrinking the covariance matrix.
   This repo has both — long-only, gross ≤ 1.0, 25% cap. The estimation-error problem HRP exists
   to solve is therefore already attenuated here by machinery the engine applies regardless of
   what a candidate does.
2. **The benchmark HRP has never been shown to beat is the one this lab actually uses.**
   `2026-08-17-naive-vs-optimized-weighting` (DeMiguel–Garlappi–Uppal) is the folder's standing
   result that 1/N is hard to beat out of sample; every book in this repo is equal-weight over a
   selected band. The primary HRP source never tested against 1/N, and the two evaluations that
   did are a one-year 10-asset study and an unread article.
3. **The lab has already measured HRP's core operation and it failed, twice.** HRP's recursive
   bisection is a **variance-based capital split between two sleeves**, applied recursively.
   `learnings.md` records that inverse-vol/risk-weighting between sleeves of unequal
   diversification systematically hands capital to the more-diversified, lower-return leg — twice
   measured — and that fixed-ratio blending beat every vol-based reweighting tried. Recursive
   bisection does not repair that; it repeats it at every node, and each split will push capital
   toward whichever branch happens to be the lower-variance one.
4. **The cluster structure inherits the session artifact.** If anyone wants the *clustering* half
   independently of the *allocation* half — a data-driven partition to replace the hand-made
   region and sector partitions this lab uses — note that a correlation dendrogram built on
   **daily** closes across 15 time zones will cluster substantially by **trading session**, which
   is the contamination the 2026-09-06 nightly measured at 4x the US-only benchmark. Build any
   such distance matrix on **weekly** returns, and check the resulting partition against the
   region labels before believing it carries anything else.
5. **Book size.** The champion holds roughly 45% of the universe via its six-tranche overlap;
   most other books here hold 20–30 names. Over a book that wide and that homogeneous, HRP's
   weights will sit close to equal weight, and the 25% cap will essentially never bind. The
   expected effect size is small before any of the objections above.

**Recommendation: do not spend a trial. Answer it free instead.** If a session wants this closed
with a measurement rather than an argument, the diagnostic is holdings-only, costs no returns and
reads no split beyond train: compute HRP weights over the seated champion's actual holdings on
train rebalance dates and report (a) the mean absolute deviation of HRP weights from equal weight,
(b) the incremental annual turnover a rolling HRP refit adds, and (c) the fraction of dates on
which the 25% cap binds. If (a) is a few percent — which points 1 and 5 predict — the sub-mechanism
is answered without a trial and `portfolio-learning` closes on its fourth operator for free.

## Related

- `2026-08-17-naive-vs-optimized-weighting` — the 1/N benchmark HRP's primary source never tested
  against.
- `2026-08-21-weight-constraints-as-covariance-shrinkage` — the reason this engine's constraint
  set already does HRP's job.
- `2026-08-18-risk-parity-equal-risk-contribution` and `2026-08-21-effective-number-of-bets-diversification-measurement`
  — the risk-budgeting family HRP belongs to, and the diversification metrics that would be the
  honest way to score it if it were built.
- `2026-08-31-signal-blending-vs-portfolio-blending` — the distinction this note turns on: the
  lab's three closures are signal-side operators, HRP is a portfolio-side one.
- `experiments/learnings.md` — the twice-measured inverse-vol/sleeve result that point 3 rests on,
  and the "blending beats switching" entry.
