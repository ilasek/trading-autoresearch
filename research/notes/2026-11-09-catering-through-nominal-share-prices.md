---
title: "Catering Through Nominal Share Prices (read as NBER Working Paper 13762)"
authors: Baker, Greenwood, Wurgler
year: 2009 (published); working-paper version read, January 2008
venue: Journal of Finance 64(6), 2559–2590 (venue tier 1); working paper = NBER WP 13762
url: https://doi.org/10.1111/j.1540-6261.2009.01511.x
citations: 199 (Crossref `is-referenced-by-count`, checked 2026-11-09)
sample_period: 1963–2006 (CRSP splits and prices; IPO prices from a separate hand-collected series)
markets: US (CRSP share codes 10 and 11)
tier: A — tier-1 venue, three-figure citations, four-decade sample, firm-level tests run alongside the time-series tests specifically to rule out composition effects, and the authors state the Stambaugh-bias concern about their own predictive regressions
validation_overlap: false (sample ends 2006)
published_post_2018: false
read: full text of NBER WP 13762 (128 KB of clean text, 590 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). The published JF version was not obtained; table numbers may have changed in review.
---

## Access

`nber.org/system/files/working_papers/w13762/w13762.pdf` on the first try — the channel
`research/README.md` already records as reliable. `pdftotext -layout` warned
`Invalid XRef entry 1` and reconstructed the table; the output passed every integrity check in the
README (character count, `" the "` count, `( )` dropout, title line), so the warning is cosmetic.

## Mechanism

**A board chooses its firm's nominal share price, and it chooses it to put the firm in whichever
price category investors are currently paying up for.** This is the competing explanation to the
norms story: same object, different driver, and the two papers cite each other.

The argument has three parts.

**1. An accounting identity for the price level.** Ignoring dividends,
`P_{i,t} = P_{i,t−1} · (1 + R_{i,t}) · (1 + S_{i,t}·N_{i,t})`, where `S` indicates a split and `N` is
the inverse split ratio minus one (`−0.5` for a 2-for-1). In logs, and substituting recursively back
to the IPO,

> `p_{i,t} ≈ p_{i,IPO} + Σ_k r_{i,t−k} + Σ_k s_{i,t−k}·n`

So the observed log price level is **the IPO price, plus accumulated capital-gain return, plus
accumulated split decisions** — the first and third terms chosen by the firm, the second given by
the market. Everything the paper does is about the determinants of the chosen terms. There are four
decision variables in it: the IPO price, the binary decision to split in a period, the net price
change due to active management `m_{i,t} ≡ p_{i,t} − p_{i,t−1} − r_{i,t}`, and the price level itself
conditional on having just split.

**2. A time-varying "low-price premium" as the catering incentive.** Following the dividend-premium
construction of the same authors' earlier work, define

- `P_CME` ("cheap minus expensive") = log average market-to-book of **low-priced** stocks minus log
  average market-to-book of **high-priced** stocks, with low/high taken as below the 30th / above the
  70th percentile of NYSE prices;
- `P_SMB` ("small minus big") = the same difference between **small-cap** and **large-cap** stocks,
  on the 30th/70th capitalisation percentiles;
- a third proxy: the **average announcement effect of recent splits**.

Because capitalisation and price are strongly related in the cross-section, `P_CME` and `P_SMB` look
much alike — which is itself part of the paper's reading, below.

**3. The predictions and what they find.** When low-priced or small-cap stocks carry relatively high
valuations, catering says splits should be more frequent, split ratios larger, chosen post-split
prices lower, and IPO prices lower. All four hold. The catering proxies explain a large share of the
annual time variation in split frequency, a very large share of the variation in log IPO offer and
first-day prices, and about half the variation in average post-split prices chosen by splitters —
magnitudes the authors argue a transaction-cost or asymmetric-information theory would struggle to
match. The results survive controls for the overall average price level and for recent returns, and
they reappear in firm-level regressions with firm and industry controls, which is the test that
rules out aggregate composition shifts.

**The interpretation that matters for a cross-sectional panel.** The authors' own reading is that,
given the strong cross-sectional price–size relation, **managers may be trying to categorise their
firms as small firms when investors favour small firms**. The robustness tests sharpen this: catering
affects post-split prices **only for larger firms** — large firms "acting small" at opportune times —
while the IPO-price results come from small, young firms. So the price level is a *categorisation
instrument*, deliberately set, and the category it signals is size.

**Why a manager would believe it works.** The paper only needs managers to believe nominal price
matters, but it motivates that belief with the return-side evidence: splitting stocks comove more
with low-priced stocks afterwards (Green–Hwang), splitting stocks' volatility rises, individuals hold
lower-priced stocks than institutions, and low-priced stocks carry more noise trading. The authors
list candidate psychologies without choosing one — nominal illusion ("\$10 has more room to grow than
\$25"), naive equation of low price with small capitalisation (a cheap heuristic, since a quote is
easier to obtain than a capitalisation), and attention or investor-recognition effects. **The
Green–Hwang leg of this motivation is the one that later failed to replicate — see the related
note.**

**Return predictability, sign only.** Treating subsequent returns as the correction of ex-ante
mispricing, the paper regresses future relative returns of low-minus-high-priced and
small-minus-large-cap portfolios on split frequency and on average post-split prices, controlling
for the overall equal-weighted price level, at one-, two- and three-year horizons. The signs are
consistent with catering throughout: **more frequent splitting, and lower chosen post-split prices,
predict lower subsequent returns on low-priced stocks relative to high-priced ones, and on small caps
relative to large caps.** Magnitudes are period-specific performance figures and are deliberately
left in the source. The authors flag the Stambaugh-bias concern themselves and report the
autocorrelation check.

