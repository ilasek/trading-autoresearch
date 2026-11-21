---
title: "Trading turnover on the Tokyo Stock Exchange — the premium is concave, not monotone; all of its content sits in the top turnover tercile; and the signal's own persistence is low enough that the long-horizon version is weaker"
authors: Hu (Shing-yang)
year: 1997
venue: "Unpublished working paper (National Taiwan University / University of Chicago), deposited on SSRN — venue tier 2 at best by this folder's rubric, and the citation count does not support that, so graded tier 3/C"
url: https://doi.org/10.2139/ssrn.15133
citations: 35 (Crossref `is-referenced-by-count`, checked 2026-11-21); Semantic Scholar's title search endpoint returned HTTP 429 (checked 2026-11-21) and was not retried
sample_period: "1976-04 to 1993-03 (monthly), from the PACAP database"
markets: "Japan only — Tokyo Stock Exchange, roughly 1,080 to 1,572 names in the monthly cross-section, 272,490 firm-months in total"
tier: "C. An unpublished 1997 working paper with a modest citation count and a self-declared survivorship problem. Kept, and kept at C rather than discarded, for two things nothing else in this folder supplies: a **non-US large-cap** reading of the turnover effect, and **numerical estimates of the turnover signal's own persistence**, which is the acceptance criterion the [2026-11-20] aim added and which the Tier-A source on the same effect does not state."
validation_overlap: false
published_post_2018: false
read: "Full text (29 pages, 52 KB of extracted text, 462 instances of `\" the \"`, zero `( )` dropout; abstract, all five sections and all six table captions intact), served by `econwpa.ub.uni-muenchen.de/econ-wp/fin/papers/9702/9702001.pdf`, HTTP 200 on the first try."
---

## Access

**A new working channel, and it is an old one: the EconWPA archive at
`econwpa.ub.uni-muenchen.de/econ-wp/<field>/papers/<yymm>/<id>.pdf`** — the pre-RePEc economics
working-paper archive, now mirrored at Munich — served a 1997 deposit in full at HTTP 200 on the
first try, with no bot challenge. This is the right channel for a **pre-2000 working paper that
never acquired a journal version**, which is a class this folder has otherwise reached only through
author pages. Note the path shape: the directory is the deposit's year-month, so the URL encodes
the date rather than the title, and a filename-shaped search will not find it.

One identification caution. The search result that surfaced this file was captioned with the
Datar–Naik–Radcliffe turnover paper's subject matter, and the document is **not** that paper — it
is a single-authored Tokyo Stock Exchange study by Shing-yang Hu that *cites* Datar–Naik–Radcliffe.
**A search engine's caption is not a title page**; the file was identified from its own first page.

## Mechanism

The paper proposes turnover as a **widely accessible proxy for liquidity**, and derives its
predictions from an Amihud–Mendelson-type transaction-cost equilibrium rather than asserting them.
The model's logic: assets differ in transaction cost, investors differ in trading frequency, and in
equilibrium investors who trade often hold the cheap-to-trade assets and therefore accept lower
gross expected returns. If observed turnover measures the **marginal holder's trading frequency**
— equivalently, the inverse of their holding period — then turnover and expected return are
negatively related.

Two further predictions follow, and they are the reason to read this paper rather than only its
abstract:

- The cross-sectional expected return is a **concave** function of turnover, not a monotone one.
  The transaction-cost premium is a decreasing and concave function of turnover and an increasing
  and concave function of trading cost, so the relation should flatten over most of the range and
  bite only at the top.
- The *time-series* expected return is an **increasing** function of aggregate turnover.

The concavity is a genuine theoretical commitment, and it is the prediction that matters for a
portfolio built on a sorted book, because it says the sort is informative at one end only.

## Construction recipe

- **Signal.** Turnover, defined here as the annualised number of shares traded in the previous
  month per ten shares outstanding. Lagged **monthly** turnover is the headline proxy for expected
  turnover; the paper also tests turnover cumulated over the previous **twelve months**.
- **Cross-sectional estimation.** Fama–MacBeth two-step: monthly cross-sectional OLS of annualised
  excess return on lagged turnover, then simple and precision-weighted time-series averages of the
  slopes. Controls in the multivariate version are market value, book-to-market and
  cash-flow-to-price.
- **The non-monotone version, which is the construction to copy.** A piecewise-linear
  cross-sectional regression with dummies for the bottom 30%, middle 40% and top 30% of turnover
  and a **separate slope inside each band**. Cut-points at the 30th and 70th percentiles are chosen
  to equalise group sizes, not fitted. This is the cheapest available test of whether a sorted
  signal's content is concentrated in one tail, and it costs one regression.
- **Portfolio version.** Monthly re-formed turnover deciles, equal-weighted.
- **Sample filters.** Only firms with positive book value and positive cash flow, following
  Chan–Hamao–Lakonishok.

## Robustness evidence (qualitative only)

- **The sign agrees with the US literature**, on a different market, a different database and a
  sample that ends before most of the US work was written. That is the main thing this note is for:
  it is the only non-US, large-cap-exchange reading of the turnover effect this folder holds.
