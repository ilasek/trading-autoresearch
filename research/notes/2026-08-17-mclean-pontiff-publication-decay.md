---
title: "Does Academic Research Destroy Stock Return Predictability?"
authors: McLean, Pontiff
year: 2016
venue: Journal of Finance (venue tier 1)
url: https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365
citations: not verified this session — Semantic Scholar, OpenAlex and Google Scholar are all egress-blocked from this sandbox; a heavily-cited tier-1 paper but no count is recorded rather than guessed
sample_period: original studies' samples through ~2013 (approximate)
markets: US cross-section, 97 published predictors
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The paper takes 97 variables that published academic studies show to predict the
cross-section of stock returns, re-computes each predictor's portfolio return in two later
windows, and decomposes the decay:

- **~26% lower out-of-sample** (after the original study's sample ends, but before
  publication). Nobody could have been trading on the paper yet, so this slice is an
  estimate of **statistical bias in the original discovery** — data mining, selection,
  overfitting. The authors treat it as an *upper bound* on the mining component.
- **~58% lower post-publication.** The extra ~32 percentage points beyond the
  pre-publication decay is attributed to **investors learning and trading the signal away** —
  arbitrage capital arriving after the result becomes public.

Two conditional findings sharpen this and matter more here than the headline numbers:

1. **Decay is larger for predictors with higher in-sample returns.** The more spectacular the
   published result, the more of it evaporates. This is exactly what selection bias predicts:
   a big in-sample number is more likely to be big *because* it got lucky.
2. **Returns are concentrated in stocks with high idiosyncratic risk and low liquidity** —
   i.e. much of the surviving predictability lives in the small, illiquid, hard-to-trade tail
   of the cross-section, where arbitrage is expensive.

These are general properties of the published-anomaly population, not statements about any
particular calendar window.

## Construction recipe

Not a strategy paper — there is no recipe to implement. What it supplies is a **discount
function to apply to every other note in this folder**, and a specification for how to think
about the lab's own multiple-testing problem:

- Treat any performance expectation carried in from a published result as needing roughly a
  halving before it is a fair prior, with a deeper cut when the published effect was large.
- Treat the pre/post-publication split as the literature's analogue of this repo's
  train/validation/holdout discipline: an effect that has not been tested outside the window
  in which it was discovered has not yet been tested.

## Robustness evidence (qualitative only)

- Very large predictor cross-section (97 variables) rather than a single anomaly — the result
  is about the *population* of published findings, which is what makes it usable as a prior.
- Sits alongside a broader replication literature reaching compatible conclusions: large-scale
  audits (Hou–Xue–Zhang's replication of the anomaly zoo; Jensen–Kelly–Pedersen's
  reassessment) find that a substantial share of published cross-sectional predictors do not
  survive careful re-testing, though they disagree on how large that share is and on how much
  is explained by microcap weighting versus genuine absence of effect. Momentum is among the
  factors that generally survive these audits.
- Methodology honesty is high: the authors explicitly separate the mining component from the
  arbitrage component rather than attributing all decay to one story.
- Limitation: US-only, and the decay estimates are averages across heterogeneous predictors.

## Implementability here

This note is the **cross-cutting discount that governs how the strategy agent should read
everything else in `research/`**, and it converges with two conclusions the lab reached on
its own.

1. **The illiquidity finding closes off a large part of the published anomaly zoo for this
   repo, structurally.** If much of the surviving predictability is concentrated in
   high-idiosyncratic-risk, low-liquidity names, then a ~145-instrument universe of large
   liquid global stocks and ETFs simply cannot access it. That is not a tuning problem; it is
   an instrument-set problem, and no amount of clever signal work fixes it. Combined with the
   repo's own survivorship bias (today's constituents) — which pushes single-stock results in
   the *optimistic* direction — the sensible posture is heavy skepticism toward any candidate
   whose edge would have to come from stock-level signal quality.
2. **It independently supports the lab's "signal definition is exhausted, construction is
   open" conclusion.** The published-signal population is decayed, partly illiquidity-bound,
   and inaccessible here; portfolio-construction and rebalance-mechanics edges (which is
   where the repo's overlapping-tranche result came from) are not part of the population this
   paper studies and do not inherit its decay estimate. That is a real asymmetry in favor of
   the axis the lab is already working.
3. **It is the external justification for the deflated-Sharpe gate.** The ~26%
   pre-publication decay is the literature's own measurement of what selection bias costs
   when you search many specifications and report the best. The repo's DSR bar is the same
   correction applied internally. The learnings file notes the recorded trial count
   *understates* the true number of candidates attempted (34 recorded vs 53 attempted at one
   point), so the repo's realized selection bias is somewhat worse than its deflator assumes —
   this paper is the reason that gap should be treated as a real problem rather than
   bookkeeping.

Concrete guidance for hypothesis-writing: when a hypothesis is motivated by a note in this
folder, it should not import a performance expectation at all (the README already forbids
this), and it should state which of the two decay channels it is exposed to — a mechanism
that is public and easily traded is exposed to the arbitrage channel; a mechanism selected
from many variants is exposed to the mining channel; most are exposed to both.

## Related

- All other notes in `research/` — this discount applies to each.
- `2026-08-17-momentum-horizon-echo.md` — a good worked example: a single-market,
  mechanism-free result that failed an out-of-sample geographic test is the exact profile
  this paper predicts will decay.
- `experiments/learnings.md`: "The DSR multiple-testing bar effectively requires one large
  single-step jump", the provenance note on unrecorded trials, and the survivorship-bias
  caveat.
