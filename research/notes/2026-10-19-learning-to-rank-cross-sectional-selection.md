---
title: "Building Cross-Sectional Systematic Strategies By Learning to Rank" — replacing a pointwise return-regression loss with a pairwise or listwise ordinal loss, on exactly the select-the-top-K decision protocol v3 admits
authors: Poh, Lim, Zohren, Roberts (Oxford-Man Institute)
year: 2021
venue: The Journal of Financial Data Science 3(2) (venue tier 3 — a Portfolio Management Research practitioner-academic journal, peer-reviewed but not a tier-1 finance outlet; the authors are an academic quantitative-finance group)
url: https://doi.org/10.3905/jfds.2021.1.060 (read as arXiv:2012.07149v1, `arxiv.org/pdf/2012.07149`)
citations: 20 (Crossref `is-referenced-by-count` on the JFDS DOI, checked 2026-10-19); 29 (Semantic Scholar by the same DOI, same date). A modest but real count for a four-year-old methods paper; the authors' two follow-ups (JFDS 2022 currency version, `10.3905/jfds.2022.1.099`; Journal of Systematic Investing 2023 transfer-ranking version, `10.52354/jsi.3.1.ii`) carry 8 and 0.
sample_period: 1980–2019 (NYSE common stocks, CRSP share codes 10 and 11, priced above $1, with a full prior year of trading)
markets: US (NYSE) single market, monthly rebalance, daily closing prices only
tier: B− — the construction is fully specified and the idea is theoretically grounded in a mature information-retrieval literature, but: single market, single asset class, **transaction costs are explicitly not modelled**, no multiple-testing treatment, no independent replication, long–short framing, and the ranking-accuracy gains that the headline return gains are attributed to are near zero in absolute terms (see Robustness).
validation_overlap: **true** — the out-of-sample window runs to 2019 and therefore overlaps this lab's 2018–2023 validation split by two years.
published_post_2018: true
read: full text of arXiv:2012.07149v1 (13 Dec 2020), `pdftotext -layout` → 70 KB of clean text, 273 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified. Includes Exhibits 1–6 and the Appendix (the LTR-to-momentum mapping and the full hyperparameter grids). The typeset JFDS version is closed — `pm-research.com` refuses an automated client by redirecting into an OpenID authorization flow [`research/README.md` 2026-09-08] — and was **not** read; nothing below depends on text the preprint does not carry, but the preprint is v1 and may differ from the published article.
---

## Mechanism

No economic mechanism, and the paper claims none: the predictors are the ordinary price-trend
signals this lab has already measured to exhaustion. The claim is entirely about the **objective
function**, and it is the applied counterpart of
`2026-10-19-consistent-scoring-functions-and-elicitability.md`.

The argument in the authors' own framing: a cross-sectional strategy is a four-step pipeline — score
every name, **rank** the scores, **select** a fraction of the ranking, then weight. Steps 2 and 3
consume an *ordering* and nothing else; the magnitude of a score is discarded by the sort. But the
contemporary "regress-then-rank" design trains its scoring model by minimising **mean squared error
against realised (volatility-normalised) forward returns** — a pointwise loss, consistent for the
conditional mean, which spends its capacity getting the *level* right for every name including the
~80% in the middle that will never be selected. The paper's phrasing: such models "do not explicitly
consider the expected ordering of returns — which is at the core of the design of cross-sectional
strategies."

Information retrieval solved this problem thirty years ago, because a search engine has the same
shape: a query, a list of candidates, a decision that only uses the top of the ordering. The
**Learning to Rank (LTR)** literature's answer is to replace the pointwise loss with one of two
families:

- **Pairwise** — model the probability that name `i` outranks name `j`, and minimise cross-entropy
  over pairs. Learns relative structure directly. Cost scales **quadratically** in the number of
  names per rebalance.
- **Listwise** — treat the whole cross-section at a date as one training example, form a probability
  distribution over permutations (or a softmax "top-one" distribution over the list), and minimise
  cross-entropy or a likelihood loss against the realised ordering. Cost scales **linearly** in the
  number of names.

The mechanism by which this is supposed to pay is stated and then tested: **better ordering → the
names that actually belong in the top bucket are more often placed there → a steeper spread between
the extreme buckets.** The paper's own validation of the mechanism is the decile table (below),
which is the part that matters for a long-only lab.

## Construction recipe

The mapping from information retrieval to a cross-sectional strategy is the transferable part, and
it is three lines:

