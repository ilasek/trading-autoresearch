---
title: "What breaks the threshold map under NON-NORMALITY — the coefficient of tail dependence, the theorem that a Gaussian dependence structure makes deep-tail agreement vanish at ANY correlation below one, the contrasting heavy-tailed case in which agreement survives at zero correlation, and the two fallacies that make a correlation a weaker summary than it looks"
authors: Embrechts, McNeil, Straumann
year: 2002
venue: "Chapter in *Risk Management: Value at Risk and Beyond* (M. A. H. Dempster, ed.), Cambridge University Press, 176–223. Peer-reviewed edited volume from a group that defines this literature; tier 1–2. The version READ is the authors' own ETH working paper dated November 1998, which carries the same title, abstract, theorems and examples."
url: https://doi.org/10.1017/CBO9780511615337.008
citations: "951 (Crossref `is-referenced-by-count` on the chapter DOI, checked 2026-11-26). The paper is also widely cited in its working-paper form, so the true count is higher; no aggregate was taken."
sample_period: "n/a — theorems, copula constructions and synthetic simulated examples. The paper contains no estimated sample and no dated empirical result."
markets: "None used for any claim recorded here. Its motivating discussion is generic financial and insurance risk, and its worked distributional examples are lognormal and Student-t constructions."
tier: "A on citations, venue, authorship and the analytic nature of the content. One qualification: the version read is the 1998 ETH working paper rather than the 2002 typeset chapter, so page references here are to the working paper; the results used (Definition 7, the Gaussian and t tail-dependence calculations, Fallacies 1 and 2, Theorem 4) are standard and are attributed in the text to Sibuya (1961), Resnick (1987), Hoffding (1940) and Frechet (1957)."
validation_overlap: false
published_post_2018: false
read: "Full text of the working-paper version, 607 KB PDF from `people.math.ethz.ch/~embrecht/ftp/pitfalls.pdf`, HTTP 200 first request; `pdftotext -layout` → 127 KB of text, 494 instances of ` the `. PARTIAL MATH DROPOUT: inline Greek letters and some sub/superscripts extract as nothing, so `lambda` and `rho` appear as blanks and 25 occurrences of `( )` are symbol dropout rather than empty parentheses (the ninth 'looks like an answer' mode in `research/README.md`, in its mild form). Every formula quoted below was reconstructed from the surrounding prose, which states each result in words as well as symbols; where a symbol could not be resolved with certainty it is marked."
access_note: "`people.math.ethz.ch/~embrecht/ftp/<slug>.pdf` — a senior author's own ETH FTP directory, flat, first request, HTTP 200. The faculty-page lesson (2026-09-18) in its plainest form, and it served a paper whose published form is a closed Cambridge chapter."
---

## Why this source is here

The [2026-11-25] aim's criterion (iii) asked what breaks the score-correlation → membership-agreement
conversion "under non-normality, since cross-sectional scores are not Gaussian and the tail is the
operative region, which is exactly where the median formula is least informative". This is the
source for that criterion, and its answer is sharper than the aim anticipated: under a Gaussian
dependence structure, **deep-tail agreement does not merely attenuate, it goes to zero**, for every
correlation strictly below one — while under a heavy-tailed dependence structure it stays strictly
positive even at zero correlation. The direction of the error in the companion notes' conversion
table therefore depends on a property of the lab's scores that the lab has never measured.

## Mechanism

No market mechanism; this is distribution theory about what a correlation does and does not say.

1. **The coefficient of upper tail dependence (Definition 7).** For continuous marginals,

   ```
   lambda = lim_{u -> 1} P[ Y > F2^{-1}(u) | X > F1^{-1}(u) ],
   ```

   when the limit exists. `lambda > 0` is asymptotic dependence; `lambda = 0` is asymptotic
   independence. **This is precisely the lab's quantity** — the probability that lead `j` selects a
   name given that lead `i` did — in the limit of a vanishingly thin top-`K`. It is a property of
   the **copula** alone, hence invariant to any strictly increasing transformation of either score.
2. **The Gaussian result.** With a Gaussian copula and correlation `rho`, conditioning gives
   `Y | X = x ~ N(rho·x, 1 − rho²)`, from which

   ```
   lambda = 2 · lim_{x -> inf} Phi_bar( x · sqrt(1 − rho) / sqrt(1 + rho) ) = 0   for rho < 1.
   ```

   The paper states the consequence in words: *"Thus the Gaussian copula gives asymptotic
   independence, provided that rho < 1. Regardless of how high a correlation we choose, if we go far
   enough into the tail, extreme events appear to occur independently in each margin."* It cites
   Sibuya (1961) and Resnick (1987, ch. 5) for alternative demonstrations.
