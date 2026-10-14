---
title: "Zeroing In on the Expected Returns of Anomalies"
authors: Chen, Velikov
year: 2022 (published issue 2023; FEDS working-paper version read, dated May 2020; first posted 2017)
venue: "Journal of Financial and Quantitative Analysis — venue tier 1. Read as Federal Reserve FEDS Working Paper 2020-039 (doi:10.17016/FEDS.2020.039), which covers 120 anomalies where the published version covers 204"
url: https://doi.org/10.1017/S0022109022000874 · full text read at https://www.federalreserve.gov/econres/feds/files/2020039pap.pdf
citations: "106 (Crossref is-referenced-by-count for the JFQA DOI, checked 2026-10-14); the FEDS working-paper DOI separately carries 5"
sample_period: "1926–2017 (CRSP returns; high-frequency spread data from ISSM/TAQ from 1983, with the HF sample running to December 2016)"
markets: "US equity (CRSP universe, including microcaps), long-short decile/quintile anomaly portfolios"
tier: "A — tier-1 venue, costs modeled from high-frequency data rather than assumed, multiple testing addressed two independent ways, data and signal definitions published as an open-source dataset. Single market"
validation_overlap: false
published_post_2018: true
---

## Access

Read in full as the FEDS working paper (1.1 MB, 72 pages; `pdftotext -layout` → 142 KB clean text;
`" the "` count 577, `( )`-dropout check zero). **The two versions differ and the difference must be
stated wherever this note is used**: the FEDS version studies 120 anomalies, the published JFQA
version 204, and the headline magnitudes differ accordingly. Everything below is from the version
read, and no figure from the published version is reported at second hand. `research/README.md`'s
note that FEDS serves Federal Reserve staff versions of closed tier-1 articles cleanly held again.

## Mechanism

This is the **prior** for the lab's live question — *is there anything left to find in a
cross-sectional sort, net of what it costs to trade?* — and it is the most directly relevant
calibration this folder holds, because it is the only source here that computes the whole deduction
chain on a large set of anomalies at once rather than defending one.

The paper takes published cross-sectional anomalies and subtracts, in order, four things that the
originating papers mostly did not:

1. **Effective bid-ask spreads**, charged as half the effective spread on every weight change, with
   spreads measured from high-frequency data where available and forecast from low-frequency proxies
   elsewhere.
2. **Post-publication decay** — the McLean–Pontiff channel this folder already holds.
3. **The structural change in trading technology**, by re-estimating on the subsample after that
   change rather than on the full history. *(The dated subsample figures are deliberately not
   recorded here; see the anti-lookahead note below.)*
4. **Data-mining bias** — the bias that arises from *selecting* the strongest anomalies, removed two
   independent ways (below).

**The result.** Net of all four, expected returns are "effectively zero" — and this holds *despite*
the authors applying state-of-the-art **cost mitigation** to every strategy first, and *despite*
their cost measure omitting price impact (so it is a lower bound on cost). Their closing accounting
attributes the originally reported gross return in roughly three parts: **~15% publication bias,
~40% trading costs, ~45% traded away over time.** Those are shares of a gross number, not an
expectation — **do not import them as a forecast**; what transfers is the ordering of the three
channels and the fact that no single one of them is the whole story.

**The two data-mining adjustments are the transferable methodology, and they disagree about nothing.**

- **Out-of-sample sort.** Rank strategies on an *in-sample* statistic, then measure their mean
  return in a later, non-overlapping sample within rank quantiles. Because sampling error in the
  two samples is independent, the later-sample mean within a quantile is an **unbiased estimate of
  the true expected return of strategies selected that way** — a selection-aware estimator that
  needs no model. They try four in-sample selection statistics: mean net return, net Sharpe ratio,
  the return reduction caused by costs, and turnover.
- **Empirical Bayes on Sharpe ratios.** Model the observed Sharpe ratio of strategy `i` as normal
  around its true Sharpe ratio with standard error `1/√T`, put a fitted location-scale `t` prior
  over the true Sharpe ratios across strategies, and report the **posterior mean** for the selected
  ones. The authors note they model the *Sharpe ratio* rather than the mean return deliberately —
  it rescales strategies to comparable volatility — and that **modelling mean returns instead
  produced even smaller adjusted expectations.**

Both adjustments, by completely different routes, say the same thing about the strongest strategies
in a large set: **most of what makes the best one look best is sampling error.**

**The finding inside the out-of-sample sort that matters most here.** Predictability of later net
returns from in-sample statistics is "weak and fragile", the best of the four selection statistics
is the **in-sample net Sharpe ratio**, and **three of the four selection statistics fail to produce
a monotone relation** across quantiles. Picking the winner of a large search by its in-sample
number transfers poorly even when the search is honest.

## Construction recipe

Two recipes, and only the first is a portfolio.

**(1) The cost-mitigated long-short implementation — the "buy/hold spread", a.k.a. banding.**
A `20/40` buy/hold spread *enters* names whose signal is in the top 20th percentile and *exits* a
held name only once its signal falls below the top 40th percentile; between the two thresholds is
an **inaction region** in which no trading occurs. Three points of construction detail:

- The rule **nests the standard academic implementation**: a `20/20` buy/hold spread *is* a plain
  quintile sort, so the band is a one-parameter generalisation of the sort rather than a different
  object. Inaction regions are the known optimal feature of trading under costs
  (Magill–Constantinides), and the authors cite Novy-Marx–Velikov for the empirical finding that the
  buy/hold spread beats the rules commonly used in industry.
- The band prescribes **which** names to hold, not their weights. The authors treat the choice
  between equal and value weighting as a second cost-mitigation lever — value weighting tilts the
  book toward larger, cheaper-to-trade names and is allowed to win when the cost saving exceeds the
  gross-return loss — and deliberately refuse richer weighting functions "to avoid overfitting".
- Their optimisation is two-step and deliberately constrained: choose the **exit** threshold to
  maximise in-sample net return within turnover quartiles (the **enter** threshold is held at a
  convention), then choose the weighting. They are explicit that optimising over more choices would
  improve in-sample performance by construction and overfit.

**(2) The selection-aware estimator, for use on a set of recorded results.**
Rank the recorded strategies on in-sample net Sharpe; evaluate within rank bins on later,
non-overlapping data; or, where no later sample exists, fit a location-scale `t` prior across the
recorded Sharpe ratios and report posterior means. The quantity to model is the **Sharpe ratio**,
not the mean return, and the standard error to use is `1/√T` under the zero-autocorrelation
assumption they state.

**One further recipe worth recording, on measuring costs from daily data.** Where high-frequency
spreads are unavailable, they forecast the effective spread by **combining several low-frequency
proxies** — the high-low estimator, the close-high-low estimator, a Gibbs estimator, and a
volume-based one — rather than choosing the best single proxy, and find the combination beats its
components because the proxies' errors partly cancel. Their caution in the other direction is just
as useful: low-frequency proxies are **biased upward** for liquid names, so a cost model built from
them overstates the bill where the lab mostly operates.

## Robustness evidence (qualitative only)

- **Methodology honesty is this source's strongest feature.** Costs are measured rather than
  assumed; multiple testing is handled two independent ways that agree; the authors state their own
  limitations plainly; and the anomaly signal definitions come from a published open-source dataset,
  so the construction choices are inspectable.
- **Aggregation is the design, not an accident.** Their explicit argument for studying a large set
  is that individual strategies' mean returns are too noisy to say anything about once stale data is
  excluded — they observe that the standard error on a mean return over a decade-and-a-half-long
  sample is of the same order as the effects being argued about. This is a statement about
  *statistical power in strategy research* and it transfers to any lab reading one trial at a time.
- **Two limitations the authors raise, both load-bearing here.** *(i)* They do **not** combine
  anomalies, and they cite evidence that combining improves performance "particularly when
  accounting for trading costs". *(ii)* Spreads are a **lower bound** on cost: they omit price
  impact, and they note the opposite argument too (that a patient trader using limit orders can pay
  less than the spread, at the price of adverse selection and execution risk).
- **Scope.** US only, CRSP universe including microcaps, long-short portfolios. Every one of those
  three differs from this lab's panel, and all three differences matter — see below.
- **Anti-lookahead note on what this entry omits.** The paper's central empirical content is a set
  of subsample magnitudes ("in this period, net of this, the average is X bps"). Those are exactly
  the figures `research/README.md` forbids recording, so this note keeps the **mechanisms, the
  ordering of the channels, the construction recipes and the estimators** and omits the numbers. The
  qualitative claim "net expected returns are an order of magnitude below gross in-sample reported
  returns, and the best-selected ones only a little above the average" is the usable form.

## Implementability here

- **The headline is a prior, and it is the right prior for the lab's current position.**
  `experiments/learnings.md` (2026-10-13/14) records roughly eighteen scores derivable from free
  daily OHLCV screened region-matched with one clearing a `t` of 2, that one failing at the 0th
  percentile of its own null, and the session's own conclusion that "the free-daily-OHLCV score space
  is close to exhausted region-matched". This paper says that outcome is **what the literature's own
  net-of-cost, selection-adjusted numbers predict** for a search over published cross-sectional
  signals — before any adjustment for the three ways the lab's setting is harder (below). A long run
  of nulls here is evidence of a correctly specified protocol, not of a broken one.
- **Three reasons the lab's setting is harder than this paper's, all of which push the same way.**
  *(i)* **Long-only.** This folder already holds the measurement that a large share of anomaly
  profits lives on the short leg
  (`notes/2026-09-06-long-side-share-of-anomaly-profits.md`,
  `notes/2026-09-22-anomaly-profits-short-leg-asymmetry.md`); the net numbers here are for
  long-short books. *(ii)* **Large-cap index members only.** The anomalies in this dataset are
  measured on a universe including microcaps, and the folder's size-group notes
  (`notes/2026-09-02-anomalies-by-size-group.md`,
  `notes/2026-10-02-replicating-anomalies-microcaps-and-breakpoints.md`) record the attenuation in
  big stocks. *(iii)* **Benchmarked, not absolute.** v3 scores skill against a fully-invested
  equal-weight pool, which `notes/2026-10-13-equal-minus-value-as-a-performance-evaluation-factor.md`
  argues is a harder subtrahend than a cap-weighted market. The paper's "effectively zero" is
  therefore an **upper bound** for what this lab should expect from the same signals.
