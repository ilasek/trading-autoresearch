---
title: "Detection of false investment strategies using unsupervised learning methods (the ONC algorithm for the effective number of trials)"
authors: López de Prado, Lewis
year: 2019 (Quantitative Finance); working-paper version dated November 2018
venue: Quantitative Finance 19(9), 1555–1565 (Tier 2 — peer-reviewed but a second-tier finance/quant journal, and the authors are practitioners writing about their own prior framework)
url: https://doi.org/10.1080/14697688.2019.1622311 ; working paper https://ssrn.com/abstract=3167017
citations: 26 (Semantic Scholar by DOI, checked 2026-09-16); 27 (Crossref, checked 2026-09-16)
sample_period: "None. The paper contains no market data of any kind — its only empirical section is a Monte Carlo study on synthetically generated block correlation matrices."
markets: none — synthetic data only
tier: "B. Peer-reviewed and squarely on this repo's problem, but: low citation count for its age, no independent replication, no market data, and the validation demonstrates only that the algorithm recovers clusters it was itself shown, never that the resulting error rate is correct."
validation_overlap: false
published_post_2018: true
---

**Read in full — but read in its working-paper form, and that matters.** `tandfonline.com` (the
published article) and `papers.ssrn.com` both returned HTTP 403 to an automated client; the text used
here is the SSRN working paper ("First version: April 4, 2018 / This version: November 1, 2018",
carrying the `ssrn.com/abstract=3167017` watermark on every page) served by a third-party mirror.
**The peer-reviewed Quantitative Finance version, published ten months later, was not read**, and
this note cannot say what the referees changed. The working paper does thank two anonymous referees,
so it is at least a post-review draft. Anything here that reads as precise — the algorithm, the
formulas — comes verbatim from that text; the tier reflects the version uncertainty.

## Mechanism

**The problem it names, and it is the lab's problem exactly.** The deflated Sharpe ratio needs two
inputs that are not properties of the strategy being tested but of the *research process* that found
it — the authors call them meta-research variables:

1. `E[K]` — the number of **effectively uncorrelated** trials;
2. `E[V[{SR_k}]]` — the **variance of the Sharpe ratios across those `K` trials**.

The second is easy to forget and the paper is emphatic that both are required. The deflator is

    SR* = √V[{SR_k}] · ( (1−γ)·Z⁻¹[1 − 1/K]  +  γ·Z⁻¹[1 − 1/(K·e)] )

with `γ` the Euler–Mascheroni constant, and the reported statistic is `PSR[SR*]` — the probabilistic
Sharpe ratio evaluated at that benchmark, which folds in the track length `T`, the skewness and the
kurtosis of the selected strategy's returns. `SR*` rises with `K` **and** with the dispersion of the
trials' Sharpes. **A search that produced widely-varying Sharpe ratios is penalised more than one
that produced tightly-clustered ones, at the same `K`.**

