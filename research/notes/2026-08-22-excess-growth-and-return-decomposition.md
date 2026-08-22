---
title: "Stochastic Portfolio Theory: An Overview"
authors: Fernholz, Karatzas
year: 2009
venue: Handbook of Numerical Analysis Vol. XV (Special Volume: Mathematical Modeling and Numerical Methods in Finance), Elsevier, pp. 89–167 — venue tier 2 (invited survey chapter; the results it surveys were published in Journal of Mathematical Economics, Finance & Stochastics, Annals of Finance and Annals of Applied Probability)
url: https://doi.org/10.1016/S1570-8659(08)00003-3
citations: 220 (Semantic Scholar, checked 2026-08-22); 71 (Crossref, checked 2026-08-22). Underlying source Fernholz–Shay (1982), Journal of Finance (tier 1), doi:10.1111/j.1540-6261.1982.tb03584.x — 136 (Semantic Scholar, checked 2026-08-22); 103 (Crossref)
sample_period: theory (no sample); the single simulation shown uses CRSP US equities 1956–2005
markets: theory is market-agnostic; the simulation uses the largest 1000 US exchange-traded stocks
tier: A for the identities (they are theorems, and cannot decay); B for the empirical content (one uncosted US simulation)
validation_overlap: false
published_post_2018: false
---

## Mechanism

The chapter's core object is an exact decomposition of a portfolio's **log** growth. For any
portfolio with weights `π(t)` on assets with prices `X_i(t)` (eq. 1.15):

```
d log V^π(t)  =  γ*_π(t) dt  +  Σ_i π_i(t) d log X_i(t)
```

The second term is the **selection term**: the weighted average of the constituents' own log
growth. It is entirely what the signal picks. The first term,

```
γ*_π(t) = ½ ( Σ_i π_i a_ii − Σ_i Σ_j π_i a_ij π_j )   =   ½ Σ_i π_i τ^π_ii        (eqs. 1.12, 3.6)
```

is the **excess growth rate**: half the difference between the weighted average of the
constituents' variances and the portfolio's own variance, equivalently half the weighted average
of the constituents' variances *measured relative to the portfolio itself*. Lemma 3.3 gives the
property that matters: for any **long-only** portfolio `γ*_π ≥ 0`, and it is strictly positive
unless the portfolio concentrates in a single name.

So a long-only book's log growth is always its holdings' average log growth *plus* a non-negative
term that depends on nothing but current weights and the covariance of what is held. That term is
the continuous-time form of the diversification return already recorded in the folder
(`½ Σ_i w_i(σ_i² − σ_ip²)`), but stated here as a general identity for *any* weight process,
including a time-varying, signal-driven one — which is precisely what session 8 asked for and did
not find. The economic content is not "rebalancing pays"; it is that the arithmetic-vs-geometric
gap of a diversified basket is smaller than the average arithmetic-vs-geometric gap of its
constituents, and the difference accrues to the holder. (See the companion note for why that is
*not* a payment for the rebalancing trades themselves.)

The second and more specialised result is the **master formula** (eq. 11.2) for *functionally
generated* portfolios — portfolios whose weights are a fixed smooth function `G` of the current
market weights `μ(t)`, via `π_i = (D_i log G(μ) + 1 − Σ_j μ_j D_j log G(μ))·μ_i` (eq. 11.1):

```
log( V^π(T) / V^μ(T) )  =  log( G(μ(T)) / G(μ(0)) )  +  ∫₀ᵀ g(t) dt
```

with drift `g(t) = −(1/2G) Σ_ij D²_ij G(μ) μ_i μ_j τ^μ_ij` (eq. 11.3). This splits relative
performance into a **positioning term** that is a bounded function of the *current* configuration
of the market, and a **cumulative drift term** that only accumulates. Remark 11.1: if `G` is
concave in the stated sense, the generated portfolio is long-only *and* `g ≥ 0`. Because `G` is
bounded on the simplex, long-horizon relative performance is governed by the drift, not the
positioning term. Special cases: constant `G` generates the market portfolio; `G(x) = (x_1···x_n)^{1/n}`
generates the equal-weighted portfolio with `g ≡ γ*_π`; `G(x) = (Σ x_i^p)^{1/p}`, `0<p<1`, generates
the diversity-weighted portfolio with `g = (1−p) γ*`; the Shannon entropy generates an
entropy-weighted portfolio with `g = γ*_μ / H_c(μ)`.

The practical remark attached to the master formula is the one worth carrying: computing the
*cumulative* drift `∫g dt` requires **no covariance estimate at all**, because the identity itself
delivers it from observable quantities (`V^π`, `V^μ`, `G(μ(0))`, `G(μ(T))`). An estimation-free
decomposition of realised performance is exactly the kind of instrument this lab prefers.

## Construction recipe

Two distinct things are recipes here, and only the first is generic:

1. **The decomposition (generic).** Given a weight matrix and daily closes, split realised log
   growth into `Σ_i π_i d log X_i` (selection) and `γ*_π dt` (excess growth). `γ*_π` is computed
   from the *realised* covariance of held names over the period and the weights actually held —
   no forecasting, no parameters. It is an accounting split of something already realised, not a
   predictor.
2. **Diversity weighting (specific, needs market capitalisations).** `μ^{(p)}_i = μ_i^p / Σ_j μ_j^p`
   for fixed `p ∈ (0,1)`, where `μ` are market weights: it shifts weight from the largest names to
   the smallest while preserving all rankings. Under weak diversity the chapter proves
   `V^{μ^(p)}(T) > V^μ(T)` almost surely, provided the horizon satisfies `T ≥ (2 / p·ε·δ)·log n`
   — an explicit long-horizon condition, not an unconditional claim, and one whose required
   horizon grows with universe size.

## Robustness evidence (qualitative only)

The decompositions are theorems, so they cannot decay and need no replication; what can fail is
the *modelling assumption* (an Itô price system with a bounded volatility structure) and the
economic reading. The chapter's own honesty is good on the boundary: the diversity results require
weak diversity of the market to hold over the horizon, the arbitrage statements are long-horizon
statements with the explicit condition above, and short-horizon versions need extra machinery
(mirror portfolios, a seed portfolio). The single empirical illustration is one market, one
universe definition, one parameter value, and the chapter states plainly that **no trading costs
were included** — which for a weighting scheme whose whole content is a rebalancing rule is the
material omission. The lineage is deep and independently developed (Fernholz–Karatzas–Kardaras,
Banner–Fernholz–Karatzas, Karatzas–Kardaras), and the base result traces to a tier-1 journal
article from 1982, but the empirical content of *this* chapter is thin and should not be leaned on.

## Implementability here

**The identity is directly usable and free; the strategy is not.**

- **Usable now: a growth-accounting diagnostic.** `γ*_π` is computable from the sanitized weight
  matrix and daily closes alone — the same input class as the folder's existing holdings-only
  diagnostics — and unlike them it is denominated in *return*, on the axis the gate reads, rather
  than in risk breadth or rank correlation. It gives a session a pre-trial answer to a question the
  lab has been asking indirectly for several sessions: **what does each concentration step cost in
  growth rate?** `γ*_π` falls mechanically as weight concentrates (it is zero for a single name),
  so the repo's documented ladder — equal-weight → rank-weight → z-score magnitude weight, then the
  buffer deletion that moved 35.1 → 30.3 names and 7.8 → 6.0 effective risk bets — has been
  spending this term monotonically, without ever pricing it. The identity says the spend is real,
  bounded, and measurable after the fact from data the repo already stores.
- **Two honest boundaries on that use.** (i) `γ*` is a term in **log** growth; a decomposition of
  log growth is not a decomposition of Sharpe, and the folder's standing gap (accuracy claims vs.
  realised Sharpe on a costed book) is not closed by it. (ii) The split is an identity, so a large
  `γ*` is not evidence of a good strategy — a book can buy `γ*` by holding more volatile,
  less-correlated names and lose more on the selection term. Treat it as a *cost accounting* for
  concentration, never as an objective.
- **Diversity weighting is not implementable here.** It is defined on market-capitalisation
  weights, and this repo has adjusted closes only, with no shares outstanding. There is no faithful
  price-only substitute: replacing `μ` with equal weights collapses the construction to the
  equal-weighted portfolio, whose drift is just `γ*`.
- **The long-horizon condition is disqualifying for the strategy claim even if caps were
  available.** `T ≥ (2/pεδ)·log n` on a ~145-instrument universe is a statement about horizons far
  longer than the repo's evaluation splits, and the almost-sure comparison is uncosted. Do not
  import "diversity weighting beats the market" as a prior.
- **The master formula does not apply to the champion.** Functional generation requires weights to
  be a fixed function of *current* market weights. A momentum book's weights depend on trailing
  returns and on its own prior membership (the buffer, when present) — it is path-dependent, so the
  estimation-free `∫g dt` shortcut is unavailable. Only the general identity (1.15) applies.

## Related

- `notes/2026-08-21-diversification-return-and-rebalancing.md` — Willenbrock's discrete-time
  statement of the same quantity; this chapter is its continuous-time generalisation to arbitrary
  (including signal-driven) weight processes, which is the extension session 8 flagged as missing.
- `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the corrective: this term is
  earned by diversified books whether or not they rebalance, and its attribution to rebalancing
  trades is disputed. **Read that note before using this one.**
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — the risk-side
  measure of the same concentration axis; `γ*` is its return-side counterpart.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the estimation-error screen. `γ*` estimates
  nothing (it is realised, not forecast), so it does not fall foul of that screen.
