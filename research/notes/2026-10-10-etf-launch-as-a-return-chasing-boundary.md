---
title: "Competition for Attention in the ETF Space — the product launch as a return-chasing selection event"
authors: Ben-David, Franzoni, Kim, Moussawi
year: 2023
venue: Review of Financial Studies (Tier 1) — read as NBER Working Paper 28369, January 2021 rev. January 2022
url: https://doi.org/10.1093/rfs/hhac048
citations: 123 (Crossref, checked 2026-10-10)
sample_period: 1993–2019 (performance tests 2000–2019)
markets: nearly all equity ETFs ever traded in the US market, classified into broad-index, smart-beta, sector/industry and thematic
tier: A
validation_overlap: true
published_post_2018: true
---

## Mechanism

A supply-side theory of **why a fund exists at all**, applied to the one asset class whose
columns in this repo's panel begin at a product launch rather than at an index committee's
decision.

The frame is Bordalo–Gennaioli–Shleifer (2016): when consumers have limited attention, suppliers
choose *which attribute to make salient*. In their model the market converges to either a
price-salient or a quality-salient equilibrium; the paper's extension is that in the ETF industry
**both equilibria coexist and segment the market**. Broad-based funds hold large, mutually similar
portfolios and compete on price, which drives fees toward zero. To defend margins, providers
launch differentiated products — sector, industry and thematic funds — that hold small,
distinctive portfolios, charge much higher fees, and compete on a *non-price* salient attribute.

The second half asks what that attribute is, and the paper eliminates the benign candidates
before settling on the unflattering one:

- **Not segment-selection skill.** Specialized funds do not deliver positive risk-adjusted
  returns; their performance is negative, concentrated in the years right after inception, and
  of similar magnitude when the *underlying indexes* are used instead of the funds, so it is not
  a fee or trading-friction story.
- **Not hedging / market completion.** If specialized funds spanned a risk investors wanted to
  insure, the portfolio of stocks most negatively correlated with the aggregate specialized-ETF
  portfolio should earn positive abnormal returns; it does not. And insurance buyers do not act
  disappointed — these funds experience *outflows* over their lives and close at significantly
  higher rates, with closure more sensitive to past performance.
- **Not a "warm glow" from values-aligned exposure.** The media sentiment of the holdings drops
  sharply right after launch, which is a souring mood rather than a stable non-pecuniary benefit.
- **Catering to sentiment is what fits.** Providers identify a popular theme and ship a product
  that tracks it; the short time-to-market (as little as 75 days) and intraday liquidity make
  ETFs unusually well suited to this. **By the time the product lists, the securities it holds
  have already had their run.** Investors use these funds as speculative vehicles, extrapolating
  recent performance.

The demand-side evidence matches the segmentation: flows into broad-based funds are strongly
fee-sensitive, flows into specialized funds are *unrelated* to fees and respond to past
performance instead, and high media exposure of a fund's holdings *reduces* the fee sensitivity
of its flows — attention spent on one attribute is attention not spent on price.

## Construction recipe

Three constructions are worth having, two of which are measurable without holdings data:

- **Differentiation (needs holdings).** For each fund at each date, `1 − cosine similarity`
  between the fund's portfolio weight vector and the weight vector of the aggregate portfolio of
  all ETFs existing at that date. A scale-free, time-varying measure of how unlike the rest of
  the industry a product is, with the industry's own composition as the reference point rather
  than a fixed benchmark.
- **The classification axis.** Broad-index and smart-beta funds → *broad-based* (they differ only
  in whether weights are market-cap); sector/industry and thematic funds → *specialized*. The
  paper's point is that the second group is a different population, not a tail of the first.
- **Event time, not calendar time.** The central result is read off **60 calendar-time portfolios
  indexed by months since launch**: for each `k = 1…60`, form a value-weighted portfolio of all
  funds in their `k`-th month of life, run the factor model on each of the 60 series, and plot
  the cumulative abnormal return against months-since-launch. This is the construction to steal.
  It separates "this product type is bad" from "this product type is bad *while it is young*",
  which no calendar-time sort can do, and the answer here is the second.
- **Holdings characteristics at launch.** Newly launched specialized funds hold stocks with
  recent price run-ups, recent and favourable media coverage, more positive earnings surprises,
  high market-to-book, high short interest, and **more positively skewed returns**. Of these,
  the past run-up and the return skewness are computable from a daily close panel; the rest are
  not.

## Robustness evidence (qualitative only)

- Coverage is essentially the population, not a sample: nearly all equity ETFs that ever traded
  in the US market, from the asset class's first year.
