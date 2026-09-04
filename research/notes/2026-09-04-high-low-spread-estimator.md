---
title: "A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices"
authors: Corwin, Schultz
year: 2012
venue: The Journal of Finance 67(2), 719–760 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1111/j.1540-6261.2012.01729.x
citations: 1009 (Crossref, checked 2026-09-04); 1030 (Semantic Scholar, checked 2026-09-04)
sample_period: 1926–2005 (US historical application); 1993–2005 (intraday TAQ validation)
markets: US exchange-listed equities; independently validated on 43 exchanges worldwide by Fong–Holden–Trzcinka
tier: A
validation_overlap: false
published_post_2018: false
---

**Text read**: the authors' 2009 NBER/Microstructure-Meetings conference PDF
(`users.nber.org/~confer/2009/mms09/Corwin_Schultz.pdf`) in full — derivation, practical
adjustments, comparison against the Roll and Effective Tick estimators, and the TAQ validation.
The published JF article is the revised version of this manuscript; the estimator's algebra and
the two practical adjustments below are the ones that appear in the published form and in every
subsequent implementation, so they are safe to rely on. Any table-level number in the published
version could differ from the conference draft, so no accuracy figure is quoted here that this
folder does not independently have from Fong–Holden–Trzcinka.

## Mechanism

The estimator rests on two claims, both structural rather than empirical.

**First**, over a trading day the observed **high** price is almost always a buy that executed at
the ask, and the observed **low** is almost always a sell that executed at the bid. So the observed
high-to-low ratio is not a pure measure of how far the stock's *value* moved; it is the value range
**inflated by one full bid–ask spread**. Every daily range in a panel of daily bars is therefore a
volatility measurement contaminated by a transaction-cost measurement, and the two are additive in
logs.

**Second — and this is the identification** — the two components scale differently with the length
of the measurement interval. The **variance** component of a log high-low range is proportional to
elapsed time: doubling the window doubles it. The **spread** component is *constant*: a two-day
high is still an ask and a two-day low is still a bid, so the same single spread inflates the
two-day range that inflated each one-day range. Comparing the sum of two consecutive one-day
squared log ranges against the single two-day squared log range therefore gives two equations in
two unknowns — volatility and spread — and both are identified.

This is why the estimator matters to a lab that has closed a whole family on the finding that every
range statistic it screened was a **level of volatility** in disguise. Corwin–Schultz is the one
range construction in the literature whose entire design purpose is to *remove* the volatility
component and keep the residual. It is not a width measure. Whether the removal actually works on
this universe is an empirical question with a free answer (below), but the object is categorically
different from the ten already screened here.

## Construction recipe

For two consecutive trading days `t` and `t+1`, with `H` and `L` the daily high and low:

```
beta  = ( ln(H_t     / L_t    ) )^2  +  ( ln(H_{t+1} / L_{t+1}) )^2
gamma = ( ln( max(H_t, H_{t+1}) / min(L_t, L_{t+1}) ) )^2

alpha = ( sqrt(2*beta) - sqrt(beta) ) / (3 - 2*sqrt(2))  -  sqrt( gamma / (3 - 2*sqrt(2)) )

S     = 2 * ( exp(alpha) - 1 ) / ( 1 + exp(alpha) )
```

`S` is the estimated **proportional** (percent) effective spread for that two-day window. Note the
sign structure the authors flag explicitly: holding `beta` fixed, a larger `gamma` implies a
*smaller* spread, and the root of the quadratic is chosen to preserve that relation.

**Two practical adjustments, both required.**

1. **Overnight returns.** Markets close overnight, so the two-day range picks up the overnight move
   while the two one-day ranges do not — which biases the spread estimate. The fix: if the close on
   day `t` lies **below** day `t+1`'s low, treat the difference as an overnight rise and *decrease*
   both of day `t+1`'s high and low by that amount; if the close on day `t` lies **above** day
   `t+1`'s high, *increase* both by the difference. Only cases where the close falls outside the
   next day's range are adjusted. The authors deliberately do **not** use the close-to-open return
   for this, on the grounds that a close-to-open change is often bid–ask bounce rather than a true
   value change (and, at the time, open prices were unreliable or missing in CRSP for a long
   stretch).
2. **Negative estimates.** When observed two-day volatility is large relative to the one-day
   ranges, `alpha` goes negative and the implied spread is negative — an artifact of estimating a
   bounded quantity from a noisy difference, not a signal. The authors' recommended handling is the
   simple one: **set negative two-day estimates to zero before averaging**, which they report gives
   more accurate window-level estimates than either keeping the negatives or dropping those
   observations.

