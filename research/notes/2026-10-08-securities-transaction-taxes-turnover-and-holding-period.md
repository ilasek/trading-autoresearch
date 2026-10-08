---
title: "Financial Transaction Taxes, Market Composition, and Liquidity — with: The Effects of Stamp Duty on the Level and Volatility of UK Equity Prices; Transaction Taxes and the Behavior of the Swedish Stock Market"
authors: Colliard & Hoffmann; Saporta & Kan; Umlauf
year: 2017; 1997; 1993
venue: Journal of Finance 72(6), 2685–2716 (venue tier 1); Bank of England Working Paper No. 71 (venue tier 3 — central-bank staff working paper, not peer-reviewed); Journal of Financial Economics 33(2), 227–240 (venue tier 1)
url: https://doi.org/10.1111/jofi.12510 (full text read from the identical ECB Working Paper 2030, https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp2030.en.pdf) ; https://www.bankofengland.co.uk/-/media/boe/files/working-paper/1997/the-effects-of-stamp-duty-on-the-level-and-volatility-of-equity-prices.pdf (full text read) ; https://doi.org/10.1016/0304-405X(93)90005-V (NOT READ — closed at Elsevier, OpenAlex reports no repository copy; cited for metadata only and no claim below rests on it)
citations: "Colliard–Hoffmann: 87 (Crossref is-referenced-by-count, checked 2026-10-08; OpenAlex 89). Umlauf: 314 (OpenAlex, checked 2026-10-08; Crossref 202). Saporta–Kan: not indexed (Crossref and OpenAlex tried by title and by author, checked 2026-10-08) — a central-bank working paper without a registered DOI; per `research/README.md` this does not by itself lower its tier, which is set by venue instead."
sample_period: "Colliard–Hoffmann: June–October 2012 (109 trading days) for market data, 2012 quarterly snapshots for institutional holdings. Saporta–Kan: UK stamp-duty receipts 1954/55–1995/96, turnover velocity 1965/66–1994/95, announcement windows around UK budget statements, plus a cross-section of ADR/underlying pairs. Umlauf: Sweden 1980–1987 (per abstract; full text not read)."
markets: "Colliard–Hoffmann: French stocks in the Euronext 100 / Next 150, with Dutch and Luxembourg Euronext-listed stocks as controls (Belgium and Portugal excluded by design). Saporta–Kan: UK equities and their ADRs. Umlauf: Swedish equities."
tier: "A for Colliard–Hoffmann (tier-1 venue, clean difference-in-differences with a same-platform control group, institutional-holdings evidence alongside the market data). B for Saporta–Kan (strong design — an ADR/underlying pair is the cleanest possible control for tax treatment — but an unrefereed working paper, single market, not independently replicated so far as this session found). Not graded for Umlauf, which was not read."
validation_overlap: false
published_post_2018: false
---

## Mechanism

Protocol v3 began charging, per name, "the listing market's transaction tax (UK stamp duty
0.5% on purchases, HK stamp duty both sides, French/Italian/Spanish FTTs on purchases)"
alongside the liquidity tier (`program.md`, Protocol v3). The lab's own v3 audit then
attributed part of the collapse of the v2 board to books tilted toward "71%-non-US,
**stamp-duty-paying** names" (`experiments/learnings.md`, Protocol v3 section). A grep across
all 170 prior notes returned **zero** for `stamp duty`, `transaction tax` as a tax (as opposed
to an execution cost), `financial transaction tax`, `Tobin tax`, `securities transaction`,
`Umlauf` and `Colliard`. This folder has eight notes on execution costs and none on the one
cost component that is a statute rather than a market outcome. This note fills that.

A securities transaction tax (STT) is a different economic object from a spread or an impact
cost, and the difference is what makes it worth a note:

- **It is ad valorem, not a function of trade size, urgency or skill.** Spreads and impact can
  be reduced by trading patiently, in smaller clips, or in more liquid names. A 50 bps stamp
  duty cannot be reduced by any of that. The only margin that moves it is **how often you
  trade** — which is exactly why it bites a strategy's design rather than its execution.
- **It is levied on net position change over a day, not on gross trades.** Colliard–Hoffmann
  state this for the French FTT and note it is the same structure as UK stamp duty: the tax is
  "payable on daily net position changes (i.e., ownership transfers), which implies that pure
  intraday trading is de facto exempted". So an STT charges the *drift* a strategy chooses to
  keep, not the churn it does within a day.
