---
title: "The Deflated Sharpe Ratio, and the probability of backtest overfitting"
authors: Bailey, López de Prado; Bailey, Borwein, López de Prado, Zhu
year: 2014
venue: Journal of Portfolio Management (venue tier 1 by this folder's rubric); companion in Journal of Computational Finance (tier 2)
url: https://doi.org/10.3905/jpm.2014.40.5.094 (DSR); https://doi.org/10.21314/jcf.2016.322 (PBO)
citations: DSR 147 (Semantic Scholar, checked 2026-08-24; Crossref 92). PBO 51 (Crossref, checked 2026-08-24; OpenAlex returns 0 and Semantic Scholar does not resolve the DOI — see Related)
sample_period: none — methodological; derivations plus Monte-Carlo verification on synthetic series
markets: none. The PBO companion illustrates on synthetic series and on unspecified strategy examples
tier: B+
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the source for the statistic in the promotion gate. `program.md` requires
`deflated-Sharpe probability ≥ 0.95`; `learnings.md` reasons at length about DSR clustering, trial
counts and effective-versus-recorded trials — all from local observation, with nothing in `research/`
on what the deflator assumes. This note covers the machinery. It is **explanatory only**: the engine
is frozen, the criterion is a human decision, and nothing below is a recommendation to change either.

The construction has two layers.

**Layer 1 — the winner's curse has a closed form.** Take `N` *independent* trials whose estimated
Sharpe ratios `{ŜR_n}` are drawn from a common distribution with mean `E[{ŜR_n}]` and variance
`V[{ŜR_n}]` (the authors motivate the common distribution by "strategy class": trials within one
research programme share a characteristic pattern). Then the expected **maximum** over the `N` trials
has a standard extreme-value approximation. The consequence is that the best of `N` tries has an
expected Sharpe ratio above zero *even when every trial's true Sharpe ratio is zero*, and it grows
with `N` and with the cross-trial dispersion.

**Layer 2 — deflate by comparing against that maximum instead of against zero.** The Probabilistic
Sharpe Ratio (PSR) computes the probability that the true Sharpe exceeds a user-chosen threshold,
correcting for sample length, skewness and kurtosis. The **Deflated** Sharpe Ratio is exactly PSR
with the threshold set to the expected maximum from layer 1. So DSR asks: *given how many things were
tried and how dispersed their results were, how surprising is this particular Sharpe ratio?*

Two consequences are worth stating separately because they explain repo-local observations that were
previously unsourced.

- **`N` is the number of *independent* trials, not the recorded count.** The authors are explicit
  that using `M` recorded trials where only `N < M` are independent overstates the threshold. Their
  suggested reduction interpolates between the two extremes on average pairwise correlation `ρ̂`:
  `N̂ = ρ̂ + (1 − ρ̂)·M`, so `N̂ → 1` as trials become perfectly correlated and `N̂ → M` as they become
  independent. **This is the mechanism behind `learnings.md`'s "DSR clustering makes within-family
  tuning nearly free"** — a family of near-identical candidates contributes almost nothing to the
  deflation, because it is almost one trial.
- **The threshold scales with `√V[{ŜR_n}]`, the *dispersion* of the trials' Sharpe ratios.** A
  research programme whose trials all land near each other faces a low bar; one that produces a wide
  spread of outcomes faces a high one. This is a second, independent channel making within-family
  tuning cheap — and it is perverse in an under-appreciated way: **a lab is penalised for the
  variance of its exploration rather than for the number of shots taken.**

The companion (PBO) attacks the same problem non-parametrically and from the model-selection side,
with a different question: not "is this Sharpe ratio significant?" but "**is my selection procedure
overfitting?**" — measured as the probability that the configuration chosen in-sample ranks below the
median out-of-sample.

## Construction recipe

**Expected maximum Sharpe ratio after `N` independent trials.** With `γ ≈ 0.5772` the
Euler–Mascheroni constant, `Z` the standard normal c.d.f., `e` Euler's number:

```
E[max{ŜR_n}]  ≈  E[{ŜR_n}]  +  √V[{ŜR_n}] · ( (1−γ)·Z⁻¹[1 − 1/N]  +  γ·Z⁻¹[1 − 1/(N·e)] )
```

Under the null that the true Sharpe ratio is zero the first term drops and the threshold is

```
ŜR₀  =  √V[{ŜR_n}] · ( (1−γ)·Z⁻¹[1 − 1/N]  +  γ·Z⁻¹[1 − 1/(N·e)] )
```

**Deflated Sharpe Ratio.** With `T` observations, `γ̂₃` skewness and `γ̂₄` kurtosis of the selected
strategy's returns (`ŜR` and `ŜR₀` in the same, non-annualised, per-period units):

```
DSR  =  Z[  ( (ŜR − ŜR₀) · √(T − 1) )  /  √( 1 − γ̂₃·ŜR + ((γ̂₄ − 1)/4)·ŜR² )  ]
```

Read the denominator: **negative skew and fat tails inflate it, lowering DSR** — i.e. a book whose
returns are left-skewed or leptokurtic needs a higher raw Sharpe ratio to clear the same bar. That is
the non-normality half of the correction, and it is the same input class Lo's variance formula uses.

Six inputs in total: `ŜR`, `T`, `γ̂₃`, `γ̂₄`, `V[{ŜR_n}]`, `N`. The first four are properties of the
selected strategy; the last two are properties of *the search that found it*.

**Estimating `N` from `M` dependent trials.** Compute the average off-diagonal correlation of the
trials' return series, `ρ̂ = ΣΣ_{i≠j} ρ_{ij} / (M(M−1))`, then `N̂ = ρ̂ + (1−ρ̂)·M`. The authors
attach two warnings and both matter: correlation is a limited notion of dependence, and **when
`M > T` — more trials than observations — the correlation matrix is numerically ill-conditioned and
the average correlation may itself be overfit**, because there are more pairwise correlations than
independent pairs of observations. Their suggested remedies are dimension reduction before averaging,
or an information-theoretic count of non-redundant sources (total correlation / multi-information).

**PBO by combinatorially symmetric cross-validation (CSCV).**

1. Form the `T × N` matrix `M` of per-period P&L series, one column per trial, rows synchronous
   across all columns.
2. Partition the rows into an even number `S` of disjoint contiguous submatrices of equal size.
3. Form **all** `C(S, S/2)` combinations of `S/2` submatrices as training; the complement is testing.
   (Symmetric by construction: training and testing sets are the same size, so the out-of-sample
   estimate is no less accurate than the in-sample selection.)
4. In each combination, pick the trial with the best in-sample performance metric, record its
   **rank** `ω̄_c` among all `N` trials out-of-sample, and form the logit `λ_c = ln(ω̄_c/(1−ω̄_c))`.
5. `PBO` = the fraction of combinations with `λ_c ≤ 0`, i.e. the probability the in-sample winner
   lands below the out-of-sample median. The *dispersion* of the logit distribution is informative
   too, not just its mass below zero.

CSCV is model-free, non-parametric, works with any performance metric estimable on subsamples, is
**deterministic** (unlike jackknife resampling, two runs give identical answers), and respects
time-dependence within blocks. Its stated requirement is that the `N` columns be alternative
configurations of a comparable search.

**A trial-budget heuristic, offered by the authors as the answer to "when should we stop testing?"**
Treat it as an optimal-stopping problem: from the set of *theoretically justifiable* configurations,
measure a random `1/e` (≈37%) of them, then keep drawing one at a time until one beats all seen so
far; stop there. The point is not the exact rule but the framing — **every additional trial
irremediably raises the false-positive probability, so the trial count should carry a cost in the
research design, not only in the deflator.**

## Robustness evidence (qualitative only)

- The extreme-value approximation for `E[max]` is **verified numerically** by the authors against
  Monte-Carlo draws across a wide grid of `(E[{ŜR_n}], V[{ŜR_n}], N)`, with the estimation error
  mapped as a heat map and the verification code published in the paper. This is the part of the
  construction with the least room for doubt.
- The PSR layer rests on a prior literature on Sharpe-ratio inflation from short samples and
  non-normal returns that this folder has independently covered (Lo 2002 and successors), so the
  non-normality correction is not a one-source claim.
- **No independent replication of the DSR statistic as such was found.** Its citation count is
  respectable rather than large for a decade-old article in a tier-1 practitioner journal.
- **The weakest joint is the input that does most of the work.** `N` is not observable, and the
  route the authors offer to it is an *interpolation* between two limiting cases, not a derivation;
  they say so themselves and add the `M > T` ill-conditioning warning. `V[{ŜR_n}]` requires that the
  unselected trials were recorded. Both are properties of the search process, which is exactly the
  information the paper argues is "the most important piece of information missing from virtually
  all backtests" — so the statistic's honesty depends on the honesty of a disclosure that is usually
  absent. In a lab that records every trial, this is a strength rather than a limitation.
- The claim that **backtest overfitting under memory effects leads to *loss* maximisation** — because
  the extreme random patterns an optimiser latches onto must be undone rather than merely diluted —
  is asserted here with the formal proof in a companion (Notices of the AMS) paper that was **not
  read** (the AMS PDF endpoint returned 403). Recorded as the source's assertion, not as verified.
- Likewise second-hand and flagged: the frequently-quoted result that **about seven trials suffice to
  produce a spurious two-year backtest with in-sample Sharpe above 1.0 and expected out-of-sample
  Sharpe of zero** is taken from Harvey–Liu's characterisation of the same companion paper (read in
  full — see the sister note), not from the original derivation.

