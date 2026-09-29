---
title: "How many factors are in a panel — the three estimator families (Bai–Ng information criteria; Onatski's edge threshold; Ahn–Horenstein's eigenvalue ratio)"
authors: Bai, Ng; Onatski; Ahn, Horenstein
year: 2002; 2010; 2013
venue: Econometrica 70(1), 191–221 (Tier 1); Review of Economics and Statistics 92(4), 1004–1016 (Tier 1); Econometrica 81(3), 1203–1227 (Tier 1)
url: https://doi.org/10.1111/1468-0262.00273 ; https://doi.org/10.1162/REST_a_00043 ; https://doi.org/10.3982/ECTA8968
citations: "Bai–Ng 4116 (Semantic Scholar by DOI), 3152 (Crossref); Onatski 671 (Semantic Scholar), 711 (OpenAlex); Ahn–Horenstein 850 (Semantic Scholar), 794 (Crossref); all checked 2026-09-27"
sample_period: "Mostly Monte Carlo. Bai–Ng's application: monthly 1994.1–1998.12, survivorship-conditioned. Onatski's application: monthly 1983.1–2003.12, survivorship-conditioned. Ahn–Horenstein's applications were not read in detail."
markets: "Bai–Ng: 4,883 NYSE/AMEX/NASDAQ stocks (T = 60) out of 8,436, restricted to those with a complete history through the last trading day of 1998. Onatski: 1,148 NYSE/AMEX/NASDAQ stocks (T = 252), restricted to those traded for the whole sample. Simulations throughout span N, T from 10 to 8,000."
tier: A
validation_overlap: false
published_post_2018: false
---

**What was read.** Bai–Ng: the **typeset Econometrica article**, in full (from a course page at
`ssc.wisc.edu`). Ahn–Horenstein: the authors' **November 2008 working-paper version**, in full (from a
seminar page at `econ.biu.ac.il`); the published 2013 Econometrica text was not read, so section
numbers and simulation tables may not match the version of record, and the citation count above is for
the published DOI. Onatski: the **March 2005 Columbia discussion-paper version** (0405-19, via the
Columbia Academic Commons OA copy that OpenAlex lists as GREEN for the REStat DOI), in full; likewise
not the version of record. All three estimator definitions below are taken from the documents actually
read and are stated there in closed form.

**Why this folder is reading three econometrics papers about counting.** The 2026-09-26 nightly's
verdict on this file's top-ranked screen was that an imported effective-rank statistic
"**has a free parameter in its own input**" — de-duplicating the feature list moved the same universe
from one pre-registered branch to the other — and the human-facing note asked for "an invariance check
before an imported screen's branches are believed". This is the literature that spent twenty years on
that exact problem. The short answer it gives is worse than the lab feared and more useful than a fix:
**the count is not a property of the panel alone, it is a property of the panel *and* the estimator,
and when the non-factor part of the panel is cross-correlated the count is not identified at all.**

## Mechanism

All three start from the same asymptotic fact, from the approximate factor model
`X_it = λ_i' F_t + e_it`. If a factor is *pervasive* — its squared loadings summed over the
cross-section grow without bound in `N` — then exactly `r` eigenvalues of the sample second-moment
matrix diverge with `N` while the rest stay bounded. Counting factors is separating a diverging
sequence from a bounded one.

**And that problem is ill-posed in a finite sample.** Onatski quotes Forni et al. on this and does not
soften it: "there is no way a slowly diverging sequence (divergence under the model can be arbitrarily
slow) can be told from an eventually bounded sequence (for which the bound can be arbitrarily large)".
Every estimator below therefore adds an identifying restriction, and the three families differ in
*which* restriction they add — which is why they can and do disagree on one panel.

- **Bai–Ng: penalise dimension.** Choose `k` to minimise a fit-plus-penalty criterion. The insight
  that earned the paper its citation count is that when the factors are *estimated* rather than
  observed, a penalty that depends only on `T` (the classic AIC or BIC) is not enough — the penalty
  must be a function of **both** `N` and `T`, because `k(N + T − k)` parameters are being fitted from
  `NT` observations. Their Theorem 2 gives necessary-and-sufficient rate conditions on the penalty
  `g(N,T)`: it must vanish, and `C²_NT · g(N,T) → ∞` with `C_NT = min{√N, √T}`. AIC fails the second
  condition for all `N,T`; BIC in `T` alone fails it when `N ≪ T`.
