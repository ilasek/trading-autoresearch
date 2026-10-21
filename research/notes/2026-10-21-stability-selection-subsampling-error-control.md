---
title: "Stability Selection" — keep the variables that survive resampling rather than the ones one fit happened to pick, which converts the unanswerable choice of penalty into a finite-sample bound on the expected number of false selections
authors: Meinshausen, Bühlmann
year: 2010
venue: Journal of the Royal Statistical Society Series B (Statistical Methodology) 72(4), 417–473 (venue tier 1 — read paper with invited discussion)
url: https://doi.org/10.1111/j.1467-9868.2010.00740.x
citations: 2245 (Crossref `is-referenced-by-count`, checked 2026-10-21); 2861 (Semantic Scholar by DOI, same date). Both indices resolved on the first call.
sample_period: none — finite-sample theory plus synthetic simulations, with two real-data illustrations (a riboflavin-production gene-expression panel, n = 115 / p = 4088, and a motif-regression problem). No market data of any period appears in it.
markets: none
tier: A
validation_overlap: false
published_post_2018: false
read: full text of `arxiv.org/pdf/0809.2932` (v2 of May 2009, 2.3 MB → 281 KB of clean text via `pdftotext -layout`, 599 instances of `" the "`, no ASCII shift, title line verified against the Crossref record). Note that `file` reports this PDF as "6 page(s)" while it extracts to 281 KB across the full article — a page-count disagreement is not a truncated fetch, and the `" the "` count is the check that caught it. This is the pre-discussion version; nothing below is attributed to discussants.
---

## Mechanism

No economic mechanism. This is the **second layer** of tonight's chain: given a procedure that picks
a subset of predictors, how do you choose how aggressive it should be, and how do you report what it
picked without overstating it?

The problem the paper attacks is one the lab has in its own vocabulary. A penalised fit returns a
different selected set for every value of the penalty `λ`, and "the general issue of selecting a
proper amount of regularisation … has largely remained a problem with unsatisfactory solutions". The
usual answer — cross-validation — is *known to select too many variables*: the paper's own
gene-expression illustration has 14 pure-noise predictors inside the cross-validated model. And
worse, in high dimensions the right `λ` depends on the **noise level**, which is exactly the quantity
you cannot estimate when `p ≫ n`.

The idea is to stop asking which single model is right. Perturb the data many times, run the
selection procedure on each perturbation, and **keep the variables that are selected often**. The
object of interest is no longer a selected set but a *selection probability per variable*.

Formally. Let `I` be a random subsample of the observations of size `⌊n/2⌋`, drawn **without
replacement** (chosen because it most closely resembles the bootstrap while staying cheap). For a
penalty `λ`, the selected set `Ŝ^λ(I)` is a function of the subsample, and the **selection
probability** of variable `k` is

    Π̂^λ_k = P*( k ∈ Ŝ^λ(I) )

where `P*` is over the subsampling (and over any randomness inside the selection algorithm). Plotting
`Π̂^λ_k` against `λ` gives a **stability path**, the resampling analogue of a regularisation path.
The **set of stable variables** at cutoff `π_thr` is

    Ŝ_stable = { k : max_{λ ∈ Λ} Π̂^λ_k ≥ π_thr }.

The reason this is more than a heuristic is the error bound. It converts the choice of `λ` — which
nothing could pin down — into a choice of *how many variables the procedure is allowed to select on
average*, which is directly observable.

## Construction recipe

