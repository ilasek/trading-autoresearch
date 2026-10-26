---
title: "Learning about beta: time-varying factor loadings, expected returns, and the conditional CAPM"
authors: Adrian, Franzoni
year: 2009
venue: Journal of Empirical Finance 16(4), 537–556 (venue tier 2 — solid peer-reviewed field journal, not JF/JFE/RFS); earlier as Federal Reserve Bank of New York Staff Report No. 193
url: https://doi.org/10.1016/j.jempfin.2009.02.003
citations: 104 (Crossref `is-referenced-by-count`, checked 2026-10-26)
sample_period: 1926Q3–2004Q4 (one conditioning variable, CAY, available only 1951Q4–2003Q2)
markets: US only — the 25 Fama-French portfolios sorted on size and book-to-market, plus the CRSP market factor
tier: B+ (peer-reviewed, long sample, mechanism derived rather than mined, and its own robustness checks are honest — but single-market, portfolio-level rather than name-level, and the headline evidence is specification-test pass/fail rather than out-of-sample forecasting)
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the economic member of tonight's cluster: a case where a latent state estimated by a
Kalman filter is not a smoothing convenience but **the quantity the theory says is priced**.

The setup. Keep the single-factor conditional CAPM, but let a name's factor loading `β_t` be
**unobservable** and let it drift. Specifically, `β_t` follows a mean-reverting AR(1) around a
long-run level `B`, optionally shifted by stationary conditioning variables `y_t`:

    β^i_{t+1} = (1 − F^i) B^i + F^i β^i_t + φ^i′ y_t + u^i_{t+1}

and — this is the paper's actual innovation — **`B^i` itself is unobserved too.** Investors do not
know a firm's long-run riskiness; they must infer both the current loading and its long-run level
from the history of realised returns. Rationality plus conditional normality then makes the
investors' belief about the loading evolve **exactly as a Kalman filter**, and the loading that
determines expected returns is the *filtered expectation*, not the realised loading:

    β^ie_{t+1|t} = (1 − F^i) B^ie_{t−1} + F^i β^ie_{t|t−1} + φ^i′ y_t + k^i_t (R^i_t − E_{t−1}[R^i_t])
    B^ie_t      = B^ie_{t−1} + K^i_t (R^i_t − E_{t−1}[R^i_t])

The second line is the mechanism in one equation. Because the *belief about the long-run mean* is a
**martingale** under the investors' information set, shocks to it never die out. That injects a
**slow-moving, highly persistent component** into perceived risk and therefore into required
returns: a name's riskiness in the distant past keeps a non-negligible weight in today's belief
about it. The authors' framing of the resulting empirical wedge is clean — if a name's systematic
risk has been *falling*, its filtered beta sits *above* an OLS beta fitted on recent data, so a
high required return is matched to a high *perceived* beta even while the measured beta is low.

The methodological corollary is the part with the longest reach, and it is stated in the abstract:
**a conditional model can be true and still be rejected by a standard OLS test, purely because the
test mismeasures the expectation investors were acting on.** The mismeasurement of the conditioning
object, not the model, produces the apparent alpha.

The specification explicitly *nests* the earlier conditional-CAPM literature: setting `u = 0`,
`F = 0` and `B` observable recovers the "betas are deterministic affine functions of state
variables" family; setting `φ = 0` with `B` observable recovers the autoregressive-beta family.
The paper's claim is that the **unobservability of `B`** is what does the work — and it says so
against itself: a variant in which `B` is an observable parameter estimated by maximum likelihood
alongside the rest produces **substantially larger pricing errors**. The result hinges on the
learning assumption, not on the filtering.

## Construction recipe

State space, per asset:

    R^i_{t+1} = β^i_{t+1} R^M_{t+1} + η^i_{t+1}                                  (observation)
    β^i_{t+1} = (1 − F^i) B^i + F^i β^i_t + φ^i′ y_t + u^i_{t+1}                 (state)
    B^i       : unobserved

so the **state vector is `(β^i_t, B^i_t)` — dimension two, per asset, estimated independently
across assets.** This is the shape the [2026-10-25] acceptance criterion asked for: `O(1)` per
name, never a joint `O(N)` state over the cross-section. The authors are explicit that cross-asset
correlation of betas is *not* in the state; it is pushed entirely into the conditioning variables
`y_t`, and error terms are assumed uncorrelated across assets.

Details that must be copied to reproduce it:

- **No intercept in the observation equation**, imposed as a model restriction for efficiency. The
  authors flag the obvious objection (omitting it could flatter their null by letting the mean of
  estimated betas soak up unexplained average return) and report results insensitive to including
  one.
- **Orthogonality of `η^i_{t+1}` to `R^M_{t+1}` is a necessary condition for the filter** and is
  proved in their appendix from the assumption that innovations to beta are idiosyncratic. A
  candidate that lets beta innovations correlate with the market has broken the estimator's
  premise, not merely stressed it.
- **Initialisation:** diffuse priors on the forecast error, and a prior of **1** for both
  `β^ie` and `B^ie` for every asset. The prior of 1 is the natural "no information ⇒ market
  beta" anchor.
- **Starting the filter early matters, and they say so:** the wedge between filtered and OLS betas
  exists only because the filter is allowed to run from the beginning of the long sample. Start it
  late and the persistent component has nothing to carry.
- **Pricing-error inference accounts for the fact that beta is estimated**, not observed — the
  paper devotes a subsection to the two methodological issues this raises.

**The parameter estimates themselves give a usable prior on magnitudes.** `F^i` — the persistence
of deviations from the long-run mean — is estimated around 20–35% for value portfolios and
insignificantly negative for growth, and the authors note that adding conditioning variables
absorbs some of that persistence (so `F` is not identified independently of the conditioning set).
The idiosyncratic return variance `σ²_η` and the beta-innovation variance `σ²_u` vary little across
specifications but **substantially across portfolios** — i.e. the right amount of filtering is a
per-name quantity, not a global constant. Of their four conditioning variables only the term spread
is consistently significant for the four portfolios they tabulate.

## Robustness evidence (qualitative only)

- **Multi-decade (about eight decades) but single-market and portfolio-level.** The test assets are
  25 US portfolios, not individual names. This is the main discount: an effect demonstrated on
  double-sorted portfolios of US stocks is not evidence about a global large-cap name panel.
- **The evidence is specification-test pass/fail, not forecasting.** Across every specification
  tried, the model *without* learning is rejected and the model *with* learning is not. That is a
  consistent pattern rather than a single lucky cut, and it is the right kind of robustness for an
  asset-pricing claim — but it is **not** out-of-sample return predictability, and must not be read
  as such.
- **The authors confront the main rival reading.** Lewellen–Nagel's critique is that measured
  covariation between beta and the market risk premium is too small to rescue the conditional CAPM.
  Adrian–Franzoni accept that finding for the *cyclical* covariation Lewellen–Nagel study and argue
  their channel is a different one — **low-frequency, idiosyncratic drift in the loading**, over
  horizons far longer than the business cycle. They also replicate the negative result: conditioning
  variables alone do not rescue the CAPM in time-series tests. Taking the critique on its own terms
  and then locating the claim outside it is unusually honest construction.
- **They test their own key assumption against itself** (the observable-`B` variant, which does
  worse) and check that `F` is stable in rolling windows before assuming it constant.
- **Qualitatively, filtered betas move more slowly than rolling-window OLS betas** — the authors
  attribute this directly to the Bayesian updating. This is the single most transferable empirical
  statement in the paper and the one the lab can act on.

## Implementability here

**This note's conclusion is a warning and a free screen, not a candidate. Read the warning first.**

**1. The trap: the Kalman recursion is causal, its hyperparameters are not.** The paper states
plainly that `F^i`, `σ²_η`, `σ²_u` and `φ^i` are **estimated by maximum likelihood on the whole
history**, while only the state is filtered recursively — and it *defends* this: "the econometrician
needs to estimate `F^i` efficiently, that is, using the entire data set", on the reasoning that
investors know the structural parameters even though they do not know `B`. That is a coherent
identification argument for an asset-pricing test and a **flat protocol violation here.** Under
`CLAUDE.md`'s machine-learning rules the lab's `causality_check` recomputes weights with the tail
hidden and fails anything whose holdings move; a filter whose variance ratio was fitted on the
visible window including the future *will* move. **The literature's standard practice is the exact
lookahead this lab's check is built to catch, and it is not flagged as such in the source, because
the source is not backtesting.** Any Kalman candidate written here must either refit hyperparameters
walk-forward (multiplying runtime by the number of rebalance dates) or fix them a priori — and by
`notes/2026-10-26-optimal-exponential-weights-signal-to-noise.md`, fixing them a priori is fixing
an EWMA span, which the lab can do in closed form.

