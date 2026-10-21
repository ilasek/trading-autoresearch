---
title: "Economic Predictions with Big Data: The Illusion of Sparsity" — inclusion probability and shrinkage are substitutes, so a method that can only select will manufacture sparsity as a variance-reduction device; and on the cross-section of stock returns the data cannot tell a sparse model from a dense one at all
authors: Giannone, Lenza, Primiceri
year: 2021
venue: Econometrica 89(5), 2409–2437 (venue tier 1 — one of economics' top five). Full text read from the working-paper version, Federal Reserve Bank of New York Staff Report No. 847, April 2018.
url: https://doi.org/10.3982/ECTA17842
citations: 169 (Crossref `is-referenced-by-count`, checked 2026-10-21); 176 (OpenAlex, same date). **Semantic Scholar's DOI endpoint returned `Paper with id DOI:10.3982/ECTA17842 not found`** for a real, published Econometrica DOI — the already-recorded `not found`-for-a-real-DOI mode, so OpenAlex was spent as the documented fallback.
sample_period: six datasets, the latest ending 2015 — macro 1960-02 to 2014-12; cross-country growth 1960–1985; equity premium 1948–2015 (annual); cross-section of US stock returns 1963-07 to 2015-06; US state crime 1986–1997; judicial circuits 1975–2008
markets: US (macro, equity premium, cross-section of stock returns, crime, judicial) plus a 90-country growth cross-section
tier: A
validation_overlap: false
published_post_2018: true
read: full text of `newyorkfed.org/medialibrary/media/research/staff_reports/sr847.pdf` (1.7 MB → 73 KB of clean text via `pdftotext -layout`, 432 instances of `" the "`, no ASCII shift, title and author lines verified against the Crossref record for the published DOI). **This is the April 2018 working paper, not the 2021 Econometrica article**, and the distinction is flagged rather than glossed: the published version may differ, and every claim below is attributed to the working paper's own text. The published abstract's three claims — posterior does not concentrate on a single sparse or dense model, concentrates on a wide set, and clear sparsity emerges only when very-low-dimension models are strongly favoured a priori — are the working paper's claims verbatim, which is the check that the argument carried through.
---

## Mechanism

No economic mechanism — and that absence is the paper's opening argument: *"In economics, there is no
theoretical argument suggesting that predictive models should in general include only a handful of
predictors. As a consequence, the use of sparse model representations can be justified only when
supported by strong statistical evidence."* This is the note that asks whether tonight's other three
— a marginal screen, a stability wrapper, an FDR filter — are answering a well-posed question.

The methodological move is to stop treating selection and shrinkage as rival philosophies and nest
them in one prior, then **let the data say which it wants**. For `y_t = u_t'φ + x_t'β + ε_t` with
standardised predictors, put a **spike-and-slab** prior on each `β_i`:

    β_i | σ², γ², q  ~  N(0, σ²γ²) with probability q,   and  exactly 0 with probability 1 − q

so that `q` is the **probability of inclusion** (how dense the model is) and `γ²` governs **how much
the included coefficients are shrunk**. Both are treated as unknown hyperparameters with their own
posteriors — that is the whole design, because the question *is* about `q` and `γ²`.

The nesting is what makes the result interpretable, and the paper spells it out: **`q = 1` is Bayesian
ridge** (a dense model, also readable as a regression on principal components with less shrinkage on
the leading ones); replacing the Bernoulli with an exponential, shifted exponential, half-Cauchy or
transformed truncated-Gamma gives the **Bayesian lasso, lava, horseshoe and elastic net** respectively
— and the paper's sharpest technical remark is that **none of those four alternative priors admits a
truly sparse representation with positive probability.** They shrink; they do not select. Only the
spike-and-slab puts mass on exact zeros, which is why it is the right instrument for the question.

The hyperprior is chosen to be agnostic between the two devices. Define
`R²(γ², q) = qkγ²v̄_x / (qkγ²v̄_x + 1)`, the share of `y`'s variance attributable to the predictors,
and put independent `Beta` priors on `q` and on `R²` (uniform, `a = b = A = B = 1`, in the baseline).
This implies a **negative prior correlation between `q` and `γ²`** — "thus agnostic about whether the
curse of dimensionality should be dealt with variable selection or shrinkage."

## Construction recipe

This is not a trading recipe; it is a **diagnostic recipe**, and that is how to use it.

1. Standardise predictors to unit variance. Keep whatever regressors must always be in the model
   (`u_t`) out of the selection.
2. Spike-and-slab prior as above; flat priors on `σ²` and on the always-included coefficients;
   `q ~ Beta(a, b)` and `R² ~ Beta(A, B)`, uniform in the baseline.
3. Sample the posterior over `(φ, β, σ², R², z, q)` with a latent inclusion indicator `z_i ∈ {0,1}`
   per predictor (the paper's Appendix A gives the full conditional structure).
4. Read off three things, in this order:
   - the **joint posterior of `(q, log γ)`** — its shape tells you whether selection and shrinkage are
     being traded off;
   - the **marginal posterior of `q`** — and note the paper's key identity: *under a flat prior on `q`,
     its posterior is proportional to the likelihood*, which factorises into a product of one-step
     predictive scores. So `p(q | y)` **is** an out-of-sample predictive-accuracy curve over model
     size, and "the choice of models with high `p(q|y)` can be interpreted as a model selection
     strategy based on cross validation." Reading the posterior of `q` is reading a cross-validation
     curve, for free, with no fold design.
   - the **per-predictor posterior inclusion probabilities** — the heat map, which is the only one of
     the three that can reveal an actual sparsity *pattern*.
5. Re-run with a **dogmatic sparse hyperprior** as the stress test: `q ~ Beta(1, k)`, which makes the
   number of included predictors approximately exponential (about 5% prior probability on more than
   three predictors, under 1% on five or more). If sparsity patterns appear only under this prior,
   they are the prior's and not the data's.

Step 5 is the paper's identifying test and the thing to copy.

## Robustness evidence (qualitative only)

**Findings, qualitatively, as the anti-lookahead rules require. No performance figure below is tied
to a date; the magnitudes quoted are identification statements about likelihood curvature, not
returns.**

**(1) Inclusion probability and shrinkage are substitutes, and the posterior says so much more
sharply than the prior.** Across all six applications the posterior of `(q, log γ)` is far more
concentrated than the prior and exhibits "an even sharper negative correlation": larger models need
more shrinkage to fit, smaller models need less. The consequence the paper draws is the one to carry:
**"dense modeling approaches might overstate the degree of shrinkage needed to achieve good fit.
Similarly, variable selection techniques that do not explicitly allow for shrinkage might
artificially recover sparse model representations simply as a device to reduce estimation error."**
A selection method with no shrinkage knob will report sparsity it did not find.

**(2) The posterior of `q` differs completely across problems — and one of the six is the cross-section
of stock returns.** Of the six, only the state-level crime application has posterior mass concentrated
on genuinely low `q`. The cross-country growth and the equity-premium applications sit at high `q`
(for the equity premium the posterior "deviates little from its uniform prior", i.e. the data say
almost nothing about model size). The macro, **cross-sectional stock returns** and judicial
applications are intermediate, with the posterior peaking at an interior point.

**(3) An interior `q` is not a sparse model — this is the title's claim and the paper's main result.**
In five of the six applications "none of the predictors appear to be systematically excluded." An
interior posterior mode for `q` does *not* mean a specific subset of that size is the right one: it
means a lot of uncertainty about *which* predictors belong, resolved differently in different
posterior draws. The paper attributes this to "a substantial degree of collinearity among many
predictors that carry similar information, hence complicating the task of structure discovery", and
concludes: **"model uncertainty is pervasive and the best prediction is obtained as a weighted average
of several models, each including between 20 and 50 regressors, but not necessarily the same ones
across models."** This is offered as the explanation for why Bayesian model averaging works
empirically where selection does not.

**(4) The cross-sectional-stock-returns application is the most extreme case in the paper, in two
independent ways, and both matter here.** Its predictors are built in the spirit of a nonparametric
characteristic sort — 36 lagged firm/stock characteristics, each turned into four dummies for
membership of the 1st, 2nd, 4th and 5th within-month quintile (the 3rd dropped for collinearity),
giving 144 regressors on a large panel. First, its **log-predictive-score curve over `q` is flat to
the order of `10⁻⁶` per observation across the entire range `q ∈ [0, 1]`** — two to four orders of
magnitude flatter than any other application in the paper. The data cannot distinguish a one-predictor
model from a 144-predictor one. Second, and more striking, it is the **one application in which even
the dogmatic sparse hyperprior fails to produce sparsity**: under `q ~ Beta(1, k)` all six
applications show clearer sparsity patterns "with the exception of finance 2, in which systematically
excluded regressors are still rare." **In the cross-section of equity returns, sparsity could not be
induced even by a prior that assigned under 1% probability to models with five or more predictors.**

**(5) The paper's own summary of its limits.** *"Economic data do not appear informative enough to
uniquely identify the relevant predictors when a large pool of variables is available … predictive
model uncertainty seems too pervasive to be treated as statistically negligible. The right approach
to scientific reporting is thus to assess and fully convey this uncertainty, rather than understating
it through the use of dogmatic (prior) assumptions favoring low dimensional models."*

**Replication and sample robustness, stated honestly.** Replication in the Hou–Xue–Zhang /
Jensen–Kelly–Pedersen sense does not apply — there is no anomaly here, and the paper's own design is
a *re-analysis of six published datasets* (Stock–Watson, Barro–Lee, Welch–Goyal, Freyberger–Neuhierl–Weber,
Donohue–Levitt, Chen–Yeh), each taken from the original authors' or a replication paper's materials.
That is unusually strong on one rubric row and weak on another: the breadth across six unrelated
prediction problems in three fields is real multi-domain evidence and the single most persuasive
thing about it, but every application is a **single sample**, five of the six are US-only, and the
method is Bayesian throughout with no out-of-sample holdout exercise beyond the predictive-score
identity of step 4. Multiple testing is not an issue in the usual sense — the paper is not searching
for an effect — but it is also not cost-aware in any sense, because it never forms a portfolio.
`published_post_2018: true`, so discount its novelty accordingly; `validation_overlap: false`, with
the latest of the six samples ending mid-2015.

## Implementability here

**Read this note as a constraint on the other three, not as a candidate.** Nothing in it ends in a
book, and it should not be made to.

**The direct collision with this folder's own standing advice, stated as a tension.**
`research/README.md`'s standing search area for machine learning asks sessions to "note especially any
finding about *how few* predictors actually matter", and the folder has two sources on the few-matter
side (`notes/2026-08-29-machine-learning-cross-section-comparative.md`,
`notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md`) plus the shrinkage cluster
(`notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`). **Tonight's source argues that the
apparent fewness is partly an artifact of estimators that can only select** — finding (1) — **and that
on the cross-section of returns specifically the data cannot support a sparse representation at all**
— finding (4). The collision is sharpened by the fact that this paper's cross-sectional application
is built on *the same characteristic set and the same quintile-dummy construction* as the folder's
2026-09-01 note, so the two are not talking past each other. The reconciliation the paper itself
offers is that both can be true: a *few* characteristics can carry nearly all the signal while the
*identity* of the selected set remains unidentified, because many characteristics carry overlapping
information. The practical reading is **"few in number, not few in identity"**, and the two claims
have opposite implications for a candidate: the first says build a small model; the second says do not
believe the particular small model you built.

**The collision with the lab's own measurements, and here the paper is in agreement rather than
tension.** `experiments/learnings.md` records, from two independent directions, that the lab's
learned candidates are not identified in exactly this way. **The first pair is v1-era and its
protocol vintage must be stated**, per `CLAUDE.md`'s rule against carrying v1/v2 constants forward:
measured 2026-08-29 on the 140-name panel, a ridge over eleven features including the champion's
12-1/6-1/3-1 lookbacks came back at **rho 0.774** to the champion, and a four-feature block with the
trend features deliberately removed came back at **rho 0.976** to an unconditional single sort on one
of its own four inputs — "feed a learner the incumbent's features and it rediscovers the incumbent,
worse." The numbers are v1 and do not transfer; **the structure does**, because it is a statement
about the feature set rather than about the fills or the cost model. The second direction is v3 and
needs no discount: [2026-10-20/21] F5/F6 found the spread amplitude and the group-explained share to
be "the slope and the volatility axis in costume", and [2026-10-17/18] found a correlation score
standardised by own volatility to be "still a volatility score with the sign flipped". **That is
finding (3) measured on this panel under the live protocol** — a collinear predictor set in which
different selections resolve to the same underlying bet. The lab reached it from the portfolio side;
this paper reaches it from the posterior side. Two independent routes to the same structure is the
strongest form of agreement available here.

**Three free, concrete things, in order of value.**

1. **Report the inclusion *frequency*, not the selected set — and this is the same instruction
   tonight's stability-selection note gives from a completely different direction.** Finding (3) says
   an interior `q` with no stable identity is the normal case; stability selection says to report
   per-variable selection probabilities. **Two Tier-A sources, one Bayesian and one frequentist,
   converging on the same reporting rule is worth more than either alone, and the lab currently
   reports neither.** Whatever the lab does with the ISIS pass, the output should be a frequency per
   feature.
2. **Copy the dogmatic-prior stress test as a falsifier for any future claim of sparsity here.** If a
   learned candidate is justified on the grounds that a handful of features matter, the check is
   whether that handful is stable when the method is *forced* to be sparse — and finding (4) says that
   on cross-sectional equity returns it may not be, even under an extreme prior. This is a
   pre-registerable kill condition, costs no trial, and would have applied retrospectively to the v2
   `sl_ridge_six_*` work.
3. **Prefer averaging over selecting when it comes to the free screens.** Finding (3)'s own
   conclusion is that the best prediction is a weighted average over many models with different
   memberships. The lab has the folder's forecast-combination material
   (`notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
   `notes/2026-08-19-model-averaging-mallows-weights.md`,
   `notes/2026-09-08-stacked-regressions-nonnegative-weights.md`) and has **already measured the
   portfolio-level version and found it wanting**: [2026-10-20/21] F11 records that a fixed equal-rank
   blend of the lab's individually-largest legs had the highest rank IC of the night and **6% realised**,
   and [2026-10-14/15] found that "combining legs does not cancel turnover on this panel; it adds".
   So the honest statement is that **model averaging is this literature's prescription and the lab has
   measured the version of it that fits in a top-K book to be a null** — the untested residual is
   averaging over *inclusion sets inside one fit* rather than over *finished books*, which is a
   different object and the only part of the prescription still open. Do not re-buy the blend.

**Known pitfalls.**

- **The paper's dependent variable is a return, not a Sharpe, and it never forms a portfolio.** Every
  claim is about *predictive identification*. The lab's binding constraint is skill against the
  equal-weight pool net of per-name v3 costs, and a predictor set can be perfectly identified and
  still worthless after costs — or unidentified and irrelevant because nothing in it is tradeable.
  **An identification result cannot qualify a candidate, only refuse a claim about one.**
- **Its universe is wide and shallow where this panel is narrow and large-cap.** About 2,250 US stocks
  per month across NYSE/Amex/Nasdaq, including the small and thinly traded names that
  `research/README.md`'s panel-width correction says are excluded here *by construction*. Finding (4)'s
  flatness may be partly a property of that breadth. By the 2026-10-20 rule ("ask for the liquid
  column; when a paper does not print one, assume the gap") **this paper prints no liquid column, so
  assume the gap** — and note the direction is ambiguous rather than conveniently favourable: a
  large-cap-only panel could be either better identified (less noise) or worse (less dispersion in the
  characteristics). State it as unknown.
- **It needs characteristics the lab does not have.** The 36 characteristics behind the
  cross-sectional application include book-to-market, return on assets and equity, price-dividend —
  fundamentals, which are out of scope here. So finding (4) is **about a richer feature set than the
  lab can build**, which cuts both ways: it is not a statement about free-OHLCV features
  specifically, and the lab's 7–15 free-OHLCV features are a far smaller pool in which identification
  should be *easier*, not harder. Do not quote finding (4) as though it were measured on this panel's
  features.
- **`p ≈ 144` against the lab's `p ≈ 7–15`.** The whole paper is about a large pool: "economic data do
  not appear informative enough to uniquely identify the relevant predictors **when a large pool of
  variables is available**". At `p = 7` the identification problem is much milder. The transferable
  part is finding (1) — selection without shrinkage manufactures sparsity — which is a property of the
  *estimator* and holds at any `p`.

## Related

- Tonight's other three notes are the machinery this one evaluates:
  `notes/2026-10-21-sure-independence-screening-marginal-vs-joint.md`,
  `notes/2026-10-21-stability-selection-subsampling-error-control.md`,
  `notes/2026-10-21-knockoff-filter-fdr-control-vs-permutation.md`. The convergence between this
  note's finding (3) and stability selection's reporting rule is the strongest cross-link of the four.
- `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` — same characteristic
  dataset, opposite emphasis; this is the stated tension.
- `notes/2026-08-29-machine-learning-cross-section-comparative.md`,
  `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`,
  `notes/2026-09-26-large-factor-models-aipt-complexity.md`,
  `notes/2026-09-26-virtue-of-complexity-return-prediction.md` — the few-versus-many axis this note
  reframes as selection-versus-shrinkage.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
  `notes/2026-08-19-model-averaging-mallows-weights.md`,
  `notes/2026-09-08-stacked-regressions-nonnegative-weights.md` — the averaging prescription finding
  (3) ends on, and `experiments/learnings.md` [2026-10-14/15] and [2026-10-20/21] F11 are the lab's
  measurements of its portfolio-level version.
- `experiments/learnings.md` [2026-10-13/14], [2026-10-17/18], [2026-10-19/20] — the three v3
  closures of `statistical-learning`, all attributed to the features; and the [2026-08-29, v1 era]
  `rho 0.774`-to-champion and `rho 0.976`-to-its-own-input entries, which are finding (3) measured
  here on the old panel, with [2026-10-17/18] and [2026-10-20/21] F5/F6 the v3 versions.
