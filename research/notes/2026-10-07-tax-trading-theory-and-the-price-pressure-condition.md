---
title: "Optimal Stock Trading with Personal Taxes — why a tax-year-end *volume* seasonal does not imply a *price* seasonal"
authors: Constantinides
year: 1984
venue: Journal of Financial Economics 13(1), 65–89 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/0304-405x(84)90032-1
citations: "293 (Crossref `is-referenced-by-count`, checked 2026-10-07); 315 (OpenAlex, checked 2026-10-07); Semantic Scholar's DOI endpoint returns a clean `Paper with id DOI:… not found` for this real, twice-indexed Tier-1 DOI — the **sixth** instance of the failure mode first recorded [2026-10-01] (checked 2026-10-07)."
sample_period: "Theory plus a simulation calibrated on actual stock prices over 1962–1977. The paper's claims used here are the theoretical ones; nothing below rests on the simulation's numbers."
markets: US equities (simulation); the theory is jurisdiction-general and is stated for a tax code with a short/long-term rate distinction, loss offsets and wash-sale rules
tier: A
validation_overlap: false
published_post_2018: false
read: "Full text, NBER Working Paper 1176 (August 1983), `nber.org/system/files/working_papers/w1176/w1176.pdf`, 51 pp., which carries the abstract, all seven sections, the figures' discussion and the reference list of the article published in JFE 1984. Extracted with `pdftotext -layout`; no ligature or math dropout (checked for the `( )` tell)."
---

## Mechanism

The tax code hands a holder of a stock a **timing option**: realize losses, defer gains. Where the
long-term capital-gains rate is below the short-term rate, it hands them a *second* timing option —
realize losses at short-term status, realize gains at long-term status, if at all. The paper solves
for the optimal exercise of both and then asks what that implies for prices at the turn of the tax
year. The answer is the reason this note exists, and it is a negative one.

**What the theory does predict.** With transaction costs and no short/long-term distinction, the
investor follows a control-limit policy: early in the tax year they are reluctant to pay the cost of
realizing a small loss, and late in the year that reluctance is overcome by the preference for a tax
rebate this year rather than next. So **realization volume rises monotonically from the start of the
tax year to its end and stops abruptly in the first few days of the new one** — realizing a given
loss on the last day of the tax year dominates realizing the same loss on the first day of the next.
The author's simulation says transaction costs do not materially erode the benefit of tax trading
once the short/long-term distinction is present, so the volume seasonal survives costs.

**What the theory does not predict: a price seasonal.** Getting from a volume seasonal to a price
seasonal requires an extra assumption that the tax code does not supply — that after selling to
realize a loss, the seller **does not repurchase the same stock, or a stock another tax-loss seller
is simultaneously dumping**. If sellers swap with each other, pairs of tax-loss sellers exchange
positions and neither price moves. Only if the selling is one-sided against a non-horizontal demand
curve does it depress prices, and then it does so **where the market is illiquid — small firms**;
when the selling dries up at the turn of the year, those prices rebound.

The paper then closes the loop adversarially against its own mechanism. A seller sophisticated
enough to be optimizing taxes is sophisticated enough to notice a price seasonality, and has at
least three cheap escapes: swap with another tax-loss seller instead of selling into the market;
**accelerate the sale by a month or two** (to October or November) so that the wash-sale waiting
period expires in time to repurchase *before* the new-year rebound; or move their own tax year-end
off December. The author's conclusion is explicit: tax-loss selling in the presence of transaction
costs **predicts a seasonal pattern in trading volume, and predicts one in prices only under the
further assumption of irrationality or ignorance on the sellers' part.**

Two further negatives worth carrying. **Tax trading does not explain the small-firm premium itself**
— only, conditionally, a seasonal in it. And the *gain*-deferral side of the option points the other
way: deferring a realized gain from the end of one tax year to the start of the next predicts
increased gain-selling early in the new year, i.e. selling pressure in prior-year **winners** in
January, which if it moved prices at all would make their January return *negative*.

## Construction recipe

There is no portfolio here; what the paper supplies is a **set of preconditions that any
turn-of-the-tax-year construction must assert, and that can be checked separately**:

1. **A volume seasonal in the right shape.** Realization volume in losing names rises through the
   tax year, peaks in its final days, and stops in the first days of the new tax year. This is the
   paper's robust prediction and it is measurable from a volume panel without any return data.
2. **One-sidedness.** The price effect exists only if the selling is not offset by substitute
   buying. The testable negation: if close substitutes exist for the name being sold, the demand
   curve is flat and the effect is zero regardless of how large the volume seasonal is.
3. **Illiquidity.** Conditional on (2), the price depression concentrates where the market cannot
   absorb one-sided flow — the small, thinly traded end.
4. **Seller naivety.** The sellers must not be timing around the price seasonality itself. Any
   sophistication (swapping, accelerating the sale, shifting the tax year) removes the price effect
   while leaving the volume effect intact.
5. **Sign for winners is the opposite.** Gain deferral predicts new-year selling pressure in
   prior-year winners, so a construction that is long winners in January is fighting this channel,
   not riding it.

