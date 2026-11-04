---
title: "A Comprehensive Look at The Empirical Performance of Equity Premium Prediction"
authors: Goyal, Welch (Crossref lists the published version as Welch, Goyal)
year: 2008 (published); working version dated 2006-01-11 is the text read
venue: Review of Financial Studies 21(4), 1455–1508 (Tier 1)
url: https://doi.org/10.1093/rfs/hhm014 — read in full (59 pp.) as the Yale ICF working version, `repec.som.yale.edu/icfpub/publications/2412.pdf`; the earlier NBER w10483 version was also downloaded and not relied on
citations: 3527 (Crossref `is-referenced-by-count`, checked 2026-11-04); Semantic Scholar's DOI record (titled "… Prediction II") reports 1457 on the same date — the split-record pattern this folder has recorded before, so the Crossref figure is the one to use
sample_period: through end-2004/2005 depending on frequency; annual, five-year and monthly horizons; data from 1871 where available, with the main evaluation in the CRSP era
markets: US aggregate equity market
tier: A
validation_overlap: false
published_post_2018: false
---

**The counterparty to the same night's `2026-11-04-timing-r2-against-the-squared-sharpe-ratio.md`,
taken deliberately rather than by accident.** The [2026-11-03] entry's cash/pool-boundary criterion
admits a source only if the cash weight is a **decision**. This paper's third stated finding is
exactly that — *"the models would not have helped"* an investor who used them for market timing —
and it is the paper the companion was written against. The folder's rule is to record a tension
explicitly rather than pick a side, and this pair is the cleanest tension in the vein: **two Tier A
papers, one sample, opposite verdicts, and a fully identified reason for the disagreement.**

Zero prior coverage of the paper: fixed-string greps across all 258 prior notes returned
`Comprehensive Look at the Empirical Performance` **0** and `equity premium prediction` **1** (an
incidental mention). The eight files matching `Goyal` are all Goyal–Wahal and others.

## Mechanism

**(1) The benchmark is the *prevailing* mean, and that choice is the whole experiment.** The null
forecast is the historical average excess return computed **on the same expanding window** the
model gets, not the full-sample average. A model must beat an estimate that is itself updating.
This is the time-series analogue of grading a stock-selection book against an equal-weighted pool
of the same eligible names: a benchmark that is cheap, parameter-free, and unavailable to criticise
for hindsight.

**(2) The headline is a null, stated at three levels.** For the predictor variables the literature
had accumulated: most have lost in-sample explanatory power over the latter part of the sample;
the few that retain in-sample significance **fail regression diagnostics built from their
out-of-sample behaviour**; and out of sample most do not merely fail to beat the prevailing mean
but **underperform** it. The authors' summary: *by assuming that the equity premium is "like it
always has been," an investor would have predicted just as well.*

**(3) The diagnostic, and it is the most portable thing in the paper.** For each model, plot the
**cumulative difference in squared errors**: cumulative squared error of the null minus cumulative
squared error of the model, as a function of time.

- Rising ⇒ the model is predicting better over that stretch; falling ⇒ the null is.
- The sign of the final value matches the sign of the `ΔRMSE` statistic, so the picture and the
  summary number cannot disagree.
- The level is arbitrary, so the reader can **re-date the start of the evaluation by sliding the
  zero line**, which makes the start-date sensitivity visible instead of hidden.
- The best and worst points of the curve are invariant to that start date.

A well-specified signal should show **all four** of:

1. significant performance both in-sample and out-of-sample over the whole evaluation period;
2. a generally upward drift (irregular is fine);
3. a drift that is **not concentrated in one short or unusual stretch**;
4. a drift that remains positive over the most recent several decades — otherwise the honest
   reading is that the underlying model has changed.

**(4) The failure mode has a signature, and the signature distinguishes two hypotheses.** A model
that is merely *low-powered* should look poor early and improve as the estimation window lengthens.
A model that is *mis-specified / unstable* looks acceptable early and deteriorates. The paper
reports the second pattern, and backs it with a direct stability test (CUSUMQ) that rejects
parameter stability for essentially every variable examined at the monthly frequency and nearly
all at the annual. **Instability, not sample size, is the diagnosis.**

