---
title: "The Power of Batching in Multiple Hypothesis Testing"
authors: Zrnic, Jiang, Ramdas, Jordan
year: 2020
venue: AISTATS (PMLR vol. 108) — venue tier 2 (refereed ML proceedings; theorems with full proofs; implemented in the Bioconductor `onlineFDR` package and described in a tier-1 review)
url: https://arxiv.org/abs/1910.04968
citations: not resolved (Crossref — the PMLR proceedings version has no registered DOI; OpenAlex — free daily budget exhausted; Semantic Scholar — HTTP 429 on six spaced attempts; checked 2026-10-30). DataCite resolves the arXiv DOI 10.48550/arXiv.1910.04968 and reports `citationCount: 0`, which is a DataCite coverage artefact and NOT a usable count — it is not treated as one here. Tier is set on venue and replication status, not on this gap
sample_period: n/a — statistical methodology. Evidence is synthetic Gaussian simulation (T = 3000 hypotheses) plus one public credit-card transaction dataset; no market data and no calendar period
markets: none (methodology)
tier: B
validation_overlap: false
published_post_2018: true
---

## Mechanism

This is the named primary behind queue item `#331`, read tonight against the criterion the
[2026-10-29] `SUMMARY.md` entry pre-committed. It is an accounting mechanism, not a market
mechanism: it says at what level a *group* of simultaneously-available hypotheses may be tested so
that a running false-discovery-rate guarantee survives an unbounded number of such groups.

