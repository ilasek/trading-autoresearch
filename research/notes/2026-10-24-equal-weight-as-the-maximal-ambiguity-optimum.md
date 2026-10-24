---
title: "On robust portfolio and naïve diversification: mixing ambiguous and unambiguous assets — worst-case risk is nominal risk plus a dual-norm penalty on the weights, so equal weight is what you hold when you know nothing"
authors: Paç, Pınar — extending Pflug, Pichler & Wozabal
year: 2018 (online 2017); the result extended is 2012
venue: Annals of Operations Research 266(1–2), 223–253 (venue tier 2 — peer-reviewed OR journal, not one of the rubric's tier-1 finance outlets). The extended result is Journal of Banking & Finance 36(2), 410–417 (venue tier 1).
url: https://doi.org/10.1007/s10479-017-2619-8 ; extended result https://doi.org/10.1016/j.jbankfin.2011.07.018
citations: "Paç–Pınar: 8 (Crossref `is-referenced-by-count`, checked 2026-10-24) — low, and the tier below reflects it. Pflug–Pichler–Wozabal (the result it extends): 203 (Crossref, checked 2026-10-24); OpenAlex 221 the same day, so the count is real and not an indexing artifact."
sample_period: "None. Both papers are theory. Paç–Pınar's Section 4 contains constructed numerical examples under assumed CVaR/Markowitz functionals, not a backtest; there is no market data anywhere in it. Nothing in either paper can touch 2018–2023."
markets: not applicable (theory). The asset model is abstract: `N` assets with an ambiguous joint distribution plus `L` assets with a fully known one.
tier: "B. The central theorem (worst-case risk = nominal + dual-norm penalty ⇒ uniform portfolio in the high-ambiguity limit) is Pflug–Pichler–Wozabal's, is published in a tier-1 finance journal, is proven for a whole class of risk measures, and has 203 citations — that part is A-grade. The extension read here is correctly derived and peer-reviewed but thinly cited (8), single-paper, and carries a limitation its authors flag themselves (no cross-market correlation). Graded on the extension, not on the result it extends."
validation_overlap: false
published_post_2018: false
read: "Paç–Pınar in full — the typeset published version, from the Bilkent University institutional repository (`repository.bilkent.edu.tr/bitstreams/b84785be-d172-440b-aa3b-519360241c46/download`, 969 KB, 31 pages, 139 KB of `pdftotext -layout` text, 470 `\" the \"`, clean). Proofs are in its Appendix and were skimmed, not verified line by line. Pflug–Pichler–Wozabal was NOT obtained (closed at Elsevier; no OA location in OpenAlex; the University of Vienna Phaidra copy is a refusal — see the access note). Its theorem is recorded here **as Paç–Pınar state and re-derive it**, which is a primary source that adopted the framework and reproduced the proof structure, not a search snippet. Ghahtarani–Saif–Ghasemi's review (read in full, own note) reports the same result independently and agrees."
access_note: "`fedora.phaidra.univie.ac.at/fedora/get/o:691640/bdef:Content/download` returns **HTTP 200 with a zero-byte body** — the same signature `research/README.md` records for `escholarship.org` on 2026-10-23, and now a second host with it. `curl -w '%{size_download}'` is the only thing that reveals it. `api.core.ac.uk` returns 429 to an unauthenticated client. `file -b` called the Bilkent PDF \"9 page(s)\"; `pdfinfo` correctly said 31 — the README's warning, confirmed again."
anti_lookahead_note: "Neither paper contains dated performance figures, market events, or regime commentary; there is nothing to withhold. The numerical examples in Section 4 are parameterised by hand."
---

## Mechanism

This lab's protocol grades every candidate as **skill** — its Sharpe minus the equal-weight eligible
pool's on the same days. The benchmark is therefore the equal-weight portfolio, and the folder has
treated it as a sensible convention backed by DeMiguel–Garlappi–Uppal's empirical finding that
nothing reliably beats `1/N`. This pair of papers says something stronger and different: the
equal-weight portfolio is **the exact solution of a specific decision problem** — the one you face
when you have no trustworthy distribution at all.

**The uncertainty model is non-parametric.** You have a nominal joint distribution `P` for asset
returns. The truth is any `Q` within a ball of radius `κ` around `P` in the Kantorovich/Wasserstein
metric. This is weaker than the usual robust-portfolio setup (which puts a set around the *moments*
`µ, Σ`): nothing about the shape of the distribution is assumed.

**Proposition 1 — the whole mechanism, in one identity.** Let `R` be any **convex, law-invariant**
risk measure on `L^p`. Under the paper's regularity conditions (the subgradient's `L^q` norm is a
constant `C`), for every `κ > 0` and every allocation `(w, v)` — `w` on the `N` ambiguous assets,
`v` on the `L` unambiguous ones:

