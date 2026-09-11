---
title: "Influential Observations and Inference in Accounting Research" — read for what winsorization and truncation actually do, which direction each biases, and why influence is a property of the fit rather than of a variable's tail
authors: Leone, Minutti-Meza, Wasley
year: 2019
venue: The Accounting Review (venue tier 1 in its own field; a top-3 accounting journal, and the methodological literature on outlier treatment lives there rather than in finance)
url: https://doi.org/10.2308/accr-52396
citations: 335 (OpenAlex, checked 2026-09-11); 325 (Crossref `is-referenced-by-count`, same date); 266 (Semantic Scholar DOI endpoint, same date). Three indices in agreement on the order of magnitude.
sample_period: simulations (no sample period); empirical illustrations on IBES analyst forecasts 2005–2011 and Compustat accruals 1972–2001; replications of three published accounting studies on their own samples
markets: US (Compustat / CRSP / IBES). The *mechanism* is a property of estimators and is market-independent.
tier: A
validation_overlap: false
published_post_2018: true
read: full text of the authors' August 2013 working draft (first draft April 2012), `zaferyuksel.com/uploads/1/2/5/8/12582384/outliers-leone-minutti-meza_wasley_2013.pdf`, complete and text-extractable. The published version is closed. **Checked against the published abstract via OpenAlex**: every claim relied on below appears in the published abstract, and the published version adds an emphasis on replicating three published studies that the draft's abstract does not carry. The draft was read; the typeset article was not. Metadata note: Crossref and OpenAlex both stamp this DOI 2016 while the volume/issue (94(6), pp. 337–364) and Semantic Scholar say 2019; 2019 is recorded here.
---

## Mechanism

The companion to tonight's standardization note, and the other half of the operator gap the
2026-09-10 entry named. A grep across all 88 prior notes finds `winsoriz` in six, always as a
passing hygiene remark inside a note about something else — an `ILLIQ` trim, a `−log(1+x)`
transform, the nonstandard-errors teams' 2.5%/97.5% reporting convention. No note asks what the
operator *does*. The lab has meanwhile run a candidate with `_daily_trim` in its name and carries
a champion whose weights are set by the magnitude of an unbounded z-score, where extreme
observations are not a nuisance but the entire portfolio.

**The central claim, and it reframes the operator.** Winsorization and truncation are applied
**variable by variable, on each variable's marginal distribution**. Influence is not a property of a
marginal distribution. An observation is influential because of where it sits in the *joint* fit —
a combination of an unusual predictor value (leverage) and a large residual. A point can be in the
1% tail of a variable and be perfectly consistent with the relationship; a point can sit well
inside every variable's tail and still dominate the estimate. So the standard treatments are
addressing a different object from the one they are believed to address. The paper's finding is
exactly that: winsorization and truncation are **ineffective at identifying influential
observations**, while influence diagnostics and robust regression both outperform them, and robust
regression outperforms everything.

**The directions of bias, which are not symmetric and are the most useful thing in the paper.**

- **Truncation biases coefficients toward zero** (except in the rare case where the true parameter
  is zero, where there is nothing to bias). Dropping the tails removes the observations carrying
  the most information about the slope.
- **Winsorizing the independent variable but not the dependent variable biases coefficients away
  from zero.** Compressing `x` while leaving `y` alone mechanically steepens the fitted slope. The
  paper's literature review is what makes this matter: 55% of surveyed studies winsorize but **only
  33% winsorize both the dependent and the independent variables**; 40% truncate, only 30% on both
  sides. The majority of applications are running the asymmetric version.
- **When the contaminating observations are randomly distributed**, winsorizing at 1%/99% is close
  to harmless and yields roughly unbiased estimates. This is the case people have in mind when they
  reach for it.
- **When the contamination is *correlated* with a predictor** — the realistic case, and the case
  where it matters — winsorization does not mitigate the bias. Robust regression based on
  MM-estimation reduces it by about 80% in their simulations.

**Why the cutoff is not a detail.** Their earnings-response illustration is the cleanest
demonstration this folder has recorded of a construction node swamping the effect being estimated.
The same regression, on the same data, with nothing changed but the winsorization cutoff:

    raw data                       slope ≈ 0.00002
    winsorized at 1% / 99%         slope ≈ 0.408
    winsorized at 5% / 95%         slope ≈ 1.618

Four orders of magnitude between "no effect" and a large one, and a further 4× between two cutoffs
both of which are conventional. **Recorded as coefficient magnitudes, on the same footing as an IC
or a monotonicity statistic — these are not returns and no period claim attaches to them.**

