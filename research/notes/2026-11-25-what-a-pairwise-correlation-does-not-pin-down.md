---
title: "What a PAIRWISE CORRELATION does NOT pin down — the closed-form competence of a correlated panel under one admissible joint distribution, a second admissible one under which correlation has NO effect at all, the feasibility ceiling c ≤ 2/(n−1), and the exact collapse M(p,1) = p"
authors: Kaniovski
year: 2010
venue: "Theory and Decision 69(3), 453–468 (DOI registered 2008 as online-first). Peer-reviewed; same journal as the Grofman–Owen–Feld review filed tonight (tier 1 within decision theory)."
url: https://doi.org/10.1007/s11238-008-9120-4
citations: "39 (Crossref `is-referenced-by-count`, checked 2026-11-25); 59 (Semantic Scholar by DOI, same date). Modest in absolute terms; the tier below rests on venue, on the content being theorems, and on the result being a negative one that cannot be flattered by a sample."
sample_period: "n/a — two theorems, four corollaries, six numerical examples with invented (p, c) pairs, and a linear program. No data."
markets: "None."
tier: "B+. Peer-reviewed and analytic, and the central finding is an identification result that is as strong as its algebra. Held below A on two counts: citation count is modest, and — the limit that matters — **what was read is the author's own September 2008 working version, not the typeset journal article**, so section numbering and any late revisions are unverified. The theorems' statements were cross-checked against the working paper's own abstract and against its proofs, both present in full."
validation_overlap: false
published_post_2018: false
read: "Full text of the working version, 24 pp., 198 KB PDF from the author's institutional page (WIFO), HTTP 200 first request; `pdftotext -layout` → 56 KB of text, 278 instances of ` the `, parenthesis balance 209/213, no ASCII shift, title line verified, proofs of both theorems present and followed. Mathematical notation extracts cleanly except for binomial-coefficient sub/superscripts, which print as `C_{n-2}^{2}` style runs; every coefficient quoted below was read from the proof's own algebra as well as from the theorem statement."
access_note: "`<author>.wifo.ac.at/fileadmin/pdf/<slug>.pdf` — an author page inside an institute's domain, surfaced directly by a title search. Worth recording as a channel: an economics-institute staff page (WIFO here) can host a complete working version of a closed Springer article. The Springer landing page for the DOI was not needed; Crossref supplied all metadata including the citation count, per the standing rule."
---

## Why this source is here

It is the adversarial half of tonight's vein, and it changes the answer. The [2026-11-24] aim asked
for *the effective number of independent rankers* as a closed-form function of **a correlation the
lab already measures**. The two Grofman-school notes filed tonight give weights and a discount in
terms of a *structural* dependence parameter (a common-factor loading). This paper asks the
question the aim actually posed — what does a panel's **correlation matrix** tell you about its
competence? — and the answer is: *by itself, almost nothing.* Criterion (i): explicitly correlated
judges. Criterion (ii): a closed form, given. Criterion (iii): the `c → 1` limit, exact. Criterion
(iv): needs only `p` and `c`. And then it shows the closed form is **not identified** by `(p, c)`.

## Mechanism

**The setting.** A homogeneous panel of `n` judges, each correct with probability `p` (`q = 1 − p`),
every **pair** of correct-vote indicators correlating at the same `c` (Pearson). Decision by simple
majority. `M_n(p, c)` is the probability the panel is collectively correct.

**The identification problem, which is the paper's premise and the thing to carry.** Computing
`M_n(p, c)` requires a **joint** distribution over the `2^n` voting profiles. The marginal
probabilities and the pairwise correlations **do not determine one**: the distributions consistent
with given `(p, c)` form a *convex set* in `2^n`-dimensional space. Bahadur's (1961) representation
characterises the solution set using **higher-order** correlation coefficients, and estimating those
needs far more data than anyone has. So one must either pick a distribution or compute bounds, and
the choice is where the answer comes from.

**Theorem 1 — the closed form, under the "B-solution" (the Bahadur / Lazarsfeld pairwise-only
representation, exact when all higher-order correlations are zero).**

```
M_n^B(p, c)  =  M_n(p, 0)  +  c · n(n-1) · (0.5 - p) · C(n-2, (n-2)/2) · p^((n-1)/2) · q^((n-1)/2)
```

where `M_n(p, 0)` is the ordinary independent-judge Condorcet probability (the binomial tail). The
correction is **linear in `c`**, and for a competent panel (`p > 0.5`) the factor `(0.5 − p)` is
negative, so positive correlation *subtracts*. The four corollaries:

- **1.1** Negative correlation raises a competent panel's competence; positive correlation lowers
  it. (`c₁ < c₂ < 0` and `c₂ > c₁ > 0` both give `M^B(p,c₁) > M^B(p,c₂)`.)
