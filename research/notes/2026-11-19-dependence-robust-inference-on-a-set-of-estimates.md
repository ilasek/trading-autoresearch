---
title: "Meta-analysis with Robust Variance Estimation: Expanding the Range of Working Models — with: Robust variance estimation in meta-regression with dependent effect size estimates"
authors: Pustejovsky & Tipton; Hedges, Tipton & Johnson
year: 2021; 2010
venue: "Prevention Science 2021 (peer-reviewed, Tier 1/2 for methods in its field); Research Synthesis Methods 1(1) 2010 (the field's methods journal, Tier 1 for this literature)."
url: "https://doi.org/10.1007/s11121-021-01246-3 (read in full from https://events.brown.edu/live/files/594-pustejovsky-tipton-2021pdf) ; https://doi.org/10.1002/jrsm.5 (NOT obtained — see Access)"
citations: "Pustejovsky–Tipton 2021: 632 (Crossref, checked 2026-11-19). Hedges–Tipton–Johnson 2010: 1,902 (Crossref, checked 2026-11-19). Tipton 2015 (Psychological Methods, 10.1037/met0000011, the small-sample correction): 746 (Crossref, checked 2026-11-19) — named, not read."
sample_period: "No market estimation window. An applied re-analysis of a meta-analytic database of randomized trials of brief alcohol interventions, plus Monte Carlo simulations at 30 and 60 primary studies per meta-analysis."
markets: "None. The object is a set of effect-size estimates with standard errors, not an asset panel."
tier: "A− for Pustejovsky–Tipton (peer-reviewed, the field's two leading methodologists, simulations with stated misspecification conditions, software named and public, and the authors state their method's own risk of analytic flexibility). B for the Hedges–Tipton–Johnson lineage, which is recorded at second hand and graded only on its 1,902 citations and this paper's description of it."
validation_overlap: false
published_post_2018: true
---

## Access

**Pustejovsky–Tipton 2021 read in full** from `events.brown.edu/live/files/594-pustejovsky-tipton-2021pdf`
(HTTP 200, 1.16 MB, 28 pages, `pdftotext -layout` into 92 KB with 528 `" the "`, publisher header and
DOI on line 1). **A university events server is a channel worth adding to the recipe**: a methods
talk's hosted paper copy is often the typeset version of record, and the path has no `.pdf`
extension, so a filename-shaped search will miss it.

**Two negative channel results, both already predicted by this file's own notes.**

1. `core.ac.uk/download/96781181.pdf` returned **HTTP 403 with a 5,393-byte body** — the Cloudflare
   challenge recorded on 2026-10-01. Confirms the standing entry; do not retry.
2. `www.ipr.northwestern.edu/documents/training-documents/theoretical-introduction-hedges.pdf`
   returned a genuine 980 KB, 8-page PDF by the right author on the right topic — and it is a
   **slide deck**, not the paper: "Meta-regression with Dependent Effect Size Estimates", Larry V
   Hedges, presented at the Joint Cochrane Campbell Colloquium, Keystone, October 2010. This is the
   twelfth "looks like an answer" mode (2026-10-14) a second time, and **tonight supplies a new,
   cheaper tell for it: the `" the "` count was ZERO.** Slide decks set text with non-breaking or
   figure spaces, so the whitespace-delimited word count that this file prescribes as the
   Caesar-shift detector doubles as a slide-deck detector — a `" the "` count of 0 on a 39 KB
   extract means the file is not prose. The deck was read only far enough to confirm what it is;
   **Hedges–Tipton–Johnson (2010) is therefore recorded as a named, unobtained source**, described
   here through Pustejovsky–Tipton's own account of it, and graded B on that basis.

## Mechanism

This is the **dispersion half** of the folder's standing aim, and it answers the aim's third
criterion — what dependence among the statistics does to the diagnostic — with a clean and
unwelcome split.

The object is a set of effect-size estimates produced by one synthesis: `T_ij` is estimate `i` from
study `j`, with standard error `s_ij`, for `i = 1,…,n_j` and `j = 1,…,J`. The meta-regression model
is `T_ij = x_ij β + u_ij + e_ij`, where `e_ij = T_ij − θ_ij` is sampling error with `E[e_ij] = 0`
and `Var(e_ij) = s²_ij`, and `u_ij` is variation in the true effects beyond what the covariates
explain. Estimates from **different** studies are assumed uncorrelated; estimates from the **same**
study are allowed to be correlated, "although typically, the analyst will not know the exact degree
of correlation."

