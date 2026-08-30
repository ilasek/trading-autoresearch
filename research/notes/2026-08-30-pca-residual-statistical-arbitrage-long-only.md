---
title: "Statistical Arbitrage in the U.S. Equities Market"
authors: Avellaneda, Lee
year: 2010
venue: Quantitative Finance (peer-reviewed, Tier 2 for this folder's purposes — not a top finance journal, heavily cited, practitioner-adjacent)
url: https://doi.org/10.1080/14697680903124632
citations: 338 (Semantic Scholar, DOI:10.1080/14697680903124632, checked 2026-08-30)
sample_period: 1997–2007 (PCA variants; correlation matrix needs a year of data from 1996), 2002–2007 (actual sector ETFs); trading thresholds calibrated on a 2000–2004 training subperiod
markets: US equities, roughly the universe of stocks above $1bn capitalisation, partitioned into 15 sectors
tier: B
validation_overlap: false
published_post_2018: false
---

The authors' 15 June 2009 working version read in full from the first author's Courant page
(`math.nyu.edu/faculty/avellane/AvellanedaLeeStatArb20090616.pdf`); the published article is
Quantitative Finance 10(7), 2010.

First note in this folder on `statistical-arbitrage`. `research/SUMMARY.md`'s open question
scoped this family narrowly — *what survives a long-only constraint* — and that is what the
Implementability section answers. The short answer is: the residual *ranking* survives, the
*hedge* does not, and the hedge is where the paper's market-neutrality came from.

## Mechanism

Decompose each instrument's return into a systematic part (its loading on a small set of
common factors) and an idiosyncratic residual. The residual is modelled as a stationary
mean-reverting process; when it wanders far from its own equilibrium, the model forecasts a
move back. This is "generalised pairs trading": instead of trading one stock against one
correlated stock, trade one stock against the group of factors that explains its systematic
variation.

The economic content is thinner than in the lead-lag family — there is no attention or
diffusion story, and the authors do not offer one. What they offer instead is a structural
claim with real teeth:

- **Mean reversion is a property of the residual, not of the price.** Whether reversion is
  measurable at all depends on *how much systematic variation you remove first*, and the
  relationship is **non-monotone**. Remove too little (a single market factor) and residuals
  are dominated by leftover common variation: the estimated reversion is slow and residual
  volatility is high. Remove too much (many factors, high explained-variance targets) and
  what is left is noise: the reversion is real but tiny, and trading costs eat it. The
  authors' phrase for the second failure is "noise trading", and they report it as a
  *steady loss*, not a weak gain.
- **The factor set can be estimated rather than assumed.** Principal components of the
  correlation matrix give an orthogonal factor set with no sector taxonomy required. The
  authors note the first eigenvector has all-positive coefficients (a market portfolio), that
  its implied weights are ∝ vᵢ/σᵢ — i.e. **inverse-volatility weighted**, which is why it
  proxies a capitalisation-weighted index well — and that higher eigenvectors are "coherent":
  neighbouring coefficients belong to the same industry, so the eigenportfolios read as
  long-short industry bets. Coherence decays as you descend into the noise spectrum, which
  is itself a diagnostic for how many factors are real.
- **The residual carries no exploitable drift at this horizon.** The authors extend the
  signal with an estimated drift term (a "modified s-score", equivalent to adding the slope
  of a 60-day moving average — a built-in momentum overlay) and report the effect on results
  is minor. Their own reading: after controlling for industry/size factors, stock returns
  have negligible momentum at this trading scale. Worth recording as an **anti-candidate**:
  bolting a trend term onto a residual-reversion signal is a tried and reportedly empty
  refinement.

## Construction recipe

Everything below is estimated on a strictly backward-looking window, so the design is
causal by construction — the authors are explicit that the residual estimate at time *t*
uses only the prior 60 days.

**Factors, two ways.**
- *PCA.* Standardise returns, take the correlation matrix over a 252-day window, keep the
  top *m* eigenvectors, form eigenportfolio returns with weights Q⁽ᵏ⁾ᵢ = v⁽ᵏ⁾ᵢ / σᵢ. The
  eigenportfolio returns are uncorrelated by construction. Equivalent to modelling the
  correlation matrix as rank-*m* plus a diagonal noise matrix chosen so the diagonal stays 1.
- *Sector ETFs.* Assign each instrument one sector ETF and regress its returns on that ETF
  alone. Simpler, but ETF returns are correlated across sectors, so a full multi-ETF
  regression produces unstable offsetting loadings; the authors' fixes are either the
  one-ETF-per-name simplification they use, or a sparse/penalised regression (they name
  matching pursuit and ridge).

