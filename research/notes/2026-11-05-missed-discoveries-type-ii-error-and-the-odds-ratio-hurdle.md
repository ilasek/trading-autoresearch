---
title: "False (and Missed) Discoveries in Financial Economics"
authors: Harvey, Liu
year: 2020
venue: The Journal of Finance 75(5), 2503–2553 — venue tier 1 by this folder's rubric
url: https://doi.org/10.1111/jofi.12951 (full text read from the first author's own page, https://people.duke.edu/~charvey/Research/Published_Papers/P143_False_and_missed.pdf; OpenAlex also lists a green-OA copy at arxiv.org/pdf/2006.04269)
citations: 117 (Crossref, checked 2026-11-05); 120 (OpenAlex, checked 2026-11-05). Semantic Scholar does not resolve the DOI (checked 2026-11-05).
sample_period: 1985–2014 (484 CAPIQ long–short strategies, US equity), 1984–2016 (18,113 data-mined anomalies from Yan–Zheng), and mutual-fund samples ending 2006 and 2016. Methodological throughout; the data are vehicles for the simulation
markets: US equity only — strategies, anomalies and mutual funds. Single-market, which is the one rubric column where this paper is weak
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

Every multiple-testing tool this folder has filed — Bonferroni, Holm, BHY, the haircut, the
deflated Sharpe, the online-FDR family — controls **Type I** error. None of them says what the
control *costs*. This paper's contribution is to put the second error on the same footing and make
both estimable for a given data set and a given testing procedure.

**1. The two rates, defined so they are symmetric.** In a multiple test the Type I analogue is the
realised false discovery rate, false positives over all discoveries:

```
RFDR   =  FP / (FP + TP)
```

and the Type II analogue the authors adopt is the **false omission rate** (also: false
non-discovery rate), misses over everything declared insignificant:

```
RMISS  =  FN / (FN + TN)
```

The symmetry is deliberate — FDR divides by all positives, so the Type II rate divides by all
negatives. The more familiar `FN/(FN+TP)` (one minus single-test power) is available and is a
transformation of these two, but the authors argue the omission rate is the right object under
multiple testing: finding three of five skilled managers among 1,000 candidates is a better
performance than finding three of five among 100, and only the omission-rate definition
distinguishes the two (2/997 against 2/97) while `FN/(FN+TP)` reports 2/5 for both.

**2. The object that joins them.** Their heuristic for trading the two off is the **odds ratio**
of false discoveries to misses:

```
ORATIO  =  FP / FN
```

with the decision rule stated plainly: *if a Type I error is `k` times as costly as a Type II
error, target `ORATIO = 1/k`.* This is a one-line substitute for writing down a loss function, and
the authors are explicit that it is a heuristic and not a derived optimum. Its advantage over
reporting the two rates separately is that it is insensitive to the base rate: when true effects
are rare, `RMISS` is mechanically tiny and looks reassuring while saying nothing about the
procedure's ability to find anything.

**3. How the Type II rate is estimated without specifying a high-dimensional alternative.** The
obstacle to any power calculation under multiple testing is that the alternative is a *vector* —
one effect size per test. The paper's device is to collapse it to a single number: assume a
fraction **`p₀` of the candidates are genuinely good**, and set their effect sizes to their own
in-sample estimates while setting everyone else's mean to exactly zero. `p₀` is treated as a
sufficient statistic for the alternative, readable either as a frequentist nuisance parameter to
be swept or as a Bayesian prior on the fraction of true effects.

**4. The double bootstrap.** One round of resampling constructs a world in which the truth is
known; a second round applies the testing procedure inside that world and records whether it was
right. That nesting is the whole method, and it is what makes the procedure's *own* error rates —
including those of procedures that are themselves bootstraps, like Fama–French (2010) — estimable.

**5. What it shows when run.** Three findings that travel:

- The classic Type I / Type II trade-off survives intact under multiple testing: raising the
  threshold lowers the false-discovery rate, raises the omission rate, and lowers the odds ratio,
  all monotonically.
- **The optimal threshold falls as `p₀` rises.** A stronger prior that real effects are common
  warrants a *more lenient* hurdle. The threshold also rises with the number of candidates tested
  and falls with the candidate pool's signal-to-noise ratio — so the same nominal hurdle means
  different things on a curated set of strategies and on a data-mined one.
- On the two sets of investment strategies studied, **neither the conventional `t = 2.0` nor the
  `t = 3.0` of Harvey–Liu–Zhu (2016) is optimal** under either criterion; the preferred cutoffs sit
  between them and depend on `p₀` and on the data set. The authors note in a footnote that
  Harvey–Liu–Zhu never intended 3.0 as a universal rule. On a large data-mined set the 5%-Type-I
  cutoff at `p₀ = 0` runs much higher than on a curated set, which is the multiple-testing problem
  behaving as expected.
