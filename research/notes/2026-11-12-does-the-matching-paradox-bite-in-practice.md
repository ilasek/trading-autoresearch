---
title: "Implications of the Propensity Score Matching Paradox in Pharmacoepidemiology"
authors: Ripollone, Huybrechts, Rothman, Ferguson, Franklin
year: 2018
venue: American Journal of Epidemiology 187(9), 1951–1961 (peer-reviewed; the leading journal of its field, outside this rubric's finance tier-1 list)
url: https://doi.org/10.1093/aje/kwy078
citations: 88 (Crossref, checked 2026-11-12)
sample_period: 1999–2002 and 2000–2007 (two US insurance-claims cohorts; no market data)
markets: n/a (observational-methods evaluation on healthcare claims)
tier: B
validation_overlap: false
published_post_2018: false
---

## Mechanism

The adversarial source for tonight's vein, and it is adversarial to **the thing this lab adopted
last night** rather than to tonight's construction. [2026-11-11] added `#435`'s rising-imbalance
curve as a standing refusal test — "plot imbalance against the number of observations pruned, and
reject a design whose curve rises." This paper takes King–Nielsen's paradox, reproduces its
qualitative behaviour in two large real datasets, and then argues that **the condition under which
the paradox actually threatens an inference is narrow and is not the condition most applied datasets
are in.**

The mechanism of the paradox, as these authors restate it, is worth having in their words because
their statement is sharper than the one the folder currently carries. Matching on a propensity score
guarantees balance on `Pr(Exposure | X)` but balance on `X` itself **only asymptotically**. Where
that asymptotic balance already holds, any further pruning of matched sets is *random with respect
to covariate balance* — so it shrinks the sample without buying anything, and can by chance increase
the covariate distance between the groups. Hence: the better balanced the data are before matching,
the sooner pruning starts to hurt.

Their twelve-unit worked example makes the arithmetic concrete and is the cleanest statement of the
paradox in the folder. Twelve units, four treated, two binary covariates perfectly balanced between
the groups, so every unit has the identical propensity score `1/3`. Any 1:1 match without
replacement is then an arbitrary choice of four controls from eight — 70 possible selections, of
which only 16 preserve the perfect balance. **So 77% of the time, covariate balance is worse after
matching than before it**, while the propensity-score distributions are perfectly balanced in every
one of the 70. The paradox is not an artifact of estimation; it is what happens when a scalar score
carries no information to discriminate on.

And then the clause that reconciles the vein, stated here by authors with no stake in it:

> "If the same procedure of pruning the worst-matched units is applied in the context of matching on
> the actual components of `X`, rather than on the scalar propensity score, an increase in imbalance
> is not expected because distances between the original covariate values inform the matching and
> pruning decisions."

This is independent confirmation of the reading `#436` arrives at from the construction side: the
paradox is a property of **pruning on a scalar summary**, not of pruning as such. It is therefore
not an argument against the cell-sort construction `#435` recommended and `#436`/`#437` specify.

## Construction recipe

Not a strategy recipe — a **diagnostic** recipe, and this is the part the lab can use directly. Two
imbalance metrics, both cheaper than `#436`'s `L₁` and both computable on this panel:

**1. Mahalanobis balance.** With `X̄_{T_k}` the vector of covariate means in group `k` and `Σ` the
sample covariance matrix of the *original* (pre-match) data:

```
MB = (X̄_{T1} − X̄_{T0})' Σ⁻¹ (X̄_{T1} − X̄_{T0})
```

Higher is worse. Note what this is and is not: it is a single scalar in the *actual covariate space*
(unlike a propensity score, which leaves that space), it accounts for covariate correlation through
`Σ⁻¹`, and because it is built from group *means* it measures first-moment imbalance only — so it
inherits exactly the limitation `#436` demonstrates with its propensity-score-weighting example,
where all mean imbalance goes to zero while the joint distribution is untouched. It is the cheap
complement to `L₁`, not a substitute for it.

**2. The C statistic.** Fit a logistic model predicting group membership from the covariates
*within the matched set*, and take its C statistic (equivalently the AUC). If the groups are
balanced, the model cannot tell them apart and `C ≈ 0.5`; `C` above 0.5 is imbalance. This is a
classifier-based balance test, it needs no bin choice at all, and it is the one metric in the vein
that is distribution-free in the covariates and reads as a single interpretable number.

**The pruning-curve protocol**, which is `#435`'s refusal test made operational:

1. Match every index unit — no caliper, no pruning yet.
2. Rank matched pairs by decreasing distance (propensity-score distance, or Mahalanobis distance).
3. Prune the single worst-matched pair. Recompute both imbalance metrics. Repeat until one pair
   remains.
4. Plot imbalance against the number of pruned pairs, and **mark on that curve the point at which
   the caliper you would actually have used stops the pruning.** This last step is the paper's
   methodological contribution over King–Nielsen, and it is the step that changes the conclusion:
   the question is not whether the curve eventually rises but whether it rises *before* the stopping
   rule fires.

Calipers used: absolute propensity-score distance of 0.05, 0.025 and 0.01, drawn from the range the
authors describe as standard practice (0.01–0.05); the criterion is met when the maximum
propensity-score distance within any surviving pair falls below the caliper. They also report that
the three calipers are always reached in that order during pruning, which is a sanity property worth
noting — the stopping rules are nested.

Design dimensions varied, since the paradox's severity depends on them: **covariate-set richness**
(19 clinically chosen covariates; then 50 and 100, the extras selected by a high-dimensional
propensity-score algorithm), **treatment prevalence** (resampled up and down while holding dataset
size fixed), and **matching algorithm** (nearest-neighbour, digit-based greedy, and Mahalanobis
nearest-neighbour). Continuous covariates were categorised before entering the propensity model, to
relax its distributional assumptions — itself a coarsening, and worth noting given the vein.

## Robustness evidence (qualitative only)

Peer-reviewed in its field's leading journal; two large real cohorts (roughly 50,000 and roughly
890,000 units) rather than a simulation; 36 matching scenarios across 12 constructed datasets; two
imbalance metrics plus standardised differences reported in supplementary material and said to
support the same conclusions; author team including a methodologist of long standing in the area; no
conflicts declared. Tier B rather than A because it is a single-domain evaluation study whose
headline is a negative about someone else's result, it has not itself been replicated in another
domain, and 88 citations is modest.