- **It confirms the lab's one construction win and says where the remaining knob is.** The lab's
  measured result that a retention band at `K = 100 / B = 200` cut turnover sharply *and raised* the
  held book's excess is the same object as this paper's buy/hold spread, at a `10/20`-style setting.
  Two refinements are free and untried here: **the exit threshold is the parameter worth optimising
  while the enter threshold stays conventional**, and **the within-book weighting is itself a cost
  lever** — though on this panel the second is closed, because the EW-vs-VW axis needs share counts
  the panel does not have (`#247`), and the lab has separately measured the whole weighting axis as
  flat. So: optimise the band's exit, leave the weighting alone.
- **The stated tension with the lab's own measurement, and its resolution — this is the night's one
  genuinely new buildable item.** The paper's first limitation says combining anomalies helps
  *particularly through trading costs*; the lab measured a walk-forward penalised linear combination
  of seven individually-null features as a null (rank IC ≈ 0, region-matched slice excess
  indistinguishable from zero). These do not contradict each other, because they are claims about
  **different channels**: the lab combined to raise the *signal* and found nothing to combine, while
  the literature's cost argument is that the *trades* of different signals partly cancel, so a
  combined book pays less turnover than the sum of its legs
  (`notes/2026-08-20-trading-diversification-combining-signals.md`). Under v3 — where drift is
  charged, costs are per name, and the pool's own bill is small — the cost-cancellation claim is
  **measurable on train for free and has never been measured here**: compute each leg's one-way
  turnover and the combined book's, and report the ratio. A combination whose IC is zero cannot be
  rescued by cheaper trading, so this is not a candidate on its own; it is the missing precondition
  for every future multi-signal proposal, and it answers "how much does a combiner have to earn in
  IC to be worth building" with a number instead of a guess.
- **The selection-aware estimator is directly applicable and is the second free item.** The lab
  records every trial with a bootstrap skill interval and ranks them with `scripts/rank_trials.py`.
  This paper's out-of-sample sort says the only in-sample statistic with *any* transfer was the net
  **Sharpe ratio** — i.e. the ratio, not the level, which is also what v3 deflates — and that even
  it was non-monotone across quantiles. The usable rule: **treat the ordering inside the leaderboard
  as uninformative, and when enough trials accumulate, shrink the best recorded skill toward the
  cross-trial mean with an empirical-Bayes posterior fitted on skill (the ratio), not on excess
  basis points.** This is the unspent "shrink half" of `#110` with a fitted prior attached, and
  `CLAUDE.md`'s own instruction that tier-1 order "is not evidence" is the same statement arrived at
  from the error-bar side.
- **What this does not license.** No candidate is proposed and no cost-model change is implied; the
  cost estimates here are US spreads from a different era of a different universe and must not be
  compared with v3's tier schedule. The band refinement and the turnover-cancellation measurement
  are both train-only.
- **Family placement.** Cross-family — it is about the yield of the whole search, not about one
  family. The band refinement attaches to `portfolio-learning`; the turnover-cancellation
  measurement to whichever family supplies the legs.

## Related

- `notes/2026-10-14-which-alpha-the-sufficient-statistic-for-beating-a-benchmark.md`,
  `notes/2026-10-14-net-of-cost-model-comparison-and-the-concave-frontier.md` — the statistic and
  its cost-aware scope; this note is the level that statistic takes in practice.
- `notes/2026-08-17-mclean-pontiff-publication-decay.md`,
  `notes/2026-10-01-discovery-sample-and-anomaly-decay.md`,
  `notes/2026-10-01-limits-of-p-hacking-publication-bias.md` — channel 2 of the four, already held
  here from both directions (decay is real; p-hacking alone cannot explain the zoo).
- `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md`,
  `notes/2026-10-08-no-trade-bands-under-proportional-costs.md` — the band, from the two papers this
  one builds its implementation on.
- `notes/2026-08-20-trading-diversification-combining-signals.md` — the cost-cancellation channel
  the tension above resolves into.
- `notes/2026-09-15-inference-on-winners-post-selection-estimation.md`,
  `notes/2026-08-24-deflated-sharpe-ratio.md`,
  `notes/2026-09-16-clustering-trials-onc-effective-number-of-trials.md` — the selection-bias
  machinery this paper's two adjustments are an applied instance of.
- `notes/2026-09-04-high-low-spread-estimator.md`,
  `notes/2026-10-05-chl-spread-estimator-close-high-low.md`,
  `notes/2026-09-04-global-liquidity-proxy-horserace.md` — the low-frequency spread proxies it
  combines rather than chooses between.
- `notes/2026-09-02-anomalies-by-size-group.md`,
  `notes/2026-09-06-long-side-share-of-anomaly-profits.md` — the two adjustments that make its
  "effectively zero" an upper bound for this lab.
