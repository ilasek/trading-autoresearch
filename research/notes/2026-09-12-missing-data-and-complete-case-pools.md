---
title: "Missing Financial Data" — read for what a complete-case pool selects on, and for why "drop the names that are not scoreable" is a construction choice rather than a data-cleaning step
authors: Bryzgalova, Lerner, Lettau, Pelger
year: 2025
venue: Review of Financial Studies (Tier 1)
url: https://doi.org/10.1093/rfs/hhae036
citations: 41 (Semantic Scholar via the SSRN registration 10.2139/ssrn.4106794, checked 2026-09-12 — the RFS DOI is NOT found in Semantic Scholar); 42 (Crossref on the RFS DOI, checked 2026-09-12). OpenAlex not consulted: daily budget exhausted (`Insufficient budget`, checked 2026-09-12)
sample_period: 1967-01 – 2020-12
markets: US (CRSP/Compustat; 45 firm characteristics)
tier: A
validation_overlap: true
published_post_2018: true
read_status: accepted version read directly (London Business School institutional repository); the published RFS version was not read
---

## Mechanism

The paper is about missing *fundamentals*, which this repo does not have. It is in this folder for
the operator underneath it, which this repo uses on every single trial: **the pool rule.** The
house construction says "every instrument scoreable on the date; where several legs are combined,
the `common` intersection of their eligibilities." That is textbook **complete-case analysis**,
and this paper is the asset-pricing measurement of what complete-case analysis costs.

**Missingness is not random, and it is not random in a particular direction.** The paper's
documented structure: missing observations cluster both cross-sectionally and over time
(blocks, not scattered points); part of the pattern is mechanical (a young name has no prior
history, so any signal with a lookback is missing for it by construction); and — the fact that
matters most — **more extreme realizations of a characteristic are more likely to be
unobserved.** Formally, the missing-completely-at-random assumption under which dropping
incomplete rows is harmless is rejected.

**Complete-case selection is selection on the outcome, not just on the sample.** Their Fact #4:
returns themselves depend on whether a characteristic is observed — names with a missing value
have lower average returns than the same names when the value is observed. So dropping
unscoreable names is not "using less data"; it is conditioning the return distribution. Any
statistic computed on the retained subsample is a statistic about a self-selected population.

**The cost compounds with the number of legs, and it compounds twice.** Missingness in any one
characteristic badly understates the problem once several are required jointly: in their panel,
requiring a full set of the 45 characteristics discards most firms and about half of total market
capitalization at any point in time. And the effect on a sorted book runs through two channels at
once, which the paper states explicitly: **requiring more characteristic observations often lowers
expected returns, while the smaller pool lowers diversification and therefore raises volatility —
so the ratio falls from both ends.** That is a direct, testable prediction about what an
intersection pool does to a multi-leg book, and it is the single most transferable sentence in
the paper.

**Why the obvious repairs fail.** Any imputation has to solve two problems at once: it needs a
model good enough for the characteristic (characteristics depend on each other in the
cross-section and on themselves over time, so omitting either is an omitted-variable bias), and it
has to be estimated on observed data while remaining valid on the *missing* data (so ignoring the
systematic missingness pattern is a selection bias in the imputation itself). The two folk
methods each fail on both counts: a **cross-sectional median** (market-wide or industry-wide)
incurs both biases, and **carrying the last observed value forward** degrades badly exactly where
missingness comes in consecutive blocks — which is the shape the paper documents.

## Construction recipe

Their method, at the level of detail needed to adapt it:

1. **A latent factor model across the characteristic cross-section on each date**, estimated
   robustly so it tolerates the systematic missingness. This captures "what other observed
   characteristics of this name imply about the missing one". Estimation is a PCA plus ridge
   regression — deliberately simple. Fitting the loadings on the whole panel gives a *global*
   variant, which is more precise when loadings are stable.
2. **A time-series component layered on top**, because the part of a characteristic that is only
   weakly correlated with other characteristics can only come from its own past. They model
   persistence directly (an AR structure in both the systematic and non-systematic components).
3. **Two variants, and the distinction is the whole ballgame for a backtest.** `B-XS` uses
   **only past** observed information; `BF-XS` combines past **and future**. The forward-looking
   variant is more accurate and is **categorically unusable in a causal backtest** — only the
   backward variant is admissible here.
4. **Judge an imputation out-of-sample by masking**, not by fit: hide observed entries under
   several assumed missingness mechanisms (completely-at-random; block-structured; and a
   *logit* scheme where the probability of being missing depends on the value itself) and measure
   recovery error on the masked entries. The block and value-dependent schemes are the realistic
   ones and are where the folk methods lose.
5. **Report the downstream consequence, not the imputation error.** Their own downstream checks are
   the ones to copy: the estimated cross-sectional risk premium of a characteristic, and the
   time series of the factor-mimicking pure-play portfolio for it. A biased imputation
   (the median) distorts both; the imputation error is not itself the quantity of interest.

## Robustness evidence (qualitative only)

- The missingness documentation is a census of one large panel across more than five decades,
  reported by characteristic, by calendar time, by market-cap quintile, and by position in a
  firm's life (missing at the beginning / middle / end). It is descriptive rather than
  inferential, which is the right standard for a fact of this kind.
