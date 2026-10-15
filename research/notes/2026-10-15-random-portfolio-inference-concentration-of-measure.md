---
title: "Randomized Control in Performance Analysis and Empirical Asset Pricing"
authors: Bachelard, Chalkis, Fisikopoulos, Tsigaridas
year: 2024
venue: "arXiv / SSRN working paper — venue tier 2 at best on this folder's rubric (preprint with substantial technical content, but almost no citations yet, so in practice it is graded as tier 3/4 evidence and tier-1 *argument*)"
url: "https://arxiv.org/abs/2403.00009 · https://doi.org/10.2139/ssrn.4744249"
citations: "1 (Crossref is-referenced-by-count on the SSRN DOI, checked 2026-10-15). Semantic Scholar returned HTTP 429 on the arXiv id and was not retried; OpenAlex not spent on it"
sample_period: "1995–2022 for the price data, with backtests beginning 2000; US large- and mid-cap only. The analytic results (concentration of measure, the m-out-of-n identification) carry no sample"
markets: "US (a CRSP proxy for the MSCI USA universe — ordinary common shares on NYSE/AMEX/NASDAQ covering 85% of total market capitalisation, ~600 names per rebalance, with a trailing-median-volume liquidity screen)"
tier: "C as evidence — a preprint with ~1 citation, no replication, one market, and an empirical section built on one index provider's guidelines. B-to-A as *argument*: its central negative result is a two-line expectation calculation plus a standard concentration-of-measure fact, both checkable without data, and it is the only source the folder has found that directly addresses the validity of the test this lab's binding gate implements"
validation_overlap: true
published_post_2018: true
---

## Access

arXiv PDF, first try: HTTP 200, 1.2 MB, `pdftotext -layout` → 187 KB of clean text, 1,046 instances
of `" the "`, `( )`-dropout check zero, displayed mathematics intact. `file` reported "2 page(s)",
which `research/README.md` already records as meaningless — judge by the character count.

**Anti-lookahead handling.** This is a post-2023 publication with a sample that reaches into the
lab's validation window, so it is flagged on both counts and handled strictly: its empirical
section is recorded **as shapes and signs only**, with every correlation coefficient, every
performance figure and every dated reference deliberately omitted, and its one narrative aside
about a post-sample market episode is not recorded at all. Everything load-bearing below is
analytic.

## Mechanism

The folder arrived at this source asking what the lab's random-selection gate is a valid test *of*.
The answer this paper gives is blunt, and it is aimed precisely at the construction
`program.md` uses: **"the use of RP-based statistical significance tests to evaluate the (over- or
under-) performance of a particular investment strategy is not appropriate. As a purely descriptive
tool, however, we consider RP-based analysis to be valuable."** Two independent reasons, one
geometric and one definitional.

**(1) A random portfolio is not an enumeration of the feasible portfolios — the measure concentrates.**
The narrative behind random-portfolio testing is that "any portfolio structure is just as likely to
occur as any other". In high dimension that is false in a specific, computable way. For weights
drawn uniformly on the `n`-simplex, the paper gives

- `E‖ω‖²₂ = (2n − 1)/n²`, and therefore
- `E‖ω − ω̄‖²₂ = (n² − n)/n³`, with `ω̄` the equal-weighted portfolio,

which **tends to zero as `n` grows**. The uniform measure piles up on a thin shell of homogeneous,
near-equal-weighted allocations — "the high-volume area of the domain" — so sparse or concentrated
portfolios (a cap-weighted book, a top-20 sort) are "extremely unlikely to be sampled". The support
of the null is a small, geometrically special region of the feasible set, not the feasible set.

**The identification that matters most here:** the standard recipe of *drawing `m` names uniformly
from `n` and equal-weighting them* — which is the lab's random-selection null — "essentially
constitutes an **m-out-of-n bootstrap**". The paper then reads off its two limits:

- At `m = n` the density "merely provides a measure of the uncertainty in the performance of the
  equal-weighted strategy", because every draw is close to equal weight in weight space. The null
  stops being a null about skill and becomes the sampling distribution of the benchmark.
