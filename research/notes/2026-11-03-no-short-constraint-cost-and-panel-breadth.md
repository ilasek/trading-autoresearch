---
title: "Portfolio Optimization with Many Assets: The Importance of Short-Selling" (published as "Mean–variance efficient portfolios with many assets: 50% short")
authors: Levy, Ritov
year: 2001 (working paper read); published 2011
venue: Quantitative Finance 11(10), 1461–1471 (peer-reviewed, Tier 2 for this folder's purposes — not a top finance journal); working version UCLA Anderson School working paper 7-01, May 2001
url: https://doi.org/10.1080/14697688.2010.514282 — working version read in full from `anderson.ucla.edu/documents/areas/fac/finance/7-01.pdf`
citations: 17 (Crossref `is-referenced-by-count` on the Quantitative Finance DOI, checked 2026-11-03); 19 (OpenAlex, same date). Semantic Scholar returned HTTP 429. The count is low for the paper's age, and is the main reason this is Tier B rather than higher — see Robustness.
sample_period: 1979–1999 (monthly CRSP, 200 firms with complete records over the period — survivorship-conditioned and acknowledged as such by the authors), plus simulations with randomly drawn covariance matrices and the analytic results, which have no sample
markets: US equities (CRSP), portfolios of up to 200 names
tier: B
validation_overlap: false
published_post_2018: false
---

Taken as the second source for the aim the [2026-11-02] open-questions entry set — *how is
the short leg's absence handled* — and it answers a question the first source
(`2026-11-03-attainable-underweight-and-the-long-only-constraint.md`) does not touch: **what
the long-only constraint costs as the panel gets wider.** That is a live question for this
lab specifically, because protocol v2 replaced a ~140-name panel with a ~1,400-name one and
nobody has asked what a long-only book can do with the extra breadth.

Zero prior coverage: greps across 255 notes returned `Levy, Ritov` **0**, `many assets` and
`importance of short-selling` **0**.

## Mechanism

Four results, of which the third and fourth are the ones that matter here.

**(1) In a mean–variance optimal portfolio of many assets, about half the assets are held
short.** Not "some", and not a function of how unusual the assets are — *half*, converging
to 50% as `N` grows. The authors show this empirically (drawing random subsets of `N` names
and optimising) and then prove it.

**(2) Optimal weights are extreme and do not shrink with `N`.** A few names carry large
positions however wide the panel is.

**(3) The closed form under equal pairwise correlation, which makes both of the above
transparent.** With common correlation `ρ`, common variance `σ²` and excess returns `µ`, the
unscaled optimal weight of name `i` is `ω_i = (a−b)µ_i + Nbµ̄`, and name `i` is held **short**
iff

```
µ_i  <  µ̄ / (1 + (1−ρ)/(Nρ))        →   µ̄   as N → ∞
```

so for a wide panel **every below-average-expected-return name is a short**, whatever the
value of `ρ` (excluding 0 and 1). The scaled weight converges to

```
w_i  →  ((µ_i − µ̄)/µ̄) · (ρ/(1−ρ))
```

which **contains no `N`**: a name whose expected excess return is 20% above average takes a
20% weight at `ρ = 0.5` whether the panel holds 200 names or thousands. Breadth does not
dilute the optimum. (With unequal variances the condition becomes
`µ_i/σ_i < mean_j(µ_j/σ_j)`, same conclusion.)

**(4) The result this note exists for: with shorting, attainable Sharpe grows without bound
in `N`; without shorting, it levels off — and the long-only ceiling has a closed form.**
Theorem 1 takes `C = M + α11'`, where `M` is a Wishart matrix with `d < N` degrees of
freedom (so `M = X'X`, i.e. a linear factor structure) and `α` is the **average covariance**.
Then as `N → ∞` the unconstrained Sharpe is of order `√N` and diverges, while

```
max_{ω ≥ 0}  (ω'µ) / √(ω'Cω)   ≤   (max_i µ_i) / √α
```

because `ω'Cω ≥ α(1'ω)²` for `ω ≥ 0`, and `ω'µ ≤ (1'ω)·max_i µ_i`. **The right-hand side does
not contain `N`.** The long-only attainable Sharpe is bounded by the largest per-name
expected excess return divided by the square root of the panel's average covariance, and
widening the panel cannot raise that bound.

**The intuition, which is the durable part.** When shorting is barred and most covariances
are positive, adding one asset to an existing efficient frontier typically produces
combinations *interior* to that frontier, so the new asset's optimal weight is zero and the
frontier does not extend. With shorting allowed, the new asset can be combined either long
or short with the existing portfolios, and for a typical asset both are about equally likely
to extend the frontier — so every added asset contributes. **The common positive covariance
component `α11'` is exactly what caps the long-only frontier, and it is the same object that
makes the long-only book a market bet.**

## Construction recipe

There is no strategy to implement here; the construction content is the diagnostic:

1. **Estimate the panel's average pairwise covariance `ᾱ`** over the window in question, in
   per-period return units.
2. **The oracle long-only Sharpe ceiling is `max_i µ̂_i / √ᾱ`** in those same units,
   annualised the usual way. Treat it as an upper bound on what *any* non-negative weighting
   of that panel could have achieved with perfect knowledge of the means — not as a target.
3. **Compare the bound computed on a narrow panel with the bound on a wide one.** The content
   of the theorem is that the two are the same up to the `max_i µ̂_i` term; if they differ a
   lot in practice, the difference is coming from the extreme of the mean estimates, not from
   breadth buying frontier extension.
4. **For the concentration statement**, use `(ρ/(1−ρ))` as the scale factor on relative
   expected return: the higher the panel's average correlation, the *more* concentrated the
   unconstrained optimum, independent of `N`.

## Robustness evidence (qualitative only)

- **The analytic results are theorems**, so they do not replicate or decay; what can fail is
  their assumption. Theorem 1 assumes one specific covariance ensemble (Wishart plus a
  constant common component). The authors back it with simulations under a different
  structure — pairwise correlations drawn uniformly on `[0.4, 0.5]`, excess returns on
  `[0, 0.2]`, standard deviations on `[0.2, 0.5]` — and report the same shape, which also
  rules out the empirical result being an artifact of estimation error or survivorship.
- **The empirical half is weak and the authors mostly say so.** 200 CRSP names with complete
  records over a twenty-year window is survivorship-conditioned (they argue it does not
  matter because the simulations agree, which is a fair but indirect defence), the covariance
  matrix is a raw sample estimate with no shrinkage in the main section, and `N` reaches only
  200. The ~50%-short result is consistent with earlier work in the same vein (Green and
  Hollifield; Levy 1983).
- **Section IV is the honest weak point.** The whole analysis assumes means and covariances
  are *known*. In practice they are estimated, and the authors concede the question by
  reference to Jagannathan and Ma: whether a weight constraint helps or hurts depends on the
  size of the estimation error against the size of the oracle performance gap. Their argument
  is that for large `N` the oracle gap is so large that the unconstrained portfolio should
  win even under substantial estimation error. **That argument is an assertion about relative
  magnitudes, not a measurement**, and it is the part of the paper to disbelieve.
- **Citations are low (17/19).** For a 2011 journal article with a theorem of this
  generality, that is a real signal and not only an age artifact — the result sits between
  the CAPM-criticism literature and the portfolio-construction literature and has been taken
  up by neither. Nothing here has been independently replicated. **Tier B.**

## Implementability here

Nothing here is a candidate. Three things it changes.

**1. It is a direct prediction about protocol v2's widening, and the lab can check it for
free.** The eligible panel went from ~140 names to ~1,400. Under Theorem 1 the attainable
long-only Sharpe does **not** grow with that, while the long–short attainable Sharpe would
have grown like `√N` — a factor of ~3. So **the 10× widening should be expected to buy
selection quality and nothing else**: more names from which to pick the same number of
holdings, not a higher reachable ceiling. The computable version is step 2 of the recipe
above, run on train and validation only. Two honest caveats before anyone leans on the
number: the bound is **loose** (it uses `max_i µ_i` over the whole panel, which on 1,400
names is an extreme order statistic), and it is an **oracle** quantity, since `µ` must be
replaced by realized means. Its content is the *absence of `N`*, not its level.

**2. It supplies a mechanism for two results the lab has already measured.** `learnings.md`
records that five family leads from five nominally different families correlate **0.75–0.85**
on validation, with the stated reason "every one of them is a long-only book over the same
names", and separately that de-concentration is expensive on this panel. Both are what
`C = M + α11'` predicts: the common component `α` is what binds the long-only feasible set,
so every long-only book is mostly the same bet on it, and the unconstrained optimum's
concentration does not fall with breadth (`w_i → ((µ_i−µ̄)/µ̄)·(ρ/(1−ρ))`, no `N`). The
practical reading: **this panel's `≤25%` position cap and the lab's measured de-concentration
price are not artifacts of a narrow panel and will not be relieved by a wider one.**

**3. The tension with Jagannathan–Ma must be stated, because this folder holds both.**
`notes/2026-08-22-long-only-as-l1-regularization.md` records that the no-short constraint
*helps* out of sample by acting as shrinkage on a noisily estimated covariance matrix. This
paper says it is extremely costly against *true* parameters. **Both are correct and they are
about different problems**: the constraint costs in the oracle problem and pays in the
estimated one. The lab's own position is a third case and worth naming — it does **not**
solve a mean–variance problem at all, it ranks on a score and holds a fixed number of names,
so it collects **neither** the oracle cost (it was never going to attain the unconstrained
optimum) **nor** the full shrinkage benefit (it estimates no covariance matrix to be shrunk).
What survives for a score-ranking long-only book is only the *ceiling* in result (4), which
is a statement about the feasible set and does not care how the weights were chosen.

**What not to take from it.** Do not read "50% of assets are held short" as "half the signal
is unreachable" — that is a statement about mean–variance weights under known parameters, not
about the share of a score's predictive content, and this folder's own
[2026-11-02] correction applies: state a gradient, not an absence. And do not use the `α`
bound as a benchmark in any gate: it is an in-sample oracle ceiling, computed from realized
means, and comparing a measured Sharpe to it would be a different and much weaker test than
the pool-relative skill the protocol already scores.

## Related

- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md` — the companion
  from tonight: the same constraint read in *weights* against a benchmark rather than in
  attainable Sharpe. The two are complementary — Jacobs–Levy say the bottom of the ranking is
  quantised to one bit; Levy–Ritov say the resulting feasible set has a breadth-independent
  Sharpe ceiling.
- `notes/2026-08-22-long-only-as-l1-regularization.md` — Jagannathan–Ma; the tension above.
- `notes/2026-09-24-long-only-minimum-variance-composition.md` and
  `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — the other half of the
  constraints-as-shrinkage literature this folder holds.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — `IR ≈ TC · IC · √BR`
  makes breadth the *only* free lunch in active management. This note is the long-only
  qualifier on that: `√BR` is a long–short statement, and the long-only ceiling does not
  grow in `N` at all.
