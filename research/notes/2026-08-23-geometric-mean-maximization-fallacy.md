---
title: "The 'Fallacy' of Maximizing the Geometric Mean in Long Sequences of Investing or Gambling; Fallacy of the Log-Normal Approximation to Optimal Portfolio Decision-Making Over Many Periods"
authors: Samuelson (1971); Merton & Samuelson (1974)
year: 1971, 1974
venue: Proceedings of the National Academy of Sciences 68(10), 2493–2496 — venue tier 1 (top peer-reviewed general-science journal); Journal of Financial Economics 1(1), 67–94 — venue tier 1
url: https://doi.org/10.1073/pnas.68.10.2493 ; https://doi.org/10.1016/0304-405X(74)90009-9
citations: Samuelson 1971 — 211 (Semantic Scholar, checked 2026-08-23); Merton–Samuelson 1974 — 70 (Semantic Scholar, checked 2026-08-23)
sample_period: none — both papers are theorems and counterexamples, no empirical sample
markets: none (decision theory over an arbitrary i.i.d. return process)
tier: A
validation_overlap: false
published_post_2018: false
full_text: Samuelson read in full (EuropePMC copy of the PNAS article, PMC389451). Merton–Samuelson read in full from the MIT Sloan working-paper version 623-72 (Nov 1972), MIT DSpace hdl 1721.1/47987, which is the paper later published in JFE.
---

## Mechanism

This pair answers session 9's open question (b) — *when does maximising log growth diverge from
what a finite-horizon, risk-scored investor wants?* — with a harder answer than the question
anticipated: **always, and by an amount that grows with the horizon.**

The object under attack is the "maximum-geometric-mean" rule: at each period choose the portfolio
weights that maximise `E[log(1 + return)]`. Its appeal rests on one true theorem and one false
corollary.

**The true theorem** (Samuelson, eq. 12). Let `Q*_T` be the terminal-wealth distribution of the
max-geometric-mean strategy and `Q_T` that of any other uniform strategy. Then
`Q*_T(x) < Q_T(x)` for `T > M(x)`. Applying the law of large numbers to
`log X_T = log X_0 + Σ_t log x_t`, the max-geometric-mean strategy makes it "virtually certain"
that over a long enough sequence one ends with higher terminal wealth than any essentially
different rule. This much is not in dispute anywhere.

**The false corollary.** That therefore the expected utility of its outcome exceeds that of any
other rule for `T` large enough, or at least becomes a good approximation. Samuelson's crucial
observation about the true theorem is that **`M` is a function of `x` that is unbounded in `x`** —
the horizon at which dominance kicks in recedes as the wealth level considered rises, so the
"almost certainly" never converts into a statement about an expectation.

Samuelson's counterexamples:

- *Linear utility.* A gamble paying $2.70 or $0.30 per dollar with equal probability has geometric
  mean `√(2.7 × 0.3) = 0.9 < 1`, so the log-maximiser holds only cash. A `max E[X_T]` investor
  invests fully, because `E{X_T} = X_0 · 1.5^T > X_0 · 1^T` **for all `T`**. He is not a fool by
  his own criterion; the rare paths where he wins repeatedly more than compensate.
- *Concave power utility.* For `u(x) = x^γ/γ` with `1 > γ ≠ 0`, the optimal uniform strategy is
  the one-period optimum `w*(γ)`, independent of `T`, and `w*(γ) ≠ w^log` for every `γ ≠ 0`. The
  strong inequality `E{X_T^γ/γ} > E{X*_T^γ/γ}` therefore holds **for all `T`, however large**.
  Concavity does not rescue the corollary.
- *Bounded utility.* Markowitz's defence — that boundedness saves the rule — fails too: for
  `γ < 0` the false rule leads to *over*-riskiness where for `γ > 0` it leads to under-riskiness,
  and the unboundedness of `u` as `x → 0` puts a prohibitive penalty on the paths, which occur at
  every `T` with positive probability, where the rule brings you close to ruin. Where utility is
  bounded above *and* finite at zero wealth, **no uniform strategy can be optimal at all**; the
  true optimum is non-uniform, riskier than the log-maximiser at low wealth and less risky at high
  wealth.

