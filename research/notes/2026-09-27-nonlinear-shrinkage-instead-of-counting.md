---
title: "Nonlinear shrinkage instead of counting — the optimal rotation-equivariant covariance estimator, and what a long-only constraint does to it"
authors: Ledoit, Wolf
year: 2020; 2017
venue: Annals of Statistics 48(5) (Tier 1); Review of Financial Studies 30(12), 4349–4388 (Tier 1)
url: https://doi.org/10.1214/19-AOS1921 ; https://doi.org/10.1093/rfs/hhx052
citations: "Analytical nonlinear shrinkage 169 (Crossref by DOI, checked 2026-09-27); the 2012 Annals predecessor 262 (Semantic Scholar by DOI, checked 2026-09-27); Markowitz Meets Goldilocks 323 (Crossref), 314 (OpenAlex), both checked 2026-09-27 — Semantic Scholar returns not-found for the RFS DOI"
sample_period: "Analytical paper: Monte Carlo only, no market data. Goldilocks: daily CRSP 1972–2011, out-of-sample 1973–2011 over 480 'monthly' (21-trading-day) investment dates with T = 250; monthly-frequency robustness run on 1945–2011 data, out-of-sample 1955–2011 with T = 120."
markets: "US common stocks (CRSP), N from 30 to 500 plus a 'all live stocks' variant; simulations at p up to 10,000"
tier: A
validation_overlap: false
published_post_2018: true   # the Annals article is 2020; the RFS companion is 2017, and both preprints predate 2018
---

**What was read, and in which version.** The *Analytical Nonlinear Shrinkage* paper was read in full
as **University of Zurich Working Paper 264** (first version September 2017, this version November
2018), which is the preprint of the 2020 *Annals of Statistics* article; the version of record was not
fetched. *Markowitz Meets Goldilocks* was read as **UZH Working Paper 137**, in full for the sections
cited below (the motivation, the backtest design, the no-short-sales section and the transaction-cost
section); the RFS version of record is closed and `zora.uzh.ch` served a 4 KB shell rather than a PDF.
The 2012 *Annals* predecessor (QuEST) and the 2004 linear-shrinkage paper were **not read** and nothing
here rests on them beyond definitions the papers above restate. **No performance number from the
Goldilocks backtest is recorded in this note**, per this folder's anti-lookahead rule; what is recorded
is the *sign and direction* of its long-only finding, which is a statement about a constraint rather
than about a period.

**Why this is filed on the same night as two counting papers.** The two companion notes end in the same
place: on a panel with near-duplicate columns the number of factors is not identified, and no
eigenvalue-threshold estimator repairs that. This literature takes the other road entirely — **do not
count, correct** — and it has a theorem saying that road is the only optimal one within its class. It
then, unusually and to its credit, reports that a long-only constraint destroys most of its own
advantage, which is the part this repo has to read first.

## Mechanism

Start from the degrees-of-freedom problem: a `p × p` covariance matrix has `p(p+1)/2` parameters and a
sample of `n` observations cannot pin them down when `p` and `n` are comparable. The sample covariance
matrix `S = Σ λ_i u_i u_i'` is not merely noisy, it is **biased in a specific, known direction**: the
large sample eigenvalues are too large and the small ones too small. The illustration the paper gives
is the cleanest available and needs no data — if every population eigenvalue equals `τ`, the sample
eigenvalues spread over the Marchenko–Pastur interval `[τ(1−√c)², τ(1+√c)²]` with `c = p/n`, so the
**maximum relative bias is of order `2√c`**.

**The key structural result, and it is why "how many factors" is the wrong question.** Restrict to
*rotation-equivariant* estimators — those that keep the sample eigenvectors and only change the
eigenvalues, which is the honest class when you have no prior information about the identity of the
variables. Within that class, Proposition 2.1 says the estimator minimising the minimum-variance loss
is, **if and only if**, the one whose `i`-th eigenvalue is

