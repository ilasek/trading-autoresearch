---
title: "What a top-K CUT costs — the attenuation factor a dichotomization applies to a correlation, the median-only arcsine identity between an indicator correlation and the underlying score correlation, and the statement that the gap WIDENS with the depth of the cut"
authors: MacCallum, Zhang, Preacher, Rucker
year: 2002
venue: "Psychological Methods 7(1), 19–40. Peer-reviewed APA flagship methods journal; tier 1 within its field. The paper is part review, part analytic derivation, part small simulation; the two results used here are analytic and are attributed to Lord & Novick (1968, p. 346), Magnusson (1966) and Cohen (1983)."
url: https://doi.org/10.1037/1082-989X.7.1.19
citations: "2,765 (Crossref `is-referenced-by-count`, checked 2026-11-26); 3,580 (Semantic Scholar by DOI, same date)."
sample_period: "n/a — analytic results plus a small simulation from bivariate normal populations at five levels of population correlation. No market data and no dated sample anywhere in the paper."
markets: "None. The paper's applied examples are psychological individual-difference measures."
tier: "A on citation count, venue and the analytic nature of the two results used. One honest qualification: the paper is a *methodological argument against a practice*, not a derivation paper, so both formulas used here are quoted from it with its own attributions (Equation 1 to Magnusson 1966; Equation 2 to Lord & Novick 1968) and were not derived in it. The median identity in Equation 2 was re-derived and numerically confirmed here (see `## Construction recipe`), so it is self-checking; Equation 3 is Equation 1 applied."
validation_overlap: false
published_post_2018: false
read: "Full text, 22 pp. (19–40), 257 KB PDF, HTTP 200 first request; `pdftotext -layout` → 124 KB of text, 485 instances of ` the `, zero `( )` dropout, no ASCII shift. Greek characters extract as mojibake (`␳` for rho), displayed formulas extract as two-column interleavings and were read against the surrounding prose; the `h/sqrt(pq)` factor and the arcsine identity were both re-checked numerically before being recorded."
access_note: "`psychology.psy.sunysb.edu/attachment/measures/content/<author>_on_<topic>.pdf` — a university psychology department's own *measures / teaching materials* directory, which hosts the typeset APA article (copyright header intact) of a paper whose publisher endpoint is closed. This is the 2026-11-24 'faculty reading-list' lesson again, now on a department-level teaching archive rather than an individual's page, and with a *topic*-derived filename rather than an `<Author><Year>` one."
---

## Why this source is here

The [2026-11-25] aim asked for the closed-form relation between the correlation of two continuous
scores and the agreement rate of the **binary top-`K` membership decisions** those scores induce,
because every instrument this folder filed on 2026-11-24 and 2026-11-25 is stated in terms of a
binary judge (`p`, `c`, `r_i`) while everything the lab measures is continuous (an IC, a rank
correlation between scores, a correlation between active-return series). `#518` supplied the
IC → `p` half. This source supplies the **other half in the only case where it is elementary**, and
— more valuable — it states in as many words that the elementary case is the *only* elementary case:

> "As the point of dichotomization moves away from the mean, the relationship between the phi
> coefficient and tetrachoric correlation becomes much more complex (Kendall & Stuart, 1961;
> Pearson, 1900), and the difference between the two coefficients becomes greater."

So the aim's own suspicion — that the median formula "is least informative" exactly where the lab's
cut sits — is the published position, and this note makes it quantitative.

## Mechanism

There is no market mechanism here. The content is the measurement-theoretic price of replacing a
continuous variable by an indicator of which side of a cut it fell on, which is precisely what the
lab does when it turns a lead's score into top-`K` membership.

1. **Dichotomizing one variable attenuates its correlation with anything else by a known factor.**
   If `X` and `Y` are bivariate normal with correlation `ρ_XY`, and `X_D` is the indicator that `X`
   exceeded a cut keeping tail proportion `p`, then (the paper's Equation 3, which is its Equation 1
   — the population point-biserial / biserial relation of Magnusson 1966 — applied):

   ```
   ρ_{X_D Y} = ρ_XY · d,     d = h / sqrt(p·q),   q = 1 − p,
   ```

   where `h` is the standard normal **density** at the cut. `d` is a pure function of the cut depth.
   It is **0.798 at the median** and falls monotonically as the cut moves into the tail. The paper
   plots `d` against `p` (its Figure 4) and states the direction: "as the point of dichotomization
   moves further from the mean, the impact on the correlation coefficient increases."

2. **Dichotomizing both variables costs the factor twice.** For cuts at the mean,
   `ρ_{X_D Y_D} = d² · ρ_XY = 0.637 · ρ_XY`, and in general "loss of effect size is greater when
   both variables are dichotomized than when only one is."

