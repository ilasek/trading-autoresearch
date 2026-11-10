---
title: "Detecting Abnormal Operating Performance: The Empirical Power and Specification of Test Statistics"
authors: Barber, Lyon
year: 1996
venue: Journal of Financial Economics 41(3), 359–399 — venue tier 1
url: https://doi.org/10.1016/0304-405X(96)84701-5
citations: 1255 (Crossref, checked 2026-11-10)
sample_period: 1977–1992 (subperiods 1977–1984 and 1985–1992); ~32,680 firm-years
markets: US — NYSE/AMEX firms with Compustat accounting data
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the paper the [2026-11-09] handover was asking for, and it answers the question in its
sharpest possible form: **what do you do when the variable you must match on is the variable that
selected your sample?**

The setting is an event study on an accounting performance measure (return on assets). A researcher
picks firms that did something — issued equity, initiated a dividend, repurchased shares — and asks
whether performance *after* the event differs from what it would have been. The trouble is that
firms do those things after unusual performance, so the sample is **selected on the level of a
mean-reverting variable**. The selection alone then manufactures a post-event change in the
measured direction, with no event effect at all: a firm picked because its performance is high is
mostly a firm whose performance contains a large transitory component, and the transitory component
dissipates. The authors name both halves of the transitory component — accounting choices and
genuine but non-recurring economics (one-off income or expense, temporary demand shifts) — but the
statistical content does not depend on which: *any* measure with a transitory component produces
this, and the authors cite prior work documenting that returns on equity are slowly mean-reverting.

Their headline result, stated in the introduction and again in the recommendations, is the one worth
carrying: **control groups matched on industry, or on industry and size, yield misspecified test
statistics whenever the sample's pre-event performance differs from the controls' — and the
misspecification is large even when that difference is slight.** Only expectation models that match
on *pre-event performance itself* are well specified in performance-selected samples. Matching on
industry and performance is, in their words, generally much more important than matching on industry
alone or on industry and size.

The deeper point, and the one that generalises past accounting: **a control group is a model of
expected performance, and writing down the matching variables is writing down that model.** The
paper makes this explicit by restating each matching scheme as an equation for `E(P_it)`. Matching
on industry alone asserts `E(P_it) = P_industry,t` — the firm's own history is irrelevant. Comparing
*changes* asserts `E(P_it) = P_i,t−1 + ΔP_industry,t` — the firm keeps its own level and inherits
only the industry's change. These are different assumptions, not different estimators of the same
thing, and the data pick between them.

## Construction recipe

**Four families of control group, in increasing strictness** (each is a different `E(P_it)`):

1. Industry only, at two-digit or four-digit SIC. The trade-off is explicit: the coarser code gives
   a larger comparison group, the finer one a closer match. (This is the caliper trade-off in its
   simplest form.)
2. Industry and size — assumes performance varies by industry *and* by firm size.
3. Industry and **pre-event performance**.
4. Size and pre-event performance, **without regard to industry**.

**Levels versus changes.** Each of (1)–(2) can be used on the *level* of performance or on the
*change*. The change form, `(P_it − P_i,t−1) − (P_ind,t − P_ind,t−1)`, is a difference-in-differences
and implicitly carries the firm's own pre-event level. The authors are unambiguous: **change models
dominate level models**, and a performance-matched level model is itself a change model in disguise
(matching in `t−1` on the level is what makes it one) — they group it with the change models for
exactly that reason.

**The caliper, stated exactly** (their scheme (4), the one well specified in every cell they test):

- Match each sample firm, in year `t − 1`, to **all** firms within **70%–130%** of its size (book
  value of total assets).
- From that set, **discard those outside 90%–110%** of the sample firm's performance in `t − 1`.
- **If the surviving set is empty**, fall back to the firm that meets the *size* criterion and is
  **closest in performance** in `t − 1`.

Note the shape: a **hard window on the first variable, a hard window on the second, and a
nearest-neighbour fallback** so that the design never silently drops an observation. Note also that
the second window (±10%) is much tighter than the first (±30%) — the selection variable gets the
tight caliper.

**What is differenced.** The sample firm's post-event performance against its one matched control's,
with the match *fixed at `t − 1`* and the control used throughout the horizon. The authors tested
letting the comparison group drift (firms entering and leaving the industry group over time) and
**recommend against it**: it does not change specification but it erodes power at longer lags, and a
constant group puts the same data requirements on sample and control.

**Statistic.** A nonparametric test (Wilcoxon signed-rank) dominates the t-statistic on power
throughout, in every analysis they run. Given the skewness of the underlying measures this is not a
close call for them.

**Lag choice.** Matching on performance lagged one year is more powerful than two or three. Power
erodes monotonically as the matching lag lengthens — i.e. a stale match is a weak match, and the
decay is in *power*, not specification.

## Robustness evidence (qualitative only)

- Results replicate across both halves of the sample split into two sub-periods: change-and-industry
  models are well specified and powerful in random samples in both; only the performance-matched
  models are well specified in the extreme deciles of performance in both.
- The conclusion holds across alternative performance measures (return on sales, return on
  cash-adjusted assets, return on market value of assets), with one exception that is about power,
  not specification: cash-flow-based measures give uniformly less powerful tests.
