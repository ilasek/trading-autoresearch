---
title: "The OPINION-LEADER model — the closed-form DISCOUNT on a correlated bloc's weight, the condition under which a panel's competence collapses to one judge's, and the answer-key-free way to score a judge's competence from its agreement with the panel"
authors: Grofman, Owen, Feld
year: 1983
venue: "Theory and Decision 15(3), 261–278. Peer-reviewed; a standard venue for decision theory and social choice (tier 1 within its field). The paper is a review that states thirteen theorems and attributes each; several of the results it reports were, at the time, unpublished manuscripts by Owen, Feld or Grofman, and this review is their primary published statement."
url: https://doi.org/10.1007/BF00125672
citations: "303 (Crossref `is-referenced-by-count`, checked 2026-11-25); 473 (Semantic Scholar by DOI, same date)."
sample_period: "n/a — theorems and arithmetic examples. The one empirical reference in the text (a correlation between legislative size and supermajority requirements in US state legislatures, Crain & Tollison 1977) is not used for any claim recorded here."
markets: "None."
tier: "A on citation count, venue and the fact that the content is analytic. Two honest downgrades that a user must carry: (a) it is a REVIEW, and the two results this note is built on — Theorem XII and its corollary — are attributed to *Owen, unpublished 1980*, so this folder holds them second-hand with no proof and no independent published statement found; (b) the displayed formula (13) as printed does not reproduce the paper's own worked number (see below), so only its corollary (14), which is self-checking at its stated limit, is used."
validation_overlap: false
published_post_2018: false
read: "Full text, 18 pp. (261–278), 821 KB PDF from Grofman's UC Irvine faculty page, HTTP 200 first request; `pdftotext -layout` → 41 KB of text, 244 instances of ` the `, parenthesis balance 256/259. Every formula quoted below was re-extracted page-by-page in `-raw` mode and cross-checked against the surrounding prose, because the `-layout` pass mangles displayed fractions and Greek letters (`α` prints variously as `a`, `ot` and `ct`; `β` as `B`; one probability prints as `0.05` where the prose and the dependent corollary both require `0.5`)."
access_note: "Same channel as the Shapley–Grofman note filed tonight: `sites.socsci.uci.edu/~bgrofman/<NN>%20<Authors>-<Title>.pdf`. Three distinct papers served at HTTP 200 on first request from this one directory. A scholar's own numbered reprint archive is the strongest form of the faculty-page channel."
---

## Why this source is here

It is the only source found tonight that gives the [2026-11-24] aim's object — **the weight to
attach to a correlated bloc of judges** — explicitly, in closed form, with an exact degenerate
limit. Criterion (i): the judges are explicitly correlated (through a common leader) and may be of
unequal competence. Criterion (ii): equation (14) below. Criterion (iii): the limit as the
dependence parameter goes to one is stated in the text and is the collapse the aim predicted.
Criterion (iv): it needs one dependence parameter and one competence per judge, and the paper
supplies a free estimator for the competence (Theorem VII).

## Mechanism

**The dependence model (assumption (1)′ of Theorem XII).** Each judge has competence `p` *when
voting independently*. With probability `α` a judge instead votes in accordance with a single
designated judge — the opinion leader — who also has competence `p`. Write `β = 1 − α`. So `α` is
a **common-factor loading**: one shared source of opinion, identical for everyone, plus independent
idiosyncratic judgment. This is the simplest dependence structure that produces positive pairwise
correlation among votes without needing a full joint distribution, and it is the structure the lab's
situation actually resembles (several scores computed from the same panel of prices).

**Theorem XII (Owen, unpublished 1980, "Think for Yourself, John").** For large `N`, the probability
the group's majority is correct falls from `P_N` (its independent-judge value) toward the leader's
own competence. *The text's displayed formula (13) is recorded here as printed —
`(α + βP_N)/(1 + α)` — with the warning that it does not reproduce the paper's own worked example,
so it should not be used.* What **is** reliable, because it is restated in prose and checks
arithmetically, is the qualitative claim and the mechanism behind it:

> "the higher `α` the lower the judgmental competence of the group majority … if `α = 0.2` and
> `p = 0.6`, then `E(P_N) = 0.6` for all `N`; i.e., the group majority is only exactly as competent
> as the opinion leader (since the opinion leader's voting bloc can be expected to determine the
> election outcome) and the Condorcet Jury Theorem effect of raising the group competence toward 1
> if `p > 0.5` is lost entirely."

**The arithmetic behind that example, derived here and not stated in the text** (elementary, and
recorded because it turns the example into a usable threshold): the expected vote share for the
leader's choice is `α + βp` when the leader is right and `α + βq` when the leader is wrong, with
`q = 1 − p`. So for large `N` the majority tracks the leader exactly whenever `α + βq > 1/2`, i.e.
whenever

