---
title: "Profitability of Momentum Strategies in the International Equity Markets" — read for the country *index* as the traded unit, the four-way decomposition of a USD-denominated index momentum profit, and which leg carries it
authors: Chan, Hameed, Tong
year: 2000
venue: Journal of Financial and Quantitative Analysis (venue tier 1)
url: https://doi.org/10.2307/2676188
citations: 326 (Crossref `is-referenced-by-count`, checked 2026-11-02). Semantic Scholar was not queried for this DOI; OpenAlex was not spent on it (budget reserved for locations lists), per `research/README.md`'s "Crossref first" rule.
sample_period: 1980-01-01 – 1995-06-30 (weekly), with a post-1985 subsample used wherever all 23 markets must be present
markets: 23 national equity market indices — 9 Asia-Pacific, 11 European, 2 North American, 1 African — all denominated in USD
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the authors' September 1999 working version, `web2-bschool.nus.edu.sg/wp-content/uploads/media_rp/publications/ykEmV1422257410.pdf`, served first try (474 KB → 80 KB of clean text, 427 instances of `" the "`, zero `( )` dropout, no ASCII shift). The published JFQA tables were not read; nothing below is taken from them. Section and table *numbers* cited are the working paper's.
---

## Mechanism

The object here is **the national equity index itself as the traded asset**, not a stock inside
one. That distinction is the whole point of the note, because this lab has two existing notes on
country momentum (`2026-08-28-international-momentum-country-neutral.md`,
`2026-11-01-anomalies-across-the-globe-country-neutral.md`) and both are about *removing* the
country bet from a stock book. Neither is about taking it.

The economic story the authors give is the standard continuation pair — underreaction to
information, and herding/flow — lifted one level up the aggregation hierarchy. The reason it is
not simply the stock-level mechanism relabelled is the **time structure**, which comes out
opposite to the stock-level one: at the index level the continuation that survives risk
adjustment lives at **2–4 weeks**, whereas at the stock level the same horizon is the classic
*reversal* window and continuation only appears at 3–12 months. A mechanism that changes sign
when you change the unit of aggregation is a different mechanism, not a different label for the
same one.

The second mechanism in the paper is specific to this lab's data type and is the reason the note
exists. **This repo's prices are USD-adjusted closes of instruments that mostly do not trade in
USD**, so every index return the lab sees is a sum of a local-currency equity return and a
currency return. The paper decomposes a USD-denominated index momentum profit into exactly that
sum and asks which part pays.

## Construction recipe

**Weighting.** A zero-cost, cross-sectionally demeaned relative-strength book — no ranking, no
bins:

    w_i,t(k) = (1/N) · [ R_i,t-1(k) − R_m,t-1(k) ],      R_m = cross-sectional mean across the N markets

so a market's weight is proportional to how far its past-`k`-week return sat from the
cross-sectional average, and the weights sum to zero by construction. `k` ∈ {1, 2, 4, 12, 26}
weeks for both the evaluation and the holding period.

**The causality guard, and it is the same one protocol v3 enforces.** The markets sit in
different time zones with different trading hours, so a given calendar day's returns cover
different real intervals. The authors handle this twice over: they work at weekly or coarser
frequency rather than daily, *and* they offset the two windows — the **evaluation week runs
Wednesday→Wednesday and the holding week runs Thursday→Thursday**, so the evaluation window
closes strictly before the holding window opens. Their stated reason is to guarantee the strategy
"does not use price information of any countries from the holding period." That is protocol v3's
fill convention arrived at independently and for the same reason, which makes this construction
natively compatible with the engine rather than something to retrofit.

**Cap-weighted variant.** `w^M_i,t(k) = h_i,t-1 · [R_i,t-1 − R_m,t-1]`, with `h` the market's
share of world capitalisation, so the book cannot take a large position in a small market.

**The decomposition.** With `R_i ≅ r_i + e_i` (local return plus currency return), the expected
profit splits into four terms:

    π1 = E{ (r_i,t-1 − r_m,t-1) · r_i,t }    equity predicted by past equity
    π2 = E{ (r_i,t-1 − r_m,t-1) · e_i,t }    currency predicted by past equity
    π3 = E{ (e_i,t-1 − e_m,t-1) · r_i,t }    equity predicted by past currency
    π4 = E{ (e_i,t-1 − e_m,t-1) · e_i,t }    currency predicted by past currency

**Volume conditioner.** A market's volume is labelled high or low purely by **its own change**:
high if volume in period `t-1` exceeded volume in period `t-2`, low otherwise. No cross-market
level comparison and no normalisation is involved — which matters here, see Implementability.

**Risk adjustment.** Normalised profits regressed per country on the excess world market return,
the system estimated by GLS with contemporaneously correlated disturbances; the alphas are the
abnormal profits.

