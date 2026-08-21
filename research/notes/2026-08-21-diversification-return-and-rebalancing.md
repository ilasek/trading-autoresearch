---
title: "Diversification Return, Portfolio Rebalancing, and the Commodity Return Puzzle — with: Diversification Returns and Asset Contributions"
authors: Willenbrock; Booth & Fama
year: 2011; 1992
venue: Financial Analysts Journal (tier 1, peer-reviewed) for both
url: https://doi.org/10.2469/faj.v67.n4.1 (preprint arXiv:1109.1256) ; https://doi.org/10.2469/faj.v48.n3.26
citations: "Willenbrock: 126 (Semantic Scholar, DOI endpoint, checked 2026-08-21); 100 (Crossref). Booth–Fama: 115 (Crossref is-referenced-by-count, checked 2026-08-21) — Semantic Scholar not queried for it after the title endpoint began returning 429"
sample_period: "No historical estimation sample — the results are algebra plus worked examples. The empirical application re-reads the Gorton–Rouwenhorst commodity futures index literature (that index's own sample runs 1959–2004)"
markets: Asset-class agnostic; the illustration is US commodity futures
tier: A on the identity (algebra, cannot decay), B on the applied claims (single worked application, no transaction costs anywhere, effectively a one-author note)
validation_overlap: false
published_post_2018: false
---

Full text read directly: the arXiv working-paper version of the published FAJ article
(`arxiv.org/pdf/1109.1256`), which carries the FAJ volume/page header. Booth–Fama (1992) is
the source of the concept and of the `g ≈ r̄ − σ²/2` starting point; it was **not read this
session** and is cited here only for what Willenbrock attributes to it, which he restates and
derives in his own appendix.

## Mechanism

**The identity.** For any asset or portfolio, geometric and arithmetic average returns are
related by `g ≈ r̄ − σ²/2`. On its own this is useless, because the arithmetic average is a
misleading performance measure. There is exactly one case where it becomes a useful
intermediate: a portfolio rebalanced to **constant weights** every period. Then, and only then,

