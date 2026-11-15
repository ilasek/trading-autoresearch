---
title: "Variable Selection for Propensity Score Models"
authors: Brookhart, Schneeweiss, Rothman, Glynn, Avorn, Stürmer
year: 2006
venue: American Journal of Epidemiology (venue tier 1 — peer-reviewed)
url: https://doi.org/10.1093/aje/kwj149
citations: 2006 (Crossref `is-referenced-by-count`, checked 2026-11-15)
sample_period: n/a — two Monte Carlo simulation experiments, no observational data of any kind
markets: none (methodology; pharmacoepidemiologic framing)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the **price list** for the inclusion rule in the companion note. It asks what each of
three kinds of covariate does to the **bias, variance and mean squared error** of an estimated
exposure effect when it is put into the conditioning set, and it answers with simulation plus
the analytic results it was built to illustrate.

Three covariate types, defined by which arrows they have:

- **`X₁` — a true confounder**: related to both exposure and outcome.
- **`X₂` — outcome-only**: related to the outcome, unrelated to the exposure.
- **`X₃` — exposure-only** (an instrument): related to the exposure, unrelated to the outcome.

The three findings, each with a mechanism rather than just a sign:

**1. Include outcome-only covariates. Always.** Adding `X₂` **reduces the variance of the
estimated exposure effect and does not change its bias.** The reason is the one worth
carrying, because it is a finite-sample argument and therefore applies to any single
realisation rather than asymptotically: a covariate that is *population*-unrelated to the
exposure will, in any actual sample, carry a small chance association with it. If that
covariate is also related to the outcome, then **in that sample it is an empirical
confounder**, and adjusting for it removes that realisation's non-systematic bias. Across
realisations, removing the non-systematic component pulls each estimate toward its mean — i.e.
lowers variance. (The paper connects this to the known result that it is better to use an
*estimated* propensity score than the true one.) In the simulation, the unbiased estimator
with the smallest variance was the one containing `X₁` **and** `X₂`, at roughly **30% less
variance** than the confounder-only model at the smaller sample size and **25% less** at the
larger.

**2. Exclude exposure-only covariates. They cost variance and buy no bias reduction.** Adding
`X₃` **increases** the variance of the estimate without reducing bias: the all-covariates
model had about **40% more variance** than the `X₁`,`X₂` model at both sample sizes. The
mechanism: an exposure-only covariate adds noise to the fitted score and raises the
correlation between the fitted score and the exposure; where the score enters an outcome model
as a covariate, raising that covariance raises the variance of the exposure coefficient. In a
*matched or stratified* analysis the same noise makes subjects get mismatched or
misclassified with respect to the covariates that do matter — and the simulation confirms the
stratified version is **more** damaged by `X₃` than the smooth-adjustment version.

**3. The best-predicting exposure model is not the best conditioning set, and the `c`
statistic is the wrong instrument for choosing one.** This is the paper's headline and it is
the finding that bears hardest on this lab. The model with the **lowest MSE** had a `c`
statistic of **0.67**; the model with the **highest `c` statistic (0.82)** — which, as the
paper notes, is always one containing all variables related to the exposure — was the one with
**40% more variance**. The authors put the reason in one sentence: *"The goal of a PS model is
to efficiently control confounding, not to predict treatment or exposure."* A selection
criterion built on prediction of the exposure will **miss covariates related only to the
outcome**, and will miss confounders that are weakly related to the exposure but strongly
related to the outcome.

**4. The one case for dropping a true confounder, and the arithmetic that closes it.** The
second experiment traces, over the plane of (confounder→outcome strength) × (confounder→exposure
strength), where including a true confounder `X₁` *raises* MSE. It does: in the region of
**strong association with the exposure and weak association with the outcome**, the variance
increase is not offset by the bias reduction. But that region **shrinks as the sample grows**,
and for a structural reason — variance falls at `1/n` while the bias from an omitted
confounder does not fall at all. The paper's conclusion is therefore narrow and should not be
over-read: *"in moderate-sized studies, one would not want to exclude any covariate related to
exposure from a PS model unless it was known a priori to be unrelated to the outcome."*