**(5) Two admissions of conservatism, both of which are the lab's own problem restated.** The
authors state that their exercise is **not a true out-of-sample test** — the evaluation data are
the same data on which the literature's models were found — and that they **ignore the question of
how an investor would have known in advance which of the many models would work.** So the real
discount is larger than the reported one, by a selection term they do not try to estimate. This is
precisely the role the deflated-skill bar plays in this repo, and it is here stated as the residual
that an out-of-sample test does *not* remove.

**(6) Their audit of the disagreeing literature traces the differences to two knobs.** Where other
papers found predictability, the authors replicated them and attributed the difference to **sample
period** and to **year-weighting / down-weighting of extreme observations** — not to method. The
general lesson is a reproduction rule: before accepting a conflict between two results on the same
data, check the window and the observation weights first.

**(7) Their reading of the companion paper's restrictions — endorsement with two caveats.** The
forecast floor (refusing a negative premium) and the wrong-sign coefficient truncation *"can be
recommended"*, and the first does most of the work. But:

- **The restriction converts the model into a non-linear one that is, on many dates, simply the
  benchmark.** In the cases where it changed the verdict, roughly half of all dates had the forecast
  truncated, i.e. the "model" *was* the unconditional model on about half the sample. A restriction
  that improves a model by replacing it with the null on half the dates is a statement about the
  null's quality, not the model's.
- **The utility-gain metric is amplified by the risk-aversion parameter** and lets a conditional
  model earn credit for *reducing variance* as well as raising the mean. With the companion's
  `γ = 3`, a small predictive advantage can translate into a return gain about an order of
  magnitude larger — in both directions. Changing `γ` changes the economic verdict, though not
  monotonically.
- **And the weight constraint binds on the benchmark too.** At `γ = 3` even the *unconditional*
  prevailing-mean strategy hits the 150% leverage cap in a non-trivial minority of months. When a
  constraint binds on both the candidate and the benchmark, part of what the comparison measures is
  which of them hits the constraint more often — not which forecast is better.

## Construction recipe

Not a strategy. A grading protocol, and all of it is free.

1. **Null = the prevailing (expanding-window) unconditional forecast**, re-estimated at every date
   the candidate is re-estimated.
2. **Report in-sample and out-of-sample performance side by side**, and treat the *divergence*
   between them as the diagnostic rather than either number alone.
3. **Plot the cumulative squared-error difference** against the null and apply the four conditions
   in mechanism (3).
4. **Classify the failure** using mechanism (4): deteriorating-late ⇒ instability;
   poor-early-improving ⇒ low power. Confirm with a parameter-stability test.
5. **State the selection residual** that the out-of-sample test does not remove, per mechanism (5).
6. **When a result conflicts with another on the same data**, check sample window and observation
   weighting before method, per mechanism (6).

## Robustness evidence (qualitative only)

- **Tier A throughout.** Top venue, one of the most-cited papers in return predictability, and the
  methodology-honesty column is unusually strong: the authors publish the two ways their own test
  is *too generous*, report that their tables are distilled from a much larger set of
  specifications, and reproduce the papers they disagree with rather than asserting around them.
- **Deliberately uniform treatment** — the same methods, periods and frequencies for every
  variable, which is the design that makes the comparison across predictors meaningful and is the
  opposite of the per-variable tuning the predictability literature had accumulated.
- **Explicitly checked against the obvious objections**: not driven by low power (the authors argue
  from the *shape* of the failure), not driven by a few outlier years, not sensitive to the data
  definitions and time-series corrections examined, and the conclusions survive encompassing tests
  that do not use ex-post information.
- **Single market, single asset, and a time-series exercise.** None of it is cross-sectional, and
  it is the aggregate US index only. The *diagnostic* is market-agnostic; the null result is about
  that one series.
- **Sample ends well before this repo's validation window**, so nothing here can leak into it.
- **Costs are not modelled.** For a timing strategy that is a smaller omission than usual (two
  trades per switch), but it means the null is a gross-return null.

## Implementability here

**The diagnostic is importable tonight and is strictly finer than what the lab currently runs.**

