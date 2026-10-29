---
title: "LORD and SAFFRON" — online FDR control by levels based on the most recent discovery: the generalisation that upgrades α-investing's mFDR to genuine FDR for *monotone* rules, prices arbitrary dependence at a `(1 + log i)` factor, and shows the realised false-discovery proportion is wide even when its mean is controlled
authors: Javanmard, Montanari (primary); Ramdas, Zrnic, Wainwright, Jordan (companion)
year: 2018
venue: The Annals of Statistics 46(2), 526–554 (venue tier 1); companion in ICML/PMLR (venue tier 2)
url: https://doi.org/10.1214/17-AOS1559
citations: 66 for Javanmard–Montanari (Crossref `is-referenced-by-count`, checked 2026-10-29, resolved first call by DOI). **SAFFRON's count could not be resolved**: it is a PMLR conference paper with no Crossref DOI, `api.crossref.org` bibliographic search returns only later articles citing it, `api.openalex.org` was already over its free daily budget (`Insufficient budget`), and `api.semanticscholar.org`'s `arXiv:` endpoint returned 429 while its DOI endpoint worked — exactly the ordering `research/README.md` records. Recorded as *not resolved (Crossref, OpenAlex, Semantic Scholar all tried, 2026-10-29)*, with no tier penalty on that basis alone per the rubric.
sample_period: n/a — methods papers. Evidence is theorems plus Gaussian-mean simulations (n = 1,000–3,000 hypotheses, 30,000 replications). **No market data, nothing after 2019.**
markets: none. The applications named are genomics and A/B testing.
tier: A (Javanmard–Montanari); B (SAFFRON — refereed conference venue, unresolved citation count, and its key claim is a power comparison in simulation)
validation_overlap: false
published_post_2018: false (JM 2018); true (SAFFRON, v2 2019)
read: full text of **arXiv:1603.09000** (10 July 2017 version, the Annals submission), `arxiv.org/pdf/1603.09000` → 164 KB of clean text, 645 instances of `" the "`, zero `( )` dropout, title line verified; and **arXiv:1802.09098v2** (10 July 2019), 88.7 KB of text, 411 instances of `" the "`. Both fetched first try with `-w 'HTTP %{http_code} size=%{size_download}'` and `file -b`. Numbering below is each arXiv version's (JM: Definition 2.1, Lemma 2.4, Theorems 3.1/3.4/3.7/4.1, Example 3.8, Proposition 4.2; SAFFRON: Theorem 1, §2.3). The published Annals and PMLR versions were not obtained and their numbering may differ. Appendices were not read beyond the statements cited.
---

## Mechanism

No economic mechanism. This is the second layer of the online error-accounting vein opened in
`notes/2026-10-29-alpha-investing-sequential-error-budget.md`, and it fixes that paper's two gaps:
the criterion (mFDR, a ratio of expectations) and the power.

**The class.** *Generalized alpha investing* (GAI) rules keep a potential `W(j)`, charge `ϕ_j` on a
non-rejection and pay `ψ_j` on a rejection, with the test level `α_j` a function of the past
*rejection indicators* only. Foster–Stine's rule is the member with `ϕ_j = α_j/(1−α_j)`,
`ψ_j = b_0 + α_j/(1−α_j)`. The governing intuition, and the reason this object behaves unlike
anything else in this folder's multiple-testing layer, is stated as **Remark 2.3**:

> as we reject more hypotheses the potential `W(j)` increases and hence we can use large test
> levels `α_j`. In other words, **the burden of proof decreases as we reject more hypotheses.**

That is the opposite sign to the deflated-Sharpe bar, which rises monotonically with the trial count
and never falls on a promotion. It is not a contradiction — the two objects answer different
questions — but it is the single most important structural difference to carry into a strategy
session, and it is developed in the implementability section below.

**LORD** = *Levels based On Recent Discovery*. Pick a non-increasing non-negative sequence
`γ = (γ_i)` with `Σγ_i = 1`; let `T(i)` be the discovery times before `i` and `τ_i = max T(i)` the
most recent one. Then the level for hypothesis `i` is a *discounted* share of wealth, with the
discount indexed by **how long it has been since the last discovery**. Three variants (eqs. 16–18):

    LORD 1:  α_i = γ_i w_0                 (i ≤ first discovery)
             α_i = γ_{i−τ_i} b_0           (after it)
    LORD 2:  α_i = γ_i (w_0 + Σ_{ℓ∈T(i)} γ_{i−ℓ} b_0)
    LORD 3:  α_i = γ_{i−τ_i} W(τ_i)        (last discovery time and the wealth at it)

