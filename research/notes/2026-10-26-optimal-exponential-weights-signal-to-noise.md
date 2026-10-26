---
title: "Optimal properties of exponentially weighted forecasts — the smoothing constant as a closed form in the signal-to-noise ratio"
authors: Muth (1960); restated and proved via Wold (1938) by Lang (1987 working paper / 1989 journal note)
year: 1960 (Muth); 1989 (Lang)
venue: Journal of the American Statistical Association 55(290), 299–306 (venue tier 1) — NOT OBTAINED; read at one remove from Lang, Journal of Economic Behavior & Organization 11(3), 1989 (venue tier 2), working-paper version IFN WP No. 179 (1987), READ IN FULL
url: https://doi.org/10.1080/01621459.1960.10482064 (Muth); https://doi.org/10.1016/0167-2681(89)90040-1 (Lang); https://www.ifn.se/media/e55pr1d5/wp179.pdf (the working paper actually read)
citations: Muth 578 (Crossref `is-referenced-by-count`, checked 2026-10-26); Lang 0 (Crossref, checked 2026-10-26)
sample_period: none — both are theory. Muth's setting is a model, not a dataset; Lang's note is a proof that the result is a corollary of Wold (1938)
markets: none
tier: A for the mathematical claim (it is a derivation, independently proved twice, and the restatement was read in full with its equations verified against a rendered page image); the tier is NOT a claim about any empirical effect, because neither source contains one
validation_overlap: false
published_post_2018: false
---

## Access note, stated before anything else

**Muth (1960) itself was not obtained** — JASA 1960 is closed at the publisher. Everything below
is read from **Lang's restatement**, which was obtained in full (IFN working paper No. 179, 5
pages). Lang reproduces Muth's model, his forecast and his coefficient formula as equations (1),
(2) and (3), and then proves them as a special case of Wold (1938, chapters 3–4). The extracted
text mangled the displayed mathematics, so **equation (3) was read from a rendered page image**
(`pdftoppm -png -r 150`, printed page 2) rather than from the text layer, and the transcription
below is from that image. The formula was then checked for internal consistency at both limits
(see "Robustness"). Treat the *attribution* as solid and the *exact notation* as Lang's rather
than Muth's.

## Mechanism

The question this answers is the one left open by
`notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md`: if a scalar-state filter is an
exponentially weighted moving average, **what should its single parameter be, and does it have to
be fitted?**

The answer is that it does not. Under one specific model the optimal smoothing constant is a
**closed-form function of one variance ratio**, with no estimation, no likelihood and no optimiser.

Muth's setting. An observed series is the sum of a constant, a **random walk** component and a
**white-noise** component:

    y_t = a + w_t + v_t

where `v_t` is white noise, `w_t` is a random walk with increment `dw_t`, and `dw_t` and `v_t` may
be contemporaneously but not intertemporally correlated (Lang sets the contemporaneous correlation
to zero for notational simplicity). This is the "local level" or "random walk plus noise" model:
a permanent component you want to track, buried in transitory noise you want to discard.

**Muth's result.** The optimal (minimum-mean-square-error) forecast of `y_{t+1}` — which is also
the optimal estimate of the permanent component `w_t` — is the exponentially weighted sum

    ŷ_{t+1} = (1 − β) · Σ_{i≥0} β^i · y_{t−i}

with

    β = 1 + σ²_dw / (2 σ²_v)  −  (σ_dw / σ_v) · [ 1 + σ²_dw / (4 σ²_v) ]^{1/2}      … Muth's (3)

This is why Friedman's adaptive-expectations rule for permanent income is not an ad-hoc
convenience: it is the optimal estimator *of exactly the process Friedman's story describes*.
Lang's contribution is to show the whole thing drops out of Wold's representation theory — take
first differences of `y`, note the correlogram of `dy` vanishes beyond lag 1, factor `R(z)`, and
the root inside the unit circle **is** `β`.

