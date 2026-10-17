---
title: "On-Line Portfolio Selection Using Multiplicative Updates"
authors: Helmbold, Schapire, Singer, Warmuth
year: 1998
venue: "Mathematical Finance 8(4), 325–347 (venue tier 1); earlier version ICML 1996, 243–251"
url: "https://doi.org/10.1111/1467-9965.00058 (full text of the published version read from https://www.cis.upenn.edu/~mkearns/finread/portfolio.pdf)"
citations: "450 (Semantic Scholar DOI endpoint, checked 2026-10-17); 245 (Crossref is-referenced-by-count, same date)"
sample_period: "Theory carries none — the bound holds for arbitrary price-relative sequences bounded below by r > 0. The experiments use the same 22-year daily NYSE panel (1962–1984) as Cover (1991), with the asset pairs likewise selected by the authors"
markets: US equities in the experiments only; the algorithm and bound are asset-class agnostic
tier: "A. Tier-1 venue, four authors with standing in online learning, read in full, and the central result is a theorem. Graded A rather than A+ on two self-admitted gaps: costs are excluded from the analysis entirely (their §6 says so), and the empirical comparison rests on one hand-selected panel"
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the same goal as `notes/2026-10-17-universal-portfolios-and-the-best-constant-rebalanced-portfolio.md`
— track the best constant-rebalanced portfolio (CRP) chosen in hindsight — reached by a route that
costs **constant time and storage per name per day** instead of growing exponentially in the number
of assets. The economic content is identical and is not repeated here; what this note adds is the
*update rule*, which is the part worth importing, and a dependence on the asset count that is
logarithmic instead of linear.

**The derivation is a regularised one-step objective, and that is the useful way to read it.** At
each day the algorithm picks the next portfolio to maximise

    F(w_{t+1}) = η · log(w_{t+1} · x_t) − d(w_{t+1}, w_t)

— the first term is the log wealth the current day's price relatives would have produced *if
repeated*, the second is a penalty for moving away from where the book already sits. `η > 0` is the
learning rate trading the two off. With `d` the relative entropy `D_RE(u‖v) = Σ uᵢ log(uᵢ/vᵢ)`
(Kivinen–Warmuth's framework; Kullback's minimum-relative-entropy principle), and with the log term
replaced by its first-order Taylor expansion around `w_t` plus a Lagrange multiplier for the budget
constraint, the maximiser is closed-form — the **exponentiated gradient** update:

    w_i^{t+1} = w_i^t · exp( η · x_i^t / (w^t · x^t) ) / Σ_j w_j^t · exp( η · x_j^t / (w^t · x^t) )

**Read as a portfolio rule this is a one-day cross-sectional momentum tilt in log-weight space.**
The exponent is name `i`'s price relative divided by the portfolio's own gross return, so weight
grows multiplicatively on every name that beat the book that day and shrinks on every name that
lagged it, by a factor exponential in the margin. It is the canonical "Follow-the-Winner" member of
this literature. Two properties fall out of the multiplicative form and both matter here: weights
can never go negative or leave the simplex, so **long-only is enforced by the algebra rather than by
a projection**; and a name driven to near-zero weight can only return slowly, which is a built-in
hysteresis.

**The penalty term is a turnover penalty in the KL metric.** That is the single most transferable
observation in the paper for a lab whose binding constraint is per-name costs: `η` is not a free
hyper-parameter in the usual sense but a dial on how far the book is allowed to move per day,
and `‖w^{t+1} − w^t‖` scales with `η` times the cross-sectional dispersion of `x_i/(w·x)`. The
authors' own exact-maximiser variant ("Exact EG"), which solves the un-Taylored objective by
gradient projection, is reported to do no better in practice than the closed form — so the
approximation costs nothing and the closed form is the right implementation.

**Initialisation and the side-information extension.** With no prior information `w¹ = (1/N,…,1/N)`
— the equal-weight book, which is the v3 benchmark. The side-information variant keeps `K` separate
portfolio vectors, one per state of a finite side-information variable `y_t ∈ {1…K}` observed at the
start of each day, and applies the EG update only to the vector indexed by the current state. Since
log wealth is additive, the problem decomposes into `K` independent EG problems on a partition of
the trading days. This is a regime-conditional allocator with the same construction and the same
(per-partition) guarantee — and, critically, **the hindsight comparator grows `K`-fold with it**,
because the best side-information-dependent CRP optimises `K` portfolios rather than one. The
authors' own illustrative state variable is which name was best over the trailing 100 trading days,
i.e. a momentum state.

## Construction recipe

Signal: none beyond the daily price-relative vector `x_t` (close-to-close gross returns). Lookback:
one day, with all memory carried in `w_t` itself.

