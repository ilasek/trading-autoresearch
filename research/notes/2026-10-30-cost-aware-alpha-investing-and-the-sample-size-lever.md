---
title: "Cost-aware Generalized α-investing for Multiple Hypothesis Testing"
authors: Cook, Dubey, Lee, Zhu, Zhao, Flaherty
year: 2024
venue: The New England Journal of Statistics in Data Science — venue tier 2/3 (peer-reviewed but a new journal; theorems with appendix proofs, so checkable)
url: https://doi.org/10.51387/24-nejsds64
citations: 1 (Crossref, checked 2026-10-30); 3 (Semantic Scholar, checked 2026-10-30)
sample_period: n/a — statistical methodology. Evidence is synthetic simulation plus two public biological datasets; no market data and no calendar period
markets: none (methodology)
tier: B
validation_overlap: false
published_post_2018: true
---

## Mechanism

This is the **third nomination** from `SUMMARY.md`'s [2026-10-29] open questions — the one named
there in the review's own words, *"where the cost of data collection is not negligible … the choice
of sample size for each experiment, as well as prior beliefs about the probability of rejection"*,
performing best *"where the aim is to maximise a limited budget of tests to achieve the highest
possible power"*. That is `program.md`'s eight-trials-a-night problem stated by somebody else, so it
was worth one paper. Read in full (arXiv v3, Nov 2023; the NEJSDS version of record is open).

The setting is α-investing: an experimenter starts with a stock of **α-wealth**, pays a bet `φ_j` to
test hypothesis `j` at level `α_j`, and receives a payout `ψ_j` on a rejection. Wealth must stay
non-negative, and that constraint is what controls the error rate over an unbounded stream. What
this paper adds is a **second budget** — real money, or samples — and the observation that once data
costs something, the *sample size of each test* becomes a decision variable sitting alongside the
level. Testing becomes a game against nature in which the experimenter chooses `(α_j, φ_j, ψ_j, n_j)`
jointly.

The part that matters here is not the method but its **dynamics**, which the paper is the first in
this vein to state as theorems:

- **Submartingale (Theorem 1):** α-wealth is stochastically non-decreasing — an unbounded number of
  tests is sustainable — when the power `ρ_j` is near one *or* the prior probability `q_j` that the
  null is true is near zero.
- **Supermartingale (Theorem 2):** α-wealth is stochastically non-increasing, and *"the generalized
  α-investing testing procedure will end in a finite number of steps"*, when power is near zero *or*
  the prior null probability is near one. The literature's name for this is **α-death**.
- **Martingale (Theorem 3):** the knife edge, reached by choosing the payoff structure so that
  nature plays an equalizing strategy — `ρ_j = (1/(1−q_j))(φ_j/ψ_j − q_j α_j)`.

And the escape route from α-death is named explicitly: non-decreasing wealth *"require[s] `ρ_j ↑ 1`
for a fixed `θ̄_j` which, in the case of a Gaussian, would require `σ_j/√n → 0` or `n → ∞`. So, the
α-wealth grows unbounded if the sample size is unbounded."* **More data per test is the only cure.**

The second failure mode is the mirror image. **Piggybacking**: an experimenter who tests easy
hypotheses first accumulates wealth and then spends it recklessly on hard ones, so that the same
difficult hypothesis is treated differently depending on where in the sequence it lands. Their
Figure 1 is the clean demonstration — a synthetic stream with `q_j = 0.01` for 100 hypotheses and
then `q_j = 0.95` for the next 100: plain ERO investing makes **8 false rejections** after the
switch, their cost-aware rule makes none. The paper's design premise is the fix stated as a
principle: *"the investigator should be indifferent, in expectation, as to the position of the
difficult hypothesis in the sequence of tests."*

## Construction recipe

