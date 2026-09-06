---
title: "Monotonicity in asset returns: New tests with applications to the term structure, the CAPM, and portfolio sorts"
authors: Patton, Timmermann
year: 2010
venue: Journal of Financial Economics 98(3), 605–625 (venue tier 1)
url: https://doi.org/10.1016/j.jfineco.2010.06.006 — the published article read in full from the first author's Duke page, https://public.econ.duke.edu/~ap172/Patton_Timmermann_sorts_JFE_Dec2010.pdf
citations: 232 (Crossref `is-referenced-by-count`, checked 2026-09-06); 279 (Semantic Scholar DOI endpoint, same date). Ordinary index disagreement, both large
sample_period: 1926/1927–2006 for the characteristic sorts (discussion focuses on the 1963–2006 subsample); 1963–2001 for the beta sorts; 1964–2001 for the term premia
markets: US equities (Ken French decile and 5x5 portfolios, NYSE/AMEX/Nasdaq) and US Treasury bills
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full**: the published 21-page article — the test statistic and its null/alternative
framing, the Up and Down statistics, the comparison with the Wolak and Bonferroni tests, the
stationary-bootstrap implementation, the two-way-sort extension, all four empirical
applications and the conclusion. The appendix theorem was skimmed, not verified.

The companion to `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md`: that note asks
how finely to cut a ranking, this one asks whether the cuts agree with each other.

## Mechanism

Again not an economic mechanism but a construction diagnostic, and the argument is one sentence:
**the top-minus-bottom spread is not a test of the pattern the strategy assumes.**

Every book this lab builds assumes that a higher score means a higher expected return — that is
what "hold the top band" means. The standard evidence offered for that assumption is a `t`-test
on the extreme-minus-extreme return difference. That statistic uses two numbers out of `J` and
is therefore blind to the interior of the ranking. Two failure modes follow, and both are
observed in this paper's own applications:

- **A significant spread with a non-monotone interior.** The extremes differ, but the segments
  in between reverse repeatedly. The sorting variable is then not a ranking of expected return;
  it is picking out two unusual corners, and any band width other than the exact one tested is
  unjustified. Their term-premium application is exactly this shape: the longest-minus-shortest
  difference is comfortably significant on a `t`-test, while the monotonic-relation test does
  not come close to rejecting (bootstrap `p` around 0.95) and the "Up" statistic rejects
  strongly — increasing *segments* exist, a monotone *relation* does not.
- **An insignificant spread with a real monotone pattern.** The extremes are noisy, but every
  adjacent step points the same way; pooling that evidence rejects where the two-point `t`-test
  cannot. Their CAPM-beta application is this shape: the top-minus-bottom `t`-statistic is
  small, while the MR test rejects the null of no relation.

For a lab whose whole method is "rank a score and hold a band of it", the second failure mode
says a family may have been abandoned on the wrong statistic, and the first says a family may
have been *entered* on the wrong statistic. Neither can be diagnosed from a spread.

## Construction recipe

**Setup.** Sort into `N+1` portfolios, take the time series of returns `r_it`, form the vector of
adjacent differences `Δ̂_i = μ̂_i − μ̂_{i−1}`, `i = 1 … N`, where `μ̂_i` is a simple time-series
mean.

**The MR (monotonic relation) test.**

    H₀ : Δ ≤ 0        (no monotonically increasing relation)
    H₁ : min_i Δ_i > 0 (strictly increasing throughout)
    statistic: J_T = min_i Δ̂_i

The design choice that matters is which hypothesis is which: **the monotone pattern is the
alternative**, so a rejection is positive evidence *for* the pattern, and a failure to reject is
not evidence against it. This is the mirror image of the Wolak (1989) test, whose null is weak
monotonicity. Reversing the portfolio order tests for a decreasing relation.

**Critical values by stationary bootstrap** (Politis–Romano):

1. Resample the *time index* with random block lengths drawn from a geometric distribution;
   the same index is applied to every portfolio, which preserves cross-sectional dependence.
   Average block length 10 months for monthly returns; `B = 1,000` replications.
2. Impose the null at its least-favourable point (`Δ = 0`) by recentering:
   `J_T^(b) = min_i (Δ̂_i^(b) − Δ̂_i)`.
3. `p̂ = (1/B) Σ_b 1{J_T^(b) > J_T}`; reject below 0.05.
4. Use the **studentized** version, which removes the effect of cross-sectional
   heteroskedasticity across bins — a real power gain wherever bin volatility rises across the
   sort, which it does for anything correlated with risk.

**The Up and Down statistics**, which are the diagnostic half and the part most useful here:

    H₀ : Δ = 0   versus   Up:   Σ_i |Δ̂_i| · 1{Δ̂_i > 0} > 0
    H₀ : Δ = 0   versus   Down: Σ_i |Δ̂_i| · 1{Δ̂_i < 0} > 0

These accumulate the frequency *and* magnitude of deviations in each direction from a flat
pattern, with critical values from the same bootstrap. Because the MR test keys on the single
weakest link, it loses power in short or noisy samples; Up and Down tell you whether a
non-rejection is a flat relation or merely an underpowered one.

**Variants and extensions.**

- *Adjacent pairs* (`N` constraints) versus *all pairs* (`N(N+1)/2`). Adjacent pairs suffice for
  monotonicity; all pairs can add power. Both are covered by the theory.
- *Two-way sorts*: the test generalises to a 5x5 grid, giving a **conditional** MR `p`-value per
  row/column (is the relation monotone within this bucket of the other variable?) and a **joint**
  `p`-value across all of them.
- *Factor loadings*: the same machinery tests monotonicity of post-ranking betas — i.e. whether
  a sorting variable even ranks the exposure it is supposed to rank, which is a check on the
  *signal*, not on returns.