Lemma 2.4: all three are GAI rules; **LORD 1 and LORD 2 are monotone, LORD 3 is not** (without extra
conditions on `γ`).

**SAFFRON** adds adaptivity, and the companion paper's own one-line placement is the clearest
summary: *"Storey-BH is to BH as SAFFRON is to LORD."* Both LORD and BH rest on a crude upper bound
on the false-discovery proportion; both Storey-BH and SAFFRON estimate instead. SAFFRON introduces a
threshold `λ` (default 1/2) and calls `p_j ≤ λ` a *candidate*; it never rejects a p-value above `λ`,
and — the mechanism that matters most here — **it loses no wealth when testing a candidate**, paying
only for the non-candidates. Its estimator replaces LORD's `Σ_{j≤t} α_j` with
`Σ α_j·1{p_j > λ_j}/(1−λ_j)`, which has unit expectation under a uniform null and a much smaller
one under a strong alternative.

## Construction recipe

**The FDR guarantee** (JM Theorem 3.1). If the null p-values are independent (of each other and of
the non-nulls), then **any monotone GAI rule with `w_0 + b_0 ≤ α` has `sup_n FDR(n) ≤ α`.** By
Lemma 2.4 this covers LORD 1 and LORD 2; LORD 3 is not covered directly, though the paper reports it
controls FDR empirically and uses it for all its own experiments. Remark 3.3 gives the sharper
statement `FDR(n) ≤ b_0·E[R(n)/(R(n)∨1)] + w_0·E[1/(R(n)∨1)]`, i.e. **FDR ≈ b_0 once discoveries are
many** — which is the regime this lab is not in.

**The criterion ladder.** Three different objects are controlled by the same class at different
parameterisations, and the choice is a power/strength trade:

    mFDR_{w0/b0}(n) = E[V]/(E[R] + w0/b0) ≤ b0      (Aharoni–Rosset; ratio of expectations)
    sFDR_{w0/b0}(n) = E[V/(R + w0/b0)]     ≤ b0      (JM Theorem 3.4; expectation of a ratio)
    FDR(n)          = E[V/(R ∨ 1)]         ≤ α = w0 + b0   (JM Theorem 3.1)

So mFDR/sFDR control permits `b_0 = α` (more wealth, more power) while FDR control forces
`w_0 + b_0 ≤ α`. The paper tested whether that extra power is worth the weaker criterion and reports
the honest answer: *"the gain in statistical power that is obtained from these criteria, rather than
FDR, is somewhat marginal"*, and Remark 3.5 shows Theorems 3.1/3.4 cannot be substantially improved.

**The default `γ` sequence**, which is the one piece of this that is a *recipe* rather than a
theorem. Proposition 4.2 characterises the power-optimising sequence under a mixture model; the
concrete choice used throughout and recommended since is

    γ_m = C · log(m ∨ 2) / (m · exp(√(log m))),     C ≈ 0.07720838 so that Σγ_m = 1

with `w_0 = 0.005`, `b_0 = 0.045` at `α = 0.05`. (Independently re-derived here over `m ≤ 2×10⁶`:
`C ≈ 0.0772` as printed, so the published constant checks out; truncating the tail makes a
re-computed `C` marginally too large.) Theorem 4.1 lower-bounds LORD's average power by
`Σ_m Π_{ℓ≤m}(1 − G(b_0 γ_ℓ))` under the mixture model, and that bound is *exact* for a slightly
weaker rule that resets the potential to `b_0` after each discovery — so it is **accurate precisely
when discoveries are rare**, which is the lab's regime.

**The dependency variant, and the price** (JM Example 3.8, from Theorem 3.7). This is the part that
matters most for a lab whose candidates share one validation window. Replace the "time since last
discovery" index with a discount on the **total** number of hypotheses tested:

    α_i = ξ_i · W(τ_i),    and FDR ≤ α under ARBITRARY dependence
    provided   Σ_i ξ_i (1 + log i) ≤ α / b_0

