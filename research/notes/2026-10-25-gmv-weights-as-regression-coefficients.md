---
title: "Estimating the global minimum variance portfolio — the GMV weights ARE OLS regression coefficients, so the whole of OLS inference (standard errors, F-tests on weight restrictions, an exact estimation-risk formula) transfers for free"
authors: Kempf, Memmel
year: 2006 (CFR working paper 05-02, 2005)
venue: "Schmalenbach Business Review 58(4), 332–348 (venue tier 2 — peer-reviewed business/finance journal, not one of the rubric's tier-1 finance outlets). Working-paper version: CFR Working Paper 05-02, Centre for Financial Research, University of Cologne."
url: "https://doi.org/10.1007/bf03396737 ; working paper read at https://www.econstor.eu/bitstream/10419/57730/1/699904641.pdf (handle https://hdl.handle.net/10419/57730)"
citations: "100 (Crossref `is-referenced-by-count` for 10.1007/bf03396737, checked 2026-10-25). Semantic Scholar not consulted for this DOI — its `/paper/search` endpoint returned HTTP 429 on the first unauthenticated call of the session, as `research/README.md` documents. OpenAlex not spent on it (the day's budget was reserved for locations lists)."
sample_period: "Theory plus one illustration. The propositions contain no data. The empirical illustration in Section 7 uses monthly MSCI total-return indices for the G7, in EUR, January 1984 – December 2003 — entirely before this lab's train window ends and far from validation."
markets: "Not applicable to the theory. The illustration is seven developed-market country indices (Canada, France, Germany, Italy, Japan, UK, US)."
tier: "B. The central result is an exact algebraic identity with a short proof, independently restated and used by later tier-1 work (Frahm–Memmel 2010 in the Journal of Econometrics builds directly on it), and the paper is honest about what normality buys and what it does not. Held at B rather than A on venue (tier-2 journal) and on citation count (100 — solid, not canonical), and because the exact distributional results are conditional on normal i.i.d. returns, with the heavy-tailed case handled only asymptotically."
validation_overlap: false
published_post_2018: false
read: "In full, the CFR working-paper version (05-02) from EconStor — 486 KB PDF, 36 pages, `pdftotext -layout` into 73 KB of clean text, 504 instances of `\" the \"`, zero `( )` dropout. All eight sections and the three appendices were read; the appendix algebra was followed but not re-derived. The typeset Schmalenbach version was NOT obtained (`doi.org/10.1007/bf03396737` is closed and the journal's own archive was not reachable); the working paper carries all six propositions, the empirical illustration and the appendix proofs, so nothing material is missing, but page and table numbers quoted here are the working paper's."
access_note: "EconStor worked on the first try, confirming `research/README.md`'s 2026-10-12 reversal of the 2026-10-04 'dark behind Anubis' entry for a second time. The route was a plain web search surfacing `hdl.handle.net/10419/57730`; the handle's landing page (24 KB) prints the `bitstream/10419/<id>/1/<numeric>.pdf` link three times. `-w 'HTTP %{http_code} size=%{size_download}'` on every fetch, per the README; both the handle page and the PDF reported real sizes."
anti_lookahead_note: "The paper holds no post-2023 content of any kind (published 2006). The one empirical illustration is reported here only for what it demonstrates about the test's POWER — that the standard errors on estimated weights are wide enough that most weights and whole groups of weights are indistinguishable from zero — and not for any return, risk or performance number. No figure from its 1984–2003 sample is carried into any claim."
---

## Mechanism

This is not a strategy source. It is the source that turns this lab's **most-used screen** — "count
the noisily-estimated parameters before proposing any weighting scheme" (item 1 of `SUMMARY.md`'s
candidate list) — from a calibration into a closed-form identity with a test statistic attached.

**The identity.** Pick any one asset `N` as the dependent variable and regress its return on the
`N − 1` *return differences*, with an intercept:

```
r_{t,N} = α + β_1 (r_{t,N} − r_{t,1}) + … + β_{N−1} (r_{t,N} − r_{t,N−1}) + ε_t ,   t = 1…T,  T > N
```

Then (Proposition 1), **exactly, in population**:

- `β_i = w_MV,i` for `i = 1 … N−1` — the OLS slopes *are* the global-minimum-variance weights;
  the last weight is `w_MV,N = 1 − Σ β_i`
- `α = µ_MV` — the intercept *is* the GMV portfolio's expected return
- `σ²_ε = σ²_MV` — the error variance *is* the GMV portfolio's return variance

The proof is two lines of algebra once you write `β^ex = Ω⁻¹ cov(r_{t,N}·1 − r_t^ex, r_{t,N})` with
`Ω = var(r_{t,N}·1 − r_t^ex)`: minimising portfolio variance subject to `1ᵀw = 1` and minimising
`Σ ε_t²` are the same program, because differentiating the sum of squares with respect to `α`
delivers the budget constraint for free. **Normality is used nowhere in it.**

**The estimators coincide too** (Proposition 2). The OLS estimate `β̂` is numerically identical to
the plug-in estimate `ŵ_MV = Σ̂⁻¹1 / 1ᵀΣ̂⁻¹1`, and `µ̂_MV = α̂`. Only the variance estimates differ,
by the scalar `(T − N)/T`: `σ̂²_MV = ((T − N)/T) · σ̂²_ε`. So this is not an *alternative* estimator
to audit — it is the same number, re-derived in a framework that already has an inference theory.

**What that buys** (Proposition 3; returns normal and i.i.d., conditioning on the `T × (N−1)` matrix
`z` of return differences):

```
β̂^ex | z  ~  N( w_MV^ex ,  σ²_MV (z'z − T z̄z̄')⁻¹ )
α̂    | z  ~  N( µ_MV   ,  σ²_MV (1/T + z̄'(z'z − T z̄z̄')⁻¹ z̄) )
(T − N) σ̂²_ε / σ²_MV  ~  χ²(T − N)
```

i.e. ordinary OLS standard errors on the weights, an ordinary `t`-test for "is this name's weight
different from zero", and — the part that matters most here — the **ordinary restricted-regression
`F`-test for any `m ≤ N − 1` linear restrictions on the weight vector**. "These three names carry no
weight", "all weights are equal", "this candidate's weight vector equals the pool's" are all one
`F(m, T − N)` away, with no new machinery and no bootstrap.

**The parameter-count theorem.** Decompose the out-of-sample variance of a book built on estimated
weights (Propositions 4 and 5):

```
var(r̂_{T+1,MV} | r_1…r_T)  =  σ²_MV  +  R̃(ŵ_MV),      R̃(ŵ_MV) = (ŵ_MV − w_MV)' Σ (ŵ_MV − w_MV)
E[ var(r̂_{T+1,MV} | r_1…r_T) ]  =  σ²_MV · ( 1 + (N − 1)/(T − N − 1) )
```

**The expected estimation-risk premium is exactly `(N − 1)/(T − N − 1)` of the true minimum
variance.** It depends on nothing but the number of names and the number of observations — not on
the covariance structure, not on the asset class, not on the sample. That is the theorem behind the
lab's screen, and it is a ratio one can compute before writing a line of a candidate.

**And you cannot estimate your way out of it** (Proposition 6): the plug-in estimator `ŵ_MV` has the
*lowest* estimation risk of all **unbiased** weight estimators. Any improvement must be a biased
estimator — which is exactly where `notes/2026-10-25-dominating-estimators-and-the-naive-diversification-test.md`
picks the thread up.

## Construction recipe

Everything here is `numpy`-level; no optimiser and no risk-free rate are involved.

1. **Build the regressor matrix.** On a panel of `N` names with `T` aligned return observations,
   choose a reference name `N` (any one; the identity is invariant to the choice, though the
   *reported* weight of the reference is the residual `1 − Σβ̂`). Form `z_t = (r_{t,N} − r_{t,1}, …,
   r_{t,N} − r_{t,N−1})` and `Z = [1 z]`.
2. **Regress** `r_{·,N}` on `Z` by OLS. Read the weights off the slopes, the GMV mean off the
   intercept, the GMV variance off the residual variance (times `(T−N)/T` if you want the plug-in
   convention).
