---
title: "Online FWER control and ADDIS-Spending" — the error-rate object that is actually right when discoveries are rare, and the mechanism that makes a *decisively* failing test cost nothing: discard any p-value above a threshold and the error budget's index does not advance
authors: Tian, Ramdas
year: 2021
venue: Statistical Methods in Medical Research 30(4), 976–993 (peer-reviewed; a specialist methods venue, not a venue-tier-1 statistics journal)
url: https://doi.org/10.1177/0962280220983381
citations: 15 (Crossref `is-referenced-by-count`, checked 2026-10-29, resolved first call by DOI). Modest in absolute terms but healthy for a 2021 methods paper in a specialist venue; OpenAlex and Semantic Scholar were unavailable this session (daily budget exhausted / 429) and were not relied on.
sample_period: n/a — a methods paper. Evidence is theorems, a Gaussian sequence model, simulations, and one real dataset (International Mouse Phenotyping Consortium). **No market data, nothing after 2021.**
markets: none. Stated application domain is biological experimentation with hypotheses accumulating over time.
tier: B
validation_overlap: false
published_post_2018: true
read: full text of **arXiv:1910.04900** (the version carrying the 03.10.20 running header), `arxiv.org/pdf/1910.04900` → 157 KB of clean text via `pdftotext -layout`, 696 instances of `" the "`, one `( )` hit (a displayed-equation artefact, not systemic dropout), title line verified. Sections read in full: 1 (introduction), 2 (online Sidak and fallback), 3.1–3.4 (discarding, adaptivity, ADDIS-Spending, local dependence), 4.1–4.2 (power theorems), 6 (conclusion). Appendices B/D/F (the proofs of Theorems 2/3/4) were **not** read; the theorem statements are quoted as stated. Numbering below (Definition 1, Propositions 3–4, Theorems 1–4, eqs. 6–23) is this version's; the SMMR version was not obtained (SAGE paywall) and may differ.
---

## Mechanism

No economic mechanism. This note exists because the two preceding notes in tonight's cluster both
reach the same conclusion by different routes — that **FDR is not the error object this lab needs** —
and this is the paper that builds the object it does need.

The argument for FWER here is not a preference, it is arithmetic. `Pr{V ≥ 1}` and
`E[V/(R∨1)]` are different numbers only when `R` is large. Under the complete null they are
identical; Foster–Stine's Theorem 2 makes them identical whenever a procedure stops at a fixed number
of rejections; and this lab makes roughly one promotion per several dozen trials and *stops the
session the moment one happens*. So the folder's existing FWER-flavoured layer was never the wrong
criterion, and what was missing was only the forward bookkeeping. The paper opens by noting that the
online FWER problem is *"underexplored"* — Foster and Stine *"only mention in passing that for online
FWER control, one can simply use an online Bonferroni method (that they term Alpha-Spending)"* — and
then builds the powerful version.

**Alpha-Spending** (online Bonferroni) is the baseline: pick `{γ_i}` summing to one, test `H_i` at
`α_i = αγ_i`. It is valid under **arbitrary dependence**, which is its whole selling point, and the
proof shows exactly where it is loose. It controls the per-family error rate
`PFER = E[V] = Σ_{i∈H₀} E[1_{P_i≤α_i}] ≤ Σ_{i∈H₀} α_i ≤ Σ_{i∈ℕ} α_i = α`, and `FWER ≤ PFER` by
Markov. Two inequalities, two distinct leaks:

- **(A)** `E[1_{P_i≤α_i}] ≤ α_i` is loose **when the null p-values are conservative** — when the
  typical null p-value sits far above where it is being tested.
- **(B)** `Σ_{i∈H₀} ≤ Σ_{i∈ℕ}` is loose **when a large fraction of the stream is non-null.**

The paper's contribution is one mechanism per leak, and the combination.

**Discarding (leak A).** Choose a threshold `τ_i`. If `P_i > τ_i`, **do not test it — discard it, at
no charge.** If `P_i ≤ τ_i`, test at `α_i < τ_i` subject to `Σ_{i∈S} α_i/τ_i ≤ α`, where
`S = {i : P_i ≤ τ_i}`. The concrete rule (eq. 11) is the one to memorise:

    α_i = α·τ_i·γ_{t(i)} ,     t(i) = 1 + Σ_{j<i} S_j

