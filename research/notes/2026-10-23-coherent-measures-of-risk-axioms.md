---
title: "Coherent Measures of Risk" — the four axioms, the proof that a quantile is not subadditive, and the fact that the axioms rule out BOTH mean-variance and semi-variance objectives
authors: Artzner, Delbaen, Eber, Heath
year: 1999
venue: Mathematical Finance 9(3), 203–228 (venue tier 1 — peer-reviewed, the founding paper of the risk-measure axiomatics literature)
url: https://doi.org/10.1111/1467-9965.00068
citations: 6846 (Crossref `is-referenced-by-count`, checked 2026-10-23, resolved on the first call)
sample_period: none — this is a theory paper. It contains no estimation, no backtest and no time series of any kind; its examples are constructed probability spaces (digital options on an unnamed stock, a three-state space, a hundred independent corporate bonds) with assumed parameters. No sample in it can touch 2018–2023 because it has no sample.
markets: not applicable (axiomatic); the regulatory systems discussed are the CME's SPAN margin system and the SEC/NASD margin rules
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the authors' own preprint, `people.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf` (Delbaen's ETH Zürich directory; 255 KB, 24 pages per `pdfinfo`, dated 22 July 1998; extracted with `pdftotext -layout` to 79 KB of clean text, 626 instances of `" the "`, no ASCII shift, no `/xHH` escapes, embedded Type-1C fonts so a real text layer). Section and proposition numbering below is the preprint's and matches the published version's structure. NOTE: `file -b` reported "10 page(s)" for this PDF and "6 page(s)" for three others fetched the same night while `pdfinfo` reported 24, 26, 34 and 25 — `file`'s page count is unreliable and `pdfinfo` is the one to use.
---

## Mechanism

This is not a strategy paper and proposes no signal. It is the paper that defines what it means for
a number to be usable as a measure of risk at all, and it belongs in this folder for one reason: the
lab's gate is built on a **variance-based** statistic (Sharpe, now skill-relative to the equal-weight
eligible pool), and this paper proves that the objective family the lab's constructions implicitly
optimise fails two of its four axioms. Knowing *which* axiom fails, and under what distributional
conditions the failure is vacuous, decides whether a downside-risk objective could ever buy anything
here.

The construction is axiomatic and runs in two directions at once. The primitive object is not the
risk number but the **acceptance set** `A` — the set of future net worths a supervisor will accept
without demanding extra capital. The risk measure is then *defined* as the minimum amount of cash
that, invested in a reference instrument with strictly positive return `r`, moves a position into the
acceptance set. Propositions 2.1–2.3 show the two formulations are equivalent: axioms on the set
(contains the non-negative cone, misses the strictly negative cone, convex, positively homogeneous
cone) correspond one-to-one with axioms on the measure.

The four axioms on `ρ`, with the authors' own justifications:

- **T — translation invariance.** `ρ(X + α·r) = ρ(X) − α`. Adding a sure amount `α` invested in the
  reference instrument reduces required capital by exactly `α`. Remark 1 notes the consequence
  `ρ(X + ρ(X)·r) = 0`: the risk number is denominated in the same units as the position, which is
  what makes it a *capital* requirement rather than merely a ranking. The authors are explicit that
  this is more than ranking, and push back by name on a reading of an earlier draft that claimed "the
  main function of a risk measure is to properly rank risks."
- **S — subadditivity.** `ρ(X₁ + X₂) ≤ ρ(X₁) + ρ(X₂)`, glossed as "a merger does not create extra
  risk." Four separate justifications are given, and they are all *institutional* rather than
  statistical: without it a trader can open two accounts and post less margin than the combined
  position requires; a firm is motivated to split into two affiliates; and — the one that matters for
  portfolio work — a supervisor with cash `m` can decentralise into per-desk limits `m₁ + m₂ = m`
  only if `ρ` is subadditive. This is the axiom that makes a risk measure *allocable*.
- **PH — positive homogeneity.** `ρ(λX) = λρ(X)` for `λ ≥ 0`. Remark 2 is candid that S alone would
  give only `ρ(nX) ≤ nρ(X)` and that the reverse inequality is *imposed* to model a supervisor in a
  setting "where no netting or diversification occurs." Remark 1 concedes that if position size
  itself drives risk (liquidation time scaling with size) the right response is to put the illiquidity
  into the future net worth, not to break PH.
