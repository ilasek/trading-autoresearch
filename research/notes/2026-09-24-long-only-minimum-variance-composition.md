---
title: "Minimum-Variance Portfolio Composition"
authors: Clarke, de Silva, Thorley
year: 2011
venue: Journal of Portfolio Management 37(2), 31–45 — Tier 1 by this folder's rubric
  (JPM is listed there), though in substance a practitioner-academic hybrid
url: https://doi.org/10.3905/jpm.2011.37.2.031
citations: 198 (Semantic Scholar by DOI, checked 2026-09-24); 162 (Crossref
  is-referenced-by-count, same DOI, checked 2026-09-24). Read in full from the typeset
  version of record hosted at `hillsdaleinv.com/uploads/` — the publisher (pm-research)
  is closed to an automated client as recorded 2026-09-08.
sample_period: 1968–2009
markets: the 1,000 largest US stocks, monthly rebalance
tier: B
validation_overlap: false
published_post_2018: false
---

Tier B rather than A deliberately: the **central content is a derivation** and cannot
decay, but every empirical illustration is single-market, single-cap-band US, and the
paper's own return comparisons are backtests of a strategy the authors' firm ran. The
theorem is what this note is for; the track record is not.

## Mechanism

The question this paper answers is the one the 2026-09-23 nightly opened and did not have
a reference for: **when you select names by how little they replicate each other, what
does the optimal book look like, and what decides membership?**

Start from the minimum-variance portfolio — the one point on the frontier whose weights
need **no expected returns at all**, only the covariance matrix. Assume a single-factor
(market) risk model, so that `σ_ij = β_i β_j σ_m²` for `i ≠ j`. Then the long-only
minimum-variance weights have a closed form:

    w_i = (σ_MV² / σ_εi²) · (1 − β_i/β_L)   if β_i < β_L,   else 0

where `σ_εi²` is the name's idiosyncratic variance, `β_L` is a single portfolio-wide
**threshold beta**, and `σ_MV²` is the portfolio's own ex-ante variance (also
portfolio-wide). The unconstrained long-short version is the same expression with a
different, slightly higher threshold `β_LS` and no truncation — names above it simply get
negative weights.

Three consequences, and all three are about **membership** rather than sizing:

1. **Systematic risk decides who is in the book; idiosyncratic risk only decides how
   much.** High `σ_εi²` pushes a weight toward zero but can never push it *out*. Only
   `β_i ≥ β_L` zeroes a name. The long-only constraint is what converts a continuous
   weighting problem into a **selection** problem, and what it selects on is co-movement.
2. **The book is small.** The threshold beta typically falls inside the lowest-beta
   quintile of the investable set, so on the order of 80% of candidates are excluded. The
   authors are explicit that this is *not* an artifact of exposure constraints, expected
   returns, or turnover penalties — variance minimisation alone disqualifies most of the
   universe.
3. **The resulting book is still mostly a market bet.** The share of the long-only
   minimum-variance portfolio's variance that is systematic equals the ratio of portfolio
   beta to threshold beta, which is high and, importantly, *more stable over time than
   either beta separately*. Their numerical work on full covariance matrices puts the
   systematic share in the 80–90% region. **Selecting on low co-movement does not produce
   a market-neutral book; it produces a lower-beta market book.**

