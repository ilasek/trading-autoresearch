---
title: "Pseudo-Mathematics and Financial Charlatanism: the expected maximum Sharpe ratio and Minimum Backtest Length"
authors: Bailey, Borwein, López de Prado, Zhu
year: 2014
venue: Notices of the American Mathematical Society 61(5), 458–471 — a peer-edited mathematics-society publication rather than a finance journal. Not on this folder's venue ladder as written; graded tier 2 because the two results carried here are propositions with appendix proofs (and both were reproduced numerically here), not empirical claims.
url: https://doi.org/10.1090/noti1105 (full text read from the first author's own page, https://www.davidhbailey.com/dhbpapers/backtest-pseudo.pdf; the publisher's own ams.org PDF endpoint returns HTTP 403 to an automated client)
citations: 178 (Crossref, checked 2026-11-05); 166 (Semantic Scholar, checked 2026-11-05)
sample_period: none — methodological. Evidence is closed-form propositions plus Monte-Carlo on synthetic Gaussian random walks (N = 1,000 paths, T = 1,000 steps); no market data anywhere in the paper
markets: none
tier: B+
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the `N > 1` complement to the same authors' MinTRL: not "how long a record do I need to
believe one Sharpe ratio", but **"how long a sample do I need before the best of `N` searched
configurations stops being a coin-flip winner"**. The mechanism is pure extreme-value arithmetic
and has nothing to do with markets.

**Step 1 — the expected maximum of `N` null statistics.** Under `SR = 0` and one year of data,
the estimated annualized Sharpe is asymptotically standard Normal (Lo's variance at `SR = 0`
gives exactly 1, and — the detail that does the damage — *increasing the observation frequency
does not shrink it*, because at `SR = 0` the variance is `1/y` with `y` in years, free of the
per-year count `q`). So the best of `N` independently-searched zero-skill configurations has

```
E[max_N]  ≈  (1 − γ)·Z⁻¹(1 − 1/N)  +  γ·Z⁻¹(1 − 1/(N·e))        γ = 0.5772156649 (Euler–Mascheroni)
```

with upper bound `√(2·ln N)`. This is a **Gumbel** approximation to the maximum of `N` standard
Normals, written as a convex blend of two Normal quantiles.

| `N` independent trials | `E[max_N]` | `√(2 ln N)` bound |
|---|---|---|
| 10 | 1.57 | 2.15 |
| 20 | 1.90 | 2.45 |
| 50 | 2.28 | 2.80 |
| 100 | 2.53 | 3.03 |
| 200 | 2.77 | 3.26 |

**Step 2 — rescale by sample length.** With `y` years the standard deviation of the annualized
Sharpe at the null is `y^(−1/2)`, so the expected best-of-`N` in-sample Sharpe is
`y^(−1/2)·E[max_N]`. Solving for `y` gives **Minimum Backtest Length**:

```
MinBTL  ≈  ( E[max_N] / S_target )²   <   2·ln[N] / S_target²        [years]
```

read as: to keep the expected best-of-`N` spurious in-sample Sharpe at or below `S_target`, the
backtest must be at least this long. The authors' own calibration at `S_target = 1`: five years of
data supports at most ~45 independent configurations; two years supports about seven. Beyond that
you are "almost guaranteed" to manufacture an in-sample Sharpe of 1 with an expected
out-of-sample Sharpe of zero.

The authors are explicit that **MinBTL is necessary, not sufficient** — a sample longer than
MinBTL can still be overfit — and that `N` must be the number of **independent** configurations.
Their suggested fix for correlated trials (reduce the dimension by PCA to get an effective `N`) is
a sketch rather than a procedure.

**Step 3 — the result that is not about counting, and is the more interesting half here.**
Sections 5–6 ask what in-sample selection does to *out-of-sample* performance, and find that the
answer depends entirely on whether the two sub-samples share a conserved quantity.

- With **no constraint** (independent Gaussian increments, zero drift), the in-sample/out-of-sample
  Sharpe scatter is a circular cloud centred on the origin: selecting the best in-sample
  configuration lifts the in-sample Sharpe to around 1.7 and leaves the expected out-of-sample
  Sharpe at zero. Overfitting buys nothing and costs nothing.
- Impose **one global constraint** — re-centre every path so its full-sample mean equals a fixed
  `µ`, removing one degree of freedom — and the scatter acquires a **significantly negative
  slope**: the harder you optimize in sample, the worse the out-of-sample result, and the expected
  out-of-sample Sharpe goes negative on a process that had no trend to begin with.

Their Proposition 6.1 is the exact statement: for two configurations `A`, `B` of one model with
equal in-sample and out-of-sample volatilities, imposing `µ_A = µ_B` on the full sample implies

```
SR_IS(A) > SR_IS(B)   ⟺   SR_OOS(A) < SR_OOS(B)
```