- As `m` falls, the imposed sparsity widens the dispersion of weights and pushes the draws toward
  **higher volatility**; the distribution broadens and its mass moves out along the risk axis. But
  it still "cover[s] only a small area of the space of feasible solutions, reflecting the
  homogeneity of sampled portfolios."

And hence the sharpest sentence in the paper for this lab's purposes: using such distributions for
significance testing "would likely result in **overly optimistic rejections of the Null
hypothesis**" — the null is too *tight*, so the test is too easy to pass, not too hard.

**(2) "No skill" is not defined until the reference point is.** A naive random portfolio centres on
the equal-weighted portfolio; a "basic" one can be centred on capitalisation weights, and either is
constructible. The two give opposite verdicts on whether the average investor is skilled, and the
paper is explicit that the dispersion is a dial as well: "We could have further expanded or
contracted the risk-return distribution by adjusting the variance in the weights, essentially
**reverse-engineering the random control to achieve a desired statistical test result. A dangerous
game.**" The equal-weighted portfolio is the naive benchmark from a *portfolio-selection*
standpoint (it is the Markowitz solution under cross-sectionally constant expectations) and is
*not* naive from an *asset-pricing* standpoint (it is an exposure to systematic styles, foremost
low size) — and the paper blames the conflation of the two for "unnecessary misinterpretations".

**The rejoinder that defuses the monkey literature.** That random portfolios beat a cap-weighted
index "does not imply that any strategy, or even most strategies, outperform the benchmark", by
Sharpe's arithmetic of active management: a random portfolio samples the **name** space uniformly
while cap weighting samples the **capital** space. The outperformance is a property of the sampler.

**The demonstration.** A deliberately meaningless characteristic — how many times a given letter of
the alphabet appears in a company's name — was used to form long-only books from a large-cap parent
index, point-in-time, held between quarterly rebalances. Every letter's book outperformed the
cap-weighted parent, a Sharpe-ratio test of the kind this folder already holds
(`notes/2026-08-24-testing-differences-of-sharpe-ratios.md`) rejected equality for the example
letter, and **inverting each book — holding everything except the named letter's firms — outperformed
as well**. Under a six-factor model most loadings were significant, market betas were below one,
and the alphas were positive and significant for nearly every letter; switching to a
thirteen-theme factor set left the alphas qualitatively unchanged while *reversing the sign* of
several betas, both with high significance. The resolution is the random portfolio used
descriptively: the letter books all sit inside the high-mass region of a naive RP's risk-return
distribution, while the cap-weighted index sits far outside it. The verdict "these are chance" is
available from the *location*; the verdict "this is significant" was available from the *test*, and
was wrong.

**The use the paper endorses instead — and it is a buildable diagnostic, not a critique.** Keep the
draws, and study **the relation between a draw's characteristic exposure and its performance**
across the sample of draws: `γ = ⟨ω, β⟩` against the draw's realized return and risk. This answers
"is this characteristic rewarded *inside* the constraint set", which a sort cannot, and it beats
sorting on two counts the authors name: it does not depend on the within-bin weighting scheme, and
it shows the **uncertainty** around a quantile portfolio — "some of the quantile portfolio[s] are
rather outlying relative to the conditional performance distributions". Their findings from running
it, signs and shapes only:

- Exposure versus **return** was positive for the value-, momentum- and quality-flavoured
  characteristics and slightly negative for size (in a universe containing only large and mid caps),
  with value and momentum showing a **non-linearity whose slope steepens at both ends**.
- Exposure versus **risk** was **U-shaped for every characteristic**: books with extreme exposure in
  *either* direction carried higher variance than unexposed books.
- Adding the benchmark-relative constraints of a real multifactor index **lands the feasible set on
  one leg of that U**, converting the U into a near-monotone relation whose sign depends on which
  leg — and in the process weakening some exposure-return relations substantially and extinguishing
  one of them, while leaving another intact.
