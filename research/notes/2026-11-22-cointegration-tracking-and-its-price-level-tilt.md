---
title: "Cointegration-based index tracking — the recipe in full, and the algebra inside it that makes its excess return a nominal-price-level tilt"
authors: Alexander, Dimitriu
year: 2003
venue: "ISMA Centre, University of Reading, discussion paper (January 2003), circulated through the EFMA 2003 accepted-papers archive — venue tier 2 (working paper). The same pair's closely related article, *Indexing and Statistical Arbitrage*, appeared in the **Journal of Portfolio Management** 31(2), 50–63 (2005), which is a tier-1 venue in this folder's rubric."
url: https://efmaefm.org/AcceptedPapers2003/AlexanderCarol_DimitriuAnca/AlexanderCarol_DimitriuAnca.pdf · companion article https://doi.org/10.3905/jpm.2005.470578
citations: "the working paper is **not indexed** (Semantic Scholar's title endpoint returned HTTP 429 and was not retried, per the README's rate-limit note; no DOI exists to resolve — checked 2026-11-22). The companion JPM article resolves to **111** (Semantic Scholar by DOI `10.3905/jpm.2005.470578`, checked 2026-11-22)."
sample_period: "daily prices; the simulation section covers 1997–2001 and the DJIA sections run from the early 1990s to 2002. Dated figures in the source are deliberately not recorded here."
markets: "DJIA constituents, plus randomly drawn sub-baskets of FTSE 100, CAC 40 and S&P 100 constituents used to build 300 synthetic equal-price-weighted indices"
tier: "C in use. The construction is described completely and the pair's companion article is tier 1, but three things keep this below B for this lab: the benchmark is **reconstructed from current index membership** (a look-ahead/survivorship benchmark), the central out-performance claim is the paper's own prior result re-simulated rather than independently replicated, and — decisively — the paper's own algebra identifies the source of the excess return as a characteristic this lab has already measured with the **opposite** sign."
validation_overlap: false
published_post_2018: false
read: "Full text (549 KB PDF → 78 KB of text via `pdftotext -layout`, 468 instances of `\" the \"`, no character shift, `( )` dropout check zero). Sections 1–7 intact; tables are marked '[Insert Table 1 here]' and are **not** in the extracted text, which is convenient here — every claim below comes from the prose and the algebra."
---

## Access

**`efmaefm.org/AcceptedPapers<YEAR>/<AuthorNames>/<AuthorNames>.pdf` is a working channel and is
nominated, which partly reverses a standing entry.** This folder carries the EFMA 2016
abnormal-turnover paper as *permanently unobtained* on the evidence of an HTTP 404 with a 13-byte
body. That verdict was about **one paper**, not the host: the 2003 accepted-papers tree served a
genuine 549 KB PDF at HTTP 200 on the first request with no challenge. EFMA's conference archive is
the right route for an **ISMA/ICMA Centre discussion paper**, a class whose original home
(`icmacentre.ac.uk/pdf/discussion/<id>.pdf`) now returns a 404 HTML page.

Two refusals recorded from the same hunt. **CentAUR (`centaur.reading.ac.uk`) holds records
without files** for both Alexander–Dimitriu JPM articles — an HTTP 200 landing page whose only PDF
links are the repository's own end-user agreement and citing guide. That is the Pure/DSpace
"record without a bitstream" mode from [2026-10-04], now observed on EPrints. And
**`carolalexander.org` returns HTTP 403 with a 166-byte body** to an automated client, so the
author-page lesson does not hold for this author.

A note on what was *not* obtained: the paper this folder actually wanted is the pair's
*The Cointegration Alpha: Enhanced Index Tracking and Long-Short Equity Market Neutral Strategies*
(ISMA DP2002-08), which is the full treatment of the construction below. RePEc prints its
discussion-paper URL in full and that URL is dead. It is a **named unobtained pointer**, worth
re-hunting only if an ICMA mirror appears — and, given the refusal below, it is not worth much.

## Mechanism

The claim is that a portfolio constructed to be **cointegrated** with an index, rather than merely
correlated with it, is a better tracker, and — the part that makes it a statistical-arbitrage
object rather than an indexing one — that such a portfolio earns a **positive excess return over
the index it tracks**, which is counter-intuitive because the most complete, most strongly
cointegrated basket ought to deliver a zero-mean tracking error.

The authors' stated rationale for preferring cointegration has three parts, and they are worth
keeping even if the return claim is refused:

1. If the index and the basket are cointegrated, the tracking error is **stationary by
   construction** — it mean-reverts rather than wandering, which is the property a tracker actually
   wants and which a correlation-based construction does not deliver.
2. Weights estimated from a long history of **price levels** are more stable than weights
   estimated from returns, because the level regression uses information that differencing throws
   away.
