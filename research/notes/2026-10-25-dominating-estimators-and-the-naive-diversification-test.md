---
title: "Dominating estimators for minimum-variance portfolios — a James–Stein shrinkage toward any reference portfolio with a closed-form intensity that estimates ONE scalar, and an exact F-test for 'should I just hold equal weight?'"
authors: Frahm, Memmel
year: 2010 (working-paper version read: Cologne Discussion Papers in Statistics and Econometrics 2/08, 2nd version, 6 November 2008)
venue: "Journal of Econometrics 159(2), 289–302 (venue tier 1 — top-five econometrics journal). Working paper: Discussion Papers in Statistics and Econometrics 2/08, Seminar of Economic and Social Statistics, University of Cologne."
url: "https://doi.org/10.1016/j.jeconom.2010.07.007 ; working paper read at https://wisostat.uni-koeln.de/fileadmin/sites/statistik/pdf_publikationen_DP/DP0208.pdf"
citations: "113 (Crossref `is-referenced-by-count` for the published DOI, checked 2026-10-25). The SSRN preprint records (10.2139/ssrn.1272969, 10.2139/ssrn.2794024) each carry 1, which is the usual preprint-record artefact and not a second count."
sample_period: "None. Theory plus Monte-Carlo simulation under assumed normal i.i.d. returns. The paper contains no market data at all — its own conclusion names 'an empirical investigation of the presented shrinkage estimators' as future work. Nothing in it can touch any evaluation window."
markets: "Not applicable (theory + simulation). The simulations are parameterised by the number of observations `n`, the number of assets `d`, and the relative loss `τ_N` of the reference portfolio."
tier: "A−. Tier-1 venue, 113 citations, exact finite-sample dominance proofs valid for every `n ≥ d+2`, `d ≥ 4`, plus large-sample results under both fixed-`d` and `n/d → q` régimes, and an explicitly stated hypothesis test with its exact distribution. Marked down a half-step from A on two honest limitations the authors state themselves: everything assumes serially independent, identically normally distributed returns (they note in the introduction that real returns show structural breaks, higher-moment serial correlation and heavy tails), and the paper contains no empirical study. The working-paper version was read, not the typeset article."
validation_overlap: false
published_post_2018: false
read: "In full, the Cologne working paper (DP 2/08, 2nd version) — 332 KB PDF, 35 pages, `pdftotext -layout` into 94 KB of clean text, 539 instances of `\" the \"`, zero `( )` dropout. Sections 1–5, Table 1, Table 2 and the statements of Theorems 1–9 read closely; the appendix lemmas (Judge–Bock / Wishart algebra) were followed structurally, not re-derived. The typeset *Journal of Econometrics* article was NOT obtained (Elsevier, closed). The published title differs from the working paper's ('Dominating estimators for minimum-variance portfolios' vs 'Dominating Estimators for the Global Minimum Variance Portfolio'), so theorem numbering may differ between the two; numbers quoted here are the working paper's."
access_note: "`wisostat.uni-koeln.de/fileadmin/sites/statistik/pdf_publikationen_DP/DP<NN><YY>.pdf` is a flat department working-paper directory and served the file on the first try — the 2026-10-16 'university department working-paper directory' lesson confirmed on a German statistics seminar. It was found as a side-effect of a web search for a *different* paper (Kempf–Memmel), which is worth recording as a pattern: a department's own DP series surfaces in searches for its other members' work."
anti_lookahead_note: "No data, no dates after publication, no performance figures. Table 2's critical relative losses are properties of the estimator's sampling distribution as a function of `(n, d)` under simulated normal returns — not measurements on any market or period — and are quoted as such."
---

## Mechanism

