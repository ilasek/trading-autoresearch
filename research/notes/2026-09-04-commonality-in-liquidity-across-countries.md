---
title: "Understanding Commonality in Liquidity Around the World"
authors: Karolyi, Lee, van Dijk
year: 2012
venue: Journal of Financial Economics 105(1), 82–112 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/j.jfineco.2011.12.008
citations: 624 (Crossref, checked 2026-09-04); 690 (Semantic Scholar, checked 2026-09-04)
sample_period: 1995–2009
markets: 40 countries, developed and emerging, individual stocks from Datastream
tier: A
validation_overlap: false
published_post_2018: false
---

**Text read**: the published JFE article in full (author-hosted PDF, complete with journal
pagination 82–112 and the appendix variable definitions).

## Mechanism

The paper is about **commonality in liquidity** — the extent to which individual stocks' liquidity
moves together within a market — and about why that co-movement is stronger in some markets than
others. It is included here for two reasons, and the second is the load-bearing one.

**The headline mechanism.** Commonality can arise from the *supply* side (liquidity providers face
funding constraints, so when their capital is impaired they withdraw from many securities at once)
or from the *demand* side (investors trade many securities in a correlated way, so order flow
itself arrives in a common factor). The paper builds testable cross-country predictions for both
and finds the demand-side account the better supported one: commonality is systematically higher in
markets with high market-level volatility — especially during large market declines — with a
greater presence of international investors, and with more correlated trading activity across
stocks. It is lower where investor property rights and corporate transparency are stronger. The
supply-side funding-constraint channel gets some support but is not the reliable explanation
outside US equity markets. The authors' framing: correlated *demand* to trade, not impaired
*capacity* to supply, is what makes many stocks illiquid together in most of the world.

**The second reason, and it is a measurement statement.** In the course of describing their
40-country Amihud panel the authors state plainly that

> a direct comparison of the level of Amihud liquidity across countries is not possible because of
> differences in currency units and trading volume definitions,

and that this does not contaminate their results because they **only relate the liquidity of
stocks within a country**. That is a Tier 1, in-print, methodological statement of exactly the
mechanism this lab discovered empirically on 2026-09-03: raw `ILLIQ` levels carry a venue
component, and the correct handling is to compare names only against peers on the same venue. The
paper does not treat this as a finding — it treats it as a known constraint that any global
liquidity study must design around, which is stronger evidence for the mechanism than a finding
would be.

## Construction recipe

**The liquidity variable.** A sign-flipped, log-damped Amihud measure at the stock-day level:

```
Liq[i,d] = − log( 1 + |R[i,d]| / ( P[i,d] * VO[i,d] ) )
```

with `R`, `P` in local currency and `VO` the day's share volume, so `P*VO` is local-currency
dollar volume. Higher `Liq` means more liquid. The `1 +` inside the log and the log itself are
purely outlier control; the sign flip is cosmetic. Screens: discard stock-days whose return is in
the top or bottom 0.1% of the within-country cross-section that day; the Ince–Porter (2006)
Datastream reversal filter on monthly returns (drop a stock-month if `(1+R_t)(1+R_{t−1}) − 1 ≤ 0.5`
and either return is ≥ 300%); drop stock-months whose total return index is below 0.01. Monthly
`Liq` is the equal-weighted average of daily `Liq` within the month.

**The commonality measure.** A two-stage Chordia–Roll–Subrahmanyam construction:

1. Remove general capital-market variation from each stock's daily liquidity series, giving
   innovations `ω[i,t,d]`.
2. Regress each stock's daily liquidity innovations on the **market's** liquidity innovations
   within a single month, including one lead and one lag:

   ```
   ω[i,t,d] = a + Σ_{j=−1}^{+1} b_j * ω[m,t,d+j] + e
   ```

   The market innovation is the previous-year market-cap-weighted average of the residuals of all
   *other* stocks in that country (stock `i` excluded; the authors report the results are not
   sensitive to including it). The stock-month commonality measure is the **R²** of this
   regression.

3. Aggregation and transformation: require ≥ 15 daily observations per stock-month; the
   country-month measure is the equal-weighted average R² across stocks, requiring ≥ 10 stocks;
   and because R² lives in [0,1] it is logit-transformed, `ln[R²/(1−R²)]`, before being used as a
   regression dependent variable (following Morck–Yeung–Yu 2000).

A parallel construction is run on **turnover** rather than liquidity, as a robustness object and as
a direct proxy for correlated trading activity.

**Explanatory variables.** Supply side: market volatility (and separately, large-decline periods),
proxies for intermediary funding conditions. Demand side: foreign and institutional investor
presence, capital-market openness, measures of correlated trading, investor sentiment,
information-acquisition incentives, and the legal-protection and transparency indices standard in
the international finance literature.

## Robustness evidence (qualitative only)

- **Scale and breadth.** Forty markets, developed and emerging, over a decade and a half of daily
  data, with results reported per country and in pooled cross-sectional and time-series
  regressions. This is one of the wider samples in this folder.
- **The cross-country level of commonality varies substantially and systematically**, and the
  same conditioning variables order it in both the cross-section (which countries) and the
  time-series (which periods within a country) — a consistency check the paper makes explicitly and
  which is the main reason to believe the demand-side reading rather than a country fixed effect
  in disguise.
- **The measurement caveat is structural, not sample-dependent.** Currency units and volume
  reporting conventions differ by venue as a matter of market design; this does not decay, get
  arbitraged away, or depend on the window. It is the one claim in this note that can be carried
  into any period without discount.
