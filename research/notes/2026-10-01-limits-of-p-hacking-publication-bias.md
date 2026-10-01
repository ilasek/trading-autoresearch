---
title: "The Limits of p-Hacking: Some Thought Experiments — with: Publication Bias and the Cross-Section of Stock Returns"
authors: Chen; Chen & Zimmermann
year: 2021; 2020
venue: "Journal of Finance 76(5), 2447–2480 (Tier 1); Review of Asset Pricing Studies 10(2), 249–289 (Tier 1). Both read from their Federal Reserve FEDS working-paper versions: FEDS 2019-016 (titled 'The Limits of p-Hacking: a Thought Experiment', January 2019) and FEDS 2018-033 (May 2018)."
url: "https://doi.org/10.1111/jofi.13036 (read from https://www.federalreserve.gov/econres/feds/files/2019016pap.pdf) ; https://doi.org/10.1093/rapstu/raz011 (read from https://www.federalreserve.gov/econres/feds/files/2018033pap.pdf)"
citations: "Chen 2021: 57 (Crossref, checked 2026-10-01), 61 (OpenAlex, checked 2026-10-01). Chen–Zimmermann: 85 (Crossref, checked 2026-10-01), 86 (OpenAlex, checked 2026-10-01)."
sample_period: "No market estimation window of their own. Chen fits the distribution of published t-statistics in two hand-assembled corpora: Harvey–Liu–Zhu's 316 factors and Chen–Zimmermann's 156 predictors. Chen–Zimmermann replicate 156 published cross-sectional predictors over each study's own original in-sample window (earliest starts in the 1920s–1960s; latest original samples end in the 2000s) plus post-publication data."
markets: US equities (CRSP/Compustat/IBES/OptionMetrics), via the published-predictor literature rather than a single panel
tier: "A for Chen–Zimmermann (Tier-1 venue, open replication data, an estimator with a stated identification argument, explicit about the HLZ disagreement it cannot reconcile). A− for Chen 2021: Tier-1 venue and a clean argument, but it is a calibration exercise on an exactly-identified model, which the author says himself provides no formal test."
validation_overlap: false
published_post_2018: true
---

## Access

**Both read in full** from `federalreserve.gov/econres/feds/files/`, which served parseable PDFs on
the first request for both. **FEDS is a reliable channel and belongs in the folder's recipe** alongside
NBER and arXiv: Federal Reserve Board staff working papers carry DOIs of their own
(`10.17016/FEDS.YYYY.NNN`), the file naming is mechanical (`<year><number>pap.pdf`), and both
published versions here are closed at the publisher (Unpaywall reports `is_oa: false` for both DOIs).

Both titles changed between working paper and journal — "a Thought Experiment" became "Some Thought
Experiments" — so a title search will miss one of the two. Resolve by DOI or by author.
`pypdf` emits `fontTools is required…` warnings on these files; the text extracts correctly anyway.

## Mechanism

These two papers are the standing **counterweight** to the data-snooping explanation of
cross-sectional predictability. Both name Linnainmaa–Roberts explicitly as the view they argue
against, so the disagreement is direct rather than inferred.

**Chen (2021): p-hacking cannot generate the observed tail.** Take the cynical story completely
seriously and write it down. Assume every factor is false, so all t-statistics — published and not —
are i.i.d. standard Normal. Assume a factor with t-statistic `t` is published with probability `p(t)`,
an increasing step function with free parameters. Fit `p(·)` to the observed histogram of published
t-statistics by method of moments; the model is exactly identified and fits either corpus very well.

Then ask the model a question it was not fitted to answer: **how often does a randomly drawn
t-statistic get published?** The staircase form gives it in closed form, and the answer is about
`1e-14`. The reason is a mismatch of supports: the published histogram has a very fat right tail (10%
of the Harvey–Liu–Zhu t-statistics exceed 6.34), and under a standard Normal those values are
essentially unreachable, so the fitted model is forced to set the publication probability for
`t < 6.0` to something infinitesimal in order to match the shape. The implied ratio of unpublished to
published factors is on the order of 100 trillion to one. Converted into labour: 10,000 economists
mining data eight hours a day, producing one factor per economist-hour, would need hundreds of
millions of years to publish 100 factors; even at ten factors per economist-second it is 15,000 years.
The conclusion is not that there is no p-hacking — it is that **p-hacking alone cannot be the whole
explanation**, because the fat right tail of published results is not a shape that selection on noise
can produce at any plausible intensity.

Chen is explicit about the argument's status: the model is exactly identified, so the fit itself is
not evidence; the discipline comes entirely from the thought experiment, in the same way
Mehra–Prescott's calibration disciplines power utility. The independence assumption is defended
empirically rather than theoretically — the average pairwise correlation between published predictor
returns is about **0.03**, with 80% of pairwise correlations between −0.36 and +0.43, and principal
component analysis needs a large number of components to span the set.

