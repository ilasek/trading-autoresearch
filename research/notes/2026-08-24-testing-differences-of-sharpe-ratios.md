---
title: "Robust performance hypothesis testing with the Sharpe ratio (with Jobson–Korkie and Memmel)"
authors: Ledoit, Wolf; Jobson, Korkie; Memmel; (Opdyke; O'Connor — secondary, see Related)
year: 2008
venue: Journal of Empirical Finance (peer-reviewed field journal, venue tier 1–2); Jobson–Korkie in Journal of Finance (tier 1); Memmel in Finance Letters (tier 3–4, three pages)
url: https://doi.org/10.1016/j.jempfin.2008.03.002
citations: 890 (Semantic Scholar, checked 2026-08-24; Crossref 856). Jobson–Korkie 1981 837 (Semantic Scholar, checked 2026-08-24; Crossref 658). Memmel 2003 367 (Semantic Scholar, checked 2026-08-24)
sample_period: methodological (simulation study, T=120 per scenario); two empirical illustrations use monthly fund returns 1994–2003
markets: none material — two US mutual funds and two hedge funds, used only to display p-values
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is not a strategy source. It is the source that answers the question session 10 left at the
top of the open list: **what is the standard error of the *difference* between two Sharpe ratios
estimated on the same sample?** — the quantity the promotion gate actually adjudicates, and the one
`notes/2026-08-23-statistics-of-sharpe-ratios.md` explicitly could not supply.

Three claims, in order of how much they matter here.

1. **There is a closed form, and it is governed almost entirely by the correlation between the two
   return series.** Jobson–Korkie derived a delta-method standard error for `Δ = Sh_a − Sh_b`;
   Memmel corrected it. The corrected expression is exact under i.i.d. bivariate normal returns
   and depends on four things only: the two Sharpe ratios, their return correlation `ρ`, and the
   sample length.
2. **That closed form is not a valid test on financial returns.** Ledoit–Wolf's whole point is that
   the Jobson–Korkie/Memmel variance formula "crucially relies on i.i.d. return data from a
   bivariate normal distribution". Relax either assumption and the formula is wrong in a specific
   direction — it is **liberal**, i.e. the true standard error is larger and the test rejects a true
   null too often. Two concrete failures they name: with non-normal i.i.d. data the fourth-moment
   entry of the asymptotic covariance is `E[(r−μ)⁴] − σ⁴` rather than `2σ⁴`, and the asymptotic
   covariance between the sample mean and sample variance is in general not zero; with stationary
   time-series data the leading entry becomes `σ² + 2Σ_t Cov(r_1, r_{1+t})` rather than `σ²`.
3. **The fix is a studentized time-series bootstrap, not a better formula.** Ledoit–Wolf state
   plainly that "in the case of general stationary data, simple and easily-implemented formulae do
   not exist" (this is also their correction of Opdyke 2007, whose time-series formulae they show
   collapse back to the i.i.d. ones). What works is resampling *blocks* of return **pairs**, and
   studentizing inside the bootstrap.

The economic content is thin by design; the value is that the whole apparatus is arithmetic on
series the repo already stores.

## Construction recipe

**The Memmel closed form.** With `Sh_a`, `Sh_b` the two Sharpe ratios in the sampling frequency's
own units, `ρ` the correlation of the two return series and `T` observations:

```
T · Var(Δ̂)  =  2(1 − ρ)  +  ½(Sh_a² + Sh_b²)  −  Sh_a·Sh_b·ρ²
```

Equivalently, in Memmel's own `Δ⁻ = Sh_a − Sh_b`, `Δ⁺ = Sh_a + Sh_b` parameterisation,
`T·Var(Δ̂) = 2(1−ρ) + [Δ⁻²(1+ρ²) + Δ⁺²(1−ρ²)]/4` (the two are algebraically identical). The test is
`Z₀ = Δ̂ / SE`, standard normal under `H₀: Δ = 0`, two-sided p-value `2Φ(−|Z₀|)`.

