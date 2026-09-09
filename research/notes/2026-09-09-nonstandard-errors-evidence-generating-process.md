---
title: "Nonstandard Errors" (the #fincap multi-analyst study)
authors: Menkveld, Dreber, Holzmeister, Huber, Johannesson, Kirchler, Neusüss, Razen, Weitzel, et al. (164 research teams; several hundred co-authors)
year: 2024 (Journal of Finance); the version read is the 2021 Bank of England staff working paper
venue: Journal of Finance 79(3), 2339–2390 — Tier 1. Text read: Bank of England Staff Working Paper No. 955, December 2021 (Tier 2 as a venue, but it is the same study).
url: https://doi.org/10.1111/jofi.13337 — text read: https://www.bankofengland.co.uk/-/media/boe/files/working-paper/2021/non-standard-errors.pdf
citations: 53 (Semantic Scholar, DOI:10.1111/jofi.13337, checked 2026-09-09)
sample_period: 2002–2018 (the single shared dataset all teams analysed)
markets: EuroStoxx 50 index futures trade records from Deutsche Börse (~720 million trade records), with an agency/principal flag; six hypotheses about trends in market-quality measures
tier: A
validation_overlap: true (the shared sample touches 2018)
published_post_2018: true
---

Read **in full** as the Bank of England staff working paper, which is the openly-hosted version
of the study published in the *Journal of Finance*; `pypdf` extracted it cleanly. The published
version's title drops the hyphen (*Nonstandard Errors*); the working paper is *Non-standard
errors*. Nothing below depends on a difference between the two.

**What is deliberately not carried across.** The six hypotheses the teams tested are statements
about *trends in market-quality measures on a real market over a dated window*. The paper's
findings about that market are exactly the class of thing this folder is forbidden to record,
and none of them appear here — not the direction of any trend, not its size, not which
hypothesis was which. Everything recorded below is a property of the *distribution of
researchers' answers*, which is a property of the evidence-generating process rather than of any
market. This is the same line the 2026-09-08 entry drew for Lo–MacKinlay: a magnitude a model
or an estimator produces is decision-relevant here; a magnitude a market realised is not.

## Mechanism

The paper's contribution is a distinction, and it is the whole idea:

- A **data-generating process (DGP)** draws a sample from a population. The uncertainty this
  creates in an estimate is the **standard error**. Every gate in this repo prices it.
- An **evidence-generating process (EGP)** turns a hypothesis into a number. Two competent
  researchers handed *the same data and the same hypothesis* will not produce the same number,
  because the mapping from hypothesis to statistic requires dozens of defensible, arbitrary
  choices: which measure operationalises the construct, which observations to drop, which
  window, which functional form, which estimator. The dispersion this creates is the
  **non-standard error (NSE)**, defined operationally as *the standard deviation across
  independent researchers of the result they report for the same hypothesis on the same sample*.

The point is that an NSE is not sampling error, is not bias, and is not incompetence. It does
not shrink with more data — the sample is held fixed by construction — and the authors show it
does not shrink much with researcher quality either. It is a second, orthogonal source of
uncertainty that ordinary reporting does not show, because a single study reports one path
through the forking garden and no measure of how wide the garden is.

The economic reason it matters is selection: a researcher free to choose among many defensible
paths, and motivated toward a result, will choose paths that produce it. NSE measures the size
of the room that freedom occupies.

## Construction recipe

The study's own design — a **multi-analyst** protocol — is the direct measurement:

1. Fix one dataset and one set of hypotheses. Here: 164 research teams, six hypotheses, one
   shared trade-record dataset. Each team estimates an average yearly change for a
   **self-proposed measure** of the construct, and reports a point estimate and its standard
   error; the ratio is the implied `t`.
2. The NSE for a hypothesis is the **standard deviation across teams** of the reported estimate.
   Report the same dispersion for the `t`-values, which measures disagreement about *statistical
   strength* rather than about magnitude.
3. Winsorize (they use 2.5%/97.5%) and report both raw and winsorized dispersion, because a
   handful of extreme paths otherwise dominates the SD.
4. Optionally run a **peer-feedback loop**: teams' reports are graded and commented on by other
   participants, teams revise, and NSE is recomputed at each stage. The change across stages
   measures how much of the dispersion is remediable by ordinary review.
5. Optionally elicit, before revealing results, each team's **belief** about how dispersed the
   other teams' answers will be. Comparing belief to realised dispersion measures whether
   practitioners know how big their own NSE is.

The single-researcher analogue — which is what a one-agent lab can actually run — is to replace
"teams" with "defensible variants of my own construction", enumerate them, and take the same
standard deviation. That is the specification-curve construction; see
`2026-09-09-specification-curve-analysis.md`.

## Robustness evidence (qualitative only)

- **NSE is on par with SE.** Across the six hypotheses, the dispersion across teams is of the
  same order as the sampling error each team reports for its own estimate. Doubling the
  uncertainty is the right first-order summary.
- **Dispersion is not a quality artifact.** NSE size co-varies only weakly with team merit,
  with reproducibility of the team's own code, or with peer ratings of the write-up. A one
  standard-deviation increase in *workflow quality* reduces NSE by about 12%; a one SD increase
  in *team quality* by about 8%, and the latter is only suggestive at the paper's own
  (deliberately conservative) significance levels. Trimming poor-quality teams does not remove
  the dispersion.
- **Disagreement extends to the sign of the verdict, not just the magnitude.** On the most
  abstract of the six hypotheses, 23.8% of teams reported a significant effect in one direction,
  8.5% a significant effect in the *opposite* direction, and 67.7% no significant effect at all,
  evaluating their own `t`-values at a conventional 5% level — same data, same hypothesis. The
  paper reports a similar pattern for the other five. The more abstract the construct, the wider
  the garden: a hypothesis about a directly countable quantity produced far less dispersion than
  one about a latent notion requiring a proxy.
- **Peer feedback helps, and the size of the help depends on what you do with outliers.** The
  cumulative reduction in NSE across four feedback stages is 8.5% on the raw sample and 53.5% on
  the winsorized sample — the gap is driven by extreme-result teams not moving. Review compacts
  the middle of the distribution and leaves the tails where they are.
- **Practitioners underestimate NSE.** In an incentivized belief survey, the average team's
  forecast of the across-team dispersion fell short of the realised dispersion by between 9.0%
  and 99.5% depending on the hypothesis, and the underestimation survives winsorizing, so it is
  not just a failure to foresee outliers.
- **Replication status.** The study is itself a replication design — 164 independent
  reproductions of the same analysis — which is an unusually strong form of the evidence this
  rubric asks for, in one market and one asset class. Its *finding* has been reproduced in a
  different domain by the portfolio-sort studies in
  `2026-09-09-nonstandard-errors-in-portfolio-sorts.md`, which get the same qualitative answer
  (NSE ≥ SE) from a mechanical enumeration of choices rather than from human teams.

## Implementability here

This is not a strategy. It is a statement about how this lab should read its own numbers, and
it converts into one free, train-only diagnostic.

**The claim, translated.** Every candidate in `strategies/candidates/` is one path through a
garden: a score, plus a pool the ranks are computed over, plus a core count, a band count, a
tranche count, a lookback, a skip, a minimum-history filter, a weighting scheme and a cap. The
protocol prices the sampling error in the resulting Sharpe — that is what `sharpe_diff_se` and
the deflator are for. It prices *nothing* about the dispersion that the other defensible
settings of those same knobs would have produced. Menkveld et al.'s finding is that in the one
setting where this has been measured against human researchers, that second dispersion is about
as large as the first.

**The free diagnostic, and both answers are findings.** Take the *seated champion*, unchanged
in signal, and enumerate the defensible variants of its construction at the nodes the lab
already varies — the ones its own journal shows it moving: core count, band count, tranche
count `K`, lookback, skip, min-history, weighting. Score each variant on **train only**. Two
numbers come out:

- the **standard deviation of train Sharpe across the variants** — the champion's own NSE; and
- the lab's recorded **promotion margins**, the validation Sharpe gaps on which seven promotions
  and nine blend declines have actually turned.

If the NSE is small relative to those margins, the lab's rankings are about signals and this
note is a closure. If it is comparable, then a share of the repo's recorded history is a ranking
of construction paths rather than of ideas, and the honest response is a written house
convention (below) rather than another candidate. Note what this diagnostic is *not*: it adds no
haircut, no correction, and no adjustment to any `t`. It is a dispersion measured on train, on
the same footing as the lab's free IC, monotonicity and depth-profile screens. That is why it is
takeable despite sitting one step from `SUMMARY.md`'s standing inference embargo.

**A precondition that must be honoured, or the diagnostic is a lie.** Every variant scored is a
*measurement*, not a trial, and must run in the session scratchpad on the train split — the same
status the lab gives its IC screens and depth profiles. Running the variants through
`run_experiment.py` would put dozens of trials in `trials.jsonl`, raise the deflated-Sharpe bar
for everything after, and read validation. Do not do that. If the variants cannot be scored
free, the diagnostic is not available.

**The remedy the literature actually supports.** The companion note's sorts study finds that
*fixing* a small number of conservative construction choices and holding them across all
candidates removes most of the dispersion. The analogue here is a short, written, frozen house
construction — which pool ranks are computed over, equal versus magnitude weighting, the
min-history filter, whether region-demeaning is applied — so that two candidates differ in
*signal* and not in *construction*. The lab has arrived at most of this by convention through
`strategies/lib/` reuse; it has never written it down, and an unwritten convention is exactly the
thing an agent silently varies.

**One analogue that does not transfer, and should not be forced.** Peer feedback is the paper's
one working remedy for dispersion, and a single-agent nightly lab has no peers. The nearest
things it has are `experiments/learnings.md`, this folder, and the human who reviews frozen-file
edits. That is worth one sentence of awareness and no machinery: do not build a "self-review
stage" on the strength of a result measured on human teams.

**Known pitfall — the reassuring reading is also available and is probably wrong.** "NSE is on
par with SE" is sometimes read as "so the effect is still there, just noisier". The paper's
sign-disagreement result blocks that reading at the level of an individual verdict: on the same
data and the same hypothesis, a fifth of teams found significance one way and a twelfth found it
the other way. What survives dispersion is a question about the *pooled* answer, and that is the
subject of the sorts note (where the sign turns out to be stable and the magnitude not) rather
than of this one.

## Related

- `2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the same measurement carried out
  mechanically on factor construction, with the decision-node list this lab can actually copy.
- `2026-09-09-specification-curve-analysis.md` — the single-researcher method for enumerating
  and displaying the garden, and the one part of it this folder does *not* import.
- `2026-08-17-rebalance-timing-luck-tranching.md` — rebalance timing luck is one coordinate of a
  specification curve, measured in isolation years before the NSE framing existed. The lab
  already acts on it (the champion buys breadth from tranches); this note says that coordinate
  was never the only one.
- `2026-08-24-deflated-sharpe-ratio.md`, `2026-08-24-multiple-testing-haircut.md` — the
  neighbouring literature the folder has embargoed. NSE is *not* that: it prices dispersion
  across paths rather than adjusting a threshold for how many paths were walked, and it yields a
  measurement rather than a haircut.
