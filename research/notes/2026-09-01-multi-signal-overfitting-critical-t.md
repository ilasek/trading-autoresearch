---
title: "Testing strategies based on multiple signals (circulated as: Backtesting strategies based on multiple signals)"
authors: Novy-Marx
year: 2016 (March 2016 draft; NBER WP 21329, July 2015)
venue: NBER working paper / author's working paper — "Revise and resubmit, Journal of Financial Economics" per the author's CV as of the version checked (Tier 2)
url: https://www.nber.org/papers/w21329 — draft read at https://mysimon.rochester.edu/novy-marx/research/MSES.pdf
citations: 41 (OpenAlex by DOI 10.3386/w21329) / 32 (Semantic Scholar, same DOI), both checked 2026-09-01
sample_period: CRSP, January 1995 – December 2014 for the simulations; a July 1963 – December 2014 illustration of the integration/mixing equivalence
markets: US common stocks (CRSP). The core results are analytic and universe-independent.
tier: B
validation_overlap: false
published_post_2018: false
---

Read **in full** from the author's own page at the University of Rochester (March 2016 draft,
50pp). Publication status confirmed from the author's posted CV, where it sits under *Working
Papers* with an R&R at the *Journal of Financial Economics*; the title on the draft is "Testing
strategies based on multiple signals" while the NBER/SSRN circulation title is "Backtesting
strategies based on multiple signals". **Tier B on venue and citation count**, and it should be
read as a *methods* paper rather than an empirical finding: the load-bearing results are
closed-form distributional statements plus a Monte Carlo, neither of which depends on the sample
the simulation happens to run on.

This note is filed for **`portfolio-learning`** and as a **cross-cutting inference note**, and it
lands directly on the thing the lab built on 2026-08-31: a book that aggregates four family-lead
signals with a **max-of-z** operator and scores far above any of its legs. The source is a
discount on that class of result — but the discount has a precise boundary, and the boundary is
the most useful thing in the paper for this lab.

## Mechanism

The subject is not a market effect. It is **what the null distribution of a backtest t-statistic
looks like when the strategy was built by combining several signals**, and the answer is that it
is nothing like a standard normal.

Two separate biases, which the paper insists on keeping apart:

- **Selection bias (the familiar one).** You try `n` signals and report the best. This is the
  bias Harvey–Liu–Zhu, Bailey–López de Prado and McLean–Pontiff address, and this folder already
  holds notes on all three. Closed form: the critical `t` at level `p` from the best of `n`
  candidates is `N⁻¹((1 − p/2)^(1/n))`, i.e. **the true p-value is about `n` times the claimed
  one** — Bonferroni, essentially.
- **Overfitting bias (the one this paper is about, and it is not the same thing).** You use
  *every* signal you considered — no selection at all — but you **sign each one so that it
  predicts positive in-sample returns**. That single act uses the data, and it biases the
  composite even with zero selection. A researcher who honestly reports all `n` signals is still
  exposed.

The demonstration is blunt: build composite signals out of **purely random** sorting variables
on real stock returns, sign each so it looks good in sample, and the resulting strategies
routinely backtest with t-statistics above five. Under some of the constructions considered,
**5% significance requires `t` above seven** — for a signal with no predictive power whatsoever
by construction. The paper's own framing: diversifying across the recommendations of stock
pickers who happened to do well in the past improves *past* performance even when the pickers
are darts.

**The two biases multiply.** Combining the best `k` of `n` candidate signals produces a bias
almost as large as selecting the single best of **`n^k`** candidates. This power law is derived
in the model and confirmed in the simulation. It is the paper's most quotable result and it is
brutal for any research programme that screens many mechanisms and then integrates the survivors.

## Construction recipe

*This is a testing recipe, not a strategy recipe.*

**Setup.** Let `t = (t₁ … tₙ)` be the t-statistics of the stand-alone strategies built on each
of `n` candidate signals, sorted, and let the composite use the best `k` of them. Under the
paper's model (active returns normal, uncorrelated across signals, equal volatility):

- **Equal-weighted composite** (each employed signal gets the same weight — the minimum-variance
  portfolio of the leg strategies):
  `t_MV(n,k) = (Σ of the k largest tᵢ) / √k = √k × (mean t of the employed legs)`
  — the scaled **L1 norm** of the top-`k` order statistics.
