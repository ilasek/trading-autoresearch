---
title: "Best Ideas"
authors: Antón, Cohen, Polk (April 2021 draft); earlier circulated as Cohen, Polk, Silli
year: 2021 (draft read); 2008 (FMG Discussion Paper 624 / Paul Woolley Centre WP 3)
venue: "Unpublished working paper. No peer-reviewed venue located on 2026-09-28 — Crossref
  resolves only SSRN preprint records. Tier 2 by this folder's rubric (working paper with
  substantial citations), and the tier is *not* raised by the authors' standing."
url: https://personal.lse.ac.uk/polk/research/bestideas.pdf ; https://doi.org/10.2139/ssrn.1364827
citations: "53 (Semantic Scholar by DOI `10.2139/ssrn.1364827`, checked 2026-09-28); 52
  (Crossref by the same DOI, checked 2026-09-28). Both indexes see only the SSRN record; a
  second SSRN record exists for the Cohen–Polk–Silli lineage (`10.2139/ssrn.1571821`, 9 on
  Crossref), so the work's citations are **split across at least two records** and both counts
  understate it. OpenAlex was unavailable (free daily budget exhausted, HTTP 429
  `Insufficient budget`). Per the rubric, tier was not moved on the count; it rests on venue
  (none) and replication (none located)."
sample_period: "January 1983 – December 2018 (holdings; the dataset begins 1980 and a 1980
  start is reported as a robustness check). The earlier lineage used 1991–2005."
markets: US domestic equity mutual funds (NYSE/AMEX/NASDAQ via CRSP; holdings from Thomson
  Reuters); international and index/tax-managed funds excluded
tier: B
validation_overlap: true
published_post_2018: true
---

**Flags first, because they bind.** The sample runs into **December 2018**, which touches this
lab's validation window (2018-01-01 → 2023-12-31) at its first year, so `validation_overlap` is
**true** and the novelty of anything taken from here is discounted accordingly. The draft read
is dated April 2021, so `published_post_2018` is **true**; the underlying work has circulated
since the mid-2000s, which is a reason to read the *idea* as older than the flag suggests but
not a reason to clear the flag. **Tier B, not higher**: no peer-reviewed venue, no independent
replication located, US-only, holdings-based, and the central normative claim is a modelled
argument rather than a measured one. Read for the **object it constructs**, not for its
magnitudes; none of its performance figures are recorded here.

## Mechanism

**A weight is a revealed alpha forecast.** Start from a manager solving a mean-variance problem
with risk aversion `k` and covariance `Ω`: optimal weights `λ = (1/k)·Ω⁻¹·µ`. Invert it and the
manager's *subjective* expected excess returns are `µ = k·Ω·λ`. Differencing a manager's weights
against a reference portfolio's weights gives the manager's subjective alpha vector directly:

    tilt = λ_fund − λ_reference
    α    = k · Ω · tilt

**The simplification that makes it computable.** Assume all off-diagonal covariance comes from
a single market factor, `Ω = Σ + σ²_M·B` with `Σ` diagonal (per-name idiosyncratic variance) and
`B` the outer product of betas. If the fund's beta is ≈ the market's, the `B` term annihilates
against the tilt vector and

    α = k · Σ · tilt        i.e.   αᵢ ∝ σ²_idio,i · (w_i − w_ref,i)
    IRᵢ = αᵢ / σ_idio,i      ∝ σ_idio,i · (w_i − w_ref,i)
    best idea = argmaxᵢ IRᵢ

So **an overweight in a high-idiosyncratic-volatility name implies a larger revealed alpha than
the same overweight in a quiet name**, and the implied information ratio is the overweight
scaled by *one* power of idiosyncratic volatility. This is the part that transfers: it is an
identity about any weighting function, not a fact about mutual funds.

**Two references, and the choice matters.** `tilt_market` uses market weights — appropriate when
the manager's opportunity set is the market. `tilt_portfolio` uses the *value-weighted portfolio
of the stocks the manager actually holds* — appropriate when the manager first selects a set `G`
of names and then optimises within it, which the authors say (from conversations with managers)
approximates real behaviour. Under that heuristic, portfolio-alpha recovers the *ranking* of the
manager's subjective alphas even though its level is arbitrary.

**The empirical claim** is that the position each manager reveals as their highest-information-
ratio idea outperforms both the market and the rest of that same manager's book, across several
definitions of "best idea", with the effect concentrated among the more active managers (the
analysis focuses on the top quartile by maximum position-level information ratio). Magnitudes
are deliberately not recorded here.

**The normative claim, which is the reason this note exists.** If a manager's alpha is
concentrated in a handful of positions, then the rest of the book is dilution: the marginal
name added beyond the best ideas carries a subjective alpha near zero and mostly contributes
variance and cost. The authors argue investors would be better served by managers holding *far*
more concentrated books than they do, and offer four reasons managers over-diversify anyway,
none of them informational: **(1) regulatory and fiduciary pressure** against concentration;
**(2) fee and asset-gathering incentives** (Berk–Green: a manager maximising fee income on a
scalable asset base will blend good ideas with index exposure rather than concentrate);
**(3) manager career risk**, since the manager is undiversified over their own fund's outcome
even when the client is not; **(4) client-side misreading of portfolio theory** — judging a
single fund on its own Sharpe ratio rather than on its contribution to the client's portfolio,
which penalises idiosyncratic risk in rating systems and hence in flows.

**The rule to carry: the observed diversification of a real book is an agency artifact, not an
estimate of how many good ideas its signal had.** That is a statement about institutions, and
this lab has no clients, no fee schedule and no career risk — so the argument transfers as a
*prior* that the tail of a ranked book is cheap to lose, not as evidence about any particular
tail.

## Construction recipe