- Their summary judgement, as a shape: tilts toward the value- and momentum-flavoured
  characteristics bought return and paid for it in volatility; the quality-flavoured tilt reduced
  risk without reducing return; the size tilt was unfavourable on both axes, and yet any deviation
  from a concentrated cap-weighted allocation mechanically increases size exposure, so the other
  tilts each carry one without its drag.

## Construction recipe

For the diagnostic, which is the part worth implementing:

1. Fix the constraint set that actually binds the strategy (long-only, the simplex, per-name caps,
   any exposure bounds, the point-in-time pool).
2. Sample the constraint set. Uniform-on-the-simplex is *not* the recommendation — it yields
   "solely homogeneous and biased portfolios". Instead **centre** the draws on a declared reference
   portfolio and match the candidate's cardinality at each rebalance date, which for a set of
   sub-books means convolving one RP per sub-book at its own cardinality. For constraint sets with
   non-trivial geometry (quadratic variance bounds, benchmark-relative exposure bands) the paper's
   technical contribution is the use of **geometric random walks** — ball walk, hit-and-run,
   coordinate-directions hit-and-run, billiard walk, Dikin/Vaidya/John walks, HMC and a reflective
   NUTS variant — surveyed with complexity results, with a C++/R implementation released.
3. For each draw compute both the performance statistic and the characteristic exposure
   `γ = ⟨ω, β⟩`, where `β` may be regression loadings on a long-short factor or standardised
   stock-level characteristics (the paper uses both and notes they correlate surprisingly weakly).
4. Read the joint distribution: exposure against return, exposure against risk, and risk against
   return, with a low-degree polynomial fit rather than a line, and overlay the candidate book.
5. Treat the output as **association, not causation** — the authors are explicit that this is not a
   treatment-control design and that the categories of an attribution are not causes.

## Robustness evidence (qualitative only)

- **The negative result is analytic** and does not depend on the sample: the two expectations above,
  plus the standard concentration-of-measure fact about the uniform measure on a high-dimensional
  convex body. That is why this note's tier splits argument from evidence.
- **The positive, empirical half is one market, one index provider's constraint set, ~600 names per
  rebalance, no peer review and essentially no citations.** The sample overlaps the lab's validation
  window. Nothing in the empirical half is treated as a finding here.
- **It agrees with the earlier literature where it should.** It cites the random-portfolio
  performance-measurement tradition (including Burns) as the "typical use case endorsed in the
  literature" before departing from it, and reproduces the cap-weighted-index-in-the-left-tail
  result that `notes/2026-10-15-random-weight-indices-and-the-equal-weight-centre.md` records.
- **It subsumes the bootstrap.** The paper shows the Efron-style resampling that appears throughout
  performance analysis is a particular instance of a random portfolio, the RP's advantage being that
  it can carry investor constraints. That claim is structural and is the reason this note sits
  alongside the folder's existing resampling coverage rather than replacing it.

## Implementability here

**The uncomfortable part first, and it must be read correctly.** The lab's binding hard gate is the
test this source says is invalid for significance. Two things keep that from being a crisis.

- **v3 escapes the paper's second criticism completely.** The reference-point ambiguity — the thing
  the authors blame for the misinterpretations in this literature — does not apply, because v3's
  *benchmark* is the equal-weight eligible pool and its null is a naive RP drawn from that same
  pool. Benchmark and null centre coincide by construction. In this paper's taxonomy the lab is
  running a naive RP against a naive benchmark, which is the coherent pairing; the incoherent
  pairings are the ones that produce monkey alpha.
- **The first criticism applies, and it cuts in the lab's favour.** If the null's support is a thin
  shell of near-pool books, the null is too *narrow*, and a narrow null means **overly optimistic
  rejections** — the gate is lenient, not harsh. So the lab's recorded 0th-percentile results are
  *stronger* evidence against those candidates than their percentiles suggest, and the gate's
  reputation as the binding constraint is not a sign that it is unfair. This is the same conclusion
  `#256` reaches from the net-expected-return side and `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md`
  reaches from the benchmark side: three independent routes to "the nulls are real".