**Robust variance estimation (RVE) is the instrument, and its logic is the mechanism.** It
"separates the choice of a set of weight matrices from the method of estimating standard errors, so
that standard errors can be obtained without having to assume a known dependence structure." You
supply a **working model** that only *approximates* the dependence. Then:

- **Even when the working model is misspecified**, the meta-regression coefficient estimates are
  unbiased and "their standard errors (along with hypothesis tests and confidence intervals) will
  provide valid quantification of uncertainty."
- **The benefit of a better working model is efficiency, not validity** — more precise coefficient
  estimates, not more honest intervals.
- **Why it works, and therefore what it costs.** The estimator averages products of residuals, and
  "even though each product of residuals provides only a very crude estimate, the RVE standard errors
  are nonetheless valid because they involve an **average** of the residual products, which will be
  accurate if calculated across a **sufficiently large number of studies**." The price is paid in the
  number of independent clusters, exactly as the Driscoll–Kraay vein (`#467`–`#476`) pays its price
  in required panel length.

**And here is the split, which is the finding.** The authors state the trade-off in their own words:
analysts "are left to choose between using RVE—which guards against model misspecification yet does
**not** emphasize descriptions of heterogeneity—and multivariate meta-analysis—which can provide
heterogeneity estimates but does **not** guard against misspecification." Under RVE the variance
components are not "a parameter used for description or inference", and the authors note this "is
where RVE diverges markedly from standard meta-analytic methods, where variance component estimates
are considered an important component of synthesis results."

So: **dependence-robust inference on a set of estimates delivers the set's MEAN and declines to
certify the set's SPREAD.** That is the direct answer to the aim's criterion (iii) on the dispersion
side, and it is a refusal rather than a correction. Their proposed hybrid — treat the richer
multivariate variance structures *as* working models inside the RVE framework — is an attempt to get
both, and its success is what the simulations test.

## Construction recipe

**The four working models, in the order they were proposed.** Choosing among them is the whole
decision.

1. **HE — hierarchical effects.** Dependence arises "solely through common features of a lab or
   research group, while within a lab or group, each effect size is estimated on an **independent
   sample**."
2. **CE — correlated effects.** Dependence arises because the estimates come from the **same
   sample** (multiple measures of one construct, or one outcome at several time points). The usual
   implementation adds the **constant sampling correlation** assumption: a single, known correlation
   `ρ` between every pair of estimates within a study, the same across studies.
3. **CHE — correlated and hierarchical effects.** Combines them: between-study heterogeneity `τ` and
   within-study heterogeneity `ω` in the true effects, *plus* within-study correlation among the
   estimates. The authors expect CHE "will be a first choice as a working model in many
   applications, especially when **little information is available** about correlations between
   included effect size estimates."
4. **SCE — subgroup correlated effects**, their new proposal. Classify every estimate into one of `C`
   categories via indicators `d_ij1,…,d_ijC`, then interact both the covariates and the random effect
   with those indicators:
   `T_ij = d_ij1 x_ij β_1 + d_ij2 x_ij β_2 + ⋯ + d_ijC x_ij β_C + d_ij1 u_1j + ⋯`.
   This "embeds the assumptions of separate meta-regression analyses into a working model for the
   full data", reproducing each subgroup's own result **while letting the subgroups be compared
   inside one model**. The reason it is needed is the reason it matters here: running separate
   analyses per subgroup makes differences across subgroups unquantifiable, because "if the
   sub-groups include **overlapping sets of studies**, the pooled effect sizes from each sub-group
   are **not independent**."

**The three-step procedure.** (i) Choose the working model from the decision tree — do the samples
contribute multiple estimates? how much is known about the sampling correlations? is there a
hierarchical structure? (ii) Fit it (REML variance components, inverse-variance weight matrices,
coefficients) — `metafor`'s `rma.mv()` in R. (iii) **Then** compute RVE standard errors, tests and
intervals on top of it — `clubSandwich`'s `coef_test()`, `conf_int()` and `Wald_test()`. Step (iii)
is the misspecification guard and is separate from step (ii) by design.