- **Onatski: estimate the noise edge and count what clears it.** Rather than assuming the systematic
  eigenvalues are *large*, assume a law-of-large-numbers regularity for the idiosyncratic ones: the
  spectral distribution of the idiosyncratic second-moment matrix has a **bounded support**, and
  (Silverstein–Choi) its density near the upper edge `u` behaves like `a·sqrt(u − x)`. Fit that square
  root to the observed spectrum where the idiosyncratic eigenvalues live, extrapolate the edge, and
  count the eigenvalues above it. This is the same idea as the Marchenko–Pastur bulk fit of the
  companion note, but with the edge *estimated from the data* instead of from an i.i.d. assumption —
  which is what makes it work when the non-factor part is autocorrelated or heteroskedastic.
- **Ahn–Horenstein: look for the gap, not the level.** If `r` eigenvalues diverge and the rest are
  bounded, then the **ratio** of adjacent eigenvalues has a spike at `k = r` and nowhere else. No
  penalty, no threshold, no variance estimate, no calibration. They also show the ratio is not a new
  idea grafted on: `ER(k)` is exactly the ratio of successive *changes* in Bai–Ng's sum of squared
  residuals, so the ratio estimator is a re-reading of the same objective — and they note the
  diagnostic reason to prefer it, namely that the `PC`/`IC` criterion function rises after its kink
  much more gently than it fell before it, while the eigenvalue ratio is sharply peaked.

## Construction recipe

Let `λ₁ ≥ λ₂ ≥ …` be the eigenvalues of the sample second-moment matrix, and `m = min(N,T)`.
Standardize columns first (Bai–Ng demean and scale each series to unit variance before taking
eigenvectors; Ahn–Horenstein use time-demeaned data).

**Bai–Ng.** With `V(k)` the mean squared residual from `k` principal components and
`σ̂² = V(kmax)`:

```
PC_p1(k) = V(k) + k·σ̂²·((N+T)/(NT))·ln(NT/(N+T))
PC_p2(k) = V(k) + k·σ̂²·((N+T)/(NT))·ln(C²_NT),        C²_NT = min{N,T}
IC_p1(k) = ln V(k) + k·((N+T)/(NT))·ln(NT/(N+T))
IC_p2(k) = ln V(k) + k·((N+T)/(NT))·ln(C²_NT)
```

Minimise over `0 ≤ k ≤ kmax`. The `IC` forms are preferred in practice for one concrete reason: they
do not need `σ̂²` and therefore **do not depend on `kmax` through the penalty's scale**. `PC_p3` and
`IC_p3` (penalty `ln(C²_NT)/C²_NT`) are stated but reported as less robust at small `N` or `T`.
`kmax` has no principled rule in a panel; the authors suggest adapting Schwert's time-series rule with
`min{N,T}` in place of `T`.

**Onatski.** Fix `rmax` (the paper uses `rmax = [1.55·T^{2/5}] + 1`, which gives 15 at `T = 252`).
Then

```
û   = w·λ_{rmax+1} + (1 − w)·λ_{2·rmax+1},     w = 2^{2/3}/(2^{2/3} − 1) ≈ 1.702
r̂_δ = #{ i ≤ n : λ_i > (1 + δ)·û }
```

`û` is a consistent estimator of the idiosyncratic edge `u`, obtained by fitting the `sqrt(u − x)`
edge density to the stretch of the observed spectrum between `λ_{2rmax+1}` and `λ_{rmax+1}`; `δ > 0`
is a markup needed because the largest idiosyncratic eigenvalue is only guaranteed to lie *below* any
number exceeding `u`. Fixed `δ` gives strong consistency; `δ ∼ n^{−γ}` for small enough `γ` is
conjectured and partly proved. The cruder variant `r̃_δ = #{i : λ_i > (1+δ)·λ_{rmax+1}}` is also
consistent but needs a larger `δ`, hence has worse finite-sample behaviour. **Five lines of code.**

**Ahn–Horenstein.** With `μ_k` the `k`-th eigenvalue of `XX'/(NT)` and
`μ*_k = μ_k / Σ_{j>k} μ_j`:

```
ER(k) = μ_k / μ_{k+1}                           → r̂_ER = argmax_{k ≤ kmax} ER(k)
GR(k) = ln(1 + μ*_k) / ln(1 + μ*_{k+1})         → r̂_GR = argmax_{k ≤ kmax} GR(k)
```

