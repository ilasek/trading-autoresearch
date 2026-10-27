---
title: "Long-Term Memory in Stock Market Prices"
authors: Lo
year: 1991
venue: Econometrica 59(5), 1279–1313 (venue tier 1)
url: https://doi.org/10.2307/2938368
citations: 1554 (Crossref `is-referenced-by-count`, checked 2026-10-27)
sample_period: 1872–1987 (daily 1962–1987, n 6409; weekly 1962–1987, n 1330; monthly 1926–1987, n 744; annual S&P Composite 1872–1986, n 115)
markets: US aggregate equity indexes (CRSP value- and equal-weighted; S&P Composite)
tier: A
validation_overlap: false
published_post_2018: false
---

> **Source read.** The published Econometrica article is closed; the text below was read from
> **NBER Working Paper 2984 (May 1989)**, the working-paper version carrying the same title and
> abstract, at `nber.org/system/files/working_papers/w2984/w2984.pdf`. That file is a
> **text-layerless scan** (`pdffonts` prints an empty font table; `pdftotext` yields 47 bytes from
> 47 pages), so it was rendered with `pdftoppm -png -r 120 -gray` and read as page images:
> title/abstract, §1 introduction, §2 (fractional differencing), §3–4 (the statistic, its
> denominator, its asymptotic distribution and critical values), §5 (the test applied), §6's
> closing summary, §7 conclusion, and Tables 1 and 2a/2b. Section numbering and equation numbers
> below are the working paper's. Published-version page numbers were not seen.

## Mechanism

There is no return-predicting mechanism in this paper. It is the **null-side anchor** of the
long-memory vein: it supplies the definition of the thing being claimed, a statistic that tests
for it, and a demonstration that the pre-existing evidence for it in equity returns was an
artifact of the statistic used.

**What long memory is.** A series is long-range dependent when its autocorrelations decay
*hyperbolically* rather than geometrically, so that no finite-order ARMA captures it. The
canonical generator is fractional differencing: `(1 − L)^d X_t = ε_t` with non-integer `d`,
expanded by the binomial theorem into an infinite AR (or MA) with coefficients
`A_k = (−1)^k C(d,k) = Γ(k − d) / (Γ(−d) Γ(k + 1))`. For the fractionally differenced process
`H = d + 1/2`.

**Why it cannot be read off short lags, which is the single most transferable fact in the paper.**
Table 1 of the working paper puts a `d = 1/3` fractional process beside an `AR(1)` with `ρ = 0.5`
(both scaled to unit variance):

| lag `k` | `ρ(k)`, `d = 1/3` | `ρ(k)`, `d = −1/3` | `ρ(k)`, AR(1) `ρ = .5` |
|---|---|---|---|
| 1 | 0.500 | −0.250 | 0.500 |
| 2 | 0.400 | −0.071 | 0.250 |
| 5 | 0.295 | −0.015 | 0.031 |
| 10 | 0.235 | −0.005 | 0.001 |
| 50 | 0.137 | −0.000 | 0.000 |
| 100 | 0.109 | −0.000 | 0.000 |

**The two models are identical at lag 1 and differ by two orders of magnitude by lag 10.** Any
screen, estimator or closed form that reads only the first autocorrelation is, by construction,
blind to the distinction this literature is about.

**Why a long-memory claim about asset prices is an economic claim.** Lo's framing: persistent
dependence would make optimal consumption/savings and portfolio allocation sensitive to the
investment horizon, would break the martingale pricing of derivatives, and — per Mandelbrot
(1971) — would be hard to arbitrage away. The conclusion runs the argument the other way: markets
clear frequently, so prices "must be immune to persistent informational asymmetries, especially
over longer time spans", and long swings are more plausible in aggregate *output* than in the
return to equity.

## Construction recipe

**The classical R/S statistic** (Hurst; Mandelbrot–Wallis). For a sample `X_1 … X_n` with mean
`X̄_n`, the rescaled range is the range of the cumulative mean-deviations divided by the sample
standard deviation `s_n`:

```
Q̃_n = (1/s_n) [ max_{1≤k≤n} Σ_{j≤k}(X_j − X̄_n)  −  min_{1≤k≤n} Σ_{j≤k}(X_j − X̄_n) ]
```

**The modified statistic.** Identical numerator; the denominator is replaced by a consistent
estimator of the **variance of the partial sum** rather than of the individual term — i.e. a
Newey–West / Bartlett long-run variance:

```
Q_n      = (1/σ̂_n(q)) [ max_k Σ_{j≤k}(X_j − X̄_n) − min_k Σ_{j≤k}(X_j − X̄_n) ]        (4.1)
σ̂²_n(q) = σ̂²_x + 2 Σ_{j=1..q} ω_j(q) γ̂_j ,     ω_j(q) = 1 − j/(q+1),   q < n          (4.2–4.3)
```

with `σ̂²_x` and `γ̂_j` the usual sample variance and autocovariances. Consistency of `σ̂_n(q)`
(Phillips 1987, Thm 4.2) needs `sup_t E|ε_t|^{2β} < ∞` for some `β > 2` and `q → ∞` with
`q ~ o(n^{1/4})`.

**Null distribution and critical values.** `V_n(q) ≡ Q_n/√n ⇒ V ≡ M° − m°`, the **range of a
Brownian bridge**, with
`F_V(v) = 1 + 2 Σ_{k≥1} (1 − 4k²v²) e^{−2(kv)²}`, `E[V] = √(π/2) ≈ 1.25`, `sd(V) ≈ 0.27`, and the
distribution positively skewed with most mass between 3/4 and 2. Fractiles (Table 2a):

| `P(V<v)` | .005 | .025 | .05 | .10 | .50 | .90 | .95 | .975 | .995 |
|---|---|---|---|---|---|---|---|---|---|
| `v` | 0.721 | 0.809 | 0.861 | 0.927 | 1.223 | 1.620 | 1.747 | 1.862 | 2.098 |

So the **two-sided 95% acceptance region is `V_n ∈ [0.809, 1.862]`** — a single, universal pair of
numbers, no simulation required. (Symmetric intervals about the mean are in Table 2b: `γ = 0.519`
for 5%, `γ = 0.432` for 10%.)

**Choosing `q`.** The theory gives no finite-sample guidance: too large and the finite-sample
distribution departs radically from the limit, too small and autocovariances beyond `q` are
omitted. Lo recommends reporting `V_n(q)` over a **range** of `q` and treating stability across
`q` as part of the evidence, and also reports Andrews' (1988) data-dependent rule, which in the
working paper's notation is

```
q = [k_n],   k_n = (2n/3)^{1/3} · ( ρ̂ / (1 − ρ̂²) )^{2/3}
```

with `ρ̂` the sample first-order autocorrelation. (The scan prints the right-hand side under the
label `s_n` while defining `q = [k_n]`; the subscript is inconsistent in the working paper and the
quantity meant is plainly `k_n`.) Andrews also suggests the alternative weights
`ω_j = 1 − |j/k_n|`. With the automatic rule, size and power were comparable to the best fixed-`q`
cases, which Lo takes as a reason to prefer it — "it eliminates one more degree of arbitrariness".

## Robustness evidence (qualitative only)

- **The bias the modification removes is enormous, and it is a bias toward finding memory.** For a
  stationary `AR(1)`, `Q̃_n/√n` converges not to `V` but to `ξV` with `ξ = √((1+ρ)/(1−ρ))`; at
  `ρ = 0.5` the mean of the classical statistic is inflated by **73%**, carrying it to ≈ 2.16,
  which the Table 2a critical values reject at any conventional level. Measured on the same
  equity index series, dividing by `s_n` instead of `σ̂_n(q)` imparted an upward bias of about
  **80%** — the classical statistic sat at 2.63 while the modified one sat at 1.46–1.50.
- **The same bias afflicts the log-log Hurst regression.** Davies and Harte (1987) show the 5%
  Mandelbrot regression test rejects `H = 1/2` **47% of the time** for a stationary Gaussian AR(1)
  with autoregressive parameter 0.3. So "the estimated Hurst exponent is above 0.5" is, absent a
  short-range correction, very largely a statement about the series' first autocorrelation.
- **The headline result.** Once the denominator accounts for short-range dependence, there is no
  evidence of long-range dependence in any of the indexes, **in any sample period or sub-period**,
  at daily, weekly, monthly or annual frequency. The point estimates were also *stable across
  truncation lags* (90 vs 270 vs 360 days gave essentially the same value), which Lo reads as
  positive evidence that dependence beyond one or two months is slight.
- **Power.** Monte Carlo evidence in §6 shows the modified statistic has power against at least two
  specific long-memory alternatives. Lo is explicit that the simulations are "merely
  illustrative": a conclusive study would sweep `d`, and the trade-off between a sample's *time
  span* and its *observation frequency* for power is left open. His own reading is that
  "short-range dependence may be the more significant feature of stock market returns".
- **The honest caveat is in the conclusion and it limits how far a non-rejection can be pushed:**
  "if some form of long-run dependence is indeed present in stock returns, it will not be easily
  detected by any of our current statistical tools." A non-rejection here is a statement about the
  test's reach, not a proof of absence. This is the hinge the critical literature turns on — see
  **Related**.