**Merton–Samuelson turn the qualitative failure into a quantity, and this is the part with the
most force here.** Define the *initial-wealth equivalent* `Π₁₂(T; W₀)`: the factor by which an
investor's starting wealth must be multiplied for him to accept the max-expected-log program
`{w⁺⁺}` in place of his true optimum `{w*}`. For the iso-elastic family they derive (their eqs.
3.9–3.10)

```
Π₁₂(T; W₀) = λ(γ)^(T/γ) ,      λ(γ) ≡ E[(Z[w*])^γ] / E[(Z[w⁺⁺])^γ]
```

with `λ(γ) > 1` and `T/γ > 0` for `γ > 0` (and the signs flipping together for `γ < 0`), so
**`Π₁₂ → ∞` as `T → ∞`.** The compensation demanded for being made to follow the log rule *grows
without bound in the horizon*. The same authors show, by the analogous "how many years behind"
calculation, that `ΔT = T − T*`, the lag in periods needed to reach a given expected-utility
level, also `→ ∞` as `T → ∞`.

The sharpest case: for `γ < −1` (a sufficiently risk-averse investor) they show `φ(γ) > 1`, hence
`Π₁₃(T) → ∞` where `{w³}` is the program *holding nothing but the riskless asset*. The
max-expected-log program is dominated by holding cash, and with `R = 1` (non-interest-bearing
cash) being forced into it is, in the limit, "just as bad as having all his initial wealth taken
away."

**The second, subtler fallacy** (Merton–Samuelson §IV–V) is the one that matters for any attempt
to rescue the rule by moving to two parameters. Because a uniform strategy makes `log(W_T/W_0)` a
sum of i.i.d. variates, the CLT suggests replacing the true terminal distribution by a *surrogate
lognormal* fitted to its first two log-moments; then `E[log return]` and `Var[log return]` become
"asymptotically sufficient parameters" and an efficiency frontier in `(μ_log, σ²_log)` appears,
with `γ` selecting the point on it. They show by counterexample that this is an **improper
interchange of limits**: the CLT statement is about the *normalised* variable, and the discrepancy
between the correctly computed expected utility and the one computed from the lognormal surrogate
**goes to infinity, not to zero, as `T → ∞`** (their eq. 5.11). The general moral they state
explicitly: `lim Prob{U_A > U_B} = 1` neither implies nor is implied by
`lim{E[U_A] − E[U_B]} > 0`, and stochastic dominance over a growing-but-finite range of `x` does
not imply asymptotic first-order stochastic dominance.

**The constructive half, and the only place a log-moment frontier is legitimate.** The `(μ_log,
σ²_log)` parameters *are* asymptotically sufficient — but not as the number of fixed-length
periods grows. They are sufficient when a **fixed** planning horizon is subdivided into more and
more sub-periods, so the underlying probabilities become continuous-time gaussian
infinitely-divisible. In that limit no surrogate is involved and no approximation error is being
smuggled in. The frontier that results is a genuine one and is **distinct from the Markowitz
mean-variance frontier**, which is defined on returns rather than on logarithms of returns.

## Construction recipe

Neither paper proposes a strategy; the transferable content is a set of decision rules about how
to *read* growth-rate quantities.

1. **Never rank two candidate books by a growth-rate statistic alone** unless the decision-maker's
   objective is literally `E[log W]`. For any other iso-elastic preference the growth-maximising
   book is strictly suboptimal at every horizon.
2. **Never argue from "it will almost certainly win eventually" to "it is better in expectation."**
   The gap between the two is the entire subject of both papers.
3. If a two-parameter `(mean-log, variance-log)` summary is used, it is defensible only as a
   *continuous-time* description of a fixed horizon, and even then it defines its own frontier —
   points cannot be compared to, or substituted for, points on a mean-variance frontier.
4. The cost of using the wrong criterion compounds. `Π₁₂ = λ^(T/γ)` means the penalty is
   multiplicative per period, so a longer evaluation window makes a growth-optimal choice *worse*
   for a risk-averse scorer, not better.

## Robustness evidence (qualitative only)