**2. The obvious candidate is already priced as a null, and that must be said out loud.** The
mechanism's direct prediction is that expected return rises in the *filtered* beta. A long-only book
tilted toward high filtered beta is a beta tilt, and `learnings.md` has measured that Sharpe is
essentially flat in beta on this panel; `notes/2026-10-13-...` and the `beta-minus` closure
(`learnings.md`, 2026-09-17) make the same point from two other directions. **Do not spend a trial
on "rank by filtered beta".** The paper is an explanation of measured alpha, not a signal.

**3. Where the real tension is, and it is a genuine one.** `learnings.md` has twice closed free
per-name betas on estimation-error grounds — `SUMMARY.md` #96's free-beta regional residual (median
beta +0.874, IQR 0.944, 48.8% of names further than 0.5 from unity) and the 2026-09-12 market-factor
rerun (median 1.002, IQR 0.621, 29.1% beyond 0.5). Both screens used **rolling-window OLS betas**.
Adrian–Franzoni's qualitative finding is precisely that a filtered beta **varies more slowly** than
a rolling-window OLS beta. So the lab's refutation is of a *noisy* loading estimate, and the
literature's object is a *shrunk* one; **the measured IQR is in part the estimation noise a filter
is designed to remove.** That does not overturn the closure — the parameter-count triage rule still
says a filtered beta estimates one parameter per name where a unit loading estimates zero, and the
#96 result also turned on the group factor being priced with the *wrong sign*, which no amount of
shrinkage repairs. But it does mean the closure was never tested against the construction this
source proposes, and the folder should record that rather than let the refutation stand as broader
than the evidence.

**4. The free screen that resolves it, and it costs no trial.** Take the lab's existing rolling
per-name betas, smooth them with an EWMA at the span that
`notes/2026-10-26-optimal-exponential-weights-signal-to-noise.md` derives from the lag-1
autocorrelation of the beta series' own differences, and re-run the #96 / 2026-09-12 diagnostics on
the smoothed series. Two pre-committable outcomes: **(a)** the IQR collapses toward unity and the
score's information content is unchanged or better — the closure was about noise, and a shrunk
loading is worth one trial; **(b)** the IQR collapses and the score's cross-sectional information
collapses with it — the "variation" was the signal, the closure stands on wider ground than before,
and the vein shuts with a measurement instead of an argument. Either way the lab learns something
and the deflated-Sharpe bar does not move. Diagnostic work that scores no returns is free and
unlimited under `program.md`.

**5. Panel and data fit.** Implementable in principle: the observation equation needs only a name's
return and a market proxy return, both of which the lab holds (`SPY` or a regional ETF as the market
leg is allowed by the hindsight guard — ETF ids are permitted). The conditioning variables `y_t`
(term spread, CAY, value spread) are **macro series the lab does not have and may not fetch**, so
only the `φ = 0` specification is reachable here — which is the specification the paper shows is the
*weaker* one. State the restriction rather than pretending the full model is available.

**Pitfalls.** (i) The result needs a long burn-in; on names whose eligibility window is short — which
under protocol v2's point-in-time membership is many of them — the persistent component the
mechanism depends on has not had time to form, and the filtered beta is just the prior of 1. (ii)
The paper's assets are portfolios; individual-name betas are far noisier, so both the wedge and the
noise are larger at name level and the sign of the net effect is not implied by anything in the
source. (iii) Runtime: a two-state filter per name over ~1,000 eligible names is cheap *as a
recursion* and expensive *as a fit* — see the runtime arithmetic in the exponential-smoothing note.

## Related

- `notes/2026-10-26-exponential-smoothing-as-a-state-space-model.md` — why a two-dimensional state
  is the good case, and what the state-space wrapper does and does not buy.
- `notes/2026-10-26-optimal-exponential-weights-signal-to-noise.md` — the closed form that replaces
  this paper's full-sample MLE of the variance ratio, and the span for the screen in §4 above.
- `notes/2026-10-26-online-state-space-spreads-discount-factors.md` — the same trap recurring in a
  literature that was *explicitly designed* to avoid full-sample estimation, which is what makes it
  a pattern rather than one paper's choice.
- `experiments/learnings.md` — `SUMMARY.md` #96 (free beta loses to a unit loading, 2026-09-10);
  the market-factor residual rerun (2026-09-12); the `beta-minus` closure (2026-09-17); and the
  standing parameter-count triage rule. Section 3 above is the explicit tension between this source
  and those results, recorded rather than resolved.
