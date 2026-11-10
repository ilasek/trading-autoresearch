---
title: "Detecting Long-Run Abnormal Stock Returns: The Empirical Power and Specification of Test Statistics"
authors: Barber, Lyon
year: 1997
venue: Journal of Financial Economics 43(3), 341–372 — venue tier 1
url: https://doi.org/10.1016/S0304-405X(96)00890-2
citations: 2102 (Crossref, checked 2026-11-10)
sample_period: July 1963 – December 1994 (1,798,509 firm-month returns)
markets: US — NYSE/AMEX/NASDAQ ordinary common shares (CRSP share codes 10, 11)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

The companion to `2026-11-10-performance-matched-controls-and-mean-reversion.md`, on **returns**
rather than accounting measures, and it settles a question the folder has been circling: **is a
matched *firm* or a matched *portfolio* the right control?** Their answer is the matched firm, and
the reason is not precision — it is that three separate biases enter through the *portfolio* side of
the subtraction and all three vanish when the benchmark is a single security held the same way the
sample security is held.

The object is a long-horizon abnormal return: a sample firm's return over one to five years, minus a
benchmark's over the same window. Two ways to accumulate it — summing monthly abnormal returns
(cumulative abnormal return, CAR) or compounding each side and differencing (buy-and-hold abnormal
return, BHAR) — and the authors favour BHAR on conceptual grounds, because it is what an investor
would actually earn.

**The four biases, and which construction each attaches to:**

- **New listing bias.** Sampled firms have a long post-event return history by construction; the
  index or reference portfolio they are measured against keeps *adding firms that began trading
  after the event month*. Since newly listed firms underperform market averages, the benchmark is
  dragged down and the abnormal return is biased **positive**. Attaches to both CAR and BHAR.
- **Rebalancing bias.** A reference portfolio's compound return is calculated assuming periodic
  (typically monthly) rebalancing, while the sample firm's return is compounded *without*
  rebalancing. Maintaining equal weights means selling what beat the average and buying what lagged
  it. The authors show directly, by sorting all securities into ten portfolios on month `t−1` return
  and reading month `t`, that **high-return names in `t−1` have low returns in `t` and vice versa**
  — so the implicit rebalancing systematically buys what subsequently does well. The index's
  compounded return is therefore **inflated** relative to a buy-and-hold security, and the BHAR is
  biased **negative**. Attaches to BHAR only. (They cite work finding the bias is *more* pronounced
  with daily than monthly returns.)
- **Skewness bias.** Long-run abnormal returns are strongly positively skewed — an individual name
  with an annual return above 100% is common, an index with one is not. A `t`-test on a positively
  skewed sample over-rejects in one tail and under-rejects in the other. The authors isolate this
  cleanly by running the same test on a **χ² distribution of known mean and comparable skewness**
  (skewness 2.83): the test rejects far too often in the low tail and essentially never in the high
  one. Worse for BHAR than for CAR.
- **Measurement bias.** The one that is *not* repaired by a matched firm when CARs are used; the
  authors evaluate its extent separately.

**Why the signs matter more than the sizes.** CARs come out positively biased and BHARs negatively
biased, from the *same* data — an apparent contradiction that is just the three biases loading
differently on the two accumulations. The lesson is that an abnormal-return number is a joint
statement about the accumulation rule and the benchmark's construction, and neither is neutral.

**The repair.** Match each sample firm to a **single control firm** and difference. This kills the
new listing bias (both must be listed in the event month), the rebalancing bias (neither side is
rebalanced), and the skewness bias (both sides are single securities, equally likely to throw a
large positive return). What is left is well specified in virtually every sampling situation they
construct.

## Construction recipe

**The control-firm caliper, exactly as stated:**

- Identify all firms with market value of equity between **70% and 130%** of the sample firm's.
- From that set, choose the firm whose **book-to-market ratio is closest** to the sample firm's.
- Hold that **same control firm for the whole horizon** of the analysis.

The order is load-bearing and the authors tested it: filtering on book-to-market *first* and then
matching on size "works well in most sampling situations", but **filtering on size and then matching
on book-to-market is the one that is well specified in virtually all of them**. Same two variables,
same data, different specification — the sequence of a two-stage match is a design choice with
consequences, not a presentational one.

**Shape of the rule, to carry rather than the constants:** a **hard window** on the first variable,
**nearest-neighbour** on the second, **no fallback needed** because the window is wide (±30%).
Compare the companion paper's scheme, where the second variable gets a hard window too *and* a
nearest-neighbour fallback — the difference is that there the second variable was the selection
variable.

**The reference portfolios they compare it against** (useful as a map of what a "benchmark" can be):
ten size deciles reconstituted annually in June, ten book-to-market deciles reconstituted in July
off NYSE breakpoints with AMEX/NASDAQ names slotted in, fifty size×book-to-market portfolios formed
by sorting into size deciles then book-to-market quintiles *within* each decile, and an
equally-weighted market index. They also run the Fama–French three-factor intercept as a fourth
approach.

**Two further construction rules they argue for:**

- **Simple returns, never continuously compounded.** Log abnormal returns are *inherently
  negatively biased* whenever there is cross-sectional dispersion in returns, by Jensen's inequality
  on the index side: the mean log abnormal return across securities sums to zero only if every
  constituent has the identical simple return, and is otherwise negative. They give a two-security
  worked example. This is an arithmetic result with no empirical content and it is **always true**.
- **Equal weighting of sample observations.** An event study by design gives equal weight to each
  observation, so comparing to a value-weighted market index is internally inconsistent whatever its
  investment appeal.
- **Missing control data.** When a control firm's post-event return data ends, they fill with the
  corresponding reference portfolio's return rather than dropping the pair.

