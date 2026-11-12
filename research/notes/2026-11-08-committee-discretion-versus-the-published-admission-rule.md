---
title: "Is Stock Index Membership for Sale?"
authors: Li, Liu, Wei
year: 2021
venue: NBER Working Paper 29365 / SSRN 3940053 (venue tier 2 — working paper; the rubric's "with substantial citations" condition is NOT met, see tier note)
url: https://doi.org/10.3386/w29365 · full text read from https://www.nber.org/system/files/working_papers/w29365/w29365.pdf
citations: 4 (Crossref `is-referenced-by-count`, checked 2026-11-08); 1 (Semantic Scholar, same DOI, same date)
sample_period: 1980–2018 (quarterly membership and addition regressions); 2015–2018 for the criterion-by-criterion violation count and the discretionary/rules-based split; Russell 1000 comparison 1996–2016
markets: US (Compustat ∩ CRSP common shares of US-domiciled corporations on eligible US exchanges); one committee-run index (S&P 500) against one mechanically-ruled index (Russell 1000)
tier: B
validation_overlap: true
published_post_2018: true
---

## Mechanism

An index's published methodology is a *rule*; its realised membership is a *decision*. This
source measures the gap between the two, for one committee-run index, by coding the
provider's own published admission criteria as regressors and asking how much of the actual
membership and the actual addition events they explain. The residual is the committee's
discretion.

Why the gap should exist at all is structural rather than behavioural. A published
methodology for a committee index is written with explicit escape clauses — a constituent
may remain after it stops satisfying the criteria until "ongoing conditions warrant"
removal, and criteria may be waived for a name promoted from the provider's own mid- or
small-cap index "if the Index Committee decides that such a move will enhance the
representativeness of the index". Representativeness is not a return objective and not a
size objective, so a rule containing that clause cannot be a rank rule, and the
membership indicator it produces is not a function of size.

The source's own framing goes further, to a conflict-of-interest channel (whether a firm's
purchases of the provider's *other* fee-based services raise its admission probability).
That inferential half is the contested part of the paper and nothing in this note depends on
it; what is used here is the descriptive half — the rule-versus-outcome gap, and its
contrast against a mechanically-ruled index.

## Construction recipe

Three constructions, all reproducible in principle from a membership series plus the
provider's rulebook.

1. **Criterion-by-criterion violation count.** For each admission event, evaluate every
   published criterion at the prior quarter-end: minimum unadjusted market capitalisation
   (a threshold the provider revises over time), two liquidity tests (annual dollar value
   traded over float-adjusted market capitalisation ≥ 1.00, *and* ≥ 250,000 shares traded in
   each of the six months to the evaluation date), a float test (investable weight factor
   above a stated percentage, itself revised), two financial-viability tests (the most recent
   quarter's GAAP earnings positive *and* the sum of the last four quarters' positive),
   a minimum seasoning since IPO, and domicile/incorporation/sector-representation tests.
   Count the fraction of actual additions violating at least one. **Then count the
   non-added names that satisfied all of them at the same moment** — this is the step that
   makes the result interpretable, because it distinguishes "the rule was waived" from
   "no qualifying name existed".
2. **Explanatory-power regressions.** On all minimum-eligible names, quarterly, regress
   (a) membership status and (b) the addition event on the coded criteria, with size-rank
   dummies, a continuous size term, a meets-the-size-threshold dummy, the liquidity,
   earnings, float, domicile and sector-representation variables, their interactions with
   the promoted-from-another-index dummy, and firm plus time fixed effects. Report `R²` for
   the level and for the event separately — they are different objects and they answer
   differently. Repeat the whole exercise for a mechanically-ruled index whose published
   criterion is essentially a size rank.
3. **The deviation-by-rank table.** Bin names by the size rank the published criteria imply
   and report, per bin, the share inside the index. This is the cleanest single output: it
   shows the *shape* of the membership indicator as a function of rank, which is what any
   candidate conditioning on eligibility is implicitly assuming.

**Measured shapes** (counts and shares, not returns). For the committee index, the published
criteria explain roughly three-fifths of the membership *level* over the full sample and
about seven-tenths on the recent subperiod where the rulebook is best documented, but only
**single-digit percentages of the addition events** — the level is partly predictable, the
*change* is close to unpredictable from the rule's own inputs. For the mechanically-ruled
index, a single size-rank dummy explains the great majority of the membership level and a
large majority of the additions. The rank table has the same message: the mechanical index's
membership indicator is near a step function in rank (top bin essentially all in, the bin
below it almost all in, the next bin almost all out), while the committee index's falls off
gradually across four bins, with the second bin close to a coin flip. In the committee
index, about a third of additions in a year violated at least one published criterion, and
*more than a hundred* non-added names satisfied every criterion at the same time.

4. **The discretionary/rules-based split and its matched control.** For each admission,
   search the non-members for names that satisfy *all* published criteria and are stronger
   on the rule's own terms (larger, correct sector, higher rule-implied admission
   probability from a rolling estimate of construction 2). An admission with no such name
   available is a **rules-based entrant**; an admission with one or more available is a
   **discretionary entrant**, and the best-qualified passed-over name is its matched
   **"discretionary out"**. Compare subsequent accounting and return outcomes across the
   three groups, entropy-balanced on pre-admission covariates.