**Chen–Zimmermann (2020): the size of the bias, estimated rather than assumed.** Instead of asking
whether selection exists, estimate how much it inflates a published return. The estimator is empirical
Bayes: the family of 156 replicated predictors identifies the dispersion of *true* returns, and each
individual predictor is then shrunk toward the family. The headline is that **publication-bias-adjusted
returns are only about 12% smaller than in-sample returns.**

The intuition is the whole paper and it is worth stating carefully, because it inverts the usual
multiple-testing reflex. Running many tests does raise the chance of lucky rejections — but the many
tests also carry information a single test does not: they reveal the **dispersion** of the underlying
effects. The observed spread of in-sample returns across published predictors is far wider than pure
selected noise could produce. A wide true-effect distribution means each individual t-statistic is
highly informative about that predictor's true return, which means little shrinkage is warranted.
Hence their second, counterintuitive implication: the false discovery rate among published predictors
is about **1.5%**, and a t-statistic hurdle of **1.79** — *below* the conventional 1.96, and far below
Harvey–Liu–Zhu's 2.88 — already delivers a 1% FDR. The authors are candid that they cannot reconcile
their hurdle with Harvey–Liu–Zhu's and suggest the difference is that HLZ's corpus is factors broadly
defined while theirs is cross-sectional predictors only.

The third result is a decomposition. Of a typical anomaly's gross long-short return, **12% is
publication bias; about 35% is mispricing that gets traded away after publication (McLean–Pontiff);
and much of the remaining ~53% is accounted for by trading costs (Chen–Velikov).** Note what that
leaves: on this accounting the statistical discount is the *smallest* of the three terms, and
**costs are the largest.**

## Construction recipe

Chen's calibration is a diagnostic, not a construction. Chen–Zimmermann's estimator is directly
implementable and is the reason this note exists.

**The shrinkage formula.** With `σ_i` the standard error of candidate `i`'s measured in-sample
(long-short, or here validation) return, and `σ̂_μ` the estimated cross-sectional dispersion of *true*
returns across the family of candidates, the normal approximation to their full estimator is

    Shrinkage_i = σ_i² / (σ̂_μ² + σ_i²)
    Bias-adjusted return_i = (1 − Shrinkage_i) × In-sample return_i

Three properties of that line matter:

1. **It is a noise-to-signal ratio, not a count.** The shrinkage depends on the candidate's own
   standard error and on the dispersion of the candidate family — and **not at all on how many
   candidates were tried.** This is the formal contrast with Bonferroni-style and deflated-Sharpe-style
   adjustments, which take the no-predictability null from the single-test setting and scale by the
   trial count.
2. **The intensity is data-determined**, with no free parameter: `σ̂_μ` is identified by the observed
   spread of in-sample results. Their own headline falls straight out of it — mean standard error
   0.19% per month against `σ̂_μ ≈ 0.45` gives `0.19²/(0.45² + 0.19²) ≈ 15%`, close to the full
   model's 12%.
3. **It shrinks the noisy candidates hardest**, which is the opposite ordering from a count-based
   deflator: short samples and volatile portfolios are the ones more likely to have got lucky. The
   approximation fits most of the 156 portfolios but under-shrinks those with the very highest
   in-sample returns, because the full model carries a fat tail in true returns that the normal
   approximation does not.

**The identification check, which is the part to copy.** Before trusting any such adjustment, compare
the observed distribution of in-sample results against what a large-bias model would predict. Their
Figure 7 is exactly this: the estimated model reproduces the observed spread of published returns,
while models imposing large publication bias (a small `σ̂_μ`, a high t-cutoff) do not. **The dispersion
of outcomes across candidates is the identifying moment**, and a session proposing any
selection correction should show that moment first.

**Chen's falsifier, as a reusable test.** Fit a pure-selection model to a set of selected results,
then compute the implied probability that a random candidate is selected and convert it into a
resource cost (candidates tried, hours spent). If the implied cost exceeds what could plausibly have
been expended, the selection story is not sufficient on its own. This is cheap, needs only the
distribution of selected statistics, and is a one-sided test — it can refute "all selection", never
confirm "no selection."

## Robustness evidence (qualitative only)

- Both papers rest on Chen–Zimmermann's open replication of 156 published predictors, which is public
  and has become a standard dataset in this literature. That is unusually strong methodological
  honesty for a publication-bias paper, and it is why the cluster grades Tier A.
- Chen's calibration result is robust to which corpus is used (the two give `6.5e-15` and `1.2e-14`)
  and, the author reports, to the histogram edges. It is **not** a formal test: the model is exactly
  identified, and the author says so in the text rather than burying it.
- The independence assumption in Chen's model is the obvious attack surface, and he defends it with
  measured correlations rather than argument. The defence is reasonable for a corpus of accounting-
  and event-based predictors; it would be weaker on a corpus dominated by a few related mechanisms.
- **The disagreement with Harvey–Liu–Zhu is unreconciled and the authors say so.** A t-hurdle of
  1.79 and a t-hurdle of 2.88 are not a rounding difference, and the stated candidate explanation
  (different corpora) is offered as a hypothesis for future work, not as a resolution. This folder
  should not treat either hurdle as settled.