1. Initialise `w¹ = (1/N,…,1/N)` on the eligible names.
2. Each rebalance date `t`: observe `x_t`, compute the book's gross return `w^t · x^t`, then apply
   the multiplicative update above and renormalise (the denominator does it).
3. **Step size.** The authors report `η ≈ 0.05` as a good choice, with performance "not overly
   sensitive" across `η ∈ [0.01, 0.15]`; a very small `η` leaves the book stuck near its
   initialisation, and a large `η` is "misled by day-to-day fluctuations" — in their two-asset toy
   market EG *loses money* for `η > 1`. Treat `[0.01, 0.15]` as a prior range, not a grid to sweep.
4. **The theory's own step size, when you want it:** `η = 2r√(2 log N / T)` with `r` a lower bound
   on price relatives and `T` the horizon — note this requires knowing both in advance, which is why
   it is not a universal algorithm in the strict sense.
5. **Unknown `r` variant, EG(η, α).** Mix the price relatives toward the all-ones vector,
   `x̃ᵗ = (1 − α/N)xᵗ + (α/N)·1`, update on `x̃` rather than `x`, and invest with the mixed portfolio
   `w̃ᵗ = (1 − α)wᵗ + (α/N)·1`. This is simultaneously a **shrinkage of the book toward equal weight**
   and the device that makes the bound hold without a known `r`.
6. **Side information:** maintain `K` weight vectors, update only the active one, invest the active
   one. Same `η` across states in their experiments, though they note different states see unequal
   numbers of days and may warrant different rates.

Costs per day: one exponential and one multiply per name, plus a normalisation — linear in `N`,
with no matrix anywhere.

## Robustness evidence (qualitative only)

- **The guarantee (Theorem 1).** For price relatives with `x_i^t ≥ r > 0` and `maxᵢ x_i^t = 1`, and
  for any CRP `u`, the log-wealth shortfall is at most `D_RE(u‖w¹)/η + ηT/(8r²)`; with uniform
  initialisation and the optimal `η`, total regret ≤ `√(2T log N)`. The `EG(η,α)` variant achieves
  `2(2N² log N)^{1/4}·T^{3/4}` without knowing `r`. **The asset-count dependence is `log N`, not
  `N`** — the structural advantage over Cover's `(m−1)log(n+1)`, and the reason this is the only
  member of the family whose bound is not absurd on a thousand-name panel.
- **…and it is still numerically vacuous at this lab's scale.** `√(2T log N)` with `T ≈ 1500` daily
  observations and `N ≈ 1000` eligible names is of order a hundred in log wealth. The honest summary
  is the same as for the universal portfolio: **the bound certifies a vanishing *rate*
  (`√(log N / T)` per period), not a usable finite-sample level.** Both the authors and Blum–Kalai
  state the trade plainly — this bound is weaker than Cover–Ordentlich's — so the only reason to
  prefer EG is computational, plus the empirical point below.
- **The dimension penalty is visible in the data, not only in the bounds, and this is the paper's
  most useful empirical result for this lab.** Their Figure 7 runs both algorithms on *random*
  subsets of the panel's names, from two up to a couple of dozen, and reports the fraction of
  best-CRP wealth captured. **That fraction falls as the subset grows, for the universal portfolio
  and for EG alike.** The experiment is a random-subset average rather than a selected showcase,
  which makes it the least cherry-picked number in the whole cluster — and it points the wrong way
  for a broad panel.
- **EG outperformed the universal portfolio in their experiments**, which the authors flag as an
  open puzzle given "the clear theoretical superiority" of Cover's bound. Blum–Kalai independently
  report the same ordering, and add that EG has no cost guarantee at all. Two groups, one dataset:
  treat it as a replicated observation about *that* panel, not about markets.
- **Admitted scope limits, in their own §6.** (i) **Costs are excluded**: with proportional
  commissions the wealth function becomes "highly non-linear and it is hard to derive an update
  rule", and they point to Blum–Kalai for the universal-portfolio version. (ii) With *per-trade*
  fixed costs the right object is a semi-CRP and finding the best rebalance subset is suspected
  computationally hard — Blum–Kalai later proved no algorithm can be universal against it.
  (iii) **"This paper and most other work on investment strategies employ a tacit assumption that
  the market is stationary… this assumption is far from being realistic."** They suggest
  drifting-concept tracking as the fix.
- **No independent replication on a modern broad panel** has been located by this folder, and the
  empirical content rests on the same hand-selected 22-year NYSE pairs as Cover. McLean–Pontiff
  applies with full force: a 1998 Tier-1 result with hundreds of citations.
- **The side-information results come with a multiple-testing caution the paper does not raise.**
  Adding a `K`-state conditioner raises the hindsight comparator as well as the algorithm, so
  "closer to the best side-information CRP" is not evidence that the conditioner carries
  out-of-sample information. The folder's own machinery is the right lens
  (`notes/2026-09-01-multi-signal-overfitting-critical-t.md`,
  `notes/2026-08-24-multiple-testing-haircut.md`).

