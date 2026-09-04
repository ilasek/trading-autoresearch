---
title: "What Are the Best Liquidity Proxies for Global Research?"
authors: Fong, Holden, Trzcinka
year: 2017
venue: Review of Finance 21(4), 1355–1401 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1093/rof/rfx003
citations: 414 (Crossref, checked 2026-09-04); Semantic Scholar's DOI endpoint returns "not found" for 10.1093/rof/rfx003 (checked 2026-09-04) — see the access note below
sample_period: 1996–2007
markets: 24,847 firms on 43 exchanges worldwide; intraday benchmarks from Thomson Reuters Tick History, US from TAQ/CRSP
tier: A
validation_overlap: false
published_post_2018: false
---

**Text read**: the authors' March 2015 working-paper version (`cicfconf.org/sites/default/files/paper_337.pdf`),
whose abstract, research design, proxy definitions and headline conclusions match the published
Review of Finance article. Section numbers below are the working paper's. Nothing here is taken
from the published version's page proofs, so a construction detail that changed in revision would
not be visible; the recipes given are stable, long-standing definitions from the cited primary
sources (Roll 1984, Lesmond–Ogden–Trzcinka 1999, Corwin–Schultz 2012) rather than novel to this
paper, with the exception of FHT itself.

## Mechanism

This is not a paper about a return premium. It is a **measurement** paper, and its object is the
gap between a liquidity *proxy* computable from daily data and the liquidity *benchmark* you would
compute if you had the intraday trade-and-quote record. That gap is the whole subject, which makes
it the natural grading instrument for any strategy whose signal is a liquidity characteristic
estimated from daily bars.

The economic setup is the standard microstructure decomposition. A trade pays some fraction of the
quoted spread (**percent effective spread**); part of that is compensation the liquidity supplier
keeps (**percent realized spread**) and part is the permanent move the trade causes (**percent
price impact**), with realized spread plus price impact summing to effective spread by
construction. Separately, the **cost per unit of volume** — the slope of the price function,
Kyle's lambda — measures how much price moves per dollar traded. These are two different things:
a percent-cost measure answers "what does a round trip cost as a fraction of price", a
cost-per-volume measure answers "how fast does price move as I push size". Amihud's `ILLIQ` is in
the second class by construction; a spread proxy is in the first.

The paper's central structural finding is that **these two classes are not equally well
approximated from daily data**, and that within each class, three things a proxy can do —
rank names cross-sectionally, track a market's liquidity through time, and get the *level* right —
come apart and must be graded separately. That separability is the mechanism worth carrying: a
proxy can be an excellent *ordering* of names inside one market and simultaneously a bad *number*,
and whether that matters depends entirely on whether the strategy compares proxy values across
groups that were estimated under different conditions.

## Construction recipe

Three performance dimensions, each computed against an intraday benchmark, each reported both
globally and exchange by exchange:

1. **Average cross-sectional correlation** — Fama–MacBeth style: correlate proxy against benchmark
   across firms within a period, then average the period correlations.
2. **Portfolio time-series correlation** — average proxy and benchmark across all stocks in a
   market per period, then correlate the two series.
3. **Average RMSE** against the benchmark, computed per exchange per period and then averaged.
   This is the *level* test, and it is the one the other two cannot substitute for.

The proxy classes and their inputs (all computable from daily data; the ones this repo could
actually build are marked):

**Percent-cost proxies**
- **Closing Percent Quoted Spread** — the closing bid–ask spread divided by the closing midpoint.
  *Not available here* (needs closing quotes, not OHLCV).
- **High-Low** (Corwin–Schultz 2012) — from daily high and low prices. **Available here**; see
  `notes/2026-09-04-high-low-spread-estimator.md`.
