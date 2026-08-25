---
title: "False discovery control with p-value weighting; and Genome-wide significance levels and weighted hypothesis testing"
authors: Genovese, Roeder, Wasserman; Roeder, Wasserman
year: 2006; 2009
venue: Biometrika (tier 1 statistics); Statistical Science (tier 1 statistics)
url: https://doi.org/10.1093/biomet/93.3.509 ; https://doi.org/10.1214/09-STS289
citations: GRW 355 (Semantic Scholar, checked 2026-08-25; Crossref 231, OpenAlex 340). RW 130 (Semantic Scholar, checked 2026-08-25; Crossref 88)
sample_period: none — methodological. Theorems plus simulation on synthetic Normal(θ,1) designs; illustrative applications to genetic association data
markets: none — the application domain is genomics/fMRI, not finance
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the machinery session 11 went looking for and could not name: a **formal, frequentist
prior-weighted multiple-testing correction**. `SUMMARY.md`'s open question (c) recorded that both
multiple-testing literatures covered here gesture at it and decline it — Harvey–Liu–Zhu say "a factor
derived from a theory should have a lower hurdle than a factor discovered from a purely empirical
exercise" but offer no machinery, and the DSR authors' optimal-stopping aside simply assumes the
candidate set is already restricted to the "theoretically justifiable". The machinery exists, it is
twenty years old, and it lives in statistics rather than finance.

**The core object.** Assign each hypothesis a non-negative weight `W_i` chosen *before* seeing the
data, divide its p-value by its weight (`Q_i = P_i / W_i`), and run the ordinary Benjamini–Hochberg
procedure on the `Q`'s. Equivalently, hypothesis `i` is rejected when `P_i ≤ W_i · T` for a common
`T`: a weight above 1 is a **relaxed** threshold for that hypothesis, a weight below 1 a **stricter**
one. Weighting the p-value is deliberately *not* the same as weighting the loss (Benjamini–Hochberg
1997): under p-value weighting every false discovery still counts equally and the thresholds move;
under loss weighting the threshold is common and the errors count differently. The former is what
"a better-motivated hypothesis deserves an easier test" means formally.

**The theorem, and the budget that is the whole story.** GRW's Theorem 4.1: the weighted procedure
controls FDR at `α(1−a)μ₀`, where `μ₀ = E(W | H = 0)` is the mean weight on true nulls; if the
weights average one, FDR ≤ α. Roeder–Wasserman's Lemmas 2.1–2.2 give the same for family-wise error
under weighted Bonferroni and weighted Holm. The striking part, stated in their own words: **"aside
from this budget requirement, any set of nonnegative weights is valid."** Error control does not
depend on the weights being good, or informative, or even on their being related to the truth at all
— only on their being fixed a priori and averaging one.

That is the mechanism the folder needed, and its shape is worth stating baldly because it is not the
shape one would guess. **Prior-motivated discounting is not free; it is zero-sum.** Lowering the bar
for a candidate you have a reason to believe in is legitimate, and costs nothing in error control,
*only because* you have raised it by exactly as much, in total, on the candidates you do not believe
in. The budget is `mean(W) = 1`. There is no version of this in which a good prior buys a discount
out of thin air.

