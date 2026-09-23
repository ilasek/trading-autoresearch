---
title: "Testing for Mean-Variance Spanning with Short Sales Constraints and Transaction Costs"
authors: de Roon, Nijman, Werker
year: 2001
venue: Journal of Finance 56(2), 721–742 (venue tier 1)
url: https://doi.org/10.1111/0022-1082.00343
citations: 299 (Semantic Scholar by DOI, checked 2026-09-23); Crossref 214 for the same DOI (checked 2026-09-23). OpenAlex not consulted — daily free budget exhausted (HTTP 429, "Insufficient budget"). Read in full from the Tilburg University repository copy of the version of record, `pure.uvt.nl/ws/portalfiles/portal/429652/roonijwer1.pdf`.
sample_period: 1985–1996 (the empirical application only; the contribution is an econometric construction)
markets: 17 emerging-market indices from the IFC Emerging Markets Data Base against developed-market benchmark indices; monthly
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

Huberman–Kandel's spanning conditions assume an investor who can short freely and trade for
nothing. **This lab is long-only at gross ≤ 1.0 and pays 15 bps a side.** This paper is the one
that says what changes, and the change is structural rather than a correction term.

**1. The equality becomes an inequality.** Frictionless spanning is the statement that the
mean-variance stochastic discount factor which prices the benchmark assets also prices the new
assets: `E[m(v) r] = i_N`. When the investor cannot short the new assets, the pricing condition
weakens to

```
E[m(v)ₜ₊₁ rₜ₊₁]  ≤  i_N          (componentwise)
```

because an asset that is *over*priced relative to the benchmark's kernel cannot be exploited —
the correcting trade is the one you are forbidden. In regression form, with
`r = a(v) + B(v) R^(v) + ε`, the intersection restriction for a given `v` becomes

```
v · a(v) + (B(v) i_L − i_N)  ≤  0
```

i.e. **a one-sided restriction on the (zero-beta-adjusted) Jensen alpha** of the new asset
against the benchmark's efficient portfolio. Only a positive alpha is evidence against spanning.
A negative alpha, which under the frictionless test would reject spanning just as loudly, is
under the constraint **perfectly consistent with spanning** — you would have wanted to short it
and you cannot, so it changes nothing you can hold.

**2. The benchmark shrinks to its unbinding subset, and this is the subtle half.** Under
short-sale constraints the Kuhn–Tucker conditions of the mean-variance problem say the efficient
portfolio for a given risk aversion is *identical to the unconstrained efficient portfolio of
only those assets whose constraints do not bind*. Write `R^(v)` for that `L`-dimensional
subvector. The mean-variance kernel that prices the constrained set is linear in `R^(v)` alone —
not in the full benchmark `R`. **So the right-hand side of the spanning regression is the set of
positions the constrained investor actually holds**, not the full menu they were offered.

**3. The constrained frontier is a finite union of unconstrained frontiers.** As risk aversion
varies, the identity of the unbinding subset changes, but only finitely often. Index the
distinct subsets `j = 1, …, M` with return vectors `R^[j]`. The constrained frontier of `R` is
made of pieces of the unconstrained frontiers of the `R^[j]`, and spanning of `r` by `R` holds
if and only if the restriction holds in **each** of the `M` regressions

```
r = a^[j] + B^[j] R^[j] + ε^[j]      with     a^[j] v + B^[j] i^[j]  ≤  i_N   for all v ∈ V^[j]
```

Because the restriction is linear in `v` on each segment, checking it at the two endpoints
`v_min^[j]` and `v_max^[j]` suffices for the whole segment. Spanning becomes a finite
collection of one-sided intersection tests rather than one two-sided joint test.

**4. Transaction costs enter by splitting every asset in two, not by subtracting a number.**
Following Luttmer, let `τ^l_i` and `τ^s_i` be the multiplicative haircuts on a long and a short
position in asset `i`. Replace the `K` assets by a `2K`-vector whose first `K` entries are
`τ^l_i R_i` (long-position returns) and whose last `K` are `τ^s_i R_i` (short-position returns),
then impose *no shorting* on the first block and *no going long* on the second. Costs are now a
short-sale-constraint problem in a doubled asset space, and the same inequality machinery
applies unchanged. The spanning conditions become a pair:

```
E[ m̄^[j](v) r̄ˡ ] ≤ i_N     and     E[ m̄^[j](v) r̄ˢ ] ≥ i_N     for all j
```