```
sup_{Q ∈ B_κ(P)}  R( ⟨X_Q1, w⟩ + ⟨X_Q2, v⟩ )  =  R( ⟨X_P1, w⟩ + ⟨X_P2, v⟩ )  +  C·κ·‖w‖_q
```

with `1/p + 1/q = 1`. **The worst case over the ambiguity ball is the nominal risk plus `Cκ` times
the dual norm of the weight vector.** The sup is gone; a robust problem has become a penalised
nominal problem, and the penalty is a *concentration* penalty on the weights.

**Why `1/N` falls out.** Minimise the right-hand side over the simplex. As `κ` grows the penalty
term dominates, and the problem becomes `min ‖w‖_q` subject to `w ≥ 0, 1ᵀw = 1` — whose solution for
any `q > 1` is `wᵢ = 1/N`. The equal-weight portfolio is the minimum-dual-norm point of the simplex.
That is Pflug–Pichler–Wozabal's theorem: as the ambiguity radius grows, the worst-case-risk-minimising
portfolio converges to the uniform one, **for every risk measure in the convex law-invariant class** —
not for one functional, and not as an empirical regularity.

**Proposition 2 — and it is a finite threshold, not just a limit.** For `p = 1` (so `q = ∞`), the
uniform portfolio is *exactly* optimal for the inner problem once

```
κ ≥ κ*  =  (N − 1)·E|⟨X_P1, 1⟩|·1_{Z̄=0}      if 1ᵀv ≠ 1
κ ≥ κ*  =        E|⟨X_P1, 1⟩|·1_{Z̄=0}        if 1ᵀv = 1
```

For `p = 2` the optimum is confined to a ball around the uniform portfolio whose radius shrinks
explicitly in `κ`. For other `p` the authors prove convergence but give no rate. **So there is a
computable ambiguity level above which equal weight is not merely near-optimal but optimal, and
`κ*` grows with `N`** — a wider panel needs more ambiguity before uniformity takes over.

**Proposition 3 — the direction of the first departure, and this is the part that is construction
material.** As `κ → ∞`, every allocation with `1ᵀv ≠ 1` becomes suboptimal: the investor **divests
the ambiguous market entirely** in favour of the unambiguous one. Along the way, two things happen at
once and they are different operations: *within* the ambiguous group the weights stay uniform, while
the *total* allocation to that group shrinks. The authors give explicit suboptimality bounds that
rule out an allocation level `s` to the ambiguous market once `κ` exceeds a stated function of `s`,
and an analogous divestment radius for `p = 2`.

So the picture is: **confidence buys concentration, and the first thing it buys is group selection,
not reweighting.** With no confidence you hold everything equally. With a little confidence you move
wealth between a better-measured group and a worse-measured one while staying uniform inside each.
Reweighting name by name inside a group is what the *last* of your confidence buys, not the first.

## Construction recipe

Taking only what the theorems license:

1. **Default to equal weight inside any set of names you cannot distinguish.** Not as a heuristic —
   as the optimum of the problem you are actually solving when the distribution is unknown.
2. **Price every departure from equal weight as a bet on a bounded ambiguity radius.** A candidate
   book `w` is implicitly asserting `κ < κ̂` where `κ̂` solves `R(w) + Cκ̂‖w‖_q = R(w^u) + Cκ̂‖w^u‖_q`.
   Since `‖w‖_q ≥ ‖w^u‖_q` always, that inequality is well posed: concentration must buy enough
   nominal risk reduction to pay `Cκ̂·(‖w‖_q − ‖w^u‖_q)`.
