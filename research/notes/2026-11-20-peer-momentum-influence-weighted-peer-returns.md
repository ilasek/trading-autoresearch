---
title: "Peer Momentum"
authors: Misirli, Scida, Velikov
year: 2021
venue: unpublished working paper (SSRN; this version dated 8 November 2021, marked "PRELIMINARY") — venue tier 2
url: https://doi.org/10.2139/ssrn.3747402 — read in full from the author-institution copy at https://business.pitt.edu/wp-content/uploads/2022/03/MSV.pdf (1.8 MB, `pdftotext -layout` → 124 KB of clean text, 631 instances of `" the "`, zero `( )` dropout)
citations: 0 (Crossref `is-referenced-by-count` on `10.2139/ssrn.3747402`, checked 2026-11-20); Semantic Scholar's search endpoint answered HTTP 429 and was not retried; **no journal version of this title is indexed in Crossref as of 2026-11-20**, five years after this draft
sample_period: 1928–2020 (networks estimated each June from 1928; Fama–MacBeth regressions 1963–2020)
markets: US only (CRSP), 49 Fama–French industries, 3,068 estimated industry-year networks
tier: B
validation_overlap: true
published_post_2018: true
---

**Read in full**: the network-estimation sections (GARCH volatility inputs, the shrinkage VAR, the
generalized variance decomposition, the three centrality measures and their PCA composite), the
strategy construction, the quintile sort table with every portfolio's own level, the Fama–MacBeth
table, the industry-momentum double sorts, the placebo test, and the appendix tables on size
quintiles, construction choices, the 23-anomaly conditional sorts and the two sample halves.

First note of the 2026-11-20 session, taking the [2026-11-19] **primary aim** — a mechanism
predicting a cross-sectional **first moment** on daily OHLCV, with the **long-leg level** stated —
in the one `program.md` sub-mechanism that had **zero** coverage: `lead-lag-spillover`'s
**network momentum** clause (a `grep -ril` across all 306 prior notes and this file returned 0 for
`network momentum`, `connectedness`, `betweenness` and `Ahern`, and every hit for `network` or
`centrality` was a *neural* network or a *non*-centrality parameter).

**The aim is discharged on criteria (i) and (ii) and FAILS on (iii), and that failure is the
night's most useful single fact** — see *Implementability* for why the signal this paper proposes
is the exact horizon the lab has already measured as a cost wall, and what survives of it.

## Mechanism

Limited attention plus slow diffusion of information between economically linked firms. The
linkage here is **intra-industry**, and the claim is the standard lead-lag one: a firm's price
underreacts to information already revealed in the prices of the firms it is connected to, so the
connected firms' past returns predict its own. Two refinements are the paper's contribution:

- **The linkage is measured, not assumed.** Rather than treating all industry members as equal
  peers (industry momentum) or using an exogenous link list (shared analysts, text-based peers,
  input-output tables), connectedness is estimated from the **co-movement of the firms' own return
  volatilities** — a directed, weighted matrix saying how much of firm `i`'s volatility forecast
  error is attributable to firm `j`. Peers that matter more get more weight in the signal.
- **The attention story has a sign prediction about *which* peers matter.** If the effect is
  investor inability to process linkages, the **peripheral** (least central) peers should carry
  more of it, because a central peer's news is salient and already priced. Dropping the most
  central peers from the signal should therefore *improve* it — a falsifiable prediction the paper
  tests and confirms on its own sample.

The determinants section is worth recording on its own: the single strongest correlate of the
composite centrality measure is the firm's **market share of industry revenues**, and central
firms are larger, invest less and have lower operating leverage. The measure is built with **no
accounting data at all**, so a price-and-volume-only construction recovers an economic-importance
ranking. That is the most transferable claim in the paper for a repo with no fundamentals.

## Construction recipe

