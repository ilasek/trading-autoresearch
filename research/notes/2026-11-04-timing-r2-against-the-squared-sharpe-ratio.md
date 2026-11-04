---
title: "Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?"
authors: Campbell, Thompson
year: 2008
venue: Review of Financial Studies 21(4), 1509–1531 (Tier 1)
url: https://doi.org/10.1093/rfs/hhm055 — read in full (32 pp.) from the Harvard DASH green-OA deposit, `dash.harvard.edu/bitstreams/7312037c-4c39-6bd4-e053-0100007fdf3b/download`
citations: 2776 (Crossref `is-referenced-by-count`, checked 2026-11-04); 2676 (Semantic Scholar by DOI, same date)
sample_period: monthly US data from 1871; forecast evaluation restricted to the CRSP era (from 1927), through end-2005; at least 20 years of data used before the first out-of-sample forecast
markets: US aggregate equity market (S&P 500 index), monthly and annual horizons
tier: A
validation_overlap: false
published_post_2018: false
---

**Taken as the [2026-11-03] entry's second-ranked aim — the CASH/POOL BOUNDARY — and it is the
source that aim's criterion was written for.** That entry's criterion: *admit a source only if it
treats the cash weight as a **decision** rather than a residual; a paper that merely allows a
risk-free asset in a mean–variance problem does not reach.* This paper's whole object is the
weight on the risky asset as a function of a conditioning variable, with the complement in the
riskless rate, under an explicit non-negativity-and-limited-leverage constraint. It reaches.

Zero prior coverage: fixed-string greps across all 258 prior notes returned
`Can Anything Beat the Historical Average` **0**, `Thompson` **0**, `cash holding` **0**,
`risk-free allocation` **0**, `partial investment` **0**, `optimal fraction in cash` **0**,
`cash weight` **0**, `utility gain` **0**, `timing the market` **0** — against `cash position` **1**
and `holding cash` **1**. Confirms the [2026-11-03] entry's reading that this is a genuine gap.

## Mechanism

**(1) The cash weight, written down as a decision.** Let `r_{t+1} = µ + x_t + ε_{t+1}` with `x_t`
a mean-zero predictor of variance `σ_x²` and `ε` of variance `σ_ε²`, and let the investor have
single-period mean–variance preferences with risk aversion `γ`. Two cases:

```
blind:     w  = (1/γ)·µ/(σ_x² + σ_ε²)          mean excess return = S²/γ
informed:  w_t = (1/γ)·(µ + x_t)/σ_ε²           mean excess return = (1/γ)·(S² + R²)/(1 − R²)
```

with `S` the **unconditional Sharpe ratio** of the risky asset and `R² = σ_x²/(σ_x² + σ_ε²)` the
regression `R²` of the return on the predictor. The informed denominator is `σ_ε²` rather than
`σ_x² + σ_ε²` precisely because the predictor's variation is now *expected* and therefore no longer
risk.

**(2) The yardstick, and it is the paper's single most transferable result.** The gain from seeing
`x_t` is

```
absolute:      (1/γ)·(R²/(1 − R²))·(1 + S²)        ≈  R²/γ
proportional:  (R²/(1 − R²))·((1 + S²)/S²)         ≈  R²/S²
```

so **the right thing to compare a timing `R²` against is the squared Sharpe ratio of the asset
being timed, at the same frequency.** Not zero, not statistical significance, not another model's
`R²` — `S²`. A predictor whose `R²` is a small fraction of `S²` cannot move the portfolio much
however significant it is; a predictor whose `R²` is comparable to `S²` is economically large even
when it looks statistically trivial. Both quantities are frequency-dependent and scale roughly
linearly in the horizon, so the comparison must be done at a single horizon.