3. **The exact relation between the two indicators' correlation and the underlying score
   correlation, at a median cut, is the arcsine identity** (the paper's Equation 2, attributed to
   Lord & Novick 1968, p. 346):

   ```
   φ = 2·arcsin(ρ_tetrachoric) / π.
   ```

   This is the aim's named median formula in the form the lab needs. (It is the same statement as
   the median orthant probability `P(both above median) = 1/4 + arcsin(ρ)/2π`: substituting that `P`
   into `φ = (P − 1/4)/(1/4)` gives Equation 2 identically. Both were checked numerically here and
   agree to four decimals.) Note that Equation 2 is *not* the same object as Equation 3's factor
   `d`: Equation 3 attenuates the correlation of an indicator with a **continuous** `Y`, Equation 2
   relates two **indicators** to the correlation of their two underlying scores.

4. **Away from the median there is no elementary closed form**, only the bivariate normal integral
   (see the companion note `2026-11-26-the-threshold-map-between-score-correlation-and-membership-agreement.md`,
   whose Equation (8) is the general case), and the *size* of the discrepancy between the indicator
   correlation and the score correlation grows with depth.

5. **Dichotomization can also manufacture structure that is not there.** With two correlated
   predictors, cutting both and running an ANOVA produces spurious main effects when one
   predictor's partial correlation with the target is near zero, and spurious interactions when the
   true effects are nonlinear — in the paper's words these are "a result of bias in estimating
   population effects and were not attributable to sampling error" (reviewing Maxwell & Delaney
   1993; Vargha, Rudas, Delaney & Maxwell 1996). Any nonlinearity in the score→return relation is
   "completely obscured" by the cut.

## Construction recipe

Not a strategy. The recipe is the conversion table the lab needs, and it is arithmetic.

**(a) The cost of the cut itself**, `d = h/sqrt(p(1−p))`, computed from the paper's Equation 3
(pure arithmetic on the published formula; no repo data, no market data):

| tail kept `p` | cut `z` | `d` (one side cut) | `d²` (both cut) |
|---|---|---|---|
| 0.50 | 0.00 | 0.798 | 0.637 |
| 0.30 | 0.52 | 0.759 | 0.576 |
| 0.20 | 0.84 | 0.700 | 0.490 |
| 0.10 | 1.28 | **0.585** | 0.342 |
| 0.05 | 1.64 | 0.473 | 0.224 |
| 0.02 | 2.05 | 0.346 | 0.120 |
| 0.01 | 2.33 | 0.268 | 0.072 |

Read the `p = 0.10` row as: **a top-decile membership flag retains 59% of the correlation that the
underlying score had with the forward return.** A top-2% flag retains 35%.

**(b) The median identity**, `φ = 2·arcsin(ρ)/π`, verified against a direct numerical evaluation of
the orthant probability at three values of `ρ`:

| `ρ` (score) | `φ` direct | `2·arcsin(ρ)/π` |
|---|---|---|
| 0.30 | 0.1940 | 0.1940 |
| 0.66 | 0.4589 | 0.4589 |
| 0.89 | 0.6986 | 0.6986 |

Use `φ < ρ` as the standing direction: **under normality a binary agreement statistic always
understates the correlation of the scores behind it**, and the understatement is worst at middling
`ρ` (at `ρ = 0.66` the median-cut indicator correlation is 0.46; at `ρ = 0.89` it is 0.70).

**(c) The remedy the paper recommends is not a better conversion, it is not cutting.** "It would
still be advisable not to dichotomize, but instead to retain information about individual
differences" — i.e. where a construction can use the score, using the score strictly dominates
using membership, and the factor in table (a) is the price of the convenience.

## Robustness evidence (qualitative only)

- **Not an empirical effect**, so replication in the Hou–Xue–Zhang / Jensen–Kelly–Pedersen sense
  does not apply. The formulas are population identities under bivariate normality; the paper's own
  contribution is the argument and the review, and both formulas carry 1960s–1980s attributions
  (Magnusson 1966; Lord & Novick 1968; Cohen 1983), i.e. they have been in the standard literature
  for decades.
- **Robustness to non-normality is asserted, not proved, and the assertion is modest**: the paper
  reports Cohen's (1983) position that "these phenomena would be altered only marginally by
  nonnormality" and that "it would require extreme skewness, heteroscedasticity, or nonlinearity to
  substantially alter these consequences." **That claim is about the *centre* of the distribution,
  and the lab's cut is in the tail.** The companion note
  `2026-11-26-correlation-is-not-the-dependence-and-the-tail-where-it-vanishes.md` is the source
  that contradicts the comfortable reading of this sentence for deep cuts, and the tension is
  recorded there rather than smoothed over.
- **Direction of the bias is unambiguous and does not depend on the sample**: the cut can only
  attenuate, under the stated assumptions. The spurious-effect results (point 5 above) are about a
  different construction (two cut predictors in an ANOVA) and are reviewed from Maxwell & Delaney
  rather than derived here.
- **The one place the paper's own evidence is thin**: its simulation asks whether sampling error can
  make a *sample* correlation rise after dichotomization, and finds it can. That is a warning
  against justifying a cut by a measured improvement, and it is a simulation, not a theorem.