**Step 1 — volatility inputs (annual).** For each stock, estimate a GARCH(p,q) conditional
volatility series from **daily returns**, `p,q ∈ {1,2}`, chosen by AIC, re-estimated **every June**
on all history available at that date. Work with the **log** of the volatility series. Filters
applied before estimating: drop a name with any missing daily return in the preceding two years;
drop a name with **five or more consecutive zero-return days** in the recent two-year sample, or
with zero returns on **33% or more** of its history; require **≥ 504** daily observations; drop a
name failing Engle's ARCH test at 1%. The authors report their filters retain under half of the
name count but over half (rising to ~90%) of market capitalisation — i.e. **the filters select
large, frequently traded names**, which is this lab's panel by construction.

**Step 2 — the network (annual, per group).** Within each of the 49 Fama–French industries, fit a
VAR on the daily log conditional volatilities of the member firms, with the shrinkage extension of
Demirer–Diebold–Liu–Yilmaz for high-dimensional systems, then take the **generalized** forecast
error variance decomposition at a **10-day** horizon. The result is an `N × N` weighted,
**directed** matrix (rows: who affects `i`); it is not symmetric and all nodes are connected with
varying weights. A minimum of **5 firms** is required for a group to get a network.

**Step 3 — centrality (annual).** Transpose to the adjacency matrix and compute three standard
measures on the weighted directed graph: **degree** (in/out/total, normalised by `N−1`),
**closeness** (inverse mean shortest path, where path length sums **inverse** edge weights), and
**eigenvector** centrality. Take the **first principal component** of the three, per
cross-section: that is "composite centrality".

**Step 4 — the signal (monthly).** Zero the diagonal of the network matrix and rescale each row to
sum to one: row `i` is now a portfolio of `i`'s peers. **Simple peer momentum** is that portfolio's
**past one-month return**. **Peripheral peer momentum (PPM)** is the same after also zeroing the
columns of peers whose composite centrality is at or above the **90th percentile** of the group,
then rescaling. Weights are held from June of year `t` to May of `t+1`; the past-month returns
refresh monthly, so the signal changes monthly.

**Step 5 — the book.** Sort into quintiles on the signal, value-weighted, NYSE breakpoints,
**rebalanced monthly**.

## Robustness evidence (qualitative only)

- **The long leg's own level is reported, which is what the aim asked for.** On the full sample,
  mean excess returns rise monotonically across PPM quintiles, and the **top quintile earns
  +1.04% per month (t 5.41)** against **+0.23% (t 1.23)** for the bottom, with the long-short at
  **+0.80% (t 6.25)**. Risk-adjusted, the top quintile's **CAPM alpha is +0.32%/month (t 4.10)**
  and its four-factor alpha **+0.28%/month (t 3.50)**, against **−0.48%** and **−0.38%** for the
  bottom quintile. **So roughly 40% of the benchmark-adjusted spread sits on the long leg** — in
  line with, and slightly better than, the long-side shares recorded in
  `notes/2026-09-06-long-side-share-of-anomaly-profits.md` and
  `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`.
- **It survives in the large-cap cell, with the level stated there too.** In a conditional double
  sort on size then PPM, the long-short is significant in **all five** size quintiles (56–83
  bps/month, `t > 3` everywhere except the smallest, which is the *largest* in magnitude). In the
  **largest** size quintile — average constituent market capitalisation in the billions, about 40
  names per cell, the closest cell in this literature to this repo's panel — the top PPM quintile
  earns **+1.01%/month** against **+0.26%** for the bottom, a long-short of **+0.75%/month
  (t 5.77)** with a four-factor alpha of **+0.63% (t 4.70)** and a **market beta of 0.00
  (t 0.11)**. This is the single most aim-relevant table in the paper: a first-moment claim, at the
  long-leg level, in large caps, with the beta reported.