**(3) The same arithmetic run backwards is an overfitting screen.** Because small `R²` already
implies large portfolio gains, **a large `R²` implies gains too large to be credible**: *"if you're
so smart, why aren't you rich?"* The paper states this as a prior — regressions with large `R²`
should be suspected of being spurious. The one legitimate exception is **horizon**: since `S²`
grows roughly in proportion to the horizon, a larger `R²` is believable at a longer horizon, which
is also why persistent predictors show `R²` rising with horizon without that being evidence of
anything.

**(4) Two weak restrictions, and they are the paper's empirical contribution.** Applied to an
expanding-window out-of-sample forecasting exercise:

- **Coefficient sign restriction** — set the slope to zero whenever its estimated sign disagrees
  with the theoretically expected sign. A short estimation window can easily produce a perverse
  sign, and a real investor would not act on one; setting it to zero is imposing the prior
  explicitly rather than pretending it is absent.
- **Forecast sign restriction (the floor)** — set the forecast of the equity premium to zero
  whenever the regression produces a negative value, i.e. refuse to forecast a negative risk
  premium.

Qualitatively: these restrictions **never worsen and almost always improve** out-of-sample
performance, and are enough to turn a set of predictors that mostly fail against the historical
average into a set that mostly beats it. They are *weak* in the sense that they require only a sign
from theory, not a magnitude.

**(5) A stronger restriction that does not reach this repo, recorded for completeness.** For
valuation ratios, a steady-state model (Gordon-growth style) pins not only the sign but the
*magnitude* of the slope, which removes the need to estimate a coefficient from a short, volatile
sample at all. The paper finds this helps further. It requires fundamentals and is out of scope
here; the general principle it illustrates is the one worth keeping — **a false restriction can
improve a forecast if it cuts the predictor's variance by more than it adds bias.**

**(6) The constrained portfolio, and the honest accounting of the gain.** Because a conditional
model raises the mean partly by taking more risk, the paper also reports a utility measure for a
`γ = 3` investor under **realistic portfolio constraints: no shorting of stocks and at most 50%
leverage, i.e. the weight on equities confined to `[0%, 150%]`**, with the variance input estimated
from a rolling five-year window of monthly data. The utility differences are stated in units of
annualised return, which makes them directly interpretable as **the annual fee or transaction cost
a user of the signal could pay before the edge disappears**. The paper notes that the gains are
*limited by* the leverage cap in combination with a high average equity premium.

## Construction recipe

1. **Fix a horizon.** Everything below must be computed at one frequency; `R²` and `S²` both scale
   with it.
2. **Estimate `S²`** for the thing being timed, on the same returns and the same frequency, in
   excess of the riskless rate.
3. **Estimate out-of-sample `R²`** for the timing signal on an expanding window, against the
   *prevailing* unconditional mean as the null (not the full-sample mean).
4. **Apply the two sign restrictions** inside the out-of-sample loop: zero the slope when its sign
   is wrong, floor the fitted premium at zero.
5. **Form the weight** `w_t = (1/γ)·(forecast/σ̂²)`, with `σ̂²` from a rolling window, then clip to
   the feasible range.
6. **Grade with `R²/S²`** for the proportional return gain and with the constrained-portfolio
   utility difference, in annualised-return units, for the fee the edge can bear.
7. **Reject on arithmetic** if `R² ≪ S²`.

## Robustness evidence (qualitative only)

- **Tier A on every column.** Top-tier venue, very high citation count, a sample spanning more
  than a century with the forecast evaluation restricted to the high-quality-data era, both
  monthly and annual horizons, and a stated multiple-testing posture: the authors say they
  **deliberately kept the methods simple to avoid the charge of reporting only the specifications
  that worked.** That is the rubric's methodology-honesty column answered in the paper's own words.
- **Multi-decade and sub-period reporting**, with the authors explicitly addressing the
  hardest-to-predict later part of their sample rather than averaging over it. The sub-period
  pattern itself is **not recorded here** under this folder's anti-lookahead rules.
- **It is a single market and a single asset — the aggregate US equity index.** No cross-country
  replication inside the paper. Its mechanism (2) is, however, an identity and does not depend on
  the market.
