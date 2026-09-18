---
title: "A tug of war: Overnight versus intraday expected returns"
authors: Lou, Polk, Skouras
year: 2019
venue: Journal of Financial Economics 134(1), 192–213 (Tier 1)
url: https://doi.org/10.1016/j.jfineco.2019.03.011 (read in full at https://personal.lse.ac.uk/polk/research/TugOfWar.pdf)
citations: 235 (Semantic Scholar by DOI, checked 2026-09-18)
sample_period: 1993–2013 (US, constrained by TAQ availability); nine non-US markets in the appendix replication
markets: CRSP-Compustat US common stocks excluding microcaps (price < $5 and/or bottom NYSE size quintile dropped); replication in Canada, France, Germany, Italy, United Kingdom, Australia, Hong Kong, Japan, South Africa (Thomson Reuters Tick History)
tier: A
validation_overlap: false
published_post_2018: true
---

**Why this note exists.** A grep across all 106 prior notes in this folder returns **zero** hits for
`overnight`, `intraday decomposition`, `tug of war`, `close-to-open` or any of the five authors
central to this literature, while `program.md` has passed strategies an **`open`** panel since
2026-08-29 and `experiments/learnings.md` (2026-08-30) records a nightly that computed overnight
return sums and screened them. The lab has been using the object without a note on it. This is the
2026-09-13 detector applied to the one panel column nobody wrote down.

## Mechanism

**The primitive.** A close-to-close daily return factors exactly into two pieces: the **overnight**
(close → next open) and the **intraday** (open → close) return. The paper's claim is that these two
pieces are not two noisy measurements of one thing — they are the footprints of two different sets of
traders, because who is in the market differs systematically between the open and the rest of the
session.