- a **query** ≡ a rebalance date;
- a **document** ≡ an eligible instrument at that date;
- a document's **relevance grade** ≡ the instrument's realised **decile** of forward return at the
  *next* rebalance (10 ordered grades `D₁ ≺ … ≺ D₁₀`).

So the training target is **not a return**. It is a within-date, cross-sectionally ranked, discretised
grade. This is the single most important construction choice in the paper and the one that is free to
copy.

**Pipeline as specified.**

1. *Features.* Price-only, three groups: (i) raw cumulative returns over 3, 6 and 12 months
   (Jegadeesh–Titman); (ii) the same returns standardised by daily volatility and rescaled to the
   horizon; (iii) **16** volatility-normalised MACD features in the Baz et al. form — the composite
   signal `Σₖ φ(Ỹ(Sₖ, Lₖ))` with short/long half-life pairs `Sₖ ∈ {8, 16, 32}`,
   `Lₖ ∈ {24, 48, 96}`, where each intermediate indicator is
   `MACD/std(p_{τ−63:τ})` further divided by `std(z_{τ−252:τ})`, plus the raw intermediate signals
   computed at the date and at 1, 3, 6 and 12 months back.
2. *Label.* Next-rebalance forward-return decile. For training and validation the forward horizon is
   set to **21 days** rather than the exact next month, which the authors flag as a practical
   convenience; it is a small target/rebalance mismatch worth not inheriting silently.
3. *Model.* Four LTR algorithms are specified: **RankNet** (pairwise, neural, cross-entropy over
   pairs, `O(N²)`); **LambdaMART** (pairwise, boosted trees, trained on λ-gradients — the product of
   a pairwise cross-entropy and the gain in NDCG, which sidesteps NDCG's flat, discontinuous,
   non-differentiable surface; implemented as XGBoost with `objective='rank:pairwise'`,
   `eval_metric='ndcg'`); **ListNet** (listwise, softmax "top-one" cross-entropy, `O(N)`);
   **ListMLE** (listwise, likelihood loss — continuous, differentiable, convex, linear complexity).
   Benchmarks: a **random** selector, the two heuristics (raw returns; volatility-normalised MACD),
   and an **MLP** trained on MSE as the regress-then-rank representative.
4. *Selection and weighting.* Fixed count — the top 100 and bottom 100 names at every rebalance
   (≈10% of the tradeable universe), monthly, *"to avoid excessive transaction costs that comes with
   trading at higher frequencies"*. Weighting is `σ_tgt/σ_i` per name, with `σ_i` an exponentially
   weighted standard deviation of daily returns with a **63-day span**, and `σ_tgt` annualised at
   15%; a second volatility scaling is applied at portfolio level for comparability.
5. *Refit schedule.* Models are **re-tuned at 5-year intervals**, then weights and hyperparameters
   are frozen and used out-of-sample for the following five years. Within a training block, 90/10
   train/validation split, Adam, up to 100 epochs, **early stopping** after 25 epochs without
   validation improvement, dropout as a tuned hyperparameter, and **50 iterations of HyperOpt** over
   the grids in the appendix (dropout ∈ {0,…,0.8}, hidden width ∈ {64,…,2048}, learning rate across
   seven orders of magnitude, minibatch size, and for LambdaMART `eta`, `num_boost_round ∈ {5,…,320}`,
   `max_depth ∈ {2,…,10}`).
6. *Evaluation.* Two metric families, and the paper's methodological contribution is insisting on
   both: finance metrics (expected return, volatility, max drawdown, downside deviation, Sharpe,
   Sortino, Calmar, hit rate, average profit/average loss) **and** ranking metrics — **Kendall's
   tau** over the whole list and **NDCG@100** at the cutoff equal to the portfolio size, computed
   separately for longs and (with reversed relevance) shorts.

## Robustness evidence (qualitative only)

- **The direction of the result is uniform and the ordering within it is not.** Every LTR model beats
  every benchmark on every profitability, risk and risk-adjusted measure reported, and the *worst*
  ranker beats the *best* benchmark on each. But **listwise does not beat pairwise** — the best model
  overall is a pairwise one — which the authors attribute to the poor signal-to-noise ratio of
  financial data compounded by sample size: listwise methods see `12·N_avg` training examples per
  year where pairwise methods see `12·N_avg²`. The honest reading is that the pairwise/listwise
  choice is unresolved and should not be treated as settled by this paper.
