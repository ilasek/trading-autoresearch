---
title: "Bagging Predictors" + "Observations on Bagging"
authors: Breiman (1996); Buja, Stuetzle (2006)
year: 1996, 2006
venue: Machine Learning 24(2), 123–140 (venue tier 1 for the field); Statistica Sinica 16 (venue tier 1 statistics; exact pages not verified)
url: https://doi.org/10.1007/BF00058655 ; http://stat.wharton.upenn.edu/~buja/PAPERS/sinica-bagging-buja-stuetzle.pdf
citations: Breiman 26,356 (Semantic Scholar by DOI, checked 2026-08-19); Buja–Stuetzle 106 (Semantic Scholar title search, checked 2026-08-19 — no DOI registered, absent from Crossref)
sample_period: n/a — simulation studies and standard benchmark datasets; no market data in either paper
markets: none (statistics / machine-learning methodology)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the literature `SUMMARY.md` named as the one unexploited seam: **why averaging an
unstable procedure improves it, and whether the improvement is a claim about the centre of
the distribution or only about its spread.** The answer is that Breiman's core result is an
accuracy claim about the centre, and it is one line of algebra.

Let `φ(x, L)` be a predictor built by running a fixed procedure on a training set `L` drawn
from distribution `P`. Define the **aggregated** predictor as the expectation over training
sets, `φ_A(x) = E_L φ(x, L)`. Then, with `Y, X` drawn from `P` independently of `L`, the
average prediction error `e = E_L E_{Y,X}(Y − φ(X, L))²` and the aggregate's error
`e_A = E_{Y,X}(Y − φ_A(X))²` satisfy

```
e_A ≤ e,      with the gap governed by   [E_L φ(x, L)]² ≤ E_L φ²(x, L)
```

i.e. the gap is exactly the **variance of the predictor across training sets**. Two
consequences Breiman draws immediately:

1. **`φ_A` always improves on `φ`.** This is not a statement about the dispersion of
   outcomes around an unchanged mean; it is a statement that expected squared prediction
   error falls.
2. **How much it improves is precisely the procedure's instability.** If perturbing `L`
   barely changes `φ`, the two sides of the inequality are nearly equal and aggregation buys
   nothing. "The more highly variable the `φ(x, L)` are, the more improvement aggregation may
   produce."

The feasible version — bagging — replaces `P` with the empirical distribution `P_L`, i.e.
averages over bootstrap resamples rather than over independent training sets. Breiman is
explicit that this version is "caught in two currents": instability gives improvement
through aggregation, but if the procedure is *stable*, `φ_B = φ_A(x, P_L)` is a worse
estimate of `φ_A(x, P)` than the original `φ(x, L)` was. **There is a crossover point at
which bagging stops improving a procedure and starts damaging it.** For classification the
asymmetry is sharper still: aggregation "can transform good predictors into nearly optimal
ones", but poor predictors into worse ones.

Breiman's named canonical example of an unstable procedure is **subset selection in linear
regression**: "the variables are competing for inclusion … and small changes in the data can
cause large changes" in which are selected. That is structurally the same object as a
top-N / buffered basket-membership rule, where instruments compete for slots.

Buja–Stuetzle attack the same question with a rigorous asymptotic analysis, replacing the
learning algorithm with a real-valued U-statistic of i.i.d. data (U-statistics of high order
can encode complex interactions while remaining analysable). Their findings, all to second
order and of size `O(N⁻²)`:

- Squared **plug-in bias always increases** with bagging; **variance often but not always
  decreases**. In their framework "the only possible beneficial effect of bagging stems from
  variance reduction", and MSE improves only when the resample is sufficiently large.
- **Bagging leaves additive statistics unchanged.** In their decomposition the first-order
  (additive) term contributes exactly zero to the bagged-minus-unbagged variance difference;
  the whole effect lives in the second- and higher-order interaction terms. *A procedure that
  is linear in the data cannot be improved or harmed by bagging at all.*
- Bagging with replacement at resample size `M_with` and without replacement at `M_w/o` are
  equivalent when `N/M_with = N/M_w/o − 1`; the equivalence held with "surprising accuracy"
  in their tree simulations, suggesting wider validity than the proof covers.
