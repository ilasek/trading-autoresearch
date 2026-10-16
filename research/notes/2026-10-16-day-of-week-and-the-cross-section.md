---
title: "Day of the week and the cross-section of returns (weekday mood as high-frequency sentiment)"
authors: Birru
year: 2018
venue: Journal of Financial Economics 130(1), 182–214 — venue tier 1
url: https://doi.org/10.1016/j.jfineco.2018.06.008
citations: 167 (Crossref `is-referenced-by-count`, checked 2026-10-16)
sample_period: July 1963 – December 2013
markets: US only — all NYSE/AMEX/NASDAQ common stocks (CRSP share codes 10, 11), with Compustat accounting data; plus VIX, CRSP Treasury fixed-term indexes, and two external Twitter-mood datasets
tier: B
validation_overlap: false
published_post_2018: true
read: full text of the author's December 2016 draft, served as a 1.4 MB PDF by the AEA 2017 conference paper archive (`aeaweb.org/conference/2017/preliminary/paper/fNkhhEd6`); `pdftotext -layout` → 219 KB of text, 820 instances of `" the "`, `( )`-dropout check zero. The published JFE version was not obtained; section numbering and table numbers below are the draft's. Tables are present in the extract but **no performance figure from them is recorded here**, per `research/README.md`'s anti-lookahead rule.
---

## Mechanism

Psychology finds that mood is low on Monday and high on Friday, and the paper's claim is that this
weekday mood cycle is a **high-frequency sentiment proxy** that moves the *relative* prices of
speculative and non-speculative stocks. Mood is treated as exogenous to fundamentals — which is the
methodological attraction, since separating sentiment from fundamentals is the hard part of the
sentiment literature — and the prediction is explicitly **cross-sectional**, not aggregate.

The classification step is where the content is. Each long-short anomaly is labelled by **which leg
holds the speculative stocks** — stocks that are hard to value and attractive to optimists: small,
young, unprofitable, volatile, non-dividend-paying, lottery-like, distressed, high-dispersion,
illiquid. Of the 19 anomalies examined, 16 have the speculative stocks on the **short** leg
(idiosyncratic volatility, MAX, nominal price, age, two distress measures, four profitability
measures, two payout measures, dispersion, cash-flow volatility, 52-week high, beta) and 3 have
them on the **long** leg (size, Amihud illiquidity, Corwin–Schultz bid-ask spread). The sign
prediction follows mechanically: on Monday (falling mood) the speculative leg underperforms, on
Friday (rising mood) it outperforms, so a long-short strategy's weekday pattern **must flip sign
with the location of its speculative leg**.

Why the aggregate and the cross-section can disagree, in the author's own words, is the part that
matters most for this lab: "changes in mood deliver clear cross-sectional predictions, but not
clear aggregate predictions", because a mood decline hits speculative stocks and simultaneously
produces a flight to quality that lifts safe ones. He notes that the *aggregate* weekend effect is
documented elsewhere as absent over most of his sample while his cross-sectional effect "holds in
all subperiods". A null on the index-level calendar effect is therefore **not** evidence against
the cross-sectional one; they are different predictions with different signs of aggregation.

## Construction recipe

- **Signal.** No new signal. Take any existing long-short characteristic sort, classify its
  speculative leg, and then **condition on the weekday of the return**, not on anything about the
  stock. The sort itself is unchanged; the calendar enters only as a partition of the return days.
- **Portfolios.** Decile long-short, formed in the conventional way for each anomaly; returns
  accumulated separately for Monday, Friday, and Tuesday-through-Thursday, then risk-adjusted with
  CAPM / three-factor / four-factor alphas. (For the size anomaly SMB is dropped from the factor
  model, and for the beta sort the market factor is dropped — a construction detail worth copying
  whenever a leg and a factor are the same object.)
- **The core test** is a two-point contrast: the long-short return on Monday against the same
  strategy's return on Friday, for each anomaly, with the sign predicted in advance from the leg
  classification.
- **The monotone version, which is the stronger test.** Twitter affect data (Golder–Macy, measured
  in the hour before the US close, with the Dodds et al. happiness index as external validation)
  shows mood *changes* increasing monotonically from Monday to Friday: Monday the largest decline,
  Tuesday roughly flat, then rising increments through Friday. That implies anomaly returns should
  be **monotone across all five weekdays** — decreasing Monday→Friday where the short leg is
  speculative, increasing where the long leg is. The paper tests and reports this monotone pattern
  for the vast majority of anomalies, which is a much harder prediction to satisfy by chance than
  the two-point contrast.
