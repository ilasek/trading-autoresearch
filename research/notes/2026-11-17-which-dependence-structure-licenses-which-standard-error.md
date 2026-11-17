---
title: "Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches"
authors: Petersen
year: 2009
venue: The Review of Financial Studies 22(1), 435–480 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhn053 — the typeset RFS article read in full from a university course mirror, https://u.osu.edu/schroeder.9/files/2020/03/PetersenRFS2009clusteringfixedeffectspaneldata.pdf (537 KB; `pdftotext -layout` → 173 KB of text, 1,457 instances of `" the "`, `( )`-dropout check zero). NBER w11280 is the working-paper version
citations: 9873 (Crossref `is-referenced-by-count`, checked 2026-11-17)
sample_period: simulations throughout (5,000 replications per design); two empirical illustrations use annual Compustat data 1965–2003 and an event-study panel. No part of the sample touches 2018–2023
markets: US equities (illustrations only); the results used here are simulation and algebra
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source the folder's open question asked for by description: **a rule for which
dependence structure licenses which variance estimator**, with the price of getting it wrong in
each direction. Three pieces.

**1. The bias in the i.i.d. standard error is a PRODUCT, and it has a closed form.** For a panel
with a cluster effect (the paper's "firm effect": dependence *within* a unit *across time*), the
true variance of the OLS slope is

> `Var(β̂) = σ²_ε / (σ²_X · n) × [1 + (m − 1) ρ_X ρ_ε]`

where `m` is the cluster size, `ρ_X` is the within-cluster correlation of the **regressor** and
`ρ_ε` the within-cluster correlation of the **residual**. The term in brackets is the entire
discrepancy: the conventional standard error estimates the first factor and silently sets the
bracket to 1.

The consequences are sharper than the usual folklore:

- **The bias is zero if *either* correlation is zero.** Residuals may be arbitrarily strongly
  correlated within a cluster and the i.i.d. standard error is still unbiased, provided the
  regressor is independent across observations. This is a *testable, free* screen, and it
  contradicts the common reflex of clustering whenever residuals look correlated.
- **The bias grows in the cluster size**, not in the sample size. Intuition the paper gives: at
  `ρ_X = ρ_ε = 1` each extra period carries no new information, but the i.i.d. formula credits it
  with `n` fresh observations and shrinks the standard error accordingly.
- Magnitudes from the simulations: with half the variance of both the regressor and the residual
  coming from the cluster effect, the i.i.d. standard error is **0.557 of the truth**, and
  **15.3%** of nominal-1% `t`-statistics clear 2.58.

**2. The cross-sectional case is the same algebra with the indices swapped, and it is worse.**
For a "time effect" — observations on *different units within the same date* correlated, which is
exactly this lab's structure — "the equations derived above are essentially unchanged… once `N`
and `T` are exchanged." So the cluster size in the bracket becomes the **number of names in a
date**. In the paper's own simulation, with half the variance from the time effect the true
standard error is **10.7×** the i.i.d. estimate and **81%** of nominal-1% `t`-statistics clear
2.58.

**3. Cluster-robust standard errors are biased DOWNWARD when clusters are few, and the bias is
tabulated.** The cluster-robust estimator is consistent in the **number of clusters**, not the
number of observations. Holding total sample size fixed and varying the number of clusters, with
`ρ_X = ρ_ε = 0.25`:

| clusters | downward bias of the cluster-robust SE |
|---|---|
| 5 | 27% |
| 40 | 3% |
| 100 | 1% |

The paper's verdict: "ten clusters is too small and five hundred is sufficient." The standard
deviation of the standard-error estimate falls with cluster count too, so MSE improves for two
reasons at once.

## Construction recipe

**The mapping, as the paper's conclusion states it.**

| dependence present | estimators that are BIASED | estimators that are UNBIASED |
|---|---|---|
| unit effect (within-unit, across time) | OLS, White, panel Newey–West, Fama–MacBeth, Fama–MacBeth with an AR(1) correction | clustered by unit (permanent *or* temporary effect); fixed/random effects **only if the effect is permanent** |
| time effect (within-date, across units) | OLS, White | Fama–MacBeth (it was designed for this); clustered by time, **but only with enough clusters** |
| both | any single-dimension correction | handle one parametrically (e.g. time dummies) and cluster on the other; or cluster on both dimensions, given enough clusters in each |

Two riders. Time **dummies** remove a time effect only if it is *fixed*; a non-fixed time effect
survives them. And the cluster-robust estimator assumes the within-cluster sum of `Xᵢₜ εᵢₜ` is
identically distributed across clusters, though the dependence **inside** a cluster may take any
form with no parametric structure assumed.

**The free diagnostic.** Because each estimator is biased in a known direction under a known
structure, comparing them *identifies the structure*:

- SEs clustered by unit much larger (3–4×) than White → a unit effect is present.
- SEs clustered by time much larger (2–4×) than White → a time effect is present.
- SEs clustered by both much larger than either single dimension → both are present.

The paper frames this as model diagnosis, not just inference repair: a biased i.i.d. standard
error means "there is information in the residual that the researcher is not using."

## Robustness evidence (qualitative only)

The core results are algebra plus 5,000-replication Monte Carlo across a grid of `ρ_X`, `ρ_ε`,
cluster counts and cluster sizes, with permanent and temporary cluster effects treated
separately — so the findings are design-robust in the way a simulation study can be. The
citation count (nearly ten thousand) and the paper's role as the standard reference in empirical
finance are the replication evidence; the algebra has been re-derived many times since. The
paper's own literature survey is part of its contribution: it documents that published work had
frequently used estimators its own table marks as biased, which is a methodology-honesty signal
rather than an effect claim.

The one limitation to carry: everything here is **model-based** — it presumes a data-generating
process with cluster components and asks for the standard error of a coefficient of that process.
The companion note records a framework under which that is the wrong question, and the two
disagree. See **Related**.

## Implementability here

**This note's screen is free, has never been run, and prices every cross-sectional association
the folder has recommended.** The lab's panel has `m ≈ 1,000` eligible names on a typical date,
and `#448`'s screen, `#453`'s audit and the mandatory rank-space residualisation are all
cross-sectional associations computed at a date. Putting the lab's own cluster size into the
bracket:

| `ρ_X · ρ_ε` (within-date) | true SE ÷ i.i.d. SE at `m = 1000` |
|---|---|
| 0.001 | 1.41× |
| 0.005 | 2.45× |
| 0.01 | 3.32× |
| 0.05 | 7.14× |
| 0.25 | 15.8× |

So a within-date correlation product of **one percent** already makes every i.i.d. interval the
folder quotes too narrow by a factor of three. Daily equity returns in one date are correlated
far above that, and the score side is too (a momentum or volatility rank is heavily
market-driven). The screen itself is two correlations and one multiplication, and it returns the
factor — **compute `ρ_X` and `ρ_ε` within date and report the bracket next to any
cross-sectional standard error**, or do not report the standard error.

**What it says about the 2026-11-17 nightly's own headline, and the news is good.** That session
regressed `null_p50 − pool` on the replicas' cost bill over the **27 v3 trials** and reported a
slope of `+1.249 ± 0.149` against a mechanically predicted `+1.0`, `t = +1.67`. The 27 rows are
not independent — the same session's board audit put them at **7–12 independent bets**. Treating
the effective count as the cluster count, the standard error should be inflated by
`√(27/12) = 1.50` to `√(27/7) = 1.96`, giving `±0.22` to `±0.29` and

> `t = 0.85` to `1.11` against the predicted `+1.0`.

The deviation from the mechanical prediction is **not** significant once dependence is charged —
which *strengthens* that session's reading (it predicted 1.0 and the data cannot reject 1.0)
rather than weakening it. Worth recording as a case where the dependence correction is on the
lab's side; `R² = 73.9%` is a descriptive fit and is unaffected either way.

**And it says the board cannot be clustered.** At 7–12 effective clusters the lab is inside the
"ten is too small" regime, where the cluster-robust estimator is itself biased **down** by the
order of 10–27%. So for board-level regressions there is no estimator in this paper that works:
the i.i.d. one is too narrow and the clustered one is too narrow as well, just less so. The
honest instrument there is the folder's existing **block resampling of dates** (`#389`'s
annotation) or a permutation, read as a shape rather than as a `p`-value — not a corrected
standard error.