Kempf–Memmel proved the plug-in minimum-variance weight estimator is the best **unbiased** one
(`notes/2026-10-25-gmv-weights-as-regression-coefficients.md`, Proposition 6), and Okhrin–Schmid
proved that de-biasing a mean-using weight estimator strictly *raises* its MSE
(`notes/2026-10-25-exact-distributions-of-estimated-portfolio-weights.md`). Both point the same way:
improvement has to come from accepting bias. This paper is that step, done exactly.

**The loss function is the right one.** Not weight error in the abstract, but
`L_{w,Σ}(v̂) = (v̂ − w)ᵀΣ(v̂ − w)`, which by Kempf–Memmel's Proposition 4 is precisely the *extra
out-of-sample variance* the book pays for having estimated its weights. Dominance in this loss is
dominance in realised risk.

**The estimator.** Let `ŵ_T` be the plug-in (traditional) GMV estimator and `w_R` any reference
portfolio with `1ᵀw_R = 1`. Define the **relative loss of the reference portfolio**

```
τ_R  =  (σ²_R − σ²) / σ²                 (how much more variance w_R has than the true GMVP)
τ̂_R  =  (σ̂²_R − σ̂²_T) / σ̂²_T             (its sample counterpart, from the sample covariance)
```

Then (Theorem 2) the shrinkage estimator

```
ŵ_S  =  κ_S · w_R  +  (1 − κ_S) · ŵ_T ,          κ_S = ((d − 3)/(n − d + 2)) · (1/τ̂_R)
```

**dominates** `ŵ_T` in that loss — `E[L(ŵ_S)] < E[L(ŵ_T)]` — for **every** `n ≥ d + 2` and `d ≥ 4`.
Not asymptotically, not on average over a prior: a strict finite-sample inequality. A modified
version `ŵ_M` (clipping `κ` at 1, in effect) dominates both `ŵ_T` and `ŵ_S` (Theorem 4).

**What is being estimated is one scalar.** `κ_S` has `d` and `n` in closed form and a single
data-dependent quantity, `τ̂_R` — the ratio of two portfolio variances. Nothing is inverted that was
not already inverted to get `ŵ_T`, and no new `d`-dimensional object is estimated. Contrast with the
usual shrinkage-toward-a-target proposals, which need a target covariance matrix.

**The relative loss is the sufficient statistic, and the whole problem is three numbers.** Theorem 3
shows the distribution of `ŵ_S`'s relative loss `τ_S` depends on `n`, `d` and `τ_R` **only** — not on
`Σ`'s shape, not on `d`'s composition. `E[τ_S]` is strictly increasing in `τ_R`, with infimum at
`τ_R = 0`, which happens if and only if `w_R` is the true GMVP. So: the better the reference
portfolio, the better the shrunk estimator, and how much better is computable.

**The naive-diversification test — the part this lab can use directly.** Take `w_R = w_N = 1/d`, the
equal-weight portfolio. There is a **critical** relative loss `τ*_N`: the point at which the shrinkage
estimator and equal weight have the same expected relative loss. Below it, hold equal weight; above
it, estimate. And `τ_N` is unobservable, so you test it (Theorem 9):

```
τ̂_R  ~  ((d − 1)/(n − d)) · F_{d−1, n−d}( τ_R · χ²_{n−1}/2 )          (conditionally noncentral F)

H0 : τ_N ≤ τ*_N        vs.        H1 : τ_N > τ*_N
```

reject `H0` when `τ̂_N` exceeds the upper `α`-quantile of that law at `τ_R = τ*_N`. **The null is
"equal weight is good enough", so the burden of proof falls on the optimiser** — the authors say they
formulated it that way deliberately.

**The critical values are brutal, and that is the finding.** Their Table 2 (critical `τ*_N`, with the
5% rejection threshold for `τ̂_N` in parentheses), from simulation under normal i.i.d. returns:

```
  n \ d       5           10            25            50          100
   12      52% (550%)  847% (99261%)     —             —            —
   24      16% (111%)   40% (334%)       —             —            —
   36       9% (59%)    19% (132%)   152% (1809%)      —            —
   60       5% (30%)     9% (58%)     28% (209%)   420% (7806%)     —
  120       2% (13%)     4% (24%)      8% (57%)     21% (161%)   377% (5202%)
```

