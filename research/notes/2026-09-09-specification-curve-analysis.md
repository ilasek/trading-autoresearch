---
title: "Specification curve analysis"
authors: Simonsohn, Simmons, Nelson
year: 2020
venue: Nature Human Behaviour 4(11), 1208–1214 — Tier 1 (peer-reviewed, methods "Resource" article)
url: https://doi.org/10.1038/s41562-020-0912-z — text read: https://faculty.wharton.upenn.edu/wp-content/uploads/2016/11/33-Simonsohn-Simmons-Nelson-2020.pdf
citations: 474 (Semantic Scholar, DOI:10.1038/s41562-020-0912-z, checked 2026-09-09)
sample_period: n/a — no market data. Two published social-science datasets are re-analysed as worked examples.
markets: none (research methodology)
tier: A
validation_overlap: false
published_post_2018: true
---

Read **in full** from the authors' institutional copy of the published article; `pypdf`
extracted it cleanly. This is the methods note for the two empirical ones written the same
session: `2026-09-09-nonstandard-errors-evidence-generating-process.md` establishes that
dispersion across defensible analysis paths exists and is large;
`2026-09-09-nonstandard-errors-in-portfolio-sorts.md` measures it for portfolio sorts. This one
is the recipe for *enumerating and displaying* that dispersion when you are one researcher rather
than 164 teams — which is this lab's situation exactly.

**Boundary declared up front.** The method has three steps and this folder imports **two of
them**. Step 3 is a joint significance test across the specification set, and a joint test is
inference machinery of the kind `SUMMARY.md` has embargoed since 2026-09-01. It is described
below so that a future session can see precisely what was declined and overrule the judgement
if it disagrees — but nothing in this folder should turn a `t`, a threshold or a promotion
decision on it. Steps 1 and 2 produce a *dispersion measured on train*, which is the same object
as the lab's free IC, monotonicity and depth-profile screens, and they are what this note
recommends.

## Mechanism

The problem: converting a hypothesis into a testable statistic requires many decisions that are
simultaneously **arbitrary** (nothing in the theory picks one) and **defensible** (a competent
reader would accept any of them). Reporting one such path gives the reader a standard error,
which measures sampling noise *within* that path, and tells them nothing about how far the answer
would have moved along a different one. Worse, the path is not drawn at random: researchers are
more likely to report evidence consistent with the claim they are making, so the reported
specification is a biased draw from the defensible set.

Specification curve analysis reports **all** reasonable specifications instead of one, where
"reasonable" is defined by three conditions that must all hold: a specification must be (1) a
sensible test of the research question, (2) expected to be statistically valid, and (3) not
redundant with another specification already in the set.

The authors are explicit that this is *not* "run every variant for robustness". They reject
including specifications that are theoretically unmotivated or unambiguously inferior to an
alternative — such a specification does not belong in a robustness test at all, and padding the
set with them mainly dilutes whatever the curve shows. The judgement about what is defensible is
the researcher's and it is the hard part; the enumeration is the easy part.

The method also composes with pre-registration in a way that matters for an autonomous lab:
rather than pre-committing to one analysis (and therefore, when paths disagree, blindly
pre-committing to one *conclusion*), a researcher can pre-commit to running the entire set they
consider valid, and learn afterwards which decisions the conclusion hinged on.

## Construction recipe

**Step 1 — identify the set.** Three sub-steps: (a) enumerate the data-analytic decisions needed
to map the hypothesis onto a statistic; (b) enumerate the defensible alternative settings of each
decision; (c) take the exhaustive combination, then delete combinations that are invalid or
redundant. If the surviving set is too large to estimate, draw a **random subset** (the authors
suggest a few thousand) rather than pruning by judgement — pruning by judgement reintroduces the
selection the method exists to remove. Their worked example reduces five decisions to 1,728
surviving specifications.

**Step 2 — estimate and display.** The **descriptive specification curve** is a two-panel figure:

- *Top panel*: the estimated effect size for every specification, **sorted by magnitude**, with
  significance marked. This shows the range of answers the defensible set produces and where the
  authors' own chosen path sits within it.
- *Bottom panel*: a "dashboard" — one row per decision node, one tick per specification, aligned
  to the same x-axis. This is the part that does the work: it makes visible *which* analytic
  decisions the estimate covaries with, without assuming that effect is linear or additive. In
  their worked example the dashboard shows that the handful of negative estimates all require one
  idiosyncratic combination of three specific choices, which is a stronger and more legible
  statement than any summary statistic.

Two summaries fall out of step 2 with no inference at all: the **standard deviation of the
estimate across specifications** (this is the non-standard error of the other two notes) and the
**share of specifications whose estimate has the predicted sign**.

**Step 3 — joint inference (described, not imported).** The null is that the effect is zero in
every specification. Three candidate test statistics: (1) the median effect across
specifications; (2) the share of specifications significant in the predicted direction; (3) the
average Stouffer `Z` across specifications, which the authors prefer on efficiency grounds since
it avoids discretizing each p-value. The null distribution is generated by a bootstrap that
enforces the null *per specification*: for each specification `k` with estimate `β̂ₖ`, form
`y*ₖ = yₖ − β̂ₖ·xₖ`; resample rows with replacement, **using the same drawn rows across all
specifications** so that cross-specification dependence is preserved; re-estimate all `K`;
repeat 500–1,000 times; and read off the share of resampled curves whose overall test statistic
is at least as extreme as the observed one.

Note the shared-rows detail — it is the same device as the studentized stationary bootstrap in
`2026-09-06-monotonicity-tests-for-portfolio-sorts.md`, which resamples dates once and applies
the draw across all bins. Whatever else is true of step 3, its dependence handling is the same
one the lab has already accepted in a screen it runs.

