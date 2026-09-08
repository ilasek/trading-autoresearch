---
title: "Stacked Regressions" (with LeBlanc–Tibshirani, "Combining Estimates in Regression and Classification", as the corroborating source)
authors: Breiman; Le Blanc, Tibshirani
year: 1996 (both)
venue: Machine Learning 24(1), 49–64 (Tier 1 for the field, peer-reviewed); Journal of the American Statistical Association 91(436), 1641–1650 (Tier 1 statistics)
url: https://doi.org/10.1007/BF00117832 — LeBlanc–Tibshirani https://doi.org/10.1080/01621459.1996.10476733
citations: Breiman 923 (Crossref, DOI:10.1007/BF00117832, checked 2026-09-08) and 1414 (Semantic Scholar, same DOI, checked 2026-09-08). **Tenth instance of the standing "disbelieve a lone count" rule, and the first where the split is two DOIs rather than two indexes**: the identical article (Machine Learning 24, 49–64) carries a *second* Crossref registration, `10.1023/A:1018046112532`, with a further 464 (Crossref) / 452 (Semantic Scholar) — so any single lookup understates the paper by a third to a half. LeBlanc–Tibshirani 372 (Semantic Scholar, DOI:10.1080/01621459.1996.10476733, checked 2026-09-08) against 48 (Crossref, same DOI).
sample_period: n/a — no market data of any kind. Two standard benchmark datasets (Boston Housing, 506 cases; an ozone dataset, 330 cases) and simulations with 40 input variables and 60 cases, 250 iterations each.
markets: none (statistics / machine-learning methodology)
tier: A
validation_overlap: false
published_post_2018: false
---

Breiman read **in full** — the typeset *Machine Learning* article, served by the UC Berkeley
statistics department's own technical-report archive
(`statistics.berkeley.edu/sites/default/files/tech-reports/367.pdf`, which despite the
tech-report URL is the published 16-page article, journal header and all). `pypdf` extracted it
cleanly. LeBlanc–Tibshirani is **not read**; its one conclusion relied on below is quoted from
Breiman's own description of it in Section 1 of the article read here, and is flagged as such
where it appears.

This is the **last sub-mechanism `program.md` names with no note across the previous 79** —
`portfolio-learning`'s "stacking or meta-labelling over family leads". `SUMMARY.md`'s
2026-09-07 audit identified it and said it should be approached knowing the family has closed
four times. It is covered here in two halves: this note is *stacking*, the estimation of
combination weights; its companion `2026-09-08-meta-labeling-and-the-value-of-a-filter.md` is
*meta-labelling*, the second-stage filter.

## Mechanism

Stacking answers a question this lab has asked four times and never once answered with an
estimator: **given K predictors of the same target, how should they be weighted?** Every
aggregation operator the lab has run fixes the weights a priori (the equal-weight mean) or uses
none at all (the max, the intersection). Stacking estimates them, and the paper's entire
contribution is *how* — two constraints, each of which fixes a distinct failure.

**Failure 1: weights fitted on the same data that fitted the predictors.** If the `v_k` were
built on the learning set `L` and the weights `α_k` are chosen to minimise squared error over
`L`, the `α_k` overfit and generalisation is poor — mechanically, the combination just loads on
whichever `v_k` is most flexible, because that one already fits `L` best. The fix is Wolpert's:
build **level-one data**. Leave case `n` out, rebuild every predictor without it, and record
`z_kn = v_k^(−n)(x_n)`. The level-one data is `{(y_n, z_n)}` — each predictor's *held-out*
prediction for each case. Fit the weights on that.