**The authors' own pre-registration rule, which is the most portable thing in the paper.** The extra
flexibility "requires analysts to make a larger number of decisions and thus expands the
possibilities for analytic flexibility or 'researcher degrees of freedom'—even **the meta-analytic
equivalent of p-hacking**." Their remedy, stated as a recommendation: "the working model be chosen
based upon a broad understanding of the data structure and data-generating process—**not by comparing
how meta-regression results change (or do not) over different working models or assumptions**."

**Small-sample adjustments** to reduce RVE's small-sample bias exist and are named (Tipton 2015;
Tipton & Pustejovsky 2015), implemented in `clubSandwich`. Not read here.

## Robustness evidence (qualitative only)

- **Simulations with deliberate misspecification.** Designs mimic the applied database but at
  **30 or 60 primary studies** per meta-analysis, under mild misspecification (right general form,
  wrong assumed sampling correlation) and strong misspecification (wrong structure entirely).
- **Coverage held.** Confidence intervals from the new CHE and SCE working models — and from the
  older CE model — were "appropriately calibrated", with coverage "close to or above the nominal 95%
  rate", and "had near-nominal coverage rates **even when the working model was quite discrepant from
  the true data-generating model**." This is the paper's central robustness claim and it is about
  the *coefficients*.
- **The variance components behaved better than the authors expected, with a caveat.** REML variance
  component estimators looked more sensitive to modelling assumptions than the CE moment estimator,
  but that sensitivity "was not necessarily indicative of reduced accuracy": the two had similar
  accuracy when CE was correct or mildly misspecified, and CHE's REML estimator was **consistently
  more accurate** when the truth included within-study heterogeneity. So the hybrid does recover some
  of what plain RVE gives up — "albeit with some sensitivity to the assumed value of the sampling
  correlation."
- **Where the choice matters and where it does not.** The new working models "could make a
  substantial difference for models that included effect-size-level predictors but made little
  difference for models with only **study-level** predictors."
- **Sensitivity to the assumed `ρ`** showed up above about 0.8 and was otherwise stable.
- **Two honest limits**: the authors caution against reading differences in standard errors across
  working models as substantive, and they say plainly that not all of the models they fit "should be
  applied or reported in practice."
- **Lineage, graded down.** The RVE result itself (coefficients consistent and asymptotically normal
  without knowledge of the covariance structure, valid even with random covariates) is
  Hedges–Tipton–Johnson 2010, **recorded at second hand** — 1,902 Crossref citations and this paper's
  description, not the article.

## Implementability here

Not a strategy. This is the instrument for reading the lab's own board under dependence, and it
mostly tells the lab to stop reading one particular number. Four findings.

- **`#489` — the lab's under-dispersion headline is a VARIANCE-COMPONENT claim, which is exactly the
  quantity the dependence-robust framework declines to certify.** The 2026-11-18 nightly's finding —
  `sd(skill)` 0.1233 against `rms(skill_se)` 0.1391, ratio 0.785, implied `var(true skill)` −0.0042,
  `p` 0.740 — is an estimate of `τ²` in this paper's notation. The RVE answer to "what does dependence
  among the estimates do to it" is not a correction: it is that the estimator which *is* robust to
  unknown dependence gives a valid **mean and coefficient** for the set and treats the variance
  component as not available "for description or inference". **The honest restatement of the
  nightly's finding under dependence is therefore about the board's common mean, not its spread** —
  and a negative implied `τ²` is, on this reading, the expected output of asking the robust machinery
  a question it does not answer, not a discovery about the board. The finding survives as a
  descriptive statement ("the measured skills are no more spread out than their own error bars"),
  and it should not be quoted as a test that the 27 objects have identical true skill.