Both results are theorems plus explicit counterexamples, so they cannot decay and are not subject
to replication risk in the usual sense — the relevant question is only whether anyone has shown
the algebra wrong, and in fifty-plus years of a large downstream literature nobody has. What is
disputed downstream is not the mathematics but its *practical weight*: the capital-growth school
(Thorp, Ziemba, Cover, Breiman's asymptotic optimality) accepts Samuelson's theorem and argues the
log criterion is nonetheless the right objective for an investor who genuinely compounds over long
horizons. That live disagreement is the subject of the companion note,
`2026-08-23-kelly-criterion-growth-security-tradeoff.md`, and the two notes should be read
together: the growth school's own summary lists "Fallacy: if maximizing `E log X_N` almost
certainly leads to a better outcome then its expected utility exceeds that of any other rule" as a
**fallacy**, citing Samuelson (1971). The two literatures agree on the mathematics and differ only
on which objective an investor should hold.

Samuelson's PNAS note carries a moderate citation count for a paper of its age (211), which
understates its standing: it is the canonical reference for this result and is cited by name
inside the growth-theory literature that disagrees with its emphasis. Merton–Samuelson's count
(70) is low for a JFE paper, and the Semantic Scholar record for that DOI is visibly damaged (it
reports year 2017 for a 1974 article), so the count should be read as an undercount in the same
class as the index anomalies session 7 recorded.

## Implementability here

Nothing to implement. What this closes is an **interpretation** question, and it closes it against
a direction the folder had been drifting toward.

**Direct bearing on the folder's own recent work.** Session 9 imported Fernholz–Karatzas's
identity `d log V^π = γ*_π dt + Σ_i π_i d log X_i` and made the excess growth rate `γ*_π` the top
candidate measurement (`SUMMARY.md` #23(b)), on the stated grounds that it is "denominated in log
growth and therefore on the gate's own axis." **That premise was wrong, and these two papers say
why in general rather than by anecdote.** Log growth is not the gate's axis; net Sharpe on a
six-year window is. A quantity denominated in log growth is not comparable to, convertible into,
or a proxy for a risk-scored objective, and Merton–Samuelson show that the natural repair — treat
`(mean-log, variance-log)` as a sufficient pair and build a frontier — is itself a fallacy outside
the continuous-time limit. `learnings.md` has since measured `γ*` on the promotion ladder and
found it a null (non-monotone, highest for the narrowest book, dominated by `Σ_i π_i a_ii`). That
empirical null and this theoretical result are the same fact seen from two sides: the lab measured
a growth-denominated quantity and found it did not track the gate, and here is the reason it never
could have been expected to.

**The generalisable screen, and it is free.** Before importing any theoretical quantity as a
diagnostic, ask: *is it denominated in the same units as the objective the gate reads?* The
folder's imports have been denominated in forecast MSE (bagging, model averaging), information
ratio (fundamental law), and log growth (stochastic portfolio theory) — three different currencies,
none of them net Sharpe. Each crossing needs an argument, and this note establishes that for the
log-growth currency **the crossing does not exist in general**, so the argument cannot be
supplied. That retires, on principle rather than by measurement, the class of proposals of the
form "optimise/measure growth rate because it is a return quantity."

**What it does *not* say.** It does not say growth-rate decompositions are useless. An accounting
identity that splits a realised quantity is still a valid accounting identity; `γ*` correctly
splits realised log growth into a selection term and an excess-growth term, and that split is true
regardless of what anyone's objective is. The error is only in treating the split as a scoring
axis. Similarly, nothing here bears on Willenbrock's or Cuthbertson et al.'s attribution
arguments, which are about where a realised return came from, not about what to maximise.

**A caution in the other direction, so the folder does not overcorrect.** The repo's gate is
itself a sample statistic on a short window, not the true objective either — see the companion
note `2026-08-23-statistics-of-sharpe-ratios.md`. "Log growth is not the gate's axis" is not the
same claim as "the gate's axis is the right one." Both of this session's notes point at the same
gap and neither closes it in the gate's favour.

## Related

- `notes/2026-08-22-excess-growth-and-return-decomposition.md` — the source whose `γ*` this note
  re-prices as an accounting term rather than an objective.
- `notes/2026-08-23-kelly-criterion-growth-security-tradeoff.md` — the growth school's reply, and
  the quantitative map from a growth objective to a risk-scored one.
- `notes/2026-08-23-statistics-of-sharpe-ratios.md` — the same question asked of the gate's own
  statistic.
- `notes/2026-08-21-diversification-return-and-rebalancing.md`,
  `notes/2026-08-22-rebalancing-return-attribution-critique.md` — the geometric-vs-arithmetic
  accounting that this note leaves standing.
- `experiments/learnings.md` — the entry recording `γ*` as a measured null on this universe.
