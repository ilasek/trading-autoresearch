---
title: "Caveat Compounder: A Warning about Using the Daily CRSP Equal-Weighted Index to Compute Long-Run Excess Returns"
authors: Canina, Michaely, Thaler, Womack
year: 1998
venue: Journal of Finance 53(1), 403–416 (Tier 1)
url: https://doi.org/10.1111/0022-1082.165353
citations: "92 (Crossref `is-referenced-by-count`, checked 2026-10-03); 151 (Semantic Scholar DOI endpoint, checked 2026-10-03); 148 (OpenAlex, checked 2026-10-03). Crossref low again, consistent with this folder's standing pattern."
sample_period: "1964–1993 (360 months), CRSP daily and monthly tapes"
markets: US equities (CRSP equal-weighted and value-weighted indices; Monte Carlo on randomly drawn CRSP portfolios of 10–900 names)
tier: "A. Tier-1 venue, four established authors, read in full, and — as with Roll — it is a result about an **estimator**, so it does not decay. Its one honest weakness is recorded below: about half the variation in the bias is explained by the theory's variables, and several coefficients come out with the *wrong sign*, which the authors state plainly rather than bury."
validation_overlap: false
published_post_2018: false
---

## Access

**Read in full.** OpenAlex reports `oa_status: closed`, but **Semantic Scholar's `openAccessPdf`
pointed at Cornell's institutional repository and the file was served on the first try**:
`ecommons.cornell.edu/server/api/core/bitstreams/<uuid>/content` (reachable; parses cleanly with
`pypdf`). Tables are images and were not read; every number below is from the body text, which states
all of them.

**Two access findings, both the inverse of recent lessons:**

1. **An `oa_status: closed` from OpenAlex is not proof that nothing is fetchable.** [2026-10-01] and
   [2026-10-02] both recorded that a `GREEN` flag is no promise of reachability. Tonight is the
   mirror image: the index that said *closed* was wrong in the useful direction, and the index that
   said GREEN was right. **Check all three indexes' location lists before declaring a paper closed** —
   this folder has now been wrong in both directions within three nights.