**The delta-method skeleton it comes from** (Ledoit–Wolf's Section 3, and the part that survives
dropping normality). Write `Δ = f(υ)` with `υ = (μ_a, μ_b, γ_a, γ_b)′` in terms of means and
*uncentered second moments*, and
`f(a,b,c,d) = a/√(c−a²) − b/√(d−b²)`. Then `√T(υ̂ − υ) → N(0, Ψ)` and
`√T(Δ̂ − Δ) → N(0, ∇f(υ)′ Ψ ∇f(υ))`, with

```
∇f(a,b,c,d) = ( c/(c−a²)^1.5 , −d/(d−b²)^1.5 , −½·a/(c−a²)^1.5 , ½·b/(d−b²)^1.5 )
```

so `SE(Δ̂) = sqrt( ∇f(υ̂)′ Ψ̂ ∇f(υ̂) / T )`. Everything hinges on the estimator of `Ψ`. Memmel plugs
in the i.i.d.-normal `Ψ`; the HAC version plugs in a kernel estimate (prewhitened
quadratic-spectral, Andrews–Monahan automatic bandwidth, with a `T/(T−4)` degrees-of-freedom
adjustment); the bootstrap version recomputes it inside each resample.

**The recommended procedure (`Boot-TS`), in full.**

1. Compute `Δ̂` and `SE(Δ̂)` on the original data, `Ψ̂` by prewhitened-QS kernel estimation.
2. Resample **blocks of return pairs** `(r_{t,a}, r_{t,b})` with the *circular* block bootstrap
   (circular rather than moving-blocks, to avoid edge effects), block length `b`.
3. In each resample, recompute `Δ̂*` **and its own** `SE(Δ̂*)` — using the block structure:
   with `l = ⌊T/b⌋`, `ξ_j = (1/√b)Σ_{t=1..b} y*_{(j−1)b+t}` and `Ψ̂* = (1/l)Σ_j ξ_j ξ_j′`, where
   `y*_t = (r*_{t,a} − μ̂*_a, r*_{t,b} − μ̂*_b, r*²_{t,a} − γ̂*_a, r*²_{t,b} − γ̂*_b)`.
   *Studentizing per-resample is the load-bearing step*: Ledoit–Wolf show a bootstrap that reuses
   one common standard error, or that is not studentized at all, buys no accuracy over asymptotic
   inference.
4. Symmetric interval: `Δ̂ ± z*_{|·|,1−α} · SE(Δ̂)` where `z*` is the `1−α` quantile of
   `|Δ̂* − Δ̂| / SE(Δ̂*)`. Reject `H₀` if the interval excludes zero. Equivalent direct p-value:
   `PV = (#{ d̃*_m ≥ d } + 1)/(M + 1)` with `d = |Δ̂|/SE(Δ̂)`, `d̃*_m = |Δ̂*_m − Δ̂|/SE(Δ̂*_m)`.
   Inverting an interval means one can resample the **observed** data rather than having to
   construct null-restricted data in which the two empirical Sharpe ratios are exactly equal.
5. **Choose the block size by calibration, not by rule of thumb** (their Algorithm 3.1): fit a
   semi-parametric model `P̂` to the observed pair series (they use VAR(1) plus a stationary
   bootstrap of the residuals for monthly data; they recommend a **bivariate GARCH for finer
   frequencies such as daily**); generate `K` pseudo-series (`K = 1000` minimum, 5000 ample); for
   each candidate `b`, compute the fraction `ĝ(b)` of intervals covering the pseudo-parameter `Δ̂`;
   pick the `b` minimising `|ĝ(b) − (1−α)|`. `ĝ(·)` is typically monotonically decreasing in `b`.

## Robustness evidence (qualitative only)

The simulation study is small but decisive in shape: six data-generating processes, all with the
null of equal Sharpe ratios true by construction (identical marginal processes), 5,000 repetitions
each, three nominal levels. The processes vary two dimensions independently — tail thickness
(normal vs `t₆`) and dependence (i.i.d., diagonal-vech bivariate GARCH, VAR(1) with AR coefficient
0.2). Findings:

- **Jobson–Korkie/Memmel is well-calibrated on i.i.d. bivariate normal data and on nothing else.**
  Heavy tails alone inflate its rejection rate by roughly a factor of two at every nominal level;
  heavy tails plus autocorrelation inflate it by roughly a factor of two-and-a-half to three. The
  distortion is always in the liberal direction.
