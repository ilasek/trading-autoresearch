---
title: "Principal Components as a Measure of Systemic Risk — the absorption ratio, i.e. the spectrum read as a time series rather than once"
authors: Kritzman, Li, Page, Rigobon
year: 2011
venue: The Journal of Portfolio Management 37(4), 112–126 (venue tier 1 on this folder's rubric, which lists JPM among the top peer-reviewed journals; the authors are practitioners at Windham/State Street with two MIT Sloan affiliations). The version read is MIT Sloan Working Paper 4785-10.
url: https://doi.org/10.3905/jpm.2011.37.4.112
citations: 366 (Semantic Scholar by DOI, checked 2026-10-06); 309 (OpenAlex by DOI, same date); 251 (Crossref `is-referenced-by-count`, same date). Three indexes, three different numbers, all in the same band — no "lone low count" problem here.
sample_period: US industry panel 1998–2010, with covariance estimation beginning 1995; global country panel 1995–2009
markets: 51 US industries inside the MSCI USA index; separately 42 country equity indexes plus some regional indexes; separately a US housing panel
tier: B
validation_overlap: false
published_post_2018: false
read: full text of MIT Sloan Working Paper 4785-10 (this version 28 June 2010) from `web.mit.edu/finlunch/Fall10/PCASystemicRisk.pdf`, served first try, parsed cleanly with `pdftotext -layout` (57 KB of text, `( )` grep clean). Equation (1) is one of several display equations that did not survive extraction; **its content is given completely in words and symbol definitions in the surrounding prose** and is restated below from that prose, not from memory. Equations (2) and (3) extracted. The published JPM version was not fetched: `pm-research.com` refuses an automated client by redirecting into an OpenID flow, as `research/README.md` records.
---

## Mechanism

There is no return premium claimed here. The object is a **state variable**, and the claim is about
*fragility* rather than about expected return: when the variance of a panel of assets is absorbed by
few directions, the assets are tightly coupled, and a shock to one of them propagates to all of them.
When variance is spread across many directions, the same shock stays local. The authors are explicit
that a high reading is **not** a forecast of a loss — it is a statement that the system is in a
condition where a loss, if one arrives, will be broad.

The statistic is the fraction of a panel's total variance explained by the first `n` eigenvectors of
its covariance matrix, computed on a rolling window so that it becomes a time series. The economic
content sits entirely in the *change*: the authors use a standardized shift of the ratio against its
own trailing level, never its raw level, for every claim about subsequent returns.

**The one comparison that justifies the statistic's existence, and it is the reason this note is in
`range-variance` rather than in `portfolio-learning`.** The obvious competitor is average pairwise
correlation, and the authors argue — with a two-period constructed example, not with data — that
average correlation is the wrong summary because it **weights every pair equally regardless of how
much variance that pair carries**. Their example has the correlation between two high-volatility
assets rise and the correlation between two low-volatility assets fall, with the average correlation
falling slightly while the absorption ratio rises sharply. The absorption ratio is computed on the
**covariance** matrix, so a correlation increase among the names that carry the variance moves it and
a correlation increase among the quiet names barely does. That is the whole distinction, it is
arithmetic rather than empirical, and it is the thing to carry: *a co-movement state variable built
on a correlation matrix and one built on a covariance matrix are different objects, and only the
second is weighted by what the portfolio's risk actually comes from.*

## Construction recipe

Enough to implement without re-reading.

**The ratio.** With `N` assets and `n` retained eigenvectors,

    AR = ( Σ_{i=1..n} σ²_{E_i} ) / ( Σ_{j=1..N} σ²_{A_j} )

where `σ²_{E_i}` is the variance of the `i`-th eigenportfolio (the `i`-th eigenvalue of the
covariance matrix) and `σ²_{A_j}` is the variance of the `j`-th asset. Note the denominator: it is the
**sum of the individual asset variances**, i.e. the trace, so `AR` is the share of total variance in
the leading subspace. High `AR` → compact, fragile; low `AR` → disparate.

**The four parameters, as the authors set them.**

- **Window**: 500 trading days of daily returns to estimate the covariance matrix and its
  eigenvectors.
- **Weighting inside the window**: both the eigenvalue variances and the asset variances are
  computed with **exponential weighting, half-life = half the window = 250 days.**
- **How many eigenvectors**: `n ≈ N/5`, fixed. For their 51-industry US panel that is 10. They say
  in a footnote that `n` should in principle be conditioned on the rank of the covariance matrix and
  that their matrices are near full rank, so fixing it is equivalent here. They also say plainly that
  fixing the *number* of eigenvectors rather than fixing a target *percentage of variance* was chosen
  "for no particular reason" — i.e. this parameter is asserted, not optimised.
- **The signal, which is a standardized shift and not a level** (their equation (2)):

      ΔAR = ( AR_15day − AR_1year ) / σ( AR_1year )

  the 15-day moving average of `AR` minus its one-year moving average, divided by the standard
  deviation of the one-year moving average. Their decision thresholds are `ΔAR > +1` and `ΔAR < −1`.

**The timing rule they test** (recorded as a construction, with its results deliberately omitted —
see the anti-lookahead note below). Start from a 50/50 stock/bond portfolio. Go to 100% stocks after
`ΔAR < −1σ`; go to 0% stocks after `ΔAR > +1σ`; hold 50/50 in between. Applied daily with a
**one-day lag after the signal**. Because ±1σ events are rare, the rule fires only a couple of times
a year — the authors report a trade count of under two per year — so it is a *very* low-turnover
overlay by construction. Warm-up: two years to estimate the covariance matrix and eigenvectors plus
one more year to estimate the standard deviation of the one-year moving average, i.e. **three years
of history before the first signal.**

**The rejected variant, and it is the part of this paper most directly useful to this lab.** The
appendix tests the obvious alternative of summarising the whole spectrum instead of truncating it: a
Herfindahl-style statistic (their equation (3)) that squares each eigenvector's share of total
variance, sums the squares and takes the square root. They report it is **significantly less
informative** than the top-`n` share and conjecture why: *the less important eigenvectors, which the
Herfindahl index includes and the top-`n` share excludes, are relatively unstable and inject noise
into the estimate.*

**A second, independent statistic defined in the same paper** (their turbulence index, attributed to
Kritzman–Li 2010 in the FAJ, which was **not** read): the Mahalanobis distance of a return vector
from its own history,

    d_t = (y_t − μ) Σ⁻¹ (y_t − μ)'

with `y_t` the period's asset-return vector and `μ`, `Σ` the historical mean vector and covariance
matrix. The authors' own description of what it measures is useful and is three things at once:
unusually large moves, **decoupling of normally correlated assets**, and **convergence of normally
uncorrelated assets**. It is scale-free by construction. They use it only as the event definition for
an event study, not as a signal.

## Robustness evidence (qualitative only)

Honest reading, and it is why this is Tier B and not Tier A.

- **The sample is one episode, not multiple decades.** The US industry analysis covers roughly a
  dozen years and the global analysis about fifteen. On this folder's rubric that fails "multi-decade,
  multi-market, subperiod stability" outright. There is no subperiod split anywhere in the paper.
- **No independent replication is cited and none is claimed.** The closest thing is a
  contemporaneous and independent application of principal components to financial-industry returns
  (Billio–Getmansky–Lo–Pelizzon), which the authors discuss as a two-regime comparison and
  distinguish from their own rolling-window approach precisely on the grounds that fixing two
  periods assumes stationarity within each.
- **Costs are not modelled** in the timing test; turnover and a trade count are reported and then
  not priced.
- **Multiple testing is not acknowledged.** Four construction parameters (window, half-life,
  eigenvector count, threshold) and one 15-day/1-year pair are each asserted once. The only
  alternative specification examined anywhere is the Herfindahl variant in the appendix.
- **Cross-panel consistency is the strongest thing on offer**: the same statistic is computed on US
  industries, on 42 country indexes, and on a housing panel, and the authors report it behaves
  comparably on all three. That is weak evidence of generality but it is the right kind.
- **The sign asymmetry is stated as a mechanism, not fitted**: a high reading is described as a
  *near-necessary but not sufficient* condition for a broad decline. The authors say explicitly that
  in many instances prices rose after a spike. Treat the statistic as a conditioner, not a predictor.

**Anti-lookahead: every performance figure, drawdown fraction, event date and episode narrative in
this paper has been deliberately left out of this note**, including the paper's own summary claims
about which historical episodes the ratio anticipated. The paper's sample ends in 2010 so none of it
touches this lab's validation window, but the figures are period-specific by construction and the
folder's rule is the folder's rule. What is recorded above is arithmetic, parameter choices and the
authors' stated mechanism.

## Implementability here

**The statistic is free, exactly computable on this universe, and nothing in it needs data this repo
does not have.** It is a rolling PCA of the daily close-to-close return panel: 140-odd instruments,
`n ≈ 28` eigenvectors at the paper's `N/5` rule, a 500-day window with a 250-day half-life. Cost per
rebalance date is one eigendecomposition of a 140×140 matrix, which is milliseconds; the ~60s/call
budget in `CLAUDE.md` is not a constraint even at a daily grid. `Q = T/N = 500/140 ≈ 3.6`, which is
the comfortable end of the Marchenko–Pastur regime the folder already has a note on — the top of the
spectrum is estimable at this `Q`, which is the part `AR` uses.

**Three adaptations this universe forces, and one it invites.**

1. **The global panel is the better fit, not the industry one.** The paper's own global version uses
   42 country equity indexes — this universe spans 15 regions and holds 42 ETFs, so the natural
   construction is `AR` over the **ETF sleeve** rather than over single names. That also sidesteps the
   survivorship problem: `program.md` says ETF-level strategies suffer least from current-constituent
   bias, and a co-movement statistic computed on 140 surviving mega-caps is exactly the kind of
   measurement the folder's survival-conditioning notes say to distrust.
2. **Non-synchronous closes will bias the ratio downward on a 15-region panel.** Daily returns across
   time zones under-measure contemporaneous co-movement, so `AR` computed on a global daily panel is
   mechanically lower than the same panel's true co-movement — and worse, the bias is not constant
   across the window if region weights move. `notes/2026-09-08-nonsynchronous-trading-econometrics.md`
   is the relevant machinery. The paper, built on one country's industries and on country indexes
   each measured in its own session, never confronts this.
3. **Use the standardized shift, never the level.** This is the paper's own practice, and it is doubly
   required here: on a panel whose composition and region weights are fixed but whose underlying
   co-movement regime drifts over decades, a fixed threshold on `AR`'s level is not comparable across
   time. See the CLMX note from tonight for the direct evidence that panel-wide co-movement levels are
   not stationary over multi-decade samples.
4. **The invitation: this is a feature, not only an overlay.** The lab's `statistical-learning` family
   takes cross-sectional features; `AR` and `ΔAR` are panel-level time-series state variables, which is
   a different shape and can only enter as a conditioner or as an interaction. The cheapest honest use
   is as a **diagnostic on the champion's own returns** — does the champion's realised risk or its
   drawdown concentration line up with `ΔAR`? — which scores no returns and costs no trial.

**The pitfall that matters most, and it is a refutation this lab already owns.** The paper's
application is a **de-risking overlay that exits to cash/bonds on a state variable**, and
`experiments/learnings.md` opens with "de-risking overlays on momentum reliably backfire
out-of-sample", established on three distinct attempts (inverse-vol + vol targeting, per-asset 200dma
trend filter, binary SPY-trend regime switch), all of which cut train drawdown and lost validation
Sharpe to dilution and whipsaw. The 2026-09-17 entry sharpens it: *every* refuted de-risking overlay
timed the book on an **external** state variable — trend, vol spike, drawdown depth, SPY regime — and
`ΔAR` is a fourth external state variable of exactly that class. **An `AR` overlay is therefore the
default-refuted idea here and must not be proposed as though the literature licensed it.**