- **Signal-weighted composite** (weight each signal by its own in-sample performance — the
  ex-post mean-variance-efficient portfolio of the legs):
  `t_MVE(n,k) = ‖top-k of t‖₂` — the **L2 norm**.
- Always `t_MV ≤ t_MVE`, with equality only when the employed legs' t-statistics are identical.
  **Letting yourself weight signals by how well they backtested is strictly worse**, and the gap
  is the entire cost of that freedom.

**Critical values to actually use** (5%, from the paper's simulation on real returns with random
signals). These are the numbers to compare a multi-signal backtest against:

| construction | 5% critical \|t\| |
|---|---|
| single best of 10 candidates (pure selection) | ≈ 2.6 |
| best 2 of 10 | ≈ 3.5 |
| best 3 of 20 | > 4 |
| best 4 of 40 | ≈ 5 |
| best `k` of `n`, signal-weighted, `n` large | up to ≈ 7–8 |

Pure-overfitting critical values (`k = n`, no selection at all) already exceed the pure-selection
values across the whole range of `n` the paper simulates — **overfitting bias alone is worse than
the multiple-testing bias this folder already corrects for.**

**Two further results with direct design consequences:**

- **The marginal-inclusion rule.** Adding one more signal to an equal-weighted composite stops
  improving the backtest t-statistic once the new signal is **less than half as good as the
  average of the signals already employed**. This is a statement about *backtested* performance,
  so it is a warning, not a target: it describes when an overfitter stops adding.
- **`k ≈ n/2`, and what it reveals.** For a typical set of candidates, the composite that
  maximises the backtested t-statistic **equal-weights roughly the best half** and discards the
  rest. The corollary is a red flag you can apply to someone else's work — *and to your own*:
  **a multi-signal strategy that contains no mediocre legs is evidence that mediocre candidates
  were considered and dropped**, i.e. evidence of selection bias on top of overfitting bias. The
  expected t-statistic in that case runs about 60% above what it would be without the selection
  step.

**The author's recommended remedy, in his own order of preference.** First choice: evaluate the
**marginal** contribution of each leg individually — the alpha of each leg's strategy *relative
to all the others* — with a Bonferroni correction for at least the number of signals employed
and honestly for the number considered. Second choice: compare the composite's `t` against the
corrected thresholds above. His closing statement is the one to carry: *combine multiple signals
you believe in individually; never believe in a combination because it backtests well together.*

## Robustness evidence (qualitative only)

- The distributional results are **analytic**, with the Monte Carlo serving as confirmation
  rather than as the evidence. They do not decay, are not subject to publication bias, and carry
  no sample — the same standing this folder already grants the range-estimator theorems.
- The simulation uses real return data (so the cross-sectional correlation structure of actual
  stock returns is preserved) with 100,000 random signal sets per `(k, n)` pair.
- Robust to the portfolio construction: the appendix repeats everything for
  capitalisation-and-signal-weighted books, and the paper shows that z-score weighting, quantile
  sorting and rank weighting produce strategies explaining 97.8–99.6% of each other's return
  variation. **The critical values are not an artifact of one weighting scheme.**
- **Unreplicated and unpublished.** No independent replication is recorded, the citation count is
  modest, and it has been under review for an extended period. The author has a substantial track
  record in exactly this area (this folder already holds two of his papers). Tier B is the honest
  grade, and the analytic core is the part to lean on.

## Implementability here

This is a note about what the lab may **conclude**, not about what it may trade. Four
consequences, in descending order of bite:

1. **The lab's max-of-z result is outside this paper's algebra, and that is a real distinction,
   not a loophole.** Section 2.1.3 proves an **exact equivalence**: for a composite formed as a
   *linear* combination of signals, the resulting strategy's return is identical to a portfolio
   of the single-signal strategies held at the composite weights. Integration and mixing are the
   same object under linearity. That is precisely why `experiments/learnings.md`'s mean-operator
   ensembles were bounded by their legs (2026-08-30, and again in the closed-form tail-depth
   penalty `√((1 + (n−1)ρ)/n)` on 2026-08-31) — the bound is not an empirical regularity, it is
   this equivalence plus Markowitz. **The max operator is not a linear combination, so neither
   the equivalence nor the bound applies to it.** The lab discovered the boundary empirically;
   this source supplies the algebra for why the boundary is where it is. It also means the
   paper's critical-value table, all of which is derived for linear composites, **does not
   transfer numerically** to a max-of-z book.
