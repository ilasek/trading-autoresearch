---
title: "Generalized Deviations in Risk Analysis" + "Optimality Conditions in Portfolio Analysis with General Deviation Measures" — the axioms a non-symmetric spread measure must satisfy, the one extra axiom that buys coherence, and a tail beta that is computable from daily closes but whose equilibrium reading needs shorting
authors: Rockafellar, Uryasev, Zabarankin
year: 2006 (both)
venue: Finance and Stochastics 10(1), 51–74 (venue tier 1, peer-reviewed); Mathematical Programming 108(2–3), 515–540 (venue tier 1, peer-reviewed)
url: https://doi.org/10.1007/s00780-005-0165-8 and https://doi.org/10.1007/s10107-006-0721-9
citations: 458 for "Generalized deviations in risk analysis" and 88 for "Optimality conditions in portfolio analysis with general deviation measures" (Crossref `is-referenced-by-count`, both checked 2026-10-23)
sample_period: none — both are theory papers with no estimation and no empirical section of any kind. No sample, therefore no overlap with any window.
markets: not applicable (axiomatic / optimization theory)
tier: A
validation_overlap: false
published_post_2018: false
read: full text of both, again from Rockafellar's flat UW directory — `sites.math.washington.edu/~rtr/papers/rtr192-GeneralizedDeviations.pdf` (238 KB, 25 pages, Finance and Stochastics manuscript version; 74 KB of text, 361 `" the "`) and `sites.math.washington.edu/~rtr/papers/rtr198-PortfolioAnalysis.pdf` (260 KB, 23 pages, "Research Report # 2004-7", University of Florida Risk Management and Financial Engineering Lab, version 3 November 2004; 23 pages of clean text). Both `pdftotext -layout`, no ASCII shift, no `/xHH` escapes. Published versions not obtained; numbering below is the preprints'. The second preprint's title reads "GENERALIZED DEVIATION MEASURES" while the published article reads "general deviation measures" — the Crossref record resolved on the published wording, and the DOI above is the published one (my first guess, `10.1007/s10107-005-0684-2`, resolves to an unrelated paper on matrix sum-of-squares relaxations; a DOI guessed from a volume number is worth nothing).
---

## Mechanism

The previous two notes leave a gap. Artzner et al. axiomatise *risk* measures — functionals on the
position itself, with translation invariance tying them to a capital requirement. But a portfolio
constructor does not usually want a capital requirement; it wants a **spread** measure, something that
plays the role standard deviation plays in mean–variance, and that is allowed to treat downside
differently from upside. Standard deviation is translation-*invariant* in the wrong way for Artzner's
axiom T: `σ(X + C) = σ(X)`, not `σ(X) − C`. So standard deviation is not a coherent risk measure, and
neither is any recognisable generalisation of it. The axiomatics do not cover the object actually used.

This pair fixes that, and the fix is clean enough to state in full.

**Definition 1 (deviation measure).** `D : L²(Ω) → [0, ∞]` satisfying

- **(D1)** `D(X + C) = D(X)` for constants `C` — it measures spread, not level;
- **(D2)** `D(0) = 0` and `D(λX) = λD(X)` for `λ > 0` — positive homogeneity;
- **(D3)** `D(X + X′) ≤ D(X) + D(X′)` — subadditivity;
- **(D4)** `D(X) ≥ 0`, with `D(X) > 0` for non-constant `X`.

D2 + D3 is sublinearity, so **every deviation measure is convex**, which is the property that makes it
usable as an optimisation objective. D1 forces `D(X)` to depend only on `X − EX`. The authors note `D`
acts as a norm on the zero-mean subspace *except* that symmetry `D(−X) = D(X)` may fail — and failing
it is the whole point.

**Example 1** is the one to carry: standard deviation `σ(X) = ‖X − EX‖` satisfies all four, and so do
the **upper and lower semideviations**

```
σ₊(X) = ‖[X − EX]₊‖ ,    σ₋(X) = ‖[X − EX]₋‖
```

which are not symmetric. So the `L²` norm of the shortfall is a legitimate convex deviation measure.

**Definition 2 (lower range dominance), the extra axiom.** `D` is lower range dominated if

- **(D5)** `D(X) ≤ EX − inf X` for all `X`.

The authors state which of their examples satisfy it, and the list is the useful content: D5 **holds**
for `D(X) = EX − inf X` and for `σ₋`; it **fails** for `D(X) = sup X − EX` and for `σ₊` — and, the one
that matters, **it fails for `σ` itself.**

**Theorem 2, the bridge.** Deviation measures correspond one-to-one with "strictly expectation
bounded" risk measures under

