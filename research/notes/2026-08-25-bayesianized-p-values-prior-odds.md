---
title: "Presidential Address: The Scientific Outlook in Financial Economics"
authors: Harvey
year: 2017
venue: Journal of Finance (tier 1)
url: https://doi.org/10.1111/jofi.12530
citations: 450 (Crossref, checked 2026-08-25; Semantic Scholar's DOI endpoint does not resolve this DOI — a third instance of the folder's "JF DOIs go missing in S2" pattern)
sample_period: none for the argument — methodological. The supporting meta-analysis of published factor t-statistics (from Harvey–Liu–Zhu) covers 1963–2012; the ticker-symbol demonstration uses CRSP from 1926
markets: US equities in the illustrations; the argument is field-wide
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The finance-venue half of the answer to `SUMMARY.md`'s open question 11(c). Where the statistics
literature gives a frequentist procedure that preserves error control under a-priori weights, this
gives the **closed-form map from a prior to a required threshold** — and, importantly for a lab
inclined to like the idea, finds that under any realistic prior in this field the threshold goes
*up*, not down.

**The complaint.** A p-value answers "what is the probability of data this extreme *if* the null is
true?" A researcher wants "what is the probability the null is true?" These are different questions
and the second cannot be answered without a prior. Harvey's framing: if you accept that the false
positive rate should be higher for theories that are implausible, you have already adopted Bayesian
reasoning, whether or not you compute anything.

**The construction.** By Bayes' theorem, posterior odds = prior odds × Bayes factor, where the Bayes
factor is the ratio of the data likelihood under the null to the data likelihood under the
alternative. The Bayes factor generally depends on how the alternative is specified, which is what
makes practitioners uncomfortable. The **minimum Bayes factor (MBF)** removes that dependence by
taking the lower bound over all specifications of the alternative — attained when the entire prior
mass on the alternative sits at the maximum-likelihood estimate, i.e. when what you believed
beforehand happens to coincide exactly with what the data show. **The MBF is therefore the most
favourable reading the evidence can ever receive**, over every possible prior on the alternative. Two
computable forms:

```
MBF     = exp(−Z²/2)                     Z the normal test statistic
SD-MBF  = −e · p · ln(p)                 for priors symmetric and descending about the null
Bayesianized p-value = (MBF × prior odds) / (1 + MBF × prior odds)
```

where prior odds are null:alternative. The SD-MBF is always larger than the MBF (weaker evidence
against the null), which is the right default when you have no directional conviction — "does this
signal predict returns positively or negatively" is exactly that case.

**The economics of the base rate.** The second strand of the argument concerns why the prior in this
field should be a long shot. Harvey lists three structural reasons the ex-ante probability of a true
new anomaly should *decline over time*: true effects become scarcer as the low-hanging fruit is
picked; as first-principles theories run out, research leans on increasingly specialised ones with
lower true-discovery rates; and the number of securities is finite relative to the number of
characteristics one can construct from them. Under a declining base rate, **the same t-statistic is
worth less later than earlier** — a mechanism-level statement, not a dated one, and it applies to any
search that has already explored a lot of a family.

**The demonstration that grounds it.** He had a research assistant form long-short portfolios on the
first three letters of ticker symbols, crossed with two sample-start choices, equal versus value
weighting, and two rebalance frequencies — roughly 25,000 portfolio choices — and report the best
t-statistic. It was 3.23, above the threshold his own prior work recommends, with near-zero beta to
known factors. The point is not that the strategy is silly; it is that **the relevant count is the
choice space, not the number of results reported**, and that a threshold alone cannot distinguish
the two. He extends this with Gelman–Loken's argument that even unexercised choices (three ways to
handle delistings, one chosen ex ante) belong in the count.

**The unintended consequence, stated against his own prior recommendation.** Raising the significance
threshold may *increase* data mining and publication bias rather than reduce it, because a higher bar
raises the return to searching harder. He is explicit that "make a decision based on t > 3" is not
sufficient. That is a caution any lab with an automatically-rising bar should carry.

## Construction recipe

