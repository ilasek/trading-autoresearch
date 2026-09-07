---
title: "The profitability of pairs trading strategies: distance, cointegration and copula methods" (with "Statistical arbitrage pairs trading strategies: review and outlook")
authors: Rad, Low, Faff; Krauss
year: 2016; 2017
venue: Quantitative Finance 16(10), 1541–1558 (peer-reviewed, venue tier 2); Journal of Economic Surveys 31(2), 513–545 (peer-reviewed survey, venue tier 2)
url: https://doi.org/10.1080/14697688.2016.1164337 — read in full from an author-hosted copy, https://randlow.github.io/2016_QF_PairsTrading.pdf · https://doi.org/10.1111/joes.12153 — read in full from the working-paper version, IWQW Discussion Paper 09/2015, https://www.econstor.eu/bitstream/10419/116783/1/833997289.pdf
citations: Rad–Low–Faff 142 (Crossref `is-referenced-by-count`, checked 2026-09-07). Krauss 190 (Crossref, same date). Semantic Scholar's title-search endpoint was rate-limited (HTTP 429) and OpenAlex's daily budget was exhausted (`Insufficient budget`) by the time these were resolved, so both counts are Crossref-only — a single-index count, per this folder's standing rule not to over-read one
sample_period: Rad–Low–Faff 1 July 1962 – 31 December 2014. Krauss is a survey with no sample of its own; the studies it reviews run from the 1960s to the early 2010s
markets: Rad–Low–Faff: US equities, CRSP share codes 10 and 11. Krauss: international, across equities, bonds, commodities and multiple frequencies
tier: B
validation_overlap: false
published_post_2018: false
---

**Read in full**: Rad–Low–Faff's data, the three strategies' construction, the cost model, the
performance and risk sections and the conclusion; and Krauss's taxonomy, the distance and
cointegration chapters and the conclusion. Both were read from freely hosted copies (an author
page and EconStor); the publisher endpoints were not needed.

**Cointegration is a named `statistical-arbitrage` sub-mechanism in `program.md` and had zero
coverage across all 76 previous notes in this folder** — the largest remaining gap on the
program's own list. This note fills it, and the answer it returns is a closure rather than a
lead.

## Mechanism

The distance method assumes that two price series that have tracked each other will keep tracking
each other. It never tests that assumption; it just measures how closely they have tracked (sum
of squared deviations of normalised prices) and bets on reversion.

Cointegration replaces the assumption with a testable statement. Two `I(1)` price series are
cointegrated if some linear combination `X2 − βX1` is stationary. By Granger's representation
theorem that is equivalent to an error-correction model, in which the deviation from the long-run
relation enters each series' increment with a coefficient that pulls it back. The mechanism is
therefore not new economics — the economic story is the same common-factor-plus-slow-information
story that underwrites the distance method — it is a **better identification of which pairs
actually have the property being traded.** Krauss's own summary of the distance approach's
weakness is exactly this: minimising SSD selects *low-variance spreads with limited profit
potential*, and without a cointegration test it admits spurious relationships that carry
divergence risk. He explicitly names "additional cointegration testing on top of SSD selection"
as the promising repair.

The arithmetic that matters for a long-only lab is one line of Rad–Low–Faff's derivation. Buy one
share of stock 2, short `β` shares of stock 1; the profit over any interval is

    (X2,t − X2,t−1) − β(X1,t − X1,t−1) = spread_t − spread_{t−1}

**The P&L of a pairs trade is identically the change in the spread.** The stationary object being
traded does not exist without both legs; the short leg is not a hedge bolted onto a bet, it *is*
the bet's other half.

## Construction recipe

Rad–Low–Faff's implementation, which follows Gatev–Goetzmann–Rouwenhorst and Do–Faff for the
distance method and operationalises Vidyamurthy for the cointegration one:

- **Formation period 12 months, trading period 6 months, a new cohort started every calendar
  month.** Cohorts overlap, so six run concurrently — structurally the same six-vintage overlap
  the champion in this repo already uses.
