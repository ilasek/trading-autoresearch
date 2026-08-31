---
title: "Long-Only Style Investing: Don't Just Mix, Integrate — and its peer-reviewed rebuttal"
authors: Fitzgibbons, Friedman, Pomorski, Serban (AQR); with Leippold, Rüegg as the opposing source
year: 2017 (both)
venue: The Journal of Investing (practitioner journal, Tier 3) — rebutted in European Financial Management (peer-reviewed, Tier 2 for this folder)
url: https://doi.org/10.3905/joi.2017.26.4.153 — rebuttal https://doi.org/10.1111/eufm.12139
citations: 34 for Fitzgibbons et al.; 23 for Leippold–Rüegg (both OpenAlex by DOI, checked 2026-08-31)
sample_period: 1993–2015 for the Fitzgibbons et al. empirical section (February 1993 – December 2015); not established for Leippold–Rüegg, which was read from its published abstract only
markets: developed-market large-cap global equities, a universe close to the MSCI World constituent list
tier: B
validation_overlap: false
published_post_2018: false
---

Fitzgibbons–Friedman–Pomorski–Serban read **in full** from AQR's own hosting of the typeset
Journal of Investing article (`aqr.com/-/media/AQR/Documents/Journal-Articles/`), Winter 2017,
26(4), 153–164. Leippold–Rüegg, *"The mixed vs the integrated approach to style investing: Much
ado about nothing?"*, EFM 24(5), 829–855, recorded **from its published abstract only** — SSRN,
Taylor & Francis, the EFMA conference mirror and the Zurich Open Repository all refused an
automated client (403/503/bot challenge); the abstract was read verbatim from the RePEc record.

This is the **`portfolio-learning` note `SUMMARY.md` asked for** — the "stacking / meta-labelling
half", a *learned combiner* rather than a risk allocator — and it is filed here because the two
sources together bear directly on a conclusion the lab reached on 2026-08-30 and recorded as
final. The relationship is not a contradiction; it is a **scope correction on what was measured**,
and the rebuttal keeps it from being more than that.

## Mechanism

Two ways to build one long-only book out of several signals, given that you already know your
preferred weight on each signal:

- **Portfolio blending / the "mix"** — construct a separate long-only portfolio per signal, then
  hold a weighted combination of those portfolios.
- **Signal blending / "integration"** — combine the signals into one aggregate per-instrument
  score first, then run portfolio construction **once** on that score.

The claim is that under a long-only constraint these are not close substitutes, and the reason
is structural rather than empirical:

**The mix's return is bounded by its components, by construction.** Over any period the mix
must land between the worst and best of the stand-alone single-signal portfolios. The integrated
portfolio carries no such bound and can beat all of them. That is the whole result in one
sentence, and it is arithmetic about what each construction is allowed to hold, not a claim
about which signals are good.

Why the bound binds only on the mix:

- A stock enters the mix if it clears the threshold on *any single* signal — even when a second
  signal says it is unattractive. The mix therefore holds names with strongly offsetting views
  and, worse, assigns them substantial weight (in the authors' backtest, over half the mix's
  weight sat in names the integrated portfolio declined to hold at all).
- The integrated book tilts toward names that look *decent on every* signal and away from names
  that look bad on any, including names that clear no single-signal threshold but are jointly
  attractive. It also stays neutral where signals disagree and cancel.
- The deeper reason is the **long-only constraint itself**. An unconstrained book expresses a
  view by going long the attractive names *and short the unattractive ones*; a long-only book can
  only underweight, so most of its risk comes from the long side and the short half of the view
  is largely thrown away. Integration recovers part of that discarded half — "avoid the name
  that is bad on signal B" is short-side information that a stand-alone signal-A portfolio has no
  way to use. The authors measure this directly: the share of portfolio risk attributable to the
  short side of the view is much higher for the integrated book.
- Equivalently in Grinold's vocabulary: the integrated construction has a materially higher
  **transfer coefficient** — roughly twice the mix's in their tests, and it degrades more slowly
  as target risk rises. The mix pays the long-only distortion **once per signal**; the integrated
  book pays it **once in total**.

The same framework says exactly **when the choice does not matter**, and this is the part the lab
needs most:

- **As signal correlation → +1 the two constructions converge and the gap goes to zero.** At
  perfect correlation the stand-alone portfolios hold the same names and the mix *is* the
  integrated book. The advantage is largest when signals are strongly *negatively* correlated
  (value and momentum being the canonical pair), remains sizable at zero-to-low positive
  correlation, and shrinks monotonically from there.
- **As target active risk → 0 the gap also goes to zero.** At low tracking error the long-only
  constraint is not binding — every desired underweight is smaller than the benchmark weight — so
  there is no distortion for integration to avoid. The gap widens as the book is pushed to be
  more concentrated.
