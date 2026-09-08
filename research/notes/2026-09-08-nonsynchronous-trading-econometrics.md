---
title: "An Econometric Analysis of Nonsynchronous Trading"
authors: Lo, MacKinlay
year: 1990
venue: Journal of Econometrics 45(1–2), 181–211 — Tier 1 (peer-reviewed)
url: https://doi.org/10.1016/0304-4076(90)90098-E — read from NBER Working Paper 2960 (May 1989), https://www.nber.org/system/files/working_papers/w2960/w2960.pdf
citations: 588 (Crossref, DOI:10.1016/0304-4076(90)90098-E, checked 2026-09-08). **Eleventh instance of the standing "disbelieve a lone count" rule**: Semantic Scholar returns *not found* for the same DOI, and OpenAlex resolves it to a record merged with the NBER working paper carrying a count of 3. Crossref is the only usable count here, and the two failures are of opposite kinds — one index missing the paper, one index holding it under a working-paper identity.
sample_period: 1962–1987 (CRSP daily/weekly/monthly, twenty size-sorted portfolios) for the empirical section only; the theory is sample-free
markets: US equities (CRSP NYSE/AMEX), size-sorted portfolios
tier: A
validation_overlap: false
published_post_2018: false
---

Read **in full** from the NBER working-paper version, which carries the complete argument
including both propositions, the time-aggregation section, the empirical section and the
extensions. The scan has **no text layer** — `pypdf` extracted 38 characters from 39 pages — so
it was read the way `2026-09-05-cross-serial-correlation-as-restatement.md` was read: rendered
page by page to PNG with `pymupdf` at 140 dpi and read visually. That is now the second time this
channel has been needed and it works reliably; `pymupdf` also removes the `pdftoppm` dependency
the README notes is missing.

**This is not the Lo–MacKinlay 1990 the folder already holds.** `2026-09-05-contrarian-profit-
decomposition.md` covers *"When Are Contrarian Profits Due to Stock Market Overreaction?"* (RFS
3(2)). This is a different paper in a different journal in the same year, and it is the one that
supplies the *measurement model* the contrarian decomposition and the lab's own regional results
both need.

## Mechanism

The question is not a strategy. It is: **what does a correlation matrix estimated from closing
prices measure, when the closes are not simultaneous?** A daily close is the last transaction
price, and last transactions do not happen at the same instant across securities — still less
across fifteen trading sessions. If news arrives near the end of a session, a security that has
already stopped trading incorporates it only in the next observation. The observed return series
is therefore a randomly time-shifted, randomly cumulated version of the unobservable "virtual"
return series, and its second moments are not the virtual ones.

The model is deliberately minimal. Security `i` fails to trade in any period with probability
`p_i`, independently across periods and securities (`δ_it` i.i.d. Bernoulli). When it does not
trade the observed return is zero; when it trades, the observed return is the **sum of the
virtual returns over the whole run of consecutive non-trading periods just ended**. Virtual
returns follow a one-factor model, `R_it = μ_i + β_i Λ_t + ε_it`. The non-trading duration
`k̃_t` then has `E[k̃] = p/(1−p)` and `Var[k̃] = p/(1−p)²` — at `p = ½` a security sits out one
period at a time on average, at `p = ¾`, three.

Everything below follows from that, in closed form.

### Individual securities (Proposition 2.1)

    E[R°_it]   = μ_i                                  — the mean is untouched
    Var[R°_it] = σ_i² + (2p_i / (1−p_i)) μ_i²          — the variance is inflated, but only if μ ≠ 0
    Cov[R°_it, R°_i,t+n] = −μ_i² p_i^n     (n > 0)     — negative, geometrically decaying
    Cov[R°_it, R°_j,t+n] = [(1−p_i)(1−p_j)/(1−p_i p_j)] β_i β_j σ_Λ² p_j^n   (i ≠ j, n ≥ 0)

