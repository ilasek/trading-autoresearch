---
title: "Making and Evaluating Point Forecasts" — the decision-theoretic result that a loss function *elicits* a specific functional of the predictive distribution, and that a mismatched loss ranks a worse forecaster first
authors: Gneiting
year: 2011
venue: Journal of the American Statistical Association 106(494), 746–762 (venue tier 1 — the discipline's flagship statistics journal; the paper is an invited review with discussion)
url: https://doi.org/10.1198/jasa.2011.r10138
citations: 1009 (Crossref `is-referenced-by-count`, checked 2026-10-19); 1251 (Semantic Scholar by DOI, same date). Two indices, same order of magnitude, Semantic Scholar the higher — the usual direction for a paper with a long preprint life.
sample_period: none — decision theory plus one synthetic simulation from a GARCH(1,1) data-generating process. No market data of any period is used anywhere in it.
markets: none
tier: A
validation_overlap: false
published_post_2018: false
read: full text of arXiv:0912.0902v2 (38 pp., `arxiv.org/pdf/0912.0902`), 108 KB of clean text, 776 instances of `" the "`, zero `( )` dropout, no ASCII shift. The JASA version is closed; the preprint carries the abstract, all five sections, Theorems 2.2–2.8, Tables 1–9 and the discussion, and its abstract matches the published one claim for claim. The published version additionally carries invited discussions by other authors, which were **not** read and are not relied on here.
---

## Mechanism

There is no economic mechanism. This is the **theory layer underneath every supervised-learning
candidate this lab will ever write**, and the reason to file it as a note is that a grep across all
201 prior notes returns zero for `scoring rule`, `proper scoring`, `elicitab`, `Bregman`,
`pinball`, `expectile`, `quantile regression` and `Gneiting`. The folder holds 200 notes about
*what to predict* and *how to weight it*; it holds nothing about **what the loss function makes a
model predict**, which is a different question with an exact answer.

The claim, in one line: **a scoring function does not measure accuracy, it names a target.** Given
a loss `S(x, y)` disclosed in advance, the forecast that minimises expected loss under the
forecaster's own predictive distribution `F` — the Bayes rule `x̂ = argmin_x E_F S(x, Y)` — is a
specific *functional* of `F` and nothing else. Squared error names the mean. Absolute error names
the median. The asymmetric piecewise-linear (pinball) loss names a quantile. Change the loss and
you have silently changed what the model is trying to be, whatever you believed you were measuring.

**The simulation that makes this concrete, and it is the single most useful thing in the paper.**
Three forecasters predict a highly volatile daily asset value generated as `Y_t = Z_t²` with `Z_t`
Gaussian and conditionally heteroscedastic (a standard GARCH(1,1) parameterisation). The
*statistician* knows the true data-generating process and the realised conditional variance, and
issues the **true conditional mean**. The *optimist* always issues a large constant; the *pessimist*
always issues a near-zero constant. Over 100,000 sequential forecasts: the statistician wins on
squared error, as she must. **The pessimist wins on both absolute error and absolute percentage
error. The optimist wins on relative error.** Two of the four error measures in universal use rank a
forecaster who knows nothing above a forecaster who knows everything, and the third ranks the other
ignorant one first. Nothing is wrong with the simulation; the measures are simply consistent for
functionals other than the mean, and a constant can be the right answer for those functionals.

The structural reason is that a point forecast is a *reduction* of a predictive distribution, and the
reduction is only meaningful once somebody has said which feature of the distribution is wanted. The
paper's prescription is therefore two-pronged and admits no third option: **either disclose the
scoring function ex ante**, so the forecaster can issue the Bayes rule for it, **or name an
elicitable target functional** and then use only scoring functions consistent for it.

## Construction recipe

This is the part to copy. Definitions first, then the characterisations, then the trap.

**Consistency.** `S` is *consistent* for the functional `T` relative to a class `F` of
distributions if `E_F S(t, Y) ≤ E_F S(x, Y)` for all `F ∈ F`, all `t ∈ T(F)` and all `x` — i.e. the
expected score is minimised by doing what the directive says. *Strictly* consistent if the minimum
is attained only there. Theorem 2.4: every consistent scoring function induces a **proper scoring
rule** for the corresponding probabilistic forecast, and Theorem 2.2 gives the duality the other way
— consistency for `T` and `T` being the Bayes rule of `S` are two statements of the same fact.

**Elicitability.** `T` is *elicitable* if some scoring function is strictly consistent for it. The
characterisations, each an "if and only if" under weak regularity conditions:

| Target functional | The consistent losses are exactly | Identification function `V(x, y)` |
|---|---|---|
| Mean / expectation | the **Bregman** functions | `x − y` |
| `α`-quantile | the **generalized piecewise linear (GPL)** functions of order `α` | `1(x ≥ y) − α` |
| `τ`-expectile | a family combining Bregman and GPL elements | `2·|1(x ≥ y) − τ|·(x − y)` |
| Ratio `E[r(Y)]/E[s(Y)]` | characterised (Osband's principle) | `x·s(y) − r(y)` |

Squared error is the canonical Bregman function; the pinball loss `(α − 1(y < x))(y − x)` is the
canonical GPL function and is exactly what classical quantile regression (Koenker–Bassett)
minimises, with Komunjer (2005) generalising to the whole GPL class. **Expectiles are the asymmetric
least-squares analogue of quantiles** and are elicitable, which matters below.

**What is NOT elicitable, and this is the hard constraint.** Theorem 2.8 (Osband): an elicitable
functional has convex level sets. Two consequences the paper draws explicitly:

- **Conditional value-at-risk (CVaR / expected shortfall) is not elicitable.** No scoring function
  is consistent for it. The paper calls this a "disconcerting negative result" and notes CVaR's
  popularity in quantitative finance.
- **The sum of two distinct quantiles is generally not elicitable.** So a composite objective built
  by adding tail quantiles is not a target any loss can honestly elicit.

**Osband's principle** is the constructive recipe for deriving the consistent class for a new
functional: find an identification function `V` with `E_F[V(x, Y)] = 0 ⟺ x ∈ T(F)`, then
`S⁽¹⁾(x, y) = h(x)·V(x, y)` for some `h`, and integrate. Worth knowing because it is how one checks
a *home-made* loss rather than guessing.

**The trap, and it is the result most likely to bite this lab: Theorem 2.7, on weighted scoring
functions.** Take any loss `S` consistent for `T`, and weight it by a function of the *realisation*:
`S⁽ʷ⁾(x, y) = w(y)·S(x, y)`. Then `S⁽ʷ⁾` is strictly consistent — but **not for `T`**. It is
consistent for `T` applied to the *tilted* distribution `F⁽ʷ⁾` whose density is proportional to
`w(y)·f(y)`. In the author's words the weighted functional "acts on the predictive distribution in a
peculiar way". Two instances worked out in the paper:

- `S = ` squared error (consistent for the mean), arbitrary weight `w`:
  `T⁽ʷ⁾(F) = E_F[Y·w(Y)] / E_F[w(Y)]`.
- `S(x, y) = (x − y)²/y²` (squared percentage error, i.e. `w(y) = 1/y²`): consistent for
  `E[Y⁻¹]/E[Y⁻²]`.

So **"I will weight the training loss toward the observations I care about" does not produce a model
that predicts the mean of those observations.** It produces a model that predicts the mean of a
reweighted distribution — a different number, generally not the one the weighting was supposed to
emphasise, and one nobody has a decision for.

**And the commonly used losses, graded.** Squared error → mean. Absolute error → median. **Absolute
percentage error → the "median of order −1"**, a non-standard functional which the paper says "tends
to support severe underforecasts"; it concludes that organisations using APE should "reassess its
suitability". Relative error `|(x − y)/x|` → the median of order 1; squared relative error
`(x − y)²/x²` → `E[Y²]/E[Y]`, as does the observation-weighted `y(x − y)²`. The **Patton family** of
homogeneous losses nests squared error and QLIKE and is consistent for the mean throughout; within
it, Patton–Sheppard recommend QLIKE for its superior power in Diebold–Mariano tests of predictive
ability — i.e. **among losses consistent for the same functional, the choice is about test power, not
about the target.** That is the one dimension on which loss choice is a free parameter.

## Robustness evidence (qualitative only)

- **The results are theorems, not estimates.** Consistency, the Bregman and GPL characterisations,
  Theorem 2.7 and the non-elicitability of CVaR are proved. They need no sample, no market and no
  replication to be believed, and they cannot decay. By the folder's own eighteenth detector
  [`SUMMARY.md` 2026-10-18] this is a source asking the reader to believe **algebra**, which is the
  cheapest of the three evidentiary standards and the one where Tier A is earned outright.
- **The practice it criticises is documented, not asserted.** The paper surveys the 2008 volumes of
  the leading forecasting, statistics, econometrics and meteorology journals and four business
  surveys, and shows squared error dominant in academia with absolute percentage error very widely
  used in industry. The target of the criticism is the field's actual habit.
- **Lineage.** The mean and quantile characterisations are classical (Savage 1971; Thomson 1979);
  the elicitability concept is Osband (1985) and Lambert, Pennock and Shoham (2008); the
  ratio-of-expectations, expectile, CVaR and weighted-scoring results are this paper's own. The
  framing it develops is Murphy–Daan (1985) and Engelberg–Manski–Williams (2009), both quoted at
  length. The paper is now the standard citation for elicitability across statistics, meteorology
  and risk measurement, which is what its citation count reflects.
- **Known limits, stated by the author.** Weight functions that depend on the *forecast* `x` rather
  than the realisation `y` "need to be handled on a case-by-case basis" — Theorem 2.7 does not cover
  them. A characterisation of elicitability in general is left open; Theorem 2.8 is necessary, not
  sufficient. And the paper is about univariate real-valued predictands: it says nothing directly
  about scoring a *vector* of forecasts jointly, which is what a cross-sectional panel is.
- **Costs, multiple testing.** Not applicable — there is no empirical claim to cost or to deflate.

## Implementability here

Nothing to implement; everything to apply. Four consequences, in descending order of how much they
should change what the lab writes next.

1. **Name the functional before writing the loss, and for this lab the functional is almost never a
   conditional mean.** Protocol v3's one admitted claim is cross-sectional name selection within
   region and type [`learnings.md` 2026-10-13/14]: the decision is "which `K` of ~1,000 eligible
   names do I hold", weighting and breadth having been measured to buy nothing. The functional that
   decision consumes is therefore an **ordering**, or equivalently, for each name, the conditional
   probability that it lands in the top `K` of its region's forward-return distribution. That
   probability is an expectation of an indicator, hence elicitable, hence trainable with a
   **strictly proper** loss — log loss or Brier score, both Bregman. **A classifier on top-`K`
   membership, trained with log loss, is a theoretically licensed design and an MSE regression on
   raw forward returns is not the same object.** This is the concrete, free design change the note
   licenses, and the companion note on learning to rank
   (`2026-10-19-learning-to-rank-cross-sectional-selection.md`) is the empirical half of it.
2. **Never weight the training loss by return magnitude.** The temptation on this panel is strong:
   the folder already holds the finding that the cross-section of long-horizon stock returns is
   dominated by a few names (`2026-08-26-skewness-and-concentration-of-stock-returns.md`), which
   invites a loss weighted by `|y|` to "focus on the movers". Theorem 2.7 says that elicits
   `E[Y·|Y|] / E[|Y|]` — a tilted mean, over-weighting the right tail of an already right-skewed
   cross-section, and not the mean of the movers. If the intent is to care about the tail, the
   honest route is to **change the functional explicitly** (predict a high quantile or a high
   expectile, with the GPL or asymmetric-least-squares loss that is consistent for it) rather than
   to reweight a mean loss and hope.
3. **Percentage- and ratio-form losses are disqualified on this panel twice over.** APE and relative
   error are consistent for strange functionals (and APE biases toward severe underforecasts), and
   separately they are defined only for strictly positive quantities while a daily or monthly
   return is signed and routinely near zero. They should not appear in any candidate. This is worth
   writing down because they are the default in a great deal of applied forecasting code.
4. **A tail-risk training objective is not available, and the lab has already discovered the
   empirical shadow of this.** CVaR is not elicitable, so no loss trains a model to minimise
   expected shortfall directly, and a sum-of-quantiles objective is not elicitable either. The lab's
   own measurement that the diversification ratio is "a composition descriptor and not a drawdown
   predictor" [`learnings.md` 2026-09-25] and the standing habit it generalised to — *pre-register a
   statistic's predictive claim separately from its descriptive one* — are the same lesson arriving
   from the empirical side. Drawdown and shortfall belong in the result card as descriptors; they
   cannot be the thing a learner minimises.

**Two further mechanics for whoever writes the first candidate under this.** (a) scikit-learn
implements the two relevant non-Bregman losses directly — `QuantileRegressor` minimises the pinball
loss (GPL, consistent for the `α`-quantile) and `HuberRegressor` a Huber loss; confirm the installed
version exposes them before designing around them, and note that a Huber loss is **not** consistent
for the mean, so a robust fit is a deliberate change of target rather than a cleaner estimate of the
same one — exactly the distinction `2026-09-11-influential-observations-winsorization-versus-robust-regression.md`
draws between trimming the data and changing the estimator. (b) Whatever loss is chosen, the model
still has to be fitted walk-forward: this note changes the objective, not the causality discipline in
`program.md` or the cross-validation caveats in
`2026-10-13-k-fold-cross-validation-under-temporal-dependence.md`.

**Pitfall worth naming.** This note licenses no expectation of an edge. It says that several ways of
training a model are incoherent and names two that are coherent; a coherent objective over a score
with no information in it is still a null. The folder's record of free OHLCV scores priced to
region-matched nulls [`learnings.md` 2026-10-14/15] is unaffected by anything here.

## Related

- `2026-10-19-learning-to-rank-cross-sectional-selection.md` — the applied half: an ordinal loss on
  exactly this lab's select-the-top-`K` decision, with a long-only decile table.
- `2026-10-19-no-arbitrage-criterion-as-the-learning-objective.md` — the third answer to "what should
  the learner minimise": a pricing-error moment condition rather than a forecast error.
- `2026-08-20-parametric-portfolio-policies.md` — the fourth answer, and the one the folder already
  held: skip the predictive loss entirely and maximise realised utility of the portfolio. Read
  against this note, BSV is the limiting case where the "functional" named is the decision itself.
- `2026-08-29-machine-learning-cross-section-comparative.md` and
  `2026-09-03-machine-learning-economic-restrictions.md` — both are about *which features* and *which
  architecture*, both minimise a mean-squared loss, and neither examines the loss. This note is the
  axis they leave untouched.
- `2026-09-11-influential-observations-winsorization-versus-robust-regression.md`,
  `2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md` — what a robust loss and a rank
  transform each do to the target; both are functional changes in Gneiting's sense.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — if the directive is an ordering, the test
  of whether it was followed is a monotonicity test, not an `R²`.
- `2026-08-26-skewness-and-concentration-of-stock-returns.md` — why the weighted-loss temptation
  arises on this panel at all, and why Theorem 2.7 is the reason to resist it.