The `(1 + log i)` factor is the whole cost of giving up independence — a sibling of
Benjamini–Yekutieli's harmonic `Σ 1/i` penalty, and much cheaper than it. Worked at `b_0 = 0.045`,
`α = 0.05` with `ξ_i = K i^{−3/2}`: the budget `Σ(1+log i)/i^{3/2} = 6.4528` gives `K = 0.1722`, so
the available level is `1.7×10⁻¹` of the wealth at the first trial after a discovery (`α_1 ≈ 7.7×10⁻³`,
one-sided `z = 2.42`), falling to `2.5×10⁻⁴` (`z = 3.49`) by the tenth and `1.5×10⁻⁶` (`z = 4.67`) by
the three-hundredth. The log factor itself costs a factor 3.3 at `i = 10` and 5.6 at `i = 100`.

**FDX, and why the naive version of it is wrong** (JM §6). Controlling `sup_n FDX_γ(n)` is *not* the
right online generalisation: the paper's cartoon counterexample has `FDP(n) = 1/2` with probability
`α` independently at each `n`, so the sup of the pointwise criterion is `≤ α` while `FDP = 1/2`
infinitely often. The right object puts the quantifier inside:
`FDX_γ = sup_θ P(sup_n FDP^θ(n) ≥ γ)`. (This is the same quantifier-placement move as
`notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md`'s anytime-valid MCS, and the
second time this folder has met it in two sessions.)

## Robustness evidence (qualitative only)

Theorems with proofs, so the usual sample axes are inapplicable; the evidence that bears on *use* is
the simulation and the follow-up literature.

**The finding that should change how any FDR number here is read.** Controlling the *mean* of the
false-discovery proportion says remarkably little about its realisation at this scale. In JM's
experiment (n = 1,000 hypotheses, 30,000 replications, all rules controlling FDR at 0.05), *"the
actual false discovery proportion ... has a very broad distribution"*, and for α-investing at
truncation `T = 0.9`, **`FDP` exceeds 0.15 — three times the nominal level — with probability 0.13**.
Reducing the test levels narrows the spread (eq. 39 gives the conditional variance
`(b_0 − ψ_j − 1)²α_j(1−α_j)`) at a direct cost in power, and the paper says adjusting the truncation
to hit a target `FDX` is *"highly nontrivial"* — which is why the supLORD rule exists (see
`notes/2026-10-29-online-multiple-testing-practical-guidance.md` §5.1.5).

**Power ordering, reported consistently by two independent groups.** JM find LORD *"particularly
effective for small `π₁`"* — i.e. when the non-null fraction is small — while *"standard alpha
investing suffers a loss of power for large `π₁`"*, attributed to the `ϕ_j = α_j/(1−α_j)` charge
making the rule effectively stop after many discoveries. The SAFFRON authors re-confirm it:
*"alpha-investing seems less powerful than the non-adaptive algorithm LORD (and LORD++)."* The two
papers also agree on where SAFFRON's adaptive gain lives: *"Experiments indicate that increasing the
fraction of non-null hypotheses allows SAFFRON to achieve a faster increase of power than LORD"*, and
SAFFRON is expected to behave *more conservatively* than LORD at a shared `γ` because it only pays on
non-candidates. Chen and Arias-Castro (cited by the review, not read here) are reported to show LORD
is asymptotically optimal in a Gaussian model — as powerful as BH to first order.

A third-party confirmation worth recording as a pointer rather than a claim: *"Online false discovery
rate control for LORD++ and SAFFRON under positive, local dependence"*, **Biometrical Journal**,
2023, `10.1002/bimj.202300177` (2 Crossref cites, checked 2026-10-29) — found while resolving
citations, not read.

## Implementability here

**Pre-committed criterion, second clause first.** The [2026-10-28] entry demanded `O(1)` state in the
number of hypotheses *already tested* and an ex-ante computable spend. Verdict by rule:

| rule | state carried | `O(1)` in hypotheses tested? | level set before the test? |
|---|---|---|---|
| LORD 1 | `τ_i`, plus whether the first discovery has happened | **yes** | yes |
| LORD 2 | all past discovery times | yes in hypotheses, `O(#discoveries)` | yes |
| LORD 3 | `(τ_i, W(τ_i))` | **yes** | yes |
| modified LORD (Example 3.8) | `(W(τ_i), i)` | **yes** | yes |
| SAFFRON | rejection times `τ_j` and candidate counts `C_j⁺` since each | yes in hypotheses, `O(#discoveries)` | yes |