- **The restrictions are not neutral and the paper says so**: the forecast floor works by refusing
  a negative premium, which pays exactly when the realised premium is positive. The companion
  note records the response literature's quantification of that objection.
- **Costs are not modelled directly**, but the utility measure is denominated in annual return, so
  it *is* a cost budget — which is more useful here than a gross Sharpe.

## Implementability here

**The reachable part is a free pre-trial screen, and it is the strongest one this folder has found
for a whole family.**

`program.md`'s `seasonality-calendar` and any other **timing** construction has to move capital
between the eligible pool and cash. `learnings.md` already carries the structural half of the
argument: v3 measures Sharpe in excess of T-bills and the benchmark pool is **fully invested**, so
a cash position forfeits the equity premium the pool keeps earning. This paper supplies the
missing quantitative half, and the two compose into a refusal test that costs no trial:

> **The timing refusal test.** At the candidate's own rebalance frequency, compute (a) the pool's
> squared Sharpe `S²` in excess of the bill rate and (b) the out-of-sample `R²` of the timing
> signal against the prevailing mean. The best proportional improvement in expected portfolio
> return available to the construction is about `R²/S²`. If that is not large enough to cover the
> v3 cost bill of the implied turnover plus the pool's own head start, the candidate is refused
> before it is written.

Three riders specific to this lab.

- **The lab's feasible range is `[0, 1]`, not `[0, 1.5]`.** The paper's own observation is that its
  gains are *limited by* the leverage cap; with gross leverage capped at 1.0 the upper half of the
  conditional response is unavailable entirely, so the edge the test should be asked to clear is
  **larger** than the paper's, not equal to it. Only the downside half of the timing response —
  moving to cash — is reachable, and that half is the half that gives up the premium.
- **The sign restrictions transfer directly and should be the default, not an option.** They need
  no fundamentals, cost nothing, and apply to the cross-section too: *zero a score whose
  cross-sectional coefficient has the wrong sign in the trailing window, and floor a predicted
  excess return at zero.* The second is the long-only constraint stated as a forecast restriction
  rather than a weight restriction, which is a cheaper place to impose it. This is the same
  mechanism as `#376`'s one-bit truncation seen from the forecast side.
- **Run mechanism (3) as an overfitting alarm on the lab's own diagnostics.** Any candidate whose
  in-sample `R²` or IC implies a gain much larger than `S²` permits should be treated as
  mis-specified or leaking, not as a discovery. This is a cheap, mechanical complement to the
  deflated-skill bar: the bar asks whether the result survives the search; this asks whether the
  result is *too good to be a result at all*.

**What does not transfer.** The predictors themselves are valuation ratios, interest rates and
macro ratios — fundamentals and term-structure data this repo does not have and does not plan to.
Nothing in the empirical half of the paper is a candidate here. The mechanism, the yardstick, the
restrictions and the constrained-weight accounting are the whole import.

## Related

- `notes/2026-11-04-out-of-sample-prediction-failure-and-the-cumulative-sse-diagnostic.md` — the
  same night's companion and the direct counterparty to this paper. Read them together: this one
  says the restricted models beat the unconditional benchmark, that one says they do not, and the
  disagreement is itself the finding.
- `notes/2026-09-03-machine-learning-economic-restrictions.md` — the modern descendant of
  mechanism (5): theory-motivated restrictions as the thing that makes a learned signal
  implementable rather than the learner's flexibility.
- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md` — `#376`'s one-bit
  truncation test; the forecast floor here is the same restriction imposed one step earlier.
- `notes/2026-08-24-deflated-sharpe-ratio.md` and `notes/2026-08-24-multiple-testing-haircut.md` —
  the search-discount machinery that mechanism (3) complements from the plausibility side.
- `experiments/learnings.md`, protocol-v3 section, structural fact (i) — the fully-invested
  benchmark and the forfeited equity premium, which is the other half of the refusal test above.