```
α  >  (p - 1/2) / p
```

With `p = 0.6` that threshold is `0.167`, and the paper's `α = 0.2` clears it — which is precisely
why its worked number is `E(P_N) = p = 0.6` for every `N`. **The weaker the judges, the lower the
common-factor loading at which the panel stops being a panel.** At `p = 0.52` the threshold is
`0.077`.

**Corollary to Theorem XII (the instrument) — the discounted bloc weight.** *If we observe a bloc
of `n` judges casting identical votes, the weight to attach to those `n` votes, which would be
`n·log(p/q)` if each had been reached independently, should be reduced to approximately*

```
log( p / q )  +  (n - 1) · log[ (α + βp) / (α + βq) ]
```

The reading is exact and is what the aim asked for: **the first member of a correlated bloc is
worth a full log-odds vote and each additional member is worth a strictly smaller one**, because
the likelihood ratio of "this judge also agreed" is `(α + βp)/(α + βq)`, not `p/q`. The text's own
limit statement: for `p > 1/2`, `(α + βp)/(α + βq)` is **decreasing in `α` and approaches 1 as
`α → 1`** — at which point every judge after the first contributes **zero** weight and the bloc *is*
one judge. That is criterion (iii) discharged in closed form, and it is the formal version of
`#522`(c) ("three near-duplicate leads are one opinion counted three times").

**Theorem VII (Feld, unpublished) — competence from agreement, with no answer key.** Let `r_i` be
the proportion of decisions on which judge `i` agrees with the panel's majority verdict. Then
`(r_i − 0.5) ∝ (p_i − 0.5)`; and for `0.55 < p_i < 0.76`, `(p_i − 0.5) ∝ ln(p_i/(1 − p_i))`, i.e.
the log-odds weight is approximately **linear** in `(p − 0.5)` over that range. The paper's own
title for it is "Correcting a True-False Exam Without an Answer Key".

**Corollary to Theorem XIII (Feld, unpublished) — the two results composed.** *The optimal log-odds
weights can be approximated by `w_i ∝ (r_i − 0.5)`*, where `r_i` is the agreement rate with the
majority. No ground truth is required anywhere in the chain.

**Context from the same review, recorded because it bounds what any of this can buy.**
- Theorem XIII is the log-odds weight itself (the Shapley–Grofman theorem, filed tonight in its own
  note), with the same worked example: competences `(0.9, 0.9, 0.6, 0.6, 0.6)` give best-member
  `0.9`, simple majority `0.87`, optimal weighted rule `0.93`.
- Theorem XIII's closing remark: "especially as `N` is large, optimal weights do not improve
  substantially on simple majority rule" (attributed to unpublished work in progress).
- Theorem VI: with every `p_i > 0.5` **and independence**, a larger majority is more likely to be
  right. With some `p_i < 0.5` it fails — the review's example `(0.8, 0.8, 0)` gives a 2-of-3
  agreement a posterior of `0.67` and a 3-of-3 agreement a posterior of **zero**.
- Theorem X (generalised Condorcet, Owen–Grofman–Feld): for any competence distribution however
  skewed, average competence above a half sends `P_N → 1`; below, to 0; **at exactly a half the
  limit is only bounded**, `0.39 < lim P_N < 0.61`.
- Theorem IX and its corollaries: with the *total* competence fixed, `P_N` is maximised by extremely
  lumpy competence distributions, and a panel with average competence **below** a half can have
  `P_N` above a half (e.g. `(0.72, 0.72, 0)`), while a panel with average above a half can have
  `P_N` below it (e.g. `(1, 0.28, 0.28)`). The average competence of a panel is not a sufficient
  statistic for the panel.

## Construction recipe

For a panel of `k` scoring rules over the same items:

1. **Binarise.** Each judge's verdict per item is "above the cut" / "below the cut". The whole
   apparatus is about dichotomous choices.
2. **Estimate `r_i`** = each judge's agreement rate with the panel's majority verdict, over dates
   and items. Costs nothing and needs no outcomes.
3. **Approximate weights** `w_i ∝ (r_i − 0.5)`, valid as an approximation to the log-odds weight
   over the competence band the review states.
4. **Estimate the common-factor loading `α`.** The model implies the pairwise agreement rate
   between two non-leader judges is `α² + 2αβ·(…) + β²(…)`; the cheap version is to fit `α` so that
   the model's implied pairwise agreement matches the measured one, or simply to read the first
   principal component's share of the judges' score variance as `α`.
5. **Discount blocs.** For a bloc of `n` judges that habitually vote together, use
   `log(p/q) + (n−1)·log[(α+βp)/(α+βq)]` as the bloc's total weight instead of `n·log(p/q)`.
