---
title: "Combining several measured signals into ONE long-only book without score weighting — the two-step selection/deconcentration construction, the cross-factor filter that recovers interaction inside a mix, and the long-only asymmetry that says exclusion beats concentration"
authors: Amenc, Ducoulombier, Esakia, Goltz, Sivasubramanian
year: 2017
venue: "The Journal of Portfolio Management 43(5) (Quantitative Strategies: Factor Investing special issue), 99–114. JPM is a tier-1 name in this folder's rubric; see Soundness for why this particular article is nevertheless not graded at the venue's tier."
url: https://doi.org/10.3905/jpm.2017.43.5.099
citations: "12 (Semantic Scholar by DOI, checked 2026-11-23); 5 (Crossref `is-referenced-by-count`, same DOI and date). Two further Crossref records (`10.3905/pa.2018.5.3.249`, `10.3905/pa.5.3.249`) are the *Practical Applications* digest of the same article and carry 0 each — the digest-record artefact, not a second count."
sample_period: "stylized-portfolio tests on US long-term data, 1975-12-31 to 2015-12-31 (score-persistence exhibit from 1971-12-31). Nothing in the article touches 2016 or later."
markets: "US large/mid-cap common stocks (CRSP/Compustat), six factor tilts: size, value, momentum, low volatility, investment, profitability. Multi-market robustness is NOT in this article."
tier: "B− (borderline C+). Read in full; forty-year sample; the construction is specified well enough to re-implement; and its central comparison is run against the *naive equal-weight* version of its own selections, which is exactly the benchmark this folder's combination notes say is the hard one. Held well below the venue's tier for four reasons stated in Soundness: every author works for the index provider whose own top-down indices form the favoured arm of the comparison, the top-down arm's return series are the provider's commercial indices rather than portfolios rebuilt by the authors, no transaction-cost model is applied anywhere (turnover is reported, never priced), and the key tests are single-market with no replication."
validation_overlap: false
published_post_2018: false
read: "Full text, the typeset JPM reprint (17 pp., 2.3 MB) from `docs3.scientificbeta.com/Library/External_use/Academic_papers/JPM_Special_Issue_2017_Cross-Factor_Interactions.pdf`, HTTP 200 on the first request, `pdftotext -layout` → 72 KB of clean text. Body text, exhibit captions and the notes under every exhibit read closely. The exhibit *tables* are images-with-captions in this reprint: their numeric cells did not extract, so every number quoted here comes from the running text, and the article's dated performance levels are deliberately NOT recorded (see Anti-lookahead)."
access_note: "New channel, nominated: `docs3.scientificbeta.com/Library/External_use/Academic_papers/<FILE>.pdf` serves typeset reprints of this group's JPM/FAJ articles with no challenge. It was found by a domain-restricted web search, not by guessing the hostname. The publisher route (`iijournals.com`) and the firm's own press release on `globenewswire.com` both refused an automated client (the latter HTTP 403 with a 694-byte body)."
---

## Why this source is here

`program.md`'s `portfolio-learning` clause ends "**this is where scouted leads become a
challenger**", and the [2026-11-22] aim asked for the one construction corner the coverage audit
left open: how a small number of **already-measured** signals becomes **one** long-only book. This
folder already holds the *weighting* half of that question from several directions — the
forecast-combination puzzle, Breiman's simplex bound, Tu–Zhou's optimal mix of a naive and an
estimated rule, Novy-Marx's linear-composite equivalence, Fitzgibbons et al.'s long-only
integration argument and its peer-reviewed rebuttal. What it did not hold is a source whose
subject is the **selection** half: what the composite score should be *used for* once you have it.

This article's answer is that the composite score should decide **membership and nothing else**,
and it is the first source in the folder to run that comparison against the naive equal-weight
version of its own selections.

## Mechanism