**The deepest point, and the one that argues against reflexive trimming.** Extreme observations in
financial panels are frequently *real low-frequency events*, not data errors. The paper's appendix
walks through named cases where an extreme buy-and-hold return traces to a specific corporate event
with an identifiable cause. Winsorizing removes them; so does truncating. If the extreme values are
where the economics lives, the treatment deletes the signal and the cutoff choice silently decides
how much.

## Construction recipe

**What robust regression is, in one paragraph.** Rather than minimizing squared residuals, minimize
a function of *weighted* residuals, with the weights falling as an observation's residual grows.
The estimator therefore reacts to deviations from the fitted model rather than to deviations from a
variable's own mean. MM-estimation (Yohai 1987) is the recommended variant: it combines a
high-breakdown initial estimate with a high-efficiency second stage, so it is resistant to
contamination *and* nearly as efficient as OLS when there is none. Available in standard packages
(`robustbase` in R, `robreg`/`mmregress` in Stata; `sklearn.linear_model.HuberRegressor` and
`RANSACRegressor` are the nearest scikit-learn objects, and `statsmodels.robust` has M-estimators —
none is exactly MM, and the note says so rather than pretending).

**Two properties worth memorizing:**

1. With no leverage points or influential observations, robust regression and OLS give essentially
   the same coefficients. The cost of using it when it is unnecessary is close to zero.
2. When contamination is uncorrelated with the regressors, MM-estimation is unbiased and matches
   OLS. It only diverges where it should.

**The authors' recommended protocol**, which costs one extra fit:

1. Estimate the model with OLS.
2. Estimate the same model with robust regression.
3. If the coefficients differ materially, **identify the specific observations driving the
   difference** and diagnose the cause (data error vs. model misspecification vs. real rare event).
4. Modify the model rather than the data if warranted — a log or **rank** transform (which changes
   neither the linearity assumption nor the data), a fat-tailed error distribution, or a nonlinear
   specification.
5. Report the impact of influential observations as part of the study.

Note step 4 explicitly lists a **rank transform as an alternative to trimming**: it bounds influence
without discarding or altering any observation, because it is a monotone map of the data rather than
a truncation of it.

## Robustness evidence (qualitative only)

- The evidence is **simulation plus replication**, which is the right pairing for a methodological
  claim: the simulations establish the direction and size of each bias under a known data-generating
  process, and the replications of three published studies establish that the choice changes
  published inferences on real data.
- The claims are about **estimators**, not about a market or a period. A bias direction derived from
  a data-generating process does not decay, does not need a multi-market sample, and is not subject
  to McLean–Pontiff post-publication decay. This is the one class of source in this folder where a
  single-country, single-database sample is not a weakness.
- The literature-review percentages (55% winsorize, 33% on both sides, 40% truncate, 30% on both
  sides) are a census of practice in one field over one window. Treat them as establishing that the
  asymmetric application is common, not as a precise constant.
- The 80% bias reduction is a simulation result under their specific contamination design and should
  be read as "most of it, not all of it" rather than as a transportable number.
- Counter-consideration the authors themselves raise: robust regression is **not a substitute for
  looking at the data**. Down-weighting influential points automatically can hide a
  misspecification that should have been fixed in the model.
- Published in a top journal in the field whose methodological literature owns this question, with
  the replication material public. Not itself replicated as far as this note establishes; its tier
  rests on venue, the simulation-plus-replication design, and three indices agreeing on a citation
  count in the low hundreds for a methods paper.

## Implementability here

**The first thing to say is that most of this paper does not apply to this lab, and saying why is
the useful part.** The lab does not estimate regression coefficients and does not test hypotheses
about slopes. It computes a score per name per date, ranks it, and holds a band. So the question is
not "should we winsorize before regressing" but **where in this pipeline does an extreme observation
actually change a holding** — and the answer is specific, checkable, and mostly "nowhere".

1. **Rank is already a robust operator, and the lab gets that for free wherever it ranks.** A rank is
   invariant to any monotone transform of the score, so **winsorizing a score before ranking it
   changes nothing at all** — a name in the top band before the winsorize is in the top band after.
   Any diagnostic or candidate whose output is a pure sorted band is immune to this whole literature
   by construction. This is not a small observation: it means the lab's exposure is confined to the
   places listed below, and a session should not go looking for it elsewhere.
2. **Magnitude weighting is where it bites, and that is the champion.** `learnings.md` records the
   equal → rank → z-score-magnitude ladder as the largest within-basket lever the lab found, and
   z-score-magnitude weighting is exactly the step that makes the *value* of the score matter rather
   than its order. There, one name with an extreme score takes capital from every other held name.
   The 25% position cap is the lab's only current defence and it is a cap, not a treatment. **A free
   train-split measurement: for each held date, what share of the book's weight sits in the single
   most extreme name, and how does that share move if the score is winsorized at 1/99 before
   weighting?** Scores no returns, costs no trial, and the answer decides whether any of this is
   live for the champion.