- **The MSE-trained net is the weakest non-random model, and that is the finding with the most
  structural content.** The MLP lands only marginally above random selection on the finance metrics
  and *below* both price heuristics; the authors put this down to overfitting on limited noisy data
  plus "the sub-optimality of the regress-then-rank approach", and note that the MLP's scores are
  forecasts of monthly returns, "which is regarded as a challenging problem" and more so when only
  price data is available. So: **a flexible learner trained on the wrong functional can underperform
  a one-line heuristic**, which is the same conclusion the no-arbitrage paper reaches by a different
  route (`2026-10-19-no-arbitrage-criterion-as-the-learning-objective.md`).
- **The long-only decile table is reported, and the gain is not confined to the short leg.** Equal-
  weighted deciles are formed on each model's own score and scaled to the volatility target. The
  random selector's decile Sharpes are **flat and non-monotone**, as they must be. The raw-return
  heuristic's rise monotonically. The MSE-trained MLP's are **nearly flat and non-monotone at the
  top** — deciles 8, 9 and 10 are not ordered. The rank-loss models' rise **steeply and monotonically
  across all ten**, and the improvement is visible in the **top decile taken alone**, not only in the
  top-minus-bottom spread. For a long-only lab this is the single most relevant piece of evidence in
  the paper, and it is the one the authors treat as confirming their mechanism.
- **The ranking-accuracy gains are tiny in absolute terms, and this is the paper's weakest seam.**
  Kendall's tau is zero for random selection and rises only to the low hundredths for the best
  ranker; NDCG@100 moves by a couple of points off the random baseline. The authors read this as
  confirmation (ranking quality improved, performance improved with it). A sceptic reads the same two
  columns as a near-zero rank correlation being asked to carry a large performance difference, which
  is a lot of leverage on a small statistic — the same scepticism the folder applies to a sort whose
  post-formation loadings collapse relative to its pre-formation ones [`SUMMARY.md` 2026-10-18]. Do
  not import any magnitude expectation from this paper. Import the construction.
- **Costs are explicitly excluded.** "All returns in this section are computed without transaction
  costs to focus on the raw predictive ability of the models." Turnover is never reported — not for
  the rankers, not for the heuristics, not in the decile tables. Since the rankers reorder the book
  more aggressively than a 12-month heuristic does, **the untested quantity is exactly the one that
  decides the question under protocol v3.**
- **Replication status: none.** No independent replication exists. The authors' own follow-ups extend
  the method to currencies and to a data-scarce transfer-learning setting rather than re-testing the
  equity result. Multiple testing is not addressed, and the search budget is large (50 HyperOpt
  iterations × 4 models × 8 refits), which the deflated-skill bar in this lab would charge for.
- **Survivorship and universe.** NYSE common stocks with a $1 price screen and a full prior year of
  trading. That is a large-cap-tilted, listing-screened panel — closer to this lab's nine-index pool
  than a full CRSP cross-section would be, which is mildly favourable for transfer.

## Implementability here

**The licensed change is a label and a loss, not a model class.** Everything the paper's architecture
section describes is out of reach or inadvisable here; everything its *problem formulation* describes
is free.

1. **What transfers for nothing: the target.** Replace a forward-return regression target with the
   name's **within-date, within-region decile of forward return**. On this panel the within-*region*
   qualification is not optional: v3's null replaces each entered name with one of the same type and,
   for stocks, the same listing region [`learnings.md` 2026-10-13/14], so a grade computed against
   the whole pool encodes a region mix the null matches move for move, and the folder has watched
   that mechanism erase an apparent signal already (average peer correlation reading strongly negative
   pool-wide and null region-matched, `learnings.md` 2026-10-14/15). **Grade within region, or the
   ordering being learned is partly the geography.**
2. **What transfers cheaply: a pairwise loss without a neural network.** RankNet's loss is the
   cross-entropy of a logistic model on the *difference* of two names' feature vectors. Fitted
   linearly, that is **a logistic regression on within-date, within-region pairwise feature
   differences** — deterministic, single-threaded, convex, one regularisation parameter, no hidden
   width and no dropout to search, and it satisfies `program.md`'s "prefer few features and a
   penalised linear model first" exactly. The `O(N²)` pair count at ~1,000 eligible names is ~500k
   pairs per date, which is the one thing to measure before writing the candidate: `program.md`
   budgets ~60 s per `generate_weights` call and the protocol makes about seven calls per trial, so
   **subsample pairs per date (or restrict to pairs spanning a grade gap) and time one call first.**
   A listwise softmax loss is `O(N)` and cheaper still, but needs a hand-written gradient step; the
   pairwise-logistic route uses only what is installed.
