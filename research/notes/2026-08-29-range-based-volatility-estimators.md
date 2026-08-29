---
title: "Range-based volatility estimation: the efficiency case and the estimator zoo"
authors: Alizadeh, Brandt, Diebold (2002); Molnár (2012); with Parkinson (1980), Garman–Klass (1980), Rogers–Satchell (1991), Meilijson (2009)
year: 2002 / 2012 (primaries); 1980 / 1980 / 1991 / 2009 (the estimators)
venue: The Journal of Finance 57(3), 1047–1091 (tier 1); International Review of Financial Analysis 23, 20–29 (tier 2); The Journal of Business (tier 1, both 1980 papers); The Annals of Applied Probability (tier 1)
url: https://doi.org/10.1111/1540-6261.00454 · https://doi.org/10.1016/j.irfa.2011.06.012 · https://doi.org/10.1086/296071 · https://doi.org/10.1086/296072 · https://doi.org/10.1214/aoap/1177005835
citations: Alizadeh–Brandt–Diebold — 1245 (Semantic Scholar DOI endpoint, checked 2026-08-29); Molnár — 131 (Semantic Scholar, checked 2026-08-29); Parkinson 1980 — 1449, Garman–Klass 1980 — 1184, Rogers–Satchell 1991 — 419 (all Crossref `is-referenced-by-count`, checked 2026-08-29)
sample_period: Alizadeh–Brandt–Diebold — January 1978 to December 1998; Molnár — 1992–2008, plus simulation
markets: five US-dollar exchange rates, daily (ABD); the 29 Dow Jones Industrial Average constituents as of 2009-01-01, daily OHLC from CRSP, 4,171 observations each (Molnár)
tier: A for the efficiency and distributional results (they are theorems about Brownian motion, not empirical regularities); B for Molnár's estimator-ranking and standardisation results (tier-2 venue, single market, one index's constituents)
validation_overlap: false
published_post_2018: false
read: full text for both primaries — ABD from the author's University of Pennsylvania page (`sas.upenn.edu/~fdiebold/papers/paper33/final.pdf`, the typeset JF article with volume and page headers); Molnár as Chapter 2 of his 2020 habilitation thesis (`kmtp.vse.cz/wp-content/uploads/post/428/Habilitace-Molnar.pdf`), which reproduces the IRFA article complete with its journal header and pagination. Parkinson, Garman–Klass, Rogers–Satchell and Meilijson are recorded **second-hand**: their formulas and efficiencies are taken as restated (with derivations) in Molnár, cross-checked against ABD's independent restatement.
---

## Mechanism

There is no return premium here. This is a **measurement** result, and it is the reason
`program.md` opened `range-variance` as a family at the same time it started passing `high` and
`low` to strategies.