- **`#490` — the cost is in the number of independent clusters, and the lab is below the smallest
  panel this literature validates.** RVE's validity rests on averaging residual products "across a
  sufficiently large number of studies", and these simulations go no lower than **30** primary
  studies. The lab has **27** recorded trials and, by its own audit, **7–12 independent bets**. This
  is the second source in two sessions to price a dependence-robust estimator in units the lab does
  not have (`#469`, `#475`–`#476` priced Driscoll–Kraay in required `T`; this prices RVE in required
  `J`). **Two independent literatures now say the same thing: the lab's board is too small to carry
  a dependence correction, whichever axis the dependence is on.** Note the small-sample adjustments
  (Tipton 2015) exist and are unread — that is the one remaining lead on this, and it is the only
  reason to reopen the question.
- **`#491` — the SCE working model is the right shape for the lab's actual comparison, and the reason
  it exists is the lab's exact problem.** The lab's recurring question is whether one **family's**
  lead differs from another's, and its families are precisely `C` categories of estimate. The authors
  built SCE because subgroup results computed on **overlapping samples are not independent** and so
  cannot be compared across subgroups — and every one of this lab's trials is computed on the **same
  dates and the same panel**, which is total overlap, the `CE`/`SCE` structure rather than the
  hierarchical one. So if the lab ever does want a dependence-aware comparison of family leads, the
  construction is: one model over all trials, covariates and random effect interacted with family
  indicators, RVE standard errors on top, clustering on the **mechanism** (the leaderboard's
  `distinct_mechanisms`, not the family label). **That is a correctly-shaped construction that the
  lab cannot presently afford** (`#490`), which is worth writing down precisely so a later session
  does not reinvent it at the same cluster count.
- **`#492` — a composed pre-trial rule, and it is free.** This paper's own anti-flexibility
  recommendation generalises past meta-analysis, and it is the discipline the lab's three nightly
  diagnostics have been missing: **fix the model for your own board's dependence from what you know
  about how the trials were generated, before you look at what it does to the answer — never by
  comparing how the answer moves across specifications.** Composed with `#488` from tonight's
  companion note: *state the selection function and the dependence working model before reading a set
  of your own statistics, and record both in the journal entry that reports the reading.* Had that
  rule been in force, the 2026-11-16 (`null_pctile` as `U(0,1)`) and 2026-11-18 (`sd(skill)` vs
  `rms(skill_se)`) readings would each have had to declare their dependence assumption up front, and
  both would have declared independence — which `#490` says is the one assumption the board cannot
  support.

**Pitfall.** The constant-sampling-correlation assumption is the soft spot. It is a single `ρ`
imposed across all studies, and the simulations find sensitivity above `ρ ≈ 0.8`. The lab's
cross-trial active-return correlation is `+0.0888` on average, which is comfortably inside the
stable region — but an *average* is not a constant, and the folder's own audit of 27 trials into
7–12 mechanisms says the within-mechanism correlations are far higher than the average. **Assume
the constant-`ρ` version is wrong here and rely on the RVE layer, not on the working model.**

## Related

- The two companion notes from the same aim, and the `p`-value half of it:
  `notes/2026-11-19-the-null-shape-of-a-set-of-ones-own-p-values.md` and
  `notes/2026-11-19-the-power-of-those-tests-and-the-selection-function-this-lab-runs.md`.
- `notes/2026-11-18-covariance-estimation-without-specifying-cross-sectional-dependence.md`,
  `notes/2026-11-18-the-unbalanced-panel-formula-and-when-not-to-use-it.md`,
  `notes/2026-11-18-inference-without-a-bandwidth-and-the-distortion-that-does-not-shrink.md` —
  the Driscoll–Kraay vein (`#467`–`#478`). This is the same question asked of a set of *estimates*
  rather than a *panel*, and it reaches the same verdict about cluster count.
- `notes/2026-11-17-clustering-as-a-design-question-not-a-correlation-question.md` — `#461`'s
  anti-correction at few clusters, which `#490` now corroborates from a second literature.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` and the
  `distinct_mechanisms` material — the lab's own clustering of its trials, which `#491` needs as its
  cluster variable.
- Named and unobtained: Hedges, Tipton & Johnson (2010) `10.1002/jrsm.5` (two dark channels
  recorded above — do not re-hunt `core.ac.uk`); Tipton (2015) `10.1037/met0000011`, the
  small-sample correction, which is the one live lead on `#490`; Tipton & Pustejovsky (2015).