6. **Check the collapse condition `α > (p − 1/2)/p` before building anything.** Above it, adding
   judges does nothing at all: the panel's competence equals one judge's.

## Robustness evidence (qualitative only)

Analytic results, so there is no sample to be fragile — and correspondingly no replication in the
empirical sense. The relevant robustness question is whether the results are *independently stated*
elsewhere, and here the answer is mixed and must be carried: **Theorem XIII is independently derived
in at least three literatures** (Shapley 1979; Nitzan & Paroush 1982; and in pattern recognition,
Pierce 1961 / Minsky & Papert 1971 / Duda & Hart 1973), whereas **Theorem XII and its corollary are
attributed to a single unpublished 1980 manuscript by Owen** and no independent published statement
of them was found tonight. The common-factor dependence model itself is standard and recurs in the
later jury literature (it is the "opinion leader" theme that Boland (1989) and its successors
develop), which is weak corroboration of the model but not of this corollary's constant.

The review's own honest limits are stated in its text: several theorems "need some qualifications",
the approximations in Theorems VII and XII are explicitly approximations, and the band
`0.55 < p < 0.76` in Theorem VII is stated without an error bound.

## Implementability here

**What this gives the lab that nothing in the folder did.** A **price for a correlated lead**. The
lab's decorrelation screen is a threshold — `learnings.md` kills a candidate blend at rank
correlation 0.89 and `leaderboard.json` groups mechanisms at active-return correlation ≥ 0.5 — and
a threshold answers "in or out" but not "worth how much". The corollary to Theorem XII answers the
second question in closed form, with the right limit behaviour at both ends (`α → 0` recovers the
full `n·log(p/q)`; `α → 1` makes every judge after the first worth exactly nothing).

**The free measurement this adds, and it needs no returns at all.** Compute each lead's agreement
rate `r_i` with the composite's own membership decision, over the dates the lab already stores
scores for. By Theorem VII that is a monotone proxy for the lead's competence, and by the corollary
to Theorem XIII it is approximately the optimal weight. **This is the only competence estimator in
the folder that does not consume an evaluation**, and it is therefore the one a session can run
before proposing a composite rather than after measuring one.

**The screen that may close the question for free.** Convert the leads' measured ICs to `p` by the
`#518` regime map (`p = 1/2 + τ/2`), estimate `α` as the first principal component's share of the
lead-score variance, and check `α > (p − 1/2)/p`. At the lab's effect sizes `p` is within a few
hundredths of a half, so the threshold is **small** — at `p = 0.52` it is `α > 0.077` — and a panel
of leads that all read the same price panel will very likely exceed it. If it does, the honest
conclusion is that *combining those particular leads cannot raise the panel's competence above the
best single lead's*, and the lab should spend its trials on a genuinely different mechanism rather
than on composite construction. That is a cheap, falsifiable pre-trial refusal, and it is the
sharpest practical thing in tonight's vein.

**What does not transfer.**
- The model has **one** common factor and assumes every judge loads on it identically. A panel of
  deliberately different signals has several shared factors with unequal loadings; `α` estimated as
  a single number is then an average, and no error bound is available.
- `p` is a per-decision competence with a ground truth. The lab's "ground truth" (did this name beat
  the pool over the next month?) is itself noisy, so `r_i` measured against the composite is the
  *only* clean quantity in the chain; competences inferred from it inherit Theorem VII's unbounded
  approximation.
- Theorem XII is large-`N`. The lab has `k` of order 2–5 leads. The corollary's per-member discount
  is still the right shape at small `n`, but the "majority tracks the leader" collapse is an
  asymptotic statement and a 3-lead panel does not have a law of large numbers.
- Nothing here is a return claim, and none is recorded.

## Related

- `notes/2026-11-25-optimal-weights-for-judges-of-unequal-competence.md` — the primary statement of
  the log-odds theorem and the bloc-partition recipe this note prices.
- `notes/2026-11-25-what-a-pairwise-correlation-does-not-pin-down.md` — the identification result
  that says a measured pairwise correlation does **not** determine a panel's competence, which is
  the reason to prefer this note's structural `α` over a correlation plugged into a formula.
- `notes/2026-11-24-when-a-positional-rule-is-the-right-aggregator.md` (`#518`) — the independent-
  judge model and the IC→`p` regime map used above.
- `notes/2026-11-24-rank-aggregation-positional-versus-pairwise.md` (`#522`(c)) — the anti-candidate
  this note turns into a formula.
- `notes/2026-11-23-filter-then-deconcentrate-instead-of-score-weighting.md` (`#513`) — the
  construction the discount attaches to.
