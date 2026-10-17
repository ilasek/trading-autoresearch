---
title: "Universal Portfolios — with: Universal Portfolios With and Without Transaction Costs"
authors: Cover; Blum & Kalai
year: 1991; 1999
venue: "Mathematical Finance 1(1), 1–29 (venue tier 1); Machine Learning 35(3), 193–205 (venue tier 2 — peer-reviewed ML journal, not one of the rubric's finance tier-1 outlets)"
url: "https://doi.org/10.1111/j.1467-9965.1991.tb00002.x (full text read from https://www.gwern.net/doc/statistics/decision/1991-cover.pdf) · https://doi.org/10.1023/A:1007530728748 (full text read from https://link.springer.com/content/pdf/10.1023/A:1007530728748.pdf)"
citations: "Cover: 864 (Semantic Scholar DOI endpoint, checked 2026-10-17); 525 (Crossref is-referenced-by-count, same date) — Crossref low again, this folder's standing pattern for pre-2000 articles. Blum–Kalai: 89 (Crossref, checked 2026-10-17)"
sample_period: "Theory carries none — both results are distribution-free and hold for arbitrary bounded price-relative sequences. The illustrations in both papers use the same 22-year daily NYSE panel (1962–1984), a set of names selected by the authors (Cover: 'two stocks chosen for their volatility')"
markets: "US equities in the illustrations only; the theorems are asset-class agnostic and stated for m assets on the portfolio simplex"
tier: "A. Tier-1 venue and heavy citation for the keystone; both read in full; the central claims are theorems rather than estimates, so they do not decay. The honest weakness is entirely on the empirical side and is flagged by the authors themselves: hand-selected asset pairs, no costs in the headline result (Cover), and a cost model whose comparator degenerates (Blum–Kalai, below)"
validation_overlap: false
published_post_2018: false
---

## Mechanism

**The object this literature competes against is the best *constant-rebalanced portfolio* chosen
in hindsight, and that object is the family protocol v3's own benchmark belongs to.** This is the
reason to read it here, and it took 192 notes to notice. A constant-rebalanced portfolio (CRP)
holds fixed proportions `b` on the simplex `β = {b : Σbⱼ = 1, bⱼ ≥ 0}` and restores them every
period; wealth after `n` periods is `Sₙ(b) = Πᵢ b·xᵢ` where `xᵢⱼ` is name `j`'s price relative on
day `i`. The v3 equal-weight eligible pool **is** the uniform CRP, `b = 1/n` on the eligible set.

Two structural facts set the stage, both one-line proofs in Cover's Section 2:

- **The hindsight target dominates every buy-and-hold.** `Sₙ* = maxᵦ Sₙ(b)` maximises over the
  simplex while buy-and-hold maximises over its *vertices* (`b = eⱼ`), so `Sₙ* ≥ maxⱼ Sₙ(eⱼ)`
  always, and likewise dominates the value-line (geometric-mean) and price-weighted indices.
  Nothing empirical is being claimed — the inequality is set inclusion.
- **Under i.i.d. draws the best CRP *is* the log-optimal (growth-optimal/Kelly) portfolio.**
  `Sₙ(b) = exp{n(W(b,F) + oₚ(1))}` with `W(b,F) = ∫ log b′x dF(x)`, so `b*(F)` maximising expected
  log wealth attains the highest achievable growth exponent (Breiman; Algoet–Cover), and no
  non-anticipating strategy can beat it asymptotically. So "track the best CRP" and "learn the
  growth-optimal portfolio without knowing `F`" are the same goal, and the i.i.d. case is where
  the goal is *also* optimal rather than merely ambitious.

**Cover's algorithm is the uniform measure on the simplex, reweighted by realised wealth.**

    b̂_{k+1} = ∫_β b · S_k(b) dμ(b) / ∫_β S_k(b) dμ(b),     S_k(b) = Π_{i≤k} b′x_i,   μ uniform

It is a performance-weighted average over a continuum of CRP "managers": give each `b` an
infinitesimal share of capital, let each compound at its own rate, and pool. `b̂₁` is the uniform
portfolio; every later `b̂_k` depends only on `x₁…x_{k-1}`, so the rule is causal by construction —
Cover makes the point explicitly that a malicious market may choose `x_k` *after* seeing `b̂_k` and
the guarantee still holds. No statistical assumption about the market is made anywhere.