Read the `d = 50, n = 120` cell: the shrinkage estimator beats equal weight only if the *true*
equal-weight portfolio carries 21% more variance than the true GMVP — and to **demonstrate** that
statistically you need a *measured* `τ̂_N` above **161%**, because `τ̂_N`'s distribution is severely
right-skewed. The dashes are cells with `n ≤ d`, where no finite value exists. The last column says
that at `d = 100` with ten years of monthly data, equal weight wins unless the true GMVP has less
than a fifth of its variance.

**Two structural corollaries.**

- **Theorem 8 — this is covariance shrinkage in disguise.** For any `w_R` there exists a
  positive-definite `Σ_R` with `w_R ∝ Σ_R⁻¹1` and `1ᵀΣ_R⁻¹1 = 1ᵀΣ̂⁻¹1`, and then
  `Σ̂_S⁻¹ = κ_S Σ_R⁻¹ + (1 − κ_S) Σ̂⁻¹` reproduces `ŵ_S` exactly. Shrinking the *weights* toward a
  reference portfolio **is** shrinking the *precision matrix* toward that portfolio's implied
  precision matrix. The authors draw the parallel to Jagannathan–Ma's result that a short-sale
  constraint is equivalent to a covariance transformation.
- **Theorem 7 and Table 1 — what happens as the panel widens.** Under `n, d → ∞` with `n/d → q`
  (the *effective sample size*), the plug-in estimator's relative loss converges to `1/(q − 1) > 0`:
  it never becomes consistent. The shrinkage estimators converge to `L(τ_R, q) < 1/(q − 1)`, so they
  dominate asymptotically too, and they dominate the reference portfolio itself uniformly once
  `q ≥ 2`. But as `q → 1⁺` they become uniformly **worse** than the reference portfolio — the
  threshold being `τ_R < (1/q)·(2 − q)/(q − 1)`. **At `q` near 1, hold the reference portfolio and do
  not estimate anything.**

## Construction recipe

1. **Fix a reference portfolio `w_R`.** For this lab the natural choice is the equal-weight eligible
   pool, because that is what skill is graded against. Any fixed, non-data-dependent `1ᵀw_R = 1`
   vector works; the theorems do not require it to be uniform.
2. **Compute `q = n/d` first.** If `q < 2`, Theorem 7 says shrinkage can be worse than simply holding
   `w_R`; if `q ≤ 1`, nothing in the non-singular theory applies at all. Stop here in those cases.
3. **Estimate `τ̂_R = (σ̂²_R − σ̂²_T)/σ̂²_T`** from the sample covariance — two quadratic forms and one
   plug-in GMV solve. This is the only data-dependent input.
4. **Run the naive-diversification test.** Simulate the law
   `((d−1)/(n−d))·F_{d−1,n−d}(τ*_N χ²_{n−1}/2)` at your `(n, d)` and your chosen `τ*_N`, take its upper
   `α`-quantile, and reject "hold equal weight" only if `τ̂_N` exceeds it. Both the critical relative
   loss `τ*_N` and the threshold require Monte-Carlo (the paper gives Table 2 for a grid); the
   simulation is cheap because Theorem 3 gives a stochastic representation in **standard**
   distributions with identity parameters — `ξ ~ N_{d−1}(0, I)`, `V ~ W_{d−1}(I, n−1)`, `χ²_{n−d}`,
   mutually independent, with `θᵀθ = τ_R` — so no return panel and no particular `Σ` has to be
   simulated, only `(n, d, τ_R)`.
5. **Only if the test rejects**, form `κ_S = ((d−3)/(n−d+2))·(1/τ̂_R)` and hold
   `κ_S w_R + (1 − κ_S) ŵ_T`; prefer the modified variant `ŵ_M`, which dominates `ŵ_S`.