## Implementability here

**Directly implementable, cheap, and the step size is the whole design.** The update is six lines
over the `prices` frame, needs no `aux` panel, no covariance matrix and no walk-forward fitting
machinery — it is causal by construction because `w_{t+1}` is a function of `w_t` and `x_t` alone, so
it passes `causality_check` trivially provided the rebalance grid is built from the visible window
only. Long-only and gross-leverage-1 are enforced by the multiplicative form. The 25% cap is the one
constraint that must be bolted on (cap-and-renormalise after the update, which is a projection the
theory does not cover).

**What the lab should expect, stated as a pre-registration rather than a hope.** `η` sets the
distance from the equal-weight pool, and the pool is the thing v3 subtracts. At the authors'
recommended `η ≈ 0.05` the per-day weight change is a few percent of a percent of the book — so a
daily-updated EG book on ~1,000 names is, to a first approximation, **the pool plus a small
one-day-momentum tilt**, and the folder's concentration result says the pool is also where the
null's draws sit. The prediction is therefore skill indistinguishable from zero with low turnover,
and the informative measurement is not the Sharpe but **the realised distance from `1/n` and the
realised turnover as functions of `η`** — which can be computed from the weight frames of a single
trial and would calibrate the whole family in one go.

**Three ways the construction is interesting in spite of that, in descending order.**

1. **As a turnover-aware *wrapper* on a score the lab already owns, rather than as a signal.** The
   relative-entropy penalty is a principled answer to a question v3 forces on every candidate: how
   far should a book move when the score moves? Replace the gradient `x_i/(w·x)` with any
   cross-sectional score `s_i` the lab holds and the same multiplicative update gives a book that
   tracks the score with a single, interpretable cost dial. This is the folder's standing
   observation that a hard constraint does the work of an estimator
   (`notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`) in a different metric, and it
   is **mechanically different from the lab's existing band and top-K machinery** — bands threshold,
   this one scales.
2. **The `EG(η,α)` mixing step is the shrinkage-toward-equal-weight operator with a derivation.**
   The folder holds the optimal naive/estimated mixing weight `δ* = π₁/(π₁+π₂)` and recorded that it
   is not computable at ~1,000 names because it needs `T > N + 4`
   (`notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md`,
   `notes/2026-10-12-nodewise-precision-matrices-and-large-portfolio-sharpe-ratios.md`). `α` is the
   same operator with the mixing weight set by a regret bound instead of by an estimate — nothing to
   invert, nothing to condition on `T` vs `N`. Worth carrying as the *computable* substitute.
3. **The side-information form is a regime-conditional allocator at a cost the lab can afford**, and
   it is the only construction this folder has found that conditions on a state without fitting a
   model to the state. The natural states here are the ones v3 already makes cheap and the folder
   has already read the literature on — a weekday or calendar partition, a dispersion or correlation
   regime from the range panel. Two cautions, both binding: the comparator inflation above, and the
   fact that `K` states cut the days per state by `K`, which multiplies the already-vacuous
   `√(T log N)` term by `√K`.

**Pitfalls.** The eligible-set churn problem is the same one the companion note records — a name
entering the panel has no `w_i^t` to update, and whatever is done about it (uniform seed, zero seed,
pro-rata dilution) is a design choice with a turnover consequence that must be stated. Second, the
update reacts to *one day* of price relatives, so on a non-synchronous 15-region panel it mixes
stale and fresh closes within each step
(`notes/2026-09-08-nonsynchronous-trading-econometrics.md`); a weekly or monthly rebalance grid with
the price relative measured over the same interval is the conservative form and costs nothing in the
theory. Third, the one-day *momentum* direction of the raw gradient is the opposite sign to the
short-horizon reversal the lab has repeatedly refuted under v3 — this is a genuine fork rather than
a contradiction, and the companion note on the Follow-the-Loser branch is where it is argued out.

## Related

- `notes/2026-10-17-universal-portfolios-and-the-best-constant-rebalanced-portfolio.md` — the same
  goal with a stronger bound, an exponential-in-`m` implementation, and the cost extension.
- `notes/2026-10-17-follow-the-loser-online-portfolio-selection.md` — the opposite-signed branch of
  the same family, and the taxonomy that places both.
- `notes/2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` — the mixing
  weight `α` substitutes for.
- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — constraints as implicit
  estimators, which is what the KL penalty is.
- `notes/2026-08-20-dynamic-trading-transaction-costs-aim-portfolio.md` — the other literature in
  which "how far to move toward the target" has a closed form, derived from costs rather than regret.
- `notes/2026-09-01-multi-signal-overfitting-critical-t.md` · `notes/2026-08-24-multiple-testing-haircut.md`
  — the lens for the side-information extension's inflated comparator.