There is also a corollary the authors draw out and this folder should keep, because it is
about estimation rather than allocation: if only the lowest-risk fifth of names can enter
the solution, then only about `20%² = 4%` of the covariance matrix's entries can ever
influence the weights. **Most of an `n × n` estimation problem is irrelevant to a long-only
variance minimiser.** That is the analytic justification for the lab's own instinct
(2026-09-23, next-ideas #4) that one number per name beats a full matrix.

## Construction recipe

**The paper's own base case**, reported because it is the specification the analytics are
checked against, and because it is unusually plain:

- Universe: the 1,000 largest US names, re-formed monthly.
- Covariance: a **60-month rolling window** of sample variances and covariances, with both
  the 1,000 diagonal and the 499,500 off-diagonal entries **shrunk toward their respective
  cross-sectional means** (Ledoit–Wolf). No factor model, no GARCH — deliberately generic
  so the result is replicable.
- Optimisation: long-only and fully invested, **no other constraints**. The shrinkage alone
  holds maximum weights to a few percent in most months, so explicit position caps are not
  needed.
- Beta inputs for the analytic version: historical betas shrunk toward one (Vasicek /
  Bayesian, ~50% shrinkage), idiosyncratic variance from the market-model residual.

**The implementable reduction**, which is the reason to record this paper at all. Under a
single-factor risk model you never build a covariance matrix:

1. Per name, estimate `β_i` and `σ_εi²` from a market regression on the visible window
   (walk-forward; each is one number per name).
2. Shrink `β_i` toward 1.
3. Solve for the threshold `β_L` — the smallest cutoff such that the weights implied by
   `(1/σ_εi²)(1 − β_i/β_L)` over the retained set sum to the budget. One-dimensional;
   bisection on the sorted beta list converges in a handful of steps.
4. Weight the survivors by `(1/σ_εi²)(1 − β_i/β_L)`, normalise, cap.

That is `O(n)` estimation plus a scalar root-find, on 145 names, with no matrix inversion
and nothing to condition badly.

## Robustness evidence (qualitative only)

- The closed form is **exact** under a single-factor covariance and is derived, not fitted.
  It cannot be data-mined and does not decay.
- The authors check it against numerical optimisation on a full sample covariance matrix
  and report that the qualitative conclusions carry: systematic risk continues to dominate
  membership, and the additional structure mostly removes a little residual idiosyncratic
  risk.
- The low-beta/high-relative-return fact the paper leans on is among the most replicated in
  the literature (traced to Black–Jensen–Scholes), and the authors note its persistence
  across the decades of their sample as evidence of staying power rather than as a
  performance claim.
- **Gaps.** Single market, large-cap only, one cap band, no transaction-cost model in the
  headline comparisons, and no multiple-testing discussion (the paper does not need one for
  its theorem, but its backtests are not defended against it either). The empirical half is
  a practitioner track record; the analytic half is the source.

## Implementability here

**Directly implementable and cheap**, which is rare in this folder. Both inputs come from
daily USD closes; the estimation is per-name; the rebalance is monthly; the whole thing
fits inside one `generate_weights` call well under the time budget.

**What it predicts about this repo's own result, and the prediction is testable for free.**
Trial #98 replaced part of the champion's score with a co-movement term and the book went
from 62.3 to 48.0 names at unchanged HHI. This paper says that is the expected signature:
a long-only objective that dislikes co-movement **contracts the membership** and does so
without necessarily concentrating the weights. The lab read the flat HHI as "the
de-concentration dial did not move"; this note supplies the reason it did not have to.

**Three uses, ranked.**

1. **As a benchmark book the lab does not have** (`portfolio-learning`, a scout). A
   long-only, single-factor minimum-variance book is a *complete strategy* specified by
   two per-name numbers and one scalar threshold, with no free parameters to sweep. It is
   the natural control for any co-movement candidate: if a clever co-movement score cannot
   beat the closed-form variance minimiser that uses the same information, the score is not
   the contribution. **Run it as a scout, not a challenger** — its expected return channel
   is variance, and `SUMMARY.md` #142 forbids aiming a challenger at the variance channel.
2. **As the membership rule underneath a momentum book.** The threshold form
   (`β_i < β_L` or out) is a screen, not a weighting: apply it to the champion's candidate
   set *before* the existing per-leg scoring, leaving every other node byte-identical —
   the same surgical shape as trial #98. This is the cheapest way to ask whether the
   co-movement gain the lab measured is available through beta rather than through
   `E/Var`, and the two are different objects (peer-set spanning versus market beta).
3. **As an estimation argument to stop a bad idea.** `SUMMARY.md` #1's standing triage rule
   kills covariance-matrix objectives on this universe. This paper explains *why* that rule
   is right even for an investor who wants exactly what the matrix is for: under a long-only
   constraint, 96% of the matrix cannot influence the answer.

**Pitfalls.**

- **The threshold is a level, and levels are where this repo's survivorship artifact
  lives.** Low `β` and low `σ` are correlated in any real cross-section; a beta-threshold
  book will look a great deal like a low-volatility book unless the lab screens for it.
  Pre-register `|ρ(β̂, 250d vol level)|` on this universe before building anything, and
  expect it to be high. If it is, the honest construction is to sort on **correlation with
  volatility held fixed** (the conditional double sort in the BAC note) rather than on beta.
- **`σ_εi²` in the denominator is an aggressive weighting.** It is inverse *idiosyncratic*
  variance, not inverse total variance, and it will pile weight into the few names with
  clean market fits. With a 25% position cap this is survivable, but the cap will bind.
- **The single-factor assumption is doing real work.** On a universe that is 15 regions
  plus 42 ETFs, one market factor is a poor model of the covariance — regional and
  ETF/constituent blocks are exactly the structure a single factor misses. The closed form
  degrades gracefully (it is still a sensible heuristic book), but the *exactness* claim
  does not transfer, and the note should not be cited as if it did.
- Nothing here addresses turnover. A 60-month covariance window is slow, which helps at
  15 bps/side, but the threshold rule can flip a name in and out on small beta changes.
  If this is ever built, band the membership.

## Related

- `notes/2026-09-24-betting-against-correlation-decomposing-beta.md` — the same `β = ρσ/σ_m`
  decomposition, used to *sort* rather than to *optimise*, and the evidence on which half
  of beta pays.
- `notes/2026-09-24-diversification-ratio-most-diversified-portfolio.md` — the competing
  long-only objective, which maximises a correlation-based ratio instead of minimising
  variance, and which is invariant to things this one is not.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — Meucci's
  PCA-based bet count, the diagnostic side of the same question.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the standing case that estimated
  optimal weights lose to naive ones out of sample; the closed form here is the
  minimum-estimation version of an "optimised" book and is the fairest test of that case
  available on this universe.
- `experiments/learnings.md` [2026-09-23] — the 62 → 48 membership contraction at flat HHI
  that this note's mechanism predicts.