- **The premium is not monotone in turnover, and the paper shows this rather than assuming it.**
  In the decile figure the average premium *rises* with turnover through the fifth decile and then
  falls, and in the piecewise regression the price of turnover is **statistically indistinguishable
  from zero in both the bottom 30% and the middle 40%, and significantly negative only in the top
  30%** (point estimate −0.355, t ≈ −4.5). The single sharpest cell is the top decile: its average
  annualised premium is about −2% against about +8% for the ninth decile, a difference significant
  both parametrically (t ≈ 5.9) and non-parametrically (60.3% of monthly differences positive).
  The author also reports that one of the two precision-weighted estimates is *inconsistent* with
  the hypothesis and that the bands cannot be statistically separated — a candour point that most
  citations of this literature drop.
- **The signal's persistence, measured.** This is the number the folder came for. Fitting an
  ARMA(1,1) to each name's monthly turnover over 1,577 stocks: **mean AR coefficient 0.63, mean MA
  coefficient 0.23**, with the AR term significantly positive for 86% of stocks and the MA term for
  only 45%. The autocorrelation of monthly turnover with its own lag is **0.51**; with lagged
  *annual* turnover it is **0.42**.
- **The long-horizon version is the weaker version.** The author tested lagged twelve-month
  turnover as the proxy in place of lagged monthly turnover and reports, in a footnote, that "the
  result is weaker" — and chose the one-month proxy on the measured grounds that the series is
  closer to an AR(1) than to a moving average.
- **Known weaknesses, stated by the author.** PACAP contains no firms delisted before 1990, so the
  sample carries **survivorship bias**; the positive-book-and-cash-flow filter adds a selection on
  top of that. No transaction costs are modelled anywhere. Multiple testing is not addressed, and
  the paper closes by flagging an **unexplained December seasonal** in the estimated price of
  turnover — an open anomaly inside its own result, which is the correct way to report one and also
  a reason not to treat the point estimates as settled.
- **No replication.** Unpublished, modestly cited, and this folder has found no independent
  re-test on Japanese data.

## Implementability here

**The signal is not computable** — turnover's denominator is shares outstanding, as in the
companion note. What this paper contributes is not a book but three numbers and one construction
that bear directly on the [2026-11-20] acceptance criteria.

1. **Criterion (iv) fails, and now it fails on measured evidence rather than on inference.** The
   session-99 aim required a formation horizon of 63 days or longer, *or* a stated rank
   autocorrelation. This source supplies the autocorrelation — monthly AR ≈ 0.63, lag-1 correlation
   ≈ 0.51 — and then reports that lengthening the formation window to twelve months **weakens** the
   result. A turnover-style volume signal is therefore a *medium*-persistence object whose
   information decays faster than a quarterly rebalance can collect, and the slow, low-turnover
   corner that v3's cost model leaves nearly free is **not where this signal's content is**. That
   closes `program.md`'s "turnover trends" clause on its own terms: the trend version is the weak
   version.
2. **Criterion (ii) fails in the same place as in the Tier-A source, and the agreement across two
   markets is what makes it a finding.** All of the cross-sectional content sits in the **top**
   turnover band; the bottom 30% carries a slope indistinguishable from zero. A long-only book can
   only *decline* to hold the top band, and the attainable-underweight vein has already priced that
   lever as small. Two independent samples, two decades apart, on two continents, both put the
   signal's content on the leg this lab cannot hold.
3. **The piecewise-linear band regression is free and should be adopted as a general screen.** For
   any proposed cross-sectional score, run three separate slopes on fixed terciles (cut-points
   chosen to equalise counts, never fitted) before building a book. If the slope is flat in the
   band the long leg would occupy, the candidate is refused without a trial. This is a strictly
   stronger pre-trial screen than a single rank IC, and the folder's own v3 learning — that "a rank
   IC cannot screen a claim that it is" — is exactly the defect it fixes: a monotone-linear summary
   statistic of a concave relation reports a signal the tradeable end does not contain. It needs no
   returns beyond the train split and no holdout.
4. **One transferable caution about cut-point choice.** The paper fixes its bands at the 30th and
   70th percentiles for a stated, non-performance reason (equal group sizes). Any band screen run
   here should do the same and record the cut-points before looking, because a band boundary is a
   free parameter and this lab's deflated-Sharpe bar counts every search.

**What does not transfer.** The time-series prediction (aggregate turnover forecasting the market)
is a timing construction, which v3 excludes by grading against a fully-invested pool. The
December-seasonal observation is a single unexplained monthly pattern in one market in one
seventeen-year sample with no multiple-testing treatment, and this folder should not carry it as
anything other than the author's own open question.

## Related

- `notes/2026-11-21-turnover-effect-uncertainty-not-liquidity.md` — the Tier-A source on the same
  effect. The two **disagree about the mechanism** (transaction-cost trading-frequency equilibrium
  here; aggregate-volatility-risk hedging there, with that paper showing turnover is if anything
  *negatively* related to liquidity) and **agree about where the effect lives**. The disagreement
  is worth preserving: this paper's liquidity reading is the one the later Tier-A source sets out
  to refute, and it refutes it with measures this one did not have.
- `notes/2026-10-05-turnover-and-the-momentum-life-cycle.md` — the third reading of the same
  variable, as a momentum-phase state variable.
- `notes/2026-09-07-high-volume-return-premium.md` — the volume object this panel *can* compute,
  and a within-name time-series rank rather than a cross-sectional rate.
- The folder's cross-family section on the shape of a sorted book — how many bins, whether the
  ranking is monotone, which end is used — which this source supplies a direct test for.