## Construction recipe

**The selection rule, as a procedure:**

1. Partition candidate covariates by their two associations: with the **outcome** and with the
   **exposure**. Both judged substantively where possible (see the companion note on why the
   data cannot do this alone).
2. **Include** everything related to the outcome, *whether or not* it is related to the
   exposure. This is the dominant term in the rule.
3. **Exclude** anything related to the exposure and known a priori to be unrelated to the
   outcome.
4. **Keep** everything related to both. Drop a true confounder only when the sample is small
   *and* the covariate is strongly exposure-related and weakly outcome-related — and treat
   that as an edge case that disappears with sample size.
5. **Do not use predictive fit of the exposure model as the criterion**, and do not report the
   `c` statistic as evidence the conditioning set is good. Both select for the wrong thing.
6. Size follows the sample: the analytic results cited (asymptotic variance of an
   exposure-model estimator is not increased, and is usually decreased, as the exposure model
   gains parameters) imply **the conditioning set should grow with the study size**, not be
   trimmed for parsimony.

**Simulation design worth copying, since it is the cheap way to price a rule.** Independent
standard-normal covariates; a probit exposure model; a log-linear Poisson outcome; a fixed
true effect; **all seven non-empty subsets** of three covariates fitted as separate
conditioning sets; bias, variance and MSE computed across 1,000 replications at two sample
sizes; and the whole thing re-run under nine single-parameter perturbations (covariate
variances up and down 50%, effect size up and down, exposure prevalence lowered). Two
adjustment devices compared — the fitted score entered as a **cubic spline** in an outcome
model, and **subclassification on score quintiles**. The qualitative pattern held in every
perturbation; only the magnitudes moved.

## Robustness evidence (qualitative only)

No data and therefore no sample period, no market, nothing to decay — which also means the
robustness evidence available is of the right kind for a simulation claim and only that kind.
The three qualitative conclusions survived all nine perturbations and both adjustment devices;
the *numbers* are explicitly stated by the authors to depend on the data-generating process
and parameter choices, and they say so without being asked. The findings are consistent with
the prior analytic results the paper cites (Rubin–Thomas approximations for bias and variance
reduction; Robins–Mark–Newey on the asymptotic variance of exposure-model estimators), which
is the relevant form of corroboration for a simulation study: one mechanism, two independent
derivations.

Honest limitations the paper states itself: only three covariates and a constant exposure
effect; the structural form of the data-generating process was never varied, only its
parameters; and the **hybrid** design — a matched or score-adjusted analysis that *also*
carries covariates in the outcome model — is left untouched, so the results say nothing about
variable selection when a variable may appear in the score model, the outcome model, or both.
That last exclusion matters here, because the lab's construction is closer to the hybrid than
to either pure case.

## Implementability here

**The direct hit, and it is the strongest single statement in this session.** The lab's
`#438` recommended a `c` statistic as a balance diagnostic; `#440` and `#441` demoted it on
*detection-efficiency* grounds (ARE `≤ 1/√π`, plus a discretization penalty, against a
location test that is minimax optimal when `d/n → 0`). This paper refuses the same statistic
on a **completely independent** ground — that maximising it selects the wrong conditioning set
— and it does so with the explicit arithmetic that the **lowest-MSE model had `c = 0.67` while
the highest-`c` model (0.82) carried 40% more variance**. Two unrelated literatures, two
unrelated arguments, same verdict. `#440` is now over-determined rather than merely supported.

