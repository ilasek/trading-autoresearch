---
title: "Sparse and Stable Markowitz Portfolios"
authors: Brodie, Daubechies, De Mol, Giannone, Loris
year: 2009
venue: Proceedings of the National Academy of Sciences 106(30), 12267–12272 — venue tier 1 (top peer-reviewed general-science journal; outside the finance journal list but above it on selectivity)
url: https://doi.org/10.1073/pnas.0904287106  (full text read from the arXiv preprint, arXiv:0708.0046v3)
citations: 578 (Semantic Scholar, checked 2026-08-22); 389 (Crossref, checked 2026-08-22)
sample_period: 1973–2006 (portfolios constructed annually from 1976 to 2006)
markets: US equities, via two Fama–French asset sets — 48 industry portfolios and 100 portfolios formed on size and book-to-market
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The paper's structural result is the one this folder needed: under a full-investment constraint,
**the long-only constraint is not a binary — it is the infinite-penalty endpoint of a continuous
shrinkage path.**

Write mean-variance selection as a constrained least-squares regression and add an `ℓ1` penalty
`τ‖w‖₁`. Because `Σ_i w_i = 1`, the objective can be rewritten exactly (their eq. 5) as

```
‖ρ·1_T − R w‖²  +  2τ · Σ_{i : w_i < 0} |w_i|  +  τ
```

so **under full investment the `ℓ1` penalty is precisely a penalty on short positions**. The
no-short-sale portfolio is the `τ → ∞` limit of this family. There is a critical value `τ₀`: for
every `τ ≥ τ₀` the penalised solution *is* the long-only optimum; below `τ₀` at least one weight
goes negative and the solution typically becomes less sparse. `τ₀` is therefore a scalar measure of
**how binding** the long-only constraint is on a given asset set, and the constraint's cost can be
traced continuously rather than guessed.

Three consequences the authors draw out:

1. **The constraint regularises.** Any `ℓp` penalty with `1 ≤ p ≤ 2` stabilises the ill-posed
   inverse problem at the core of Markowitz optimisation, reducing sensitivity to collinearity
   among assets. This is the Jagannathan–Ma effect, and their framework nests it as a special case.
2. **The constraint also *selects*, which the prior literature missed.** No-short-sale optima are
   automatically **sparse** — they hold few names. The authors state the literature "has focused on
   the stability of positive solutions, but seems to have overlooked the sparsity of such
   solutions", and suspect earlier work stopped its optimisers before components converged to zero.
   In their runs the long-only optimum held between 4 and 11 of 48 industry portfolios (averaging
   about 6 across 30 annual formations) and between 3 and 13 of the 100 size/book-to-market
   portfolios. **Concentration is a consequence of the constraint, not an independent design
   choice.**
3. **A proportional transaction cost is the same mathematical object.** For an investor whose cost
   is a bid-ask spread, total cost is proportional to gross market value, i.e. to the `ℓ1` norm; a
   fixed per-name overhead adds a penalty on the *number* of names traded, which `ℓ1` also
   promotes. Applying the penalty to the *change* `Δw` rather than to `w` turns the same machinery
   into a rebalancing-cost regulariser that "naturally trades off portfolio volatility for
   transaction cost".

## The crossover — the part that answers the question this session was chasing

Session 8 asked whether there is literature in which a **binding** constraint costs more than the
estimation error it suppresses, and whether the crossover has a stated condition. This source gives
the first half cleanly and the second half honestly:

- On the **48 industry portfolios**, the best portfolios found anywhere along the whole `τ` path
  had **no short positions** — i.e. the long-only constraint sat at or near the optimum and cost
  nothing.
- On the **100 size × book-to-market portfolios**, the best portfolios **did** include short
  positions, and the authors report that optimal sparse portfolios allowing shorts significantly
  outperformed both the evenly-weighted portfolio *and* the optimal no-short-positions portfolio.

So the constraint is sometimes free and sometimes expensive, on the same method, in the same
sample, with only the asset set changed. **But the paper states no general condition** for which
side of the crossover a universe falls on; `τ` is tuned on training data, and the crossover is
located empirically per asset set. The honest answer to the open question is therefore: *yes, a
binding constraint demonstrably can cost more than it saves; no, there is no stated rule for
predicting when — only a one-dimensional, estimable knob that makes the question answerable instead
of ideological.* (The natural reading of the two asset sets — that the more collinear, factor-spanned
set is where the constraint bites — is **the lab's inference, not the source's**, and must not be
cited as theirs.)

## Construction recipe