2. **`ecommons.cornell.edu` is a reliable DSpace channel** whose `server/api/core/bitstreams/<uuid>/content`
   form serves files directly, in contrast to `pyxida.aueb.gr`, which runs the same software behind
   **Anubis** (see the companion note's Access section).

## Mechanism

**The arithmetic of compounding a daily equal-weighted index is not the arithmetic of holding an
equal-weighted portfolio, and the gap is far larger than researchers guess.** This is the direct
empirical measurement of the Roll (1983) / Blume–Stambaugh (1983) result; the authors cite both as
the reason the bias should exist and say most economists "(should) know" it, while observing that a
casual poll of empirical finance researchers found only heavy data users had any sense of its
magnitude.

The two quantities compared:

- **Compounded daily**: form the equal-weighted cross-sectional mean return each day, then multiply
  the daily gross returns across the month. This is *daily rebalancing* — Roll's `RB` at daily
  frequency.
- **Monthly**: link each security's own daily returns across the month, then average across
  securities. This is Roll's `BH` over a one-month horizon.

**Finding.** The compounded-daily equal-weighted return exceeds the monthly equal-weighted return by
roughly **0.43% per month, about 6% per year** — on the order of **one third of the average monthly
return** — and it was higher in *every single year* of the sample. (Recorded as the magnitude of an
**estimator bias** in a pre-1994 US panel, which is this paper's entire contribution; the paper's
year-by-year and month-specific narratives are deliberately not recorded here.) The **value-weighted**
index shows no such bias, which is the clean control: compounding a value-weighted index is unbiased,
compounding anything else is not.

**Why.** The authors regress the gap (`Diff`) on the theory's drivers and find it is larger when:

- the **average first-order autocorrelation of individual securities is more negative** (bid-ask
  bounce) — coefficient negative and highly significant;
- the **portfolio's own first-order autocorrelation is more positive** (non-synchronous trading) —
  positive and significant;
- the **cross-sectional variance of returns** is higher — positive and significant, **but this is the
  opposite sign from what Roll's theory predicts**, which the authors flag and attribute to possible
  departures from normality/independence;
- a direct bid-ask proxy — the variance of excess-return-to-price, borrowed from Blume–Stambaugh —
  raises explanatory power sharply (`R²` from ~22% on autocorrelations alone to ~47%, ~50% with both).

**The relative magnitudes identify which channel dominates.** Mean portfolio autocorrelation is about
+20% with coefficient 0.0035; mean individual-security autocorrelation is about −6.3% with coefficient
−0.032. So the **individual-security channel has roughly two-and-a-half times the effect of the
portfolio channel** — i.e. **bid-ask bounce matters more than non-synchronous trading** for this bias.

**Turnover and dividends do not matter.** Higher turnover should mean less bounce and less
non-synchronous trading; the coefficient has the expected negative sign but is **insignificant**. A
dividend-timing channel (daily tape adds dividends on the ex-day, monthly tape at month end) is
signed as expected and also insignificant.

**The result that makes this a problem for a small universe.** A Monte Carlo on randomly drawn CRSP
equal-weighted portfolios of 10, 100, 300, 600 and 900 names gives annualised gaps of about **6.5%,
7.1%, 7.2%, 7.2% and 7.2%** respectively. **The bias does not diversify away.** It is already nearly
full-size at ten instruments and is flat from 100 upward. The authors also note it afflicts *any*
equally-weighted portfolio whose long-run return is computed from daily data, not just a benchmark.

## Construction recipe

The paper's own remedies, in its stated order of preference (worst to best):

1. **Use a value-weighted index** as the benchmark — unbiased under compounding. Cheapest fix, but it
   changes the object being measured.
2. **Use monthly rather than daily data** for the equal-weighted series. The authors note, citing
   Roll (1983), that **the gap between a yearly buy-and-hold and a *monthly* rebalance is very
   small** — the damage is specific to daily compounding. For a horizon that does not align to month
   boundaries, *splice*: daily tape for the partial first month, monthly for the whole months, daily
   for the partial last month.
3. **Compute the buy-and-hold return directly** — take the portfolio's price-index level (dividends
   reinvested) at the first and last day of the holding period and form the return from those two
   numbers. The authors call this "clearly the best": exact, bias-free, and it imposes no restriction
   on the weighting scheme of the benchmark.

They explicitly decline to recommend monthly rebalancing as a real-world *strategy* — the comparison
is about the arithmetic's fidelity to a holding experience, abstracting from transaction costs.

## Robustness evidence (qualitative only)

- **Tier-1 venue, read in full, and the mechanism is pre-registered by two earlier Tier-1 papers**
  (Roll 1983; Blume–Stambaugh 1983) rather than discovered by search. That is the strongest form of
  replication available for an estimator result.
- **Internal control that works**: the value-weighted index shows no bias, exactly as theory says, and
  the authors include it specifically as a check on their own method.
- **Monte Carlo robustness across portfolio size** (10 to 900 names) — the key external-validity
  evidence for a universe much smaller than CRSP.
- **Methodology honesty is high and recorded as such**: they report that only about half the monthly
  variation in the bias is explained by the theory's variables, and that the cross-sectional-variance
  coefficient has the *wrong sign*. They do not claim the theory is complete.
- **Known limits**: single market (US), single data vendor (CRSP), and the regressions are monthly
  time series over 360 observations, so the explanatory decomposition is far weaker evidence than the
  headline gap. The headline gap is a near-arithmetic identity; the attribution to channels is not.

## Implementability here

**Not a candidate strategy — a measurement check, and the most directly actionable item in tonight's
cluster.**

- **This universe sits in the worst part of the parameter space on one axis and the best on another.**
  Worst: ~140 instruments is inside the flat region of the Monte Carlo, so **the lab gets essentially
  the full bias, and cannot argue it away by diversification** — the folder should stop expecting
  small-N to help here. Best: the lab's candidates rebalance **monthly**, and both this paper and Roll
  say a monthly rebalance is close to buy-and-hold. The exposure therefore depends entirely on
  whether the *reported statistic* is computed from a daily grid or from monthly-linked returns.
