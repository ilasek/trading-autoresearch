---
title: "Simultaneous high-probability bounds on the false discovery proportion in structured, regression and online settings"
authors: Katsevich, Ramdas
year: 2020
venue: The Annals of Statistics 48(6), 3465–3487 — venue tier 1
url: https://doi.org/10.1214/19-AOS1938
citations: 33 (Crossref, checked 2026-10-30); 54 (Semantic Scholar, checked 2026-10-30)
sample_period: n/a — statistical methodology. Evidence is theorems plus simulations and one genome-wide association study; no market data and no calendar period
markets: none (methodology)
tier: A
validation_overlap: false
published_post_2018: true
---

## Mechanism

This is the named primary behind queue item `#328` — the cheapest thing in the folder's queue and
the only item in the sequential-testing vein that needs **no protocol change at all**. Read in full
tonight (arXiv v4, the version submitted to the *Annals*).

The object is a **post-hoc, simultaneous upper bound on the false discovery proportion**. The
distinction from everything else in this vein is worth stating precisely, because it is what makes
the bound free. An FDR procedure controls `E[FDP(R*)] ≤ q` for **one** rejection set `R*`, the one
its own stopping rule picked; the experimenter must report that set and no other, and the guarantee
is about an average over repetitions. These bounds instead hold **simultaneously over a whole path
of candidate rejection sets**, with probability `1 − α`, so the experimenter may look at every bound
on the path and *then* choose which set to report, keeping the guarantee on whatever they chose.
That is the Goeman–Solari exploratory-inference paradigm, reached here by a martingale argument
rather than by closed testing, which is what buys the closed form.

The authors state the diagnostic use in as many words: *"our results can also be used as diagnostic
tools for FDR procedures: one can run an FDR procedure at a certain level and then obtain a valid
upper bound on the FDP of the resulting rejection set."* And for the online case they are explicit
that the guarantee is **post hoc**, so it *"would apply to any sequence of rejections produced by any
online algorithm, that may or may not have been designed for FDR or FDP control."* Nothing about the
procedure that generated the rejections has to change, or even to have existed.

The economic content is nil; this is pure accounting. Its value to this lab is that it answers a
question the lab has never been able to ask: *of the promotions this lab has made, what fraction
could be false, with 95% confidence?*

## Construction recipe

Every bound in the paper has the same shape. Take a **path** of nested candidate rejection sets
`Π = (R_0, R_1, …)`, take the **FDP estimate** `V̂(R_k)` that some FDR procedure implicitly uses on
that path, pick a regularisation constant `a > 0`, and form

    FDP̄(R_k)  =  c(α) · ( a + V̂(R_k) ) / |R_k|,        Pr{ FDP(R_k) ≤ FDP̄(R_k) for all R_k ∈ Π } ≥ 1 − α