**Aggregation.** The window-level estimate is the average of the overlapping consecutive two-day
estimates over the window, after zeroing negatives. The paper requires at least 12 daily
observations for a monthly estimate, and reports that **weekly** estimates (five consecutive
trading days) also work — so the estimator does not need a long window to be usable.

**A by-product worth knowing.** The same two equations that solve for the spread also solve for a
**spread-adjusted range estimate of variance**. If a range volatility estimator is ever wanted on
this universe again, this is the version that is not contaminated by transaction costs — which is a
different defect from the one that closed `range-variance` here, but a real one.

## Robustness evidence (qualitative only)

- **Validated against intraday ground truth.** The paper's central test is against effective
  spreads computed from intraday TAQ data over more than a decade, at both weekly and monthly
  frequencies, and both on correlation with the benchmark and on the deviation of the *level* from
  the benchmark. It is compared head-to-head against the two established daily-data alternatives,
  the Roll covariance estimator and the Effective Tick estimator, and it wins on both dimensions in
  the pooled sample and in each of the tick-regime subperiods examined.
- **Independently re-validated on a global sample.** Fong–Holden–Trzcinka's 43-exchange horserace
  (see the companion note) is the strongest external evidence: High-Low is consistently among the
  top three percent-cost proxies on cross-sectional correlation, portfolio time-series correlation
  and level accuracy, and it is significantly the **best of all daily-data proxies at capturing the
  level** of percent realized spread and percent price impact. That is independent replication on
  a different sample, a different data vendor and a different set of markets.
- **Known boundary.** For the very largest, most heavily traded stocks the Effective Tick estimator
  correlates better with intraday effective spreads than High-Low does. The authors note that the
  quote-clustering assumptions Effective Tick relies on are venue- and regime-specific, which is
  why they do not treat it as a general-purpose alternative — but the boundary is real, and this
  repo's universe is entirely large stocks. **This is the single most important discount on the
  note.**
- **Assumptions that can fail.** The derivation assumes the high is a buy and the low is a sell,
  continuous trading through the day, and no discreteness. None is exactly true; the paper is
  candid about this and the negative-estimate handling is a symptom of it. Thin trading is the
  worst case: a stock that barely trades has a range set by a handful of prints and the
  identification degrades.
- **Long-horizon applicability.** The estimator has been applied to daily data going back to the
  1920s, which is evidence that it does not depend on modern market structure to be computable —
  though "computable" is weaker than "accurate", and the pre-TAQ accuracy is unverifiable by
  construction.

## Implementability here

**This is directly buildable on this repo's data as of the 2026-08-29 contract change.**
`generate_weights(prices, aux)` supplies `aux["high"]`, `aux["low"]` and `prices` (closes) on the
same index and columns. The estimator needs nothing else — **no volume, no currency, no share
count, no fundamentals.**

**Why it is worth a screen despite two closed families.**

- Against **`liquidity-volume`**: it is a *percent-cost* proxy, the class Fong–Holden–Trzcinka show
  is far better measured from daily data than the cost-per-volume class `ILLIQ` belongs to. It
  contains no volume, so it cannot be a venue-volume sort, a size sort, or a
  turnover sort in costume — the three explanations that have absorbed most of this family's
  screening effort. It is the cleanest available test of whether the family's content is liquidity
  or is volume.
- Against **`range-variance`**: all ten mechanisms screened there sort on a cross-sectional level of
  *width*, and the lab established that the width level **is** the survivorship artifact. This is
  the first range object proposed here that is a *difference* of two range statistics designed to
  cancel exactly that level. It is not a proposal to reopen the family on hope; it is a proposal to
  test the one construction the family's own identified cause does not automatically explain.

**A pre-registered screen that decides it either way, before any trial is spent.** Compute the
Corwin–Schultz spread on a trailing quarter and measure `spearman(CS_spread, trailing 21-day range
volatility)` cross-sectionally.

- **If |spearman| is high** (say ≥ 0.7, the neighbourhood where `MAX(5)` sat against 21-day vol at
  +0.872 and where de-levelled range vol sat against the raw GK level at +0.563), then the
  variance cancellation has failed on this universe and the object is the level artifact again.
  **Record `range-variance` closed an eleventh time on its own cause, and close the
  percent-cost route with it** — no trial.
- **If |spearman| is low**, the cancellation worked, and the lab holds a liquidity characteristic
  that is orthogonal to both volatility and volume — which is a genuinely new axis on this
  universe and the first `liquidity-volume` object whose null hypothesis is not "it's volume".

Two further free controls, both cheap and both discriminating, to run in the same screen:
`spearman(CS_spread, region-relative log ADV)` (if this is near −0.9 as region-relative `ILLIQ`
was, it is the size ranking again) and the **region-demeaning contrast** that
`notes/2026-09-04-global-liquidity-proxy-horserace.md` sets out: because a percent-cost proxy is
already unit-free, the lab's own 2026-09-03 rule predicts region-demeaning should help it
**much less** than it helped `ILLIQ`. A percent-cost proxy that gains just as much from
region-demeaning as `ILLIQ` did would falsify the venue-unit account of the current family lead,
which is a more valuable outcome than a passing screen.

