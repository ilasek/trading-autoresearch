---
title: "Inference on Winners"
authors: Andrews, Kitagawa, McCloskey
year: 2024 (Quarterly Journal of Economics); circulated as NBER WP 25456 from 2019, revised 2021
venue: Quarterly Journal of Economics (Tier 1)
url: https://doi.org/10.1093/qje/qjad043 ; working paper https://www.nber.org/papers/w25456
citations: 30 (Crossref cited-by on the journal DOI, checked 2026-09-15); 6 (OpenAlex, same date — its record is **merged with the 2019 working paper** and dated 2019, and the number is not credible for a paper this heavily built on); **not found** by Semantic Scholar on *either* the QJE DOI or the NBER DOI `10.3386/w25456`. See the access note below; the tier here rests on venue and on documented downstream use, not on a count
sample_period: n/a — econometric theory in a finite-sample normal model. Its two illustrations use a 2007 charitable-giving randomized trial and US census-tract mobility estimates; **no market data anywhere in the paper**
markets: none (methods paper); the paper names "the expected return of the trading strategy that performed best in a backtest" as a motivating example in its first paragraph
tier: A
validation_overlap: false
published_post_2018: true
---

**Read in full**, as NBER WP 25456 (January 2019, revised September 2021), 94 pages, complete and
text-extractable on the first try. NBER remains this folder's most reliable channel; contrast the
2026-09-13 warning about pre-2000 NBER scans — a post-2015 NBER paper is born-digital and needs no
rendering.

This note exists because the lab selected an argmax on 2026-09-14 and had no literature to read it
against. The 2026-09-14 nightly scored **178 variants of the champion's own construction**, found a
train dispersion of 0.079, identified `core_n = 10` as the best single cell, and **embargoed it** on
three arguments from this repo's own history. This paper is the general theory of that situation,
and it says the embargo was right *and* supplies the thing the embargo could not: a number for how
much of a selected winner's advantage is selection.

It is worth being precise about what is new here, because this folder is heavily covered on the
neighbouring vein. `2026-08-24-deflated-sharpe-ratio.md`, `2026-08-24-multiple-testing-haircut.md`,
`2026-08-25-prior-weighted-multiple-testing.md` and `2026-09-01-multi-signal-overfitting-critical-t.md`
are all about **testing**: given that I searched `N` candidates, is the best one *significantly*
better than nothing? This paper is about **estimation**: given that I searched `N` candidates and
picked the best, *what is that one actually worth*? The two questions have different answers, and
a repo whose gate compares a challenger's point estimate to an incumbent's point estimate is asking
the second one every night.

## Mechanism

Take a finite set of candidates `Θ`, each with an unbiased estimate `X(θ)` of its true value
`µ(θ)`. Select `θ̂ = argmax_θ X(θ)`. Then `X(θ̂)` is **not** an unbiased estimate of `µ(θ̂)`, because
a candidate is more likely to be selected precisely when its estimate is one of the lucky ones. The
paper establishes that this holds in the sharpest available form: `X(θ̂)` has positive **median**
bias both *conditional on which candidate won* and *unconditionally*, for every true `µ`:

    Pr_µ{ X(θ̂) ≥ µ(θ̂) | θ̂ = θ̃ } > 1/2    for all µ and all θ̃

The consequence is stated plainly and is the sentence worth carrying: **follow-up will be
systematically disappointing relative to what the original selection implied.** This is the same
object as the "winner's curse" recorded elsewhere in this folder, but here it is a property of the
*point estimate* rather than of a p-value, and it does not require the candidates to be independent
or the number of them to be large.

Two structural facts govern how big the bias is:

1. **It grows with the number of candidates.** The paper's own illustration compares 2, 10 and 50
   candidates and finds conventional confidence intervals cover reasonably at 2 and can under-cover
   substantially at 10 and 50 — "as is natural since a larger number of policies allows more scope
   for selection".
2. **It vanishes when one candidate is clearly ahead.** The paper is explicit: where the winner's
   curse does not arise "because one treatment considered is vastly better than the others", the
   corrected procedures *coincide* with the conventional ones. The correction costs nothing in the
   easy case, which is what makes it safe to adopt as a standing convention rather than as a
   special-case tool.

Fact 2 is the mechanism a lab should internalise, because it says where the bias lives: **in the
gap between the winner and the runner-up, measured against the standard error of their difference.**
A curve whose argmax is a hair above the second-best cell is almost all selection; a curve whose
argmax is far clear of the field is almost all signal. This is not an intuition — it falls directly
out of the conditioning event, next.

## Construction recipe

Work in the finite-sample normal model the paper derives everything in: `X ~ N(µ, Σ)` over the
candidate set, with `Σ` known (in practice, consistently estimated — the paper proves the feasible
plug-in versions are uniformly asymptotically valid over a large class of data-generating
processes, so an estimated `Σ` is legitimate).