- **1.2** At `p = 0.5` correlation has **no** effect — a randomising panel is unaffected.
- **1.3** For `c > 0`, higher individual competence still gives higher collective competence
  (`dM^B/dp > 0`), established using the feasibility bound below.
- **1.4** For `c > 0`, **the effect of a larger panel is ambiguous**: enlargement can *reduce*
  competence up to a certain size and becomes beneficial only beyond it. The sign hinges on
  `F(n) = n − 3/(4pq)`.

**The feasibility ceiling, and it is the sharpest practical statement in the paper.** For the
B-solution to be a distribution at all (non-negative probabilities), Bahadur's exact bounds are

```
-2q / (p·n(n-1))   ≤   c   ≤   2pq / ((n-1)pq + 0.25 - γ),       γ = min_t {[t - (n-1)p - 0.5]²} ≤ 0.25
```

and the paper notes the simple consequence `c ≤ 2/(n − 1)` for `c > 0`. The asymmetry matters:
positive `c` is `O(n⁻¹)`, negative `c` is `O(n⁻²)`, and **`|c| → 0` as `n → ∞`**, i.e. *in a large
homogeneous panel each pair of judges can only be weakly dependent.* A strongly correlated large
panel is not a panel with a bad correlation number — it is a panel this model cannot represent.

**Theorem 2 — the refusal, under the "Q-solution" (the distribution closest to a benchmark in a
quadratic metric, obtained by regularisation).**

```
M_n^Q(p, c)  =  M_n(p, 0)      for every c
```

*The probability of a homogeneous panel being correct under simple majority is completely
independent of the correlation coefficient.* Positive correlation raises the probability of all
broad coalitions including the wrong ones, and under majority rule the two effects cancel exactly.
The paper's own gloss on what this means:

> "an empirically relevant second-order dependence structure such as a correlation matrix between
> the votes conveys little information about the sensitivity of the Condorcet probability to
> correlation. The possibilities range from completely insensitive, to very sensitive."

The invariance is fragile in a specific, useful way: the examples show it needs **simple majority
and homogeneity**. For a heterogeneous panel, or any supermajority rule, correlation does move the
answer — and in the paper's examples positive correlation *helps* under a supermajority (while the
supermajority itself lowers the probability of a correct verdict).

**The exact degenerate limit (Section 4.1), which is criterion (iii) discharged.** Joint
distributions typically fail to exist for very high correlation, but `c = 1` is a special case that
does exist: all judges vote together, correct with probability `p`. Hence

```
M_n(p, 1)  =  p
```

— *the collective competence of a perfectly correlated panel equals that of a single judge.* And
the mirror statement, which rules out a tempting construction: **a joint distribution does not exist
for perfect negative correlation** with `n ≥ 3`. "Three jurors cannot be mutually contrarian."
Positive correlations reflect common rather than contrarian tendencies, and they make
high-consensus outcomes more probable than independence would.

**The bounds approach (Section 6) — what to do instead of picking a distribution.** Solve two
linear programs over the convex set of distributions consistent with `(p, c)`:
`M̲_n(p,c) = min_π M_n` and `M̄_n(p,c) = max_π M_n`. These are the honest limits of what the
panel's competence can be given what is known. In the paper's six examples the minimising and
maximising solutions differ **in their third-order correlations**, which is exactly where the
unidentified information lives. Any convex combination of the two is also admissible.

## Construction recipe

This is a screen and an interpretation rule, not a portfolio construction.

1. **Convert each lead's cross-sectional skill to a competence `p`** (the `#518` regime map).
2. **Measure `c`** as the average pairwise correlation of the leads' *binarised* verdicts
   (above/below the book's cut), not of their raw scores — the model is about vote indicators.
3. **Check feasibility first.** If `c > 2/(k − 1)` for the panel's own `k`, the pairwise-only
   representation does not exist and no closed form applies. Report that and stop.
4. **If feasible, bracket rather than estimate.** Compute `M_k(p, 0)` (free, a binomial tail),
   `M_k^B(p, c)` from Theorem 1 (the pessimistic end for `c > 0`), and note `M_k^Q = M_k(p, 0)`
   (the no-effect end). The pair is the interval the correlation alone supports. If a decision
   flips inside that interval, the correlation is not enough information to make it.
5. **Use `M_k(p, 1) = p` as the floor-of-usefulness test**: a composite of leads cannot be worth
   building unless it is expected to land meaningfully above the best single lead's `p`.

## Robustness evidence (qualitative only)

Theorems with proofs given in full, so robustness is about the assumptions, and they are exactly
where the result bites: homogeneity (equal `p`, equal pairwise `c`), simple majority, and a
dichotomous choice. The paper's own numerical examples probe each, and the invariance of Theorem 2
breaks under heterogeneity and under supermajority rules — so the "correlation does not matter"
reading must not be over-generalised, and this note does not.

The paper builds on and corroborates an existing line (Bahadur 1961; Boland 1989; Berg 1993; Ladha;
Nitzan) rather than standing alone — its own abstract says both theorems "corroborate existing
results". The corroboration is of the *directional* claims (positive dependence hurts, negative
helps); the identification result is the novel part and is the part this folder is using.