**What they found, qualitatively.** Matching substantially improved covariate balance relative to
the unmatched data in every scenario. Imbalance did eventually rise with continued pruning, and did
so sooner when the propensity model used more covariates — consistent with the paradox, and with
King–Nielsen's own mechanism, since more covariates means units with similar scores have more
dissimilar profiles. But in every case the caliper criteria were reached **near the lowest region of
the imbalance curve**, i.e. the paradox's harmful region lay beyond where any conventional analysis
would have stopped. Mahalanobis-distance matching produced near-monotonically *decreasing*
imbalance curves — as the paradox's own logic predicts, since it prunes on covariate-space distance —
but with large covariate sets it achieved good balance only after discarding a very large share of
the matched data, and the authors judge propensity-score matching the better option in the
high-dimensional case for that reason. Their explanation for Mahalanobis' weakness in high dimension
is that it treats all interactions in the covariate space as equally important, which a logit-based
score does not.

**The boundary condition, which is the transferable content.** The paradox should be a practical
concern **only** when (a) the pre-match data are *already* well balanced, so that balance worsens
after the full match or after very few prunings, or (b) pruning is allowed to continue well past
where a reasonable caliper would have stopped. Their claims datasets are in neither position: the
pre-match imbalance is large, which is what gives matching room to help before the paradox bites.

**Their recommendation, which contradicts `#437`'s.** They "stress the importance of checking
covariate balance after PSM in order to identify any increase in covariate imbalance — at the very
least, via a univariate comparison of the pre- and postmatched covariate distributions." Iacus–King–
Porro argue the balance-checking loop should be *eliminated*. The disagreement is real but it is not
symmetric: `#437`'s licence to skip checking comes from the MIB bound, which a propensity-score
match does not have, and this paper is about propensity-score matches. **Both can be right: check
when your construction carries no bound, and the bound is what buys the right not to check.** Also
note that `#436` shows a univariate comparison — precisely what this paper falls back on — is the
check that can pass while the joint distribution is untouched, so this recommendation is the weakest
part of the paper.

**A pointer, not read.** The same first author has a later *American Journal of Epidemiology* study
comparing coarsened exact matching against propensity-score methods, reported in search results as
finding propensity-score matching performs nearly as well as fine stratification, especially at
higher treatment prevalence. That would be adversarial to `#436`/`#437` directly rather than to
`#435`, and it is the right first target if this vein is ever reopened. **It was not obtained or
read, and nothing is carried from it.**

