---
title: "Machine Learning vs. Economic Restrictions — where the profitability of learned return signals actually lives"
authors: Avramov, Cheng, Metzker
year: 2023
venue: Management Science 69(5), 2587–2619 (venue tier 1)
url: https://doi.org/10.1287/mnsc.2022.4449
citations: 201 (Crossref `is-referenced-by-count`, checked 2026-09-03); Semantic Scholar by DOI reports 119 (checked 2026-09-03) — the lower of the two, consistent with this folder's standing "disbelieve a lone low count" note, here with Crossref as the higher source
sample_period: full sample 1957–2017; models trained from 1957, validated 1987–1991 in the rolling scheme, with the reported out-of-sample evaluation over 1987–2017
markets: US (CRSP/Compustat), 94 firm characteristics plus macro state variables
tier: A
validation_overlap: false
published_post_2018: true
---

Read **in full** from the INFORMS typeset article (34 pages) served from the second author's own
site (`si-cheng.net/wp-content/uploads/2023/05/2023-ms-avramov_cheng_metzker-machine-learning-vs.-economic-restrictions.pdf`),
complete with volume, issue and page headers. Author-hosted copies of INFORMS articles are a
channel that had not been used in this folder before and worked first try.

This is the cost-and-feasibility companion to the same night's `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md`.
It takes four published machine-learning return-prediction methods, reproduces their headline
results, and then asks a single question: **how much of the predictability is left once you exclude
the stocks a real long-only book cannot hold, and once you pay for the turnover?**

## Mechanism

The paper's subject is not a new signal; it is the **location** of an existing family of signals in
the cross-section, and the economic reading of that location.

**The four methods examined.** A three-hidden-layer feed-forward neural network as in Gu–Kelly–Xiu
(GKX); a no-arbitrage-constrained multi-network architecture as in Chen–Pelger–Zhu (CPZ); the
linear instrumented principal component analysis of Kelly–Pruitt–Su (IPCA); and a conditional
autoencoder (CA), which relaxes IPCA's linearity by modelling factor loadings with a network. All
four take the same 94 firm characteristics (plus macro state variables) and predict the
cross-section of stock returns. A fifth object, the SDF of Kozak–Nagel–Santosh, is used to repeat
the exercise on a portfolio universe rather than on individual stocks.

**Finding 1 — the predictability is concentrated in stocks that are hard to arbitrage.** Relative to
the all-stock result, the risk-adjusted long-short payoff of the *deep* learners falls by roughly
half to three-quarters when microcaps are excluded (below the 20th NYSE size percentile), by a
comparable amount when firms without credit-rating coverage are dropped, and by roughly
three-quarters to nearly all of it when financially distressed firms facing deteriorating credit are
excluded — after which none of the deep-learning methods produces a significant value-weighted
risk-adjusted return at the 5% level. The same restrictions applied to traditional anomaly sorts
produce a **similar proportional** deterioration, so this is a statement about where cross-sectional
predictability lives in general, not a special indictment of neural networks.

**Finding 2 — and this is the one that matters most for a big-stock universe: the *nonlinearity* is
what is concentrated there.** IPCA, the linear method, underperforms the deep learners on the full
sample but its performance deteriorates only *modestly* on the cheap-to-trade subsamples. The
authors read this directly: modelling nonlinearities is especially useful for difficult-to-value and
difficult-to-arbitrage stocks. Where those stocks are absent, the extra machinery buys much less
over a linear model.

**Finding 3 — turnover is the second constraint and it binds independently.** All four learned
signals turn over far faster than most individual anomalies — monthly long-short turnover of at
least ~87% for the shallowest of them and up to roughly 150% for others. Converting the
risk-adjusted payoff into a **break-even one-way transaction cost** (payoff divided by turnover),
the full-sample break-evens sit near the upper end of plausible cost estimates, and once microcaps
are excluded they fall by roughly half and land **at or below** the cost levels the empirical
trading-cost literature implies for the same kinds of portfolios. The mechanism is not subtle: the
mean-variance-efficient portfolio implied by an estimated pricing kernel takes extreme positions
that must be continually re-established.

