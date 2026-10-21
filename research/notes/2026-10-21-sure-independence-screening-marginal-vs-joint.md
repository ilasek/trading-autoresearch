---
title: "Sure Independence Screening for Ultrahigh Dimensional Feature Space" — the conditions under which ranking predictors by their *marginal* correlation keeps every important one, the three ways it fails, and the iterated-residual procedure that repairs it
authors: Fan, Lv
year: 2008
venue: Journal of the Royal Statistical Society Series B (Statistical Methodology) 70(5), 849–911 (venue tier 1 — with invited discussion, which is JRSS-B's marker for a read paper)
url: https://doi.org/10.1111/j.1467-9868.2008.00674.x
citations: 2118 (Crossref `is-referenced-by-count`, checked 2026-10-21); 2802 (Semantic Scholar by DOI, same date). Both indices resolved on the first call. Semantic Scholar returns the record under the title *"Discussion of 'Sure Independence Screening for Ultra-High Dimensional Feature Space'"* — the DOI is right and the citation count is the article's, but the title field is the bound discussion, which is a tell worth keeping: a Semantic Scholar title mismatch on a JRSS-B DOI is an indexing artifact, not a wrong DOI.
sample_period: none — asymptotic theory plus synthetic simulations, with one microarray benchmark (leukemia gene expression, 38 training / 34 test subjects) as the real-data illustration. No market data of any period appears in it.
markets: none
tier: A
validation_overlap: false
published_post_2018: false
read: full text of `arxiv.org/pdf/math/0612857` (43 pp., 467 KB → 137 KB of clean text via `pdftotext -layout`, 802 instances of `" the "`, no ASCII shift, title line verified against the Crossref record). This is the authors' v2 of August 2008, i.e. the article without the bound JRSS-B discussion; every claim below is from the article's own text, and nothing is attributed to discussants.
---

## Mechanism

No economic mechanism. This is the **statistical layer directly under `program.md`'s charter
question for `statistical-learning`** — "which feature groups carry signal" — and specifically under
the *procedure* by which that question gets answered. It is the first note in this folder about
**selection** as opposed to **shrinkage**: the folder holds eight notes that mention the lasso and
eight that mention sparsity, and every one of them treats a penalty as a way to *estimate* a
coefficient vector. None asks the prior question of how a predictor gets into the candidate set in
the first place, or what a screen that puts it there can and cannot see.

The object of study is the cheapest possible screen. Standardise every predictor column to mean
zero and unit sample standard deviation, standardise the response, and compute

    ω = Xᵀ y

which is the vector of **marginal correlations** of each predictor with the response. Rank the
`|ω_j|`, keep the top `d`, discard the rest. Fan and Lv call this **Sure Independence Screening**
(SIS) — "independence" because each feature is used *on its own* to decide how useful it is. Its
cost is one `p × n` by `n` matrix-vector product plus a partial sort: `O(np)`.

The paper's contribution is to say exactly when this works. Define the **sure screening property**
as

    P(M* ⊆ M_γ) → 1    as n → ∞,

where `M*` is the set of truly nonzero coefficients and `M_γ` the set the screen keeps. "Sure
screening" is a statement about **not losing anything**, not about precision: the kept set may be
far larger than `M*`. The rationale the paper gives for why a *marginal* object should have this
property at all is a nice one and is worth carrying: componentwise regression is the `λ → ∞` limit
of ridge regression, `λω^λ → ω`, so a marginal correlation screen is the **maximally shrunk**, and
therefore minimum-variance, member of the ridge family. Ranking by marginal correlation is ranking
by the noisiest-signal-but-least-noisy estimator available.

## Construction recipe

**SIS.** Standardise all columns. Compute `ω = Xᵀy`. Keep the `d` largest `|ω_j|`. The paper's
recommended `d` is `n − 1` or `n / log n`; its own simulations and the leukemia analysis use
`d = [n / log n]` or `[2n / log n]`, and it notes the results "are not very sensitive to the choice
of `d` as long as it is not too small". Then fit a moderate-dimensional penalised model (SCAD,
adaptive lasso, Dantzig selector — the paper studies all three) **on the surviving `d` columns
only**. Note the screen uses only the *order* of the `|ω_j|`, so it is invariant to scaling.

**How large must `d` be?** This is the part worth transcribing precisely, because it runs opposite
to intuition. Theorem 1 holds under four conditions with two rate parameters: `κ`, which indexes
how weak the smallest true signal is (`min_{i∈M*} |β_i| ≥ c₂ n^{-κ}`), and `τ`, which indexes
collinearity (`λ_max(Σ) ≤ c₄ n^τ`). The theorem needs `2κ + τ < 1`, and the reduced model size must
satisfy `d = n^{θ*}` with **`θ* > 2κ + τ`**. The paper states the reading itself:

> "The weaker the signal, the larger the `κ` and hence the larger the required model size.
> Similarly, the more severe the collinearity, the larger the `τ` and the larger the required
> model size."

And `κ < 1/2` is required outright, "since we can not detect signals that of smaller order than
root-`n` consistent". **So a marginal screen's guarantee demands that you keep *more* candidates
when the signals are weaker and the predictors more correlated, and it offers nothing at all once
the signal is below root-`n` detectability.**

**The three failure modes** (the paper's own list, opening Section 4.1):

1. An **unimportant** predictor highly correlated with an important one can outrank a genuinely
   important predictor that is only weakly related to the response.
2. An **important predictor that is marginally uncorrelated but jointly correlated** with the
   response *cannot be picked up by SIS* and never enters the model. Condition 3 of the theorem
   exists precisely to assume this away — the paper says so in as many words: "This condition rules
   out the situation in which an important variable is marginally uncorrelated with `Y`, but jointly
   correlated with `Y`."
3. **Collinearity** among predictors independently degrades selection (Condition 4 assumes
   `λ_max(Σ)` does not grow too fast, which "rules out the case of strong collinearity").

**ISIS — the repair, and it is an iterated-residual procedure.** The essence is "iteratively apply a
large-scale variable screening followed by a moderate-scale careful variable selection":

1. Run SIS to `d = [n / log n]` survivors, then a penalised fit (SCAD or lasso) on those survivors;
   call the selected set `A₁`.
2. Regress `Y` on `A₁` and take the **residuals**. Treat the residual vector as the new response.
3. Apply step 1 to the **remaining `p − |A₁|` predictors**, against the residual response, giving
   `A₂`.
4. Repeat until `|A| = |∪A_i|` is just under `n` (the paper takes the largest `ℓ` with `|A| < n`).
5. Run a final moderate-scale penalised fit (SCAD / lasso / Dantzig) on `A`.

Why the residual step fixes modes 1 and 2 at once: the residuals are orthogonal to everything in
`A₁`, which (a) strips the borrowed correlation that let a collinear impostor rank highly, and
(b) *gives* correlation to the predictors that were marginally null only because of the variables now
in `A₁` — "after variables in `A₁` entering into the model, those that are marginally weakly
correlated with `Y` purely due to the presence of variables in `A₁` should now be correlated with
the residuals." If `|A_i| = 1` at every step, ISIS degenerates to matching pursuit / greedy
selection; with `|A_i| > 1` it is strictly more than that.

**Two cheaper repairs the paper also offers,** both relevant here because they do not need the
iteration: (i) **group the predictors** into small disjoint blocks (its example is blocks of five)
and screen the *groups*, "in this way there is less chance of missing the important variables by
taking advantage of the joint information among the predictors"; and (ii) **transform the predictors
to weaken their mutual correlation before screening** — either subject-matter differencing (its own
example is weights at ages 2, 9, 18 replaced by `(w₁, w₂−w₁, w₃−w₂)`, and it names financial time
series explicitly: "Differencing can significantly weaken the correlation among those variables"), or
statistically, by clustering correlated predictors and replacing each cluster with sparse principal
components.

## Robustness evidence (qualitative only)

**Replication status.** The Hou–Xue–Zhang / Jensen–Kelly–Pedersen sense of replication does not
apply — there is no anomaly and no cross-section of returns here. The relevant analogue is that this
is a *read paper* at JRSS-B, published with invited discussion, and one of the most-cited
methodological results in high-dimensional statistics on both indices. McLean–Pontiff decay does not
apply either: a screening procedure has no premium to arbitrage away.

**Simulation evidence, and it is the sharpest thing in the paper.** Three designs, 200 datasets
each, `X ~ N(0, Σ)` with `σ_ii = 1` and `σ_ij = ρ` off-diagonal, scoring the frequency with which
the kept set contains the whole true model. All three methods are made to select the same number of
variables so the comparison is fair.

- **Design I**, `Y = 5X₁ + 5X₂ + 5X₃ + ε`, i.e. all three signals marginally correlated with `Y`.
  SIS does well when `n` is adequate and degrades with `ρ` and with `p`; the lasso is somewhat
  better; the gap closes to nothing by `n = 50`. **Nothing here is alarming.**
- **Design II** adds `X₄` with correlation `√ρ` to every other predictor and coefficient `−15√ρ`,
  constructed so that **`X₄` is marginally uncorrelated with `Y` while being one of the four true
  predictors.** At `p = 1000, ρ = 0.5`, the frequency of recovering the true model is **0.000 for
  SIS and 0.000 for the lasso at `n = 20`, `n = 50` and `n = 70` alike**, while **ISIS is 1.000 at
  all three**.
- **Design III** adds a fifth predictor whose contribution to the response is the *same size as the
  noise*, so that it ranks below pure-noise predictors on marginal correlation. Again at
  `p = 1000`: SIS 0.000, lasso 0.000, ISIS 1.000 at every `n` tried.

Two things to take from Designs II–III. First, the failure is **not a small-sample or
low-power effect** — more data does not fix it, because the quantity being ranked does not contain
the information. Second, and this is the load-bearing one, **the one-pass penalised joint fit fails
exactly as completely as the marginal screen does.** Only the *iterated-residual* procedure finds
the variable. A lasso or ridge over the whole candidate block is not a remedy for mode 2.

**The spurious-correlation result,** Section 1.3, independent of everything above and worth its own
line. With `p` genuinely independent standard normal predictors and `n = 60`, the distribution of the
**maximum absolute sample correlation among the predictors** is concentrated roughly between 0.55 and
0.75 for `p = 1000` and shifts higher again for `p = 5000` (500 simulations). The predictors are
independent by construction. The paper notes the multiple canonical correlation between *groups* of
predictors is larger still, because there are already `O(p⁵)` ways of choosing a 2-against-3
grouping. So in any wide candidate set, both the largest marginal correlation *with the response*
and the largest correlation *among predictors* are large for free.

## Implementability here

**State the regime honestly first, because it is not the paper's.** Fan–Lv is about `p ≫ n`
("ultrahigh dimensional" means `log p = O(n^ξ)`). The lab's learned candidates are the opposite
corner: the 2026-10-13 ridge screen had **seven** features against roughly a thousand eligible names
per date and 62 scored month-ends, and the 2026-10-17/18 gradient-boosting variant and the
2026-10-19/20 pairwise ranker used 5–15. The sure-screening *theorem* therefore has no work to do on
this panel, and nothing below leans on it. **What transfers is the failure-mode taxonomy and the ISIS
construction, both of which are finite-`p` facts about the difference between marginal and joint
information and hold at `p = 7` exactly as at `p = 1000`.**

**The tension, and it is a live one.** `experiments/journal.md` [2026-10-20/21], idea 2 for the next
session, adopts as a standing refusal rule: *compute each object's within-region rank IC, multiply by
3.37 for a ceiling on train skill, and refuse the candidate if that ceiling is under ~0.03.* A rank IC
of a single score against forward returns **is a marginal screen** — it is `ω_j` in rank space — and
Condition 3 of Theorem 1 is precisely the assumption that makes such a screen safe. The lab has
therefore adopted, as a rule, a procedure whose one documented catastrophic failure mode is a
predictor that is **marginally null and jointly important**, and has not checked whether that mode is
present. Three further points sharpen rather than soften this:

- **The lab's own closure of the family was measured with the two procedures that both fail.**
  `experiments/learnings.md` [2026-10-13/14] reports that a walk-forward ridge over seven
  individually-null features is itself null (rank IC +0.0066, t +0.28), and reads this as "the legs
  give a combiner little to combine". In Design II the one-pass lasso over the full candidate set
  recovers the true model **0% of the time** at every sample size — so "a one-pass penalised fit over
  these features is null" is **not** evidence that no marginally-null-but-jointly-important feature is
  among them. That inference is exactly the one Fan–Lv's Design II is built to break. This is a
  tension with the *inference*, not with the *measurement*: the ridge number is what it is, and the
  2026-10-17/18 and 2026-10-19/20 closures (nonlinear capacity, ordinal loss) are untouched by this
  note because they vary the learner and the objective, not the screen.
- **The direction of the required-`d` result is the opposite of the lab's rule.** The theorem says a
  weaker signal requires keeping a *larger* candidate set. The refusal rule drops candidates *because*
  their marginal signal is weak. Both can be right — they answer different questions (is this object
  worth a trial on its own, versus might this object matter inside a fit) — but the rule should not be
  read as evidence about the second question, and the journal's own phrasing ("a refusal rule only",
  "it can refuse and it cannot qualify") is already the right shape; this note adds *what* it cannot
  refuse.