- **M — monotonicity.** `X ≤ Y` pointwise implies `ρ(Y) ≤ ρ(X)`.

A fifth, **R — relevance** (`ρ(X) > 0` for `X ≤ 0`, `X ≠ 0`), is stated separately and is explicitly
described as necessary but not sufficient to stop concentration going undetected. Coherence
(Definition 2.4) is T + S + PH + M.

**The two remarks that matter most here are one sentence long and sit under Axiom M.** The authors
record, without ceremony, that:

- **Axiom M rules out** `ρ(X) = −E[X] + α·σ(X)` for `α > 0` — the mean-variance objective. A
  mean-minus-multiple-of-standard-deviation criterion is **not monotone**: you can improve every
  outcome pointwise and make this number worse, because raising the good outcomes raises `σ`.
- **Axiom S rules out** the "semi-variance" type measure `ρ(X) = −E[X] + σ((X − E[X])⁻)` — mean minus
  the *standard deviation of the shortfall*. This one is monotone but **not subadditive**.

So the axioms do not merely prefer downside measures to symmetric ones. They reject the obvious
symmetric objective on monotonicity and the obvious downside objective on subadditivity, and the
reason the second fails is subtle enough that it is worth stating precisely what the functional is —
see **Related**, because a different functional with almost the same name *does* satisfy all four.

## Construction recipe

There is no portfolio recipe. What is constructible from this paper is a **test** and two **measures**.

**The test.** To check whether a candidate objective `ρ` is coherent, check the four axioms directly;
they are cheap to check and the two failures above are the common ones. The practical diagnostic for
subadditivity failure is the authors' own: build two positions whose individually-measured risks are
small because their bad events sit in disjoint low-probability sets, and observe that the sum's risk
exceeds the sum of the parts.

**The negative result for quantiles.** VaR is defined (Definition 3.3) as the negative of the upper
`α`-quantile of `X/r`: `VaRα(X) = −inf{x : P[X ≤ x·r] > α}`. It satisfies T, PH and M and **fails S**.
Three constructions are given:

1. **Digital options.** Two options on the same stock with the same expiry: `A` pays 1000 if `S_T > U`,
   `B` pays 1000 if `S_T < L`, with `L < U` and `P{S_T < L} = P{S_T > U} = 0.008`. A trader writing
   two `A`s has 1% VaR `−2u`; writing two `B`s, `−2l`; writing `A + B`, the *positive* number
   `1000 − l − u`. The authors note this shows something worse than non-subadditivity: **the
   acceptance set induced by VaR is not convex.**
2. **Two i.i.d. variables** with density 0.90 on `[0,1]` and 0.05 on `[−2,0]`: each has 10% VaR equal
   to 0, while the sum's 10% VaR is strictly greater than 0. Non-subadditivity for *independent* risks.
3. **Concentration blindness** (credited to Albanese). Base rate zero, all corporate spreads 2%,
   independent default probability 1% per name. 1,000,000 borrowed and invested in **one** name has 5%
   VaR of `−20,000` — "no risk". Spread equally over **one hundred** names, the probability of two or
   more defaults exceeds 0.18, so the 5% VaR is positive. **Diversifying raised the measured risk
   while the single-name pile-up went undetected.**

A fourth example on a three-state space shows VaR also discourages a Pareto-improving risk exchange
between two risk-averse agents.

The authors' two stated grounds for rejecting VaR: (a) it aggregates badly, even across independent
risks; (b) it does not encourage, and sometimes prohibits, diversification, "because value at risk
does not take into account the economic consequences of the events the probabilities of which it
controls."

**The constructive proposal (§5.1).** Two functionals, both averaging the tail rather than reading its
edge:

- **Tail conditional expectation** (the paper's coinage; also "TailVaR"):
  `TCEα(X) = −E[X/r | X/r ≤ −VaRα(X)]`.
- **Worst conditional expectation:** `WCEα(X) = −inf{E[X/r | A] : P[A] > α}`.

**WCE is the coherent one; TCE is not coherent in general.** Proposition 5.1 gives `TCEα ≤ WCEα`, and
Proposition 5.3 gives equality when the base probability is uniform and the variable is suitably
generic — i.e. **the two coincide when the loss distribution has no atom at the quantile, and come
apart when it does.** Proposition 5.4 is the paper's sharpest practical statement: if the base
probability is uniform and a coherent measure depends only on the distribution of the discounted risk
and dominates `VaRα`, then it dominates `WCEα`. WCE is therefore the *cheapest* coherent measure that
is still at least as conservative as a VaR-based regulatory floor — which is the authors' stated
reason for proposing it.

The representation theorem (§4.1, invoked but not reproduced here) is that **every** coherent measure
is a supremum of expectations over a set of "generalised scenarios" — i.e. a worst case over a family
of probability measures. Every coherent measure is a stress test, and every stress test over a convex
family is coherent.

## Robustness evidence (qualitative only)

This is a mathematics paper; "robustness" means the theorems are correct and the axiomatics took hold,
and both are true. With 6846 Crossref citations it is one of the most-cited papers in mathematical
finance, it founded a literature (convex risk measures, spectral/distortion measures, elicitability)
that has run for a quarter century, and its axiom set is the one subsequent work argues *with* rather
than around. The substantive later development is that **positive homogeneity (PH) is the axiom the
field actually weakened** — convex risk measures drop PH and keep convexity — and that the authors
themselves flagged PH as the imposed one. Nothing here depends on PH holding.

The one result in the paper that is a *limit* on its own force, and the most important sentence in it
for this lab, is Remark 1 after the VaR definition:

> if quantiles are computed under a distribution for which all prices are jointly normally
> distributed, then the quantiles do satisfy subadditivity as long as probabilities of exceedance are
> smaller than 0.5

with `VaRα(X) = −(E[X] + Φ⁻¹(α)·σ(X))`. **Under joint normality VaR is an affine function of mean and
standard deviation, and is subadditive.** Every counterexample in the paper requires either a
discretely-atomic payoff (digital options, defaults) or a deliberately non-normal density. The
coherence argument therefore has teeth exactly to the extent that the loss distribution being
optimised over is *not* approximately normal — which is a statement about the object being measured,
not about the axioms, and is the hinge on which implementability here turns.

No decay question arises: axioms do not decay, and there is nothing here for McLean–Pontiff or
Hou–Xue–Zhang to replicate.

## Implementability here

**What is directly usable.** The four-axiom test is free, needs no data, and applies to any objective
the lab writes down. Two conclusions follow immediately and both are about the lab's own machinery
rather than about a candidate:

1. **The gate's statistic is not a coherent risk measure, and that is fine.** v3 grades on skill —
   Sharpe minus the equal-weight eligible pool's Sharpe on the same days — which is a
   mean-over-standard-deviation ranking statistic, and Axiom M rules out exactly this family. But the
   axioms are a theory of *capital requirements*, justified throughout by decentralisation and margin
   arguments (a supervisor splitting `m` into `m₁ + m₂`, an exchange worried about two accounts). The
   lab has no capital requirement to allocate, one book, and one supervisor. **A Sharpe-based gate is
   not made unsound by failing an axiom whose entire justification is institutional.** This cuts off
   an argument that the folder should not want made: "the gate is incoherent, therefore replace it."
   The reason to care about coherence here would be a *construction* objective, not a *grading*
   statistic.
2. **The sub-additive/convex distinction is the one that bears on construction.** If a candidate ever
   minimises a risk functional to choose weights, non-convexity of that functional in the weights is
   the real cost — it admits multiple local minima and makes the resulting book an artefact of the
   optimiser's start point rather than of the data. This is the operational content of the VaR
   counterexamples for a weight-choosing candidate, and it is why the next note's CVaR formulation
   matters.

**The binding limit, and it should be stated before any downside-risk candidate is written.** Remark 1
above says VaR, CVaR and standard deviation are all affine in `(mean, σ)` under normality, so they
induce **the same ranking of portfolios**. The lab's panel is daily closes on large-cap national index
members, aggregated into a long-only book of many names. A diversified daily portfolio return is a
sum of many weakly-dependent components; it is not Gaussian, but it is far closer to Gaussian than
the digital-option and default payoffs every counterexample in this paper needs. **The prior should
therefore be that a coherent-risk objective and a variance objective pick nearly the same long-only
book, and that the difference between them is a tail effect of second order to the construction
choices the folder has already measured.** A downside-risk candidate that does not say up front where
its non-normality is coming from is proposing a re-parameterisation of minimum-variance weighting.

**Three concrete pitfalls for anything built from this paper.**

- **Use WCE/CVaR, never TCE, on a discrete sample.** An empirical daily sample with `T` observations
  puts an atom of mass `1/T` at every observed loss, so the quantile *always* sits on an atom and
  Proposition 5.1's inequality `TCE ≤ WCE` is strict rather than an equality. The naive estimator
  "average the losses worse than the `α`-quantile" is TCE, is not coherent, and is not the thing the
  next note's linear program computes. The gap is exactly the atom at the quantile.
- **Positive homogeneity is doing no work and should not be defended.** If a candidate needs an
  objective that is convex but not positively homogeneous (any of the convex-risk-measure family),
  nothing in this paper argues against it; PH is the axiom the authors imposed to model a regulator
  who forbids netting.
- **The concentration example is about a measure, not about diversification.** It must not be read as
  evidence for or against concentration in a book. It says a 5% quantile cannot see a hundred
  independent 1% events, which is a fact about reading a distribution at one point.

**Universe fit.** Nothing here needs fundamentals, intraday data or volume; the paper needs no data at
all. It is a constraint on objectives, available for free to every candidate, and it is one of the few
sources in this folder whose content cannot be invalidated by a measurement.

## Related

- **`2026-10-23-cvar-optimization-as-a-linear-program.md`** is the direct sequel: Rockafellar–Uryasev
  take the WCE idea, give it a general-distribution definition that stays coherent in the presence of
  atoms (the splitting of the atom at the quantile is exactly what Proposition 5.1's strict inequality
  is about), and turn its minimisation into a linear program. That note also carries the result that
  under normality minimum-CVaR, minimum-VaR and minimum-variance portfolios **coincide**, which is the
  quantitative form of the Remark 1 limit above.
- **`2026-10-23-generalized-deviation-measures.md`** resolves an apparent contradiction with this
  note, and the resolution is a definitional one worth stating here because it is easy to get
  backwards. Artzner et al. rule out the "semi-variance type" measure
  `ρ(X) = −E[X] + σ((X − E[X])⁻)` on subadditivity. Rockafellar–Uryasev–Zabarankin's **lower
  semideviation** `σ₋(X) = ‖[X − EX]₋‖` satisfies all their deviation axioms, is lower range dominated,
  and therefore (their Theorem 2) makes `R(X) = −E[X] + σ₋(X)` **coherent**. These are different
  functionals: Artzner's applies the standard-deviation operator `σ(Z) = ‖Z − EZ‖` to the shortfall
  `Z`, while RUZ's applies the plain `L²` norm `‖Z‖`. **The difference is whether the shortfall is
  centred before the norm is taken, and it is the difference between subadditive and not.** This is
  my reading of the two definitions side by side, not a claim either paper makes about the other.
- **`2026-10-23-noise-sensitivity-of-risk-measures.md`** is the counterweight to the whole vein: it
  measures what replacing variance with a tail measure costs in estimation error, and the answer is
  that the coherent measures are the *fragile* ones. Read with this note, the pair says a tail measure
  is better axiomatically and worse statistically, and that the second effect is the larger one at
  this panel's dimensions.
- **Tension with `experiments/learnings.md`, flagged rather than resolved:** the learnings file's
  material on de-concentration pricing and risk-bet calibration was measured on `price-trend`
  constructions under v1/v2, and `CLAUDE.md` forbids carrying its constants across families or into
  v3. Nothing in this note supplies a constant, so there is nothing to carry; but a candidate that
  proposes a downside-risk *weighting* scheme is making a concentration bet, and the learnings file's
  standing warning that such bets have repeatedly backfired applies to it on the lab's own evidence,
  independently of what this paper says about axioms.
- Related folder sections: `SUMMARY.md`'s "The objective itself — growth, utility, and the gate's own
  statistic (cross-family)" is where the gate-statistic question lives, and this note's point 1 above
  belongs with it; "What statistic decides that a book beat its benchmark" is the v3-specific version
  of the same question.