```
(a) D(X) = R(X − EX)        (b) R(X) = E[−X] + D(X)
```

and — the punchline — **`R` is coherent if and only if `D` is lower range dominated.**

Read that against the first note and it settles the apparent contradiction there. `R(X) = −E[X] + σ(X)`
is the mean-variance objective and is **not** coherent, because `σ` is not lower range dominated; this
is the same failure Artzner et al. recorded under axiom M. `R(X) = −E[X] + σ₋(X)` **is** coherent,
because `σ₋` is. And Artzner et al.'s ruled-out "semi-variance type" measure
`−E[X] + σ((X − E[X])⁻)` is a *third* functional — it applies the standard-deviation operator
`σ(Z) = ‖Z − EZ‖` to the shortfall `Z`, where `σ₋` applies the plain norm `‖Z‖`. **Whether the
shortfall is centred before the norm is taken is the difference between subadditive and not.** (That
reconciliation is my reading of the two definitions placed side by side; neither paper says it about
the other.)

**Theorem 1, the dual form, and the object that makes it computable.** A lower semicontinuous deviation
measure is exactly one representable as

```
D(X) = EX − inf_{Q ∈ 𝒬} E[XQ]
```

over a **risk envelope** `𝒬` — non-empty, closed, convex, with `EQ = 1` for all `Q ∈ 𝒬`, and containing
for every non-constant `X` some `Q` with `E[XQ] < EX`. So every deviation measure is a worst case over
a family of re-weightings of the probability measure, and the familiar measures differ only in which
re-weightings are admitted. For **CVaR-deviation** (Example 3), `D(X) = CVaRα(X − EX)`, the envelope is

```
𝒬 = { Q : 0 ≤ Q ≤ α⁻¹ , EQ = 1 }
```

— re-weight any state up to `1/α` times its true probability, but no further. The corresponding risk
measure is `R(X) = CVaRα(X)`, coherent and strictly expectation bounded, as the previous note had it.

**Examples 4 and 5** close the family under mixing: `D(X) = ∫ CVaRα(X − EX) dλ(α)` for a weighting
measure `λ` on `(0,1)` is again a deviation measure, and in the atomic case

```
D(X) = λ₁·CVaR_{α₁}(X − EX) + … + λ_m·CVaR_{α_m}(X − EX),   Σλᵢ = 1, λᵢ > 0
```

is lower range bounded with `R(X) = Σ λᵢ CVaR_{αᵢ}(X)` coherent. Example 5 extends to a worst case over
a *collection* of such mixtures. The companion paper also records the spectral identity
`CVaRα(X) = α⁻¹ ∫₀^α VaR_p(X) dp` — CVaR is the average of VaR over all deeper levels — and the
minimisation form `CVaRα(X) = min_C { C + α⁻¹ E[X + C]₋ }`, the same auxiliary-variable device as the
previous note, with the argmin an interval whose endpoint is VaR.

**The companion paper's new object: risk identifiers.** For each `X`,

```
𝒬(X) = argmin_{Q ∈ 𝒬} E[XQ] = { Q ∈ 𝒬 : D(X) = EX − E[XQ] }
```

— the admitted re-weightings that "bring out the worst in `X`". These are the subgradients of `D`, and
they are what the first-order conditions are written in. For CVaR-deviation at level `α`, the risk
identifier is essentially determined (Example 4 of the companion): `Q*(ω) = α⁻¹` where
`X*(ω) < −VaRα(X*)`, `Q*(ω) = 0` where `X*(ω) > −VaRα(X*)`, and the boundary state takes whatever
value is needed for `EQ* = 1`. **The subgradient of CVaR is the normalised indicator of the tail** —
which is why, as the next section shows, every first-order condition it generates is a conditional
expectation over the worst `α` fraction of states.

## Construction recipe

**The generalised beta, and it is a tail beta.** The companion paper's Theorem 5 and Definition 3 give
CAPM-like optimality conditions in which the classical `β` is replaced by a `D`-specific coefficient.
For CVaR-deviation (its Example 8), with `X*` the optimal ("master fund") return and `rᵢ` an
instrument's return:

```
βᵢ = E[(E rᵢ − rᵢ) Q*] / CVaRα(X* − E X*)
```

and when `prob{X* = −VaRα(X*)} = 0` this reduces to a ratio of conditional expectations (their 5.11):

```
βᵢ = E[ E rᵢ − rᵢ | X* ≤ −VaRα(X*) ]  /  E[ E X* − X* | X* ≤ −VaRα(X*) ]
```