v3 already reports train skill split into two sub-periods — 1997–2008 and 2009–2017 — which is
mechanism (3)'s condition 3 and 4 evaluated at two points. The cumulative-squared-error plot is the
same test evaluated at **every** point, and it costs nothing beyond what a trial already computes.
The direct translation for this repo:

> **Free screen: the cumulative active-return curve against the pool.** For any candidate, plot
> cumulative (candidate return − equal-weight eligible pool return) over the train window. Apply
> the four conditions. A curve whose whole rise sits in one short stretch fails condition 3; a
> curve that rises then goes flat or negative over the later part fails condition 4 and indicates
> instability rather than low power. Neither failure needs a validation number to detect, and both
> are invisible in a single skill statistic with an error bar.

This is complementary to, not a substitute for, `scripts/rank_trials.py`: the ranking script says
whether two candidates can be separated; this says whether one candidate's edge accrued in a way
that could recur.

**Three further transfers.**

- **Mechanism (4) is the test the lab's own repeated finding has been missing.** `learnings.md`
  records several signals whose sign **inverts across train sub-periods** and were declined on that
  basis. This paper names the inference that justifies the decline: deteriorating-late is the
  signature of mis-specification, and a longer sample does not fix it. (The companion night's
  `σ_IC` quantity is the same phenomenon measured as a dispersion rather than diagnosed from a
  shape — the two are worth computing together.)
- **Mechanism (7)'s first caveat is a trap this lab can walk into cheaply.** If the sign
  restrictions from the companion note are adopted — and they should be — then the fraction of
  dates on which the restriction is active must be reported alongside the result. A candidate that
  is the equal-weight pool on most dates and a tilt on a few is **mostly the benchmark**, and its
  skill interval will be narrow for that reason rather than from precision. The lab has already met
  the structural version of this (a near-full-pool equal-weight book cannot clear a null gate that
  permutes its own names); this is the forecast-side version.
- **Mechanism (7)'s third caveat applies to v3's `≤25%` cap and gross-leverage limit.** When a
  constraint binds on both the candidate and the pool, part of the measured difference is
  constraint-hitting. Worth a one-line check in any trial where the cap binds.

**What does not transfer.** The predictor variables are macro and valuation series this repo does
not hold; the null result is about them, on one index, and is not evidence about anything in
`program.md`'s families. Importing it as "timing does not work" would be exactly the kind of
analogy `CLAUDE.md` forbids. What is importable is the **grading apparatus** and the **failure
taxonomy**.

**And the tension with the companion, stated rather than resolved.** On the same data and the same
question, the restricted models beat the prevailing mean (companion) and the models do not warrant
an investment endorsement (this paper). Both are right about different objects: the companion shows
that a **weak prior imposed on a noisy estimator** improves it, and this paper shows that
**the improvement runs mostly through replacing the estimator with the benchmark**, that the
remaining edge is not stable across sub-periods, and that the economic magnitude depends on a
risk-aversion parameter and a leverage cap. For this lab the operative synthesis is narrow and
usable: **adopt the restrictions, use `R²/S²` as the yardstick, and require the cumulative curve
before believing either.**

## Related

- `notes/2026-11-04-timing-r2-against-the-squared-sharpe-ratio.md` — the counterparty. Read as a
  pair.
- `notes/2026-11-04-generalized-fundamental-law-strategy-risk-and-the-transfer-coefficient.md` —
  `σ_IC` is this paper's instability diagnosed from a shape, measured instead as a dispersion.
- `notes/2026-09-09-specification-curve-analysis.md`,
  `notes/2026-11-02-multiverse-of-country-level-research-designs.md` — mechanism (6) (sample window
  and observation weights as the explanation for conflicting results) is the two-knob special case
  of the multiverse these notes describe.
- `notes/2026-11-01-reproduction-versus-replication-open-source.md` — mechanism (6) as a
  reproduction rule.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — mechanism (5)'s unestimated selection residual is
  what the deflator exists to charge.
- `notes/2026-10-28-model-confidence-set-the-set-valued-ranking.md` — the complementary question
  (which candidates can be separated) to this paper's question (did this candidate's edge accrue
  recurrently).
