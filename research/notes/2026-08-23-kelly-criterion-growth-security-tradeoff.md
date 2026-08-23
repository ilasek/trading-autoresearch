---
title: "Good and Bad Properties of the Kelly Criterion / Long-Term Capital Growth: The Good and Bad Properties of the Kelly and Fractional Kelly Capital Growth Criteria"
authors: MacLean, Thorp, Ziemba
year: 2010, 2011
venue: Quantitative Finance 10(7), 681–687 — venue tier 2 (peer-reviewed field journal); the same material as a chapter in *The Kelly Capital Growth Investment Criterion: Theory and Practice*, World Scientific Handbook in Financial Economics Vol. 3 (2011) — venue tier 3 (edited handbook)
url: https://doi.org/10.1080/14697688.2010.506108
citations: 84 (Semantic Scholar, checked 2026-08-23); 69 (Crossref is-referenced-by-count, checked 2026-08-23)
sample_period: none for the propositions (all are theorems or parametric illustrations); the secondary results it tabulates draw on simulation studies rather than a historical sample
markets: none — the analysis is over an arbitrary favourable i.i.d. investment process; illustrations use coin-tossing, blackjack and a geometric Wiener process
tier: B+ (the individual propositions are theorems from tier-1 sources — Breiman, Algoet–Cover, Bell–Cover, Hakansson–Miller — and cannot decay; the survey itself is a field-journal/handbook summary rather than a primary result, and the two figures it leans on hardest are drawn second-hand from other papers)
validation_overlap: false
published_post_2018: false
full_text: read in full from the authors' dated draft "Good and bad properties of the Kelly criterion" (1 January 2010), the text of the World Scientific chapter, hosted on a UC Berkeley course page. Two sources it tabulates were NOT read and are recorded here as second-hand and flagged in-text — MacLean, Ziemba & Blazenko 1992 (Management Science 38(11), 1562–1585, doi:10.1287/mnsc.38.11.1562, 188 citations on Semantic Scholar, checked 2026-08-23, oa_status closed) and Chopra & Ziemba 1993 (Journal of Portfolio Management 19(2), 6–11, doi:10.3905/jpm.1993.409440, 1311 citations on Semantic Scholar, checked 2026-08-23, oa_status closed; its central table is reproduced verbatim in the text read).
---

## Mechanism

The companion note (`2026-08-23-geometric-mean-maximization-fallacy.md`) records the case against
maximising `E[log W]`. This is the same object seen from the other side, by three of the criterion's
principal proponents, and it is more useful to this lab than the attack is — because it supplies the
**explicit map** between a growth objective and a risk-scored one, and because its list of "bad
properties" is a list of exactly the failure modes a Sharpe-scored, cost-paying, leverage-capped
book would suffer.

The Kelly criterion maximises `E[log(wealth)]` period by period. Its central claim, and the one
nobody disputes, is asymptotic: it maximises the limiting exponential growth rate of wealth
(Breiman 1961; Algoet–Cover 1988). The authors' own summary of the trade is blunt: *"The main
disadvantage of the Kelly criterion is that its suggested wagers may be very large. Hence, the Kelly
criterion can be very risky in the short term."*

**The exact bridge from growth to Sharpe, and it is one line.** In continuous time
`g_p = E_p − ½V_p`. Under a CAPM-style single risky asset with `E_p = r_0 + (E_M − r_0)X`,
`V_p = σ²_M X²`, setting `dg_p/dX = 0` gives the Kelly weight and growth rate

```
X* = (E_M − r_0)/σ²_M            g* = r_0 + ½·[(E_M − r_0)/σ_M]²  =  r_0 + ½·SR²
```

(the proof in their appendix is due to Markowitz.) So at the growth-optimal point, and *only*
there, growth rate and Sharpe ratio are monotone transforms of one another: the Kelly book's excess
growth is **half the squared Sharpe ratio**. This is the crossing session 9's open question (b) was
looking for — and reading it carefully shows why it does not deliver what the folder hoped. The
identity holds *at the optimum of a leverage choice*. It says: choose leverage `X*`, and then the
growth you get is a function of the Sharpe of the underlying asset. It does **not** say that growth
rate ranks two *unlevered* books the way Sharpe does. Substituting a fixed `X` (as a
leverage-capped book must) leaves `g_p = r_0 + (E_M − r_0)X − ½σ²_M X²`, in which the ordering by
`g` and the ordering by `(E_M − r_0)/σ_M` come apart as soon as the two candidates differ in
volatility.

