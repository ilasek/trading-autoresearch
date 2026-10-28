---
title: "Locally minimax optimal confidence sets for the best model" — the fundamental limit on identifying the best of many candidates from a fixed sample, and a sample-splitting test that attains it; the separation rate grows only as √(log of the number of *confusable* candidates), but no valid procedure of any kind can beat it
authors: Kim, Ramdas
year: 2025
venue: arXiv preprint `2503.21639` (v4, 22 September 2025) — math.ST. **Not peer-reviewed.** By this folder's rubric that is tier 4/working-paper territory and the rubric's standing instruction is explicit: "a preprint with no replication is Tier C however impressive its architecture."
url: https://arxiv.org/abs/2503.21639
citations: 0 (OpenAlex `cited_by_count` for `10.48550/arXiv.2503.21639`, checked 2026-10-28 — the work resolves and the count is genuinely zero, not missing). Crossref has no record of the arXiv DOI. Semantic Scholar returned HTTP 429 on the arXiv-id endpoint and was not retried, per `research/README.md`'s guidance not to spend calls on a rate-limited endpoint.
sample_period: none for the theory. The one real-data illustration is two held-out machine-learning classification competitions with 44 and 39 submitted models and test sets of 183 and 1,236 binary-error observations. **One of the two competitions postdates 2023; nothing from either is used here beyond the structural shape (d models, n observations) and the qualitative ordering of set sizes**, and no dated result, no performance figure and no narrative from them appears below.
markets: none — the paper is domain-free statistics
tier: C
validation_overlap: false
published_post_2018: true
read: full text of `arxiv.org/pdf/2503.21639` on the first try (1.9 MB → 757 KB of clean text via `pdftotext -layout`, 711 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). Sections 1–7 and Appendix A.10 read in full; the long proof appendices were skimmed only for the statements relied on here. Note for a later session: `pdftotext -layout` on this file pads heavily with whitespace, so pipe regions through `tr -s ' '` before reading them.
---

## Mechanism

No mechanism in the economic sense. This is the **theory of the object the previous note describes**:
given `2n` observations of a vector `X ∈ R^d` with unknown mean `µ`, form a confidence set for
`arg min_k µ_k`. For this lab, `d` is the number of recorded trials and each observation is one day's
vector of losses (negated active returns) across them, so this is `rank_trials.py`'s tier-1 problem
stated exactly.

Why the tier grade is C and the note is still worth its length: the content is theorem-and-proof, so
the parts this note leans on are **checkable rather than believed** — the separation-rate arithmetic,
the construction, and the explicit union-bound computation in Appendix A.10. The tier constrains how
much weight the paper's *novel comparative* claims get (that its test beats the alternatives
empirically), and those are the claims this note does not rely on.

## Construction recipe

**The dual problem.** By test–confidence-set duality, test `H₀ : r ∈ Θ` versus `H₁ : r ∉ Θ` for each
`r`, where `Θ = arg min_k µ_k`, then set `Θ̂ = {k : ψ_k = 0}`. Writing
`s = sargmin_{k ≠ r} µ_k` (smallest index attaining the min), the hypothesis reduces to
`H₀ : µ_r − µ_s ≤ 0`, a one-sided one-sample problem — except that `s` is unknown.

**The DA (dimension-agnostic) argmin test.** Split the `2n` observations into halves `D₁, D₂`.

1. **Selection on `D₂`.** Either the plug-in rule `ŝ_plug = sargmin_{k ≠ r} X̄_k^{(2)}`, or the
   noise-adjusted rule
   `ŝ_adj = sargmin_{k≠r} (X̄_k^{(2)} − X̄_r^{(2)}) / √(γ_k' Σ̂^{(2)} γ_k ∨ κ)` with
   `γ_k = e_r − e_k` and `κ = 10⁻⁸` for numerical safety — i.e. select on a signal-to-noise ratio
   rather than on a raw mean difference.
2. **Inference on `D₁`.** Reject `H₀ : r ∈ Θ` iff
   `√n · γ_ŝ' X̄^{(1)} > z_{1−α} · √(γ_ŝ' Σ̂^{(1)} γ_ŝ)` — a plain one-sided `t`-test of whether
   `µ_r − µ_ŝ > 0`.
3. **Multi-split aggregation.** Average the statistic over `K` random splits (the paper uses 10 and
   50) and threshold via the subsampling calibration of Guo–Shah (2025), to remove the dependence on
   one arbitrary split.

**Why the splitting is load-bearing, not hygiene.** Under `H₀`, `µ_r − µ_ŝ ≤ 0` for *any* `ŝ ≠ r`, so
validity survives a wrong selection; under `H₁`, `ŝ` is right often enough to give power. Without the
split, the same data pick the most significant comparison and then test it — "which results in
strongly dependent summands in the test statistic. This strong dependency structure breaks the
conditions for central limit theorem and leads to invalid inference." The naive statistic
`max_{k ≠ r} (X̄_r − X̄_k)/σ̂_{r,k}` is exactly that double dip.

