---
title: "α-investing" — a forward-spent error budget for a stream of hypotheses: a scalar wealth that is charged for each test and *paid* on each rejection, with the criterion it controls (mFDR) provably equal to FDR exactly when the procedure stops after a fixed number of rejections
authors: Foster, Stine
year: 2008
venue: Journal of the Royal Statistical Society Series B 70(2), 429–444 (venue tier 1)
url: https://doi.org/10.1111/j.1467-9868.2007.00643.x
citations: 86 (Crossref `is-referenced-by-count`, checked 2026-10-29). Resolved first call by DOI; OpenAlex's free daily budget was already exhausted this session and Semantic Scholar 429'd on its non-DOI endpoints, so neither was spent here.
sample_period: n/a — a methods paper. Evidence is theorems plus simulations (spike-and-slab Gaussian means, m = 200 and 4,000 tests). **No market data, no financial sample, nothing after 2007.**
markets: none. The method is domain-free; its stated applications are clinical endpoints and variable selection in regression.
tier: A
validation_overlap: false
published_post_2018: false
read: full text of the authors' **24 July 2007** version, 16 pp., from UPenn ScholarlyCommons DSpace 7 — record `repository.upenn.edu/handle/20.500.14332/47482`, bitstream `/server/api/core/bitstreams/8d0b6861-5058-46a1-999d-814be380e755/content` (249 KB → 72.8 KB of clean text via `pdftotext -layout`, 429 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). The record's second bitstream is a **JPEG thumbnail** — the 2026-10-10 `repository.arizona.edu` caution again. Numbering below (eqs. 8–17, Definitions 1–4, Lemmas 1–2, Theorems 2–3) is this version's; the JRSS-B version was not obtained (Wiley paywall) and the published numbering may differ. The draft carries **no "do not quote" notice** (checked, per the 2026-10-07 discipline). Sections read in full: 2 (criteria), 3 (investing rules), 4 (mFDR), 5 (uniform control), 6 (policies), 7 (discussion), and the Theorem-3 appendix proof.
---

## Mechanism

No economic mechanism — this is the **error-accounting layer**, and it is the first object this
folder has read that spends a type-I error budget *forward*, as candidates arrive, rather than
recomputing a correction backwards over the trials recorded so far. Every multiple-testing note in
this folder to date — `notes/2026-08-24-deflated-sharpe-ratio.md`,
`notes/2026-08-24-multiple-testing-haircut.md`,
`notes/2026-09-15-reality-check-max-statistic-under-dependence.md`,
`notes/2026-09-16-does-meff-control-the-familywise-error-rate.md` — is **fixed-sample and
retrospective**. This one is not, and a lab that adds one hypothesis per night is its canonical
setting.

