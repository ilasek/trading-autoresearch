---
title: "Inference Without Smoothing for Large Panels with Cross-Sectional and Temporal Dependence"
authors: Hidalgo, Schafgans
year: 2021 (arXiv preprint 2020)
venue: Journal of Econometrics 223(1), 125–160 (venue tier 1)
url: https://doi.org/10.1016/j.jeconom.2020.10.003 — read in full from the authors' arXiv preprint, https://arxiv.org/pdf/2006.14409 (498 KB, 49 pages; `pdftotext -layout` → 225 KB of text, 574 instances of `" the "`, `( )`-dropout check 1, no ASCII shift)
citations: 2 (Crossref `is-referenced-by-count`, checked 2026-11-18); 5 (Semantic Scholar, checked 2026-11-18)
sample_period: theorems and Monte Carlo throughout (critical values from 500,000 simulations; size and power tables over (n,T) grids). No empirical application, and no financial data anywhere in the paper
markets: none
tier: B
validation_overlap: false
published_post_2018: true
---

## Mechanism

Tonight's adversarial third, and it pays for itself the way the last three sessions' thirds did:
it **overturns the finite-sample standing of the estimator the aim was about**, and it does so
with a number rather than an argument.

**The claim about Driscoll–Kraay.** Hidalgo–Schafgans characterise that estimator as *"a hybrid
between an HAC and a cluster one: they employ the HAC methodology to deal with the temporal
dependence whereas they employ a cluster type of estimator to account for the cross-sectional
dependence."* They credit it with the thing tonight's primary admits it for — it *"avoid[s] the
need to specify an ordering of individuals"* — and then locate two residual costs in the half it
did **not** solve:

1. **A bandwidth must still be chosen for the temporal dependence.**
2. **The implicit assumption is that temporal dependence is homogeneous across names.** If it is
   not, *"even the selection of a bandwidth parameter to account for the temporal dependence may
   become infeasible. Any cross validation algorithm used to determine the bandwidth parameter for
   temporal dependence may then need to be performed for each individual."*

