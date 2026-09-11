---
title: "On the Robustness of Size and Book-to-Market in Cross-Sectional Regressions" — recorded for one fact: a headline cross-sectional premium can be entirely an artifact of the observations an outlier rule would remove
authors: Knez, Ready
year: 1997
venue: The Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.1997.tb01113.x
citations: 287 (OpenAlex, checked 2026-09-11); 274 (Semantic Scholar, same date); 131 (Crossref `is-referenced-by-count`, same date). **Two-DOI registration — see the access note below**: the same article is also registered as `10.2307/2329439` (JSTOR), under which OpenAlex reports 69, Crossref 35, and Semantic Scholar returns *not found*. Any single lookup against the JSTOR DOI understates the article by roughly 4×.
sample_period: not established — the paper was not read. It re-examines Fama–French (1992), whose sample is 1963–1990, and was published in 1997, so the sample necessarily ends more than two decades before this lab's validation window.
markets: US (CRSP/Compustat cross-section, following the Fama–French 1992 design)
tier: A
validation_overlap: false
published_post_2018: false
read: **NOT READ — the published abstract only**, retrieved verbatim from OpenAlex's `abstract_inverted_index` for DOI `10.1111/j.1540-6261.1997.tb01113.x`. The article is closed: Unpaywall reports `is_oa: false` with **zero** OA locations, OpenAlex reports `oa_status: closed` and `any_repository_has_fulltext: false`, and the only two locations it holds are the Wiley DOI and a JSTOR SICI link. No preprint, working-paper or repository copy was found. **Everything below that is attributed to the paper comes from those four abstract sentences and nothing else**; the construction details, the robust estimator's specification and the economic argument were not read and are not reported here.
---

## Mechanism

This note exists to put a number on the stake of its companion,
`notes/2026-09-11-influential-observations-winsorization-versus-robust-regression.md`. That note
establishes *which* outlier treatment is least biased. This one records what the choice is worth:
the answer, in the most-studied cross-sectional premium in the literature, is **the entire effect**.

The paper's two findings, as its abstract states them:

1. Applying a **robust regression estimator** to the Fama–French (1992) cross-sectional regressions,
   **the risk premium on size completely disappears when the 1 percent most extreme observations are
   trimmed each month.**
2. The negative average of the monthly size coefficients reported by Fama and French **can be
   entirely explained by the 16 months with the most extreme coefficients.** For a monthly sample
   spanning several decades — a few hundred cross-sections — that is a low-single-digit percentage
   of the periods carrying all of the result.

The authors do not read this as debunking the size effect. Their stated position is the opposite and
it is the more interesting one: that investigating *why* the effect is concentrated in a handful of
observations and periods could reveal the economic forces underlying it, and may yield insight into
how firms grow. The extreme observations are treated as where the economics is, not as noise to be
cleaned away — which is the same posture the Leone et al. note records from the statistics side, and
the reason neither note recommends trimming as a default.

**The general mechanism, stated at the level this folder records:** in a cross-sectional regression
or sort, the estimate is a weighted combination of observations in which the extreme ones carry
disproportionate weight. Two consequences follow, and both are structural rather than sample-specific:

- **Concentration in observations.** A premium can be produced by a fraction of a percent of the
  name-months. Removing them is not hygiene; it is a substantive change to what is being estimated.
- **Concentration in periods.** Even with every observation retained, the average of a series of
  period-by-period coefficients can be delivered by a handful of periods. A mean coefficient — and,
  by the same algebra, a mean IC — is not evidence of a pervasive effect until the concentration of
  the series that produced it has been looked at.

## Construction recipe

**Not available — the paper was not read.** What the abstract names, and nothing more:

- The estimator is a **robust regression** applied to the standard Fama–MacBeth-style cross-sectional
  regression of returns on size and book-to-market. The specific robust estimator, its tuning and its
  breakdown point are not established here. (Robust regression in this period is typically an
  M-, S- or LTS-estimator; MM-estimation, the variant the Leone et al. note recommends, postdates
  Yohai 1987 and would have been available, but **which one this paper uses is not known to this
  note** and must not be guessed.)
- The trimming rule is **1% of the most extreme observations, re-applied each month** — i.e. a
  per-cross-section rule, not a pooled one. This is the one construction detail the abstract
  actually fixes, and it is the one that matters most for transferring the idea.