**The 2× Kelly theorem, the sharpest single result here.** Substituting `Y = 2X*` into the same
expression yields `g − r_0 = 2(E_M − r_0)²/σ²_M − 2(E_M − r_0)²/σ²_M = 0`. **Betting exactly twice
the Kelly fraction gives a growth rate equal to the risk-free rate**, with all the added variance
and none of the added growth. Beyond that, growth falls and eventually becomes negative. Hence
their rule: *it never pays to bet more than Kelly* — beyond that point risk rises and growth falls,
so Kelly dominates every more-aggressive strategy in geometric risk-return space. The growth
function is a concave parabola in exposure with roots at 0 and 2× Kelly, so **the penalty for
overbetting is quadratic while the penalty for underbetting is only linear near the optimum.**

**Fractional Kelly is the interpolation, and its algebra is the map to a risk-averse scorer.** For
negative power utility `δw^δ` with `δ < 0` (converging to log as `δ → 0`), and a stationary
lognormal process, the optimal portfolio is obtained by putting `α = 1/(1 − δ)` in the Kelly
portfolio and `1 − α` in cash. Half Kelly is `δ = −1`, quarter Kelly is `δ = −3`. The authors state
the boundary explicitly: this is exact for lognormal investments, approximately correct for other
distributions, and **does not apply generally** — their coin-tossing counterexample gives
`f*_δ = (p^α − q^α)/(p^α + q^α)`, which is not `α·f*`.

**The growth-security trade-off, tabulated.** Their reproduction of MacLean–Ziemba's blackjack
illustration (2% advantage) maps Kelly fraction to `P[doubling before halving]` and relative growth
rate: 0.5× Kelly gives 0.89 and 0.75; 0.7× gives 0.78 and 0.91; **full Kelly gives 0.67 and 1.00**;
1.5× gives 0.56 and 0.75; 2.0× gives 0.50 and 0.00. Two things to read off. Full Kelly accepts a
**one-in-three chance of halving before doubling** to buy the last of the growth. And the growth
curve is nearly flat approaching the optimum from below — 0.8× Kelly retains 96% of the growth —
while security improves fast, which is the whole practitioner argument for fractional Kelly.

**The estimation-error result, and it is the hinge of this note.** They report, from Chopra–Ziemba
(1993) following Kallberg–Ziemba, the ratio of certainty-equivalent loss for errors in the three
input classes, and — the part the folder does not already have — its **dependence on risk
aversion**:

| Risk tolerance | means vs covariances | means vs variances | variances vs covariances |
|---|---|---|---|
| 25 | 5.38 | 3.22 | 1.67 |
| 50 | 22.50 | 10.98 | 2.05 |
| 75 | 56.84 | 21.42 | 2.68 |

with the headline summary `20 : 2 : 1` for means : variances : covariances. Risk tolerance here is
`RT(w) = 100 / (½ R_A(w))` with `R_A = −u''/u'`. The direction is unambiguous: **the lower the risk
aversion, the more damaging errors in estimated means become.** And log utility has `R_A(w) = 1/w`,
which for any non-trivial wealth is close to zero — the *least* risk-averse point on the scale.
The authors draw the conclusion themselves: *"Given the extreme sensitivity of E log calculations
to errors in mean estimates, these estimates must be accurate and to be on the safe side, the size
of the wagers should be reduced."* So the growth-optimal criterion is not merely one objective
among many — **it is the objective most exposed to estimation error in exactly the input this repo
estimates worst.** (Chopra 1993 separately reports turnover is also most sensitive to errors in
means, though by a much smaller margin than performance is.)