**The object. Two constructions of a multifactor long-only book.** *Top-down* (this folder's
"mix", "portfolio blending") builds one diversified sleeve per factor and blends the sleeves.
*Bottom-up* (this folder's "integration", "signal blending") makes one pass over securities,
ranking them by a composite of the single-factor scores. The authors add a distinction this folder
has not had a name for, and it is the useful one: inside either construction, weights come either
from **diversification-based weighting**, which "essentially ignores information on factor scores
and targets diversification benefits instead", or from **score weighting**, which "completely
ignores any diversification considerations but uses stock-specific factor exposure information to
determine the weight of each stock". The paper's two-by-two is therefore *selection breadth* ×
*weighting rule*, and its finding is that the second axis matters more than the first.

**Claim 1 — a composite score is a return forecast, and it is reliable only in the broad.** The
stated reason not to let scores set weights is that "factor scores are implicit return forecasts,
which are notoriously difficult to make and inherently noisy at the stock level"; that the
characteristic/return relation is validated on *diversified test portfolios* and does not hold
with precision name by name; that it need not be monotone; and that differences among *intermediate*
groups — exactly the differences an arithmetic composite leans on — "are not as reliable" than the
best-versus-worst difference. The conclusion drawn is a design rule: use the score to make "broad
distinctions between stocks that rank well and stocks that rank poorly", then let a weighting rule
that contains no score at all handle the rest.

**Claim 2 — score weighting buys tilt strength and sells risk-adjusted performance.** Across both
composite formulae (arithmetic, geometric) and both selection breadths (half-universe, quintile),
score weighting raises *factor intensity* — the sum of the non-market betas — and is nevertheless
dominated by plain equal weighting of the same selection: "score weighting does not deliver any
clear benefits in terms of average returns or Sharpe ratio over equal weighting, and it is clearly
dominated by equal weighting in terms of information ratio", with lower extreme tracking error and
lower extreme underperformance for equal weighting. The reported *proportions*, which are
construction costs rather than performance levels: extreme tracking error about **a third higher**
under score weighting at the narrow selection, and extreme underperformance about **half again as
large** for the most concentrated construction versus the least. The authors' own summary of the
arithmetic is the sentence this lab has written four times from its own trials: "If more powerful
tilting increases returns but increases risk in the same proportion, there is nothing to be gained
on a risk-adjusted basis."

**Claim 3 — the intensity-is-not-the-objective result, with a clean control.** There is "no clear
relationship" between the factor intensities they measure and risk-adjusted performance; excess
return **per unit of factor intensity** is *lower* for score weighting at both breadths and under
both composites. The control is the right one: they lever the diversified books (long the strategy,
short the cap-weighted reference) up to the *same* factor intensity as the most intense
score-weighted book, and the diversified books still have the higher Sharpe ratio. The analogy they
draw is exact and transfers: loading on high-exposure names to reach a target exposure is the same
error as loading on high-beta names to reach a target beta instead of levering a diversified book.

**Claim 4 — the asymmetry, and it is the most important sentence in the article for this lab.**
"However, in a long-only context, it may be less important to identify factor champions than to
avoid factor losers." Cap-weighted portfolios of the top 5%/10% composite-score names are compared
with cap-weighted portfolios of the *bottom* 5%/10%, and the loser books' underperformance is
**larger in absolute value** than the champion books' outperformance (both signed as expected).
The design consequence they draw: "the elimination of stocks with poor multifactor scores from
long-only portfolios may prove more powerful than the concentration in factor champions, and
interestingly, it can be accommodated by a top-down approach."

**Claim 5 — the mechanism of integration's advantage, restated as a dilution problem, and the fix.**
Why does a mix of sleeves have lower composite exposure at all? Because a stand-alone sleeve for
factor A holds names with "low or negative scores with respect to the other targeted tilt", and
those names "cause accelerated dilution of the scores of targeted tilts within the total
portfolio". The gap between what a mix and a single pass can achieve therefore **widens with the
targeted concentration and with the number of factors, and narrows with factor correlation** — the
same three boundary conditions this folder recorded from Fitzgibbons et al., arrived at
independently. The fix proposed is not to abandon the mix but to remove the diluting names from
each sleeve: filter, then deconcentrate.

**Claim 6 — where score weighting's turnover comes from, mechanically.** Composite scores are only
modestly autocorrelated from one annual rescoring to the next, so "selections based on
backward-looking scores may have a hard time delivering the same intensity in the post-formation
period". A *selection* turns that instability into turnover only when a score moves far enough to
change membership; a *weighting* function of the score turns every small score change into a trade.
In their words, deconcentration weighting "avoids a powerful source of additional turnover" by
"preventing fine distinctions in factor scores from affecting the weights of selection securities".
Measured churn of the selection alone, before any weighting: annual turnover on the order of **90%**
for a cap-weighted top-decile composite selection, crossing **100%** for the top 5%. They also
report the netting effect in a six-sleeve blend: "the cancellation of cross trades across sleeves
more than offsets the turnover required to periodically reset the allocation."

**Claim 7 — a diagnostic distinction this folder should adopt.** Lower volatility is not evidence
of diversification. For their bottom-up books, volatility is materially below the cap-weighted
universe while the Goetzmann–Li–Rouwenhorst measure (portfolio return variance over the
weighted-average variance of its constituents) is *comparable*, which says the volatility came
"primarily by concentration in securities that offer lower total volatility (which heightens
conditionality risk)" rather than from idiosyncratic-risk diversification. Their stated reason the
GLR measure must be high for a champion book is structural: diversification potential falls with
constituent correlation, and names selected on a composite of several scores are more correlated
with each other than average names are.