**Finding 4 — the learned signals are interpretable, and what they load on is a checklist of
limits-to-arbitrage.** Stocks in the long leg are typically small, value, illiquid, old, low-priced,
low-beta, medium-term winners, with low asset growth, low equity issuance, and low credit-rating and
analyst coverage. So the black box rediscovers the anomaly literature — a point in its favour
methodologically (no preselection of characteristics, so no data-snooping through the anomaly zoo)
and a point against its tradeability on a liquid universe.

**Finding 5 — two results that cut the other way, and should not be dropped when quoting this
paper.** (a) Unlike most individual anomalies, whose payoff is concentrated in the **short** leg, the
learned signals earn a significant risk-adjusted return in the **long** leg while the short leg is
insignificant — which is precisely the half a long-only book can hold. (b) Decomposing the payoff
against an industry benchmark, the **intra-industry** strategy (long industry winners, short industry
losers) outperforms both the unconditional strategy and the inter-industry (industry-rotation)
version: the learned signal is more informative for stock selection *within* peer groups than for
picking industries. (c) The signals mitigate downside risk and behave well in market-stress states.

## Construction recipe

This is an evaluation protocol rather than a strategy, and the protocol is the transferable part:

- **Split by tradeability before reading any cross-sectional result.** Re-run the same sort with
  microcaps excluded, with hard-to-value names excluded, and value-weighted as well as
  equal-weighted, and report all of them. The gap between the all-stock and restricted versions *is*
  the finding.
- **Report turnover next to the payoff, and convert to a break-even cost.** Break-even one-way cost
  = risk-adjusted payoff ÷ turnover, in the same units. A signal is only interesting if that number
  exceeds the cost you actually pay; quoting a payoff without it is uninformative for a
  cost-constrained book.
- **Decompose the payoff into within-group and across-group components** by benchmarking each name
  against its industry (or region) average, then building three books: unconditional, intra-group,
  inter-group. Which of the three carries the payoff tells you what the signal is.
- **Interpret the learner by regressing or sorting its selections on known characteristics.** If the
  long leg's characteristic profile is a list of illiquidity and distress proxies, the model has
  found limits to arbitrage, not a new mechanism.
- **Rolling refits with a validation block**: the models are trained on an expanding window with a
  separate validation slice used to choose hyperparameters, then applied out of sample — the
  bookkeeping shape this repo already implements in `strategies/lib/walkforward.py`.

## Robustness evidence (qualitative only)

Four independently published methods spanning linear and deep architectures, replicated by this
team before being stress-tested; a large multi-decade US sample; the same restrictions applied to
traditional anomaly sorts as a control, giving a comparison rather than an isolated number. The
authors report robustness to imposing the economic restrictions on the *training* sample rather
than only the evaluation universe, to a value-weighted loss function, and to predicting
risk-adjusted rather than raw returns. Tier-1 venue, and the paper's direction of travel is
deflationary about its own field, which is the honest direction. The main gaps: single market (US),
and the restrictions studied are size/distress/rating-coverage rather than an explicit
liquidity-cost model of the specific portfolios. The findings sit alongside — and agree with — the
broader replication literature this folder already holds on microcap-driven anomaly evidence.

## Implementability here

1. **The dominant fact: this repo's universe is the restricted subsample, permanently.** ~145
   large-cap global names and 42 ETFs contain no microcaps, essentially no distressed names, and
   nothing without rating or analyst coverage. Everything this paper strips out to make its point is
   already absent here by construction. **The expected size of any learned cross-sectional edge on
   this universe is the restricted-subsample number, not the headline** — which for the deep methods
   is not statistically distinguishable from zero at conventional levels, and whose break-even cost
   sits at or below realistic trading costs *before* this repo's 15 bps/side is applied.