**Failure 2: the predictors are strongly correlated, because they are all predicting the same
thing.** Least squares on level-one data is then unstable — the `α_k` swing on small data
changes. Breiman reports trying ridge and several variants on the weights: "Results were better
than using the least squares `{α_k}`, but were not consistent." What works consistently is
minimising level-one squared error **subject to `α_k ≥ 0`**, and nothing else. Non-negative
least squares stabilises the combination *and* sparsifies it. Breiman is explicit that no
general proof exists ("a general proof is not yet in place"); the evidence is Theorem 1 below,
two benchmark datasets and several thousand simulation runs. Breiman records that
LeBlanc–Tibshirani, working independently and trying other stacking methods, "come to the
conclusion that non-negativity constraints lead to the most accurate combinations" — this is
Breiman's characterisation of their paper, not a reading of it.

**Why non-negativity works, and this is the part that transfers.** Impose `α_k ≥ 0` *and*
`Σ α_k = 1`. Then for every `x`,

    min_k v_k(x)  ≤  v(x) = Σ α_k v_k(x)  ≤  max_k v_k(x)

— the combination is an **interpolating predictor**, and stacking is the search for the best
interpolator. That is a structural bound, derived in two lines, and it is the same bound this
lab has measured five separate times as "the gain is bounded by the components' disagreement".
Breiman then shows the simplex is doing less work than it looks: the sum-unconstrained
non-negative optimum comes out with `Σ α_k` **near** one anyway (0.7–0.9 for stacked subsets,
1.1–1.3 and 0.6–1.1 for stacked ridge), and constraining the sum changes the error hardly at all
— its main effect is that *more* models get non-zero weight.

## Construction recipe

1. Fix a pool of `K` predictors `v_1 … v_K` of one numerical target, all built by procedures
   you can re-run.
2. **Generate level-one data by held-out prediction.** Split the learning data into `J` folds;
   for each fold `j`, rebuild all `K` predictors on `L − L_j` and record their predictions on
   `L_j`. Stack those into an `N × K` matrix `Z` aligned with `y`.
3. **Fit `α` by non-negative least squares on `(y, Z)`** — `min_α Σ_n (y_n − Σ_k α_k z_kn)²`
   subject to `α_k ≥ 0`. Breiman uses the Lawson–Hanson NNLS algorithm. Do **not** add the
   `Σ α_k = 1` constraint; it is unnecessary and costs sparsity.
4. Rebuild the `K` predictors on all the data and combine them with the fitted `α`.
5. **Use `J`-fold, not leave-one-out.** Ten-fold level-one data gave *lower* model error than
   leave-one-out in all three correlation regimes tested, as well as being far cheaper — the
   only case in the paper where the cheaper choice is also the better one.

**Three quantitative regularities of the fitted `α`, all of which are predictions about what a
stack will look like before you build it.**

- **The stack is sparse.** Out of 40 candidate predictors, the average number receiving non-zero
  weight is **3.1** for stacked subset regressions (range 2.9–3.4 over 15 simulation designs),
  **1.6–2.3** for stacked ridge regressions, and **3.4** for the two pools stacked together. On
  the tree data, roughly 50 subtrees were available and on average **6.3–6.5** entered the stack.
  Non-negativity is doing model selection, not just weighting.
- **Gains come from *dissimilar* predictors.** Stacking subset regressions with ridge
  regressions beat both and beat "best of best" (cross-validate each family, take the better
  winner) uniformly and sometimes by a large margin. Stacking ridge regressions *alone* barely
  helped, and Breiman's stated reason is that ridge solutions at adjacent penalties are nearly
  the same function, whereas subset regressions change a lot between `k` and `k+1` variables.
  His conclusion: "stacking will reduce error when the predictors being stacked together are not
  overly similar."
- **Simple mixtures are not a substitute, but they are close.** Equal-weight mixtures of the
  5 or 10 best-CV models, and a mixture of everything within a fraction of the best CV error,
  were each "sometimes close to stacking, sometimes substantially worse", and stacking was
  uniformly best. For ridge pools the simple mixtures were *rarely* better than the single best.