3. **The asymmetry finding maps onto a node the lab has already used without a rationale.** Winsorize
   the predictor but not the outcome and the estimated relation is biased *away from zero* — i.e.
   toward finding an effect. The lab's nearest analogue is a score built from trimmed inputs while
   the returns it is graded against are untrimmed. A candidate with `_daily_trim` in its name exists
   in the trial history. **If a future session trims, it should state which side is trimmed and why,
   because the two sides are not interchangeable.** This is a `#93` house-convention line, and it is
   one sentence long.
4. **Where the lab genuinely does fit a model, this is a live design choice.** Any
   `statistical-learning` candidate, and tonight's parametric-portfolio-policy proposal, fits
   coefficients. There, a squared-error objective is dominated by the extreme observations of a
   140-name cross-section, and a Huber-type loss is the cheap, deterministic, scikit-learn-available
   fix. `notes/2026-08-29-machine-learning-cross-section-comparative.md` already records the same
   recommendation arrived at from the ML side; this is an independent arrival at it from the
   statistics side, which raises the prior on both.
5. **The cross-section is 140 names, so 1% is one name.** This is the sharpest constraint on
   importing anything here. A 1%/99% winsorization on a monthly cross-sectional panel of thousands
   of firms touches a stable, meaningful set of observations. On 140 names it touches **one name at
   each end**, and which name that is will be noise. A 5%/95% rule touches seven. **Any trimming rule
   this lab adopts must be specified in *names*, not in percent**, or it is a different operator at
   every pool size — and, per tonight's companion note, the pool size here moves.
6. **The step-4 recommendation the lab can act on today is the rank transform**, which it already
   uses, and which the paper endorses as the treatment that bounds influence without altering data.
   Where a magnitude is genuinely wanted, a rank-based magnitude (e.g. a normal-scores transform of
   the rank) is the bounded-influence version of the z-score-magnitude weighting the lab now uses —
   and it is a *different* object from the "linear rank-weight" rung already on the ladder, which
   throws the magnitude away entirely.

**Pitfalls.**

- **Do not import the coefficient numbers.** The 0.00002 / 0.408 / 1.618 sequence is an illustration
  of a mechanism on accounting data. It establishes that a cutoff can dominate an estimate; it
  establishes nothing about the size of that effect here.
- **Do not treat "use robust regression" as a portable instruction.** It is an instruction about
  regression estimators. The lab's pipeline is mostly not a regression, and the honest translation
  is "use a bounded-influence loss where you fit, and use ranks where you don't".
- **The `ILLIQ` trim already in this folder is a different operator from the ones studied here** and
  should not be re-graded by this note. `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md`
  records the trim as part of the *measure's definition* — it is how the estimator is kept from being
  dominated by a few stock-days — not as a treatment applied to a regression variable. Conflating the
  two would be an error in both directions.
- **This is a discipline, not a candidate.** Nothing here proposes a book. Consistent with the
  standing 2026-09-08 warning that the lab's bottleneck is not idea supply, the whole note reduces to
  one free measurement (item 2), one convention line (item 3), and one design default for fitted
  models (item 4).

## Related

- `notes/2026-09-11-trimming-and-the-size-premium.md` — the finance demonstration that the treatment
  choice can decide the *sign* of a cross-sectional premium; this note says which treatment, that
  note says how much is at stake.
- `notes/2026-09-11-parametric-portfolio-policies-standardized-characteristics.md` — the other half of
  tonight's operator gap, and the construction where unbounded standardized tails set the weights
  directly.
- `notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md` and
  `notes/2026-09-09-nonstandard-errors-evidence-generating-process.md` — the same object one level up:
  winsorization cutoff is one node in the specification space those papers enumerate, and the 164-team
  study's own protocol winsorizes at 2.5%/97.5% and reports both raw and winsorized dispersion.
- `notes/2026-09-09-specification-curve-analysis.md` — the method for displaying how much a node like
  this is worth, and the natural home for a cutoff sweep if the lab ever runs `#92`.
- `notes/2026-08-29-machine-learning-cross-section-comparative.md` — the Huber-loss recommendation
  reached independently from the ML literature.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` and
  `notes/2026-09-04-commonality-in-liquidity-across-countries.md` — the two places this folder already
  records outlier handling, both as part of a measure's definition rather than as a treatment.
- `experiments/learnings.md` — the z-score-magnitude weighting ladder; and the 52-week-high refutation,
  whose stated cause (a bounded `(0,1]` score with no tail, so band membership flips on noise) is a
  distribution-shape finding the lab reached empirically and never had a note behind.