**Stated limitations, from the authors.** Equal weighting of specifications is a default, not a
result — weighted variants of all three statistics exist but the authors doubt meaningful weights
can be identified in practice. The set can never be exhaustive. And because the method reduces
rather than eliminates ambiguity, a motivated researcher retains room to shape what goes in the
set.

## Robustness evidence (qualitative only)

This is a methods paper, so "robustness" means adoption and demonstrated discrimination rather
than out-of-sample replication. Both are present. It is heavily cited for a 2020 methods
article; it is published in a Tier 1 peer-reviewed venue with reference implementations released
by the authors; and its own demonstration is a discriminating one — applied to three findings
from two published papers, it reports one as robust, one as weak and one as not robust at all.
A method that returns "robust" for everything it is pointed at would be worth little, and this
one does not.

It sits in an identified lineage the paper places itself in — extreme-bounds analysis, reporting
the SD of estimates across a few chosen alternatives, and multiverse analysis (Steegen,
Tuerlinckx, Gelman and Vanpaemel, *Perspectives on Psychological Science*, 2016, DOI
10.1177/1745691616658637; 1,141 citations, Semantic Scholar, checked 2026-09-09 — **not read**,
cited here only as the acknowledged predecessor for the "report the whole set of defensible
analyses" idea). Its claimed advances over that lineage are the dashboard display, which
localises *which* decision drives the variation, and the joint test this folder declines.

## Implementability here

**What to import: steps 1 and 2, on train, in the scratchpad.** The object to curve is not a new
strategy — it is a construction the lab already owns. The concrete first run:

1. **Decisions.** Take the seated champion and list the nodes its own construction fixes: pool
   the ranks are computed over, `CORE_N`, `BAND_N`, tranche count `K`, lookback, skip,
   min-history requirement, weighting scheme. The
   `2026-09-09-nonstandard-errors-in-portfolio-sorts.md` table maps each to its published
   analogue if a defence is wanted for including it.
2. **Settings.** For each node, list only settings the lab would actually defend in a candidate
   file — the condition (1)-(2)-(3) test above, applied honestly. A `CORE_N` of 3 is not
   defensible on a ~96-name scoreable pool and does not belong in the set; the range the lab's
   own trials have already used is the natural defensible range.
3. **Set.** Exhaustive combination, delete the invalid (e.g. `BAND_N < CORE_N`), and random-
   subsample if it does not fit the compute budget.
4. **Score on train only.** Every point on this curve is a free measurement, exactly like the
   lab's depth profiles. **None of it goes through `run_experiment.py`** — that would record
   hundreds of trials, raise the deflated-Sharpe bar for all future candidates, and read
   validation. This is the one way the note could do harm and it is worth restating in any
   session that acts on it.
5. **Display and read.** Sorted train Sharpe across the set, plus a dashboard of which node each
   point used. The two numbers to carry out: the **SD across the set** (the champion's own
   non-standard error) and **which node the variation localises on**.

**What that buys, concretely.** The lab's live decisions are priced on Sharpe *differences* — the
required-gain table, the nine-session blend decline, the promotion margins. The curve's SD is the
scale on which those differences should be read. If the champion's construction alone spans a
range comparable to the margins the lab acts on, then the ranking is partly a ranking of paths;
if it does not, the lab's margins survive a real challenge and the question is closed. Both
answers are findings, which is the shape `SUMMARY.md` says a proposal should have.

**A second, cheaper use that needs no new machinery.** The dashboard's diagnostic value is
available even at `K = 8` or so. Any time a session proposes a candidate that differs from an
existing book at more than one node, scoring the intermediate combinations on train separates
"the signal did it" from "one of the two knobs did it". The lab has already done exactly this
once, by hand and without the name: the 2026-09-08 `price-trend` pair was designed as two trials
differing in a single expression (`CORE_N` 22 → 30) specifically to remove the first's confound.
That is a two-point specification curve, and it is the right instinct generalised.

**What not to import, restated.** Step 3's joint test. It is the part that would let a session
say "the effect is jointly significant across specifications", and that is a `p`-value on a
family of tests — the embargoed object. The folder's standing position is that dispersion
measured on train is admissible and threshold-adjusting inference is not, and this note stays on
that side of the line deliberately. If a future session concludes the embargo should not have
covered step 3, the argument to beat is that its bootstrap gives a *decision rule* rather than a
*measurement*, and the lab's decision rules live in a frozen file that belongs to the human.

**A limitation that binds harder here than in the source.** The authors warn that the set can
never be exhaustive and that a motivated researcher shapes what goes into it. An autonomous agent
writing its own defensible-set definition, scoring it, and then reporting the result is that
failure mode with nobody in the loop. The mitigation the paper offers is pre-commitment: write
the node list and the settings into the journal entry **before** scoring anything, and treat a
node added after seeing results as a finding about the agent rather than about the strategy.

## Related

- `2026-09-09-nonstandard-errors-evidence-generating-process.md` — why the dispersion this method
  displays is worth displaying, measured against human research teams.
- `2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the same enumeration carried out on
  factor construction, with the node list closest to this repo's own knobs.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — the shared-draw bootstrap device, and
  the precedent for taking a source adjacent to the inference embargo when what it yields is a
  train-split statement about a construction's shape.
- `2026-08-17-rebalance-timing-luck-tranching.md` — a one-node specification curve avant la
  lettre, and the node this lab already treats as consequential.
- `2026-08-24-multiple-testing-haircut.md`, `2026-08-24-deflated-sharpe-ratio.md` — the embargoed
  neighbours. Step 3 belongs with them; steps 1 and 2 do not.