**The economics, such as it is:** nothing in this is about markets. What it is about is the
general principle that **the right amount of smoothing is set by how much of the variance is
permanent**. A series whose innovations are mostly permanent should barely be smoothed; one whose
innovations are mostly transitory should be smoothed heavily. The tuning knob is not a taste
parameter — it is an estimate of a ratio.

## Construction recipe

Write `q = σ²_dw / σ²_v`, the **signal-to-noise variance ratio** (permanent-shock variance over
transitory-shock variance), and let `α = 1 − β` be the smoothing weight on the newest observation,
so the recursion is the familiar `l_t = l_{t−1} + α (y_t − l_{t−1})`. Then Muth's (3) rearranges to

    α = sqrt( q + q²/4 ) − q/2

and the usual pandas-style span is `span = 2/α − 1`. The map, computed from that closed form:

      q (signal/noise)   α        half-life (periods)   EWMA span
      0.0001             0.0100          69.3              200
      0.001              0.0311          21.9               63
      0.0025             0.0488          13.9               40
      0.01               0.0951           6.9               20
      0.04               0.1810           3.5               10
      0.1                0.2702           2.2                6.4
      0.25               0.3904           1.4                4.1
      1.0                0.6180           0.7                2.2

Two limits worth memorising, both checkable by hand:

- `q → 0` (all noise, no permanent component): `α → 0`. Never update; the best estimate is the
  long-run mean.
- `q → ∞` (all signal, pure random walk): `β → 0`, `α → 1`. The best forecast is the last
  observation — **which is the statement that a random walk cannot be smoothed usefully.**

And the rule of thumb that falls out of the small-`q` expansion, exact to the digits in the table
above: `α ≈ √q`, hence

    span ≈ 2 / √q

So **the span is twice the reciprocal of the square root of the signal-to-noise ratio.** A
20-period EWMA is the optimal filter for a series whose permanent-shock variance is about 1% of
its transitory-shock variance; a 200-period one, for 0.01%.

To *use* it you need `q`, and the model hands you an estimator for free: under this model
`corr(Δy_t, Δy_{t−1}) = r_1 = −σ²_v / (2σ²_v + σ²_dw) = −1/(2 + q)`, so

    q = −1/r_1 − 2

read straight off the **lag-1 autocorrelation of the first differences**, which is one line of
pandas and consumes no trial. (Lang derives the same `r_1` on his way to factoring `R(z)`; the
rearrangement is arithmetic.) Note the model constrains `r_1 ∈ (−1/2, 0)`: a positive lag-1
autocorrelation of differences is the model saying it does not fit, not a value of `q`.

## Robustness evidence (qualitative only)

- **This is a theorem, twice.** Muth derives it by lag-operator / z-transform prediction theory;
  Lang derives it independently as a corollary of Wold's autoregressive and moving-average
  representation theory, and the two agree. The folder's own [2026-10-25] detector — *when a lab
  applies a rule as a calibration, look for the theorem it approximates, and read the agreement as
  the finding* — applies here in the same shape: **a smoothing span chosen by horse-race is the
  approximation; this is the closed form it approximates.**
- **Internal consistency check performed here, not taken on faith.** The transcribed formula was
  evaluated at both limits (`q → 0` gives `α = 0`; `q → ∞` gives `α = 1`) and against the standard
  local-level identity `α = (−q + √(q² + 4q))/2`, which it reproduces exactly. This matters because
  the formula was read from a page image of a 1987 typescript.
- **The scope is narrow and should not be widened.** The optimality holds *for the random-walk-plus-
  noise model and for no other*. If the permanent component is mean-reverting rather than a random
  walk, or if the noise is autocorrelated, the optimal filter is not an EWMA and this constant is
  not optimal. Lang's framing makes the boundary explicit: the result is the `N = 1` case of a
  theorem about correlograms that vanish beyond lag `N`.
- **No empirical content whatsoever.** Neither source estimates anything on market data. Nothing
  here is evidence that a price series *is* random walk plus noise, and the folder should not let
  the elegance of the formula smuggle in that premise.

