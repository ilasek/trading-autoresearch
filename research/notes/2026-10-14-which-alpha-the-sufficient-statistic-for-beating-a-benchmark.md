---
title: "Which Alpha?"
authors: Barillas, Shanken
year: 2017 (NBER working-paper version November 2015)
venue: "Review of Financial Studies 30(4), 1316–1338 — venue tier 1. Read as NBER Working Paper 21698, which carries the full argument and both propositions"
url: https://doi.org/10.1093/rfs/hhw101 · full text read at https://www.nber.org/system/files/working_papers/w21698/w21698.pdf
citations: "377 (Crossref is-referenced-by-count for 10.1093/rfs/hhw101, checked 2026-10-14)"
sample_period: "n/a — the content is two propositions in portfolio algebra; the illustrative numbers are US equity, 1963–2013, and none of them is recorded here"
markets: "US equity factors and decile test portfolios, in the illustrations only"
tier: "A — tier-1 venue, heavily cited, and the central claim is a proof rather than an estimate, so it cannot decay. The empirical illustrations are single-market and are not used below"
validation_overlap: false
published_post_2018: false
---

## Access

Read in full as NBER WP 21698 (198 KB; `pdftotext -layout` → 57 KB clean text; `" the "` count
517 raw, so no Caesar-shift; `( )`-dropout check zero, displayed algebra intact). The published
RFS version was not fetched and nothing below depends on it; the working paper states the
propositions, the proofs and the conclusions in full. A Tsinghua PBCSF mirror of the same title
also returned HTTP 200 but extracted to 5 KB and was discarded — **a 95 KB PDF that yields 5 KB
of text and seven instances of `" the "` is a cover page or a slide deck, not the paper**, and the
character count caught it where `file` did not.

## Mechanism

This is not a strategy. It is the answer to the question protocol v3 forces on every candidate:
**what statistic decides whether a book is better than the portfolio it is graded against?**

The paper's object is model comparison — two sets of traded factors, and a set of test assets to
judge them on. Its result is that the test assets are **irrelevant**. Everything follows from one
identity, due to Gibbons, Ross and Shanken (1989), which the paper quotes as its equation (2):

> `α′ Σ⁻¹ α = Sh(f, R)² − Sh(f)²`

where `α` and `Σ` are the intercepts and residual covariance from the time-series regression of
the test-asset excess returns `R` on the factor excess returns `f`, and `Sh(·)²` is the **maximum
squared Sharpe ratio** attainable from portfolios of the given returns plus the risk-free asset.
Read right to left: *the quadratic form in the alphas is exactly the improvement in squared Sharpe
ratio that adding the test assets to the factors would buy.* A non-zero alpha is not a
disagreement with a model; it is a measured amount of frontier expansion.

**Proposition 1 (test-asset irrelevance).** For a model `M1` nested in a larger `M`, "`M1` prices
both the test assets and the excluded factors" holds **if and only if** the excluded factors
satisfy `M1` *and* the larger model prices the test assets. The second clause is common to both
models being compared, so it cancels. What distinguishes the models is only **how well each prices
the factors the other one has and it lacks.** The paper shows the same cancellation for the
statistical likelihood and for the modified Hansen–Jagannathan distance of Kan–Robotti, and notes
(its footnote 8) that the GRS measure is a *sum* of a function of the excluded-factor alphas and a
function of the test-asset alphas, with no interaction — which is why the second term drops out of
a difference. The authors are candid that they and their colleagues found this counter-intuitive.

**The two-portfolio corollary, which is the form the lab needs.** Take `f` to be a single
benchmark `B` (one portfolio) and `R` to be a single candidate book `C`. Regress `C`'s excess
returns on `B`'s: `C = α + βB + ε`, with residual volatility `σ_ε`. Then

> `Sh(B, C)² = Sh(B)² + (α / σ_ε)²`

The quantity `AR ≡ α / σ_ε` is the **appraisal ratio** — the whole of what `C` adds. Three
consequences follow by algebra alone, and all three are statements about the lab's own gate:

1. **The exact frontier-expansion condition is `SR_C > ρ · SR_B`**, not `SR_C > SR_B`. Writing
   `β = ρ σ_C / σ_B` gives `α = σ_C (SR_C − ρ SR_B)`, so `α > 0` exactly when the candidate's own
   Sharpe exceeds the benchmark's **scaled down by their correlation**. A standalone-Sharpe
   difference is therefore **sufficient but not necessary** for the candidate to improve on the
   benchmark in a mean-variance sense: `SR_C > SR_B` implies `α > 0` (because `ρ ≤ 1`), but the
   converse fails whenever `ρ < 1`.
2. **A long-only, unlevered blend is enough to capture it.** Let `w(κ) = (1 − κ)B + κC`, which is
   long-only and fully invested for `κ ∈ [0, 1]` whenever `B` and `C` are. The derivative of
   `w(κ)`'s Sharpe ratio at `κ = 0` has the **sign of `α`** (the active portfolio `d = C − B` has
   the same alpha on `B` as `C` does, so `d(SR)/dκ |₀ ∝ σ_B² α`). No leverage, no short position
   and no estimated covariance matrix is required to turn a positive alpha into a higher Sharpe
   ratio. The Sharpe-maximising mix has the closed form
   `κ* = (μ_d σ_B² − μ_B σ_Bd) / (μ_B σ_d² − μ_d σ_Bd)` with `d = C − B`; if `κ* ≥ 1` the best
   feasible blend is the candidate itself and blending buys nothing.
3. **The prize is second-order in the appraisal ratio.** `Sh(B,C) − Sh(B) = √(SR_B² + AR²) − SR_B
   ≈ AR² / (2 SR_B)`, and the long-only constraint can only reduce it. So the gap between "expands
   the frontier" and "beats the benchmark standalone" is real but **small**: an appraisal ratio
   that would be respectable in a long-short setting converts into a Sharpe increment one order of
   magnitude smaller. This is the honest counterweight to consequence 1.

## Construction recipe

Everything here is computable from two return series and costs no trial.

1. **Compute the benchmark's and the candidate's daily excess returns over the same days**, on
   the train split only.
2. **Regress candidate on benchmark** (ordinary least squares, intercept free). Record `α` (per
   day, annualise by × 252), `β`, `σ_ε` (annualise by × √252) and `ρ`.
3. **Report the appraisal ratio `AR = α / σ_ε`** alongside, not instead of, the Sharpe difference.
   `AR²` is the squared-Sharpe increment; `√(SR_B² + AR²) − SR_B` is the attainable Sharpe gain
   with unconstrained mixing, and the `κ*` above gives the long-only attainable part.
4. **To compare two candidates with each other, regress each on the other.** Proposition 1 says
   any third set of portfolios — the pool, a factor set, a basket of previous trials — contributes
   nothing to the comparison once both directions of that pairwise regression are in hand. A
   candidate that prices the other's returns while the other cannot price its own is the better
   one, whatever either scores against a common third object.
5. **Inference on the difference is a separate problem and is already in this folder.** The
   increment is an estimate; its standard error is not the regression's reported one when returns
   are non-normal or autocorrelated — see `notes/2026-08-24-testing-differences-of-sharpe-ratios.md`
   and `notes/2026-09-23-spanning-test-power-and-step-down.md`, which are the matching test
   machinery for exactly this quadratic form.

## Robustness evidence (qualitative only)

- **The core content is a proof.** Proposition 1 and the GRS identity hold in any sample, in any
  market, for nested and non-nested model pairs alike, and under the stated assumption that the
  chosen metric has no interaction between excluded-factor alphas and test-asset alphas — which
  the paper verifies for the likelihood, the Sharpe criterion and the modified HJ distance.
- **What the proof does *not* carry.** The identity is about population moments. Every term —
  `α`, `σ_ε`, `ρ`, `SR_B` — is estimated, and the maximum squared Sharpe ratio is the single most
  upward-biased statistic in this folder's experience (`notes/2026-08-24-deflated-sharpe-ratio.md`,
  `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md`, whose
  theorems prove the Sharpe ratio converges more slowly than the weights do). Treating a measured
  `AR` as the available prize is the same error the deflated-Sharpe literature exists to prevent.
- **One known limitation the authors raise themselves.** Their comparison is among *given* models;
  it says nothing about whether either is any good. "We do not presume that any of the models under
  consideration is perfect." A candidate can win the pairwise comparison and still be worthless.