**The free screen this gives the lab, which it has never run.** The lab's mandatory joint
control is `{within-region log P, vol126}`, and the record shows it being judged by its
`rho` to the *score*: the 2026-11-13/14 calibration table reports `rho_logP` per object, the
2026-11-12/13 entry reasons about `rho` to the controls (`+0.09`, `−0.11`) when a sign flip
looked too large to explain. **Every one of those readings is on the exposure side.** This
paper says the exposure-side association is the one that predicts the *variance cost*, and
that the admission decision should turn on the **outcome-side** association — which the lab
has not measured for either control. So:

> **Before admitting a variable to the joint control, measure its association with the
> forward return, not only its correlation with the score.** A control strongly related to
> the score and weakly related to forward returns is the `X₃` case: it adds variance to every
> reading taken through it and removes no bias.

This is computable on train alone, costs no trial, reads no holdout, and the lab already has
the machinery (the within-region rank-space residual pipeline) to produce it.

**It also supplies a candidate explanation for something in the lab's record that currently
has none.** Twice the joint control has **raised** a reading rather than lowering it
(`rank_stability` US `+212 → +483, t +2.10`; plain 12−1 momentum to controlled `z +2.05` to
`+2.45` on the full window). `#444`'s precision-transform mechanism is one explanation —
whitening a correlated cross-section can increase standardised signal. This paper offers a
second and more mundane one: **a control on the `X₃` end inflates the variance of what is read
through it**, and an inflated-variance reading is as likely to come out larger as smaller. The
two explanations are distinguishable by the screen above — the precision-transform story
predicts a real increase in standardised signal, the `X₃` story predicts a noisier estimate
with an unchanged centre, and the controls' outcome-side associations separate them. Either
way, **the lab should stop reading "the control raised it" as corroboration**, in both
directions.

**Where the transfer stops, said precisely.** (i) The lab residualises the *score* on the
controls; the paper models the *exposure*. The bias–variance logic is about what enters the
conditioning set and carries over, but the variance algebra (score-exposure covariance driving
the coefficient variance) is specific to the score-as-covariate design and should not be
quoted as holding term-for-term here. (ii) The paper's own stated gap is exactly the lab's
design — the hybrid case where a variable can sit in more than one place — so the lab is
*outside* the regime the simulation covers, and the three qualitative rules should be carried
while the magnitudes are not. (iii) The `30% / 25% / 40%` figures are properties of one
data-generating process with three independent normal covariates; **they are not a
calibration for this panel** and must not be carried as one, exactly as `learnings.md`'s
constants must not be carried into a new family.

**Tension with `#444`, and it is a real one worth keeping in view.** `#444` says *adding
covariates to a joint balance test weakens it* (the detectability condition puts total squared
difference against `√p`). This paper says *adding outcome-related covariates to a conditioning
set improves the estimate* and that the set should **grow** with sample size. Both are
correct and they are about different objects — the **power of a test** versus the **MSE of an
estimator** — but the lab runs both and must not let the rule for one leak into the other.
The operational split: **short, pre-named list for the balance test; outcome-related
inclusion for the control used in a reading.**

**Cost profile: free.** One cross-sectional association per candidate control, computed on
train.

## Related

- `notes/2026-11-15-the-modified-disjunctive-cause-criterion.md` (same session) — the inclusion
  rule this note prices, and the reasons the data cannot choose the set by itself.
- `notes/2026-11-15-instrumental-variables-as-bias-amplifiers.md` (same session) — the `X₃`
  case taken further: not merely a variance cost but, with residual unmeasured confounding, a
  **bias amplifier**.
- `notes/2026-11-13-accuracy-tests-are-underpowered-for-signal-detection.md` — `#441`'s
  "testing requires less regularization than predicting"; this note is the conditioning-set
  twin of the same statement.
- `notes/2026-11-13-classification-accuracy-as-a-two-sample-test.md` — the `c` statistic as a
  test, refused here on independent grounds.
- `notes/2026-11-10-characteristic-matched-benchmark-portfolios.md` and
  `notes/2026-11-11-matching-on-the-estimated-score-and-its-variance.md` — the matched-design
  vein, where the same score is built for a different purpose.