2. **What *does* transfer, undiminished, is the selection half.** The max-of-z candidate selects
   four legs from a screened pool. The lab's own record says how large that pool is: eight
   screened `range-variance` mechanisms, several `liquidity-volume` volume functionals, the
   `statistical-arbitrage` residual grid, `DELAY`, the seasonal constructions, plus 57 legacy
   `price-trend` variants. **`k ≈ 4` chosen from `n` of order 20–30 puts the effective selection
   count in the `n^k` regime**, which is the paper's exponential result. The honest reading is
   not "the result is spurious" — the legs were each screened on their own train-split evidence
   first, which is exactly the practice the author endorses — but that **the composite's apparent
   margin over its legs cannot be given a conventional t-interpretation**, and the lab's own
   report of it (`0.88–1.01 as a range, never 1.008 as a point`) is the right instinct arrived at
   independently.
3. **The `k ≈ n/2` red flag applies to the lab's own construction.** The four legs in the
   integrated book are four *family leads* — by definition the best of their families, with the
   weaker members discarded. A composite containing no mediocre legs is the paper's stated
   signature of selection bias. The lab should expect the integrated book's edge over its legs to
   shrink out of sample for this reason alone, independent of any of its other discounts.
4. **A concrete, free procedure the lab can adopt tonight.** The author's first-choice remedy —
   *evaluate each leg's marginal alpha relative to all the others, Bonferroni-corrected for the
   number of signals considered* — is computable from stored trial return series with no new
   trial and no holdout read. It answers a question the lab currently cannot answer about the
   integrated book: **which legs are carrying it, and would any of them survive being priced
   against the other three.** If the integrated book's edge collapses to one leg, that leg is the
   candidate and the integration is decoration.

**One thing this note must not be read as saying.** The paper is explicit that combining signals
is fine and that efficient combinations of genuinely informative signals do have higher Sharpe
ratios. The prohibition is narrow and exact: *do not treat a composite's backtest as evidence
about the components.*

## Related

- **`research/notes/2026-08-31-signal-blending-vs-portfolio-blending.md`** — Fitzgibbons et al.
  argue that under a long-only constraint, integration (blend the signals, construct once) is
  structurally superior to mixing (construct per signal, then allocate). **This source proves the
  two are identical for linear composites of signal-weighted books.** The two are reconcilable
  and the reconciliation is worth stating: Fitzgibbons et al.'s gap comes entirely from the
  *long-only truncation*, which is a nonlinearity applied after the linear blend; Novy-Marx's
  equivalence is derived for untruncated signal-weighted books. **Strip the nonlinearity and the
  integration advantage vanishes** — which is a sharper statement of the same claim, and it
  predicts that the size of an integration advantage should scale with how binding the long-only
  constraint is. That is a checkable prediction, and Leippold–Rüegg's "much ado about nothing"
  rebuttal is what it looks like when the constraint is slack.
- **`experiments/learnings.md`, 2026-08-31 (the mean/max entry)** — the empirical shadow of the
  equivalence above. See consequence 1.
- **`research/notes/2026-08-24-multiple-testing-haircut.md`**, **`2026-08-24-deflated-sharpe-ratio.md`**,
  **`2026-08-17-mclean-pontiff-publication-decay.md`** — the selection-bias literature this
  folder already holds. This source's contribution is that **the deflated-Sharpe machinery, which
  corrects for trial count, does not correct for the signing-and-combining step at all.** The
  lab's protocol counts trials; it does not count signals inside a trial. A four-leg integrated
  candidate is one trial and carries a bias the trial count cannot see.
- **`research/notes/2026-08-19-model-averaging-mallows-weights.md`** and
  **`2026-08-17-forecast-combination-why-averaging-beats-selecting.md`** — the pro-averaging
  literature. The tension is only apparent: those sources are about *forecast accuracy* under a
  known loss function; this one is about *inference* on a backtest. Both can be right, and the
  practical synthesis is that averaging is a good estimator and a bad witness.