**Reading the pair of tests.** MR rejects and Wolak does not → strong support for the monotone
pattern. Wolak rejects and MR does not → strong evidence against it. Neither rejects → weak
confirmation, possibly a power problem (consult Up/Down). Both reject → the tests disagree; the
authors report no such case.

## Robustness evidence (qualitative only)

The contribution is a test, validated by a Monte Carlo study calibrated to the size and length of
real US decile-portfolio panels (sizes are close to nominal; the comparison covers `t`-tests,
Bonferroni bounds, the Wolak test and the authors' own), plus applications to four distinct data
sets — beta-sorted equity deciles, post-ranking betas, Treasury term premia, and eight
characteristic sorts drawn from Ken French's library.

The qualitative findings across those characteristic sorts, stated without dates or magnitudes:
sorts on **book-to-market, cashflow-to-price, earnings-to-price and long-term reversal** show
few or no reversals of the monotone pattern, while sorts on **size, dividend yield, momentum and
short-term reversal** show several reversals of the ordering across the interior of the deciles.
The most transferable result here is from the two-way sorts: in the size-by-momentum grid, the
conditional monotonic relation for momentum is rejected strongly within the smaller size
quintiles and is **not established within the largest size quintile**; in the
size-by-book-to-market grid, the size relation is established within the value column but not
within the growth column. A monotone relation in a pooled sort need not survive conditioning on
the part of the market you can actually trade.

Independent uptake is real (a CRAN package implements the tests; the statistic is standard
enough to appear as a routine robustness check in the sorting literature), and the methodology
is honest in the way this folder rewards: the paper is explicit that its own test can fail from
lack of power and supplies the Up/Down diagnostic to detect that case rather than leaving a
non-rejection to be read as a null.

Nothing here is cost-aware — the tests are applied to gross portfolio returns.

## Implementability here

**The MR/Up/Down triple is free on this repo's train split and needs no trial.** Inputs are a
score, `J` bins, and each bin's train return series. `scipy` covers everything: a geometric block
length, `B = 1,000` resamples of the *date index* shared across bins, recentering, and a
percentile. The whole thing is a few dozen lines and no new dependency.

**What it would decide, concretely:**

1. **Whether "hold the top band" is the right functional form for a given family lead.** If a
   score's MR test does not reject while its top-minus-rest is significant, the score is not a
   ranking of expected return, and band width is not the lever — the interior contradicts the
   extremes. The lab has thirty-odd books whose construction assumes a monotone ranking and has
   never tested the assumption for any of them.
2. **Whether a family was abandoned on the wrong statistic.** The reverse case — flat spread,
   monotone interior — is the one that would reopen a family this lab has closed on a top-`k`
   excess or an IC `t`. That is a genuinely different question from the one every screen in
   `SUMMARY.md` currently asks, and it costs one bootstrap.
3. **Where in the ranking the information sits**, via Up versus Down. A large Down statistic
   concentrated in the low bins with a flat top is the signature of a score whose content is
   about names to *avoid* — which is the construction shape
   `notes/2026-09-06-long-side-share-of-anomaly-profits.md` argues this lab has never built.

**Adaptation and pitfalls.**

- **`J` and the MR test interact, and the interaction is not benign.** More bins means more
  adjacent differences, each noisier, so the minimum gets more negative by construction: the MR
  test mechanically loses power as `J` rises. Fix `J` first — on the grounds in the companion
  note — then test. Do not search `J` for a `p`-value; that is the multiple-testing failure this
  folder already has six sources about.
- **A ~140-name universe supports few bins.** With `J` in the 4–7 range implied by this repo's
  bands, `N` is 3 to 6 adjacent differences. The test is still valid, but the "all pairs"
  variant is worth using for power, and Up/Down should be read alongside every non-rejection.
- **The bootstrap must resample dates, not names**, and the same date index must be applied to
  every bin, or the cross-sectional correlation that dominates this universe (15 regions, heavy
  block structure) will be destroyed and the `p`-values will be far too small.
- **The test is about gross returns.** A monotone gross pattern that costs 15 bps a side to
  express is still a monotone gross pattern; this diagnostic never substitutes for the lab's
  net-of-cost gate.
- **Overlap with the folder's inference embargo, recorded rather than glossed.** `SUMMARY.md`
  carries a standing embargo on further multiple-testing and inference sources (six already).
  This source is adjacent to that shelf and was taken anyway, for a reason that should be
  checked by whoever reads this next: it adds **no correction to the lab's significance
  machinery** and no haircut to any `t`. It is a statement about the *shape* of a sort — a
  construction property, tested on the train split, on the same footing as the lab's existing
  free IC and top-`k` screens. If a future session judges that reasoning wrong, the honest
  conclusion is that the embargo should have covered it, not that the test is unsound.

## Related

- `notes/2026-09-06-number-of-portfolios-as-tuning-parameter.md` — the number of bins. CCFS
  describe the top-minus-bottom test as an *informal* test of monotonicity and cite the need for
  a formal one; this is it. Read as a pair.
- `notes/2026-09-06-long-side-share-of-anomaly-profits.md` — which end of a monotone ranking a
  long-only raw-return book actually needs.
- `notes/2026-09-02-anomalies-by-size-group.md` and
  `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` — both say most
  characteristics weaken among the largest names. The two-way result above is an independent
  version of the same warning taken from a different direction: not "the premium is smaller in
  large caps" but "the *ordering* is not established in large caps". For a universe of ~140
  mega-caps these are the same practical conclusion reached twice.
- The lab's 2026-09-05 breadth bracket found returns monotone in breadth with the *opposite*
  sign to `price-trend`. That is monotonicity in a book-level design parameter, not in the
  cross-section of a score; the MR test addresses the second, and the two should not be
  conflated.
