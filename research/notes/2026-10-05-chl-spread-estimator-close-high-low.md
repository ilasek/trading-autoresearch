---
title: "A Simple Estimation of Bid-Ask Spreads from Daily Close, High, and Low Prices (the CHL estimator)"
authors: Abdi, Ranaldo
year: 2017
venue: The Review of Financial Studies 30(12), 4437–4480 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1093/rfs/hhx084
citations: 340 (Crossref `is-referenced-by-count`, checked 2026-10-05); 359 (OpenAlex, checked 2026-10-05); Semantic Scholar returns a clean `not found` for this real DOI (checked 2026-10-05)
sample_period: "Validation against intraday quotes: 1993–2015 (TAQ); historical application: NYSE from 1926 and AMEX from 1962, through 2015. Simulation evidence is sample-free."
markets: US exchange-listed equities (NYSE, AMEX; a Nasdaq-NMS robustness sample), plus Monte Carlo simulation under a GBM efficient price
tier: "A. Tier-1 venue, well cited for its age, the core result is a theorem about a Brownian efficient price rather than an empirical regularity, and the empirical part is an estimator horserace against an intraday benchmark rather than a return prediction. The one gap to record: the validation is **US-only**, so its ranking against Corwin–Schultz is not independently established on an international panel."
validation_overlap: false
published_post_2018: false
read: "Full text of the April 2017 working-paper version (University of St. Gallen, Swiss Institute of Banking and Finance WP 2016/04, `alexandria.unisg.ch`, 61pp) — the version of record for the published RFS article. `pdftotext` drops the mathematics in this file, so equations (8)–(11) were read **visually**, from `pdftoppm` page renders, and are transcribed below from the rendered pages."
---

## Access

`alexandria.unisg.ch/server/api/core/bitstreams/<uuid>/content` returned HTTP 200 and a clean
61-page PDF. **Note the contrast worth recording: this is the same DSpace bitstream URL form that
`pyxida.aueb.gr` serves behind Anubis** [2026-10-03] — so once again the platform predicts nothing
and the institution's bot policy predicts everything, and a `server/api/core/bitstreams/…/content`
URL is worth trying rather than assuming.

**A second worked example of the "math does not extract" failure, and the fix.** `pdftotext
-layout` produced a fully readable 152 KB text file in which **every displayed equation and every
inline symbol was silently missing** — not garbled, *absent*, leaving sentences like "the estimator
in which (  ) is replaced with ( )". This is more dangerous than a scan, because the text looks
complete and parses fine. The tell is a definition that reads as empty parentheses. `pdftoppm -png
-r 120 -gray -f 12 -l 16` rendered the five relevant pages and the equations were legible
immediately, at a cost of four image reads. **Check a formula-bearing paper's extracted text for
empty parentheses before trusting it.**

Semantic Scholar's clean `not found` for a real, indexed DOI recurred here — the **sixth** recorded
instance. Crossref answered first try, OpenAlex second.

## Mechanism

This is not a return anomaly; it is a **measurement** result, in the same category as
`2026-08-29-range-based-volatility-estimators.md`. It answers: given only daily close, high and low
prices, what is the best estimate of a security's effective bid-ask spread?

The logic is Roll's — the observed price departs from the efficient price by a transaction-cost
wedge, so the covariance structure of that wedge identifies the spread — with one substitution that
does all the work. Roll uses **neighbouring closes** as the reference for today's close, which forces
him to assume serially independent trade directions and an equal chance that a close is buyer- or
seller-initiated; both assumptions are contradicted in the microstructure literature and Roll's own
estimator famously returns a negative squared spread a large fraction of the time.

Abdi–Ranaldo replace the neighbouring closes with the **mid-range**: the average of the day's high
and low **log** prices. Three facts make this a better reference point, and the first is why the
whole thing works.

1. **The mid-range of *observed* prices equals the mid-range of *efficient* prices**, because under
   the (empirically supported, and analytically relaxable) assumption that the high is buyer-
   initiated and the low is seller-initiated, the half-spread is added at the high and subtracted at
   the low and **cancels in the average**. So the mid-range is a spread-free observable — a quantity
   you can compute from contaminated data that is not itself contaminated.
2. The efficient price **passes through the mid-range at least once during the day**, and the day-`t`
   mid-range occurs before the close while the day-`t+1` mid-range occurs after it, so the **average
   of two consecutive mid-ranges is an unbiased proxy for the end-of-day-`t` midquote**.
3. The squared distance between the close and that proxy therefore contains exactly two pieces — the
   squared effective half-spread, and the efficient-price variance introduced by the proxy. The
   second piece is separately identified by the **variance of changes in mid-ranges**, which contains
   no spread at all. Subtract and the spread falls out.

Three consequences matter for anyone choosing between this and Corwin–Schultz's high-low (HL)
estimator, and the authors state all three:

- **It uses a strictly wider information set** — close, high and low, rather than high and low.
- **It is robust to overnight and non-trading-period price moves, so it needs no ad-hoc overnight
  adjustment.** HL compares a one-day range to a two-day range and therefore inherits whatever
  happened between the two closes; CHL does not, because the efficient-price-variance term is
  estimated from the mid-ranges themselves. (Corwin–Schultz handle this with an explicit overnight
  correction; CHL removes the need for one.)
- **It is much less sensitive to how many trades a day actually contains.** A range needs two
  extremes to be realised and collapses toward zero when trading is thin; an average of two prices
  degrades far more gracefully. This is why the authors' accuracy advantage is largest exactly where
  it matters — illiquid names and thinly traded days.

## Construction recipe

Let `c_t` be the **log** close of day `t`, and `h_t`, `l_t` the log high and low. Define the
mid-range

    η_t = (h_t + l_t) / 2

The identification (their Theorem 1, equation 9) is

    s² = 4·E[ (c_t − η_t)(c_t − η_{t+1}) ]

with the efficient-price-variance correction (their Proposition 3, equation 8) being
`E[(η_{t+1} − η_t)²] = (2 − k₁/2)·σ²_e` where `k₁ ≡ 4·ln(2)` — the same `4 ln 2` constant that runs
through the Parkinson/Garman–Klass range literature.

Because a sample estimate of the right-hand side can be negative, the paper gives two corrected
estimators over a window of `N` days (their equations 10 and 11), transcribed from the rendered
page:

    ŝ_monthly  = sqrt( max{ 4 · (1/N) · Σ_t (c_t − η_t)(c_t − η_{t+1}) , 0 } )

    ŝ_two-day  = (1/N) · Σ_t ŝ_t ,
                 where  ŝ_t = sqrt( max{ 4 · (c_t − η_t)(c_t − η_{t+1}) , 0 } )

i.e. the *monthly-corrected* version truncates once, after averaging; the *two-day-corrected*
version truncates each two-day estimate at zero, takes roots, then averages.

**Which one to use, and why it is not the unbiased one.** The paper's own finding is that the
monthly-corrected version is **less biased** but the two-day-corrected version **correlates better
with the intraday benchmark**, and they use the two-day version for all their asset-pricing work —
the same choice Corwin–Schultz make for the same reason. Their explanation is that the monthly
version implicitly estimates `E[s²]`, which exceeds `(E[s])²` whenever the spread varies within the
window, whereas isolating a single close transaction per two-day estimate needs no assumption about
the within-window spread distribution. **Record this as a general principle rather than a detail:
when a truncation is needed, truncating early costs bias and buys correlation with the truth, and
for a ranking signal correlation is the thing you want.** This folder has the same trade-off recorded
from the opposite direction in `2026-09-11-influential-observations-winsorization-versus-robust-regression.md`.

**Data hygiene the paper specifies and a user must copy.** Discard any two-day period that includes
a **non-trading day** or a day with a **zero price range**, and require a minimum number of valid
estimates per window (they use 12 days of trades in a month). Both screens exist because `h = l`
makes `η_t = c_t` and the product degenerates.

**Rebalance cadence.** The estimator is defined on a window, not a day. The paper works monthly
throughout, which lines up with this lab's monthly rebalance without any adaptation.

## Robustness evidence (qualitative only)

- **Against an intraday benchmark, in the absence of end-of-day quote data, CHL generally wins on
  both cross-sectional and average time-series correlation with the effective spread, and has the
  lowest estimation errors** — against the Roll, HL, FHT and Gibbs-sampler alternatives. The margin
  is consistent "in levels or in changes, and across subperiods".
- **The advantage widens for less liquid names**, which is the opposite of the usual pattern where an
  estimator is validated on the liquid names it works on. The authors show the same in simulation:
  the range-based competitor degrades as trades per day fall; CHL degrades much less.
- **Partial correlations are the strongest evidence and are easy to miss.** The authors ask whether
  CHL carries information *not already in* the other estimators, and report significantly positive
  average partial cross-sectional and time-series correlations, again largest for the wider-spread
  quintiles. That is the claim that matters for anyone already computing an illiquidity measure:
  it is not a re-labelling of what you have.
- **It extends the measurable history**, which is the authors' own stated motivation — NYSE from
  1926 — and they apply it to transaction-cost-adjusted returns, systematic liquidity risk and
  commonality in liquidity, reporting it more accurate than Roll or HL for those purposes too.
- **The gap: all validation is US.** Corwin–Schultz has an independent 43-exchange validation
  (Fong–Holden–Trzcinka) recorded in this folder; CHL does not, as far as this note establishes.
  **Do not treat "CHL beats HL" as established on a global panel.**