What is *different* about it is narrow and specific, and it is worth stating precisely because the
difference is measurable rather than rhetorical: the three refuted overlays all traded often, and the
lab's own [2026-09-02] measurement established that **the cost of an overlay is set by the number of
boundary crossings, not by the fraction of time it is out** — a monthly in/out overlay costs ~24× of
annual turnover and must avoid more than ~3.6%/yr to pay for itself. A ±1σ rule on `ΔAR` crosses on
the order of **twice a year**, so its cost is roughly an order of magnitude smaller. That reasoning
is mine, not the lab's and not the paper's: the 3.6%/yr figure was measured for a monthly calendar
overlay on the equal-weight universe, and rescaling it by crossing count is the natural reading of the
lab's own rule but **has not been measured.** The precondition is a free one and belongs before any
trial. See candidates **#204** and **#205**.

**The Herfindahl finding is the single most directly useful thing in this paper for this lab, and it
has nothing to do with timing.** The 2026-09-26 nightly ran an inverse-Herfindahl effective-rank
statistic on a characteristic-managed second-moment matrix and found it read anything from 0.208·P to
0.638·P depending on which near-duplicate columns went in, with an i.i.d. control at 0.775·P and a
placebo at 0.875·P. This paper tested the Herfindahl form against the top-`n` share on a real panel
and reports the Herfindahl form is **less informative**, attributing it to instability in the small
eigenvalues — which is independently exactly what
`notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md` proves must happen, since
the bottom of an estimated spectrum is where the noise lives and a Herfindahl sum weights it in.
**Two Tier-A/B sources and the lab's own measurement now agree that a whole-spectrum concentration
statistic is the wrong summary and a truncated top-`n` share is the right one.** That is a free
re-specification of a screen the lab has already run and found uninterpretable. See candidate **#203**.