- **`κ < 1/2` is a hard ceiling that applies to the lab directly.** The rank IC screens are computed
  on `n ≈ 62` scored dates. Signals below root-`n` order are undetectable by *any* of this machinery,
  marginal or joint, which is the same statement as the lab's own noise floor (train skill scattered
  at sd 0.025, [2026-10-20/21] F8) arriving from theory.

**Concrete adaptation — and it is free, which is the point.** The lab already holds the ingredients:
a walk-forward harness (`strategies/lib/walkforward.py`), a feature block whose members are
individually priced, and a rank IC statistic. **One ISIS pass over the existing block costs no trial
and is the identifying test for mode 2.** Recipe, in the lab's own units:

1. Take the existing feature block, within-peer-group z-scored, and the peer-demeaned forward
   63-day target, on the price calendar (the `target.index`-as-clock trap recorded in
   [2026-10-13/14] applies unchanged).
2. Fit the walk-forward penalised model on the **single highest-|rank IC| feature alone**. Take the
   residual of the target against its fitted score.
3. Re-score **every remaining feature's rank IC against that residual**, not against the raw target.
4. If a feature's |rank IC| against the residual is materially larger than against the target, mode 2
   is present in this block and the lab's marginal refusals are not safe. If no feature moves, mode
   2 is absent and **the existing closure is strengthened, not weakened** — which is why this is worth
   running whichever way it comes out.