Read the first-order own-autocorrelation: it is proportional to `μ²` and therefore **vanishes for
a zero-mean security**. Its most negative attainable value is `−(|ξ|/(1+√2|ξ|))²` where
`ξ = μ/σ`, with infimum `−½` as `|ξ| → ∞` and never attained at finite `ξ`. For daily returns
`ξ` is of order 0.1, so this bound is small; the authors report that even at an extreme
`ξ = 0.21`, the induced *weekly* first-order autocorrelation reaches at most about −8% and
requires a daily non-trading probability above 0.90 — which by `E[k̃] = p/(1−p)` means an average
run of nine consecutive non-trading days.

### Portfolios (Proposition 2.2) — where the effect actually lives

Group securities by their non-trading probability and equal-weight within group. As the group
size grows,

    Var[R°_κ]                = β_κ² ((1−p_κ)/(1+p_κ)) σ_Λ²
    Corr[R°_κt, R°_κ,t+n]    = p_κ^n                              (n ≥ 0)
    Cov[R°_at, R°_b,t+n]     = [(1−p_a)(1−p_b)/(1−p_a p_b)] β_a β_b σ_Λ² p_b^n

Three things flip relative to the individual case, and every one of them matters more here than
the individual-security result does.

1. **The sign flips and the mean drops out.** Portfolio autocorrelation is `p^n` — *positive*,
   equal to the non-trading probability itself, and independent of `μ`. Diversification does not
   average the artifact away; it converts a small negative one into a large positive one. An
   observed portfolio return series is an exact AR(1) with autoregressive coefficient `p`. The
   authors' own summary: "If the non-trading phenomenon is extant it will be most evident in
   portfolio returns."
2. **Variance is *deflated*, not inflated.** `(1−p)/(1+p) < 1`. Volatility estimated from a
   stale-closing series understates the true volatility of the underlying.
3. **The lagged cross-covariance is asymmetric, and the asymmetry is pure measurement.** The
   `p_b^n` factor attaches to the *lagging* security only, so

        γ_ab(n) / γ_ba(n) = (p_b / p_a)^n

   — the "A leads B" pattern appears whenever `p_a < p_b`, with no lead-lag mechanism present at
   all. The authors state this as the origin of the size-sorted lead-lag patterns in their own
   earlier work.

### The identification result, which is the paper's most useful export

Because the whole lagged covariance structure is generated by one number per portfolio, the
model is **heavily overidentified**. For any chain of distinct portfolios `κ_1 … κ_r`,

    [γ_aκ1(n) γ_κ1κ2(n) … γ_κr b(n)] / [γ_κ1a(n) γ_κ2κ1(n) … γ_bκr(n)]  =  (p_b / p_a)^n

so with `N_p` portfolios the `N_p²` distinct lagged covariances are constrained to
`N_p(N_p+1)/2` free parameters. That is a **specification test with no free lunch attached**: a
lagged cross-covariance matrix generated by non-synchronicity must satisfy every one of those
restrictions, and one generated by a genuine information-diffusion mechanism has no reason to.

### Time aggregation (Proposition 3.2)

Sampling at `q` of the base periods:

    Var[R°_κτ(q)]                  = [q − 2p_κ (1−p_κ^q)/(1−p_κ)] β_κ² σ_Λ²
    Corr[R°_κτ(q), R°_κ,τ+n(q)]    = (1−p_κ^q)² p_κ^{nq−q+1} / [q(1−p_κ²) − 2p_κ(1−p_κ^q)]

and for the contemporaneous cross-portfolio covariance the bracket is
`q − [p_a(1−p_a^q)(1−p_b)² + p_b(1−p_b^q)(1−p_a)²] / [(1−p_a)(1−p_b)]`. The structure of both is
the same: **the induced term is bounded in `q` while the signal term grows linearly in `q`**, so
the relative contamination falls like `1/q`. Portfolio autocorrelation is monotonically
decreasing in `q` at every `p`; the lagged cross term carries `p^{nq−q+1}`, which collapses
geometrically in `q`. Aggregation is the fix, and it is a rate, not a threshold.

### A derived corollary this repo should carry (derived here, not stated in the paper)