- Each name's price is a **cumulative return index scaled to $1** at the start of the formation
  period (dividend- and corporate-action-adjusted).
- **Distance method**: rank all possible pairs by SSD of normalised prices over the formation
  period; take the **20 lowest**. A name may appear in several pairs provided the partner differs.
- **Cointegration method**: walk *down the same SSD-sorted list*, testing each candidate pair for
  cointegration with the **two-step Engle–Granger procedure** (OLS cointegrating regression, then
  the ECM), discarding pairs that fail, and stopping once **20 cointegrated pairs** have been
  collected. Estimate `β` for each survivor. Note the selection metric is unchanged — cointegration
  is a *filter* applied to the distance method's own ranking, not a different ranking.
- **Trading rule, both methods**: recompute the spread in the trading period, standardise it by
  the formation-period mean and standard deviation, and open when the standardised spread diverges
  beyond **±2**; the direction of the divergence sets which leg is long. For the cointegration
  method the leg sizes are `$1` of one name against `$β` of the other. **Close when the spread
  returns to zero.** A pair is then monitored again and may complete several round trips within
  its trading period.
- **Costs, and they are heavier than this repo's.** Time-varying institutional commissions
  declining from 70 bps in the early sample to 9 bps in the later years, plus a market-impact
  estimate of 30 bps in the earlier sub-period and 20 bps in the later one, and **the whole thing
  doubled** because a complete pairs trade is two round trips. Short-selling fees are assumed
  negligible only because low-price and low-cap names are screened out first.

## Robustness evidence (qualitative only)

**The headline result, and the reason this note exists: cointegration performs about as well as
the distance method, and after costs slightly worse.** Over a 52-year US sample, Rad–Low–Faff find
the two methods deliver comparable economic and risk-adjusted performance, with "very similar pair
trade properties and risk profiles". Before costs the cointegration method is ahead on
lower-partial-moment and drawdown measures; after costs the distance method is slightly superior.
The copula method is the weakest of the three on both, which the authors attribute to a high
proportion of trades that never converge.

Other qualitative findings worth carrying:

- **Costs consume the majority of the gross return for every method tested.** For the distance and
  cointegration methods roughly three-fifths of the gross spread return is lost to the cost model
  above; for the copula method close to nine-tenths. This is not a marginal drag, and it is
  measured under a cost model in which the modern-era per-side charge is around 29 bps — roughly
  twice this repo's 15 bps — but applied to two legs and multiple round trips per pair.
- **The effect is not a risk premium and it decays.** Krauss's synthesis: pairs-trading
  profitability has low exposure to systematic risk factors, **declines over time**, and is partly
  explained by information diffusion and market frictions such as liquidity. That is the
  McLean–Pontiff shape, and the decay is documented independently by several of the studies he
  reviews.
- **Multi-market and multi-asset confirmation of the underlying effect** (bonds, commodities,
  other frequencies), with the original distance-method findings usually reproduced. The
  *comparison* between distance and cointegration, however, rests on one market — Rad–Low–Faff is
  US-only — which is why this note is tier B rather than A.
- **A construction warning from Krauss that generalises well past pairs trading**: an SSD-style
  "pick the closest tracking pair" metric systematically selects for *low spread variance*, which
  is not the same as selecting for *strong mean reversion*. A selection rule can be optimising the
  wrong moment of the object it selects. Pearson correlation on returns is reported to do
  slightly better than SSD; a cointegration test does better still at identification, and — per
  the headline above — that improved identification does not survive the cost of getting it.

## Implementability here

