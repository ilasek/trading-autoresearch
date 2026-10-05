---
title: "The History of the Cross-Section of Stock Returns"
authors: Linnainmaa, Roberts
year: 2018
venue: Review of Financial Studies 31(7), 2606–2649 (Tier 1). Read from NBER Working Paper 22894 (December 2016), which is the pre-publication version of the same study.
url: https://doi.org/10.1093/rfs/hhy030 · full text read from https://www.nber.org/system/files/working_papers/w22894/w22894.pdf
citations: 260 (Crossref is-referenced-by-count, checked 2026-10-01); 297 (OpenAlex, checked 2026-10-01). Semantic Scholar does not resolve this DOI (checked 2026-10-01).
sample_period: 1918–2015 (CRSP returns 1926-01 to 2015-12; hand-collected Moody's Industrial and Railroad manual accounting data back to 1918; Compustat from 1947, comprehensive from 1962)
markets: US common stocks (NYSE from 1926, AMEX from 1962, NASDAQ from 1972); 36 accounting-based anomalies
tier: A — Tier-1 venue, multi-decade hand-collected sample that is genuinely out-of-sample by construction, explicit about data-quality limits, and the design is a direct test rather than a horserace
validation_overlap: false (sample ends 2015-12, before the lab's 2018–2023 validation window)
published_post_2018: false (RFS 2018; the version read is the 2016 NBER working paper)
---

## Access

**Read in full** from NBER, which served a 74-page parseable PDF on the first request. NBER remains
the folder's most reliable single channel. The published RFS version is closed (Unpaywall reports no
OA location for the DOI); nothing in this note depends on a difference between the two versions, and
where the note quotes a number it is the working paper's.

Index behaviour worth recording: **Semantic Scholar returns `not found` for the RFS DOI** while
Crossref and OpenAlex both resolve it. This is a third failure mode for S2 after the DOI-endpoint
success and the `/paper/search` rate limit — a clean "not found" on a real, indexed, Tier-1 DOI. Do
not conclude from an S2 miss that a paper is unindexed.

## Mechanism

The paper asks a question the anomaly literature mostly cannot: **what does a cross-sectional
predictor look like in the data that existed before anybody went looking for it?**

Nearly all accounting-based anomalies were discovered in post-1963 Compustat data, because that is
when Compustat becomes free of backfill bias. The authors hand-collect accounting data from Moody's
Industrial and Railroad manuals back to 1918 and merge it with CRSP and Compustat, producing a panel
in which each of 36 anomalies can be measured in three distinct eras:

1. **pre-sample** — data that existed before the anomaly was discovered, and that the discovering
   author did not use;
2. **in-sample** — the window the original study actually used;
3. **post-sample** — data accumulating after discovery.

Three competing explanations make different predictions across those eras:

- **Unmodeled risk** — the effect should be present in all three. There is no reason the discovery
  window should stand out.
- **Mispricing** — the effect should be *stronger* going backward in time, because trading costs and
  limits to arbitrage were larger then, and weaker going forward as capital arrives.
- **Data-snooping** — the effect should be strongest in the in-sample window specifically, and
  **symmetric** on either side of it: equally absent before and after.

The finding is the third pattern, and the symmetry is what makes it diagnostic. Average returns,
Sharpe ratios, CAPM and three-factor alphas, and information ratios all fall sharply and significantly
when moving out of the original window **in either direction**. The pre- and post-discovery estimates
are generally within one standard error of each other, while the in-sample period differs from both by
at least four standard errors. Returns "jump up as we enter the in-sample period and then, after this
period ends, fall back to levels that are statistically indistinguishable from those seen during the
pre-sample period."

That symmetry is the whole argument. A backward-looking decline cannot be arbitrage — arbitrageurs
did not trade on a signal nobody had published yet — and it is the wrong sign for the mispricing
story, which predicts *larger* profits in the higher-cost past. Selection on the sample is the only
explanation left standing that predicts a two-sided drop.

**The second mechanism, and for this lab the more important one: selection distorts second moments,
not just first.** An anomaly's t-statistic is higher when its returns are *less volatile*, and
referees routinely require that a candidate predictor not be subsumed by known factors — so a
candidate is more likely to clear review when its correlation with existing anomalies is
**atypically low**. Both volatility and correlation are therefore selected on, and both should revert
out of sample. The authors measure this with a panel regression of each anomaly's return on the
average return of all *other* anomalies, split by whether each is in its in-sample or out-of-sample
era. While an anomaly is in-sample it loads **0.59** on the index of other in-sample anomalies and
only **0.09** on the index of out-of-sample ones; once it moves out of sample those become **0.17**
and **0.54** (t = −9.9 and +11.3). The crucial control: running the same regression **backward**, into
the pre-discovery era — a boundary that holds no significance whatsoever for an arbitrageur — gives
the same pattern (0.62 / 0.06 in-sample, becoming 0.01 / 0.42, t = −13.5 and +8.1).

The symmetry of *that* result is what separates this from McLean–Pontiff's arbitrageur-comovement
story. Capital flowing into a published anomaly can explain higher correlations after publication; it
cannot explain the identical pattern appearing before discovery. **A measured low correlation to
existing strategies is partly a selection artifact and reverts out of sample.**

## Construction recipe

No strategy. Three usable constructions:

- **The three-era test, as a design.** For any predictor with an identifiable discovery window, split
  the available history into pre-sample / in-sample / post-sample and compare. The signature of
  selection is *symmetry* — a drop of similar size on both sides. The signature of arbitrage is
  *asymmetry* — a drop only on the forward side. The signature of risk is *no drop*. This is a
  three-way discriminator from one table, and it needs no new data beyond history on both sides of the
  discovery window.
- **The halving rule.** The authors' own recommendation for what an asset-pricing model should be
  held to: out-of-sample alphas run **40% to 60% of in-sample alphas** depending on the model, so the
  correct standard is explaining *approximately half* of the in-sample alpha; the remainder is the
  spurious part, and "even the correct asset pricing model could not be expected to explain [it]
  away." Three-factor **information ratios** fall by **more than three-fifths** moving out of sample
  in either direction.
- **The correlation-reversion adjustment.** When a candidate's value rests on a *measured* low
  correlation to an incumbent, that correlation is a selected quantity and the selection inflates
  exactly the property being relied on. The regression above is the template for measuring the
  reversion: regress the candidate on an index of in-sample peers and an index of out-of-sample peers,
  and read the interaction.

The authors are explicit about the limit of all this: because selection "affects all facets of return
processes — averages, volatilities, and correlations with other anomalies and factors — it will be
difficult to correct test statistics even approximately." Their preferred remedy is not a correction
factor but genuinely out-of-sample data.

## Robustness evidence (qualitative only)

- The out-of-sample window is out-of-sample **by construction**, not by assumption: the pre-discovery
  data were physically unavailable to the discovering authors, hand-collected from Moody's manuals for
  this study. This is the strongest form of the evidence available in the cross-sectional literature
  and is why the paper is graded Tier A despite testing anomalies this repo cannot trade.
- The paper devotes a section to data quality and gives four separate checks that the pre-1963
  accounting data are comparable to the post-1963 data. The authors also show results are unchanged
  when the first twelve years are dropped, i.e. when the sample is restricted to data after the
  Securities Exchange Act of 1934 — which addresses the obvious objection that early accounting data
  are simply noisier and would mechanically weaken any pre-sample effect.
- Individual anomaly estimates are acknowledged to be noisy; the paper's conclusions rest on
  aggregation across the 36 anomalies, which the authors state plainly as the reason for aggregating.
  At most 16 of the 36 earn significant CAPM or three-factor alphas pre-discovery and 10 post-
  discovery, so the claim is about the *distribution*, not about any single predictor being dead.
- **The headline conclusion is contested, and the contest is live.** See the companion note from this
  session: Chen's p-hacking calibration and Chen–Zimmermann's publication-bias estimator reach a much
  smaller discount from the same literature, and both cite this paper by name as the view they are
  arguing against. That disagreement is recorded as a tension, not adjudicated — read the two notes
  together.
- Scope caveat that matters here: all 36 anomalies are **accounting-based**. The paper says nothing
  directly about price- or volume-based predictors, which is everything this repo can trade. The
  selection mechanism is generic; the measured magnitudes are not transferable.

## Implementability here

No candidate. This is a **discount on the lab's own measurement machinery**, and one of its findings
bears on a rule `program.md` currently states as fact.

**The load-bearing implication: the leaderboard's `rho` is a selected quantity.** `program.md` says a
challenger blends the incumbent with decorrelated family leads and "argue[s] the blend from the
leaderboard's rho — never from hope." `experiments/learnings.md` puts the gain a decorrelated
challenger needs at +0.438 Sharpe, read off that same correlation. This paper's Table-9 result says
the measured decorrelation of a *selected* lead is partly an artifact of having selected it, and that
it reverts. The lab's leads are selected on validation performance, which is not identical to the
academic publication filter — but the lab *does* apply the second half of the filter explicitly: it
prefers leads that are decorrelated from the incumbent, which is exactly the "not subsumed by known
factors" screen the paper identifies as the source of the distortion. **The required-gain table is
therefore optimistic in a direction nobody has priced**, and the error is largest for the leads the
lab likes most.

Two free things follow, both diagnostics on data the lab already has, neither a trial:

1. **Measure the reversion directly.** The lab stores per-trial validation returns. For each family
   lead, compute its correlation to the champion on the *train* split and on the *validation* split
   separately. If a lead's decorrelation is a selection artifact, the train-split correlation should be
   systematically higher than the validation-split one for leads that were chosen partly on being
   decorrelated — and the gap is a direct estimate of how much of the measured `rho` is selection.
   This is a read of two already-scored splits, costs no trial, and either calibrates the required-gain
   table or clears it.
2. **Apply the symmetry discriminator to the lab's own refutations.** Several of this repo's
   strongest negative results rest on a single split. Where a mechanism has been measured on both
   train and validation, check whether a decline is two-sided (selection) or one-sided (something
   real). The lab currently reads a train→validation drop as overfitting without distinguishing the
   two, and the three-era logic says those are different diagnoses.

**On importing the magnitudes — do not.** The 40–60% range and the three-fifths information-ratio
decline are measured on US accounting anomalies with multi-decade in-sample windows and a formal
publication filter. This repo's objects are price- and volume-based, its "discovery window" is a
six-year validation split, and its filter is a deflated-Sharpe gate rather than a referee. The
*mechanism* transfers; the *constants* do not, and `CLAUDE.md`'s standing rule against carrying
constants across contexts applies with full force. What transfers is the shape: **a two-sided drop
indicts the selection, a one-sided drop indicts the world.**

**A caution against over-reading.** The paper does not say cross-sectional predictability is absent —
it says the *discovery-window estimate* of it is inflated by roughly a factor of two, and that
the residual is real enough that the right standard for a model is explaining about half. A session
that reads this note as "anomalies are fake" has read it wrong, and the Chen note from the same
session argues the inflation is far smaller still.

## Related

- `research/notes/2026-10-01-limits-of-p-hacking-publication-bias.md` (this session) — **the direct
  counterweight.** Chen and Chen–Zimmermann estimate the same discount at ~12% rather than 40–60% and
  name this paper as the view they oppose. The two notes are a stated tension; neither is retracted.
- `research/notes/2026-10-01-survival-conditioning-induced-drift.md` (this session) — selection on
  *survival* rather than on *discovery window*; the same operator applied to a different conditioning
  set, and the only one of the three with a closed form.
- `research/notes/2026-08-17-mclean-pontiff-publication-decay.md` — the post-publication decay
  literature this paper extends backward in time. McLean–Pontiff measure only the forward side; the
  backward side is this paper's contribution and is what makes the diagnosis possible.
- `research/notes/2026-09-15-tweedies-formula-empirical-bayes-selection-bias.md` — what a *selected
  maximum* is worth, which is the same statistical problem at the level of a single estimate rather
  than a literature.
- `research/notes/2026-09-09-nonstandard-errors-in-portfolio-sorts.md` and the folder's
  multiple-testing cluster — those ask whether the best of `N` is significant; this one asks what the
  winner's measured *correlation structure* is worth, which none of them covers.
- `experiments/learnings.md` — the +0.438 required-gain figure and the leaderboard `rho` it is read
  off.