Divide the `n = 0` cross-covariance by the two portfolio standard deviations. The virtual
portfolios are perfectly correlated in the limit (both are `μ_κ + β_κ Λ_t`), so the observed
correlation *is* the attenuation:

    ρ°_ab  =  √((1−p_a²)(1−p_b²)) / (1 − p_a p_b),   equivalently
    (ρ°_ab)²  =  1 − [ (p_a − p_b) / (1 − p_a p_b) ]²

**The attenuation depends only on the difference between the two groups' non-trading
probabilities, and is exactly 1 when they are equal.** Two groups sampled equally staleley are
measured without bias; two groups sampled differently are measured with a downward bias in their
contemporaneous correlation that carries no information about the assets. This is algebra from
their (2.24) and (2.27) and is offered as such — the paper does not write it down — but it is
the form the lab needs, because *the difference of within-group and cross-group mean correlation
is precisely this attenuation*, and measuring it identifies `|p_a − p_b| / (1 − p_a p_b)`.

## Construction recipe

There is no strategy here. The recipes are estimators and tests.

- **Estimate `p_κ` for any group directly**: it is the `n`-th root of the `n`-th order
  autocorrelation of the group's observed return series. First-order autocorrelation alone
  suffices, and unlike the individual-security estimator it needs no mean return.
- **Estimate relative `p`'s from asymmetry**: `p_b/p_a = [γ_ab(n)/γ_ba(n)]^{1/n}`, then check
  the estimate is stable across `n` — the model says the `n = 2` ratio must be the square of the
  `n = 1` ratio.
- **Test the model**: impose the chain restrictions above across all groups. Consistency is
  evidence the pattern is measurement; violation is evidence it is not.
- **Correct by aggregation**: recompute the moment of interest at `q = 5, 10, 21` and read the
  trend. The bias falls like `1/q`, so a single weekly reading is a partial correction, not a
  clean one, and the *sequence* is more informative than any one horizon.

## Robustness evidence (qualitative only)

Tier-1 peer-reviewed, from authors with the defining track record in this exact area, and the
theory is closed-form algebra that cannot decay. It generalises the earlier non-trading models
(Fisher; Scholes–Williams 1977; Cohen et al.; Dimson 1979) by letting the non-trading process be
stochastic and unbounded rather than confined to a fixed interval, and by delivering portfolio
and cross-portfolio moments rather than beta corrections. The extensions section states, without
full derivation, that the results survive an autocorrelated common factor, cross-sectionally
correlated disturbances, multiple factors, and a Markov-chain (rather than i.i.d.) non-trading
process — under the last, sign reversals become *possible* but the authors judge them unlikely
at empirically relevant parameters.

**The paper's own conclusion is negative, and it is the single most important thing in it to
record honestly.** Applied to US common stocks, the magnitudes do not work. Using non-trading
probabilities estimated four different ways and two sets of betas, the largest implied
first-order autocorrelation for a weekly equal-weighted index is about **7.5%**, and using direct
estimates of non-trading it is **under 2%** — against an observed index autocorrelation several
times larger. Their verdict: the evidence "provide[s] little support for nonsynchronous-trading
as an important source of spurious correlation in the returns of common stock."

**So the mechanism is real, exactly quantified, and empirically small — for a single-country
universe of actively traded stocks sampled at a common close.** Whether it is small for a
universe spanning fifteen trading sessions is a question the paper does not address and this note
must not answer for it. What can be said structurally: their `p` is a probability of *no trade*,
and a liquid Tokyo-listed instrument trades every day, so `p ≈ 0` on their reading. The quantity
that plays `p`'s role across time zones is the fraction of a US-session day's information that a
foreign close cannot yet contain — a *systematic* offset, not a random censoring, and the model
does not claim to cover it. Treat the algebra as the right functional form and the US magnitudes
as evidence about US single-name data only.

## Implementability here

Nothing to build. This is a measurement note, and it lands on four things the lab already does.