**Fama–MacBeth is cheap here and is the right default for date-clustered questions.** The lab
already computes per-date cross-sectional quantities; the Fama–MacBeth standard error is the
standard deviation of the per-date estimates over dates, and under a pure time effect it is
unbiased where clustering by time is not (because the lab has many dates, this reverses the
paper's own caution about too-few clusters — the lab has thousands of dates and ~1,000 names, so
**clustering by date is the well-populated dimension and clustering by name is the sparse one**,
the opposite of the corporate-finance panel the paper is written about). Note the paper's own
caveat that Fama–MacBeth is biased in the presence of a *unit* effect, which on this panel means
persistence in a name's own score and residual across dates — present, and the reason to prefer
clustering by date with time-demeaning over Fama–MacBeth alone when both matter.

**Pitfalls.** (i) The "fixed effects fix it" route works only for a *permanent* effect; a
slowly-decaying one is not removed by dummies. (ii) The mapping table is about *bias in the
standard error*, not about the coefficient — none of this changes a point estimate. (iii) None
of it licenses reading a `p`-value; see the companion note for why the lab's question may not
be the one this framework answers at all.

## Related

- `research/notes/2026-11-17-clustering-as-a-design-question-not-a-correlation-question.md` —
  the direct adversary. It argues that within-cluster correlation neither implies nor is implied
  by the need to cluster, which contradicts the screen above *as a decision rule* while leaving
  it intact as a *magnitude*. The tension is stated there and in `SUMMARY.md`.
- `research/notes/2026-11-17-many-covariates-variance-estimation-and-its-independence-assumption.md`
  — `#458`: the estimator `#454` names excludes exactly the dependence this note prices.
- `research/notes/2026-11-14-two-sample-location-test-without-a-dimension-condition.md` and
  `research/notes/2026-11-14-hotelling-t2-under-high-dimension.md` — `#445`, the same i.i.d.
  problem on the two-sample side, with the within-date permutation as its repair.
- `research/notes/2026-11-04-out-of-sample-prediction-failure-and-the-cumulative-sse-diagnostic.md`
  — `#389`, whose block-resampling annotation is the instrument this note points board-level
  regressions back to.
- `research/notes/2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` — the same
  "rows in one date are not independent" objection, there against cross-validation folds.
