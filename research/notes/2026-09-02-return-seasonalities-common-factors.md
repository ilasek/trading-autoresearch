---
title: "Return Seasonalities — with its seasonal-reversals companion"
authors: Keloharju, Linnainmaa, Nyberg
year: 2016 (JF); 2021 (JFE companion)
venue: Journal of Finance (Tier 1); Journal of Financial Economics (Tier 1)
url: https://doi.org/10.1111/jofi.12398 — companion https://doi.org/10.1016/j.jfineco.2020.07.009
citations: 116 for the JF paper (Semantic Scholar by DOI, checked 2026-09-02); 24 for the JFE companion (Semantic Scholar by DOI, checked 2026-09-02)
sample_period: January 1963 – December 2011 (JF paper)
markets: NYSE/Amex/Nasdaq individual stocks; plus characteristic- and industry-sorted portfolios, 15 anomaly premiums, commodities, and a cross-section of country stock-market indexes
tier: A
validation_overlap: false
published_post_2018: false
---

The JF paper was read **in full** from its NBER working-paper version (`w20815`, circulated as
*Common Factors in Return Seasonalities*), which is the same paper under its earlier title. The
2021 JFE companion is recorded **from its published abstract only** (closed access; abstract read
from the Semantic Scholar record for the DOI) and is used for one structural claim it states
outright.

This note exists because `seasonality-calendar` is the thinnest family that is still live, it
holds the lab's strongest single leg by cross-sectional content (`learnings.md`, 2026-09-01: the
`seasonal` leg's decile-10 excess is the only one of four legs with reliable content), and the
folder's one previous note on it (Heston–Sadka) left the lab with a **failed identification** it
then argued past. This source is the direct successor to that literature and it supplies a better
identifying test.

## Mechanism

The claim is *not* that stocks repeat their own past shocks. It is that **expected returns vary
from calendar month to calendar month**, and that a sort on a stock's own historical
same-calendar-month returns is a **noisy proxy for a bundle of characteristics whose premiums are
seasonal**.

The authors' identification for this is a fixed-effects contrast, and it is the sharp part of the
paper: the annual-lag pattern appears in pooled regressions with **stock fixed effects**, and it
**disappears once the regressions include stock-calendar-month fixed effects**. That is what rules
out "stocks repeat shocks" and rules in "each stock has its own twelve monthly expected returns".

The economic content follows from that. Suppose small stocks tend to outperform large ones in a
particular month. Then a firm's historical returns in that month are a noisy signal of its size,
and a sort on past same-month returns predicts future same-month returns *because it correlates
with size*. Generalise across characteristics: a sort on past same-calendar-month returns picks up
every seasonality regardless of origin, because it is equivalent to regressing returns on a noisy
combination of all the attributes whose premiums are seasonal. Individual stocks **aggregate**
seasonalities across factors; that is why the effect looks strong in single names and weak in any
one factor.

Three structural consequences the lab should carry:

- **The seasonal component dominates the unconditional one.** The authors state that in terms of
  extracting expected-return information from historical returns, the seasonal component
  overwhelms the unconditional cross-sectional component. Their sharpest version of this is at the
  anomaly level: a meta-strategy selecting among 15 anomalies on their historical *same*-month
  premiums is strongly profitable, while selecting on their *other*-month premiums is not — knowing
  how an anomaly does in other calendar months is uninformative about this month.
- **At least two-thirds of the seasonality comes from common factors**, identified by a variance
  test: the seasonality strategy's variance is about five times what it would be if it bore only
  idiosyncratic risk. Size, dividend-to-price and industry are named as the biggest contributors.
  The authors draw the operational conclusion themselves: **seasonal strategies must stay exposed
  to systematic risk, because hedging that exposure removes the seasonality with it.**