## Implementability here

**This is a strong fit, and the reason is specific to what this lab has already measured.**
`experiments/learnings.md` [2026-08-29, nightly] killed **log average dollar volume** stone dead on
this universe (IC +0.0010, t = +0.11) while Amihud `ILLIQ` survived, and [2026-08-31] killed the
relative-volume substitute too, concluding that *"the family's live content is `ILLIQ`'s price-impact
**numerator** and not trading activity under any normalisation"* — because on 140 mega-caps a
volume ranking is a size ranking with no illiquid tail.

**CHL is a price-impact-style illiquidity measure with no volume term at all.** It is built from
close, high and low only. That makes it the cleanest available test of the lab's own conclusion:
if the live content really is the cost-of-trading numerator rather than activity, a CHL tilt should
work at least as well as `ILLIQ` and should be **less** correlated with size than `ILLIQ` is, since
`ILLIQ` still carries dollar volume in its denominator.

Four concrete advantages on this specific panel:

1. **No dependence on the `volume` panel, which `program.md` warns is NaN on foreign holidays and is
   a share count in native units.** A measure needing only `high`, `low`, `close` sidesteps both the
   missingness and the cross-market units problem in one step. For a 15-region universe that is not a
   minor convenience.
2. **It is a `liquidity-volume` construction that is simultaneously a `range-variance` one**, since
   `η_t` is built from the daily bar's extremes — and `range-variance` is a family this lab has
   declared "unreachable rather than unexplored" after nine screened mechanisms, *all of which were
   width measures*. The mid-range is a **location** statistic of the bar, not a width. That is a
   genuinely unscreened object on this universe.
3. **It is monthly by construction**, matching the champion's cadence, and the signal is a slow-moving
   characteristic, so turnover should be low — the opposite of the 5–10 day reversal the lab found
   structurally forbidden by its own 15 bps.
4. **It is cheap.** Three vectorised operations on panels the engine already hands the candidate.

**The causality pitfall, and it is disqualifying if ignored.** Equation (9) uses **η_{t+1} — the
*next* day's mid-range.** An estimate indexed to day `t` is not knowable at the close of day `t`.
The lab's `causality_check` recomputes weights with the tail hidden and fails anything whose holdings
move, so a naive implementation will fail it. The fix is trivial and must be explicit in the
candidate: **compute the window's estimate using only two-day pairs whose *second* day is strictly
before the formation date.** In practice, when forming weights on date `T`, build the estimate from
pairs `(t, t+1)` with `t+1 ≤ T − 1`. Say this in the hypothesis so it is checkable in review rather
than discovered by the gate.

**Three further cautions.**

- **The universe fights the measure.** This is ~140 global mega-caps and 42 ETFs; true effective
  spreads across it are small and may be compressed into a range where the estimator's noise
  dominates its signal. The paper's own advantage is concentrated in wide-spread names, and this
  panel has none. **Expect a small `t` and pre-register that expectation**; the honest first use is
  as a *screen* on whether the measure separates the universe at all, not as a candidate.
- **Zero-range and stale-price days are not rare here.** Foreign names on local holidays are exactly
  the `h = l` case the paper discards. Apply the authors' screens; do not let a forward-filled or
  stale bar enter a two-day pair.
- **Check it against `ILLIQ` before building a book on it.** The rank correlation between CHL and the
  lab's existing `lv_amihud_illiquidity_tilt` score is a one-line diagnostic and decides whether this
  is a new leg or the same leg. The lab has been burned by exactly this before —
  `experiments/learnings.md` records a candidate returning at rho 0.976 to the Amihud leg. If CHL
  rank-correlates above ~0.9 with `ILLIQ` here, the interesting question is not "does it predict" but
  "which end of a near-identical ranking pays", which is the same question [2026-08-29] had to answer
  about log ADV.

## Related

- `2026-09-04-high-low-spread-estimator.md` — Corwin–Schultz, the estimator this one is built to
  beat; read the two together, and note that this note's source is the challenger and is therefore
  not a neutral referee.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md`,
  `2026-08-31-amihud-volume-component-decomposition.md` — the measure the lab already has a scout on,
  and the decomposition that located its live content in the numerator.
- `2026-09-04-global-liquidity-proxy-horserace.md` — the horserace framing; CHL's absence from an
  international horserace is the gap recorded above.
- `2026-08-29-range-based-volatility-estimators.md` — the `4 ln 2` constant and the range-estimator
  zoo; the mid-range is the one function of the daily bar that family does not contain.
- `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the same
  bias-versus-correlation trade-off that decides which of the two corrected estimators to use.
- `experiments/learnings.md`, [2026-08-29, nightly] and [2026-08-31, nightly] — the log-ADV and
  relative-volume nulls that make this a test of the lab's own stated conclusion rather than a new
  guess.