**What is guaranteed.** The wealth ratio decays only polynomially in `n`:
`Ŝₙ/Sₙ* ≈ (m−1)!(2π/n)^{(m−1)/2}/|Jₙ|^{1/2}` under smoothness and interior-maximum conditions
(Theorem 6.1), with `Jₙ` the `(m−1)×(m−1)` sensitivity (negative Hessian of `Wₙ` at `b*ₙ`); hence
`(1/n)log Ŝₙ − (1/n)log Sₙ* → 0` for *arbitrary* bounded sequences. Blum–Kalai restate the same
content as a clean finite-`n` bound, `Ŝₙ/Sₙ* ≥ 1/((n+1)^{m−1})`, and note the Dirichlet(½,…,½)
prior of Cover–Ordentlich improves it to `2·(1/(n+1)^{m−1})^{1/2}`. **The whole guarantee is a
statement about the growth *rate*, and its price is a term that grows linearly in the number of
assets and only logarithmically in time.**

**Blum–Kalai's extension is the one that matters for a lab that charges costs.** With a fixed
proportional commission `c` charged on purchases, and with the *comparator also paying its own
commissions* (the best CRP is modelled as the optimal investor who sells stock to fund her own
rebalancing costs), the bound becomes

    Ŝₙ^c / (best cost-paying CRP) ≥ ((1+c)n + m − 1 choose m−1)^{-1} ≥ 1/((1+c)n + 1)^{m−1}

i.e. **the commission enters only by scaling `n` inside the log**, and the universal portfolio
still matches the best cost-paying CRP's exponential growth rate. This answered a question Cover
had left open. The reading that matters is the second half: because the benchmark pays costs too,
**as `c` grows the best cost-paying CRP degenerates toward a single name held without trading**
(buy-and-hold is the zero-turnover CRP), so in a high-cost world "universal" means no more than
"asymptotically no worse than the best buy-and-hold".

## Construction recipe

Two implementable forms, in increasing order of how much they can actually be built here.