- **It is asymmetric and jurisdictional.** The French FTT and UK stamp duty fall on
  **purchases** only; Hong Kong's falls on both sides. Scope is set by the issuer's domicile and
  listing, not the investor's: the French FTT "applies to shares of all listed companies
  incorporated in France with a market capitalization above one billion euros... and to all
  investors, irrespective of their country of residence". A tax is therefore a property of the
  *column*, not of the strategy.

Two theoretical channels, both named explicitly by Colliard–Hoffmann as the mechanisms their
hypotheses test, say what a rational holder does about it:

1. **Turnover adjustment.** Investors facing a proportional tax "reduce their portfolio
   turnover" in the affected securities. This "is at the center of the equilibrium models of
   Constantinides (1986) and Vayanos (1998)".
2. **Holdings adjustment (the clientele effect).** Amihud–Mendelson (1986) show that "in
   equilibrium, assets with higher transaction costs are held by investors with longer average
   holding periods". High-cost names migrate to patient holders rather than becoming cheap.

Colliard–Hoffmann find **both** margins operating, and emphasise that they are complementary
rather than competing. Their most transferable sentence is the one about where the adjustment
shows up:

> "The theoretical literature suggests that market participants adjust their behavior so as to
> minimize the impact of the tax (e.g., Constantinides (1986)). The impact of a tax on
> aggregate market outcomes should thus be **second order** compared to changes in the affected
> investors' portfolios and trading strategies."

They also record that "modest aggregate effects can hide large adjustments by individual
investors" — the aggregate price series is the wrong place to look for a tax, and the holder's
own policy is the right one.

**Capitalisation.** Saporta–Kan ask the complementary question — does the tax sit in the price
level? — with the cleanest available control: ADRs, which are not subject to UK stamp duty,
against the same companies' London-traded shares. Their findings "are consistent with the
hypothesis that stamp duty is capitalised in prices", and announcements of stamp-duty increases
(decreases) moved equity returns in the expected direction. The economic logic is that the tax
is a levy on *every future transfer* of the share, so its present value is capitalised, and
capitalised **in proportion to the name's expected turnover** — a name that changes hands often
carries more of the tax in its price than a name that does not.

**Volatility.** Both readable sources reject the proponents' central claim. Saporta–Kan, using
univariate GARCH models, "find that stamp duty has no effect on volatility, contradicting the
key hypothesis put forward by proponents of transaction taxes". Umlauf's abstract reports that
volatility did not decline when the Swedish taxes were introduced even though price levels and
turnover did; this session could not read that paper and records the direction only as
corroborating what Saporta–Kan tested directly. Colliard–Hoffmann find no support for the
"composition effect" by which a tax is supposed to improve market quality, and support instead
for a "liquidity effect through which such a tax worsens market quality and indirectly affects
even exempted traders" — including market makers and intraday traders who pay no tax at all.

## Construction recipe

There is no strategy to implement here. What there is, is a cost model and a design constraint,
and they are specific enough to build against.

**The turnover elasticity — the number that matters.** Saporta–Kan summarise the econometric
literature on how much turnover responds to an STT. Jackson and O'Donnell (1985), on UK
quarterly data, estimate that a one-percentage-point cut in stamp duty (from 2% to 1%) "leads
to a dramatic 70% increase in equity turnover". Lindgren–Westlund (1990) and Ericsson–Lindgren
(1992), on Swedish and international panel data, find that "in the long run, a one percentage
point increase in the STT leads to a decrease in turnover of between 50% and 70%". These are
policy elasticities, not strategy performance figures, and they are the right order-of-magnitude
anchor: **the optimal response to an ad valorem transaction tax is a large cut in turnover, not
a small one.** A strategy that pays a 50 bps stamp duty on every purchase of a UK name and does
not change its UK rebalance cadence relative to its US one is leaving the whole adjustment
margin unused.

**How to charge it.** Three structural features, all from the sources rather than inferred:

- Charge it on the **net daily position change** per name, not on gross turnover, and on the
  **taxed side only** where the statute is one-sided (purchases for UK/FR; both sides for HK).
- Scope it by the **issuer's listing/incorporation**, not the holder — so it is a per-column
  constant, computable once per name and reusable.
- Treat it as **unavoidable by execution**: unlike a spread, no amount of patience, clip-sizing
  or liquidity-seeking reduces it. It belongs in the strategy's objective function, not in its
  execution model.