**1. It supplies the missing formula for an artifact the lab has now measured twice
independently.** 2026-09-06 measured a ~4x session-offset artifact in regional cross-serial
residuals; 2026-09-07 measured same-region-minus-different-region mean pairwise correlation at
**+0.144 on daily returns against +0.030 on weekly**, a 4.8x ratio, and drew the correct rule
("any clustering built here must use weekly returns"). The derived corollary above is exactly
that statistic: within-group pairs share a `p` and are unattenuated; cross-group pairs differ in
`p` and are attenuated by `√((1−p_a²)(1−p_b²))/(1−p_a p_b)`. The lab's number is the attenuation,
and it identifies the implied `|p_a − p_b|/(1 − p_a p_b)` directly — turning a measured ratio
into a *parameter*, which can then be checked against the paper's other predictions on the same
data. Two independent measurements of the same artifact and a closed-form generator for it is
the point at which the lab should stop rediscovering it.

**2. It sharpens the `lead-lag-spillover` closure rather than reopening it.** The lab's #78
resolved into "measurement in one partition, a forbidden-horizon cross-asset effect in the
other". The overidentifying restrictions are a stronger test than any run so far and they cost
no trial: they say the whole regional lagged cross-covariance matrix must be generated by fifteen
numbers. This does not reopen a family the lab has closed — it converts "we think this partition
is measurement" into a testable statement that can fail. See candidate #89.

**3. It names a bias in a number the lab prices every blend on, and the direction is not
obvious.** The required-gain table is read off `rho` between a candidate's and the champion's
return series, and the paired standard error `sqrt(1−rho)` is the resolution floor for every
promotion decision. If those series are computed from daily USD closes and the two books differ
in regional composition — which the seated `liquidity-volume` lead, a *region-relative* `ILLIQ`
construction, does by design — then their measured contemporaneous correlation is attenuated by
the factor above. An attenuated `rho` inflates the paired SE and pushes the required-gain table
*upward*, so the error is conservative rather than permissive; but it is an error in the one
number eight consecutive sessions of blend declines rest on. **Free measurement: recompute the
champion-versus-leg `rho` at `q = 1, 5, 10, 21` and report the sequence.** Flat means the two
books have the same effective `p` and the daily number is clean; rising in `q` means it is not,
and the model says the `1/q` trend identifies how much. See candidate #90.

**4. A standing caution for `range-variance` and any volatility-weighted construction.**
`Var[R°_κ] = β_κ²((1−p)/(1+p))σ_Λ²`: close-to-close volatility estimated on a group whose closes
are stale relative to the information flow is biased **downward**, and unequally so across
regions. Any construction that ranks or weights on close-to-close volatility across this
universe's fifteen sessions inherits that bias as a regional tilt. The family is closed fourteen
times over and this is not an argument to reopen it; it is a reason not to trust a cross-regional
volatility *ranking* in any family.

**Known pitfalls.** The `p^n` estimator is an autocorrelation, and this repo's standing habit
applies: 2026-09-07 killed a `DELAY` statistic that reproduced its own null in level, dispersion
*and* persistence. Any `p` estimated here should be simulated under a no-lag null before it is
believed, and the overidentifying restrictions are the natural placebo — a null that satisfies
them is measurement, one that fails them is something else. Second, the model assumes i.i.d.
Bernoulli censoring; a systematic time-zone offset is a *deterministic* lag, and the correct
reading of a `p` estimated here is "the i.i.d.-censoring parameter that would produce the same
second moments", not a trading probability.

## Related

- `notes/2026-09-05-contrarian-profit-decomposition.md` — the *other* Lo–MacKinlay 1990. That
  paper decomposes contrarian profits into own- and cross-autocovariance terms; this one says how
  much of the cross term a measurement artifact can generate, and gives the test that separates
  them.
- `notes/2026-09-05-cross-serial-correlation-as-restatement.md` — Boudoukh–Richardson–Whitelaw's
  point that a cross-serial pattern can be a restatement rather than a mechanism. This is the
  structural model behind one of the two candidate restatements, with its magnitudes attached.
- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` and
  `notes/2026-09-05-price-delay-market-frictions.md` — both use Dimson-style lagged regressions;
  this note is the model those corrections were built for.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md` — the "build the distance
  matrix on weekly returns" rider, which this note derives rather than observes.
- `notes/2026-08-29-range-based-volatility-estimators.md` — range estimators are within-day and
  therefore immune to the close-staleness bias in point 4, which is a point in their favour that
  the folder has not previously stated.
