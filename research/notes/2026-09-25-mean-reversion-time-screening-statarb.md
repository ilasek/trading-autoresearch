---
title: "Risk Control of Mean-Reversion Time in Statistical Arbitrage"
authors: Yeo, Papanicolaou
year: 2018 (journal issue; working paper 2016, draft read dated December 2017)
venue: Risk and Decision Analysis 7(1–2), 1–23 — Tier 3/4 (peer-reviewed but a low-tier venue outside finance)
url: https://doi.org/10.3233/rda-170132
citations: 14 (Semantic Scholar, checked 2026-09-25); 8 (Crossref, checked 2026-09-25)
sample_period: 2000–2014 (daily), with the trading evaluation reported over 2005–2014
markets: US equities — 378 S&P 500 names with a complete price history over the sample
tier: C
validation_overlap: false
published_post_2018: false
---

**Text read**: the authors' own manuscript, in full, from
`http://math.stanford.edu/~papanico/pubftp/RDA_manuscript.pdf` (the Stanford faculty-page channel
again — first hit, no publisher involved). **Deliberately omitted from this note**: the paper's
entire empirical section is organised into dated two-year regime windows with event labels
attached to each. That is the shape `research/README.md` bans outright, so nothing from it is
recorded here and nothing below depends on it. What is recorded is the construction and the
parameter-sensitivity *shapes*, which is where this paper's value for the lab lies anyway.

**Why a Tier C source gets a note at all.** Two reasons, and they should both be visible to
whoever reads this. First, it is one of the two classical benchmarks that
Guijarro-Ordonez–Pelger–Zanotti (Management Science; see
`notes/2026-09-25-deep-learning-statistical-arbitrage-residual-construction.md`) name and
implement as the state of the art they are arguing against — so its construction is load-bearing
in a Tier-1 paper even though its own venue is weak. Second, its contribution is **two screens**,
and a screen is the one kind of object in this vein that survives the long-only constraint intact.
The tier is C for its evidence and should not be leaned on for any expectation about size.

## Mechanism