## Implementability here

**This is the cheapest item this folder has produced in several sessions, and it is a diagnostic
rather than a candidate.** It consumes no trial, no holdout look and no new machinery.

1. **It converts the lab's commonest free parameter into a measurement.** Every lookback, span or
   half-life the lab has ever chosen by sweep — momentum formation windows, volatility spans,
   smoothing of any per-name estimate — is, under this model, determined by a ratio that can be
   *estimated from the data the lab already holds*. The procedure is: take the series, difference
   it, read `r_1`, set `q = −1/r_1 − 2`, set `span = 2/α − 1`. **If the span that falls out is
   wildly different from the one the lab's sweeps settled on, that disagreement is itself the
   finding** — it says the series is not random-walk-plus-noise, and the model behind the smoothing
   is wrong even though the smoothing may still work.
2. **It prices the "Kalman filter" framing to zero for the scalar case.** Combined with the
   companion note, the chain is: scalar-state Kalman filter ⇒ steady-state gain ⇒ EWMA ⇒ one
   constant ⇒ a closed form in one variance ratio. **A candidate whose novelty is "we use a Kalman
   filter" on a one-dimensional state is proposing an EWMA with a particular span, and should be
   written, and graded, as that.** This is the acceptance criterion the [2026-10-25] open question
   asked for, answered in the affirmative but deflated: the vein yields an `O(1)` construction, and
   the `O(1)` construction is something the lab can already write in one line.
3. **The direct application worth a free screen: smoothing a per-name beta.** `learnings.md` has
   twice measured that a freely estimated per-name beta is where estimation error enters (median
   trailing beta ≈ 1.0 with an IQR of 0.62–0.94, and 29–49% of names further than 0.5 from unity),
   and has closed `SUMMARY.md` #96's free-beta residual on exactly that ground. Muth says the
   *right* amount to shrink such an estimate toward its own past is not a taste parameter. Reading
   `r_1` off the series of rolling betas gives the span, and the screen — does smoothing the beta
   at that span narrow the IQR without flattening the cross-sectional information content? — costs
   nothing. See the beta note for why this is the live tension and not a settled question.
4. **Where it does NOT apply, stated so a later session does not over-reach.** The model's
   observable is a *level* observed with noise. A return series is already the difference of a
   level; applying the formula to returns is a different model (`q` on returns answers "how much of
   the expected-return variation is permanent", which is a far stronger claim than "how much of the
   price variation is permanent"). Under protocol v3 the fill convention means a smoothed signal's
   turnover is charged as drift-correcting trades, so a long span is cheap and a short one is not —
   the formula sets the *statistically* optimal span, and the **cost-optimal** span is longer. Both
   numbers should be stated when either is used.

**Pitfall, and it is the one that matters.** A positive lag-1 autocorrelation of differences, or an
`r_1` outside `(−1/2, 0)`, means the model is rejected and `q` is undefined — but the arithmetic
`q = −1/r_1 − 2` will still return a number. That is the folder's [2026-10-25] second transferable
in a new dress: *ask what the formula returns when its assumption fails, and if the answer is "a
plausible number", check the precondition explicitly.* **Check `r_1 ∈ (−1/2, 0)` before using `q`.**

## Related

- `notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md` — the general taxonomy this is
  the scalar case of. That note establishes the state is small; this one says the small state needs
  no fitting.
- `notes/2026-10-26-learning-about-beta-kalman-filtered-loadings.md` — the application, and the
  place where the literature fits the variance ratio on the full sample instead of using this.
- `notes/2026-10-26-online-state-space-spreads-discount-factors.md` — the discount factor `δ` is a
  reparameterisation of the same single knob, arrived at from the Bayesian side.
- `experiments/learnings.md` — the lab's standing parameter-count triage rule (`SUMMARY.md` #1).
  A fixed, closed-form `α` estimates **zero** parameters per name; a fitted one estimates one.
  That distinction is precisely the axis that rule is about.