## Construction recipe

The pieces, in the order a candidate would implement them. All of it is characteristic-and-rank
arithmetic; no optimiser, no covariance matrix.

1. **One score per leg.** For each targeted effect, one "single consensual metric", normalised to a
   rank score in [0, 1] cross-sectionally at each rescoring date.
2. **Composite score.** Arithmetic mean of the normalised rank scores (they test a geometric mean
   too and find "no evidence that geometric averaging is superior"). Note the composite is built
   from *ranks*, not from raw signal magnitudes or z-scores.
3. **Selection, broad.** Per leg, keep the top **half** of the eligible universe on that leg's own
   score. (Their stylized tests also run a quintile selection; the half-universe one is the
   building block of the indices they favour.)
4. **The cross-factor filter — the article's actual contribution.** *Within each single-leg
   selection*, drop the names with the worst **composite** score across the *other* targeted
   factors, shrinking each leg's selection from 50% to **30%** of the universe. The resulting
   per-leg books carry their own tilt *plus* above-average exposure to the other legs, so blending
   them dilutes less. The composite used for the filter deliberately **omits the size score**,
   "because any diversification-weighting scheme induces a tilt away from the largest
   capitalizations that is not diluted by blending" — i.e. do not filter on a characteristic your
   weighting rule already delivers for free.
5. **Weighting, score-free.** Weight each leg's surviving names by a deconcentration rule: equal
   weighting / maximum deconcentration (maximise the effective number of names, which equals equal
   weighting when unconstrained), or an equal-weighted average of several diversification-based
   weighting schemes, which "averages the biases introduced by each scheme and reduces idiosyncratic
   model risk".
6. **Blend the legs.** Equal allocation across the six sleeves is the baseline. The one variant that
   uses optimisation puts it *only at the allocation stage*: allocate across the (already
   diversified) sleeves to maximise the book's geometric average exposure to the targeted factors —
   never at the name level.
7. **Rebalance.** Annual rescoring of all securities (June, in their persistence exhibit) with
   quarterly index reconstitution in the provider's methodology; the article's own argument is that
   the rebalance grid matters far less than whether scores touch *weights*.

## Robustness evidence (qualitative only)

- **Sample.** Four decades of US data, daily returns in USD, for the stylized portfolios. One
  market. No out-of-sample country or region evidence in this article; the authors cite their own
  companion papers for the single-factor version of the same result.
- **Within-sample robustness.** The ordering (deconcentration ≥ score weighting on relative
  risk-adjusted terms) is reported as holding at both selection breadths and under both composite
  formulae, and the instability finding is reported as not driven by any single factor. That is
  genuine internal replication across construction choices, which is the axis this folder cares
  about most.
- **Independent replication: none found.** Citation count is low in both indexes, and the
  comparison has not been re-run by a disinterested party as far as this session could establish.
  The adjacent peer-reviewed literature disagrees in both directions (see Related), so treat the
  *direction* of the comparison as contested and the *mechanisms* as the transferable part.
