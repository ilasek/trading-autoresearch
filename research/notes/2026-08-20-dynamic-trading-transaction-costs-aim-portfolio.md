---
title: "Dynamic Trading with Predictable Returns and Transaction Costs"
authors: Gârleanu, Pedersen
year: 2013 (published); NBER WP 15205, 2009 (version read)
venue: Journal of Finance 68(6), 2309–2340 (venue tier 1)
url: https://doi.org/10.1111/jofi.12080 ; WP read in full at https://www.nber.org/system/files/working_papers/w15205/w15205.pdf
citations: 557 (Semantic Scholar by DOI, checked 2026-08-20)
sample_period: theory has none; the empirical illustration uses commodity futures 1996-01-01 – 2009-01-23
markets: 15 commodity futures (the theory is asset-class agnostic)
tier: A on the closed-form theory; B on the empirical illustration (single asset class, and in-sample by the authors' own statement)
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source `SUMMARY.md` open question 6(a) asked for: the crossing from *signal
properties* to *the portfolio a cost-paying investor actually holds*, derived rather than
asserted. The setup is a mean-variance investor who observes `K` return-predicting factors
`f_t` with mean-reversion dynamics `Δf_{t+1} = −Φ f_t + ε_{t+1}`, faces trading costs
`TC(Δx_t) = ½ Δx_tᵀ Λ Δx_t`, and maximises discounted expected excess return net of a risk
penalty and net of those costs. It is solved in closed form. Three results matter here.

**1. The optimal policy is partial adjustment toward a target.** Under Assumption A
(`Λ = λΣ`, costs proportional to the risk of the trade),

```
x_t = (1 − a/λ)·x_{t−1}  +  (a/λ)·aim_t
```

with the *trading rate* `a/λ < 1` a scalar given in closed form, **decreasing in transaction
costs `λ` and increasing in risk aversion `γ`**, and — the part worth noticing — independent
of the current portfolio and of the portfolio's history. The investor never trades all the
way to the target.

**2. The target is not the frictionless optimum; it aims in front of it.** The frictionless
("Markowitz") portfolio `(γΣ)⁻¹ B f_t` is a moving target because the factors mean-revert.
The optimal *aim* portfolio is an exponentially weighted average of the current and all
future expected Markowitz portfolios,

```
aim_t = Σ_{τ ≥ t} z(1−z)^{τ−t} · E_t[Markowitz_τ],     z = γ/(γ + a)
```

with `z` decreasing in transaction costs. Higher costs ⇒ more weight on where the target is
*going*, less on where it is now.

**3. Signals are weighted by persistence, not by strength alone.** With `Φ` diagonal, the aim
portfolio is exactly the Markowitz portfolio built from **down-scaled** signals:

```
aim_t = (γΣ)⁻¹ B · ( f¹_t/(1 + φ₁a/γ),  …,  f^K_t/(1 + φ_K a/γ) )ᵀ
```

A fast-decaying signal (large `φ_k`) is shrunk harder than a persistent one, and the *relative*
down-weighting of the fast signal against the slow one **increases with transaction costs**.
The economic reading the authors give: an investor facing costs should trade aggressively only
on signals whose benefit accrues over a long enough period to amortise the trade. Absent costs
the investor re-optimises for free and alpha decay plays no role at all — persistence weighting
is a *purely cost-induced* phenomenon.

**Corollary (Proposition 5), and the one this repo should read twice.** An investor who has
followed the optimal policy holds

```
x_t = Σ_{τ ≤ t} (a/λ)(1 − a/λ)^{t−τ} · aim_τ
```

— **the current optimal portfolio is an exponentially weighted average of past target
portfolios.** Averaging over formation dates is not a variance-reduction trick bolted onto a
cost problem; under quadratic costs it *is* the optimal cost-aware policy, stated as an
equality.

## Construction recipe

Enough to implement, though see the caveats below before doing so:

- Estimate `B` (loadings of returns on signals), `Σ` (return covariance), `Φ` (per-signal
  mean-reversion rate, i.e. alpha decay — the authors report it as a half-life), and calibrate
  `λ` from a price-impact estimate.
- Form `Markowitz_t = (γΣ)⁻¹ B f_t`.
- Form `aim_t` by dividing each signal `f^k_t` by `(1 + φ_k a/γ)`.
- Each period, move a **fixed fraction** `a/λ` of the distance from the current book to `aim_t`.
- Signals in the paper's own illustration are **rolling Sharpe ratios over three horizons**
  (past 5 days, past 1 year, past 5 years), each a mean price change divided by that window's
  standard deviation of daily price changes, with the denominator winsorised below the tenth
  percentile. The three horizons were chosen precisely so that their decay rates differ.
- Extension in Section IV: with *persistent* price impact (market impact that decays slowly
  rather than vanishing each period) the two principles survive, but both the trading rate and
  the aim portfolio change form.

## Robustness evidence (qualitative only)

- The core results are closed-form solutions of a stated model, so they cannot decay; what can
  fail is the model's fit to reality. The load-bearing modelling choices are quadratic costs,
  linear factor dynamics, and mean-variance preferences.
- The paper is candid about its cost specification being chosen "partly for tractability",
  while citing empirical work finding costs to be convex, and some estimating them as
  quadratic.
- The empirical illustration is one asset class and is **in-sample by the authors' own
  statement**: they estimate the predictive regression over the whole sample and write that "a
  more realistic analysis would consider rolling out-of-sample regressions", justifying the
  choice as isolating the portfolio insight from forecast noise. It is an illustration of the
  theory, not evidence for it. This is exactly the failure mode of `SUMMARY.md` screen 4(b) —
  translate the result into the position held at each date and count which inputs were
  unavailable then — and it should be applied to this paper as readily as to any other.
- The authors state the boundary with the older frictions literature explicitly: the
  trade-partially-toward-the-aim policy "is qualitatively different from the optimal strategy
  with proportional or fixed transaction costs, **which exhibits periods of no trading**"
  (Constantinides 1986 and successors, solved numerically).

## Implementability here

The theory transfers as *structure*; the parameterisation does not.

**What transfers, and it is the folder's missing bridge.** Proposition 5 is a portfolio-level,
net-of-cost, realised-objective statement that the optimal book is a decaying average of past
target portfolios. Every prior account of the champion's six overlapping formation tranches in
this folder — estimator (Jegadeesh–Titman), dispersion (Hoffstein et al.), forecast accuracy
(Pesaran–Timmermann, Breiman), information ratio (Grinold / Ding–Martin) — is a claim about a
*predictor* or an *IR*, with the crossing to realised net return left as the lab's own
inference. This source makes the object of the claim a portfolio held by a cost-paying
investor. It does not prove the lab's result (see the gaps below), but it is the first source
read here whose conclusion is stated in the same currency as the lab's measurement.

**Which cost model you have decides which mechanism you get, and this repo has both.** The
authors' own contrast is the useful one: **quadratic** costs ⇒ partial adjustment toward a
target every period; **proportional or fixed** costs ⇒ *periods of no trading*. This repo pays
a flat 15 bps/side, i.e. proportional — so the branch of the literature that its cost model
selects is the no-trade-region branch, which is what the champion's hold-25/enter-15 hysteresis
buffer implements. The tranche-averaging structure that this paper derives belongs to the
*other* branch. That both mechanisms are present in the champion is a fact about the champion,
not a prediction of this source; what the source does supply is that the two are **the
canonical answers to two different cost specifications**, so they are complements by
construction rather than two versions of one idea. Note also that the trading rate `a/λ` is
*decreasing* in costs — but a 1/K-per-tranche recommitment scheme fixes the rate by
construction at `1/K` and never estimates it, which is the trade this repo should prefer (see
screen #1).

**What does not transfer.** (a) The policy is unconstrained: no long-only constraint, no
`≤ 1.0` gross leverage, no 25% position cap. `(γΣ)⁻¹ B f_t` is a levered long-short tangency
portfolio; the entire construction is defined by deviations in both directions from zero.
(b) It requires estimating `B`, `Σ`, `Φ` and `λ` — the noisily-estimated-parameter class that
`SUMMARY.md` screen #1 exists to kill, and `Σ` specifically is the object the ERC theorem and
the two inverse-vol refutations already closed here. (c) Costs are quadratic in trade size,
which is a market-impact model for a large investor; a flat per-side bps charge is linear and
has no interior optimum of the same shape.

**A live tension, and it should be recorded rather than smoothed.** Proposition 4 says weight
signals **by persistence**, and says the tilt should grow with transaction costs. The lab's
four horizon legs (63/126/189/252 days) have different alpha decays by construction, and the
lab weights them **equally**, with `learnings.md` recording equal weights as load-bearing and
trial #44 showing the result insensitive to the one zero-parameter deviation that could be
tried. These are not in conflict, and the resolution is the folder's standing one: Proposition
4 gives the optimal weights **when `Φ`, `Σ`, `B` and `λ` are known**; the lab's result is about
what happens when they must be estimated from a short, heteroskedastic sample. Hansen's four
conditions (note `2026-08-19-model-averaging-mallows-weights.md`) say which regime you are in,
and this repo is in the second. So: **not grounds to reweight the horizon legs by lookback
length.** It *is* grounds to state the equal-weight choice more precisely than "don't estimate
weights" — the model-optimal weights are known in closed form, tilt toward the long horizons,
and are declined here because their inputs are not.

**Free triage rule this yields, costing no trial.** Before proposing any new signal leg, ask
what its alpha decay is relative to the legs already held, because under costs a fast-decaying
signal is worth strictly less than its gross alpha suggests — and the discount grows with the
cost rate. This is the mechanism-level reason the lab's short-term-reversal legs kept
subtracting value once turnover was fixed directly: a 1–5 day signal has a half-life of days
against a momentum leg's months, so it is the most heavily discounted object in the space.
Consistent with, and independent of, the liquidity-provision argument that already closed
family 4.

## Related

- `notes/2026-08-17-averaging-over-estimation-windows.md`, `notes/2026-08-19-bagging-averaging-unstable-predictors.md`,
  `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the three prior accounts of
  vintage averaging, all of which stop at a predictor or an IR. This note supplies the
  portfolio-level version and is the answer to open question 6(a).
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — banding as the
  top-ranked cost-mitigation technique; here it acquires a theoretical home as the
  proportional-cost branch of the frictions literature.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — a second, independent
  reason fast signals lose under costs.
- `notes/2026-08-20-parametric-portfolio-policies.md` — the same crossing attempted from the
  estimation side rather than the theory side.
- `notes/2026-08-20-trading-diversification-combining-signals.md` — what happens to the cost
  term when several targets are averaged before trading.