## Implementability here

1. **The headline is a brake on a refusal test the lab adopted last night, and the brake should be
   applied.** `#435`'s rising-curve test, taken literally, would refuse any design whose
   imbalance/pruning curve rises anywhere. This paper says the curve rises eventually in large
   covariate sets as a matter of course, and that the question is whether it rises **before the
   lab's own stopping rule fires**. So the refusal test should be restated: *plot the curve, mark
   where your selection rule actually stops, and refuse only if imbalance at that point is worse
   than at the unmatched starting point.* That is a strictly weaker and more defensible test than the
   one currently in the standing list, and it costs the same single plot.

2. **The C statistic is the cheapest balance diagnostic in the vein and the lab should prefer it to
   a per-covariate comparison.** It needs no bin choice (unlike `L₁`), no covariance inversion
   (unlike Mahalanobis balance), and it answers the question a matched control actually poses: *can
   anything tell the candidate's names apart from the control's names?* On this panel that is a logit
   of selected-versus-control on a handful of coarsened covariates at each rebalance date, and the
   output is a time series of `C` with 0.5 as the null. A control whose `C` sits well above 0.5 is
   not a control, whatever its per-covariate means say. Note the one caveat that comes from inside
   the vein: fitting a classifier on the matched set is fitting a propensity score after the fact,
   so `C` is a diagnostic to read, never an objective to optimise — optimising it would reintroduce
   exactly the specification search `#437` is trying to eliminate.

3. **Mahalanobis balance is computable here but is a first-moment metric, and the panel's covariance
   matrix is the obstacle.** The formula needs `Σ⁻¹` of the original data. With roughly a thousand
   eligible names and a handful of covariates the inversion is fine — but the folder's own
   `notes/2026-10-12-*` estimation work and `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md`
   are about exactly the regime where a sample covariance matrix is not invertible, so this metric
   is safe at **covariate** width and not at **name** width. Keep the distinction explicit: `k` here
   is the number of matching covariates, not the number of instruments.

4. **The pre-match imbalance level decides whether the lab is in the paradox's regime at all, and
   this is a free, answerable question.** The paradox threatens designs whose groups were already
   balanced. The lab's matched controls are drawn from the same eligible panel as the candidate's
   selections, differing only on the selection variable — which is close to the *well-balanced*
   case, i.e. closer to the paradox's dangerous regime than these authors' claims data are. **So the
   reassurance in this paper does not straightforwardly transfer, and the honest conclusion is that
   the lab should measure its own pre-match imbalance before deciding how much weight `#435`'s
   refusal carries.** That measurement is one `L₁` or one `C` on the unmatched cross-section.

Pitfalls:

- **Domain transfer is the main limit and it cuts both ways.** This is healthcare claims data with
  binary treatments, a large control reservoir, and a prevalence that can be resampled. The lab's
  "treatment" is a selection rule applied to a panel of returns, with a control reservoir that is
  the same panel. The *mechanism* statements (what the paradox is, when it bites, what pruning on
  covariate distance does differently) transfer; the *empirical* reassurance does not, for the reason
  in item 4.
- **Treatment prevalence mattered less than expected for covariate balance.** The authors varied it
  substantially and report that it changed the balancing of score distributions much more than the
  balancing of the underlying covariates — the curve shapes barely moved. For the lab that means the
  *fraction of names selected* is not the lever that decides whether a matched control is balanced,
  which is worth knowing before a breadth sweep is run for that purpose.
- **Nothing here licenses a claim about effects.** The paper's own closing caution is that only
  imbalance and study size are controlled directly during matching, so its effect-estimate trends
  support no strong statement. With `#418` in force on this panel, the same holds here a fortiori.

## Related

- `notes/2026-11-11-the-psm-paradox-and-random-pruning.md` (`#435`) — the source this one tests;
  item 1 above is the amendment to its refusal test.
- `notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md` (`#436`) — `L₁`, and the
  demonstration that the univariate check this paper falls back on can pass while the joint
  distribution is unchanged.
- `notes/2026-11-12-coarsened-exact-matching-as-applied-construction.md` (`#437`) — the opposite
  recommendation on balance checking, and why both can hold.
- `notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md` (`#433`) — the
  asymptotic-balance property whose finite-sample failure is the paradox.
- `notes/2026-10-25-testing-portfolio-weights-when-the-panel-is-wide.md` — the covariance-inversion
  regime that bounds item 3.