- **Soundness — the four reasons this is B− and not A.** (a) **Conflict of interest, stated in the
  article's own bylines**: all five authors are at EDHEC-Risk Institute / ERI Scientific Beta, and
  the top-down arm of the comparison *is* that firm's index range, with its data "sourced from the
  ERI Scientific Beta website". The bottom-up arm is reconstructed by the authors from published
  descriptions of competitors' methods. A head-to-head in which one side is the authors' product and
  the other is the authors' implementation of a rival's product is the weakest possible design for a
  horse race, whatever the arithmetic around it. (b) **The benchmark is the firm's own cap-weighted
  index**, and all relative statistics are measured against it. (c) **No cost model anywhere**:
  turnover is reported and discussed, never charged, so "lower turnover" is an input to an argument
  the paper does not close. (d) **Multiple testing is raised against opponents** (they cite
  Novy-Marx and Harvey–Liu–Zhu on the data-mining risk of composite-score engineering) **and not
  against themselves**, though their own exhibits sweep eight stylized constructions and four
  proprietary indices.
- **Anti-lookahead.** The article is full of dated performance levels (returns, Sharpe ratios,
  information ratios, tracking errors over 1975–2015) and none of them is recorded here. What is
  recorded is directional (which construction ranks higher on which statistic), proportional
  (extreme-risk and turnover ratios *between* constructions), or mechanical (how a weighting rule
  converts score noise into trades). The sample ends in 2015, so even the omitted numbers could not
  touch the lab's validation window.

## Implementability here

**This is a construction source for the challenger the leaderboard has never built, and almost all
of it runs on this repo's data.** Rank scores, a composite of ranks, a selection, a deconcentration
weighting and a sleeve blend need nothing but the panel and the legs the lab already has. The
specific adaptation:

- **Use each family lead's own score as its leg's score.** The lab's leads are already
  cross-sectional scores on the `eligible` panel. Normalise each to a within-date rank in [0, 1] —
  which is what the lab's own `#375`/`#376` work says is the only part of a score a long-only book
  can express anyway — and average the ranks arithmetically for the composite.
- **The one new operator, and the reason this note exists: a filter, not a weight.** The lab has
  measured the **mean** operator (bounded by its legs, refuted), the **max** operator, the
  **intersection**, and equal-weight ensembles of finished *return series* (monotone decreasing
  against the best member). It has never measured *per-leg selections filtered by the other legs'
  composite, then deconcentrated*. That construction is outside Breiman's simplex bound and outside
  Novy-Marx's linear-composite equivalence for the same reason the max operator is: the filter is a
  nonlinearity applied **before** portfolio construction, inside each leg, not a reweighting of
  finished books. The folder's own standing rule — "the value of an aggregation operator is the
  value of its nonlinearity" — says this is the next operator to try, and it is cheap.
- **The asymmetry claim is directly testable here and it fits the lab's own geometry.** `#375`
  established that on an equal-weighted pool every excluded name receives the identical `−1/N`
  active weight, so a score's information is usable for *membership* and unusable for *ordering the
  bad names*. Claim 4 says the exclusion lever is the stronger one in a long-only book to begin
  with. Together they predict that a candidate built as "exclude the worst composite scores from a
  broad selection, equal-weight the rest" should beat both a champion-concentrated book and a
  score-weighted book **on skill against the equal-weight pool**, which is exactly the v3 statistic.
- **The direct tension with `learnings.md`, which must be stated and not smoothed over.** The lab
  has measured, on the v1 140-name panel inside the momentum family, that **magnitude weighting
  carries information beyond concentration** (≈0.116 of Sharpe net of the de-concentration price)
  and that de-concentration *costs* roughly 0.05 of Sharpe per 30% of HHI. Claim 2 says
  score weighting is dominated by equal weighting of the same selection. Both can be true, and the
  candidate reasons are worth pre-registering because they are testable: (i) the lab measured
  **absolute Sharpe**, this paper's dominance is clearest on **information ratio** and on extreme
  *relative* risk — and the v3 objective moved the lab onto the relative statistic; (ii) the lab's
  measurement predates v3's drift-and-turnover charging, which is where score weighting pays its
  bill; (iii) a ~140-name survivor panel cannot show the "concentrated in a few highly correlated
  names" failure this paper diagnoses with the GLR measure, whereas a ~1,000-name panel can. Do not
  import this paper's conclusion over the lab's own measurement; re-measure it under v3 and report
  which of (i)–(iii) explains the gap.