They also show their own central limit theorem provides **primitive conditions** for the CLT that
Driscoll–Kraay (and Kim–Sun's spatial-HAC) *assume*, and that their dependence class is strictly
larger — admitting **strong, "long-memory" cross-sectional dependence** that the strong-mixing
random-field route rules out.

**The construction: make the time axis uncorrelated instead of modelling it.** Take the DFT of
each name's series across the `T` dates. The spectral representation of a fixed-effects panel is
such that the transformed errors become **approximately temporally uncorrelated** (though
heteroskedastic) across frequencies — the Hannan (1963) observation. A White-type estimator can
then be built across frequencies with no smoothing at all:

> `Φ̆ = (1/T) Σ_{j=1..T−1} [ n^{−1/2} Σ_p J_x̃,p(λ_j) J_û,p(−λ_j) ] [ n^{−1/2} Σ_p J_x̃,p(−λ_j) J_û,p(λ_j) ]'`

where `J_·,p(λ_j)` is the discrete Fourier transform of name `p`'s series at frequency `λ_j`. The
**inner sum over names at each frequency** is what absorbs the cross-sectional dependence — the
same "collapse the cross-section" move as Driscoll–Kraay, but performed per *frequency* rather
than per *date*, which is why no lag truncation is needed. Sandwiching with `Σ̃_x` built the same
way gives `(nT)^{1/2} V̂^{−1/2}(β̃ − β) → N(0, I)`.

There is an exact **time-domain analogue**,
`Φ̆ = (1/n) Σ_{p,q=1..n} Σ_{|ℓ|=0..T−1} γ̂_x,pq(ℓ) γ̂_u,pq(ℓ)` — a double sum over **all pairs of
names and all lags**, with no truncation. Mathematically identical; computationally it is the
difference between `O(nT log T)` and `O(n²T)`, which at `n ≈ 1,000` is the difference between
cheap and not.

On top of the estimator they give **two frequency-domain wild bootstraps** (a "naïve" one assuming
homogeneous temporal dependence, a "wild" one allowing heterogeneity), neither of which needs a
bandwidth or a block length.

## Construction recipe

1. Within-transform for fixed effects, then take the DFT of each name's regressor and residual
   series over the `T` dates.
2. At each Fourier frequency `λ_j`, form the cross-name sum `n^{−1/2} Σ_p J_x̃,p(λ_j) J_û,p(−λ_j)`.
3. Average the outer products of those sums over the `T − 1` frequencies ⇒ `Φ̆`. Build `Σ̃_x` the
   same way; sandwich.
4. For finite-sample improvement, resample the normalised DFTs: the **naïve bootstrap** (resample
   a common standardised sequence; valid under homogeneous temporal dependence) or the **wild
   bootstrap** (name-specific multipliers; valid under heterogeneous temporal dependence). Neither
   takes a tuning parameter. The naïve variant gave sizes closer to nominal where it is valid.
5. **Scope limits stated by the authors.** The base version *"precludes the presence of
   conditional heteroskedasticity"*. Section 4 relaxes this to a multiplicative structure
   `v_pt = σ₁(w_p) σ₂(ρ_t) u_pt`, where the conditioning variables **need not be observed** — so
   groupwise (cross-sectional-only) heteroskedasticity is handled for free, and a non-constant
   `σ₂(ρ_t)` has a stated simple robustification. Fully general `v_pt = σ(x_pt) u_pt` would
   reintroduce a bandwidth, which the authors say and do not do.

## Robustness evidence (qualitative only)

All numbers below are **Monte Carlo rejection rates for a nominal 5% test** (and, for Table 2,
power at `β = 0.1`) — simulation diagnostics, not performance on any market. Cross-sectional
dependence is generated by drawing random locations on a line and setting weights
`c_ℓ(p) = (1 + |s_ℓ − s_p|)^{−10}` for "weak" and `^{−0.7}` for "strong" dependence; the
Driscoll–Kraay competitor uses Andrews' (1991) parametric AR(1) plug-in to choose its lag.

**1. Driscoll–Kraay's asymptotic `t`-test is oversized at every `(n, T)` simulated, and the
driver is the temporal dependence, not the spatial.** At `n = 100`, nominal 5%, weak spatial
dependence, DK with asymptotic critical values:

| `T` | AR(1) `ρ = 0.7` | AR(1) `ρ = 0.9` |
|---|---|---|
| 16 | .249 | .414 |
| 32 | .185 | .350 |
| 64 | .132 | .249 |
| 128 | .108 | .181 |
| 256 | .088 | .132 |

Strong spatial dependence changes these only marginally, and not always upward: at `T = 16` the
weak/strong pair is **.249 / .261** for `ρ = 0.7` and **.414 / .400** for `ρ = 0.9`. So a nominal
5% test rejects at **9–13% even at `T = 256`**, and at **~25–41% at `T = 16`** — and which of the
two dependence axes is strong barely matters.

**2. Fixed-`b` critical values help substantially and do not fix it.** Using Kiefer–Vogelsang /
Vogelsang fixed-`b` critical values for the same DK estimator moves `T = 16, ρ = 0.9` from .414 to
**.255** and `T = 256, ρ = 0.9` from .132 to **.096** — a real improvement, *"in accordance with
Vogelsang (2012)"*, and still roughly double nominal. This is the direct answer to the folder's
nominated fallback source: fixed-`b` is worth having and is not a solution.

**3. The decisive finding, and it is a refusal rather than a correction. Under heterogeneous
temporal dependence, DK's size distortion does not shrink in `T` at all.** With name-specific AR
and MA coefficients spread over `[0.5, 0.9]` and the plug-in still fitting AR(1), at `n = 100`,
weak spatial dependence, nominal 5%:

| process | DK asy, `T=64 / 128 / 256` | DK fixed-`b` | DK moving-block bootstrap | HS cluster (asy) |
|---|---|---|---|---|
| Mixed AR(1) | .189 / .144 / .121 | .132 / .114 / .098 | .062 / .078 / .073 | .101 / .082 / .064 |
| Mixed AR(1)/MA(1) | .176 / .149 / .112 | .132 / .120 / .095 | .083 / .097 / .084 | .080 / .068 / .058 |
| **Mixed AR(3)** | **.147 / .146 / .137** | **.135 / .137 / .132** | **.120 / .122 / .127** | .064 / .057 / .053 |
| Mixed AR(3)/MA(3) | .134 / .109 / .094 | .113 / .094 / .087 | .094 / .089 / .080 | .068 / .057 / .053 |

Read the **Mixed AR(3)** row: DK's size is **flat in `T`** — .147, .146, .137 — and so are its
fixed-`b` (.135, .137, .132) and moving-block-bootstrap (.120, .122, .127) variants, while the
bandwidth-free cluster estimator converges to nominal (.064, .057, .053). **Quadrupling the panel
length buys nothing.** The mechanism is plain: the lag length was chosen by an AR(1) plug-in while
the truth is AR(3), and a misspecified bandwidth is a bias that `T` does not wash out. The authors
make the same point about the block bootstrap — *"the MBB approach is sensitive to the chosen
blocksize, and its selection here was appropriate given the imposed AR(1) temporal dependence
(which is unknown in practical applications)"* — and note MBB is **not even valid** when temporal
dependence is heterogeneous, *"as it depends on some type of temporal homogeneity or even
stationarity."*

**4. The cluster estimator's own cost, stated by its authors.** Its asymptotic critical values
also *"suffer, in particular, from `T` being small, more so when the temporal dependence is
stronger"* (.316 at `n=100, T=16, ρ=0.9`), and the bootstrap is what repairs that (.125). And it
is not uniformly better: where DK's size distortion is smallest, *"any apparent power loss of
cluster based inference disappears"*, but DK's MBB variant *"performs very well"* in the
homogeneous setting.

**5. Power is the sobering column.** Under **strong** spatial dependence at `n = 100, T = 256,
ρ = 0.9`, power against `β = 0.1` is **.348** (cluster asy) to **.453** (DK asy, inflated by its
size distortion) — i.e. even with 25,600 name-periods, a real slope is detected less than half the
time once the cross-section is strongly dependent. Power rises faster in `T` than in `n`.

**Grading.** Tier **B**: top-tier venue and a genuine theorem, but **2 Crossref / 5 Semantic
Scholar citations** and its own results unreplicated. The results carried here are the simulation
tables, which are self-contained and reproducible from the stated designs; the asymptotic theory
is taken as stated and not relied on beyond the comparisons.

## Implementability here

**What this changes about tonight's primary.** The aim asked for an estimator whose cost is in
required panel length, and Driscoll–Kraay is that estimator. This source says the cost schedule
is **not** simply "more dates ⇒ better": length pays off only if the **temporal** side is
specified well enough, and when it is not, no amount of length helps. That reframes the lab's
situation. The lab has a lot of `T` (1,562 daily dates, ~251 month-ends) — plenty by
Driscoll–Kraay's own `T ≥ 20–25` floor and by the `T = 256` end of these tables — so on the
homogeneous-dependence rows the lab sits where DK's size is ~.09–.13 against .05. That is a
**~2× overstatement of significance**, which is a real discount and a bounded one.

But daily equity returns are not plausibly homogeneous in their temporal dependence across ~1,000
names, and the AR(3) row is where that lands: **a ~2.7× oversized test that does not improve with
length.** The honest reading is that for a forecast claim on this panel, a Driscoll–Kraay `t` of
2.0 is not a 5% result, and the lab cannot buy its way out with more dates.

**Concrete adaptations, cheapest first.**

1. **Report the DK `t` with a stated discount rather than as a `p`-value.** On this evidence a
   nominal 5% DK test is a ~10–14% test at the lab's `T`. Quoting it as "significant at 5%" is the
   error; quoting the statistic with the bracket is not.
2. **Prefer the bootstrap over the asymptotic critical values, and prefer the frequency-domain
   wild bootstrap over the moving block.** The lab already runs a paired stationary block
   bootstrap on the time axis for `skill_se`; this source says a block bootstrap is **invalid**
   under heterogeneous temporal dependence, which is the regime the lab is plausibly in. That is a
   direct, unflattering comment on an instrument the lab uses, and it belongs in the record even
   though the lab's own use is on a *portfolio* return series (`n = 1`), where the heterogeneity
   objection does not bite. Keep the two cases separate: `n = 1` time-series bootstrap, fine;
   bootstrapping a wide dependent panel by blocks, not fine.
3. **The DFT estimator is implementable here and the time-domain form is not.** `numpy.fft` over
   a `T × n` residual array, one cross-name sum per frequency: `O(nT log T)` and a few lines. The
   `O(n²T)` time-domain double sum at `n ≈ 1,000` is ~10⁶ name-pairs × `T` lags and should not be
   attempted.
4. **Check the scope limit before adopting it.** The base estimator precludes conditional
   heteroskedasticity — and daily equity returns are the canonical conditionally heteroskedastic
   series. Section 4's multiplicative relaxation covers **cross-sectional-only** heteroskedasticity
   for free (names with permanently different volatilities: fine, and that is a large part of the
   lab's problem), and gives a stated fix for a common time-varying factor `σ₂(ρ_t)`. Genuine
   per-name GARCH is outside it. This is the reason the estimator is a **nominated instrument and
   not a drop-in replacement**, and it is why tonight admits Driscoll–Kraay as the primary rather
   than this.

**Pitfall worth naming separately.** Tables 1 and 3 together say something uncomfortable about how
this lab reasons: the quantity that mattered was not the one the aim was pointed at. The aim asked
about **cross-sectional** dependence; the simulations say the **temporal** specification dominates
the size distortion, and strong-versus-weak spatial dependence barely moves it. The lesson
generalises past this vein — when two nuisance axes are both present, the one that gets the
attention is not necessarily the one that costs.

## Related

- `notes/2026-11-18-covariance-estimation-without-specifying-cross-sectional-dependence.md`
  (this session) — the estimator this note attacks in finite samples while accepting its
  cross-sectional logic.
- `notes/2026-11-18-the-unbalanced-panel-formula-and-when-not-to-use-it.md` (this session) — the
  bandwidth default `m(T) = floor[4(T/100)^{2/9}]` that this note shows to be the binding error
  when temporal dependence is heterogeneous.
- `notes/2026-11-17-which-dependence-structure-licenses-which-standard-error.md` — `#461`'s
  few-cluster bias; the fixed-`b` reference distribution nominated there as the likely repair is
  evaluated here and found partial.
- `notes/2026-10-27-modified-rescaled-range-and-the-long-memory-null.md` — the folder's other
  long-memory entry; this source admits long-memory **cross-sectional** dependence, which is a
  different axis.
- `experiments/learnings.md`, the paired stationary block bootstrap entries — the instrument item
  2 above comments on, and the `n = 1` scope that keeps the comment from applying to the lab's
  current use.
