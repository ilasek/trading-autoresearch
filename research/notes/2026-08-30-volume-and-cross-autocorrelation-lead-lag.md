---
title: "Trading Volume and Cross-Autocorrelations in Stock Returns"
authors: Chordia, Swaminathan
year: 2000
venue: Journal of Finance (Tier 1)
url: https://doi.org/10.1111/0022-1082.00231
citations: 662 (OpenAlex, DOI:10.1111/0022-1082.00231, checked 2026-08-30). Semantic Scholar's DOI record returns 117 for the same paper and appears to be a split/duplicate record; OpenAlex is the count used here.
sample_period: 1963–1996 (analyst-matched subsample 1976/1977–1996)
markets: US, NYSE/AMEX common stocks, daily and weekly frequency
tier: A
validation_overlap: false
published_post_2018: false
---

Typeset article read in full from a university course-reading mirror
(`cis.upenn.edu/~mkearns/finread/Chordia_lead_lag.pdf`).

Second note on `lead-lag-spillover`. Where
`notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` supplies the mechanism and the
multiple-testing discipline at a monthly horizon, this one supplies the *sorting variable*
and a per-instrument statistic, at the daily/weekly horizon — and a blunt cost caveat from
the authors.

## Mechanism

**Differential speed of adjustment to common information.** Some stocks incorporate
market-wide news into price quickly; others do so with a lag. Where that is true, the fast
group's return today predicts the slow group's return tomorrow, mechanically, without any
firm-specific information advantage. The paper's contribution is that **trading volume is
what separates fast from slow**, over and above firm size.

The paper is careful to distinguish this from the three rival accounts of the same
statistical pattern, and this taxonomy is the useful part:

1. *Time-varying expected returns* — cross-autocorrelation is a restatement of portfolio
   autocorrelation and contemporaneous correlation, with nothing extra in it.
2. *Microstructure* — non-synchronous or thin trading manufactures the lag.
3. *Speed of adjustment* — the slow group genuinely underreacts to common news.

These are separated empirically by (a) controlling for the follower's own lags, (b)
controlling for size and screening out non-trading, and (c) asymmetry: fast→slow prediction
must be stronger than slow→fast. Only (3) predicts the asymmetry. The paper finds the
asymmetry survives inside the *largest* size quartile and in the later half of the sample,
which is what rules out thin trading as the whole story.

An important second-order point the paper makes about diagnostics: **own-autocorrelation is
not a valid speed-of-adjustment measure.** A stock that responds to today's *and*
yesterday's market news shows positive own-autocorrelation while being the faster adjuster;
a stock that responds only to yesterday's shows zero. Cross-autocorrelation does not have
this defect. Any screen this lab builds for "who is slow" must therefore be a
cross-quantity, not an own-lag quantity.

Why it is not arbitraged away: the authors say plainly that it probably is not tradeable —
transaction costs at these horizons are likely to overwhelm the profits. They present the
result as evidence about how prices become informationally efficient, **not** as a strategy.
Take that at face value; it is the same structural objection this lab has already recorded
against short-horizon reversal.

## Construction recipe

**Sorting.**
- Volume is measured as **turnover** — shares traded per day divided by shares outstanding —
  averaged over the *previous* year. This choice is deliberate and load-bearing: in their
  sample, raw share volume correlates ≈0.78 with firm size and dollar volume similarly,
  while **turnover correlates only ≈0.15 with size and ≈0.60 with raw volume**. Turnover is
  the part of volume that is not a size ranking.
- Double sort, annually: four size quartiles, then four turnover quartiles within each size
  quartile → 16 portfolios. Composition frozen for the remainder of the year (so the sort
  itself contributes no turnover). Equal-weighted portfolio returns.
- Screens: ordinary common shares only; closed-end funds, REITs, ADRs and trust components
  excluded; a stock must have ≥90 daily volume observations in the previous year; and
  returns of stocks that did not trade at *t* or *t−1* are dropped from the portfolio return
  at *t*, which removes two-consecutive-day non-trading from the lead-lag estimate.
- Weekly returns measured Wednesday close to Wednesday close; results replicate with Tuesday
  and Friday week-ends, which is their check against weekday-autocorrelation seasonality.

**Testing the lead-lag.**
- Bivariate VAR on a pair of portfolios *within the same size quartile* — high turnover and
  low turnover — with own lags of both included, plus Granger-causality tests in both
  directions. The claim is the *asymmetry* of the two directions, not the significance of
  one of them.
- Dimson (1979) market-model regressions on a zero-investment portfolio that is long the
  high-turnover and short the low-turnover portfolio of the same size, regressed on
  contemporaneous market return plus leads and lags (four lags/leads daily, two weekly).
  Loading on *lagged* market returns is the signature of delayed adjustment.

**The per-instrument statistic worth stealing.** From a Dimson regression of instrument *i*
on the market with five leads and five lags, define

    x_i     = ( Σ_{k=1..5} β_{i,k} ) / β_{i,0}
    DELAY_i = 1 / (1 + e^{−x_i})            # logit, in (0,1)

Higher `DELAY` = slower adjustment. The logit is not decoration: the raw ratio is
non-monotonic and behaves badly for large stocks, whose contemporaneous beta exceeds one and
whose lagged betas go negative, so `x` is often negative there; the transformation is
monotonic in `x`, bounds the statistic, and damps outliers. It is computed from **closes
only** — no volume needed — which makes it free here.