- **One cell resists every design they try, and the authors say so**: small firms with unusually
  strong past performance. Every expectation model is misspecified there; performance matching makes
  it less severe but does not fix it; only size-**and**-performance matching *without regard to
  industry* produces a well-specified statistic in that cell.
- The authors' own diagnosis of that failure is the most transferable sentence in the paper:
  **the tendency to mean-revert is itself cross-sectionally heterogeneous.** Smaller firms'
  performance measures revert faster than larger firms'. So matching on the *level* of the selection
  variable is only sufficient when the *speed* of reversion is common across the matched pair; where
  it is not, the match is imperfect in a known direction and the estimate inherits the difference.
  Their closing instruction is to ask, before trusting the design, whether the sample's performance
  measure has more or less tendency to mean-revert than the control's.

## Implementability here

**This is a design note, not a signal note.** The measured object is accounting ROA, which this lab
cannot see at all (no fundamentals). Nothing in it is a candidate. What it supplies is a
*construction for a control group* that the folder did not hold — a grep across all 275 prior notes
on 2026-11-10 returned **zero** for `matching variable`, `caliper` and `synthetic control`, and the
four `matched control` and five `propensity` hits were other people's event studies or, in every
`propensity` case, the unrelated phrase *selling propensity*.

**Why the lab needs it.** Protocol v2's `eligible` panel makes several natural "events" available —
a name becoming eligible, a name entering or leaving a liquidity or volatility band, a name entering
a momentum decile — and `#424` established that **all of them are selected on past performance**
(57% of one event sample sat in the top two momentum deciles). The direct analogue of this paper's
result is: *a cohort defined by any of those events, compared against the eligible pool, will show a
post-event return difference that is a selection artifact, and no amount of care about the event
window fixes it.* The repair is a matched control, and the matching variable must be the thing that
did the selecting.

**The translation, with the substitution named.** The lab's mean-reverting selection variable is not
ROA; it is **past return**. The identical argument applies, with two differences that both cut the
same way:

- *Direction is not guaranteed.* Accounting performance reverts; returns revert at some horizons and
  continue at others. So the sign of the artifact is a function of the horizon the cohort is defined
  on, not a constant. This makes a matched control *more* necessary, not less — the researcher
  cannot sign the bias a priori and subtract it.
- *The reversion speed is heterogeneous here too, and along an axis the lab already measures.* The
  paper's small-firm cell has its counterpart in this panel's volatility and liquidity cross-section.
  A matched control that pins the past-return level but not the volatility level inherits exactly the
  residual this paper flags.

**A concrete adaptation of the caliper, for a scout.** For a cohort defined by event `E` on date
`d`, build the control by, for each event name: (i) restrict to names `eligible` on `d` that did
**not** experience `E`; (ii) keep those within a hard window of the event name's **formation-window
past return** (the tight caliper, since that is the selection variable); (iii) among those, take the
nearest on a second variable the lab can compute — trailing volatility or log dollar-volume rank;
(iv) if the window is empty, fall back to the nearest on the selection variable among those meeting
the second criterion, so no event name is dropped. Fix the match at `d` and hold it for the horizon.
Difference the two books' returns. Report the paired difference with a rank-based statistic rather
than a `t`, per the paper's power result.

**Pitfalls, named.**

- **Match on the region too, or report both ways.** `#421` established that any pooled score
  correlated with a price or currency level is approximately a region bet on this panel; a matched
  control drawn pooled across the nine markets will match on region only by accident.
- **The ±10% caliper is not transferable as a number.** It is calibrated to the dispersion of ROA in
  a US accounting panel. The *shape* (tight window on the selection variable, loose on the nuisance
  variable, nearest-neighbour fallback) transfers; the constants do not, and `CLAUDE.md`'s rule
  against importing constants by analogy applies with full force.
- **The match is fixed at formation and must not be refreshed with hindsight.** Re-matching at every
  date using the control's later behaviour is a peek; the paper's own recommendation to hold the
  comparison group constant has the same shape as the lab's causality check.
- **This buys identification, not a candidate.** A matched-control design is the right way to learn
  *whether a cohort effect exists*; it is not itself a long-only book, and anything it establishes
  still has to be built as a strategy and run through the gate.

## Related

- `notes/2026-11-09-price-based-comovement-and-its-failed-replication.md` — the paper that made this
  gap visible: a momentum-matched control plus a triple difference killed a comovement result
  (`#424`). This note supplies the construction that paper used without describing.
- `notes/2026-11-10-control-firm-versus-reference-portfolio-biases.md` — the same authors' companion
  on *stock returns*, with the control-firm-versus-reference-portfolio comparison and the three
  biases.
- `notes/2026-11-10-characteristic-matched-benchmark-portfolios.md` — the matched-*portfolio* form of
  the same idea, whose third matching dimension is prior-year return.
- `notes/2026-11-10-matching-estimator-bias-and-the-dimension-of-the-match.md` — the econometrics of
  what an imperfect match costs, with a rate and a correction.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` and
  `notes/2026-11-07-index-addition-comovement-across-forty-national-indices.md` — the lab's two
  standing "membership as event" items, neither of which is built against a matched control.