- **The disagreement with Linnainmaa–Roberts is the live one**, and is the reason these notes were
  written in the same session. Two Tier-A studies of the same literature put the discovery-window
  inflation at ~12% and at 40–60% respectively. They are not measuring quite the same object —
  Linnainmaa–Roberts compare realised returns across eras for accounting anomalies; Chen–Zimmermann
  estimate a shrinkage from the cross-candidate dispersion for a broader predictor set — but the gap
  is far too large to be explained away on that basis, and neither note in this folder retracts the
  other.

## Implementability here

No candidate. The deliverable is a **second, independent discount on a measured result**, with a
different functional form from anything this folder has filed, plus a correction to how the first one
should be read.

**The direct use: a magnitude to go with the lab's significance gate.** `program.md`'s promotion rule
deflates by the total number of trials ever recorded and asks for a probability ≥ 0.95. That is a
*significance* statement. The 2026-09-15 session recorded the gap in writing — this folder's
multiple-testing notes "all ask whether the best of `N` is *significant*, and none asks what the best
of `N` is *worth*" — and Tweedie's formula was filed as the partial answer. **Chen–Zimmermann is the
rest of the answer, in a closed form the lab can evaluate on data it already stores.** The lab holds
104 recorded trials with validation returns. The dispersion of their validation performance identifies
`σ̂_μ`; each trial's own standard error gives `σ_i`; the formula then returns a per-candidate
bias-adjusted expected return. Free, no trial, no holdout, and it answers the question the deflator
does not ask: *by how much should a promoted candidate's measured edge be marked down?*

**The uncomfortable implication of running it, and the reason it should be run anyway.** The
estimator's intensity is governed by `σ̂_μ`, the dispersion of *true* performance across candidates.
This lab's trial history is heavily concentrated in one family — 34 of the first 55 trials and all
promotions in `price-trend` — and a family of near-variants has a genuinely small true dispersion.
A small `σ̂_μ` drives `Shrinkage → 1`. **So the formula predicts that a sweep of close variants should
be shrunk almost to nothing, while a set of genuinely different mechanisms should be shrunk very
little** — which is the same conclusion `program.md`'s breadth mandate reaches on other grounds,
arrived at from estimation theory rather than from search policy. Two consequences:

- Running the estimator **on the full 104-trial history pooled** would understate `σ̂_μ` and
  over-shrink everything. Computing it **per family** and comparing is the informative version, and
  the comparison is itself the finding.
- This is a reason to compute the adjustment, not to act on a single number from it. It is a
  diagnostic for the human and for the folder, not a new gate — `CLAUDE.md` forbids reinterpreting
  the protocol's thresholds, and nothing here is a proposal to do so.

**The correction to how the costs line should be read.** On Chen–Zimmermann's decomposition, the
largest single slice of a typical anomaly's gross return is **trading costs**, and the statistical
discount is the smallest. For a lab paying 15 bps per side with a one-day execution lag, that
reorders the list of things worth worrying about: the deflator is not what is standing between this
repo and a decorrelated challenger, and `program.md` already says as much from its own measurement
("the deflator is not what was stopping exploration"). This note is independent, literature-side
corroboration of that specific claim.

**What not to do with this.** (i) Do not import the 12%, the 1.5% FDR or the 1.79 hurdle as
constants. They are estimated on US published cross-sectional predictors with multi-decade original
samples, under a referee filter this lab does not have; `CLAUDE.md`'s rule against carrying constants
across contexts applies. What transfers is the **formula and its identifying moment**. (ii) Do not
read "publication bias is small" as "this lab's selection problem is small" — the lab selects on a
six-year validation window with a far smaller effective sample than a published study's original
sample, which makes `σ_i` larger and therefore the shrinkage *larger*, not smaller, under the same
formula. (iii) Do not use the Chen calibration to dismiss the Linnainmaa–Roberts note. It refutes
"everything is selection"; it does not establish any particular small value for the discount, and the
authors of both papers agree on the sign.

## Related

- `research/notes/2026-10-01-discovery-sample-and-anomaly-decay.md` (this session) — **the stated
  tension.** Linnainmaa–Roberts puts the discovery-window inflation at 40–60%; these papers put it at
  ~12%. Both are Tier A, both are cited by the other, and neither is retracted here.
- `research/notes/2026-09-15-tweedies-formula-empirical-bayes-selection-bias.md` — the same empirical-
  Bayes idea applied to a single selected maximum. Chen–Zimmermann is the family-level version with an
  identification argument attached, and together they close the "what is the best of `N` *worth*" gap
  that note opened.
- `research/notes/2026-08-24-deflated-sharpe-ratio.md` and the folder's multiple-testing cluster
  (effective number of trials, `meff`, familywise error) — all count-based. This note's formula is
  **not** count-based, and the contrast is the point: dispersion across candidates, not their number,
  sets the shrinkage.
- `research/notes/2026-08-17-mclean-pontiff-publication-decay.md` — supplies the 35% mispricing term
  in the decomposition above.
- `research/notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the other source in this
  folder that treats dispersion-across-researchers as the informative object.
