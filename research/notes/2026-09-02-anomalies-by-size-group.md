---
title: "Dissecting Anomalies — which return predictors survive among big stocks"
authors: Fama, French
year: 2008
venue: Journal of Finance (Tier 1)
url: https://doi.org/10.1111/j.1540-6261.2008.01371.x
citations: 1312 (Semantic Scholar by DOI, checked 2026-09-02)
sample_period: July 1963 – December 2005
markets: NYSE, Amex and (after 1972) Nasdaq common stocks
tier: A
validation_overlap: false
published_post_2018: false
---

Read **in full** from the authors' December 2006 working draft, hosted at
`ivey.uwo.ca/media/3775531/dissecting_anomalies.pdf`, of the paper published as JF 63(4),
1653–1678. The draft labels the smallest size group "tiny"; the published version calls it
"microcaps". Terminology aside, the size-group construction and the pervasiveness conclusions are
the same, and nothing recorded below depends on the difference.

This note answers the **single question `SUMMARY.md` named as the most consequential unknown about
this repo's instrument set**: where in the size distribution the universe sits, and what that
implies about which predictors can work on it. The folder has taken three readings on this
question that point in different directions (Gu–Kelly–Xiu: ML predictability *stronger* among large
stocks; Freyberger et al.: *fewer* characteristics survive among large firms; the liquidity
premium's location in the illiquid tail). This source measures predictability **by size group
directly**, which is what the open question asked for.

## Mechanism

This is not a paper about one effect; it is a paper about **how much of the anomaly literature is a
statement about stocks nobody can hold much of**, and the mechanism it identifies is a construction
artifact rather than an economic force.

The standard test forms equal-weight decile portfolios on an anomaly variable and reads the
long-short spread of the extremes. Two facts make that spread a statement about the smallest
stocks:

1. **Tiny stocks are about 3% of total market capitalisation but about 60% of the *number* of
   stocks.** In an equal-weight scheme, a portfolio is a count, not a value — so the spread is
   mostly theirs by construction.
2. **The cross-sectional dispersion of anomaly variables is largest among tiny stocks.** So they
   are over-represented *again* in the extreme deciles specifically — more than 60% of the names in
   the tails — beyond what their share of the count already implies.

Value-weighting is not the fix: VW hedge returns can be dominated by a handful of the largest
stocks, which is an unrepresentative picture in the other direction. The authors' answer is to stop
aggregating and **sort within size groups separately** — tiny, small and big, split at the 20th and
50th percentiles of NYSE market cap — and to read pervasiveness off whether the effect appears in
all three. They pair the sorts with cross-section regressions, noting each method's shortcomings
(sorts cannot control for multiple variables at once; regressions impose a functional form and
weight observations in ways that let extreme values matter), and report both.

**What survives among big stocks.** Net stock issues, accruals, and **momentum** are pervasive:
they show up strongly in all three size groups in the regressions, and in sorts at least in the
extremes. **Asset growth and profitability are less robust** — there is an asset-growth effect in
the average returns of tiny and small stocks but it is **absent among the big stocks that account
for more than 90% of market capitalisation**; and among profitable firms higher profitability is
associated with higher returns, but there is little evidence that unprofitable firms earn unusually
low returns (an asymmetry, not a clean monotone effect).

The general principle to carry: **"the anomaly exists" and "the anomaly exists where a large-cap
portfolio can trade it" are different claims**, and a large fraction of published cross-sectional
evidence establishes only the first.

## Construction recipe

Not a strategy recipe — a **testing** recipe, which is how it should be used here:

- **Split the universe by size before evaluating any cross-sectional predictor**, at fixed
  percentile breakpoints of market cap, and re-run the sort inside each group. Report all groups.
- **Never read pervasiveness off an equal-weight all-stock decile spread.** Report both EW and VW,
  and treat a large gap between them as evidence the effect lives in the small tail.
- **Run sorts and cross-section regressions together** and require the same conclusion from both.
  Sorts cannot hold other characteristics fixed; regressions impose linearity and let extreme
  observations pull the fit. Agreement across the two is the evidence; disagreement is a finding
  about the functional form.
- Form size groups annually at a fixed date and hold, so group membership is not itself a
  high-frequency signal.

## Robustness evidence (qualitative only)

Four decades of US data, the full NYSE-Amex-Nasdaq cross-section, five anomaly families examined
under two methodologies that the authors state "sometimes differ on nuances, but support the same
general conclusions". Single-market (US), which is the main gap: the size-group decomposition is
not run out-of-country here. The authors are among the most-cited in the field and the paper is
itself a methodological check on prior work rather than a new-effect claim, which is the honest
direction for a source to point. Its central methodological message — that microcaps drive much
of the anomaly literature — is corroborated by the later replication literature this folder
already holds (Hou–Xue–Zhang), which reaches the same conclusion from a much larger anomaly count.

## Implementability here

**This universe is entirely "big", with no tiny or small group at all** — ~145 global large-cap
names plus 42 ETFs, chosen as current constituents. On this paper's taxonomy, every trial this lab
has ever run is a **big-stock sort**, and the reference class for what should work is the big-stock
column, not the headline result of whatever paper motivated the candidate.

1. **The lab's entire empirical history is what this paper predicts, and that correspondence is
   the most useful thing in this note.** Of the predictors the authors certify as pervasive in big
   stocks — net stock issues, accruals, momentum — **the first two require fundamentals this repo
   does not have, leaving momentum as the only one computable from daily OHLCV.** And momentum
   (`price-trend`) is exactly where all 7 of the lab's promotions sit, while every family built on
   a cross-sectional characteristic *level* has closed on measurement: `liquidity-volume` twice,
   `range-variance` four times over nine screened mechanisms, with `learnings.md`'s own diagnosis
   for the latter being that "the level *is* the survivorship artifact". This paper supplies the
   prior that would have predicted all of it in advance.
2. **The practical rule this yields is a pre-trial screen, and it is free.** Before proposing a
   candidate from a source, ask: **did the source report the effect separately for big stocks, and
   did it survive there?** If the source only reports an all-stock equal-weight spread, the
   expected effect on this universe should be discounted hard — possibly to zero — regardless of
   the source's tier or citation count. This is a cheaper filter than a trial and it applies to
   every note in this folder retrospectively.
3. **It sharpens the standing three-source tension rather than settling it, and the sharpening is
   the useful part.** Gu–Kelly–Xiu find ML predictability stronger among large stocks;
   Freyberger et al. find fewer characteristics surviving among large firms; this paper finds
   *some* characteristics fully pervasive and others exclusively small-cap. These are consistent
   once separated: **the number of characteristics that work among big stocks is small, and
   forecast accuracy from the few that do work can still be high there.** For a 145-name large-cap
   universe that reads as: expect few live signals, not weak ones — which is precisely what the
   `research/README.md` guidance for `statistical-learning` already says ("prefer few features and
   a penalised linear model first"), now with a direct measurement behind it rather than an
   argument from universe size.
4. **A caution about the lab's own construction.** This repo's books are long-only top-N of ~140,
   which is closer to equal-weight than value-weight. The paper's warning about EW spreads is
   about *tiny* stocks being over-represented in the tails, and there are none here — so the
   specific artifact does not apply. But the underlying mechanism does: **the extreme deciles of a
   sort over-sample whichever names have the largest dispersion in the sort variable**, and on this
   universe that is a live concern for any level-based characteristic, which is the same failure
   `range-variance` closed on.
5. **What it does not license.** It says nothing about ETFs, about non-US markets separately, or
   about the families this lab has open beyond the characteristic sorts (`lead-lag-spillover`,
   `seasonality-calendar`, `portfolio-learning` are all outside its scope). Do not extend the
   big-stock column to them by analogy — that is exactly the move `CLAUDE.md` forbids for
   `learnings.md`'s constants.

**No new candidate follows from this note, and that is deliberate.** It is a prior-setting source,
not a mechanism source. Its value is that it makes the next negative result in a characteristic
family cheap to interpret and, better, cheap to *skip*.

## Related

- `notes/2026-09-01-nonparametric-characteristic-selection-large-stocks.md` (Freyberger et al.) and
  `notes/2026-08-29-machine-learning-cross-section-comparative.md` (Gu–Kelly–Xiu) — the other two
  readings on the size question; point 3 reconciles all three.
- `notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md` and
  `notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md` — the universe's other
  standing bias; the two compound, since current-constituent selection is itself a size-and-survival
  filter.
- `notes/2026-08-29-amihud-illiquidity-measure-and-replication.md` — the liquidity premium's
  location in the illiquid tail, which this paper's taxonomy explains as a small-stock effect.
- `experiments/learnings.md` 2026-08-31 and 2026-09-01 — the `range-variance` and
  `liquidity-volume` closures that point 1 argues were predictable from this source.