**Why clustering rather than a correlation threshold or an average correlation.** Their objection to
the constant-average-correlation route (Harvey–Liu's Šidák-based correction) is structural and is the
paper's best paragraph: *"A family of backtests often contains heterogeneous strategies. Trials that
belong to the same strategy tend to be highly correlated among themselves, while trials that belong
to different strategies tend to exhibit a lower correlation. This clustering of trials around
heterogeneous strategies leads to a hierarchical structure, which can be highly irregular and
complex."* A single average correlation cannot represent that; nor, by the same argument, can a
single threshold. The proposed fix is to **partition the trials and count the partitions**.

**The three claimed differences from the Harvey–Liu vein**, stated fairly because they are also the
places the two literatures disagree: no normality assumption on returns (skewness and kurtosis enter
through the PSR); extreme-value rather than Šidák machinery; and no constant-correlation assumption.
The authors describe the two approaches as complementary rather than rival, and say their `E[K]`
estimator is usable inside either.

**Type I over Type II, deliberately.** The paper argues for familywise error control rather than FDR
in finance, on the grounds that investors are shown only the single best strategy out of a family —
"in finance there is actually a single car unit produced per model, which everyone will use" — so
controlling an *error rate* across discoveries is beside the point when only one discovery is ever
deployed. **That argument transfers to this repo directly**: one champion is seated, not a portfolio
of everything that passed.

## Construction recipe

**ONC (Optimal Number of Clusters), in full.** Inputs: the `N × N` correlation matrix `ρ` of the
trials' return series.

1. **Correlation → proper metric.** `D_ij = √(½(1 − ρ_ij))`. This satisfies the metric axioms
   (non-negativity, identity, symmetry, sub-additivity); a raw correlation does not.
2. **Metric → distance of distances.** `D̃_ij = √(Σ_k (D_ik − D_jk)²)`, the Euclidean distance between
   rows of `D`. The stated reason: `D_ij` depends on one correlation, while `D̃_ij` incorporates
   the whole system, which reduces noise. **Cluster on `D̃`, not on `D`.**
3. **Base clustering.** Double loop: for each of `n_init` random initialisations, and for each
   `k = 2 … N−1`, run k-means on `D̃`; score the partition by
   `q = mean(silhouette) / std(silhouette)` — the **t-statistic of the silhouette scores**, not the
   mean silhouette. Keep the `(k, initialisation)` pair with the highest `q`. This simultaneously
   fixes k-means' two weaknesses: `k` is chosen by an objective rather than by the user, and the
   random initialisation is searched over rather than accepted.
4. **Top-level refinement.** Compute the same quality score `q_k` for each individual cluster in the
   winning partition. Take the clusters scoring below the average `q̄`; call their number `K_1`. If
   `K_1 ≤ 2`, return the base partition. Otherwise re-run step 3 **recursively on `ρ` restricted to
   the members of those `K_1` clusters**, and keep the re-clustering only if the average quality of
   those clusters improves. Concatenate accepted clusters with the re-done ones.
5. `E[K]` is the number of clusters returned.

**Then the second meta-research variable, which is where most of the bookkeeping is.**

6. For each cluster `k`, aggregate its members into one series with **minimum-variance weights**
   `w_k = Σ_k⁻¹·1 / (1'·Σ_k⁻¹·1)` on the within-cluster covariance, giving `S_{k,t} = Σ_i w_{k,i} r_{i,t}`.
   The stated reason for minimum variance rather than equal weight is to stop a single high-variance
   member from dominating its cluster's series.
7. Annualise each cluster's Sharpe: `Years_k = (last date − first date)/365.25`,
   `Frequency_k = T_k / Years_k`, `aSR_k = SR_k · √Frequency_k`. Trials with different rebalance
   cadences are otherwise not comparable.
8. `E[V[{SR_k}]] = V[{aSR_k}] / Frequency_k*`, where `Frequency_k*` is the **selected strategy's**
   frequency — so that `SR*` lands in the same units as the `SR̂` the DSR compares it against.

**The two uses the authors claim for `E[K]`**, and they are different formulas: inside the False
Strategy theorem for `E[max SR]` (above), or as the exponent in a Šidák correction to get a FWER.
The same estimate feeds both.

## Robustness evidence (qualitative only)

**This section is short because the evidence is thin, and that is the single most important thing to
carry from this note.**

- **The validation is synthetic and circular in a specific way.** The Monte Carlo builds correlation
  matrices with `K` planted blocks — `N ∈ {20, 40, 80, 160}`, minimum block size 2, `K` from 3 up to
  `N/2`, 1,000 replications per parameter set — and reports the ratio of recovered `K` to planted
  `K`, which clusters near 1 with outliers. **That establishes that ONC recovers block structure it
  was given. It does not establish that the number of clusters in a real family of backtests is the
  number of independent tests**, and it never checks a realised false-positive rate. No permutation
  benchmark, no FWER calculation, nothing of the kind the genomics literature routinely runs against
  its own effective-count estimators.
- **No market data appears anywhere in the paper**, so there is no cost treatment, no sample period,
  no cross-market evidence and nothing to decay. (This is also why it is entirely safe against this
  folder's embargo.)
- **No independent replication.** 26–27 citations for a 2019 article is low, and this folder found no
  third-party study testing ONC's error control.
- **The block-generating process is favourable to the method.** Blocks are built by copying one
  Gaussian series within a block and adding independent noise, i.e. exact one-factor blocks with a
  tunable within-block correlation. Real trial families are not block-diagonal: the 2026-09-15
  nightly found this repo's own 90 series carry a single component at ~79% of variance *across* all
  of them, which is a structure ONC's simulation never presents.
- **The paper is honest about what the variables are** — it says plainly that `E[K]` and
  `E[V[{SR_k}]]` are usually unknown because researchers "hide, not track, not report or underreport"
  their trial counts, and that even a scrupulous researcher faces the dependence problem. That
  framing is right and is why this repo's `trials.jsonl` is unusual and valuable.

## Implementability here

**Implementable tonight, cheaply, and with one finding available for free — but it is a plug-in and
inherits the critique in the companion notes.**

- **Everything needed is stored and scikit-learn is installed.** `N ≈ 90` validation return series;
  ONC is `KMeans` plus `silhouette_samples` over `k = 2 … N−1` with a handful of initialisations, on
  a 90×90 matrix. Seconds. No trial is consumed, no candidate file is written, no holdout is read.
- **The direct comparison is the point.** The engine obtains its trial count by single-linkage
  clustering at `ρ ≥ 0.95` (per the 2026-09-15 journal entry; `engine/` is frozen and was not read).
  That is a *threshold* rule; ONC is an *objective* rule that chooses its own `k`. The 2026-09-15
  entry already established that single linkage reads 90 clusters on a one-factor null at pairwise
  0.80 — a documented failure of the threshold rule on synthetic data the lab generated itself.
  **Running ONC on the same matrix, and on the same one-factor null, is the like-for-like control**,
  and it can fail: if ONC also returns ~`N` on the null, the clustering route is no better than the
  threshold and the finding is a closure.
- **The free finding, and this is the highest-value item in the note.** The DSR needs *both* `K` and
  `V[{SR_k}]`, and the paper is explicit that the variance must be computed **across cluster-level
  series** — min-variance aggregates, annualised — not across the raw trials. If the repo's deflator
  clusters to get `K` but takes the Sharpe dispersion across all 90 raw trial Sharpes, the two inputs
  are computed on different populations and `SR*` is internally inconsistent. **This is checkable
  from the journal and the engine's own read-only functions without editing anything**, it costs
  nothing, and both answers are findings. Whoever checks it should note that the inconsistency, if
  present, moves `SR*` in a direction that depends on whether within-cluster dispersion exceeds
  between-cluster dispersion, which is itself worth reporting.
- **The frequency bookkeeping in steps 7–8 is not decoration.** This repo mixes monthly-rebalanced
  and higher-cadence books. Comparing their Sharpes without the `√Frequency` adjustment, or reporting
  `V[{SR_k}]` in units other than the candidate's own, biases `SR*` by a factor nobody would see.
- **What this does not settle.** ONC produces another number to put beside the engine's 24, the
  participation ratio's 1.56 and the eigenvalue family's spread. **It has no more claim to being the
  effective number of tests than they do** — it is the same plug-in structure, validated against
  planted clusters rather than against a realised error rate, which is exactly the gap
  `2026-09-16-does-meff-control-the-familywise-error-rate.md` documents in the older and much better
  studied literature. Adding a fourth estimator widens the spread; it does not resolve it.

**Pitfalls.**

- **k-means is not deterministic.** The algorithm searches over initialisations by design, so a
  reported `E[K]` must come with a fixed seed and the `n_init` used, or it is not reproducible. The
  repo's own causality check compares holdings at `1e-6` for exactly this reason.
- **The published snippets are Python 2** (`xrange`, `dict.values()` arithmetic, a deprecated
  `KMeans(n_jobs=...)`). Anyone porting them is rewriting, not copying, and should say so.
- **`D̃` is a distance of distances.** Clustering `D` instead is a different algorithm and will give a
  different `K`; the substitution is easy to make by accident.
- **Do not let a large `E[K]` be read as licence and do not let a small one be read as a reason to
  relax a bar.** Both directions are argued in the companion notes and in the 2026-09-15 journal
  entry; nothing in this paper changes them.

## Related

- `2026-09-16-does-meff-control-the-familywise-error-rate.md` — **the critique this method inherits**,
  from a literature that has been testing effective-count plug-ins against realised error rates for
  twenty years and never certified one.
- `2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` — the eigenvalue
  alternatives to clustering; ONC is the same quantity by a different route.
- `2026-08-24-deflated-sharpe-ratio.md` — the formula this paper supplies the inputs for, and the
  note whose `N` this whole session is about.
- `2026-08-24-multiple-testing-haircut.md` — the Harvey–Liu constant-average-correlation route this
  paper argues against by name, and which it nonetheless calls complementary.
- `2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — the same author's clustering
  machinery applied to *allocation* rather than to counting trials; the correlation-to-metric step
  (`√(½(1−ρ))`) is shared, the linkage choice is not.
- `2026-09-15-reality-check-max-statistic-under-dependence.md` — the resampling route, and the one
  that does not need an effective count at all.