- **Most of the effect is the GROUP AVERAGE, not the network — and the paper's own placebo says
  so.** Replacing the variance-decomposition matrix with a **random log-normal matrix** of the same
  size (diagonal zeroed, rows rescaled) and repeating 1,000 times gives placebo long-shorts of
  **+0.50% to +0.69%/month** with `t` from 4.80 to 6.59, against PPM's +0.80%. PPM beats the 98th
  percentile of that distribution and is not spanned by any placebo draw (alphas +0.16% to +0.34%,
  all significant), but read the other way: **a peer-weighted average of past one-month returns
  with arbitrary weights already earns most of the measured premium.** The estimated network is
  worth roughly 0.11–0.30%/month on top of "any within-group weighting".
- **And much of the residual is industry momentum.** Controlling for one-month industry momentum in
  a conditional double sort cuts the PPM spread from **+0.80% to +0.30%/month (t 3.32)** — the
  *weakest* of all 23 conditional sorts the paper runs against the Novy-Marx–Velikov anomaly set.
  The reverse sort kills industry momentum (to +0.23%, t 2.06), so the paper's claim is that PPM
  **spans** industry momentum rather than adding to it. For a lab that cannot form industry labels
  at all, the honest reading is that **the mechanism's profits are mostly a within-group
  continuation effect, and the network is the increment.**
- Nearly orthogonal to classic 12−2 momentum (Fama–MacBeth `t` 7.37 with the full control set
  including size, value, profitability, investment and one-month reversal; neither sort subsumes the
  other in double sorts). Present in **both halves** of the sample studied, materially weaker in the
  later half. Construction changes (equal weighting, all-stock breakpoints, decile sorts) do not
  overturn it; the weakest variant is the four-factor alpha under all-stock breakpoints.
- **Rubric gaps, stated plainly.** Single market (US). **No independent replication** — zero
  Crossref citations and no indexed journal version five years after this draft, which for a paper
  reporting a `t` above 6 is itself information and is the main reason this is Tier B rather than
  higher. **Transaction costs are not modelled anywhere in the paper** (striking, given an author
  whose published work is the cost taxonomy this folder already holds), and **neither turnover nor
  any persistence statistic for the signal is reported**. Multiple testing is addressed only
  through the 23-anomaly conditional sorts and the placebo distribution — which is more than most,
  and is not a deflation.

## Implementability here