Not independently replicated in this folder: Boland (1989), Berg (1993) and Ladha (1992) are cited
here as the antecedents and **none was obtained tonight**; they are recorded as named pointers,
nothing more.

## Implementability here

**The reading rule this produces, and it is the night's main product.** The lab's standing instinct
— and the shape of the [2026-11-24] aim — is to convert a measured correlation between leads into
an *effective number of independent leads* and then into a weight. **This source says that number
is not identified by the correlation.** Two equally admissible joint distributions consistent with
the same `(p, c)` give (a) a competence that falls linearly in `c` and (b) a competence that does
not depend on `c` at all. What is missing is third- and higher-order dependence, which the lab
cannot estimate at its sample sizes. So: a correlation between leads is grounds for a **refusal**
(do not count two correlated leads as two opinions) and for **bounds**; it is not grounds for a
calibrated weight. Where the lab wants a weight, it should come from the *structural* loading `α` of
the opinion-leader note, which is a modelled quantity with a stated limit, not from `c` plugged into
a formula.

**The feasibility ceiling applied to the lab's own numbers, which is a free and quite sharp
screen.** `learnings.md` records an inter-signal ensemble killed at rank correlation **0.89** and a
promoted blend whose legs correlate **0.66**. Taking those as binarised-vote correlations (they are
not, strictly — see below), the ceiling `c ≤ 2/(k − 1)` is satisfied only for `k ≤ 3` at `c = 0.89`
and for `k ≤ 4` at `c = 0.66` — and `2/(k−1)` is only a necessary consequence of the exact bound, which is tighter, so even those are optimistic. **A panel of five or more leads correlating at 0.66 is outside the
model's feasible set entirely**, meaning the dependence is dominated by higher-order structure and
every "effective number of judges" calculation on it is a category error. That is the formal version
of the lab's own measured result that breadth only pays when it comes from decorrelated sources.

**What is free.** Steps 1–4 above are arithmetic on stored scores: a binomial tail, one closed-form
correction, one inequality. No trial, no holdout, no new data.

**What does not transfer, stated plainly.**
- `c` here is the correlation between **binary correct/incorrect indicators**. The lab measures rank
  correlation between continuous scores and correlation between active return series. These are
  different objects with different magnitudes, and the conversion is not supplied by this paper. Any
  use of 0.89 or 0.66 in the ceiling test must say that it is a substitution, as this note does.
- Homogeneity (all leads equally competent, all pairs equally correlated) is false for the lab's
  leads. The paper's Example VI shows the Q-invariance fails for heterogeneous panels — so neither
  end of the bracket is exactly right for a real panel, and the bracket is indicative.
- The whole model is a *dichotomous* choice. A long-only book's membership decision is dichotomous
  per name (`#375`, `#376`), which is why the transfer is legitimate at all — but the names are not
  one decision, they are ~1,000 correlated ones, and nothing here handles that multiplicity.
- No performance figure, no period claim, and no return expectation is recorded or implied.

## Related

- `notes/2026-11-25-the-opinion-leader-model-and-the-bloc-weight-discount.md` — the structural
  alternative this note points to: a dependence parameter that *is* a model, versus a correlation
  that is not identified.
- `notes/2026-11-25-optimal-weights-for-judges-of-unequal-competence.md` — Theorem III there is the
  companion refusal test (whether any weighted rule is optimal under dependence); this note is why
  the `p(k)` table, not the correlation, is the thing to tabulate.
- `notes/2026-11-24-when-a-positional-rule-is-the-right-aggregator.md` (`#518`) — the independent-
  judge derivation whose assumption is priced here.
- `notes/2026-11-24-rank-aggregation-positional-versus-pairwise.md` (`#522`(c)) — the anti-candidate
  this note upgrades from a worry to an identification result.
- `notes/2026-09-16-clustering-trials-onc-effective-number-of-trials.md` and
  `notes/2026-09-16-effective-number-of-independent-tests-eigenvalue-estimators.md` — the folder's
  existing "effective number" machinery, which is about *tests*, not judges; this note is the reason
  not to reuse it for aggregation weights.