The idea is an analogy made exact. Classical α-spending (Tukey, quoted in the paper: *"Once we have
spent this error rate, it is gone"*) splits a fixed α over a sequence of tests, which is Bonferroni
written sequentially and loses power as the sequence lengthens. α-investing changes one thing: **a
rejection pays into the budget.** Foster and Stine's own rewrite of Tukey is the whole mechanism —
*"Rules that invest the error rate wisely earn more for further tests."*

So the object carried forward is a scalar, the **alpha-wealth** `W(j) ≥ 0`, with `W(0) = α`
conventionally 0.05 or 0.10. Before testing `H_j` the rule names a level `α_j` it can afford; after
the test,

    W(j) − W(j−1) = +ω            if p_j ≤ α_j   (a rejection: pay-out ω < 1)
                  = −α_j/(1−α_j)  if p_j > α_j   (slightly more than α-spending charges)

Under a true null with uniform `p_j`, the expected change is `−(1−ω)α_j < 0`: testing a null costs
wealth in expectation, and the rule must keep `W` non-negative, which is what bounds the error.

The criterion this controls is **not** FDR but `mFDR_η`, a ratio of expectations rather than the
expectation of a ratio (Definition 1, eq. 11):

    mFDR_η(m) = sup_θ  E_θ[V^θ(m)] / (E_θ[R(m)] + η),   typically η = 1 − α

`V` counts false rejections, `R` all rejections. The paper concedes the weakness in as many words —
*"mFDR does not control a property of the realized sequence of tests; instead it controls a ratio of
expectations"* — and compensates with **uniform** control: mFDR is held at `α` at *every* rejection
and at every stopping time (Definitions 2–3), not merely at a horizon fixed in advance.

## Construction recipe

**The rule.** An α-investing rule is a function `α_j = I_{W(0)}({R_1,…,R_{j−1}})` of the initial
wealth and the **prior rejection indicators only** (eq. 7). It is not a function of past p-values,
past z-scores or past estimates, and the paper is explicit about why that matters: *"Because neither
the payout ω nor the cost α/(1−α) reveals p_j (other than to indicate if p_j ≤ α_j), subsequent tests
need only condition on the sequence of rejections, R_1,…,R_j."* The validity condition on the tests
(eq. 10) is correspondingly weak — `E_θ(V_j^θ | R_{j−1},…,R_1) ≤ α_j` — and **the tests need not be
independent**, because the proof runs through optional stopping on a sub-martingale rather than
through a dependence assumption.

**The guarantee** (Theorem 3). An α-investing rule governed by the wealth update above with
`W(0) ≤ αη` and pay-out `ω ≤ α` controls `mFDR_η` at level `α`, at every finite stopping time. The
proof (appendix, Lemma 2) shows `A(j) ≡ αR(j) − V^θ(j) + ηα − W(j)` is a sub-martingale and applies
optional stopping. With `η = 1 − α` this also gives **weak FWER control at α**, because under the
complete null `mFDR_{1−α}(m) ≤ α` implies `E_θ[V^θ(m)] ≤ α`.

**Two concrete rules.** Following a rejection at `k*`, invest heavily and decay quadratically
(eq. 9): `α_j = W(j−1)/(1 + j − k*)`, which puts half the current wealth on the test right after a
rejection. The *aggressive* version (eq. 15) additionally forces the wealth to be exhausted by a
known last hypothesis `m`: `α_j = W(j−1)·[1/(1+j−k*) ∨ 1/(1+m−j)]`.

**Policies, which the paper says matter more than the spending function.** (i) *Best-foot-forward*:
order the hypotheses so the ones most likely to be rejected come first, because their rejections fund
the rest. (ii) *Spending-rate*: be "thrifty" (never commit all current wealth) but do not hoard —
*"There is no reward for conserving alpha-wealth unused."* (iii) *Revisiting*: the **same hypothesis
may be tested more than once**, at a small level first and a larger one later, *"so long as subsequent
tests condition on prior outcomes"* — concretely, the second look's rejection region solves
`P_0(p_j ≤ p* | p_j > β_1) = (p* − β_1)/(1 − β_1) = β_2`. Nibbling this way reproduces step-down BH in
the limit as the nibbles go to zero. (iv) The alternative "regulator" (eq. 17),
`+ω + log(1−p_j)` on a rejection and `log(1−α_j)` otherwise, has the same expected pay-out but
**reveals `p_j`**, so the rule must then condition on the rejected p-values — a strictly heavier
bookkeeping requirement, and the paper flags it as awkward under dependence.

## Robustness evidence (qualitative only)

The result is a theorem with a martingale proof, not an empirical effect, so the rubric's sample
axes do not apply; what matters is how the follow-up literature has treated it. It has been
generalised twice in ways that confirm validity and bound power: Aharoni–Rosset's *generalized
α-investing* contains it as a special case, and Javanmard–Montanari
(`notes/2026-10-29-lord-online-fdr-and-the-dependency-price.md`) place it inside the same class and
prove **FDR** (not merely mFDR) control for the monotone members. Both of those papers, and
Ramdas et al.'s SAFFRON, report in simulation that **plain α-investing is less powerful than the
later non-adaptive LORD rules**, which the SAFFRON authors attribute to the `ϕ_j = α_j/(1−α_j)`
charge: the rule can effectively stop after many discoveries. So the honest summary is *valid, very
general, and superseded on power*.

Two further honesty points the paper makes itself. First, the criterion gap is real but closes in a
specific case — **Theorem 2**: if the procedure stops at the `r`-th rejection (`T_{R=r} < ∞` a.s.)
then `γ_R = σ_R/µ_R = 0` and

    FDR = mFDR_0 = cFDR = eFDR = pFDR = E[V^θ(r)]/r,     and   FDR ≤ α(r+2)/(r+1)

plus `Var(V^θ(r)) ≤ αr` and `P(V^θ(r) ≥ 1 + αr + k√r) ≤ e^{−k²/2}` for rules with `α = ω = W(0)`.
A bit of algebra (eq. 14) bounds `mFDR_0 − FDR` by terms in `γ_R`, so the two criteria are close
whenever the number of rejections has small coefficient of variation. Second, the contamination
hazard, stated in the Discussion and applying to *any* FDR-like procedure: if the stream is seeded
with trivially-false hypotheses — the paper's example is a first hypothesis claiming *"gravity does
not exist"* — then *"all subsequent tests are tainted"*, because the easy rejection manufactures
wealth. Step-down BH shares the defect (the first real hypothesis is tested at `2α/m` rather than
`α/m`).

## Implementability here

**This is bookkeeping, not a strategy, and the first thing to check is whether the bookkeeping is
even affordable.** On the criterion this folder pre-committed in the [2026-10-28] open-questions
entry — *admit the vein only if the first paper yields a rule whose state is `O(1)` in the number of
hypotheses already tested and whose per-trial spend is computable **before** the trial is run* —
α-investing **passes both clauses, cleanly**:

- *State.* The rule depends on the past only through the rejection indicators; under eq. 9 or eq. 15
  it depends only on `(W(j−1), k*)` — a float and an integer. Nothing like "re-examine the whole
  p-value history at each step" appears, which was the abandonment condition.
- *Ex-ante spend.* `α_j` is set **before** `p_j` is seen, by construction (eq. 7). The level for
  tomorrow night's candidate is computable tonight.

**What maps onto what.** One recorded trial = one hypothesis `H_j`. A `PROMOTE` = a rejection
`R_j = 1`. The lab already has the two things the rule needs: an ordered stream (nightly trials) and
a one-sided test statistic per trial (validation skill over the equal-weight pool with a paired
block-bootstrap error, per `program.md`). What it does not have is a p-value the rule may charge
against — the bootstrap gives an interval, and turning it into an honest one-sided p-value is a
protocol change, so **nothing here can be run without a human**. File it as accounting the lab could
adopt, not as a gate to switch on.

**The one number that decides whether this is a gate or a diary.** With the standard level schedule
and `α = 0.05`, the implied one-sided `z` a candidate must clear runs from about **2.6** (first trial,
or the trial right after a promotion) to about **4.0** after a hundred trials with no reward — the
arithmetic is worked in
`notes/2026-10-29-online-multiple-testing-practical-guidance.md`. Against that,
`notes/2026-10-28-argmin-inference-minimax-separation-rate.md` (`#323`) puts this lab's *detection*
floor at a full-window `|t|` of ≈ 2.80 at `τ = 50`, and `program.md` records that **no promotion in
this repo's history has ever cleared `|t| = 2` on validation**. So an α-investing gate would have
promoted nothing, ever. **Adopt it as a diary, not a gate**: a wealth column in the journal makes the
forward price of a trial explicit, which no artefact here currently does.

**Three findings that transfer regardless of whether the wealth is ever tracked.**

1. *A re-test of a refuted idea is legitimate, and the paper says exactly what makes it legitimate.*
   `CLAUDE.md` permits re-testing a refuted idea "unless you have a specific reason, which you must
   state". The *revisiting policy* supplies the validity condition: the second look is honest if it
   **conditions on the first look's non-rejection and nothing else** — the threshold solves
   `P_0(p ≤ p* | p > β_1) = β_2`. Which means the stated reason may not be *"its p-value was nearly
   there"*. Using the first look's *magnitude* to decide whether to look again is the one thing that
   voids the guarantee. (Independently confirmed in
   `notes/2026-10-29-online-multiple-testing-practical-guidance.md` §5.1.6.)
2. *Padding a roster with easy rejects is a measurable error, not just bad taste.* The gravity
   example is the scout track's hazard written in advance: a stream seeded with hypotheses certain to
   be rejected manufactures budget for the ones that follow. Under protocol v3, `FAMILY_LEAD` and
   `SCOUT` verdicts never face the champion comparison, so **only `PROMOTE` should ever be counted as
   a rejection** in any such accounting. A scout that trivially leads an empty family must not fund
   a later challenger.
3. *The criterion gap is not a gap at this lab's rate.* The usual objection to mFDR — that it is
   weaker than FDR — is formally right and practically void here. Under the complete null
   `FDR(m) = FWER(m)`, and by **Theorem 2** a procedure that stops at `r` rejections has
   `FDR = mFDR_0` exactly, with `FDR ≤ α(r+2)/(r+1)` — at `r = 1` that is `1.5α`. The lab makes
   roughly one promotion per several dozen trials and *stops the session the moment one happens*, so
   it lives in exactly the stopped-at-small-`r` regime where the weak criterion and the strong one
   coincide. This answers the harder half of the pre-committed criterion directly: **an FDR target is
   not the thing the vein buys. The error object the folder already has is the right one; what is new
   is the forward spending.**

**Pitfalls.** (a) The `η` convention matters: `η` near zero gives "a less satisfactory criterion",
and under the complete null no procedure can push `mFDR_0` below 1. (b) `W(0) ≤ αη` and `ω ≤ α` are
*conditions of the theorem*, not tuning knobs — at `α = 0.05, η = 0.95` the initial wealth is capped
at 0.0475. (c) Do not import the eq. 17 regulator for its extra power; it forces the rule to
condition on realised p-values, which is heavier bookkeeping and worse under dependence. (d) The
paper's power case rests on *ordering hypotheses well*, and it says honestly that *"it may be
difficult a priori to order the hypotheses in such a way that those most likely to be rejected come
first"* — for this lab that ordering is the nightly family allocation in `program.md`, chosen for
breadth rather than for probability of rejection, so the best-foot-forward power gain is **not**
available here and should not be assumed.

## Related

- `notes/2026-10-29-lord-online-fdr-and-the-dependency-price.md` — the generalisation that upgrades
  mFDR to FDR, prices dependence with a `log i` factor, and supersedes this rule on power.
- `notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md` — the FWER-side rules, and the
  mechanism (discarding) that makes a decisive reject *free*.
- `notes/2026-10-29-online-multiple-testing-practical-guidance.md` — the peer-reviewed synthesis, the
  level arithmetic for this lab, and the field's own caveat about small numbers of hypotheses.
- The fixed-sample layer this sits beside: `notes/2026-08-24-deflated-sharpe-ratio.md`,
  `notes/2026-08-24-multiple-testing-haircut.md`,
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md`,
  `notes/2026-09-16-clustering-trials-onc-effective-number-of-trials.md`.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — the `|t|` floor that decides this
  vein is a diary rather than a gate.
- Tension to carry, not to resolve here: `experiments/learnings.md` records "every trial raises the
  bar" and also that clustering makes within-family tuning "nearly free in deflation terms". The
  online accounting prices trials on a **different axis entirely** — where the p-value landed, not how
  correlated the trial was. See the implementability section of
  `notes/2026-10-29-online-fwer-and-discarding-conservative-nulls.md`.
