---
title: "Tests of Mean-Variance Spanning"
authors: Kan, Zhou
year: 2012
venue: Annals of Economics and Finance 13(1), 139–187 (peer-reviewed field journal; venue tier 2 by this folder's rubric, but the core results are theorems with exact finite-sample distributions plus a 100,000-path simulation study, not an empirical regularity)
url: http://aeconf.com/articles/may2012/aef130105.pdf (published version; working-paper DOI https://doi.org/10.2139/ssrn.231522)
citations: 32 (Semantic Scholar, by the working-paper DOI 10.2139/ssrn.231522, checked 2026-09-23); Crossref 15 for the same DOI (checked 2026-09-23). **Both counts are for the SSRN record only and undercount the article.** The published Annals of Economics and Finance version carries no registered DOI, so it is indexed as a separate work that neither index resolves by identifier; OpenAlex, which is where a split work is normally reconciled, returned HTTP 429 "Insufficient budget" (daily allowance exhausted) and Semantic Scholar's title-search endpoint returned HTTP 429. Per the rubric, tier is not downgraded on an index gap alone.
sample_period: methodological — exact distributions, power functions and simulations; two illustrations use monthly data (a two-asset benchmark frontier estimated 1926–2006, and an international diversification application 1970–2007)
markets: none material — NYSE equal- and value-weighted indices as a stylised benchmark pair, and seven international equity indices in the application
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

Huberman–Kandel say *what* to test. This paper says **what the test can and cannot see**, and
the answer is the sharpest methodological result this folder has filed against the lab's
current blocker.

Set up as in the previous note: benchmark returns `R₁` (`K` assets), test returns `R₂`
(`N` assets), regression `R₂ = α + β R₁ + ε`, `δ = 1_N − β 1_K`, `Σ = Var[ε]`, and the spanning
null `H₀ : α = 0, δ = 0`.

**1. The two restrictions are the two frontier portfolios, exactly.** Kan and Zhou compute the
weights the test assets receive in the two canonical frontier portfolios of the combined set:

```
weight of test assets in the tangency portfolio          ∝ Σ⁻¹ α
weight of test assets in the global-minimum-variance pf  ∝ Σ⁻¹ δ
```

So `α = 0` *is* the statement "the tangency portfolio holds none of the candidate" and `δ = 0`
*is* "the global-minimum-variance portfolio holds none of it". With `N = 1`, `Σ` is a scalar —
the candidate's **residual variance against the incumbent** — and the optimal tilt toward the
candidate is `α / σ²_ε`, not any fixed blend weight. Two frontier portfolios holding zero of the
candidate implies, by two-fund separation, that *every* frontier portfolio holds zero of it.

**2. All invariant tests are functions of two eigenvalues, and the eigenvalues are Sharpe
ratios.** Let `λ₁ ≥ λ₂ ≥ 0` be the eigenvalues of `Ĥ Ĝ⁻¹` (with `Ĥ = Θ̂ Σ̂⁻¹ Θ̂'`,
`Θ = [α, δ]'`). Then

```
LR = T Σ ln(1 + λᵢ)      W = T Σ λᵢ      LM = T Σ λᵢ/(1 + λᵢ)
```

and, with `θ̂(r)` the sample Sharpe of the tangency portfolio of all assets and `θ̂₁(r)` that of
the benchmark alone,

```
λ₁ = max_r [ (1 + θ̂²(r)) / (1 + θ̂₁²(r)) ] − 1
λ₂ = min_r [ (1 + θ̂²(r)) / (1 + θ̂₁²(r)) ] − 1
```

`λ₁` is the **largest** squared-Sharpe improvement available anywhere along the frontier, `λ₂`
the **smallest**. In finite samples `W ≥ LR ≥ LM` always, so the three can disagree.

**3. The power result, and it is the one that matters here.** With a single test asset
(`N = 1`, so `λ₂ = 0`) all three tests are increasing transformations of one `F` test, whose
non-central distribution has noncentrality `T·ω` with

```
ω = (Θ' Ĝ⁻¹ Θ) / σ²          σ² = residual variance of the test asset
  = (c − c₁)/ĉ₁  +  [θ²(μ̂_g₁) − θ₁²(μ̂_g₁)] / (1 + θ̂₁²(μ̂_g₁))
      └── GMV channel ──┘     └────── tangency channel ──────┘
```

where `c = 1'V⁻¹1` for the combined set and `c₁` for the benchmark (the reciprocals of the
global-minimum-variance variances), and the bracketed term is the gain in the squared slope of
the frontier's asymptote.

**The two channels do not contribute equally, and the asymmetry is enormous.** In the authors'
stylised two-benchmark illustration, a test asset that merely shaves a few percent off the
global-minimum-variance standard deviation — geometrically a barely visible change to the
opportunity set — produces `ω = 0.161`, almost all of it from the first term. A test asset that
**doubles the slope of the frontier's asymptote** — an enormous economic improvement, the
tangency Sharpe twice as large — produces `ω = 0.0299`, a fifth as much.

The reason is stated plainly and it is the Merton (1980) point: `c − c₁` depends on `V` only,
and covariances are estimated far more accurately than means; the tangency term depends on both
`μ` and `V`, and is therefore mostly sampling error. So:

> **A spanning test detects variance improvements easily and mean improvements barely. Statistical
> significance and economic significance are not merely imperfectly aligned here — for realistic
> alternatives they are close to *anti*-aligned.**

Kan and Zhou draw the two-sided conclusion themselves: a low p-value does not imply an
economically important frontier shift, and **a high p-value does not imply the test assets add
little**.

**4. Fat tails make it worse, asymmetrically.** Under multivariate Student-`t` returns the
asymptotic variance of `α̂` is almost unchanged from the normal case, but that of `δ̂` is much
larger. Consequences: (a) the non-robust Wald test of *spanning* is badly oversized — the limit
of its expected bias is about `1/(ν − 4)`, so ~100% at `ν = 5` and ~16.7% at `ν = 10` — whereas
the same adjustment barely matters for a test of `α = 0` alone; (b) the *power* loss from fat
tails falls almost entirely on the `δ` channel. Even so, a small GMV difference remains easier
to detect than a large tangency difference.

## Construction recipe

**The N = 1 correction — read this before running anything.** Kan and Zhou open by flagging two
common mistakes in applied use of the Huberman–Kandel test, and the second is exactly the case
a one-champion, one-candidate lab is in:

```
N ≥ 2 :  (U^(−1/2) − 1) · (T − K − N)/N        ~ F(2N, 2(T−K−N))
N = 1 :  (1/U − 1) · (T − K − 1)/2             ~ F(2, T−K−1)      ← the correct one
```

The first form "has been used to test the spanning hypothesis in the literature for `N = 1`" and
**is not valid there**. (The other flagged mistake: the test statistic is often miscomputed
because of a typo in the original 1987 paper.) Small-sample corrections for the three asymptotic
statistics: replace `T` by `T − K − (N+1)/2` for LR, `T − K − N + 1` for W, `T − K + 1` for LM.

**The step-down test — the part to actually adopt.** Rather than the joint test, run the two
restrictions sequentially and report both:

```
F₁ = ((T−K−N)/N) · (|Σ̄|/|Σ̂| − 1) = ((T−K−N)/N) · (â − â₁)/(1 + â₁)   ~ F(N, T−K−N)
      tests α = 0                     â  = squared tangency Sharpe, all assets
                                      â₁ = squared tangency Sharpe, benchmark only

F₂ = ((T−K−N+1)/N) · (|Σ̃|/|Σ̄| − 1)                                   ~ F(N, T−K−N+1)
      tests δ = 0 conditional on α = 0
```

`F₁` and `F₂` are **independent** under the null, so a step-down run at sizes `α₁`, `α₂` has
overall size `α₁ + α₂ − α₁α₂`. `F₁` is the GRS statistic (Gibbons–Ross–Shanken 1989,
*Econometrica* 57, 1121–1152, DOI 10.2307/1913625 — **not read**, paywalled at JSTOR and refused
by ResearchGate with HTTP 403; its identity is taken from Kan–Zhou, who derive it); **with
`N = 1` it has one numerator degree of freedom and is therefore the square of the ordinary
`t`-statistic on `α̂`.**

Two benefits, both of which the lab wants:

1. **You learn which channel caused the rejection** — tangency (`F₁`) or global-minimum-variance
   (`F₂`).
2. **You can set the two sizes differently**, according to which channel you consider
   economically important, instead of letting the relative *statistical accuracy* of `α̂` and
   `δ̂` decide it for you — which is what the joint test does, and why the joint test's power
   function is the wrong shape.

**Power calibration, as a property of the `F` distribution (no market content).** For a single
test asset at 5% size, achieving ≥50% rejection probability needs `ω* = Tω/(T−K−1)` above
roughly `0.089` at `T − K = 60`, `0.043` at `120`, `0.022` at `240`.

**Without normality.** Kan and Zhou give GMM versions. Their finite-sample finding is worth
copying: the general GMM Wald `W_a` requires estimating a large `S₀` matrix and performs badly —
often over-rejecting *more* than the non-robust test — once `N` is not small; the
elliptical-distribution GMM Wald `W_a^e` behaves much better. **Prefer the elliptical correction
over the general one when `N` is not tiny relative to `T`.**

## Robustness evidence (qualitative only)

- Analytic results with proofs in the appendix; exact finite-sample null distributions for all
  three statistics; power functions derived, not simulated, for the normal case; simulation
  (100,000 paths) for the non-normal case. For a methods paper this is the strongest available
  form of evidence and it does not decay.
- The power functions are computed **conditional on `Ĝ`**, i.e. on the realised benchmark
  frontier — the same conditioning GRS use. Unconditional power is not what is reported.
- The paper's central negative claim (statistical significance ≠ economic significance for
  spanning tests) is a statement about sampling error in `μ̂` versus `V̂`, which is one of the
  most robust facts in the estimation literature and is independent of market, period or asset
  class.