## Robustness evidence (qualitative only)

- **Where the effect lives in horizon.** Profits decline monotonically as the holding period
  lengthens. After world-market beta adjustment the picture sharpens considerably: at 1 week the
  alphas are near zero and the joint test that all are zero **cannot** be rejected; at **2 and 4
  weeks** most countries have positive alphas and the joint test is rejected at the 1% level; at
  12 and 26 weeks the abnormal profits **disappear** and many countries turn negative. So simple
  beta adjustment explains most of the long-horizon profit and none of the 2–4-week profit. The
  usable window is narrow and is neither the shortest nor the longest.
- **The currency component is a rounding error at short horizons, and negative at long ones.**
  π1 — equity predicted by past equity — contributes **more than 90%** of total profit at the
  1-week holding period and more than 80% at 2 and 26 weeks. π2 and π4 are small throughout.
  **π3 is negative at the 12- and 26-week holding periods**: a market whose currency appreciated
  is followed by *weaker* equity performance. The authors' summary is that accounting for
  exchange-rate fluctuation "does not add much to momentum profits."
- **The long leg carries it.** Splitting the book, **buying the winner portfolios yields
  significant profits consistently, while selling the loser portfolios yields insignificant
  profits or losses.** This is the opposite of the usual anomaly shape and is the single most
  decision-relevant sentence in the paper for a long-only lab.
- **Cap-weighting shrinks but does not kill it.** Cap-weighted profits are generally smaller than
  the equal-ish weighted ones but **remain statistically significant at the short holding
  periods** — and the authors flag beforehand that this is the test that would expose the effect
  as a small/illiquid-market artefact, since the five largest markets are about three-quarters of
  world capitalisation. It is not such an artefact at short horizons.
- **Volume.** Momentum profits are higher for the high-lagged-volume group: continuation is
  stronger following an increase in trading volume.
- **Subperiod.** Results on a post-1985 subsample are similar to the full sample, with π1 still
  dominant; the authors had expected weaker profits as capital controls were relaxed and did not
  find that.
- **Null.** 2,000 bootstrap samples scrambling the index return series while preserving
  cross-market correlation; the bootstrap p-values are stronger than the asymptotic ones.
- **The gap, and it is the rubric's cost dimension.** **No transaction costs are modelled
  anywhere in the paper**, and the economic-significance measure is a frictionless zero-cost
  arbitrage return. Every magnitude is gross. Tier A is assigned on venue, citation count,
  breadth of markets, explicit risk adjustment and a real bootstrap null; the cost dimension
  fails outright and is the reason the Implementability section below is arithmetic rather than
  enthusiasm.

## Implementability here

**The traded unit exists in this panel.** The v2/v3 eligible panel carries 42 ETFs alongside the
stocks, including single-country ETFs, and `learnings.md` records a seated `liquidity-volume`
lead that held 42% ETFs with `EWU` as its most-held name — so an ETF-only or ETF-heavy book is
reachable and has precedent, and ETFs enter `eligible` from their first price.

**What is genuinely new relative to the lab's record.** Everything in `learnings.md` about ETFs
is about *static diversified sleeves* — inverse-vol across a 10-ETF sleeve, risk parity, blending
a sleeve into a stock momentum book — all of which capped out below the champion, and all of
which were **allocation across asset classes**, not **cross-sectional relative strength among
country indices**. The construction above has not been tried here.

**Four things that transfer directly.**

1. **The horizon is 2–4 weeks, not 12 months.** The lab's `price-trend` cap and its exhausted
   12-1 lineage do not reach this, and the paper's own risk adjustment kills the 12-week and
   26-week versions. Do not build the 12-1 version of this; it is the one the evidence refuses.
2. **The weighting is demeaned relative strength, which the lab already computes.** The long-only
   adaptation is the positive half of `w`, renormalised — and the paper's long/short split says
   that is the half that pays, so the long-only constraint is unusually cheap here instead of
   unusually expensive.
3. **The causality guard is already protocol.** v3 fills a row at each name's first real close
   after the row date, which is the Wednesday/Thursday offset generalised. Nothing special is
   needed and the old same-close lead-lag objection does not apply.
4. **The volume conditioner survives this lab's own objection to ETF volume.** `learnings.md`
   records that ETF dollar volume fails as a liquidity proxy because creation/redemption means
   the numerator counts securities the ETF does not trade. That is a **level and cross-sectional**
   objection. This conditioner is a **within-instrument time-series change** — is this ETF's
   volume higher this period than last — so the objection does not reach it. Worth saying
   explicitly because the lab has a standing anti-candidate on "the liquidity level or trend in
   any form", and this is neither a level nor a trend but a one-lag change used only as a
   conditioner.

