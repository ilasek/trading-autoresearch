---
title: "Pairs trading, the distance method — relative-value convergence between matched substitutes, and what a long-only book can keep of it"
authors: Gatev, Goetzmann, Rouwenhorst; with Do, Faff as the independent cost-and-decay reexamination
year: 2006 (GGR, published); 2010 and 2012 (Do–Faff)
venue: Review of Financial Studies 19(3), 797–827 (venue tier 1); Financial Analysts Journal 66(4), 83–95 (venue tier 1); Journal of Financial Research 35(2), 261–287 (venue tier 2, peer-reviewed field journal)
url: https://doi.org/10.1093/rfs/hhj020 — working-paper version read at https://www.nber.org/system/files/working_papers/w7032/w7032.pdf ; Do–Faff at https://doi.org/10.2469/faj.v66.n4.1 and https://doi.org/10.1111/j.1475-6803.2012.01317.x
citations: GGR 642 (Crossref `is-referenced-by-count`, checked 2026-09-03); Semantic Scholar resolves the same DOI to the working-paper record with 929 (checked 2026-09-03). Do–Faff 2010: 254; Do–Faff 2012: 164 (both Semantic Scholar by DOI, checked 2026-09-03)
sample_period: 1962–1997 in the NBER working-paper version read here (the published RFS version extends the sample; its exact end date was not verified from a source read for this note). Do–Faff 1963–2009
markets: US (CRSP daily), liquid common stocks; sector-restricted variants within Utilities, Transportation, Financials and Industrials
tier: B
validation_overlap: false
published_post_2018: false
---