```
d*_i = u_i' Σ u_i           (up to one common positive scale factor)
```

that is: *the true variance of the sample eigenvector's own direction*. Not zero for small `i`, not a
common shrinkage target, not a bulk-vs-signal dichotomy — **each direction gets its own number**. The
same estimator is finite-sample optimal under Frobenius loss (their 2012 paper's Section 3.1). So the
decision problem is not "which eigenvalues are noise" but "what value should each eigenvalue take",
and **a factor count is a crude, two-level quantisation of an answer that is continuous in `i`**. This
is the "Goldilocks" point of the companion paper's title: linear shrinkage optimises over two free
parameters (intercept and slope on the eigenvalues), nonlinear shrinkage over `p` — the same number as
the assets, neither too few nor too many.

`d*_i` is unobservable. The large-dimensional asymptotic replacement (Theorem 3.1) is a function of
the *limiting sample spectral density* `f` and its **Hilbert transform** `Hf`:

```
d°(x) = x / ( [π·c·x·f(x)]² + [1 − c − π·c·x·Hf(x)]² )
```

and any estimator minimising the asymptotic minimum-variance loss is equal to this one up to scale
(part b of the theorem — it is a characterisation, not just a sufficient condition). The contribution
of the analytical paper is to estimate `f` **and** `Hf` directly by kernel smoothing of the observed
eigenvalues, rather than recovering population eigenvalues by numerical inversion (QuEST) or by sample
splitting (NERCOME).

## Construction recipe

Fully closed-form, ~20 lines, no optimisation, no tuning beyond one exponent the authors justify by
citation. For sample covariance `S = Σ_{i=1}^p λ_i u_i u_i'` with `n` observations and `c = p/n`:

1. **Global bandwidth** `h = n^{−1/3}` (Theorem 4.1 requires a negative exponent of `n` strictly less
   than `2/5`; `1/3` is the first simple fraction below it, following Jing et al.).
2. **Locally adaptive bandwidth** `h_j = λ_j · h`, i.e. proportional to the eigenvalue being smoothed.
   This is the paper's second innovation and the reason a single global bandwidth fails: the spectrum's
   scale varies across its own range, so one bandwidth is ill-suited to the whole of it.
3. **Kernel density at each eigenvalue**, Epanechnikov:
   `f̃(λ_i) = (1/p)·Σ_j (3/(4√5·h_j))·[1 − (1/5)·((λ_i − λ_j)/h_j)²]₊`
4. **Its Hilbert transform**, in closed form for this kernel (Proposition 4.1):
   `Hf̃(λ_i) = (1/p)·Σ_j { −3(λ_i − λ_j)/(10π h_j²) + (3/(4√5 π h_j))·[1 − (1/5)((λ_i−λ_j)/h_j)²]·ln| (√5 h_j − λ_i + λ_j) / (√5 h_j + λ_i − λ_j) | }`
5. **Shrunk eigenvalues**:
   `d̃_i = λ_i / ( [π·(p/n)·λ_i·f̃(λ_i)]² + [1 − p/n − π·(p/n)·λ_i·Hf̃(λ_i)]² )`
6. **Recompose**: `S̃ = Σ_i d̃_i u_i u_i'`. Eigenvectors are untouched, by construction.

Notes on use. The kernel's support at `λ_i` is `[λ_i(1 − √5·n^{−1/3}), λ_i(1 + √5·n^{−1/3})]`, whose
lower end is positive only when `n > 5√5 ≈ 11.2`, so the authors state it is **unadvisable to use the
procedure when `p < 12`**. The `p > n` case is covered: the `p − n` smallest sample eigenvalues are
exactly zero and the density is taken over the `n` nonzero ones. Reference code is in the paper's
Appendix D. The trace is preserved asymptotically by the scale convention `α = 1`.

## Robustness evidence (qualitative only)

- **The optimality is a theorem within a stated class**, not a backtest finding: the class is
  rotation-equivariant estimators, the loss is minimum-variance (also Frobenius for the finite-sample
  version), and the asymptotics are `p, n → ∞` with `p/n → c`. Outside that class — if you have real
  prior information about which variables are which, e.g. an industry or region structure — the
  theorem does not apply and a factor model may do better. The Goldilocks paper's own tables report
  factor-based portfolios doing about as well as, and under one constraint better than, the
  rotation-equivariant ones.
- **Simulation evidence is strong and internally benchmarked.** The Monte Carlo compares six
  estimators including the infeasible finite-sample optimum `S*` as a 100% reference, and reports the
  analytical formula recovering nearly all of the attainable loss reduction where linear shrinkage
  recovers about half — closing to essentially all of it at `p = 10,000`, `n = 30,000`. It matches the
  numerical QuEST estimator's accuracy at roughly a thousandth of the compute (`O(p²)` for the
  kernel step, against the `O(p³)` eigendecomposition every method needs anyway). Bandwidth and kernel
  choices are checked for sensitivity in a dedicated robustness section.