**Why the asymmetry pays.** Since the alternative's p-value distribution `F` is stochastically
smaller than uniform, up-weighting a true alternative gains more power than down-weighting another
true alternative loses ("power arbitrage" in GRW's phrasing). Hence the headline empirical result,
which both papers make in different ways: **informative weights buy a substantial power gain;
uninformative or even adversarially wrong weights cost very little.** GRW: "the loss of power is not
serious even if the weights are completely wrong". Roeder–Wasserman's Theorem 3.4 makes the worst
case precise — with minimum weight `b` and smallest above-one weight `B`, the worst-case gain
exceeds the worst-case loss whenever `Φ̄(z_{αB/m} − ξ) + Φ̄(z_{αb/m} − ξ) ≤ 2Φ̄(z_{α/m} − ξ)`, and as
`b → 1` the set of `ξ` where weighting hurts shrinks to measure zero.

Two economic readings of that robustness, both portable:

1. **The safe regime is sparse weighting.** Few large weights, and a minimum weight close to 1. If
   `ε` (the fraction receiving the large weight `B`) is small, `B` can be large with negligible loss:
   Roeder–Wasserman's Theorem 3.3 shows a turnaround point `B₀(ε)` exists and rises steeply as `ε`
   falls. Concretely, at `ε = 1/m` (up-weighting exactly one hypothesis), `w₁ ≈ B` and `w₀ ≈ 1`, and
   in the double limit the up-weighted hypothesis reaches power 1 while everything else keeps power
   1/2. **Betting the whole prior budget on one pre-named candidate is the robust play; spreading
   modest tilts over many is the fragile one.**
2. **The weights are unstable but the power is not.** Their Lemma 3.6 shows the optimal weight
   function is essentially a discontinuous function of the underlying effect vector — an arbitrarily
   small perturbation of the effect distribution can change an optimal weight by a factor of a
   thousand. That would be alarming if power tracked weights; it does not. This is the same
   estimate-versus-objective distinction the folder has recorded elsewhere (an unstable input feeding
   a flat objective).

## Construction recipe

**The procedure (GRW, wBH).**
1. Assign weights `W_i > 0` to each hypothesis such that `(1/m) Σ W_i = 1`. The weights must be
   chosen **before** the p-values are seen — formally, `W` is conditionally independent of `P` given
   `H`.
2. Compute `Q_i = P_i / W_i`.
3. Apply BH at level `α` to the `Q_i`. (An adaptive FDR procedure may be substituted for extra power.)

For exceedance control (`P{FDP > c} ≤ α`) rather than mean control, run weighted Bonferroni or
weighted Holm to get a family-wise rejection set `R₀`, then augment with up to `#(R₀)·c/(1−c)` extra
rejections. GRW's tuning note: **use a large weight ratio `r` for FDX control and a smaller one for
FDR control**, because the exceedance version is markedly more robust to bad weights.

**What the optimal weights look like** (Roeder–Wasserman Theorem 3.1, a special case of Spjøtvoll
1972, independently obtained by Rubin–Dudoit–van der Laan). Maximising average power subject to
`W ≥ 0` and `mean(W) = 1` gives a one-parameter family

```
ρ_c(ξ) = (m/α) · Φ̄( ξ/2 + c/ξ ) · I(ξ > 0),      c set so that mean(ρ_c) = 1
```

equivalently the test-specific cutoff `T_j > ξ_j/2 + c/ξ_j`. **This function is unimodal in `ξ`, not
monotone** — the argument `ξ/2 + c/ξ` is minimised at `ξ = √(2c)`, so the weight peaks at an
*intermediate* prior effect size and falls away on both sides. The reading is exact and useful:
down-weight the hopeless (too small to detect however hard you push) *and* the obvious (already
detected at weight one); spend the budget on the **marginal** hypotheses. Roeder–Wasserman formalise
"marginal" as the effect with power 1/2 at unit weight, `ξ₀ = z_{α/m}`, and recommend choosing the
weight scheme to be good there.

**Where weights may come from.** Two channels, with a hard boundary between them.
- *External weights* — prior information from outside the data being tested. This is the channel the
  theorems are about; it is prone to bias but the robustness results bound the damage.
- *Estimated weights* — from the data. Here the boundary: splitting the sample, estimating weights on
  one half and testing on the other, **does gain over unweighted testing of the second half but does
  not beat simply using the full data unweighted** (Rubin–Dudoit–van der Laan; corroborated by Skol
  et al.). Weights extracted from the same data you are testing are not a free lunch; the information
  has to come from outside.
- The one estimated scheme that does work is *grouped* and deliberately crude — the "sieve
  principle". Partition the tests into `K` groups of at least 20–30, fit a two-component mixture per
  group by method of moments to get `(π̂_k, ξ̂_k)`, weight the whole group by `w(ξ̂_k)`, smooth toward
  the average (`ŵ_k = (1−γ)w(ξ̂_k) + γ·mean`, with `γ ≈ 0.01–0.05`), and renormalise. It preserves
  error control because far fewer parameters are estimated than there are observations, so **a single
  lucky test cannot up-weight itself** — only its whole group can.

## Robustness evidence (qualitative only)

The FDR/FWER control results are theorems with proofs given in full (GRW §4, adapting
Benjamini–Yekutieli; Roeder–Wasserman §2), and cannot decay. The power results are asymptotic
expansions plus simulation over Normal(θ,1) alternative families across a range of alternative
prevalence and weight strength; GRW report FDR held at or below nominal in every configuration
simulated, with the weighted procedure conservative under informative weighting (Type I error rate
`μ₀t` falls below `t`). Both papers are in tier-1 statistics venues, are well cited for their age and
field, and the weighting idea has an independent lineage reaching back to Holm (1979), Spjøtvoll
(1972) and Benjamini–Hochberg (1997), with the optimal-cutoff result independently rediscovered by
Rubin–Dudoit–van der Laan. Neither paper is about finance, and neither models costs, dependence
across time, or anything resembling a portfolio; the transfer below is a transfer of *machinery*, not
of evidence.

One honest limit: GRW's FDR proof assumes independent p-values (with a remark that discreteness
weakens the key equality to an inequality); the family-wise results are distribution-free in the
dependence structure but Bonferroni/Holm-based and hence less powerful. A repo whose trials are
heavily correlated is in the regime where the independence assumption is least comfortable.