**Cost-aware ERO (CAERO).** Per test, solve a small constrained program:

    maximise over (φ_j, α_j, ψ_j, n_j):   E_θ(R_j)·ψ_j  −  λ·c_j·n_j
    subject to   ψ_j ≤ φ_j/ρ_j + α           (mFDR control)
                 ψ_j ≤ φ_j/α_j + α − 1       (mFDR control)
                 φ_j/ρ_j = φ_j/α_j − 1
                 ρ_j = 1 − Φ( z_{1−α_j} − θ̄_j/(σ_j/√n_j) )      (level–power–sample-size link)
                 ρ_j ≥ ρ_lo                                      (power floor)
                 φ_j ≤ a·W_α(j−1)                                (bet cap)
                 n_j·c_j ≤ W_$(j)                                (money budget)
                 E[ΔW_α] = 0                                     (equalizing / martingale)

Inputs that must be supplied per test: the prior `q_j` that the null is true, the alternative
`θ̄_j`, the noise scale `σ_j`, the per-sample cost `c_j`, and the two wealth stocks. Settings the
authors use: **`a = 0.025`** as the cap on the fraction of α-wealth a single test may bet
(*"setting a = 0.025 gave good results"* — introduced specifically to stop "betting the farm"), and
**`ρ_lo = 0.9`** when `n` is unconstrained. A finite-horizon variant optimises over the next 2–5
tests rather than myopically.

The two constraints doing the conceptual work are the level–power–sample-size link, which is what
makes `n_j` a lever at all, and `E[ΔW_α] = 0`, which is what makes abstaining free (below).

## Robustness evidence (qualitative only)

Peer-reviewed, theorems proved in appendices, synthetic experiments plus two public biological
datasets (a prostate-cancer expression set and LINCS L1000). Low citation count and a young venue,
hence tier B rather than A; nothing here has been independently replicated.

The authors' own limitations are the useful part:

- **Sensitivity to the prior is asymmetric.** CAERO is *robust to variance* in `q_j` around a correct
  mean — they attribute this to the rule's conservatism and its chance to recover from losses — but
  **sensitive to bias**. Their measured instance: with a true null probability of 0.9 on average, an
  assumed `q = 0.85` performs **273 fewer tests** than the correct value, because the downward bias
  makes the rule spend α-wealth more aggressively than it should. They name the investigator who is
  *"systematically optimistic"* as the failure case and say the principled fixes — robust
  optimisation, or online learning of the `q` process — are outside the paper's scope.
- **The martingale constraint is only in expectation**, so gambler's ruin remains possible; the bet
  cap `a` is a patch, not a guarantee.
- No hedging of either wealth stock, and the money budget is assumed to be fixed and non-replenishing.

## Implementability here

**Verdict: an ANTI-CANDIDATE as a method, and the clearest statement in the vein of why. Three
transferable findings, all free.**

**Why the method itself cannot be used.** CAERO's entire contribution is the choice of `n_j`, and
**this lab has no such lever**: the validation window is fixed by protocol at roughly 1,510 trading
days, identical for every candidate, and cannot be extended for a promising one. Remove `n_j` and
constraint (19e) ceases to be a decision and the program degenerates to the ERO investing the paper
itself shows is prone to piggybacking. Worse, the power floor is arithmetically out of reach: a
one-sided test at level `α_j` reaches power `ρ_lo` only if the non-centrality — which is the
full-window `|t|` this lab measures — satisfies `|t| ≥ z_{1−α_j} + z_{ρ_lo}`, i.e. **`|t| ≥ 2.93` at
a 5% level for `ρ_lo = 0.9`** (3.24 at 2.5%; 2.49 at 5% even if the floor were relaxed to 0.8),
against `program.md`'s record that **no promotion in this lab's history has ever cleared `|t| = 2` on
validation** and `#323`'s detectable gap of `1.41 / 2.15 / 2.80` at this window's width. Constraint
(19f) is infeasible here for any effect size this lab has ever measured. This is the **fourth
consecutive session** to arrive at the fixed width of the validation window as the binding
constraint, and the first to arrive there from a paper whose explicit remedy is buying more data.