- **Methods that ignore Type II error can be badly underpowered**, and the paper's headline
  application is that a widely used bootstrap procedure for fund performance can, with high
  probability, declare zero alpha across the board even when a substantial fraction of funds truly
  outperform and their realised returns are large. A non-rejection from an underpowered procedure
  is not evidence of absence.

The framing sentence worth carrying verbatim in spirit: when a study's main finding is the
**non-existence** of an effect, test power directly determines the credibility of that finding,
because power *is* the probability of rejecting when the effect is real.

## Construction recipe

The procedure, as the paper states it, for a panel `X₀` of `N` candidate return streams over `T`
periods and a chosen significance threshold (or any data-dependent testing procedure):

1. Bootstrap the **time periods** of `X₀` to get `Xᵢ`; compute the `1 × N` vector of t-statistics
   `tᵢ` on it.
2. Rank `tᵢ`. For the top `p₀` fraction, find the same candidates in `X₀` and shift their means to
   match those top-ranked means from `Xᵢ`; shift every other candidate to **exactly zero in-sample
   mean**. Call the assembled panel `Yᵢ` — a world where the truth is known and `p₀` of candidates
   are genuinely good.
3. Bootstrap the time periods of `Yᵢ` `J` times; on each draw apply the testing procedure and
   record the realised `RFDR`, `RMISS`, `RRATIO`.
4. Repeat `I` times and average over both indices. The paper uses `I = 100`, `J = 1,000`.

Four implementation points the paper is careful about:

- **Resample time periods, not candidates**, and resample the *same* periods across all candidates
  in the second stage. This is what preserves the cross-sectional correlation among tests, and it
  is why the resulting ROC curve accounts for test dependence while a t-statistic distribution does
  not.
- **`p₀` must be small enough** that the top `p₀·N` candidates have positive means in *every*
  bootstrap draw, not merely in the original sample — otherwise the constructed "true" effects are
  not consistent with a one-sided alternative.
- Sweep `p₀` rather than committing to one value, and read off which multiple-testing adjustment
  performs well *across* the plausible range. The paper's finding is that competing adjustments
  tend to keep the same ordering regardless of `p₀`, so the comparison is robust even when the prior
  is not.
- The error rates are **implicit functions of the threshold**, so the output is a curve, and the
  threshold is chosen off the curve by whichever criterion (fixed Type I, target ORATIO, ROC
  tangency) has been adopted in advance.

## Robustness evidence (qualitative only)

- **Venue and citation record are the strongest of tonight's three sources**, and the method is
  non-parametric, which is its main robustness claim: no distributional assumption on returns, and
  dependence across tests handled by construction.
- **Independent corroboration of the direction, from inside and outside finance.** The paper cites
  a survey finding that the large majority of results in many research areas are underpowered, and
  an older count that only a small minority of published economics papers consider power at all;
  within finance it places itself alongside several papers questioning the power of FDR-based fund
  evaluation. So "the Type I-only convention leaves large Type II errors" is a multi-source claim,
  not this paper's alone.
- **Where it is weak, by this folder's own rubric.** Single market (US); costs not modelled
  anywhere; the specific numerical thresholds are properties of the two data sets studied and the
  authors say so. `p₀` is an assumption dressed as a parameter — sweeping it mitigates but does not
  remove that. And the paper does not address publication bias in the curated data set it uses,
  which it acknowledges is selected toward strategies known to have performed well.
- **An honest limit the authors raise against their own programme**: the quest for statistical power
  need not align with the economic objective, and a method with low power can still carry economic
  implications. Power is a property of the test, not of the decision.
- **Anti-lookahead note.** The paper's samples end in 2016, so nothing in it can touch this lab's
  validation window, and no performance figure, return, alpha or event narrative from it is recorded
  here. The threshold magnitudes above are decision cutoffs calibrated on named data sets, not
  performance claims, and are recorded as such.

## Implementability here

**Status against the acceptance criterion** (admit only a source yielding a computable minimum
detectable effect as a function of something the lab controls): **it reaches, but on the
procedural reading rather than the closed-form one, and that should be stated rather than
glossed.** There is no formula here. What there is, is a *construction* that returns the Type II
error rate as a function of two things the lab does control — the significance threshold it sets
and the prior `p₀` it is willing to assert — for an arbitrary testing procedure including the one
the lab actually uses. A source giving only a power simulation for one estimator on one data set
would have been recorded as read-and-closed; this is the general machine, and the two
closed-form sources filed tonight supply the number this one supplies the apparatus for.

