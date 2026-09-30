---
title: "Optimal shrinkage of portfolio weights toward a target portfolio"
authors: Bodnar, Okhrin, Parolya
year: 2023
venue: Journal of Business & Economic Statistics 41(1), 140–156 (Tier 1; published online December 2021)
url: https://doi.org/10.1080/07350015.2021.2004897 · open access via https://opus.bibliothek.uni-augsburg.de/opus4/files/91736/91736.pdf
citations: 66 (Semantic Scholar, checked 2026-09-30); 69 (OpenAlex, checked 2026-09-30)
sample_period: 2000-01-01 to 2018-03-23 (daily)
markets: 395 S&P 500 constituents
tier: B — Tier-1 venue, open access, proved results and an unusually careful empirical design, but transaction costs are explicitly neglected and there is no independent replication
validation_overlap: true (the sample runs into the first quarter of 2018, inside the lab's validation window)
published_post_2018: true
---

## Access

**Read in full** from the Augsburg institutional repository, which serves the **version of record**
under the article's open licence. This re-confirms the 2026-09-07 finding that a German institutional
repository is a reliable channel: the Taylor & Francis endpoint is the nominal OA location, but the
repository copy parsed cleanly on the first try and carries the journal's own pagination.

## Mechanism

The companion note (`2026-09-30-optimal-shrinkage-of-a-high-dimensional-mean-vector.md`) shrinks the
*input* to a portfolio rule. This paper shrinks the **output**: the estimated weight vector itself is
pulled toward a target portfolio, with an intensity derived from the same `p/n` random-matrix
asymptotics.

The reason to prefer weight space is stated directly and is the paper's best argument: the covariance
matrix and the mean vector are *parameters of the return distribution*, whereas the weights are **the
object the investor actually cares about**. Optimising the estimation of an input does not optimise
the thing built from it, because the map from inputs to weights is nonlinear and amplifies error
unevenly. Shrinking where the loss lives is the more direct fix.

The economic content of the intensity is that it prices estimation risk against the target's own
sub-optimality. A target portfolio is biased — it ignores the signal — but it has no estimation
error. The sample portfolio is unbiased but noisy. The optimal intensity is the point where the
marginal bias added by pulling further toward the target equals the marginal variance removed, and
that point is a function of how wide the cross-section is relative to the sample.

## Construction recipe

```
w_GSE = alpha * w_S + (1 - alpha) * b ,        with b'1_p = 1
```

so unlike the mean-vector case this **is** a convex combination — the budget constraint forces it.
`w_S` is the sample expected-utility portfolio,

```
w_S  = S^-1 1 / (1' S^-1 1)  +  (1/gamma) * Q_hat * y_bar
Q_hat = S^-1 - (S^-1 1 1' S^-1) / (1' S^-1 1)
```

i.e. the sample global-minimum-variance portfolio plus a signal tilt in the space orthogonal to it.

`alpha` is calibrated by maximising a **unified mean-variance objective**
`U(beta) = w'mu - (beta/2) w' Sigma w`, where different `beta` recover different familiar criteria:
`beta = gamma` gives expected utility, and other values give out-of-sample variance minimisation and
related measures. This is a genuinely useful piece of engineering — one derivation covers several
objectives, so the lab's choice of grading statistic can be plugged in rather than re-derived.

The oracle intensity (Theorem 2.1, `c < 1`) depends **only on `c` and the parameters of the efficient
frontier** — `R_GMV`, `V_GMV`, the slope `s`, and the target's own return `R_b` and variance `V_b`.
The feasible version (Proposition 2.2) substitutes consistent estimators of those five quantities,
each carrying an explicit `1/(1 - p/n)` inflation correction. For `c > 1` a separate intensity
`alpha+` is derived using the Moore–Penrose pseudo-inverse.

**Targets considered:** the equally weighted portfolio and two modified global-minimum-variance
portfolios. Worth recording precisely, because it closes a loop with the classical literature: the
authors note that **the equally weighted portfolio is what you get if you assume all assets have
equal expected returns, equal variances and equal correlations** — which is exactly the
Frost–Savarino (1986) prior. `1/N` is not an atheoretical fallback here; it is the portfolio implied
by the maximally shrunk prior.

## Robustness evidence (qualitative only)

The empirical design is better than the norm and worth imitating: rather than reporting one
portfolio, the authors draw a thousand random asset subsets of size `p = 300` from the constituent
universe and rebuild the strategies on each, so the reported comparisons are distributions over
universes rather than a single draw. That is a direct answer to the selection concern the folder
raised in `2026-09-09-nonstandard-errors-in-portfolio-sorts.md`.

The most valuable finding is a **non-monotonicity in `c` that contradicts the obvious intuition**:
the shrinkage intensity on the sample estimator **falls to zero as `c` approaches 1 from below**, so
at `c ≈ 1` the book collapses entirely onto the target and the signal is discarded; then for `c > 1`
the intensity **rises again**, because the pseudo-inverse of a genuinely rank-deficient sample
covariance is better behaved than the near-singular inverse at `c ≈ 1`. The practical statement:
**`p ≈ n` is the worst place to be, worse than `p > n`.** Anyone choosing an estimation window by
"make sure I have at least as many observations as assets" is steering toward the failure point
rather than away from it.

Methodology honesty is mixed, and this is what caps the tier. Costs are a stated omission — "we
neglect the transaction costs in the below discussion" — while the strategy **reallocates daily**.
For this lab that combination is close to disqualifying on its own: a daily-reallocated 300-name
book at 15 bps per side is a very different object from the one measured. Multiple testing is not
discussed. There is no independent replication.

## Implementability here

This is the note in tonight's set whose operator is **not** absorbed by the lab's existing knobs.
The companion note shows that shrinking a *score* toward a scalar target is exactly a `FLOOR`
reparametrisation under `c - c.min() + FLOOR`. Shrinking the *weights* toward a target portfolio is
not, because the target enters after the weighting function rather than before it:

```
w_final = (1 - phi) * w_champion + phi * b
```

with `b` the equal-weighted book over the same holdings, or a minimum-variance book. This is a
genuinely different operator from anything `FLOOR` reaches, it preserves the long-only and
budget constraints for any `phi` in `[0,1]` when `b` is long-only, and it acts **hardest on exactly
the positions the lab says matter** — the ten names holding 61.41% of gross ([2026-09-27]) are the
ones furthest from `1/N`, so they move most per unit of `phi`. The lab's standing question was an
operator that moves the top ten weights; this is one, and it needs no new signal.

Two honest qualifications. First, the lab's book is not a mean-variance portfolio, so the derived
intensity formula does not transfer — `R_GMV`, `V_GMV` and `s` are efficient-frontier parameters of
an optimiser the lab does not run. What transfers is the **shape** (shrink the realised weight vector
toward a long-only target) and the **regime warning** about `c`; an intensity would have to be
calibrated some other way, and a hand-picked `phi` reintroduces exactly the free parameter that made
this literature attractive. That is a real cost and should be stated in any hypothesis built on it.
Second, and cutting the other way: this operator is a de-concentration overlay, and the lab has
measured a de-concentration price before. The folder's own standing warning applies —
`experiments/learnings.md` records that de-risking and de-concentration overlays on this base have
repeatedly backfired, and the constants were measured on `price-trend`. **Nothing here says this
one will differ**; what is new is only that the operator reaches the weights the other overlays could
not.

Free items, no trial needed: compute `p/n` for whatever window any covariance-using diagnostic
already runs on, and check how close it sits to 1. Every covariance-based statistic the lab computes
inherits the near-singularity problem described above, and the fix (shorten `p`, lengthen `n`, or
move to the daily panel) is a choice of window rather than a candidate.

## Related

- `2026-09-30-optimal-shrinkage-of-a-high-dimensional-mean-vector.md` — the same machinery in input
  space, and the `FLOOR`-equivalence result that makes this note the interesting half of the pair.
- `2026-09-30-bayes-stein-shrinking-an-estimated-mean-vector.md` — the Frost–Savarino prior whose
  implied portfolio is the `1/N` target used here.
- `2026-08-17-naive-vs-optimized-weighting.md` — why `1/N` is the benchmark worth shrinking toward.
- `2026-09-24-long-only-minimum-variance-composition.md` — the other target portfolio considered here.
- `2026-09-28-best-ideas-and-the-cost-of-overdiversification.md` — the argument on the other side:
  shrinking toward `1/N` dilutes the highest-conviction positions, which is the cost this operator
  pays for its variance reduction.
- `2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the concern the random-subset design answers.