**The rate.** Define the **confusion set** of `r`:

    C_r = { k ∉ {r} ∪ Θ_{−r} :  (µ_r − µ*)/2  ≤  µ_k − µ*  ≤  C_n √(log d / n) }

i.e. the candidates close enough to the best to be mistaken for it, but not so far from `r` as to make
the comparison easy. Candidates outside it do not contribute to the problem's difficulty. With
`τ = |C_r|`, the **critical radius** is

    ε* = √( (1 ∨ log τ) / n )                                        (eq. 8, σ suppressed)

Theorem 3.1: power → 1 whenever the true gap exceeds `C'_n ε*` for any `C'_n → ∞`. Corollary 3.2:
then `r` is excluded from `Θ̂` with probability → 1. Theorem 3.3 and Corollary 3.4 are the matching
**lower bounds**: if the gap is sufficiently *smaller* than `ε*`, then *no* asymptotically level-`α`
test has non-trivial power and *no* asymptotically valid confidence set can reliably exclude `r`. The
rate therefore interpolates from the parametric `1/√n` when the confusion set is small to
`√(log d / n)` in the worst case, and the DA test attains it **without knowing `τ`**, which is what
"locally minimax optimal" means here.

**Uniform coverage.** Section 5 distinguishes three guarantees — *weak* (`Θ̂` meets `Θ`), *pointwise*
(`inf_{r ∈ Θ} P(r ∈ Θ̂) ≥ 1−α`), *uniform* (`P(Θ ⊆ Θ̂) ≥ 1−α`) — identical when `Θ` is a singleton and
strictly ordered otherwise. The DA test targets pointwise. Two upgrades to uniform are given: a
one-step version running the test at `α/d` (union bound; globally but not locally minimax optimal) and
a two-step version that pre-screens on `D₂` at level `n^{−1/2}` and then tests on the full sample at
`α/(1 ∨ |Θ̂^{(2)}|)`, which the simulations find holds its nominal level while the one-step version is
conservative.

## Robustness evidence (qualitative only)

Theory: validity needs only a Berry–Esseen-type moment condition on the contrasts
`W_k = γ_k'(X − µ)` — "little more than finiteness of a second moment" — and permits arbitrarily
strong dependence **between coordinates**, which is the relevant direction here (two trials' daily
active returns are heavily correlated). A heavy-tail-robust variant attaining the same rate is given
in Section 4, exercised on multivariate-`t(3)` draws.

Simulation findings, reported as the paper's own and discounted to tier C: a competitor method based
on cross-validation plus privacy noise is **liberal**, with an empirical–nominal gap of 0 to 0.05 that
does not shrink as the sample grows; Bonferroni and a rank-CI method are valid but less powerful; and
the computational spread is large — at `d = 100`, `2n = 1000`, single core in R, the MCS bootstrap at
`B = 5000` takes **633 s** against **0.007 s** for the base DA test, with the 10-split aggregate at
5–11 s.

**The qualification that matters most, and the one this folder should carry.** Appendix A.10 supplies a
complete, explicit proof of Hansen–Lunde–Nason's Theorem 1(i) (credited to Jing Lei), and the bound it
reaches is

    P(M* ⊄ MCS)  ≤  |M*| × 2^{|M₀|} × o(1)  +  α + o(1)

so "as long as `|M₀|` remains constant" the `α` survives; "however, when the size of the model space
`|M₀|` increases with `n`, stronger uniform conditions … or specific convergence rates are needed to
ensure validity." Their conclusion is worded as a reading, not a refutation: "**we believe that the
MCS procedure should be viewed as a fixed-size model selection method**". HLN's own statements are
consistent with that — nothing there claims a growing `M₀` — so this is a scope clarification. It is
recorded here rather than in the MCS note because the arithmetic is this paper's.

## Implementability here

**The headline is a free, decisive piece of arithmetic about the lab's own board, and it is a lower
bound — so it cannot be fixed with a better test.**

Take the validation window at `2n ≈ 1,510` daily observations, hence `n ≈ 755` per half. Rearranging
`ε*`, the gap a valid procedure can detect corresponds to a **one-sided `t`-statistic on the inference
half of order `√(1 ∨ log τ)`**:

| confusable candidates `τ` | `ε*` (units of σ, the sd of a pairwise daily difference) | required `t` on the half-sample | equivalent `t` on the full window |
|---|---|---|---|
| ≤ 1 | 0.0364 | 1.00 | 1.41 |
| 5 | 0.0462 | 1.27 | 1.79 |
| 10 | 0.0552 | 1.52 | 2.15 |
| 30 | 0.0671 | 1.84 | 2.61 |
| 50 | 0.0720 | 1.98 | 2.80 |
| 60 | 0.0736 | 2.02 | 2.86 |

