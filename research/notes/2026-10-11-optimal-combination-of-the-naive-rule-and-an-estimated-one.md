---
title: "Markowitz meets Talmud: A combination of sophisticated and naive diversification strategies"
authors: Tu, Zhou
year: 2011
venue: Journal of Financial Economics 99(1), 204–215 (venue tier 1, peer-reviewed)
url: https://doi.org/10.1016/j.jfineco.2010.08.013 · typeset version read at https://down.aefweb.net/WorkingPapers/w715.pdf
citations: 420 (Crossref is-referenced-by, checked 2026-10-11); 493 (OpenAlex, checked 2026-10-11)
sample_period: simulations (10,000 draws per design, one- and three-factor data-generating processes, T = 120/240/…); real data monthly, July 1963 – August 2007
markets: seven US datasets — the five used by DeMiguel–Garlappi–Uppal (2009) plus Fama-French 25 size/book-to-market and 49 industry portfolios, with the factor portfolios as additional assets
tier: A — tier-1 venue, heavily cited, closed-form results with proofs, honest about its own failures. Downgraded on one axis only: **no transaction costs and no short-sale constraint**, and the finite-sample claims rest on simulation designs the authors choose
validation_overlap: false
published_post_2018: false
---

## Access

The typeset published version is openly mirrored at `down.aefweb.net/WorkingPapers/w715.pdf`,
which OpenAlex's `locations` list names as the green copy for the Elsevier DOI.
`pdftotext -layout` gave 107 KB with no `( )` dropout and no shifted-ASCII artifact (the
`" the "` count is unchanged by a decode attempt), so the algebra is intact and was read
directly. The SSRN working-paper record (`10.2139/ssrn.1362477`) is behind the usual
Cloudflare challenge and was not needed.

## Mechanism

The question is the one protocol v3 created for this lab: **the benchmark is a naive
equal-weight portfolio, and a candidate is an estimated rule. How much of the estimated rule
should you hold?** Tu–Zhou answer it as a bias-variance trade-off with a closed form, and
the economics is entirely in two sentences they state plainly: *the `1/N` rule is biased but
has zero variance; a sophisticated rule is asymptotically unbiased but has sizable variance
in small samples.*

Write the combined rule as a convex mixture

```
ŵ_c = (1 − δ)·w_e + δ·w̃ ,          w_e = 1_N/N ,      0 ≤ δ ≤ 1
```

with `w̃` any estimated rule. Under i.i.d. normal excess returns, mean-variance preferences
with risk aversion `γ`, and the standard decision-theoretic loss
`L(w*, ŵ_c) = U(w*) − E[U(ŵ_c)]` against the true optimum `w* = Σ⁻¹µ/γ`, the loss separates:

```
L(w*, ŵ_c) = (γ/2)·[ (1−δ)²·π₁ + δ²·π₂ ]
π₁ = (w_e − w*)'Σ(w_e − w*)         ← the squared bias of the naive rule
π₂ = E[(w − w*)'Σ(w − w*)]          ← the estimation variance of the sophisticated rule
δ* = π₁/(π₁ + π₂)
```

**Proposition 1 is the result worth carrying.** Whenever `π₁ > 0` — i.e. whenever `1/N` is
not exactly the true optimum, which is always — there is a `δ*` strictly inside `(0,1)` at
which the mixture's loss is **strictly lower than both** `L(w*, w_e)` and `L(w*, w)`. The
naive benchmark and the estimated rule each hold information the other lacks, and the mixture
is not a compromise but a dominating third object. The authors' own gloss: if `π₁ = π₂` then
`δ* = 1/2` and the mixture's loss is *half* either component's — "exactly like a
diversification over two independent and identically distributed risky assets". The
diversification here is across **estimation errors**, not across assets.

The general two-rule coefficient, with `a = w_e − w*` and `b = w̃ − w*`, is

```
δ = (a'Σa − a'ΣE[b]) / (a'Σa − 2a'ΣE[b] + E[b'Σb])
```

so the cross term `a'ΣE[b]` matters: the right mixture weight depends on whether the naive
rule's bias and the estimated rule's error point the same way.