**The procedure.** Choose a selection algorithm (lasso, forward selection, orthogonal matching
pursuit, anything that returns a subset). Choose a regularisation region `Λ`. Draw ~**100 subsamples
of size `⌊n/2⌋` without replacement** ("evaluating selection probabilities over 100 subsamples seems
sufficient in practice"). Run the algorithm on each. Record, per variable, the fraction of subsamples
in which it was selected. Keep the variables whose maximum selection frequency over `Λ` exceeds
`π_thr`.

**The error bound (Theorem 1).** Let `N` be the set of noise variables, `q_Λ = E|Ŝ^Λ(I)|` the average
number of variables selected, and `V = |N ∩ Ŝ_stable|` the number of false selections. Under two
assumptions — that the selection indicators for the *noise* variables are **exchangeable**, and that
the base procedure is **no worse than random guessing** —

    E(V) ≤ (1 / (2π_thr − 1)) · q_Λ² / p.

`E(V)` is the per-family error rate. The constructive recipes the paper gives from it:

- With **`π_thr = 0.9`** (its default) and **`q_Λ = 0.8√p`**, `E(V) ≤ 1`.
- With **`q_Λ = 0.8√(αp)`**, the **familywise** error rate is controlled at `α`: `P(V > 0) ≤ α`.
- Or fix `Λ` and solve for `π_thr` instead. Either direction works.

To make `q_Λ` knowable rather than estimated, **parameterise the procedure by the number of selected
variables `q` rather than by `λ`**: take the first `q` variables to enter the regularisation path.
Then `q_Λ` is exactly what you set it to. This is the step that makes the bound usable.

**Insensitivity, which is the practical selling point.** "The exact cutoff `π_thr` … is a tuning
parameter but the results vary surprisingly little for sensible choices", with `π_thr ∈ (0.6, 0.9)`
giving similar answers, and the results do not depend strongly on `Λ` either. **Pointwise control** —
a single `λ`, chosen loose enough that `Ŝ^λ` is somewhat too large — is explicitly supported and is
"in our experience very successful"; for procedures that select incrementally (`Ŝ^λ ⊆ Ŝ^{λ'}` for
`λ ≥ λ'`), pointwise control and control over `Λ = [λ, ∞)` are equivalent.

**Randomised lasso, and the consistency claim.** The paper's sharper theoretical result needs one
extra ingredient. The **randomised lasso with weakness `α ∈ (0, 1]`** replaces the common penalty
with an independently randomly reweighted one:

    β̂^{λ,W} = argmin_β ‖Y − Xβ‖²₂ + λ Σ_k |β_k| / W_k,    W_k i.i.d. in [α, 1]

implemented by simply **rescaling column `k` of the design by `W_k`** and running a standard lasso.
The weights are *not* based on any previous estimate (unlike the adaptive lasso) — "it is simply
chosen at random!" The paper is candid that this "seems nonsensical at first sight" and that a single
randomised fit is useless; it is only the *selection frequency over many randomised fits* that is
powerful. Its recommended weight distribution for the theory is `W_k = α` with probability `p_w` and
`1` otherwise, and in practice it recommends **combining random weight perturbation with subsampling**
(Remark 4).

Theorem 2's content: ordinary lasso variable-selection consistency requires the **irrepresentable /
neighbourhood-stability condition**

    max_{k ∈ N} | sign(β_S)ᵀ (X_Sᵀ X_S)^{-1} X_Sᵀ X_k | < 1,

which is sufficient and *almost necessary*. Stability selection with the randomised lasso is
variable-selection consistent **without it**, needing only a sparse-eigenvalue (sparse Riesz)
condition — stronger than the bare sparse Riesz condition but "typically much weaker than the
standard assumption of the 'irrepresentable condition'". On a high-probability set, **no noise
variable is selected**, and every true variable with `|β_k| > 0.3(Cs)^{3/2}λ` is selected; variables
with coefficients below that bound may be missed.

**Remark 3 is the behavioural summary worth carrying:** the guarantee holds **for all `λ ≥ λ_min`**,
so if `λ` is chosen *too large*, stability selection still admits no noise variables — it only misses
some real ones. A hard-thresholded lasso at too large a `λ`, by contrast, *includes* noise variables.
"Stability selection with the randomised Lasso exhibits an important property of being conservative
and guarding against false positive selections."

**Cost.** 100 subsamples of size `n/2` is "roughly three times more expensive than 10-fold CV" in the
`p > n` regime (quarter-cost per fit × 100 ≈ 25 single fits, against ≈ 8.1 for 10-fold CV), rising to
roughly 5.5× when per-fit cost is linear in `n` rather than quadratic — which is the `p < n` case, and
therefore the lab's case. The paper's own benchmark: stability selection with the lasso, `p = 1000`,
`n = 100`, 100 subsamples, **about 10 seconds** on a 2.2 GHz processor using a coordinate-descent
implementation.

## Robustness evidence (qualitative only)

Replication in the Hou–Xue–Zhang / Jensen–Kelly–Pedersen sense does not apply — no anomaly, no
cross-section of returns. The analogue is that this is a **read paper** at JRSS-B, published with
invited discussion, and among the most-cited methodological papers in high-dimensional statistics on
both indices. McLean–Pontiff decay does not apply.

Honest statement of the evidence's shape. The **exchangeability assumption is the weak point and the
paper says so**: "perhaps stronger than one would wish, but there does not seem to be a way of
getting error control in the same generality without making similar assumptions." It is satisfied
when the design is random and the noise predictors' joint distribution is exchangeable — independence
is a special case, and so is joint normality with a *common* pairwise correlation `ρ` among the noise
variables. It is **not** guaranteed on real data, and the paper's defence is empirical: "for real data,
we have no guarantee that the assumption is fulfilled but the numerical examples … show that the bound
holds up very well for real data." Critically, **exchangeability is needed only for Theorem 1's bound**
— the consistency result, the insensitivity to `λ`, and the improvement in selection quality do not
rest on it.

The qualitative empirical claim across the paper's regression, graphical-modelling and
motif-regression examples is that "variable selection and structure estimation improve markedly for a
range of selection methods if stability selection is applied", and in its permuted-gene illustration
the stability path separates genuine from permuted predictors visibly better than the regularisation
path does — with the randomised lasso separating them completely where the plain lasso does not.

## Implementability here

**This is the most directly usable of tonight's four notes, because the lab's existing harness
already produces the perturbations the method needs, and because the lab has an open problem of
exactly this shape.**

**Where it fits.** The companion note
`notes/2026-10-21-sure-independence-screening-marginal-vs-joint.md` proposes a free ISIS pass over
the lab's feature block to test for a marginally-null-but-jointly-important feature. That pass
*selects*, and a single selected set reported from one fit on one train window is the thing
`SUMMARY.md`'s post-selection material (`#108`–`#110`, 2026-09-15) and the lab's own
specification-curve embargo of 2026-09-14 exist to discipline. **Stability selection is the wrapper
that makes the ISIS pass reportable**: run the pass on ~100 subsamples, report selection
frequencies, and keep only features above a cutoff. The lab gets a per-feature number with an error
bound instead of a set with none.

**Translate the bound into the lab's numbers.** With a feature block of `p ≈ 7–15`, `√p` is 2.6–3.9,
so `q_Λ = 0.8√p ≈ 2–3` features at `π_thr = 0.9` gives `E(V) ≤ 1`. For familywise control at
`α = 0.1`, `q_Λ = 0.8√(0.1p) ≈ 0.7–1.0` — i.e. **at this `p`, honest familywise control over the
feature block admits about one feature.** That is a useful and slightly deflating number to have
before writing a learned candidate: it is the selection-side analogue of the lab's own finding that
the gate admits very little, and it arrives from a completely independent direction. It also says
the bound is *loose* at small `p` (the paper notes the minimum achievable non-trivial PFER is `1/p²`,
"low enough for all practical purposes as long as `p > 10`"), so treat the arithmetic as a
sanity-check on ambition rather than as the operative screen.

**What subsample to draw, and this is the one place the recipe needs changing.** The paper's `⌊n/2⌋`
without replacement assumes i.i.d. rows. The lab's rows are not: they are name-date observations
with cross-sectional correlation within a date and serial correlation across dates, which is the
setting `notes/2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` is about.
**Subsample whole dates (or whole blocks of consecutive dates), never individual name-date rows** —
drawing rows breaks the dependence structure and would make the selection frequencies optimistic in
the same way the lab's [2026-10-20/21] pooled-rank error did. A block subsample of half the
month-ends, drawn as contiguous blocks, is the conservative version and costs the same.

**A second, cheaper use that needs no new fit: stability as a diagnostic on what the lab already
has.** `experiments/learnings.md` [2026-08-29, v1 era, 140-name panel — the numbers do not transfer
to v3 but the observation does] records of its first learned candidate that "nothing in the
construction asks it to be stable", and that the same learner "rediscovers the incumbent, worse"
when fed the incumbent's own lookbacks. **The selection frequency of each feature across the
walk-forward refits the lab already runs is a stability path for free** — the refits are not
subsamples of the paper's kind, but a feature selected in 5% of month-end refits and a feature
selected in 95% of them are different objects, and the lab currently reports neither. This is a
retrospective pass over existing fits.

**A third use, and the one this note would push hardest.** `#282` from 2026-10-20 says an error bar
computed from pooled residuals of a conditional-mean model has a width that cannot depend on the
state. `[2026-10-20/21]` F8 then gave the lab a **pooled** noise floor (train skill scattered at
sd 0.025) and F10 showed the realisation ratio varies by object (6% to 38%, negative once) — i.e. the
floor is exactly the state-independent pooled object `#282` warns about. **A subsampling distribution
of the screen's own statistic is the state-dependent replacement**: resample blocks of dates,
recompute the rank IC, and read the floor off the resulting spread per object rather than off one
pooled number. That costs no trial and no holdout, and it is the same machinery as the selection
frequencies.

**Known pitfalls.**

- **Exchangeability is the assumption to state, not to assume.** The lab's features are visibly
  *not* exchangeable — [2026-10-17/18] and [2026-10-20/21] F5/F6 document several of them collapsing
  onto the volatility axis and the slope. So Theorem 1's `E(V)` bound should be reported as
  indicative, and the consistency and insensitivity benefits (which do not need it) relied on
  instead. Do not quote `E(V) ≤ 1` as if it were measured here.
- **Determinism.** `CLAUDE.md` requires candidates to be deterministic to 1e-6, because
  `causality_check` reads non-determinism as a peek. Both the subsampling and the randomised lasso's
  weights are random, so **every draw must come from a seeded generator fixed in the candidate file**,
  and the weights must be a deterministic function of (seed, refit date). A stability-selection
  screen run *outside* a candidate, as a free measurement, has no such constraint; one run *inside*
  `generate_weights` does.
- **Cost against the ~60s-per-call budget.** `CLAUDE.md` notes the protocol calls `generate_weights`
  about seven times per trial on a panel ~10× wider than v1's. 100 subsampled refits inside a
  candidate is almost certainly out of budget; the paper's own guidance — "if computational costs
  would scale linearly with sample size … this factor would increase to roughly 5.5" times a single
  CV — is the figure to plan against. **Run the stability screen as a free measurement to choose the
  feature set, then hard-code the chosen set in the candidate.** That is a selected object and must
  be declared as one, which is what the companion knockoff note and the 2026-09-15 post-selection
  material are for.
- **It does not create signal.** Stability selection makes a selection reproducible and bounds its
  false discoveries. If the features carry nothing — which is the lab's measured position after three
  closures — a stable selection of nothing is what it will return. Its value here is that it makes
  the *reporting* honest and gives the per-feature number the lab lacks, not that it is a route to a
  candidate.
- **`π_thr` is insensitive but not free.** The paper's range is `(0.6, 0.9)`. Pick one before looking
  (0.9, its default), write it down, and do not tune it — tuning it is precisely the
  argmax-over-variants act the lab embargoed on 2026-09-14.

## Related

- `notes/2026-10-21-sure-independence-screening-marginal-vs-joint.md` is the procedure this one
  wraps; `notes/2026-10-21-knockoff-filter-fdr-control-vs-permutation.md` is the alternative error
  criterion (FDR rather than PFER/FWER) and carries the finding about why a *permutation* null cannot
  substitute for either; `notes/2026-10-21-illusion-of-sparsity-selection-versus-shrinkage.md` asks
  whether a selected set is the right object at all.
- `notes/2026-08-19-bagging-averaging-unstable-predictors.md` is the closest existing note: it is
  about averaging the *predictions* of an unstable predictor, where this is about averaging its
  *selections*. The two are the same subsampling idea pointed at different outputs, and the
  distinction is worth keeping — `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` draws the
  analogous line one level up.
- `notes/2026-10-13-k-fold-cross-validation-under-temporal-dependence.md` is why the subsample must be
  blocks of dates rather than rows.
- `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-08-24-multiple-testing-haircut.md` and the
  2026-09-15 post-selection cluster are the folder's existing error-rate material; all of it asks
  whether the best of `N` *results* is significant, where this asks how many of the selected
  *variables* are false. Different unit, different bound.
- `experiments/learnings.md` [2026-08-29, v1 era] ("nothing in the construction asks it to be
  stable") is the lab's own statement of the gap this note fills; `[2026-10-20/21]` F8/F10 are the
  pooled noise floor the subsampling distribution would replace, and those are v3.