**Time to dominance, and this is the result with the most bearing on the repo's evaluation
problem.** Kelly's advantage is asymptotic, and the authors give the timescales explicitly. In
continuous time with a geometric Wiener process, `μ_α = 20%` vs `μ_β = 10%` with
`σ_α = σ_β = 10%`: A is ahead of B with 95% confidence after **five years**. Keep the same means
but set `σ_α = 20%`, `σ_β = 10%`: it takes **157 years**. In coin-tossing, an edge of 1.0% versus
1.1% takes **two million trials** for an 84% chance that the better game dominates. Doubling the
volatility of the better strategy multiplied the required sample by ~30. This is a statement about
how long a sample must be to distinguish two strategies whose edges differ modestly — the same
statement the companion Sharpe-ratio note makes with a standard-error formula, arriving from a
completely different direction.

## Construction recipe

There is no strategy here to build under this repo's constraints (see below), but there are four
propositions usable as screens, all free.

1. **Exposure ladder.** Growth as a function of exposure is a concave parabola with roots at zero
   and 2× the growth-optimal exposure. Underbetting costs growth roughly linearly near the optimum
   and buys security fast; overbetting costs growth *and* security together. Any proposal that
   increases a book's effective risk exposure should be argued as a move *up* that parabola, with a
   claim about which side of the vertex the book sits on.
2. **Fractional-Kelly mapping.** `α = 1/(1 − δ)` converts a risk-aversion parameter into a blend
   weight between the growth-optimal book and cash — exact under lognormality only. Its useful
   direction here is diagnostic: a book that is "growth-optimal" is by construction the choice of an
   investor with risk aversion near zero.
3. **Estimation-fragility ordering.** Errors in means cost roughly ten times what errors in
   variances cost and twenty times what errors in covariances cost, and the multiple *rises* as risk
   aversion falls.
4. **Sample-size sanity check.** Two strategies with similar edges require enormous samples to be
   distinguished, and the requirement scales sharply with the volatility of the better one.

## Robustness evidence (qualitative only)

The individual propositions are theorems and carry tier-1 provenance: asymptotic growth optimality
(Breiman 1961; Algoet–Cover 1988), never risks ruin (Hakansson–Miller 1975, Management Science),
myopia (Hakansson 1971; Mossin 1968), competitive optimality `E(X/X*) ≤ 1` (Bell–Cover 1980, 1988),
median-maximisation (Ethier). None of these can decay. The 2×-Kelly zero-growth result is
independently attributed to three authors (Thorp 1997; Stutzer 1998; Janacek 1998).

The survey itself is a summary, and two of the numbers this note leans on hardest — the
certainty-equivalent-loss table and the growth-security table — are **reproduced from papers not
read here** (Chopra–Ziemba 1993; MacLean–Ziemba 1999 via MacLean–Ziemba–Blazenko 1992), both
closed-access with no repository copy found. Recorded as second-hand rather than upgraded. The
Chopra–Ziemba original carries 1311 citations, so the result is not obscure, but the exact table
entries have not been verified against their source here.

The honest boundary on the whole literature is the one the authors state in their own "bad
properties" and "observations" list, and it is the same boundary Samuelson established:
- *"Fallacy: If maximizing `E log X_N` almost certainly leads to a better outcome then the expected
  utility of its outcome exceeds that of any other rule provided N is sufficiently large.
  Counterexample: ... See Samuelson (1971) and Thorp (1971, 2006)."* The two literatures agree on
  the mathematics.
- *"The Kelly portfolio does not necessarily lie on the efficient frontier in a mean-variance
  model (Thorp, 1971)."* Stated flatly, by the growth school, in its own summary.
- Despite superior long-run growth, Kelly like any strategy can have a poor outcome, and half Kelly
  "does not help much" in the worst cases while giving up most of the upside frequency.
- The unweighted average rate of return converges to half the arithmetic rate, so "you may
  regularly win less than you expect."
- For any fixed-fraction strategy in coin-tossing, `n` wins and `n` losses leaves you at
  `W_0(1 − f²)^n < W_0`.
- The authors note that real-world overbetting has produced blow-ups, and that practitioners who
  prioritise capital preservation sharply reduce risk as drawdown increases — an observation, not a
  derived policy.

## Implementability here

**The strategy is not implementable and should not be attempted**, for the same structural reason
that closed families 2 and 3: the mechanism is a *leverage rule*, and gross leverage ≤ 1.0 removes
the half of it that does anything.