3. **Add `‖w‖_q` to the objective rather than bounding the number of holdings.** A dual-norm penalty
   with a tunable coefficient is the theoretically sanctioned de-concentration device, and it is one
   scalar. For `p = 1` it is `‖w‖_∞` (cap the largest weight); for `p = 2` it is `‖w‖₂` (a
   Herfindahl-style penalty). The protocol's 25% position cap is already an `‖w‖_∞` constraint — i.e.
   the lab is *already* running the `p = 1` version of this penalty in constraint form.
4. **Split the panel by how well-measured each name is, tilt between the groups, stay uniform inside
   them.** This is Proposition 3's operational content, and it requires only a classifier for
   "ambiguous versus unambiguous", not a return forecast.
5. **Do not read the group-tilt magnitudes off the paper.** See the limitation below.

## Robustness evidence (qualitative only)

- **Generality is the strong point.** Proposition 1 holds for the whole class of convex law-invariant
  risk measures, so the conclusion is not an artifact of variance or of CVaR. It covers the mean-variance
  (Markowitz) functional and CVaR explicitly, which are the two the authors then work out in Section 4.
- **Two independent derivations of the central result.** Pflug–Pichler–Wozabal proved it; Paç–Pınar
  adopt the framework, re-derive the proposition with the extra unambiguous-asset term, and confirm
  the convergence. The review note's independent reading of the same literature reports the same
  statement. For a theorem that is the right kind of corroboration.
- **The Wasserstein-ball model is the honest version of "I don't know the distribution."** Unlike
  moment-based uncertainty sets, it does not smuggle in a parametric family. That is why the result
  is about ambiguity rather than estimation error, and the two are not the same thing.
- **Known related finding in the same direction.** The authors note that their own earlier work with
  *parametric* mean uncertainty produced the same qualitative behaviour (shrinking risky allocation
  as the uncertainty radius grows), and that this paper's contribution is proving the uniform
  portfolio *persists* while the allocation shrinks, under a non-parametric model.
- **The limitation the authors flag, and it bites here.** The model has **no correlation between the
  ambiguous and unambiguous markets**; they call this a shortcoming and name fixing it as future work.
  In this lab both candidate groups would be equities on the same panel and strongly correlated, so
  the clean "divest one market for the other" arithmetic does not transfer. What survives the
  limitation is (a) the within-group uniformity result, which is Pflug's and needs no market split at
  all, and (b) the *sign* of the group tilt. The *magnitudes* and the divestment rates do not survive,
  and are not recorded above.
- **The second limitation, and it is mine rather than theirs.** `R` must be a convex law-invariant
  **risk measure**. The Sharpe ratio is not one — it is a ratio, not convex in `w`. So these theorems
  say equal weight minimises worst-case *risk*; they do **not** prove it maximises worst-case *Sharpe*,
  which is the statistic this lab's benchmark is measured in. The decision-theoretic identity for the
  equal-weight pool is therefore strong but not exact for the protocol's own objective. Do not write
  it down as though it were.
- **Thin citation count on the extension (8).** The extension's specific propositions have not been
  independently checked by a literature. Weight them accordingly; weight the Pflug result more.

## Implementability here

**Status: one free interpretation rule, one cheap construction idea, and one correction to how the
folder has been describing the benchmark.**

- **The free interpretation rule, and it is the most useful thing here.** The v3 benchmark — the
  equal-weight eligible pool — is not an arbitrary yardstick. It is (up to the Sharpe-versus-risk
  caveat above) the portfolio that solves the maximal-ambiguity problem. So **"beating the pool" is
  formally a claim that the candidate's ambiguity about the return distribution is below a finite,
  `N`-dependent threshold**, and a candidate should be read as making that claim. This reframes
  candidate-list item 1 (count the noisily-estimated parameters) from a calibration into a
  consequence: an estimation-heavy weighting scheme loses to equal weight precisely when its
  ambiguity exceeds `κ*`, and `κ*` *rises* with `N`. The v2/v3 panel is roughly a thousand eligible
  names on a typical validation date against the v1 panel's 140, so the threshold the lab must beat
  is **higher now than when every weighting-scheme verdict in `learnings.md` was measured.** That is
  an argument for expecting equal weight to be *harder* to beat on the wide panel, not easier, and
  it is derived rather than measured.