- **The gap widens with the number of signals combined**, because with more signals it becomes
  ever more likely that a name clearing one threshold is unattractive on some other.

A secondary, smaller benefit: **trade netting**. Rebalancing a mix can have one sleeve buying a
name while another sells it — real costs paid on both sides for no change in aggregate exposure.
Integrating nets those trades before they reach the market. The saving is modest when turnover is
already constrained and grows when it is not, and it is larger for more numerous, more weakly
correlated signals.

### The rebuttal, and it is the more rigorous source

Leippold–Rüegg re-examine the integrated-versus-mixed comparison **using statistical tools for
robust performance testing** and conclude, verbatim from the published abstract: *"we demystify
these findings as a statistical fluke. We do not find any evidence favouring the integrated
approach. What we do find is that the integrated approach exhibits a higher sensitivity to the
low-risk anomaly. However, this reduction in risk does not lead to an improvement in
performance."*

Two things to take from it. First, the empirical magnitude claimed by the practitioner source is
contested in a peer-reviewed venue by authors doing exactly the kind of multiple-testing-aware
performance comparison this lab's own gate implements — which is why this note is Tier B and not
higher. Second, the *specific* alternative explanation offered is useful on its own terms:
integration may be loading on a low-risk tilt rather than combining information better. A book
built on averaged scores concentrates in the middle of every signal's distribution, which is
mechanically a less extreme, lower-volatility book. **The lab can and should test that confound
directly rather than inheriting either side's conclusion.**

## Construction recipe

The integrated construction, in the form this repo could build:

1. For each constituent signal, compute a **cross-sectional score** per instrument per rebalance
   date — a z-score or rank, on the same scale across signals. This is the step that matters: an
   integrated build needs each leg to expose a *score*, not a finished weight vector.
2. Form the aggregate score as the desired-weight-weighted average of the constituent scores
   (equal weights if you have no view on relative signal quality).
3. Run portfolio construction **once** on the aggregate score — thresholding into a long-only
   book, or tilting benchmark weights by the score. The authors state the benefits accrue under
   both a hard cutoff rule and a full optimisation, and also to the "hold everything, tilt by
   score" construction.
4. Rebalance on one cadence, netting all trades at the aggregate level.

The diagnostic to carry alongside it: **transfer coefficient** — the correlation between the
book's active weights and the unconstrained ideal implied by the aggregate score. It is
computable without any performance data and it is the quantity the mechanism claims to improve.

The **decisive free diagnostic** implied by the mechanism: compute the **cross-sectional rank
correlation between the constituent signals** at each rebalance date. That number, not any
performance statistic, predicts whether integration can help at all.

## Robustness evidence (qualitative only)

The mechanism half is a simulation result plus an algebraic argument, and the algebraic core —
that a portfolio mix is bounded between its components while an integrated book is not — is not
in dispute in either source. The simulations vary one parameter at a time (signal correlation,
target tracking error, number of signals) with the ideal unconstrained Sharpe normalised so
comparisons are meaningful, which is honest practice.

The empirical half is one backtest, one universe, one signal pair (a standard 12-1 momentum and a
book-to-price value), one two-decade sample, by authors with a commercial interest in the
conclusion. It is net of estimated transaction costs and includes sector-exposure constraints,
which is more than most practitioner work does. It has **not** survived independent replication:
the one peer-reviewed re-examination this note found rejects it as a statistical fluke under
robust testing.

So: the **construction-level mechanism is sound and general**, and the **magnitude is contested
and should not be carried into a hypothesis**. That split is the honest summary and it is what
the *Implementability* section is built on.

## Implementability here

**This bears on `experiments/learnings.md`'s 2026-08-30 closure of `portfolio-learning`, and it
narrows it rather than overturning it.**

The lab priced equal-weight ensembles of the eight recorded legs' **stored validation return
series** and found the ensemble monotone decreasing in the number of legs against the best single
member, concluding the family is "closed on arithmetic before its first trial". That measurement
is exactly, and only, the **portfolio mix** — combining finished long-only books at the return
level. The bound the lab measured is the bound this literature says the mix has *by construction*.
What was not measured is the **integrated** construction, which the same literature says is not
subject to that bound. The lab's arithmetic is correct and its scope is one of the two
constructions.

That said, **the mechanism's own preconditions are mostly unmet here**, and the honest expectation
is a small gain, not a rescue:

- The integration advantage vanishes as signal correlation rises, and the lab's legs correlate
  0.68–0.98 with two pairs at 0.98. On its face this is the regime where the mechanism predicts
  nothing.