- **The leg decomposition, which is the identification.** Run the long leg and the short leg
  separately. A mispricing story requires the Friday-minus-Monday difference to sit in the
  **speculative** leg alone, and that is what is reported: for the 16 short-leg-speculative
  anomalies the short leg carries all the variation (and the single-leg difference is generally
  *larger* than the long-short portfolio's); for size, illiquidity and bid-ask the long leg carries
  it instead.
- **The holiday extension, built the same way.** Three mood-shifted day types, each defined purely
  from the exchange calendar: **Tuesdays following a Monday holiday** (depressed mood), **Thursdays
  preceding a Friday holiday** and the **Wednesday before Thanksgiving** (elevated mood, by
  anticipation). The prediction is that an ordinary Tuesday behaves more like a Monday and a
  pre-holiday Thursday/Wednesday more like a Friday — i.e. the mood label, not the weekday label,
  is what the cross-section responds to.
- **A built-in placebo, pre-specified.** From McLean–Pontiff's and Engelberg–McLean–Pontiff's
  anomaly lists, 44 further anomalies are selected *because* they have **no clearly speculative
  leg** — either neither leg is speculative (momentum is his example) or both are (book-to-market
  and sales growth, where one leg is extreme growth and the other distress). The prediction is a
  **null** for all 44, and the author's framing is that finding the weekday pattern there would
  refute the mood mechanism rather than extend it.
- **Independent, non-return corroboration.** VIX rises on Monday and falls on Friday, surviving
  controls for lagged VIX, lagged VIX², macro-announcement days (CPI, PPI, employment, FOMC) and
  year-month fixed effects; Treasury bond returns show the mirror-image pattern, consistent with a
  Monday flight to safety. These are the same prediction measured on instruments that are not the
  stocks being sorted.

## Robustness evidence (qualitative only)

- **Subperiod stability**: the cross-sectional effect is reported present in all subperiods, in
  explicit contrast to the aggregate weekend effect's documented disappearance. This is the
  strongest robustness claim in the paper and the one that distinguishes it from the calendar
  literature it grows out of.
- **Breadth across anomalies**: the sign prediction holds for all 19 anomalies on the
  Monday-versus-Friday contrast, 56 of 57 anomaly-by-day-type cells go the predicted way in the
  holiday tests, and the monotone-across-weekdays prediction holds for most anomalies. Consistency
  across many *pre-signed* tests is doing the work here, not the size of any one estimate.
- **Risk-premium alternative addressed directly**: because monthly factors are used to adjust
  returns measured on day subsets, the paper re-does the adjustment with factors decomposed into
  their Monday and Friday components; inferences are unchanged.
- **Mechanism measured independently of returns**: Twitter affect, a second happiness index, VIX,
  and Treasury returns all point the same way.
- **Gaps, and they matter for grading.** No transaction costs anywhere in the paper — the phrase
  does not appear, and a strategy that is long the speculative decile on Friday and short it on
  Monday is a full round trip per week per name. Single market (US), no international replication
  in the paper. No multiple-testing haircut, though the pre-signed, 19-anomaly, 5-weekday,
  3-holiday-type design is substantially self-protecting. Most of the 19 anomalies need Compustat
  fundamentals. `published_post_2018: true`, so `research/README.md`'s novelty discount applies.

## Implementability here

**The strategy is not implementable; the diagnostic is, and it is free.** The tradeable form of
this result is a two-day-per-week position in a decile portfolio — on this panel that is roughly 100
boundary crossings a year against `learnings.md`'s measured ~24-crossing monthly overlay already
costing 3.6%/yr of transition cost, with v3 charging 15–40 bps per side plus stamp duty on UK and
HK names. It is dead on arrival for the same reason as every other timing overlay here, only
~4× worse, and that arithmetic is already settled in the lab's own records. What survives is a set
of **measurements on return series the lab already stores**:

- **A weekday decomposition of every family lead's active return, with the sign pre-registered from
  the leg classification.** Five of the 19 anomalies are buildable on this repo's data —
  idiosyncratic volatility, MAX (`2026-09-01-max-lottery-extreme-positive-returns.md`), the 52-week
  high, trailing beta, and listing age (`2026-09-13-listing-age-as-a-level-effect.md`) — plus the
  two the lab has actually scouted leads in: **Amihud illiquidity**
  (`2026-08-29-amihud-illiquidity-measure-and-replication.md`) and the **Corwin–Schultz /
  high-low bid-ask spread** (`2026-09-04-high-low-spread-estimator.md`,
  `2026-10-05-chl-spread-estimator-close-high-low.md`). For the illiquidity and spread legs the
  predicted sign is **the opposite** of the other anomalies — their speculative leg is the long
  leg, so their edge should concentrate on **Friday**, not Monday. That is a genuinely falsifiable,
  zero-cost test of whether the lab's illiquidity lead is the mood-driven mispricing effect the
  literature describes or something else, and the opposite sign makes it hard to pass by accident.
- **It doubles as a tradeability screen, which is the use the lab should care about more.** A leg
  whose entire edge lives on one weekday cannot be harvested by a monthly rebalance, because a
  monthly book holds the name on all five. So this decomposition tells the lab something it has
  never checked about every seated and scouted leg: **how much of the measured skill is reachable at
  the rebalance cadence it is actually trading.** A leg that is flat across weekdays is the
  *good* outcome here.
- **The survivorship confound is severe for exactly these legs and must be stated in the
  hypothesis, not discovered after.** `learnings.md` [2026-08-29] measures a high-minus-low
  volatility spread of **+19.4%/yr on train** on this universe — the survivorship artifact observed
  directly — and [2026-09-17] concludes `beta-minus` is "the volatility level wearing a risk
  label". Birru's speculative axis *is* the volatility/illiquidity/low-price axis. A weekday
  decomposition is still informative (an artifact in the level has no reason to be concentrated on
  Fridays), but any *candidate* built from the speculative-leg classification would be sorting on
  the lab's most contaminated characteristic, and `2026-09-17-downside-beta-and-the-volatility-confound.md`
  is the precedent for what that produces.
- **The pre-holiday day types are derivable here, with one trap.** Pre- and post-holiday windows
  need a per-region trading calendar; the repo forward-fills closes across foreign holidays, so the
  close panel cannot see a closure, while the `volume` frame is NaN on those days and can. Build
  the calendar from the volume NaN blocks, and respect `learnings.md`'s caution that a vendor gap
  and a real closure are indistinguishable in that frame — fix a minimum-valid-observations rule
  per region before looking at any result.
- **The placebo design is the part to copy wholesale.** Selecting 44 anomalies *because* the
  mechanism predicts nothing for them, and reporting that as a result, is precisely the control
  `learnings.md` [2026-09-02] concluded the lab most needed and
  `2026-09-03-pairs-trading-distance-method.md` found in one other source. Any weekday
  decomposition the lab runs should include legs for which the mood story predicts a flat profile —
  momentum first, since the paper names it as its own placebo.

**What this note does not license.** No weekday-conditional book, no magnitude expectation, and no
claim that any named weekday effect exists on *this* panel. Its content is a leg-classification
rule, a pre-signed sign prediction, a monotone-across-weekdays version of it, a placebo set, and
the aggregate-versus-cross-section distinction that reconciles it with
`2026-10-16-calendar-effects-data-mining-robust-test.md`.

## Related

- `2026-10-16-calendar-effects-data-mining-robust-test.md` — the index-level counterpart. Hansen–
  Lunde–Nason cannot certify a Monday effect in index returns once the calendar universe is
  controlled for; Birru explains why that is compatible with a strong cross-sectional weekday
  effect, and the folder should hold both rather than treating either as the verdict on "weekday
  effects".
- `2026-10-16-mood-beta-and-seasonal-recurrence.md` — Hirshleifer–Jiang–Meng's model generalises
  this paper's weekday result into a single loading (mood beta) and predicts recurrence across
  congruent mood periods and reversal across non-congruent ones; Birru's Monday/Friday pair is
  their canonical non-congruent pair.
- `2026-09-01-max-lottery-extreme-positive-returns.md`,
  `2026-08-29-amihud-illiquidity-measure-and-replication.md`,
  `2026-09-04-high-low-spread-estimator.md`, `2026-10-05-chl-spread-estimator-close-high-low.md`,
  `2026-09-13-listing-age-as-a-level-effect.md` — the five legs of the nineteen that this repo can
  actually build, and hence the testable subset.
- `2026-09-17-downside-beta-and-the-volatility-confound.md`,
  `2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — why the speculative axis is
  the lab's most contaminated axis on this universe.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — the monotone-across-weekdays prediction
  is a monotonicity test with the calendar as the ordering variable, and the folder's existing note
  says what such a test does and does not establish.
- `2026-09-18-overnight-intraday-return-decomposition.md`, `2026-09-18-beta-at-night-versus-day.md`
  — the other partition of the daily bar the folder holds: there the session boundary, here the
  weekday. Both ask which slice of calendar time a measured premium actually lives in.
- `2026-10-04-sad-daylight-seasonal-mechanism.md`,
  `2026-10-05-sad-weather-exchange-and-the-integration-escape.md` — the mood-channel literature at
  the seasonal frequency, of which this is the weekly-frequency version.
- `2026-08-17-mclean-pontiff-publication-decay.md` — the source of the 97-anomaly list the 44
  placebo anomalies are drawn from.
