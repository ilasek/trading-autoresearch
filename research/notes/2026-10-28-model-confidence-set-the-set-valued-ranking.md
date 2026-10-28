---
title: "The Model Confidence Set" — a confidence interval for the identity of the best model: an elimination procedure whose surviving set contains every genuinely-best object with probability 1−α, and which is deliberately *large* when the data cannot separate the candidates
authors: Hansen, Lunde, Nason
year: 2011
venue: Econometrica 79(2), 453–497 (venue tier 1)
url: https://doi.org/10.3982/ECTA5771
citations: 2079 (Crossref `is-referenced-by-count`, checked 2026-10-28). Resolved on the first call; OpenAlex and Semantic Scholar were not spent on it.
sample_period: 1979Q1–2006Q4 for the Taylor-rule application; the inflation-forecast application follows Stock–Watson (1999) and uses that paper's design. Simulations are the main evidence. **No part of the sample reaches 2018.**
markets: none in the strategy sense — US macro series (inflation forecasts, federal funds rate). The method is domain-free and the paper's own framing is "objects evaluated in terms of a loss function".
tier: A
validation_overlap: false
published_post_2018: false
read: full text of **CREATES Research Paper 2010-76** (Aarhus University), the authors' own working-paper version of the Econometrica article, fetched from `repec.econ.au.dk/repec/creates/rp/10/rp10_76.pdf` on the first try (363 KB → 187 KB of clean text via `pdftotext -layout`, 681 instances of `" the "`, zero `( )` dropout, no ASCII shift, title line verified). Numbering below (Definitions 1–4, Assumptions 1–2, Theorems 1–4, Lemmas 1–2, Corollary 1) is this version's. **The Econometrica version was not obtained** — `econometricsociety.org` is paywalled with only the supplement free, and the Atlanta Fed working-paper path `atlantafed.org/-/media/documents/research/publications/wp/2005/wp0507a.pdf` returned **HTTP 200 with a 48 KB JavaScript body** (a new "looks like an answer" mode; see the session's access notes). The CREATES version carries the full theory, both applications and the bootstrap description.
---

## Mechanism

No economic mechanism. This is the **measurement layer of the lab's own board**, and the reason to
file it is that `scripts/rank_trials.py`'s docstring already uses this paper's name for what it
prints — "**tier 1 is the model confidence set** — the trials the data cannot separate from the best
at the 10% level" — while the folder had, before tonight, exactly **one** passing mention of the
object across 234 notes and no note on it.

The problem the paper solves is that standard practice picks one model by lowest loss and says
nothing about the uncertainty in that pick. The MCS replaces the point answer with a set. Its
governing idea, quoted because the lab's own board rests on it:

> The MCS acknowledges the limitations of the data, such that uninformative data yields a MCS with
> many models, whereas informative data yields a MCS with only a few models.

and, on the case where the elimination rule questions a good model before the bad ones are gone:

> The lack of power causes the procedure to terminate too early (on average), and the MCS will
> contain a large number of models, including several inferior models. **We view this as a strength
> of the MCS procedure.** Since lack of power is tied to the lack of information in the data, the MCS
> should be large when there is insufficient information to distinguish good and bad models.

A wide tier 1 is therefore the procedure working, not the procedure failing. That reading is the
single most useful thing this note carries into a strategy session.

## Construction recipe

**Objects and losses.** `m₀` candidates indexed by `M₀ = {1,…,m₀}`; `L_{i,t}` is candidate `i`'s loss
in period `t`, `t = 1,…,n`. Relative performance `d_{ij,t} = L_{i,t} − L_{j,t}` with
`µ_{ij} = E(d_{ij,t})` assumed finite and **independent of `t`**. Definition 1: the set of superior
objects is `M* = {i ∈ M₀ : µ_{ij} ≤ 0 for all j ∈ M₀}`.

**The algorithm** (Definition 2) needs two ingredients — an *equivalence test* `δ_M` of
`H_{0,M} : µ_{ij} = 0 for all i,j ∈ M`, and an *elimination rule* `e_M` naming which object to drop
when the test rejects:

    Step 0: M ← M₀
    Step 1: test H_{0,M} with δ_M at level α
    Step 2: if accepted, the MCS is M; otherwise drop e_M from M and go to Step 1

**Why this does not accumulate type-I error.** Assumption 1 asks only that (a) the test's asymptotic
size not exceed `α`, (b) its asymptotic power be one, and (c) `P(e_M ∈ M* | H_{A,M}) → 0`. Theorem 1
then gives `lim inf P(M* ⊂ MCS) ≥ 1 − α` and `P(i ∈ MCS) → 0` for every `i ∉ M*`. The paper's own
explanation of the mechanism is the part worth memorising: in the informative case the first time a
superior model is questioned is when the test is applied to `M*` itself, so one `α` covers the whole
run — "the sequential testing is halted when the first hypothesis is 'accepted'". Corollary 1: if
`M*` is a singleton, the MCS equals it with probability → 1.

**Coherency, for finite samples.** Theorem 2: if `P(δ_M = 1, e_M ∈ M*) ≤ α` *unconditionally*, the
`1−α` coverage holds in finite samples, not just asymptotically. Definition 3 makes that operational
as **coherency**, `P(δ_M = 1, e_M ∈ M*) ≤ P₀(δ_M = 1)` with `P₀` the measure obtained by imposing the
null via `d_{ij,t} ↦ d_{ij,t} − µ_{ij}`. Coherency forbids some test/elimination pairings, including
the most powerful test, and the paper's analogy is exact: an F-test can reject "all coefficients are
zero" while no individual `t` is significant, so a rejection need not identify a culprit — the
footnote puts it as "it is easier to conclude that a murder has taken place, than it is to determine
who committed the murder".

**MCS p-values.** The elimination rule induces a nested sequence `M₀ = M₁ ⊃ M₂ ⊃ … ⊃ M_{m₀}`.
Definition 4: the MCS p-value of the `j`-th eliminated model is `p̂ = max_{i ≤ j} P_{H_{0,M_i}}`, a
**running maximum** (with `P_{H_{0,M_{m₀}}} ≡ 1` by convention, since the last survivor is being
compared with itself). Theorem 3 makes the useful consequence hold: model `i` is in the `1−α` MCS if
and only if `p̂_i ≥ α`. So every candidate gets one number, and the set is read off a threshold
rather than re-running the algorithm per `α`.

**Which test statistic.** Assumption 2 is the regularity condition: `E|d_{ij,t}|^{r+γ} < ∞` for some
`r > 2`, `γ > 0`, and `{d_{ij,t}}` strictly stationary with positive variance and `α`-mixing of order
`−r/(r−2)`. Note carefully what it restricts — *the differences, not the losses*: "a loss function
need not be stationary as long as the loss differentials satisfy Assumption 2 … allows for some types
of structural breaks and other features that can create non-stationary `{L_{i,t}}`, as long as all
objects in `M₀` are affected in a 'similar' way".

Three statistics, with `d̄_{ij}` the sample mean difference and `d̄_{i·} = L̄_i − L̄_·` the loss of `i`
relative to the **average across the models currently in `M`**:

| statistic | form | when |
|---|---|---|
| `T_Q` | `n X̄' Σ̂^# X̄` on `m−1` contrasts, `χ²_q` with `q = rank(Σ̂)` | small `m`; needs `Σ̂`, whose elements number order `m²` |
| `T_max,M` | `max_{i ∈ M} t_{i·}`, `t_{i·} = d̄_{i·}/√v̂ar(d̄_{i·})` | large `m`; no `Σ̂` needed |
| `T_R,M` | `max_{i,j ∈ M} |t_{ij}|`, `t_{ij} = d̄_{ij}/√v̂ar(d̄_{ij})` | large `m`; `t_{ij}` **is** the Diebold–Mariano statistic |

`T_max` and `T_R` have non-standard limits depending on the correlation matrix `ρ` of the `d̄_{i·}`
(Lemma 2, Theorem 4: `T_max → F_ρ`, the law of the maximum of `N_m(0, ρ)`), and the paper's answer is
a **moving-block bootstrap**, which estimates the needed quantile and disposes of the nuisance
parameter implicitly. The natural coherent elimination rule for `T_max` is to drop the model attaining
the max; the paper proves (Section 3.1.2's coherency argument) that this pairing satisfies Definition 3.

Two explicit scope statements the paper makes about itself, both of which matter below:

- "the MCS is specific to [the] set of candidate models, `M₀`, and therefore **silent about the
  relative merits of objects that are not included in `M₀`**";
- "When `m` is large relative to the sample size, `n`, reliable estimates of `Σ` are difficult to
  obtain" — the same `N/T` complaint as `#294` and `#306`–`#310`, now about the comparison matrix.

## Robustness evidence (qualitative only)

Tier-1 venue, 2079 citations, and the method is standard enough to have CRAN and MATLAB
implementations maintained by third parties (Bernardi–Catania's `MCS` package is cited in the
follow-up literature). The theory is theorem-and-proof, so "replication" means independent
re-derivation, and there is some: `notes/2026-10-28-argmin-inference-minimax-separation-rate.md`
(Kim–Ramdas) reproduce Theorem 1(i) explicitly, crediting a proof to Jing Lei, and reach the same
conclusion for a **fixed** candidate-set size. Their qualification is recorded in that note and is
the one caveat a lab should carry: the asymptotic argument's union bound carries a factor
`|M*| × 2^{|M₀|} × o(1)`, which vanishes only while `|M₀|` is held constant, so the procedure is
best read as a **fixed-size** model-selection method. HLN's own statements are consistent with this —
Assumption 1 and Theorem 1 are stated "for any `M ⊂ M₀`" with `M₀` given — so this is a scope
clarification, not an error, and nothing in HLN claims otherwise.

Known limitation documented from the sequential side rather than here: applying the MCS repeatedly as
data accumulate degrades its coverage. See `notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md`.

## Implementability here

**Free, holdout-free, and already half-built.** Everything the MCS needs is a matrix of per-period
losses for the candidates on common dates, which is what `experiments/trial_returns/` holds and what
`scripts/rank_trials.py` already loads. The loss is `L_{i,t} = −r_{i,t}` (or `−(r_{i,t} − r_{pool,t})`),
`n ≈ 1,510` validation days, `m₀` = the number of recorded trials. Nothing in the procedure reads
holdout, re-runs a strategy, or spends a trial against the deflated bar. I have **not** read
`engine/ranking.py` — `research/README.md` puts `engine/` off-limits to this agent — so what follows
is a set of checkable questions for whoever owns that file, not a claim about what it does.

1. **Put the equal-weight eligible pool into `M₀`.** This is the one structural recommendation and it
   is free. The MCS's centering is `d̄_{i·} = L̄_i − L̄_·`, the average over the *surviving candidates* —
   a moving target that shrinks as models are eliminated. The lab's `skill` is centred on a fixed
   external benchmark that is **not** a candidate. Those answer different questions: an MCS over
   trials alone returns "the best trials, among trials", and that set can consist entirely of books
   worse than the pool. Enter the pool as one more object and the output reads directly in the gate's
   own language: **if the pool survives to the end of the elimination, the data do not distinguish any
   recorded trial from the benchmark.** That is `program.md`'s promotion question asked at the level of
   the whole board instead of one candidate at a time, and it costs one extra column.
2. **Use `T_max` or `T_R` with the moving-block bootstrap, not a quadratic form.** `m₀` grows nightly
   while `n` is fixed at the validation window, so `Σ̂`'s order-`m²` elements are exactly the regime
   HLN say to avoid. `T_R`'s building block `t_{ij}` is the Diebold–Mariano statistic, so a pairwise
   board the lab may already compute is the raw material.
3. **Report MCS p-values, not tier labels.** Definition 4's running maximum gives every trial one
   number with the property that membership at any `α` is a threshold on it. That is strictly more
   informative than a tier, and it removes the temptation the current board's own docstring warns
   against ("the order inside tier 1 is not evidence") by making the non-evidence explicit: two trials
   with the same `p̂` are the same answer.
4. **Check Assumption 2 across protocol versions, because the ranking and the deflator disagree about
   scope.** `scripts/rank_trials.py` collects `recorded_trials(version)` — one protocol version — while
   `program.md`'s deflated bar counts "every recorded trial of every protocol version". Assumption 2
   needs `{d_{ij,t}}` stationary, and v1/v2/v3 differ in fill convention, drift treatment and cost
   model, so a difference between a v1 and a v3 trial is **not** a stationary series even on the same
   dates. Restricting the MCS to one version is therefore the right call; the note to make is that the
   two numbers on the board answer questions over two different candidate sets, and only the deflator's
   set is the one the search actually explored.
5. **Read a wide tier 1 as the answer.** The quoted passages above make this the paper's own position.
   A board on which ten trials cannot be separated is a board saying the validation window has
   ~1,510 days and the candidates' active returns are nearly collinear — which is information, and is
   the same message `#294`/`#306`'s `N/T` arithmetic delivers from the estimation side.

**Pitfalls.** (i) The MCS is silent about objects outside `M₀`, so tier 1 says nothing about candidates
nobody has written — it is not a statement about the design space. (ii) Coherency is a constraint on
the test/elimination pairing, not a free choice: a more powerful test with an incoherent rule can
eliminate good models, and the paper's murder analogy is the reason. (iii) `µ_{ij}` is assumed constant
in `t`; the lab's own records of sign inversion across sub-periods (`learnings.md`, the CIV-beta entry
and the 2026-10-27/28 phase table) are evidence against that assumption holding across a two-decade
train split, which is why the *sequential* formulation and its three graded notions of superiority are
the better fit — see the companion note.

## Related

- `notes/2026-10-28-argmin-inference-minimax-separation-rate.md` — the same object with a minimax
  theory, a `0.007 s` alternative to the bootstrap, and the `|M₀|` fixed-size qualification.
- `notes/2026-10-28-sequential-model-confidence-sets-anytime-valid.md` — the same object made valid
  under a candidate set and a sample that both grow, which is the lab's actual pattern.
- `notes/2026-10-19-consistent-scoring-functions-and-elicitability.md` — the MCS takes the loss
  function as given; whether the chosen loss elicits the functional the lab cares about is that note's
  question, and it is upstream of this one.
- `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` and
  `notes/2026-10-23-noise-sensitivity-of-risk-measures.md` (`#294`) — the `N/T` arithmetic that
  explains *why* tier 1 is wide, from the estimation side rather than the testing side.
- `notes/2026-09-15-reality-check-max-statistic-under-dependence.md`,
  `notes/2026-09-16-does-meff-control-the-familywise-error-rate.md`,
  `notes/2026-08-24-deflated-sharpe-ratio.md` — the folder's existing multiple-testing layer. Those
  answer "is the best one real?"; this answers "which ones could be the best?", and the lab needs both.
- `program.md` §"Objective and promotion rule" and `scripts/rank_trials.py` — the board this note is
  about.