## Construction recipe

Reproducible as stated, modulo the fundamentals it needs:

- **Splits.** CRSP distribution code 5523, share codes 10/11. Three buckets: *regular splits* ratio
  > 1.25:1, *stock dividends* 1.01:1–1.25:1, *reverse splits* < 1:1. Pre-split price is the close the
  day before; post-split price is the pre-split price divided by the ratio.
- **Active price management `m`.** For each listed firm and year, the log difference between the
  actual year-end price and the beginning-of-year price grown at the **capital-gain** return
  (dividends deliberately excluded, so that dividend policy is exogenous rather than lumped into
  price management). Averaged across firms for the aggregate series.
- **Catering proxies.** As above; value-weighted and equal-weighted variants both reported, the
  equal-weighted market-to-book winsorised at 10, Berkshire Hathaway excluded from mean-price
  computations.
- **Specifications.** Four dependent variables (`p_IPO`, the split indicator `s`, `m`, and `p`
  conditional on splitting), each run at the market level on the catering proxies and at the firm
  level on firm and industry controls plus the proxies. The price-level specification is restricted
  to firms that split in the period, because only those made an active choice.
- **Predictive regressions.** `R_{t+1} = a + b·s_t + c·p^EW_{t−1} + u`, and the same with average
  post-split price in place of `s`; `R` is the low-minus-high-price or small-minus-large-cap relative
  return, at one-, two- and three-year horizons. The overall price level `p^EW` is the control that
  makes the question "does *excess* splitting predict".

## Robustness evidence (qualitative only)

- Four decades, four distinct dependent variables, and the same sign on all of them.
- **Firm-level tests are run specifically because the aggregate tests could be composition shifts**,
  and the proxies retain incremental explanatory power after firm and industry controls. This is the
  single most reassuring design feature.
- Subsample splits, time trends and difference specifications are reported with little change.
- The IPO leg is the cleanest identification in the paper: a newly public firm has no legacy price,
  so its chosen price is pure active selection.
- Known limits, stated by the authors: a short time series for the return-predictability tests;
  Stambaugh bias in predictive regressions with persistent regressors; and the open question of
  *why* nominal prices matter to investors at all, which the paper explicitly does not answer.
- One framing tension with the companion literature that should be read as a scope statement rather
  than a contradiction: the constancy emphasised by the norms paper is constancy **relative to
  economy-wide nominal growth**; average chosen prices still vary by a factor of two to three across
  decades, and that variation is what catering explains.

## Implementability here

**Not a candidate, for three independent reasons, and a reading rule that survives all three.**

1. **Every input is a fundamental.** Market-to-book needs book equity; the split indicator needs a
   distribution file; the IPO price needs an offering record; capitalisation needs a share count
   (`#408`). The `prices` + `aux` contract supplies none of them, and the hindsight guard refuses the
   membership and universe files that would be the nearest substitutes. There is no version of this
   that a candidate file can compute.
2. **The signal is a single time series.** `P_CME` is one number per year for the whole market. Even
   with fundamentals it would be a market-timing conditioner, not a cross-sectional score, and
   `program.md`'s objective is a long-only cross-sectional book scored against an equal-weight pool
   that it would be timing *against itself*.
3. **The tradeable direction is the short leg.** The predictability the paper reports is *low-priced
   minus high-priced* and *small minus large* going **down** after heavy splitting. Long-only, the
   reachable side is "hold high-priced / large names when the proxy is high", which is an
   unconditional large-cap tilt with a slow conditioner on top — and `#414` already prices
   size-and-friction-shaped mechanisms at this lab's worst category prior.

**The reading rule that does survive.** The identity
`p_t = p_IPO + Σ r + Σ s·n` is the cleanest available statement of what a price level contains, and
it has a direct consequence for this lab's back-adjusted panel: back-adjustment strips the `Σ s·n`
term *and* re-bases the `Σ r` term on the end of the sample, so the stored level is **the negative of
the name's future cumulative adjustment**, up to a constant. The catering result adds that the split
term is **not** noise to be removed — it is a deliberate, size-correlated managerial choice. So the
stored adjusted level is a *function of a future managerial decision that is itself predicted by the
firm's size and by a market-wide valuation state*. That is a strictly worse object to have inside a
cross-sectional score than "a units problem", and it is the mechanism behind the nightly's finding
that partialling `log P` out of unit-free slow objects can invert their sign.

**One free refusal test it supplies.** A candidate that sorts this panel on anything monotone in the
stored price level — including quantities that merely *correlate* with it at low rank correlation —
is partly sorting on future split-and-dividend behaviour. Refuse it before writing it, or state the
within-region `log P` control in the hypothesis and report the score both ways.

## Related

- `2026-11-09-the-nominal-share-price-puzzle-and-the-price-norm.md` — the competing explanation
  (norms) for the same object, with the cross-country and trading-cost facts this note does not have.
  The two disagree about the driver and agree that the level is chosen.
- `2026-11-09-price-based-comovement-and-its-failed-replication.md` — this paper cites Green–Hwang as
  evidence that "return characteristics actually are affected by nominal price"; that specific leg of
  the motivation did not survive replication. The catering results themselves are untouched by it,
  because they are about managerial behaviour, which needs only the *belief*.
- `2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` — same author on the
  Nikkei's weighting rule; the price level there is an index-weight determinant rather than a
  category label.
- `2026-11-06-index-membership-is-not-an-information-free-selection.md` and `#415` — the same shape
  of finding one level up: a selection that looks mechanical is a decision.
