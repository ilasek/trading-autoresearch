---
title: "Non-standard errors in asset pricing: Mind your sorts" (with Walter–Weber–Weiss, "Methodological Uncertainty in Portfolio Sorts", circulated as "Non-Standard Errors in Portfolio Sorts", as the corroborating source)
authors: Soebhag, van Vliet, Verwijmeren; corroborating source Walter, Weber, Weiss
year: 2024 (primary, published version); corroborating source circulated 2022, revised 2024
venue: Journal of Empirical Finance 78, 101517 — peer-reviewed field journal (Tier 1–2). Corroborating source: SSRN working paper, WU Vienna (Tier 2), with public replication code.
url: https://doi.org/10.1016/j.jempfin.2024.101517 — corroborating https://doi.org/10.2139/ssrn.4164117 — code https://github.com/patrick-weiss/PortfolioSorts_NSE — text read in full: http://wp.lancs.ac.uk/fofi2022/files/2022/09/FoFI-2022-124-Amar-Soebhag.pdf
citations: 12 (Semantic Scholar, DOI:10.1016/j.jempfin.2024.101517, checked 2026-09-09); corroborating source 5 (Semantic Scholar, DOI:10.2139/ssrn.4164117, checked 2026-09-09)
sample_period: 1972–2021 (US stock returns, in the version read in full)
markets: US equities (CRSP/Compustat); the standard factor zoo, plus a survey of construction choices across 323 published empirical asset-pricing studies
tier: B
validation_overlap: true
published_post_2018: true
---

The primary is read **in full** as the August 2022 working-paper version (the FoFI 2022
conference copy, hosted by Lancaster; ScienceDirect returns a bot challenge to an automated
client and SSRN 403s). The **published** version's abstract was read separately via OpenAlex and
is cited where it differs: the working paper enumerates **eleven** binary construction choices
(2¹¹ = 2,048 versions of each factor) while the published abstract names **rebalancing frequency**
among the consequential choices, which the working paper does not vary. Where the two disagree,
the published abstract is authoritative and is flagged inline.

The corroborating source is **not read in full** — SSRN refuses an automated client. Its
abstract (from the WU Vienna research portal) and its public code repository are read; its
decision-node table is reproduced below from the authors' own published blog description of the
paper. Nothing below rests on the corroborating source alone except where it says so.

Tier **B** rather than A: peer-reviewed, directly on-point and independently corroborated by a
second team with public code, but single-market (US), and the text read in full is the
working-paper version.

**What is deliberately not carried across.** Both papers report Sharpe-ratio levels and ranges
for named factors over dated samples. Those are exactly the figures this folder is forbidden to
record and none of them appear here — not a median, not a range, not a before/after. What is
recorded is the **ratio of the non-standard error to the standard error**, which is a property
of the design space rather than a market realisation, on the same footing as the cost-consumed
*fraction* the 2026-09-07 entry admitted and the model-implied magnitudes the 2026-09-08 entry
admitted. Also recorded is the *proportional* reduction a fixed convention buys, which is a
property of the same design space.

## Mechanism

Menkveld et al. (`2026-09-09-nonstandard-errors-evidence-generating-process.md`) measure
non-standard error by hiring 164 teams. These papers get at the same quantity far more cheaply:
**enumerate the choices mechanically and compute every version yourself.** A characteristic-sorted
portfolio is not one object; it is a function of a sorting variable *and* of a dozen construction
decisions, each of which has two or three defensible settings that appear in published work. The
NSE is then the standard deviation of the resulting statistic across that enumerated set.

Two things make this the more useful of the two measurements for a lab like this one. First, the
choice set is *observable* — the primary's authors classify the choices actually made in a
representative set of 323 published empirical asset-pricing studies, so the enumeration is not a
strawman. Second, no binary option is close to universal: some are chosen roughly 50/50 across
the literature, which is what makes the resulting dispersion real rather than an artifact of
including choices nobody makes.

The economic content is that a construction choice is not cosmetic — it changes *what is in the
book*. The clearest instance the primary identifies: equal-weighting produces a portfolio with
materially higher illiquidity than value-weighting, and the higher gross risk-adjusted return
that follows is a compensation for that illiquidity rather than a stronger reading of the
sorting characteristic. The choice moves the exposure, and the exposure moves the number.

## Construction recipe

**The primary's eleven binary choices** (working-paper version; 2,048 combinations per factor):

1. 70/30 versus 80/20 characteristic breakpoints
2. NYSE versus NYSE-AMEX-Nasdaq ("NAN") breakpoint universe
3. include versus exclude negative-book-equity firms
4. include versus exclude microcaps
5. price filter versus none
6. include versus exclude utilities
7. include versus exclude financials
8. industry-neutralize the characteristic versus not
9. value-weighting versus equal-weighting
10. independent versus dependent double sorts
11. sort on the most recent market capitalization versus the June value