**The economic content of this construction is the paper's headline and it is the part to
carry:** diversification benefits that are clearly present in the frictionless test can be
absent once the investor cannot short, and can be absent again once even *small* proportional
costs are charged. The unconstrained spanning rejection is an upper bound on what a constrained,
cost-paying investor can actually take.

## Construction recipe

For the case that matters here — `K` benchmark assets you hold long-only, `N = 1` candidate you
can only hold long, proportional costs:

1. **Build cost-adjusted return series first.** Multiply each position's gross return by its
   round-trip haircut in the direction actually traded. Do this before any regression; the test
   is defined on the returns an investor can actually realise, not on paper returns with a cost
   footnote.
2. **Identify the unbinding benchmark subset(s) `R^[j]`.** Solve the long-only mean-variance
   problem over a grid of risk aversions; each distinct support set is one segment `j`. In the
   common special case where there are short-sale constraints on the *candidate only* and not on
   the benchmark, `R^[j] = R` and there is a single segment — the regression is the ordinary one.
3. **Run the regression(s)** `r = a^[j] + B^[j] R^[j] + ε^[j]` and form the vector of Jensen
   alphas `α_J(v)` of the candidate relative to the constrained-efficient benchmark portfolio
   with zero-beta return `1/v`.
4. **Test the inequality with a one-sided Wald statistic** (Kodde–Palm):

   ```
   ξ(v) = min_{α_J(v) ≤ 0} ( α̂_J(v) − α_J(v) )' Var[α̂_J(v)]⁻¹ ( α̂_J(v) − α_J(v) )
   ```

   Under the null this is distributed as a **mixture of χ² distributions**,
   `Pr{ξ ≥ c} = Σᵢ Pr{χ²ᵢ ≥ c} w(N, i, Var[α̂_J])`, where the weights are the probabilities that
   `N − i` of the `N` elements of a `N(0, Var[α̂_J])` draw are strictly negative. The weights can
   be obtained by simulation (Gouriéroux–Holly–Monfort); Kodde–Palm also give p-value bounds that
   avoid computing them. **With `N = 1` the mixture is just `½·χ²₀ + ½·χ²₁`** — a one-sided test.
5. **For spanning rather than intersection**, repeat at `v_min^[j]` and `v_max^[j]` for every
   segment and require all of them to pass.

**Estimating `R^[j]` rather than knowing it does not break the test.** The paper's appendix shows
the limit distribution of the Wald statistic is unaffected by having to infer the unbinding set
from the sample, provided the relevant efficient portfolio has no weight exactly at zero.

## Robustness evidence (qualitative only)

- **Monte Carlo evidence on size, reported in both directions.** With short-sale constraints on
  the *new* asset only, finite-sample rejection rates are almost indistinguishable from the
  asymptotic ones — the test is usable at samples as short as five years of monthly data. With
  constraints on the benchmark as well, and the unbinding subset estimated, the test
  **under-rejects**: rejection rates are always below the asymptotic level and rise monotonically
  with sample length, reaching acceptable accuracy by about ten years of monthly data. The bias
  is conservative, which is the right direction for a promotion gate.
- **Power is essentially unaffected by the constraint.** The simulated power functions for the
  frictionless test, the constraint-on-new-asset-only test, and the constraint-on-everything
  test lie close together; estimating the unbinding set costs only a little.
- The paper is honest about the alternative it displaces: **Glen and Jorion's intersection test
  with short-sale constraints is built on a difference of Sharpe ratios and has no known
  distribution.** The contribution here is a statistic with one. It also avoids assuming a
  riskless asset exists, and extends to spanning rather than only intersection.
- Independently corroborated in structure by the stochastic-discount-factor literature: a
  frontier shift is equivalent to a shift in the Hansen–Jagannathan volatility bound, and the
  constrained kernel derived here is the minimum-variance kernel among those that price the
  constrained set — so the duality survives the frictions.
- **Limitation**: unconditional spanning only (the authors note the conditional extension is
  straightforward but do not do it), constant `a` and `B`, and proportional costs only — no
  fixed costs, no impact, no capacity.
- **Limitation**: the empirical application is a diversification question about one asset class
  against another. Nothing about *that* application transfers; the construction does.

## Implementability here

**This is the note that matters most for a long-only lab, and its first consequence is a free
correction to how the lab reads any spanning diagnostic it runs.**