3. Cointegration with an index should be easy to find, since an index — equal- or
   capitalisation-weighted — is itself a linear combination of its constituents' prices.

**The second mechanism in the paper, and the one that condemns it.** Section 2 works through the
two-stock case and reaches a clean algebraic result: in a cointegrating regression of the log index
on log prices, **the stock with the higher price receives a higher weight than its index weight**,
and the gap between the tracking weights and the index weights *grows with the dispersion of the
constituents' prices*. The authors treat this as motivation for their new dispersion measure. Read
as a statement about what the portfolio is betting on, it says something sharper: a
cointegration-optimal tracker is, mechanically, a **tilt towards high nominal price**, scaled by
cross-sectional price dispersion. The excess return the paper reports is that tilt's return.

The paper's third object is the dispersion measure itself — `index dispersion`, the cross-sectional
standard deviation of constituent prices around their mean — which they relate to tracking
out-performance through a two-state Markov switching model. That part is regime-timing and is
outside what this lab trades; it is recorded here only so a later session does not re-find it.

## Construction recipe

**The tracking portfolio.** Over a rolling calibration window, estimate by OLS

    ln(index_t) = c₁ + Σ_{k=1..n} c_{k+1} · ln(P_{k,t}) + ε_t

then **normalise the fitted coefficients to sum to one**; those normalised coefficients are the
portfolio weights. Details the paper is explicit about:

- **Calibration window**: a fixed-length rolling window of **three to five years of daily data**.
  The authors argue the window must be at least three years for the Engle–Granger machinery to
  behave.
- **Rebalance cadence**: every **10 trading days**, re-estimating the regression on the new window
  and resetting weights to the new normalised coefficients.