- **HAC inference is asymptotically right and liberal in finite samples**, consistently with a wide
  prior literature on HAC in small samples. Prewhitening helps but does not fix it.
- **An i.i.d. bootstrap is fine for i.i.d. data and liberal for time-series data** — for the VAR
  processes it is no better than, and sometimes worse than, HAC.
- **The studentized time-series bootstrap is close to nominal in all six processes.** Their standing
  recommendation is to always use it with financial return data, because even series with
  negligible return autocorrelation usually have autocorrelated *squared* returns.
- Kernel choice is immaterial (Parzen ≈ QS).

Independent replication of the *simulation* was not found, but the analytical claim needs none: the
i.i.d.-normal `Ψ` is either the right matrix or it is not, and Ledoit–Wolf show the two entries that
are wrong. The methodological status is settled enough that Ledoit–Wolf is the status-quo reference
in the applied literature.

## Implementability here

This is the folder's most directly usable session in some time: it is arithmetic on series already
stored, and it closes a question the lab has been reasoning around.

**1. The exact relation between the paired standard error and the single-strategy one.** Setting
`Sh_a = Sh_b = Sh` in Memmel's formula factorises cleanly:

```
T · Var(Δ̂)  =  (1 − ρ) · [ 2 + Sh²(1 + ρ) ]
```

against `T · Var(ŜR) = 1 + ½Sh²` for one strategy (the i.i.d. formula Lo gives). So

```
SE(Δ̂)  =  SE(ŜR) · sqrt( (1−ρ)·(2 + Sh²(1+ρ)) / (1 + ½Sh²) )   ≈   SE(ŜR) · sqrt( 2(1−ρ) )
```

the approximation holding whenever `Sh² ≪ 2` **in the sampling frequency's own units** — which for
daily data is overwhelming (a 1.19 annualised Sharpe is `Sh_daily ≈ 0.075`, `Sh² ≈ 0.0056`). At
`ρ = 0` the factor is exactly `√2`; the whole of the folder's "the paired SE is far smaller than
`√2·SE(ŜR)`" is the factor `√(1−ρ)`. **The gate's resolving power is set by one number: how
correlated the candidate is with the champion.**

**2. A free, closed-form, pre-trial screen — and it reproduces the lab's bootstrap floor.** On `T`
daily observations, the *annualised* paired standard error is
`SE ≈ sqrt(2·252·(1−ρ)/T)`. On the repo's 1,562-day validation window that is
**`SE ≈ 0.568·√(1−ρ)`**: 0.031 at `ρ = 0.997`, 0.057 at 0.99, 0.080 at 0.98, 0.127 at 0.95, 0.172 at
0.909. `learnings.md` records a stationary-block paired bootstrap giving "~0.026–0.07 for a
near-identical construction (correlation > 0.98)" and "~0.13–0.17 for a structurally different one
(correlation ~0.9)". The closed form lands on both ranges without resampling anything. The
consequence is that **a candidate's error bar can now be written down before the candidate is
built**, from a single guessed correlation, with no series required at all.

**3. But the closed form is a *floor*, not the answer.** Ledoit–Wolf's simulation says the
Jobson–Korkie/Memmel SE is too small under exactly the two conditions that hold here — fat tails and
volatility clustering in daily equity returns. Used as a screen it is therefore conservative in the
right direction: if a pre-registered effect is inside the closed-form floor, the honest error bar is
*wider* still and the effect is certainly unresolvable. It must not be used the other way round — a
`|t| > 2` computed from this formula is not evidence of significance.

**4. The lab's own paired bootstrap is the right family, and this source names the one refinement
worth making.** `learnings.md` describes a stationary block bootstrap on the paired series, checked
across expected block lengths of 1 to 63 days. That is the correct object (resample pairs, preserve
cross-correlation, preserve time dependence). Two refinements are free and sourced:
*(a) studentize* — recompute a standard error inside every resample and take the quantile of
`|Δ̂* − Δ̂|/SE(Δ̂*)`, rather than the quantile of `Δ̂*` itself; Ledoit–Wolf's whole accuracy gain over
HAC comes from this step, and a non-studentized bootstrap is shown to be no better than asymptotic
inference. *(b) Calibrate the block length* rather than reporting robustness across a grid: fit a
bivariate GARCH to the pair (their explicit recommendation at daily frequency), simulate, and pick
the `b` whose empirical coverage is closest to nominal. Neither runs a strategy nor touches a trial
count.