Two riders that matter. **To allow `r = 0`**, prepend a mock eigenvalue
`μ̃_0 = w(N,T)` for any sequence with `w(N,T) → 0` and `w(N,T)·m → ∞` — the version read states the
requirement rather than fixing a choice, so pick one and write it down — and include the extra ratio
`μ̃_0/μ_1` in the maximisation — otherwise the estimator cannot return zero and will always
find at least one factor. **The ratio need not be single-peaked**: when factors have different
signal-to-noise ratios the locus has multiple peaks and **the first peak is not necessarily the
maximum**, so the argmax must be taken over the whole range rather than read off the first spike.
A `kmax`-free variant (`LR`, the log-ratio estimator) exists and is consistent, but its finite-sample
behaviour depends on an arbitrary multiplicative constant the authors leave open.

## Robustness evidence (qualitative only)

- **All three are consistency theorems with extensive Monte Carlo, across `N` and `T` from 10 to
  8,000, homo- and heteroskedastic errors, autocorrelated errors, cross-correlated errors, equal and
  unequal factor strengths, and (for `ER`) the `r = 0` case.** The simulation designs are shared
  across the three papers — Ahn–Horenstein explicitly reproduce "the benchmark table reported in both
  BN and Onatski" — so the comparisons are like-for-like, which is rare.
- **The ordering that emerges, and it is the transferable part.** With i.i.d. errors everything works
  above modest sample sizes (Bai–Ng report their criteria precise once `min{N,T} ≥ 40`, and inadequate
  below that). Introduce **autocorrelated** errors and the `IC`/`PC` criteria degrade as the
  autocorrelation rises, while `ER`, `GR` and Onatski hold up. Introduce **cross-sectionally
  correlated** errors and `IC`/`PC` **overestimate** the number of factors unless the cross
  correlation is very weak — and, crucially, *more time-series observations do not fix it*:
  Ahn–Horenstein report the `IC`/`PC` estimators performing **worse as `N` increases** at `T ≤ 100`,
  and no better at `(N,T) = (1000,500)` than at `(1000,50)`. `ER`/`GR` are also reported as
  insensitive to `kmax` (the same answer at `kmax = 8` and `kmax = 90` for `N = T = 100`), which
  `IC`/`PC` and Onatski are not at small samples.
- **Weak factors are where the ordering reverses, and where the honest warning lives.** Onatski's
  estimator is designed to detect factors whose share of variance is small, and is reported as better
  powered for them; `ER` and `GR` can miss them when the strong and weak signal-to-noise ratios differ
  a lot (`GR` less so than `ER`). But Ahn–Horenstein then measure something more important than the
  count: in a design with a genuinely weak third factor, **even when an estimator returns the right
  number, the third principal component is the one most correlated with the true third factor only
  about a quarter of the time** — in their run, 26%, against 28% for the fourth PC and 44% for the
  fifth. The first two PCs always matched the two strong factors. **A weak factor can be counted and
  still not be identified.**
- **On real stock returns the estimators disagree by a factor of four.** Onatski's application
  (monthly, 1,148 survivors, `T = 252`, `rmax = 15`) returns **8** for all three of his `δ` settings,
  while Bai–Ng's own four preferred criteria on the same data return **6, 5, 4 and 3**; Bai–Ng's own
  application (`N = 4883`, `T = 60`) returns **2**. Onatski attributes the gap to sample length and to
  his method's greater power against weak factors. Earlier literature he surveys spans one to six.
  **This is the single most useful fact in the cluster for this repo: five defensible estimators, one
  panel, answers from 3 to 8.** Recorded as a spread of estimates, not as a performance claim.
- **Sample-robustness discount, and it is the same one this repo lives with.** Both empirical panels
  are **survivorship-conditioned by construction** — Bai–Ng keep firms with a complete history through
  the last trading day of their sample, Onatski keeps stocks "traded during the whole sample period".
  So the applications inherit exactly the bias `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`
  documents, and the counts above should be read as counts *on a survivor panel*.
- **Nothing here is about returns.** These are second-moment results. No risk premium, no
  performance, no cost model anywhere in the cluster — which is why the tier is A on methodology and
  why nothing in this note can be used to justify expecting a strategy to pay.

## Implementability here

**Free, diagnostic, and this is the note that says what the lab's failed screen should be replaced
with.** No trial is implied by anything below.

- **The replacement for `EffRank` as a "how many directions" statistic is `ER`/`GR`, and the reason is
  specific rather than aesthetic.** `EffRank = (tr A)²/tr(A²)` is a smooth functional of the *whole*
  spectrum, so every near-duplicate column moves it. `ER(k) = μ_k/μ_{k+1}` reads two adjacent
  eigenvalues and asks where the gap is. It needs no `σ̂²`, no penalty, no `kmax` tuning, and it is
  scale-invariant in a way `EffRank` is not. It will not make the duplication problem disappear — see
  the next point — but it localises the answer instead of averaging the contamination over the whole
  spectrum, and it can be computed on the identical matrix the lab already built.
