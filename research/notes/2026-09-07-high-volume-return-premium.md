---
title: "The High Volume Return Premium" (with the cross-country replication "The high volume return premium: Cross-country evidence")
authors: Gervais, Kaniel, Mingelgrin; Kaniel, Ozoguz, Starks
year: 2001; 2012
venue: Journal of Finance 56(3), 877–919 (venue tier 1); Journal of Financial Economics 103(2), 255–279 (venue tier 1)
url: https://doi.org/10.1111/0022-1082.00349 — read in full from the Rodney L. White Center working-paper PDF, https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9901.pdf ; replication https://doi.org/10.1016/j.jfineco.2011.08.012 (abstract and metadata only, see below)
citations: GKM 910 (Semantic Scholar DOI endpoint, checked 2026-09-07). KOS 94 (Semantic Scholar DOI endpoint) / 93 (Crossref `is-referenced-by-count`), same date
sample_period: GKM 15 August 1963 – 31 December 1996. KOS **not verified** — the full text is behind a publisher paywall; a 2012 JFE article cannot reach 2018, so its `validation_overlap` is false regardless
markets: GKM: US, NYSE common stocks (CRSP), with a TAQ subsample for spreads. KOS: 41 countries, developed and emerging
tier: A
validation_overlap: false
published_post_2018: false
---

**Read in full**: the GKM working paper carrying the published argument — data and interval
construction, the volume classification, the three portfolio strategies, the risk section
(systematic risk, stochastic dominance, bid-ask spreads), the robustness section (measurement of
volume, announcements, absolute returns, return autocorrelation), the economic-profitability
section and the conclusion. **KOS was not read**: closed access, and its finding is recorded here
from the publisher's own abstract (via RePEc) rather than from the paper.

This is the first note in the folder on a volume **shock**. Every previous `liquidity-volume`
note is about a volume or illiquidity **level** — `2026-08-29-amihud-illiquidity-measure-and-replication`,
`2026-08-31-amihud-volume-component-decomposition`, `2026-09-04-global-liquidity-proxy-horserace`.
It also arrives against two of this lab's own nulls, and **the tension is the reason to read it
carefully rather than a reason to skip it** — see *Related*.

## Mechanism

A stock that has just traded an unusual amount is a stock that more people have just looked at.
The paper's preferred story is Merton's (1987) investor-recognition equilibrium: a security held
by a smaller investor base carries a shadow cost for incomplete information, and anything that
widens the base lowers that cost — which shows up, once, as a price increase. A volume shock is a
proxy for such a widening. The premium is therefore not a risk premium and the authors do not
claim it is one; it is a one-off revaluation as a name moves into more portfolios' attention.

Three supporting mechanisms are named and none is discarded:

- **Diamond–Verrecchia (1987) asymmetry.** Short-sale constraints mean good news is expressed by
  trading and bad news is partly suppressed, so volume itself becomes an asymmetric signal about
  the sign of information — which is the only way a *symmetric* quantity (a shock in either
  direction of the volume distribution) can predict a *signed* return.
- **Blume–Easley–O'Hara (1994), Bernardo–Judd (1996).** When traders are uncertain about how
  aggressively informed others are, current volume carries information about the precision of the
  signal being traded on, and therefore about how prices will continue to move.
- The authors are explicit that no existing model reconciles all their facts, and say so in the
  conclusion. Take the mechanism as underdetermined.

The decisive empirical property, and the one that makes this worth a lab's time, is that the
premium is **stronger when the extreme-volume names whose formation-period *return* was also
extreme are removed**. Volume is not standing in for a return move. A parallel classification run
on *absolute* returns instead of volume does not reproduce the effect, and the result survives
controls for the contemporaneous volume/return correlation and for return autocorrelation.

## Construction recipe

GKM's daily construction, which is what matters here because it needs nothing but a daily close
and a daily volume:

1. **Split the sample into non-overlapping 50-trading-day intervals**, skipping one day between
   consecutive intervals so the last day of an interval is not always the same weekday. (This is
   a day-of-week control, not a cosmetic choice.)
2. Within each interval, days 1–49 are the **reference period** and day 50 is the **formation
   period**.