- **Known limitation acknowledged by the authors.** The demand-side variables are country-level
  and slow-moving, so the cross-sectional tests have few effective degrees of freedom; the
  time-series tests carry more of the identification. The paper is candid that the specific
  mechanics of the demand-side channel remain unresolved and calls for further work.
- No replication in the Hou–Xue–Zhang / Jensen–Kelly–Pedersen sense applies here — those catalogue
  return anomalies, and this paper's object is a liquidity *co-movement* statistic, not a
  tradeable premium. Grade it on venue, sample breadth and methodology honesty; on all three it is
  Tier A. It is **not** a source of a return signal and should not be read as one.

## Implementability here

**What is directly usable, and it is a constraint rather than a signal.** The lab's 2026-09-03
`liquidity-volume` result — that region-demeaning `ILLIQ` ranks materially better than
sector-demeaning or no demeaning, with the account that venue sets part of the level — now has
independent Tier 1 support that predates it by more than a decade, from a study that built a
40-country Amihud panel and refused to compare its levels across countries at all. Three
consequences:

1. **The lab's account of #71 is corroborated, and its scope is now bounded from the outside.**
   The paper names two sources of non-comparability: **currency units** and **trading volume
   definitions**. This repo's `dollar_volume` is `close_usd * volume`, so the currency-unit half is
   *already handled* — a USD price times a share count is a USD quantity regardless of venue. The
   half that remains is **volume definition**: whether a venue's reported share volume
   double-counts dealer trades, whether off-exchange and dark volume is consolidated into the
   reported figure, and what fraction of a dually-listed name's trading the sampled venue captures.
   That is a genuinely different and narrower reason than "tick size, lot size, settlement, listed
   float", which was the lab's stated account. Lot size in particular should *not* matter for
   dollar volume: it changes share counts and prices reciprocally.

   **This is a free, discriminating check the lab can run.** If venue non-comparability enters
   through volume *reporting*, region-demeaning should also improve a plain log-dollar-volume
   ranking's internal coherence — while if it enters through the `|return|` numerator (tick size,
   closing-auction mechanics), it should not. `learnings.md` already records that region-relative
   `ILLIQ` rank-correlates −0.912 with region-relative log ADV while the size sort's own tail is a
   null, so half the data for this is already on disk.

2. **Do not build a commonality signal.** The R² construction above is a within-country statistic
   requiring ≥10 stocks per country-month. This universe has ~145 instruments across 15 regions —
   under ten names per region on average, and 42 of them are ETFs whose "commonality" with their
   own constituents is definitional rather than economic. The paper's own minimum-stock screen
   would reject most of this panel. Record `commonality` as **unreachable on this universe for a
   structural reason** rather than untested, in the same way `statistical-arbitrage` and
   `range-variance` were closed.

3. **The peer group for demeaning should be the venue, not the region.** The paper's unit is the
   *country* because that is where the currency and the volume convention are set. This repo's
   `region` grouping is coarser (15 regions, some of them multi-country). If a region contains two
   exchanges with different volume-reporting conventions, region-demeaning removes only the average
   of the two. Whether refining region → listing venue improves the #71 leg is a free screen on the
   existing candidate and is the natural next measurement in that family — and it comes with the
   right prior attached: the effect should get *stronger*, not weaker, if the venue account is
   correct, and a null there is evidence against the account.

**Pitfalls.**
- The paper's demand-side conclusions are about *why liquidity co-moves*, not about *what earns a
  return*. Nothing in it licenses a hypothesis of the form "buy names with low commonality". The
  liquidity-risk pricing literature it cites (Pástor–Stambaugh, Acharya–Pedersen) is a different
  question and is not covered by this note.
- The `−log(1 + ILLIQ)` transform is a sensible piece of outlier hygiene this repo could adopt for
  free, but note that it is a **monotone** transform, so it changes nothing in a rank-based sort.
  It matters only if `ILLIQ` is used as a regression input or a weighting scale — which is exactly
  the situation a learned candidate would be in.
- Their day-level and month-level filters (0.1% return winsorisation within country-day, the
  Ince–Porter reversal filter) are Datastream-specific hygiene. This repo's store is a different
  vendor with different pathologies; do not import the filters without checking they bind on
  anything.

## Related

- `notes/2026-09-04-global-liquidity-proxy-horserace.md` — Fong–Holden–Trzcinka reach the same
  non-comparability conclusion from the measurement side ("none of the cost-per-volume proxies
  captures the level of lambda, at either frequency") and name two percent-cost proxies that avoid
  the problem by containing no volume at all.
- `notes/2026-08-31-amihud-volume-component-decomposition.md` — Lou–Shu drop an entire exchange
  from a *single-country* sample over a volume-reporting convention. That is the same
  non-comparability, at a finer granularity than country, and it is why point (3) above expects
  venue to beat region.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the measure itself and its
  replication record.
- `notes/2026-08-28-local-versus-global-factor-construction.md` and
  `notes/2026-08-28-international-momentum-country-neutral.md` — the country-neutral construction
  question for *return* signals. Worth reading against this note: `learnings.md`'s 2026-09-03 rule
  ("before neutralising a score against anything, ask whether the thing being removed is a unit or
  a return") is precisely the boundary between those notes and this one.
- `experiments/learnings.md`, 2026-09-03 — the lab's own region-relative `ILLIQ` measurement, which
  this note corroborates and re-scopes.