2. **The sharpest practical consequence, and it is a prior rather than a screen: prefer the linear
   model, and expect the nonlinear one to add nothing.** Finding 2 is a direct measurement of what
   `research/README.md` already advises on general grounds ("prefer few features and a penalised
   linear model first"). It says more than that: the *reason* to prefer linear here is not merely
   sample size, it is that the incremental value of nonlinearity was measured and found to live in
   exactly the names this universe does not contain. A candidate proposing a tree ensemble, a
   boosted learner or a network on this cross-section should be expected to reproduce its linear
   counterpart at higher turnover — which is a strong enough prior to decline such a candidate
   without a trial, and to state that the family's remaining live question is about *construction*,
   not about model class.
3. **Turnover is the second, independent reason, and the lab has already measured its own version of
   it.** `learnings.md` records that outside `price-trend`, turnover differences dominate every
   comparison, and that the union books run 13–19× annually with cost drag of 2–3%/yr. A learned
   monthly signal turning over ~90–150% a month is far outside that, and there is no version of it
   that survives 15 bps/side. If a learned candidate is ever built here, **its turnover must be
   constrained in the objective or by construction** (fewer rebalance dates, banding, or a fixed
   quota) rather than measured afterwards.
4. **Two genuinely encouraging results the lab should not discard with the rest.** The long-leg
   result (finding 5a) says the half a long-only book can hold is the half that carried the
   risk-adjusted payoff for these signals — the opposite of the standard anomaly pattern, and
   directly relevant to a repo whose central constraint is `max_leverage = 1.0`. And the
   intra-industry decomposition (finding 5b) says the content is in **peer-relative** ranking, which
   is a construction the lab can express cheaply: score each name against its region or sector peer
   group rather than against the whole universe. That is a free diagnostic on any existing leg —
   rebuild the score as a within-group deviation and compare — and it is a different question from
   the regional-neutralisation bracket `learnings.md` closed, which was about *weights*, not about
   the scoring benchmark.
5. **A caution against over-reading this note.** It measures US individual stocks, so it says
   nothing directly about the ETF half of the universe, about `seasonality-calendar`,
   `lead-lag-spillover` or `portfolio-learning`, and nothing about whether a *learned combiner over
   the lab's own legs* (a handful of inputs, not 94) inherits any of these problems — a 10-input
   problem is not the high-dimensional problem this paper stress-tests. Do not carry the
   attenuation ratios into those settings by analogy.
6. **What it licenses in `SUMMARY.md`.** A pre-trial rule of the same shape as #68's big-stock rule,
   and stacking with it: before proposing any learned candidate, state which subsample of the
   source's universe this repo resembles and what the source reported *there*. Free, retrospective,
   and it would have discounted the family's headline appeal before the lab's own penalised-combiner
   screen was run.

## Related

- `notes/2026-09-03-shrinking-the-cross-section-sdf-shrinkage.md` — the companion; that note says
  what to estimate and how to regularise it, this one says how much of the estimate survives
  restriction and cost. This paper also uses that paper's SDF estimator for its portfolio-universe
  test.
- `notes/2026-09-02-anomalies-by-size-group.md` (Fama–French 2008) — the same conclusion reached
  twenty years earlier for traditional anomaly sorts; `SUMMARY.md` #68 is the rule, this is its
  machine-learning instance, and the two together make the big-stock discount the folder's most
  general screen.
- `notes/2026-08-29-machine-learning-cross-section-comparative.md` (Gu–Kelly–Xiu) — one of the four
  methods stress-tested here; read that note's claim that ML predictability is *stronger* among
  large stocks against this note's finding 2, which locates the deep learners' *edge over linear
  models* among small and distressed ones. Both can hold: accuracy versus where the extra
  nonlinearity pays.
- `notes/2026-08-27-momentum-net-of-costs-debate.md` and
  `notes/2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the break-even-cost framing
  and the standard responses to high turnover.
- `experiments/learnings.md` 2026-08-29 (the penalised linear combiner) and 2026-08-30 (turnover
  dominates comparisons outside `price-trend`) — the lab's own measurements that points 2 and 3
  connect to.