3. **The heavy-tailed contrast.** For a bivariate Student-t with `nu` degrees of freedom and
   correlation `rho`, the same construction gives a **strictly positive** limit,
   `lambda = 2·t_bar_{nu+1}( sqrt(nu+1) · sqrt(1−rho) / sqrt(1+rho) )` (symbols partly reconstructed
   from the dropout; the paper's own table is the reliable record). Its tabulated values:

   | `nu` | `rho` = −0.5 | 0 | 0.5 | 0.9 |
   |---|---|---|---|---|
   | 2 | 0.06 | 0.18 | 0.39 | 0.72 |
   | 4 | 0.01 | 0.08 | 0.25 | 0.63 |
   | 10 | 0.00 | 0.01 | 0.08 | 0.46 |
   | ∞ | 0 | 0 | 0 | 0 |

   The paper's comment: *"Perhaps surprisingly, even for negative and zero correlations, the
   t-copula gives asymptotic dependence in the upper tail. The strength of this dependence increases
   as nu decreases and the marginal distributions become heavier-tailed."* **Two uncorrelated leads
   with heavy-tailed scores can agree on 18% of a vanishingly thin top-`K`; two Gaussian leads
   correlated at 0.9 agree on 0%.**
4. **Fallacy 1 — marginals and correlation do not determine the joint law.** True inside the
   elliptical world ("if we know that `(X,Y)` have a bivariate normal distribution, then the
   expectations and variances... and the correlation uniquely determine the joint distribution"),
   false outside it: the paper constructs uncountably many bivariate distributions with standard
   normal marginals and correlation **zero** whose densities look nothing like the independent
   bivariate normal.
5. **Fallacy 2 — the attainable correlation range depends on the marginals.** By the
   Hoffding–Frechet theorem (its Theorem 4) the set of attainable correlations for given marginals is
   a closed interval `[rho_min, rho_max]` with `rho_min < 0 < rho_max`, attained exactly at
   counter- and comonotonicity, and `rho_max = 1` only if the two marginals are of the same type. So
   a correlation near zero can be the *maximum possible* dependence for a pair, and "low
   correlation" is not "near independence".
6. **Rank correlation is copula-invariant; Pearson correlation is not.** Spearman's and Kendall's
   measures depend on the copula only, so they are unchanged by a monotone re-scaling of either
   score; Pearson's is not, and the paper's main advantages/disadvantages discussion turns on this.

## Construction recipe

No portfolio. Three instruments, all free and all holdings- or score-only.

1. **The chi-plot test for the lab's own scores.** For a pair of leads, compute the *measured*
   overlap `P(both selected | one selected)` at a ladder of cut depths — `q` = 0.5, 0.2, 0.1, 0.05,
   0.02 — using converted-to-normal ranks of the scores on each rebalance date, pooled across dates.
   Plot it against `q`. **A sequence that keeps falling toward zero as `q` shrinks is the Gaussian
   signature** (`lambda = 0`), and the normal-theory table in
   `2026-11-26-the-threshold-map-between-score-correlation-and-membership-agreement.md` is the right
   reading instrument. **A sequence that flattens at a strictly positive level is tail dependence**,
   and every normal-theory conversion on the shelf understates deep-cut agreement — by the whole
   level at which the sequence flattens.
2. **Use a rank measure, not Pearson, wherever a correlation feeds a dependence conclusion** (point
   6). The lab's 0.89 figure is a *rank* correlation, which is the right choice; any Pearson
   correlation of raw active-return series is not interchangeable with it and the two should not be
   substituted for one another in `#523`/`#525`.
3. **Stop treating a single correlation number as a summary of two leads' relationship** (points 4
   and 5). The defensible summary is the pair (rank correlation, deep-cut overlap), because the
   first is invariant and estimable and the second is the quantity a membership construction
   actually pays for.

## Robustness evidence (qualitative only)

- **Theorems, not estimates**, so replication status does not apply; the key results are attributed
  to Sibuya (1961), Resnick (1987), Hoffding (1940) and Frechet (1957) and have been standard for
  decades. The paper is among the most cited statements of them in the risk-management literature.
- **The Gaussian asymptotic-independence result is exact and assumption-free given the copula.** It
  does not depend on marginals at all, which is what makes it usable here: the lab's scores need not
  be normal for the conclusion to bite, only their *dependence structure*.
- **The t-table is a property of a model family, not a measurement**, and the degrees of freedom are
  a free parameter. Treat the numbers as showing the *shape* of the contrast, not as calibrated to
  anything here. No claim in this note depends on a particular `nu`.
- **The honest limit of the source for this folder's purposes**: it says what the deep-tail limit is
  for two named families, and nothing about the *rate* at which the Gaussian case approaches zero.
  The sub-asymptotic rate is the Ledford–Tawn / Coles–Heffernan–Tawn literature, **which was located
  bibliographically in this session and not obtained** (see the coverage row), so the folder holds
  the limits and not the rate. For a finite cut like the lab's top 2–10%, the rate is what actually
  matters, and the numerical table in the companion note is currently standing in for it.

## Implementability here

Protocol v3, ~1,400-name point-in-time panel plus 42 ETFs, cut depths 2%–20%.

1. **This is the tension in tonight's set, and it must not be resolved by preference.** The
   Tier-A MacCallum note reports Cohen's position that non-normality alters dichotomization
   attenuation "only marginally"; this Tier-A source proves that in the deep tail the Gaussian and
   heavy-tailed cases differ by the entire quantity. **Both are right about their own regime**:
   Cohen is describing a median-ish split, where the bulk of the distribution does the work, and
   this paper is describing the limit. The lab's cut is in between, so neither statement can be
   quoted as covering it, and instrument 1 above is the measurement that settles which end it is
   nearer. Any session that quotes one of the two without the other is over-claiming.
2. **A concrete consequence for `#513`/`#525`.** If the lab's lead scores are tail-dependent, then
   two leads that look decorrelated in the body of the cross-section still agree heavily on the
   names a top-`K` construction holds, so a composite built by intersecting or majority-filtering
   selections is **more** concentrated than the full-cross-section correlation suggests, and
   `#525`'s collapse condition is nearer to binding than the measured `alpha` implies. If they are
   Gaussian-like, the opposite: the deep cut *manufactures* diversification that the correlation
   does not show, and a top-`K` composite over leads is a better bet than the 0.89 figure suggests.
   **The sign of this effect is exactly the open question in the composite vein, and instrument 1
   answers it for free.**
3. **An anti-candidate, stated plainly.** Do not build a construction whose edge is "these two
   signals are uncorrelated, so combining them diversifies". Fallacies 1 and 2 say a near-zero
   correlation can be consistent with strong, structured dependence and can even be the maximum
   attainable for the pair; the tail results say the dependence that matters for a selection
   construction lives where a correlation does not look. This is a sharper version of the warning
   already carried in `#517`.
4. **Reading rule for this folder.** Every instrument on the shelf that converts between a
   correlation and an agreement rate is a *Gaussian-copula* instrument, including tonight's table.
   Label them so. The conversion is not a fact about the lab's scores; it is a fact about a model
   the lab has not tested.

Known pitfalls. (i) `lambda` is a limit, and no finite top-`K` ever reaches it — the test in
instrument 1 is a trend across depths, not an estimate of `lambda`, and the deepest cuts have the
fewest names and the widest sampling error, so read the ladder, not its last rung. (ii) Pooling
across rebalance dates assumes the dependence structure is stable across dates; it is the standard
assumption and it is an assumption. (iii) Tail dependence is a property of the *pair*; with five
leads there are ten pairs and no single number summarises them, which is the same unit-of-check
trap this folder has fallen into before.

## Related

- `2026-11-26-the-threshold-map-between-score-correlation-and-membership-agreement.md` — the
  normal-theory conversion table whose deep-cut columns this note qualifies.
- `2026-11-26-what-a-top-k-cut-costs-the-dichotomization-attenuation.md` — the Tier-A source whose
  "non-normality matters only marginally" sentence is in tension with this one; see point 1.
- `2026-11-25-what-a-pairwise-correlation-does-not-pin-down.md` — `#523`. Fallacy 1 here is the
  continuous-margin sibling of Kaniovski's binary-margin identification refusal, and the two
  together are a general statement: **a correlation plus marginals is not a dependence structure**,
  in either the binary or the continuous case, and only an assumption like joint normality makes it
  one.
- `2026-10-19-consistent-scoring-functions-and-elicitability.md` — the other note in this folder that
  turns on what a summary statistic does and does not pin down.