The problem it solves is that the obvious thing does not work. Running an offline procedure (BH, or
Storey's adaptive version of it) separately on each arriving batch, each time at the nominal level
`α`, **breaks FDR control** — the paper's own simulation shows realised FDR well above nominal for
small non-null fractions, and the only case where it does not is a batch so large that only three
batches are composed, where the trivial worst case `FDR ≤ 3α` saves it. So "we run BH on tonight's
eight candidates at 5%" is not a guarantee about anything beyond one night.

The fix is a *level* that is chosen before each batch and shrunk to pay for everything already
spent. At time `t` a batch of `n_t` hypotheses arrives, BH is run on it at a level `α_t` that is
measurable with respect to the past, and `α_t` is set so that an **empirical over-estimate of the
running false-discovery proportion** stays below `α` for every `t`. The estimate is purely
observable — every term in it is known to the experimenter — and controlling it implies the real
guarantee. That device is Storey's empirical-Bayes reading of BH, carried into a sequential setting.

The structural claim, and the reason the review called this the right shape for a nightly lab, is
that the construction **interpolates**: with a single batch the experimenter may spend the whole
budget and recovers plain BH; with batches of size one the estimate collapses to the one implicitly
used by LORD (or, in the adaptive version, SAFFRON). Batch size is the dial between offline power
and online openendedness.

## Construction recipe

Three procedures, and the distinction between them is the whole of tonight's finding.

**`BatchBH`.** Choose levels `α_s` such that, for all `t`,

    FDP̂(t) = Σ_{s≤t}  α_s · R_s⁺ / ( R_s⁺ + Σ_{r≤t, r≠s} R_r )   ≤ α

where `R_s` is the number of rejections in batch `s` and `R_s⁺` is the **augmented** count: the
largest number of rejections BH would have made in batch `s` if one of its p-values were replaced by
zero, levels and other p-values held fixed. `R_s⁺` can be as large as `n_s` for adversarial
p-values (their example: `n=3`, p-values `{2α/3, α, 4α/3}`, `R=0` but `R⁺=3`), but they measure
`R⁺ − R` concentrating around **1** in practice. An explicit update achieving it (their Algorithm 2)
needs a non-negative budget sequence `{γ_s}` with `Σ γ_s = 1`, sets `α_1 = γ_1 α`, and then

    α_{t+1} = [ Σ_{s≤t+1} γ_s α  −  Σ_{s≤t} α_s R_s⁺/(R_s⁺ + Σ_{r≠s,r≤t} R_r) ] · (n_{t+1} + Σ_{s≤t} R_s) / n_{t+1}

**`BatchSt-BH`.** The same with Storey-BH inside each batch, a user constant `λ_t ∈ (0,1)`
(`λ_t = 0.5` is their default; smaller if strong signal is expected), and the summand multiplied by
`1{P_{s,max} > λ_s}` — i.e. a batch whose *largest* p-value is below `λ_s` costs nothing.

**`BatchPRDS_BH`** (their Section 5, the variant that matters here). A much simpler estimate,

    FDP̂(t) = Σ_{s≤t}  α_s · n_s / ( n_s + Σ_{r<s} R_r )   ≤ α

with the explicit rule (their Algorithm 1): `α_1 = γ_1 α`, and after batch `t`,

    α_{t+1} = α · (γ_{t+1} / n_{t+1}) · ( n_{t+1} + Σ_{s≤t} R_s )

Note the denominator runs over `r < s`, not `r ≤ t`: each term is **frozen at the moment its batch is
tested**. This is a mini-batch generalisation of LOND.

**Guarantees.**

- `BatchBH` / `BatchSt-BH` (Theorems 1 and 2): anytime `FDR(t) ≤ α` for all `t`, *if* all null
  p-values in the sequence are independent of each other and of the non-nulls, *and* the procedure
  is **monotone** (making any tested p-value smaller may only increase the total rejection count).
- `BatchPRDS_BH` (Theorem 3): anytime `FDR(t) ≤ α`, *if* each batch satisfies **PRDS** internally
  and batches are independent of each other. No monotonicity requirement is stated for it.
- Because all three compose offline procedures with their own guarantees, they **also imply FDR
  control within each constituent batch**, not only over the whole stream — a genuine extra for a
  lab that cares about a night as well as about all time.

**Two construction details that bite at small batch size.** (i) Monotonicity is a property of the
p-value *distribution*, can be checked empirically (it does not involve the unknown ground truth),
and the paper's experiments **do not enforce it** — they use rules that are monotone "with
overwhelming probability" under natural p-value distributions and say so explicitly. (ii) The budget
sequence has to be chosen for the batch size: at their smallest batch size (10) they need
`γ_s ∝ s^{-2}` to stop `α_t` collapsing, precisely because `R_t⁺` can approach `n_t` when `n_t` is
small; at larger batch sizes they spend aggressively (`γ_1 = γ_2 = ½`).

**PRDS, concretely.** A p-value vector `P = (Φ(Z_1), …, Φ(Z_n))` from a multivariate Gaussian `Z`
with covariance `Σ` satisfies PRDS **iff `Σ_{i,j} ≥ 0` for every null `i` and every `j`**. So the
condition is non-negative correlation between each null hypothesis's statistic and every other
statistic in the same batch.

## Robustness evidence (qualitative only)

Theorems with proofs, by four authors central to this literature, in refereed proceedings, with a
reference implementation in `onlineFDR`; the batched rules are described (as attribution) in
Robertson–Wason–Ramdas's tier-1 review. Not independently replicated, hence tier B rather than A.

The methodological honesty is high and is the reason the evidence cuts against the review's summary
in one place. Three admissions matter:

- **The batch-size/power relationship is not monotone and the authors say they do not understand
  it.** Their discussion states it plainly — a very large batch makes BH's `α/n` slope conservative,
  so splitting may be better — and names a rigorous analysis of batch size versus power as an open
  problem.
- **Their power comparison is for the independence-assuming variants only.** Every experiment in the
  paper runs `BatchBH` or `BatchSt-BH` against LORD or SAFFRON. **`BatchPRDS_BH` is never run** —
  it exists in Section 5, Definition 4, Algorithm 1, Theorem 3 and an appendix proof, with no
  measured power anywhere.
- **At the smallest batch size the advantage largely disappears.** On the real dataset at `α = 0.1`,
  `BatchBH` at batch size 10 scored power **0.242 ± 0.053** against LORD's **0.231 ± 0.051** — a gap
  of about a fifth of one standard deviation — while batch size 100 scored **0.299 ± 0.100**; the
  adaptive pair was **0.240 ± 0.052** against SAFFRON's **0.211 ± 0.041**. In the easier synthetic
  design, the batch procedures beat LORD *"with the exception of `BatchBH` with the smallest
  considered batch size, for small values of `π₁`"*. The realised FDR at batch size 10 also ran
  highest of the three batch sizes (0.126 against LORD's 0.082, nominal 0.1).

## Implementability here

**The pre-committed criterion from the [2026-10-29] `SUMMARY.md` entry, answered clause by clause.**

- **(a) Is the per-batch level stated before the batch is run?** **Yes, for all three variants.** The
  paper requires `α_t` to be measurable with respect to `F^{t-1} = σ(P_1, …, P_{t-1})` and says in as
  many words that *"the test level at time t is only allowed to depend on information seen before
  t"*; Algorithm 1 computes `α_{t+1}` at the end of batch `t`. (Worth noting the filtration is the
  p-values themselves, richer than the `σ(R_1, …, R_t)` of earlier online work — they take the
  larger filtration deliberately, at the cost of giving up mFDR proofs.)
- **(b) Is the carried state `O(1)` in the number of batches already tested?** **`BatchBH` and
  `BatchSt-BH`: no. `BatchPRDS_BH`: yes.** In the first two, the `s`-th summand's denominator
  contains `Σ_{r≤t, r≠s} R_r`, so it changes every time a new batch is tested; evaluating the
  estimate at time `t` requires the triple `(α_s, R_s, R_s⁺)` for **every** past batch — state grows
  linearly in the number of nights. `BatchPRDS_BH`'s denominator `n_s + Σ_{r<s} R_r` is frozen when
  batch `s` is tested, so Algorithm 1 carries exactly a cumulative rejection count and a batch index.
- **(c) Is there a guarantee valid under dependence *within* a batch?** **Yes — and only for
  `BatchPRDS_BH`.** Theorem 1 and Theorem 2 require the null p-values to be independent of each other
  and of the non-nulls, which is dependence *within* a batch as much as across; Theorem 3 requires
  exactly **PRDS inside each batch and independence across batches**, which is this lab's own
  structure (eight candidates on one window, often one family, nearly independent night to night).

**So `#331` is ADMITTED, but as `BatchPRDS_BH` only — and the power claim does not come with it.**
This is the honest outcome and it is narrower than the review's attribution suggested. The clause
*"have a higher power than the fully online testing algorithms"* is measured for the two variants
that fail (b) and (c); the one variant that passes all three clauses is a mini-batch generalisation
of LOND, which the review's own table describes as having *"substantially lower power than the
algorithms above"*, and which this paper never measures. **The frame for this lab is online-batched
LOND, not online-batched BH.** A session wanting the batched-BH power would have to assume
within-night independence across eight candidates sharing one window — the one assumption this lab
provably cannot supply.

**The second clause of the criterion: what the paper's own arithmetic says at this lab's scale.**
Batch size ≈ 8 *is* inside the paper's measured range (its smallest batch size is 10, and the
`γ_s ∝ s^{-2}` budget it prescribes there is prescribed because small batches are the hard case). The
answer at that size is the one quoted above: a power gain of roughly a fifth of a standard deviation
on real data, and in the synthetic design the sole case where a batched rule *loses* to LORD is
small batch size at small non-null fraction — which is this lab's regime on both axes.
**On total hypothesis count the paper gives no number in the lab's range and none is extrapolated
here:** its synthetic design is `T = 3000` and its real-data test split is tens of thousands of
hypotheses, against this lab's few hundred recorded trials. The authors name the batch-size/power
trade-off as an open question and give only an intuition for it, so there is nothing to import.

