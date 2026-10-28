---
title: "Sequential model confidence sets" — a confidence set for the best model that may be looked at after every new observation without losing its guarantee, built from e-processes and Ville's inequality; plus the measured price of re-looking at an ordinary model confidence set instead
authors: Arnold, Gavrilopoulos, Schulz, Ziegel
year: 2026
venue: Journal of the Royal Statistical Society Series B 0(0) (venue tier 1 — one of statistics' flagship journals; refereed, with three anonymous referees acknowledged)
url: https://doi.org/10.1093/jrsssb/qkag066
citations: 1 (Crossref `is-referenced-by-count`, checked 2026-10-28). Essentially uncited: the article was published in 2026 and the count carries no information yet, which is why the tier below is B and not A despite the venue.
sample_period: none for the theory. Two non-financial case studies (an epidemiological forecast hub and a numerical-weather post-processing exercise) and three simulations. **No market data of any period, and no dated outcome from either case study is recorded below.**
markets: none
tier: B
validation_overlap: false
published_post_2018: true
read: full text of `arxiv.org/pdf/2404.18678` (v4, dated 22 January 2026 — the version matching the published article) on the first try (1.4 MB → 132 KB of clean text via `pdftotext -layout`, 593 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). Sections 1–6, Supplement C and the discussion read in full; Supplements E–H skimmed for the statements relied on. Reference implementation in R at `github.com/GGavrilos/SMCS` (named by the paper; not fetched — this agent does not run code).
---

## Mechanism

No economic mechanism. The mechanism is **inferential**, and it is the one defect of the previous two
notes' object: a model confidence set is computed from a fixed sample, once. The authors' framing of
why that is the wrong shape:

> they presuppose a fixed sample size which stands in contrast to the fact that model selection and
> forecast evaluation are inherently sequential tasks where we successively collect new data and where
> the decision to continue or conclude a study may depend on the previous outcomes.

A **sequential** model confidence set (SMCS) for a target sequence `(M*_t)` at level `α` is a sequence
of sets with

    Q( ∃ t ≥ 1 : M*_t ⊄ M̂_t )  ≤  α        equivalently    Q( ∀ t ≥ 1 : M*_t ⊆ M̂_t ) ≥ 1 − α

and the paper is emphatic that the quantifier's position is the content: this "is a much stronger
requirement than assuming `Q(M*_t ⊆ M̂_t) ≥ 1−α` for all `t`". A fixed-sample set re-examined after
every new observation has the weaker property at each `t` and no control at all over the maximum.

**Three graded notions of "best", and choosing among them is a modelling decision the lab has to make
explicitly.** With `d_{ij,t} = L_{i,t} − L_{j,t}`, `µ_{ij,t} = E(d_{ij,t} | F_{t−1})` and
`∆_{ij,t} = (1/t)Σ_{s≤t} µ_{ij,s}`:

| target | definition | when it is the right question |
|---|---|---|
| strongly superior `M^{s,*}` | `µ_{ij,t} ≤ 0` a.s. for all `j`, all `t` | losses i.i.d., or nested information sets; this is Diebold–Mariano's and Hansen–Lunde–Nason's implicit target |
| uniformly weakly superior `M^{uw,*}` | `∆_{ij,t} ≤ 0` a.s. for all `j`, all `t` | better on *average* always, but not every period |
| weakly superior `M^{w,*}_t` | `∆_{ij,t} ≤ 0` a.s. for all `j`, at this `t` | relative performance may change over time |

`M^{s,*} ⊆ M^{uw,*} ⊆ M^{w,*}_t`; the first two **may be empty** while `M^{w,*}_t` never is. The
paper's argument for not defaulting to the strongest: a forecaster that is ideal on most days and
slightly worse on one weekday would be *excluded* by any powerful monitor of the strong hypothesis,
while being superior under the uniformly weak one.

## Construction recipe

**The primitive.** A *test supermartingale* for a hypothesis `H` is a non-negative process `(M_t)`
with `M₀ ≤ 1` that is a supermartingale under every `Q ∈ H`; its value is the wealth of a gambler
betting against the null. **Ville's inequality** (1939) is the whole foundation:

    sup_{Q ∈ H}  Q( ∃ t ∈ N : M_t ≥ 1/α )  ≤  α

so `ψ_t = 1{M_t ≥ 1/α}` is a valid sequential test at any stopping time — no correction for the number
of looks, because the bound is already over all `t`. An *e-process* is the weaker object that suffices:
a non-negative adapted `(E_t)` with `E_Q(E_τ) ≤ 1` for every (possibly infinite) stopping time `τ`,
equivalently one upper-bounded by a test supermartingale that may differ per `Q ∈ H`. Ville's
inequality still holds. A `(1−α)` **confidence sequence** for `(θ_t)` is a sequence of sets with
`Q(∀t : θ_t ∈ C_t) ≥ 1 − α` — a confidence interval whose coverage is time-uniform.

**The multiple-testing layer** (Theorem 3.1). Build an e-process `E_{ij,t}` per ordered pair for the
pairwise hypothesis; average over `j` to get `E_{i·,t} = (1/(m−1)) Σ_{j≠i} E_{ij,t}`, an e-process for
the intersection `∩_{j≠i} H_{ij}`; then adjust by the closure principle with the arithmetic mean as
e-merging function,

    E*_{i·,t} = min_{ I ⊆ {1..m}, i ∈ I }  (1/|I|) Σ_{j ∈ I} E_{j·,t}        (eq. 6)

and define `M̂_t = { i : E*_{i·,t} < 1/α }` (eq. 7). This is an SMCS for the strongly or uniformly
weakly superior set, **and so is its running intersection** `M̃_t = ∩_{r ≤ t} M̂_r`. Vovk–Wang's
Algorithm 1 computes the minimum in `O(m²)`; the supplement improves it to `O(m log m)`. Two facts
about the power ceiling: the arithmetic mean "essentially dominates all other symmetric e-merging
functions" (Vovk–Wang Prop. 3.1), so the conservatism is not a merge-function choice; and adjusting
the *pairwise* e-processes directly instead of the per-model ones gives a uniformly **less** powerful
test.

**The concrete e-processes.** Assume conditionally bounded loss differences `|d_{ij,t}| ≤ c_{ij,t}/2`
for a *predictable* `(c_{ij,t})`. Then (Proposition 3.2) the betting product

    E_{ij,t} = Π_{r ≤ t} ( 1 + λ_{ij,r} · d_{ij,r} ),       0 ≤ λ_{ij,t} ≤ 1/c_{ij,t}  predictable

is an e-process for the strong hypothesis — one line of arithmetic per day per pair. For the uniformly
weak hypothesis and uniform bounds `|d_{ij,t}| ≤ c_{ij}/2`, Proposition 3.3 (due to Choe–Ramdas 2023)
gives the exponential form `E_{ij,t} = exp{ λ_{ij} t ∆̂_{ij,t} − ψ_{E,c_{ij}}(λ_{ij}) V_{ij,t} }` with
`ψ_{E,c}(λ) = (−log(1−cλ) − cλ)/c²` and empirical-variance process
`V_{ij,t} = Σ_{r≤t}(d_{ij,r} − γ_{ij,r})²` for a predictable `γ`. For the **weakly** superior target,
Section 3.3 builds instead a time-uniform confidence region for the matrix `∆_t` from a test
supermartingale `M_t(X) = (1/(m(m−1))) Σ_{i≠j} M_{ij,t}(x_{ij})`, takes
`C_t = {X : M_t(X) ≤ 1/α}`, and excludes `i` when no feasible `X ∈ C_t` has `x_{ij} ≤ 0` for some `j`
(eq. 9, Theorem 3.4); Proposition 3.5 shows `C_t` is a convex upper set when the `M_{ij,t}(·)` are
convex and decreasing, which reduces the feasibility check to the boundary `x_{ij} = 0` (eq. 10), and
Proposition 3.6 supplies qualifying supermartingales. This route is "much more expensive
computationally", so the paper uses Theorem 3.1 for the uniformly weak target and reserves the
confidence-sequence machinery for the weak one.

**Turning conditional bounds into uniform ones, and the cost of doing so** (Section 3.4). Set
`d̃_{ij,t} = d_{ij,t}/c_{ij,t}`, which is bounded by `1/2` by construction. But the superior set is then
defined on the rescaled differences, `∆̃_{ij,t} = (1/t) Σ_r µ_{ij,r}/c_{ij,r}` — **the transformation
changes what "best" means**, from best in raw loss to best in loss-per-unit-of-predicted-scale. That is
a substantive reinterpretation, not a normalisation, and the paper says so.

**Betting scheme.** Following Waudby-Smith–Ramdas, predictable `λ_{ij,t}` beats the method of mixtures
for the strong hypothesis; for the weak hypotheses mixtures gave no significant power gain over a fixed
`λ_{ij}`, so the authors recommend using the e-processes directly. Simulation 1 simply takes
`λ_{ij,t} = (2c_{ij})^{−1}`.

## Robustness evidence (qualitative only)

Peer-reviewed at a tier-1 statistics journal; the guarantees are non-asymptotic and distribution-free
given the boundedness condition, so there is no sample or market to be robust across. The components
are independently established (Ville 1939; Howard–Ramdas–McAuliffe–Sekhon on confidence sequences;
Vovk–Wang on e-merging; Choe–Ramdas on sequential forecaster comparison; Marcus–Peritz–Gabriel's
closure principle), which is the relevant analogue of replication for a construction paper.

**Two measured numbers, and they are the honest frame for the whole vein.** In a simulation with
`m = 49` candidates whose best is a singleton: the SMCS **never wrongly excludes the best model** in
1,000 runs — i.e. it is conservative — and its average size at `t = 1000` is **8.41** of 49 (9.95 in a
second design). Running the *ordinary* MCS over the same sequential design, "although its size is
generally better than that of the SMCSs, **the coverage rate drops below the nominal level `1−α = 0.9`
to about `0.8`**". So the price of repeatedly looking at a fixed-sample set is roughly a doubling of
the error rate, and the price of fixing it is a set about six times larger than the truth.

**Stated limitations, from the discussion.** The main constructions assume (conditionally) bounded
score differences, and "important loss functions such as the squared error or the logarithmic score do
not satisfy this requirement" — a squared-error treatment is given in a supplement, but the authors
call for further work. Coverage is uniform over models (`P(Θ ⊆ Θ̂)`); the marginal/pointwise guarantee
of the argmin literature needs the adaptation in their Supplement D, and a time-uniform FDR version is
only sketched (Supplement E), with the explicit warning that FDR "fundamentally changes the type of
validity".

## Implementability here

**First, the axis correction, because getting this wrong would make the note useless.** The SMCS's `t`
indexes **new observations arriving over time** with a candidate set fixed in advance. The lab's
validation board grows along the *other* axis: the 2018–2023 window is fixed at ~1,510 days while the
number of recorded trials rises every night. Time-uniformity does not address a growing `m`; that is
`notes/2026-10-28-argmin-inference-minimax-separation-rate.md`'s problem and its answer there is
`α/d`-style correction, not a martingale. **So this note's construction is not the fix for
`rank_trials.py`.**

Where it *is* exactly the right object is the lab's other board: the **incubation / forward-scoring
track**. `strategies/incubating/` freezes a candidate at registration and `experiments/incubation.jsonl`
accumulates its post-registration returns as new days arrive — a fixed roster, data arriving in
sequence, and a monitor that is looked at repeatedly. That is the SMCS's setting precisely, and it is
also the setting in which a fixed-sample procedure's coverage degrades from 0.9 to 0.8 by the paper's
own measurement. (I have not read `experiments/incubation.jsonl` or `reports/incubation.md` — both are
on this agent's and the strategy agent's forbidden list — so this is a statement about the mechanism
`CLAUDE.md` and `program.md` document, not about any number in it.)

Concretely, and all of it free:

1. **Losses.** `L_{i,t} = −(r_{i,t} − r_{pool,t})` for each frozen candidate `i` on each new day `t`,
   so `d_{ij,t}` is the daily difference of two candidates' active returns. The pool belongs in `M₀`
   as a candidate, for the reason given in the MCS note: then "the pool is still in the set" is the
   readable statement of "no incubating candidate has yet shown itself better than the benchmark".
2. **Predictable bound.** Proposition 3.2 needs `|d_{ij,t}| ≤ c_{ij,t}/2` with `c_{ij,t}` predictable.
   A trailing-volatility cap on the pairwise daily difference, computed from information through
   `t−1`, satisfies this and is the same discipline the protocol's causality check already enforces —
   so the construction's one awkward requirement happens to be something this lab is already built to
   do. Then `λ_{ij,t} = 1/(2 c_{ij,t})`.
3. **Which target.** The lab's own records argue against the strong hypothesis: `learnings.md` has a
   signal whose sign **inverts across train sub-periods** (the CIV-beta entry) and a phase table whose
   spread exceeds its effect (2026-10-27/28). Under the strong target, a candidate that is better on
   average but worse in one regime gets excluded; under the weak target it does not, and the paper's
   weather case study is the demonstration that models excluded early can legitimately re-enter later.
   **A board that can never re-admit a candidate is asserting stationarity.** The cost of the weak
   target is the expensive confidence-sequence route; the uniformly weak target via Theorem 3.1 is the
   cheap middle and is probably where to start.
4. **Expect a wide set and do not read that as failure.** 8.41 of 49 against a singleton truth, with
   the merge function already at its power ceiling. This is the same message as HLN's "we view this as
   a strength" and the same message as the minimax lower bound in the companion note, now arriving
   from a third direction. Three independent literatures agreeing that the honest answer is a wide set
   is the most robust finding of this session.

**Pitfalls, in order of how likely they are to bite.**
- **`M₀` must be fixed before the first look.** The closure principle in eq. (6) is over subsets of
  `M₀`, so admitting a new candidate to the roster mid-stream breaks the guarantee. On an incubation
  board that gains members this is the binding constraint. Two legitimate options: pre-reserve a roster
  size (paying the `|I|` factor for slots not yet used), or restart the monitor when the roster changes
  and accept that the guarantee is per-cohort. The time-uniform **FDR** direction the paper sketches is
  the principled fix, and it is not yet available.
- **The rescaling in Section 3.4 changes the target.** If a volatility cap is used to get uniform
  bounds, the set is a set of candidates best *per unit of predicted scale*, which is a different —
  arguably better, but different — question from best in raw active return. Say which one a board
  answers.
- **Conservatism is structural**, not a tuning failure; do not reach for a cleverer merge.
- **No part of this reads holdout**, scores a candidate, or spends a trial against the deflated bar. It
  is a monitor over returns the engine already writes.

## Related

- `notes/2026-10-28-model-confidence-set-the-set-valued-ranking.md` — the fixed-sample procedure this
  extends, and the source of the 0.9 → 0.8 comparison.
- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — the other axis (`d` growing on fixed
  data) and the lower bound that says a wide set is unavoidable at this window length.
- `notes/2026-10-19-consistent-scoring-functions-and-elicitability.md` — the paper's own supplement
  insists the loss be a proper scoring rule / consistent scoring function; that note is the prerequisite
  for choosing `L`.
- `notes/2026-10-22-breakdate-inference-unknown-timing.md`, `notes/2026-10-22-regime-switching-financial-markets.md` —
  the weak-versus-strong superiority choice is the same question those notes ask about parameter
  constancy, now asked about *relative* performance, where it is cheaper to answer because only the
  difference has to be stable.
- `notes/2026-10-21-knockoff-filter-fdr-control-vs-permutation.md` — the FDR-versus-FWER trade this
  paper's Remark 1 declines to make, and the reason (it changes what is being guaranteed).
- `CLAUDE.md` (the incubation table rows) and `program.md` §"The two tracks" — the board this applies to.