**(1) Grid-quantised universal portfolio (Cover's own implementation).** Replace the integrals by
sums over a lattice of the simplex — Cover's two-asset illustration uses `b ∈ {0, 1/20, …, 1}`,
and defines the target `Sₙ*` relative to that same lattice. Maintain one running wealth
`S_k(b) = S_{k-1}(b)·(b′x_k)` per grid point, and set `b̂_{k+1} = Σ_b b S_k(b) / Σ_b S_k(b)`. Cost:
one multiply per grid point per day. Grid size is `O(n_grid^{m−1})`, which is why the paper's
examples have two to four assets.

**(2) Blum–Kalai randomised implementation — the one that scales, and it is free.** Draw `N`
portfolios uniformly at random from the simplex, invest `1/N` of capital in each, and **never
transfer capital between them.** Each sub-portfolio rebalances internally to its own fixed weights;
the meta-allocation requires no trading at all, because a buy-and-hold over sub-accounts
*automatically* performance-weights them. By Chebyshev, `N = (R−1)/(ε²δ)` draws give wealth within
`1−ε` of the exact universal portfolio with probability `1−δ`, where `R = Sₙ*/Ŝₙ`; worst case `R`
grows like `n^{m−1}`, but the authors note that in the published stock experiments `R < 2` for the
asset pairs tried, making `N` small. Under the Dirichlet(½,…,½) prior `R` grows at worst like
`n^{(m−1)/2}`.

**(3) Dimension handling (Cover §9).** If the best CRP lies on a `k`-face of the simplex (only `k`
names active), the bound improves to the `k`-dimensional one *provided the prior puts mass on the
faces*. Cover's general universal portfolio therefore mixes uniform measures `μ_S` over every
sub-simplex `B(S)`, `S ⊆ {1…m}`, rather than using the interior-uniform measure alone. Practical
reading: **a prior that cannot reach sparse portfolios cannot earn the sparse portfolio's bound.**

**(4) Cover's own cost patch, and its status.** §10: "we have ignored trading costs. In practice we
would not trade daily, but only when the current empirical holdings were far enough from the
recommended `b̂_k`. (A rule of thumb might be to trade only if the increase in `W` is greater than
the logarithm of the normalized transaction costs.)" That is a no-trade band stated as a
rule of thumb, with no guarantee attached — and Blum–Kalai §5 proves why one is hard to attach:
**no strategy can guarantee the growth rate of the best *semi*-CRP** (a CRP allowed to skip
rebalances on any subset of days). Their counterexample is a two-name market where each period one
relative is `1` and the other `ε`; every non-anticipating strategy earns `((1+ε)/2)ⁿ` in
expectation, while the hindsight semi-CRP that rebalances only just before each switch earns at
least `(3/2)^{n−1}` times as much. So the cost-aware class the band belongs to is **not learnable**,
which is a reason to take the band's width from the proportional-cost literature instead
(`notes/2026-10-08-no-trade-bands-under-proportional-costs.md`), not from this one.

## Robustness evidence (qualitative only)

- **The theorems need no robustness section**; they are worst-case over arbitrary bounded sequences
  and hold for every `n`. Both papers are honest that this is the *whole* of the guarantee.
- **The guarantee is numerically vacuous at any sample length a daily equity backtest can reach,
  and this is checkable in one line rather than taken on faith.** The log-wealth shortfall allowed
  by the bound is `(m−1)·log(n+1)`. At `m = 2` and a 22-year daily sample that is already ≈ 8.6 in
  log wealth; at a handful of assets it is tens; on a thousand-name panel it is in the thousands.
  Dividing by `n` to get a per-day rate does not rescue it — `(m−1)log(n+1)/n` is still of order
  one percent per day at `m = 5`, `n ≈ 1500`. **Nothing in this literature licenses the sentence
  "provably as good as the best CRP" as a finite-sample claim.** What the bound certifies is a
  *rate*: the shortfall cannot grow linearly in `n`, so the strategy cannot be catastrophically and
  permanently wrong relative to the best CRP. That is a real property and it is not a performance
  promise.
- **The observed shortfall, in the papers' own experiments, is much smaller than the bound and
  degrades monotonically with the number of assets.** Blum–Kalai report `R < 2` for the asset pairs
  tried; the companion note's source (`notes/2026-10-17-exponentiated-gradient-portfolio-update.md`)
  reports a direct experiment over *random* asset subsets in which the fraction of best-CRP wealth
  captured falls steadily as the subset grows from two names to a couple of dozen, for the universal
  portfolio and its competitor alike. The dimension penalty in the bound is therefore visible in
  practice, not just in the analysis.
- **Independent replication status: none, in the finance sense.** This is a mathematics result
  rather than an anomaly, so Hou–Xue–Zhang / Jensen–Kelly–Pedersen do not apply; but equally, no
  independent group has published an out-of-sample portfolio study of the algorithm on a modern
  broad panel that this folder has located. The empirical claims in both papers rest on one
  22-year NYSE panel with hand-selected constituents, and Blum–Kalai state plainly that with
  commission "it performed well on some sets of stocks and not as well on others".
- **Admitted in-sample tuning.** Blum–Kalai rebalance monthly in their cost experiments and write
  that "one way to select how often to rebalance is to choose the period length which gives the
  best result on past data". Rebalancing less often was "very beneficial, especially with larger
  commissions" — a finding about costs, recorded here as the direction of the effect only.
- **McLean–Pontiff discount applies with full force**: both papers are decades old and heavily
  cited, so any exploitable component has been public for a generation
  (`notes/2026-08-17-mclean-pontiff-publication-decay.md`).

## Implementability here

**The headline is a mapping, and it is free.** Under protocol v3 the lab grades every candidate
against the equal-weight eligible pool and tests it against 200 random-selection draws. Read
through this literature, **all three objects live on the same simplex of constant-rebalanced
portfolios**:

| v3 object | This literature's name for it |
|---|---|
| the equal-weight eligible pool (the benchmark) | the uniform CRP, `b = 1/n` |
| the 200 random replica books (the null) | draws from a measure on the CRP simplex |
| — (not currently a candidate) | the uniform measure *reweighted by realised wealth* = Cover's `b̂` |
| the unreachable best book in hindsight | `Sₙ*`, the best CRP |

Three consequences, in descending order of usefulness.

1. **The lab's null, read as a strategy, is Blum–Kalai's randomised universal portfolio with its
   performance weighting switched off.** Their construction *is* "draw `N` random portfolios, hold
   them, never transfer between them" — which is what the gate already simulates. The folder's
   2026-10-15 cluster established that the uniform measure concentrates (`E‖ω − ω̄‖²₂ → 0`), so the
   un-reweighted average of those draws *is* the pool, up to a vanishing shell. **Therefore a naive
   universal-portfolio candidate differs from the v3 benchmark by exactly its performance tilt, and
   by nothing else.** That is a pre-registrable prediction: measure the tilt (mean absolute weight
   deviation from `1/n`) before scoring anything, and if it is small the candidate is the pool
   wearing a hat — zero skill by construction, and the lab has already measured the
   null-collapse version of this fact.
2. **The regret bound cannot be imported as a reason to expect skill, and its asset-count term
   says where the construction is even coherent.** On ~1,000 eligible names the `(m−1)log(n+1)`
   term is hopeless and the grid implementation is impossible. The regime where the construction
   is at least *computable and low-dimensional* is `portfolio-learning`'s own charter use:
   **a meta-allocator over a handful of family-lead return streams** (`program.md`: "stacking or
   meta-labelling over family leads"). With `K` leads, the Blum–Kalai randomised form costs `K`
   running wealth counters and *no meta-level turnover* — the sub-accounts' internal turnover is
   whatever the leads already pay. That is the cheapest possible shape under v3's cost model and
   it needs no covariance matrix, no expected-return vector and no tuning parameter, which puts it
   on the right side of the folder's standing parameter-counting triage (candidate idea 1).
3. **The cost result is the one to quote, and it cuts against the family.** Blum–Kalai's Theorem 2
   survives proportional costs in *form* — which matches the folder's finding that v3's
   squared-Sharpe/skill statistic is coherent precisely because v3's costs are proportional
   (`notes/2026-10-14-net-of-cost-model-comparison-and-the-concave-frontier.md`). But the
   comparator degenerates toward buy-and-hold as `c` rises, and v3's costs are not small: 15–40 bps
   per side by liquidity tier plus UK/HK stamp duty and the French/Italian/Spanish FTTs, on a panel
   that is majority non-US. A CRP's turnover is the drift it undoes, every rebalance, forever.

**Known pitfalls, specific to this panel.**

- **The eligible set changes.** A CRP is defined on a fixed asset list; under v2 a column enters
  the panel when a committee adds a name and leaves when one is deleted. The running wealth
  counters `S_k(b)` are only comparable across `b` while the asset list is fixed, so the
  construction needs an explicit entry/exit convention (re-normalise the surviving sub-accounts,
  which is itself a trade) and the folder's index-maintenance notes bear on it
  (`notes/2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md`).
- **The 25% position cap and long-only are *already* this literature's setting** — the simplex is
  exactly long-only with gross leverage 1 — so nothing has to be adapted there, and the cap simply
  restricts `β` to a sub-polytope. Cover's margin variant (adding levered copies of each asset as
  extra "assets") is out of scope and must not be used.
- **Drift is the mechanism, so drift cannot be free.** The whole CRP effect is the wealth transfer
  performed when restoring weights; under v1/v2 that transfer was costless and under v3 it is
  charged per name. Any trial must therefore report turnover, and the folder's 2026-10-09/10
  measurement — a 100-name book at 1.3× annual turnover pays about 14 bps/yr, while a 10× book
  lost 0.22 of skill to a cost doubling — sets the scale of what a daily CRP would pay.
- **The i.i.d. premise behind the target's optimality is the premise the lab's own benchmark
  literature disputes.** Restoring fixed weights transfers wealth from winners to losers, which is
  a mean-reversion bet; the folder already holds the result that such trades have zero expected
  value under i.i.d. and pay only where relative prices mean-revert
  (`notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md`,
  `notes/2026-08-22-rebalancing-return-attribution-critique.md`). Cover's §7 needs i.i.d. for
  `Sₙ*` to be *optimal*; the distribution-free bound needs nothing, but then `Sₙ*` is merely the
  best member of an arbitrary class. **Both readings cannot be used at once**, and the honest one
  here is the second.

## Related

- `notes/2026-10-17-exponentiated-gradient-portfolio-update.md` — the linear-time competitor to
  this algorithm, with a weaker bound and a usable step-size dial.
- `notes/2026-10-17-follow-the-loser-online-portfolio-selection.md` — the branch of the same
  literature that claims real returns, and the assumption list that rules it out here.
- `notes/2026-10-15-random-portfolio-inference-concentration-of-measure.md` ·
  `notes/2026-10-15-random-weight-indices-and-the-equal-weight-centre.md` — why the uniform measure
  on this simplex is the pool.
- `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` — the v3 benchmark read as a
  CRP, and where its return comes from.
- `notes/2026-10-08-no-trade-bands-under-proportional-costs.md` — the band Cover guesses at,
  derived properly, and the reason this literature cannot supply it.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — the parameter-counting triage this
  construction passes.
- `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md` ·
  `notes/2026-08-23-geometric-mean-maximization-fallacy.md` — the growth objective this literature
  adopts without argument, and the standing case against adopting it here.
