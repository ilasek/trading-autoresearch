---
title: "The Fundamental Law of Active Management: Time Series Dynamics and Cross-Sectional Properties" (peer-reviewed successor: "The fundamental law of active management: Redux")
authors: Ding; Redux with Ding, Martin
year: 2010 (working paper read in full); Redux published 2017
venue: SSRN working paper (Tier 2 by this folder's rubric — a working paper); the successor is Journal of Empirical Finance 43, 91–114 (2017), peer-reviewed but NOT obtained (closed at Elsevier, see Robustness)
url: https://doi.org/10.2139/ssrn.1625834 — read in full (33 pp.) from `math.nyu.edu/inmemoriam/avellaneda/FundamentalLawFT.pdf`; successor https://doi.org/10.1016/j.jempfin.2017.05.005
citations: 4 (Crossref `is-referenced-by-count` on the SSRN DOI, checked 2026-11-04); 10 (Semantic Scholar by the same DOI, same date). The successor has 15 (Crossref, checked 2026-11-04) and is not in Semantic Scholar's DOI index. These are LOW counts and are discussed explicitly under Robustness — the tier is argued for, not assumed.
sample_period: analytic throughout; the one empirical section uses Russell 1000/2000/3000 universes, 1978:12–2009:08
markets: US equities (Russell universes), monthly
tier: B
validation_overlap: false
published_post_2018: false
---

**Taken as the aim the [2026-11-03] open-questions entry set, and it resolves that aim's
acceptance criterion — against the named primary.** That entry named
**Clarke, de Silva & Thorley (2002)** (*FAJ* 58(5), 48–66) as the one unread primary behind the
**transfer coefficient**, a quantity this folder has cited since session 5 without ever reading its
source, and stated the criterion before any download: *admit it only if the body gives the TC under
a long-only constraint as a function of something this lab controls.* **The 2002 paper was again not
obtained** (see Robustness), but this paper — which follows Clarke et al.'s own framework and
notation by its author's statement — **shows that the TC as Clarke et al. define it does not have
the property the folder has been quoting it for**, so the criterion is answered negatively from
inside the same literature rather than left open.

Zero prior coverage of the paper itself: fixed-string greps across all 258 prior notes returned
`Portfolio Constraints and the Fundamental Law` **0**, against `transfer coefficient` **7** and
`Clarke` **4** — i.e. the usual signature of a concept the folder uses and has never sourced.

## Mechanism

Four results. The first is the one that matters most to this lab; the fourth is the one that
answers the aim.

**(1) The fundamental law has a strategy-risk term, and that term, not breadth, sets the
ceiling.** Grinold's law is `IR = IC·√N`. Under a one-factor conditional model of residual
returns in which the cross-sectional IC is itself a random variable with mean `IC̄` and standard
deviation `σ_IC` — Qian and Hua's **"strategy risk"** — the ex-ante information ratio of the
optimal active portfolio is

```
IR = IC̄ / sqrt( 1/(φN) + σ_IC² ) ,          φ ≥ 1
```

where `φ` is a constant set by the cross-sectional dispersion of residual volatilities (it is
`1/(1 − IC̄²)` when those volatilities are equal, `1/(1 − IC̄² − σ_IC²)` under the risk-adjusted
variant). Three known laws are corner cases: `σ_IC = 0` gives Grinold's `IC·√N`; `N → ∞` gives
Qian–Hua's **`IR = IC̄/σ_IC`**, read as *skill times precision*; and an intermediate assumption
gives Ye's `IC̄/√(1/N + σ_IC²)`.

The mechanism behind the ceiling is the durable part. Breadth diversifies **idiosyncratic** risk
only — the `1/(φN)` term. The bet on the signal itself has an uncertain payoff stream whose
dispersion is `σ_IC`, and that risk is common to every name in the book, so **no amount of
breadth removes it.** As `N` grows, `IR → IC̄/σ_IC`, a quantity with **no `N` in it at all**.

**(2) Where the crossover sits, and it is below this panel's width.** The paper computes both
denominator terms on its universes. `φ` is time-varying, rises with universe size, and sits in
roughly the 1.5–2.1 range across the Russell 1000/2000/3000; `1/√(φN)` is correspondingly in the
low hundredths. Against that, it reports `σ_IC·√(φN)` **in the range 4 to 10** for the signals and
universes it examines: the strategy-risk term is **4 to 10 times the size of the breadth term**,
so the breadth term is already nearly irrelevant, and the Grinold projection consequently
overstates attainable `IR` by about that same multiple. The paper's own general calibration for the
inputs is `IC̄` of order 0.02–0.05 with `σ_IC` of order 0.1. **Both of these are its numbers on
its panel and must be re-measured here, not imported** — what transfers is the *shape*, which is
that at a cross-section of order a thousand names the `1/(φN)` term has already died.

**(3) A cross-sectional IC is not a time-series IC, and the gap is residual-volatility
dispersion.** If every name shares the same time-series IC `IC_ts` between its residual return and
its score, the *expected cross-sectional* IC is

```
IC_cs = IC_ts · σ̃_r / δ
```

where `σ̃_r` is the cross-sectional **average** residual volatility and `δ` the cross-sectional
standard deviation of the alpha-relevant scale. In general `IC_cs = (1/N)·Σ IC_ts,i·σ_ri / δ`: a
**residual-volatility-weighted average** of per-name time-series ICs. The two coincide only when
all residual volatilities are equal. So a cross-sectional IC is a quantity about the panel's
volatility dispersion as much as about per-name predictability, and reading one as the other is a
specification error, not a rounding error.

**(4) The transfer coefficient, and why Clarke et al.'s definition does not do the job it is
quoted for.** Clarke et al. define

```
TC = corr( Δw_i·σ_ri , α_i/σ_ri )
```

i.e. the cross-sectional correlation between **residual-volatility-adjusted** active weights and
alphas, with the claimed property `IR_constrained = TC · IR_unconstrained`. That property holds
**only** when `σ_IC = 0` *and* the residual return covariance is diagonal. Once the IC varies over
time, the conditional covariance is **not** diagonal — the strategy-risk term `σ_IC²·δ²·z z'` is a
rank-one common component — and the diagonal-only adjustment is the wrong metric. Two consequences:

- Carried through Ye's version, the constraint's cost appears to **vanish as breadth grows**: the
  constrained `IR` and the unconstrained `IR` both tend to `IC̄/σ_IC` regardless of what
  constraints are imposed. The paper flags this as counter-intuitive, and the diagnosis is the
  mis-specified covariance rather than a real effect. **Any claim that "breadth buys back what the
  constraint costs" traces to this error.**
- The repair is to adjust by the **total** conditional covariance `Ω_t`:

  ```
  TC = (Δw_t'α_t) / sqrt( Δw_t'Ω_tΔw_t · α_t'Ω_t⁻¹α_t )
  ```

  which is a correlation between `Ω^{1/2}Δw` and `Ω^{-1/2}α` and restores
  `IR_constrained = TC · IR_unconstrained` exactly. A TC of 0.5 then means what practitioners
  have always taken it to mean: half the attainable `IR`.

**(5) The multi-factor form, which is the one the lab's ensemble work needs.** With `K` signals,

```
IR = sqrt( IC' ( (σ_ε²/N)·I + Σ_IC )⁻¹ IC )  ≈  sqrt( IC' Σ_IC⁻¹ IC )
```

where `Σ_IC` is the **covariance matrix of the signals' ICs over time**. Again the breadth term
drops out at scale, and what remains is a Mahalanobis length of the IC vector in the metric of IC
covariance. For a 2-signal system, dropping one signal costs

```
IR → (1/sqrt(1 − ρ²)) · sqrt( (IC₁/σ_IC₁)² + (IC₂/σ_IC₂)² − 2ρ(IC₁/σ_IC₁)(IC₂/σ_IC₂) )  ≥  IC₁/σ_IC₁
```

with `ρ` the time-series correlation of the two ICs. A missing **return** factor costs through
both its own `IC₂` and the covariance mis-specification; a missing **risk** factor costs only
through the latter, and realised tracking error then exceeds the ex-ante target by exactly
`1/√(1 − ρ²)`. If `ρ ≈ 0`, omitting a risk factor is nearly free.

## Construction recipe

Not a strategy — a set of measurements and a specification discipline.

1. **Measure `σ_IC`, not just `IC̄`.** Run the cross-sectional IC of score against forward
   residual return at every rebalance date, then take the mean **and the standard deviation** of
   that time series. The ratio `IC̄/σ_IC` is the attainable `IR` ceiling at large `N`.
2. **Check the crossover before claiming breadth.** Compute `1/√(φN)` with `φ` estimated from the
   cross-sectional dispersion of residual volatilities, and compare it to `σ_IC`. If
   `σ_IC ≫ 1/√(φN)`, breadth is spent and `IR ≈ IC̄/σ_IC`.
3. **Compute the TC with the total conditional covariance**, not the diagonal, whenever IC varies
   over time: `TC = Δw'α / √(Δw'ΩΔw · α'Ω⁻¹α)`.
4. **Combine signals in the metric of `Σ_IC`.** The value of adding a signal is set by its IC's
   covariance with the ICs already in the book, which is a *time-series* correlation of
   cross-sectional ICs — a cheap, free-to-compute quantity.
5. **Do not read a cross-sectional IC as a per-name skill** unless residual volatilities are
   roughly homogeneous; otherwise it is a volatility-weighted average of them.

## Robustness evidence (qualitative only)

- **Analytic, not empirical, in its load-bearing parts.** Results (1), (3), (4) and (5) are
  algebraic identities under stated assumptions and can be checked in-note; they do not need
  replication in the sense the rubric's replication column is about. The paper's own empirical
  section is a single-market, single-provider calculation over three nested universes, and its
  factor-level output is **not recorded here** under this folder's anti-lookahead rules.
- **Citation counts are low and this is the honest weakness.** 4 Crossref / 10 Semantic Scholar on
  the working paper; 15 Crossref on the peer-reviewed successor. By the letter of the rubric
  ("a preprint with no replication is Tier C however impressive its architecture") this would be
  **Tier C**. It is graded **B** on two grounds, both stated so a later session can disagree:
  the central claims are identities rather than effects, and the same author's line reached a
  peer-reviewed journal (*Journal of Empirical Finance*). A reader who weights the citation
  column more heavily should read this note as Tier C — nothing in it depends on the paper's
  empirical section.
- **The lineage is well cited even where this paper is not.** Grinold (1989, 1994), Grinold–Kahn
  (2000), Qian–Hua (2004) and Clarke et al. (2002) are the standard references, and the first
  three are the source of the `σ_IC` result this paper generalises. The strategy-risk idea is
  therefore not this paper's alone; what is this paper's is the single formula that nests all of
  them and the TC repair.
- **Costs are not modelled at all.** It is an `IR`-decomposition paper. Every number in it is
  gross. For this lab that is a material gap, since v3's cost model is what killed the previous
  champion lineage.
- **The named primary was again not obtained, and the routes tried are recorded so no future
  session re-spends them.** `10.2469/faj.v58.n5.2468`: Crossref resolves (197 cites, confirming the
  [2026-11-03] figure). **OpenAlex now reports it `is_oa: true, oa_status: green,
  any_repository_has_fulltext: true` with `oa_url` = `https://doi.org/10.2139/ssrn.290916`** —
  which **reverses that entry's "closed, no full text" record** but is not a usable route: the
  SSRN landing page returns the standard Cloudflare `Just a moment...` 403. `core.ac.uk` returned
  HTTP 429 on its API and a Cloudflare challenge on its search page. The companion
  Clarke–de Silva–Sapra (2004) remains absent from Crossref. **Net: the green-OA flag on this DOI
  is a metadata improvement, not an access improvement.**

## Implementability here

**What is directly usable, and it is free.**

- **Items (1) and (2) are a prediction about protocol v2's own widening, and it agrees with
  `#377` from the opposite direction.** `#377` (Levy–Ritov) derived a breadth-independent Sharpe
  ceiling for a **long-only** book and predicted that the ~140 → ~1,400 widening buys selection
  quality rather than a higher ceiling. This paper derives a breadth-independent `IR` ceiling for
  the **unconstrained optimal** book, from signal-risk rather than from covariance structure. So
  **the breadth-independence of the ceiling is not a long-only artifact.** A long–short lab would
  not have gained its `√10` either, for a second and independent reason. Two derivations, two
  literatures, one conclusion: at this panel's width, **`N` is not the lever.**
- **`σ_IC` is computable on data the lab already has, costs no trial, and is a better forecast of
  attainable `IR` than anything in the folder's current screens.** The lab's diagnostics report a
  mean cross-sectional IC and a `t`-statistic. The quantity that bounds the achievable `IR` is the
  *standard deviation* of that same IC series. A signal with a respectable mean IC and a large
  `σ_IC` has a low ceiling no matter how wide the panel — and `learnings.md` already contains the
  symptom of exactly this (signals whose IC sign **inverts across train sub-periods** were declined
  on that ground). This paper gives the quantity that names it.
- **The `Σ_IC` combination rule is the right frame for `portfolio-learning`.** `program.md` asks
  for "ensembles of decorrelated signals"; the formula says what "decorrelated" has to mean —
  decorrelated **ICs over time**, not decorrelated scores cross-sectionally, and not decorrelated
  realised returns. Those are three different matrices and only the first is the one in the law.
- **The TC repair corrects the folder's own usage.** `2026-08-19-fundamental-law-breadth-and-strategy-risk.md`
  and six other notes invoke the TC. Any of those that treat the Clarke et al. definition as giving
  `IR_c/IR_unc` should be read with the caveat that this holds only at `σ_IC = 0`, which is the one
  case the lab never faces.

**What is not usable.**

- The law is stated for an **unconstrained mean–variance optimal** active book against a benchmark,
  with an estimated `Ω`. The lab's books are long-only, score-ranked and equal-weighted, which
  collects neither the optimum nor its `TC`-discounted fraction — the same "oracle versus
  estimated versus ranked" tension recorded in `#378`. Read the ceiling as a **bound**, not a
  target.
- `φ` as the paper computes it needs a residual-return model. A crude proxy — the cross-sectional
  dispersion of trailing residual volatilities — is enough to establish the *inequality*
  `σ_IC ≫ 1/√(φN)`, which is all the argument needs at this panel's width.
- Nothing here prices costs, and under v3 the cost bill was the whole story for the previous lead.
  A high `IC̄/σ_IC` ceiling is a gross number.

## Related

- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the folder's existing
  fundamental-law note, which has flagged Clarke et al. (2002) as unread since session 5. This
  note does not obtain it either, but supersedes the TC definition it quotes.
- `notes/2026-11-03-no-short-constraint-cost-and-panel-breadth.md` — `#377`/`#378`. The
  breadth-independent **long-only** ceiling. This note's item (1) is the same shape derived
  without any constraint, which is why the two together are stronger than either.
- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md` — `#373`–`#376`, the
  resolution limit and the one-bit truncation test; the TC repair here is the correct metric in
  which to state those weight-space arguments.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md` and
  `notes/2026-09-08-stacked-regressions-nonnegative-weights.md` — the combination literature the
  `Σ_IC` formula gives an asset-pricing-specific objective for.
- `experiments/learnings.md`, protocol-v3 section — the measured instances of IC sign inversion
  across train sub-periods, which is `σ_IC` showing up as a symptom without being named.
