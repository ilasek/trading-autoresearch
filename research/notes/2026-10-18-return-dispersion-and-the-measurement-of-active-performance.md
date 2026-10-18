---
title: "Return dispersion and the measurement of active performance — why a period's active return has to be divided by that period's cross-sectional volatility"
authors: de Silva, Sapra, Thorley (2001); Ankrim, Ding (2002); the restatement, critique and replication read here are Gething (2014)
year: 2001; 2002; 2014
venue: Financial Analysts Journal 57(5), 29–42 (venue tier 1, practitioner-academic); Financial Analysts Journal 58(5), 67–73 (same); University of Cape Town MPhil dissertation, Department of Actuarial Science (venue tier 4 — a student dissertation, used here only as a restatement channel and as an independent out-of-US test)
url: https://doi.org/10.2469/faj.v57.n5.2479 · https://doi.org/10.2469/faj.v58.n5.2469 · https://open.uct.ac.za/bitstream/11427/13123/1/thesis_com_2014_gething_b.pdf
citations: de Silva–Sapra–Thorley — 40 (Crossref `is-referenced-by-count`, checked 2026-10-18), 54 (OpenAlex, same date), 59 (Semantic Scholar, same date). Ankrim–Ding — 32 (Crossref, same date), 45 (OpenAlex, same date); Semantic Scholar reports 1, which is a broken record rather than a citation count and is not used. Gething — not indexed (Crossref and OpenAlex title searches both return no match, checked 2026-10-18; Semantic Scholar not tried, since a dissertation with no DOI cannot be resolved by the endpoint this environment can rely on), as expected for a student dissertation
sample_period: the two FAJ articles study US (and, for Ankrim–Ding, several non-US) equity markets and active-manager cross-sections over the late 1990s and around 2001, with a twenty-year Japanese series as the historical comparison; Gething uses South African retail and institutional funds over two windows inside 2006–2013
markets: United States large-cap plus "several equity markets" outside the US including Japan (Ankrim–Ding); South Africa, JSE All Share universe (Gething)
tier: B — the mechanism rests on two tier-1 practitioner-academic articles whose **bodies were not read**, plus one tier-4 restatement that was read in full. The algebra below is simple enough to verify independently; the empirical claims are recorded as the sources state them and no magnitude is carried over
validation_overlap: false
published_post_2018: false
read: **Neither FAJ article's body was obtained.** Both are CFA Institute premium member content: `rpc.cfainstitute.org` serves a public landing page carrying the **verbatim author abstract** (HTTP 200, ~58 KB) and no PDF, and OpenAlex reports `oa_status: closed, any_repository_has_fulltext: false` for both DOIs with no repository location to try. The abstracts quoted below are from those two pages. The *method* — the dispersion-weighted regression — is recorded **second-hand** from Gething (2014), read in full from `open.uct.ac.za` (HTTP 200, 781 KB; `pdftotext -layout` → 133 KB of text, 683 instances of `" the "`, no `( )` dropout), which restates Ankrim–Ding's CSV definition and de Silva et al.'s adjustment with their equations and then tests both. This follows the precedent of `2026-08-29-range-based-volatility-estimators.md`, where Parkinson and Garman–Klass are recorded via Molnár's restatement. Treat the construction as reliable and the two articles' own arguments as unread.
---

## Mechanism

The two FAJ articles make one claim and it is a claim about **measurement, not about returns**:
the spread between good and bad active outcomes is mostly a function of how widely the underlying
securities' returns are spread on the day, and only secondarily a function of skill.

de Silva, Sapra and Thorley state it this way (verbatim from the abstract): *"The wide dispersion
in security returns has led to correspondingly wide dispersion in fund returns … We argue that the
wide dispersion in fund performance is a natural result of increased security return dispersion and
has little to do with changes in the informational efficiency of the market or the range of
managerial talent."* The consequence they draw is the useful part: *"The dramatic increase in return
dispersion warrants a reexamination of traditional methodologies for measuring fund performance
that implicitly assume constant dispersion. We show how performance benchmarking can be extended to
incorporate the information embedded in return dispersion … by correcting fund alphas with a period-
and asset-class-specific measure of security return dispersion."*

Ankrim and Ding supply the robustness half, also verbatim: *"We demonstrate that changes in the
level of cross-sectional volatility have a significant association with the distribution of active
manager returns. We further show that these observations are neither unique to U.S. equities nor
merely a product of the 'technology bubble'; they are observable in several equity markets."* Per
Gething's restatement they answer three questions explicitly — the association is not confined to
US large-caps, a long Japanese series shows it is not unprecedented, and comparing inside and
outside the period of a sector boom shows no statistically significant difference — i.e. it is a
structural relationship, not an episode.