- **Limitation**: the analysis assumes `α` and `β` constant over the window, exactly as
  Huberman–Kandel do, and says nothing about what a regime shift in `β` does to either channel.
- **Limitation**: everything here is about *unconstrained* frontiers. A long-only investor's
  frontier is a different object; see tonight's third note.

## Implementability here

**This is the most directly useful thing in tonight's session, and it is free — one OLS
regression on two stored daily return series, no trial, no holdout.**

The lab's standing structural finding (`experiments/learnings.md`, 2026-09-22) is that as a
candidate leg becomes more decorrelated from the champion, the best blend cell's gain and
Memmel's paired standard error rise together, so the `t` barely moves. This paper supplies a
**second, independent explanation of the same phenomenon**, and it is a more general one:

> The quantity the lab is trying to resolve is a **difference of tangency Sharpe ratios** — the
> `α` channel. That channel is the one whose sampling error is dominated by the error in
> estimated *means*. The literature's own power analysis says it is very hard to detect **even
> when the true improvement is large**: an alternative that doubles the tangency slope is barely
> rejectable at realistic sample lengths. The lab is not failing to find an effect; it is
> scoring on the channel that its data, or anyone's data, cannot resolve.

Three concrete things to do with this, in order of cheapness:

1. **Run the step-down decomposition on the seated family lead against the champion.** `K = 1`
   (champion daily net returns), `N = 1` (the lead's). Report `F₁` (tangency) and `F₂`
   (GMV | α=0) separately, with the **`N = 1` F form above**, not the `N ≥ 2` one. This costs
   nothing, spends no trial, reads no holdout, and it partitions the lab's null: "the leg is
   worthless" and "the leg is valuable through the variance channel and the Sharpe gate cannot
   see it" are different answers and the lab currently cannot tell them apart.
2. **Report `α̂ / σ̂_ε` — the appraisal ratio — alongside every `ρ_to_champion`.** For a leg with
   `β ≈ 0` against the champion, `α ≈ μ_leg` and `σ_ε ≈ σ_leg`, so the appraisal ratio collapses
   to the leg's **standalone** Sharpe. This is the same conclusion the lab reached empirically
   ("what the blend route needs is a leg that is decorrelated **and** much better standalone")
   arrived at from the frontier geometry, and it says the lab's reading is right rather than
   pessimistic. Decorrelation alone moves `ω` not at all if `α` does not move with it.
3. **Do not let the `δ` channel become a promotion argument without a Sharpe argument.** The
   detectable channel is variance reduction. But this repo's gate scores a Sharpe ratio, and a
   variance reduction only raises a Sharpe ratio if the mean does not fall in proportion. A
   candidate that rejects on `F₂` and not `F₁` has demonstrated that it changes the
   global-minimum-variance portfolio — which is **not** what `engine/protocol.py` scores. Say
   so in the hypothesis line rather than discovering it at the gate.

**Pitfalls, stated because each one is reachable from here:**

- **Daily returns are fat-tailed, and the fat-tail penalty lands on the `δ` channel.** If the
  step-down is run on daily data with a normal-theory `F₂`, the GMV verdict is the unreliable
  one, not the tangency verdict. Use the elliptical GMM version, or run the step-down on
  monthly-aggregated returns and accept the shorter `T`.
- **This does not license a promotion.** The gate is a fixed-weight Sharpe comparison and
  Memmel/Ledoit–Wolf is the correct statistic for it. A spanning rejection is a *diagnostic* —
  it says the optimal book would hold some of the leg — and the optimal weight `α/σ²_ε` is
  itself an estimate with all the instability the folder's naive-vs-optimized note documents.
  Treat a rejection as a reason to keep working on a family, never as a substitute for the gate.
- **Two tests on the same pair of series is two tests.** The step-down's overall size is
  `α₁ + α₂ − α₁α₂`, and the lab's deflated-Sharpe bookkeeping should see a free diagnostic as a
  free diagnostic — it is not a scored trial, but it is a look, and a decision taken on it is a
  selection.
- **Do not run this on the holdout.** It is a frontier comparison on realised returns and it is
  exactly the kind of "just checking" `CLAUDE.md` forbids.

## Related

- **`research/notes/2026-09-23-mean-variance-spanning-and-intersection.md`** — the hypothesis
  this paper analyses. Read that first.
- **`research/notes/2026-09-23-spanning-under-short-sales-and-costs.md`** — the long-only
  version. Note the interaction: the constrained test is one-sided, which *recovers* some of
  the power this paper says the tangency channel lacks.
- **`research/notes/2026-08-24-testing-differences-of-sharpe-ratios.md`** — Ledoit–Wolf's point
  that the Jobson–Korkie/Memmel closed form is liberal under non-normality and serial
  dependence is the same warning as this paper's Section on Student-`t` returns, arriving at the
  same place from a different statistic. Both say: the normal-theory closed form understates
  the error bar on daily financial returns.
- **`research/notes/2026-08-17-naive-vs-optimized-weighting.md`** — why `α/σ²_ε` as an
  *implemented* weight is far less attractive than as a *test* quantity.
- **`research/notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md`** and
  **`research/notes/2026-09-09-nonstandard-errors-evidence-generating-process.md`** — the lab's
  measured construction non-standard error is the same kind of object as `ω`'s denominator: a
  floor on what any difference of estimated means can resolve.
- **`experiments/learnings.md` [2026-09-22]** — "the blend route does not become more resolvable
  as the leg becomes more decorrelated — it moves along a ray". This paper explains the ray:
  both the gain and the error bar on a tangency improvement are governed by the error in
  estimated means, and decorrelation changes neither.