## Implementability here

Protocol v3, ~1,400-stock point-in-time panel plus 42 ETFs, roughly a thousand names eligible on a
validation date. Nothing here is a book; all four products are free.

1. **The honest restatement of the aim's question, and it is a correction to how this folder has
   been writing its instruments.** `#519`, `#523`, `#525`, `#526` and `#527` all take a *binary*
   agreement quantity. The lab holds *continuous* score correlations. The conversion exists, it is
   `φ = 2·arcsin(ρ)/π` **only at a median cut**, and at the lab's actual cut depth it is the
   bivariate normal integral. **Substituting a measured score correlation for a binary agreement
   rate overstates agreement**, which means `#523`'s feasibility test and `#525`'s collapse
   threshold have been fed numbers biased toward *more* dependence than the binary panel actually
   has. Both products therefore err on the conservative side for a refusal and on the wrong side
   for an admission — state which when either is run.
2. **The selection step in `#513` has a measurable price, and it is large.** `#513`'s
   filter-then-deconcentrate replaces each lead's score by a membership decision and then
   equal-weights. Table (a) says a top-decile membership flag carries 59% of the score's correlation
   with the forward return, and a top-5% flag 47%. The construction must buy back that loss in
   turnover, robustness or de-concentration terms. This is a **free, pre-trial, holdings-only
   arithmetic** check: for each lead, compute the IC of the continuous score and the IC of its own
   top-`K` indicator on the same dates, and verify the ratio lands near the `d` of the chosen cut.
   **If the measured ratio is materially *above* `d`, the score's information is concentrated in its
   tail** (the opposite of normality's prediction) and the cut is cheaper than the table says; if it
   is materially *below*, the score's content is in the middle of the cross-section and selecting on
   it is worse than the table says. Either outcome is a fact about the panel the lab does not have.
3. **The `d`-table is also the right way to choose `K`.** `d` falls slowly from the median to the
   top 30% (0.798 → 0.759) and then steeply (0.585 at 10%, 0.346 at 2%). A construction that must
   cut should cut shallowly; the lab's broad-selection-then-filter shape in `#513` is, on this
   arithmetic, the correct shape, and a "top 20 names of a thousand" book is paying a 0.27 factor
   for concentration. Note what this does **not** say: it says nothing about expected return per
   name, only about how much of the score's linear association with the target survives the
   flattening. A convex score→return relation would change the conclusion, and point 5 above says a
   cut would hide exactly that.
4. **Anti-candidate, and it is a direct warning about an existing lab habit.** Do not cut two
   correlated predictors and compare cell means (or, in this lab's dialect, do not build a 2×2
   double sort on two correlated leads and read a "main effect" off it). The reviewed result is that
   this produces spurious main effects precisely when one predictor's partial association with the
   target is near zero and the two predictors are correlated — which is the lab's situation, with
   leads at 0.89 rank correlation. **Use the regression (or the continuous composite) and keep the
   scores.**

Known pitfalls. (i) Everything here assumes bivariate normality of the two *continuous* variables;
cross-sectional scores are not Gaussian and the deep tail is the operative region, so treat the
table as the normal-theory reference point, not as a measurement. (ii) `d` is about a *linear*
association; a rank-based IC will not attenuate by exactly `d`. (iii) The paper is about one cut on
a continuous variable; the lab's top-`K` is a cut on a *rank within a date*, which is a
cross-sectionally standardised variable — closer to the normal-theory case than a raw score, which
is the one respect in which the lab's setting is friendlier than the paper's.

## Related

- `2026-11-26-the-threshold-map-between-score-correlation-and-membership-agreement.md` — the general
  (arbitrary, unequal cut) form of Equation 2, its invertibility, and what happens with more than
  two judges.
- `2026-11-26-correlation-is-not-the-dependence-and-the-tail-where-it-vanishes.md` — why the
  "non-normality alters this only marginally" sentence above must not be carried into the deep tail.
- `2026-11-24-when-a-positional-rule-is-the-right-aggregator.md` — supplies the IC → `p` half of
  the bridge (`p = 1/2 + arcsin(ρ)/π` for a *pairwise ordering* under joint normality). Note the
  family resemblance and the difference: that arcsine is for concordance of a *pair of items*, this
  one for agreement of a *pair of judges* on membership. They are different objects with the same
  functional form, and the folder should not interchange them.
- `2026-11-24-top-k-distance-measures-and-the-equivalence-class.md` — the measurement-side reason a
  full-cross-section decorrelation screen cannot answer a top-`K` question.
- `2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` — `#513`, the construction
  whose selection step this note prices.
- `experiments/learnings.md`'s v1 finding that magnitude weighting is information-bearing and
  de-concentration is costly: this note is the normal-theory argument for the *first* half of that
  (a score carries more than a flag) and says nothing about the second.
