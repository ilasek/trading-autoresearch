---
title: "The THRESHOLD MAP in both directions — the exact bivariate-normal formula taking a score correlation and a cut depth to the correlation of the two top-K membership indicators, the proof that it is strictly increasing and therefore uniquely invertible, the feasibility bounds a deep cut imposes on NEGATIVE agreement, and the positive-semidefiniteness failure that breaks the map for more than two judges"
authors: Wong, Ben Chaouch
year: 2026
venue: "arXiv preprint (cs.CE), 2607.16801v1. Not peer-reviewed; authors give their affiliation as 'Independent researcher'. Venue tier 4 by this folder's rubric. The classical results it restates are attributed in it to Emrich & Piedmonte (1991, The American Statistician), Qaqish (2003), Prentice (1988) and Chaganty & Joe (2006) — none of which was obtained or read."
url: https://arxiv.org/abs/2607.16801
citations: "0 (Crossref has no record of the preprint; Semantic Scholar not queried for a July-2026 arXiv item, checked 2026-11-26). Antecedent counts not resolved — see tier note."
sample_period: "n/a — analytic derivations plus synthetic numerical illustrations. No market data of any kind in the paper."
markets: "None. The paper's framing application is a generic portfolio of binary-outcome 'programs' (risk modelling), with no instruments, no prices and no dated sample."
tier: "C. A preprint with no citations and no replication is Tier C however clean its mathematics, per `research/README.md`. It is used here for ONE purpose only — the statement and the derivative of the threshold map, which is elementary, self-checking and was verified numerically in the scratchpad against the independently-sourced median special case in the companion MacCallum note (agreement to four decimals at three values of rho). No claim in this note rests on the paper's own contribution (its linear-programming feasibility machinery), and no claim rests on its unread antecedents beyond the attribution of the formulas."
validation_overlap: false
published_post_2018: true
read: "Full text, 574 KB PDF from arXiv, HTTP 200 first request; `pdftotext -layout` → 114 KB of text, 377 instances of ` the `, zero `( )` dropout, no ASCII shift, title line checked. Equations (3), (8) and (9) and the derivative of `g_ij` were read directly; the appendices (numerical illustration, LP formulations) were skimmed and are not used."
access_note: "arXiv, trivially. Recorded because the *route in* was the arXiv API over https (`export.arxiv.org/api/query?search_query=all:tetrachoric`) after four named classical channels went dark in the same session — a keyword query against the arXiv API is a cheap way to find a modern restatement of a closed classical result, and a restatement whose algebra is self-checking is worth more than an unobtainable primary."
---

## Why this source is here