**Reading a result.** Take the test statistic `Z`, form `MBF = exp(−Z²/2)` (or `SD-MBF = −e·p·ln(p)`
if the prior on the alternative is symmetric and descending about the null), state the prior odds
explicitly, and report the Bayesianized p-value alongside the frequentist one. Harvey's worked case:
a t of 2.6 (p = 0.014) gives MBF = 0.034; at even odds the posterior probability of the null is
0.033, but at modest 2:1 odds against the effect it is 0.064 — a doubling from a change of prior that
nobody would call aggressive.

**Setting a threshold.** Invert it: fix the posterior probability of the null you are willing to
tolerate and the prior odds, and solve for the required statistic. For the MBF,
`S = sqrt(−2 · ln( BPV / ((1 − BPV) · PO) ))`, with `BPV` the target Bayesianized p-value and `PO` the
prior odds; for the SD-MBF, solve `p·ln(p) = −e⁻¹·BPV/((1−BPV)·PO)` numerically and convert. The
resulting grid is the paper's Table III, and its shape is the fact to carry:

| target P(null true) | even odds (1:1) | 4:1 against | 19:1 against | 99:1 against |
|---|---|---|---|---|
| 0.10 (MBF) | 2.10 | 2.68 | 3.21 | 3.69 |
| 0.05 (MBF) | 2.43 | 2.94 | 3.43 | 3.88 |
| 0.05 (SD-MBF) | 2.93 | 3.41 | 3.86 | 4.29 |
| 0.01 (SD-MBF) | 3.49 | 3.89 | 4.29 | 4.67 |

**The single most important line in that table for a lab tempted by prior-based discounts:** even at
**even odds** — the most generous prior anyone could claim for a new idea — and even under the MBF,
which is the most favourable Bayes factor that exists, the threshold for a 5% posterior probability
of the null is **2.43**, above the conventional 2.0. Under the more honest SD-MBF it is 2.93. A prior
never buys a bar *below* the naive frequentist one; it only relocates the bar relative to a long-shot
default. That is the boundary condition the folder's open question needed and did not have.

## Robustness evidence (qualitative only)

The MBF is not Harvey's result — it is Edwards–Lindman–Savage (1963), with the SD-MBF from
Bayarri–Berger (1998) and the class of alternative-prior minimum Bayes factors from Berger–Sellke
(1987); Harvey's contribution is the transposition into finance plus the tables. The algebra cannot
decay. The supporting empirical claims are of two kinds. The publication-bias evidence is a
meta-analysis of reported t-statistics across published factor studies over five decades, whose
diagnostic is distributional and shape-based (roughly as many studies reporting t in 2.00–2.57 as in
2.57–3.14, with very few below 2.00 published at all) — a pattern that is hard to generate without
selection. The base-rate argument is reasoned rather than measured, and the author says so. The
address is heavily cited, in the field's top venue, by an author with a long track record on exactly
this question, and it is unusual in arguing *against* the interpretive convenience of the author's own
prior recommendation.

Two limits worth recording. First, the MBF's optimism is structural: it assumes the alternative was
specified, before the fact, at precisely the value the data ended up favouring. Nobody's prior is
that good, so every Bayesianized p-value computed this way is a **lower bound on the probability the
null is true**, i.e. the most flattering number available. Second, the framework is single-hypothesis
Bayesian updating; it is complementary to, not a substitute for, an explicit multiple-testing count,
and Harvey is explicit that the two problems compound.

## Implementability here

**Explanatory only.** `engine/protocol.py` and the deflated-Sharpe criterion are frozen and their
interpretation is a human decision. Nothing below is a recommendation to rescore anything, and
session 11's item (d) — recomputing the repo's own gate statistic under a different framework and
reporting that the champion "would have passed/failed" — remains **declined**.

**1. What it settles.** The folder asked for machinery to distinguish a hypothesis-first protocol
from a parameter sweep of the same length. Half of the answer is here, and it is quantitative: the
distinction is worth the difference between the columns of the table above. Moving from a 19:1
long-shot prior to even odds is worth about **1.0 in t-units** at a 5% posterior-null target — real,
bounded, and far smaller than the rhetorical weight the distinction usually carries. The other half —
what the discount costs elsewhere — is in the companion note.