5. Iterate while something moves; stop when nothing does. Then price the final fitted score the
   ordinary way (within-region rank IC, × 3.37, the standing screen triple plus the volatility-ratio
   column of [2026-10-13/14] and the Sharpe-not-bps correction of [2026-10-20/21]).

Step 3 is the whole note in one line, and it is roughly the cost of the IC board the lab already
builds.

**Two cheap variants worth the same pass**, both from the paper rather than from analogy.
**Grouped screening**: score the lab's features in small blocks rather than singly, which is one
regression per block and is what "there is less chance of missing the important variables" means
operationally. **Decorrelating transform before screening**: the paper names differencing of
financial series specifically, and the lab's feature block is visibly collinear in the way mode 1
describes — [2026-10-17/18] records that average residual correlation reads rank −0.543 to 126-day
volatility and a correlation score standardised by own volatility "is still a volatility score with
the sign flipped", and [2026-10-20/21] F5/F6 found the spread amplitude and the group-explained share
to be "the slope and the volatility axis in costume". A screen run on a cluster-and-sparse-PCA
transform of the block, or on differences between features rather than levels, is a different ranking
of the same information.

**Known pitfalls.**

- **The test is one-sided in the same way every other screen here is.** ISIS can *find* a
  jointly-important feature; it cannot prove one is absent. If the features genuinely carry nothing,
  ISIS returns nothing, and that is consistent with the lab's measured nulls. Do not write the
  result up as "the features are vindicated" or "the features are refuted" — it discriminates one
  specific failure mode and nothing else.
- **ISIS is a selection procedure fitted on data, so it multiplies the search.** Every iteration is
  another look at the same train window. Under protocol v3 the deflated-skill bar counts recorded
  *trials*, not free screens, so a free ISIS pass does not raise it — but the selected feature set is
  then a *selected* object, and `notes/2026-09-15`'s post-selection material and the companion notes
  written tonight (`stability-selection`, `knockoff-filter`) are what bound the damage. Run the
  stability-selection wrapper over the ISIS pass rather than reporting a single selected set.
- **`O(np)` is the screen's cost, not the procedure's.** ISIS runs a penalised fit per iteration. At
  the lab's `p`, this is nothing; the binding cost remains the walk-forward refit count under the
  ~60s-per-call budget in `CLAUDE.md`.
- **Do not import the simulation's effect sizes.** Design II's `−15√ρ` coefficient is constructed to
  make the marginal correlation *exactly* zero. Real marginal nulls are approximate, so the real
  failure is partial — a feature whose marginal rank IC is depressed rather than annihilated. The
  mode is a direction, not a magnitude.

## Related

- The three other notes written tonight complete the chain this one starts: how to make a selection
  reproducible and error-controlled (`notes/2026-10-21-stability-selection-subsampling-error-control.md`),
  how to bound the false-discovery rate of a selected set and why a *permutation* construction
  cannot do it (`notes/2026-10-21-knockoff-filter-fdr-control-vs-permutation.md`), and whether a
  sparse selection is the right object at all on cross-sectional equity data
  (`notes/2026-10-21-illusion-of-sparsity-selection-versus-shrinkage.md`).
- `notes/2026-08-29-machine-learning-cross-section-comparative.md` and
  `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` are the folder's two
  sources that report *which* characteristics survive a selection; neither describes the selection
  machinery, which is what this note supplies.
- `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md` and
  `notes/2026-09-26-large-factor-models-aipt-complexity.md` are the shrinkage side of the
  selection-versus-shrinkage axis that tonight's illusion-of-sparsity note names explicitly.
- `notes/2026-09-26-virtue-of-complexity-return-prediction.md` and the random-Fourier-feature
  identity recorded in `SUMMARY.md` (`#154`) say what an overparameterised fit *is*; this note says
  what gets into it.
- `experiments/learnings.md` [2026-10-13/14], [2026-10-17/18] and [2026-10-19/20] are the lab's three
  closures of `statistical-learning`, all attributed to the features. The tension stated above is
  with the inference from the first of them only.
