---
title: "Momentum Crashes / Momentum Has Its Moments (paired sources)"
authors: Daniel, Moskowitz (2016); Barroso, Santa-Clara (2015)
year: 2016, 2015
venue: Journal of Financial Economics (both, venue tier 1); Daniel–Moskowitz also NBER WP 20439
url: https://www.sciencedirect.com/science/article/pii/S0304405X16301490 ; https://www.sciencedirect.com/science/article/abs/pii/S0304405X14002566
citations: Daniel–Moskowitz (2016) 919 (OpenAlex, checked 2026-08-17 — not indexed in Semantic Scholar under its DOI); Barroso–Santa-Clara (2015) 623 (Semantic Scholar, same date)
sample_period: Daniel–Moskowitz 1927–2013; Barroso–Santa-Clara US ~1927–2011 (approximate; full text not retrievable this session)
markets: Daniel–Moskowitz US equities plus cross-asset momentum checks; Barroso–Santa-Clara US equities (with international checks)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

Momentum's unconditional average return is high and its unconditional volatility is
moderate, but its return distribution is **left-skewed with rare, persistent, deep
drawdowns**. Both papers argue this tail is partly forecastable, and they forecast it two
different ways.

**Daniel–Moskowitz (2016) — the economic story.** Crashes occur in *panic states*: after
sustained market declines and when market volatility is elevated. Critically, they are
**contemporaneous with market rebounds** — the strategy loses when the market turns back up,
not when it falls. The mechanism is optionality on the short leg. After a large market
decline, the past-loser portfolio is populated by firms whose equity has become deeply
out-of-the-money and highly levered; that equity behaves like a call option on firm value,
so its beta rises sharply and its payoff becomes convex in the market. Shorting that
portfolio is shorting a call. When the market rebounds, the losers' convex payoff dominates
and winners-minus-losers takes a large loss. The conditionally high premium the market
attaches to those option-like payoffs is why ex-ante expected momentum returns are *low*
precisely in panic states.

**Barroso–Santa-Clara (2015) — the statistical story.** Momentum's own risk is highly
persistent and therefore predictable from its own recent realized variance, and momentum
volatility rises going into crashes. Scaling exposure inversely to forecast volatility
therefore de-risks ahead of the tail.

The two are complementary: Daniel–Moskowitz condition on *market* state and forecast both
mean and variance; Barroso–Santa-Clara condition only on the *strategy's own* variance.

## Construction recipe

**Barroso–Santa-Clara volatility scaling**
- Estimate realized variance of the momentum strategy's own daily returns over a trailing
  **126 trading days** (~6 months), as the mean of squared daily returns.
- Annualize; set the scaling factor to (target vol) / (forecast vol), with a target of
  **12% annualized**.
- Apply the scalar to the long and short decile portfolios; the weight is time-varying and
  is not capped at one in the original (leverage is used when forecast vol is low — a point
  that matters below).
- Signal, sort, and rebalance are otherwise the standard 12-1 monthly momentum construction.

**Daniel–Moskowitz dynamic weighting**
- Define a *bear/panic state* from market-level variables: a negative cumulative market
  return over a long trailing window (on the order of two years) combined with elevated
  market volatility. This is a **market-level, not book-level** state variable.
- Forecast momentum's conditional mean (using the panic-state indicator and its interaction
  with market volatility) and its conditional variance.
- Set the weight on the strategy so that conditional volatility of the scaled strategy is
  proportional to its conditional Sharpe ratio — the mean-variance-optimal dynamic scale,
  rather than a constant-volatility target. This distinction matters: constant-vol targeting
  ignores that expected return *itself* falls in panic states, so it de-risks less than
  optimally exactly when the premium is worst.

## Robustness evidence (qualitative only)

- The crash phenomenon appears in multiple asset classes, not only US equities, and across a
  very long (multi-decade, pre-war-inclusive) sample.
- Volatility of momentum is strongly autocorrelated — that part is about as robust as
  empirical finance gets and is not specific to momentum.
- Both risk-management schemes are widely replicated in follow-up work; the general finding
  that scaling momentum by its own trailing volatility improves risk-adjusted outcomes is one
  of the more reproducible practitioner-relevant results in the area.