## Robustness evidence (qualitative only)

- The specification results are built from 1,000 random samples per design across the full
  three-decade panel, and are reported by size decile, by book-to-market decile, and by sampling
  scheme — so "well specified in virtually all sampling situations" is a statement about a grid,
  not an average.
- The companion literature agrees on the diagnosis and differs on the remedy: Kothari–Warner (same
  journal, same year, 706 Crossref citations as of 2026-11-10) reach the same conclusion about
  long-horizon tests being misspecified, working through asset-pricing-model benchmarks where Barber
  and Lyon work through reference portfolios. Barber and Lyon's distinctive claim is that the
  **control-firm** route is robust where both of the others are not.
- The rebalancing-bias mechanism is independently corroborated inside the paper by the month `t−1`
  / month `t` sort, which is a short-horizon reversal result stated as a property of the *benchmark*
  rather than as a tradeable signal.

## Implementability here

**The sharpest consequence is about this lab's own benchmark, and it is free to check.**

Protocol v3 grades every candidate on **skill = the book's Sharpe minus the equal-weight eligible
pool's on the same days**. The equal-weight pool is, in this paper's vocabulary, a *reference
portfolio with periodic rebalancing*, and a candidate that rebalances rarely is, in this paper's
vocabulary, a *buy-and-hold security*. Both of the benchmark-side biases therefore have a defined
sign in the lab's own measurement:

- **The rebalancing channel inflates the pool.** The pool's weights are restored on some cadence;
  the trades that restore them buy recent relative losers and sell recent relative winners. Where
  relative prices mean-revert at that cadence, those trades are profitable and the pool's compounded
  return exceeds what the same names bought and held would have produced. A low-turnover candidate
  measured against it is therefore handed a **benchmark with a reversal bonus baked in**, and its
  skill is biased **down** by an amount that grows with the horizon and with the strength of
  short-horizon reversal in the panel. This is not a new claim for the folder — it is exactly the
  conditional that `2026-08-22-rebalancing-return-attribution-critique.md` proved (rebalancing
  trades have zero expected value under IID and pay only where relative prices revert) — but this
  paper supplies the **antecedent measured on a wide cross-section** and, more usefully, names it as
  a *bias in a measured abnormal return with a sign* rather than as an attribution question.
- **The new-listing channel works the other way and this panel has it structurally.** Under
  protocol v2 a column appears in `prices` only once the name has been eligible, so the equal-weight
  eligible pool is continually admitting names *at the moment they enter an index*. A candidate's
  book, once formed, is not. Whatever an entering cohort's return profile is relative to incumbents,
  the pool inherits it and the candidate does not — and `#401`/`#411` establish that admission is
  not an information-free selection. This is the new listing bias, in a panel built to have it.

**What to do about it, at zero trial cost:** report, next to skill, the pool's **buy-and-hold**
counterpart over the same window — the same eligible names, weighted equally at the start of the
measurement window and left to drift. The gap between the rebalanced pool and its own buy-and-hold
version is the rebalancing channel, measured rather than argued, and it is the quantity by which a
low-turnover candidate's skill is understated. Pair it with `#425`'s realised-beta diagnostic: both
are free, both are properties of the benchmark rather than the book, and both have the sign of the
lab's standing train-versus-validation puzzle.

**For a matched-control scout**, the transferable design rules are: hard window on the first
variable then nearest-neighbour on the second; **test the order of the two stages** rather than
assuming it; hold the match fixed for the horizon; difference compounded simple returns, never log
returns; and expect the matched-firm design to be better specified than *any* portfolio benchmark,
including a well-built one.

**Pitfalls, named.**

- The 70%–130% size window is calibrated to a US cross-section of ~1,800,000 firm-months. This
  panel is ~1,400 names with roughly a thousand eligible on a typical date, concentrated in nine
  large-cap national indices. A ±30% market-cap window on *this* panel may return a handful of names
  or, inside one index's mid-section, hundreds. **Measure the window's yield before fixing it**, and
  do not import the constant.
- Market value of equity is not available here. A size-like proxy must be built from price and
  volume, and `#408` establishes the obvious one is unavailable while `#416` establishes that no
  size threshold recovers index membership in the first place. A liquidity (dollar-volume) window is
  the honest substitute and should be described as such rather than as a size match.
- Book-to-market is unavailable here, full stop. The second matching dimension has to be something
  the panel holds — trailing volatility, dollar-volume rank, or region.
- The skewness result is a warning about the *statistic*, and it applies to this lab directly: any
  paired difference accumulated over a long horizon on single names is positively skewed, so a
  rank-based or bootstrap statistic is the right default. The lab's existing block-bootstrap
  machinery is the right shape already; a plain `t` on compounded differences is not.

## Related

- `notes/2026-11-10-performance-matched-controls-and-mean-reversion.md` — the same authors on
  accounting measures; the source of the "match on the selection variable" rule and the second
  caliper shape.
- `notes/2026-08-22-rebalancing-return-attribution-critique.md` — proves the rebalancing channel is
  a *conditional* bet on relative mean reversion; this note is its antecedent, measured.
- `notes/2026-10-13-equal-weighting-and-the-rebalancing-component.md` and
  `notes/2026-10-13-equal-minus-value-as-a-performance-evaluation-factor.md` — the
  benchmark's-own-return cluster: the pool as a size/value tilt plus a constant-weight rebalancing
  channel. The new-listing half is new here.
- `notes/2026-11-06-index-membership-is-not-an-information-free-selection.md` — why this panel's
  new-listing bias is not mean-zero.
- `notes/2026-11-10-characteristic-matched-benchmark-portfolios.md` — the matched-portfolio
  construction this paper argues against for test specification, which nonetheless has the
  decomposition the lab wants.