**The corroborating source's fourteen decision nodes** (69,120 combinations for a single sorting
variable), reproduced from the authors' own blog description of the paper — a wider net, and the
one whose axes map best onto this repo:

| Node | Options |
|---|---|
| Size restriction | none / NYSE 5% / NYSE 20% |
| Financials | include / exclude |
| Utilities | include / exclude |
| Positive book equity | include / exclude |
| Positive earnings | include / exclude |
| Stock-age restriction | none / > 2 years |
| Price restriction | none / > USD 1 / > USD 5 |
| Sorting-variable lag | 3 months / 6 months / Fama-French convention |
| Rebalancing | monthly / annually |
| Breakpoint quantiles, main sort | 5 / 10 |
| Sort structure | single / double dependent / double independent |
| Breakpoint quantiles, secondary sort | 2 / 5 |
| Breakpoint exchanges | NYSE / all |
| Weighting scheme | equal / value |

**The measurement.** For each combination, build the factor and compute the statistic of
interest — the primary uses the (maximum) Sharpe ratio, so that both individual factors and
whole factor models can be compared on one metric. The NSE is the standard deviation of that
statistic across combinations. The primary computes it two ways:

- **uniform** — every combination equally likely, which measures the *room a motivated researcher
  has* to optimise along a criterion; and
- **popularity-weighted** — each binary option weighted by how often it is chosen in the 323
  surveyed studies, which measures the dispersion a *reader* should expect from an unseen paper.

**The reporting recommendation.** Rather than defending one path, report the distribution of
results across the combinations — a "specification check". See
`2026-09-09-specification-curve-analysis.md` for the formal version of that display.

## Robustness evidence (qualitative only)