## Implementability here

**Explanatory and prescriptive-about-protocol only — nothing here can or should touch `engine/`.**
The promotion gate lives in a frozen file and its criterion is a human decision. What this note
supplies is the answer to a question the folder posed, plus one screen.

**1. The answer to open question 11(c), and it is not the answer the question expected.** A
prior-weighted correction exists and is rigorous, so "a theory-motivated candidate deserves an easier
test" is a formally defensible position rather than special pleading. But the machinery attaches two
conditions that the question did not anticipate, and both bite here:

- *The budget.* Discounts must be paid for. A protocol that lowers the bar for well-motivated
  candidates without raising it for the rest is not doing prior weighting; it is just lowering the
  bar. The lab currently has no mechanism that could spend such a budget — every trial faces the same
  deflated-Sharpe threshold — so the correct reading is that **this literature does not licence any
  session to treat its own hypothesis as pre-approved**. If anything it says the opposite: an
  unweighted protocol is the `W ≡ 1` special case, which is exactly the choice a lab makes when it
  declines to rank its own ideas in advance.
- *A priori.* The weights must be fixed before the data are seen. The lab's protocol already has the
  right shape here — `CLAUDE.md` requires the hypothesis to be written before the code — and that
  discipline is precisely what would make a weight admissible. What is missing is that the ranking is
  never *recorded* as a weight before the run, so nothing distinguishes a hypothesis-first trial from
  a post-hoc rationalisation in the trial log.

**2. A free screen, and it inverts a natural instinct.** The optimal weight function is unimodal.
If a session ever does rank its candidates by prior plausibility, the extra budget belongs on the
**plausible-but-marginal** idea — not on the one it is most confident about (already detectable at
unit weight, so the weight is wasted) and not on the speculative long shot (undetectable at any
weight this budget can buy). Applied to this repo's own record: the ideas worth a discount are the
ones landing *just* short of the bar for a stated mechanical reason, which is a description of
several entries in `learnings.md`.

**3. The boundary that closes the tempting shortcut.** Estimating weights by splitting the sample
does not beat using the whole sample unweighted. Any future proposal to derive a candidate's
"deserved" discount from the validation split itself — a pre-screen, a warm-up window, a first-half
fit — is refuted at the mechanism level by that result, and would in any case score returns and so
fall outside the holdings-only free-diagnostic exemption (session 6's item (c)).

**4. The one structural fact that transfers cleanly.** The sieve/grouped weighting scheme requires a
partition of the hypotheses into economically meaningful groups with ≥20–30 members each, and gets
its stability from the group being the unit. This repo *has* such a partition — `program.md`'s seven
strategy families — and `learnings.md` has independently observed that DSR clustering makes a tight
family behave like nearly one trial. Those are the same fact from two directions: within-family
correlation is what makes a family the natural unit of both deflation and weighting.

**Pitfalls.** (a) Do not read "any weights are valid" as "weights don't matter" — validity and power
are different claims, and the *validity* is what is unconditional. (b) The robustness results are
about *power*, in a Normal location model with independent tests; nothing here says a weighted
procedure is robust when applied to a correlated, cost-paying, sequentially-explored search like this
one. (c) The literature's `m` is thousands to millions of simultaneous tests; this repo's is dozens
of sequential ones, so quantitative recipes calibrated at `z_{α/m}` do not carry over — the shapes do.

## Related

- `notes/2026-08-24-multiple-testing-haircut.md` — Harvey–Liu's FDR-controlling haircut is the
  unweighted procedure this generalises, and is where the "a theory-derived factor should have a
  lower hurdle" quote sits without machinery attached. This note supplies the machinery.
- `notes/2026-08-24-deflated-sharpe-ratio.md` — the gate's own statistic. Note that DSR is a
  *single-threshold* framing: every candidate is compared against the same expected-maximum bar, so
  it is structurally the `W ≡ 1` case and has no slot for a prior. That is a fact about the gate, not
  a criticism of it, and the engine is frozen either way.
- `notes/2026-08-25-bayesianized-p-values-prior-odds.md` — the same question in Bayesian vocabulary
  and in a finance venue: prior odds times a minimum Bayes factor. Where this note gives the
  frequentist procedure that preserves error control, that one gives the closed-form threshold as a
  function of the prior — and finds the required threshold *rises* under any realistic finance prior.
- `notes/2026-08-25-hierarchical-bayesian-factor-replication.md` — the grouped/sieve idea realised
  empirically in finance: clusters of related strategies sharing an alpha component, with each
  member's estimate shrunk toward its cluster.
- `experiments/learnings.md` "every trial raises the bar" — session 11 corrected this once (it is an
  FWER property, not a law). This adds a second correction of a different kind: under a weighted
  scheme a trial's bar can be *lowered*, but only by raising another's.