In words: **the name's mean shortfall, conditional on the reference portfolio being in its worst `α`
tail, divided by the reference portfolio's own mean shortfall over the same states.** It is a beta
estimated on a sub-sample selected by the *reference* series, not by the name's own. For the
semideviations (their Example 7) the analogous coefficients are `covar(−rᵢ, Q*)/D(X*)` with `Q*`
supported on the states where `X*` attains its lower range.

That is a complete recipe needing only (i) a reference return series, (ii) each name's return series,
(iii) a tail level. All three exist here from daily closes alone.

**The two optimisation recipes.** Either minimise `D(X)` subject to a return floor (the direct
generalisation of minimum-variance; an LP for CVaR-deviation and mixed CVaR-deviation, by the previous
note's formulation applied to the demeaned series), or use the first-order conditions in terms of risk
identifiers to characterise the optimum without solving it. The companion paper's §5 is explicitly
about the second.

## Robustness evidence (qualitative only)

Theory again, so robustness means correctness plus uptake, and both hold: 458 citations for the
Finance and Stochastics paper, a peer-reviewed venue of the first tier, and the deviation-measure /
risk-envelope framework is now the standard language for this family. The one-to-one correspondence in
Theorem 2 and the duality in Theorem 1 are the kind of result that is either right or visibly wrong,
and no subsequent literature disputes them. The spectral representation of CVaR and the
minimisation form are independently established (Acerbi, and the authors' own earlier paper).

The authors are notably careful about two places where *earlier* literature was not, and both are
recorded here because they are the limits that matter:

- **Non-uniqueness.** Mean absolute deviation lacks strict convexity, so the master fund need not be
  unique; the authors say so, and criticise a predecessor (Konno) for obtaining `β` coefficients
  "without confronting the possibility" of the extra term that arises on the set where the reference
  series exactly equals its mean. Non-strictly-convex deviation measures give optima that are *sets*,
  not points. CVaR-deviation is in this class.
- **The no-shorting multipliers, and this is the serious one.** Their own models `P(Δ)` and `P₀(Δ)`
  **do not impose `xᵢ ≥ 0`.** They note that Konno's model does impose it but that those constraints
  "are anyhow suppressed in the developments of [9] by assuming that the Lagrange multipliers
  associated with them can merely be taken to be 0, which amounts to a claim that nonnegativity will
  automatically follow from optimality. No support for such a claim is offered." They add that without
  shorting "the potential need for a master fund of negative type does not come into view." This is
  the authors drawing a boundary around their own result, and it is the boundary that bites here.

No decay and no replication question: there is nothing empirical to decay or replicate.

## Implementability here

**The headline, stated before the opportunities so it is not lost: the equilibrium reading of the
generalised beta does not survive this lab's constraint set, and the authors are the ones who say so.**
The master-fund and CAPM-like relations are derived without `xᵢ ≥ 0`. This repo is long-only with gross
≤ 1.0, so the nonnegativity multipliers are active for the overwhelming majority of a ~1,000-name
eligible cross-section — at any given rebalance most names are at the `xᵢ = 0` boundary — and the
authors' own critique of Konno is precisely that these multipliers cannot be waved away. **So formula
(5.11) must not be used as an asset-pricing relation or as an expected-return forecast here.** Doing
so would import an equilibrium conclusion from a model whose binding constraint the lab has and the
model does not.

**What survives, and it is the more useful half.** Formula (5.11) is *also* just a well-defined
statistic of two return series and a tail level — a conditional-shortfall ratio — and its definition
owes nothing to the optimality theory. As a **cross-sectional feature** it is computable, causal and
cheap:

- Take the reference series `X*` to be the **equal-weight eligible pool**, which under v3 is the
  benchmark every number is graded against. This is the right choice and it is not arbitrary: the
  gate measures skill relative to that pool, so a name's co-movement with the pool *in the pool's own
  worst states* is the risk the gate is implicitly net of.
- For each name, over a trailing window, compute the mean of `(E rᵢ − rᵢ)` restricted to the days on
  which the pool's return was in its worst `α` fraction, and divide by the pool's mean shortfall on
  those same days.
- That is one conditional mean per name over `T·α` days. No LP, no covariance matrix, no `N/T`
  problem — it is a univariate statistic per column and sidesteps every dimensional objection in the
  noise-sensitivity note.

**The arithmetic that decides whether it is worth writing, and it must be done first.** With a
two-year trailing window (`T ≈ 500`) and `α = 0.1`, the conditioning set is **50 days**; at `α = 0.05`,
**25 days**. Each name's `βᵢ` is a 25-to-50-observation mean. Two consequences:

1. **The cross-sectional dispersion of `βᵢ` will be dominated by sampling noise unless the window is
   long or `α` is loose.** `α = 0.2` on a three-year window gives ~150 conditioning days, which is
   defensible; `α = 0.01` is not implementable at any window this panel's history supports.
2. **The free screen to run before any candidate.** Compute `βᵢ` on this panel and measure its
   cross-sectional rank correlation with (a) ordinary full-sample beta to the pool and (b) trailing
   volatility. If the tail beta is a near-monotone function of plain beta — which is what the previous
   notes' normality argument predicts, since under joint normality all of these collapse to
   `(µ, σ)` functionals — **the vein is closed for weighting and selection, and the measurement cost
   was a handful of lines with no trial spent and no holdout read.** If it is not, the residual is the
   thing to build on, and it has a clean story: asymmetric co-movement with the benchmark in the
   benchmark's bad states, which is not what a variance-based gate can see.

**Three further implementability notes.**

- **Mixed CVaR-deviation is the right way to avoid choosing `α`.** Example 4 says a convex combination
  over several levels is still a deviation measure and still coherent in the `R` form. Averaging over
  `α ∈ {0.1, 0.15, 0.2}` is one line, keeps the LP an LP, and removes a tuned parameter — which, given
  that the deflated-Sharpe bar counts every trial, is worth more here than it would be elsewhere.
  This is the same temporal/parameter-breadth argument the folder has repeatedly found to be the
  robust move, applied to a tail level rather than a lookback.
- **Non-uniqueness is a causality-check hazard, not just an aesthetic one.** CVaR-deviation is not
  strictly convex, so its optimum can be a set. The protocol's `causality_check` compares holdings at
  `1e-6` and reads any movement as a peek. A candidate that solves a non-strictly-convex program must
  add a strictly convex tie-breaker (a small ridge on the weights, or an `L2` penalty on deviation
  from equal weight) or it will fail the check for reasons that have nothing to do with lookahead.
- **`σ₋` as a drop-in.** The cheapest usable thing in this pair is the observation that `σ₋` — the
  `L²` norm of the shortfall below the mean — is a convex, lower-range-dominated deviation measure, so
  swapping trailing `σ` for trailing `σ₋` in an inverse-risk weighting keeps every convexity property
  the symmetric version had. It is a one-token change in a weighting helper, and the honest prior is
  again that on near-symmetric daily equity returns it will track `σ` closely. Measure the rank
  correlation before writing a candidate around it.

**Universe fit.** Nothing here needs volume, the daily range, fundamentals or intraday data; the whole
pair runs on return series. `strategies/lib/features.py` already has causal cross-sectional
normalisation and long-only weighting helpers, and a new helper computing a conditional-shortfall
statistic from the `eligible` panel would be an additive file — permitted, and it must not import
`groups.py` or anything reaching the legacy universe.

## Related

- **`2026-10-23-coherent-measures-of-risk-axioms.md`** — this note resolves the semideviation question
  that note raises, via D5 and Theorem 2. It is also the note carrying the normality remark that makes
  the "measure the rank correlation first" screen the right first step for everything proposed here.
- **`2026-10-23-cvar-optimization-as-a-linear-program.md`** — the computational half. The
  minimisation form `CVaRα(X) = min_C {C + α⁻¹E[X + C]₋}` recorded above is that note's Theorem 1 in
  the companion paper's notation, and the mixed-CVaR extension there is Example 4 here.
- **`2026-10-23-noise-sensitivity-of-risk-measures.md`** — the reason this note pushes the *univariate
  per-name* statistic rather than the *joint optimisation*. The `N/T` result there rules out the
  latter at this panel's width; the tail beta above is designed to live inside that constraint.
- Folder sections this bears on: "Asymmetric comovement — the down half of the market and the third
  moment (cross-family)" is the closest existing neighbour and the tail beta above is a sharper,
  dual-derived version of the object discussed there — **anyone pursuing this should read that section
  first, because if the lab has already measured a downside-beta tilt on this panel then the screen
  above is partly spent.** Also "The co-movement channel — correlation as an object separate from
  volatility"; "The benchmark's own return — what an equal-weighted pool mechanically earns" (the pool
  is the reference series proposed above); and "Estimating the book instead of forecasting it", whose
  dimensional verdict is why the univariate route is preferred.
- **`experiments/learnings.md`:** no tension. Nothing there has measured a deviation-measure objective
  or a tail beta under any protocol version. Its warnings about de-concentration pricing and risk-bet
  calibration are v1/v2 `price-trend` constants and `CLAUDE.md` forbids carrying them here; they are
  not carried.