- **The duplication problem has a name in this literature and it is an identification failure, not a
  nuisance.** Onatski's Assumption 4(iii) is the condition his method needs, and he says exactly what
  violates it: the method "will break down" when "a handful of linear combinations of `ε_t` explain a
  disproportionately large part of the variation in the idiosyncratic term, which makes these
  combinations look very much like common factors". **Three nested momentum legs and four
  volatility/range estimators in a fourteen-column feature panel are that handful, by construction.**
  He calls the assumption "a basic identification assumption", because without it we are back to
  telling a slowly diverging sequence from a bounded one. The consequence for the lab is cleaner than
  its 2026-09-26 verdict: it is not that `EffRank` in particular has a free parameter, it is that
  **on a panel with duplicated columns no eigenvalue-based count of dimensionality is identified**,
  and swapping in a better estimator does not repair that. The honest fix is to de-duplicate the
  *design* — one column per mechanism, chosen before any spectrum is computed — and then report the
  count as conditional on that list, which is what the nightly's own next-idea 1 already proposes.
- **Dimensions here, and they are unfavourable in a way worth stating before anyone runs this.** The
  instrument panel is `N ≈ 145`. Bai–Ng need `min{N,T} ≥ 40` — satisfied. But `ER`/`GR`'s edge over
  `IC`/`PC` is largest, and `IC`/`PC`'s cross-correlation bias is worst, exactly in the
  `N ≈ 100–200`, `T ≈ 50–250` corner this repo lives in. On the **feature** panel (`P ≈ 8–14`
  managed portfolios) all of these asymptotics are simply out of range: `ER` with `kmax` of order `P`
  on a 14-column panel is not the object the theorems describe, and a count from it should be reported
  with that said, or not reported.
- **The weak-factor result is a direct warning about every PCA-residual construction in this repo.**
  `learnings.md` [2026-09-25] records residual-reversal work at `K = 3` and `K = 5`, and
  `SUMMARY.md` #152 already establishes that under long-only those extra legs are unhedged rather than
  removed. Ahn–Horenstein add the estimation half: at plausible sample sizes **the third, fourth and
  fifth principal components are not reliably the third, fourth and fifth factors** — the identity of
  a weak PC is close to a coin flip even when the count is right. So `K > 2` is not just an unhedged
  exposure, it is an unhedged exposure to a *direction that is not the one named*. `K = 1` and `K = 2`
  are the only PCs the simulations report as always matching their intended factors.
- **The three-estimator spread is itself the screen worth running, and it is free.** Compute `IC_p1`,
  `IC_p2`, Onatski's `r̂_δ` and `ER`/`GR` on the same matrix. If they agree, the count is a property of
  the panel; if they span a range (as they do on real monthly returns), it is a property of the
  estimator and **no branch of any pre-registered screen conditioned on the count may fire**. This is
  the "invariance check before an imported screen's branches are believed" that the 2026-09-26 nightly
  asked for, in the cheapest available form: four one-line statistics on a matrix already in memory,
  with the disagreement itself as the verdict. Fix the estimator list and the de-duplicated column
  list **in writing before computing any of them**, or the choice of estimator becomes the new free
  parameter.
- Long-only, costs, turnover and the 25% cap are all irrelevant here; nothing is traded.

## Related

- `notes/2026-09-27-marchenko-pastur-noise-null-for-correlation-spectra.md` — the i.i.d. version of
  Onatski's edge, and the parameter-free eigenvector test that survives when the count does not.
- `notes/2026-09-27-nonlinear-shrinkage-instead-of-counting.md` — the position that the count is the
  wrong question, plus the long-only result that spoils the answer.
- `notes/2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` and
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md` — the same "count the independent directions" problem in the multiple-testing setting, where the lab's
  pre-registered control already disqualified the Kaiser `λ ≥ 1` rule for returning 44 on 90
  independent series. Kaiser is the crudest member of the family above.
- `notes/2026-08-21-effective-number-of-bets-diversification-measurement.md` — `EffRank`'s home.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the bias both empirical
  applications above carry.
- `notes/2026-09-26-large-factor-models-aipt-complexity.md` — the source of the eigenvalue-spectrum
  theorem whose screen (#153) the lab disqualified; this note is why the disqualification generalises.
- `experiments/learnings.md` [2026-09-26] — `EffRank`'s free parameter, and the tenth instance of
  "check the statistic is invariant to the thing it is not supposed to measure".
- `experiments/learnings.md` [2026-09-25] — the `K = 3` / `K = 5` PCA residual readings.