**The budget's index `t(i)` counts only the tests that were not discarded.** A test whose p-value
lands above `τ` leaves the index — and hence every future level — exactly where it was.

**Adaptivity (leak B).** Choose `λ_i`. A `P_i ≤ λ_i` is a *candidate* and costs nothing; a
`P_i > λ_i` costs `α_i/(1−λ_i)` from the budget, subject to `Σ_{i∉C} α_i/(1−λ_i) ≤ α`. This is the
FWER-side twin of SAFFRON's mechanism.

**ADDIS-Spending** combines both, and is the paper's recommendation:

    α_i = α·(τ_i − λ_i)·γ_{t(i)} ,     t(i) = 1 + Σ_{j<i} (S_j − C_j)

with `S_j = 1{P_j ≤ τ_j}`, `C_j = 1{P_j ≤ λ_j}`, `λ_i < τ_i`, `α_i < τ_i`, and
`Σ_{i∈S\C} α_i/(τ_i − λ_i) ≤ α`. **The index advances only on p-values in the band `(λ, τ]`** —
neither a clear success nor a clear failure moves it. Setting `λ ≡ 0` recovers Discard-Spending;
setting `τ ≡ 1` recovers Adaptive-Spending. Suggested defaults: `λ = 1/4`, `τ = 1/2`.

## Construction recipe

**The validity condition, and it is the condition that decides whether this applies here.** The
discarding mechanism needs the nulls to be *uniformly conservative* (Definition 1):

    Pr{P ≤ xτ | P ≤ τ} ≤ x   for all x, τ ∈ [0,1]    ⟺    F(τx) ≤ x·F(τ)

i.e. `F` convex; a non-decreasing density suffices. **Theorem 1**: ADDIS-Spending controls PFER (hence
FWER) when the null p-values are uniformly conservative and independent of each other and of the
non-nulls. Proposition 3 (quoted from Zhao et al.) supplies the case that matters: *for a
one-dimensional exponential family with true parameter `θ ≤ θ₀`, the p-value from the uniformly most
powerful test of `H₀ : θ ≤ θ₀` is uniformly conservative* — exactly uniform at the boundary
`θ = θ₀`, and conservative in the interior. The paper's own worked instance:

> One simple example ... is the one-sided test of Gaussian mean, where we test the null hypothesis
> `H₀ : µ ≤ 0` against the alternative `H₁ : µ > 0` with observation `Z ∼ N(µ, 1)`. ... the p-value
> resulting from UMP test, that is `P = Φ(−Z)` is uniformly conservative, and is conservative if
> `µ < 0`, while **the conservativeness increases as `µ` decreases**.

**Local dependence** (§3.4, following Zrnic et al.). Independence is unrealistic — *"tests that occur
nearby in time may share the same dataset; null hypotheses are often constructed given the information
of recent testing results"* — but arbitrary dependence across all time is equally unrealistic. The
middle object is: for each `i` there is a lag `L_i` with `P_i ⊥ P_1,…,P_{i−L_i−1}`, so `P_i` may be
*arbitrarily* dependent on the previous `L_i` p-values and is independent of everything before them
(with `L_{i+1} ≤ L_i + 1`). The fix is the **"principle of pessimism"**: ignore what happened in the
last `L_t` steps and hallucinate the worst outcome for them, formally `α_i, τ_i, λ_i ∈ F^{i−L_i−1}`.
The altered ADDIS-Spending rule (eq. 23) is one index shift:

    α_i = α(τ_i − λ_i)·γ_{t(i)} ,   t(i) = 1 + (L_i ∧ (i−1)) + Σ_{j<i−L_i} (S_j − C_j)

**Theorem 2**: altered ADDIS-Spending controls PFER (hence FWER) in a strong sense under uniformly
conservative nulls *and* local dependence. The lag costs exactly `L_i` positions in the `γ` sequence —
a cheap, explicit, one-off price.

