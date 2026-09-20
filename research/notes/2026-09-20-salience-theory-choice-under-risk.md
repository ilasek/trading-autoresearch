---
title: "Salience Theory of Choice Under Risk"
authors: Bordalo, Gennaioli, Shleifer
year: 2012 (QJE 127(3), 1243–1285); read from NBER Working Paper 16387 (September 2010)
venue: Quarterly Journal of Economics (Tier 1)
url: https://doi.org/10.1093/qje/qjs018 — version read: https://www.nber.org/system/files/working_papers/w16387/w16387.pdf
citations: 735 (Semantic Scholar by DOI, checked 2026-09-20); 1178 (Crossref is-referenced-by-count, checked 2026-09-20)
sample_period: n/a — decision theory plus laboratory choice experiments; no market data
markets: none (theory and experimental choice data)
tier: A
validation_overlap: false
published_post_2018: false
---

Read **in full**, in the NBER working-paper version. `scholar.harvard.edu` returned **403** to the
typeset QJE PDF it hosts and `dash.harvard.edu`'s bitstream endpoint returned **405**; the NBER
mirror served the paper on the first try, as `research/README.md` predicts. The published QJE
version was not read, so the construction constants below are attributed to the version read —
they are the same values Cosemans–Frehen cite from the published paper, which is a cross-check.

This is the first of three notes from 2026-09-20 and it is the **theory primitive only**. It
proposes no portfolio and contains no market data. Read it for the salience function and the
decision weights; the tradeable object is in `2026-09-20-salience-theory-stock-prices.md`, and the
reason to be sceptical of it is in `2026-09-20-salience-international-replication.md`.

## Mechanism

The paper is a theory of choice among lotteries in which **attention is drawn to payoffs that
stand out relative to the alternatives on offer**. A decision maker does not evaluate a lottery in
isolation; they compare it, state by state, against the other lotteries available, and the states
where their payoff differs most from what else is on the table capture disproportionate attention.
Objective probabilities are then replaced by **decision weights** that overweight those salient
states and underweight the rest.

The economic content for asset pricing is in **what determines the distortion**. Three properties
define a salience function:

- **Ordering** — salience of a state rises with the distance between this lottery's payoff in that
  state and the average payoff of the alternatives in that state. Salience is about a *difference*,
  not a level.