- **`c = p/n` governs everything, and the direction is counter-intuitive.** As the concentration ratio
  rises from 0.1 toward 0.9, *every* shrinkage estimator's measured improvement over the sample
  covariance matrix rises — "higher concentration ratios make all shrinkage estimators look good", and
  at the high end the ordering among them stops mattering much. The corollary is that the regime where
  choosing a good shrinkage rule matters most is the *moderate* one.
- **The `2√c` rule of thumb is the honest headline and it is uncomfortable.** To hold the relative
  error in weights allocated across sample eigenvectors to 5% you need `2√(p/n) = 0.05`; for a 30-stock
  portfolio that is on the order of two centuries of daily data. And at `c = 1/5` — five times more
  observations than assets — the required correction is already "highly nonlinear". So the claim is not
  that shrinkage helps at high `c`; it is that **there is no `c` at which the sample covariance matrix
  is adequate for this purpose**.
- **The long-only result, and it is the one this repo must read.** Section 5.5.4 of the Goldilocks
  paper imposes a lower bound of zero on all weights and reports that the **sample covariance matrix
  becomes uniformly best among the rotation-equivariant portfolios**; disallowing short sales *helps*
  the sample matrix and *hurts* linear shrinkage, nonlinear shrinkage and the single-factor variant.
  The authors attribute this to Jagannathan–Ma — a no-short-sales constraint *is* an implicit shrinkage
  of the covariance matrix — and Remark 5.2 concedes the scope directly: their method is useful to a
  long-only manager only in the case where the long-only constraint is *not binding*, i.e. a
  benchmarked manager running a dollar-neutral active overlay whose short side is well diversified.
- **Selection in the backtest universe is worth naming.** At each rebalance the 500 largest stocks
  with a complete 250-day past history *and* a complete 21-day forward history are identified, and `N`
  are drawn at random from those 500. The forward-history requirement is a look-ahead in the universe
  definition (the folder has a note on exactly this shape), and the "largest, complete-history"
  screen is the same survivorship conditioning this repo's own universe carries.
- **Costs are acknowledged as unmodelled.** The Goldilocks backtest takes no transaction costs, and the
  authors identify two sources they did not charge: monthly turnover from weight changes, and turnover
  from the investment universe itself changing between rebalances. They report the nonlinear portfolios
  having *lower* average turnover than linear shrinkage in a limited unconstrained run, and state that
  actively limiting turnover is beyond the paper's scope. **So the cost side of this literature is
  open**, which for a 15 bps/side repo is the gap that matters most.

## Implementability here

**The honest verdict is: implementable, cheap, and mostly redundant — and that conclusion is the
paper's own, not this folder's.** No candidate is proposed.

- **The engine already applies the treatment.** `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`
  records Jagannathan–Ma's result that a long-only constraint plus a position cap *is* covariance
  shrinkage, and this repo imposes both unconditionally (gross ≤ 1.0, 25% cap, no shorts). The
  Goldilocks paper measures what that does to nonlinear shrinkage's edge and finds it removed — the
  sample matrix wins under no-short-sales. **Two independent Tier-1 sources now say the same thing
  about this repo's constraint set**, which is a stronger basis for declining than an accumulation of
  nulls.