- **Between rebalances**: hold **share counts** constant — the book drifts with prices and is not
  re-weighted. (This matches protocol v3's drift convention exactly.)
- **Log formulation on purpose**: specifying in logs means that, *provided the tracking error is
  stationary*, the first difference gives a portfolio whose expected return equals the index's.
  The stationarity proviso is load-bearing and is not optional.
- **Cointegration must be tested, not assumed.** OLS on non-stationary dependent variables is
  only valid in the cointegrated case; if the residuals are non-stationary the coefficients are not
  consistent and no inference from them is valid. They use **Engle–Granger (1986)** two-step
  testing and defend it here on the grounds that its usual limitations do not bite: the window is
  long, there is an economic reason to put the index on the left-hand side, and one cointegrating
  vector suffices.
- **Variants the companion paper swept**: number of stocks in the basket, the stock-selection rule,
  the spread between the tracked benchmark and the index, and the calibration length.

**The dispersion measure.** With all constituent prices rescaled to 100 at the start of the period,

    d_t = sqrt( Σ_k ( (P_{k,t} − I_t) / I_t )² / n )

where `I_t` is the equal-weighted average of the rescaled prices.

**The synthetic-index experiment, which is a method worth copying.** To test whether the
out-performance generalises beyond the DJIA, the authors drew **100 random fixed-size baskets** from
each of three national-index universes, defined an equal-price-weighted index for each basket, and
tracked each of the 300 synthetic indices with a cointegration-optimal portfolio of its own
constituents. That is a randomised-construction null in the sense of the [2026-11-20] placebo
lesson — except that here it is used to *confirm* the effect rather than to price it down, and the
confirmation is exactly what the refusal below reinterprets.

## Robustness evidence (qualitative only)

- **Cross-market breadth of a kind.** The effect is reported in four universes (one real, three
  synthetic) with basket sizes from 25 to 80, which the authors read as showing the result is not
  a DJIA artefact.
- **But the breadth is not independent of the mechanism.** Every one of the 300 synthetic indices
  is **equal-price-weighted**, and the tracker's tilt (above) is towards high nominal price. A
  construction whose tilt is defined relative to a price-weighted benchmark, tested against
  price-weighted benchmarks in every case, has not been tested across mechanisms — it has been
  tested four times on the same one. The authors' own algebra predicts the result they then
  report as independent confirmation.
- **Time variability is the paper's own headline finding**: the out-performance is concentrated in
  part of the sample, which is what motivates the regime model. A construction whose edge is
  concentrated in a subperiod and explained by a fitted two-state model afterwards is, in this
  folder's terms, a subperiod-instability finding reported as a regime discovery.
- **The benchmark is reconstructed from current membership.** The paper states that the index is
  "reconstructed historically based on the current membership of the market index". That is the
  look-ahead benchmark this folder already has a note on: the basket is built from names known to
  have survived to the construction date, and both the tracking quality and the excess return are
  measured against a benchmark with the same bias.
- **Costs.** Rebalancing every 10 trading days on a full-constituent basket is heavy turnover, and
  the extracted prose carries no cost model. Treat every reported figure as gross.
- **Replication status.** No independent replication is known to this folder. The companion JPM
  article's own abstract (read at second hand through indexing records, not quoted here) reports
  the weaker conclusion that for simple index tracking cointegration offers no clear advantage over
  tracking-error-variance methods, with an advantage appearing only when tracking is made harder —
  i.e. **the pair's own peer-reviewed statement is more modest than this working paper's**. Prefer
  the published statement.

## Implementability here

**The construction is implementable and should not be implemented. The reason is a measurement
this lab already has, and it costs nothing to apply.**

The mechanical content of a cointegration-optimal tracker is a tilt towards **high nominal price**,
growing with cross-sectional price dispersion (Mechanism, above — this is the source's algebra, not
an inference about it). The lab's own nightly measured the **log price level** as a cross-sectional
score and found its one-bit information coefficient running **−0.030 → −0.051 → −0.073 → −0.109 →
−0.150** across horizons from 21 to 504 days, with the standing recommendation that any screen
beyond 63 days must partial out the log price level within region. So:

1. The tilt this construction imposes is **the wrong sign at every horizon the lab has measured**,
   and it gets worse as the horizon lengthens — while this construction's calibration window is
   three to five years.
2. Correcting it as the standing recommendation requires — partialling out the log price level
   within region — **removes the tilt that generates the reported excess return**. There is nothing
   left to test.
3. The panel makes it worse, not better. Nominal price conventions differ across this universe's
   markets by roughly three orders of magnitude, so a regression on raw log prices across a global
   panel loads on a listing convention rather than on anything about the companies. The correct
   construction would be within-region, which fragments the cointegrating regression into nine
   small ones.

Three further obstacles, any one of which would be enough on its own:

4. **OLS coefficients are not non-negative.** Nothing in the method constrains the fitted weights
   to be positive, and normalising them to sum to one does not fix that. A long-only version is a
   *different* estimator — a non-negative least squares on log levels — with none of the paper's
   cointegration argument behind it. This folder's `long-only-as-ℓ1-regularization` note is the
   relevant frame: imposing non-negativity is a regularisation that changes the object, not a
   detail.
5. **Rebalancing every 10 trading days is inside the lab's 21-day cost wall**, on a basket holding
   every constituent, with v3 charging 15–40 bps per side plus UK, HK, French, Italian and Spanish
   transaction taxes. The two companion notes from tonight both point the other way — one of them
   found slower rebalancing better *gross* of costs.
6. **The dispersion measure is not a well-defined characteristic.** `d_t` is computed after
   rescaling all prices to 100 at the start of the period, so its level is a function of
   **time elapsed since the arbitrary rebasing date** — prices diverge from a common start, so `d_t`
   trends upward mechanically. Any regression of anything on `d_t` is partly a regression on a
   clock. A usable version would have to be scale-free and rebase-free (a cross-sectional
   dispersion of *returns* or of log-price *changes*), at which point it is the dispersion object
   this folder already holds notes on.

**What is worth keeping.** Two things, both construction hygiene rather than signal. (i) The
**stationarity requirement**: if a book is built to track a benchmark, the right property to test is
that the tracking error mean-reverts, not that it is small on average — and that is a testable
property of any candidate's active return series, free, with no holdout. (ii) The **synthetic-index
randomisation** as a method: building many random benchmarks from the same universe and running the
same construction against each is a legitimate null, and it is the same instrument as the lab's own
`benchmarks.random_null_v3` pointed at the *benchmark* rather than at the book.

## Related

- The nominal-price-level vein in `research/SUMMARY.md` (candidate items `#420`–`#426`), closed by
  the lab's own measurement — the ground on which this construction is refused.
- `notes/2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` and
  `notes/2026-11-09-the-nominal-share-price-puzzle-and-the-price-norm.md` — what a price-weighted
  benchmark does to a measured cross-section, which is what all 300 synthetic indices here are.
- `notes/2026-08-22-long-only-as-l1-regularization.md` — why dropping the non-negativity constraint
  is not a detail.
- `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the reconstructed-from-current-membership
  benchmark, which this source uses and does not flag.
- `notes/2026-09-07-cointegration-pairs-versus-distance-method.md` and
  `notes/2026-09-03-pairs-trading-distance-method.md` — the pairwise cointegration literature; this
  source is its index-level counterpart.
- `notes/2026-11-22-enhanced-indexation-as-a-benchmark-relative-linear-program.md` and
  `notes/2026-11-22-stochastic-dominance-over-the-benchmark-and-the-shortfall-lp.md` — the two
  constructions from the same clause that survive, and the contrast is instructive: both work on
  **excess returns** and are therefore scale-free, while this one works on **price levels** and is
  therefore not.
- `notes/2026-10-22-regime-switching-financial-markets.md` *(the regime literature)* — where the
  paper's second half lives, and which the lab's budget rules cap as `price-trend`.