- **The test the lab should run is one-sided, not two-sided.** If the lab adopts tonight's
  step-down diagnostic (see the Kan–Zhou note), the `α` restriction should be tested as
  `α ≤ 0`, not `α = 0`, because the lab cannot short the candidate. Practically: with `N = 1`
  the null distribution is `½·χ²₀ + ½·χ²₁`, which **halves the p-value of a positive alpha**
  relative to the two-sided test. This is a genuine power gain, and it comes from the
  constraint rather than in spite of it — a rare direction for a constraint result in this
  folder, and worth noticing given how much of Kan–Zhou's message is that power is scarce.
- **A negative alpha is not evidence.** Under the constraint, a candidate with a *negative*
  alpha against the champion is spanned, full stop. `experiments/journal.md` records a scout
  (`lv_illiq_evar_signflip`) whose whole content was a mis-signed leg losing 0.217 with a
  resolvable `t = −2.38`. Under the frictionless reading that is a strong rejection of spanning;
  under the correct long-only reading it is **the null holding**. The sign falsifier remains a
  valid identification device — it distinguishes a mechanism from an artifact — but it is not a
  spanning rejection and should not be reported as one.
- **The benchmark for the regression is the champion's *held* book.** The champion runs a
  hold-25/enter-15 band over a 140-name universe, so on any given day most of the universe is at
  weight zero: constrained. The paper's `R^(v)` construction says the pricing kernel is linear in
  the unbinding positions. For a lab that treats the champion as a *single* return series
  (`K = 1`), this is automatically satisfied — the champion's realised return already embodies
  its own constrained optimum — and the single-segment simplification applies: short-sale
  constraints on the candidate only, `R^[j] = R`, one regression, and (per the simulation
  evidence) no small-sample size problem. **Use the champion's realised net return series as the
  benchmark, not a reconstructed menu of the instruments it chooses from.** The second would
  drag in the multi-segment machinery for no gain.
- **Costs belong inside the return series, which is already how this repo works.** The engine
  applies 15 bps a side and a 1-day lag before returns are recorded, so the stored champion and
  candidate series are already `τ`-adjusted in the paper's sense. One caveat: the paper's
  doubled-asset construction charges the *marginal* trading a new position induces. A spanning
  test run on two separately-costed books understates the cost of holding them together only if
  their trades offset; with a long-only, non-overlapping-signal pair they mostly will not.
- **Expect the constrained verdict to be weaker than the frictionless one, and treat that gap as
  information rather than disappointment.** The paper's central empirical lesson, in permitted
  form, is that a frictionless test can find a clear frontier improvement where the constrained,
  cost-paying test finds none — and that *small* costs are enough to do it. The lab's own
  fifteen-session blend decline is the same shape measured with a different instrument.
- **Pitfall — do not use the mixture distribution and then also choose the side after looking.**
  The one-sided gain is real only if the direction is fixed in advance. The lab already has the
  discipline for this (pre-registered sign falsifiers); it applies here verbatim.
- **Pitfall — `N = 1` per test, but several candidates is several tests.** The mixture weights
  are defined for a vector of alphas; running the diagnostic on seven family leads one at a time
  is seven one-sided tests and the folder's multiple-testing material applies.

## Related

- **`research/notes/2026-09-23-mean-variance-spanning-and-intersection.md`** — the frictionless
  hypotheses this paper generalises.
- **`research/notes/2026-09-23-spanning-test-power-and-step-down.md`** — the power analysis. The
  two interact: Kan–Zhou say the tangency channel is nearly undetectable two-sided; this paper
  says a long-only investor's version of that test is one-sided, which buys some of it back.
- **`research/notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`** — Stambaugh–Yu–Yuan's
  finding that most of a published cross-sectional spread sits on the leg a long-only book
  cannot hold. That is the *economic* version of this paper's *econometric* point, and the two
  should be read together: the short leg is where the effect is, and the short leg is also where
  the spanning test's evidence is thrown away.
- **`research/notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md`** and
  **`research/notes/2026-08-17-naive-vs-optimized-weighting.md`** — the folder's standing
  "constraints are estimators as well as leaks" position. This note is a case where the
  constraint is unambiguously a leak on the economics and unambiguously a *gain* on the
  statistics.
- **`experiments/learnings.md` [2026-09-22]**, trial #97 — the mis-signed leg. Reread under this
  note: `t = −2.38` against the champion is the long-only null holding, not a rejection.
