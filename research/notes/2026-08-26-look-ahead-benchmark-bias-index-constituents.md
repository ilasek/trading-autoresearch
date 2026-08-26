---
title: "Look-Ahead Benchmark Bias in Portfolio Performance Evaluation — with: Long-Term Impact of Russell 2000 Index Rebalancing"
authors: Daniel, Sornette & Wöhrmann; Cai & Houge
year: 2009; 2008
venue: Journal of Portfolio Management 36(1), 121–130 (tier 1 by this folder's rubric, practitioner-facing); Financial Analysts Journal 64(4), 76–91 (tier 1, peer-reviewed)
url: https://doi.org/10.3905/jpm.2009.36.1.121 (full text read from arXiv:0810.1922) ; https://doi.org/10.2469/faj.v64.n4.7 (full text read from the author-hosted accepted version, biz.uiowa.edu/faculty/thouge/index_paper.pdf)
citations: "Daniel–Sornette–Wöhrmann: 19 (Crossref is-referenced-by-count, checked 2026-08-26; OpenAlex reports 1, an evident undercount for a JPM article — the folder's standing 'disbelieve a lone low count' rule applies). Cai–Houge: 35 (OpenAlex, checked 2026-08-26; Crossref 29)"
sample_period: "Daniel et al.: CRSP US stocks 1926–2006 (26,892 names), split into eight ten-year windows, plus a six-year illustration. Cai–Houge: Russell 2000 additions and deletions 1979–2004"
markets: US equities — the running top-500 capitalisations (Daniel et al.); US small caps (Cai–Houge)
tier: B for both — the mechanisms are demonstrable by construction and the venues are strong, but each is a single-market study with modest citation counts and no independent replication found
validation_overlap: false
published_post_2018: false
---

## Mechanism

Session 12 named "the statistical properties of the universe itself — survivorship bias and
constituent selection" as the largest unquantified discount this repo applies to every stock-level
result. These two sources address the half that is specifically *this repo's* data construction, and
they are unusually on-point: the first paper's opening example **is** the repo's universe-building
procedure, described step by step and then shown to be a large bias.

**The look-ahead benchmark bias (Daniel–Sornette–Wöhrmann).** The authors set out the standard
backtest recipe verbatim — (1) obtain the list of index constituents *at the present time*, (2)
retrieve each name's price history over the past period, (3) backtest on that set — and observe that
step (1) leaks the future into the sample. This is distinct from ordinary survivorship bias, which
concerns names that ceased to exist; here even names that survived the whole period are selected on
their *end-of-period ranking*. A capitalisation-ranked index cannot, almost by construction, contain
a name that fell far behind its sector peers, so the end-of-period constituent list is a set of names
selected for having *not* fallen behind over the very window you are about to score.

Their measurement is a matched pair: for each of eight consecutive ten-year windows, form an equally
weighted $1 portfolio in the 500 largest capitalisations as measured at the **end** of the window
(the biased one) and another in the 500 largest as measured at the **start** (implementable in real
time), and hold both. The ex-post portfolio wins consistently across all eight windows spanning
1926–2006, and the authors' headline figure for the magnitude is **up to 8% per annum** of
overstated expected return. Two structural features of the distortion matter more than the level:
it **inflates the Sharpe ratio** (return up *and* risk down, because the selected names are the ones
that did not blow up) and it **understates peak-to-valley drawdown**. The result is reported as
robust to the number of names selected.

**Three secondary results, each of which is separately useful.**

- *The bias in the bias estimate.* The standard way to size survivorship or look-ahead bias — run the
  same performance statistic on a clean and a biased database and difference them — is itself biased,
  and in the direction that makes the problem look smaller than it is. The reason is that a
  survivorship-selected database has **smaller covariance terms**, which enters the sampling
  distribution of the Sharpe estimate. Their conclusion: "the bias is worse than one thinks it is
  when reading the literature", naming several of the standard references.
- *The distortion has a preferred victim.* For a set of assets with equal means and variances and
  zero covariances, naive equal weighting has a slightly better expected Sharpe than sample-based
  Markowitz optimisation. Estimate the inputs on survivorship-biased data instead — higher means,
  lower variances — and **the ordering flips**, so the optimiser now appears to win. The bias
  systematically favours estimated-optimisation schemes over naive diversification.
- *The proposed remedy is a null distribution, not a correction.* Because one can never be certain a
  look-ahead bias has been removed, they propose benchmarking a strategy against **constrained random
  portfolios run on the same biased data**: random long-only books matched to the strategy's leverage,
  average holding period and turnover. Since the same bias contaminates both, the strategy's value is
  the excess over the random-portfolio distribution, not over the index. In their illustration, such
  non-informative random strategies on a look-ahead-selected 500-name universe produced Sharpe ratios
  of roughly 2 and comfortably beat the index — which is the point: on a contaminated universe, a
  strategy with no information at all looks excellent against the obvious benchmark.

**Why index membership selects on past return (Cai–Houge).** The second source supplies the channel.
Index membership is defined by a *threshold* on a characteristic — for the indices in question,
market capitalisation — so additions and deletions are, mechanically, names that have recently
crossed that threshold, which means names with large recent returns of a determinate sign. The
authors measure the crossing directly on the Russell 2000, a **small-cap** index bounded above and
below, which lets both signs be observed in the same study:

- Firms deleted from the **top** of the index (grown too large) averaged roughly **+69%** over the
  prior year; firms deleted from the **bottom** (shrunk too small) averaged roughly **−36%**.
- Firms entering from the **bottom** (grown into it from below) averaged roughly **+53%** over the
  prior year; firms entering from the **top** (shrunk into it from above) averaged roughly **−28%**.

So threshold crossings are not a mild perturbation of the universe — they are events with prior-year
returns measured in tens of percent, i.e. exactly the horizon a 6–12 month momentum signal ranks on.
The authors further find that the effect does not stop at the crossing date: large firms deleted from
the top continue to exhibit **short-term price momentum** into the following year, while additions
that are new issues have poor long-run returns. Their headline is that a buy-and-hold portfolio of
the original constituents beats the annually reconstituted index, by an average of about 2.2% over
one year and 17.3% over five, and that this is attributable to post-crossing momentum plus new-issue
underperformance rather than to index-inclusion price pressure.

## Construction recipe

Neither is a strategy; both are diagnostics.

**Sizing the bias (Daniel et al.'s matched-pair design).** Requires point-in-time constituent lists,
which this repo does not have — so it is recorded as the *shape* of the right measurement, not as a
runnable one. For each historical window: build the same book twice, once on the universe as it was
at the window's start and once on the universe as of today, and difference every scored statistic
(return, Sharpe, max drawdown). The gap is the look-ahead benchmark bias for that window.

**The random-portfolio null (their remedy, and the buildable half).** Generate many random long-only
books on the *same* universe, matched to the strategy on the constraints that determine how much of
the bias a book can absorb — gross leverage, number of positions, average holding period, turnover —
and report the strategy's statistic as a quantile of that distribution rather than as a level. The
matching is the load-bearing part: an unmatched random benchmark measures the wrong thing.

## Robustness evidence (qualitative only)

The look-ahead result is established in eight consecutive non-overlapping decade windows of a single
market, with the direction consistent in all eight (weakest in one) and stated as robust to the
number of names. The mechanism is not statistical — it is a construction artifact, reproducible by
arithmetic on any dataset, which is why the folder rates its *logic* above its citation count. What
is *not* established is any cross-market evidence: both papers are US-only, and neither has an
independent replication that this session could find. Nothing here decays in the McLean–Pontiff
sense, because nothing here is a tradeable effect.

The two soft spots to hold against the headline magnitude. First, part of the gap in the
illustrative comparison is attributable to equal versus value weighting, which the authors address
by comparing equally-weighted ex-post against equally-weighted ex-ante rather than against the index
— the like-for-like comparison, and the one the 8% figure rests on. Second, the "up to" in "up to 8%
per annum" is doing real work: it is an upper end across windows, not a central estimate, and the
paper's own Table shows the ex-ante and ex-post means statistically indistinguishable in the earliest
decades. **Do not carry 8% as this repo's discount.** Carry the direction and the fact that the
magnitude is of the same order as an entire equity risk premium.

Cai–Houge is FAJ-published and moderately cited, and its within-study design is strong — the crossing
direction is observed on both sides of the same index in the same sample, which is what makes the
mechanism generalisable rather than a small-cap curiosity. But it is one index, one country, one
25-year sample, unreplicated.

## Implementability here

**(a) The construction the first paper attacks is, exactly, this repo's.** `program.md` records the
universe as "**current** constituents → survivorship bias inflates stock-picking results;
ETF-level strategies suffer least." That is the right instinct and it names the wrong bias. The
distortion measured here does not require any name to have died: it is present among names that
survived the entire window, because the selection is on *end-of-period rank*, not on existence. The
practical consequence is that the caveat's escape hatch is narrower than it reads. It is true that
ETF-level strategies suffer least — an ETF sleeve chosen for asset-class coverage is not selected on
its own trailing return — but the ~145-name stock leg is exposed to the full effect, and so is any
statistic computed on it, including the ones the gate reads.

**(b) The distortion's shape maps onto three specific things the lab has measured.** Return up,
volatility down, drawdown understated — all three in the flattering direction, and all three are gates
in `program.md`. That is worth stating precisely because the lab's drawdown gate is one of the hard
gates a candidate must clear: a universe selected on end-of-period rank makes the drawdown gate
easier to clear than it would be in real time, uniformly across candidates. This does not
differentially favour any one candidate over another — it is a level shift on the whole ladder — but
it means the gate is measuring something more permissive than its number suggests.

**(c) The one that changes how an existing folder principle should be read.** The bias
*systematically favours estimated-optimisation schemes over naive diversification*, by inflating
means and shrinking covariances — the two inputs an optimiser is most sensitive to. The folder's
screen #1 (DeMiguel–Garlappi–Uppal: a weighting scheme's out-of-sample cost scales with how many
noisily-estimated parameters it needs) is therefore, if anything, **understated on this repo's data**:
the data construction here tilts the comparison *toward* the expensive class, and estimated schemes
still lost twice in the lab's record. That strengthens rather than weakens the existing prior, and it
is a genuinely new reason for it.

**(d) The momentum-specific channel, with the extrapolation flagged as the lab's, not the source's.**
Cai–Houge establish that index membership is a threshold on a characteristic and that crossings are
large-past-return events. Their index is bounded on both sides, so both signs appear. This repo's
universe is drawn from **large-cap** indices, which are bounded from below only — meaning additions
are names that grew *up* through the threshold (past winners) and deletions are names that shrank
*down* through it (past losers). A universe of *today's* large-cap constituents therefore contains,
at every historical date, names that were on their way up through the bar, and excludes names that
were on their way down. **That is the direction that flatters a cross-sectional momentum book**, and
it is a second, independent route to the same conclusion as
`notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` reaches from BGIR's selection
taxonomy. *The one-sided-threshold extrapolation is this lab's inference.* Cai–Houge study a
two-sided small-cap index and never make it; do not cite them as having done so.

**(e) The random-portfolio null is the session's one buildable recommendation, and it is not free.**
It answers a question no statistic in this repo asks — *how much of the champion's measured edge is
available to a book with no information at all on this universe?* — and it is the correct control for
a contaminated universe precisely because the contamination is applied to both sides. Three honest
costs, all of which put it in the same category as session 11's PBO item rather than in the free-
diagnostic class: it **scores returns**, so it is outside the holdings-only exemption; it must be run
on the validation split to be comparable to the gate's number, re-using a split rather than supplying
an independent look; and `CLAUDE.md` requires every strategy run to go through `run_experiment.py`,
so whether a random-portfolio null distribution counts as trials is a **human decision**, not a
session's. Recorded as a proposal to a human, with the matching requirement (leverage, position
count, holding period, turnover) as its load-bearing detail.

**(f) What is not available here.** The matched-pair measurement that would actually size this repo's
bias needs point-in-time constituent lists. `program.md` lists survivorship-bias-free point-in-time
data under "Future upgrades (do not start without human approval)". So the honest status of the
discount is: its *mechanism* is now sourced and its *direction* is unambiguous, and its **magnitude
on this universe remains unmeasured and unmeasurable with the data the repo has**. That is a better
statement than the caveat had, and it is not a number.

## Related

- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` — the same bias from the
  inference side; that note's selection-rule taxonomy and this note's threshold-crossing channel are
  two routes to the same sign.
- `notes/2026-08-26-skewness-and-concentration-of-stock-returns.md` — why the excluded names matter
  so much: the excluded tail is where the median outcome lives.
- `notes/2026-08-17-naive-vs-optimized-weighting.md` — screen #1, which point (c) strengthens.
- `notes/2026-08-24-deflated-sharpe-ratio.md`, `notes/2026-08-17-mclean-pontiff-publication-decay.md`
  — the other two discounts between a backtest statistic and what is available forward. This is a
  third, and it is orthogonal to both.
- `program.md` → "Constraints and known caveats"; `experiments/learnings.md` → "Data & methodology
  caveats (permanent)".
