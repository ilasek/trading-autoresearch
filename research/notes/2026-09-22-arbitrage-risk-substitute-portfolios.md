---
title: "Does Arbitrage Flatten Demand Curves for Stocks?"
authors: Wurgler, Zhuravskaya
year: 2002
venue: Journal of Business 75(4), 583–608 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1086/341636
citations: 721 (Semantic Scholar, DOI lookup, checked 2026-09-22); 715 (Crossref
  is-referenced-by-count, same DOI, checked 2026-09-22). Read in full from the author's
  institutional mirror at parisschoolofeconomics.com (typeset journal version, 26 pp.).
sample_period: 1976–1989 (S&P 500 addition events); arbitrage-risk inputs estimated on
  daily returns over a [−365, −20] calendar-day pre-event window
markets: US equities (CRSP NYSE/AMEX/NASDAQ), 259 index-addition events
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

Textbook arbitrage keeps demand curves for individual stocks flat because a mispriced stock
can be offset against a **perfect substitute**. The paper's observation is that no such
substitute exists for an individual equity. An arbitrageur who buys a cheap stock and hedges
with the closest basket they can assemble is left holding the residual — the paper's
**arbitrage risk** — and the amount of that residual determines how hard they will lean on
the mispricing.

The prediction that follows is about *slope*, not about average returns: a stock whose
substitutes are poor has a **steeper demand curve**, so a given demand shock moves its price
further. The paper tests this with a demand shock whose direction, timing and approximate
size are known in advance and are unrelated to fundamentals — inclusion in a value-weighted
index — and finds the price response rising in arbitrage risk and in shock size, in the
predicted direction.

The general form worth carrying past the index-inclusion setting: **arbitrage risk is a
property of the hedge, not of the asset.** It is the variance the arbitrageur cannot lay
off, and it is what converts a demand shock into a price move. Anything that changes who can
hedge what — the size of the substitute set, the correlation structure, the tradability of
the offsetting leg — changes the elasticity of the price to flows.

The paper's most useful empirical by-product is not the demand-curve result at all. It is
the measurement of **how little of a single stock's variance is hedgeable**:

- Arbitrage risk `A` is on the **same order of magnitude as the stock's total variance**.
  Hedging with a carefully matched basket removes about **one-fifth** of the variance for a
  typical stock, and up to about three-fifths for a small minority. For some names hedging
  is effectively impossible — "short-sellers of these stocks may as well hold a risk-free
  asset rather than search for substitutes."
- The two constructions — `A₁`, the residual variance against the **market alone**, and
  `A₂`, the residual variance against **three industry-, size-, and book-to-market-matched
  stocks** — correlate at about **0.98** and have similar explanatory power. The elaborate
  matching buys almost nothing over a market-model residual.
- This agrees with independent evidence (Roll 1988) that daily-return `R²` against
  best-fitting models averages around 0.20.
- Arbitrage risk is **decreasing in size**: the correlation between `log(market value)` and
  `A` is negative and strongly significant.

That last pair of facts is the reason this note exists for this lab, and the reason is
developed under *Implementability* below.

## Construction recipe

**Arbitrage risk for a name `i`, in two versions.** Both are estimated on daily *excess*
returns over a trailing window (the paper uses `[−365, −20]` calendar days relative to the
event, i.e. roughly a year of daily data ending a month before the measurement date — a
gap that is a causality convenience here as well as there).

- `A₁` — regress the name's excess return on the market's excess return,
  `R_i,t − R_f,t = β_i (R_m,t − R_f,t) + ε_i,t`, and take `Var(ε_i)`.
- `A₂` — pick a small set of substitutes (the paper uses **three**) by sorting all
  same-industry names into quintiles on `|ΔMarketCap|` and `|ΔBook-to-Market|` relative to
  the subject name, ordering by size-quintile then B/M-quintile, taking the top three and
  breaking ties on the smaller capitalisation difference. Then regress
  `R_i,t − R_f,t = Σ_k β_k (R_sub_k,t − R_f,t) + ε_i,t` and take `Var(ε_i)`.
  Working in **excess** returns is deliberate: it removes the need to constrain the
  coefficients to sum to one to keep the position zero-net-investment.

The economic object is the variance of a **$1 long in the name against $1 short in the
best-available substitute basket**, which is why it is a residual variance and not a
covariance.

**The two derived quantities**, and they behave very differently:

- The **level**, `A` itself — an idiosyncratic-variance measure, nearly collinear with total
  variance in this data.
- The **hedgeable fraction**, `E / Var(R_i − R_f)` where `E = Var(R_i − R_f) − A` — the share
  of the name's variance a substitute basket can remove. This is a **ratio**, dimensionless
  in volatility, and it is the number the paper reports as ≈ one-fifth for a typical stock.
  A name with a low hedgeable fraction has no close substitutes and, by the mechanism, a
  steeper demand curve.

**Horizon caveat stated by the authors**: the measure is estimated at daily frequency, which
they concede is "surely much too short" relative to an arbitrageur's true horizon. Their
defence is that the **cross-sectional ranking is preserved** across frequencies — hedging
that is hard daily is hard at longer horizons. That is an assumption, not a result.

## Robustness evidence (qualitative only)

- The `A₁` ≈ `A₂` finding (correlation ≈ 0.98) is itself a robustness result: the measure is
  insensitive to how the substitute set is chosen, which is unusual and is what makes the
  construction portable to universes without industry or book-to-market data.
- The hedgeability magnitude is independently corroborated by Roll's daily-return `R²`
  evidence from a different literature and a different method.