- The underperformance result is reported for raw and risk-adjusted returns, after fees, and is
  reproduced on the funds' underlying indexes, which removes the fee and implementation
  explanations.
- The four hypotheses are tested against each other rather than serially confirmed, and three are
  rejected on their own distinct predictions (the negatively-correlated-stock portfolio for
  hedging; flows, closures and closure-performance sensitivity for insurance; post-launch media
  sentiment for warm glow). This is an unusually disciplined elimination structure for a
  catering paper.
- Known limits, stated here rather than in the paper: **one market, one asset class, one
  product-level institution.** The media, analyst-expectation and clientele evidence relies on
  US data sources that have no analogue elsewhere in this folder's constraints, and the sample
  touches 2018–2019, so `validation_overlap` is true and nothing quantitative from it may be
  carried into a hypothesis.

## Implementability here

This is the **ETF half of the dataset-boundary question** [2026-10-09] and it changes the reading
of the panel's 42 ETF columns.

Protocol v2/v3 makes a stock column appear when an index committee adds the name and makes an ETF
column appear **from the ETF's first price**. Session 56 asked the right question of the stock
half — *who moves this boundary, on what information, and is anyone obliged to trade when it
moves?* — and got three unfavourable answers. Asked of the ETF half, the answers are different
and the last one is the sharp one:

- **Who:** a fund provider, not a committee.
- **On what information:** recent performance of a theme or segment, and investor attention to
  it. The launch decision is return-chasing by construction, and for *specialized* products the
  paper's whole case is that the run-up precedes the listing.
- **Is anyone obliged to trade when it moves:** **yes — the v3 equal-weight eligible pool.** It
  holds every eligible instrument, so it takes a position in each ETF from that fund's first
  price, i.e. at the launch date, in whatever the provider chose to launch. A candidate is under
  no such obligation.

That asymmetry is the same shape as #223 — a candidate can decline a cost the benchmark is
forced to pay — and it is a *different* exposure from the stock-side one, because it is about the
ETF sleeve rather than about fresh index entrants.

**Free, returns-free, and it gates everything else in this note (see #227):** this panel has 42
ETFs and `eligible` is True for an ETF from its first price, so the census is pure accounting on
the `eligible` matrix and the first-price dates. How many of the 42 are sector/industry or
thematic rather than broad market or region trackers; what share of the ETF sleeve's weight sits
in funds inside their first 60 months of eligibility, train and validation separately; and
whether that share differs between the two splits. If the specialized population here is two or
three region-sector funds, the vein is empty and this note costs the lab nothing — which is the
outcome to expect and the reason to count before building.

**Two proxies make the mechanism partially measurable without holdings data.**
*(a)* Months since a column's first price is a launch-age variable, available for every ETF.
*(b)* `1 − |corr|` of an ETF's returns against the equal-weight eligible pool over a trailing
window is a **returns-based differentiation proxy**, cheap and causal, and it stands in for the
cosine-similarity measure the paper uses on holdings. Both are computable under v3 without
touching anything new.

**What not to do.**
- Do not import the magnitude or the sign of any performance number from this paper. The sample
  touches the validation window, and the lab's own history with ETF sleeves is all pre-v3
  [`learnings.md`: standalone diversified ETF sleeves cap out well below the champion; the
  inverse-vol blends handed the sleeve most of the capital].
- Do not build a *thematic-ETF* trade. The classification requires prospectus and index-identity
  information the panel does not carry, and the paper's population is US-listed single-country
  products, while this panel's ETFs are mostly broad regional and asset-class trackers.
- The honest claim for any candidate from this note is the weak one — "declines a seasoning
  exposure the benchmark is obliged to hold" — and with v3 skill intervals near ±0.33 that is
  worth a trial only if #227's census says the weight is actually there.

## Related

- `notes/2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` and
  `notes/2026-10-09-index-inclusion-demand-curves-vs-price-pressure.md` — the stock half of the
  same boundary question, and the source of #220–#223.
- `notes/2026-10-10-etf-arbitrage-shock-propagation.md`,
  `notes/2026-10-10-etf-flows-and-the-premium-change-null.md` — the signal-side ETF literature;
  this note is the panel-side one, and the two are independent.
- `notes/2026-09-20-salience-theory-stock-prices.md` — the same Bordalo–Gennaioli–Shleifer
  salience machinery applied to prices rather than to product supply.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` — positive return skewness as
  the characteristic specialized funds' holdings share, measurable here from daily closes.
- `notes/2026-10-01-survival-conditioning-induced-drift.md`,
  `notes/2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — fund *closures* are the
  exit side of this boundary, and the panel's ETF columns are subject to the same
  survival-conditioning theorem as its stock columns.