The constant `c(α)` is explicit, tight and dimension-free; which `c` applies depends on the case.
The authors recommend **`a = 1`** (*"usually, we set a = 1"*, and *"we have found a = 1 to be a good
choice"*; different `a` gives envelopes tighter in different places). The paper tabulates the
`(path, V̂)` pairs and the FDR procedure each comes from: sorted path with `V̂ = n·p_(k)` → BH;
pre-ordered paths → accumulation tests and Selective/Adaptive SeqStep; interactive paths → STAR and
AdaPT; and the two online cases below. Bounds can be extended off the path to all subsets by
interpolation.

**The two cases this lab would use.**

*Batch / BH (Theorem 1).* With hypotheses sorted by p-value and `R_k = {j : p_j ≤ p_(k)}`,

    FDP̄_sort(R_k)  =  [ log(1/α) / log(1 + log(1/α)) ] · ( 1 + n·p_(k) ) / |R_k|

requiring null p-values independent and stochastically larger than uniform.

*Online, any algorithm (Theorem 4, part 1 — the one `#328` needs).* Let `α_1, α_2, …` be the levels
at which hypotheses were tested, each predictable with respect to a filtration `G_k` containing at
least the past accept/reject indicators, and let `R_k = {j ≤ k : p_j ≤ α_j}`. Then with

    FDP̄_online-simple(R_k)  =  [ log(1/α) / ( a · log(1 + log(1/α)/a) ) ] · ( a + Σ_{j≤k} α_j ) / |R_k|

the bound holds simultaneously for all `k ≥ 0` with probability `≥ 1 − α`, **provided the null
p-values are conditionally super-uniform given the past**: `Pr{p_k ≤ s | G_{k-1}} ≤ s` for every null
`k` and every `s ∈ [0,1]`.

*Online, adaptive (Theorem 4, part 2).* Replacing `Σ α_j` with `Σ (α_j/(1−λ_j))·1{p_j > λ_j}` — the
SAFFRON/alpha-investing estimate — gives the same form with `B ≡ sup_j α_j/(1−λ_j)` appearing in the
constant. This is tighter when many p-values are large (conservative nulls), which is this lab's
documented regime.

So the whole recipe for a post-hoc audit is: **the number of rejections, and the sum of the levels at
which every hypothesis was tested.** Two numbers.

## Robustness evidence (qualitative only)

Tier-1 journal, 33 Crossref / 54 Semantic Scholar citations, theorems with proofs, reproduction code
published by the authors. The bounds are compared against the existing simultaneous-FDP alternatives
(Goeman–Solari closed testing with Simes and Fisher local tests) in the paper's own simulations, and
the authors are candid about where they lose: the GS–Simes bound is *"tightest for small rejection
set sizes"* and the comparison is region-by-region rather than uniform. Their stated advantage over
closed testing is not tightness but that *"our closed-form expressions make the price of simultaneity
explicit"*. The martingale technique is new in the paper and is contrasted deliberately with the
backwards-filtration supermartingale argument used for FDR control.

## Implementability here

**`#328` is computable, and at this lab's current scale it is VACUOUS. That is tonight's answer and
it is arithmetic, not opinion.**

`c(α) = log(1/α)/(a·log(1 + log(1/α)/a))` at `α = 0.05` is **2.163** at `a = 1`, 1.636 at `a = 2`,
1.276 at `a = 5`. The bound is informative only when it comes out below 1, which requires

    |R_k|  ≥  min over a>0 of  c(0.05, a) · ( a + Σ_{j≤k} α_j )

Using the figures this folder may legitimately read — the **seven promotions** `program.md` records
and the **~129 recorded trials** named in `SUMMARY.md`'s [2026-10-29] entry and in the repo's own
commit log (I have not read `experiments/trials.jsonl`; a strategy session should confirm both
inputs and the per-trial levels before quoting any of this) — and assuming each trial was tested at
a nominal one-sided 5%, `Σ α_j ≈ 6.45` and the bound evaluates to

    FDP̄ ≈ 2.30  at a = 1,   1.98 at a = 2,   1.94 at a ≈ 2.7  (the minimum over a)

A bound of 1.94 on a proportion says nothing. **Non-vacuity at seven rejections requires
`Σ α_j ≤ 2.35`, i.e. an average per-trial level at or below about 1.8%.** The full threshold table,
`a` optimised, at `α = 0.05`:

    rejections R        1      2      3      5      7     10     20
    max Σ α_j       0.019  0.180  0.477  1.314  2.347  4.114  10.953
    ⇒ avg level
      over 129      0.015% 0.14%  0.37%  1.02%  1.82%  3.19%   8.49%
      trials

Three things follow, and the first is the useful one:

1. **The diagnostic's informativeness turns entirely on the per-trial level actually recorded, and
   the deflated bar works in its favour.** If the lab's effective per-trial level were a flat 5%, the
   bound is dead. But this lab's gate is a *deflated*-skill threshold that **tightens as the trial
   count grows** — which is exactly the `Σ α_j`-conserving behaviour the bound rewards. The question
   "is `#328` worth computing?" therefore reduces to one measurable quantity: **the sum of the
   effective levels at which the recorded trials were tested.** If that sum is below ~2.35, the lab
   can publish a 95% upper bound on the false-discovery proportion of its promotion history for the
   cost of a sum; if it is near 6.45, it cannot, and should say so rather than report a bound above 1.
   This is a sharper statement than `#328` was filed with, and it is a *precondition*, not a result.
2. **A single rejection can essentially never carry a non-vacuous bound** (`Σ α_j ≤ 0.019`). So this
   is an audit of the *history*, never of one promotion — which is the right reading anyway, and
   matches `#322`'s interpretation rule that single-candidate verdicts at this window's width are not
   separable.
3. The adaptive version (Theorem 4 part 2) is the one to compute if either is, because it credits
   conservative nulls and `learnings.md` records this lab's typical candidate sitting at negative
   validation skill — the uniformly-conservative regime `#330` established.

**The assumption that is the real obstruction, and it is the same one that narrowed `#331` tonight.**
Theorem 4 needs `Pr{p_k ≤ s | G_{k-1}} ≤ s` — the current null p-value conditionally super-uniform
given everything already seen. Every hypothesis this lab tests lives on **the same fixed 2018–2023
validation window**, and a new candidate's returns are correlated with the recorded returns of past
candidates, which are in `G_{k-1}`. Conditional super-uniformity is therefore not free here; it is
the assumption a shared window specifically breaks. Tonight's other note found the identical
obstruction from the other side — the batched FDR rules' power claim rests on independence within a
night, which one window cannot supply, leaving only the positive-dependence variant. **Stated once
as the night's structural finding: in this lab every hypothesis is a function of one fixed window, so
"independent across tests" is the single assumption that no sequential error-control object can get
here, and each such object must be checked against that before its arithmetic is believed.**

A second, smaller mismatch: requirement (22) wants `α_{k+1}` predictable. The lab's bar depends on the
*effective* trial count, which is computed from past trials' correlation structure — a function of
past returns, not merely of past verdicts. A larger filtration is permitted by the theorem, so this
alone is not a violation; it is the conditional-super-uniformity clause above that does the damage,
and the two should not be conflated.

**Pitfalls.** (a) `Σ α_j` runs over **every hypothesis tested, not every rejection** — an audit that
sums only the promotions' levels would understate it by a factor of ~18 here and produce a bound that
is wrong rather than merely wide. (b) `α` in the bound is the confidence level of the *bound*, not
the testing level; both being 0.05 in the arithmetic above is a coincidence of convention. (c) The
block-bootstrap calibration question that `SUMMARY.md` lists as a standing human decision applies
here too, and in the same linear form the review's footnote prices it. (d) Nothing in this note
licenses weakening the deflated bar; a post-hoc FDP bound and a promotion gate answer different
questions, and this one is explicitly not a gate.

## Related

- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` §5.1.9 — the review that
  attributed this bound and filed it as `#328`; the attribution is accurate and the note adds the
  precondition it could not supply.
- `notes/2026-10-30-online-batched-fdr-and-the-dependence-that-matters.md` — the other half of
  tonight's cluster, and the independent instance of the same shared-window obstruction.
- `notes/2026-10-28-model-confidence-set-the-set-valued-ranking.md` — the other post-hoc,
  set-valued object this folder has read; both answer "what can be said after the fact" rather than
  "what should the gate be".
- `notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md` — `#330`'s conservative-null
  regime, which selects the adaptive version of this bound over the simple one.