## Implementability here

**This is a screen, not a book.** Nothing in the paper produces portfolio weights, and the note is
filed as the vein's null-side anchor exactly as the [2026-10-26] open question pre-committed.

- **Cost: zero trials, no holdout.** `Q_n`, `σ̂_n(q)` and `V_n(q)` are a cumulative sum, a max, a
  min and a Bartlett-weighted autocovariance sum — a few lines of pandas/numpy per series, and the
  critical values are the fixed pair `[0.809, 1.862]`. Nothing here goes near `run_experiment.py`.
- **Sample lengths available.** The lab's train window is ≈ 5,300 daily observations per
  continuously-eligible name and validation ≈ 1,500; the pool index itself has the same length.
  Lo's daily tests ran on 6,409 observations, so **the train window is the only window on this
  panel with a comparable number of observations**, and a per-name test on validation alone is
  running at a quarter of his `n`.
- **`q` must be fixed a priori or read off a trailing window only.** The Andrews rule depends on
  `ρ̂`; computing `ρ̂` on the full visible window and then applying the statistic backwards is the
  exact hazard item `#311` names. If this is ever used inside a candidate rather than as an
  offline diagnostic, `q` is a hyperparameter in `#311`'s sense.
- **What it can decide cheaply.** Before any multi-scale, fractional-differencing, Hurst-ranking or
  long-memory construction is written here, run `V_n(q)` on the pool's own excess-return series and
  on a sample of eligible names' return series over train, across `q ∈ {5, 21, 63, 126, 252}`, and
  report whether anything leaves `[0.809, 1.862]`. If nothing does, the vein has no object on this
  panel and the right outcome is to not write the candidate.
- **A caution about what a non-rejection licenses.** Lo's own conclusion says a long-run effect may
  simply be undetectable at these sample sizes, and
  `notes/2026-10-27-hurst-estimator-finite-sample-confidence-intervals.md` prices exactly how
  undetectable. A `V_n` inside the band is a reason not to *build* on long memory; it is not
  evidence that the lab's measured 60-month cross-sectional reversal is absent, because that is a
  different object (see below).
- **The object mismatch, stated so no later session conflates them.** Lo tests a **univariate**
  aggregate index series for hyperbolic autocorrelation decay. The lab's 2026-10-26/27 result — the
  mean **cross-sectional rank correlation** of market-demeaned returns over `[−2h, −h]` against
  `[−h, 0]`, which is 4–9× larger at `h = 60` months than at any other horizon — is a
  cross-sectional, relative-return object of the DeBondt–Thaler kind. **A long-memory null on the
  index neither supports nor refutes it.** What Lo's paper *does* bear on is the temptation to
  reach for fractional differencing or a Hurst exponent as the explanation of that 60-month
  finding: that would be importing a univariate machine into a cross-sectional fact.

## Related

- `notes/2026-10-27-hurst-estimator-finite-sample-confidence-intervals.md` — the finite-sample
  price of this whole family of estimators; read it before quoting any `Ĥ`.
- `notes/2026-10-27-long-memory-and-regime-switching-identification.md` — Diebold–Inoue, who argue
  the long-memory/structural-change distinction is not identified at all under a small amount of
  switching. Together with Lo they bracket the vein: Lo says the evidence dissolves under a
  short-range correction, Diebold–Inoue say that even surviving evidence would not pin down a
  mechanism.
- `notes/2026-10-27-wavelet-multiscale-decomposition-and-scale-by-scale-beta.md` — the construction
  half of the same vein.
- `notes/2026-09-21-har-rv-volatility-cascade.md` — the one place this folder already touched long
  memory, and it reached the same verdict from the volatility side: the HAR cascade reproduces the
  stylised facts that motivate long-memory models "without being a long-memory model", and the
  exact ARFIMA machinery "buys little".
- `notes/2026-10-26-optimal-exponential-weights-signal-to-noise.md` and SUMMARY item `#312` — the
  lab closed `#312` on train by measuring `r₁`, the **lag-1** autocorrelation of first differences.
  Lo's Table 1 is the standing reminder that `r₁` identifies the short-memory model's parameter and
  says nothing about the long-lag decay rate; the `#312` closure is correct as stated and should
  not be read as a finding about long memory.
- `notes/2026-08-24-testing-differences-of-sharpe-ratios.md` — the Bartlett/HAC long-run-variance
  denominator in (4.2) is the same object that note handles for the gate's own statistic.