- **The average ratio of non-standard error to standard error across factors exceeds one** —
  1.18 under uniform choice probabilities and 1.08 under popularity weighting, in the version
  read in full; the published abstract restates the same conclusion ("the average ratio of the
  non-standard error to the standard error across factors exceeds one"). Weighting by what
  researchers actually do shrinks the dispersion only slightly, because the literature's choices
  are genuinely split rather than concentrated on one convention.
- **For several individual factors the NSE exceeds the SE outright**, so the dispersion is not
  carried by one pathological factor.
- **The independent corroboration agrees on the direction and adds the reassuring half.**
  Walter–Weber–Weiss, on a different and wider node set with public code, report that NSEs in
  portfolio sorts are *on average larger than standard errors*, that supposedly innocuous
  decisions cause large variation in estimated premiums, standard errors, NSEs and `t`-statistics
  alike, and that the impact of a given node varies widely across sorting variables — while
  premiums and alphas remain **pervasively positive for almost all sorting variables**. Their own
  summary of that: the *size* of a premium is uncertain, its *sign* is remarkably stable. (From
  the abstract and the authors' blog description; the paper was not read in full.)
- **Which nodes carry the dispersion.** The primary names the **breakpoint universe**
  (NYSE versus all exchanges), **microcap inclusion**, **industry adjustment** and **equal versus
  value weighting**; the published abstract adds **rebalancing frequency**. The
  corroborating source's finding that node importance varies by sorting variable is the caveat
  on that list: it is a place to look first, not a universal ranking.
- **A convention removes most of it.** Fixing three conservative choices — NYSE breakpoints,
  excluding microcaps, value-weighting — reduces the average non-standard error by about **70%**.
  This is the paper's most actionable result and it is a proportional statement, not a
  performance one.
- **The dispersion propagates upward into model selection.** Which factor model wins a maximum-
  squared-Sharpe comparison, the optimal mean-variance weights inside a model, and the economic
  gain to a mean-variance investor all move with the construction choices. A horse race between
  two constructions is partly a race between two construction conventions.
- **Known gaps.** Single market (US). Costs are examined in additional tests rather than imposed
  throughout. Multiple testing is acknowledged explicitly — the paper's own framing is that
  construction ambiguity is what *enables* p-hacking — and it cites the haircut literature rather
  than adding to it.

## Implementability here

**Direct, and the mapping is close.** This repo sorts a ~145-instrument universe on a score and
builds a long-only book from the ranks. Almost every node above has a live analogue that
candidates in this repo have silently varied from trial to trial:

| Their node | This repo's analogue |
|---|---|
| Breakpoint universe (NYSE vs all) | which pool ranks are computed over — full universe, scoreable pool, or region-relative |
| Microcap / price / age filters | the minimum-history requirement, the NaN-volume holiday handling, any dollar-volume floor |
| Industry neutralization | region demeaning, and the member-median controls the lead-lag work used |
| Equal vs value weighting | equal-weight versus magnitude-weighted books, and the 25% cap that truncates the latter |
| Breakpoint quantiles (5 / 10) | `CORE_N` / `BAND_N` — how many names are held and how many are banded |
| Sorting-variable lag (3 / 6 months) | the skip period and the signal lookback |
| Rebalancing (monthly / annually) | rebalance cadence and the tranche count `K` |
| Single vs double sort | single-score books versus the lab's two-score constructions |

**What this says about the lab's own history, and it is not a criticism.** The lab has already
found two of the primary's four consequential nodes to be consequential *here*, independently and
empirically: region-demeaning is one of the two recorded exceptions to its cross-sectional screen
rule, and the 2026-09-08 session's fifth finding was that an equal-weight rank-slice screen
mis-prices a magnitude-weighted book by roughly 2.5× — a weighting-scheme mismatch, exactly node
9. Two independent literatures and one lab converging on *weighting* and *the pool the ranks are
taken over* as the nodes that move the answer is about as strong as this kind of evidence gets.
The 2026-09-06 conclusion that "a concentration calibration is a property of a construction, not
of a family or a score" is the same statement in the lab's own vocabulary.

**The one action that costs nothing and needs no trial.** Write down the house construction. The
primary's 70%-reduction result is that a *fixed, conservative, uniformly-applied* convention
removes most of the dispersion — not that any particular convention is right. The conservative
settings here are already implicit in `strategies/lib/` reuse; making them explicit (which pool,
which weighting, which filter, which cadence, and that a candidate varying one of them is varying
a construction rather than testing a signal) converts an unwritten habit into something a session
can be held to. An unwritten convention is precisely the thing an autonomous agent varies without
noticing.

**The reassuring half, and how far it goes.** Walter–Weber–Weiss's "sign stable, magnitude
uncertain" maps onto a distinction this lab already draws between its **free IC screens**, which
read a sign, and its **validation Sharpe**, which reads a magnitude. Taken seriously it says the
IC screens are measuring the durable object and the Sharpe levels are measuring a
construction-dependent one — which is an argument for weighting the free directional screens more
heavily in *deciding what to build*, and none at all for changing the promotion rule, which is
frozen and belongs to the human.

**Known pitfalls.**

- **The universe is the difference that matters most.** Their consequential nodes are dominated by
  microcap and exchange filters on a several-thousand-name US cross-section. This universe is
  ~145 large global instruments with 42 ETFs and no microcaps at all, so nodes 2, 4 and 5 partly
  collapse here — while nodes 8, 9, 10 and the breakpoint-count node have *more* room, because a
  ~96-name scoreable pool makes `CORE_N` a far coarser lever than a quintile breakpoint on 3,000
  names. Do not import their node ranking; re-measure it, exactly as `CLAUDE.md` requires for
  constants carried between families.
- **Survivorship cuts the other way here.** Their samples are survivorship-free CRSP panels; this
  universe is current constituents. A construction node that concentrates the book on the names
  with the longest histories is also concentrating it on the survivorship artifact this lab has
  already identified. That is an argument for including the min-history filter as an explicit
  node in any dispersion measurement, not for treating it as fixed.
- **Do not run the enumeration through `run_experiment.py`.** Thousands of construction variants
  are a *measurement*, free and train-only, in the session scratchpad. Passing them through the
  protocol would put thousands of trials in `trials.jsonl` and raise the deflated-Sharpe bar
  permanently for every future candidate. This is the single way this note could do damage.

## Related

- `2026-09-09-nonstandard-errors-evidence-generating-process.md` — the source of the NSE concept,
  and the free train-only diagnostic that follows from it.
- `2026-09-09-specification-curve-analysis.md` — the formal version of the "specification check"
  this paper recommends, and the part of it this folder does not import.
- `2026-08-17-rebalance-timing-luck-tranching.md` — the rebalance-cadence node, measured on its
  own before the NSE framing existed, and the one the lab already acts on.
- `2026-09-06-number-of-portfolios-as-tuning-parameter.md` — the breakpoint-count node, treated
  there as an estimation problem with an optimal answer; treated here as a source of dispersion.
  The two readings are complements: one asks what `J` should be, the other asks how much the
  answer moves when it is not that.
- `2026-09-06-long-side-share-of-anomaly-profits.md`, `2026-09-02-anomalies-by-size-group.md` —
  the size/microcap thread this folder has embargoed. Nothing here re-opens it; the microcap node
  is named only to say it does not bind on this universe.