**The conditional (median-unbiased) procedure.** Let `Y(θ̃)` be the quantity of interest for
candidate `θ̃` and define

    Z_θ̃ = X − ( Σ_XY(·, θ̃) / Σ_Y(θ̃) ) · Y(θ̃)

i.e. the part of the estimate vector orthogonal to `Y(θ̃)`. Conditional on `{θ̂ = θ̃, Z_θ̃ = z}`, the
winner's own estimate `Y(θ̂)` follows a **one-dimensional truncated normal** on an interval
`[L(θ̃, z), U(θ̃, z)]`. The paper's Proposition 1 (built on Lee et al. 2016's polyhedral lemma)
gives the endpoints in closed form:

    L(θ̃, Z_θ̃) =  max over {θ : Σ_XY(θ̃) > Σ_XY(θ̃,θ)}  of  Σ_Y(θ̃)·( Z_θ̃(θ) − Z_θ̃(θ̃) ) / ( Σ_XY(θ̃) − Σ_XY(θ̃,θ) )
    U(θ̃, Z_θ̃) =  min over {θ : Σ_XY(θ̃) < Σ_XY(θ̃,θ)}  of  the same expression

Then with `F_TN(y; m, θ̃, z)` the truncated-normal CDF (strictly decreasing in `m`), define `µ̂_α` as
the unique solution to `F_TN(Y(θ̂); µ̂_α, θ̃, Z_θ̃) = 1 − α`. The paper shows `µ̂_α` is the **optimal**
`α`-quantile-unbiased estimator conditional on `θ̂`. So:

- **point estimate**: `µ̂_{1/2}` — median-unbiased conditional on which candidate won;
- **interval**: `CS_ET = [ µ̂_{α/2}, µ̂_{1−α/2} ]` — equal-tailed, conditional coverage `1 − α`.

**The special case worth memorising.** With two candidates of equal, independent variance, the
conditioning event reduces to "`X(1)` is a normal truncated below at `x(0)`" — truncated at the
*other candidate's observed value*. Generalising through Proposition 1, the lower truncation point
is set by the runner-up. That is the formal content of "the correction is governed by the
winner-to-runner-up gap": all the shrinkage comes from how much probability mass the truncation
removes, and it removes almost none when the winner is far ahead.

**Two alternatives the paper prices, both relevant here.**

- **Projection intervals** — form a simultaneous confidence band over *all* candidates and read off
  the interval for the selected one. Unconditionally valid, but wider than conventional intervals
  *even when conventional intervals are fine*. The paper finds they beat conditional intervals when
  there is substantial randomness in which candidate wins (i.e. no clear best).
- **Hybrid** — combine conditioning and projection. Keeps most of the conditional method's
  performance in the easy case while capping length in the hard case; in the paper's calibrated
  simulations hybrid intervals are typically shorter than both, often by a large margin. This is
  the paper's recommended default and the one to implement if only one is implemented.

**Sample splitting is the third option, and the paper's treatment of it is the part this repo
should read most carefully.** Choosing the target on one subset and estimating on the remainder
gives unbiasedness and valid conventional intervals *conditional on the target*. The paper does not
dispute this — it says the cost is twofold: the split-sample target is **necessarily more variable**
than the full-data target (you select on less information, so you more often select a different
candidate), and the procedure is **inefficient** within the class of procedures with the same
target (you estimate on less information too).

## Robustness evidence (qualitative only)

- The results are finite-sample exact in the normal model and the paper proves **uniform asymptotic
  validity** for feasible versions with non-normal data and estimated variances — the first such
  result in the conditional-inference literature, per the authors.
- The corrections are shown to be optimal within their class (median/quantile unbiasedness
  conditional on the selection), drawing on Pfanzagl's results for exponential families, rather
  than being one heuristic among several.
- The phenomenon is independently documented in other fields with the same structure and the same
  remedy shape — genome-wide association studies and online A/B testing are both cited. That
  cross-field recurrence is the strongest robustness signal available for a methods result: it is
  not a finance regularity that can decay.
- **The paper's own limit, stated by the authors**: the goal is to evaluate a selected rule *taking
  the selection rule as given*, not to improve the selection rule. Correcting the winner's curse
  does not tell you to pick a different winner.
- **A caveat that points directly at this folder's next note.** In the paper's second application,
  conventional empirical-Bayes corrections (of the kind in `2026-08-25-hierarchical-bayesian-factor-replication.md`,
  and the subject of `2026-09-15-tweedies-formula-empirical-bayes-selection-bias.md`) **reduce but do
  not eliminate** the bias. The reason is exact and worth carrying: a standard empirical-Bayes
  correction corresponds to a *normal* prior on the underlying effects, and it corrects the winner's
  curse when that normal prior matches the true distribution of effects — **but not in general
  otherwise**. The two corrections in this session's notes are therefore not interchangeable; this
  one makes no assumption about the distribution of true effects, and the other one does.