6. **Equivalently** (Theorem 8), shrink the precision matrix: `Σ̂_S⁻¹ = κ_S Σ_R⁻¹ + (1−κ_S) Σ̂⁻¹`, then
   take its GMV solution. Note `Σ̂_M` is positive-definite while `Σ̂_S` need not be.

## Robustness evidence (qualitative only)

- **The dominance results are proofs, exact for every `n ≥ d+2`, `d ≥ 4`** — no asymptotics, no
  priors, no simulation needed to establish them. Theorem 9's `F` law for `τ̂_R` is likewise exact.
  Table 2's numbers are simulated only because the *critical* loss has no closed form.
- **`d ≥ 4` is a real condition**, inherited from the James–Stein structure (`κ_S` carries `d − 3`).
  The method has nothing to say about three-asset problems, which is irrelevant here.
- **Assumptions the authors flag themselves.** Serially independent, identically normally distributed
  returns throughout; the introduction explicitly notes that real returns show structural breaks,
  serial correlation in higher moments and heavy tails, and that the paper assumes them away. There is
  **no empirical study** — the conclusion names one as future work. A reader who wants to know how the
  estimator behaves on real data will not find out here.
- **The `τ_R`-only dependence is the load-bearing simplification** and it is proved (Theorem 3), not
  assumed: the whole decision reduces to `(n, d, τ_R)`. That is what makes Table 2 portable across
  asset classes — and it is also what makes the result fragile to the i.i.d.-normal assumption, since
  `τ̂_R`'s distribution is where normality enters.
- **Independent corroboration of the direction, not the constants.** The conclusion that naive
  diversification is hard to beat when `d` is large relative to `n` is DeMiguel–Garlappi–Uppal's
  empirical finding (`notes/2026-08-17-naive-vs-optimized-weighting.md`), Tu–Zhou's combination result
  (`notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md`), and
  Pflug–Pichler–Wozabal's decision-theoretic one
  (`notes/2026-10-24-equal-weight-as-the-maximal-ambiguity-optimum.md`), reached three other ways.
  This paper is the one that supplies a **test**.
- **Known limitation of the test's framing.** The authors state that for conventional `α` their rule
  *favours* equal weight by construction: failing to reject does not establish that equal weight is
  better, only that the optimiser has not been shown to be. That asymmetry is a feature for a lab
  whose benchmark *is* equal weight, and a bug for anyone wanting a symmetric comparison.

## Implementability here

**This is the most directly usable source of the session, and the use is a free screen rather than a
candidate.** v3 grades every candidate as Sharpe minus the equal-weight eligible pool's. Theorem 9
converts "can this weighting scheme beat the equal-weight pool?" into an `F`-statistic computable from
returns the lab already holds, with no trial consumed and no holdout touched — on the **variance**
axis only, which is the honest scope.

**What the numbers say about this panel.** The lab's effective sample size `q = n/d`:

- **~1,000 eligible names, daily returns over six years (`n ≈ 1,512`): `q ≈ 1.5`.** This is inside
  the régime where Theorem 7 says shrinkage can be *worse* than simply holding the reference
  portfolio, and where the plug-in estimator's relative loss limits to `1/(q−1) ≈ 2.0` — i.e. three
  times the minimum variance, matching Kempf–Memmel's `(N−1)/(T−N−1) ≈ 1.95` for the same cell by a
  different route.
- **A 100-name book on monthly data (`n ≈ 70` over validation): `q < 1`.** Nothing in the
  non-singular theory applies; see `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md`.
- **A 100-name book on one year of daily data (`n = 252`): `q ≈ 2.5`.** This is the one cell where
  the machinery is comfortably in scope, and extrapolating Table 2's shape (`d = 100, n = 120` needs a
  measured `τ̂_N` above 5202%) the required demonstrated improvement is still enormous.

**Three things it changes.**

