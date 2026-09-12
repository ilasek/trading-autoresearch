---
title: "Rank Transformations as a Bridge between Parametric and Nonparametric Statistics" — read together with the aligned-rank-transform correction and the factorial-ANCOVA failure evidence, for what the `rank` operator assumes
authors: Conover, Iman (1981); Wobbrock, Findlater, Gergle, Higgins (2011); Headrick, Sawilowsky (2000); Sawilowsky, Blair, Higgins (1989)
year: 1981
venue: The American Statistician (Tier 1 methodology journal); ACM CHI (Tier 1 conference); AERA conference paper via ERIC (Tier 4); Journal of Educational Statistics (Tier 1 methodology journal)
url: https://doi.org/10.1080/00031305.1981.10479327 · https://doi.org/10.1145/1978942.1978963 · https://files.eric.ed.gov/fulltext/ED440996.pdf · https://doi.org/10.3102/10769986014003255
citations: Conover–Iman 3948 (Semantic Scholar, checked 2026-09-12); Wobbrock et al. 3079 (Semantic Scholar, checked 2026-09-12); Sawilowsky–Blair–Higgins 35 (Crossref on 10.3102/10769986014003255, checked 2026-09-12; a second registration 10.2307/1165018 for the same article shows 26 — the two-DOI pattern again); Headrick–Sawilowsky not indexed (Semantic Scholar, Crossref tried, checked 2026-09-12 — an ERIC conference document with no DOI)
sample_period: none — statistical methodology and Monte-Carlo simulation, no market data
markets: none
tier: A for Conover–Iman and Wobbrock et al.; B for Sawilowsky–Blair–Higgins; C for the Headrick–Sawilowsky conference document
validation_overlap: false
published_post_2018: false
read_status: Wobbrock et al. and Headrick–Sawilowsky read in full; Conover–Iman recorded from its abstract and from the three later papers' descriptions of it (The American Statistician is closed and no open copy resolved); Sawilowsky–Blair–Higgins recorded from its abstract and from Headrick–Sawilowsky's account of it
---

## Mechanism

The `rank` operator is the one this lab applies to almost every score, and it has never had a
note. It is not a neutral pre-processing step; it is a *nonlinear* transform with three specific
properties, two of which are the reason it is used and one of which is a trap.

**What it is.** Conover and Iman's proposal is that a large family of nonparametric procedures can
be obtained by *replacing each observation by its rank and then running the ordinary parametric
procedure on the ranks* (ties averaged). Wilcoxon, Kruskal–Wallis and Spearman all fall out of
this recipe; that unification is what the paper is cited 3900+ times for. A cross-sectional
portfolio sort is exactly this construction: replace each name's score by its rank in the
cross-section, then take a fixed function of the ranks (the top band).

**Property 1 — it preserves order and nothing else.** A rank is invariant under *any* strictly
monotone transform of the score. Log, square-root, affine rescaling, z-scoring, winsorizing at any
symmetric pair of cutoffs, clipping the tails: none of these change a single rank, so none of them
change a rank-and-band book. This is the general statement of what this folder measured
piecemeal on 2026-09-11 (winsorization does not reach a sorted band) and it is worth stating as a
theorem rather than a finding: **the entire class of monotone score repairs is a no-op on a
ranked book.** The corollary is the useful half: a rank is robust to outliers by construction,
because an outlier is just the last rank.

**Property 2 — it destroys spacing, so the only thing a ranked book can exploit is depth.**
Once ranked, the difference between the best name and the second-best is identical to the
difference between rank 90 and rank 91. All the information the score carried about *how much*
better one name is has been deleted. Everything a rank-and-band construction can earn therefore
comes from the *shape of expected return as a function of rank* — the depth profile this lab
started measuring on 2026-09-08 — and from nothing else. That is why profiling depth and then
setting the band is the right order of operations, and why a magnitude-weighted book is a
genuinely different object from a ranked one rather than a refinement of it.

**Property 3 — it is nonlinear, so it does not commute with combining variables.** This is the
trap, and it is where the later literature lives. Because ranking is nonlinear,
`rank(a·x + b·y) ≠ a·rank(x) + b·rank(y)`: the rank of a composite is not any combination of the
ranks of its parts. In the ANOVA setting this shows up as the RT distorting *interactions*
between factors, and it was severe enough that the procedure was withdrawn as a general
recommendation for factorial designs. Headrick and Sawilowsky's simulations state the mechanism
in the sharpest available form: in their factorial ANCOVA experiment **"the nonlinear nature of
the RT reversed the absence of interaction in the original scores when both main effects were
present"** — that is, the rank transform *manufactured* an interaction that did not exist in the
levels. Their second finding is the one that should worry a lab whose signals correlate:
**the stronger the correlation between the variate and the covariate, the worse the distortion.**

**Property 4 (structural, not from these papers) — a rank is defined only relative to a pool.**
Ranking is not a per-name function. Adding or removing instruments, or changing the eligibility
rule for a date, changes the rank of every name whose score did not move. This is the operator-level
statement of two things this lab has already hit: the `common` intersection silently changing the
train sample when a leg with a longer lookback is added (2026-09-04), and the seated
`liquidity-volume` lead's ETF question (2026-09-10). Neither was a bug in a signal; both were the
`rank` operator doing what it does.

## Construction recipe

The recipe is the three-line one everybody already uses, plus the two corrections the later
literature adds:

1. **Rank within the cross-section on each date**, ties averaged (Conover–Iman's own convention;
   averaged ties are what keeps the transform well-defined and symmetric).