- **The lab is already running the `p = 1` penalty and should notice.** The protocol's 25% per-position
  cap is an `‖w‖_∞` bound, which Proposition 1 identifies as the dual-norm penalty for `p = 1`
  ambiguity. The cap is usually described in this repo as a risk-management rule; it is also,
  exactly, a robustness device with a known decision-theoretic reading.
- **The construction idea, and it is cheap and new to this folder.** Partition the eligible panel by
  **measurement quality rather than by signal** — candidate axes available from the protocol's own
  data: length of available price history (a recently-eligible name has a short, thin record),
  trailing dollar-volume tier (the engine already computes it for costs), and fraction of
  forward-filled/holiday prints in the trailing window (a name with many non-real closes is measured
  worse). Then hold **equal weight within each group and tilt the group budget toward the
  better-measured group**, with the tilt as the single parameter. Proposition 3 gives the direction;
  the magnitude is the thing to measure. This is a `portfolio-learning` candidate that estimates
  almost nothing — one scalar — so item 1's triage rule passes it, which almost no weighting proposal
  in this folder does.
- **The guard, and it is worth checking before writing code.** "Length of available price history" and
  "is the name recently eligible" are properties of the visible panel at each rebalance date and are
  causal. They must be computed from the `eligible` frame and `prices` as truncated, never from a
  membership file — `CLAUDE.md` refuses a candidate that reads those. A column appears in `prices`
  only once the name has been eligible, so history length is directly measurable without touching
  anything forbidden.
- **What not to do.** Do not build a Wasserstein-robust optimizer. The radius `κ` is unobservable, the
  problem needs a solver this repo does not have, and Proposition 1's whole point is that the robust
  problem *equals* a penalised nominal problem — so the penalty is the implementable object and the
  optimizer is not. Also do not treat `κ*`'s formula as a number to compute: `C` and `1_{Z̄=0}` are
  properties of the chosen risk measure's subgradient, not quantities this panel hands you.

## Related

- `2026-08-17-naive-vs-optimized-weighting.md` — DeMiguel–Garlappi–Uppal's empirical `1/N` result.
  This note supplies the theorem the folder has been missing underneath it: not "optimization is too
  noisy to pay" but "uniformity is the optimum of the maximally-uncertain problem".
- `2026-10-11-optimal-combination-of-the-naive-rule-and-an-estimated-one.md` and
  `2026-10-15-random-weight-indices-and-the-equal-weight-centre.md` — the equal-weight point as a
  shrinkage target and as the centre of the random-portfolio null. Three different literatures now
  put the same point at the centre, for three different reasons; that coincidence is itself worth
  recording.
- `2026-10-24-transaction-costs-as-robustness-and-regularization.md` — the same dual-norm algebra for
  *parameter* uncertainty and trading costs. Note which vector each penalises: that one penalises
  `w − w₀` (the trade), this one penalises `w` (the holding). Costs push you toward *not moving*;
  ambiguity pushes you toward *being spread out*. They are not the same force and a candidate can
  need both.
- `2026-10-24-uncertainty-sets-as-dual-norm-penalties.md` — the general optimization result that both
  are instances of.
- `2026-10-23-coherent-measures-of-risk-axioms.md` and `2026-10-23-cvar-optimization-as-a-linear-program.md`
  — `R` convex and law-invariant is the class those notes characterise, and CVaR is the worked case in
  Section 4 here. The 2026-10-23 session concluded a mean-CVaR objective is not worth building on this
  panel (candidate items 294/299); nothing here reopens that, because the object taken from tonight is
  the **penalty**, which estimates nothing.
- `2026-10-24-robust-portfolio-selection-landscape-and-over-conservatism.md` — where this result sits
  in the robust-portfolio literature, and the independent confirmation of the Pflug theorem.
