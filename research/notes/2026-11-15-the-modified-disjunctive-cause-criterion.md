---
title: "Principles of Confounder Selection"
authors: VanderWeele
year: 2019
venue: European Journal of Epidemiology (venue tier 1 — peer-reviewed)
url: https://doi.org/10.1007/s10654-019-00494-6
citations: 1466 (Crossref `is-referenced-by-count`, checked 2026-11-15)
sample_period: n/a — no data; a synthesis of graphical and potential-outcome results, argued on causal diagrams
markets: none (methodology; epidemiologic framing)
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

The paper answers a question this folder has never had a source on: **given a list of
candidate covariates and a cost per covariate, which ones belong in the conditioning set?**
It is the *rule* layer that `#444` demanded and could not supply.

The setting is an exposure `A`, an outcome `Y`, and measured covariates `C`. The target
condition is that the counterfactuals `Y_a` are independent of `A` given `C` — called
ignorability, exchangeability, selection on observables or exogeneity in different
literatures, and all the same statement. The paper's organising observation is that there
is a **ladder of selection criteria ordered by how much structural knowledge each demands**,
and that the two criteria practitioners actually use sit at opposite ends and **both fail**,
in opposite directions:

- **The backdoor-path criterion** (Pearl) is complete but requires the entire causal diagram,
  including every relation *among the covariates themselves*. Almost never available.
- **The "pre-treatment" criterion** — adjust for everything measured before the exposure — is
  the liberal end. It fails because a pre-exposure covariate can be a **collider**: in the
  M-shaped diagram where a measured `L` is a common effect of two independent unmeasured
  variables `U₁` (a cause of `A`) and `U₂` (a cause of `Y`), the unadjusted analysis is
  *unbiased* and conditioning on `L` *opens* the path `A–U₁–L–U₂–Y` and introduces bias. So
  the liberal rule can manufacture a confound that was not there.
- **The "common cause" criterion** — adjust for common causes of exposure and outcome — is the
  conservative end. It fails the other way: if a true common cause `U` is unmeasured but a
  measured `C` that is a cause of `Y` only (not of `A`) would have sufficed to block the path,
  the common-cause rule says not to control for `C` and leaves bias on the table.
- **The disjunctive cause criterion** sits between them: control for each pre-exposure
  covariate that is **a cause of the exposure, or of the outcome, or of both**. It needs only
  per-covariate knowledge ("is this a cause of `A`? of `Y`?"), never covariate-to-covariate
  structure. Its theoretical property is the reason to prefer it: **for every causal diagram,
  if any subset of the measured covariates suffices to control confounding, the set the
  disjunctive cause criterion selects suffices too.** Neither of the two criteria above has
  that property — the M-diagram breaks the pre-treatment rule and the unmeasured-`U` diagram
  breaks the common-cause rule.

Two qualifications turn it into the paper's actual recommendation. (i) A covariate that is a
cause of the exposure and is *otherwise unrelated to the outcome* — an **instrument** — can
**amplify** bias from residual unmeasured confounding when adjusted for ("Z-bias"), so it
should be dropped from the set even though the disjunctive rule admits it. (ii) A covariate
that fails the rule but is a **proxy for an unmeasured common cause** should be added: a
proxy is a confounder measured with error, and adjusting for it usually (not always) reduces
confounding bias.

## Construction recipe

**The modified disjunctive cause criterion**, as the paper states it, in order:

1. Restrict to covariates **prior to** the exposure. (Not because pre-exposure status is
   sufficient — it is not, per the M-diagram — but because a post-exposure covariate may be a
   mediator, and adjusting for a mediator blocks part of the total effect you are trying to
   measure.)
2. **Include** every such covariate that is a cause of the exposure, or of the outcome, or of
   both.
3. **Exclude** any variable *known* to be an instrumental variable (cause of the exposure,
   related to the outcome only through the exposure).
4. **Add** any variable that fails step 2 but is a good **proxy for an unmeasured common
   cause** of exposure and outcome — and restrict this step to proxies for *common* causes.
   A variable that is simultaneously a proxy for a cause of the exposure only and a proxy for
   a cause of the outcome only *is* the M-diagram collider, so the loose version of this step
   re-introduces the bias step 2 was designed to avoid.