**How many factors.** Two schemes, both reported:
- Fixed count (they use 15 on a US large-cap universe).
- Variable count, chosen each day so that the retained eigenvalues explain a fixed
  percentage of the trace of the correlation matrix. They compare 45% / 55% / 65% / 75% and
  1 factor and 15 factors. 55% is the best of the variable-target schemes and is roughly
  comparable to (slightly behind) the fixed 15. **75% loses steadily.** One factor is worst.
  The number of components required to hit a fixed explained-variance target is itself
  time-varying: it falls when cross-sectional correlation concentrates and rises when
  variance is spread across many modes. That is a free regime statistic, computable from the
  same eigendecomposition.

**Residual model and signal.**
- Fit the residual *Xᵢ(t)* on a 60-business-day window as an Ornstein–Uhlenbeck process
  (equivalently an AR(1) on the cumulative residual), giving speed of reversion κᵢ, mean
  mᵢ, and volatility σᵢ. The window length is chosen as roughly one earnings cycle.
- Equilibrium standard deviation σ_eq,i = σᵢ / √(2κᵢ). Define the **s-score**
  `sᵢ = (Xᵢ(t) − mᵢ) / σ_eq,i` — the residual's distance from its own equilibrium in
  standard deviations. Dimensionless, so one set of thresholds serves all names.
- **Reject names whose reversion is too slow:** require κᵢ > 252/30 ≈ 8.4, i.e. a
  characteristic reversion time τᵢ = 1/κᵢ under 30 days — about half the estimation window,
  so the constant-parameter assumption is not being stretched. When κ falls below the
  threshold the model is rejected for that name: no new position, and existing ones closed.
  Typical estimated reversion times in their data are on the order of a week.
- Trade rule: open when |s| exceeds 1.25, close a long at s = −0.50, close a short at
  s = +0.75 (deliberately asymmetric, calibrated on a training subperiod, and reported as
  such). Positions are **"bang-bang"**: full size on when the signal fires, off when it
  closes, with no continuous rebalancing toward a target — which the authors report
  outperforms continuous adjustment, they suspect because the model is misspecified and
  continuous tracking just trades the misspecification.
- Sizing: each position is a fixed fraction Λ of equity, Λ chosen for a target gross
  leverage; Λ doubles as a per-name concentration cap.
- Costs: a flat 5 bps slippage per trade (10 bps round trip), applied to the absolute change
  in each position's dollar value.

**Volume as a return rescaling ("trading time").** Rather than using volume as a sorting
variable, rescale returns by how much trading produced them:

    R̃ₜ = Rₜ × ( ⟨δV⟩ / ΔVₜ )

where ΔVₜ is volume over the interval and ⟨δV⟩ a trailing average daily volume (they use a
10-day window — short enough to sit inside the 60-day estimation window, long enough to
average spikes; explicitly not optimised). A move on heavy volume is shrunk, a move on light
volume is inflated. The economic reading: a large price change accompanied by heavy trading
is more likely to be information than an excursion worth fading, so **the rescaling
discourages fading high-volume moves**. Reported to help the ETF-based signals unequivocally
and to do little for PCA-based ones.

## Robustness evidence (qualitative only)

- Two structurally different factor constructions (statistical and taxonomic) give
  qualitatively similar signals, which is the paper's main internal robustness check.
- The non-monotone factor-count result is established across six configurations, and the
  failure mode at high factor counts is attributed to costs — a mechanism, not just a
  weaker number.
- The design is genuinely out-of-sample in the causal sense (rolling backward windows) and
  costs are modelled, if simply.
- The thresholds are calibrated on a training subperiod and the authors say so.
- **Gaps.** Single market, single sample, one author team, no independent replication known
  to this folder. Multiple testing is not addressed. The universe is
  survivorship-relevant (US large caps as of a point in time) without the paper discussing
  it. Published in a quantitative-finance venue rather than a top finance journal, and the
  literature it builds on (Lehmann, Lo–MacKinlay) is far better replicated than this
  specific construction is. Treat the *construction rules* as well-motivated craft and the
  *result* as unreplicated.
- The tier-1 antecedent this folder already holds — short-horizon reversal as compensation
  for liquidity provision — is the reason to expect the effect to be real and the reason to
  expect it to be uncollectable by a fee-paying taker.

## Implementability here

**The central problem: the hedge is the strategy, and this book cannot hold it.**
Every position in the source is a stock against βᵢ dollars of its factors. The residual is
what is traded; the factor leg is what makes the residual *tradeable* rather than merely
*measurable*. A long-only book with gross ≤ 1.0 can hold only the cheap side. What survives
is not a market-neutral residual portfolio but a **long book whose cross-sectional weights
are tilted by a residual signal** — its returns dominated by the market exposure it cannot
remove. That is the mechanism-level reason this family cannot deliver decorrelation here,
and it matches what the lab has already measured directly: five long-only family leads from
five different mechanisms correlate 0.75–0.85 with each other. Removing factor structure
from the *signal* does not remove it from the *book*.