- **It is not a trial-worthy candidate, and the reason is not cost or difficulty.** A better covariance
  estimate is an *allocator* input, and this lab's measured history on allocators is consistent:
  variance-based splits between sleeves have failed twice (`learnings.md`), HRP was declined on the
  same grounds (`SUMMARY.md` #86), and `notes/2026-09-08-stacked-regressions-nonnegative-weights.md`
  shows any fully-invested long-only reweighting of finished books is bounded by the simplex. Nonlinear
  shrinkage changes *which* long-only minimum-variance book you get; it does not escape that bound.
  The lab's seated `E/Var` is a membership rule, not an optimiser, and it does not invert anything.
- **What is worth taking, and it is the framing rather than the estimator.** The `d*_i = u_i' Σ u_i`
  characterisation is the cleanest available argument that **"how many factors are real" is a badly
  posed question in a decision problem**. A count imposes a two-level answer (`keep` / `discard`) on a
  quantity the theorem says is continuous in `i`. That directly bears on this repo's PCA-residual
  constructions: choosing `K` is choosing a quantisation, and the companion note's weak-factor finding
  says the identity of the marginal component is a coin flip anyway. The transferable rule: **when a
  construction's parameter is "how many directions", check whether the underlying decision actually
  needs a count or only needs a weight.**
- **Dimensions here, if anyone does compute it as a diagnostic.** `p ≈ 145` instruments — comfortably
  above the `p ≥ 12` floor. A 250-day window gives `c = 0.58`, which by the paper's own rule of thumb
  puts the maximum relative bias of the sample eigenvalues at order `2√0.58 ≈ 1.52`, i.e. **of the same
  order as the eigenvalues themselves**. A 1000-day window gives `c = 0.145` and `2√c ≈ 0.76` — still
  large. So the repo's 250-day trailing covariance, used in the `E/Var`, diversification-ratio and
  effective-bets diagnostics recorded throughout `learnings.md`, has eigenvalues that are badly
  biased even though its *weights* are protected by the constraints. **Any diagnostic that reads
  eigenvalue levels off that matrix — not weights, levels — inherits that bias**, and that includes
  `EffRank` and the eigenvalue shares the 2026-09-26 session computed. This is a free and specific
  caution about numbers the lab has already recorded.
- **Cost and turnover cannot be imported from this literature at all**, because it charges none. Any
  use of a shrunk covariance inside a book here would have to be costed from scratch.
- Compute is not an obstacle: `O(p³)` eigendecomposition on 145 names is milliseconds, far inside
  `CLAUDE.md`'s ~60s per call, and the formula is deterministic, which the causality check requires.
  `scipy`/`numpy` suffice; no new dependency.

## Related

- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — Jagannathan–Ma, the reason this
  estimator is mostly redundant here, and the result the Goldilocks paper cites to explain its own
  long-only finding.
- `notes/2026-09-24-long-only-minimum-variance-composition.md` — what a long-only minimum-variance
  book actually holds on a universe like this one.
- `notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md` — the same
  Marchenko–Pastur spread, read as a null hypothesis rather than as a bias to correct.
- `notes/2026-09-27-counting-factors-eigenvalue-estimators.md` — the counting road, and why it is not
  identified on a duplicated-column panel.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — the "never invert anything"
  answer to the same conditioning problem, declined here; nonlinear shrinkage is the opposite answer
  and is declined for a different reason.
- `notes/2026-09-08-stacked-regressions-nonnegative-weights.md` — the simplex bound that any
  long-only reweighting of finished books obeys.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — where a better covariance estimate would *not* help:
  the gate's statistic.
- `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` and
  `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the two biases in the
  Goldilocks backtest's universe rule.