The structural point for a strategy lab: (1) is a prediction about *volume*, (2)–(4) are preconditions
about *market structure and investor behaviour*, and **only their conjunction gives a return
prediction.** A null return result on a universe that fails (3) therefore says nothing about the
mechanism.

## Robustness evidence (qualitative only)

This is a theory paper with a calibrating simulation, so "robustness" means logical generality
rather than out-of-sample survival. The control-limit result is driven by the interaction of
transaction costs with the annual tax deadline and does not depend on the particular tax rates; the
author works through four separate tax-code scenarios (long-term-only taxation, gains-deferral,
long-term rate with same-year offsets, and no rate distinction but costs present) and reports that
**none of the first three predicts increased tax-loss selling at the year-end at all** — the
year-end concentration comes specifically from the transaction-cost/control-limit scenario. That
makes the familiar "investors dump losers in December" story the *least* general of the four, which
is a stronger statement than a single-model result.

The price-pressure step is where the paper is deliberately unwilling to go, and subsequent work has
not overturned the logic — it has instead gone looking for direct evidence that the behaviour is in
fact naive in the required way (see `2026-10-07-tax-loss-trading-and-wash-sales-investor-level.md`,
which finds exactly that, and `2026-10-07-tax-year-end-alignment-and-the-australian-test.md`, which
finds the cross-country pattern does not line up with tax years).

## Implementability here

**This note is a screen, not a candidate.** Its value is that it prices the preconditions for a
turn-of-the-tax-year construction *before* a trial is spent, and on this repo's universe two of the
five fail or are unverifiable:

- **Precondition 3 (illiquidity) fails by construction under protocol v2.** The v2 pool is ~1,400
  names that were ever members of nine large-cap indices (S&P 500, DAX, CAC 40, FTSE 100, SMI, AEX,
  Euro Stoxx 50, Nikkei 225, Hang Seng) plus 42 ETFs. Every one of them is a large-cap index member
  on the dates it is eligible. The mechanism's price channel is explicitly a *small-firm, illiquid
  market* channel. So this universe truncates precisely the tail the effect is supposed to live in,
  and a flat result on it is **uninformative about the mechanism** rather than evidence against it.
  Say so in the hypothesis rather than discovering it in the verdict.
- **Precondition 2 (one-sidedness) is adverse here too**: within a nine-index large-cap pool, close
  substitutes are abundant — same region, same index, similar beta — which is the Scholes
  flat-demand-curve case the paper names.
- **Precondition 1 is free and testable.** The repo now passes `volume` and `dollar_volume` to
  strategies. The paper's volume prediction — realization volume in losing names rising through the
  tax year and stopping in the first days of the new one — is measurable on train with no return
  data and no trial. It is the cheapest possible discriminator and it is a *volume* claim, which is
  a family (`liquidity-volume`) the lab has already built features for.
- **Precondition 5 is a sign constraint the lab can use for free**: it predicts prior-year
  *winners* should, if anything, be weak at the turn of the year, which is the opposite sign from
  momentum. That makes "is the January coefficient on a 12-month momentum score lower than its
  February–November coefficient?" a free train-only screen with a pre-registered direction.

The honest summary for the strategy agent: **the theory makes the tradeable version of this
mechanism conditional on an illiquidity channel this universe does not contain.** The pieces of it
that are still reachable are a volume-pattern check and a sign constraint, both free.

## Related

- `notes/2026-10-07-tax-loss-trading-and-wash-sales-investor-level.md` — the investor-level evidence
  that the naivety condition (4) is empirically met, including its own footnote conceding that the
  observed end-of-December concentration is *not* optimal tax timing by this paper's standard.
- `notes/2026-10-07-tax-year-end-alignment-and-the-australian-test.md` — the cross-country test of
  whether the seasonal follows the tax year, and the a-priori objections to the price-pressure step,
  which overlap this paper's almost exactly.
- `notes/2026-10-07-past-return-consistency-and-the-seasonal-in-the-past-return-relation.md` — the
  cross-sectional measurement of what actually happens to past-return effects in December and
  January.
- `notes/2026-09-22-arbitrage-risk-substitute-portfolios.md` — Wurgler–Zhuravskaya on whether
  arbitrage flattens demand curves, which is precondition (2) stated as its own literature: the
  price effect of uninformed flow is larger exactly where good substitutes are missing.
- `notes/2026-09-22-limits-of-arbitrage-performance-based.md`, `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`
  — the standing framework for "why does an effect survive", of which this is a clean instance.
- `notes/2026-09-19-v-shaped-selling-propensity.md` — the other literature in this folder about
  *when holders sell*, there driven by the reference price rather than the tax calendar.
- Tension with `experiments/learnings.md` [2026-09-01]: the lab closed the `calendar` half of
  `seasonality-calendar` on the ground that a long-only book whose only alternative is cash cannot
  exploit a calendar window unless the complement window's return is ≤ 0. **That closure does not
  reach this mechanism**, because the construction it implies is a *cross-sectional* reallocation
  inside the turn-of-the-year window at constant gross exposure, not a decision to be in or out of
  the market. The binding objection here is the universe's liquidity profile, not the complement
  window.