3. **Standard errors** come from `σ̂²_ε (Z'Z)⁻¹` under normal i.i.d. returns. Under heavy tails —
   the elliptical case, which the paper treats in Section 5 — Propositions 1 and 2 survive untouched
   because their proofs never used normality, but the error term becomes heteroskedastic in the
   regressors, the estimators are only *asymptotically* normal, and the covariance matrix must be
   **White-corrected**. The paper applies the White correction in its own illustration.
4. **Test a weight hypothesis** with the restricted-regression `F`. For "the GMV portfolio is equal
   weight", impose `β_i = 1/N` for all `i = 1…N−1` (`m = N−1` restrictions); for "these `k` names are
   unnecessary", impose `β_i = 0` on them (`m = k`). The statistic is `F(m, T − N)`.
5. **Screen before building.** Compute `(N − 1)/(T − N − 1)` first. It is the fraction of the true
   minimum variance you expect to pay for having estimated the weights, and it is finite only for
   `T > N + 1`.

## Robustness evidence (qualitative only)

- **Propositions 1, 2 and the estimation-risk identity are algebra, not estimates.** They hold
  exactly, in any sample, for any positive-definite `Σ`, with no distributional assumption beyond the
  existence of second moments. There is nothing in them to replicate or decay.
- **The distributional results (Proposition 3) are the part with assumptions**: normal, i.i.d.,
  `T > N`. The paper itself widens this to the elliptical class — which admits the Student-`t` and so
  the heavy tails real return data show — and finds that only Proposition 3 needs modifying, via
  asymptotic normality plus White standard errors. It does **not** handle serial dependence,
  conditional heteroskedasticity or structural breaks, and says so.
- **Independent uptake.** Frahm–Memmel (2010, *Journal of Econometrics*) builds its dominance theory
  on this representation; Okhrin–Schmid (2006, *Journal of Econometrics*) derives the same GMV
  weight distribution by a different route (the multivariate `t`, from Wishart algebra) and agrees
  with it. Two independent derivations of the same conditional law is a stronger footing than the
  venue tier alone suggests.
- **Power, qualitatively.** The paper's own illustration is the honest advertisement *against*
  over-reading estimated weights: on seven country indices with two decades of monthly observations —
  a case with `(N−1)/(T−N−1)` under 3%, i.e. about as favourable as this kind of estimate ever gets —
  most individual weights were not distinguishable from zero at the 10% level, and the joint
  hypothesis that three of the seven carry **no weight at all** could not be rejected
  (`F(3, 233) = 0.58`). The construction that survives such a test is not a precise one.

## Implementability here