2. **Normalize the rank by the pool size**, not by a constant, if ranks from different dates are
   ever compared, pooled or fed to a model. A raw rank of 20 means something different in a
   pool of 90 than in a pool of 140. Mapping to `(rank − 1)/(N − 1)` on `[0,1]` (or to `[−1,1]`,
   the convention the machine-learning asset-pricing papers use) is what makes a rank a
   date-comparable quantity.
3. **If a combination is involved, align before ranking, not after.** This is the whole content of
   the aligned rank transform (ART): where the naive RT ranks the raw response and then fits the
   full factorial model, the ART first *strips* every effect except the one being tested — each
   response has its cell mean subtracted and the estimated effects of the other factors removed —
   and ranks the *residual*. Ranking after alignment restores the correct behaviour for both main
   and interaction effects; ranking before it does not. The transferable instruction is:
   **when a score is supposed to measure one thing net of another, residualize first and rank the
   residual — do not rank the raw quantity and then try to correct the ranks.**

## Robustness evidence (qualitative only)

- Conover and Iman's unification is uncontested for *single-factor* problems: RT-based one-way and
  two-sample tests are the standard nonparametric procedures and were already in wide use before
  the paper named the pattern.
- The interaction failure is not a single result. It was established independently across the
  factorial-ANOVA literature (Sawilowsky–Blair–Higgins; Higgins–Blair–Tashtoush) and then
  extended to factorial ANCOVA by Headrick–Sawilowsky, who find severely inflated Type I error
  for the interaction test whenever both main effects are non-null, **regardless of the
  conditional distribution or the sample size simulated**. The direction of the failure is
  monotone in the correlation between the variate and the covariate.
- The ART correction has itself been independently validated and is widely used; its own
  literature carries a further, more recent line of criticism about how far the alignment argument
  extends to complex designs, so the alignment step should be read as a *repair of a known
  distortion*, not as a guarantee.
- Nothing here is period-specific or market-specific: these are properties of the transform, so
  there is no decay story and no replication-crisis discount to apply.

## Implementability here

The lab already uses this operator everywhere; the value of the note is the constraints it
imposes, and every one of them is free to check.

1. **Stop proposing monotone score repairs for ranked books.** Winsorizing, clipping, logging,
   z-scoring or re-standardizing a score changes no rank and therefore no ranked book. The three
   places in this repo where such a repair *can* matter are exactly the non-rank-invariant ones:
   the `price-trend` magnitude weighting, any fitted model that consumes score levels, and any
   per-period mean read as evidence. Everywhere else the honest answer to "should we winsorize
   this?" is "it is an identity on this construction".
2. **A blend of ranks and a rank of a blend are different books, and the difference grows with the
   correlation between legs.** This is Property 3 made concrete, and it bears directly on the
   arm the 2026-09-11 session declined in pre-registration (rank-and-band on the identical
   `theta'x` composite). That arm is not "the same score, banded" — ranking a composite of
   correlated characteristics is the configuration Headrick–Sawilowsky show is worst behaved.
   The free screen is two lines: build `rank(mean(rank(x1), rank(x2)))` and
   `rank(a·x1 + b·x2)` on the same dates and report the Spearman correlation between them and the
   overlap of their top-20 books, exactly as the 2026-09-10 session priced demean-vs-residual.
   Both answers are findings; a high correlation retires the question permanently.
3. **The ART instruction and the residual-momentum construction are the same instruction.**
   "Align, then rank" (this note) and "regress out the common factors, then rank the residual"
   (`2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md`) are one idea reached
   from two literatures. Where a score is meant to be net of something, the neutralization
   belongs *inside* the score, before the ranking — never as a post-hoc adjustment to a ranked
   book, and never as a group adjustment applied to ranks.
4. **Report pool size beside any rank-based statistic.** A rank of 20 in a pool that shrank from
   140 to 96 because a leg's lookback bound the `common` intersection is a different exposure at
   the same nominal band. This is free and it would have caught the 2026-09-04 sample change at
   the time rather than after.

**Pitfalls.** (a) Do not read Property 1 as "ranking is robust, therefore ranking is better": it
is robust because it is lossy, and the loss is Property 2. (b) Ties: with 140 instruments and a
score with plateaus (anything built from counts, or from a signal that saturates), averaged ties
change band membership in a way that is invisible in the score. (c) The ANOVA results are about
*hypothesis tests*, not about portfolio returns — what transfers is the algebraic fact
(nonlinearity, no commutation with combination, distortion increasing in correlation), not the
Type I error rates, which have no counterpart here.

**Anti-candidate.** There is no book in this note. Nothing here proposes a new score; it says
which proposals about existing scores are identities and which are genuinely different objects.
A session should spend at most the two free screens in point 2 and point 4 on it.

## Related

- `2026-09-11-influential-observations-winsorization-versus-robust-regression.md` — the special
  case of Property 1 that this lab reached first, from the outlier side.
- `2026-09-11-parametric-portfolio-policies-standardized-characteristics.md` — the one
  construction here that ranks nothing, and therefore the one where monotone repairs bite.
- `2026-09-08`-era depth-profile work and `2026-09-06-number-of-portfolios-as-tuning-parameter.md`,
  `2026-09-06-monotonicity-tests-for-portfolio-sorts.md` — what is left to exploit once Property 2
  has deleted the magnitudes.
- `2026-08-31-signal-blending-vs-portfolio-blending.md` — the *where to blend* question; this note
  adds that the ranking step is itself part of the blend's definition.
- `2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — "align, then rank" in its
  asset-pricing form.
- `2026-09-10-country-demeaned-versus-country-mean-characteristics.md` — a group demean is an
  alignment; this note says why it belongs before the rank rather than after.