**The binding constraint is turnover, and the lab already owns the arithmetic to refuse this
before building it.** A 2–4-week rebalance is 13–26 rebalances a year on a cross-section of
roughly 15 country/region ETFs. The 2026-11-01/02 nightly calibrated **0.007–0.018 of Sharpe
skill lost per unit of engine-counted annual turnover**, and concluded that >3×/yr cannot keep
more than 0.025 of cost and >12×/yr cannot keep 0.10. **Run that arithmetic on the realised
turnover of this construction before writing the file**, exactly as F8's duty-cycle arithmetic
was used. Two things push in the candidate's favour and should go into the same calculation:
US-listed ETFs carry **no stamp duty or FTT** (the 2026-11-01/02 F1 measurement found taxes are
~0 of skill at low turnover anyway), and liquid ETFs sit in the **cheapest 15 bps tier**, which
F1 found is the irreducible floor. The honest position is that this is the one family where the
cost floor is lowest and the horizon is shortest, and those two pull against each other; the
arithmetic decides it, not this note.

**Three further cautions.**

- **Breadth.** ~15 country/region ETFs with staggered inception is a far thinner cross-section
  than the ~1,000-name stock panel. The 2026-11-01/02 nightly's F3 refuted the general claim that
  thin legs are worse per name, which weakens the usual objection — but it does not establish
  that a 15-name book clears a bar calibrated on a 1,000-name one.
- **The benchmark is not the country pool.** v3 grades skill against the **equal-weight eligible
  pool**, which is ~1,000 mostly-stock names. An ETF-only book is a large active bet against that
  pool and its skill number will be dominated by that bet, not by the country-selection signal.
  Whoever builds this should say in the hypothesis which of the two they are testing.
- **Sample age.** 1980–1995, 23 markets including several that were then segmented. The authors
  themselves expected and did not find decay after capital-control liberalisation, but this is a
  pre-1996 result and `2026-08-17-mclean-pontiff-publication-decay.md` applies.

## Related

- **Companion source, abstract obtained and body NOT obtained: Bhojraj & Swaminathan (2006),
  "Macromomentum: Returns Predictability in International Equity Indices," *Journal of Business*
  79(1) 429–451, `10.1086/497416`, 156 Crossref cites (checked 2026-11-02).** OpenAlex reports
  `oa_status: closed, any_repository_has_fulltext: false` with the publisher DOI as the only
  location; Cornell eCommons returns **0 results** for the title. Per `research/README.md`'s rule
  — when a paper's channels are dark, spend the budget on a different source for the same
  mechanism — no third channel was attempted. The abstract was read from the RePEc record
  (`ideas.repec.org/a/ucp/jnlbus/v79y2006i1p429-428.html`) and reports: country indices show
  momentum in the first year after formation and **reversals over the following two years**, and
  **positive currency momentum predicts lower future stock index returns, which weakens momentum
  and strengthens reversals in USD-denominated returns.** Nothing beyond that abstract is used
  anywhere in this note or in `SUMMARY.md`.
  - **The tension with this note's source is apparent rather than real, and the resolution is the
    horizon.** Chan–Hameed–Tong say the currency channel "does not add much"; Bhojraj–Swaminathan
    say it materially weakens momentum. But **both report the same sign** — CHT's π3 is negative
    at 12 and 26 weeks, and a negative π3 *is* "currency appreciation predicts weaker subsequent
    equity returns." The disagreement is about magnitude at different horizons: negligible at
    1–4 weeks, large enough at a year and beyond to help turn continuation into reversal. The
    transferable rule, which neither paper states in this form, is that **a USD-denominated
    country score is cleanest at short horizons and increasingly self-contaminating as the
    horizon lengthens.** Recorded as a reconciliation hypothesis, not as a finding of either
    paper.
- `2026-11-02-multiverse-of-country-level-research-designs.md` — independently finds that the
  country-level signal that survives a 13,824-design multiverse is **short-term** (one-month)
  momentum while 12-1 momentum is fragile, and that value-weighting cuts country-level payoffs.
  Both match this paper. It also finds the opposite of this paper on the instrument: ETF-based
  implementations of country effects pay substantially less than index-based ones. Read the two
  together; that note carries the discount.
- `2026-11-02-winner-loser-reversals-in-national-indices.md` — the long-horizon end of the same
  term structure.
- `2026-09-10-currency-component-in-usd-converted-returns.md` — Campbell–Serfaty-de
  Medeiros–Viceira on the same `R = r + e` decomposition, but for **variance and hedging**, not
  predictability. That note establishes that a USD conversion adds a priced risk factor; this one
  adds that the added component is also *predictable* and signs against a long-horizon momentum
  score. They are complements, not duplicates.
- `2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — the volume-conditions-continuation
  result at the stock level.