## Related

- `notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md` — the null this statistic
  should be read against, and the theorem that makes the Herfindahl finding above predictable rather
  than surprising. `AR` at `Q ≈ 3.6` uses the top of the spectrum, which is the estimable part.
- `notes/2026-09-27-counting-factors-eigenvalue-estimators.md` and
  `notes/2026-09-27-nonlinear-shrinkage-instead-of-counting.md` — the same spectrum read for a *count*
  and for a *shrinkage*; this note reads it for a *level through time*, which is the third use and the
  one with no prior note.
- `notes/2026-10-06-betaless-variance-decomposition-and-average-correlation.md` — tonight's companion,
  and the direct rival summary: average correlation ≈ average market-model R², with the non-stationarity
  that forces the standardized-shift form above.
- `notes/2026-09-08-nonsynchronous-trading-econometrics.md` — the downward bias on a 15-region daily
  panel.
- `notes/2026-08-17-volatility-timing-managed-portfolios.md` and
  `notes/2026-09-21-volatility-targeting-impact-and-the-momentum-overlay.md` — the state-variable
  overlay literature this joins, and which this lab has repeatedly refuted.
- `experiments/learnings.md`: the opening "de-risking overlays reliably backfire" entry (three refuted
  attempts), the [2026-09-17] generalisation to external state variables, and the [2026-09-02]
  boundary-crossing cost rule that is the only quantitative reason to look again.
- Kritzman & Li, "Skulls, Financial Turbulence, and Risk Management", FAJ 66(5), 30–41, 2010,
  `10.2469/faj.v66.n5.3` — **not read**, CFA Institute's site is closed to this client. The turbulence
  index above is taken from its restatement inside the primary and nothing else is claimed for it.