**The clientele story.** Some investors prefer to transact at or near the open (in the paper's
evidence: smaller trades, retail-linked order flow, and flow reacting to news released while the
market was shut); others transact through the day and especially into the close (larger trades,
institution-linked, execution systems that deliberately avoid the open's volatility). If a clientele's
order flow is persistent, then a stock that is pushed up overnight by one clientele's demand tends to
be pushed up overnight again next period — and the part of that push that was not information must
eventually revert, most plausibly in the *other* period, when the opposing clientele dominates. So the
signature of a clientele tug of war is a **pair** of effects:

1. **Own-period continuation.** Past overnight returns positively forecast future overnight returns;
   past intraday returns positively forecast future intraday returns.
2. **Cross-period reversal.** Past overnight returns *negatively* forecast future intraday returns,
   and vice versa.

Both are strong in the data, both hold in every one of the nine non-US markets tested, and — the fact
that makes this hard to dismiss as microstructure noise — **both are still measurable when the signal
is lagged by as much as five years.** A bid-ask bounce or a stale-quote artifact does not survive a
60-month lag. The authors are explicit that the mechanism has no formal risk model behind it; the
limits-to-arbitrage sketch in their Internet Appendix (built on Gromb–Vayanos) motivates the timing
variable below but is not a pricing theory.

**The second, larger finding — when a known premium is actually earned.** They decompose the returns
of 14 standard characteristic strategies into overnight and intraday components and find the split is
almost never even. Two groups, cleanly separated:

- **Premium earned overnight:** price momentum, industry momentum, earnings momentum, time-series
  momentum, and short-term reversal. *Every past-return-based strategy is an overnight strategy.*
- **Premium earned intraday:** size, value, profitability, investment, market beta, idiosyncratic
  volatility, equity issuance, discretionary accruals, share turnover. *Everything else.*

And for each strategy with a significant intraday premium, the **overnight** component carries an
economically significant premium of the *opposite* sign — so the side of the trade that looks riskier
(high beta, high idiosyncratic volatility, high turnover) is *paid* overnight and *punished* intraday.
The authors' own reading: these classic anomalies are primarily **intraday** anomalies, and their
overnight halves look more like what a risk story would predict. Their honest caveat is that they
cannot map this to a formal model of risk.

## Construction recipe

**Decomposing the bar — and this is the part worth copying exactly.** They do *not* compute the
overnight return directly as `open_t / close_{t−1} − 1`. They compute the intraday leg from same-day
prices and **impute** the overnight leg as the residual:

    r_intraday,s   = P_close,s / P_open,s − 1
    r_overnight,s  = (1 + r_close-to-close,s) / (1 + r_intraday,s) − 1

so that by construction `(1 + r_overnight)(1 + r_intraday) = (1 + r_close-to-close)` exactly. The
assumption this buys is stated plainly: **all dividend adjustments, splits and other mechanical price
events are assigned to the overnight period.** They verified it by re-running with dividend months
excluded and report no material change. Monthly components are the within-month products of the daily
ones, and they multiply to the standard monthly return.

**The open price itself.** Their headline measure is the volume-weighted average price over the first
half hour (9:30–10:00), chosen for robustness against a thin opening print, and they drop observations
with fewer than 1,000 shares traded in that window. They report that results are robust to three
plainer alternatives: **the CRSP opening price**, the first TAQ trade price, and the quote midpoint at
the open. A daily-bar `open` field is therefore an acceptable proxy by the paper's own robustness
check — this is what makes the mechanism reachable at all in a repo with no intraday data.

**Missing opens.** If day `s` has no open, they hold the overnight position from the day `s−1` close
to the *next available* open, so the components still aggregate to the realised close-to-close return.

**Sorts.** Monthly rebalance, deciles on the prior month's cumulative overnight (or intraday)
component, value-weighted, microcaps excluded. Longer-horizon versions use an **exponentially weighted
moving average of the monthly components with a 60-month half-life, skipping the most recent month**
(`EWMA_NIGHT`, `EWMA_DAY`) — the skip is there specifically so the long-horizon result cannot be the
one-month result repackaged.

**The timing variable (`TugOfWar`).** For a strategy `s`, EWMA its overnight and intraday component
returns (half-life 60 months) and take the spread, oriented so that a high value always means "the
period in which this strategy earns its premium has been unusually strong lately":

    TugOfWar_s,t = EWMA(r_overnight,s) − EWMA(r_intraday,s)   for overnight strategies
    TugOfWar_s,t = EWMA(r_intraday,s) − EWMA(r_overnight,s)   for intraday strategies

The prediction is a positive slope forecasting the strategy's subsequent **close-to-close** return.
They control for the EWMA of the strategy's own past close-to-close return, its return volatility, the
lagged 12-month market return, market volatility, the characteristic spread between the legs, and the
short-interest difference between the legs — i.e. the timing claim is made *net* of the obvious
alternative timing variables, including the strategy's own past total return.

## Robustness evidence (qualitative only)

- **Multi-market.** The one-month overnight continuation, the one-month intraday continuation and the
  cross-period reversal appear in **every one of the nine non-US markets** tested, with the reversal
  roughly equal in absolute magnitude to the continuation. The long-horizon EWMA versions are also
  significant across those markets.
- **Persistence.** Significance of the four firm-level sorts survives lagging the signal out to five
  years. This is the paper's strongest defence against a microstructure explanation and is the reason
  to treat the decomposition as an economic object rather than a data artifact.
- **Not news.** The decomposition results are not attributable to macroeconomic or firm-specific news
  announcements; the earnings-announcement channel is examined separately.
- **Not an open-price definition artifact.** Robust to four different open-price constructions
  (half-hour VWAP, CRSP open, first trade, quote midpoint) and to dropping small caps entirely.
- **Costs are not modelled in the headline results, and the authors say so.** Their own statement about
  what a long-horizon investor gets from the paper is worth quoting in substance: not a new book, but
  **order timing** — trade at the open or the close depending on which period your strategy's premium
  accrues in. They speculate that high-frequency exploitation *may* survive costs "for execution-savvy
  short-term investors", which is an admission that it may not for anyone else.
- **Replication status.** No Hou–Xue–Zhang / Jensen–Kelly–Pedersen row exists for this, because it is
  a decomposition of existing anomalies rather than a new characteristic sort. The nine-market
  appendix is the replication evidence, and it is the authors' own.

## Implementability here

**Read this section before proposing anything.** The honest summary is that the *headline* mechanism
is **not tradeable in this repo**, one specific corollary is, and the gap between those two statements
is where a trial would be wasted.

**1. The engine holds close-to-close. The effect is a decomposition of close-to-close into two
offsetting halves.** A candidate returns target weights; the engine forward-fills, applies a one-day
execution lag and costs, and the position is held across both the night and the day. The paper's
firm-level result is that past overnight winners earn *positive* overnight and *negative* intraday
returns going forward — so a 24-hour holder collects the sum of a positive and a negative term. There
is no way to express "hold overnight only" in the strategy contract, and any proposal that needs to
trade at the open is out of scope, full stop.

**2. The lab has already measured the naive version, and it lost.** `experiments/learnings.md`
(2026-08-30, `range-variance`) records that "the overnight/intraday decomposition loses to not
decomposing" — trailing 63-day overnight sums produced a weaker Q5-universe spread than the plain
trailing 63-day *total* return, with a null IC throughout. **That result is exactly what this paper
predicts**, and it should be read as a confirmation rather than a refutation: a 63-day overnight sum
used to predict close-to-close returns is collecting the continuation term and the cross-period
reversal term at once, and they offset. The nightly screened the construction the paper says will not
work close-to-close. It did not screen the constructions below. *(Noting the agreement is the point;
it is not a licence to re-run the same screen.)*

**3. What is actually reachable.** Three shapes, in descending order of how much this note is willing
to stand behind them:

- **(a) Signal hygiene, free, no trial.** The paper's strategy decomposition says *which component a
  characteristic's information lives in*. Past-return signals (momentum, reversal) are overnight
  objects; risk-level and turnover signals are intraday objects. The corresponding measurement move is
  to compute an existing signal on the component it lives in rather than on the close-to-close return
  — e.g. a reversal score from intraday returns only, or a volatility estimate from open-to-close
  returns only (which drops overnight gaps and is a different estimator from anything in
  `notes/2026-08-29-range-based-volatility-estimators.md`). The **book is still held close-to-close**;
  only the signal changes. This is the one family of ideas the decomposition genuinely opens here.
- **(b) The overnight share as a characteristic.** The fraction of a name's trailing total return
  earned overnight is a clientele-tilt proxy, and the natural long-only leg is the *low* end. This is
  the same object Aboody et al. sort on — see
  `notes/2026-09-18-overnight-return-as-firm-sentiment.md`, which has the tradeable horizon and the
  long-only orientation, and is the note to build from. **Do not build the candidate from this note.**
- **(c) `TugOfWar` as a timing variable — do not propose it.** See the tension section below.

**4. Data pitfalls specific to this universe, and two of them can silently produce nonsense.**

- **Verify the `open` panel is on the same adjusted, USD-converted basis as `prices` before anything
  else.** `CLAUDE.md` documents `prices` as USD-adjusted closes and `aux["open"]` merely as a frame on
  the same index and columns; it does not say the open is FX-converted or split-adjusted. If it is not,
  `close/open − 1` is not an intraday return but a currency or split *level*, off by orders of
  magnitude. The 2026-08-30 nightly evidently got plausible numbers out of the panels, so they are
  presumably consistent — confirm it anyway with a one-line magnitude check (the cross-sectional
  distribution of `close/open − 1` should look like a daily return, not like an exchange rate).
- **Prefer the paper's imputation to the direct ratio.** Computing `r_intraday = close/open − 1` from
  the same day's two prices and backing out the overnight leg from the (already correct) adjusted
  close-to-close return is robust to the dividend/split adjustment convention and to any same-day
  scaling that is common to both prices. The direct `open_t / close_{t−1} − 1` is not, and it is the
  construction that breaks on ex-dates. *(Aboody et al. use the direct form, with CRSP prices adjusted
  for splits and dividends. Two published conventions; this repo should use the imputed one.)*
- **Forward-filled closes across foreign holidays are a landmine.** This universe spans 15 regions on
  one calendar. On a day when a foreign market is shut, a forward-filled close paired with a stale or
  missing open manufactures a spurious "overnight" return of exactly the wrong kind — the same
  non-synchronous-trading problem already documented in
  `notes/2026-09-08-nonsynchronous-trading-econometrics.md`, now applied inside the day. Any
  implementation must mask days where the instrument did not trade, and the volume panel (not
  forward-filled, NaN on foreign holidays per `CLAUDE.md`) is the available mask.
- **"Overnight" is local, not global.** For a Tokyo-listed name the close-to-open window is the
  Tokyo night, which overlaps the US trading day. The clientele story is about *who trades at a local
  open*, so it survives; but nothing in the paper licenses comparing a Japanese name's overnight
  return with a US name's overnight return as if they were the same period. A candidate that sorts
  across regions on this characteristic is implicitly making that comparison. Region-demeaning is the
  obvious defence — and the lab's one recent measurement win (`lv_illiq_region_relative`) is a region
  demean, so the machinery exists (`notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md`).
- **Universe mismatch.** The paper excludes microcaps and value-weights. This universe is ~145 large,
  current, surviving global names — nearer their large-cap subsample than their full sample, which is
  the *favourable* direction for once, and the paper reports the effect holds excluding small caps.

## Tensions with this lab's own results — stated, not smoothed over

1. **`TugOfWar` is a timing rule on a strategy's own past component returns, and the lab killed the
   nearest sibling of that object last night.** The 2026-09-17 nightly built a pre-registered pair of
   sleeve books differing only in whether a sleeve is dropped when its own demeaned trailing 12-month
   return is negative; the timed book lost to its own untimed control on validation, with cost ruled
   out as the explanation, and the journal's own next-ideas list says *do not propose a second
   factor-momentum variant*. `TugOfWar` times the same kind of book on a **decomposed** version of the
   same past return. It is a different signal, but it is the same *operation*, and the standing
   benchmark from `SUMMARY.md`'s 2026-09-17 entry applies unchanged: a timing rule must beat
   buy-and-hold of the things it times, not the incumbent. **This note does not propose it.** If a
   future session revives it, the untimed control is mandatory and comes first.
2. **"Blending beats switching" (learnings.md) now has a third instance queued against it and no new
   evidence for it.** Nothing here reconciles that; the decomposition is a measurement claim, and its
   timing corollary is the part this lab has repeatedly refuted in other clothing.
3. **The paper's momentum result cuts toward the incumbent, not away from it.** If price momentum's
   premium is an overnight object and the champion is a momentum book held 24 hours, then the champion
   is already collecting a positive night leg and a negative day leg and netting them. That is a
   *description* of the incumbent, not an improvement to it, and it predicts that decomposing the
   champion's own realised returns into night and day would show the premium concentrated overnight —
   a holdings-only diagnostic that costs no trial and would be the cheapest possible test of whether
   this whole literature describes this universe at all.

## Related

- `notes/2026-09-18-overnight-return-as-firm-sentiment.md` — the tradeable long-only version, with a
  close-to-close holding period; build from that note, not this one.
- `notes/2026-09-18-beta-at-night-versus-day.md` — the systematic-risk half of the same
  decomposition, and the reason a beta or volatility sort held 24 hours is a sum of two opposite slopes.
- `notes/2026-08-29-range-based-volatility-estimators.md` — the other way to use the non-close columns
  of a daily bar; the open-to-close-only volatility estimator suggested above sits alongside these.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md` — the stale-price problem, here operating
  inside the day rather than across days.
- `notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — the region demean that
  a cross-region overnight sort needs.
- `notes/2026-09-17-factor-momentum-timing-a-portfolio-on-its-own-past-return.md` — the anti-pattern
  `TugOfWar` belongs to, and the untimed-baseline screen that kills it cheaply.
- `experiments/learnings.md` (2026-08-30) — the lab's own overnight-sums screen, which this paper
  predicts.