**Choosing `γ`** (Theorem 3). For Alpha-Spending in a Gaussian mean model, among `q`-series the
power-optimal `q` tends to 1 as the horizon grows, so *"one should resort to log-`q`-series for higher
power"* — the same family as LORD's default. The trade-off is stated plainly: slower decay protects
long-run detection, but *"if the testing process stops at a certain point, then the sequence that
decays too slow will hurt the power"*. **Theorem 4**: in that model, with a log-`q` series, there is a
`c*` such that `E[D_ADDIS(λ,τ)] ≥ E[D_spend]` for all `λ ∈ [0, c*)` and `τ ∈ (c*, 1]` with
`τ − λ < 1`; and `c*` increases with the non-null fraction, the alternative mean *and* `µ_N`,
**reaching one when `µ_N = 0`**. That last clause is the sharp boundary: if the nulls are exactly
uniform, `c* = 1`, the admissible `τ` collapses to 1 and **the discarding gain vanishes**. The gain
exists only to the extent the nulls are genuinely conservative.

## Robustness evidence (qualitative only)

Theorems with proofs (the proofs themselves not read here), plus a Gaussian-model power analysis,
simulations, and one real biological dataset. The paper is honest about the trade it is making — the
adaptive and discarding mechanisms *"essentially require independence between p-values"*, relaxed only
to local dependence, while *"Alpha-Spending works even when the p-values are arbitrarily dependent"*.

Its negative result is as useful as its positive one and is reported without hedging: the
straightforward online extensions of classical offline FWER methods — **online Sidak**
(`α_t = 1 − (1−α)^{γ_t}`, valid under independence) and the **online fallback** procedure (valid under
arbitrary dependence, recycling levels from rejected hypotheses) — *"have a fairly negligible power
improvement over Alpha-Spending when non-nulls are interspersed randomly over time"*, and are
*"sub-optimal when they encounter a non-vanishing proportion of non-nulls, or a significant proportion
of conservative nulls"*. So **two of the four rules in this paper are not worth implementing**, and the
paper says so. That is methodology honesty in the rubric's sense and is why the tier is B rather than
C despite the specialist venue and modest citation count: the independent-replication evidence a
grading would want does not yet exist, and the power claims rest on an idealised Gaussian model.

Independent corroboration of the standing of these rules, from a peer-reviewed review read the same
session (`notes/2026-10-29-online-multiple-testing-practical-guidance.md`): it places alpha-spending
as *"robust to arbitrary dependence"* with *"very low power"*, and ADDIS-spending as *"higher power
than Alpha-spending"* with the caveat *"unclear how robust to departures from independence"* — and
notes that Fischer et al. extended ADDIS-spending to graphical testing procedures while keeping FWER
control and improving its power under local dependence.

## Implementability here

**The reason this is the most actionable note in tonight's cluster.** The lab's hypothesis is a
one-sided test of exactly the form Proposition 3 covers: validation **skill** — Sharpe minus the
equal-weight eligible pool's on the same days — against `H₀ : skill ≤ 0`, with a paired block-bootstrap
standard error. And the lab's own measurements say its typical candidate sits well **inside** the null,
not at its boundary: `experiments/learnings.md` records the 2026-10-26/27 nightly finding that ten
trials cleared the train gate at **mean validation skill −0.105** while five failed it at **−0.037**.
Negative `µ` is precisely the condition under which `P = Φ(−Z)` is conservative, *"while the
conservativeness increases as `µ` decreases"*.

**So the lab is not near the `µ_N = 0` boundary where Theorem 4's `c*` reaches one and discarding buys
nothing. It is deep in the regime where discarding buys the most.** That is the finding, and it is the
one thing in this vein that is specific to this lab rather than generic.

**What it implies, concretely: the cost of a trial depends on where its p-value landed, not on how
decorrelated it was.** Under ADDIS-Spending with `λ = 1/4`, `τ = 1/2`:

- a candidate with `p > 1/2` (measured skill below the pool — most of this lab's trials) is
  **discarded: the budget index does not advance and every future level is unchanged**;
- a candidate with `p ≤ 1/4` is a candidate and also costs nothing;
- only a candidate landing in the band `(1/4, 1/2]` — a *near-miss* — advances the index.

**This is a direct tension with `experiments/learnings.md`, and it should be recorded as a tension
rather than resolved.** That file's second entry reads *"Every trial raises the bar: the deflated-Sharpe
benchmark grows with the trial count in `experiments/trials.jsonl`. Sweeping parameters wastes shared
budget"*, and `program.md` repeats it (*"every trial ... raises the deflated-Sharpe bar for all future
candidates — wasteful trials have a real cost"*). The same file also records that DSR clustering makes
within-family tuning *"nearly free in deflation terms"*. The online-FWER accounting prices trials on an
**orthogonal axis**: a decisive failure is free however decorrelated it was, and a near-miss is the
expensive thing however correlated it was. Neither accounting is wrong — they bound different error
rates — but a session that quotes "every trial raises the bar" as though it were the whole cost
structure is using one axis and calling it the budget. **Both prices exist and they rank trials
differently.**

**The level arithmetic, which is also why this stays a diary.** `α = 0.05`, `λ = 1/4`, `τ = 1/2`, the
log-`q` default `γ`, so `α_i = 0.0125·γ_{t(i)}`:

    t(i) =  1   →  α = 1.24e-3   one-sided z = 3.03
    t(i) =  5   →  α = 1.62e-4   z = 3.60
    t(i) = 10   →  α = 9.04e-5   z = 3.74
    t(i) = 20   →  α = 4.75e-5   z = 3.90

and with a nightly batch of eight treated as one locally-dependent block (`L = 7`, eq. 23), the index
starts at 8 rather than 1, so the first level is `1.10e-4` (`z = 3.69`) and twenty band-landings later
it is `3.43e-5` (`z = 3.98`). Compare plain Alpha-Spending at the lab's raw count: `t = 36` gives
`z = 3.70`, `t = 110` gives `z = 3.98`.

**Two readings of those numbers, and both matter.** (i) The discarding mechanism genuinely converts
the lab's raw trial count into a far smaller effective index — **tens, not hundreds** — which is the
largest single power gain available anywhere in this vein, and it arrives for free from a property the
lab has already measured. (ii) It is still not enough. Every level above demands a one-sided `z`
beyond 3.0, against `notes/2026-10-28-argmin-inference-minimax-separation-rate.md`'s detection floor of
`|t| ≈ 2.80` at `τ = 50` and `program.md`'s record that **no promotion in this repo's history has ever
cleared `|t| = 2` on validation**. The binding constraint is the width of the validation window, which
is exactly what `#323` said and which no error-rate rule can relax.

**Adaptations if the lab's human ever wants this.** (a) Count **only `PROMOTE` as a rejection**;
`FAMILY_LEAD` and `SCOUT` never face the champion comparison and must not fund anything — this is
Foster–Stine's gravity hazard. (b) Set the lag `L` from the session structure, not from taste: within
one night eight candidates share a window, and within a family they share a return stream, so `L = 7`
is the floor and a family-level block is the honest version. (c) `τ = 1/2` means "discard anything
whose measured skill is at or below the pool's" — operationally the lab's existing `REJECT` verdicts,
which makes the rule's bookkeeping almost free to compute from `trials.jsonl` *retrospectively, by a
human*. (d) Do **not** implement online Sidak or online fallback; the paper measures them as
negligible improvements on alpha-spending.

**Pitfalls.** (a) Uniform conservativeness is an assumption about the **null** distribution, and a
bootstrap p-value is not automatically the UMP p-value of an exponential family — the Proposition 3
route is an argument by analogy until someone checks the lab's bootstrap calibration, and this note
does not claim it has been checked. (b) `λ < τ` and `α_i < τ_i` are conditions, not knobs. (c) The
local-dependence fix is *pessimistic by construction*: it throws away the last `L` steps' information,
so a large `L` is a real power cost, paid up front. (d) Theorem 4's guarantee is for a log-`q` series
only; a `q`-series or a hand-tuned sequence voids it. (e) Everything here is **FWER/PFER**, so it is
not comparable to an FDR number at face value — `FWER ≤ PFER` by Markov and the chain is one-way.

## Related

- `notes/2026-10-29-alpha-investing-sequential-error-budget.md` — the mFDR/FDR equivalence at a fixed
  number of rejections, which is the reason FWER is the right object here at all; also the gravity
  hazard on padded rosters.
- `notes/2026-10-29-lord-online-fdr-and-the-dependency-price.md` — the FDR side, SAFFRON's adaptivity
  (which does *not* pay here) versus this paper's discarding (which does), and the arbitrary-dependence
  `(1 + log i)` price.
- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — the review's placement of these
  rules, and the field's own caveat that online testing is weak below ~1,000 hypotheses.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — the `|t|` floor that caps all of it.
- `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md` — the lab's existing FWER
  machinery, which this would sit beside rather than replace.