**Read in full**: the NBER working-paper version of GGR (`w7032`, 35 pages, extracted cleanly),
which contains the complete methodology, the risk decomposition, the bootstrap control and the
transaction-cost discussion. **Not read in full**: both Do–Faff papers. Every route tried refused an
automated client or is closed access (SSRN 403 as documented; the Wiley and Taylor & Francis pages
serve no full text; Semantic Scholar's `openAccessPdf` for the 2012 paper points back at SSRN). Their
role below rests on **abstracts obtained verbatim from a university research portal**, and every
claim attributed to them is flagged as second-hand. The tier is B for that reason and because the
evidence read here is single-market.

This is the second source in `statistical-arbitrage`, a family with one prior note and one declined
lab screen. It is a **different object** from the family's existing coverage: Avellaneda–Lee trade
the residual of a stock against an estimated factor set; this trades one stock against **one matched
partner**, with no factor model, no estimation of a covariance matrix, and no parameter beyond two
window lengths and a trigger.

## Mechanism

**The economic claim is about the Law of One Price at the level of individual securities.** Two
securities that are close economic substitutes should be priced closely; a temporary divergence is
either an inventory or liquidity shock in one of them, or a piece of news that has reached one price
before the other. Betting on convergence is a bet that the local market for those two names is
integrated. The authors frame the profits as compensation for supplying that integration —
"marginal profits from risk arbitrage of these temporary deviations are crucial to the maintenance
of first-order efficiency" — which makes the effect a **liquidity-provision** premium in the same
family as short-horizon reversal, but *conditioned on a substitute relationship* rather than on a
name's own past return.

Four structural findings, all mechanism rather than performance:

1. **The matching is done in price space, not in characteristic space.** Partners are chosen by
   minimising the sum of squared deviations between two normalised cumulative total-return series.
   No fundamentals, no industry classification is required (though restricting to industry is
   examined and works). This is the entire reason the method is reachable on daily closes alone.
2. **The trade is conditional, not a sort.** A position exists only when the normalised prices have
   diverged by more than a threshold calibrated on the formation window; most of the time most pairs
   hold nothing. Pairs open on the order of a couple of round trips per six-month trading window,
   and stay open for on the order of weeks rather than days.
3. **It is not the bid-ask bounce, and it is not one-day reversal.** Two separate controls. (a)
   Delaying every open and close by **one full day** removes a substantial part of the raw profit —
   the authors treat that drop as a conservative lower-bound estimate of the effective spread in
   their sample, on the order of tens of basis points per round trip — and the strategy is analysed
   with that delay imposed throughout. (b) Monthly returns are **positively** autocorrelated, so the
   payoff accrues gradually over the holding period, which is the opposite of a short-horizon
   reversal signature.
4. **The convergence bet is not factor-neutral in practice, despite being built to be.** Market
   exposure is small and insignificant — expected, since partners are chosen for comovement — but
   exposures to size, value, the bond default premium and the term premium are positive and
   significant, and the regression R² is low while intercepts remain significant. So a matched pair
   removes the market and leaves other systematic exposure behind. This matters enormously for the
   long-only adaptation below.

**The control that deserves separate billing.** To test whether the profits are merely disguised
short-horizon reversal, the authors bootstrap **random pairs formed within the same sector** and
trade them by the identical rules. That is a placebo whose partner-selection information has been
destroyed while everything else — universe, trigger, windows, cost treatment — is held fixed, and
the real strategy's profits sit far in the tail of that distribution. It is a 1990s instance of the
exact control this lab discovered it needed in 2026-09-02.

**Where Do–Faff enter (second-hand).** Their two papers re-examine the same rules over a longer
sample with an explicit cost model. From their abstracts, verbatim: after controlling for
"commissions, market impact, and short selling fees, pairs trading remains profitable, albeit at
much more modest levels", with what survives concentrated "among portfolios of well-matched pairs
that are formed within refined industry groups"; and pairs trading "exhibits a lower risk and lower
return profile than a short-term reversal strategy that sorts stocks relative to their industry
peers". They also document a **secular decline** in the strategy's profitability across their
sample, and report that refinements to the matching algorithm recover part of it. Two directional
lessons to carry, both cost-relevant and neither dated: **finer industry grouping in the matching
step is where the surviving profit is**, and **the effect has decayed since publication**, which is
what `notes/2026-08-17-mclean-pontiff-publication-decay.md` predicts for a widely published rule.

## Construction recipe

The full distance method, enough to implement without re-reading:

- **Formation window: 12 months of daily data.** Screen out any stock with one or more no-trade
  days over the window (a liquidity filter and a data-hygiene step in one). Build a **cumulative
  total-return index** for each survivor, normalised to a common starting value, with dividends
  reinvested.
- **Matching**: for each stock, choose the partner minimising the **sum of squared deviations**
  between the two normalised price series over the formation window — exhaustive pairwise search.
  Optionally restrict matching to within broad sector groups; the sector-restricted variant is
  reported as profitable in every group examined, and Do–Faff report that *finer* grouping is where
  the cost-surviving profit sits.
- **Selection**: rank pairs by the same distance and trade the top *N* (they report top 5 and top
  20). They also trade **pairs 101–120** as a deliberate control on whether the effect is specific to
  the very closest matches.
- **Trigger**: open when the normalised prices diverge by more than **two standard deviations of the
  pair's spread as estimated over the formation window** — long the lower-priced (relative) name,
  short the higher-priced one, one dollar each way.
- **Exit**: at the **next crossing** of the two normalised prices; force-close any open position at
  the end of the trading window. Pairs may reopen within a window, in either direction.
- **Trading window: the following 6 months.** Both 12 and 6 are stated by the authors as arbitrary
  choices held fixed throughout the study — worth noting, because it means neither is tuned.
- **Execution convention: a one-day delay on every open and close**, explicitly to avoid trading on
  the bid-ask bounce.
- **Overlapping tranches**: the strategy is initiated at the **beginning of every month**, so six
  staggered six-month portfolios run concurrently, each formed on its own prior twelve months.
- **Accounting**: return on *committed* capital (payoff summed over all pairs, divided by the number
  of pairs in the portfolio, counting a dollar for pairs that never open) is the conservative
  measure; return on *employed* capital (divided by the number of pairs that actually opened) is the
  flattering one. Report the conservative one.
- **Placebo**: repeat everything with randomly assigned within-sector partners and read the real
  result's p-value against that distribution.

## Robustness evidence (qualitative only)

Multi-decade daily US sample in the version read, extended by an independent team in a later
peer-reviewed paper with an explicit cost model — replication with costs by authors other than the
originators is the strongest single item in this source's favour. Profitable in every broad sector
group examined, not confined to one; the effect survives the authors' own random-pairs bootstrap and
their conservative execution and accounting conventions; the "pairs 101–120" portfolio is a designed
robustness arm rather than an afterthought. Two acknowledged gaps and one caution. The gaps: the
evidence read here is **single market**, and both windows and the trigger are hand-chosen (though
fixed a priori, not searched). The caution: the authors state plainly that data-snooping is a
serious concern for a strategy this well known, and Do–Faff's documented decay is what that concern
looks like realised. The 2010 paper's own title — "Does simple pairs trading still work?" — is the
literature asking the question, and its answer is qualified rather than affirmative.

## Implementability here

The universe is ~145 global large-cap names plus 42 ETFs across 15 regions, long-only at gross ≤ 1.0
with ≤ 25% per position, daily USD-adjusted closes (plus OHLCV), 15 bps/side and a 1-day execution
lag.

1. **Three of this repo's constraints are already the source's own conventions, which is unusual and
   should be said first.** The **one-day execution lag** the engine imposes is the exact convention
   GGR adopt deliberately; the **overlapping monthly tranches** are the same mechanism
   `learnings.md` records as "the strongest mechanism in the repo"; and the formation input is a
   normalised **total-return** series, which is what `prices` already is. Nothing about the recipe
   needs to be bent to fit here.
2. **The long-only adaptation is a selection rule, and it is the honest version of the idea.** Only
   the cheap leg is holdable. So: at each month-end, form pairs on the trailing 12 months, compute
   each name's current spread against its partner in formation-window standard deviations, and hold
   the names most **depressed relative to their own matched partner** — a fixed slice, or every name
   past the 2σ trigger, capped and equal-weighted. What is lost is precisely the hedge: the pair's
   short leg is what removes the common exposure, so a long-only book keeps the market and — per
   finding 4 — the size, value and rate exposures too. **This is the same structural point the
   folder's existing `statistical-arbitrage` section makes about residual reversion, arriving from a
   different construction**, and it means the candidate must be framed as *"does a partner-relative
   spread rank names better than an unconditional price rank?"* — a selection question — not as a
   decorrelation claim.
3. **It is the family's first genuinely *conditional* object, which is the gap the folder itself
   identified.** `SUMMARY.md`'s `statistical-arbitrage` section notes that the lab measured an
   unconditional cross-sectional IC while Avellaneda–Lee trade a conditional excursion, and that an
   unconditional IC can be null while the conditional tail trade is not. The distance method is
   conditional by construction — most pairs hold nothing most of the time — so a long-only version
   of it tests the untested half of that tension. It is also cheap to *pre-screen* for free on train:
   compute the pair-spread z-score panel and read the forward-return spread of the most-depressed
   names against the rest, before any trial is spent.
4. **Turnover looks favourable relative to everything else in this family, and that is the main
   reason to prefer it.** A couple of round trips per pair per six-month window, with positions held
   for weeks, is far below the 13–19× annual turnover of the lab's union books and orders of
   magnitude below a learned monthly signal. At 15 bps/side that difference is worth 2–3%/yr, which
   `learnings.md` calls the largest unattacked drag outside the champion. **But do not assume it:
   the long-only version re-forms its holdings every month and has no "closed" state, so its
   turnover is a property of the ranking's persistence, not of the pair rule. Measure it
   holdings-only before proposing.**
5. **Four universe-specific pitfalls, in order of how likely they are to decide the result.**
   (a) **Cross-region matching will find currency and region factors, not substitutes** — two names
   in the same country will comove for reasons that have nothing to do with being economic
   substitutes. Restrict matching within region, or within region × sector, which is also the
   direction Do–Faff report as the surviving one. (b) **The ETFs will dominate the top of any
   distance ranking**, because broad index funds have low idiosyncratic variance and will match each
   other almost perfectly — the same reason GGR's top pairs are full of utilities. Decide in advance
   whether ETFs are eligible as partners, and report the mixed-pair share. (c) **Survivorship**:
   pairs are formed among today's constituents, so both members of every pair survived; the folder's
   standing survivorship notes apply with extra force to a strategy that bets on convergence rather
   than on continuation. (d) **145 names is a thin matching pool.** GGR match within thousands; with
   ~145 instruments and a within-region restriction, some regions will have too few names to match
   at all. **Precondition, free and to be run first: count the eligible names per region and the
   distribution of formation-window match distances.** If the best available partner for most names
   is a poor match, the mechanism is absent by construction and that is the finding — the same shape
   as the precondition that killed `SUMMARY.md` #69.
6. **The placebo is not optional here, and the source supplies it.** `learnings.md` (2026-09-02)
   concluded that "a placebo arm is the cheapest falsification this lab has and it had never been
   run", after a random partner bought as much as a real one in a union book. GGR's random-pairs
   bootstrap is the same control for this mechanism, was run by the authors themselves, and costs
   the lab one extra weight-matrix build with shuffled partner assignments. **A long-only pairs
   candidate should be proposed with its random-partner control specified in advance**, and the
   comparison is what makes the result interpretable either way.
7. **What this note does not claim.** No performance expectation: the numbers in the source are from
   a US all-stock sample with a short leg, no position cap, and a cost environment that is not this
   one, and Do–Faff's own finding is that costs and time both take large bites. The value of the
   note is a **construction** with an unusually small number of free parameters and a built-in
   control — not a promise about its size.

## Related

- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` (Avellaneda–Lee) — the family's
  other note. Same family, opposite construction: an estimated factor model and a residual s-score
  there, a single matched partner and no estimation here. The two agree on the long-only diagnosis
  (only the cheap side is holdable, and the book keeps the factor exposure the signal removed) and
  differ on everything else, which makes the distance method the cheaper first test of the family's
  central question.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — the mechanism this strategy is
  most easily confused with; GGR's positive monthly autocorrelation and their one-day-delay control
  are the two pieces of evidence that separate them, and Do–Faff (second-hand) compare the two
  directly and report pairs trading as the lower-risk, lower-return of the pair.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the decay Do–Faff document is this
  literature's own instance of it; a heavily published rule from a top journal is exactly the
  profile that decays.
- `notes/2026-08-31-intra-industry-lead-lag-grouping.md` and
  `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` — the folder's other within-group
  constructions; the grouping question ("how fine?") is the same one Do–Faff answer for matching.
- `experiments/learnings.md` 2026-09-02 (the placebo partner) — point 6; and the standing
  overlapping-tranche result, which this recipe uses natively.