3. Measure daily volume as **dollar volume** (share volume × that day's price). The authors also
   ran the study on the *number of transactions* and report results similar or slightly stronger;
   share volume and dollar volume both work.
4. **Classify the name on the formation day by a within-name time-series rank**: if formation-day
   volume is among the **top 10%** of the 50 daily volumes of that interval, the name is
   *high-volume* for that interval; among the **bottom 10%**, *low-volume*; otherwise *normal*.
   Note what this is not: it is not a cross-sectional ranking of volume, and it never compares one
   name's volume to another's.
5. **Form at the close of the formation date and hold 20 trading days without rebalancing.** The
   long side is the high-volume set, the short side the low-volume set.
6. **Weekly variant**: reference period 49 weeks, formation period 1 week, same top/bottom-decile
   rule. The authors report the effect does not depend on the formation period's length.

Filters and stratification used in the paper, with their purpose:

- Price above $5 throughout the reference period (bid-ask bounce and price discreteness).
- Exclude names with a merger, delisting, partial liquidation or SEO during, or within a year
  before, the interval; require a year of listed history.
- **Analysis is run separately within size groups** (large = market-cap deciles 9–10, medium 6–8,
  small 2–5, decile 1 dropped) because the *level* of volume differs by size by orders of
  magnitude. The within-name ranking already neutralises this, so the stratification is a
  belt-and-braces control rather than part of the signal.
- A nontrading correction: names with more than four non-traded days in the reference period that
  also did not trade on the formation day are classified low-volume only with probability
  `5/(N+1)`, to stop mechanical zeros dominating the low bin.

The stronger variant, and the one to implement first: **apply the classification only to names
whose formation-period return was not itself in the extreme tails.** In the paper this is the
subset with the largest effect and the cleanest interpretation.

## Robustness evidence (qualitative only)

- **Not a risk story.** The high-volume side carries *lower* systematic risk than the low-volume
  side — the wrong direction for a risk explanation of a long-high/short-low spread. The
  strategy's return distribution first-order stochastically dominates that of random portfolios
  formed on the same dates, tested two ways.
- **Information risk falls after high volume.** Bid-ask spreads following high-volume formation
  periods are smaller than the name's own recent average, and larger after low-volume periods.
- **Not driven by announcements or outliers.** Removing firm-announcement windows does not remove
  the effect; it is not a handful of events.
- **Robust to how volume is measured** (dollar volume, share volume, transaction counts) and to
  the length of the formation period (one day or one week).
- **Multi-market replication.** KOS report the premium in 41 countries, in developed *and*
  emerging markets, and that it is **not explained by systematic differences in risk or
  liquidity**; its cross-country magnitude lines up with characteristics the investor-recognition
  hypothesis says should matter. This is a genuine independent replication on a different data
  vendor and a different universe, which is the strongest robustness evidence available for any
  volume signal this folder has covered. It is recorded from the abstract, not the paper.
- **Costs are treated honestly by the authors themselves, and the news is bad.** GKM explicitly
  decline to claim the market-order version is exploitable. Their stated arithmetic, taken from
  Lehmann (1990) and Conrad–Gultekin–Kaul (1991): a one-week return below 1% is consumed by
  one-way costs of **20 bps**. They therefore build a limit-order version instead, in which the
  entry is a passive order at the prevailing quote and unfilled orders simply do not trade.
  **That is not a construction this repo can run** — there is no intraday data, no order model,
  and the engine's execution is a 1-day-lagged fill at the close.

## Implementability here

**What fits unusually well.** The classification is a *within-name time-series rank over a 50-day
window*. That makes it immune to everything that has made cross-sectional volume objects hard on
this universe: different share-unit conventions across 15 regions, different currencies, and the
absence of shares outstanding (which is why the turnover sort was declared uncomputable here).
`aux["volume"]` and `aux["dollar_volume"]` are both usable; the paper says the choice barely
matters. Nothing about the recipe needs the universe to be homogeneous.

**Five concrete pitfalls, in the order they will bite.**

1. **Volume is not forward-filled**, so foreign holidays produce NaN, and a name's 50-day window
   will hold fewer than 50 observations at different times for different regions. Rank over the
   non-NaN days and require a minimum count (say 35 of 50). Do **not** port GKM's `5/(N+1)`
   randomisation: it exists to stop US microcaps with genuinely zero trading from flooding the
   low bin, the long-only book here never trades the low bin, and a randomised classification
   would fail the lab's causality check on determinism grounds.
2. **The stale-volume trap this repo has already been bitten by.** `learnings.md` records that
   the first traded day after a foreign holiday carries a multi-day *return* against a one-day
   *volume*, which inflated `ILLIQ`. The same asymmetry inflates a volume shock in the opposite
   direction — the post-holiday day is a genuine one-day volume against a multi-day information
   accumulation, so it will look like a *low*-volume day relative to nothing. Screen the
   classification's hit rate by region before believing any result.
3. **Breadth is not pinned.** A fixed top-decile rule classifies a *binomial* number of names on
   each formation date — roughly 10% of the scoreable pool in expectation, with real dispersion,
   and the pool itself grows from ~55 names to ~126 across this repo's history. This is exactly
   the 2026-09-06 general rule ("any non-linear set operator must have its breadth pinned by
   construction"). Take the **top `k` names by formation-day within-name volume rank**, not a
   fixed decile threshold.
4. **Horizon and cost.** A 20-day hold with a full re-formation each interval is roughly a
   5–6x-a-year turnover on the conditional sleeve. At 15 bps/side this is not obviously fatal —
   the repo's cheapest books trade under 1x and the seated `liquidity-volume` lead trades ~1.2x,
   but 5x books have run here before — yet the authors' own 20 bps break-even is a warning that
   the gross effect is small. `learnings.md`'s standing rule ("the strongest signal measurable
   here is 5–10 day reversal, and a book paying 15 bps a side is on the wrong side of it") puts
   20 days just past that boundary, not comfortably beyond it.
5. **The long-only half is the favourable half, for once.** Only the high-volume side is
   tradeable here, and it is the side the paper shows carries *lower* systematic risk. That is
   the opposite of the usual long-only truncation problem, where the short leg carries the
   content. It does not follow that the long side carries most of the *return* — see
   `2026-09-06-long-side-share-of-anomaly-profits` — but the risk asymmetry runs the right way.

**Two constructions, in the order they should be tried.**

- **(a) The zero-turnover version first: use the state as a filter, not a sort.** The
  classification is a per-name ternary state, not a score. Applied to an existing book's entry
  decisions — defer buying a name flagged low-volume; prefer a name flagged high-volume among
  otherwise-tied candidates — it adds no positions and almost no turnover, so it is nearly free
  to test and cannot be killed by the cost model. This also sidesteps the breadth problem in 3.
- **(b) The standalone sleeve second**, as a top-`k` book on formation-day volume rank, with the
  normal-return filter of the paper's strongest variant applied.

**The one diagnostic that decides whether this is worth a trial at all**, and it should be
pre-registered before any file is written: this lab has already measured a relative-volume score
and reported "predicts nothing, IC |t| ≤ 1.06 at every horizon". **IC is a whole-cross-section
statistic, and 2026-09-06 established on this repo's own champion that a score can fail a
monotone-relation test while its top bin runs +8%/yr.** GKM's claim is *literally* a corner claim
— the top decile of a within-name distribution — and is not a claim that relative volume ranks
expected return. So the honest test is not another IC: it is **the top-`k` excess of the
high-volume state against the pool, measured on train**, and it should be run before a candidate
file exists. If that excess is null too, the family's volume-shock branch closes properly, on the
statistic the claim is actually about.

## Related

- **Direct tension with two of this lab's own results, and it must not be waved away.**
  `learnings.md` records (i) `SUMMARY.md` #53's relative-volume substitute for the turnover sort
  as a measured null — and a *well-identified* null, since `spearman(rel-volume, log ADV) = +0.045`
  proves it was not a disguised level — and (ii) the repaired standardized-unexplained-volume
  object as a null on the top-band statistic (top-20 excess +0.09 %/yr, top-10-of-pool
  −0.77 %/yr). The lab's conclusion from (i) was that "the family's live content is `ILLIQ`'s
  price-impact numerator and not trading activity under any normalisation". **GKM is a third
  object in that class and the prior against it is strong.** What it adds that neither prior
  screen had: (a) an extreme-decile *state* rather than a continuous score — and (ii)'s null was
  measured on a top band, which is the right statistic, while (i)'s was an IC, which 2026-09-06
  showed is blind to a corner; (b) the normal-return filter, which neither prior object applied;
  (c) a 41-country independent replication behind it, which no volume object screened here has
  had. If the top-`k` diagnostic above comes back null, that is a **third** null in one class and
  the branch should be written up as closed rather than re-approached.
- `2026-08-31-amihud-volume-component-decomposition` (Lou–Shu) is the source the lab used to
  separate `ILLIQ`'s numerator from its volume denominator; this note is about neither, since a
  within-name shock is orthogonal to both by construction.
- `2026-09-06-monotonicity-tests-for-portfolio-sorts` supplies the reason the IC null above is
  not decisive.
- `2026-09-06-long-side-share-of-anomaly-profits` supplies the caution on assuming the long side
  carries the effect.
- `2026-09-04-high-low-spread-estimator` is the other daily-bar route to the spread evidence GKM
  reports from TAQ, if anyone wants to check the spread channel without intraday data.