- **Diminishing sensitivity** — salience falls when all payoffs in a state shift away from zero
  together. The same absolute difference is perceived less intensely at higher payoff levels. (This
  is Weber's law; the paper says so explicitly.)
- **Reflection** — salience depends on magnitude, not sign. A state where the alternatives differ
  sharply in losses is as salient as one where they differ sharply in gains.

A fourth property, **convexity**, limits diminishing sensitivity so that at large absolute payoffs
the *difference* (the numerator) again dominates.

**The distinction that makes this a separate theory rather than a relabelling of prospect theory
is worth stating precisely, because it is the whole source of the empirical prediction.** In
cumulative prospect theory the probability distortion is a *fixed* function of the payoff's **rank**,
so tail events are *always* overweighted. In salience theory the distortion depends on the payoff's
**magnitude and the choice context**, so a tail payoff is overweighted **only if it is salient** —
and a tail payoff shared by every alternative is not salient at all. The paper's own illustration:
in a choice between two correlated lotteries that both pay $2000 in a 10%-probability state, CPT
overweights that state (low probability, extreme payoff) while salience theory gives it **no**
extra weight, because the state does not discriminate between the two lotteries and therefore
cancels out. Risk seeking arises when a lottery's **upside** is the salient state and risk aversion
when its **downside** is; no concave-convex value function is required to generate either.

## Construction recipe

The tractable functional form the paper uses throughout, for payoff `x_is` of lottery `i` in state
`s` against the average payoff `x̄_s` of the alternatives in that state:

```
σ(x_is, x̄_s) = |x_is − x̄_s| / (|x_is| + |x̄_s| + θ),     θ > 0
```

with `x̄_s = (1/N) Σ_i x_is` over the `N` lotteries in the choice set.

**What `θ` does.** It sets the relative strength of ordering (numerator) against diminishing
sensitivity (denominator). At `θ = 0`, any state where the lottery pays exactly zero attains
**maximal** salience (`σ(0, x) = 1` for every `x`), which is degenerate. A strictly positive `θ`
prevents that: a zero-payoff state can be unremarkable when the alternatives are also small. It
also controls convexity — smaller `θ` is more convex.

Given `σ`, the decision maker **ranks** the states by salience, `k = 1` (most salient) to `k = S`,
and replaces objective probabilities `π_s` with `π̃_is = π_s · ω_is`, where

```
ω_is = δ^k_is / ( Σ_s' δ^k_is' · π_s' ),        δ ∈ (0, 1]
```

The weights are normalised so `E[ω_is] = 1` — the distortion has mean zero, it only reallocates
weight. `δ = 1` is the rational agent (no distortion). `δ < 1` overweights salient states; as
`δ → 0` the agent attends only to the single most salient payoff. `δ` is read as a proxy for
cognitive ability, not a preference parameter.

**The calibration, which is what the empirical literature imports and is the reason this note
exists as a separate file: `θ = 0.1` and `δ = 0.7`.** The paper derives these from its
experimental evidence on long-shot lotteries (the working-paper version states `δ ≈ 0.7` with
`θ = 0.1` in three separate places, including the condition `δ < 0.73` under which the model
reproduces the observed risk attitudes). **These are fixed constants, not estimated on market
data** — a point that matters a great deal for how a candidate built on them is graded here; see
"Implementability".

## Robustness evidence (qualitative only)

- **Venue and citation weight.** A top-five economics journal, and by citation count one of the
  most-cited decision-theory papers of its decade in both indices checked.
- **Experimental rather than market evidence.** The paper's own tests are choice experiments and
  classic violations of expected utility — Allais paradoxes, preference reversals, the
  instability of risk preferences across choice sets. It accounts for them without a
  concave-convex value function.
- **Independent experimental confirmation is cited in the successor literature.** Mormann and
  Frydman's lottery-choice experiments find risk taking systematically affected by the
  **correlation structure between lotteries** — the context-dependence that is salience theory's
  signature and that neither expected utility nor any parameterisation of CPT accommodates.
- **What this paper is not.** There is no asset-pricing test here, no market data, no returns, and
  therefore nothing in this note to discount for lookahead. The asset-pricing model that turns
  this theory into a cross-sectional prediction is a separate paper by the same authors (BGS,
  *Salience and Asset Prices*), and the empirical implementation is a third paper.
- **Rubric rows that do not apply.** Replication status, sample robustness and cost modelling are
  all vacuous for a decision-theory paper. Tier A is awarded on venue, citations and the
  independent experimental support, and the tier of the *tradeable* claim is set in the other two
  notes, not here.

## Implementability here

Nothing in this note is directly implementable — it is the primitive. Two things carry forward and
both are about how the lab should *grade* a salience candidate rather than how to build one:

1. **`θ = 0.1` and `δ = 0.7` are calibrated constants from laboratory experiments, fixed before
   any market data is touched.** A candidate using them estimates **zero** parameters from the
   price panel. Under this folder's candidate #1 (*count the noisily-estimated parameters before a
   weighting-scheme trial*), that is the best possible grade: no covariance matrix, no per-asset
   forecast, no in-sample fit, nothing to shrink. This is a genuinely unusual property among the
   behavioural scores this lab has tried, and it should be stated in any hypothesis built on it.
   It is also a **falsifiable commitment** — if a candidate only works after `δ` is tuned, the
   theory has been abandoned and what remains is a fitted decay parameter.
2. **The context-dependence is the theory's entire content, and it is testable by ablation.**
   Ordering says salience is a function of a **difference from the alternatives**. Strip the
   context out — compare each payoff to zero instead of to the alternatives — and the salience
   function collapses to a monotone function of `|x|`, i.e. to a pure magnitude ranking. That
   degenerate case is exactly the volatility/`MAX`-style object this lab has refuted repeatedly.
   So the theory hands the lab a **pre-registerable ordered prediction** rather than a single
   number: the context-dependent version must outperform the context-free version, or what is
   being measured is not salience. The empirical note works this out in full.

## Related

- `2026-09-20-salience-theory-stock-prices.md` — the cross-sectional implementation; read next.
- `2026-09-20-salience-international-replication.md` — the multi-market qualification.
- `notes/2026-09-01-max-lottery-extreme-positive-returns.md` and the folder's other prospect-theory material: this
  is the **sibling** theory to the probability-weighting limb already covered there, and the two
  make *different* predictions (see "Mechanism" above). The 2026-09-19 open question flagged that
  the folder cites prospect theory's primitives without covering all of them; salience theory is
  the adjacent theory that had **zero** coverage across all 112 prior notes.