**5. The power point, and it cuts against the lab's framing.** Opdyke (2007) corrected
Jobson–Korkie's third error — their claim that the test's power is chronically low and insensitive
to `ρ`. It is not: **power *rises* with `ρ`**, which is the same fact as the `√(1−ρ)` shrinkage of
the standard error. So the lab's result is stronger than it may look. Finding that consecutive
ladder rungs correlating 0.909–0.997 still fail to separate is not "the test is weak here"; it is
the test operating in its *most* favourable regime and still returning nothing. The structural
counterweight, also from this cluster: testing a difference against a **moving benchmark** has far
lower power than testing a Sharpe ratio against **zero** at the same `T`, because the reference
point is displaced. The gate asks the low-power question by construction, and no amount of sample
would change which question it asks.

**Boundaries.** (a) All of this is inference about a *difference of true Sharpe ratios*; it says
nothing about multiple testing, which is a separate correction (see the two companion notes from
this session). A candidate can be both statistically indistinguishable from the champion *and*
inflated by selection — the two adjustments compose, they do not substitute. (b) Ledoit–Wolf assume
strict stationarity of the bivariate return process, which a lab with a structural-breaks prior
should notice it is asserting. (c) The formulae are for excess returns over a benchmark; when the
benchmark is another portfolio rather than the risk-free rate, the authors note the quantity is
strictly an information ratio. (d) Nothing here licenses changing the promotion criterion — the
engine is frozen and the criterion is a human decision; this is an error bar to attach to readings,
which is what `learnings.md` already does.

## Related

- `notes/2026-08-23-statistics-of-sharpe-ratios.md` — Lo (2002) on the single-Sharpe standard error
  and the `η(q)` annualisation correction. Ledoit–Wolf's Remark 3.1 places Lo exactly: his "IID
  Returns" section *is* Jobson–Korkie/Memmel (it assumes i.i.d. normal), and his "Non-IID Returns"
  section *is* the HAC inference of their Section 3.1 — which they then show is liberal in finite
  samples. This closes the open question that note raised, and it settles the ordering: HAC beats
  the i.i.d. formula, and the studentized time-series bootstrap beats HAC.
- `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-08-24-multiple-testing-haircut.md` — the
  other half of the inference problem: selection across many trials rather than comparison of two.
- `experiments/learnings.md`, the paired-bootstrap entry and the ⚠ standing protocol concern — this
  note is the literature behind a measurement the lab made first. No tension: the lab's method is
  the one this source recommends, and the closed form it did not have reproduces its numbers.
- **Secondary sources in this cluster, recorded honestly.** *Opdyke (2007, Journal of Asset
  Management)* — **not read**; its content here is taken from Ledoit–Wolf (who correct its
  time-series formulae) and from O'Connor (who credits it with fixing Jobson–Korkie's power claim).
  *O'Connor (2024, Econ Journal Watch, "Revisiting Hypothesis Testing with the Sharpe Ratio",
  https://econjwatch.org/1300)* — **read in full**; used here only to verify Memmel's formula
  verbatim from a source that reproduces its algebra, and for the power argument. It is a comment
  article in a low-citation venue (Crossref reports 1 citation for the SSRN version, checked
  2026-08-24), it is `published_post_2018: true`, and its critical thesis about Ledoit–Wolf's
  empirical illustration is *not* carried into this note. Tier C on its own.
- *Jobson–Korkie (1981)* and *Memmel (2003)* were **not read directly** (JF is closed-access here;
  *Finance Letters* has no locatable copy). Their formula is recorded from two independent sources
  that reproduce it — Ledoit–Wolf's `Ω` matrix plus delta method, and O'Connor's explicit restatement
  — and the two agree algebraically.