3. **What does not transfer.** LambdaMART is XGBoost, which `program.md` does not list among the
   available libraries (scikit-learn and scipy), and scikit-learn exposes no pairwise or listwise
   ranking objective. Do not plan around NDCG-gradient boosting here. The neural variants are
   additionally ruled out on the determinism requirement — the causality check compares holdings at
   `1e-6` and treats non-determinism as a peek — and on the 5-yearly-refit-with-50-HyperOpt-iterations
   schedule, which is a search budget the deflated bar would charge for in full.
4. **The free screen to run before spending a trial, and it costs nothing.** The lab already has the
   feature panels and the realised forward returns. Fit the pairwise-logistic ranker walk-forward and
   compare its **within-region rank IC** against the rank IC of the same features scored by (a) the
   raw heuristic and (b) an MSE-fitted penalised linear model on the same features. The paper's
   prediction is that the ranker's rank IC exceeds both while remaining small in absolute terms. If
   it does not — if the three rank ICs are indistinguishable on this panel — the whole family is
   closed for the price of a diagnostic, and that is a result worth recording either way. If it does,
   **pre-register the second question before looking: does the rank-IC gain survive the turnover the
   reordering costs?** The paper never asks it, v3 charges per-name liquidity tiers plus UK/HK/FR/IT/ES
   transaction taxes and charges the trades that undo drift, and `SUMMARY.md` #18's short-horizon cost
   wall has already killed one lead-lag object on exactly this ground [`learnings.md` 2026-09-25].
5. **Family and budget.** This belongs in `statistical-learning`, not `price-trend`. That matters
   under `program.md`'s allocation rule, and it matters substantively: the *features* here are the
   momentum lineage the lab has measured to a null, so **a ranker on momentum features is a refinement
   of a null, in the exact sense in which residual momentum was found to be one** (rank-correlated
   +0.903 to raw 12-1 momentum, `learnings.md` 2026-10-14/15). The honest version of this candidate
   puts the ordinal loss over a score from a family with a *live* lead, or over a feature set that is
   not the trend block, and reports its correlation to the incumbent's momentum score as a
   pre-condition rather than an afterthought.

**Pitfalls.** (a) The 21-day training target against a month-end rebalance grid is a mismatch; use the
actual next-rebalance horizon. (b) Deciles are formed on realised forward returns, so every label is
by construction unavailable until the horizon closes — `strategies/lib/walkforward.py` exists for
precisely this bookkeeping and a training row must not be released before its target was realised.
(c) The paper's selection rule is a fixed count of 100 names; the lab's own measurement is that a
fraction-of-the-cross-section rule means different things in different eras of a universe that grows
from ~139 to ~906 eligible names [`learnings.md` 2026-09-25], so **fix the count, cap it at the
eligible count, and do not skip thin dates.** (d) Nothing here licenses an expectation about
magnitude: the paper's headline gain is gross, single-market, and rests on a rank statistic that is
near zero in absolute terms.

## Related

- `2026-10-19-consistent-scoring-functions-and-elicitability.md` — the theory this paper is an
  instance of. An ordinal loss over graded labels is a consistent scoring function for a different
  functional than the conditional mean; Gneiting is why that sentence is precise rather than a
  preference.
- `2026-10-19-no-arbitrage-criterion-as-the-learning-objective.md` — the third member of the chain,
  and the one that reaches the same "a flexible learner on the wrong objective loses to a simple
  model on the right one" conclusion from the asset-pricing side.
- `2026-08-29-machine-learning-cross-section-comparative.md` — the reference comparative study, every
  model in which minimises a pointwise loss. Read together: GKX settles *which estimator* given the
  MSE objective; this paper argues the objective was the wrong one to hold fixed.
- `2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md` — what the decile/grade
  transform throws away, and when it is safe.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` and
  `2026-09-06-number-of-portfolios-as-tuning-parameter.md` — the decile table is this paper's
  evidence, and these two notes are how to read one without deceiving yourself; ten grades is a
  tuning parameter the paper never varies.
- `2026-10-15-random-portfolios-as-the-null-of-no-skill.md` — the paper includes a *random* selector
  as its floor benchmark and reports its decile table as flat. That is the lab's own v3 null arriving
  independently in a practitioner paper, and it is the strongest external corroboration the folder
  holds for the gate's design.
- `2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` — the 90/10 within-block split
  and early stopping here are exactly the setting those cautions are about.
- `experiments/learnings.md` 2026-10-14/15 (momentum lineage priced to a null; residual momentum as a
  refinement of a null) — the tension to state out loud: this paper's demonstration case is the one
  feature block this lab has already closed.