Matching `DELAY` in year *t* against characteristics in year *t−1*, high-`DELAY` names have
materially lower raw volume and lower turnover than low-`DELAY` names of the same size
quartile (the size-quartile-4 exception is attributed to Dimson estimation noise where
adjustment is fast for everyone). High-`DELAY` names are also smaller, followed by fewer
analysts, higher priced, and *lower* volatility; bid-ask spread differences across the two
groups are not economically meaningful. The authors show the result is not driven by the
extreme illiquid tail by reporting volume percentiles inside the slowest portfolio.

## Robustness evidence (qualitative only)

- Holds at both daily and weekly frequency, and to three different weekday definitions of a
  week.
- Holds within the largest size quartile — the case where non-trading cannot be the
  explanation — and in the later subperiod.
- Survives controlling for the follower's own autocorrelation, which is what separates it
  from the "cross-autocorrelation is just portfolio autocorrelation" account.
- Two independent methods (VAR/Granger and Dimson leads-and-lags) give the same direction,
  and a third, characteristic-level test on individual stocks agrees.
- Single market, single (long) sample. No independent replication is recorded in this note;
  the paper is heavily cited but this folder has not verified a formal replication.
- **The authors' own verdict on tradeability is negative**, on cost grounds, and they offer
  it as the explanation for why the effect persists.
- Incidental level result, consistent with the folder's liquidity material: within their
  sample there is a *negative* cross-sectional relation between trading volume and average
  return — high-volume names earn less. Not the paper's subject, and not a claim it tests
  carefully, but it points the same way as the illiquidity-premium literature.

## Implementability here

**The sorting variable is not directly available, and this is the first thing to solve.**
This repo receives `volume` (share count, native units, not forward-filled) and
`dollar_volume`, but **not shares outstanding**, so turnover as defined here cannot be
computed. Substituting raw or dollar volume reintroduces exactly the ≈0.78 correlation with
size that the paper's design exists to remove — and the lab has already measured the
consequence of that on this universe: log average dollar volume behaves as a pure size
ranking here and screens as a clean null. Two workable substitutes, both causal and cheap:

- **Relative volume (volume shock):** each name's volume divided by its own trailing average
  (e.g. 10–60 trading days). This is a within-name normalisation, so the size level cancels
  by construction, the same job turnover does. It is a *time-series* rather than
  *cross-sectional* normalisation, so it measures "unusually active for this name" rather
  than "actively traded relative to its float" — a related but not identical quantity. Say
  which one the hypothesis is about.
- **`DELAY` itself as the sort.** The Dimson statistic above needs only closes, sidesteps
  the missing-float problem entirely, and is the paper's own measure of the thing the volume
  sort is a proxy *for*. If the mechanism is speed of adjustment, sorting on the direct
  measure is strictly closer to the hypothesis than sorting on its proxy. Estimate it
  walk-forward on a rolling window (annual re-estimation matches the paper) against an
  equal-weighted universe return as the "market"; NaNs on foreign holidays must be handled
  explicitly since the panel is global and unsynchronised.

**Horizon versus the cost model — the binding constraint.** The effect here is daily and
weekly. This engine imposes a one-day execution lag, so a signal formed on day *t*'s close
is traded at day *t+1*'s close: for a daily lead-lag, that is most of the effect gone. The
weekly version survives the lag far better and is the only version worth a trial. Even then,
15 bps per side is roughly triple the friction the practitioner statistical-arbitrage
literature assumes at this horizon, and the paper's authors already expect costs to
dominate. `learnings.md` records the same wall from the reversal side: the strongest signal
measurable on this universe sits exactly at the horizon the cost model forbids. **A daily
lead-lag candidate should not be run without first showing, on the train split, that the
signal has a weekly-or-slower component.**

**Cross-instrument non-synchronicity is a confound here in a way it is not in the source.**
This universe spans 15 regions with non-overlapping trading sessions and USD conversion of
unhedged foreign prices. Asia closing before the US guarantees a mechanical "US leads Asia"
cross-autocorrelation at the daily frequency that has nothing to do with speed of
adjustment. The paper's own screens (drop returns where the instrument did not trade at *t*
or *t−1*; move to weekly) are the right templates, and the weekly frequency is the cleaner
of the two. Any daily region-level lead-lag result on this universe should be assumed to be
a time-zone artifact until a weekly version reproduces it.

**Where it could still pay.** The honest case is not "trade the daily lead-lag" but "use
`DELAY` or relative volume as a *conditioning* variable" — the mechanism says slow names
underreact to common news, which is a statement about *which names* a market-wide move has
not yet been priced into. That is a monthly-rebalanced cross-sectional tilt built from a
daily-frequency statistic, which is the shape this engine's cost model can actually carry.

**Pitfalls.** (a) `DELAY` estimated on 5 leads and 5 lags from a short window is noisy;
the paper re-estimates annually on a full year of daily data. (b) High-`DELAY` names in the
source are *lower* volatility and smaller — on this survivorship-conditioned universe of
large global names, a `DELAY` sort risks collapsing into a low-vol tilt, which this lab has
refuted twice and re-refuted with a range estimator. Check the overlap before running it.
(c) Volume is not forward-filled and is NaN on foreign holidays; a trailing-average
denominator must skip rather than zero-fill those, or the shock measure spikes on calendars
rather than on information.

## Related

- `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md` — the monthly-horizon,
  group-level version of the same family, with the fundamentals screen and the
  count-against-chance discipline.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — Lo–MacKinlay (1990) is
  the direct antecedent of this paper, and the cost objection is the same one.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the other place in this
  folder where a volume-based measure's correlation with size decides whether it carries
  information; the turnover-versus-raw-volume distinction here is that finding's mechanism.
- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` — uses volume in a
  different way (rescaling returns into trading time) for a related short-horizon purpose.
- `experiments/learnings.md` — the measured null on log average dollar volume in this
  universe, and the standing turnover-dominates-mechanism warning.
