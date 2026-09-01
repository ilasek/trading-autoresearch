---
title: "Dissecting Characteristics Nonparametrically"
authors: Freyberger, Neuhierl, Weber
year: 2020 (RFS 33(5), 2326–2377; circulated as NBER WP 23227, March 2017)
venue: The Review of Financial Studies (Tier 1)
url: https://doi.org/10.1093/rfs/hhz123 — NBER draft read at https://www.nber.org/papers/w23227
citations: 635 (OpenAlex by DOI, checked 2026-09-01; the Semantic Scholar DOI endpoint returns "not found" for this DOI)
sample_period: July 1963 – June 2015 (some tables to June 2014); out-of-sample exercise begins after a model-selection step that ends in December 1990
markets: US common stocks (CRSP/Compustat), single market
tier: B
validation_overlap: false
published_post_2018: true
---

Read **in full** from the NBER working-paper PDF (`nber.org/system/files/working_papers/w23227`),
March 2017 draft, including the appendix table of selected characteristics and the variable
definitions. The published RFS version is the citable one and its metadata is recorded above.

**Graded B, and the reason is narrow.** On venue, citation count, method and honesty about model
selection this is a Tier A source. It loses the grade on two of the rubric's four robustness
signals: it is **single-market** (US only) and it models **no transaction costs at all**, while
its headline object is an equally-weighted extreme-decile long/short book rebalanced **monthly**
— the single most cost-exposed construction in the literature. Every performance claim in it is
gross. Read it for *which characteristics survive conditioning* and for *what functional form
buys*, not for magnitudes.

This is a `statistical-learning` note, and it is filed because of one table: the authors re-run
their selection **restricted to large firms**, and this repo's ~145-instrument universe of global
large caps is the closest thing it has to that subsample.

## Mechanism

There is no economic effect here. The paper answers Cochrane's "multidimensional challenge" —
*which characteristics really provide independent information about average returns, and which
are subsumed by others?* — with a method, and the method's output is a **shortlist**.