- **But the lab measured the wrong correlation for this purpose, and the distinction is
  load-bearing.** The 0.68–0.98 figures are correlations of *realised return series of long-only
  books*. The quantity that governs the integration gap is the **cross-sectional correlation of
  the signals**. Two long-only books drawn from the same ~145-name universe share a large common
  market component that inflates return correlation far above the signal correlation underneath —
  which is precisely the long-only distortion the mechanism is about. Signals correlating, say,
  0.3 cross-sectionally can easily produce books whose returns correlate 0.9. **Recomputing the
  correlation matrix on cross-sectional signal ranks rather than on return series is free, needs
  no trial, and is the single measurement that decides whether `portfolio-learning` is closed.**
  If signal ranks also correlate 0.7–0.98, the family closes on the literature's own terms and
  can be recorded as closed twice over. If they are materially lower, the closure was measured on
  a confounded statistic.
- The gap also grows with target active risk, and this book is long-only, capped at 25% per
  position, gross ≤ 1.0 — a moderately-constrained, moderately-concentrated regime, i.e. the
  middle of the range rather than the end where integration pays most.

If the diagnostic reopens the family, the build is cheap and specific: expose each family lead's
cross-sectional score, average the z-scores (equal weights — the folder's standing screen against
estimating parameters applies, and an optimised combiner estimates many), and construct one
long-only book from the composite in a single step. This is a **different function from
portfolio-level blending**: `program.md` points challengers at `strategies/lib/blend.py`, which
combines *books*; integration combines *scores* and would need a new library file (permitted —
adding files to `strategies/lib/` is allowed, editing existing ones is not).

Pitfalls, and the first is the one that most likely decides the outcome:

- **The low-risk confound is the null hypothesis, not an afterthought.** Leippold–Rüegg's finding
  is that integration's apparent edge is a volatility tilt. Averaging scores mechanically pulls a
  book toward the centre of every signal's distribution, which lowers its volatility, and this
  lab has already measured that its risk-weighted and inverse-vol constructions lose. Any
  integrated candidate must be checked against a plain low-volatility book before its result is
  attributed to information combination — otherwise the lab will have re-run its own refuted
  low-vol trial under a new name. This is a screen, and it is free.
- **The mechanism assumes the constituent signals are individually worth holding.** It is a
  statement about combination efficiency, not about signal quality; it cannot manufacture a
  premium that is not in the legs. The lab's solved required-leg-Sharpe table (1.34–1.42 against
  a 1.120 champion) is a separate and still-binding constraint, and nothing here relaxes it.
- **Do not import the magnitude.** Both the simulated and the backtested improvements are
  period- and universe-specific, contested in the peer-reviewed literature, and produced on a
  MSCI-World-scale universe of thousands of names. This universe has ~145. Breadth enters this
  mechanism directly — the integrated book's advantage comes from finding jointly-attractive
  names that no single-signal threshold reaches, and in a 145-name cross-section there are few
  such names to find.
- **The trade-netting benefit is small here and may be zero.** It scales with the number of
  weakly-correlated sleeves and with unconstrained turnover; a two-or-three-leg blend of
  highly-correlated monthly-rebalanced legs has little to net. Do not build a candidate whose
  case rests on it.
- **The authors are the strategy's vendors.** AQR sells integrated multi-style products. That is
  not disqualifying — the article is transparent about method and costs — but it is why the
  peer-reviewed rebuttal carries more weight here than the citation counts alone suggest.

## Related

- `notes/2026-08-22-long-only-as-l1-regularization.md` — the same constraint from the other
  direction, and the natural companion: this note is about what the long-only constraint costs
  *when you combine signals*, that one about what it does to a single one.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
  `2026-08-19-bagging-averaging-unstable-predictors.md`,
  `2026-08-20-trading-diversification-combining-signals.md` — the folder's existing combination
  material, all of which combines **forecasts** or **portfolios**. This note supplies the missing
  distinction between the two and says the choice is first-order under a long-only constraint.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — supplies the transfer
  coefficient the mechanism improves, and the breadth term that this universe is short of.
- `notes/2026-08-18-risk-parity-equal-risk-contribution.md` and
  `2026-08-17-naive-vs-optimized-weighting.md` — the parameter-counting screen, which applies to
  the *weights on the scores*: use equal weights, not estimated ones.
- **Tension with `experiments/learnings.md`, recorded not adjudicated.** The lab's 2026-08-30
  entry closes `portfolio-learning` "on arithmetic before its first trial". The bound it measured
  is the mix bound, which this literature agrees is real and binding; the integrated construction
  is untested here and is not subject to it. The lab's conclusion should be read as *"combining
  the legs at the portfolio level cannot work"* — which is well-supported — rather than *"the
  family is closed"*, and the free signal-rank-correlation diagnostic above converts one into the
  other in either direction at zero cost. `SUMMARY.md`'s 2026-08-30 downgrade of the **HRP** half
  is untouched by this note and, if anything, corroborated: HRP is a risk allocator over finished
  books, i.e. a mix.
