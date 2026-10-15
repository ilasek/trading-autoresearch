---
title: "Performance Measurement via Random Portfolios / Random Portfolios for Evaluating Trading Strategies"
authors: Burns
year: 2004 and 2006 (working papers); the first revised as a chapter in *Optimisation, Econometric and Financial Analysis* (Springer, 2007)
venue: "Burns Statistics working papers — venue tier 3 (credible practitioner research, single-author firm). The 2004 paper's revision appears as a chapter in an edited Springer volume (*Advances in Computational Management Science*), which lifts the methodology half slightly above a self-published note but is not peer review in the JF/JFE/RFS sense"
url: "https://doi.org/10.2139/ssrn.630123 (2004) · https://doi.org/10.2139/ssrn.881735 (2006) · https://doi.org/10.1007/3-540-36626-1_11 (Springer chapter). Both working papers read in full from the author's own site: https://www.burns-stat.com/wp-content/uploads/perfmeasrandport.pdf and https://www.burns-stat.com/wp-content/uploads/evalstrat.pdf"
citations: "8 for the 2004 working paper, 7 for the 2006 working paper, 6 for the Springer chapter (Crossref is-referenced-by-count, checked 2026-10-15); 10 for the Springer chapter (OpenAlex, checked 2026-10-15). Low absolute counts; per `research/README.md` the tier is not downgraded on count alone for practitioner work, and the method itself is cited well beyond these records by later authors who re-derive it"
sample_period: "illustrative only — a ~190-name unsystematic mixture of US large and small caps from 1996, with the strategy example trading over a ~1000-day window inside it. No multi-decade or multi-market claim is made"
markets: US equities (one illustrative universe)
tier: "C — practitioner working papers, no replication, no multi-market evidence, and the empirical content is one worked example. Graded as hypothesis-and-method fodder, NOT as evidence. What makes it worth a note at full depth is that it is the primary source for the construction this lab's own hard gate implements, and its methodological claims (the p-value convention, the Fisher pathology, the matched-dimension argument) are checkable arithmetic rather than empirical findings"
validation_overlap: false
published_post_2018: false
---

## Access

Both working papers read in full from `burns-stat.com/wp-content/uploads/<slug>.pdf`, linked from
the paper's own landing page under `/documents/working-papers/<slug>/`. HTTP 200, 215 KB and
916 KB, `pdftotext -layout` → 52 KB and 30 KB of clean text, 320 and 213 instances of `" the "`,
`( )`-dropout check zero. **A single-author consultancy's own flat `/wp-content/uploads/` directory
is a first-try channel in the same family as `research/README.md`'s faculty-page and
`robjhyndman.com/papers/` lessons**, and the landing page prints the exact filename, so no guessing
is needed.

The Springer chapter (`10.1007/3-540-36626-1_11`) was **not** obtained and nothing below is
attributed to it; the author's own landing page says it is the 2004 paper "with some additional
material", and the 2004 text was read instead.

## Mechanism

This is not a strategy. It is the primary source for **the object this lab's binding gate is made
of**, and until tonight the folder had 189 notes and zero coverage of it. `program.md`'s hard gate
reads: *validation Sharpe must beat the 90% quantile of 200 random portfolios built exactly like
the candidate (same holdings schedule, weights and stock/ETF mix) from the same point-in-time
pool*, region-matched under v3. That construction is this literature's, and these two papers are
where its logic, its correct p-value and its known failure modes are set out.

**The idea.** Replace the *reference point* (a benchmark) with a *reference set*: the distribution
of outcomes over portfolios that **obey the strategy's constraints but use no information**
("random portfolios … portfolios that obey given constraints but ignore utility"). A strategy's
p-value is its rank inside that distribution. Three properties follow, and they are the reason to
prefer it to a benchmark comparison:

1. **It is distribution-free.** "The statistical statements that result are distribution-free —
   there are no assumptions on the distribution of returns or measures of utility." Any statistic
   can be graded: return, Sharpe, a utility, a drawdown, a net-of-cost number. Nothing is assumed
   about return normality or about a factor model being correctly specified.
2. **A benchmark-relative ratio mixes skill with *opportunity*.** The paper's cleanest argument:
   imagine every asset in the universe returns the same amount over a window. Portfolios still
   differ from the benchmark day to day, so tracking error is non-zero — but every portfolio ends
   the window with the same return, so **every information ratio is zero regardless of skill.**
   Information ratios "are not purely a measure of skill, but rather are a combination of skill and
   opportunity." The dispersion of the random-portfolio distribution in a window *is* that window's
   opportunity set, measured rather than assumed.
3. **The probability of beating a fixed benchmark is dominated by the benchmark's own weights.** A
   benchmark is hard to beat precisely when its heavily weighted names happen to do well, and the
   more unequal its weights the wilder the swing. The paper's three artificial benchmarks on one
   universe were highly correlated with each other and yet gave *unrelated* outperformance
   probabilities across sub-periods, because **small differences in benchmark return translate into
   large differences in the fraction of random portfolios beaten.** Stated positively: a
   random-portfolio percentile is a *very sensitive* measure. Stated as a warning: it is a
   magnifying glass, and two strategies whose statistics differ trivially can land far apart in
   percentile.

