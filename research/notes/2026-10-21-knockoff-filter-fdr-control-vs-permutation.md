---
title: "Controlling the False Discovery Rate via Knockoffs" — exact finite-sample FDR control for a selected variable set under any fixed design, built by manufacturing a decoy copy of each predictor that preserves the *cross*-correlations a permutation destroys
authors: Barber, Candès
year: 2015
venue: The Annals of Statistics 43(5), 2055–2085 (venue tier 1 — the discipline's flagship theoretical-statistics journal)
url: https://doi.org/10.1214/15-AOS1337
citations: 562 (Crossref `is-referenced-by-count`, checked 2026-10-21); 880 (Semantic Scholar by DOI, same date). Both indices resolved on the first call.
sample_period: none — finite-sample theory plus simulations, with one real design matrix (an HIV non-nucleoside reverse-transcriptase-inhibitor drug-resistance panel, n = 747 / p = 319) used to supply realistic sparsity and heavy-tailed noise. No market data of any period appears in it.
markets: none
tier: A
validation_overlap: false
published_post_2018: false
read: full text of `arxiv.org/pdf/1404.5609` (v3 of October 2015, 860 KB → 90 KB of clean text via `pdftotext -layout`, 727 instances of `" the "`, no ASCII shift, title line verified). This is the **IMS electronic reprint of the published article** and says so in its own header ("This is an electronic reprint of the original article published by the Institute of Mathematical Statistics in The Annals of Statistics, 2015, Vol. 43, No. 5, 2055–2085. This reprint differs from the original in pagination and typographic detail") — the second confirmation in two sessions that for an IMS journal the arXiv copy is the version of record, not a preprint.
---

## Mechanism

No economic mechanism. This is the **error-rate layer** of tonight's chain: given a selected set of
predictors, how many of them are false, and can that be bounded without knowing the noise level?

The setting is the classical linear model `y = Xβ + z`, `z ~ N(0, σ²I)`, with `X` **fixed** and
`n ≥ p`. The object controlled is the **false discovery rate** — the expected fraction of truly-null
variables among the selected ones. The guarantee is unusual in how little it asks: it holds **in
finite samples**, **for any design matrix**, **for any number of true variables**, **for any
coefficient amplitudes**, and **without any knowledge of `σ`**.

The construction is the idea worth carrying, and it is a general lesson about building a null. For
each predictor `X_j`, manufacture a **knockoff** `X̃_j` that is a decoy: it is designed to behave like
`X_j` with respect to the *other* predictors but to carry no association with the response. The
decoys cost nothing — "their construction does not require any new data". Normalise so `‖X_j‖₂ = 1`
and let `Σ = XᵀX`. The knockoff matrix is required to satisfy

    X̃ᵀX̃ = Σ,    XᵀX̃ = Σ − diag{s},    s ≥ 0,

which says: the decoys have **the same internal correlation structure** as the originals, **and the
original-to-decoy cross-correlations equal the original-to-original ones off the diagonal**
(`X_jᵀX̃_k = X_jᵀX_k` for all `j ≠ k`). Only on the diagonal do they differ: `X_jᵀX̃_j = 1 − s_j`
against `X_jᵀX_j = 1`. Power comes from making `s_j` as large as possible, so a variable is not too
similar to its own decoy. One explicit construction, valid when `n ≥ 2p`:

    X̃ = X(I − Σ^{-1} diag{s}) + Ũ C,

with `Ũ` an `n × p` orthonormal matrix orthogonal to the span of `X`, `CᵀC = 2diag{s} −
diag{s}Σ^{-1}diag{s}` a Cholesky factor, and `diag{s} ⪯ 2Σ` the condition guaranteeing it exists.
(Section 2.1.2 extends to `p < n < 2p`.)

Then each variable competes against its own decoy. Fit whatever procedure you like on the **augmented
`n × 2p` design `[X X̃]`** — the paper's worked choice is the lasso path, with `Z_j = sup{λ : β̂_j(λ) ≠ 0}`
the penalty at which column `j` first enters — and set

    W_j = max(Z_j, Z̃_j) · sign(Z_j − Z̃_j),

so `W_j` is large and positive when the real variable enters the path early **and before its own
decoy**. The whole method rests on one symmetry: for a truly null variable, there is nothing to
distinguish it from its decoy, so **the sign of `W_j` is an independent coin flip**, giving

    #{j : β_j = 0, W_j ≥ t}  =ᵈ  #{j : β_j = 0, W_j ≤ −t}.

The negative `W_j`s are therefore a free, unbiased count of how many nulls the positive side contains.

## Construction recipe

1. Normalise columns of `X`. Compute `Σ = XᵀX` (assumed invertible).
2. Choose `s ≥ 0` with `diag{s} ⪯ 2Σ`, as large as possible componentwise, and build `X̃` by the
   formula above.
3. Fit a path-based or sequential procedure on `[X X̃]`. Compute `W_j` per the sign-and-magnitude rule.
   Any statistic satisfying the paper's **sufficiency** and **antisymmetry** properties works (Section
   2.2) — it names forward-selection entry order as an alternative to lasso entry.