- The period-concentration finding is computed on the **series of monthly coefficients**, i.e. a
  second-stage diagnostic on the Fama–MacBeth time series rather than on the cross-section.

Anyone who needs the estimator's specification must obtain the article; this note deliberately
leaves the blank visible rather than filling it from memory.

## Robustness evidence (qualitative only)

- Published in a top-tier journal, targeting the single most-replicated result in the
  cross-sectional literature, and still cited at a rate in the high hundreds nearly three decades on.
- **The finding is corroborated in direction by the subsequent methodological literature**, which is
  the honest form of support available for a note built on an abstract:
  `notes/2026-09-11-influential-observations-winsorization-versus-robust-regression.md` records
  simulation and replication evidence that outlier treatment changes coefficients and inferences, and
  that the direction of the change depends on which side is treated. Knez–Ready is the finance
  instance of the general claim, not an isolated result.
- **It sits alongside, not against, this folder's standing size-effect discounts.** The size premium
  is already discounted here on independent grounds — `notes/2026-09-02-anomalies-by-size-group.md`
  and `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` both find
  characteristic predictability concentrated outside the large-cap range this universe occupies, and
  `notes/2026-08-17-mclean-pontiff-publication-decay.md` supplies the post-publication decay. This
  note adds a *third*, mechanically distinct discount: even within the original sample, the premium
  was carried by the observations an outlier rule would delete.
- **Limits that must be stated.** Single market, single sample, and — decisively for how much weight
  to put on it — **the paper itself was not read**. Its tier reflects its venue and citation record;
  the *evidentiary* weight this folder should place on it is bounded by the four sentences that were
  read. No claim here should be built on it alone.

## Implementability here

There is nothing to build. There is one diagnostic, and it is free.

1. **The period-concentration check, run on the lab's own scores.** The lab grades candidate scores
   by IC and by top-band excess return, and both are means of a period-by-period series. The
   translation of finding (2) is exact and needs no market data beyond what a train-split diagnostic
   already touches: **for each score, sort the per-period contributions and ask how many periods
   deliver the whole mean.** If a family lead's IC comes from a handful of months, the lab has a
   concentration finding about that lead, and it has it for free — no `run_experiment.py`, no trial,
   no holdout. This composes directly with the monotonicity work of 2026-09-06 and with `#92`'s
   specification curve, and it is the kind of check that can *fail*, which is what this folder has
   said repeatedly it should be producing.
2. **The 1%-per-cross-section rule does not survive the move to this universe, and the reason is the
   one tonight's companion note already gives.** One percent of 140 names is **one name**. A rule
   that removes a stable, meaningful tail from a cross-section of thousands removes a coin-flip from
   this one. Any concentration check here must be specified in **names and periods**, never in
   percent, and the lab should expect the check to be noisier than the literature's version by
   roughly the ratio of the cross-section sizes.
3. **It sharpens a caution about the champion specifically.** Under z-score-magnitude weighting the
   most extreme names are the largest positions, so observation-concentration and
   position-concentration are the same thing. The lab already tracks HHI and breadth per book. The
   missing statistic is the *return* analogue: not how concentrated the weights are, but how
   concentrated the realized edge is across periods.

**Pitfalls.**

- **Do not read this as "the size effect is fake".** The authors explicitly do not, and the abstract
  says so. The transferable claim is about concentration and about the leverage of the outlier rule,
  not about the existence of a premium.
- **Do not import the numbers as thresholds.** "1%" and "16 months" are properties of one sample and
  one design. They establish that concentration of this magnitude is possible in a headline result;
  they calibrate nothing here. `CLAUDE.md`'s rule against carrying constants across families applies
  with extra force to a constant carried from a paper that was not read.
- **Do not cite this note as evidence for a construction choice.** It is abstract-only. Where a
  decision needs support, the support is the Leone et al. note, which was read in full.

## Related

- `notes/2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the
  methodology behind this result, read in full; the primary of the pair.
- `notes/2026-09-11-parametric-portfolio-policies-standardized-characteristics.md` — the third of
  tonight's notes; the construction in which extreme standardized scores become extreme weights.
- `notes/2026-09-02-anomalies-by-size-group.md` and
  `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` — the two standing
  size/large-cap discounts this note adds a third, independent mechanism to.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the fourth discount, and the reason none of
  them should be read as surprising.
- `notes/2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — the other "is the headline statistic
  hiding its own structure" diagnostic in this folder; the period-concentration check proposed above
  is its time-series counterpart.