**Finding 1 — α-death is a prediction, not bad luck, and `#332` is upgraded from attribution to
theorem.** Theorem 2 says wealth is supermartingale, and testing ends in finite steps, when power is
near zero or the prior null probability is near one. This lab satisfies **both** antecedents: the
`|t|` floor above is the first, and `learnings.md` records the typical candidate at negative
validation skill, which makes the honest `q` here very close to one. So the α-death `#332` diagnosed
from the review is the *predicted* state of any wealth-based gate in this lab, derivable before any
implementation — and the paper's own escape route (`n → ∞`) is the one route the protocol forbids.
A session should not read this as a reason to loosen anything; it is a reason not to build the gate.

**Finding 2 — a formal licence to abstain, stronger than `#332`'s.** The equalizing-strategy
construction sets payoffs so that *"the investigator is indifferent as to whether to test or not test
and the expected payoff is 0"*: under a correctly calibrated martingale wealth rule, **declining to
run a trial costs nothing in expectation.** So the lab's existing practice — killing candidates on
free screens before writing them, and running fewer than eight trials on a thin night — carries no
hidden opportunity cost in error-budget terms. The contrapositive is the sharper half and is worth
carrying: **a scheme under which abstaining feels costly is a scheme that is not martingale** — it is
either piggybacking (submartingale) or dying (supermartingale).

**Finding 3 — the prior must come from the lab's own base rate, not from the designer's belief.** The
bias asymmetry above is aimed squarely at a research lab: a systematically optimistic `q_j` is the
default state of anyone who has just written a hypothesis they like, and bias (unlike noise) is what
this class of rule cannot absorb. If any wealth-based accounting is ever built here, **`q_j` must be
set from the measured base rate of this lab's own recorded verdicts and nothing else.** Note the
direction: the honest `q` here is *higher* than a designer would write down, and a too-low `q` causes
over-spending, so the error is in the dangerous direction.

**A fourth item, offered as a reading of the lab's history rather than as a finding.** `program.md`
records that between trials #43 and #51 four consecutive promotions raised validation Sharpe while
holdout Sharpe fell — which is the shape of this paper's Figure 1, where accumulated wealth from easy
tests finances false rejections once the stream turns hard. The paper's own principle (indifference to
the difficult hypothesis's position in the sequence) is what a holdout veto enforces and a sequential
wealth rule structurally cannot, and that is consistent with `#332`'s finding that the veto covers a
failure mode the sequential layer provably cannot see. Offered as consistency, not proof: this lab's
episode was never measured against this paper's mechanism, and nobody should claim it was.

**Pitfalls.** (a) Everything above is about *accounting*; nothing in this paper proposes or motivates
a strategy, and no part of it belongs in a hypothesis. (b) `mFDR` here is the Foster–Stine object, a
third denominator alongside the two `notes/2026-10-29-online-multiple-testing-practical-guidance.md`
already warns about — check the denominator before comparing any level across these notes.
(c) Their `a = 0.025` and `ρ_lo = 0.9` are tuned on their simulations and must not be carried over as
constants. (d) The paper's simulations are the authors' own, in their own favour, and unreplicated.

## Related

- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — §5.1.8, which nominated this
  paper; and the source of `#332`'s α-death / piggybacking framing, which this note upgrades to
  theorems.
- `notes/2026-10-29-alpha-investing-sequential-error-budget.md` — Foster–Stine, the α-investing
  primary this paper extends; its `mFDR_η` sub-martingale argument is the object under discussion.
- `notes/2026-10-30-online-batched-fdr-and-the-dependence-that-matters.md` and
  `notes/2026-10-30-post-hoc-fdp-bounds-for-any-rejection-sequence.md` — tonight's other two notes;
  all three land on the fixed validation window as the binding constraint, by three different routes.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — `#323`'s detectable-gap arithmetic,
  which is what makes this paper's power floor infeasible here.