5. Then fit: either one regression on the whole selected set, or — preferably where the sample
   supports it — a principled machine-learning estimator (the paper names targeted maximum
   likelihood) that handles post-selection inference internally.

**Covariate timing, as a construction knob.** If exposure and covariates are measured at the
same time, a covariate cannot be told apart from a mediator; the paper's remedy is to take the
covariate from the **wave before** the exposure, and to include the **prior level of the
exposure** as well. With repeated measurement this is a free design improvement and it is
also a sensitivity analysis: fit with contemporaneous covariates and again with lagged ones
and compare.

**What the paper says about letting the data pick the set** — and this is the part that bears
directly on a lab that already runs penalised models:

- **Statistics alone cannot do it.** No test distinguishes a confounder from a mediator,
  because neither temporal order nor causal direction is in the joint distribution. Some
  substantive knowledge is required *before* any selection procedure runs.
- **Backward and forward selection preserve sufficiency** — if the full set suffices and every
  include/exclude decision is made correctly, the selected set suffices too (forward selection
  needs an extra faithfulness assumption). But the decisions are made with `p`-values, so
  "correctly" is doing real work, and **inference after selection is invalid**: fitting the
  final model on the selected set gives estimates and intervals that are not what they claim.
  Selecting on half the data and fitting on the other half is valid and costs a large amount
  of precision.
- **Backward selection has a self-defeating precondition**: it requires that the full model be
  fittable. If it is, you could simply have used the full model.
- **The change-in-estimate rule (drop unless the estimate moves > 10%)** inherits every
  problem above and adds one of its own: it is **invalid for non-collapsible measures** (odds
  and hazard ratios with a common outcome), where the estimate moves on adjustment even in a
  randomised trial, and can also fail to move on adjustment for a real confounder because
  confounding and non-collapsibility offset.
- **The high-dimensional propensity score** — rank covariates by an approximate bias
  contribution built from each covariate's outcome association and its exposure prevalence,
  keep the top fraction — uses both associations and is therefore better aimed than stepwise,
  but **loses the sufficiency property** because it screens one covariate at a time
  *marginally* rather than conditionally on the others.

## Robustness evidence (qualitative only)

Analytic rather than empirical: the sufficiency property of the disjunctive cause criterion is
a theorem over all causal diagrams, not a finding in a sample, so there is no sample period,
no market and nothing to decay. The two qualifications are each supported by their own
literatures (the bias-amplification result has since been proved in general — see the
companion note) and the paper is explicit that the proxy qualification is **not guaranteed**
to reduce bias, only usually to.

The author is one of the two authors of the originating disjunctive-cause result and a
co-author of the general Z-bias theorem, so the synthesis is by someone with the track record
in the area. The paper presents itself as "not definitive" and as a starting point for
refinement — read that as the honest statement it is, not as a hedge.

## Implementability here

**What this maps onto.** The lab runs two objects that are conditioning sets chosen without a
rule. (i) The **mandatory joint control** — within-region rank-space OLS residual of a score
on log `P` and `vol126` — applied nine times before it was first calibrated. (ii) The
**covariate list for a balance test** on which names a book holds (`#442`–`#445`), where
`#444` establishes that each covariate the book does not shift costs power. Both are
conditioning sets, both were assembled by accretion (`vol126` and `amihud126` from the lab's
own closures, region from the 2026-09-03 `lv_illiq_region_relative` win, log `P` from
`#420`–`#426`), and the folder has never held a source on how such a list should be chosen.

Translating the roles is straightforward and the translation is what makes the rule usable:
**exposure `A` = the thing the candidate does** (a score's rank, or `eligible = 1`, or
hold/not-hold), **outcome `Y` = the forward return**, **covariates `C` = the observables**.
Note the lab's controls are applied as a residualisation of the *score*, not as a propensity
model, but the rule is about which variables enter the conditioning set and is indifferent to
the fitting device.