## Implementability here

**1. What the DSR formula says about this repo's own gate, mechanically.** The deflation bar depends
on the search, through two numbers: `N` and `√V[{ŜR_n}]`. Neither is a property of the candidate.
Two operational readings follow, both free and both explanatory only:

- A candidate proposed inside a tightly-clustered family raises the bar for everyone else by very
  little, because it barely raises `N̂` and may *lower* `√V[{ŜR_n}]`. A structurally novel candidate
  raises it by much more. `learnings.md` observed the first half; the second half — that a wild
  trial *widens the dispersion and thereby raises the threshold for every later candidate more than
  its own increment to the count does* — is new, and is a reason to prefer well-motivated
  exploration over scattershot exploration that goes beyond the trial-count argument already on
  record.
- The `M > T` warning bites in the opposite direction from the one that might be expected here. This
  repo has far more observations than trials, so the average-correlation route to `N̂` is
  well-conditioned — an unusual and favourable position relative to the setting the authors describe.

**2. The holdout critique, which lands squarely on this repo's design and must be read carefully.**
The paper's position is blunt: "the holdout method can not prevent backtest overfitting: holdout
assesses the generality of a model as if a single trial had taken place… If we apply the holdout
method enough times (say 20 times for a 95% confidence level), false positives are no longer
unlikely: they are expected." Two things must be said, in this order.