(My arithmetic from eq. (8) at `n = 755`; the last column multiplies by `√2` because inference uses
half the window. `C'_n → ∞` means these are floors to be comfortably exceeded, not thresholds to be
met.) Three readings, in descending order of how much they should change behaviour:

1. **The lab's board sits inside the region the lower bound declares undecidable.** `program.md`
   records that "no promotion in this repo's history has ever cleared |t| = 2 on validation", against
   a trial count of 36 at the v3 cut-over and more since. At `τ` in the tens the table's required
   full-window `t` is 2.1–2.9. So the observed `t`s are *below the minimax floor for a board this
   size* — and Corollary 3.4 says that is not a defect of the lab's ranking code, because **no valid
   procedure can exclude a candidate at those gaps.** A wide tier 1 is therefore not a weakness of the
   bootstrap; it is the only honest answer available at this `n` and this `d`. This is the same
   conclusion HLN reach philosophically ("we view this as a strength"), now as a theorem with a number.
2. **A crowded board is cheap; a short window is not.** The rate's dependence on the candidate count
   is `√log τ` — going from 10 recorded trials to 50 raises the required `t` by a factor of
   1.98/1.52 = **1.30**, while halving the window would raise it by `√2 = 1.41`. So the deflated bar's
   premise (each trial raises the bar for all future candidates) is right in direction and **mild in
   magnitude on the separation axis**: the marginal cost of one more trial to the board's resolving
   power is logarithmic. The binding constraint is the fixed 2018–2023 window, not the trial count.
   (This bears only on *separation between candidates*; it says nothing about the deflated-Sharpe
   bar's own multiple-testing logic, which is a different statement — see the related notes.)
3. **Only the confusion set counts, and it is smaller than `d`.** `τ` counts candidates genuinely
   close to the best, not all recorded trials: a trial whose skill is far below the leader's does not
   degrade the rate. So the right diagnostic for the board is "how many trials sit within half the
   leader's gap of the best", which is computable from stored validation returns and is a better
   summary of the board's difficulty than `d`.

**How to implement, concretely and for free.** The DA argmin test on `experiments/trial_returns/`:
loss `L_{i,t} = −(r_{i,t} − r_{pool,t})`, split the validation days into halves (the paper splits
i.i.d. observations — see the pitfall below), select with `ŝ_adj`, test with the one-sided `t`, invert
over all `r` for the set, and aggregate over 10–50 splits. Three settings follow from this lab's cell
rather than from taste: use `ŝ_adj` not `ŝ_plug`, because trials differ widely in volatility and the
noise-adjusted rule selects on signal-to-noise; use the **two-step** uniform construction if the
question is "does tier 1 contain every best trial" (the lab's question) rather than "is this trial
plausibly best"; and expect a *wider* set than the current board if the current board is pointwise,
since Section 6.6 finds pointwise methods substantially under-cover `P(Θ ⊆ Θ̂)` when `|Θ|` is large.

**Pitfalls.**
- **The theory is for i.i.d. observations across `t`.** Daily active-return differences are close to
  serially uncorrelated but are heteroskedastic and volatility-clustered, which is *not* i.i.d. The
  paper's dependence allowance is across coordinates, not across time. HLN's `α`-mixing assumption plus
  the moving-block bootstrap is the more honest fit to daily data; the DA test's advantage is speed and
  the rate, not time-series generality. Do not present a DA set as assumption-free on this panel.
- **Sample splitting costs `√2` in `t`** and introduces split randomness; the multi-split aggregate is
  not optional at this `n`.
- **The set is still silent about `M₀`'s complement** — same scope limit as the MCS.
- **Nothing here touches holdout**, and nothing here is a candidate. This is a diagnostic over already
  recorded validation returns, so it spends no trial and raises no bar.

## Related

- `notes/2026-10-28-model-confidence-set-the-set-valued-ranking.md` — the method this paper gives a
  theory for and a qualification to. Read that one first.
- `notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md` — the other response to the
  fixed-`|M₀|` problem: instead of letting `d` grow with `n`, make the guarantee time-uniform.
- `notes/2026-10-23-noise-sensitivity-of-risk-measures.md` (`#294`) and
  `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` (`#310`) — the two other
  places this folder has turned a panel's shape into an exact number. Note the contrast worth keeping:
  those are `N/T` ratios that **diverge** at a critical value, whereas this one grows as `√log τ` and
  therefore never blows up. Not every width penalty is a cliff.
- `notes/2026-10-21-stability-selection-subsampling-error-control.md` and
  `notes/2026-10-21-knockoff-filter-fdr-control-vs-permutation.md` — the selection-error layer; the
  multi-split aggregation here is the same subsampling idea applied to a test rather than to a
  selection frequency.
- `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-09-16-clustering-trials-onc-effective-number-of-trials.md` —
  the deflator's own machinery. Reading 2 above is about separation between candidates and does **not**
  license weakening the deflated bar; the two corrections answer different questions.