**The long-only constraint is not a discount on this family, it is a structural refutation of
this particular sub-mechanism, and `program.md` asks candidates to say so explicitly.** The P&L
identity above means the traded object is the spread. Remove the short leg and what remains is
"buy the cheaper member of a pair that has diverged", i.e. a **plain reversal signal on a single
name**, with the partner supplying nothing but a reference level. That object has no `I(0)`
property, the cointegration test that justified the pair no longer certifies anything about it,
and `learnings.md`'s standing horizon rule applies with full force: the strongest reversal
measurable on this universe is at 5–10 days and a book paying 15 bps a side is on the wrong side
of it. This is the same wall `2026-08-30-pca-residual-statistical-arbitrage-long-only` hits from
the residual-reversion direction.

**The specific move this note forecloses.** The lab has already refuted the distance method. The
natural next thought — *the distance method failed because it never tested for cointegration;
build the econometrically sound version* — is exactly Krauss's recommended repair, and
Rad–Low–Faff have already run it on a 52-year sample with costs: it is a wash before costs and
slightly worse after. **Do not spend a trial re-deriving that.** If `statistical-arbitrage` is
revisited it should be on a different object (Krauss's time-series and stochastic-control
branches, or the multivariate/quasi-multivariate constructions he reports outperform the
univariate ones), not on the cointegration filter.

If someone builds it anyway, four practical notes:

1. **`statsmodels` is not in `requirements.txt`** — only `numpy`, `pandas`, `scipy` and
   `scikit-learn`. The OLS cointegrating regression is trivial in `numpy`, but the second step
   needs a residual-based unit-root test whose critical values are **not** the standard
   Dickey–Fuller ones (the residuals are estimated, which shifts the null distribution). Those
   would have to be hard-coded from published tables or replaced by a bootstrap on the formation
   window. A candidate that uses ordinary ADF critical values on estimated residuals is
   over-rejecting and will select spurious pairs — the exact failure cointegration was added to
   prevent.
2. **Pair count is not a compute problem but is a multiple-testing one.** 140 instruments give
   9,730 unordered pairs, tested every formation window. Selecting the 20 that pass a 5% test out
   of thousands of candidates is a search, and this repo already has the machinery to think about
   that: `2026-08-24-multiple-testing-haircut`, `2026-09-01-multi-signal-overfitting-critical-t`.
   Rad–Low–Faff sidestep it by testing *down a pre-sorted SSD list* rather than testing all pairs
   — that ordering is doing real work and should be kept.
3. **The 42 ETFs are both the best and the worst part of this universe for the idea.** Region and
   sector ETFs on overlapping baskets are cointegrated for a *mechanical* reason, so genuine
   cointegrated pairs are much easier to find here than in a stock-only universe — but their
   spreads are small, dominated by tracking noise, and across time zones dominated by the session
   offset the 2026-09-06 nightly measured at 4x the US-only benchmark. Any ETF pair spanning two
   sessions will show a spurious lead-lag spread that looks tradeable and is not. Build and test
   spreads on **weekly** returns, or restrict pairs to a single session.
4. **Causality and refit cost.** Selection and `β` must be re-estimated per formation window,
   which is walk-forward by construction and deterministic, so the lab's causality check is
   satisfiable. The convergence-triggered exit is the awkward part: the engine forward-fills sparse
   weight rows and applies a 1-day lag, so a rule of the form "close when the spread crosses zero"
   has to be expressed as a full daily weight path, not as an event.

## Related

- `2026-09-03-pairs-trading-distance-method` — the Gatev–Goetzmann–Rouwenhorst source this note is
  the sequel to; the lab refuted the method, and this note says the econometric upgrade does not
  rescue it.
- `2026-08-30-pca-residual-statistical-arbitrage-long-only` — the other `statistical-arbitrage`
  branch, which fails on the same long-only wall from the residual direction.
- `2026-08-17-mclean-pontiff-publication-decay` — the decay shape Krauss reports for this family.
- `2026-08-24-multiple-testing-haircut`, `2026-09-01-multi-signal-overfitting-critical-t` — the
  selection-out-of-thousands problem in point 2.
- `2026-09-05-cross-serial-correlation-as-restatement` — the nonsynchronous-trading argument
  behind the ETF-pair warning in point 3.