So the vein **admits**, and the abandonment condition ("needs the whole history of p-values
re-examined at each step") is met by none of them. Note the precise reading that makes this work: every
rule here carries state that grows with the number of **discoveries**, never with the number of
hypotheses — and this lab has seven promotions in its whole history, so the state is a handful of
numbers either way. **LORD 1 is the member to prefer**: it is the only one that is both `O(1)` *and*
covered by the FDR theorem, since LORD 3 — the variant JM themselves use — is not provably monotone.

**Which variant this lab would actually need, and it is not the headline one.** The lab's trials are
**not independent**: eight candidates per night are measured on one 2018–2023 window, and
`program.md` records that the deflator clusters 109 recorded trials into **36 effective** ones. The
independence hypothesis of Theorem 3.1 therefore fails on the lab's own measurement, which rules out
LORD 1/LORD++ as stated and sends the lab to **Example 3.8's modified LORD**: discount by the total
number of hypotheses tested, not by the time since the last discovery, and respect
`Σ ξ_i (1 + log i) ≤ α/b_0`. That is the honest rule here, and its arithmetic above says the required
one-sided `z` is past 3.5 by the tenth trial.

**What the numbers say the vein is worth.** Against
`notes/2026-10-28-argmin-inference-minimax-separation-rate.md`'s detection floor (`|t| ≈ 2.80` at
`τ = 50`) and `program.md`'s record that no promotion here has cleared `|t| = 2`, every level computed
above is **unreachable**. The conclusion is the same as the α-investing note's and is reinforced by a
second, independent route: adopt the accounting as a **diary**, never as a gate.

**Three things that transfer whether or not any wealth is ever tracked.**

1. *The adaptive rule buys nothing in this lab's regime, and both source groups say why.* SAFFRON's
   gain requires a significant fraction of non-nulls with strong signals, and it pays on every
   non-candidate. In a lab where most candidates have **negative** measured skill, nearly every trial
   is a non-candidate at `λ = 1/2`, so SAFFRON pays on nearly every trial and reduces to LORD. **Do
   not reach for the adaptive variant here** — and note this is the opposite conclusion to the FWER
   side, where the *discarding* mechanism does pay precisely because the nulls are conservative
   (`notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md`). Adaptivity to the non-null
   *fraction* is worthless here; adaptivity to null *conservativeness* is not. They are different
   mechanisms and SAFFRON only has the first.
2. *A controlled mean FDR is not a controlled realised FDP, and at seven discoveries the gap is the
   whole story.* `FDP` three times nominal with probability 0.13 was measured at a thousand
   hypotheses and many discoveries; with `R` in single digits the proportion is a coarse ratio whose
   variance dominates. Any future statement of the form "this lab's false-discovery proportion is
   about X" needs the `FDX`-style quantifier, not the FDR-style mean.
3. *The quantifier-placement lesson now has two instances in two sessions.* JM's `sup_n` cartoon and
   the anytime-valid MCS of `notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md` are
   the same error and the same fix. **Free prediction rule:** when a criterion is extended from a
   fixed horizon to a stream, check whether the paper moved the quantifier inside the probability or
   merely took a supremum of pointwise guarantees — the second is almost always the wrong object, and
   it is cheap to check before reading further.

**Pitfalls.** (a) LORD 3 is the variant most papers mean by "LORD" and it is **not** provably
monotone, so a result quoted for "LORD" may be an empirical claim rather than a theorem — check which
variant. (b) `w_0 + b_0 ≤ α` is required for FDR; relaxing to `b_0 = α` silently downgrades the
guarantee to mFDR/sFDR, for a power gain the authors call marginal. (c) The `γ` sequence's
normalising constant depends on summing to infinity; a truncated sum gives a `C` that is too large
and a budget that is overspent. (d) Example 3.8's dependency bound holds for *arbitrary* dependence,
which is pessimistic; the realistic structure here is **local** dependence (within a night, within a
family), and the rules built for that are in the next two notes.

## Related

- `notes/2026-10-29-alpha-investing-sequential-error-budget.md` — the rule this generalises, and the
  mFDR/FDR equivalence at a fixed number of rejections.
- `notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md` — the discarding mechanism that
  makes a decisive reject cost nothing, and the local-dependence treatment.
- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — LORD++ in closed form, the
  `supLORD` FDX rule, and the field's own small-`T` caveat.
- `notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md` — the same quantifier move on
  a different object.
- `notes/2026-09-16-clustering-trials-onc-effective-number-of-trials.md` and
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md` — the lab's existing
  dependence-correction layer, which this prices differently.