- **Free measurements this source motivates, all on stored objects, none needing the holdout.**
  (a) **Score persistence**: the within-date rank autocorrelation of each lead's score between
  consecutive rebalance dates, and of the composite. Claim 6 says a weighting function of a
  modestly-persistent score is a turnover machine; the lab can read the persistence off its own
  scores before building anything. (b) **The GLR ratio** of any candidate book — portfolio return
  variance over the weighted-average variance of its holdings — printed next to its volatility, to
  separate "this book is less volatile because it diversified" from "this book is less volatile
  because it selected low-volatility names", which is the exact confound `learnings.md` records as
  the refuted low-vol family and as a repeated confound in de-risking trials. (c) **The dilution
  measurement**: for each pair of leads, the average composite rank of the names one lead selects on
  the *other* lead's score. That is the quantity Claim 5 says the filter removes, it is computable
  from stored holdings, and it predicts the filter's effect size before a trial is spent.
- **What does not transfer.** The factor set (profitability, investment) needs fundamentals and is
  out of scope; the size leg is explicitly redundant under deconcentration weighting, and on this
  repo's panel equal-weighting a broad selection of ~1,000 large-cap index members already carries
  whatever small-size tilt is available. Their "multi-strategy" weighting (an equal-weighted average
  of five diversification schemes, several of them covariance-based) collides with the lab's own
  refutations of inverse-vol and risk-parity weighting on this universe; the maximum-deconcentration
  variant — plain equal weighting of the selection, subject to the engine's 25% cap — is the one to
  use. Their netting claim (Claim 6's last sentence) is measured on six sleeves and should not be
  carried to a two- or three-leg blend, where this folder's existing note already prices netting at
  close to nothing.
- **Cost sense check under v3.** A top-decile composite selection churning ~90–100% a year is a
  *selection* turnover figure with no cost attached; under v3's 15–40 bps per side plus statutory
  taxes, and with drift charged between rows, that is a real bill. The paper's qualitative ordering
  — selection-driven turnover < score-weighting-driven turnover, and cross-sleeve netting reduces
  the blend's bill below the sum of its sleeves' — is the part to carry, with the lab's own numbers
  substituted.

## Related

- `notes/2026-08-31-signal-blending-vs-portfolio-blending.md` — Fitzgibbons et al. argue the
  opposite ranking (integration beats the mix under a long-only constraint) with the *same* three
  boundary conditions (signal correlation, active-risk target, number of signals). This article is
  the mirror-image practitioner position, and the two together say the ranking is not settled.
- `notes/2026-11-23-exposure-matched-blend-comparison-and-the-active-risk-crossover.md` — the
  peer-reviewed framework in which both can be right: the comparison *crosses over* in the level of
  active risk.
- `notes/2026-11-23-long-only-sleeve-mix-and-how-much-of-the-efficient-book-it-captures.md` — the
  theory side, which prices the mix's inefficiency against an optimised long-only book of
  individual securities.
- `notes/2026-09-08-stacked-regressions-nonnegative-weights.md` and
  `notes/2026-09-01-multi-signal-overfitting-critical-t.md` — the two results that bound every
  *reweighting* of finished long-only books. The filter in Claim 5 is the construction that sits
  outside both bounds.
- `notes/2026-11-03-attainable-underweight-and-the-long-only-constraint.md` (`#375`, `#376`) — the
  one-bit-truncation geometry that makes Claim 4's "avoid losers rather than pick champions" the
  natural operator on an equal-weighted pool.
- `notes/2026-08-20-trading-diversification-combining-signals.md` — the cost-side counterpart:
  trades net inside a combined book. Claim 6's six-sleeve netting statement is the practitioner
  version, and this folder's existing caution about two- and three-leg blends still applies.
- `notes/2026-09-07-hierarchical-risk-parity-clustering-allocation.md`,
  `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` — equal weighting as the
  benchmark that keeps winning, now joined by a provider-authored source that also could not beat it
  with its own score.
- `experiments/learnings.md` — the magnitude-weighting and de-concentration constants this note is
  in explicit tension with (see Implementability).