The Kelly prescription is "hold `X* = (E_M − r_0)/σ²_M` of the risky asset." For a book whose
Sharpe is around 1 and volatility around 20%, `X*` is far above 1, so the constraint binds at
`min(X*, 1)` essentially always and the rule degenerates into "be fully invested" — which the
champion already is. This is the third independent appearance of the pattern the folder now has a
name for: *the mechanism scales exposure up when conditions are good, and a leverage cap keeps only
the de-risking half.* Here it is even starker, because the Kelly rule has no de-risking half at all
on a book this attractive. Recorded as an anti-candidate.

**What is worth carrying is the diagnostic reading, and it is uncomfortable.**

(a) **The champion sits on the aggressive side of this literature's own risk dial, and its
promotion history has been walking further up it.** `learnings.md` records a concentration ladder —
equal weight → rank weight → magnitude weight → buffer deletion — in which each step raised
validation Sharpe while widening drawdown, collapsing risk breadth (7.8 → 6.0 effective risk bets),
and raising the weighted average variance of what is held. In this literature's vocabulary that is
movement toward the vertex of the growth parabola and past the point where a risk-averse investor
would stop. The growth-security table is the general form of that trade-off: security falls fast in
the last stretch before the growth optimum, and the growth gain over that stretch is small.

(b) **The estimation-fragility ordering sharpens `SUMMARY.md` screen #1 rather than repeating it.**
The folder's screen counts noisily-estimated parameters. This source weights them: means cost ~10×
what variances cost and ~20× what covariances cost. Two consequences. First, the folder's blanket
"covariance-based objectives are the expensive class" is *directionally right but understates the
real ordering* — a scheme that estimates expected returns is far worse than one that estimates a
covariance. The champion estimates neither (its score is an observed cross-sectional statistic,
not a forecast of a mean), which is a stronger endorsement than the parameter count alone gave it.
Second, the multiplier **rises as risk aversion falls**, so the more concentrated and aggressive
the book, the more a given estimation error costs it — which is a second, independent reason to
read the concentration ladder as raising fragility rather than merely raising drawdown.

(c) **The time-to-dominance numbers land directly on the ⚠ standing protocol concern.** The
validation split is six years. This source's own illustration says two strategies differing by
10pp of annual mean, at 10% volatility, need five years to separate at 95% confidence — and that
doubling the better one's volatility pushes the requirement to 157 years. The champion's book runs
at roughly 23% annualised volatility, and the promotion ladder's steps are worth a few hundredths
of a Sharpe each. The literature's answer to "can a six-year window discriminate between these
candidates?" is *no, not remotely*, and it gives that answer without any reference to this repo's
data. That is the same conclusion the companion note reaches from the standard error of the Sharpe
ratio itself, and the two should be quoted together.

(d) **One thing this does *not* license.** "Kelly says be aggressive" is not an argument for the
concentration ladder, and "Kelly says the book is overbet" is not an argument against it. Neither
claim can be made without estimating `E_M` and `σ_M` for the book — a mean estimate, the most
error-prone input on the list, on the shortest sample. The usable content is the *shape* of the
trade-off (concave, asymmetric, security falling fast near the optimum), not a located optimum.

## Related

- `notes/2026-08-23-geometric-mean-maximization-fallacy.md` — the case against the objective this
  source advocates; the two agree on all mathematics and differ on emphasis.
- `notes/2026-08-23-statistics-of-sharpe-ratios.md` — the same sample-size conclusion via the
  standard error of the gate's own statistic.
- `notes/2026-08-22-excess-growth-and-return-decomposition.md` — the growth-rate identity whose
  status as a *scoring axis* both of this session's first two notes reject.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — screen #1, which this source re-weights:
  means ≫ variances ≫ covariances, with the ratio rising as risk aversion falls.
- `notes/2026-08-17-volatility-timing-managed-portfolios.md`,
  `notes/2026-08-18-risk-parity-equal-risk-contribution.md`,
  `notes/2026-08-18-low-risk-investing-industry-neutral.md` — the three prior cases of a mechanism
  that needs leverage this repo does not have.
