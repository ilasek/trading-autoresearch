---
title: "ETF Arbitrage, Non-Fundamental Demand, and Return Predictability — and why the price-observable half of it is a null"
authors: Brown, Davies, Ringgenberg
year: 2021
venue: Review of Finance (Tier 1) — read as the Final Accepted Manuscript in the University of Arizona repository
url: https://doi.org/10.1093/rof/rfaa027
citations: 134 (Crossref, checked 2026-10-10)
sample_period: 2007–2016
markets: 1,515 US-listed ETFs (equity and other asset classes), filtered to ≥$50M assets and ≥12 months of history; leveraged and unleveraged sub-samples
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

The same primary-market link as Ben-David–Franzoni–Moussawi, read as a **measurement device
rather than as a propagation channel**. The argument is an identification one and it is the
reason to read this paper: an ETF share is a claim on the ETF's assets, so *excess demand for
either side must be non-fundamental*, because a fundamental revision moves both. Creation and
redemption happen only when the law of one price is violated between the two sides. Therefore
**observed primary-market activity is a direct, signed signal that a non-fundamental demand
shock has occurred** — without needing to identify who demanded what or why.

The model is a small one with authorized participants, ETF-share demand and
underlying-asset demand, and its useful output is a set of remarks rather than a closed form:

- **Flows are symptomatic of non-fundamental demand** (their Remark 2) — this is the licence for
  the whole empirical design.
- **The best signals come from ETFs with volatile flows and with different clienteles on the two
  sides** (Remark 3), which is why leveraged and high-primary-activity funds are treated
  separately rather than pooled.
- **The sign of the predictive coefficient identifies which side is more demand-sensitive**
  (Remark 7). A negative flow-to-future-return relation means the ETF *shares* absorbed the
  non-fundamental shock, so the mispricing is in the wrapper and reverts.
- **Premium changes signal non-fundamental demand only if the AP market is not perfectly
  competitive** (Remark 4). This remark is what the paper's own null later turns into evidence.
- **Share-return and NAV-return predictability should be approximately the same** (Remark 8) —
  the distortion is not confined to the wrapper's price, it is pushed into the assets.

The authors are explicit that whether flows signal *large* distortions is not a theoretical
question: "ETF flows are akin to observing ice in the ocean" — observable, but the mass beneath
is unknown a priori. The paper's contribution is to measure it.

## Construction recipe

Two candidate signals, both defined per ETF per month:

- `ETFFlow(j,t) = SharesOutstanding(j,t) / SharesOutstanding(j,t−1) − 1` — the percentage change
  in shares outstanding, i.e. net creation/redemption. **A share-count quantity, with no price
  input at all.**
- `ETFPremChange(j,t) = (p_t/π_t − 1) − (p_{t−1}/π_{t−1} − 1)` — the change in the ETF premium,
  where `p` is the share price and `π` is NAV per share. **The price-observable analogue of the
  same shock.**

Sorting and evaluation:

- Each month, sort ETFs into deciles on the prior month's signal (highest creations = decile 10).
  Hold equal-weighted and AUM-value-weighted long-short portfolios at 1-, 3- and 6-month
  horizons. For overlapping multi-month returns, Newey-West standard errors with lag equal to the
  horizon in months. The 6-month strategy is implemented as an equal-weighted overlay of the six
  most recent 1-month-formation portfolios, one rolling out and one rolling in each month.
- Sample filters that matter: ≥$50M assets (removes 27% of funds but <1% of capitalisation,
  and is motivated explicitly as a guard against **non-synchronous prices** in thinly traded
  funds); ≥12 months of history; a "mature" flag set once a fund both passes the size threshold
  and has a month in which at least half the trading days showed creation/redemption activity
  (this halves the fund count and costs only ~10% of capitalisation).
- Panel regressions with date fixed effects as the multivariate counterpart, using decile dummies
  *and* the continuous signal.