So the honest framing for a candidate is: **"does a residual s-score rank names better than
a raw price rank?"** — a selection question — and not "does residual reversion earn an
uncorrelated premium", which the long-only constraint forecloses. Read
`notes/2026-08-22-long-only-as-l1-regularization.md` first: the constraint is an estimator as
well as a leak, and on a signal this noisy the shrinkage may be worth more than the lost leg.

**The tension with the lab's own screen, stated rather than resolved.** `learnings.md`
records that on the train split, residualising 5-day reversal made it *worse* — raw reversal
IC beat one-factor, PCA k=3 and PCA k=5 residuals, monotonically the wrong way — and the
family was declined. This source's own results say the same thing about the low end of that
range: one factor is the *worst* configuration they test, for a stated reason (slow measured
reversion, high residual volatility). The lab's tested range, k ∈ {1, 3, 5}, sits entirely
in the region this source also found worst, and its reported optimum — ~15 factors, or a
55%-explained-variance target — was not tested. **This is a tension, not a refutation of the
lab's result**, for three reasons that must be stated with it:

1. Scaling does not transfer. 15 factors on a universe of many hundreds of names is a very
   different factor-to-name ratio than 15 on ~140 instruments; the "too many factors ⇒ noise
   trading" failure would arrive at a lower count here, and the explained-variance target,
   not the count, is the transferable parameter.
2. The two measurements are of different objects. The lab measured an **unconditional
   cross-sectional IC** of a residualised reversal signal. This source trades a
   **conditional excursion**: only names whose residual is more than 1.25 equilibrium
   standard deviations from its mean *and* whose estimated reversion speed clears a
   threshold. An unconditional IC can be null while the conditional tail trade is not; the
   κ-filter and the s-score threshold are precisely the parts a plain IC screen discards.
3. The cost gap runs the wrong way. This source pays 5 bps per trade against this repo's 15,
   and its characteristic holding period is on the order of a week. The configuration it
   reports as *losing money* is the one where costs overwhelm a small residual — which is
   the regime a 3×-more-expensive book starts in.

**If a follow-up trial is run in this family, the cheap discriminating version is:** hold the
factor count fixed by an explained-variance target rather than by count; add the κ-filter
and the |s| > threshold conditioning that the earlier screen lacked; and rebalance monthly,
not daily. Report the gross-versus-net decomposition explicitly, because `learnings.md`'s
standing finding is that outside `price-trend` a turnover difference swamps every mechanism
difference the lab tries to measure.

**Things that port cleanly and cheaply.**
- The **s-score** is a well-specified, dimensionless, causal cross-sectional statistic:
  residual distance from its own equilibrium in units of √(σ²/2κ). It is strictly better
  specified than "trailing n-day return" as a reversal signal, whatever the factor count.
- The **κ-filter** as a general design idea: only take a mean-reversion bet in names where
  the estimated reversion time is short relative to the estimation window. This is a
  falsifiable admissibility condition, and nothing in this lab's reversal work has used one.
- The **explained-variance factor count as a regime statistic** — the number of components
  needed for a fixed variance share, computable from the same eigendecomposition, is a
  free `range-variance`-adjacent measure of cross-sectional correlation concentration.
- The **trading-time volume rescaling** is directly computable from the repo's
  `volume`/`dollar_volume` panels and is a *different* use of volume from anything the lab
  has tried (a return transformation, not a sort). Its economic content — do not fade a move
  that came with heavy trading — is testable on its own, on any reversal signal, without the
  rest of this apparatus. Watch the NaNs: volume is not forward-filled, so the denominator
  must skip foreign holidays rather than treat them as zero volume, or the rescaling
  explodes exactly on the days the panel is thinnest.

**Do not port:** the bang-bang all-or-nothing sizing (it is a turnover machine under a
15 bps/side model, and the reason it wins in the source — avoiding tracking of a misspecified
model — is cheap to obtain here instead by rebalancing less often), the specific 1.25/0.75/
0.50 thresholds (calibrated on another universe and another cost level), and the drift
extension (reported as adding nothing).

## Related

- `notes/2026-08-22-long-only-as-l1-regularization.md` — the prior `SUMMARY.md` names as the
  right one to read before this family; the long-only constraint as shrinkage rather than
  pure loss.
- `notes/2026-08-17-short-term-reversal-as-liquidity-provision.md` — why short-horizon
  reversal exists and why a cost-paying taker is on the wrong side of it. This is the
  standing structural objection to the whole family here.
- `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md` — the other volume use in
  this session; there volume sorts names, here it rescales returns.
- `notes/2026-08-29-range-based-volatility-estimators.md` — σ estimation quality feeds
  directly into σ_eq and hence into the s-score's denominator.
- `notes/2026-08-21-weight-constraints-as-covariance-shrinkage.md` and
  `notes/2026-08-18-risk-parity-equal-risk-contribution.md` — the inverse-volatility reading
  of the first eigenportfolio connects to both.
- `experiments/learnings.md` — the declined `statistical-arbitrage` screen this note is in
  tension with, and the long-only decorrelation finding that bounds what the family can be
  worth here.