— **in-sample ranking inverts out of sample, exactly and by construction.** Re-centring is just
the cheapest way to introduce "memory": any mechanism that pins a sample aggregate (a conserved
mean, a fixed total, a reversal) produces a compensation effect, and under compensation the
selection step is actively harmful rather than merely uninformative. This is the precise condition
separating "selection is noise" from "selection is poison", and it is testable.

## Construction recipe

Nothing to trade; three things to compute.

1. **`E[max_N]` for your search.** The formula above, with `N` the count of *independent* trials.
   Multiply by the standard error of whatever statistic is being maximised to get the expected
   best-of-search value under the null.
2. **MinBTL** by inverting it against a tolerance `S_target` you are willing to see a null
   strategy reach.
3. **The compensation diagnostic.** Across a set of already-recorded trials, regress the
   out-of-sample statistic on the in-sample one. Slope ≈ 0 means the unconstrained case (selection
   is pure noise, and the haircut literature's corrections are the right tool). Slope significantly
   **negative** means a conserved quantity is binding and the in-sample ranking is anti-informative
   — in which case selecting the in-sample best is worse than selecting at random, and no
   multiple-testing correction repairs it, because the problem is the sign of the signal rather
   than its size.

## Robustness evidence (qualitative only)

- **Reproduced here.** `E[max_10] = 1.575` against the paper's 1.57; MinBTL at `S_target = 1` gives
  5.00 years for `N = 45` and 1.92 for `N = 7`, against the paper's "5 years / no more than 45" and
  "7 configurations / 2-year backtest". The Gumbel blend and the `√(2 ln N)` bound both check out.
- **The extreme-value result is standard mathematics**, not a finance finding: the authors cite
  Embrechts et al. for the bound, and the propositions are proved in their own appendix. It is not
  the kind of claim Hou–Xue–Zhang or Jensen–Kelly–Pedersen replication studies address, and no
  decay question applies.
- **Two assumptions carry all the weight, and both cut toward over-statement.** (i) *Independence*
  of the `N` trials — the paper calls this "quite conservative" and it is: correlated trials have a
  smaller effective `N` and therefore a smaller `E[max]`. (ii) *Asymptotic Normality of the Sharpe
  estimator at the null* — fine for the mean of many observations, weaker for a short record or a
  heavy-tailed one, and the companion MinTRL paper is where the non-Normality adjustment lives.
- **Honesty, with one caveat about venue.** Costs are not modelled; multiple testing is the paper's
  entire subject; the propositions are proved. But the article is partly a polemic — its title and
  Section 7 ("Is backtest overfitting a fraud?") argue a professional-ethics case — and the
  rhetorical register is not evidence. Only the two propositions and the simulation design are
  recorded here.
- **Anti-lookahead note.** The paper contains no market data, no dated performance and no event
  narrative, so there is nothing of that kind to withhold.

## Implementability here

**Status against the acceptance criterion** (a computable minimum detectable effect as a function
of something the lab controls): **it reaches, and the controlled input is the trial count.** It is
also the half of the bracket the [2026-11-04] open-questions entry was missing — MinTRL bounds the
design from the effect side, MinBTL from the search side.

**1. Translating it into v3's statistic.** The paper's `y^(−1/2)` is the standard error of an
annualized Sharpe at the null. v3 does not score a Sharpe; it scores **skill** = candidate Sharpe
− equal-weight pool Sharpe on the same days, whose standard error is the paired one
`SE(skill) ≈ √(2(1−ρ)/T)` (`notes/2026-08-24-testing-differences-of-sharpe-ratios.md`). Step 1
transfers unchanged with that substitution, giving the **expected maximum spurious skill of a
search**:

```
E[max spurious skill]  ≈  SE(skill) · E[max_N]
```

At `T = 1562` daily validation observations:

| `ρ` | `SE(skill)` | `N = 10` | `N = 50` | `N = 100` | `N = 200` |
|---|---|---|---|---|---|
| 0.99 | 0.057 | 0.09 | 0.13 | 0.14 | 0.16 |
| 0.95 | 0.127 | 0.20 | 0.29 | 0.32 | 0.35 |
| 0.90 | 0.180 | 0.28 | 0.41 | 0.45 | 0.50 |
| 0.80 | 0.254 | 0.40 | 0.58 | 0.64 | 0.70 |

and the **search-adjusted minimum detectable skill** at 80% power, `SE·(E[max_N] + 0.842)`:

| `ρ` | `N = 10` | `N = 50` | `N = 100` | `N = 200` |
|---|---|---|---|---|
| 0.99 | 0.14 | 0.18 | 0.19 | 0.20 |
| 0.95 | 0.31 | 0.40 | 0.43 | 0.46 |
| 0.90 | 0.43 | 0.56 | 0.61 | 0.65 |
| 0.80 | 0.61 | 0.79 | 0.86 | 0.92 |

(My arithmetic, from the formula above plus the paired SE.) Three readings:

- **The trial count is the mild axis; the benchmark correlation is the brutal one.** Going from 10
  to 200 independent trials raises the required skill by ~1.2×; going from `ρ = 0.99` to `ρ = 0.80`
  raises it by ~4.5×. This is the same ordering `#323` found on the separation axis (log in the
  candidate count) arriving from a completely different derivation, and it says the deflated bar's
  per-trial cost is real but second-order next to the choice of how far from the pool to build.
- **A structurally different candidate on this window needs skill of roughly 0.4–0.9 to be
  detectable after the search is accounted for.** Whether any mechanism in this literature plausibly
  delivers that is a separate question, but the number is now on the table rather than implicit,
  and it is the honest reading of a long run of near-zero skill readings: **those readings are
  consistent both with absent effects and with a design whose floor sits well above the effect
  sizes the sources describe.** This is the direct answer `#357`/`#358` needed and it answers in the
  second direction, not the first.
- **The usable lever is `ρ`, and it is a construction choice, not a statistic.** Building a small,
  deliberate tilt on the pool rather than a distinct book cuts the MDE by a factor of 3–4. The
  catch, stated in the MinTRL note, is that it cuts attainable skill too; the design question is
  whether attainable skill falls slower than `√(1−ρ)`.

**2. MinBTL read against this lab's fixed window.** The validation window is fixed at 2018–2023
(~6.2 years) and cannot be lengthened, so MinBTL has to be read backwards as a **trial budget**:
at `S_target = 1` in raw-Sharpe units, 6.2 years supports about **89 independent** configurations.
Two reasons that number is not a verdict on the lab's recorded trial count. It is for a *raw*
Sharpe, not for the paired skill statistic the gate actually adjudicates; and it requires
*independent* trials, where this lab's are heavily overlapping — `program.md`'s own
`distinct_mechanisms` field is a crude effective-`N`, and the leaderboard's family structure means
the effective count is far below the recorded count. The right use is as a **pressure gauge on
`N_eff`**: if the effective number of independent mechanisms ever approached ~90, the window alone
would guarantee a spurious in-sample Sharpe of 1.

**3. The compensation diagnostic is the free item, and it is the one worth running first.**
Proposition 6.1 says a conserved sample aggregate makes in-sample ranking *anti*-informative. The
lab's splits are consecutive slices of a single realised path on a single panel, every candidate is
graded against the same fully-invested pool, and a long-only book's weights sum to a constant —
three candidate conserved quantities. Which case the lab is in is **directly measurable from data
it already stores**: regress validation skill on train skill across recorded trials. A slope near
zero means the haircut machinery is the right tool. A **negative** slope would mean train skill is
a contrarian indicator for validation skill, which would invalidate the whole "clear the train gate
then test on validation" ordering and would be an engine-level finding rather than a strategy one.
**The lab has already produced the number, and it reads benign — weakly.** The 2026-11-04/05
nightly reports `corr(train statistic, validation skill) = −0.074` over fifteen trials, and
explains it by regime mix: the benchmark pool's own Sharpe swings so much between sub-windows that
"there is no stable quantity to predict". Proposition 6.1 is a **second, structurally different
explanation of the same observation**, and the two are distinguishable by sign — regime mix
predicts a correlation of zero, a conserved sample aggregate predicts a **negative** one. At
`n = 15` the estimate separates neither, which is this note's own argument applied to this note's
own diagnostic. So the instruction for the lab is not "run it" but **"re-read its sign as trials
accumulate, and interpret a persistently negative slope against Proposition 6.1 rather than only
against regime mix"** — because only one of the two explanations makes in-sample selection
*actively harmful* rather than merely uninformative, and the remedies differ completely.

**4. Pitfall.** The `y^(−1/2)` scaling means **doubling the observation frequency does not help** —
at the null the variance is set by calendar time, not by the number of bars. Nothing is gained by
measuring the same six years more finely, which is worth stating because the MinTRL note's
frequency result points the other way and the two are easy to confuse: frequency buys resolution
when there is a real effect to resolve (`ŜR² ≠ 0`), and buys nothing at all against a search
through nulls.

## Related

- `notes/2026-11-05-minimum-track-record-length-and-the-probabilistic-sharpe-ratio.md` — the `N = 1`
  companion by the same authors; this paper names it and states exactly why it does not suffice.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — the same `E[max_N]` expression used *post hoc*, to
  deflate a reported Sharpe, rather than *ex ante*, to size a sample. Identical mathematics,
  opposite direction; the folder had the first and not the second.
- `notes/2026-08-24-multiple-testing-haircut.md` and
  `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — the correction-after-the-fact vein,
  40 notes deep, that this note is the design-side complement to.
- `notes/2026-09-15-reality-check-max-statistic-under-dependence.md` — what happens to the maximum
  statistic when the trials are *not* independent, i.e. the assumption this paper admits is
  conservative.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — `#323`, which reaches the same
  "candidate count is a log axis, window length is the binding one" conclusion from minimax theory.
- `notes/2026-11-04-out-of-sample-prediction-failure-and-the-cumulative-sse-diagnostic.md` —
  `#390`'s failure taxonomy (low power looks poor early and improves; mis-specification deteriorates
  late) is the time-path version of the two regimes Proposition 6.1 separates.
