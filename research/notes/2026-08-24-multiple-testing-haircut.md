---
title: "Backtesting: the multiple-testing haircut, and the significance threshold for a new factor"
authors: Harvey, Liu; Harvey, Liu, Zhu
year: 2015
venue: Journal of Portfolio Management (venue tier 1 by this folder's rubric); companion in Review of Financial Studies (tier 1)
url: https://doi.org/10.3905/jpm.2015.42.1.013 (haircut); https://doi.org/10.1093/rfs/hhv059 (thresholds)
citations: Harvey–Liu 110 (Semantic Scholar, checked 2026-08-24; Crossref 68). Harvey–Liu–Zhu 2116 (OpenAlex, checked 2026-08-24; Crossref 2020)
sample_period: Harvey–Liu is methodological. Harvey–Liu–Zhu catalogues factor tests published 1967–2012
markets: US cross-section of equity returns (the factor catalogue); the haircut method itself is asset-class agnostic
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The rival formalisation to the deflated Sharpe ratio, from the econometrics side rather than the
extreme-value side, and the one with by far the heavier citation weight behind it.

The core observation is an identity, not a model: with `T` observations, the t-statistic for the null
of zero mean return and the Sharpe ratio are the same number up to scale,

```
t = ŜR · √T          equivalently          ŜR = t / √T
```

so a Sharpe ratio *is* a p-value in disguise. That makes the whole apparatus of multiple-testing
correction directly applicable: convert the Sharpe ratio to a t-ratio, the t-ratio to a p-value,
adjust the p-value for the number of tests that preceded the discovery, convert back. The gap between
the original and the adjusted Sharpe ratio is the **haircut**, `hc = (ŜR − HSR)/ŜR`.

Two results carry the note.

**1. The haircut is strongly nonlinear in the Sharpe ratio, and the industry's 50% rule of thumb is
wrong in both directions.** Across all three adjustment methods and a wide range of assumed trial
counts, the haircut is **larger — often much larger — than 50% for annualised Sharpe ratios below
about 0.4**, and **at most about 25% for Sharpe ratios above 1.0**. Marginal strategies are gutted;
exceptional ones are barely touched. The economics is that a mediocre result is exactly what a large
random search produces by chance, while a large one is not; so 50% is simultaneously too lenient for
weak strategies and too harsh for strong ones.

**2. The choice of error rate matters more than the choice of adjustment within an error rate, and
finance should control the false discovery rate.** Family-wise error rate (FWER) controls the
probability of *even one* false discovery; false discovery rate (FDR) controls the *proportion* of
discoveries that are false. Bonferroni and Holm control FWER (Holm uniformly weaker, but tracking
Bonferroni closely); Benjamini–Hochberg–Yekutieli (BHY) controls FDR and is much more lenient
precisely where the two frameworks disagree — at low Sharpe ratios. The authors advocate BHY:
"FWER seems appropriate for applications where a false discovery brings a severe consequence… In
financial applications, it seems reasonable to control for the rate of false discoveries, rather than
the absolute number."

**The property that follows from that choice, and that no other source in this folder has supplied:
an FDR-controlling threshold does not rise without limit as trials accumulate.** In the companion,
Bonferroni- and Holm-implied thresholds are monotonically increasing in the number of discoveries,
while the BHY-implied threshold is **not monotonic — it fluctuates and then stabilises**, because at
a fixed significance level the law of large numbers forces the realised false-discovery rate to
converge to a constant. Under FWER, every trial makes life permanently harder for every later
candidate; under FDR, it does not.

## Construction recipe

**Independent case (the intuition).** If `N` strategies are tried and the best is reported, the
multiple-testing p-value for observing a maximum t-statistic at least as large as the one seen is

```
p_M = 1 − (1 − p_S)^N
```

With `p_S = 0.05` and `N = 10`, `p_M = 0.401`. The haircut Sharpe `HSR` is then defined by inverting
the single-test p-value relation at `p_M`. For small `p_S` this is approximately Bonferroni.

**Dependent case (the method).** Order the `M` p-values ascending, `p_(1) ≤ … ≤ p_(M)`.

- *Bonferroni* (FWER): `p^B_(i) = min[M·p_(i), 1]`.
- *Holm* (FWER, step-down): `p^H_(i) = min[ max_{j ≤ i} { (M − j + 1)·p_(j) }, 1 ]`.
- *BHY* (FDR, step-up, valid under **arbitrary** dependence): `p^BHY_(M) = p_(M)`, and for `i ≤ M−1`,
  `p^BHY_(i) = min[ p^BHY_(i+1), (M·c(M)/i)·p_(i) ]`, with `c(M) = Σ_{j=1..M} 1/j`. (Setting
  `c(M) = 1` recovers the original Benjamini–Hochberg procedure, valid only under independence or
  positive dependence.)

Holm and BHY need the empirical distribution of p-values across the strategies tried, not just the
count. Harvey–Liu supply that from the companion's structural model, which is fitted to the published
factor population **and corrects for the unobserved failed tests** — the ones nobody wrote up — and
for the correlation among strategy returns, which "effectively reduces the number of independent
tests" (the same lever as the DSR note's `N̂`). Their implementation draws `N` t-statistics from that
model, adjusts the `N+1` p-values, repeats many times, and takes the median adjusted p-value.

**Inputs the user must supply**, and the authors list them as the method's main weakness: sampling
frequency, number of observations, the Sharpe ratio (and whether it is annualised and whether it is
autocorrelation-corrected, plus the return autocorrelation if not), the assumed number of tests, and
**the assumed average correlation among strategy returns**.

**Minimum-profitability inversion.** The same machinery run backwards answers a more useful question
for a research programme: *given a significance level, a sample length, a volatility and an assumed
trial count, what is the minimum average return a proposed strategy must clear?* The gap is large —
in their worked example, going from single-test to BHY-adjusted at a fixed sample length and
volatility raises the monthly return hurdle by roughly two-thirds.

**Threshold for a new factor (companion).** From 313 published cross-sectional asset-pricing papers,
1967–2012, with thresholds re-derived at each point in time: the Bonferroni-implied hurdle rises from
1.96 to roughly 3.8 over the catalogue's span; Holm tracks it slightly below; BHY stabilises around
3.4 at 1% and about 2.8 at 5%. Their headline recommendation is **a t-ratio above 3.0 for a newly
proposed factor**, and they are explicit that this is a **lower bound**, because the catalogue counts
only *published* factors and the unpublished failures are invisible. Restricting to a homogeneous
subset — factors published from 2000 onward, Fama–MacBeth tests, at least the three Fama–French
controls — lowers the implied thresholds somewhat but not below the conventional 2.0 by any route.

## Robustness evidence (qualitative only)

- The p-value adjustment procedures are **theorems of statistics**, not empirical findings: Holm's
  and Bonferroni's guarantee on FWER and BHY's guarantee on FDR hold by construction, and the
  Yekutieli `c(M)` correction extends BHY's validity to arbitrary dependence among the test
  statistics. That part cannot decay.
- The companion is a heavily cited tier-1 publication whose census of the factor literature is
  reproducible from a published list, and it explicitly footnotes that its three adjustments are
  robust to heterogeneity in when and how each factor was tested — non-simultaneity and differing
  test methods do not invalidate the type-I control.
- What is *not* a theorem is the **structural model of the unobserved tests**, which is what makes
  the dependent-case haircut computable. It is an estimated correction for a population nobody
  observes, and its output is only as good as the assumption that the observed publications are a
  representative "elite" subset.
- The authors' own caveat list is unusually candid and worth carrying whole: high Sharpe ratios can
  come from non-normality, and **the method makes no correction for skewness or kurtosis** (they name
  this as future work — it is precisely what the deflated Sharpe ratio adds); the Sharpe ratio may
  not measure risk properly; the significance level, the multiple-testing method, and the number of
  tests are all judgment calls; and the number of tests is unobservable.
- The two frameworks in this session's pair of notes were developed contemporaneously and each cites
  the other approvingly, with the differences stated rather than papered over: Harvey–Liu identify
  *the group of strategies with non-zero returns*, the López de Prado programme evaluates *the
  relative performance of one strategy against a pool*; Harvey–Liu need only test statistics, the
  other needs each strategy's full time series; one is econometrics, the other is closer to machine
  learning.

## Implementability here

**1. The nonlinearity is the transferable result, and it is a genuine tension with the folder's
current reading of the gate.** `learnings.md` records that the DSR bar "effectively requires one
large single-step jump" and that incremental Sharpe gains cannot clear it. Under the haircut
framework, the *level* of the Sharpe ratio, not only the increment, governs how hard multiple testing
should bite — and a book in the neighbourhood of 1.0 sits in the region where the literature says the
multiple-testing penalty should be **mild** (≤ ~25%), while the region that deserves savaging is
below 0.4. This is recorded as a difference between two published corrections, **not** as a claim
that the repo's gate is mis-set: the two statistics answer slightly different questions, the engine is
frozen, and its thresholds are a human decision. What it does license is a sharper description of
what the gate is doing — it applies a deflation driven by the *search*, and the competing framework
would apply one driven by the search *and* the level.

**2. The FWER/FDR distinction, and a correction to a sentence the folder repeats.** "Every trial
permanently raises the bar for all future candidates" is a **family-wise-error-rate statement**. It
is true of Bonferroni and Holm and of any extreme-value threshold that grows in `N`. It is *not* true
of an FDR-controlling procedure, whose threshold stabilises rather than diverging with the trial
count — and FDR is what this literature recommends for finance, on the argument that an investor
cares about the *proportion* of allocated strategies that are duds, not about never allocating to
one. This does not change the repo's gate. It does mean the folder should stop writing "every trial
raises the bar" as if it were a law of statistics; it is a consequence of one choice of error rate.

**3. The in-sample-versus-out-of-sample section is the most directly relevant passage in either
source, and it names a cost of this repo's design that nothing here has priced.** Their argument
against relying on a holdout has four legs, three of which apply directly:

- *An OOS test is rarely truly out of sample.* A researcher tries a strategy, sees it fail, revises,
  tries again — "this trial and error approach is not truly OOS, but the difference is hard for
  outsiders to see."
- *An OOS test only works probabilistically*: success can be luck at both the in-sample selection
  step and the out-of-sample step.
- *Given the researcher has lived through the data, there is no true OOS built from historical data
  at all.* (This one bites hardest on a human-designed research programme, less on an agent, but the
  agent's priors come from the same literature.)
- **The type-I / type-II trade-off of splitting, which is the part worth carrying.** Holding data
  back shortens the in-sample window, which *loses true discoveries that never reach the
  out-of-sample stage*. Their worked illustration: with a 50/50 split you might identify ten
  promising strategies in-sample and confirm two, while having missed three true ones to bad luck in
  the short in-sample period; with a 90/10 split you recover two of those three, but now have too
  little held-out data to discriminate. "At its core, the OOS exercise faces a trade-off between
  in-sample and out-of-sample testing power."

  This is the **type-II mirror image of the ⚠ standing protocol concern** in `learnings.md`. That
  concern is that the gate reads a split that has disagreed with the holdout; this source says the
  three-way split *also* silently discards true discoveries at the first stage, and that the cost is
  structural rather than a defect of implementation. Both are arguments about the split, pointing the
  same way, from opposite error types. Recorded for the human reviewing that concern; it is not a
  licence for any session to reinterpret the protocol.

  Their tentative remedy — a lenient in-sample cutoff, then the out-of-sample test, then a
  multiple-testing correction on the **full** data, taking the intersection of survivors — is
  recorded as the literature's proposal and nothing more. It would require an engine change and is a
  human decision.

**4. One respect in which this lab is in better shape than the literature the source criticises.**
The whole difficulty in both this note and its sister is that `N` is unobservable — "the most
important piece of information missing from virtually all backtests is the number of trials
attempted". This repo records every trial, by protocol, in an append-only file. The correction that
these sources can only approximate is, here, computable from a known count. That is worth stating,
because it means the honest response to a high deflation bar is not to doubt the bar.

**5. What does not transfer.** The `t > 3.0` threshold is about *published asset-pricing factors*
evaluated against a null of zero, on a US cross-section, usually long–short and usually before costs.
It is not a bar for a long-only candidate being compared against an incumbent champion, and quoting
it as one would be a category error of the same shape the folder guarded against with the fundamental
law's information ratios. Nor does the haircut framework handle the non-normality that the deflated
Sharpe ratio does; on the repo's own daily series that omission runs in the direction of leniency.

## Related

- `notes/2026-08-24-deflated-sharpe-ratio.md` — the sister statistic, and the one the gate uses. The
  DSR authors describe the two thresholds as complementary and suggest computing both; this note
  supplies the FDR property and the level-dependence that the DSR framing lacks, and DSR supplies the
  non-normality correction that Harvey–Liu explicitly leave to future work.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the third leg of this session's
  inference triangle: comparing two candidates, rather than deflating one.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md` — the same problem observed after the fact
  rather than corrected in advance; Harvey–Liu–Zhu position their work explicitly against it.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the precedent for the category
  warning in point 5: a threshold defined on a benchmark-relative, long–short, gross-of-cost quantity
  does not transfer to this repo's total-Sharpe gate.
- **Reading note.** Harvey–Liu (2015) was read in full from the author's Duke-hosted PDF.
  Harvey–Liu–Zhu (2016) was read **in part** — abstract, introduction, the multiple-testing sections
  and the threshold results — not cover to cover; nothing is attributed to its unread sections.