## Robustness evidence (qualitative only)

- **The direction of the headline split replicates a prior result and refines it.** The
  documented post-admission deterioration in operating performance of index additions
  generally is, in this decomposition, concentrated in the discretionary entrants;
  rules-based entrants show no relative decline against the control group. The relative
  *stock*-return ordering runs the same way at multi-year horizons: discretionary entrants
  worst, then the passed-over names, then rules-based entrants. **The reported magnitudes are
  deliberately not transcribed here** — they are performance figures and this folder does not
  carry them; the sign and the ordering are the transferable content.
- **The mechanical-index contrast is the most robust element** because it needs only two
  membership series and a size rank, has no coding judgment in it beyond the rank itself, and
  comes out in the same direction on both the level and the event.
- **Weakest elements, stated plainly.** (i) The paper is an unpublished working paper with
  **4 Crossref citations** and no replication; it has been publicly disputed by the index
  provider. (ii) The violation counts depend on the authors' coding of criteria whose text
  uses "should" rather than "must", and on fundamentals (GAAP earnings, float) measured with
  a lag; a conservatively coded criterion set *understates* eligibility and therefore
  *overstates* violation. (iii) The rules-based/discretionary classification is only as good
  as the rule-implied probability model that ranks the candidates. (iv) The conflict-of-interest
  interpretation is a joint test of the gap *and* a motive; this note uses only the gap.
- **Sample caution for this lab:** the sample runs to 2018, so it touches the first year of
  the lab's validation window. One year of a 39-year sample, and nothing recorded here is a
  dated claim, but `validation_overlap` is flagged `true` on the arithmetic.

## Implementability here

The object is this repo's `eligible` panel. Under protocol v2 the panel's columns appear and
disappear because nine index membership series say so, and `eligible`'s first `True` *is* an
admission event (`#410`). This source says what kind of event that is, and the answer differs
by index.

- **Do not build a candidate whose signal is "anticipate admission".** For a committee index,
  the addition *event* is explained in single-digit percentages by the provider's own published
  criteria — and those criteria include fundamentals this repo does not have. A candidate
  working from daily OHLCV is strictly worse informed than a regression that already fails.
  This is a free refusal test, in the sense of `#413`: it costs no trial and it rules out a
  construction a session could otherwise spend a night on.
- **The complement is the usable half: conditioning on the admission *having happened* is
  fine, and that is what `#411`'s newly-eligible-cohort scout already does.** Nothing here
  weakens that scout; this source only closes the forecasting version of it.