**Why this is mechanism and not bookkeeping.** An active book's return relative to a benchmark is
`a'r`, where `a = w − w_bench` is the vector of active weights. Hold the active weights fixed and
widen the cross-section of `r`: the active return widens with it, in both directions, with no change
in skill. So active return measured in raw units is in units that change over time, and a time
series of such measurements is **heteroskedastic by construction**, with the scale given by the
day's cross-sectional volatility. Every statistic computed from that series under an
equal-variance assumption — an OLS alpha, a mean, a `t`-statistic, a Sharpe-like ratio — is
mis-specified in a knowable way. Gething's framing, which is the clearest of the three sources, is
exactly this: dispersion in fund returns produces a heteroskedastic time series, and that is what
makes plain OLS the wrong estimator. His closing line is the mechanism in one sentence: *managers
cannot expect to generate alpha without the existence of CSV.*

## Construction recipe

- **The dispersion statistic** (Ankrim–Ding's definition, as restated by Gething). For a market of
  `N_t` assets, cross-sectional **variance** in period `t` is

      X²_t = Σ_i w_it ( r_it − r_mt )²,     r_mt = Σ_i w_it r_it

  with `w_it` the weight of asset `i` at the **beginning** of period `t`. Cross-sectional
  volatility is `X_t = sqrt(X²_t)`. Substituting `w_it = 1/N_t` gives the "uniform" (equal-weighted)
  CSV; leaving the weights as market-capitalisation weights gives cap-weighted CSV. This is the
  identical object to the `CSV` of
  `2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md`, reached from the
  performance-measurement side a decade earlier and with no estimator theory attached.
- **The uncorrected baseline.** The ordinary market-model regression on excess returns,
  `(r_P,t − r_F,t) = α_P + β_P (r_M,t − r_F,t) + ε_P,t`, estimated by OLS. Its implicit assumption is
  that `Var(ε_P,t)` is constant across `t`. That is the assumption dispersion breaks.
- **The correction: weighted least squares with weights proportional to inverse CSV.** Multiply both
  sides of the regression by `sqrt(w_t)` and estimate by OLS on the transformed data:

      sqrt(w_t) · r_i,t = sqrt(w_t) · ( α_i + β_i r_m,t + ε_i,t ),
      sqrt(w_t) = annualised, normalised **inverse** CSV over the period associated with t

  i.e. periods of wide cross-section are down-weighted and periods of narrow cross-section are
  up-weighted, because the latter carry more information per observation about the mean. This is
  nothing more exotic than the textbook heteroskedasticity correction, and Gething says so,
  quoting Wasserman: fit well where the noise is small, and expect to fit poorly where it is big.
- **The two measures the correction can use.** de Silva et al.'s abstract specifies a **period- and
  asset-class-specific** dispersion measure, so the dispersion used must be the dispersion of the
  *opportunity set the book actually drew from*, not of some wider market. Gething had to use a
  market-wide index CSV because fund-level and style-level CSV were unavailable, and flags this as
  the weakest part of his implementation: a market-average CSV makes the adjustment less accurate
  than a sector- or style-specific one would be.
- **The diagnostic step that belongs with it.** Both the restated method and Gething's own procedure
  test for heteroskedasticity *first* and then apply WLS, rather than applying WLS unconditionally.
  The question "is this series heteroskedastic in dispersion?" is separately answerable and should
  be answered before anything is re-weighted.

## Robustness evidence (qualitative only)

- **Multi-market, by design.** Ankrim–Ding's stated contribution is that the dispersion/active-spread
  association is present outside US equities and outside one episode, and Gething is an independent
  test in a third market (South Africa) a decade later with a different fund population. The
  *relationship* is about as well travelled as a practitioner result gets.
- **The sharpest finding is Gething's and it is a negative.** Applying the inverse-CSV weighting
  changes the **values** of fund alphas but a Wilcoxon rank-sum test detects **no significant
  difference in the rankings** of funds between the OLS and WLS estimates. Rank-wise, the correction
  does nothing. He is explicit that the value changes are small, and that their practical
  consequence is for remuneration rather than for identifying who is good. **A correction that moves
  every estimate but preserves the order buys nothing for selection — it buys calibration.** That is
  the single most transferable sentence in this note.
- **And the critique, which is the reason this is Tier B and not Tier A in spirit.** Gething's stated
  objection to the CSV-adjusted alpha is that fund-return dispersion and security-return dispersion
  are *intrinsically linked*, so adjusting for CSV also adjusts away part of whatever dispersion
  genuine differences in talent produce; the two cannot be disentangled from fund returns alone. He
  reports his simulation showing alpha dispersion falling under the adjustment, and that this did
  not reproduce in his real-market data — which he attributes to sample size and data problems
  rather than claiming either way.
- **The WLS weighting choice is itself a free parameter** with a material effect on the estimated
  coefficients, acknowledged in the source. Choosing it after seeing results would be a researcher
  degree of freedom of exactly the kind the deflated-Sharpe machinery exists to punish.
- **Replication status: none in the formal sense.** Neither FAJ article appears in
  Hou–Xue–Zhang or Jensen–Kelly–Pedersen, because neither proposes an anomaly. The citation counts
  are modest and typical for FAJ methodology pieces.
- **Methodology honesty: unassessable for the two primaries**, whose bodies were not read. For
  Gething: data limitations, the proxy-benchmark problem and the weighting-choice problem are all
  stated by the author rather than discovered by the reader, which is the right sign.

## Implementability here

**This is not a candidate. It is a correction to how the lab reads its own numbers, and it is free
and retrospective.** Nothing below touches the engine or the gate.

- **The lab's `skill` statistic is exactly the object these sources are about.** Under v3, skill is
  validation Sharpe minus the equal-weight eligible pool's Sharpe on the same days — a statistic
  built from a series of **active** returns relative to an equal-weighted benchmark, averaged over a
  six-year window. The sources' claim is that the per-day variance of that series is proportional to
  that day's cross-sectional dispersion, which on this panel moves by a large multiple across the
  window. The implication is a property of the lab's error bars, not of its edge: **a candidate's
  skill estimate is a mean of observations with non-constant variance, and treating them as
  exchangeable overstates the information in the wide-dispersion days.**
- **The free measurement, which can be run before any candidate is written.** Take any stored trial's
  daily active-return series and the daily equal-weighted `CSV` of the eligible pool over the same
  dates. (i) Test whether `|active return|` scales with `CSV_t` — this is the heteroskedasticity
  test the method says to run first. (ii) If it does, recompute each lead's skill with observations
  weighted by `1/CSV_t`, and compare both the point estimates **and the bootstrap intervals**.
  (iii) Then apply Gething's test: does the *ordering* of the board change? His South African answer
  was no. **Pre-register that prediction before looking**, because if the order is unchanged here
  too, the right conclusion is that the correction belongs in the error bars and nowhere else, and
  the lab should stop there rather than building anything on it.
- **The one place it could matter more than calibration.** `scripts/rank_trials.py` puts every v3
  trial in tier 1 — the data cannot separate them. Tier width is driven by the variance of the skill
  difference, and a variance-stabilising transform is precisely a way to narrow an interval without
  touching the point estimate. If the dispersion correction shrinks the intervals materially, it
  makes the board more resolvable with no new trials spent. If it does not, that is itself worth
  recording: it says the board's irresolution is not a heteroskedasticity artifact.
- **Use the pool's own dispersion, and nothing wider.** de Silva et al.'s "asset-class-specific"
  qualifier is binding here: the dispersion that scales a candidate's active return is the dispersion
  of the **eligible panel it selected from**, not of a global index. The lab's `eligible` mask makes
  this exactly computable, and Gething's inability to do the style-specific version is the one
  limitation of his test that this lab does not share.
- **Two warnings carried from the sources.** First, the correction removes signal along with noise:
  if a candidate's edge is genuinely larger when the cross-section is wide — which is what an
  opportunity-set story *predicts* — then dividing by dispersion deletes the very thing worth
  measuring. The honest use is as an **estimator of the same quantity with lower variance**, checked
  against the unweighted estimate, never as a replacement score. Second, the weighting is a free
  parameter; fix it as plain `1/CSV_t` in advance and do not tune it.
- **What this does not license.** It is not a reason to reinterpret any recorded verdict. The gate's
  statistics are owned by `engine/protocol.py`, the manual forbids reinterpreting them, and
  everything here is diagnostic work that scores no returns — which the budget rules make free and
  unlimited.

## Related

- `2026-10-18-cross-sectional-variance-as-model-free-idiosyncratic-volatility.md` — the same `CSV`
  statistic with its estimator theory, its admissibility condition and its biases. Read that note
  before computing the denominator this one asks for.
- `2026-10-18-dispersion-beta-and-the-cross-section.md` — the third use of the same statistic, as a
  priced state variable rather than a scale.
- `2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — Grinold's `IR ≈ IC · sqrt(breadth)`
  and the Clarke–de Silva–Thorley transfer coefficient. Note the overlap in authorship and the
  division of labour: the fundamental law says what sets the *active risk* a book can take, and this
  note says that the units that risk is measured in move over time. Same family, different clause.
- `2026-10-11-tracking-error-frontiers-and-the-active-return-ceiling.md` and
  `2026-10-14-which-alpha-the-sufficient-statistic-for-beating-a-benchmark.md` — the folder's other
  two notes about the benchmark-relative objective v3 adopted; this one is about the *scale* of the
  statistic those two are about.
- `2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the other result in the folder about the
  error bar rather than the estimate.
- `experiments/learnings.md`, the deflated-Sharpe and effective-trial-count material: a
  variance-stabilised skill estimate changes the numerator of every `t`-like quantity the lab
  computes by hand, and must not be mixed with an unadjusted one in the same comparison.