**Where the escape hatches are — and that they are closed here.** The literature's documented
avoidance routes are instrument substitution and venue migration: Saporta–Kan's ADRs escape UK
stamp duty entirely; Colliard–Hoffmann note that ADRs were exempt from the French FTT through
their sample; the Swedish episode is cited (Lybeck 1991, Umlauf 1993, Campbell–Froot 1994) for
activity shifting to untaxed locations. **None of these is available to a candidate in this lab**,
because the instrument set is fixed by the `eligible` panel and the engine assigns the tax from
the listing market. The only margin left is turnover. That is a narrowing, and it is worth
saying plainly: the real-world practitioner's first response to an STT is to trade a different
instrument, and a candidate here cannot.

## Robustness evidence (qualitative only)

- **Independent designs, same direction.** Colliard–Hoffmann's own robustness discussion notes
  that studies "using a variety of different control groups, reach remarkably similar
  conclusions". Their identification is a difference-in-differences against non-French stocks
  trading on the *same platform* (Euronext), which removes platform, currency-regime and
  macro-shock confounds in a way a cross-country comparison cannot; they explicitly drop Belgium
  (which raised its own FTT simultaneously) and Portugal (sovereign-debt stress), which is the
  kind of exclusion that makes a diff-in-diff credible rather than convenient.
- **Two margins, measured separately.** The turnover and holdings channels are tested on
  different data (millisecond market data vs. institutional portfolio snapshots), so the
  conclusion that both operate does not rest on one dataset.