- **FHT** (this paper's contribution) — an analytic simplification of the LOT Mixed model, from
  the frequency of zero returns and the volatility of non-zero returns:

  ```
  sigma = std(non-zero daily returns over the window)
  Zeros = (# zero-return days) / (# days)
  FHT   = 2 * sigma * Phi^{-1}( (1 + Zeros) / 2 )
  ```

  where `Phi^{-1}` is the inverse standard normal CDF. **Available here — closes only, no volume,
  no range.** The intuition is that a zero observed return is the signature of a true value change
  too small to escape the round-trip cost band, so a higher zero-return frequency at a given return
  volatility implies a wider band. Both LOT measures rest on exactly these two ingredients
  (zero-return proportion and return volatility) and outperform either one alone; FHT keeps the two
  ingredients and drops the numerical likelihood maximisation.
- **Zeros / Zeros2 / LOT Mixed / LOT Y-Split** — the older zero-return family. Available here in
  principle; the paper's point is that they are dominated.
- **Roll** (1984) and **Extended Roll** — from the serial covariance of daily price changes.
  Available here, with the standard nuisance that the covariance is frequently the wrong sign.
- **Effective Tick** — from the clustering of prices on tick multiples. Available in principle but
  its assumptions are venue-specific.

**Cost-per-volume proxies** are, with one exception, just a percent-cost proxy divided by average
daily local-currency volume: *Closing Percent Quoted Spread Impact*, *LOT Mixed Impact*, *High-Low
Impact*, *FHT Impact*, *Roll Impact*, and so on. The exception is **Amihud**, which is the
mean over days of `|return| / dollar volume` and is its own thing.

**Daily-frequency versions.** Most of these break down at a one-day window; the paper examines the
two percent-cost proxies that survive (High-Low, Closing Percent Quoted Spread) and four
cost-per-volume proxies (Amihud, Amivest, and two others) against daily benchmarks.

## Robustness evidence (qualitative only)

The horserace is over a multi-year, 43-exchange, developed-and-emerging sample and is reported
**per exchange**, not only pooled, which is the robustness dimension that matters most for a
multi-region universe. The findings that survive that disaggregation:

- **Percent-cost proxies measured from daily data are far better than cost-per-volume proxies.**
  The best percent-cost proxy reaches an average cross-sectional correlation with percent effective
  spread around 0.8; the best cost-per-volume proxy reaches around 0.56 against lambda. Roughly the
  same ordering holds at the daily frequency. If a strategy needs a liquidity *number*, the
  spread-class number is the better-measured one by a wide margin.
- **The zero-return family is dominated, and by a lot.** Against percent effective spread, the
  raw Zeros proxy sits near 0.4 where the best proxy sits near 0.8, and LOT Mixed is roughly
  two-thirds of the way. FHT — the simplification — lands consistently in the top three percent-cost
  proxies on every dimension, so the simplification loses nothing relative to the model it
  simplifies.
- **Correlation and level are genuinely separate results.** The proxy that best *ranks* names is
  not always the one that best *matches the level*: on the RMSE tests, High-Low is significantly the
  closest to the level of percent realized spread and percent price impact, while a different proxy
  wins on effective and quoted spread. The paper's own summary of the pattern is blunt: the five
  best monthly cost-per-volume proxies (including Amihud) are all highly correlated with lambda and
  **none of them captures its level, at either frequency**.
- **Which proxy wins is exchange-dependent for the cost-per-volume class and not for the
  percent-cost class.** The best percent-cost proxy has the highest cross-sectional correlation on
  42 of 43 exchanges — near-total dominance. The cost-per-volume class fragments: across the 43
  exchanges the top slot is taken by five different proxies, and **Amihud wins on 2 of them**
  (it is the top or statistically indistinguishable from the top on 6). Amihud is nevertheless the
  best *daily* cost-per-volume proxy globally. So "Amihud is a good measure" and "Amihud is the
  best measure on your particular venue" are different claims and the second is usually false.
- **Predecessors and successors.** The paper is the global extension of Goyenko–Holden–Trzcinka
  (2009) and Lesmond (2005), and it is the source that has been carried on this folder's unread
  list — under the 2009 US paper's name — since 2026-08-29 and formally dropped on 2026-09-02.
  This is the international version of that horserace and it answers a different question than the
  one the drop was reasoning about; see *Related*.

## Implementability here

**Two proxies in this paper are buildable on this repo's data and neither has been tested.**
FHT needs only the close series (zero-return frequency plus non-zero-return volatility);
High-Low needs `aux["high"]` and `aux["low"]`. Both are **percent-cost** measures, which is the
class this paper says is far better measured from daily data, and — this is the part that matters
for this lab specifically — **neither contains volume at all**.

That last point is the interesting one. Every object `liquidity-volume` has screened here has had
volume in it, and the family's recurring failure mode in `learnings.md` has been the suspicion that
a volume-containing sort is partly a venue sort or a size sort in costume. A percent-cost proxy
sidesteps the entire question: it is a fraction of price, dimensionless, and it never touches a
share count or a currency unit. If a liquidity characteristic still ranks names usefully when the
volume is removed, the family's content is not a volume artifact; if it does not, that is a clean
negative that the volume-based screens could not deliver.

**A discriminating free prediction about the incumbent leg.** The lab's 2026-09-03 result is that
region-demeaning `ILLIQ` is worth a great deal, with the stated account that `ILLIQ`'s cross-region
*level* is set partly by the venue — and its own control was that the same operator does nothing or
hurts on the two **unit-free** legs. This paper supplies the general version of that account
(cost-per-volume proxies are correlated with lambda but do not capture its level) and therefore a
sharp prediction: **region-demeaning should help a percent-cost proxy materially less than it
helped `ILLIQ`**, because a percent-cost proxy is already unit-free. Measuring both the raw and the
region-demeaned version of FHT or High-Low costs one screen and either outcome is informative — if
region-demeaning helps a percent-cost proxy just as much, the lab's venue-unit account of #71 is
wrong and something else (a regional return premium, a survivorship artifact) is doing the work.

**Concrete adaptation.**
- FHT over a trailing quarter is the cheapest thing on this list: `sigma` from non-zero daily
  returns, `Zeros` as the zero-return fraction, one inverse-normal call. Rebalance monthly, sort
  cross-sectionally, take the long tail. It is a slow characteristic, so expect turnover in the
  1–2x range rather than the 13–19x the union books were paying.
- The paper's proxies are all estimated over a **window**, and it reports both monthly and weekly
  estimates as usable. A trailing-quarter window on this universe is comfortably inside that.
- Do **not** build the "Impact" versions (percent-cost divided by average volume) as a first
  attempt. They put volume back in, they are the class this paper says fails on level, and the lab
  has already screened the volume-functional question twice.

**Pitfalls.**
- **The zero-return count is contaminated on a multi-region panel.** This repo's close series is
  forward-filled across foreign holidays but its volume panel is not. A forward-filled close
  produces a *spurious* zero return, which FHT reads as illiquidity. The fix is free and already
  known here: use the volume panel's NaN pattern to identify non-trading days and exclude them from
  both the zero count and the day count before computing `Zeros`. Getting this wrong would make FHT
  a **holiday-calendar sort**, ranking the 15 regions by how many local holidays fall in the
  window — a textbook instance of this repo's own "check the statistic is invariant to the thing it
  is not supposed to measure" rule.
- Zero returns also arise from a price that simply did not move enough to clear the *tick*, and
  minimum tick size is a venue property. So FHT is not perfectly venue-free even though it is
  unit-free, and the region-demeaning prediction above is a prediction about *magnitude*, not about
  a zero.
- The paper's benchmarks are intraday and unavailable here, so none of its accuracy results can be
  reproduced on this universe. What transfers is the *ordering of proxies* and the
  correlation-versus-level distinction, not any number.
- This universe is ~145 large, liquid global names. `SUMMARY.md` #68's standing rule applies: an
  effect located in the illiquid tail is unreachable here. But note the rule cuts differently for a
  *measurement* claim than for a *premium* claim — this paper's finding is about how well a proxy
  measures, which does not require dispersion in the premium, only dispersion in liquidity.

## Related

- `notes/2026-09-04-high-low-spread-estimator.md` — the Corwin–Schultz estimator this paper grades,
  in full construction detail.
- `notes/2026-09-04-commonality-in-liquidity-across-countries.md` — an independent Tier 1 source
  stating in print that `ILLIQ` levels are not comparable across countries, which is the same
  finding as this paper's "none of them captures the level of lambda" arrived at from the other
  direction.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the replication cluster, and
  the horserace of Amihud against simpler same-input measures.
- `notes/2026-08-31-amihud-volume-component-decomposition.md` — Lou–Shu's decomposition, whose
  conclusion (the premium sits in the volume denominator, not the price-impact numerator) is
  complementary: this paper says the *measure* is weakest exactly in the cost-per-volume class.
- `SUMMARY.md`'s coverage log, 2026-08-29 through 2026-09-02: this source is the international
  successor to the Goyenko–Holden–Trzcinka horserace that was carried unread for four sessions and
  then dropped. The drop's reasoning — "a horserace of liquidity proxies cannot change a null
  measured on this universe" — was sound when `liquidity-volume` was closed twice on nulls. It no
  longer holds: the family reopened on 2026-09-03 through a *measurement* correction, and this is
  the measurement literature.

## Access note

Semantic Scholar's DOI endpoint returns "not found" for `10.1093/rof/rfx003`, a 400-plus-citation
Review of Finance article. That is a **sixth** instance of this folder's standing "disbelieve a
lone count" rule and the second journal family (after Journal of Finance and JFE) where the
Semantic Scholar DOI endpoint silently misses a well-cited paper. Crossref resolved it
immediately. The full text came from the authors' conference-version PDF on `cicfconf.org`, a
host not previously used here and worth trying for finance working papers whose publisher endpoint
is closed.