- *This repo's protocol is better than the target of that criticism.* The holdout is not used for
  selection at all; it is evaluated automatically at promotion time, after the decision, and every
  touch is journaled. That is the strongest available form of the discipline.
- *And the criticism still applies at the level of the programme.* The number of holdout evaluations
  is itself a trial count of a second kind, and it is not currently deflated by anything. Six
  promotions is six looks. This does **not** license anything — using the holdout to select is
  forbidden by `program.md`, and the argument for that prohibition is exactly the one the source
  makes. It is recorded so that the count is visible.

**3. PBO/CSCV is computable here, and is a returns-scoring diagnostic rather than a free one.** The
repo stores each trial's validation return series on a common 1,562-day index, which is precisely the
`T × N` matrix CSCV needs. Running CSCV over it would answer, non-parametrically, "has this lab's
selection procedure been overfitting?" — a question no statistic currently in the repo asks. Three
qualifications, and the third is a caution the folder should hold itself to. (a) By the discipline
recorded at session 6, **anything that scores returns is not covered by the holdings-only
diagnostic exemption**, and this scores returns; it should be treated with the same care as a
backtest even though it re-runs no strategy. (b) CSCV assumes the columns are alternative
configurations of one search; this repo's trials span several families, and pooling them would answer
a blurrier question than pooling one family's ladder. (c) It would be computed **on the validation
split**, i.e. it re-uses the split the gate already reads — it is not a second, independent look at
anything, and must not be presented as one.

**4. What this does not supply.** No mechanism, no strategy, no signal. It is machinery for grading
the search, and its only strategy-level implication is the one `program.md` already states — that
trials are costly. It also does **not** speak to the comparison of two candidates on the same
window; that is the sister note's subject, and the two corrections compose rather than substitute.

## Related

- `notes/2026-08-24-multiple-testing-haircut.md` — Harvey–Liu's haircut is the competing
  formalisation of the same problem, and the DSR authors explicitly frame the two as
  **complementary**: their `E[max{ŜR_n}]` and Harvey–Liu's Benjamini–Hochberg-derived threshold play
  the same role, and they recommend computing DSR against both. That note also carries the property
  the DSR framing lacks — that under an FDR-controlling procedure the bar does **not** rise without
  limit with the trial count.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the other inference problem: two
  candidates on one window, rather than one candidate against many trials.
- `notes/2026-08-23-statistics-of-sharpe-ratios.md` — Lo (2002), the source of the non-normality and
  short-sample corrections the PSR layer builds on.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the empirical counterpart: post-publication
  decay is what selection bias looks like measured after the fact.
- `experiments/learnings.md` — "the DSR multiple-testing bar effectively requires one large single-step
  jump", "clustering makes within-family tuning nearly free", and the effective-versus-recorded trial
  count. All three are local observations of the two mechanisms above; none is contradicted.
- **Index note.** The PBO companion resolves badly: OpenAlex returns `cited_by_count: 0` for
  `10.21314/jcf.2016.322` and Semantic Scholar does not resolve the DOI at all, while Crossref reports
  51 — a fifth instance of the folder's standing "disbelieve a lone low count" warning, here with a
  *zero* as the tell. Crossref's count is the one recorded.
