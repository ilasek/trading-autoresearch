---
title: "Do ETFs Increase Volatility? — ETF arbitrage as a shock-propagation channel into constituents"
authors: Ben-David, Franzoni, Moussawi
year: 2018
venue: Journal of Finance (Tier 1) — read as NBER Working Paper 20071, April 2014 rev. June 2014 (Tier 2 version of the same paper)
url: https://doi.org/10.1111/jofi.12727
citations: 604 (Crossref, checked 2026-10-10)
sample_period: 2000–2012 (the NBER w20071 version that was read; the published 2018 JF version was not obtained and its sample may be longer)
markets: 660 US-listed plain-vanilla long equity ETFs (broad-based and US sector) and their US constituent stocks; tests run on the S&P 500 universe and extended to Russell 3000
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

An ETF and the basket of securities it holds are two claims on the same cash flows trading in
two venues. The primary market is the link: authorized participants (APs) exchange creation
units of ETF shares against the underlying securities with the sponsor, and that exchange is
profitable exactly when the ETF's secondary-market price has moved away from its NAV. A premium
makes APs buy the basket and deliver it for new shares; a discount makes them buy shares and
redeem them for the basket, which they then sell.

The paper's claim is that this link is a **two-way propagation channel, not merely a
tracking-error eliminator**. It is argued through Greenwood's (2005) risk-averse market-maker
model applied to two assets with identical fundamentals. A *non-fundamental* demand shock hits
the ETF (an institution scaling up an existing allocation, say). Arbitrageurs absorb it by
shorting the ETF, which requires the ETF price to rise to compensate them for inventory risk;
they hedge the short by buying the basket, which requires the *constituents'* prices to rise for
the same reason. Both legs move, so the shock arrives in the underlying prices with no news
about the underlying. When other liquidity arrives or uncertainty resolves, both legs revert.
The consequence is a **mean-reverting component added to constituent prices** — non-fundamental
volatility in Black's (1986) sense — in proportion to how much of a stock is held through ETFs.

Two auxiliary pieces are needed and the paper supplies both explicitly:

- **A counterfactual.** If ETFs merely re-housed the same clientele, the shocks would have
  arrived in the stocks anyway (Grossman's 1988 argument for futures). The propagation story
  therefore needs ETFs to *attract* a new, shorter-horizon clientele, which follows from
  Amihud–Mendelson (1986) and Constantinides (1986): investors with shorter holding periods
  self-select into the cheaper-to-trade vehicle. Its testable implication is that ETF ownership
  raises constituent **turnover**, not only volatility, and that is what the paper uses turnover
  for.
- **A discriminating prediction against stale pricing.** A rival account produces the same
  price path from *fundamental* news: if price discovery happens in the (more liquid) ETF first,
  the ETF moves and the constituents follow with a lag. The two accounts differ in exactly one
  observable — **only the non-fundamental shock reverses**. Gradual price discovery leaves prices
  at the new level. This is the identifying restriction of the whole paper, and it is the one
  worth carrying away.

## Construction recipe

- **ETF ownership (the right-hand-side variable).** For each stock-month, sum across ETFs the
  dollar value of that stock held by each ETF, divided by the stock's market capitalisation,
  using the most recently reported quarterly holdings. Universe filtered to plain-vanilla long
  US equity ETFs: leveraged, inverse, active, long/short, dedicated-short, non-equity and
  international funds are excluded by CRSP style and Lipper objective codes.
- **Stock-level ETF flow (the event variable).** The ownership-weighted average, across the ETFs
  that hold the stock, of each ETF's daily flow, where an ETF's daily flow is the
  creation/redemption measured as a fraction of prior-day assets. Note that this is a *share-count*
  quantity, not a price quantity.
- **Non-fundamental volatility, measure 1 (intraday).** O'Hara–Ye (2011) variance ratio, itself
  Lo–MacKinlay (1988): `|var(k-period returns) / (k · var(1-period returns)) − 1|`, with
  single-period returns over 5 seconds and `k = 3` (15-second multi-period returns, chosen to
  match the 15-second NAV dissemination frequency APs trade against). Zero under a random walk;
  larger means more mean reversion at that horizon. Regress on lagged ETF ownership with stock
  controls and time fixed effects.
- **Non-fundamental volatility, measure 2 (daily — the one implementable from daily bars).**
  Regress stock returns at horizons of 1 day and up to 20 and 40 days *after* a stock-level ETF
  flow on that flow, with stock controls, time fixed effects and standard errors clustered by
  stock. The prediction is a same-signed move on the flow day and partial reversal afterwards.
- **Identification.** Three layers, in increasing strength: cross-sectional and time-series
  variation in ownership with controls; first differences (to remove the stock's level of
  ownership); and a regression discontinuity at the Russell 1000/2000 cutoff, where a stock's
  index assignment — and hence its mechanical ETF ownership — jumps at a market-cap rank
  threshold at the annual June reconstitution.
- **Cross-sectional conditioning on arbitrage cost.** The effect should be *stronger* where
  arbitrage is cheaper. Proxies: bid–ask spread and stock lending fees (Markit Securities
  Finance). This is the sign test that distinguishes "arbitrage is doing it" from "something
  correlated with large, liquid, widely held stocks is doing it".

## Robustness evidence (qualitative only)

- The volatility and turnover results hold on the S&P 500 universe, weaken but survive when
  extended to smaller stocks, and survive in first differences.
- The variance-ratio result is unambiguous in sign across specifications: higher ETF ownership,
  prices further from a random walk at the horizon arbitrageurs operate on.
- The reversal test is the key one and it is **partial, not complete**: the authors estimate that
  roughly 45% of the initial flow-day price move has reverted by twenty trading days, and that
  extending the window to forty days does not increase it. Their own reading is that flows carry
  fundamental and non-fundamental information in roughly equal shares — i.e. the channel is real
  and the signal in it is half noise *about half the time*, which is the honest version of the
  result and the one a strategy should be sized against.
- Effects shrink when arbitrage is costlier (wider spreads, steeper lending fees), which is the
  predicted direction and the paper's main defence against an omitted-characteristic story.
- Scope: US equity ETFs only. The authors argue no theory prevents generalisation to other
  underlying asset classes, and note that synthetic (swap-based) ETFs, more common in Europe,
  still involve the underlying securities in secondary-market arbitrage — but that is an argument,
  not evidence, and no non-US test is in the paper.
- The mechanism is the same family as index-trading comovement results (Basak–Pavlova) and the
  index-inclusion demand-curve literature already covered here, with the ETF primary market as a
  faster, continuously open version of the same channel.

## Implementability here

**The right-hand side is not observable in this repo, and that is the central fact.** ETF
ownership and stock-level ETF flows both require fund holdings and share-count data. This panel
is daily OHLCV for ~1,400 index-member stocks plus 42 ETFs, under protocol v3. Neither the
ownership measure nor the flow measure can be built, and nothing in the daily bar is a
substitute for a share-count change (see the companion note, which measures the price-side
substitute and finds it null).

What *is* reachable, and what this note licenses:

1. **A conditioning variable, not a signal.** The paper's cross-section says the propagated
   non-fundamental component is concentrated in names that are *cheap to arbitrage and heavily
   held through baskets*. On this panel the only available proxies are liquidity-tier membership
   and index membership itself — both of which the lab already has, and both of which it has
   already measured as cross-sectional *levels* that are confounded with the survivorship/level
   artifact [`learnings.md` 2026-08-31]. So the honest statement is: this paper gives a reason to
   expect short-horizon mean reversion to be *stronger in the liquid, index-core, ETF-covered
   names* than in the rest — the opposite of the usual "reversal lives in the illiquid tail"
   prior — and that is a free, returns-based check on an existing signal, not a new signal.
2. **v3 removes most of the horizon the effect lives on.** The flow-day move is same-day and the
   reversal is measured from the day after. v3 fills a row emitted on date `d` at each name's
   next *real* close, so a one-to-three-day reversal is effectively unreachable, exactly as the
   lab found when its v2 residual-reversion result died on the fill convention. The part of the
   paper's reversal that survives the fill rule is the slow remainder out to twenty days, which
   is where the estimate is weakest relative to its fundamental-information share.
3. **It explains the lab's existing null rather than contesting it.**
   [`learnings.md` 2026-08-31] screened ETF-versus-constituent lead-lag on 9 SPDR sector ETFs
   plus VNQ and found the ETF's residual of the member-median control a null at every horizon
   pair. That screen tested the **stale-pricing / price-discovery** branch of Figure 2 — does the
   ETF lead the basket directionally — which is precisely the branch this paper sets up as the
   *rival* to its own mechanism and does not claim. The propagation mechanism predicts a
   **reversing** component in the constituents conditional on *primary-market activity*, with no
   directional lead at all. The lab's null is therefore consistent with this paper, and a
   repeat of the directional test would re-measure the branch neither side predicts.
4. **Non-US ETFs in this panel are the worst possible place to look.** A US-listed country ETF
   prints its close hours after the local market closed, so any ETF-versus-basket divergence
   computed from closes is dominated by the time-zone artifact the folder's nonsynchronous-trading
   notes already describe, not by a premium. v3's own fill note makes the same point in the other
   direction.

**Pitfalls.** (a) The ownership measure is quarterly holdings carried forward monthly; any
replication is as stale as the filings. (b) The intraday variance ratio needs second-level trades
and is simply out of scope — do not substitute a daily-frequency variance ratio and call it the
same statistic, since the 15-second choice is tied to NAV dissemination and has no daily analogue.
(c) The RDD is the only clean identification in the paper and it needs the Russell cutoff and
reconstitution calendar, which this panel does not have.

## Access

The published JF version is paywalled; **NBER w20071** (`nber.org/system/files/working_papers/w20071/w20071.pdf`)
parses cleanly with `pdftotext -layout` — no ASCII shift (the `" the "` count is unchanged by a
decode attempt) and no `( )` math dropout beyond a handful of display equations whose symbols are
dropped, including Equation (2), whose content was recovered from the surrounding prose and from
the independently stated O'Hara–Ye / Lo–MacKinlay definition. Two author-hosted routes for the
published version 404'd (`fisher.osu.edu`, `u.osu.edu/bendavid`). The note's sample period is the
working paper's; the published version was **not read**.

## Related

- `notes/2026-10-10-etf-flows-and-the-premium-change-null.md` — the companion paper, which
  measures the price-observable half of this channel (ETF premium changes) against the
  share-count half (flows) and finds only the latter predicts. Read the two together before
  proposing anything in this vein.
- `notes/2026-10-10-etf-launch-as-a-return-chasing-boundary.md` — the other half of the ETF
  question on this panel: where the 42 ETF columns come from.
- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` — the gradual-information-diffusion
  mechanism, which is the *rival* account (Figure 2 here) rather than this one.
- `notes/2026-10-09-index-inclusion-demand-curves-vs-price-pressure.md`,
  `notes/2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — the same
  non-fundamental-demand channel at the index-event frequency.
- `experiments/learnings.md` [2026-08-31] — the lab's ETF-versus-constituent lead-lag null, which
  this note reads as consistent with the paper, for the reason given above.