Two negative results from the same paper are as useful as the positive one. **Combining more
than two rules dominates in theory and need not in practice** — each extra component adds a
coefficient to estimate, and the estimation error grows. And **combining two rules neither of
which is `1/N` is usually worse than including `1/N`**: the zero-variance anchor is what the
construction is for.

## Construction recipe

Feasible version (their Proposition 2, for the mixture of `1/N` with the unbiased scaled
maximum-likelihood rule `w = Σ̃⁻¹µ̂/γ`, `Σ̃ = T/(T−N−2)·Σ̂`):

```
π̂₁ = w_e'Σ̂w_e − (2/γ)·w_e'µ̂ + (1/γ²)·θ̃²
π̂₂ = (1/γ²)·(c₁ − 1)·θ̃²  +  c₁·N/(γ²·T)
c₁ = (T−2)(T−N−2) / ((T−N−1)(T−N−4))          requires T > N + 4
δ̂  = π̂₁/(π̂₁ + π̂₂)
ŵ_CML = (1 − δ̂)·w_e + δ̂·w
```

where `θ̃²` is Kan–Zhou's estimator of the squared slope `θ² = µ'Σ⁻¹µ`. The same scheme is
given for mixtures with the Jorion (1986) Bayes-Stein rule (via an approximation, since the
moments are intractable), the MacKinlay–Pástor latent-factor rule, and the Kan–Zhou
three-fund rule, which uses `δ̂_k = (π̂₁ − π̂₁₃)/(π̂₁ − 2π̂₁₃ + π̂₃)` and therefore carries the
cross term explicitly.

Mechanics that transfer regardless of which sophisticated rule is used:

1. **`δ` is one scalar.** That is the whole design argument: a single parameter is estimable
   even when `µ` and `Σ` are not, so the mixture inherits most of the benefit and little of
   the noise. The authors say so explicitly and it is the reason the construction survives
   small `T`.
2. **`T > N + 4` is a hard requirement** for `c₁` to exist (it is what makes `E[Σ̂⁻¹]` have a
   second moment). It is not a technicality; it is the binding constraint on where this can
   be used at all.
3. **`δ̂` is re-estimated at each rebalance** from the trailing window — nothing is fitted
   once and applied backwards.
4. **`γ` enters `δ̂`**, so the mixture weight is preference-dependent. There is no
   preference-free version of this coefficient.

## Robustness evidence (qualitative only)

- **What the paper itself reports as failures.** In the simulation design that reproduces
  DeMiguel–Garlappi–Uppal's setting with a short estimation window, the combination rules
  beat each of their sophisticated components but **still lose to `1/N`** — the authors
  attribute this to a data-generating process that happens to favour the naive rule, and the
  ordering reverses as `T` grows. They also report that two of the four sophisticated
  components lose money on a risk-adjusted basis before combination. Nothing here supports a
  claim that the mixture always wins.
- **The objective is not the Sharpe ratio, and the authors flag the gap themselves.** They
  optimise expected-utility loss. They note that maximising the Sharpe ratio and maximising
  expected utility coincide when the parameters are *known* and **diverge once they are
  estimated**, and they choose the utility criterion. So `δ*` above is the optimal mixture
  weight for a quadratic-utility loss, *not* for a Sharpe-difference statistic.
- **Independent re-examination is unfavourable.** Bock's sixteen-strategy horse race across
  six datasets (see the companion note) tests both Tu–Zhou mixtures: the `1/N`-with-
  mean-variance mixture has higher Sharpe ratios than the plain mean-variance rule but
  **fails to dominate `1/N` or minimum-variance**, and the `1/N`-with-three-fund mixture is
  reported *below* its own uncombined three-fund counterpart in all but one dataset. That
  source is an unrefereed preprint and cannot overturn a tier-1 result, but it is the only
  independent multi-dataset test of these rules this folder has found, and it points the
  other way.
- **Gaps that bite here.** No transaction costs anywhere in the paper; no short-sale or
  long-only constraint (`w̃` is unconstrained and can be heavily levered); i.i.d. normal
  returns; a riskless asset assumed present; and the real-data evidence is monthly US
  portfolio data, not individual stocks on a global panel.

## Implementability here

The structural fit is unusually good and the numerical fit is bad, and both halves matter.

**Why the structure fits.** Footnote 5 of the paper makes the bridge the lab needs without
being asked: *"the performances of most institutional managers are benchmarked to an index…
then the return on the index portfolio can be viewed as the riskless asset to apply the same
framework"*. Protocol v3 grades Sharpe **minus the equal-weight eligible pool's on the same
days**, so the lab is already working in exactly that space — the pool in the role of the
riskless rate, and the candidate's deviation from it in the role of the risky position. In
that frame a candidate is *already* a mixture `pool + δ·(rule − pool)`, and the question
"how big should the active deviation be?" has a closed-form answer rather than a guess.

**The one-line candidate shape this licenses.** Take any existing book `w̃` and submit
`(1−δ)·w_pool + δ·w̃` with `δ` *derived* rather than fitted — this is a different object from
the lab's existing `FLOOR`-style de-concentration knobs, because it mixes toward the
**benchmark the statistic is computed against**, not toward a flat weight on the book's own
selection. Two pre-registration disciplines make it honest: `δ` must be recomputed at each
rebalance from trailing data only, and the comparison must be against the *same* `w̃`
submitted un-mixed, or the trial measures the mixture and the book together.

**Why the numbers do not fit, and what to do about it.** `T > N + 4` is fatal on the raw
panel: roughly a thousand names are eligible on a typical date, and the usable trailing
window is nowhere near that long. Every quantity in the feasible estimator (`c₁`, `θ̃²`,
`Σ̂⁻¹`) is unusable at `N ≈ 1000`. Three routes out, in order of honesty:

1. **Apply the mixture at the sleeve level, not the name level.** The construction needs the
   dimension of the *rules being mixed*, not of the universe, only because `π̂₂` is derived
   for the ML rule specifically. For a candidate that is already a long-only book of `k`
   positions plus the pool, the object being sized is one scalar `δ`, and `π₁`, `π₂` can be
   estimated from the realised active-return series of the book against the pool instead of
   from `Σ̂⁻¹` — a departure from the paper that must be declared as such in the journal,
   because it replaces their estimator with a different one.
2. **Reduce `N` before using the paper's own estimator.** The rules they mix were designed
   for a few dozen assets. The lab's region/liquidity sleeves are a natural coarsening, and
   `T > N + 4` is satisfiable there.
3. **Do not use the ML component at all.** The paper's own conclusion is that the
   MacKinlay–Pástor latent-factor rule is the one sophisticated component that does not
   perform poorly on real data; a factor-structure estimate of `µ` is also the only one with
   a chance of being stable at this panel's width, and it echoes this folder's standing
   finding that the dominant signals are few.

**Three cautions.** *(i)* The mixture optimises a utility loss, and v3 scores a Sharpe
difference with a paired bootstrap; the authors themselves say these objectives separate
under estimation error, so a derived `δ` is not an optimised `δ` for the lab's statistic —
which is a reason to *pre-register* `δ` from the formula rather than scan it. *(ii)* The
construction is cost-free in the source, and mixing toward the pool changes turnover in a way
v3 charges: the pool itself drifts, so `(1−δ)·w_pool` is not a free leg. *(iii)* Mixing
toward the benchmark **mechanically compresses skill along with tracking error**; with v3's
90% skill intervals near ±0.33, a heavily shrunk book is a book whose skill cannot be
measured. That tension is the practical content of the companion note's `√d` ceiling: the
mixture buys a lower loss against the *true* optimum, not a larger measured difference
against the pool.

## Related

- `notes/2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md` — the
  known-moments geometry of the same problem; this note is its finite-sample half.
- `notes/2026-10-11-reward-to-risk-timing-against-the-naive-benchmark.md` — the
  independent re-test that does not support these mixtures.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal, the result
  this paper answers.
- `notes/2026-09-30-shrinking-portfolio-weights-toward-a-target.md`,
  `notes/2026-09-30-bayes-stein-shrinking-an-estimated-mean-vector.md`,
  `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` — the folder's other
  shrinkage notes. This one differs in *what* is shrunk and *toward what*: portfolio weights
  toward the equal-weight portfolio, with the mixture weight in closed form.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md`,
  `notes/2026-08-19-model-averaging-mallows-weights.md` — combination in forecast space; this
  is the same bias-variance argument in weight space.