**2. The composition that is now available, and is free.** Session 11 obtained the closed-form
**paired** standard error of a difference of Sharpe ratios,
`T·Var(Δ̂) = 2(1−ρ) + ½(Sh_a² + Sh_b²) − Sh_a·Sh_b·ρ²`. A difference divided by that standard error
is a `Z`, and `exp(−Z²/2)` is then the MBF for the hypothesis "this candidate genuinely beats the
champion". Nothing new needs measuring: the paired SE is computable in closed form before a candidate
is built, so the whole chain — predicted `ρ` → paired SE → `Z` → MBF → Bayesianized p under a stated
prior — is a **pre-trial** calculation. Three cautions attach and all are load-bearing. The paired
closed form is a *floor* on the error bar (liberal under fat tails and volatility clustering, per
Ledoit–Wolf), so the `Z` it produces is an upper bound and the MBF a lower one — two optimistic
approximations compounding in the same direction. The MBF is itself the most favourable Bayes factor
available. And the result is a comment on the *comparison*, not a substitute for the gate.

**3. The base-rate argument applied honestly to this repo.** Harvey's three reasons for a declining
prior all have local analogues. `learnings.md` records that signal-definition work is "heavily
explored and low-yield"; the folder's own tally is that the literature has closed six directions and
opened roughly one; and the universe is ~145 fixed instruments against an unbounded space of
constructions. Each is an instance of one of his three mechanisms. The implication is uncomfortable
and should be stated: **the prior odds for a new idea in this repo's most-worked family are getting
worse over time, so the required t for the same posterior confidence is rising for reasons entirely
separate from the trial count.** The DSR's rising bar and this are two different effects that happen
to point the same way.

**4. The choice-space point, which the repo has already half-recorded.** `learnings.md` notes that
`main`'s recorded trial count understates the true number of candidates attempted (34 recorded vs 53
attempted at one accounting; 45 recorded vs 11 effective under DSR clustering at another). Harvey's
ticker demonstration is the same observation with the count pushed further: the honest denominator
includes choices that were made silently and never appeared as trials — lookback grids not swept
because one value was picked, buffer widths chosen by convention, universes not varied. This does not
license a session to invent a number; it licenses recording, in the journal, which choices a
candidate fixed by fiat rather than by test.

**5. The counterweight that must travel with the whole idea.** Harvey's conclusion runs *against* the
use a lab would most like to make of him. His thesis is that finance's priors are long shots and the
field's thresholds are consequently too low, not too high. Anyone citing this note as support for
easing a bar has read it backwards.

**Pitfalls.** (a) The MBF requires a normal-approximation `Z`; a Sharpe-difference statistic on
1,562 daily observations is plausibly in that regime but its own standard error is the fragile part,
not the normality. (b) Prior odds must be *stated*, not implied — the whole value of the framework is
that it forces the prior into the open, and it is trivially abusable if the prior is chosen after
seeing the result. (c) Nothing here handles multiplicity; it is a per-hypothesis calculation.

## Related

- `notes/2026-08-25-prior-weighted-multiple-testing.md` — the frequentist companion. It supplies the
  constraint this note lacks (a discount must be paid for out of a fixed budget); this note supplies
  the exchange rate the other lacks (what a prior is worth in t-units).
- `notes/2026-08-24-multiple-testing-haircut.md` — Harvey–Liu's haircut, and Harvey–Liu–Zhu, whose
  "t > 3" recommendation this address explicitly says is necessary but not sufficient. Read together
  they are one author's position across two papers, and the later one is the qualification.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — the gate's statistic, which is a frequentist
  single-threshold construction with no slot for a prior.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the paired standard error that turns a
  Sharpe gap into the `Z` this note's MBF consumes.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — post-publication decay, the empirical
  consequence of the publication-bias mechanism described here.
- `experiments/learnings.md` — the recorded-versus-attempted trial-count gap, and the ⚠ standing
  protocol concern.