The [2026-11-25] aim named the quantity it needed — the probability that two correlated leads put the
same name above a top-`K` cut, as a function of the score correlation `ρ` **and the depth of the
cut** — and said the classical answer "exists and is arithmetic". Four classical channels for it went
dark in this session (see `## Access` in `SUMMARY.md`'s coverage row). This preprint restates the
map and, more usefully, supplies three things the aim did not ask for and the lab needs:

- the **general** form of the map, for arbitrary and *unequal* cuts, not only the median;
- a one-line **proof that it is strictly increasing**, hence that a measured agreement rate pins
  down a unique score correlation — which is the exact point on which Kaniovski's refusal (`#523`)
  does *not* bite, and the reason why is worth stating precisely;
- the **failure mode beyond two judges**: a set of pairwise-calibrated score correlations need not
  assemble into any valid joint Gaussian, so a five-lead agreement matrix can be pairwise-consistent
  and globally impossible.

## Mechanism

No market mechanism. The object is a measurement identity for a latent-Gaussian threshold model —
the model in which each judge has a continuous score, the scores are jointly normal, and the
decision is "score above the cut".

1. **The forward map (the paper's Equation 8).** For two latent normal scores with correlation
   `r_ij` and cuts `t_i = Φ⁻¹(p_i)`, `t_j = Φ⁻¹(p_j)`, the Pearson correlation of the two resulting
   indicators is

   ```
   Corr(X_i, X_j) = [ Φ₂(t_i, t_j; r_ij) − p_i·p_j ] / sqrt( p_i(1−p_i) · p_j(1−p_j) ),
   ```

   with `Φ₂(·,·;r)` the bivariate standard normal CDF. Equal cuts at tail fraction `q` reduce this to
   `φ = [Φ₂(z_q, z_q; ρ) − q²] / (q(1−q))`, and at `q = 1/2` to the arcsine identity in the companion
   note. **This is the aim's missing half, in full generality.**
2. **"Naive" substitution is wrong, and the paper says so as its headline.** Setting the latent
   correlation equal to the target indicator correlation "is generally incorrect after
   thresholding", because thresholding is many-to-one, the resulting marginals are discrete, and
   Pearson correlation is not margin-free. A Gaussian copula preserves rank measures (Kendall's tau,
   Spearman's rho) but **not** Pearson correlations under a change of marginals — and a threshold is
   a change of marginals.
3. **The inverse map is unique (the tetrachoric calibration).** Define
   `g_ij(r) = [Φ₂(t_i,t_j;r) − p_i p_j] / sqrt(p_i(1−p_i)p_j(1−p_j))`. Its derivative is
   `g'_ij(r) = φ₂(t_i,t_j;r) / sqrt(p_i(1−p_i)p_j(1−p_j)) > 0`, with `φ₂` the bivariate normal
   density. So `g_ij` is strictly increasing and invertible on its admissible range, and a measured
   pairwise agreement rate yields **one** latent correlation `r*_ij = g_ij⁻¹(ρ_ij)`. There is no
   closed-form inverse; it is a one-dimensional monotone root-find.
4. **Feasibility bounds on a binary correlation (the paper's Equation 3, attributed to Chaganty &
   Joe).** For Bernoulli pairs,

   ```
   ρ_min = [max(0, p_i + p_j − 1) − p_i p_j] / sqrt(p_i(1−p_i)p_j(1−p_j)),
   ρ_max = [min(p_i, p_j)        − p_i p_j] / sqrt(p_i(1−p_i)p_j(1−p_j)).
   ```

   At equal cuts `p_i = p_j = q ≤ 1/2`, `ρ_max = 1` but `ρ_min = −q/(1−q)`. **Negative agreement is
   bounded hard by the depth of the cut and positive agreement is not** — an asymmetry with a direct
   consequence below.
5. **Beyond two judges, pairwise calibration can be globally infeasible.** Assemble the calibrated
   `r*_ij` into a matrix. If it is positive semidefinite, thresholding a Gaussian with that
   correlation matrix reproduces every requested pairwise agreement exactly. If it is **not** PSD,
   "no joint Gaussian latent vector exists with those pairwise calibrated entries", hence no exact
   latent-Gaussian threshold representation of the requested agreement structure exists at all; and
   "any practical repair that replaces `R*` by a nearby PSD matrix must change at least one latent
   pair, and therefore changes at least one induced Bernoulli correlation as well." The paper is
   careful that this is a *representability* test, not a feasibility test: a target may be
   Bernoulli-feasible (some joint law exists) and still fall outside the Gaussian-threshold family,
   and conversely a target may fail the pairwise Bernoulli bounds and then no joint law exists at
   all, by any method.

## Construction recipe

The conversion table the lab needs, computed as pure arithmetic on Equation 8 (scipy's bivariate
normal CDF in the scratchpad; **no repo data, no market data, no backtest**). `overlap` is
`P(both in top-q | one in top-q) = Φ₂(z_q,z_q;ρ)/q` — the fraction of a top-`K` list two leads share
— and `φ` is the correlation of the membership indicators.

| score corr `ρ` | `q`=0.5 | `q`=0.2 | `q`=0.1 | `q`=0.05 | `q`=0.02 |
|---|---|---|---|---|---|
| 0.30 | φ 0.194 / ov 0.597 | 0.163 / 0.331 | 0.129 / 0.216 | 0.098 / 0.143 | 0.065 / 0.083 |
| 0.50 | 0.333 / 0.667 | 0.295 / 0.436 | 0.249 / 0.324 | 0.204 / 0.244 | 0.152 / 0.169 |
| 0.66 | 0.459 / 0.729 | 0.420 / 0.536 | **0.372 / 0.435** | 0.323 / 0.357 | 0.264 / 0.279 |
| 0.89 | 0.699 / 0.849 | 0.672 / 0.737 | **0.637 / 0.674** | 0.600 / 0.620 | 0.552 / 0.561 |

Three readings, all free:

1. **The lab's own numbers.** Two leads whose scores correlate at 0.89 share **67%** of a top-decile
   selection, not 89%; their membership flags correlate 0.637. At 0.66 they share **44%**. So a
   correlation-based decorrelation screen and a top-`K` overlap screen disagree by 15–22 points at a
   decile cut, in the direction of the overlap being *smaller*.
2. **Depth moves the answer monotonically downward, and the sensitivity to depth is largest at
   middling `ρ`.** From `q = 0.5` to `q = 0.02`, `φ` falls by 0.147 at `ρ = 0.89` and by 0.195 at
   `ρ = 0.66`; the *overlap* falls much faster (0.849 → 0.561 and 0.729 → 0.279). Any statement of
   the form "the leads agree on X% of names" is meaningless without the cut depth attached.
3. **The negative side is capped.** At `q = 0.1`, `φ ≥ −0.111`; at `q = 0.05`, `φ ≥ −0.053`. Two
   top-decile selections of the same thousand names **cannot** be strongly anti-correlated, because
   they cannot be much more disjoint than chance already makes them. This is an independent,
   purely combinatorial reason why `#528`(d)'s refusal of a deliberately contrarian panel holds, and
   it is stronger than that argument: there, mutual contrarianism admitted no joint distribution for
   `k ≥ 3`; here, even for `k = 2`, the depth of the cut forbids it.

Feasibility and representability, as a two-stage pre-trial test (both free, both holdings-only):
first check every measured pair against the Bernoulli bounds in point 4; then root-find each
`r*_ij = g_ij⁻¹` and check that the assembled matrix is PSD. Report which stage fails.

## Robustness evidence (qualitative only)

- **Not an empirical claim**, so replication status does not apply. The map in Equation 8 and the
  monotonicity argument are elementary and were verified here: at `q = 1/2` the formula reproduces
  `2·arcsin(ρ)/π` to four decimals at `ρ = 0.3, 0.66, 0.89`, matching the independently-sourced
  identity in the companion MacCallum note. That cross-check is the only reason a Tier-C preprint is
  being relied on at all.
- **The paper's own contribution is not used here.** Its LP/PMF feasibility machinery and its
  separating-witness results are unreplicated preprint material; this note takes only the
  threshold-map section, whose content the paper itself attributes to Emrich & Piedmonte (1991) and
  Qaqish (2003). **Those antecedents were not obtained**, so the attribution is recorded and not
  verified — a later session wanting a Tier-A citation for Equation 8 should chase Emrich & Piedmonte
  in *The American Statistician* 45(4).
- **The model's assumption is the binding limitation and it is exactly the lab's weak spot.**
  Everything above is *conditional on joint normality of the latent scores*. The paper never claims
  otherwise; it is a simulation-method paper in which normality is a design choice rather than a
  hypothesis about data. Under non-normality the map is simply a different function, and the
  companion note on tail dependence says the deep-tail end of the table is where the difference is
  biggest.

## Implementability here

Protocol v3, ~1,400-name point-in-time panel plus 42 ETFs, roughly a thousand eligible on a
validation date, cut depths the lab actually uses in the 2%–20% range. Nothing here is a book.

1. **The bridge the shelf has been missing is now closed, in both directions, with a caveat.**
   `#519`'s top-`K` agreement screen, `#523`'s feasibility ceiling `c ≤ 2/(k−1)`, `#525`'s collapse
   threshold `α > (p−1/2)/p`, `#526`'s `r_i` and `#527`'s `p(k)` table all take a **binary**
   agreement number. The lab holds **continuous** score correlations. The table above converts, and
   the conversion is **not** the identity: at the lab's measured 0.89 and a decile cut the binary
   number is 0.637. **Every one of those five instruments should be re-read with the converted
   number, and each will move toward admissibility**, because they were all being fed an
   over-stated dependence. State the cut depth whenever one is quoted.
2. **`#523`'s refusal and this note's uniqueness result do not contradict each other, and the reason
   matters.** Kaniovski's theorem (`#523`) says marginals plus pairwise correlations do not identify
   a joint distribution over *binary* judges, so a measured `c` cannot yield a weight. Here the
   inverse map *is* unique. The difference is a **modelling assumption**: adding "the latent scores
   are jointly normal" is exactly what buys identification, and the assumption is unverifiable from
   the agreement table alone. So the honest procedure is: convert under normality, *and* report the
   Kaniovski bracket, and if the two disagree about a decision, the decision is not supported.
3. **A new free pre-trial test for a multi-lead composite, and it can refuse `#513` outright.** Take
   the lab's stored lead scores, choose the `K` the construction will use, compute each pair's
   **measured** top-`K` overlap directly from the holdings (no conversion needed — this is a count),
   then (a) check each pair against the `ρ_min`/`ρ_max` bounds at that `q`, (b) invert each to a
   latent `r*_ij`, (c) test the assembled matrix for PSD. **A non-PSD outcome means the five leads'
   agreement structure has no latent-Gaussian representation at all**, which in turn means every
   normal-theory instrument on the shelf (this note's table included) is being applied outside its
   model, and the composite question has to be decided by direct measurement rather than by any of
   it. Run this before `#525`.
4. **A diagnostic worth more than the conversion: compare the measured overlap with the
   normal-theory prediction.** For each pair, read the score correlation, look up the predicted
   overlap in the table, and compare with the counted overlap at the same `K`. **Measured overlap
   above prediction means the leads agree more in the tail than joint normality implies** — the
   scores share a common factor concentrated in the extremes, which is the case in which a composite
   adds least and `#525`'s collapse condition is closest to binding. **Measured below prediction
   means the tails are more idiosyncratic than the bodies**, which is the case in which selecting on
   several leads adds genuinely independent information even though the full-cross-section
   correlation looks fatal. **This single comparison decides the question that the 0.89 rank
   correlation has been standing in for since 2026-11-24**, it needs no trial, and it needs no
   holdout.

Known pitfalls. (i) The lab's cut is on a *rank within a date*; ranks are uniform, not normal, so
convert ranks to normal scores (`Φ⁻¹` of the fractional rank) before using any of this, or the
latent-normal assumption is violated at the first step. (ii) `q` here is the fraction of the
*eligible* panel selected, which changes date by date as eligibility changes; use the date's own
`q`. (iii) Unequal cuts are handled by the general Equation 8, so leads selecting different
numbers of names are fine — but then `ρ_max < 1` and the bounds in point 4 are the binding check.
(iv) Do not use this to *generate* anything; it is a reading instrument.

## Related

- `2026-11-26-what-a-top-k-cut-costs-the-dichotomization-attenuation.md` — the median special case
  from a Tier-A source, the cross-check that licenses this note, and the price of the cut itself.
- `2026-11-26-correlation-is-not-the-dependence-and-the-tail-where-it-vanishes.md` — what happens to
  the deep-cut columns of the table above when the scores are not jointly normal.
- `2026-11-25-what-a-pairwise-correlation-does-not-pin-down.md` — `#523`, the identification refusal
  this note's uniqueness result sits beside; see point 2 for why they are compatible.
- `2026-11-25-the-opinion-leader-model-and-the-bloc-weight-discount.md` — `#524`/`#525`, the
  instruments whose inputs this note converts.
- `2026-11-24-top-k-distance-measures-and-the-equivalence-class.md` — the metric-side statement that
  a top-`K` question is not answerable by a full-cross-section measure; this note is the
  distributional-side statement of the same thing.
- `2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` — `#513`, which point 3 can
  refuse before a trial.