- **Different seasonality strategies are only weakly correlated with each other.** Within US
  equities the small-stock and high-dividend-yield seasonality strategies correlate about 0.17;
  correlations weaken as the assets become less alike and are negligible across asset classes
  (country indexes and commodities are unrelated to US equities), and daily-frequency seasonality
  is uncorrelated with monthly.

The 2021 companion revises the risk framing from the same authors: it reports **seasonal
reversals** — a stock with elevated expected return in one month has depressed expected returns in
other months, and the pattern **sums to approximately zero over the calendar year**. Their reading
is temporary mispricing rather than risk. Recorded as a tension inside the cluster rather than
resolved: the 2016 paper argues the seasonalities are factor-borne and unhedgeable, the 2021 one
argues they net out annually and look like mispricing.

## Construction recipe

- **Signal**: for each stock and each month, the **average of that stock's returns in the same
  calendar month over the prior 20 years**. Cross-sectionally demean returns before averaging
  (the authors demean in the cross section throughout, because stocks differ in how much history
  they have).
- **Sort**: deciles on that average; long the top decile, short the bottom. Monthly formation,
  one-month holding period — the signal is month-specific, so it must be re-formed every month.
- **The portfolio-level variant matters more here than the stock-level one.** The authors show
  that seasonality strategies trading **well-diversified portfolios formed on characteristics such
  as size and industry** are about as profitable as those trading individual stocks, and they
  replicate the annual-lag pattern on the returns of 58 characteristic-sorted portfolios: the
  average coefficient is positive at every annual lag out to 20 years, with 19 of 20 at |t| ≥ 2.
- **Same-versus-other-month is the identifying contrast**, run at the level of whatever assets are
  being sorted: rank on the same calendar month's history, and separately on the other eleven
  months' history over the same window. The result that identifies a seasonal is that the
  same-month sort carries the information and the other-month sort does not.
- **Do not neutralise the systematic exposure.** Per the variance decomposition above, the
  factor exposure is the effect's carrier, not a nuisance.
- **Execution overlay, as a zero-turnover alternative**: delay a sale whenever the strategy calls
  for selling a stock whose seasonal predicts a high expected return next month. This adds no
  turnover — it re-times turnover that was going to happen anyway.

## Robustness evidence (qualitative only)

Multi-decade US sample. The pattern is present at every annual lag out to twenty years at both
stock and portfolio level. The authors emphasise **pervasiveness**: unlike many anomalies that
falter in particular corners of the market, seasonalities vary little from one set of stocks to
another, and — unlike every anomaly in the Stambaugh–Yu–Yuan sentiment study — are about equally
strong in high- and low-sentiment periods. The effect is documented outside US single stocks in
anomaly premiums, commodities, country indexes, and at daily frequency. Heston–Sadka's
international companion (this folder's 2026-08-29 note) is the cross-market evidence for the
stock-level version. The authors find **no measurable link to macroeconomic risks** under the
Chordia–Shivakumar and Liu–Zhang variables and methods, and do not claim a risk explanation
beyond "many factors with seasonal premiums". The 2021 companion's reversal result cuts against
the risk reading from the same authors, which is a live disagreement rather than settled
knowledge.

## Implementability here

**Reachable, and this is the note's main content: it says the lab has been testing the wrong
object.**

1. **The lab's failed pre-registered screen was the wrong screen, and this source supplies the
   right one.** On 2026-08-29 the lab pre-registered Heston–Sadka's *sign disagreement* (annual
   lags positive, non-annual negative) and it failed on this universe — annual +15.7%/yr
   (t = +5.16) and non-annual **+12.8%/yr (t = +3.70)**, both positive — so the session concluded
   the contrast separating a calendar seasonal from persistent cross-sectional mean-return
   differences was "absent here", and argued past it. **This source predicts that failure.** Its
   whole thesis is that the seasonal component *overwhelms* the unconditional component rather
   than opposing it in sign; a positive non-annual coefficient is what a universe of 140 names
   with large persistent mean-return differences should produce, and it does not by itself deny a
   seasonal. The identifying test that does discriminate is **stock fixed effects versus
   stock-calendar-month fixed effects**, or equivalently the **same-month versus other-month sort
   run on the same assets over the same window**. Both are free panel computations on train, and
   neither costs a trial.