**Why the frozen engine is load-bearing rather than bureaucratic.** "Reverse-engineering the random
control to achieve a desired statistical test result. A dangerous game." The lab's null copies the
candidate's own weight vector, so a candidate *does* partly choose its null's dispersion — and
`experiments/learnings.md` [2026-10-07] already measured the direction (concentration is judged
against a wider null, so it is not a free pass). That the sampler itself lives in `engine/` and
cannot be touched is what keeps the dial out of a candidate's hands. Worth stating in the journal
once, because it converts a rule into a reason.

**One free diagnostic, and it is the night's main buildable item.** Every v3 trial already generates
200 region-matched replica books and scores them. Each replica has an *exposure to the candidate's
own score* — `γ = ⟨ω_replica, score⟩`, computable on the dates the trial already uses — and a
realized Sharpe. Regressing the second on the first, with a quadratic term, gives the
exposure-performance relation **inside v3's actual constraint set** and answers three questions the
lab currently cannot:

1. **Is the candidate's book an outlier relative to equally-exposed random books, or a typical
   member of its own exposure class?** This is the folder's "is a sorted slice evidence" question
   (`SUMMARY.md`, "The shape of a sorted book") in the form this paper endorses, and it
   distinguishes a real tilt from a draw that happened to land where the score is high.
2. **Is the relation monotone over the reachable range of exposure?** The paper's finding is that
   constraints land you on one leg of a U, so the sign of the relation *inside* a constraint set can
   differ from the sign of the unconstrained sort. The lab sorts and takes a top-K slice; the U-shape
   prediction is that the extreme-exposure end carries higher variance, which a Sharpe objective
   penalises precisely where the sort concentrates.
3. **Does the exposure axis explain the geography/selection split the lab now quotes with every
   trial?** `geography = null_median − pool` and `selection = candidate − null_median` are two
   summary numbers; the replica-level scatter is the distribution they are summarising, already
   computed and currently discarded.

None of this touches the holdout, none of it needs new data, and — importantly — none of it is a
protocol change: it is a read of output the engine already produces.

**Two scope limits to carry.** (a) The algebra says uniform draws converge on equal weight at rate
`1/n`; at ~1,000 eligible names that convergence is essentially complete, so the lab's `p90`-flat-in-K
table is the Sharpe-metric shadow of this geometry and **not an independent fact** — do not cite the
two as corroborating each other. (b) The geometric-random-walk machinery is the paper's answer to
sampling a constraint set with quadratic or benchmark-relative bounds. The lab does not need it: its
constraint set is a simplex with per-name caps and a region quota, where direct draws suffice. Filed
as a pointer in case a future gate acquires a variance or exposure bound.

## Related

- `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — the method this paper criticises,
  whose matched-dimension rule is the constructive half of the same insight.
- `notes/2026-10-15-random-weight-indices-and-the-equal-weight-centre.md` — the ten-million-draw
  empirical case this paper re-reads, and the variance-axis hypothesis it leaves open.
- `notes/2026-09-15-reality-check-max-statistic-under-dependence.md`,
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md` — the folder's resampling
  coverage, which this paper's "the bootstrap is a particular instance of a random portfolio" claim
  places inside the same family.
- `notes/2026-09-11-parametric-portfolio-policies-standardized-characteristics.md` — the other route
  to "performance as a function of a characteristic exposure", by optimising the exposure rather than
  sampling it.
- `notes/2026-09-09-specification-curve-analysis.md` — the nearest thing the folder already holds to
  "locate the strategy inside a distribution of defensible alternatives"; this paper's descriptive
  use of RPs is the portfolio-weight version of the same discipline.
- `notes/2026-10-13-equal-minus-value-as-a-performance-evaluation-factor.md` — why an equal-weighted
  reference point is itself an exposure, which is this paper's reference-point criticism stated as a
  factor.