- Known weakness for our purposes: **both papers evaluate long-short winners-minus-losers**,
  and both allow leverage. Neither is a long-only study.
- Both are essentially costless in the headline tests; volatility scaling adds turnover on
  top of an already high-turnover strategy, which is under-charged in the papers.

## Implementability here

**This is the note with the sharpest tension against the lab's own results, and reading it
carefully resolves the tension rather than overturning either side.**

`experiments/learnings.md` records that the correctly-specified "basket's own realized vol"
trim is *worse than deleting the overlay entirely*, and that the champion's accidental
winner was a **defensive-cohort** stress trigger — style-orthogonal to the momentum book.
The lab's conclusion: "measuring the thing you are de-risking is precisely the wrong
signal", because a momentum basket's volatility rises in melt-ups as readily as in crashes.
Barroso–Santa-Clara say the opposite: scale by the strategy's own realized vol.

**The reconciliation is the long-short/long-only distinction, and it is not a quibble.**
The object whose volatility Barroso–Santa-Clara measure is *winners minus losers* — a
market-neutral-ish spread whose variance is driven by cross-sectional dispersion and by the
loser leg's rising beta, i.e. by exactly the convexity Daniel–Moskowitz identify. A
long-only momentum basket has no short leg; its realized volatility is dominated by plain
market beta, so it is high in violent up-moves as well as down-moves. Measuring it therefore
produces a trigger that fires on melt-ups — which is precisely what the lab observed
empirically. **So the lab's refutation of basket-own-vol trimming and the paper's endorsement
of strategy-own-vol scaling are consistent; the papers' mechanism simply does not survive
dropping the short leg.** Do not re-import Barroso–Santa-Clara as a reason to revisit
basket-own-vol trimming — this note is evidence *against* that, not for it.

The same argument caps how much Daniel–Moskowitz can offer here. Their crash mechanism is
short-leg optionality; a long-only book never shorts the convex losers and so does not own
the crash they are managing. The headline benefit should be assumed largely unavailable.

What is left that is genuinely worth considering, ranked honestly:

- **The panic-state indicator is style-orthogonal and market-level**, which is the one
  property the lab has found to work (the defensive-cohort trigger). Its specification is
  also a *conjunction* — long-horizon negative market return **and** elevated market
  volatility — and it drives a *continuous* scale, not a binary switch. That distinguishes
  it mechanistically from the three refuted overlays (200dma per-asset filter, binary
  SPY-trend switch, drawdown-state brake), all of which were single-variable and/or binary.
- **But the lab's prior on this whole family is now heavily negative**, and two specific
  learnings must be honored by any such candidate: the trigger has to react faster than the
  monthly rebalance cadence (a monthly-only check made a sound crash signal look like a
  no-op), and the *release* rule must not be slower than the recovery (the drawdown brake
  failed on exactly that, staying de-risked into a strong recovery year). Daniel–Moskowitz's
  two-year trailing market return is a **slow, lagging state variable** — structurally the
  same defect as the refuted drawdown brake. This is the reason to rank the idea low, and it
  should be stated in any hypothesis built on it rather than discovered again.
- **Leverage is not available.** Both schemes scale up when forecast volatility is low; this
  repo is capped at gross leverage ≤ 1.0. A long-only implementation can only ever take the
  *de-risking* half of the scalar, which is the half that costs return. Any expectation
  drawn from these papers must be discounted for that asymmetry — a one-sided scaler is a
  materially different and worse object than the one they test.
- **Costs.** 126-day-vol scaling changes exposure continuously; at 15 bps/side that is real.
  The learnings file also notes turnover reduction is a spent lever at current levels, which
  cuts the other way — there is little cost headroom to give away.

## Related

- `2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the base signal whose tail these
  papers manage.
- `experiments/learnings.md`: "A headline mechanism in this repo was mis-specified" (the
  defensive-cohort finding), "De-risking overlays on momentum reliably backfire
  out-of-sample", "Drawdown-state braking is refuted", and the cadence lesson — all four are
  load-bearing for how this note should be used.