There is no signal to implement. The implementable object is the **inversion**, which runs on
weights this repo already emits:

1. Choose a reference weight vector `w_ref` and say which one it is. The two defensible choices
   mirror the source: the universe's own neutral book (equal weight over the tradeable universe
   — this repo has no capitalisation weights) or the equal/neutral weight over **the names the
   candidate actually holds**, which is the `tilt_portfolio` analogue and the right one when the
   book is a selection followed by a weighting.
2. Estimate per-name idiosyncratic volatility `σ_idio,i` causally over a trailing window, as the
   residual of a single-factor (equal-weight universe) regression.
3. Read off the implied per-name alpha `∝ σ²_idio,i · (w_i − w_ref,i)` and implied information
   ratio `∝ σ_idio,i · (w_i − w_ref,i)`.
4. Rank by implied IR. The "best idea" of the book is the argmax; the tail is everything whose
   implied IR is indistinguishable from zero.

Every step is a read on emitted weights. None of it requires a trial.

## Robustness evidence (qualitative only)

- Reported robust to the choice of reference (market tilt vs portfolio tilt), to the
  activeness cutoff used to select funds, to assuming equal idiosyncratic risk across names,
  and to starting the sample three years earlier.
- A parallel hedge-fund sample is reported to show the same direction, with heterogeneity by
  fund size.
- The authors state their measure of a manager's conviction is a poor proxy for the manager's
  actual belief, and argue this biases *against* finding the effect — an honest framing, but it
  is an argument rather than a test.
- **Weaknesses that decide the tier.** No peer-reviewed venue. No independent replication
  located. Quarterly holdings disclosure, US-only, one holdings vendor. Transaction costs are
  not modelled. Multiple testing is not addressed. The normative "managers should concentrate
  more" conclusion rests on a stylised two-asset example, not on a measured counterfactual.
- **A direct tension with the companion note filed tonight, and it should not be smoothed
  over.** Frazzini–Friedman–Pomorski (`notes/2026-09-28-active-share-and-its-deactivation.md`)
  find that distance-from-benchmark and other concentration measures do **not** predict fund
  performance once the benchmark is controlled for, and state the general principle that taking
  more active risk is not by itself a source of return. Best Ideas argues concentration in the
  *top-ranked* positions is where the return is. These are reconcilable — a *level* of
  concentration is not a *ranking* of positions, and the Best Ideas claim is conditional on the
  manager's own ordering being informative — but the reconciliation is exactly the assumption
  the lab cannot take for granted about its own score. **Whoever uses either note should carry
  both: concentration per se buys nothing; concentration *in the right names* is the whole
  claim, and identifying the right names is the thing in dispute.**

## Implementability here

**Not a candidate. A free measurement that answers a question the lab has already posed.**

`experiments/learnings.md` [2026-09-27] established that the seat is "a ~10-name book with a
~38-name tail of dust": ~61.41% of gross in the ten largest weights, ~1.43% in the ten smallest
of ~48, ratio 0.023 — and that this is a property of the `c − c.min() + FLOOR` magnitude
weighting function rather than of any candidate. The lab's next-ideas item 2 asks for a
candidate that **moves the seat's top ten weights**, and explicitly rules out re-sweeping the
weighting function as the way to get there.

This source supplies the diagnostic that sits between those two facts, and it is free:

- **Back out the alpha the seat's weighting function is implicitly asserting.** Apply the
  inversion above to the champion's emitted validation weights. Two readings are informative
  and neither licenses a trial:
  (a) does the ranking by *implied IR* (which carries one power of idiosyncratic volatility)
  agree with the ranking by *weight*? Where it does not, the weighting function is asserting an
  alpha ordering different from the one the score intended — that gap is a property of the
  magnitude-weighting step and is measurable without touching a signal;
  (b) what is the implied alpha of the 38-name tail? If it is indistinguishable from zero, the
  source's "over-diversification" reading applies to this book, and the lab's own null on
  deleting 42% of names (`rho` 0.9908, 2026-09-10) stops being a surprise and becomes a
  *prediction* — which is the honest way to file a result that explains a past null rather than
  proposing a new trial.
- **A falsifiable expectation to pre-register before running it**, so the measurement can fail:
  if the seat's weights were a pure magnitude transform of one score, the implied-IR ranking
  should depart from the weight ranking **only** through `σ_idio`, so the Spearman correlation
  between the two rankings should be high and its shortfall should be explained by the
  cross-sectional dispersion of `σ_idio` in the held names. A *low* correlation would mean the
  weighting function and the score disagree about the top of the book, which would be a finding
  about this repo's construction and not about any literature.

**What this note does not license.** It does not license a more concentrated candidate. The
source's normative argument runs through agency frictions this lab does not have, and the
repo's 25% cap and drawdown gate already price concentration. It does not license reading the
tail's small weights as evidence they are worthless — that is what the measurement is for. And
it imports no magnitude of any kind: `validation_overlap: true` on a US mutual-fund sample
ending in 2018 is precisely the case the flag exists for.

## Related

- The fact this note is aimed at: `experiments/learnings.md` [2026-09-27] (the ~10-name book,
  0.023) and [2026-09-10] (do not infer return-space distance from holdings-space distance).
- Companion filed the same night and in tension with this one:
  `notes/2026-09-28-active-share-and-its-deactivation.md`.
- Weighting-function literature already filed:
  `notes/2026-08-17-naive-vs-optimized-weighting.md`,
  `notes/2026-09-11-parametric-portfolio-policies-standardized-characteristics.md`,
  `notes/2026-08-20-parametric-portfolio-policies.md`,
  `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md`.
- Constraint algebra that bounds what any reweighting of finished books can do here:
  `notes/2026-09-08-stacked-regressions-nonnegative-weights.md`,
  `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`.