**What is reachable.** Every input is daily price data: the volatility inputs are GARCH on daily
returns (or, cheaper and already in `strategies/lib/features.py`, a **range-based** estimator —
Garman–Klass or Parkinson — which is what `research/README.md`'s `range-variance` material is for);
the network is a VAR plus a generalized variance decomposition; the centralities are three graph
statistics. No fundamentals, no intraday, no analyst data, no link list. The filters the paper
applies select exactly this panel's kind of name.

**Three hard adaptations, in descending severity.**

1. **There are no industry labels here, so the peer group must be something else.** `program.md`
   lists point-in-time sector labels as an unapproved future upgrade, and the v2 hindsight guard
   refuses `groups.py`. The available grouping axes are **listing region / index** and
   `strategies/lib/calendar_peers.py`. A region is a far coarser and more heterogeneous peer set
   than a 49-way industry split, and the mechanism's own story is about *economic* links — so the
   region-level version tests a weaker hypothesis than the paper's.
2. **The paper's signal is a ONE-MONTH peer return, and this lab has measured that horizon as a
   cost wall independent of what supplies the signal.** `experiments/learnings.md` (2026-09-25,
   trial #101) scored names by the mean trailing **21-day** return of their `K = 4` most-correlated
   peers, turned over **18.6× on validation**, paid 5.58%/yr of cost against +4.5% net, and
   recorded the lesson in as many words: *"the wall is about the 21-day horizon, whoever supplies
   the signal."* It also established the useful half: **estimating the neighbourhood is nearly free
   in turnover** (freezing the peer set month to month changed core churn by 0.0005), so the
   expensive part is the signal's horizon, not the network's.
3. **The lab has already recorded this sub-mechanism as closed on a measurement.** The same entry
   says so explicitly, and the object it closed on — `peer_ret` — "cleared all three orthogonality
   gates, including +0.004 against the champion's own momentum score, the most orthogonal object
   this repo has put beside the seat — and still produced a 0.339 book."

**The tension, stated rather than smoothed over.** This source and the lab's measurement are not in
conflict about the same object. The lab's `peer_ret` was an **equal-weighted average over a `K = 4`
undirected correlation neighbourhood at a 21-day horizon**; the paper's object is an
**influence-weighted average over the whole group, from a directed VAR decomposition, with the most
central peers excluded**. The paper's placebo test is the sharpest available evidence on whether
that difference can matter at all, and its answer is *modestly*: arbitrary weights get most of the
way. Combined with the lab's measured cost wall at the 21-day horizon, the paper's own construction
is **not a candidate here as written**.

**What survives, and it is a book rather than a diagnostic.** The two pieces that are *operators on
a peer average* rather than the signal itself, moved to the horizon band where this lab's seat
already operates at ~3× turnover:

- a **within-region**, **influence-weighted** peer average of the **63–252-day** peer return
  (within-region is not a preference: `learnings.md` 2026-10-11 records that the region-matched
  null gate matches cross-region lead-lag move for move, so only the *within*-region version is
  reachable at all), with
- the **peripheral-peer exclusion** (drop the top-decile-central peers' influence before averaging),
  and
- the **no-trade retention band**, which is the one construction that has paid under v3.

Pre-signed **+** (continuation). **Free screens to run before spending a trial, in order**: (a) the
rank correlation between the influence-weighted peer average and the plain equal-weighted one over
the same peer set — if it is near 1, the network is decorative and the whole vein reduces to a
group-momentum object the lab has nulled; (b) the lab's own mandatory joint control (`logP`,
`vol126`) plus a momentum control, since a peer average of past returns is a momentum object by
construction and the record's "an old object in costume" failure has now fired four times; (c) the
level screen the record requires — **the slice's excess in bps, its beta and its turnover
together** — against the paper's own large-cap numbers as the prior.

**The cost arithmetic, done once here so a session does not have to.** In the paper's largest size
quintile the top slice beats the average of its own five size-quintile slices by about **36
bps/month**. A monthly full reshuffle of a large-cap book pays, under v3's own schedule, roughly
15–20 bps per side on both sides of whatever fraction it replaces — of order **30 bps/month** at
near-complete quintile turnover, before UK/HK/FR/IT/ES transaction taxes on a 71%-non-US panel.
**The paper's long-leg advantage and this protocol's cost bill for collecting it monthly are the
same size**, which is the third independent reason not to implement the signal at its published
cadence and the reason the proposal above moves the horizon out.

## Related

- The lab's own measurement that closes the paper's construction: `experiments/learnings.md`
  2026-09-25 (trial #101 `peer_ret`, 18.6× turnover, "the wall is about the 21-day horizon"), and
  2026-10-11 on the region-matched null gate.
- The instrument the network rests on: `notes/2026-11-20-variance-decomposition-connectedness-as-network-degree.md`.
- Centrality as a *characteristic* rather than a weighting scheme, and why its sign is not
  pre-signable: `notes/2026-11-20-network-centrality-as-a-priced-characteristic.md`.
- The peer-group lead-lag mechanisms this folder already holds:
  `notes/2026-08-30-industry-lead-lag-gradual-diffusion.md`,
  `notes/2026-08-31-intra-industry-lead-lag-grouping.md`,
  `notes/2026-08-30-volume-and-cross-autocorrelation-lead-lag.md`,
  `notes/2026-09-05-cross-serial-correlation-as-restatement.md`,
  `notes/2026-09-05-price-delay-market-frictions.md`.
- The long-leg share this paper's table corroborates:
  `notes/2026-09-06-long-side-share-of-anomaly-profits.md`,
  `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`.
- The grouping-axis question the region adaptation runs into:
  `notes/2026-09-10-country-demeaned-versus-country-mean-characteristics.md`,
  `notes/2026-08-28-international-momentum-country-neutral.md`.
- The band: `notes/2026-10-08-no-trade-bands-under-proportional-costs.md`.