- The procedure is explicitly modelled on Pontiff (1996), who used ten open-end funds as the
  substitute universe for closed-end funds — so the "residual against a small matched
  basket" construction predates this paper and has been used in at least two settings.
- **Gaps against the rubric.** Single market (US), single event type (index additions), and
  a sample period that is a narrow window by this folder's usual standard. Transaction costs
  of the *hedge* are discussed qualitatively (the authors note that hedging with many assets
  would be "prohibitively" costly, which is why the substitute set is capped at three) but
  are not modelled in the tests. Multiple testing is not discussed. The paper is Tier A on
  venue, citation weight and the internal consistency of its two measures — not on sample
  breadth.
- The paper makes **no claim about average returns**. It is about price response to flow.
  Anyone reading it as "low-hedgeability stocks earn more" is reading in something that is
  not there; the return-sign question is the subject of
  `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md`.

## Implementability here

This is the note in tonight's cluster with a construction this repo can actually build, and
the reason it matters is a collision with the lab's own strongest measured fact.

**The problem this solves.** `experiments/learnings.md` (2026-09-06 onward) identifies the
**volatility level** as this universe's dominant survivorship artifact — high trailing
volatility predicts high forward return here because the constituents are current survivors
— and fourteen mechanism screens have now reduced score after score to it. Every
limits-to-arbitrage variable in the standard toolkit (IVOL, total vol, Amihud `ILLIQ`) is a
*level*, and on this universe a level is the artifact. `A₁` and `A₂` are levels too and
inherit the problem wholesale: the paper says so itself, reporting `A` as the same order of
magnitude as total variance.

**The escape is the ratio.** `E / Var` — the fraction of a name's variance that a substitute
basket removes — is scale-free in volatility by construction. Two names with the same
trailing volatility can have very different hedgeable fractions, and it is the fraction, not
the level, that the mechanism says governs how far a flow can push a price. This is the
argument the 2026-09-20 open question asked every new score to supply: *what does it vary
that the refuted ones did not?* It varies the **correlation structure around the name**,
which no functional of the name's own price path can see, and which the lab has never
ranked on.

**How to build it on this repo's data**, with the fundamentals stripped out:

- The universe is ~145 instruments. `A₂`'s matching needs industry and book-to-market, and
  this repo has neither. **The paper's own 0.98 correlation says that does not matter**: use
  a data-driven substitute set instead — the `k` names (k ≈ 3–5) with the highest trailing
  correlation to the subject over the estimation window, excluding the subject. That is the
  same object the matching was a proxy for.
- Regress the subject's daily return on the substitute basket's daily returns over a
  trailing ~250-day window ending a month before the measurement date, take the residual
  variance `A`, and form `E/Var = 1 − A/Var`.
- Everything is OLS on daily closes, deterministic, and causal by construction if the window
  is rolled. `strategies/lib/features.py` already has the cross-sectional normalisation
  helpers; the regression is the only new machinery.
- **ETF-versus-stock is the natural first cut and it is nearly free.** 42 of the ~145
  instruments are ETFs, which are baskets and should be the *easiest* things in the universe
  to hedge with other baskets; single names should be the hardest. If `E/Var` does not
  separate those two groups sharply, the measure is not working here and the vein closes for
  zero trials. That is a precondition, not a result, and it should be checked first.

**Pre-registered discipline this construction needs, given the lab's history.** Before any
book: correlate `E/Var` with 21-day Garman–Klass volatility and with 12−1 momentum on the
train split. The whole claim is that it is *not* the volatility level; if `|spearman|`
against the volatility level is large, it is the artifact in a new costume and the lab
should say so and stop, exactly as it did with `beta-minus` (2026-09-17) and `VSP`
(2026-09-19).

**What it cannot do here.** Two limits, both real:

- The paper's *test* is an index-inclusion event study. This repo has no point-in-time index
  membership and no flow data, so the demand-shock half of the model is unreachable. Only
  the arbitrage-risk half transfers.
- The mechanism is about **price response to flow**, not about expected return. A low-`E/Var`
  name is predicted to move further per dollar of demand — in *either* direction. Turning
  that into a long-only book requires a separate reason to believe the flow is positive, and
  this note does not supply one. Its honest use is as a **conditioning variable** on a score
  the lab already has, not as a score.

Pitfalls:

- With 145 instruments and a `k`-name substitute basket chosen on trailing correlation, the
  selection is in-sample by construction. Roll the selection window and lag it; the
  `[−365, −20]` gap in the original is a free template.
- Do not raise `k`. The paper caps the basket at three explicitly because hedge transaction
  costs scale with it, and its 0.98 result says a bigger basket buys nothing anyway.
- Volume is not forward-filled in this repo's `aux` frames and is NaN on foreign holidays.
  This construction needs closes only, so it sidesteps that — keep it that way.

## Related

- `2026-09-22-limits-of-arbitrage-performance-based.md` — the theory this measures, and the
  reason an un-hedgeable residual is what deters a specialist.
- `2026-09-22-arbitrage-asymmetry-ivol-sign-flip.md` — what the sign of the return effect is,
  once you know which side of the mispricing a name is on.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the other arbitrage-cost
  proxy in this repo, and the one the lab has already had a measurement win with
  (`lv_illiq_region_relative`, 2026-09-03), also by making a *relative* quantity out of a
  level.
- `experiments/learnings.md`, 2026-09-06 onward — the volatility-level survivorship artifact
  that the `E/Var` ratio is designed to sidestep.