The daily high and low contain intraday sample-path information that the close alone throws away.
The intuition, in ABD's words: on a day when the price swings substantially but by chance closes
near where it opened, the squared or absolute return reports low volatility while the range
correctly reports high. Formally, for a driftless Brownian motion the log range has **about
one-quarter the standard deviation of the log absolute return** as an estimator of log volatility
(0.29 versus 1.11 in ABD's Table I) — both are unbiased in the sense that they move one-for-one
with log volatility on average, but one is far less noisy.

The second, less-known property is distributional. The log absolute return is badly non-Gaussian
(skewness −1.53, kurtosis 6.93); the **log range is almost exactly Gaussian** (skewness 0.17,
kurtosis 2.80). ABD's whole estimation method rests on this: it makes Gaussian quasi-maximum
likelihood correct rather than merely convenient for a latent-volatility state-space model. For
this lab the same fact has a plainer use — a log-range volatility feature is close to normally
distributed and therefore behaves well under linear models and cross-sectional standardisation,
where log |return| does not.

Third: **the range is robust to microstructure noise in a way that high-frequency realised
volatility is not.** Bid-ask bounce inflates the volatility of high-frequency returns without bound
as the sampling frequency rises; it adds at most one spread to the high-minus-low difference,
regardless of how many trades occurred. Molnár makes the offsetting point: infrequent observation
biases the observed range *down* (the true high is not traded), while the spread biases it *up*,
and for liquid instruments both effects are small and partially cancel.

## Construction recipe

Write `c = ln(C) − ln(O)`, `h = ln(H) − ln(O)`, `l = ln(L) − ln(O)` — **all three measured from the
open, not from the previous close**. This is the definition every formula below assumes, and getting
it wrong is the documented failure mode (see pitfalls).

- **Parkinson (1980)** — range only:

      σ²_P = (h − l)² / (4 ln 2)

- **Garman–Klass (1980)** — the practical form the authors themselves recommend, obtained by
  dropping a negligible cross-product term from their minimum-variance analytical estimator:

      σ²_GK = 0.5 (h − l)² − (2 ln 2 − 1) c²

  It has a clean reading as the **minimum-variance combination of the Parkinson estimator and the
  simple squared return**.

- **Rogers–Satchell (1991)** — the only one of the set that permits an arbitrary drift:

      σ²_RS = h(h − c) + l(l − c)

- **Meilijson (2009)** — a four-term combination outside the analytical class, marginally more
  efficient than Garman–Klass.

**Efficiency** (defined as the variance of the simple squared-return estimator divided by the
variance of the estimator, so higher is better; squared return = 1 by construction):

    squared return  1.0
    Parkinson       4.9
    Rogers–Satchell 6.0  (at zero drift; > 2 for any drift)
    Garman–Klass    7.4
    Meilijson       7.7

**What every one of them measures is trading-day volatility, not daily volatility.** All are
derived for a continuously observed price over one session; none sees the overnight gap. Molnár
gives the jump-adjusted Parkinson form (adding `j = ln(O_t) − ln(C_{t−1})`, the opening jump) and
immediately warns that simply adding the jump term raises the estimator's variance when jumps are a
large share of daily return, so the correct adjustment is a *weighted* combination whose optimal
weights depend on the jump share — not an unweighted sum.

**Assumptions behind all of them**: zero drift (except Rogers–Satchell), continuous sampling, no
bid-ask spread, constant volatility within the day. Molnár's judgement, which is the reason to
neglect drift on daily data: for essentially any financial asset the mean daily return is far
smaller than its daily standard deviation, so the zero-drift assumption is a very good approximation
at the daily frequency — and stops being one at annual horizons.

## Robustness evidence (qualitative only)

- **The efficiency and distributional results are theorems**, derived from Feller's distribution of
  the range of a Brownian motion and Karatzas–Shreve's for the absolute value. They do not decay,
  do not depend on a sample, and are not subject to publication bias — an unusual footing for
  anything in this folder. What *is* empirical, and therefore subject to the usual discounts, is
  whether real daily bars behave enough like Brownian motion for them to apply.
- **All the estimators are unbiased for the variance; none is unbiased for the standard
  deviation.** Molnár's first contribution is that taking the square root introduces a bias, and he
  quantifies it. Anything scaling positions by an estimated σ (rather than σ²) inherits it.
- **The estimators rank consistently** — by the mean or the standard deviation of their sampling
  distribution, the order is Meilijson, then Garman–Klass, then Rogers–Satchell, then Parkinson,
  then absolute returns — matching the efficiency table.
- **Being a good variance estimator does not make an estimator a good denominator, and this is the
  paper's most practically useful finding.** Molnár standardises returns by each estimator and
  checks the resulting distribution against the N(0,1) benchmark:
  - **Parkinson** — mechanically correlated with the return it is meant to standardise (the range
    is by construction at least the absolute return, so `|r| / σ_P` is bounded above by
    `sqrt(4 ln 2) ≈ 1.665`; the correlation is 0.79). The standardised distribution has **no tails
    and is bimodal**.
  - **Meilijson** — the same defect, much milder.
  - **Rogers–Satchell** — catastrophic as a denominator: standardised kurtosis ≈ 124 and strong
    spurious skew. Molnár's reading is that its generality (drift independence) works *against* it
    when the drift is in fact zero, because it can land near zero.
  - **Garman–Klass** — subtracting the squared return from the Parkinson term cancels most of the
    correlation with `|r|` (down to 0.36), and the standardised returns come out approximately
    normal. **His conclusion is explicit: of the estimators studied, Garman–Klass is the only one
    appropriate for standardising returns**, and it is the one he uses in his own empirical work.
- **Costs and multiple testing** are not applicable — neither paper proposes a trading strategy.
  Nothing in this note is an alpha claim and it should not be read as one.
- Sample robustness is the cluster's weak spot: ABD's empirics are five FX rates, Molnár's are one
  index's constituents in one market. But the load-bearing claims are analytical, and the empirics
  are only checking them.

## Implementability here

**Fully in scope, and cheaper than anything else the new panel makes possible.** `aux` supplies
`open`, `high`, `low` on exactly the same index and columns as `prices`, so all four estimators are
a handful of vectorised operations with no fitting, no lookback tuning and no extra turnover of
their own. `strategies/lib/features.py` already carries a range-volatility helper.

Two distinct uses, and they call for different estimators:

1. **As a feature to sort on.** The `range-variance` family in `program.md` means constructing
   signals from this — cross-sectional dispersion of range volatility, vol-of-vol, changes in range
   volatility, correlation-regime proxies. Here Garman–Klass or Meilijson are the efficient choices;
   the log of the estimator is the near-Gaussian quantity and is the right thing to
   rank-standardise.
2. **As a denominator — scaling, vol-targeting, inverse-vol weighting, or normalising a return
   feature.** Here Molnár's result binds hard: **use Garman–Klass, not Parkinson, and never
   Rogers–Satchell.** This matters directly because the folder's existing risk-parity and
   vol-targeting notes are all about *what* to divide by and none of them is about *how well the
   divisor is measured*. A range-based σ with roughly 7× the efficiency of a squared-return σ is a
   free improvement in every one of those constructions — which is worth stating precisely because
   `learnings.md` has refuted the *constructions*, not their measurement. **A vol-targeting or
   inverse-vol idea that failed on a close-to-close σ is not automatically reopened by a better σ,
   and `CLAUDE.md`'s rule against carrying constants into a new family by analogy applies: if the
   lab wants to claim measurement was the binding constraint, it has to re-measure, not assume.**

**Known pitfalls, in the order they are likely to bite here.**

- **The `c`, `h`, `l` in every formula are measured from the *open*, not from the previous close.**
  Molnár documents this as a real error in the published literature: substituting
  `ln(C_t) − ln(C_{t−1})` for `c` in the Garman–Klass formula produces a quantity that is
  emphatically not the Garman–Klass estimator (he names two published papers that do it). It is the
  single easiest mistake to make with the panel this repo now passes.
- **The overnight gap is invisible to all of these.** On a global universe with 15 regions, a large
  fraction of each instrument's daily variance is realised while its market is shut. A raw
  Garman–Klass estimate is therefore a systematic *under*-estimate of daily volatility, and the
  size of the under-estimate differs across regions in a way that is correlated with time zone.
  For a **cross-sectional** sort this is a confound; a close-to-close volatility estimate does not
  share it. Either restrict range-based comparisons to instruments in the same session, or carry
  both estimators and treat their ratio (the jump share) as a feature in its own right rather than
  as an error term.
- **Adjustment basis.** `prices` here are USD-adjusted closes. Confirm that `open`, `high` and
  `low` sit on the same adjustment and currency basis before differencing logs — a split or a
  dividend adjustment applied to close but not to high/low turns one day's range into an enormous
  spurious volatility spike. Whatever the panels' actual convention, a candidate should assert it
  rather than assume it, since a single mis-adjusted day dominates a trailing average.
- **Zero and near-zero ranges.** A non-trading day or a stale foreign quote gives `h = l = c = 0`
  and hence σ² = 0. Every one of these estimators is a denominator somewhere downstream; guard it.
- **The square-root bias** is small but real and points the same way for every instrument, so it
  mostly cancels in a *cross-sectional* comparison and mostly does not in a *time-series* target
  (a vol-targeting rule aiming at a fixed annualised number will systematically miss).

## Related

- `2026-08-29-machine-learning-cross-section-comparative.md` — ranks return volatility,
  idiosyncratic volatility and beta as the **third** most informative feature group in a
  thirteen-method horserace, after price trends and liquidity. This note is how to measure that
  group properly from the bar this repo receives.
- `2026-08-17-volatility-timing-managed-portfolios.md`,
  `2026-08-18-risk-parity-equal-risk-contribution.md` — the constructions that divide by a
  volatility estimate. Both were measured on close-to-close volatility; neither is reopened by this
  note, but both have a measurement input this note improves.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md` — `ILLIQ`'s numerator is an absolute
  return, so it is partly a volatility measure; a range-based volatility control is the natural way
  to separate the two, and is what Amihud's own factor construction does.
- `2026-08-23-statistics-of-sharpe-ratios.md` — the other place in this folder where the sampling
  distribution of a volatility estimate, rather than its point value, is the object of interest.