**What this is for: it is an inference device, not a strategy.** The lab has already measured that
the GMV *objective* is not a source of skill on this panel — v3's `pt_lowvol_gk_quarterly` delivered
every risk reduction it promised (slice volatility 0.61× the pool's, beta 0.62 against 0.98) and
earned exactly proportionally less, landing at the 64th percentile of its own null, and
`experiments/learnings.md` records "Sharpe is flat in beta on this panel, so risk-reduction is not a
source of skill." Nothing below proposes building a minimum-variance book. The value is the
arithmetic.

**The screen, with this panel's numbers.** `(N − 1)/(T − N − 1)` at daily frequency, where `T` is the
count of return observations in the estimation window:

| names `N` | `T = 252` (1yr daily) | `T = 756` (3yr) | `T = 1512` (6yr) |
|---|---|---|---|
| 25 | 0.11 | 0.03 | 0.02 |
| 50 | 0.24 | 0.07 | 0.03 |
| 100 | **0.66** | 0.15 | 0.07 |
| 250 | — (`T < N+2`) | 0.49 | 0.20 |
| 1000 | — | — | **1.95** |

Read the cell as *extra* out-of-sample variance as a fraction of the minimum attainable. A 100-name
book estimated on one year of daily data expects 66% more variance than the thing it was trying to
minimise; the full eligible panel (~1,000 names) estimated on six years of daily data expects
**three times** the minimum variance. At *monthly* frequency — which is this lab's usual rebalance
grid, and where a candidate has ~70 validation observations — the formula is undefined for anything
past about 65 names. **This is the quantitative form of the rule, and it is free to apply.**

**Three concrete uses:**

1. **Pre-registering a weighting proposal.** Any candidate whose weights come from a covariance
   estimate should state `N`, `T`, and `(N−1)/(T−N−1)` in its hypothesis line. If that number is not
   small, the proposal is predicted to lose on the risk axis it was built to win, before costs.
2. **An exact test against the pool, on the risk axis only.** The restricted `F` gives a clean,
   pre-registerable answer to "is this book's weight vector distinguishable from equal weight?" —
   computed from returns the lab already has, requiring no new backtest and therefore not consuming a
   trial. Note the direction of the inference carefully: it tests the *weights*, i.e. a
   second-moment claim, and says nothing about skill.
3. **Choosing `K`.** The band result (`B = 200` retention on `K = 100`) and the tail-depth confound
   (a top-100 drawn from 498 reaches a more extreme tail than one drawn from 284) are both decisions
   about `K`. This formula adds a third term to that trade-off that was previously only qualitative.

**Pitfalls specific to this repo.**

- **The GMV portfolio is long-short.** The unconstrained `β̂` will be negative on many names, so the
  weight vector this regression returns is not directly tradeable under the long-only constraint. The
  constrained version is a different object, and by Jagannathan–Ma the constraint is itself a
  covariance shrinkage (see `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`). Use
  the regression for inference on the *unconstrained* object, or re-derive it under the constraint;
  do not quietly clip the output and keep the standard errors.
- **`T > N + 1` is a hard wall, not a guideline.** Both the estimator and the estimation-risk formula
  cease to exist below it. On the ~1,000-name eligible panel at monthly frequency the quantity is not
  large — it is undefined.
- **Returns here are neither normal nor i.i.d.** The elliptical extension covers the tails but not the
  serial dependence, and `learnings.md` has independently measured that near-static books produce
  "one draw repeated" with inflated `t`-statistics. Treat any `F`-statistic from this machinery as an
  upper bound on the evidence, exactly as the lab already treats its own overlapping-window
  `t`-statistics.
- **v3 breaks the identity between a weight vector and a book.** Rows are filled at the next real
  print, positions drift between rows, and costs are charged per name. The regression's `w` is a
  target weight at a date; the thing v3 measures is a traded book. The inference applies to the
  former.
- **Do not import the illustration's conclusions.** Seven country indices over two decades of monthly
  data is not this panel, and the paper's finding that three of seven weights could be zeroed is a
  statement about *that* `N` and `T`. The transferable part is the formula and the test, not the
  verdict.

## Related

- `notes/2026-10-25-exact-distributions-of-estimated-portfolio-weights.md` — Okhrin–Schmid derive the
  same GMV weight law from Wishart algebra (a multivariate `t`), and show the contrast: the
  *Sharpe-ratio-optimal* weight estimator has **no finite moments at all**. Read the two together:
  the GMV case is the only one where this inference machinery exists.
- `notes/2026-10-25-dominating-estimators-and-the-naive-diversification-test.md` — Frahm–Memmel take
  Proposition 6 as their starting point (best *unbiased* ⇒ go biased) and turn the relative loss of a
  reference portfolio into an `F`-distributed statistic, which is the properly-powered version of the
  "is equal weight good enough?" test sketched above.
- `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` — what happens to these tests
  when `N/T` is not small and when `Σ` is rank-deficient, which is this panel's actual regime.
- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — Jagannathan–Ma: the long-only
  constraint is a covariance transformation, which is why constraining is not free inference.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal, the empirical
  horse-race this note supplies the closed form for.
- `notes/2026-10-24-equal-weight-as-the-maximal-ambiguity-optimum.md` — the other half of the case for
  the pool: equal weight as an exact decision-theoretic optimum rather than a statistical fallback.
- `experiments/learnings.md` (2026-10-09/10, v3) — "Sharpe is flat in beta on this panel, so
  risk-reduction is not a source of skill", and the 2026-08-20 entry closing risk-contribution caps
  on the grounds that they need a covariance matrix. This note prices that objection.