The two standard tools both fail at this question for structural reasons the paper is explicit
about. Conditional portfolio sorts hit the curse of dimensionality past two or three
characteristics. Linear Fama–MacBeth regressions impose a functional form that is wrong (the
relation between a characteristic's rank and expected return is generally not a straight line)
and are sensitive to outliers in the characteristic.

The proposed estimator: model expected return as an **additive** function of the individual
characteristics, each entered as a **quadratic spline** over its cross-sectional rank, and select
which characteristics enter using an **adaptive group LASSO** (each characteristic's whole spline
basis is one group, so a characteristic is either in or out as a unit). Ranks rather than raw
values make it insensitive to outliers; the spline lets each characteristic's contribution bend;
the group penalty does the selection. The estimator has a model-selection consistency property —
under its assumptions it recovers the true set of relevant characteristics with probability
approaching one.

**The result with the most content is a negative one.** Of 36 candidate characteristics — the
usual zoo of size, book-to-market, beta, profitability, accruals, investment, past-return
predictors, volatility and volume measures — **most do not survive conditioning on the others**.
This is the same message this folder already holds from the machine-learning-comparative
literature, arrived at by a completely different route: the dominant signals are few.

## Construction recipe

*This is a selection procedure and a shortlist, not a strategy.*

**Procedure.** Cross-sectionally rank each characteristic each month; fit an additive quadratic
spline model of next-month return on the ranks; penalise with an adaptive group LASSO, one group
per characteristic; the selected set is the answer. The authors use knot counts from 4 to 19 and
report the selection across all of them, which is the right robustness display for a method whose
output *is* a set.

**The shortlists, which are the reusable content:**

- **All stocks, full sample:** 15 of 36 characteristics survive. Among them and computable from
  daily price/volume data alone: **idiosyncratic volatility, lagged turnover, closeness to the
  52-week high, momentum, short-term reversal, long-term reversal, standardized unexplained
  volume**, plus lagged market capitalisation. The rest are accounting variables.
- **Restricted to firms above the 10% NYSE size breakpoint:** assets-to-market-cap, total assets,
  beta, fixed-costs-to-sales and **idiosyncratic volatility lose their incremental power**.
- **Above the 20% breakpoint:** capital intensity, earnings-to-price, **lagged turnover** and
  **momentum** also drop out; *intermediate* momentum enters.
- **Above the 50% breakpoint — the largest firms, and the subsample closest to this repo — only
  seven characteristics retain incremental predictive power**, and the ones named are the
  book-to-market ratio, **closeness to the high price**, **past-return-based predictors**,
  SG&A-to-market-cap, and **standardized unexplained volume**.
- **Most consistent across every specification, sample half, knot count and size cut:** *size,
  closeness to the previous 52-week high, short-term reversal, and standardized unexplained
  volume.* Three of those four are computable from daily bars.

**Definitions worth copying exactly:**

- **Standardized unexplained volume (SUV)**, following Garfinkel (2009). Over the previous month,
  regress **daily volume** on a constant and on the **absolute values of positive and negative
  daily returns entered separately** (i.e. two regressors: `max(r,0)` in absolute value and
  `|min(r,0)|`, allowing volume to respond asymmetrically to up- and down-moves). SUV is the sum
  of the residuals — volume *not* explained by the size and sign of that day's price move —
  standardized by the standard deviation of the regression residuals. It is a measure of trading
  activity that is **orthogonal by construction to contemporaneous price movement**.
- **Closeness to the 52-week high**: current price divided by the highest price over the trailing
  52 weeks. Note that in this paper it enters *conditional on* momentum, reversal and the other
  survivors — it is not being proposed as a better momentum score.
- **Intermediate momentum**: the return over months t−12 to t−7, skipping the recent window.

**The functional-form finding, stated carefully.** In their out-of-sample design (select once on
data through 1990, then roll a 10-year estimation window forward one month at a time and predict
one month ahead), the nonparametric model selected **eight** characteristics and the linear model
selected **twenty-one** — and the model with fewer characteristics did better out of sample. Two
diagnostic runs pin down why: giving the *nonparametric* estimator the linear model's 21
characteristics improves out-of-sample performance, while giving the *linear* estimator the
nonparametric model's 8 characteristics produces a result identical to its own 21. **The gain is
in the functional form, not in the characteristic count**, and the linear model's extra
characteristics are it overfitting in sample. That is a much sharper claim than "nonlinearities
matter" and it is the one to carry.

## Robustness evidence (qualitative only)

- **Multi-decade single-market sample**, with the selection reported across three knot counts and
  four size cuts, which is the relevant robustness axis for a selection method.
- **Substantial instability across sample halves.** Fewer characteristics are selected in the
  earlier half than the later half; every characteristic selected in the earlier half is also
  selected in the later one, plus additional ones. The authors also document substantial time
  variation in individual characteristics' conditional predictive power, with size the most
  stable. **A shortlist from this method is not a constant** — treat the intersection across
  specifications (the four "most consistent" above) as the durable part and the rest as
  sample-dependent.
- **Single market. No cross-country evidence at all.** This folder's own
  `2026-08-28-local-versus-global-factor-construction.md` is the standing warning about importing
  a US-only characteristic shortlist into a 15-region universe.
- **No costs, and the construction is the expensive kind.** See the grading note above.
- **Replication status:** not covered by Hou–Xue–Zhang or Jensen–Kelly–Pedersen, both of which
  assay individual anomalies rather than selection methods. The method itself has been widely
  cited and re-used; its specific shortlist has not, to this note's knowledge, been independently
  re-derived.

## Implementability here

**The single most useful thing in this source for this lab is the large-firm restriction**, and
it should be read as a warning before it is read as an opportunity.

**The warning.** As the universe moves up in size, characteristics drop out — and the ones that
drop out include several the lab has spent trials or screens on. **Idiosyncratic volatility loses
its incremental power at the *first* size cut.** **Lagged turnover and momentum lose theirs at
the second.** This is independent, out-of-sample-in-the-relevant-sense corroboration of three
results this lab measured on its own universe and recorded as puzzling or disappointing: the
`liquidity-volume` volume nulls (log ADV a clean null at t = +0.11; relative volume null at every
horizon), the repeated failure of volatility-level sorts, and the general difficulty of beating
the incumbent inside `price-trend`. **A ~145-name large-cap universe is exactly where this source
predicts most characteristics stop working**, and that prediction has now been confirmed here
several times without the lab having a reason for it. This is the reason.

**The opportunity, and there is one specific one.** Of the characteristics that survive at the
largest size cut, most need fundamentals and are out of scope. **Standardized unexplained volume
does not** — it needs daily volume and daily returns, both of which this repo has had since
2026-08-29. And SUV is not among the volume functionals the lab has screened. The record shows
`ILLIQ`, ratio-of-means Amihud, the constant-Amihud `A_C`, log average dollar volume, and
relative volume — **every one of them a function of the volume *level* or of volume scaled by a
price move.** SUV is a *residual*: volume conditioned on the price move that would normally
explain it. That is a different object from all five, in the same way that the note above argues
the upper-tail statistic is a different object from the eight width statistics.

Concretely, and cheapest first:

1. **Free screen.** Compute SUV on the train split. Check `spearman(SUV, log ADV)` and
   `spearman(SUV, |return|)` first — if SUV is 0.9-correlated with a functional the lab has
   already nulled, the family closes properly for the third time, exactly as `A_C` did on
   2026-08-31 by the pre-registered rule. If it is genuinely orthogonal, measure its information
   coefficient at 5/21/63 days and apply screen (iii) of `SUMMARY.md` #52 (horizon decay).
2. **The 52-week-high tension is live and the lab's refutation does not close it.**
   `experiments/learnings.md` records 52-week-high proximity as "tried and refuted", but reading
   the entry: it was swapped in as a **drop-in replacement for the champion's return-magnitude
   z-score inside the same buffer-band machinery**, and it failed because the bounded `(0,1]`
   ratio clusters near 1 and doubled turnover. That is a refutation of *one construction*, and
   the lab's own entry says so. This source finds closeness-to-the-high surviving **conditional
   on momentum, short-term reversal and long-term reversal**, i.e. as an *additional* signal
   rather than a better momentum score — which is precisely the use the lab's refutation did not
   test. The turnover objection is also construction-specific and has a known fix in this repo:
   rank the signal and feed it to the max-of-z integration rather than to a buffer band.
3. **The functional-form result argues for a specific kind of learned candidate, and against the
   kind the lab has already ruled out.** `experiments/learnings.md`'s standing design rule is
   that a learned candidate earns a trial only when it is asked for something a sort cannot
   express. This source says what that something is: **the shape of one characteristic's relation
   to return**, not an interaction and not a better ranking. A monotone rank sort is a specific
   and probably wrong functional form; a spline in the rank of a single characteristic is the
   minimal departure from it, is walk-forward fittable in the sense `strategies/lib/walkforward.py`
   supports, has a handful of parameters rather than hundreds, and is cheap enough to refit
   monthly. That is a much narrower learned candidate than the ridge block the lab tried.
4. **Do not import the shortlist as a feature block.** With four to seven usable characteristics
   and ~145 names, and given the previous note's arithmetic on selection bias, the temptation to
   fit the full additive model here should be resisted: the paper's own estimator needs hundreds
   of thousands of observations for its selection consistency, and this cross-section is three
   orders of magnitude smaller.

**Pitfalls:**

- **Volume is not forward-filled and is NaN on foreign holidays** (the strategy contract says so
  explicitly). SUV's within-month regression needs enough valid daily observations per name;
  decide and document a minimum-observation rule before looking at any result, because the
  alternative is a signal defined on a different number of days per region.
- **Volume is a share count in native units.** SUV's regression is scale-free in the sense that
  standardising by the residual standard deviation removes the units, but the *level* differences
  across regions and share-price conventions will still show up in the fit quality. Consider
  running the regression on log volume.
- **Survivorship again.** The size-cut result is the mechanism by which this repo's universe
  differs from CRSP; it is not a substitute for the constituent-selection artifact this folder
  already documents. Both are present and they are different problems.

## Related

- **`research/notes/2026-08-29-machine-learning-cross-section-comparative.md`** (Gu–Kelly–Xiu) —
  the same "few predictors matter, and nonlinearity is where the gain is" conclusion by a
  different method. Note the direct tension this folder already recorded on 2026-08-29:
  Gu–Kelly–Xiu report machine-learning predictability *stronger among large stocks*, while this
  source finds *fewer characteristics surviving* among large stocks. Both can hold — one is about
  forecast accuracy, the other about the number of independent predictors — but the pair sharpens
  the open question rather than settling it, and this note is the second half of it.
- **`research/notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`** and
  **`2026-08-31-amihud-volume-component-decomposition.md`** — the volume functionals already
  screened. SUV is the one that is not a function of the volume level.
- **`research/notes/2026-09-01-multi-signal-overfitting-critical-t.md`** — the reason not to
  treat this source's shortlist as a licence to build a multi-characteristic composite.
- **`experiments/learnings.md`** — the 52-week-high refutation (see point 2), the
  `liquidity-volume` nulls, and the learned-candidate design rule.