2. **The 20-year lookback is a real obstacle and should be checked before anything else.** The
   recipe wants 20 prior observations of each calendar month. The lab's existing
   `seasonal_same_month_return` uses a much shorter window; the store's history bounds how many
   annual lags are available for the newest instruments, and warmup shortens the eligible universe
   exactly the way `learnings.md` has already recorded for other long-lookback constructions. Count
   the available annual lags per instrument first — the honest version of this signal may not fit,
   and that is a finding.
3. **The portfolio-level variant is the one that fits this universe, and it is the strongest
   suggestion in this note.** The authors show seasonality in the cross section of **country
   indexes** and in characteristic-sorted portfolios, about as strongly as in single stocks. This
   repo has **42 ETFs across 15 regions** — country and sector sleeves are exactly the diversified
   portfolios the paper says work. An ETF-only seasonal sort also sidesteps the survivorship bias
   that `program.md` warns inflates single-stock results, and it addresses the note's own worry
   about single-name seasonality on a survivorship-conditioned universe.
4. **Turnover is the binding constraint and the folder has already priced it.** The signal
   re-forms every month and rotates the whole book; the lab measured 17.1x turnover (~2.6%/yr) on
   its existing seasonal scout, and Heston–Sadka's own conclusion was that round-trip costs may
   swallow a gain of this size. The execution-overlay form is the cost-free alternative and remains
   untested here.
5. **The 0.17-style low correlation across seasonality strategies is directly useful to the live
   `portfolio-learning` result.** The lab's 2026-09-01 finding is that legs earn their place by
   **timing independence, not signal** — four legs at cross-sectional |rho| 0.054–0.070 build a
   book better than any leg alone. This source says seasonality strategies **in different corners
   of the market are near-uncorrelated with each other**, and negligibly correlated across asset
   classes. That is a principled source of the "fifth maximally orthogonal leg" the lab's
   prospective test needs: a **country-index seasonal** should be close to unrelated to the
   existing US-heavy single-name seasonal, by the source's own measurement rather than by hope.
6. **Do not carry the risk framing into a hedging decision without noting the 2021 reversal
   result.** If seasonalities net to zero over the calendar year, then a long-only book that is
   seasonally tilted every month is buying and selling the same names around the year, and the
   annual net is the thing to measure. This is checkable for free and it bears on whether the
   signal is worth its turnover at all.

**Pitfall specific to this lab.** `learnings.md`'s 2026-08-29 entry records that the lib's
`seasonal_same_month_return` traded one month late, and that correcting the alignment turned a
null into a large positive. A month-indexed signal is exactly the construction where an off-by-one
is invisible and decisive. Any new seasonal candidate should re-verify the alignment against the
corrected helper rather than assume it.

## Related

- `notes/2026-08-29-same-calendar-month-seasonality.md` — Heston–Sadka, the direct predecessor.
  This note **supersedes its identifying test**: the sign-disagreement screen the lab
  pre-registered from it is not the discriminating contrast, and its failure on this universe was
  over-read. The execution-overlay suggestion is common to both sources and is corroborated here.
- `experiments/learnings.md` 2026-08-29 (failed pre-registered screen; the `MonthEnd`/`MonthBegin`
  alignment bug) and 2026-09-01 (legs add timing independence, not signal; the seasonal leg is the
  only one with reliable cross-sectional content).
- `experiments/learnings.md` 2026-09-01 — the structural closure of the **calendar** half of this
  family. That closure is about time-series timing overlays against cash and does not touch the
  cross-sectional object in this note, which is always fully invested.
- `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` — for the correlation argument in
  point 5.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the reason point 3
  prefers the ETF-level variant.