Classical residual arbitrage (Avellaneda–Lee) assumes each residual is an Ornstein–Uhlenbeck
process and trades its normalised deviation. The paper's observation is that this makes the whole
strategy depend on an estimated quantity — the **mean-reversion speed** `kappa`, equivalently the
reversion *time* `tau = 1/(kappa * dt)` — which is estimated separately for every name, is widely
dispersed across names, is **not stable over time**, and is known to be **biased** by every
standard estimator (least squares, ML and GMM all produce biased `kappa` in short samples; the
literature's fixes, e.g. jackknifing, are cited but not used here).

The resulting risk is structural rather than statistical: if a residual's estimated reversion is
too slow, a position opened on it has no reliable closing time, so capital is held against a
deviation that may not come back inside the holding horizon. The response is to **not trade
those residuals at all** rather than to trade them smaller. Three layers, addressed to three
distinct failure modes:

1. **Strategic reliability** — a residual whose estimated reversion is slow is excluded from the
   investable set. The premise offered is economic, not just statistical: names with a more
   distinguishable correlation structure have residuals that are better decoupled from the common
   factors, hence less trending.
2. **Estimation reliability** — even among selected names, a *particular* signal is refused when
   the OU fit that produced it is poor. Quality of the fit, not size of the deviation, decides
   whether the signal is actionable.
3. **Temporal reliability** — the selection is refreshed on a schedule, because the ranking by
   reversion speed decays as the correlation structure moves.

## Construction recipe

**Residuals** (Avellaneda–Lee's construction, reproduced):
- Normalise returns `M_it = (R_it - mean_i)/sigma_i` over a window `T`; correlation matrix
  `C = (1/T) M M'`; eigendecompose.
- **Eigen-portfolio weights** `q_m^i = v_m^i / sigma_i` — the `1/sigma_i` rescaling is deliberate
  and its stated purpose is to stop the factors being dominated by the volatility level of their
  constituents. Factors are `F_m = <q_m, r_t>`.
- Regress returns on the estimated factors (multivariate least squares) for loadings `L`;
  residuals `U = R - L F`.

**OU calibration**: discretise to an AR(1) on the *integrated* (cumulative) residual `X_it`,
estimate `(kappa, m, sigma)` by least squares per name per date, with the equilibrium standard
deviation `sigma_tilde_i = sigma_i / sqrt(kappa_i)`.

**Screen 1 — selection by reversion speed.** Quality score
```
QS_i = (1 / T_train) * sum over the training window of kappa_hat_i,n
```
i.e. the time-average of the name's estimated reversion speed over a training window. Rank, keep
the top `n`. Sizes tested: 25/50/75/100 out of 378. Note the normalisation caveat the authors
flag: `kappa_hat` depends on the estimation-window length, so the score is only comparable across
names when the window is held fixed — which it is here, and must be anywhere it is used.

**Screen 2 — selective trading by goodness of fit.** Accept a signal only when the OU regression's
`R^2 > eta`, for a cutoff `eta` in (0,1). This is a gate on the *estimate*, not on the *signal*,
and it is the part with no analogue anywhere in this lab's current machinery.

**Screen 3 — refresh.** Re-run the selection every estimation window (selection interval set equal
to the estimation window length, for consistency of the information used).

**Trading rule** (classical, recorded for completeness):
```
s_it = (X_it - m_i) / sigma_tilde_i
open short  s > +1.25   ->  close short  s < +0.5
open long   s < -1.25   ->  close long   s > -0.5
```

**Constraints**, imposed in the allocation optimisation rather than by construction:
- **Factor neutrality**: `sum_i L_ik q_it = 0` for *each* factor `k` — note this is `p`
  constraints, one per factor, not one market constraint.
- **Dollar neutrality**: long and short dollar amounts equal.
- A fixed total leverage, so portfolio size changes the dispersion of weights and not the gross.

**Parameter grid actually explored**: estimation window 30/60/90/120 days; 5/10/15/20 factors
removed; portfolio size 25/50/75/100.

## Robustness evidence (qualitative only)

- **A factor-count ceiling, measured on a universe of 378 names**: removing more than about **30**
  principal components leaves residuals too noisy to estimate reversion from, so the usable range
  is well below that. On ~140 instruments the analogous ceiling is lower still — a ratio argument,
  not a transplant, and it should be re-measured rather than scaled.
- **Shorter estimation windows are more sensitive to transaction costs.** Stated by the authors
  as the expected direction, and it is: a shorter window produces a faster-moving signal, hence
  more round trips. The transferable form is that the estimation window and the cost budget are
  not independent choices.
- **Portfolio size helps stability but not monotonically** — the largest tested set was not the
  best. Consistent with the folder's standing material on effective breadth versus nominal count.
- **Equal allocation across selected names, ignoring the optimisation, is unstable**, and the
  stated reason is mechanical: equal amounts do not satisfy the factor-neutrality conditions.
  This is a caveat *about long-short books specifically* and does not transfer to a long-only
  book, where there is no neutrality condition to violate — see below, and contrast with the
  2026-09-24 nightly's finding that equal weighting beat an estimated-variance weighting on this
  repo's own universe.
- **What is missing, and it is why the tier is C**: single market, single sample, one research
  group, no independent replication, no multiple-testing treatment for a design with at least four
  swept parameters, and results reported by dated regime rather than as a pooled test. The OU
  estimator bias is acknowledged and then not corrected.

## Implementability here

**The screens transfer; the strategy does not.** The trading rule is a long-short, factor-neutral,
dollar-neutral book with daily position management — none of which is reachable under this repo's
constraints. But both screens are **membership rules**, and this is the general point worth
carrying past this note:

> A neutrality constraint needs both legs and dies under a long-only budget. A **selection**
> screen does not: refusing to hold a name costs nothing and requires no short. So when adapting a
> statistical-arbitrage construction to a long-only book, the reachable part is almost always the
> part that decides *membership*, and the unreachable part is the part that decides *hedging*.

That is directly relevant to the seat this lab currently holds: the promoted `E/Var` term is
itself a membership rule built from a local correlation structure, and both screens here are the
same species of object.

**Two specific, cheap things a session could do with this, neither of them requiring a trial:**

1. **Reversion-speed selection as a screen on an existing score.** Fit an AR(1) on each name's
   cumulative residual from a PCA factor model over a trailing window, rank by `kappa_hat`, and
   ask whether the lab's existing reversal-family ICs are concentrated in the fast-reverting half.
   Note what this is testing: not "does reversion predict returns", but "is the lab's measured
   reversal effect attributable to the subset where the reversion assumption is estimable at all".
   A null there is informative — it says the effect is not the mechanism the family is named for.
2. **A fit-quality gate.** The lab has, as far as this folder records, **no** operator that
   refuses to act on a signal because the estimate behind it is poorly determined; every score is
   used at face value once computed. An `R^2` (or standard-error) gate is a new operator class,
   and it is free to evaluate on train.

**Pitfalls, and the first is serious.** (i) `kappa_hat` is biased and the bias grows as the
window shortens; selecting the *largest* estimated `kappa` therefore selects partly on estimation
error, which is precisely the post-selection problem this folder already documents — see
`notes/2026-09-15-inference-on-winners-post-selection-estimation.md` and
`notes/2026-09-15-tweedies-formula-empirical-bayes-selection-bias.md`. Time-averaging `kappa_hat`
over a training window (the paper's `QS`) mitigates but does not remove it. (ii) On this universe
the `1/sigma_i` eigen-portfolio rescaling is not cosmetic: the volatility level here is a measured
survivorship artifact, so factors built without the rescaling will be dominated by it. (iii) The
AR(1) fit needs enough observations per name per date; the paper's own floor is that ~5 days is
useless and 30–120 is the workable range, which sets a minimum data cost for any version of this.

## Related

- `notes/2026-08-30-pca-residual-statistical-arbitrage-long-only.md` — Avellaneda–Lee, whose
  residual construction, `s`-score and thresholds this paper reproduces exactly and whose
  factor-count finding it independently re-encounters as a noise ceiling.
- `notes/2026-09-25-deep-learning-statistical-arbitrage-residual-construction.md` — the Tier-1
  paper that treats this construction as a benchmark, and whose argument is that the
  two-number OU summary throws away most of the residual path.
- `notes/2026-09-15-inference-on-winners-post-selection-estimation.md` — why selecting on the
  maximum of a noisy estimate needs a correction.
- `notes/2026-09-25-short-term-residual-reversal.md` — the other route to a membership rule from
  a residual, at a horizon this repo's costs can actually afford.