- Investor-level counterparts, for the welfare claim rather than the signal: the internal rate of
  return (treating the representative holder as responsible for all flows) and a
  share-growth-adjusted return (an investor who reallocates monthly between the fund and cash on
  last month's flow).

## Robustness evidence (qualitative only)

- Flows predict subsequent returns with a **negative** sign, at 1-, 3- and 6-month horizons, in
  portfolio sorts and in panel regressions with date fixed effects.
- **The relation is non-linear**: decile-dummy specifications are significant while the
  continuous flow measure is not, at every horizon. A linear cross-sectional score on this signal
  is the wrong functional form by the paper's own evidence — the information is in the tails.
- **Where the predictability lives differs by fund type.** In leveraged funds essentially all of
  it is earned in the first month after formation; in mature unleveraged funds there is nothing
  at one month and the effect appears over months two to six. Same mechanism, different speeds,
  consistent with Remark 3's volatility-of-flows ordering.
- Survives: FF3, Carhart, FF5 and Hou–Xue–Zhang factor adjustments; pre-sorting on fund size (so
  it is not a small-fund artifact — large funds show it too); de-levering the leveraged funds to
  remove their embedded optionality; orthogonalising to aggregate US net equity fund flows.
  **Passive index *mutual fund* flows show no such predictability**, which is the paper's
  argument that the signal is about the AP-mediated LOOP violation and not about retail
  performance-chasing in general.
- Using **NAV returns in place of share returns** gives qualitatively the same result, as
  Remark 8 predicts — so this is not a wrapper-pricing curiosity, the distortion reaches the
  assets.
- **The decisive negative, and the reason this note exists: ETF premium changes do not predict
  the cross-section of returns.** The sorted returns are generally positive in sign but not
  statistically distinguishable from zero at any horizon, in any of the three samples. The
  authors' own reading is that this is what the model predicts *if the AP market is highly
  competitive and premia are measured with noise* (Remark 4 failing in the benign direction).
  They abandon the premium signal and work exclusively with flows.
- A second negative in the same direction, in a footnote: **ETF flows are neither highly
  persistent nor correlated with contemporaneous returns.** So the working signal is not a
  disguised momentum or reversal variable, and — the direction that matters here — **no
  function of past returns is a proxy for it.**
- Scope limits: US-listed funds; one decade; the strongest results sit in leveraged funds, which
  are a product type this panel does not contain. The authors acknowledge the overlapping-return
  and Stambaugh-bias issues and address them with Newey-West and date fixed effects respectively.

## Implementability here

**Read as a construction, this paper closes a candidate shape rather than opening one, and it is
the cheapest closure in this folder since the scalar-target score-shrinkage cancellation (#174).**

The tempting candidate on this panel is obvious and the lab could build it today: the universe
holds 42 ETFs *and* the index-member stocks those ETFs track, so a **synthetic premium** is
computable from closes alone — take an ETF's return against the equal-weighted (or
eligible-weighted) return of the index members it tracks, accumulate the gap, and trade the
divergence as a reversion signal. No holdings file, no NAV feed, no share counts.

That candidate is refused by this paper on three independent grounds, and the first is sufficient:

1. **The premium side is the half that does not work.** `ETFPremChange` is the published,
   Tier-A, correctly-measured version of exactly that signal — computed against the fund's *true*
   NAV, on the funds where the arbitrage is most active, over a ten-year sample — and it is a
   null at every horizon in every sub-sample. A synthetic basket proxy is a noisier version of a
   statistic that fails when measured cleanly. Building it would be spending a trial to add
   measurement error to a published zero.
2. **The signal that does work cannot be seen from prices, and the paper says so in the strongest
   available form.** `ETFFlow` is a share-count change. If flows were correlated with
   contemporaneous or past returns, a price-based proxy would exist; the paper reports they are
   not, and that they are not persistent either. There is no daily-bar substitute.
3. **The synthetic-premium proxy is dominated by a time-zone artifact on this panel.** The
   paper's own $50M filter is justified as a guard against non-synchronous prices *within one
   market*. Here, eight of the nine index regions close hours before a US-listed ETF prints, so
   an ETF-minus-basket gap built from closes mostly measures the stale half of the pair — the
   artifact the folder's nonsynchronous-trading notes describe and the one v3's next-real-close
   fill rule was introduced to stop candidates from harvesting.

What survives as usable:

- **The non-linearity finding is transferable and free.** Decile dummies significant, continuous
  measure not, at all three horizons — a clean instance of the folder's standing point about the
  shape of a sorted book: when the information is in the tails, a linear score on the same
  variable measures nothing. Worth stating as a reason to *check* the shape before concluding a
  signal is absent, on any family.
- **The paper's filter logic is a free screen.** Requiring a minimum size and a minimum of
  *primary-market activity* removed half the funds for a tenth of the capitalisation. The
  analogue here is pure accounting on the `eligible` panel (how much of the ETF sleeve's weight
  sits in funds that are small or barely traded), and it composes with the region × liquidity ×
  tax census (#214) and the eligibility-turnover census (#220) into one pass.
- **It corroborates the lab's ETF-versus-constituent null** [`learnings.md` 2026-08-31] from a
  second direction: not only is there no directional lead (the stale-pricing branch), there is no
  tradeable *divergence* either when the divergence is measured properly.

## Access

The published Review of Finance version is closed and all three indexes report no fetchable OA
copy (`any_repository_has_fulltext: false` in OpenAlex). **The University of Arizona repository
served the Final Accepted Manuscript**: resolve `hdl.handle.net/10150/661294` to
`repository.arizona.edu/handle/10150/661294`, read the `/bitstreams/<uuid>/download` links out of
the landing page, and fetch them — one is the 53-page PDF (907 KB, parses cleanly with
`pdftotext -layout`, no ASCII shift, no `( )` math dropout) and one is a thumbnail PNG, so `file`
the result. This is a **new working channel for this folder**, found through OpenAlex's own
`locations[].landing_page_url` list rather than by guessing a hostname — exactly the 2026-10-04
procedure, and another instance of a co-author's institutional repository holding what the
publisher refuses.
Note that the OpenAlex record's `any_repository_has_fulltext: false` was **wrong** for this
article — the handle it listed in the same response held the file.

## Related

- `notes/2026-10-10-etf-arbitrage-shock-propagation.md` — the propagation mechanism this paper
  turns into a measurement device. Read first.
- `notes/2026-10-10-etf-launch-as-a-return-chasing-boundary.md` — the third leg: the ETF columns'
  own entry dates.
- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` and the lab's v2
  residual-reversion result — the other place a divergence-reversion construction died, and it
  died on the fill convention rather than on the signal.
- `notes/2026-10-09-index-inclusion-demand-curves-vs-price-pressure.md` — non-fundamental demand
  at the event frequency, where the price-observable version *is* measurable (and is still not
  reachable here, for different reasons: #226).