**Derived arithmetic (mine, from the paper's Algorithm 1 and its own `γ_s ∝ s^{-2}` prescription for
small batches; not a result in the paper).** At `α = 0.05`, `n_t = 8`, BH rejects a batch's smallest
p-value only if it is at or below `α_t/8`, so the required one-sided `z` per night is:

    night t        1      2      4      8     16     32     64
    α_t (no       .0304  .0076  .0019  .00047 .00012 .00003 .000007
      rejections
      yet)
    required z    2.67   3.11   3.49   3.85   4.18   4.48   4.77

Accumulated rejections relax it only slightly (at night 16, ten prior rejections move the required
`z` from 4.18 to 3.99). A non-decaying uniform budget spread over 100 nights sits at `z = 3.84`
throughout. These are the same magnitudes `#334` computed for LORD and ADDIS-spending, against
`#323`'s detectable `|t| ≈ 1.41 / 2.15 / 2.80` at this window's width and `program.md`'s record that
**no promotion in this lab's history has ever cleared `|t| = 2` on validation**. So the batched frame
is the right *shape* and does not change the *verdict*: an online FDR gate of any flavour, batched
or not, would have promoted nothing. This is the fourth consecutive session to land on the fixed
width of the validation window as the binding constraint.

**The one design implication that is free and actionable now.** PRDS is a checkable condition with a
sharp failure mode: for Gaussian statistics it holds iff every null candidate's statistic has
non-negative covariance with every other statistic in the same batch. A night of eight candidates
from one family on one window plausibly satisfies it. **A night that deliberately mixes a candidate
with its own inverse, hedge or decorrelated complement does not** — negative cross-correlation is
exactly what PRDS forbids. That is a constraint on *how a night's eight candidates are chosen*, and
it cuts against the instinct to fill a night with deliberately decorrelated bets. Note it is a
constraint on the batched guarantee only; it says nothing about `program.md`'s distinct-mechanism
rule, which exists for different reasons and should not be read as being in tension with it.

**Pitfalls.** (a) The experiments do not enforce monotonicity, so even the measured power numbers
are for a heuristic rather than for the theorem's object — and monotonicity is a property of the
p-value distribution, which for a block-bootstrapped skill statistic is not obviously anything.
(b) `R_t⁺` requires re-running BH on the batch `n_t` times with one p-value zeroed; at `n_t = 8`
that is free, but it is a quantity the lab does not currently record. (c) `BatchPRDS_BH` needs
batch-to-batch independence of null p-values; two consecutive nights that re-test the same mechanism
on the same window are not independent, which is a real restriction on nightly agendas and not a
technicality. (d) Nothing here is a reason to weaken the deflated bar, which answers a different
question.

## Related

- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — the review that attributed the
  batched rules and named this paper as the target; its §5.1.7 claim is the one narrowed above.
- `notes/2026-10-29-lord-online-fdr-and-the-dependency-price.md` — LORD and the `(1 + log i)` price
  of abandoning independence; `BatchPRDS_BH` pays for dependence differently, by restricting it to
  the inside of a batch and demanding it be positive.
- `notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md` — ADDIS-spending, the other
  rule whose level arithmetic was computed at this lab's scale.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — the `|t|` floor the table above
  is measured against.
- `notes/2026-10-30-post-hoc-fdp-bounds-for-any-rejection-sequence.md` — the other half of tonight's
  cluster: what can be said about an existing rejection history *without* adopting any of this.
