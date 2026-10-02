---
title: "Replicating Anomalies"
authors: Hou, Xue, Zhang
year: 2020
venue: Review of Financial Studies 33(5), 2019–2133 (Tier 1). Read from the author-hosted typeset version of record.
url: https://doi.org/10.1093/rfs/hhy131 · full text read from https://theinvestmentcapm.com/uploads/1/2/2/6/122679606/houxuezhang2020rfs.pdf
citations: 1,037 (Crossref is-referenced-by-count, checked 2026-10-02); 847 (Semantic Scholar DOI endpoint, checked 2026-10-02). OpenAlex not consulted — its free daily budget was already exhausted at session start (HTTP 429, `Insufficient budget`).
sample_period: 1967-01 to 2016-12 (plus per-anomaly re-runs truncated to each original study's own window, the earliest of which start at 1967-01)
markets: US common stocks, NYSE + Amex + NASDAQ, financials and negative-book-equity firms excluded; 452 published anomaly variables in six categories
tier: A — Tier-1 venue, four-figure citations, a direct large-scale replication rather than a horserace, explicit about multiple testing, and the authors publish their variable definitions in full (Appendix A) so the construction is auditable
validation_overlap: false (sample ends 2016-12, before the lab's 2018–2023 validation window)
published_post_2018: true (RFS 2020; advance access December 2018)
---

## Access

**Read in full** (abstract, Sections 1–2, Section 3.1, the conclusion, and Appendix B) from
**`theinvestmentcapm.com`**, Lu Zhang's own site, which serves the typeset version of record at
`/uploads/1/2/2/6/122679606/houxuezhang2020rfs.pdf` — a 115-page PDF that `pypdf` parsed cleanly.
The guessable path `theinvestmentcapm.com/HouXueZhang2020RFS.pdf` 404s; the file list on
`/research.html` is the way in. This is the 2026-09-18 faculty-page lesson holding for a
**project site** rather than a university tree: a prolific author's own research page is the first
place to look for a closed Tier-1 article.

## Mechanism

This is not a note about an anomaly. It is a note about **how much of a measured cross-sectional
result is the measurement**, and it is the pessimistic half of the pair whose optimistic half this
folder already holds (Jensen–Kelly–Pedersen,
`2026-08-25-hierarchical-bayesian-factor-replication.md`).

The authors assemble 452 published anomaly variables — 57 momentum, 69 value-versus-growth, 38
investment, 79 profitability, 103 intangibles, 106 trading frictions — re-implement each from its
original study's own variable definition, and run every one through a common grid of procedures. The
whole result turns on **two construction choices that most original studies made differently**:

1. **Where the decile breakpoints fall.** Breakpoints computed on the NYSE-only cross-section
   (NYSE) versus on the pooled NYSE-Amex-NASDAQ cross-section (All).
2. **How the members of a decile are weighted.** Value-weighted (VW) versus equal-weighted (EW).

Their headline: with **NYSE breakpoints and value weights**, 65% of the 452 anomalies cannot clear
`|t| ≥ 1.96` on the high-minus-low decile return — i.e. the replication rate is 35%. Switch to
pooled breakpoints and equal weights, which is what many original papers did, and the failure rate
falls to 41.4%.

**The mechanism connecting the two is one sentence: the extreme buckets of an uncontrolled sort fill
up with the noisiest members of the pool.** The authors spell out why, citing Fama–French (2008):

- Microcaps (below the 20th percentile of NYSE market equity) are **~3% of aggregate market
  capitalization but ~60% of the number of stocks**.
- Microcaps have the **highest cross-sectional dispersion** both of returns and of most anomaly
  variables.
- Consequently, with pooled breakpoints, **microcaps can be more than 60% of the names in an extreme
  decile**. NYSE breakpoints, by contrast, "assign a fair number of small and big stocks into extreme
  deciles."
- Equal weighting then gives those names full voice in the decile return, and OLS Fama-MacBeth
  regressions do the same thing in regression form, because OLS weights by count.

So the two choices compound: pooled breakpoints decide *who reaches the tail*, and equal weighting
decides *how loudly the tail speaks*. Neither is technically wrong; the authors' claim is that the
results they produce "can be very fragile, if not misleading."

**Three further findings that matter more than the headline:**

- **The casualty is concentrated, not spread.** In the trading-frictions category — liquidity, market
  microstructure, volume, volatility — **102 of 106 variables (96%) fail** at `|t| ≥ 1.96` with
  NYSE-VW. Momentum (63.2%) and investment (73.7%) replicate acceptably; value-versus-growth (42%)
  and profitability (44.3%) moderately; intangibles (25.2%) and trading frictions poorly. The
  authors' own reading: "economic fundamentals are more important than trading frictions in driving
  the cross section of expected returns."
- **Equal-weighting revives some of that category and not others.** With pooled breakpoints and equal
  weights, short-term reversal, share turnover, dollar-trading-volume variation, absolute
  return-to-volume (Amihud) and the count of zero-volume days come back; the probability of informed
  trading, the Pastor–Stambaugh liquidity beta, the Acharya–Pedersen liquidity betas, idiosyncratic
  volatility, the high-low bid-ask spread and intermediary-leverage beta **do not**. Even at maximum
  microcap weight, 60.4% of the trading-frictions category still fails.
- **It is not sample extension.** Re-running each anomaly truncated to its own original study's
  window gives a 34.7% replication rate against 35% in the extended sample; 31 anomalies lose
  significance when the sample is extended and 32 gain it. Whatever is wrong is in the construction,
  not in the extra years.

**Multiple testing.** Beyond `|t| ≥ 1.96` the authors apply Harvey–Liu–Zhu's cutoffs of **2.78 and
3.39**, derived from the Benjamini–Hochberg–Yekutieli false-discovery-rate adjustment at the 5% and
1% levels. At 2.78 the NYSE-VW replication rate falls to 17.9% (13.3% for FM-WLS), and the failure
rate is 52% even under maximum-microcap-weight sorts. The authors state in a footnote that these
cutoffs "are only heuristic in nature" — worth carrying, because this folder's multiple-testing notes
treat such thresholds more firmly than their own authors do.

## Construction recipe

What is implementable from this paper is a **set of measurement conventions**, not a signal.

- **Deciles, monthly or annual.** Annual sorts at the end of June of year `t` on a variable from the
  fiscal year ending in calendar `t−1`, held July `t` → June `t+1`. Monthly sorts on the latest known
  value, with a 4-month lag for quarterly accounting items other than earnings.
- **The four-cell procedure grid.** Report NYSE-VW, NYSE-EW, All-VW and All-EW, plus FM-OLS and
  FM-WLS. The grid *is* the robustness check: an effect that lives in only one cell is a statement
  about that cell's weighting, not about the cross-section.
- **Breakpoint pool ≠ return pool.** Breakpoints and return weights are independent knobs, and the
  paper also reports all-but-micro and micro-only variants in which the breakpoint sample and the
  return sample are both restricted. Forming buckets on one pool and weighting on another is a
  legitimate and separately-reportable choice.
- **Fama-MacBeth hygiene.** Winsorize each regressor cross-sectionally at 1%–99% every month, then
  standardize it (subtract the cross-sectional mean, divide by the cross-sectional SD) so a slope
  reads as the return change per one cross-sectional SD. Newey-West the `t`-values. Footnote 8 gives
  the explicit algebra showing the FM slope is the return of a zero-investment portfolio with unit
  characteristic spread, and that WLS by market equity simply replaces `(X'X)⁻¹X'` with
  `(X'MX)⁻¹X'M` for a diagonal value-weight matrix `M`.
- **Multi-month holding periods by overlapping sub-portfolios.** For a `k`-month holding period,
  average the `k` sub-deciles formed at `t−s`, `s = 0…k−1`, exactly as Jegadeesh-Titman do, and take
  the same average over sub-regression slopes on the regression side.
- **Delisting adjustment** — Appendix B, written up separately in
  `2026-10-02-delisting-returns-the-other-half-of-survivorship.md`.

## Robustness evidence (qualitative only)

The paper *is* a robustness exercise, so the relevant question is whether its own finding is robust.
In its favour: 452 variables re-implemented from original definitions; a five-decade sample; results
reported across six procedures rather than one; the original-window re-run that removes "you just
added years" as an explanation; and a published variable appendix. Against it, and the authors say so:
the multiple-testing cutoffs are heuristic; the microcap controls are advocated rather than derived;
and the whole exercise is US-only, so nothing here is evidence about non-US cross-sections.

**The standing tension to carry, not resolve.** Jensen–Kelly–Pedersen (2023, JF,
`2026-08-25-hierarchical-bayesian-factor-replication.md`) study much the same literature with a
hierarchical Bayesian model and conclude that most factors *do* replicate, and replicate globally.
These two Tier-A papers disagree, and they disagree about method rather than about data: HXZ's unit of
analysis is a single anomaly tested alone against a fixed `|t|` bar, JKP's is an anomaly shrunk
toward its cluster's mean under a prior. This is the same shape as the 40–60% versus ~12% discovery-
window disagreement recorded on [2026-10-01]: **both sides agree on the sign and shape — a measured
in-sample cross-sectional edge is an overestimate, by more for noisier candidates — and disagree on
the magnitude.** Carry both; adopt neither constant.

## Implementability here

This repo is *not* the sample HXZ are warning about, and getting that right is the whole of this
section.

**What does not transfer.** The lab's universe is ~145 large global stocks and ETFs. It contains **no
microcaps at all**. So the specific channel HXZ identify — extreme deciles stuffed with 3%-of-cap
names — cannot be the lab's inflation mechanism, and the paper's prescription (NYSE breakpoints,
value weights) is not a defect list for this repo. In particular this is exactly the situation
`CLAUDE.md` warns about: **do not import HXZ's constants by analogy.** "Equal weighting is
dangerous" is, in HXZ's hands, shorthand for "equal weighting overweights microcaps"; in a universe
with no microcaps that argument does not apply, and the lab's equal-weighted book is not condemned by
this paper.

**What does transfer, and it is the more useful half.** The *abstract* mechanism — an uncontrolled
cross-sectional sort reaches its extreme buckets disproportionately for the pool's
highest-dispersion members, and the measured spread is then mostly a statement about those members —
is universe-independent. The lab has already measured its own instance of it: `learnings.md` records
that a raw sort "reaches the extreme buckets more often for high-vol names," and that on this
universe "the level *is* the survivorship artifact." **Same symptom, different selecting variable:**
HXZ's pool selects on size, this repo's on survival. The transferable discipline is the one HXZ
apply, and it is free here — *report the spread under at least two weighting schemes and two bucket
counts, and treat an effect that lives in only one cell as a statement about that cell*. The folder
already holds the pieces (`2026-09-06-number-of-portfolios-as-tuning-parameter.md`,
`2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md`); HXZ is the evidence that the
check is load-bearing rather than cosmetic.

**The uncomfortable cross-reference, and it costs nothing to make.** Of HXZ's 106 trading-frictions
variables, 96% fail at `|t| ≥ 1.96` with NYSE-VW; the named failures include Amihud's
return-to-volume, idiosyncratic and total volatility, the Bali-Cakici-Whitelaw maximum daily return,
the Corwin-Schultz high-low spread, Datar-Naik-Radcliffe turnover, Liu's zero-volume-day count,
Jegadeesh short-term reversal, and both the Pastor-Stambaugh and Acharya-Pedersen liquidity betas.
**This folder has a note on every one of those**, and the lab has independently closed several of
them on its own data: ILLIQ's mean channel [2026-09-24], liquidity risk as a documented negative
[2026-09-29], dispersion as the survivorship artifact in another costume, short-term residual
reversal [2026-09-25]. That is not a coincidence to be impressed by — it is the literature and the
lab arriving at the same place from different directions, and it should **lower the prior on any
further `liquidity-volume` or `range-variance` candidate** that is a bare characteristic sort. The
families are not closed; the bare-sort shape inside them is the thing with a bad record on both
sides of the fence.

**One free observation about the lab's own bar.** HXZ's single-test bar is `|t| ≥ 1.96` and their
multiple-testing bar is 2.78. `program.md` records that **no promotion in this repo's history has
ever cleared `|t| = 2` on validation.** Those two facts sit next to each other without any new
measurement: on HXZ's accounting, the entire champion sequence would be a sequence of replication
failures. This is not an argument to change the gate — the gate is deflated-Sharpe-based and the
holdout veto was added for exactly this reason — but it is the honest frame for how much any single
promotion here is worth, and it is worth one line in a weekly report.

**Pitfalls.**
- Do not read "value-weight instead of equal-weight" as advice for this repo. This universe's
  value weights would concentrate the book in a handful of mega-caps and run straight into the 25%
  position cap; the `FLOOR`-based weighting the lab already uses is a different animal.
- Do not read the per-category replication rates as a ranking of families to try. They are rates over
  *published US anomalies in that category*, not over the mechanism space, and the categories do not
  map onto `program.md`'s families.
- The 2.78 cutoff is not interchangeable with this lab's deflated-Sharpe threshold. They control
  different things (FDR over a literature versus the selection bias in one maximum over this repo's
  own trial history), and HXZ's own footnote calls theirs heuristic.

## Related

- `2026-08-25-hierarchical-bayesian-factor-replication.md` — Jensen-Kelly-Pedersen, the opposing
  Tier-A verdict on the same literature. Read the two together or neither.
- `2026-10-01-discovery-sample-and-anomaly-decay.md` and `2026-10-01-limits-of-p-hacking-publication-bias.md`
  — the discovery-window and publication-bias halves of the same problem.
- `2026-10-02-delisting-returns-the-other-half-of-survivorship.md` — this paper's Appendix B is the
  construction primary for that note.
- `2026-09-06-number-of-portfolios-as-tuning-parameter.md`, `2026-09-11-trimming-and-the-size-premium.md`,
  `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the folder's
  existing notes on bucket count, trimming and influence, all of which HXZ's grid is an instance of.
- `2026-08-29-amihud-illiquidity-measure-and-replication.md`, `2026-09-04-high-low-spread-estimator.md`,
  `2026-09-01-max-lottery-extreme-positive-returns.md`, `2026-09-29-liquidity-risk-priced-innovations.md`
  — four of the named trading-frictions failures.
- `experiments/learnings.md` — "the level *is* the survivorship artifact", and the raw-sort/extreme-
  bucket observation that is this paper's mechanism with a different selecting variable.