**Pitfalls, in order of how likely each is to invalidate a result here.**

1. **The price basis of `aux["high"]` and `aux["low"]` must be checked first, and it is free.**
   The contract documents `prices` as USD-adjusted closes and `dollar_volume` as `close_usd *
   volume` with volume in native share units — it does *not* state whether high and low are
   USD-converted or native. It matters: the estimator's one-day terms are ratios within a day, so
   any per-day scale cancels, but `gamma` spans two days, so if high/low are USD-converted the
   two-day range legitimately absorbs the overnight FX move for the 13 non-USD regions while the
   one-day terms do not. That is a **mechanical inflation of `gamma` on exactly the foreign names**,
   which biases their spread estimates downward and makes the resulting sort partly a
   currency-volatility sort. If they are USD-converted, either estimate in native units (divide out
   the FX series, which is in the store) or restrict to USD names for the screen. **Determine this
   before computing anything.**
2. **Non-trading days must be dropped.** This repo's close series is forward-filled across foreign
   holidays; the volume panel is not. A stale bar has `H = L = close`, giving `ln(H/L) = 0` and a
   `beta` of zero while `gamma` stays positive — which forces a negative `alpha` and a zeroed
   estimate. Across 15 regions with non-overlapping sessions this would rank names by local
   holiday count. Use the volume panel's NaN pattern to identify and exclude non-trading days
   before forming two-day pairs, exactly as the Amihud note already warns for `ILLIQ`'s day-level
   screens.
3. **Do not skip the overnight adjustment.** It is three lines and the estimator is materially
   biased without it, and this panel — where "overnight" for a foreign name spans a full US
   session — is the worst case for skipping it.
4. **Do not skip the negative-to-zero step**, and use the authors' version (zero the *two-day*
   estimates before averaging), not the alternatives.
5. **The large-stock boundary is the real risk.** Effective Tick beats High-Low on the very largest
   stocks in the paper's own tests, and every name here is large. That does not make High-Low
   useless — it is still a top-three global proxy — but it means the expected dispersion in true
   spread across this universe is small, and a sort on a small-dispersion characteristic
   estimated with noise is mostly a sort on the noise. `SUMMARY.md` #68's big-stock rule applies
   with full force: **check that the estimated spread has meaningful cross-sectional dispersion on
   this universe before treating a sort on it as a signal.** This should probably be part of the
   same precondition screen.
6. **Cost profile is favourable.** An estimated spread over a trailing quarter is a slow
   characteristic, so a monthly-rebalanced tail book on it should turn over in the low
   single digits — the regime the current family lead occupies (1.2x, ~0.18%/yr of drag), not the
   13–19x the union books were paying. Nothing here needs the execution overlay to be viable.

**What this is not.** It is not a return premium and no source in this note claims one. The
hypothesis a candidate would test is that a *better-measured* liquidity characteristic ranks names
better than a worse-measured one — the same shape as the lab's own 2026-09-03 finding, where the
mechanism was measurement rather than a premium. Do not import a performance expectation from the
spread-premium literature into it.

## Related

- `notes/2026-09-04-global-liquidity-proxy-horserace.md` — Fong–Holden–Trzcinka, the independent
  global validation of this estimator and the source of the percent-cost / cost-per-volume
  distinction that motivates the screen above. Also the source of FHT, the *other* percent-cost
  proxy buildable here (closes only, no range), which is the natural second arm of the same screen.
- `notes/2026-09-04-commonality-in-liquidity-across-countries.md` — why raw `ILLIQ` levels are not
  comparable across venues, and why a proxy with no volume in it sidesteps that problem entirely.
- `notes/2026-08-29-range-based-volatility-estimators.md` — Parkinson / Garman-Klass /
  Rogers-Satchell. This note's estimator uses the same inputs to answer a different question, and
  its variance by-product is the transaction-cost-corrected version of those estimators.
- `experiments/learnings.md`, 2026-08-31 through 2026-09-02 — the `range-variance` closure: ten
  screened mechanisms, one identified cause (the cross-sectional width *level* is the survivorship
  artifact), and the recommendation that the family is unreachable on this universe. This note does
  not contest that finding. It observes that the identified cause does not automatically cover a
  construction built to difference the level away, and it proposes the free test that decides it.
- `experiments/learnings.md`, 2026-09-03 — the region-relative `ILLIQ` result and the transferable
  rule about units versus returns, which the region-demeaning contrast above is designed to stress.