**The usable rule, in the lab's terms.** Admit a control if it is plausibly a cause of the
score **or of the forward return**; drop it if it is a cause of the score and plausibly
unrelated to the forward return; add a variable that is neither but is a **proxy for something
that drives both**, and only if it is a proxy for something driving *both*. Two of the lab's
own controls can be read against this immediately: log `P` entered as a **score-side
contaminant** (Amihud is proportional to `1/price`, and the back-adjusted level is the subject
of the engine issues filed 2026-10-18 / 2026-10-22), which is the *exposure* side of the
criterion — the rule says that is the side that needs the extra scrutiny, not the side that
licenses inclusion. The decisive question the lab has never asked of a candidate control is
**whether it is related to the forward return at all**.

**The pre-exposure restriction is not satisfied automatically here and it is cheap to get
wrong.** A control computed over a trailing window that ends *after* the score's own
as-of date is the mediator case: it is partly an effect of the thing being measured.
`vol126` and log `P` as of the rebalance date are fine; a control that peeks past it is both a
causality-check failure and a mediator.

**What the criterion cannot give this lab, stated plainly.** Step 2 needs per-covariate causal
knowledge, and the lab does not have a causal diagram for its panel — what it has is the
measured fact that log `P` carries an engine artifact. So the criterion is usable here as a
**checklist that forces the question** ("is this a cause of the score, of the return, or
neither?") and as a **veto on three specific moves**, not as an algorithm. The three vetoes
are the transferable part:

1. **Do not select controls by how well they predict the score.** This is the same statement
   `#441` makes about regularisation and `#440` makes about the AUC, arriving from the
   conditioning-set side. See the companion note for the simulation that prices it.
2. **Do not use a change-in-estimate threshold as the admission rule for a control** — which
   is close to what the lab does when it keeps a control because it moved a reading. The rule
   is invalid for non-collapsible measures; a Sharpe difference or a bps/yr reading is not an
   odds ratio, so the non-collapsibility clause does not bite directly, but the prior clause
   does: a 10%-style threshold can fire on sampling variation, and the lab's own record holds
   a control that *created* a reading (`rank_stability`, US +212 → +483) rather than removing
   one.
3. **Treat any data-driven control selection as costing the validity of the interval that
   follows it.** The lab's gate is a point estimate against a bar, with a bootstrap interval
   and a deflated-skill correction for the number of trials. **Choosing the control set by
   looking at the data adds a selection the deflator does not count**, because the deflator
   counts recorded trials and a control choice is not a trial. This is the same hole `#437`
   exists to remove for coarsening choices and `#444` for the sum-type/max-type choice: the
   repair is the same one — **pre-register the control set before the reading**.

**Cost profile: free.** No trial, no fitting, no data. It is a checklist run before a
candidate file is written, which puts it alongside `#413`'s composed pre-trial rule.

**Pitfall specific to this panel.** The M-diagram is not hypothetical here. A variable that is
a common *effect* of two unmeasured drivers — one touching the score, one touching returns — is
exactly what a liquidity-ish observable on a point-in-time index panel can be, because
index admission is itself a selection (`#416`–`#418`) and conditioning on a consequence of it
is conditioning on a collider. `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md`
already records that observables cannot deliver strong ignorability for admission on this
panel; the present note says what to do with that fact — **not** adjust for more things.

## Related

- `notes/2026-11-15-covariate-selection-for-the-propensity-score.md` (same session) — the
  simulation that prices steps 2 and 3 in bias and variance, and shows the best-predicting
  exposure model is not the best conditioning set.
- `notes/2026-11-15-instrumental-variables-as-bias-amplifiers.md` (same session) — the general
  theorem behind step 3, and the free with-and-without diagnostic for when you cannot tell an
  instrument from a confounder.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` — the lab's own
  selection-as-treatment framing and the finding that observables cannot deliver strong
  ignorability for index admission.
- `notes/2026-11-13-accuracy-tests-are-underpowered-for-signal-detection.md` and
  `notes/2026-11-14-sparse-alternatives-and-the-precision-transformed-test.md` — `#441`'s
  "testing requires less regularization than predicting" and `#444`'s covariate-list cost,
  which this note's step 2 both complements and, on one point, is in tension with (see the
  cross-note tension recorded in `SUMMARY.md`).
- `notes/2026-09-09-specification-curve-analysis.md` and
  `notes/2026-11-12-coarsened-exact-matching-as-applied-construction.md` — the post-selection
  inference problem in its other two appearances in this folder.