4. Pick the threshold. For a target FDR `q`, the **knockoff** threshold is

       T = min{ t ∈ W : #{j : W_j ≤ −t} / (#{j : W_j ≥ t} ∨ 1) ≤ q },

   and the **knockoff+** threshold adds one to the numerator:

       T = min{ t ∈ W : (1 + #{j : W_j ≤ −t}) / (#{j : W_j ≥ t} ∨ 1) ≤ q }.

   `W` is the set of distinct nonzero `|W_j|`; `T = +∞` (select nothing) if the set is empty.
5. Select `Ŝ = {j : W_j ≥ T}`.

**The guarantees.** Knockoff (Theorem 1) controls a *modified* FDR,
`E[ #false / (#selected + q^{-1}) ] ≤ q` — close to the FDR when many variables are selected.
Knockoff+ (Theorem 2) controls the **FDR exactly**: `E[ #false / (#selected ∨ 1) ] ≤ q`. Knockoff+ is
always the more conservative of the two, and the paper says the `+1` "is necessary both theoretically
and empirically to control FDR in scenarios where extremely few discoveries are made" — which is this
lab's regime, so **knockoff+ is the variant to use here.**

The ratio in the threshold is the **knockoff estimate of the false discovery proportion**: the
negative-`W` count on the numerator stands in for the unobservable null count on the positive side,
and the substitution is conservative because strong real signals are mostly on the positive side. The
estimate is tight unless the signal is weak.

## Robustness evidence (qualitative only)

Replication in the Hou–Xue–Zhang / Jensen–Kelly–Pedersen sense does not apply; McLean–Pontiff decay
does not apply. The analogue is venue and uptake: a flagship theoretical-statistics journal, several
hundred citations on Crossref and several hundred more on Semantic Scholar, and the procedure has
spawned its own literature (the paper's own framing anticipates the extension to random designs; this
note covers only the fixed-design result it proves).

**The finding that matters most here is not the FDR bound — it is Section 3.1, the comparison against
a permutation construction.** A natural and widely used alternative is to build the decoy by
**permuting the rows** of `X`: `X^π_{i,j} = X_{π(i),j}`. This preserves the internal correlation
structure exactly (`X^πᵀX^π = XᵀX = Σ`) and breaks the association with `y`, so it looks like it
should work. It does not, and the paper is precise about why: when the features are centred,
`X^πᵀX^π = Σ` **but `XᵀX^π ≈ 0`**. The permuted columns are uncorrelated with the *original* columns,
whereas genuine nulls are correlated with the real signals. So the permuted decoys and the real nulls
behave completely differently in the fit, the exchangeability lemmas fail, and **"a permutation-based
construction can dramatically underestimate the FDP in cases where `X` displays nonvanishing
correlations."**

The measured size of the failure, in a design built to be mild — rows i.i.d. `N(0, Θ)` with unit
variances and **`Θ_ij = 0.3` for all off-diagonal entries**, `X ∈ R^{300×100}`, `y = 3.5(X₁ + … + X₃₀) + z`,
`z ~ N(0, I)`, 1000 trials, nominal `q = 20%`:

| method | realised FDR (nominal 20%) |
|---|---|
| knockoff | 12.29% |
| permutation | **45.61%** |

Two and a quarter times the nominal rate, from a uniform pairwise correlation of 0.3. The paper is
careful to generalise: "there are many ways in which the permuted features may be used to try to
estimate or control FDR, but in general such methods will suffer from similar issues arising from the
lack of correlation between the permuted and the original features." **The failure is structural —
it is the missing cross-correlation block, not the particular statistic.**

**Robustness to non-Gaussian noise** (Section 4.1), on the real HIV design matrix — sparse columns,
20 true signals, and residuals resampled from the empirical distribution of the real responses, whose
sample excess kurtosis of 9.24 corresponds to a `t` with about 4.65 degrees of freedom. Against a 20%
nominal level: knockoff 25.72%, knockoff+ 20.31%, BHq 25.47%, with power 63.5% / 60.7% / 69.4%.
Knockoff+ holds its level; the unmodified knockoff overshoots slightly. The paper calls this "an
extremely challenging scenario" because with sparse columns and heavy-tailed noise the marginal
statistic `X_jᵀz` is badly non-Gaussian and no central limit theorem applies. **So the method degrades
gracefully rather than catastrophically off its assumptions — but it does degrade, and the `+` variant
is what preserves the level.**

## Implementability here

**The sample-size condition is satisfied here, which is unusual and worth stating first.** The method
needs `n ≥ p` and its cleanest construction needs `n ≥ 2p`. The lab's learned candidates run 5–15
features against roughly a thousand eligible names per date over tens of month-ends, so `n ≫ 2p` by
orders of magnitude. **Fixed-design knockoffs are directly applicable to this panel**, with no need
for the random-design machinery the subsequent literature developed for `p > n`. That is the opposite
of the situation with `notes/2026-10-21-sure-independence-screening-marginal-vs-joint.md`, whose
asymptotic regime does *not* match the lab.

**The transferable finding is about the lab's own null, and it should be read carefully because it is
a tension, not a refutation.** Protocol v3's gate uses a **region-matched random-selection null**
that, per `experiments/learnings.md` [2026-10-14/15], "permutes a candidate's weight vector within
region". Section 3.1 says a permutation decoy fails to control false discoveries when the columns of
the design are correlated, because permutation destroys the cross-correlation block. **The two objects
are not the same thing and the result does not transfer mechanically**: the lab's null is a
distribution over *portfolios* used to place one candidate's Sharpe in a percentile, not a decoy
*design matrix* used to select variables, and `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md`
with `#260`-era material is where that null's own justification lives. What *does* transfer is the
diagnostic question, and it is cheap: **a permutation null is only as good as the dependence it
preserves between the permuted object and the thing it is standing in for.** The lab already has two
independent findings pointing at exactly this seam —

- [2026-10-14/15]: "null power is continuous in how concentrated the book is", with the null's
  percentile running 0% for the equal-weight pool up to 100% for a pure tilt. A null whose power
  depends on a property of the candidate is a null whose calibration is candidate-specific.
- The **engine issue filed 2026-10-18** (still a human decision): the null's replicas are not held to
  the eligibility boundary the candidate is held to, worth +0.005 to +0.017 of Sharpe *to the null*.

so the honest statement is that Section 3.1 is **third-party, independent evidence that
permutation-built nulls mis-estimate false-discovery rates in precisely the circumstance the lab's
own measurements already flag** (correlated columns — and this panel's names are correlated by
construction). It is a reason to take the standing engine issue seriously, not a reason to claim the
gate is wrong; the lab cannot edit the engine, and `CLAUDE.md` says so.

**Concrete, free use — and there is a clean one.** Use knockoff+ as the **feature-selection error
criterion** for the ISIS pass the companion note proposes, in place of or alongside stability
selection:

1. Build the feature matrix as the lab already does: features within-peer-group z-scored over
   eligible names, target the peer-demeaned forward 63-day return, frames on the price calendar (the
   `target.index`-as-clock trap of [2026-10-13/14]).
2. Construct knockoff columns from `Σ = XᵀX` of that feature block. With `p ≈ 7–15`, this is a
   `15 × 15` Cholesky — microseconds, nothing against the ~60s-per-call budget.
3. Fit the lasso path on the augmented `2p`-column block, walk-forward, deterministic (fixed
   `random_state`, single-threaded, per `CLAUDE.md`'s ML rules).
4. Compute `W_j`, apply the knockoff+ threshold at a pre-registered `q` (0.1 or 0.2, written down
   before looking).
5. Report the selected set. **An empty selected set is the informative outcome** and is the honest
   way to write down "no feature in this block survives FDR control" — which is what three closures
   already suggest, and which the lab currently states as a Sharpe number rather than as a
   selection-level result.

Step 5 is the value: it gives `program.md`'s charter question ("which feature groups carry signal")
an answer **in the units of the question** — a set of features with a bounded false-discovery rate —
rather than in the units of a portfolio.

**Two further honest uses, both as discipline rather than as a route to a candidate.** The
`W_j` sign symmetry is a **free instrument check** of the same family as the lab's standing method
rule (*"an object and its own negation cannot both be positive, so run the negation of every score
through any new statistic before reading it"*, [2026-10-20/21]): under the global null the `W_j`
signs should be roughly balanced, and a visibly lopsided sign distribution on a block the lab
believes to be null means the construction is wrong, not that signal was found. And **knockoff+'s
comparison against BHq is the right frame for the lab's existing multiple-testing stack**: BHq
controls FDR across *hypotheses given z-scores*, knockoffs control it across *variables given a
design*, and the deflated-Sharpe bar controls it across *trials*. Three different units; none
substitutes for another.

**Known pitfalls.**

- **Do not read Section 3.1 as "the v3 gate is invalid".** It is evidence about permutation decoys in
  variable selection. Stating it as more than that would be exactly the kind of cross-domain
  over-transfer `CLAUDE.md`'s hard rules warn against ("do not carry its constants into a new family
  by analogy"). If the lab wants to act on it, the act is the already-filed engine issue plus a
  measured check, not a claim.
- **Fixed design means fixed.** The guarantee treats `X` and `X̃` as fixed and takes expectations over
  the Gaussian noise only. The lab's feature matrix is rebuilt at each walk-forward refit, so the
  guarantee applies **per refit**, not across the sequence of refits. Aggregating selections across
  refits is a stability-path exercise (the companion note), not an FDR-controlled one.
- **Gaussian-noise assumption, and how far it bends.** The HIV simulation shows knockoff+ holding its
  level at an excess kurtosis of 9.24 while the unmodified knockoff overshoots. Cross-sectional equity
  returns are heavy-tailed, so **use knockoff+ and expect the realised rate to sit at rather than
  under the nominal one.**
- **Power, not just level.** `s_j` should be as large as `diag{s} ⪯ 2Σ` allows; a decoy too similar to
  its original destroys power silently while keeping the level. With a visibly collinear feature block
  — and [2026-10-17/18] and [2026-10-20/21] F5/F6 document several of the lab's features collapsing
  onto the volatility axis and the slope — `Σ` is near-singular in places, `s` is forced small, and
  **power will be poor exactly where the features are redundant.** That is the method telling the
  truth about the block, and it is the same message as the illusion-of-sparsity note's.
- **It does not create signal.** Same caveat as every other note tonight: FDR control on a null block
  returns the empty set.

## Related

- Tonight's other three: `notes/2026-10-21-sure-independence-screening-marginal-vs-joint.md` (the
  screen whose output this bounds), `notes/2026-10-21-stability-selection-subsampling-error-control.md`
  (the alternative error criterion — PFER/FWER by subsampling rather than FDR by decoys; stability
  selection needs exchangeability of the noise variables, knockoffs need `n ≥ p` and Gaussian noise,
  so neither dominates), and
  `notes/2026-10-21-illusion-of-sparsity-selection-versus-shrinkage.md` (whether a sparse selected set
  is the right object for cross-sectional equity returns at all — which, if its answer is right, is a
  limit on what any of these three can deliver here).
- `notes/2026-10-15-random-portfolios-as-the-null-of-no-skill.md`,
  `notes/2026-10-15-random-portfolio-inference-concentration-of-measure.md` and
  `notes/2026-10-15-random-weight-indices-and-the-equal-weight-centre.md` are the folder's material on
  the lab's own permutation null; this note is the first to supply an *outside* result about what a
  permutation decoy fails to preserve.
- `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-08-24-multiple-testing-haircut.md`,
  `notes/2026-09-01-multi-signal-overfitting-critical-t.md` and the 2026-09-15 post-selection cluster
  are the trial-level multiple-testing stack; the unit here is the variable, not the trial.
- `experiments/learnings.md` [2026-10-14/15] (null power continuous in concentration) and the
  **engine issue of 2026-10-18** are the lab's own observations about its null that this note's
  Section 3.1 result speaks to.