- The paper places itself explicitly as the **complement** to the superior-predictive-ability
  literature (White 2000; Hansen 2005; Romano–Wolf 2005 — see
  `2026-09-15-reality-check-max-statistic-under-dependence.md`): that literature tests whether the
  best candidate beats a benchmark, this one estimates what the best candidate is worth. A lab that
  wants both needs both.

## Implementability here

**Directly, cheaply, and on objects that already exist in this repo.** Everything the conditional
procedure needs is a vector of candidate estimates and their covariance, and the lab produces both
as a by-product of the work it already does.

- **The 2026-09-14 specification curve is exactly the input.** 178 variants, each with a train
  Sharpe; the covariance of those Sharpe estimates is computable from the paired return series the
  same harness produced. The repo already carries the paired machinery — `metrics.sharpe_diff_se`
  (Memmel's correction to Jobson–Korkie), used by the holdout veto and noted in
  `2026-08-24-testing-differences-of-sharpe-ratios.md`. The off-diagonal of `Σ` is that quantity.
- **The cheapest usable version needs no matrix at all.** Because the truncation point is set by the
  runner-up, a first-order reading of "how much of this argmax is selection" is the winner-to-
  runner-up gap divided by the standard error of their *difference*. On a curve of 178 nearly
  collinear variants that SE is small and the gaps are small, which is the regime where the
  correction is largest. The lab can compute this from two return series.
- **The lab's own three-split protocol is the sample-splitting option, and this paper is the first
  source here that prices it honestly.** Selecting a construction on train and scoring it on
  validation *is* valid — the repo's instinct is correct and this source backs it. What the source
  adds is the cost: the selection is noisier than it would be on all the data, and the estimate is
  noisier too. That matters for reading a train screen: a construction chosen on train is not the
  construction that would have been chosen on everything, so a train-selected cell carries variance
  the validation number does not reveal. It is an argument for the conditional correction *in
  addition to* the split, not instead of it.
- **The honest use, and the one to propose.** Not to pick a better cell — the paper says explicitly
  it does not improve the selection rule, and the lab's `core_n` embargo rests on reasons this
  source does not touch. The use is **as a discount applied to any number that was selected as a
  maximum**, including the historical promotion margins. A promotion is an argmax: the champion seat
  went to whichever candidate scored best on validation among those tried.

**Pitfalls, stated because they are real and some of them bite here.**

- **The conditioning event must be the actual selection rule.** The theory conditions on
  `θ̂ = argmax X(θ)`. If a cell was chosen by an argmax *plus* human judgement, a pre-registered
  default, or a prior refusal to go below some depth, the conditioning event is not the one in
  Proposition 1 and the correction as written does not apply. The lab's house defaults are not
  argmaxes and should not be corrected as if they were — and, usefully, the 2026-09-14 finding that
  the house default sits at the **67th percentile rather than the maximum** of its own curve is
  exactly the evidence that this repo's construction was not selected this way.
- **Normality of the estimates.** The finite-sample results are normal-model;
  `2026-08-23-statistics-of-sharpe-ratios.md` records that Sharpe-ratio estimates are not normal in
  small samples and that the standard error depends on higher moments. The feasible asymptotic
  version is the one to use, and its validity is asymptotic in the length of the return series, not
  in the number of candidates.
- **`Σ` must be estimated on the same window the estimates come from**, which for this repo means
  train. A train-estimated `Σ` used to correct a train-selected argmax is internally consistent;
  using it to correct a validation number is not.
- **Nothing here reaches the holdout, and nothing here is a candidate.** The procedure consumes
  numbers the lab has already computed on a split it is already allowed to read. It scores no new
  returns and proposes no book.

## Related

- `2026-09-15-tweedies-formula-empirical-bayes-selection-bias.md` — the empirical-Bayes alternative
  to this correction, and the one this paper shows is only valid when its implicit normal prior is
  right.
- `2026-09-15-reality-check-max-statistic-under-dependence.md` — the testing complement, named as
  such by this paper's own related-literature section.
- `2026-08-24-deflated-sharpe-ratio.md` — the folder's existing winner's-curse coverage, which is a
  *test* under an **independence** assumption; this note is the *estimate* under arbitrary
  dependence, so the two do not overlap as much as the shared phrase suggests.
- `2026-09-09-specification-curve-analysis.md` and `2026-09-09-nonstandard-errors-in-portfolio-sorts.md`
  — the machinery that produces the curve this correction is applied to. Those two say how wide the
  curve is; this one says what its maximum is worth.
- `2026-08-25-hierarchical-bayesian-factor-replication.md` — the empirical-Bayes shrinkage this
  paper finds insufficient in general.
- `2026-09-06-number-of-portfolios-as-tuning-parameter.md` — the other note about selecting a
  construction knob, and the one that established the lab's asymptotic regime does not exist at
  `n ≈ 140`.