1. **It gives the lab's standing "equal weight wins" verdict a test statistic instead of a
   calibration.** `SUMMARY.md` item 1 ("count the noisily-estimated parameters") and
   `experiments/learnings.md`'s repeated closure of covariance-based constructions have rested on
   horse-races and the ERC theorem. Theorem 9 is the hypothesis test, with the null on the side the
   lab already believes.
2. **It is the one weighting construction in this folder that estimates a single scalar.** The
   2026-10-24 open-questions entry nominated item `#303` partly on that ground. `κ_S` needs `τ̂_R` and
   nothing else; a candidate built on it has one free number, which the deflated-Sharpe bar can
   actually afford.
3. **Theorem 8 connects it to a result the lab has already priced.** Shrinking weights toward the pool
   is shrinking the precision matrix toward the pool's implied precision matrix — the same family as
   Jagannathan–Ma's constraint-as-shrinkage, which this folder covers and which v3's long-only
   constraint already imposes for free. **A candidate that shrinks toward the pool and is also
   long-only is applying two overlapping shrinkages**, and should say which one it thinks is doing the
   work.

**Pitfalls.**

- **Dominance is in variance, and variance is not skill on this panel.** The loss function is extra
  out-of-sample *variance*. `experiments/learnings.md` (2026-10-09/10) measured that Sharpe is flat in
  beta here, so a construction that provably reduces variance has no established route to skill.
  Reducing estimation risk is a reason to *prefer* a weighting among equally-motivated ones, not a
  reason to expect skill.
- **The test is about weights, not about costs.** `ŵ_S` moves with `τ̂_R`, so re-estimating it at each
  rebalance makes it turn over. v3 charges 15–40 bps per side plus transaction taxes, and
  `learnings.md`'s band result says the cheapest construction is the one that declines to trade.
  Shrinkage toward a fixed reference reduces turnover relative to `ŵ_T`; it does not reduce it
  relative to holding the reference.
- **`τ̂_R` contains `σ̂²_T`, which needs `n > d`.** The screen cannot be run on the full panel at
  monthly frequency, and running it on a selected subset puts the selection inside the statistic.
- **The reference portfolio must be fixed in advance.** Choosing `w_R` after looking at `τ̂_R` for
  several candidates breaks both the dominance proof and the test.
- **Do not read Table 2 as a measurement.** It is the sampling behaviour of an estimator under
  simulated normal i.i.d. returns. Its shape (thresholds exploding in `d/n`) is the transferable part;
  its exact cells are not this panel's.

## Related

- `notes/2026-10-25-gmv-weights-as-regression-coefficients.md` — Kempf–Memmel: the loss function used
  here is their Proposition 4, their Proposition 6 (best unbiased) is this paper's premise, and their
  `(N−1)/(T−N−1)` is the `τ_T` this paper improves on.
- `notes/2026-10-25-exact-distributions-of-estimated-portfolio-weights.md` — Okhrin–Schmid: why
  de-biasing is the wrong move, and why a mean-using weight rule cannot be rescued this way at all.
- `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` — the `q ≤ 1` and singular-`Σ`
  cases this paper's non-singular theory excludes, and a shrinkage-based *test* (as opposed to
  estimator) for them.
- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — Jagannathan–Ma, the result
  Theorem 8 generalises.
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` — Tu–Zhou's
  combination rule: same shape, different objective (expected utility rather than variance) and
  different intensity.
- `notes/2026-10-24-equal-weight-as-the-maximal-ambiguity-optimum.md` and
  `notes/2026-08-17-naive-vs-optimized-weighting.md` — the decision-theoretic and empirical versions of
  the same verdict.
- `notes/2026-10-24-transaction-costs-as-robustness-and-regularization.md` — the cost-penalty
  reduction. Note which vector each penalty acts on: that one penalises `w − w₀` (don't move), this one
  pulls `w` toward `w_R` (stay near the reference).
