---
title: "Dynamic modeling of mean-reverting spreads for statistical arbitrage — on-line estimation with discount factors"
authors: Triantafyllopoulos, Montana
year: 2009 (published online; Comput Manag Sci 8(1–2), 23–49)
venue: Computational Management Science (venue tier 2 — peer-reviewed but outside the finance journals the rubric tiers); read from the arXiv v3 preprint, which is the same paper
url: https://doi.org/10.1007/s10287-009-0105-8 (published); https://arxiv.org/abs/0808.1710 (the version read in full)
citations: 36 (Crossref `is-referenced-by-count` on the published DOI, checked 2026-10-26; the arXiv DOI record shows 0, which is a record-splitting artefact and not a second count)
sample_period: the two illustrations use daily closes 1980-03-23 → 2008-08-06 (a US equity pair) and 2006-05-23 → 2008-08-06 (a pair of commodity ETFs); the methodological content has no sample
markets: US equities and US-listed ETFs, two pairs only
tier: B− on the construction (peer-reviewed, the algorithm and its two theorems are fully specified and were read in full) and NOT RATED on performance, because the paper contains no strategy evaluation at all — see "Robustness"
validation_overlap: false
published_post_2018: false
---

## Mechanism

Tonight's cluster asked what a state-space construction looks like when it is kept `O(1)` and kept
*causal*. This source is the one that attacks the second half directly: its explicit purpose is to
replace the iterative, window-based maximum-likelihood calibration that the pairs-trading
state-space literature inherited from Elliott, Van der Hoek & Malcolm (2005, *Quantitative
Finance* 5(3), 271–276; 306 Crossref cites, **not obtained** — Taylor & Francis is closed and the
Adelaide repository handle that indexes it now 404s, so Elliott's model is restated here from this
paper's own full exposition of it, which reproduces its equations) with a **non-iterative
recursion that runs forward in time and never looks back.**

The parent model first. An observed spread `y_t` between two assets is treated as a noisy reading
of a hidden true spread `x_t`:

    x_t = A + B x_{t−1} + ε_t        (hidden state, ε_t ~ N(0, C²))
    y_t = x_t + ω_t                  (observation, ω_t ~ N(0, D²))

written from `x_t − x_{t−1} = a − b x_{t−1} + ε_t` with `A = a`, `B = 1 − b`. The paper derives the
mean-reversion condition explicitly: `E(x_t) → a/b` and `Var(x_t) → C²/(1 − (1−b)²)` **iff
`|1 − b| = |B| < 1`**, and both diverge geometrically otherwise. So **`|B| < 1` is the whole of
"this spread mean-reverts", and `B` is one number.**

The extension. Let `A` and `B` drift:

    y_t = A_t + B_t y_{t−1} + ε_t
    A_t = φ₁ A_{t−1} + ν_{1t},   B_t = φ₂ B_{t−1} + ν_{2t}

With `θ_t = (A_t, B_t)′` and `F_t = (1, y_{t−1})′` this is `y_t = F_t′ θ_t + ε_t`,
`θ_t = Φ θ_{t−1} + ν_t` — **a two-dimensional state**, again `O(1)` and again one filter per
spread, never a joint state across the cross-section. Theorem 1 gives sufficient conditions for
`{y_t}` to still mean-revert: either the static case (`φ₁ = φ₂ = 1`, `V_t = 0`, `|B₁| < 1`), or
`φ₁, φ₂` inside the unit circle with `V_t` bounded and `|B_t| < 1` eventually.

**The mechanism that makes this note worth writing is the estimation, not the model.** The authors'
diagnosis of the parent approach is worth quoting in substance: Elliott et al. calibrate by running
the EM algorithm to convergence over a look-back window of size `N`, re-running it each time the
window shifts; `N` must be chosen so that the parameters are constant within the window; too small
biases the estimates, too large invalidates the modelling assumptions; EM converges slowly; and a
vanilla EM gives **no measure of parameter uncertainty**. Their replacement is a conjugate Bayesian
recursion in which the evolution covariance is not estimated at all but *implied* by **discount
factors**.

## Construction recipe

Priors: `θ₁ | σ² ~ N₂(m₁, σ² P₁)`, `σ² ~ IG(n₁/2, d₁/2)`. The full recursion, per step:

    R_t = Φ P_{t−1} Φ + V_t          Q_t = F_t′ R_t F_t + 1      e_t = y_t − F_t′ Φ m_{t−1}
    K_t = R_t F_t / Q_t              m_t = Φ m_{t−1} + K_t e_t    P_t = R_t − K_t K_t′ Q_t
    r_t = y_t − F_t′ m_t             n_t = n_{t−1} + 1            d_t = d_{t−1} + r_t e_t
    S_t = d_t / n_t

**The discount-factor trick.** Rather than estimating the evolution covariance `V_t`, take `P₁` and
`V_t` diagonal and set

    V_t = diag( δ₁⁻¹(1 − δ₁) φ₁² p_{11,t−1} ,  δ₂⁻¹(1 − δ₂) φ₂² p_{22,t−1} )

so that `R_t = diag(φ₁² p_{11,t−1}/δ₁, φ₂² p_{22,t−1}/δ₂)`: moving from `t−1` to `t`, the prior
variance of `A_t` is inflated by `1/δ₁` and that of `B_t` by `1/δ₂`. **`δ = 1` means no stochastic
evolution (the parameter is constant); `δ < 1` means the filter forgets, and faster for smaller
`δ`.** One scalar per state component, bounded in `(0, 1)`, replaces an entire covariance matrix.

Uncertainty comes free from the conjugate structure: `θ_t | y^t ~ t₂(n_t, m_t, P_t S_t)`, so a
`(1 − γ)%` interval for `B_t` is `m_{2t} ± t_{γ/2} √(P_{22,t} S_t)`, and the one-step predictive
interval for `y_{t+1}` is `f_{t+1} ± t_{γ/2} √(Q_{t+1} S_t)`. **The monitoring rule is then: track
the posterior mean of `B_t` and its credible band, and declare mean reversion lost when `|B̂_t|`
and its band leave the unit interval.**

Diagnostics, all sequential: the mean squared standardised forecast error (should be ≈ 1 if the fit
is good), the predictive log-likelihood in closed form, sequential Bayes factors, AIC and BIC.

**Theorem 2** gives the limit of `P_t` in closed form provided `δ_j < φ_j²`, with geometric
convergence — i.e. **the filter reaches a steady-state gain**, which is the fact that connects this
construction back to the EWMA equivalence in the companion notes. The authors also note that prior
sensitivity is negligible given a reasonable amount of data, since initial information is deflated
over time; their own illustrations simply use `m₁ = (0,0)′`, `P₁ = p₁ I₂` with `p₁` large, `n₁ = 3`,
`d₁ = 1`.

**Building the spread itself, recursively.** The hedge ratio `β_t` in `y_t = p⁽¹⁾_t − β_t p⁽²⁾_t`
need not be an OLS fit on history. The paper gives **flexible least squares** (Kalaba–Tesfatsion),
which minimises

    C(β; μ) = Σ_t (p⁽¹⁾_t − β_t p⁽²⁾_t)² + μ Σ_t (β_{t+1} − β_t)²

— one scalar `μ` penalising temporal change, with `μ → ∞` recovering OLS — and has a purely
recursive estimator. The authors record an algebraic connection between FLS and the Kalman filter.
**This is the single most directly reusable object in the paper: a causal, one-parameter,
time-varying regression coefficient with no likelihood maximisation anywhere.**

The trading rule attached is deliberately minimal: long the spread when `y_t > x̂_t`, short when
`y_t < x̂_t`, with an entry threshold `z_t` to clear costs left as an open question the authors
decline to answer (they list candidate approaches from the literature and move on), along with exit
rules, stop-losses, and how to select pairs at all.

## Robustness evidence (qualitative only)

**The honest headline is that this paper contains no strategy evaluation.** Its "experimental
results" are (i) Monte Carlo on simulated data and (ii) two illustrations on historical closes in
which the filter's verdict on whether a spread mean-reverts is compared against three standard
cointegration tests (ADF, Phillips–Perron, Phillips–Ouliaris). **No returns, no costs, no P&L, no
out-of-sample test of the trading rule.** Taken on its own terms it is a *monitoring* paper, and
the right tier for the construction is B− with performance unrated. The folder should not let the
`statistical-arbitrage` keyword make it sound like more than that.

What the illustrations do establish, qualitatively: the on-line `|B̂_t|` monitor agrees with the
formal cointegration tests **most of the time but not always** — in one example two of three tests
agreed with the monitor and the third did not; in the other, two of three agreed on the full sample.
The authors' own summary is that the model "seems to generally agree with most formal cointegration
tests" and that "further formal comparisons and more detailed studies will be needed". That is an
appropriately weak claim for the evidence.

**Two methodology concerns found by reading rather than reported by the authors**, both recorded
because they affect how the recipe should be used here:

1. **The hyperparameters are still chosen by maximising the likelihood over the data.** §4.4 offers
   two routes — optimise `(φ₁, φ₂, δ₁, δ₂)` by likelihood subject to `δ_i < φ_i²`, or set
   `φ₁ = δ₁ = 1` and optimise only `(φ₂, δ₂)` — and the real-data illustrations use **full
   optimisation of all four**. So a framework whose stated motivation was to escape iterative
   full-window MLE still selects its four free knobs by in-sample likelihood. **This is the same
   trap as the beta note's, in a literature explicitly built to avoid it — which is what makes it a
   pattern rather than one author's lapse.**
2. **The reported `φ₂` values in both illustrations are far outside the unit circle**, while §3.2
   states `φ₁, φ₂` are "usually assumed to lie inside the unit circle so that `A_t` and `B_t` may be
   weakly stationary". The paper does not reconcile this. It may be an artefact of the
   `δ_i < φ_i²` constraint pushing `φ` upward (a larger `φ²` admits a smaller, i.e. more
   forgetful, `δ`), but as printed the fitted model violates the stationarity assumption its own
   Theorem 1(b) rests on. **Do not copy their numeric settings; derive `δ` from the forgetting
   half-life you want and leave `φ = 1`, which is the Corollary-1 route the authors themselves
   offer.**

## Implementability here

**What transfers: the estimation pattern. What does not: the strategy.**

**1. The long-only constraint bites hard, and the paper offers nothing on it.** A spread position is
long one leg and short the other by construction; the rule above takes a short position half the
time. On this lab's book only the cheap side of a residual is tradeable, which means at most
**half of the signal's occurrences are expressible**, and the half that is expressible is the
"this name is cheap relative to its pair" half. `program.md` requires a `statistical-arbitrage`
candidate to say how the missing short leg is handled; this source does not help, because it never
considers the constraint. The honest adaptation is a **long-only overweight of the cheap leg against
the eligible pool**, not a pair.

**2. Costs are an open question in the paper and a binding gate here.** The authors explicitly leave
the entry threshold `z_t` — the thing that decides whether a trade clears costs — unresolved. Under
protocol v3 the cost model is per-name liquidity tiers (15/20/30/40 bps per side) plus UK/HK/FR/IT/ES
transaction taxes, with drift-correcting trades charged, and the paper's own framing targets
"aggressive strategies that execute a trade at each single time tick" on high-frequency data.
**A construction designed for tick-frequency trading, ported to daily closes with 15–40 bps per side
and stamp duty, is a different object, and nothing in the source speaks to whether it survives.**

**3. The two things genuinely worth taking.**

- **Flexible least squares as a causal, one-parameter time-varying regression.** This is reusable
  far outside pairs trading: anywhere the lab currently fits a rolling-window regression coefficient
  per name (hedge ratios, betas, factor loadings), FLS replaces "pick a window length `W`" with
  "pick a change penalty `μ`" and makes the estimate a recursion rather than a sequence of
  independent fits. It estimates **one scalar for the whole panel**, not one per name per date,
  which is the right side of the lab's parameter-count triage rule. And because `μ → ∞` recovers
  OLS, a candidate can be written with `μ` as its single knob and the OLS case as its own control.
- **The discount factor as the single forgetting knob.** `δ` ∈ (0,1) is the same object as the EWMA
  `α` of the companion notes approached from the Bayesian side, and Theorem 2's steady-state limit
  is the formal statement that the two coincide once the filter converges. So the lab can set `δ`
  from a target half-life in closed form instead of maximising anything — **which removes concern
  (1) above entirely and makes the construction pass `causality_check` by design.**

**4. The free diagnostic.** `|B̂_t| < 1` with a credible band is a **mean-reversion monitor**, and a
monitor is not a trial. Running it across the eligible panel's residuals — against a market or
regional ETF leg, which the hindsight guard permits — answers "is there anything here to revert at
all?" before a `statistical-arbitrage` candidate is written. Given that the lab's residual-reversal
leads have repeatedly collapsed into one mechanism, a cheap screen that says *where* and *whether*
reversion exists is better value than another construction on top of the same return stream.

**Pitfalls.** (i) The model's observable is a spread, i.e. a difference of **price levels**, not
returns — porting it to returns changes the object. (ii) Both illustrations are single pairs chosen
after the fact; pair selection is explicitly named by the authors as unsolved, and a pair found by
searching a ~1,400-name panel for cointegration is a multiple-testing problem of exactly the kind
the deflated-Sharpe bar exists to price. (iii) `Q_t = F_t′R_tF_t + 1` carries `y_{t−1}` inside `F_t`,
so the filter's gain depends on the spread's own level — on a spread that is not demeaned this
couples scale and adaptation, and Theorem 2's limit for `p₂₂` is itself a function of the
equilibrium mean `μ`.

## Related

- `notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md` and
  `notes/2026-10-26-optimal-exponential-weights-signal-to-noise.md` — the discount factor `δ` here
  and the smoothing constant `α` there are the same knob; Theorem 2's steady state is why.
- `notes/2026-10-26-learning-about-beta-kalman-filtered-loadings.md` — the first instance of the
  full-sample-hyperparameter trap. This note is the second, and the second is the one that makes it
  a pattern.
- `experiments/learnings.md` — the lab's residual-reversal leads collapsing into a single mechanism,
  and the standing parameter-count triage rule that FLS's single `μ` is on the right side of.
- **Unobtained pointer for a later session:** Elliott, Van der Hoek & Malcolm (2005), *Quantitative
  Finance* 5(3), 271–276, `10.1080/14697680500149370`, 306 Crossref cites — the parent model.
  Closed at Taylor & Francis; `digital.library.adelaide.edu.au` and the `hdl.handle.net/2440/17846`
  handle both return HTTP 404 (the repository has moved and the handle was not re-minted). Its model
  and its EM calibration are restated in full by the paper read here, so a direct read would add the
  original's simulation study and nothing structural.