- `r̄_p = Σ_i w_i r̄_i` (the portfolio's arithmetic average is the weighted average of the
  assets' arithmetic averages), and
- `Σ_i w_i σ_ip = σ_p²` (portfolio variance is the weighted average of asset-portfolio
  covariances).

Applying `g ≈ r̄ − σ²/2` to both sides of the first and substituting the second gives

```
g_p  ≈  Σ_i w_i [ g_i + ½ (σ_i² − σ_ip²) ]

Diversification Return  ≈  ½ Σ_i w_i ( σ_i² − σ_ip² )
```

So the rebalanced portfolio's geometric return exceeds the weighted average of the assets'
geometric returns by half the weighted average of (asset variance − asset's covariance with the
portfolio). Both steps used constant weights; neither holds otherwise.

**What actually generates it.** Willenbrock's central correction — against Gorton–Rouwenhorst
and others — is that the diversification return is **not** caused by the variance reduction of
holding many assets. Variance reduction is *necessary but not sufficient*. The source is the
**rebalancing itself**: holding weights constant forces you to sell whatever has appreciated in
relative value and buy whatever has declined in relative value. That contrarian act monetises
fluctuation. His demonstrations are decisive and require no data:

- Take assets each of which has a **zero** geometric average return over the horizon. Unrebalanced,
  the portfolio returns zero. Rebalanced, it returns something positive. The *entire* return is
  the diversification return.
- Take assets with identical non-zero geometric returns. The rebalanced portfolio earns that
  return **plus** an increment; the unrebalanced one earns just that return.
- If the assets had zero volatility, their covariances with the portfolio would vanish too and
  the term would be zero. Hence "an alternative name for diversification return might be
  **volatility return**".
- Minimal example: two assets returning `+25%, −20%` and `−20%, +25%`. Each has zero geometric
  return over the two periods. Rebalanced to equal weights after the first period, the portfolio
  gains.

**The precise definition** (the approximate formula above being a Taylor expansion): the
diversification return is the difference between the geometric average return of a rebalanced
portfolio of volatile assets and that of a hypothetical rebalanced portfolio with the **same
weights and same asset geometric returns but zero volatility** — the latter being the
*strategic return*.

**The buy-and-hold counterpart, and it is a different mechanism.** A buy-and-hold book earns no
diversification return (its weights are not constant), but it can still beat the
initially-weighted average of its assets' compound returns, because the best performers become a
larger share of the book over time. Willenbrock is explicit that this is a *totally different and
unrelated* source of return — and that it comes with a **changing risk profile**, which the
rebalanced book does not have. His summary image: a rebalanced commodity index and its
buy-and-hold twin both earn excess returns, for reasons that have nothing to do with each other;
the buy-and-hold version's return is venture-capital-shaped, a few large winners paying for many
losers.

## Construction recipe

Not a strategy. Two things to compute and one question to ask.

1. **Size the term.** With a trailing covariance and the current book,
   `DR ≈ ½ Σ_i w_i (σ_i² − σ_ip²)`, where `σ_ip = Cov(r_i, r_p)`. Inputs are holdings and
   instrument returns; no strategy returns are scored.
2. **Read where it comes from.** `σ_i² − σ_ip²` is large for an asset whose volatility is
   largely *idiosyncratic to this book* and near zero for an asset that is essentially a levered
   copy of the book. So the term is concentrated in the diversifying, weakly-correlated
   positions, and a book whose risk collapses onto one or two directions has almost none of it.
3. **Ask of any rebalance-cadence or weighting change**: does it change the **weights held
   constant** (which is where the term lives) or only *which names are held*? The formula is
   indifferent to the details of the rebalancing but not to whether weights are reset at all.

## Robustness evidence (qualitative only)

- **The identity is algebra** — a second-order Taylor expansion plus two constant-weight
  accounting facts — so it cannot decay and needs no replication. Booth–Fama derived the same
  quantity two decades earlier from the variance-minus-covariance side; Willenbrock's claim to
  novelty is the *interpretation*, i.e. that rebalancing rather than variance reduction is the
  source, and the explicit demonstration that buy-and-hold has none of it.
- **The applied half is much weaker.** One worked application (a commodity futures index),
  effectively a single-author note, no historical estimation of its own, and — decisively for
  this repo — **no transaction costs modelled anywhere**. The paper's closing claim that
  "diversification return can be a significant source of return for any rebalanced portfolio of
  volatile assets" is a gross-of-costs statement.
- **Its own literature disagrees about the concept**, which the paper documents: Erb–Harvey,
  Gorton–Rouwenhorst and Idzorek all define or attribute the quantity differently, and
  Willenbrock argues Gorton–Rouwenhorst's variance-reduction attribution is "faulty logic".
  Treat the *identity* as settled and the *attribution* as this paper's argument.

## Implementability here

This is a genuinely uncovered axis for this folder — nothing read in seven prior sessions
distinguishes the return a book earns from *rebalancing* from the return it earns from its
*signal* — and it produces one cross-link, one re-pricing, and one clean tension.

1. **The cross-link, and it is the reason this note was written alongside the effective-bets
   one.** `σ_i² − σ_ip²` is a per-asset measure of how much of a position's volatility is
   *not* the book's own volatility. That is the same quantity, in return units, that the
   effective-number-of-bets statistic measures in risk units. So the lab's own measurement —
   the champion's top name at 17.2% of capital but 30.9% of variance, effective risk bets ~6
   against 13.3 by weight — is simultaneously a statement that its **diversification return is
   small**, because magnitude weighting puts the most capital on the names that are both the
   most volatile *and* the most correlated with the rest of the book, which is exactly the
   configuration in which `σ_ip² → σ_i²`. Concentration has so far been priced here only
   through drawdown. This says it costs on a second axis, and the size of that cost is
   computable from holdings before any trial.
2. **The re-pricing: turnover reduction is not free on the gross axis, and the folder has been
   treating it as free.** `SUMMARY.md` records the cost-mitigation family as closed and the
   hysteresis buffer as the literature's top-ranked technique, on the grounds that the trades a
   band suppresses are the low-information ones near the cutoff. Willenbrock says the
   rebalancing trades are what generate the diversification return. Both can hold, and the
   distinction is the useful part: **a membership band suppresses churn in *which* names are
   held, while a weight reset restores constant weights among the names retained.** The first
   forgoes little diversification return; the second is where the term lives. So the
   free question to ask of any future turnover-reducing proposal — a wider band, a slower
   cadence, a no-trade region on weights, a "don't re-size unless the target moved by x" rule —
   is *which of the two it throttles*. The folder's existing verdict survives for banding
   specifically; it does not extend to weight-reset suppression, and the champion's re-sizing
   cadence is exactly the mechanism at issue (`learnings.md` already records a re-sizing
   proposal killed on a −22% turnover / −27% HHI trade-off in which this term was never
   counted).
3. **The clean tension, stated rather than resolved: rebalancing and momentum want opposite
   things.** The diversification return is paid for a *contrarian* act — trimming what rose in
   relative weight. The buy-and-hold incremental return is paid for the *opposite* — letting
   winners grow. Willenbrock's point is that these are different, unrelated sources, not two
   views of one. A cross-sectional momentum book that resets to signal-proportional target
   weights each month is doing neither cleanly: relative to price drift it trims within the
   held set (earning some of the term), but its targets themselves chase the signal (giving it
   back). This is a real, previously unrecorded decomposition of what the champion's monthly
   re-set is doing, and it predicts that the term is *smaller* for a magnitude-weighted momentum
   book than for an equal-weighted one — which is a pre-registrable direction, not a hypothesis
   to build.
4. **Boundaries, so this is not over-read.** (a) The diversification return is **not alpha**:
   it is a decomposition of the geometric return of a book against the geometric returns of its
   own constituents, and a book can have a large one and a poor total return. It is not a reason
   to prefer any strategy over any other. (b) It is an **approximation** (second-order Taylor),
   and it holds exactly only for constant weights, which no signal-driven book has. (c) **Costs
   are unmodelled in the source and are decisive here.** The term is half a variance difference
   per period; the repo pays 15 bps/side on every trade that harvests it. Nothing in this paper
   establishes that it survives that, and this note is emphatically **not** grounds to rebalance
   more often — the folder's own record prices total cost drag at ~0.019 Sharpe, which bounds
   what the whole cost/turnover axis can be worth in either direction.
5. **Net standing here: an accounting lens and one free measurement, not a candidate.** The
   measurement is `½ Σ w_i(σ_i² − σ_ip²)` on the champion's holdings, computed the same way and
   at the same cost as the existing risk-contribution vector. Its value is that it makes a
   previously invisible cost of concentration visible and puts a number on it before a
   construction proposal is built.

## Related

- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the risk-side
  measure of the same quantity; point 1 is the bridge.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the endorsement of
  banding that point 2 bounds rather than overturns.
- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — the no-trade-band
  branch of the frictions literature, which is what the champion's buffer implements and what
  point 2 says must be distinguished from weight-reset suppression.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the 1/N benchmark whose "hard to beat"
  reputation this note partly explains: an equal-weighted rebalanced book maximises exactly the
  `σ_i² − σ_ip²` term that magnitude weighting gives away.
- `notes/2026-08-18-risk-parity-equal-risk-contribution.md` — the `σ_mv ≤ σ_erc ≤ σ_1/N`
  ordering, which is the risk-side shadow of the same ranking.
- `experiments/learnings.md`, "Weight concentration is not risk concentration" and "Turnover
  reduction is now a spent lever on the overlapping-tranche base".