- They flag a definitional caveat that matters for reading the whole literature: their bias
  result concerns **plug-in** bias (relative to the population functional), not **estimation**
  bias (relative to the true underlying function). They observe in simulation that for a
  smooth underlying function bagging can reduce *estimation* bias too, consistent with
  Bühlmann–Yu's account in which bagging a hard threshold rule is equivalent to fitting that
  rule convolved with a narrow kernel — i.e. bagging **smooths hard decisions**.
  (Bühlmann–Yu itself was not readable this session — Project Euclid serves a bot challenge —
  so that mechanism is recorded second-hand from Buja–Stuetzle's description of it, not from
  the source.)

The two papers do not contradict each other so much as answer different questions: Breiman's
inequality is about the *idealised* aggregate `φ_A` versus the base predictor, and it is
unconditional; Buja–Stuetzle's is about the *feasible* bagged statistic at finite resample
size, where the bootstrap approximation costs bias. Both agree that the size of any effect is
set by how nonlinear/unstable the base procedure is, and that a stable or additive procedure
gains nothing.

## Construction recipe

1. Fix the base procedure. Do not change it — bagging is a wrapper, not a redesign
   ("all that needs adding is a loop in front that selects the sample and a back end that
   does the aggregation").
2. Generate `B` perturbed views of the training data. Two equivalent knobs: bootstrap
   resampling with replacement, or subsampling without replacement at fraction `α`; the
   equivalence `N/M_with = N/M_w/o − 1` maps one onto the other.
3. Run the identical procedure on each perturbed view.
4. **Average the outputs** (numerical target) or take a plurality vote (class target). For
   probability-style outputs Breiman found averaging and voting gave virtually identical
   error rates.

Parameters, and how the sources say to set them:

- **Number of replicates `B`.** Strong diminishing returns. In Breiman's classification
  experiment, going 10 → 25 → 50 → 100 replicates moved the error rate 21.8 → 19.5 → 19.4 →
  19.4 against an unbagged 29.0: "most of the improvement using only 10", and beyond 25
  "love's labour lost". The curve is concave and saturates early.
- **Resample size / perturbation strength.** Buja–Stuetzle: MSE improves only for
  sufficiently *large* resample sizes (small `g`); push the perturbation too far and the bias
  term, which grows quadratically in `g`, dominates. There is an interior optimum, not a
  monotone "more perturbation is better".
- **Whether to bag at all.** Check instability first. Breiman's own control is nearest-
  neighbour classification, which is stable with respect to data perturbation; bagging it
  produced **identical** misclassification rates on all six datasets tried — a literal no-op,
  and he explains why with a Poisson argument (a case's nearest neighbour is absent from a
  bootstrap sample only ~37% of the time, so a majority of replicates almost never flips).

## Robustness evidence (qualitative only)

- Breiman reports gains across simulated data and several standard benchmark datasets, in
  both regression and classification, for two different unstable base procedures (trees and
  forward variable selection). The pattern that instability predicts the gain, and stability
  predicts a no-op, is consistent across all of them.
- The result has been reworked independently at least three times with different formalisms
  (Buja–Stuetzle's U-statistics; Chen–Hall on estimating equations; Knight–Bassett on
  quantiles, both cited by Buja–Stuetzle) with agreeing qualitative conclusions — bias up,
  variance usually down, effect size governed by nonlinearity.
- Bagging is now standard infrastructure rather than a contested finding, and the base result
  is algebra rather than an empirical regularity, so **it cannot decay and carries no
  publication-decay discount**. The corresponding weakness is that none of this evidence is
  financial: there is no cost model, no market, and no reason to assume the effect sizes
  transfer.
- Honest limit recorded rather than smoothed: Buja–Stuetzle's asymptotics put the effect at
  `O(N⁻²)`, which they concede "may not seem to explain the sometimes considerable
  improvements due to bagging seen in trees". Their reconciliation — that the effective `N`
  for a local tree estimate is the terminal-node size, which is small — is a plausibility
  argument, not a proof. So the *size* of the bagging effect is less well understood than its
  *sign* and its *precondition*.

## Implementability here

Nothing here needs new data; the value is interpretive and diagnostic.

**1. This is the missing mean-shifting argument, with one honest gap.** The folder's standing
open question was that the lab's overlapping-tranche result is a claim that the tranched book
*earns more*, while Jegadeesh–Titman framed overlapping portfolios as a statistical estimator
and Hoffstein et al. framed tranching as dispersion reduction around an unchanged mean.
Breiman's inequality is the claim that was missing: aggregating over perturbed fits lowers
expected squared prediction error, unconditionally, by an amount equal to the base
procedure's instability. The gap that remains, and it must not be glossed: this is an **MSE
claim about a predictor**, not a claim about portfolio return or Sharpe. The bridge from
"lower forecast error" to "higher realised return" is the lab's inference, not the source's,
and the same caveat already recorded for the estimation-window literature applies here.

**2. The instability precondition is met, and by Breiman's own example.** The champion's
construction is: score each instrument, apply a hysteresis membership band, keep the top set,
weight by score magnitude. Membership is *subset selection* — instruments compete for slots
and a small price change flips a name in or out — which is the exact procedure Breiman names
as unstable. So the lab's mechanism sits on the side of the crossover where the literature
predicts aggregation should help, and it sits there for a reason that can be stated rather
than measured.

**3. Free screen, no trial, and it sharpens a rule the lab discovered empirically.** *Bagging
leaves additive statistics unchanged.* Averaging over vintages can only move a construction to
the extent that construction is **nonlinear** in the data. This is the general form of the
lab's own #41/#42 finding — that collapsing two lookbacks into one score before selecting
"discards the fact that the two windows disagree about which names to hold". For a linear
map from score to weight, averaging the portfolios equals the portfolio of the averaged
score, and there is nothing to gain; it is the threshold (buffer, top-N, cap, trim) that
makes the two operations different objects. Practical rule for any future vintage-averaging
proposal, derivable on paper: **write down whether the per-vintage output is a nonlinear
function of the data. If it is linear, averaging vintages is algebraically identical to
averaging scores, and the idea is a no-op before it is a trial.**

**4. It predicts the shape of the `K` curve without licensing a sweep.** Breiman's replicate
count saturates early — most of the gain by ~10, nothing after ~25 — and Buja–Stuetzle put an
interior optimum on perturbation strength rather than a monotone gain. Both point the same
way for the standing "do not sweep K" rule: the expected gain from 6 → 12 tranches is small
and the curve is concave, so any future proposal to deepen the tranche stack should
pre-register a small effect size, as the lab's diagnostic-first habit requires. It also
supplies a second, independent reason for the upper bound the lab already derives from
post-formation reversal: past a point, more perturbation costs bias.

**5. Known pitfalls.** (a) The crossover is real — bagging a *stable* procedure is not
neutral but mildly harmful, so "average over more things" is not a free move to apply to
every component. (b) In classification, aggregation makes poor predictors worse; the
asymmetry is a caution against wrapping a weak signal in an ensemble and expecting the
wrapper to rescue it. (c) All effect sizes here are from non-financial data with no
transaction costs; only the sign and the precondition transfer.

## Related

- `notes/2026-08-17-averaging-over-estimation-windows.md` — the other accuracy-level account
  of the same lab mechanism, arriving from structural-break forecasting rather than from ML.
  The two are complementary: Pesaran–Timmermann explain why averaging over *estimation
  windows* lowers forecast error under an unknown break; Breiman explains why averaging over
  *perturbed fits* lowers it whenever the fitting procedure is unstable, with no break needed.
- `notes/2026-08-17-forecast-combination-why-averaging-beats-selecting.md` — the same law one
  level up, for forecasts of a single target.
- `notes/2026-08-17-jegadeesh-titman-overlapping-momentum.md`,
  `notes/2026-08-17-rebalance-timing-luck-tranching.md` — the estimator and dispersion
  framings this note completes.
- `notes/2026-08-19-model-averaging-mallows-weights.md` — when *estimated* averaging weights
  are provably justified, and why the lab's setting is not one of those cases.
- `notes/2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the same question answered
  in portfolio vocabulary rather than prediction-error vocabulary.