**Theorem 1 — an exact condition for when combining cannot beat selecting.** Let
`R_ij = Σ_n (y_n − v_i(x_n))(y_n − v_j(x_n))` be the residual cross-product matrix and let `k`
index the best single predictor (`R_kk` minimal). Then the best single predictor is also the
best stacked predictor **if and only if `R_kk ≤ R_ik` for all `i`**. Writing `ρ_ik` for the
correlation between residual sets `i` and `k` and `σ_i` for their standard deviations, the
condition is

    ρ_ik  ≥  σ_k / σ_i     for every i.

In words: **selection is already optimal exactly when every rival with comparable error is
nearly the same function as the winner.** The proof is the Kuhn–Tucker conditions for the
quadratic program, so it is necessary *and* sufficient, not a bound. Note what the statistic is
— a correlation of *residuals*, not of predictions, and not of the predictors' own returns.

## Robustness evidence (qualitative only)

Peer-reviewed in a tier-1 venue for its field, and the seed of a very large downstream
literature (stacking is now a standard ensemble method and the direct ancestor of every "super
learner" construction). The two constraints have been independently arrived at: Breiman reports
LeBlanc–Tibshirani reaching the same non-negativity conclusion by a different route, and the
practice of building level-one data from held-out folds is universal in the descendant
literature. Theorem 1 is algebra and does not decay.

**The honest limits, and they are large for this lab's purposes.**

- **The objective is squared error, not Sharpe.** Every result above — the interpolation bound,
  Theorem 1, the sparsity — is derived for `min Σ (y − Σ α v)²`. Nothing in the paper licenses
  transferring the *numbers* to a ratio objective, and the residual-correlation condition in
  Theorem 1 is not the same object as a return-series correlation between two books.
- **The data are i.i.d. draws.** There is no time series anywhere in the paper. Its `J`-fold
  random cross-validation is exactly the leakage the lab's own causality check exists to catch,
  and the level-one data here would have to be generated walk-forward with the target's
  realisation horizon respected.
- **No costs, no constraints, no turnover.** A stack re-fits `α` as data accrue; the paper
  never counts what changing `α` would cost to trade.
- **Evidence is two datasets and one simulation design** — 40 variables, 60 cases, Gaussian
  inputs with an AR(1)-type correlation structure at `R = 0.7, 0, −0.7`, and Breiman's own
  warning attached: "the structure of the simulation may dictate the result", offered
  specifically about ridge-versus-subset comparisons.

## Implementability here

**What is genuinely new: the lab has never estimated a combination weight.** Its four
`portfolio-learning` closures are the equal-weight mean over stored return series (2026-08-30),
the max-of-rank and max-of-z over signals (2026-08-31), and the intersection (2026-09-06). None
of them fits `α`. Stacking is therefore a real untried operator and not a fifth restatement of
the same one — *and this source predicts, from outside, that it will not help here.* Three
independent reasons, in increasing force:

1. **The pool is Breiman's bad case.** His gains come from dissimilar predictors; his ridge pool,
   where adjacent members are near-identical, is the case where stacking barely beats selection.
   `learnings.md` records the eight leads correlating **0.68–0.98** on return series with two
   pairs at **0.98** ("an allocator over these allocates over one thing"). That is the ridge
   pool, not the subset-plus-ridge pool.
2. **Sparsity says the stack collapses.** With 40 candidates the average stack held 3.1 of them;
   with ~50 subtrees, 6.3. A pool of **eight** legs, most of them mutually correlated above 0.9,
   should be expected to produce a stack of one or two — i.e. selection, arrived at expensively.
3. **A fully-invested long-only book is *forced* onto the simplex, and that is the whole bound.**
   This is the note's central point for this repo and it is structural rather than empirical.
   Breiman's interpolation result says `α ≥ 0` **and** `Σ α = 1` implies the combination is
   bounded between its components pointwise. A capital mix over finished long-only books
   satisfies both constraints *by construction* — capital shares are non-negative and, if the
   book is fully invested, they sum to one. So the mean operator's bound is not a fact about
   averaging that the lab happened to measure; it is the simplex, and **no reweighting of
   finished books, learned or not, can escape it.** That includes hierarchical risk parity and
   every clustering allocator (`SUMMARY.md` #86 reaches the same verdict by a different route),
   and it is the same conclusion Novy-Marx's linear-composite equivalence reaches for signal
   blending.

**Which makes the interesting question the escape, and Breiman names both exits.**

- **Exit 1 — drop the linearity.** The max operator is not of the form `Σ α_k v_k`, so neither
  the interpolation bound nor Theorem 1 applies to it. The lab found this empirically
  (mean 0.635 against max-of-z 1.008 on one fixed leg set) and it now has a second derivation.
- **Exit 2 — drop `Σ α = 1`, which means letting the book hold cash.** Breiman's stacks
  routinely sum to 0.7–0.9, and he shows the sum constraint is not needed. The repo's
  constraint is *gross leverage ≤ 1.0*, not `= 1.0`, so a book that scales its total invested
  weight is admissible. **But this exit is not free and should not be read as an opening**: a
  book whose total weight varies over time is a market-timing bet, and the value of such a bet
  is priced exactly and unforgivingly by the companion note. The lab's `price-trend` record
  already refutes the regime-switching version of it. Recorded here as *the structurally
  available escape*, with the price attached, so that a future session does not rediscover the
  exit without the price.

**If a session does build a stack anyway**, the recipe adapted to this repo: level-one data
generated by `strategies/lib/walkforward.py`'s release rule, never by random folds; the `α`
fitted by `scipy.optimize.nnls` on out-of-fold *signal* values rather than on finished books, so
that the operator sits before portfolio construction and is not automatically on the simplex;
weights refit at a cadence slow enough that the turnover of refitting is visible; and the count
of non-zero `α` reported as a first-class result, because a stack of one is Theorem 1 telling you
the answer.

**The free screen this note contributes, which costs no trial and no holdout look.** Theorem 1
is directly computable and it *decides in advance* whether any fitted-weight combination can beat
the best single leg. Build the residual matrix over the leg pool with respect to whatever target
the legs are predicting (forward returns, on the train split), find the best single leg `k`, and
check `ρ_ik ≥ σ_k / σ_i` for every `i`. If it holds, selection is provably optimal and no
stacking, meta-labelling, HRP or learned combiner can improve on it — the answer is the incumbent
leg. If it fails for some `i`, that `i` names the one leg worth combining. See candidate #88.
Its stated limit is the objective mismatch above: it decides the squared-error question exactly,
and the Sharpe question only by analogy, so it is a kill switch rather than a green light.

## Related

- `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` — mix versus integration under a
  long-only constraint. Breiman's interpolation result is the general form of why the *mix* is
  bounded: the mix lives on the simplex.
- `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — Novy-Marx's exact equivalence
  between a linear composite and a portfolio of its legs, and the lab's mean/max boundary. Same
  conclusion from the portfolio side; this note supplies it from the estimation side, plus the
  necessary-and-sufficient condition for when the combination is degenerate.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — a clustering allocator
  is a capital mix over finished books and therefore an interpolating predictor; anti-candidate
  #86, now with a structural reason as well as a measured one.
- `notes/2026-08-19-bagging-averaging-unstable-predictors.md` — Breiman's *other* averaging
  result. Bagging averages one procedure over resamples; stacking weights different procedures
  on held-out data. The bagging note's variance/centre distinction is the right frame for reading
  the sparsity result here.
- `notes/2026-09-08-meta-labeling-and-the-value-of-a-filter.md` — the second half of the same
  `program.md` clause, and the price of Exit 2 above.
- `experiments/learnings.md`, 2026-08-30 and 2026-08-31 — the eight-leg ensemble table, the
  0.68–0.98 leg correlations, and the mean/max operator result this note re-derives structurally.