- **The finding is explicitly not a small-cap artifact**: at no point in their sample is
  missingness confined to small companies, and coverage for small and large names converges in
  the later part of the sample. This matters here because the obvious dismissal — "our universe is
  140 large instruments, so this is someone else's problem" — is the dismissal the paper's own
  evidence blocks.
- The method comparison is a horse race against the two conventions in actual use (cross-sectional
  and industry medians; stale values), under multiple masking mechanisms, and the ordering is
  uniform rather than scheme-dependent.
- **Caveats stated plainly.** The object is US accounting data; the imputation machinery is
  designed for a panel of many characteristics per name, which is where its cross-sectional
  factor step gets its information. A panel with a handful of characteristics has much less for
  that step to work with, and the paper's method should not be assumed to transfer at full
  strength to one.
- `validation_overlap: true` — the sample runs to the end of 2020, so it touches this lab's
  validation window. Nothing timed is taken from it here; the claims recorded above are
  structural.

## Implementability here

**The paper's own method is not the deliverable — the diagnostics are.** This repo has no
fundamentals, its instrument count is ~140, and a 45-characteristic factor imputation has no
counterpart. But the repo has three live instances of the operator, and none of them has ever
been measured:

1. **The `common` intersection when legs are combined.** The paper's prediction is specific: the
   intersection lowers expected return *and* lowers breadth, so the ratio falls from both ends.
   The free screen is a direct test of the first channel, and it is two lines on train: for a
   given pair of legs, compare the forward returns of the names the intersection **excludes** with
   those of the names it keeps, pooled over rebalance dates. If they differ materially, the
   intersection is selecting on the outcome and every statistic computed after it is conditional.
   Both answers are findings; a null retires a standing worry cheaply.
2. **A score's own min-history requirement**, which is mechanical missingness in exactly the
   paper's sense — a long-lookback leg is undefined for any instrument whose history is short, and
   this repo's instruments start at very different dates. The 2026-09-04 finding that a band-width
   change silently changed the *train sample* is the same phenomenon caught from a different
   angle, as is the 2026-09-02 result that only 5 of 42 ETFs reach a 20-year lookback. **Pool size
   over time should be printed beside every score**, and any candidate whose pool differs from the
   incumbent's is varying a construction node, not testing a signal.
3. **NaN volume on foreign holidays**, which the strategy contract states outright: the `aux`
   frames are not forward-filled, so volume is missing on any date a name's home market is shut.
   This is the paper's worst case in miniature — the missingness is a **block, clustered by
   country, and perfectly correlated across all names sharing a calendar**. Two consequences
   follow directly. A cross-sectional median fill would impute a global median into an entire
   region's names on a single date, which is precisely the omitted-variable bias the paper
   measures; and a stale-value fill degrades exactly where blocks occur. The defensible handling
   for a daily-bar gap of this shape is to make the *signal* robust to it — aggregate over a
   window long enough that a holiday is a missing observation rather than a missing value, and
   average over the observations present — rather than to invent a value.

**A rule worth adopting regardless of any trial: imputation is a construction node.** If a
candidate fills anything, the fill rule belongs in its hypothesis line and in the house table
alongside pool, band and weighting, because two books differing only in their fill rule are two
constructions. This repo's current default is "drop", which is a choice with the properties
documented above, not the absence of one.

**Pitfalls.** (a) `BF-XS` and anything like it is a lookahead — the causality check will catch a
naive version, but a smoothed or centred fill is the same error in disguise. (b) Imputation error
is *systematic*, not idiosyncratic: it is correlated across names on a date, so it does not
diversify away inside a book and it can create apparent cross-sectional structure. (c) Ranking
after imputing means part of the ranking is made of fitted values —
`2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md`'s Property 4 applies, and the
imputed names' ranks move every other name's. (d) Do not import the paper's magnitudes: they are
properties of a several-thousand-name US accounting panel and there is no reason for them to hold
on 140 global price series.

**Anti-candidate.** Nothing here proposes a book, and an imputation module would be a
`strategies/lib` addition serving no measured need. The value is three free diagnostics and one
naming rule.

## Related

- `2026-09-12-residual-momentum-neutralizing-a-score-by-regression.md` — that paper's §5.5
  complete-history control is the right version of diagnostic 1, run by authors who anticipated
  the objection; this note says why it was not a formality.
- `2026-09-12-rank-transform-what-it-preserves-and-what-it-breaks.md` — Property 4: a rank is
  defined only relative to a pool, so a pool rule *is* a scoring decision.
- `2026-08-26-survivorship-conditioning-and-spurious-persistence.md`,
  `2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — selection on membership; this
  note is selection on *observability*, which is a separate channel that operates inside an
  already-fixed universe.
- `2026-09-09-nonstandard-errors-in-portfolio-sorts.md` — the pool rule is one of the construction
  nodes whose dispersion that literature measures.
- `2026-08-19-fundamental-law-breadth-and-strategy-risk.md` — the breadth half of the two-channel
  cost.
- `2026-09-08-nonsynchronous-trading-econometrics.md` — the other consequence of a shared trading
  calendar; that note is about stale *prices*, this one about absent *observations*.