- **Replication status: not applicable in the usual sense.** The algebra has been absorbed into the
  standard toolkit (it is the premise of the whole net-of-cost model-comparison literature — see
  `notes/2026-10-14-net-of-cost-model-comparison-and-the-concave-frontier.md`, where its scope limit
  is established). 377 citations record adoption, not independent re-measurement.

## Implementability here

- **The statistic v3 uses is sufficient but not necessary, and this is the one place where the gate
  is stricter than the economics.** v3 scores **skill** = candidate validation Sharpe − equal-weight
  eligible pool's Sharpe on the same days. By consequence 1, a candidate whose skill is slightly
  negative can still expand the pool's frontier — precisely when `SR_C > ρ SR_B` with `ρ < 1`. For a
  concentrated book drawn from the same panel, `ρ` is high but not one, so the admissible region is
  a thin band below the gate rather than a wide one.
- **The construction that converts the band into a passing book is a blend toward the pool, and it
  is legal under the protocol.** A candidate may emit `w = (1 − κ) · (equal weight over eligible) +
  κ · (its tilt)`; the row is long-only, fully invested and monthly, and the pool's own measured
  turnover on this panel is small, so the blend's cost bill is near the tilt's own. This is the
  construction `#241` (confidence-weighted blending toward the benchmark) was already pointing at
  from the Black–Litterman side; `Which Alpha?` supplies the κ and the exact condition under which
  any κ > 0 helps.
- **But read consequence 3 before writing it.** The attainable Sharpe increment is `≈ AR²/(2 SR_B)`
  and the long-only κ makes it smaller. **A candidate that cannot beat the pool standalone will not
  be rescued into a *large* skill number by blending** — it can only be moved from slightly
  negative to slightly positive, and the deflated-skill bar is on the far side of that. So the
  honest use of this note is as a **pre-trial screen on the alpha, not as a rescue mechanism**: a
  candidate with `α ≤ 0` against the pool on train cannot help under any blend and should not be
  written; a candidate with `α > 0` but negative standalone skill is worth exactly one trial at the
  `κ*` computed on train, pre-registered.
- **Two interactions with the v3 gate set that must be stated before any such trial.** *(i)* The
  random-selection null replaces the names a candidate *enters* with same-region, same-type peers
  and keeps the schedule and the weight vectors, so a blended book's replicas are "pool + random
  tilt" and the percentile still prices the selection — but as `κ → 0` both the skill advantage and
  the separation from the replicas shrink together, so **κ trades skill magnitude against null
  power** and an extreme-small κ fails the null gate by construction (the lab's own measured fact
  that a near-full-pool book cannot clear a null that randomises its own names). *(ii)* Train skill
  must be above zero at the *same* κ; the blend is not a validation-only device.
- **The leaderboard consequence is free and is the part that applies tonight.** Ranking trials by
  skill against a common pool is **not** a comparison of the trials. By Proposition 1, the pool
  cancels: to decide whether candidate A or candidate B is the better bet, regress each one's
  active return on the other's and look at the two alphas. This is a sharper version of the rule
  `CLAUDE.md` already states ("family leads whose active returns correlate are one bet, whatever
  their labels") — correlation says they are the same bet, the pairwise alphas say which one to
  keep, and `scripts/rank_trials.py`'s tier-1 set is the set where neither direction is decisive.
- **Family placement.** Cross-family methodology — `portfolio-learning` if it must be filed under
  one. It proposes no signal.

## Related

- `notes/2026-09-23-mean-variance-spanning-and-intersection.md`,
  `notes/2026-09-23-spanning-test-power-and-step-down.md`,
  `notes/2026-09-23-spanning-under-short-sales-and-costs.md` — the spanning trilogy. Spanning asks
  whether `α = 0` for *all* new assets; this note is the one-asset version with the increment made
  explicit, and the three spanning notes supply the inference and the long-only caveats.
- `notes/2026-10-14-net-of-cost-model-comparison-and-the-concave-frontier.md` — the scope limit:
  the squared-Sharpe criterion here survives proportional costs and fails under price impact.
- `notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md`,
  `notes/2026-10-12-black-litterman-benchmark-anchored-tilting.md` — the other two routes to a
  benchmark-anchored book; `κ` here is the same knob the tracking-error frontier calls `κ` and
  Black–Litterman reaches by reverse optimisation.
- `notes/2026-08-24-deflated-sharpe-ratio.md`,
  `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md` — why the
  measured increment is an upper bound.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the matching inference.
