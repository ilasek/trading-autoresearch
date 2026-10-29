---
title: "Online multiple hypothesis testing" (review) — the field's own synthesis: LORD++ in closed form, the two named failure modes of a wealth-based budget (*alpha-death* and *piggybacking*), the batched rules that beat the fully-online ones, and the admission that online testing is weak below about a thousand hypotheses
authors: Robertson, Wason, Ramdas
year: 2023
venue: Statistical Science 38(4), 557–575 (venue tier 1 — the discipline's review journal)
url: https://doi.org/10.1214/23-STS901
citations: 23 (Crossref `is-referenced-by-count`, checked 2026-10-29) and 23 (Semantic Scholar DOI endpoint, same date) — the two indexes agree exactly. OpenAlex was over its free daily budget and was not consulted.
sample_period: n/a — a review of methodology. Its own case studies are a mouse-phenotyping database and a platform clinical trial. **No market data, nothing after 2023.**
markets: none. Named application domains are genomics, clinical platform trials and A/B testing.
tier: A (peer-reviewed review in a tier-1 venue; but a review, so every claim in it is secondary and is flagged as such below)
validation_overlap: false
published_post_2018: true
read: full text of **arXiv:2208.11418**, the preprint of the Statistical Science article, `arxiv.org/pdf/2208.11418` → 110 KB of clean text via `pdftotext -layout`, 718 instances of `" the "`, zero `( )` dropout, title and author line verified. Sections read in full: 1.2 (error rates), 2.2.1–2.2.2 (LORD/LORD++/SAFFRON), 5.1.1–5.1.10 (extensions), 5.2 (shortcomings), 6 (practical guidance incl. Table 4). Not read: §3 simulations in detail, §4 case studies, §2.1 GAI derivation (covered by the primaries in this cluster). Section numbering is the preprint's. **A review's claims about papers not read here are recorded as the review's attributions, not as verified findings.**
---

## Mechanism

No economic mechanism. This is the synthesis layer for the vein opened tonight, and it earns its own
note for three things no primary in the cluster supplies: a closed-form LORD++, the field's own names
for the two ways a wealth-based budget fails, and an honest statement of where the whole approach does
not work.

**LORD++, in the form to copy.** Given a non-increasing `{γ_t}` with `Σγ_t = 1`:

    α_t = w_0 γ_t  +  (α − w_0)·γ_{t−τ_1}·1{τ_1 < t}  +  α · Σ_{j : τ_j < t, τ_j ≠ τ_1} γ_{t−τ_j}

where `τ_j` is the time of the `j`-th rejection. The review's own gloss is the useful part: the first
term is the share of the initial wealth spent at `t`; the rest are the shares of the *earnings* from
earlier rejections, where **LORD++ awards `α − w_0` for the first rejection and `α` for every
subsequent one**, each reward being immediately spread over the future on the same `{γ_t}` schedule
shifted to start at the next instant. The reason the first reward is smaller is pure arithmetic on
`FDP = V/(R ∨ 1)`: the denominator is 1 whether `R` is 0 or 1 and only starts growing at the **second**
rejection, so `w_0` plus the first reward must not exceed `α`. The review's placement:
**"LORD++ as the online analog of the BH procedure"**, since `FDP̂_LORD(t) = Σ_{j≤t} α_j / (R(t) ∨ 1)`
is the online counterpart of BH's `FDP̂_BH(s) = n·s/|R(s)|`.

The default sequence is the one already met in this cluster, `γ_t ∝ log(t∨2)/(t·exp(√(log t)))`,
attributed to Javanmard–Montanari as power-maximising in the Gaussian setting. The guarantee
(attributed to Ramdas et al. 2017) is the familiar two-tier one: **conditional super-uniformity of the
nulls buys mFDR; independence plus monotonicity buys FDR.**

**The two named failure modes.** These are the review's terms and they are the single most
transferable thing in it:

- **Alpha-death.** *"a long stretch of null hypotheses, so that online testing algorithms make
  (almost) no rejections and lose nearly all of their alpha-wealth. Subsequently, the algorithm may
  have essentially no power, unless a non-null hypothesis with extremely strong signal (small
  p-value) is observed."*
- **Piggybacking.** *"a substantial number of rejections are made so that the online testing
  algorithms earn and accumulate enough alpha-wealth to reject later hypotheses at much less
  stringent thresholds (hence the later tests 'piggyback' on the success of earlier tests). This can
  lead to a spike in the FDR locally in time, even though the FDR over all time is controlled."*

The named remedy for both is **decaying-memory FDR (mem-FDR)** (attributed to Ramdas, Yang, Wainwright
and Jordan, NeurIPS 2017): a user-chosen discount `δ ∈ (0,1]` that *"pays more attention to recent
discoveries"* and *"thus smoothly forgets the past"*, with GAI++ rules that control mem-FDR under
independence — and, separately, *"they showed how to allow the algorithm to **abstain from testing** in
order to recover from alpha-death."*

## Construction recipe

**The error-rate ladder, with the review's own ranking.** `FDP(T) = V(T)/(R(T)∨1)`;
`FDR = E[FDP]`; `mFDR = E[V]/E[R∨1]`; `FDX_ε(T) = Pr{sup_{t≤T} FDP(t) ≥ ε}`. The review calls FDR
*"the central metric of interest"* and mFDR *"a convenient theoretically tractable proxy ... the
pragmatic alternative error rate choice if a suitable algorithm for FDR control is not available"*, and
is careful that the two have been found empirically similar in some settings and **not in general**.

**A validity-robustness result worth more than it looks.** Footnote 1: if the p-values are only
approximately valid — if there is an `ϵ > 0` with `Pr(P_t ≤ x) ≤ x(1 + ϵ)` for all `x` — then *"it is
straightforward to check that the FDR proofs still go through ... guaranteeing an FDR of `α(1 + ϵ)`
instead."* The degradation is **linear in the calibration error**, not catastrophic. For any lab whose
p-values come from a bootstrap rather than an exact null, this is the difference between "the theory
does not apply" and "the theory applies with a known, proportional haircut."

**Which rule for which dependence (Table 4, the whole point of the paper).** Condensed, with the
review's own pros and cons:

| error rate | rule | dependence assumption | the review's verdict |
|---|---|---|---|
| FDR / mFDR | **LORD++** | independent nulls (FDR); conditional super-uniformity (mFDR) | extensions exist for prior/penalty weights, decaying memory, asynchronous and batch testing; *"empirically robust to positive dependence"*; **not** robust to arbitrary dependence; typically lower power than SAFFRON/ADDIS |
| FDR | **SAFFRON** | as above | higher power *"if there is a significant fraction of non-nulls and the signals are strong"*; not robust to dependence |
| FDR | **ADDIS** | as above | higher power than SAFFRON *"when there are conservative nulls"*; asynchronous extension exists |
| FDR | **LOND** | **positive dependence (PRDS)** | provable control under positive dependence; *"substantially lower power than the algorithms above"* |
| FDX | **supLORD** | conditional super-uniformity | also controls mFDR **and FDR at stopping times**; the user picks the number of rejections after which FDX control begins, in exchange for power |
| FWER | **alpha-spending** | **none — arbitrary dependence** | *"very low power, rejects only a few hypotheses before becoming unable to reject any more"* |
| FWER | **ADDIS-spending** | uniformly conservative, independent nulls | higher power than alpha-spending; *"unclear how robust to departures from independence"* |

**The batched rules, which are the right shape for a lab that tests in nightly groups.** Attributed to
Zrnic, Jiang, Ramdas & Jordan (AISTATS 2020): online, FDR-preserving versions of BH and Storey-BH for
a stream of *batches*. They *"interpolate between online and offline methodology, thus trading off the
best of both worlds"* — with one batch they recover BH (or Storey-BH), with batches of size one they
recover LORD++ (or SAFFRON) — they *"have a higher power than the fully online testing algorithms"*,
a positive-dependence-valid variant was derived, and because they compose offline procedures they
*"imply FDR control over each constituent batch, and not just over the whole sequence of tests."*

**Asynchrony**, attributed to Zrnic, Ramdas & Jordan (JMLR 2021): versions of LORD++ and SAFFRON that
output `α_t` *at the beginning* of the `t`-th test and control mFDR *"despite arbitrary local
dependence and regardless of the decision times"*, at fixed times and at certain adaptively chosen
stopping times. The cost is explicit: *"in order to account for the uncertainty about the tests in
progress, the test levels assigned by asynchronous online procedures will often be more conservative."*

**The retesting rule.** §5.1.6 states the condition that makes a second look at the same hypothesis
legitimate: *"the choice of whether to retest must be made without using knowledge of the p-value
itself, but only that it was not rejected (e.g. that it is greater 0.01). In this example, under the
null the p-value will still be conditionally uniform in [0.01, 1]."* This independently confirms
Foster–Stine's revisiting policy
(`notes/2026-10-29-alpha-investing-sequential-error-budget.md`) from a second source.

**A free post-hoc diagnostic, applicable to procedures that were never designed for any of this.**
§5.1.9, attributed to Katsevich & Ramdas (*Annals of Statistics* 48(6), 3465–3487, 2020): a class of
simultaneous FDP bounds that are *"finite-sample"*, have *"a simple closed form"*, and — the operative
clause — *"since the guarantees are post hoc, they apply to any sequence of rejections produced by any
online algorithm, that may or may not have been designed for FDR or FDP control."* So a `1 − α`
confidence bound on the FDP of an existing rejection set can be computed **without changing the
procedure that produced it**.

**Software**: the `onlineFDR` R package on Bioconductor implements LORD++, SAFFRON, ADDIS and most of
the extensions including the online-FWER and online-FDX rules, with a Shiny app. Named, not run.

## Robustness evidence (qualitative only)

As a review in a tier-1 venue by authors central to the literature, its value is its breadth and —
unusually — its candour about limits. §5.2 is where it earns the tier, and the first shortcoming is
the one that governs everything in tonight's cluster:

> Online testing algorithms are most powerful in settings where there are a large number (i.e.
> `T > 1000`) of hypotheses that will eventually be tested. Thus the biggest advantage will likely be
> in settings such as A/B testing in large tech companies or in large-scale biological data
> repositories. However, while platform trials provide a framework for a trial to continue
> indefinitely in theory, in practice they will typically evaluate a maximum number of interventions
> in the low tens. Hence, **there is a need for investigation of optimal online testing procedures
> when the maximum number of hypotheses to be tested is relatively low and when the correlation
> between hypotheses is known** (e.g. because of a shared control arm).

The remaining shortcomings are equally relevant: optimal choices of `w_0`, `{γ_t}`, `{λ_t}` are
**open**; the batch-size/power trade-off is **open**; and *"one major shortcoming with almost all of
the proposed online testing algorithms is their reliance on the assumption of independence of the null
p-values for provable FDR control, which is unlikely to always be case in real data applications"*,
with arbitrary dependence across all time called *"a rather pessimistic and unrealistic assumption"*
and local dependence the realistic middle. On computation: *"the algorithms presented in this paper
all scale linearly with the number of hypotheses tested."*

The review also records a governance problem that has no analogue in a single-agent lab but is worth
knowing exists: a common online procedure across teams means *"their tests must be subject to a level
determined by the results of experiments by other groups"*, which the authors expect to be hard to
sell.

Everything in this note attributed to Ramdas et al. 2017, Zrnic et al. 2020/2021, Xu & Ramdas 2022,
Katsevich & Ramdas 2020, Tian & Ramdas 2019, Fischer et al. 2023, Chen & Arias-Castro 2021, Döhler et
al. 2021, Cook et al. 2022, Weinstein & Ramdas 2020 or Fisher 2021/2022 is **the review's
attribution**; those papers were not read.

## Implementability here

**The honest headline first: the review's own small-`T` caveat is the discount on this entire vein.**
`program.md` records 109 trials at the v3 cut-over clustering to 36 effective ones. That is two orders
of magnitude below the `T > 1000` where the review says the advantage lives, and it sits squarely in
the band the review names as an **open problem** — *"relatively low"* numbers of hypotheses *"when the
correlation between hypotheses is known"*. The lab's correlation structure is, in fact, partly known
(the deflator already clusters trials), which makes this lab an instance of the open problem rather
than a beneficiary of the solved one. **Nothing in tonight's cluster should be presented to a strategy
session as a better gate.**

**The level arithmetic, worked once here for the whole cluster.** `α = 0.05`, the default
`γ_t ∝ log(t∨2)/(t·exp(√(log t)))` with its normalising constant re-derived as `C ≈ 0.0772`,
one-sided `z` from `Φ⁻¹(1−α_t)`:

    Alpha-spending (online Bonferroni), alpha_t = alpha*gamma_t
       t =   1   alpha = 4.96e-3   z = 2.58
       t =   8   alpha = 4.40e-4   z = 3.33
       t =  36   alpha = 1.07e-4   z = 3.70      <- the lab's effective trial count
       t = 110   alpha = 3.50e-5   z = 3.98      <- the lab's raw trial count

    LORD++ / LORD, k trials after a promotion (reward alpha spread on the gamma schedule)
       k =   1   alpha = 4.96e-3   z = 2.58
       k =   5   alpha = 6.48e-4   z = 3.22
       k =  10   alpha = 3.61e-4   z = 3.38

    FDR parameterisation (w_0 = 0.005, b_0 = 0.045), no reward yet
       t =   1   alpha = 4.96e-4   z = 3.29
       t = 100   alpha = 3.86e-6   z = 4.47
       t = 300   alpha = 1.25e-6   z = 4.71

    finite-horizon alpha-spending, wealth exhausted by trial M (uniform alpha/M)
       M =   8   alpha = 6.25e-3   z = 2.50      <- one night's budget
       M = 300   alpha = 1.67e-4   z = 3.59

Against this: `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` puts the *detectable*
full-window gap at `|t| ≈ 1.41 / 2.15 / 2.80` for confusion-set sizes `τ = 1 / 10 / 50`, and
`program.md` records that **no promotion in this repo's history has ever cleared `|t| = 2` on
validation**. Every level above except the two most generous (`z = 2.50`, `z = 2.58`) sits **above the
detection floor**. The conclusion is arithmetic, not judgement: *an online error-rate gate, honestly
parameterised, would have promoted nothing in this lab's history, and the binding constraint is the
width of the 2018–2023 window rather than the error rule.* That is the same conclusion `#323` reached
from a completely different direction, which is the strongest form of agreement available here.

**What the lab's condition is called, and that it has a published name is the finding.** With roughly
seven promotions across ~109 trials and a recent run dominated by `REJECT`/`GATE_FAIL`, this lab is in
**alpha-death**: a wealth-based budget started at the beginning of its history would now be near zero,
and *"the algorithm may have essentially no power, unless a non-null hypothesis with extremely strong
signal is observed."* Two consequences worth a human's attention:

1. *The remedy is published and it is a discount factor.* **mem-FDR** forgets the past at a
   user-chosen rate `δ`. `program.md` currently takes the opposite position by design — *"The trial
   count spans every version ... v1's 104 trials and v2's all searched the same 2018–2023 window"* —
   and that position is correct for the reason given (they really did search the same window). But the
   literature says a *principled* discount exists, controls a named error rate, and is the standard
   answer to exactly the condition this lab is in. **Whether the lab wants it is a human decision**
   about which window its history is really about; the point this note can make is that "discount old
   trials" is not a corner-cut, it is a published error-rate object.
2. *Abstention is a legitimate move.* The same work *"showed how to allow the algorithm to abstain
   from testing in order to recover from alpha-death."* `program.md` budgets eight trials a night and
   `CLAUDE.md` tells a session to spend them across families. Under this accounting, **running fewer
   trials on a night with no good hypothesis is a recognised, error-rate-preserving action rather than
   a wasted session.** That is a real licence, and it is the opposite of what a budget-filling
   instinct would do.

**And what the lab's one recorded multi-promotion episode is called.** `program.md` records a run of
four consecutive promotions whose holdout performance subsequently deteriorated, and that this is why
the holdout veto exists. **Piggybacking** is the literature's name for that failure mode and its
mechanism is exactly the one `program.md` describes structurally: a run of rejections loosens the
threshold for what follows, so the error rate spikes *locally in time* even when the all-time rate is
controlled. The lab reached the right remedy (a veto that is not part of the sequential budget) by
observation; the literature reached it by theory. Worth recording because it means the holdout veto is
**doing a job the sequential layer provably cannot do** — a local-in-time error spike is invisible to
an all-time guarantee — so nothing in this vein is a candidate for replacing it.

**The one structural recommendation, and it is the night's best-aimed item.** The lab does **not**
test one hypothesis at a time: it tests **up to eight per night**, available simultaneously, dependent
within the night (one window, often one family) and far closer to independent across nights. That is
precisely the **online batched** setting, where the review reports the rules *"have a higher power than
the fully online testing algorithms"*, recover BH within a single batch, come in a
positive-dependence-valid variant, and *"imply FDR control over each constituent batch, and not just
over the whole sequence of tests"*. So **if any of this vein is ever implemented here, the frame is
online-batched BH / Storey-BH over nightly batches — not LORD, not SAFFRON, not ADDIS.** Both of the
fully-online families computed above are the wrong shape for this lab's actual experimental design, and
the batched rules are strictly more powerful in it. The primary (Zrnic, Jiang, Ramdas & Jordan,
AISTATS 2020, *The power of batching in multiple hypothesis testing*) was **not read tonight** and is
the named first target for whichever session picks this up.

**The one free diagnostic that needs no protocol change at all.** Katsevich–Ramdas simultaneous FDP
bounds are *post hoc* and apply to **any** rejection sequence from any procedure. So a `1 − α` upper
bound on the false-discovery proportion of this lab's seven promotions is computable from the recorded
verdicts alone, with no change to `run_experiment.py`, no new trial, and no holdout read. That is the
cheapest item in tonight's output and the only one that could be acted on without a protocol decision.

**Pitfalls.** (a) This is a review: every claim about a paper not in tonight's cluster is an
attribution, and a session acting on one should read the primary. (b) The `onlineFDR` package is R and
Bioconductor; the lab is Python with a frozen `engine/`, so it is a reference implementation, not a
dependency. (c) `mFDR` here means `E[V]/E[R∨1]`, which is Foster–Stine's `mFDR_η` at a different
offset and **not** Javanmard–Montanari's `sFDR` — three similar names for three different objects
across the cluster's three primaries; always check the denominator. (d) The review's own mFDR/FDR
"empirically similar" remark is explicitly *not* general, and the counterexample it cites is in the
Javanmard–Montanari supplement.

## Related

- The three primaries of tonight's cluster:
  `notes/2026-10-29-alpha-investing-sequential-error-budget.md`,
  `notes/2026-10-29-lord-online-fdr-and-the-dependency-price.md`,
  `notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md`.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — the `|t|` floor the level arithmetic
  above is measured against; same conclusion by a different route.
- `notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md` — the other anytime-valid object
  this folder has read, and the axis correction that applies here too: a sequential guarantee over
  *new data* with a fixed roster is not the same object as a fixed window with a growing roster.
- `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-08-24-multiple-testing-haircut.md`,
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md`,
  `notes/2026-09-16-clustering-trials-onc-effective-number-of-trials.md` — the fixed-sample layer this
  would sit beside.