**1. What transfers immediately and costs nothing.** The reporting convention. Every `REJECT`,
`GATE_FAIL` and `SCOUT` line in the journal currently says a version of "no skill found". Composed
with tonight's MDE arithmetic, each of those can instead say **"no skill above `X` found"**, with
`X` the design's minimum detectable skill at the candidate's own benchmark correlation. That single
change converts a null from an absence of evidence into a bounded statement, which is precisely the
distinction this paper exists to draw, and it requires no new computation beyond `ρ` and the
window length.

**2. The ORATIO rule, and why it is a question for the human owner rather than an import.** The
rule is arithmetic once the cost asymmetry is named, and this lab's asymmetry is unusually sharp in
*both* directions. A false promotion installs a champion that later candidates must beat and that
the holdout has already been spent on — expensive, and partly irreversible. A miss costs a
mechanism that is then recorded as refuted in `learnings.md` and not revisited — also partly
irreversible, and the current gate structure means misses are never observed at all, so their rate
is unmeasured by construction. Which `k` is right is a decision about the lab's purpose; what this
note supplies is that **the choice of `k` is equivalent to the choice of the bar**, and that the
bar is currently set with `k` implicitly at infinity.

**3. The double bootstrap is runnable here, with one real obstacle.** The lab stores per-trial
return streams, so the batch version of the procedure has its inputs: treat the recorded trials as
the candidate cross-section, resample validation dates, and estimate the Type I and Type II rates
of the **deflated-skill bar itself** at a sweep of `p₀`. That would answer `#357`/`#358` —
whether the bar's severity is an estimate or an assumption — empirically rather than by
calibration. The obstacle is a structural mismatch: this is a **batch** framework (N candidates,
one decision) while the lab tests **sequentially** (one candidate per trial, over sessions), which
is the online-FDR vein the folder covered on 2026-10-29/30. The `p₀`-sweep and the ORATIO criterion
transfer to the online setting unchanged; the bootstrap mechanics need a batch, and the natural
batch is the recorded trial history read retrospectively rather than the next candidate.

**4. The `p₀` monotonicity is a usable prior-setting rule, and it points against the current
regime.** The optimal hurdle *falls* as the prior fraction of true effects rises. This lab's
recorded prior is very low — a long history of near-zero skill readings — which under this paper's
logic argues for a *higher* hurdle, not a lower one. But the same history is also what tonight's
MDE arithmetic says is unsurprising under a true-but-small effect, so the `p₀` estimated from the
lab's own outcomes is contaminated by the design's own power. The non-circular version is to set
`p₀` from the external literature's hit rate rather than from the lab's outcomes, and this folder
is the place that number would come from.

**5. Pitfall.** The omission-rate definition makes the Type II number look small whenever true
effects are rare, which is exactly this lab's regime. Reading `RMISS` alone here would be
reassuring and wrong; the odds ratio is the statistic to read, and the paper says so.

## Related

- `notes/2026-11-05-minimum-track-record-length-and-the-probabilistic-sharpe-ratio.md` and
  `notes/2026-11-05-minimum-backtest-length-and-the-expected-maximum-sharpe.md` — the closed-form
  halves of tonight's design question; this is the procedural half, and it is the only one of the
  three that can price the *cost* of the threshold rather than its level.
- `notes/2026-08-24-multiple-testing-haircut.md` and `notes/2026-11-01-weak-identification-of-t-stat-hurdles.md`
  — the `t = 3.0` hurdle this paper declines to treat as universal, and the identification problem
  underneath it.
- `notes/2026-10-29-lord-online-fdr-and-the-dependency-price.md`,
  `notes/2026-10-29-alpha-investing-sequential-error-budget.md`,
  `notes/2026-10-30-online-batched-fdr-and-the-dependence-that-matters.md` — the sequential setting
  the lab is actually in, and the reason the bootstrap half of this paper does not transfer
  directly.
- `notes/2026-10-30-cost-aware-alpha-investing-and-the-sample-size-lever.md` — the only prior note
  in this folder that puts power on the same footing as level; it does so inside a sequential
  testing budget, which is the complement of this paper's batch treatment.
- `notes/2026-09-15-inference-on-winners-post-selection-estimation.md` — what to do with the
  *estimate* of a candidate that clears whatever hurdle this framework sets.
- `notes/2026-11-04-out-of-sample-prediction-failure-and-the-cumulative-sse-diagnostic.md` —
  `#390`'s taxonomy says an underpowered model's cumulative curve looks poor early and improves,
  which is the shape test for the diagnosis this paper makes statistically.