- **The lab's weights are forward-filled to a daily grid.** The strategy contract says rows may be
  sparse (monthly rebalances) and "the engine forward-fills and applies a 1-day execution lag, costs,
  and caps". A forward-filled monthly weight vector on a daily grid is **economically** a monthly
  rebalance, so the position path is fine. The question is purely how the engine turns that path into
  a Sharpe: daily portfolio returns compounded (`RB`-at-daily, biased up) or instrument returns linked
  then weighted (`BH`, unbiased). **This agent is not permitted to read `engine/` and makes no claim
  about which it does.** It is a one-look question for the strategy agent or the human and it is
  upstream of every number on the leaderboard, so it should be answered before it is argued about.
- **If the engine does compound a daily equal-weighted cross-section, the bias is a level shift on
  every trial — including the champion and including the holdout veto's paired comparison.** A level
  shift common to candidate and incumbent largely cancels in a *paired* `t`, which is the lab's gate,
  so the leaderboard's *rankings* would be far more robust than its *absolute* Sharpes. That is worth
  stating because it bounds the damage: this channel threatens the lab's reported levels much more
  than its promotion decisions. It does **not** cancel where the two books differ in bid-ask-bounce
  exposure — which is precisely the `liquidity-volume` and low-volatility cases.
- **The bid-ask-bounce ordering is the cheap test, and the paper supplies its statistic.** The
  dominant driver is the *average first-order autocorrelation of individual instruments*, and the
  best single proxy is the **variance of excess-return-to-price**. Both are computable from closes
  alone, causally, on data the lab already has, for free. A book whose holdings have more negative
  individual autocorrelation should show a bigger daily-versus-monthly gap. **This is the measurement
  that turns the companion note's prediction into a number.**
- **Universe caveat specific to this repo.** This lab's panel is global with foreign-holiday gaps, so
  non-synchronous trading is *structurally worse here than in CRSP* — a global cross-section mixes
  instruments whose last trade is up to a day apart by construction, which is the textbook generator
  of the positive portfolio autocorrelation this paper measures. The paper finds the portfolio channel
  is the *weaker* of the two in CRSP, but it has no evidence on a multi-region panel and neither does
  this folder. **Treat the relative importance of the two channels as unmeasured here.**
- **42 of the lab's ~140 instruments are ETFs**, which are themselves value-weighted baskets. By this
  paper's own control result those carry no compounding bias of their own, so a book's exposure to
  this bias should **scale with its weight on single stocks rather than ETFs** — another free,
  falsifiable ordering across books already on the board.
- **Pitfall:** the fix is not to switch the engine (frozen, and correctly so). The fix is to know which
  quantity the engine reports, and to stop comparing it to literature premia computed the other way.
  Note also that this folder's own standing instruction — never import performance expectations from
  literature into hypotheses — is partly *motivated* by this paper: published premia and lab Sharpes
  can differ by the estimator alone.

## Related

- `2026-10-03-mean-return-computation-rebalanced-vs-buy-and-hold.md` — Roll and Blume–Stambaugh, the
  theory this paper measures. Read that one first; this one supplies the magnitude and the
  size-invariance.
- `2026-10-03-international-panel-screens-datastream.md` — the panel defects that inflate the
  individual-autocorrelation term this bias is driven by.
- `2026-10-02-noisy-prices-and-biased-premium-estimates.md` — ABK; the excess-return-to-price variance
  used here as a bid-ask proxy is the same object ABK's multiplicative-noise correction reweights.
- `2026-09-04-global-liquidity-proxy-horserace.md` — the zero-return and proportional-spread proxies,
  which are the other route to the same bounce statistic.
- `2026-08-27-momentum-net-of-costs-debate.md` and `2026-08-27-live-execution-costs-implementation-shortfall.md`
  — the cost literature; note that this bias is **not** a cost and is not reduced by modelling costs.