- **The "discretionary entrant" conditioning variable is NOT computable here, and the obvious
  proxy is wrong in a way worth stating.** The classification needs, at the admission date,
  the set of non-member names satisfying every published criterion — i.e. GAAP earnings,
  float factors, domicile and the provider's sector-representation state. The repo's contract
  gives `prices` plus `aux`'s open/high/low/volume/dollar_volume. Of the rule's inputs, only
  the *liquidity* tests are even approximately reachable (via `dollar_volume`), and the one
  the classification leans on hardest — "a larger non-member satisfying all criteria existed" —
  needs **market capitalisation, which needs a share count, which is a fundamental and outside
  the contract** (the same block as `#408`'s). Substituting dollar-volume rank for size rank
  does not rescue it: dollar volume is turnover × price, it is one of the criteria *being
  tested* rather than the criterion the classification uses, and this lab has repeatedly
  measured liquidity-shaped effects as the weakest category it can resolve (`#405`, `#411`'s
  frictions-shaped prior). **Record the mechanism; do not write the candidate.**
- **What it changes for free, and this is the valuable part: the nine membership series are
  not one kind of object.** If any of this panel's nine indices is committee-run and any other
  is rank-ruled, then the relationship between "eligible" and "large" is a near-step function
  in some sub-populations and a gentle gradient in others. Three consequences. (i) Any
  candidate that treats `eligible` as a proxy for a size screen is making a claim that holds in
  one sub-population and fails in another, and the failure is not noise — it is the second
  bin's coin flip. (ii) The equal-weight eligible pool, which is the benchmark *every* skill
  number in this lab is measured against, inherits that heterogeneity; it is a pool of nine
  differently-selected sets, not one large-cap pool (this sharpens `#404`'s and `#407`'s
  structural explanations for `#393`'s high `ρ`). (iii) A cross-index comparison of anything
  conditioned on eligibility compares selection rules as well as economics.
- **Pitfall specific to the panel's construction.** `program.md` says a column appears in
  `prices` only once its name has been eligible, so the *pre*-admission window does not exist
  here — which already blocks the before/after designs (`#412`). This source adds that even
  the *cross-section at the admission date* is unavailable in the form the classification
  needs, because the passed-over names are by definition non-members and therefore not
  columns.

## Annotation added 2026-11-12 — this note is WHY strong ignorability fails on this panel

Written as a fact about index committees, this note turns out to be the load-bearing premise of the
matched-design vein the folder closed over 2026-11-10/11/12, and the connection should be stated
rather than left for a reader to assemble.

`notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` establishes that
admission to the panel is a selection on past performance — i.e. a **treatment** with a propensity
score `pr(eligible | x)` constructible from characteristics the panel holds. The matched-design
literature then says that conditioning on such a score suffices for a causal claim **only under
strong ignorability**: assignment must be independent of the potential outcomes given the observed
covariates (`notes/2026-11-11-the-propensity-score-as-the-coarsest-balancing-score.md`, `#433`).

**This note is the reason that assumption is unavailable here.** If the rule as written is not the
decision as made — if a committee's judgement enters the assignment — then part of the assignment
mechanism is unobserved *by construction*, not merely unmeasured for want of effort. No enrichment
of the observable covariate set fixes it, because the missing variable is a deliberation. That is
the content of `#418`'s standing caveat, and this note is its source.

Three consequences worth carrying:

1. **Everything the lab builds on an eligibility propensity score is descriptive.** A matched
   comparison between admitted and not-yet-admitted names is a statement about covariate balance,
   not an effect estimate. The folder's scalar-score notes are filed on that basis and this is why.
2. **The same discretion is inside the benchmark.** Protocol v3 scores every candidate against the
   equal-weight eligible pool, whose membership is produced by the same discretionary rule. So the
   unobserved component is not confined to the treatment side of a lab comparison; it is in the
   subtrahend of every skill number. `#418` records this; the point here is that it follows from
   *this* note rather than from a property of the pool's weighting.
3. **It does not make the diagnostics worthless, and it says which ones survive.** An imbalance
   measure computed between two groups — `L₁` (`notes/2026-11-12-monotonic-imbalance-bounding-and-the-l1-measure.md`,
   `#436`) or the C statistic (`notes/2026-11-12-does-the-matching-paradox-bite-in-practice.md`,
   `#438`) — needs no ignorability assumption at all, because it makes no counterfactual claim. It
   reports how far apart two observed distributions are. That is the class of statement this panel
   supports, and the class the folder should keep building.

## Related

- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` — the same
  object from the other side: admission carries information about the firm. This source says
  *who decides* and how much of the decision the published rule accounts for.
- `notes/2026-11-07-index-addition-comovement-across-forty-national-indices.md`,
  `notes/2026-11-07-free-float-redefinition-as-a-benchmark-change.md`,
  `notes/2026-11-07-price-weighted-index-and-the-cross-section-of-comovement.md` — the index
  *rule* cluster; those three hold the rule fixed, change it, and apply it across markets. This
  one asks whether the rule is followed.
- `notes/2026-11-08-the-mechanical-counterfactual-index-and-its-tracking-error.md` — the same
  gap measured by building the mechanical alternative explicitly and comparing return series,
  rather than by regression `R²`.
- `notes/2026-11-06-investability-frictions-and-the-microcap-screen.md`,
  `notes/2026-10-09-index-effect-decay-migrations-and-liquidity-provision.md` — the panel's
  admission rule as a screen, and index-effect decay.