Not buildable here (see below), but recorded for completeness. Minimise
`‖ρ·1_T − R w‖² + τ‖w‖₁` subject to `w'μ̂ = ρ` and `w'1 = 1`, on a training window of returns.
Solve with a constrained homotopy/LARS algorithm, which exploits the piecewise-linear dependence of
the solution on `τ` to return the whole path — every sparsity level — in one run. Select a point on
the path by a rule fixed in advance (the long-only endpoint; a target number of active positions;
or a band of active positions), then hold to the next annual formation. Their empirical protocol
re-forms annually and evaluates the following year out of sample.

## Robustness evidence (qualitative only)

Strong on the theory side, moderate on the empirical side. The `ℓ1`-as-short-sale-penalty identity
and the `τ₀` threshold are algebra and cannot decay; the stabilisation property has a proof in the
underlying inverse-problems literature (Daubechies–Defrise–De Mol). The empirical work is a
multi-decade US sample with annual out-of-sample re-formation and is benchmarked against `1/N`,
which the folder already records as a hard benchmark — but it is **one country, one data vendor's
constructed portfolios, and portfolios rather than securities**, and the paper reports no
transaction costs in the evaluation despite discussing cost modelling at length. The authors
themselves flag the extensions not done (larger asset collections, criteria other than Sharpe,
automatic selection of the number of assets). Independent and simultaneous work by
DeMiguel–Garlappi–Nogales–Uppal (2009, *Management Science*, doi:10.1287/mnsc.1080.0986; 1,009
citations, Semantic Scholar, checked 2026-08-22) reaches the same place from the norm-constraint
side and nests Jagannathan–Ma, Ledoit–Wolf and `1/N` as special cases of one constraint-tightness
parameter — **that paper is closed-access and no full text could be read this session; it is
recorded here as unread, not summarised second-hand**, and remains the better target if a future
session gets access, since its whole subject is the tightness trade-off.

## Implementability here

**Explanatory, not buildable.** Everything on the `τ` path below `τ₀` requires shorting, which the
repo forbids, and every point on it requires an estimated covariance and expected-return vector —
screen #1's expensive class at full strength. The repo also never solves an optimisation problem;
its weights are a monotone transform of an observed score. What the source changes is how three
things already in the folder should be read:

- **The long-only constraint is doing estimation work, and the folder now has both signs of it.**
  Session 8 recorded Jagannathan–Ma's result that a binding weight constraint is algebraically a
  covariance shrinkage — a benefit the folder had never counted. This source is the counterweight
  session 8 asked for: the same constraint is the endpoint of a path, and on one of two asset sets
  the endpoint was demonstrably past the optimum. The correct standing statement is therefore
  neither "constraints are good" nor "constraints leak signal", but: **a constraint is a shrinkage
  intensity, its cost and its benefit both scale with how binding it is, and which dominates is an
  empirical question about the universe.** That kills the taboo risk session 8 flagged without
  reversing the folder's prior.
- **Concentration is partly an artifact of the constraint, not purely a choice.** The repo's
  strongest mechanism — magnitude weighting, escalated to a hard top-15 per leg — has been read
  throughout as a deliberate concentration lever whose benefit is signal and whose cost is
  drawdown. This source shows that a long-only optimum on a correlated universe concentrates
  *automatically*, into single-digit name counts, purely as a consequence of the positivity
  constraint. That does not explain away the lab's measured gains, but it does mean "few names" is
  the expected shape of a long-only solution here rather than an aggressive stance requiring its
  own justification — and, symmetrically, that a proposal to *widen* the book is a proposal to move
  away from where the constraint pushes.
- **The repo's cost model is itself a regulariser.** 15 bps per side on the trade vector is
  literally an `ℓ1` penalty on `Δw`. Reading the champion's buffer, and Gârleanu–Pedersen's
  no-trade band under proportional costs, alongside this identity: the band is what an `ℓ1` penalty
  on trades produces, and its shrinkage side-effect is not separable from its cost side-effect.
  Recorded as explanation only — `learnings.md` prices the buffer's cost effect on the current base
  at ~0.003 Sharpe and the cost-mitigation axis is closed by enumeration.

## Related

- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — Jagannathan–Ma; this source
  nests it as the `τ → ∞` endpoint and supplies the missing other side of the ledger.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the estimation-error screen; the whole `τ`
  path except its endpoint is inside the expensive class.
- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — proportional costs imply
  a no-trade band; this note gives the same object its regularisation reading.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` and
  `notes/2026-08-22-excess-growth-and-return-decomposition.md` — the risk-side and return-side
  prices of the concentration this constraint induces.