**The second paper's addition: the null is a distribution over *paths*, not over portfolios.** For
a trading strategy (as against a fund's holdings), the right null is "a number of hypothetical fund
managers that perform the same task that we do, but have no skill" — each one holding a portfolio
and, at each rebalance, making a **random trade away from its own current portfolio** subject to
the same constraints, including the turnover cap. The null then inherits the strategy's turnover
and its drift structure rather than being a fresh independent draw at each date.

## Construction recipe

Enough to implement, and each item is a decision the lab has already made implicitly:

- **The constraint set *is* the null hypothesis.** The draws must obey the number of names, the
  maximum weight, the concentration limits, the turnover cap, the long-only/long-short condition
  and the universe. "An accurate assessment of skill with random portfolios requires a knowledge of
  both the returns of the fund and the constraints that the fund obeys." Anything the strategy is
  constrained by and the draws are not becomes part of what the test measures.
- **The p-value is never zero.** It is `(n_extreme + 1) / (N + 1)`, where `n_extreme` counts draws
  as good as or better than the strategy and the `+1` counts the observed strategy itself. "In many
  cases this adjustment … can be considered pedantic. However, when using Fisher's method of
  combining p-values, the pedantry is necessary."
- **For combining, use *centered* p-values:** `p = (n_extreme + 0.5) / (N + 1)`, which keeps a
  draw-beating-everything record from mapping to an infinite normal quantile.
- **Combine sub-period p-values with Stouffer's method, not Fisher's.** Fisher's
  `−2 Σ ln p_i ~ χ²_{2k}` has a concrete pathology the paper demonstrates: a record that is extreme
  in *both* directions across sub-periods (beats every draw in some, loses to every draw in the
  others) yields a tiny combined p-value for skill **and** an identically tiny one for anti-skill —
  "we are in the uncomfortable position of being convinced that the manager both outperforms and
  underperforms." Stouffer (`Φ(Σ Φ⁻¹(p_i)/√k)`, weights allowed for unequal periods) returns ~0.5
  on the same record. The combination requires non-overlapping periods for independence.
- **Read the sequence, not only the total: the p-value control chart.** Non-overlapping sub-period
  p-values, Stouffer-smoothed, show *when* the strategy worked and when it did not, and can be read
  as a control chart signalling that a book has gone out of control in either direction.
- **Randomise the starting portfolio too, and run the whole procedure from several of them.** The
  influence of the starting portfolio persists far longer than its turnover suggests — in the
  paper's example the initial book was still handicapping the comparison after the portfolio had
  been turned over many times, and reversing the starting portfolio's signs produced a near-mirror
  null distribution that would have reversed the verdict. Recommended acceptance condition: run the
  procedure from several random starting portfolios, require the resulting p-values to be
  *uniformly* small, and be "quite concerned if any are close to 1".
- **Match every dimension on which the strategy systematically differs from the draws.** Two
  worked instances, and they are the most transferable thing in either paper:
  - **Realized volatility.** The example strategy's optimiser implicitly favoured lower volatility
    while the draws were unconstrained in it; the author's reading is that an unmatched volatility
    gap makes the p-values *drift* over the window and that constraining the draws to a volatility
    not much above the strategy's "would probably provide a fairer assessment".
  - **The number of closing positions.** Matching it removed an apparent decay in the strategy's
    edge over time — i.e. what looked like an alpha model losing power was the draws diverging from
    the starting portfolio faster than the strategy did.
  The general rule: **a random-portfolio test has power against exactly the dimensions on which the
  candidate differs from the draws, and no power against the dimensions that are matched.** Every
  matching decision is simultaneously a confound removed and a mechanism made invisible.
- **Symmetry is a property of the constraint set, not of randomness.** Long-short draws are nearly
  symmetric around zero gain *only if* flipping every sign stays feasible; a fixed starting
  portfolio or an asymmetric net-exposure band breaks that, and then the null's centre is wherever
  the constraint set puts it. For a long-only book the symmetry is broken by construction, so the
  null is centred on whatever the constraint set typically earns — never on zero.

## Robustness evidence (qualitative only)

Thin, and the note's tier says so. There is no replication, no multi-market evidence and no
multi-decade sample; the empirical content is one illustrative universe and one worked strategy.
The author's claim that random-portfolio tests have more power than information-ratio tests on the
same data is **unreplicated** and is recorded here as a claim, not a finding.

What does carry weight is that the methodological arguments are arithmetic rather than empirical —
the `(N+1)` denominator, the Fisher two-sided pathology, the opportunity-versus-skill argument and
the matched-dimension argument can each be checked without data, and the first three are standard
results in the Monte-Carlo-test literature. The method has been taken up and then *criticised* by
later authors on grounds that do not touch these points: see
`notes/2026-10-15-random-portfolio-inference-concentration-of-measure.md`, which cites this work as
the endorsed use case before arguing that the sampling distribution it relies on cannot be
objectively approximated.

## Implementability here

The lab is already running this test; what is new is the operating manual for it.

**What v3's null matches** (from `program.md`): the holdings schedule, the weights, the stock/ETF
mix, the point-in-time pool, the listing region of each replaced name, and — through the same
execution model — the costs and turnover. `experiments/learnings.md` [2026-10-07] confirms the cost
half empirically ("random books churned 22× a year pay the same costs").

**What it does not match, as far as `program.md` states:** the candidate's **realized volatility**
and the **number of positions that close** inside the window. Both are named failure modes above,
and both are already measured in the lab's standing pre-trial screen (slice volatility as a ratio
to the pool's) or are free to measure.

Five items, all free, none requiring the holdout:

1. **Report the null result as a p-value with its resolution, not as a bare percentile.** With 200
   draws the finest attainable p-value is `1/201 ≈ 0.005`: the lab's recorded "0th percentile"
   results are `p ≈ 0.995` *against* the candidate (and ≈ 0.005 for the one-sided test in the other
   direction), the "75th percentile" is `p ≈ 0.25`, and F8's "98th percentile" is `p ≈ 0.02` and no
   finer. A gate at the 90% quantile of 200 draws is a one-sided 10%-level Monte Carlo test, and
   quoting it that way makes the deflation bookkeeping comparable with every other test the lab
   runs.
2. **Stouffer-combine the two train sub-periods the protocol already reports apart.** v3 prints
   train skill for 1997–2008 and 2009–2017 separately. These are non-overlapping, so their null
   p-values combine legitimately, and the Fisher pathology is live here rather than hypothetical:
   the lab has already seen candidates strong in one sub-period and weak in the other, which is the
   exact record on which Fisher's method certifies both skill and anti-skill. Use centered
   p-values.
3. **Build the p-value control chart, i.e. the sequence of sub-period null percentiles.** This is
   the generalisation of the lab's own [2026-10-14/15] decomposition
   (`geography = null_median − pool`, `selection = candidate − null_median`), which is the
   one-window version. A *sequence* separates two hypotheses the single window cannot: the signal
   decayed, versus the null drifted away from the candidate on an unmatched dimension.
4. **Read the null's standard deviation as the window's opportunity set.** The lab's [2026-10-07]
   K-table already has it (`sd` 0.094 at K=10 down to 0.013 at K=200 on train). The consequence is
   that a percentile is skill *divided by* opportunity: two windows in which a book has identical
   skill will give different percentiles if the dispersion differs, which is a mechanism-level
   reason that the lab's validation percentiles and its train screens disagree so often, and it
   predicts that the disagreement is worse for large-K books because their null is tight.
5. **Treat the volatility gap as a live and *signed* question rather than a settled one.** This
   source says an unmatched volatility advantage flatters the candidate; the lab has one
   observation pointing the other way (`rv_arbrisk_peer_neutral`, slice volatility 0.92× the
   pool's, landed at the 0th percentile). One observation is not a refutation, and the reverse
   reading is in the sister note: variance reduction may be the one axis the null cannot imitate.
   Either way it should be quoted with every trial and not assumed to be neutral.

**Pitfalls.** (a) The draws' construction must stay outside a candidate's reach — "the constraint
set is the null hypothesis" means a candidate that changes its constraints changes its own test.
The lab's frozen-engine rule and its [2026-10-07] finding that concentration is judged against a
*wider* null are the right answer to this, and this note is the reason the rule matters rather
than a formality. (b) None of this licenses reading the holdout: everything above is computable on
train and on validation from numbers the protocol already prints. (c) The path-wise versus
per-date-independent question about the lab's own draws is **not resolved here** — `engine/` is not
readable in a research session, and `program.md`'s "same holdings schedule, weights and stock/ETF
mix" does not settle whether successive draws are linked. It is a question for the nightly, not an
assumption to build on.

## Related

- `notes/2026-10-15-random-weight-indices-and-the-equal-weight-centre.md` — why this null's *centre*
  is the equal-weight pool and only its dispersion is a design choice.
- `notes/2026-10-15-random-portfolio-inference-concentration-of-measure.md` — the direct argument
  that this test is not valid for significance, and why the lab's version escapes one half of that
  argument and not the other.
- `notes/2026-09-15-reality-check-max-statistic-under-dependence.md` and
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md` — the folder's existing coverage
  of resampling against a *max* statistic over many strategies. That is a different null (one
  strategy's many variants) from this one (one strategy's many unskilled peers); the lab runs both,
  the deflator and this gate, and [2026-10-07] found this gate the binding one.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the parametric alternative the lab
  uses for its holdout veto (Jobson–Korkie with Memmel's correction); this null needs none of its
  distributional assumptions and grades any statistic, which is the trade this note is about.
- `experiments/learnings.md` [2026-10-07] (the K-table and "the gate reduces to beat pool +
  1.28·sd(K)"), [2026-10-13/14] and [2026-10-14/15] (the geography/selection split, and the three
  recorded null percentiles) are the lab's own measurements of the object described here.