- **The volatility null is robust across three settings** — UK (GARCH on announcement-dated
  rate changes), Sweden (per Umlauf's abstract) and France (market-quality measures) — and in
  all three the proponents' hypothesis fails. That is unusual agreement for a politically
  charged question.
- **Known gaps.** Colliard–Hoffmann's market-data window is five months around one policy
  change in one country: a clean experiment, not a multi-decade sample. Saporta–Kan is
  unrefereed and single-market. The turnover elasticities quoted above come from studies this
  session did **not** read (they are Saporta–Kan's summary of them), and two of the three date
  from the 1990s; treat the 50–70% range as an order of magnitude with a secondary-source
  provenance, not as a calibrated coefficient. Umlauf was not obtained at all.
- **Multiple testing / costs.** Not applicable in the usual sense — these are policy-evaluation
  papers, not anomaly papers, so there is no factor zoo to deflate. Colliard–Hoffmann model
  transaction costs as the object of study rather than as a nuisance.

## Implementability here

**Which panel.** Everything below is about the protocol v3 panel: ~1,400 stocks that were ever
members of nine indices plus 42 ETFs, point-in-time, ~1,000 eligible on a typical validation
date. The tax exposure is not evenly spread across it. Of the nine tracked indices, **FTSE 100
(UK stamp duty, 0.5% on purchases), CAC 40 (French FTT on purchases), Hang Seng (HK stamp duty,
both sides)** are directly taxed, and Italian and Spanish FTTs reach names in the Euro Stoxx 50.
The S&P 500, DAX, SMI, AEX and Nikkei legs are untaxed. So the panel contains a **large,
pre-existing, exogenous cross-sectional split in the per-round-trip cost of a name that has
nothing to do with liquidity** — and the engine already knows which side of it every column is
on.

Four concrete consequences, in the order they are worth acting on:

1. **A region-conditional turnover budget, not a global one.** The honest implication of the
   turnover-elasticity literature is that the optimal rebalance cadence is *per name*, and
   should be markedly slower for taxed names. A candidate that rebalances its FTSE and Hang
   Seng holdings on the same clock as its S&P holdings is mis-specified relative to the
   theory, not merely expensive. The cheapest version of this is a two-speed rebalance:
   emit rows for taxed columns on a slower grid than untaxed ones. Note this interacts
   directly with v3's drift charging — see note 3 tonight on no-trade bands, which gives the
   *width* of the right band from the cost, and where a 50 bps stamp duty implies a band
   roughly `(50/15)^(1/3) ≈ 1.5×` wider than a liquid untaxed name's.
2. **A free, train-only diagnostic the lab has never run: decompose the realised cost of any
   existing trial into liquidity-tier cost and tax.** This needs no new candidate and no new
   trial. If the tax share of a book's total cost is large, item 1 is the highest-value
   construction change available under v3; if it is small, this whole vein is closed cheaply
   and that is worth knowing too. The v3 audit's phrase "stamp-duty-paying names" asserts the
   first without quantifying it.
3. **Do not build a cross-sectional "tax premium" signal.** This is the trap the sources
   specifically warn against, and it is worth stating as an anti-candidate. Amihud–Mendelson and
   the capitalisation result together imply taxed names should carry *some* higher gross
   expected return as compensation — which looks like a free long-only tilt toward UK and HK
   names. But Colliard–Hoffmann's conclusion is that the adjustment is second-order in prices
   and first-order in holders' policies, and the compensation accrues to the **long-horizon
   holder** who actually realises the lower turnover. A monthly-rebalanced book tilted toward
   taxed names pays the tax and collects the premium meant for someone holding for years. Worse,
   on this panel the tilt is nearly collinear with "non-US", which the lab's v3 audit already
   identifies as a property of the books that collapsed. Any such candidate must be region-
   demeaned, and even then it is testing a holding-period premium with the wrong holding period.
4. **One thing to check before trusting any v3 skill number, which this session may not do
   itself.** The skill statistic is the candidate's Sharpe minus the equal-weight eligible
   pool's. If the pool's return is computed **gross of costs** while candidates are charged, then
   every candidate is being compared against a benchmark that pays no stamp duty, and the tax is
   being charged asymmetrically to the thing under test. If the pool is charged, a second
   question follows: the pool holds ~1,000 names across all nine indices, so it pays tax on its
   own reconstitution turnover, and its cost drag is a function of index membership churn. Both
   are answerable only by reading `engine/`, which a strategy session may do and this agent may
   not. This is the same look that `SUMMARY.md`'s standing item **#188(a)** has asked for since
   2026-10-03, now with a sharper question attached to it.

**Pitfalls.** (a) Do not infer the tax from the price series — it is in the level, not in the
returns, and Saporta–Kan needed ADR pairs to see it at all. (b) The tax is on net daily position
change, so a candidate that emits a full row daily and lets the engine net it is charged
differently from one that emits sparse rows; the two are not equivalent even at equal average
holdings. (c) Nothing here licenses a change to `engine/costs.py`: the tax model is the
protocol's, and if it looks wrong the route is a `## Engine issue` journal entry, not a fix.

## Related

- `notes/2026-08-27-live-execution-costs-implementation-shortfall.md` and
  `notes/2026-08-27-market-impact-functional-form-and-trade-rate.md` — the *other* kind of cost:
  size-, urgency- and skill-dependent, and reducible by execution. The contrast is the point of
  this note: an STT has none of those margins.
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — Novy-Marx–Velikov's
  cost-mitigation toolkit (banding, staggered partial rebalancing, liquidity screening). Their
  techniques all reduce *turnover*, which is exactly the margin an STT leaves open, so that note
  is the right place to look for the how once item 1 above is accepted. Their ~50%-turnover-per-
  month threshold was calibrated on US equities with no STT, so it is a floor here, not a
  threshold.
- `notes/2026-10-08-no-trade-bands-under-proportional-costs.md` (tonight) — gives the optimal
  band width as a function of the proportional cost, which is how a per-name tax becomes a
  per-name rebalance rule. These two notes are meant to be read together.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — Amihud (2002). Note that
  **Amihud–Mendelson (1986)**, `https://doi.org/10.1016/0304-405X(86)90065-6`, 3,656 Crossref
  citations (checked 2026-10-08), is a *different* paper and was uncovered by this folder until
  now: it is the equilibrium clientele result that consequence 3 above turns on. Not read in
  full this session; cited for the result Colliard–Hoffmann attribute to it.
- `notes/2026-10-07-tax-trading-theory-and-the-price-pressure-condition.md` and
  `notes/2026-10-07-tax-loss-trading-and-wash-sales-investor-level.md` — also "taxes", and a
  **different mechanism entirely**: those concern the *holder's* capital-gains position and the
  calendar on which they realise it. An STT is a levy on the transfer itself, paid by whoever
  trades, with no reference to gain, loss or holding period at purchase. Constantinides (1986)
  appears in both veins, which is a coincidence of author rather than of mechanism — there it is
  the tax-timing option, here it is the turnover-adjustment equilibrium.
- `experiments/learnings.md`, Protocol v3 section — the v3 re-measurement that names
  "stamp-duty-paying names" as a contributor to the v2 board's collapse, and which this note
  supplies the missing literature for. No tension: the lab's finding and these sources point the
  same way. The tension is with the v1/v2 learnings' flat "15 bps/side" premise, which the
  `Data & methodology caveats` block still carries and which v3 has superseded.
