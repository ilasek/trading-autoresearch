---
title: "Mean-Variance Spanning"
authors: Huberman, Kandel
year: 1987
venue: Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.1987.tb03917.x
citations: 605 (Semantic Scholar by DOI, checked 2026-09-23); Crossref 286 for the same DOI (checked 2026-09-23). OpenAlex not consulted — the day's free budget was exhausted (HTTP 429, "Insufficient budget"). Read in full from `people.umass.edu/kazemi/871/HubermanKandel.pdf`, a JSTOR scan of the version of record with a readable text layer.
sample_period: 1964–1983 (the empirical illustration only; the paper's content is a theorem and an exact-distribution result)
markets: NYSE monthly returns, thirty-three size-sorted equal-weighted portfolios against three size-based indices
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is not a strategy source and it predicts no returns. It is the source that defines the
question this lab has been asking in a different vocabulary for sixteen sessions: **given a
book you already hold, is a new return stream worth holding *at all*?**

Huberman and Kandel separate two distinct versions of that question, and the separation is the
contribution.

Let `R` be a `K`-vector of returns on the assets you already hold (here: the champion, so
`K = 1`) and `r` an `N`-vector of returns on the candidates (here: one new leg, so `N = 1`).
Assume the linear model

```
r = a + B R + e,        E[e] = 0,   Cov(e, R) = 0
```

which is nothing more than the OLS regression of the candidate's return series on the
incumbent's.

1. **Intersection** — the two minimum-variance frontiers touch at *one* point. This is the
   statement that *a particular investor*, with one particular risk aversion, cannot improve.
   Proposition 1: intersection holds if and only if there exists a scalar `w₀` with

   ```
   a = w₀ (i_N − B i_K)
   ```

   If a risk-free asset exists and the frontiers touch on the line through it, `w₀` is the
   risk-free rate, and in excess-return form the condition collapses to `a = 0` — i.e. the
   candidate has zero Jensen alpha against the incumbent.

2. **Spanning** — the two frontiers *coincide*, so no investor of any risk aversion can
   improve. Proposition 3: spanning holds if and only if

   ```
   a = 0_N        (the tangency condition)
   B i_K = i_N    (the global-minimum-variance condition)
   ```

The second condition is the one an alpha test alone does not see. Write `δ = i_N − B i_K`.
`a = 0` says the candidate adds nothing to the *mean* side of the frontier; `δ = 0` says it
adds nothing to the *variance* side. A leg can be worth holding through either channel, and
the two are tested by different restrictions on the same regression.

The economic reading of why the pair is necessary and sufficient: if both hold, then for every
candidate (or portfolio of candidates) there is a portfolio of the incumbent assets with the
*same* mean (because `a = 0` and `B i_K = i_N`) and *strictly lower* variance (because `e` is
uncorrelated with `R` and `Var[e]` is positive definite). The candidate is dominated, so no
frontier portfolio holds any of it.

Spanning is also the exact-arbitrage-pricing and `K`-fund-separation condition: under the linear
model, spanning of `r` by `R` implies `K`-fund separation, and intersection with a risk-free
asset is the exact-APT restriction. That is why the same algebra appears in the asset-pricing
literature and in the "is this fund/market/factor worth adding" literature.

## Construction recipe

The whole test is one multivariate regression and a determinant ratio.

1. Choose the **benchmark set** `R`: the returns of the book you already hold. For a one-book
   lab this is a single series, `K = 1`.
2. Choose the **test set** `r`: the returns of the candidate(s), `N` of them.
3. Run `r_t = a + B R_t + e_t` over `T` observations by OLS. Let `Σ̂` be the unconstrained
   residual covariance and `Σ̃` the residual covariance estimated under the two restrictions.
4. `U = |Σ̂| / |Σ̃|`. The likelihood-ratio statistic is `−T ln U`, asymptotically `χ²_{2N}`.
   The constrained estimation never has to be run: `Σ̃ − Σ̂ = Θ̂' Ĝ⁻¹ Θ̂` with `Θ = [a, δ]'`,
   so `1/U` follows from the unconstrained fit alone.
5. **The exact small-sample distribution is available** — this is the paper's practical selling
   point over an asymptotic `χ²`. Huberman and Kandel give the exact null distribution of the
   likelihood ratio under conditional normality of `r` given `R`. (Note that only the
   *conditional* distribution must be normal; the benchmark's own distribution may be anything,
   including time-varying.)

Two construction choices the paper makes explicit and that carry over:

- **The regression is on raw or excess returns, either works**, but the two restrictions mean
  different things in each case; the `a = 0` half is the familiar Jensen alpha only in excess
  form.
- **`a` and `B` are assumed constant over the estimation window.** The paper tests that
  assumption rather than asserting it (its Subsection B is a temporal-constancy test of the
  regression coefficients), which is the right habit: a spanning verdict is only as good as
  the stability of the beta it conditions on.

## Robustness evidence (qualitative only)

- The result is a **theorem**, not an empirical regularity, so "replication" means the algebra
  has been re-derived and extended rather than re-measured. It has been, repeatedly and by
  independent groups: the regression characterisation is the starting point of every later
  spanning paper, including the two other notes filed tonight.
- The framework has been generalised in directions that all preserve the two-restriction
  structure: to GMM without the normality assumption, to stochastic-discount-factor /
  volatility-bound form (a frontier shift is equivalent to a shift in the Hansen–Jagannathan
  volatility bound), to conditional versions, to non-mean-variance utility, and to the presence
  of market frictions (tonight's de Roon–Nijman–Werker note).
- **Known limitation, and it is not small**: the test asks whether the *ex ante* frontiers
  coincide, but is run on *ex post* sample moments. Everything about its behaviour — size,
  power, and whether a rejection means anything economically — depends on estimation error in
  `μ̂` and `V̂`, which the 1987 paper does not analyse. That is exactly the gap tonight's
  Kan–Zhou note fills, and the answer there is unfavourable to the channel this lab cares about.
- In the authors' own illustration, a coarse three-index summary of a cross-section did **not**
  span the finer sort it was drawn from — recorded here only as a demonstration that the test
  can reject, not as a claim about any strategy.

## Implementability here

**Directly implementable, free, and it is a different hypothesis from the one the gate tests.**
That last clause is the point of this note and it must not be skipped.

- `K = 1` (the champion's daily net return series, already stored), `N = 1` (a candidate's).
  One OLS regression on stored series. No trial, no new data, no holdout.
- **What it answers**: *should an unconstrained mean-variance investor who already holds the
  champion hold any of this leg at all?* The `a` half is the tangency channel; the `δ` half is
  the variance channel.
- **What it does not answer**: whether a *specific fixed-weight* blend of champion and leg has
  a higher Sharpe ratio than the champion. That is the lab's actual gate, and Memmel's paired
  standard error is the right statistic for it. The spanning test is not a repair of the blend
  board and must not be read as licensing a promotion the gate declines.
- The distinction is worth stating in one line because the lab is about to be tempted by it:
  **the gate compares two specific books at a weight fixed in advance; the spanning test
  compares two *frontiers* at whatever weight is optimal.** A leg can be spanning-rejected (the
  optimal book holds some of it) and still fail the gate (the honest, pre-registered weight
  does not beat the incumbent by a resolvable margin). Both statements can be true at once and
  the lab has already measured the second.
- **Intersection is the cheaper and more targeted of the two hypotheses for a lab with one
  objective.** Spanning asks about every risk aversion; intersection asks about one. If the
  lab ever wants "does this help *me*, at *my* operating point", the one-restriction
  intersection test at the relevant `w₀` is the test, and it has one degree of freedom rather
  than two.
- **Pitfall — the constancy assumption is load-bearing.** `a` and `B` are assumed constant over
  the whole window. The champion is a trend book whose beta to any candidate will move with the
  cross-sectional regime; a spanning verdict computed over a full train split is an average
  over those regimes. Run the paper's own temporal-constancy check before believing a borderline
  verdict, or split the window and report both.
- **Pitfall — this is a test on *realised* return series, so it inherits every bias in them.**
  If both the champion's and the candidate's returns are lifted by the survivorship artifact
  `learnings.md` documents, spanning is tested between two contaminated series and the verdict
  is about the contaminated frontier. The test is a statistic, not a cleansing operation.

## Related

- **`research/notes/2026-09-23-spanning-test-power-and-step-down.md`** — Kan and Zhou's power
  analysis of exactly this test. Read it before running it: it shows the `a` channel is the one
  this framework has almost no power to detect, and the `δ` channel the one it detects easily.
- **`research/notes/2026-09-23-spanning-under-short-sales-and-costs.md`** — de Roon, Nijman and
  Werker replace the two equalities with inequalities when the investor cannot short, which is
  this lab's case.
- **`research/notes/2026-08-24-testing-differences-of-sharpe-ratios.md`** — the *other* way to
  ask "is the new book better", and the one the lab's gate actually uses. Jobson–Korkie/Memmel
  and Ledoit–Wolf test a difference of Sharpe ratios between two given books; Huberman–Kandel
  test whether one book's frontier already contains the other. Different nulls; do not
  substitute one for the other.
- **`research/notes/2026-08-21-effective-number-of-bets-diversification-measurement.md`** — the
  folder's other frontier-geometry note. The `δ = 0` restriction is a statement about the global
  minimum-variance portfolio, which is the same object the effective-number-of-bets literature
  decomposes.
- **`experiments/learnings.md` [2026-09-15]** records that removing the market from the
  correlation input to the required-gain table "changes what the number describes and not one
  dollar of what the book earns", and that raw `ρ` is the correct input there. **That entry is
  correct and this note does not reopen it.** The spanning regression's residual is not being
  substituted into Memmel's formula; it is the object of a different null.
