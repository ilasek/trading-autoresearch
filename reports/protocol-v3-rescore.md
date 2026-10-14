# Protocol v3 re-scoring — every strategy, with the T-bill rate (2026-10-13, updated 10-14)

> **What this is.** A re-scoring, not new research. Every strategy the lab has recorded was re-run
> under **protocol v3**: 104 under v1, 6 under v2 (5 scored), and 3 under v3. The eight ported v1
> champions and three sanity strategies were re-run too.
> It supersedes the W41 re-scoring (`reports/2026-W41.md`), which ran before the cash-rate series
> was in the store and so paid 0% on cash and measured Sharpe on raw returns. This run uses the
> stored 13-week T-bill rate (`RATE_US3M`, 1.82%/yr on average over validation) and today's
> membership store, after PR #9.
>
> Train and validation only: **no holdout data was read**, and nothing was added to
> `experiments/trials.jsonl`, so no deflated bar moved.
> - Harness: `scripts/rescore_protocol_v3.py`, unchanged; 123 rows, 0 errors. The third v3 trial, recorded on
>   2026-10-14, was scored on 10-14 with the same harness and data.
> - Raw rows: `experiments/protocol_v3/rescore.jsonl`.
> - Validation returns: `experiments/protocol_v3/returns/`.
> - **Check:** the three v3 trials reproduce their recorded validation Sharpe and skill exactly
>   (0.304 / −0.033, 0.218 / −0.119 and 0.285 / −0.052).
> - **Every strategy, in order:** see the appendix at the end.

## In plain English

**The question.** Every strategy is asked one thing: would it have done better than simply
buying an equal slice of every stock in the index and holding it (the "basket")?

**The answer: no strategy the lab has built can be shown to do better.**
- **A coin-flip split.** Of the 85 strategies that picked from the whole market, about half came
  out a little ahead of the basket over 2018–2023 and half a little behind. Every gap is smaller
  than what six years of luck can produce.
- **The leaders are one idea.** The best-looking strategies are almost all "buy last year's
  winners", tried about 60 different ways. Try one idea 60 ways and the best version will look
  good by luck alone.
- **The earlier years don't back them up.** On 1997–2017, almost none of them beat the basket
  either. A real edge should show up in both periods; none does.
- **The apparent winners cheated, without meaning to.** The only strategies that clearly beat the
  basket were limited to companies we already know survived to today. One of them picks stocks
  at random, so the edge comes from knowing the survivors, not from the method.
- **Bottom line.** After about 110 attempts, nothing beats owning the whole basket. That is a real
  result: it says this search, with free daily prices and long-only portfolios, has not found an
  edge.

**TL;DR.** The T-bill rate changes the levels and not the verdict. **No unconfined strategy shows
skill it can prove.** "Skill" means Sharpe minus that of an equal-weight basket of every eligible
stock, both measured in excess of T-bills.

- **The basket's Sharpe fell from 0.45 to 0.34.** Its own excess return is paying for cash now,
  and it is less volatile than most of the books measured against it. That lifted the median
  trial's skill by +0.04. The lift is not evidence of skill.
- **Unconfined trials (85).** None has a 90% skill interval above zero. 39 have positive point
  skill. The best is +0.15, with an interval about ±0.6 wide. The best deflated-skill
  probability is **0.26** against a bar of **0.95**.
- **All 85 sit in tier 1.** The data cannot separate any of them from the best. 61 of them are
  one mechanism (momentum).
- **Train gate.** Only **5** unconfined trials beat the basket on train (1997–2017):
  - four ETF allocation books;
  - one stock-selection book, v3-3 `lv_illiq_peer_neutral_band`, recorded on 10-14.

  All five have negative validation skill. **No unconfined
  stock-selection strategy beats the basket on both train and validation.**
- **Confined trials.** As before, the only intervals above zero belong to the confined trials,
  which can only pick from today's survivors. One of the three is a no-information placebo.
- **The only gated pass.** `hindsight_winners`, a sanity strategy that cheats by design, clears
  every gate. The other is the confined trial #23.

## What changed since the W41 re-scoring

| | W41 re-scoring (cash at 0%) | this re-scoring (T-bill rate) |
|---|---|---|
| equal-weight basket, validation Sharpe | 0.45 | **0.34** |
| equal-weight basket, train Sharpe | — | 0.52 |
| median validation Sharpe, all scored trials | 0.41 | **0.33** |
| median change in a trial's Sharpe | — | −0.08 (range −0.38 to −0.06) |
| median change in a trial's skill | — | **+0.04** (largest move −0.26) |
| rank agreement of skill with W41 (Spearman) | — | +0.98 |

**Why skill moved, and in which direction.**
- **The mechanism.** Subtracting the T-bill rate lowers a book's Sharpe by the cash rate divided
  by the book's volatility.
- **Concentrated books gain skill.** The basket's volatility is 15.9%, below most of the 15–30
  name momentum books. So the basket loses more Sharpe than those books do, and their skill
  rises.
- **Low-volatility books lose skill.** The fall in skill tracks a book's own volatility (the
  change in skill correlates +0.83 with the book's volatility). The calmest books lose the
  most:

  | # | strategy | volatility | change in skill |
  |---|---|---|---|
  | 99 | `rv_minvar_closedform` | 4.0% | −0.26 |
  | 5 | `gtaa_trend_diversified` | 7.4% | −0.13 |
  | 8 | `risk_parity_multi_asset` | 7.8% | −0.11 |
  | 3 | `ew_global_etf` | 9.7% | −0.07 |
  | 6 | `lowvol_equity_tilt` | 10.0% | −0.07 |

  These five books had looked like ties with the basket under rf = 0. That was cash and bond
  carry counted as return.
- **W41's caveat was partly wrong.** It predicted that seeding the rate would "barely move skill".
  That holds for the momentum majority. It does not hold for the allocation and low-volatility
  books.
- **Cash interest and membership.** Recomputing every book at rf = 0 reproduces W41's Sharpe to
  within 0.01 for 113 of 120 rows. The seven exceptions (+0.02 to +0.08) are books that sit
  partly in cash, which now earns interest:
  - the ETF/bond rotators #2 and #4;
  - the seasonal books #59 and #60;
  - the placebo partner #75;
  - the minimum-variance book #99;
  - risk parity #8.

  The PR #9 membership corrections did not visibly move any validation number.

**What did not change.**
- **The gates still fail most trials** (a trial can fail several):
  - train skill not above zero: 98 of 112 scored trials;
  - not beating 90% of random books built like it: 74;
  - validation drawdown worse than −45%: 23;
  - one trial each for too few positions and too much turnover.
- **One real trial clears every gate:** #23, which is confined.
- **The v1 record still does not predict v3.** Rank agreement between v1's recorded validation
  Sharpe and v3 is +0.46. The median recorded Sharpe was 0.87; under v3 it is 0.33.

## Strategy leaderboard (v3, unconfined, with error bars)

**Every one of the 85 unconfined trials is in tier 1.** The 10% model confidence set cannot
separate any of them from the best, so the order below is not evidence. Ranking comes from
`engine.ranking.rank_table` over the re-scored validation returns, the same method as
`scripts/rank_trials.py`.

**Column notes:**
- "Mech." groups trials whose returns in excess of the basket correlate at 0.5 or more; trials
  in one mechanism are one bet.
- "DSR" is the deflated-skill probability. It is illustrative: it uses the re-scored skills and
  standard errors against the v3 deflator, with 112 recorded trials across all versions and
  **39 effective**. A seat needs 0.95.
- "Random %ile" is where the trial's Sharpe sits among random books built like it (50 draws).

**The 15 unconfined trials with the highest skill:**

| tier | # | strategy | family | skill [90% CI] | skill @2× cost | train skill | random %ile | DSR | mech. | what it does |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 33 | `mom_zscore_overlap6_fixed_anchor` | cross-sectional momentum | +0.15 [−0.44, +0.65] | +0.14 | −0.07 | 96 | 0.22 | M1 | Recent winners, one-sixth of the book rebuilt each month, sizing each stock against a fixed yardstick. |
| 1 | 39 | `mom_zscore_overlap6_market_trim` | regime switching | +0.15 [−0.55, +0.76] | +0.14 | −0.02 | 90 | 0.26 | M1 | The six-month blend, with the safety cut-back triggered by the whole market's swings. |
| 1 | 37 | `mom_zscore_overlap6_trim_universe` | cross-sectional momentum | +0.15 [−0.56, +0.73] | +0.13 | −0.01 | 84 | 0.25 | M1 | The six-month blend, with the cut-back watching every stock actually held. |
| 1 | 42, 46 | `mom_zscore_overlap6_hzn_avg4` / `mom_hzn_avg4_k6_cohort_trim` | cross-sectional momentum | +0.14 [−0.44, +0.61] | +0.13 | −0.06 | 92 | 0.19 | M1 | Four winners portfolios (12, 9, 6, 3-month gains), a quarter in each, blended over six months. Identical returns. |
| 1 | 34 | `mom_zscore_overlap6_live_tranche` | cross-sectional momentum | +0.14 [−0.62, +0.77] | +0.11 | −0.09 | 96 | 0.25 | M1 | The six-month blend, dropping older picks the latest ranking no longer likes. |
| 1 | 32, 35, 38, 40 | `mom_zscore_overlap6_daily_trim` / `_notrim` / `_legacy_trim` | cross-sectional momentum / regime switching | +0.13 [−0.54, +0.69] | +0.12 | −0.08 | 90 | 0.22 | M1 | Recent winners, one-sixth rebuilt each month. Identical returns: the safety cut-back never fires under v3. |
| 1 | 41 | `mom_zscore_overlap6_hzn_avg` | cross-sectional momentum | +0.13 [−0.49, +0.63] | +0.11 | −0.08 | 84 | 0.20 | M1 | Two winners portfolios (12- and 6-month gains), half in each. |
| 1 | 61 | `sl_ridge_nontrend_block` | statistical-learning | +0.12 [−0.22, +0.41] | −0.05 | −0.11 | 98 | 0.07 | M2 | A ridge model retrained monthly on four non-trend clues (calendar month, ease of trading, unusual volume, last month's drop). |
| 1 | 36 | `mom_zscore_overlap6_ddbrake` | regime switching | +0.10 [−0.60, +0.70] | +0.08 | −0.08 | 72 | 0.22 | M1 | Adds a drawdown brake: 60% exposure from 20% below peak until within 10%. |
| 1 | 53 | `mom_hzn_avg4_noagree` | cross-sectional momentum | +0.09 [−0.47, +0.54] | +0.02 | −0.12 | 98 | 0.15 | M1 | Four-window winners without the bonus for multi-window agreement. |
| 1 | 50 | `mom_hzn_avg4_no_resize` | cross-sectional momentum | +0.07 [−0.50, +0.51] | +0.04 | −0.13 | 82 | 0.14 | M1 | Never resizes a stock it already holds. |
| 1 | 22 | `mom_multihorizon_zscore_damped_buffered` | cross-sectional momentum | +0.07 [−0.53, +0.60] | +0.02 | −0.06 | 88 | 0.17 | M1 | Two-window winners, with position sizes softened. |
| 1 | 65 | `pt_raw_reversal_control` | price-trend | +0.06 [−0.31, +0.37] | −0.07 | −0.31 | 100 | 0.05 | M2 | Buys last month's biggest fallers. A raw-reversal control. |
| 1 | 47 | `mom_hzn_avg4_subsample_bag3` | combinations | +0.06 [−0.50, +0.50] | −0.00 | −0.10 | 96 | 0.13 | M1 | Four-window winners averaged over three random sub-samples of the stock list. |

**What these rows show:**
- **Train.** Every row has negative train skill, so each fails the train gate.
- **Costs.** The non-momentum rows lose their skill at twice the costs.

**The v2 and v3 trials:**

| tier | # | strategy | family | skill [90% CI] | skill @2× cost | train skill | DSR | mech. | what it does |
|---|---|---|---|---|---|---|---|---|---|
| 1 | v2-3 | `sa_pca_resid_reversion` | statistical-arbitrage | +0.02 [−0.30, +0.30] | −0.20 | −0.30 | 0.02 | M2 | Buys the 30 stocks that fell furthest relative to look-alike stocks last month. |
| 1 | v2-1 | `pt_resid_reversal_v2` | price-trend | +0.02 [−0.32, +0.31] | −0.13 | −0.30 | 0.02 | M2 | Buys the 30 stocks that fell furthest behind the average stock last month. |
| 1 | v2-6 | `lv_resid_rev_illiq_tilt` | liquidity-volume | +0.01 [−0.37, +0.31] | −0.26 | −0.24 | 0.03 | M2 | The look-alike bounce-back bet, tilted toward thinly traded stocks. |
| 1 | v3-3 | `lv_illiq_peer_neutral_band` | liquidity-volume | −0.05 [−0.27, +0.15] | −0.06 | **+0.08** | 0.00 | M9 | Illiquid stocks, judged only against peers in the same region. Beats the basket on train but not on validation; fails the random and drawdown gates. |
| 1 | v3-1 | `pt_lowvol_gk_quarterly` | price-trend | −0.03 [−0.26, +0.21] | −0.05 | −0.06 | 0.00 | M1 | The 100 calmest eligible stocks by a year of daily trading ranges, equal weight, rebalanced quarterly. |
| 1 | v3-2 | `sa_resid_rev63_band` | statistical-arbitrage | −0.12 [−0.32, +0.04] | −0.23 | −0.00 | 0.00 | M2 | Buys the 100 stocks most behind what market-wide factors predicted over three months, keeping holdings while in the top 200. |
| 1 | v2-5 | `sl_ridge_six_masked` | statistical-learning | −0.15 [−0.45, +0.13] | −0.28 | −0.54 | 0.00 | M2 | A ridge model on six stock measurements, look-ahead leak fixed. |
| 1 | v2-2 | `pt_resid_reversal_band` | price-trend | −0.23 [−0.46, −0.03] | −0.43 | −0.18 | 0.00 | M2 | The bounce-back bet on ranks 31–120 instead of the top 30. |
| — | v2-4 | `sl_ridge_six_features` | statistical-learning | not scored | | | | | Failed the look-ahead check. |

**Unconfined trials whose interval is entirely below zero** (7), meaning they reliably trail
the basket:
- `lv_amihud_illiquidity_tilt` (#57): −0.47;
- `sc_same_month_seasonal_aligned` (#60): −0.48;
- `sc_same_month_seasonal` (#59): −0.39;
- `pl_factor_momentum_timed` (#92): −0.39;
- `pl_2leg_placebo_partner` (#75): −0.27;
- `sa_pca_residual_excursion` (#63): −0.25;
- `pt_resid_reversal_band` (v2-2): −0.23.

## By family (unconfined trials)

| family | trials | median skill | best skill | median v3 Sharpe | median Sharpe as recorded | mechanisms |
|---|---|---|---|---|---|---|
| regime switching | 5 | +0.10 | +0.15 | 0.43 | 1.05 | M1 |
| cross-sectional momentum | 33 | +0.04 | +0.15 | 0.38 | 1.05 | M1 |
| price-trend | 7 | +0.02 | +0.06 | 0.35 | 0.65 | M1, M2 |
| liquidity-volume | 5 | −0.01 | +0.01 | 0.33 | 0.67 | M2, M3, M7, M9 |
| combinations | 8 | −0.04 | +0.06 | 0.29 | 0.87 | M1 |
| statistical-arbitrage | 3 | −0.12 | +0.02 | 0.22 | 0.47 | M2, M4 |
| short-term mean reversion | 2 | −0.14 | +0.03 | 0.19 | 0.60 | M2 |
| volatility targeting / risk parity | 2 | −0.15 | −0.05 | 0.19 | 0.42 | M1 |
| statistical-learning | 3 | −0.15 | +0.12 | 0.19 | 0.60 | M2 |
| time-series momentum / trend following | 2 | −0.17 | −0.13 | 0.17 | 0.43 | M1 |
| portfolio-learning | 5 | −0.17 | −0.01 | 0.16 | 0.80 | M1, M2, M6 |
| range-variance | 4 | −0.20 | −0.10 | 0.14 | 0.44 | M1, M5 |
| low-volatility / quality tilts | 2 | −0.28 | −0.26 | 0.05 | 0.66 | M1 |
| lead-lag-spillover | 2 | −0.33 | −0.30 | 0.01 | 0.35 | M8 |
| seasonality-calendar | 2 | −0.44 | −0.39 | −0.10 | 0.71 | M1 |

**15 family labels, 9 mechanisms.**
- **M1** (momentum, plus the ETF and blend books that move with it) holds 61 trials, with median
  skill +0.00.
- **M2** (short-term and residual reversal) holds 15, with median skill −0.01.
- **The other seven** mechanisms hold one or two trials each. Their best skill is +0.00 (#94's overnight-sentiment
  reversal); the rest are negative.
- **Family medians.** The top family medians are positive only because of the basket's lower
  bar. The order of families is the same as in W41.

## Ported v1 champions

v1's champion lineage, as ported to read point-in-time members. These are validation numbers
under v3.

| promoted | strategy | v3 Sharpe (W41 → now) | v3 skill [90% CI] | train skill |
|---|---|---|---|---|
| #1 | `mom_12m_baseline` | 0.46 → **0.39** | +0.06 [−0.54, +0.53] | −0.10 |
| #35 | `mom_zscore_overlap6_daily_trim` | 0.39 → 0.32 | −0.02 [−0.73, +0.53] | −0.07 |
| #41 | `mom_zscore_overlap6_hzn_avg` | 0.39 → 0.31 | −0.03 [−0.68, +0.48] | −0.05 |
| #42 | `mom_zscore_overlap6_hzn_avg4` | 0.39 → 0.31 | −0.03 [−0.67, +0.44] | −0.03 |
| #43 | `mom_zscore_hzn_avg4_k1` | 0.24 → 0.17 | −0.17 [−0.79, +0.36] | −0.04 |
| #45 | `mom_hzn_avg4_k1_cohort_trim` | 0.24 → 0.16 | −0.17 [−0.80, +0.32] | −0.01 |
| #51 | `mom_hzn_avg4_nobuffer` | 0.23 → 0.16 | −0.18 [−0.82, +0.32] | −0.02 |
| #98 | `pt_mom_evar_arbrisk` ⚠ confined | 0.12 → 0.03 | −0.31 [−0.94, +0.17] | +0.04 |

**The ladder still runs backwards.**
- **The first champion is still the best.** Plain 12-month momentum is the best of the eight, and
  it ties the basket.
- **Later promotions made it worse.** Each promotion after #42 lowered v3 Sharpe.
- **No seat.** The v1 champion holds no seat under v3, and no v2 or v3 candidate has earned one.

## The confined trials

27 v1 trials read `strategies/lib/groups.py` and could only rank today's surviving large caps.
Their numbers are survivorship-biased under any protocol. They still top the raw table:

| # | strategy | skill [90% CI] | W41 skill |
|---|---|---|---|
| 79 | `pl_union_region_relative_illiq` | +0.34 [+0.08, +0.59] | +0.33 |
| 71 | `pl_fixed_share_tails` | +0.28 [+0.03, +0.52] | +0.27 |
| 77 | `pl_zeroleg_all_placebo` | +0.27 [+0.02, +0.48] | +0.27 |
| 68 | `pl_maxleg_signal_blend` | +0.28 [−0.07, +0.58] | +0.27 |

- **The intervals above zero.** These are still the only three trials in the lab's history with a
  skill interval above zero, and one of them, #77, picks stocks with a random hash. That is the
  price of picking among known survivors.
- **#23 clears every gate.** `mom_multihorizon_zscore_sectorneutral` clears every v3 gate
  (skill +0.19 [−0.38, +0.63]). It is confined by its own sector list.

## Sanity checks

| strategy | v3 Sharpe | skill [90% CI] | random %ile | clears all gates? | reading |
|---|---|---|---|---|---|
| `random_selection` | −0.09 | −0.42 [−0.77, −0.17] | 28 | no | A random book trails the basket by 0.42: the cost of trading and concentrating with no information. |
| `momentum_12_1` | 0.39 | +0.06 [−0.54, +0.53] | 88 | no | Plain 12-month momentum ties the basket. Identical to ported #1. |
| `hindsight_winners` | 1.03 | +0.70 [+0.15, +1.20] | 100 | **yes** | A hard-coded list of today's big winners passes every gate. Only the hindsight guard stops it. |

## Conclusions

1. **The T-bill rate was the last missing input, and it did not rescue anyone.** With cash
   priced correctly the basket is a lower bar (0.34). Still, no unconfined trial clears it with
   an interval above zero. The best deflated-skill probability is 0.26 against 0.95, with 39
   effective trials searched in this window.
2. **Train skill is the binding constraint, not validation.** 98 of 112 trials fail the train
   gate. The five unconfined trials that pass it (four ETF allocation books, one illiquidity
   book) all lose to
   the basket on validation. No stock-selection idea in the record beats the basket in both
   periods.
3. **The cheap-but-wrong comparison is gone.** Low-volatility and bond-heavy books had looked
   like ties with the basket only because cash and carry earned nothing in the benchmark either.
   Priced correctly, they trail it by 0.07–0.26 of Sharpe.

---
**Caveats.**
- **Null draws.** The random-selection gate used 50 draws instead of a trial's 200, so the
  percentiles are approximate.
- **Old code.** v1 code ran seeing each stock only while it was an index member (variant V3m, as
  in the v2 re-scoring).
- **Deflated skill.** The DSR column is illustrative: no trial was recorded.
- **Holdout and forward numbers.** None appear here, by design.
- **Scope.** This is research output on free daily data with modelled costs, not investment
  advice.

---

## Appendix: every strategy, in order

**How to read these tables:**
- **Order.** Sorted by validation skill (Sharpe minus the equal-weight basket's, both above
  T-bills), computed by `engine.ranking.rank_table`.
- **Tier.** Tier 1 means the data cannot separate the strategy from the best (10% model
  confidence set). Order inside tier 1 is not evidence.
- **"vs basket".** Reads the 90% interval:
  - *better* means the whole interval is above zero;
  - *worse* means the whole interval is below zero;
  - *can't tell* means the interval spans zero.
- **"random %ile".** Where the strategy's Sharpe sits among 50 random books built like it. The
  gate needs 90 or more.
- **"gates failed".**
  - *train*: no skill on 1997–2017;
  - *random*: below the 90th random percentile;
  - *drawdown*: worse than −45% on validation;
  - *positions*: too few positions;
  - *turnover*: turnover too high.
- **Duplicates.** Rows with identical numbers (e.g. #32, #35, #38, #40) are different code
  producing the same trades under v3.

### A. The 85 unconfined strategies (the real ranking)

| rank | tier | # | strategy | family | mech. | v3 Sharpe | skill [90% CI] | vs basket | skill @2× cost | train skill | random %ile | gates failed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | #33 | `mom_zscore_overlap6_fixed_anchor` | cross-sectional momentum | M1 | 0.49 | +0.15 [−0.44, +0.65] | can't tell | +0.14 | −0.07 | 96 | train |
| 2 | 1 | #39 | `mom_zscore_overlap6_market_trim` | regime switching | M1 | 0.49 | +0.15 [−0.55, +0.76] | can't tell | +0.14 | −0.02 | 90 | train |
| 3 | 1 | #37 | `mom_zscore_overlap6_trim_universe` | cross-sectional momentum | M1 | 0.48 | +0.15 [−0.56, +0.73] | can't tell | +0.13 | −0.01 | 84 | train, random |
| 4 | 1 | #42 | `mom_zscore_overlap6_hzn_avg4` | cross-sectional momentum | M1 | 0.48 | +0.14 [−0.44, +0.61] | can't tell | +0.13 | −0.06 | 92 | train |
| 5 | 1 | #46 | `mom_hzn_avg4_k6_cohort_trim` | cross-sectional momentum | M1 | 0.48 | +0.14 [−0.44, +0.61] | can't tell | +0.13 | −0.06 | 92 | train |
| 6 | 1 | #34 | `mom_zscore_overlap6_live_tranche` | cross-sectional momentum | M1 | 0.47 | +0.14 [−0.62, +0.77] | can't tell | +0.11 | −0.09 | 96 | train |
| 7 | 1 | #32 | `mom_zscore_overlap6_daily_trim` | cross-sectional momentum | M1 | 0.47 | +0.13 [−0.54, +0.69] | can't tell | +0.12 | −0.08 | 90 | train |
| 8 | 1 | #35 | `mom_zscore_overlap6_daily_trim` | cross-sectional momentum | M1 | 0.47 | +0.13 [−0.54, +0.69] | can't tell | +0.12 | −0.08 | 90 | train |
| 9 | 1 | #38 | `mom_zscore_overlap6_notrim` | cross-sectional momentum | M1 | 0.47 | +0.13 [−0.54, +0.69] | can't tell | +0.12 | −0.08 | 90 | train |
| 10 | 1 | #40 | `mom_zscore_overlap6_legacy_trim` | regime switching | M1 | 0.47 | +0.13 [−0.54, +0.69] | can't tell | +0.12 | −0.08 | 90 | train |
| 11 | 1 | #41 | `mom_zscore_overlap6_hzn_avg` | cross-sectional momentum | M1 | 0.46 | +0.13 [−0.49, +0.62] | can't tell | +0.11 | −0.08 | 84 | train, random |
| 12 | 1 | #61 | `sl_ridge_nontrend_block` | statistical-learning | M2 | 0.46 | +0.12 [−0.22, +0.41] | can't tell | −0.05 | −0.10 | 98 | train |
| 13 | 1 | #36 | `mom_zscore_overlap6_ddbrake` | regime switching | M1 | 0.43 | +0.10 [−0.60, +0.70] | can't tell | +0.08 | −0.08 | 72 | train, random |
| 14 | 1 | #53 | `mom_hzn_avg4_noagree` | cross-sectional momentum | M1 | 0.43 | +0.09 [−0.47, +0.54] | can't tell | +0.02 | −0.12 | 98 | train |
| 15 | 1 | #50 | `mom_hzn_avg4_no_resize` | cross-sectional momentum | M1 | 0.41 | +0.07 [−0.50, +0.51] | can't tell | +0.04 | −0.13 | 82 | train, random |
| 16 | 1 | #22 | `mom_multihorizon_zscore_damped_buffered` | cross-sectional momentum | M1 | 0.41 | +0.07 [−0.53, +0.59] | can't tell | +0.02 | −0.06 | 88 | train, random |
| 17 | 1 | #65 | `pt_raw_reversal_control` | price-trend | M2 | 0.40 | +0.06 [−0.31, +0.37] | can't tell | −0.07 | −0.31 | 100 | train, drawdown |
| 18 | 1 | #47 | `mom_hzn_avg4_subsample_bag3` | combinations | M1 | 0.40 | +0.06 [−0.50, +0.50] | can't tell | −0.00 | −0.10 | 96 | train |
| 19 | 1 | #54 | `mom_hzn_avg4_rankweight` | cross-sectional momentum | M1 | 0.39 | +0.06 [−0.49, +0.51] | can't tell | −0.01 | −0.06 | 90 | train |
| 20 | 1 | #52 | `mom_hzn_avg4_equalweight` | cross-sectional momentum | M1 | 0.38 | +0.05 [−0.47, +0.47] | can't tell | −0.03 | −0.10 | 90 | train |
| 21 | 1 | #21 | `mom_multihorizon_zscore_buffered` | cross-sectional momentum | M1 | 0.38 | +0.04 [−0.62, +0.63] | can't tell | −0.00 | −0.05 | 78 | train, drawdown, random |
| 22 | 1 | #28 | `mom_zscore_narrow_daily_volspike_trim` | cross-sectional momentum | M1 | 0.38 | +0.04 [−0.62, +0.63] | can't tell | −0.00 | −0.05 | 78 | train, drawdown, random |
| 23 | 1 | #29 | `mom_zscore_volspike_hedge_redirect` | cross-sectional momentum | M1 | 0.38 | +0.04 [−0.62, +0.63] | can't tell | −0.00 | −0.05 | 78 | train, drawdown, random |
| 24 | 1 | #55 | `mom_hzn_disjoint4_overlap6` | cross-sectional momentum | M1 | 0.37 | +0.04 [−0.36, +0.34] | can't tell | +0.02 | −0.08 | 80 | train, random |
| 25 | 1 | #86 | `pt_depth_breadth_pinned` | price-trend | M1 | 0.37 | +0.04 [−0.50, +0.45] | can't tell | −0.03 | −0.11 | 96 | train |
| 26 | 1 | #85 | `pt_depth_vs_vintage_breadth` | price-trend | M1 | 0.37 | +0.04 [−0.52, +0.47] | can't tell | −0.03 | −0.10 | 84 | train, random |
| 27 | 1 | #43 | `mom_zscore_hzn_avg4_k1` | cross-sectional momentum | M1 | 0.37 | +0.03 [−0.58, +0.51] | can't tell | −0.03 | −0.08 | 86 | train, random |
| 28 | 1 | #45 | `mom_hzn_avg4_k1_cohort_trim` | regime switching | M1 | 0.37 | +0.03 [−0.58, +0.51] | can't tell | −0.03 | −0.08 | 86 | train, random |
| 29 | 1 | #12 | `str_reversal_monthly` | short-term mean reversion | M2 | 0.37 | +0.03 [−0.39, +0.37] | can't tell | −0.09 | −0.33 | 100 | train, drawdown |
| 30 | 1 | v2-3 | `sa_pca_resid_reversion` | statistical-arbitrage | M2 | 0.36 | +0.02 [−0.30, +0.30] | can't tell | −0.20 | −0.30 | 98 | train |
| 31 | 1 | #51 | `mom_hzn_avg4_nobuffer` | cross-sectional momentum | M1 | 0.36 | +0.02 [−0.60, +0.52] | can't tell | −0.04 | −0.08 | 82 | train, random |
| 32 | 1 | v2-1 | `pt_resid_reversal_v2` | price-trend | M2 | 0.35 | +0.02 [−0.32, +0.30] | can't tell | −0.13 | −0.30 | 100 | train, drawdown |
| 33 | 1 | v2-6 | `lv_resid_rev_illiq_tilt` | liquidity-volume | M2 | 0.34 | +0.01 [−0.37, +0.31] | can't tell | −0.26 | −0.24 | 100 | train |
| 34 | 1 | #44 | `mom_zscore_hzn_geom4_k1` | cross-sectional momentum | M1 | 0.34 | +0.01 [−0.59, +0.48] | can't tell | −0.06 | −0.05 | 88 | train, random |
| 35 | 1 | #24 | `mom_multihorizon_zscore_widebreadth` | cross-sectional momentum | M1 | 0.34 | +0.00 [−0.62, +0.53] | can't tell | −0.05 | −0.08 | 76 | train, random |
| 36 | 1 | #25 | `mom_zscore_volspike_trim` | cross-sectional momentum | M1 | 0.34 | +0.00 [−0.62, +0.53] | can't tell | −0.05 | −0.08 | 76 | train, random |
| 37 | 1 | #26 | `mom_zscore_daily_volspike_trim` | cross-sectional momentum | M1 | 0.34 | +0.00 [−0.62, +0.53] | can't tell | −0.05 | −0.08 | 76 | train, random |
| 38 | 1 | #27 | `mom_zscore_daily_volspike_trim_fixed` | cross-sectional momentum | M1 | 0.34 | +0.00 [−0.62, +0.53] | can't tell | −0.05 | −0.08 | 76 | train, random |
| 39 | 1 | #20 | `mom_zscore_weighted_buffered` | cross-sectional momentum | M1 | 0.34 | +0.00 [−0.71, +0.61] | can't tell | −0.04 | −0.15 | 58 | train, random |
| 40 | 1 | #94 | `lv_overnight_sentiment_reversal` | liquidity-volume | M7 | 0.34 | +0.00 [−0.25, +0.22] | can't tell | −0.02 | −0.15 | 82 | train, random |
| 41 | 1 | #64 | `lv_trading_time_reversal` | liquidity-volume | M2 | 0.33 | −0.01 [−0.41, +0.31] | can't tell | −0.13 | −0.29 | 100 | train, drawdown |
| 42 | 1 | #16 | `mom_str_reversal_buffered` | combinations | M1 | 0.33 | −0.01 [−0.50, +0.37] | can't tell | −0.08 | −0.13 | 82 | train, random |
| 43 | 1 | #73 | `pl_2leg_content_partner` | portfolio-learning | M2 | 0.33 | −0.01 [−0.30, +0.27] | can't tell | −0.17 | −0.28 | 100 | train, drawdown |
| 44 | 1 | #19 | `mom_rankweighted_buffered` | cross-sectional momentum | M1 | 0.32 | −0.02 [−0.66, +0.52] | can't tell | −0.07 | −0.11 | 50 | train, random |
| 45 | 1 | #15 | `mom_str_reversal_composite` | combinations | M1 | 0.31 | −0.02 [−0.61, +0.47] | can't tell | −0.09 | −0.13 | 52 | train, random |
| 46 | 1 | v3-1 | `pt_lowvol_gk_quarterly` | price-trend | M1 | 0.30 | −0.03 [−0.26, +0.21] | can't tell | −0.05 | −0.06 | 60 | train, random |
| 47 | 1 | #14 | `mom_str_reversal_blend` | combinations | M1 | 0.30 | −0.04 [−0.55, +0.35] | can't tell | −0.12 | −0.14 | 76 | train, random |
| 48 | 1 | #48 | `mom_hzn_avg4_phase4` | combinations | M1 | 0.29 | −0.05 [−0.65, +0.43] | can't tell | −0.11 | −0.09 | 80 | train, drawdown, random |
| 49 | 1 | #10 | `mom_etf_volweighted_blend` | combinations | M1 | 0.29 | −0.05 [−0.50, +0.32] | can't tell | −0.08 | −0.07 | 30 | train, random |
| 50 | 1 | #3 | `ew_global_etf` | volatility targeting / risk parity | M1 | 0.29 | −0.05 [−0.47, +0.30] | can't tell | −0.05 | +0.04 | 26 | random |
| 51 | 1 | v3-3 | `lv_illiq_peer_neutral_band` | liquidity-volume | M9 | 0.28 | −0.05 [−0.27, +0.15] | can't tell | −0.06 | +0.08 | 0 | drawdown, random |
| 52 | 1 | #18 | `mom_buffered_etf_blend` | combinations | M1 | 0.28 | −0.06 [−0.65, +0.40] | can't tell | −0.10 | −0.07 | 38 | train, random |
| 53 | 1 | #17 | `mom_12m_buffered` | cross-sectional momentum | M1 | 0.27 | −0.07 [−0.69, +0.43] | can't tell | −0.11 | −0.08 | 32 | train, random |
| 54 | 1 | #30 | `mom_12m_daily_volspike_trim` | cross-sectional momentum | M1 | 0.27 | −0.07 [−0.69, +0.43] | can't tell | −0.11 | −0.08 | 32 | train, random |
| 55 | 1 | #9 | `mom_etf_blend` | combinations | M1 | 0.24 | −0.10 [−0.70, +0.39] | can't tell | −0.14 | −0.09 | 34 | train, random |
| 56 | 1 | #49 | `mom_hzn_avg4_weekly_resize` | cross-sectional momentum | M1 | 0.24 | −0.10 [−0.69, +0.38] | can't tell | −0.22 | −0.13 | 86 | train, drawdown, random |
| 57 | 1 | #95 | `rv_sleeve_voltarget_phi05` | range-variance | M1 | 0.24 | −0.10 [−0.33, +0.13] | can't tell | −0.11 | −0.19 | 0 | train, random |
| 58 | 1 | #1 | `mom_12m_baseline` | cross-sectional momentum | M1 | 0.23 | −0.11 [−0.74, +0.41] | can't tell | −0.16 | −0.10 | 36 | train, drawdown, random |
| 59 | 1 | #93 | `pl_factor_momentum_untimed` | portfolio-learning | M6 | 0.23 | −0.11 [−0.33, +0.05] | can't tell | −0.21 | −0.10 | 100 | train |
| 60 | 1 | v3-2 | `sa_resid_rev63_band` | statistical-arbitrage | M2 | 0.22 | −0.12 [−0.32, +0.04] | can't tell | −0.23 | −0.00 | 76 | train, random |
| 61 | 1 | #5 | `gtaa_trend_diversified` | time-series momentum / trend following | M1 | 0.21 | −0.13 [−0.71, +0.39] | can't tell | −0.20 | +0.06 | 14 | random |
| 62 | 1 | v2-5 | `sl_ridge_six_masked` | statistical-learning | M2 | 0.19 | −0.15 [−0.45, +0.13] | can't tell | −0.28 | −0.54 | 62 | train, drawdown, random |
| 63 | 1 | #100 | `rv_minvar_equalweight` | range-variance | M1 | 0.17 | −0.17 [−0.55, +0.18] | can't tell | −0.23 | −0.20 | 4 | train, random |
| 64 | 1 | #74 | `pl_2leg_null_partner` | portfolio-learning | M2 | 0.16 | −0.17 [−0.46, +0.05] | can't tell | −0.38 | −0.20 | 84 | train, random |
| 65 | 1 | #2 | `gtaa_trend_etf` | time-series momentum / trend following | M1 | 0.14 | −0.20 [−0.86, +0.37] | can't tell | −0.25 | −0.06 | 24 | train, positions, random |
| 66 | 1 | #66 | `pt_fast_reversal_slow_grid` | price-trend | M2 | 0.12 | −0.22 [−0.52, +0.11] | can't tell | −0.35 | −0.12 | 68 | train, drawdown, random |
| 67 | 1 | #91 | `rv_volofvol_top15` | range-variance | M5 | 0.12 | −0.22 [−0.72, +0.16] | can't tell | −0.26 | −0.10 | 6 | train, random |
| 68 | 1 | #56 | `sl_ridge_xs_walkforward` | statistical-learning | M2 | 0.11 | −0.22 [−0.62, +0.13] | can't tell | −0.34 | −0.30 | 26 | train, drawdown, random |
| 69 | 1 | #31 | `mom_52wkhigh_zscore_buffered` | cross-sectional momentum | M1 | 0.11 | −0.23 [−0.73, +0.22] | can't tell | −0.45 | −0.18 | 72 | train, random |
| 70 | 1 | v2-2 | `pt_resid_reversal_band` | price-trend | M2 | 0.11 | −0.23 [−0.46, −0.03] | worse | −0.43 | −0.18 | 66 | train, random |
| 71 | 1 | #63 | `sa_pca_residual_excursion` | statistical-arbitrage | M4 | 0.09 | −0.24 [−0.38, −0.12] | worse | −0.43 | −0.08 | 24 | train, random |
| 72 | 1 | #8 | `risk_parity_multi_asset` | volatility targeting / risk parity | M1 | 0.09 | −0.25 [−0.72, +0.19] | can't tell | −0.26 | +0.16 | 10 | random |
| 73 | 1 | #13 | `mom_lowvol_doublesort` | low-volatility / quality tilts | M1 | 0.07 | −0.26 [−0.84, +0.26] | can't tell | −0.39 | −0.11 | 4 | train, random |
| 74 | 1 | #75 | `pl_2leg_placebo_partner` | portfolio-learning | M1 | 0.07 | −0.27 [−0.59, −0.00] | worse | −0.49 | −0.25 | 54 | train, random |
| 75 | 1 | #6 | `lowvol_equity_tilt` | low-volatility / quality tilts | M1 | 0.03 | −0.30 [−0.84, +0.21] | can't tell | −0.40 | −0.01 | 28 | train, random |
| 76 | 1 | #101 | `ll_peer_momentum` | lead-lag-spillover | M8 | 0.03 | −0.30 [−0.94, +0.26] | can't tell | −0.47 | −0.28 | 36 | train, drawdown, random |
| 77 | 1 | #11 | `str_reversal_stocks` | short-term mean reversion | M2 | 0.02 | −0.32 [−0.83, +0.12] | can't tell | −0.87 | −0.41 | 100 | train, drawdown, turnover |
| 78 | 1 | #4 | `mom_invvol_target` | cross-sectional momentum | M1 | 0.01 | −0.33 [−0.91, +0.22] | can't tell | −0.39 | −0.09 | 12 | train, random |
| 79 | 1 | #102 | `ll_peer_momentum_evargate` | lead-lag-spillover | M8 | -0.02 | −0.36 [−1.03, +0.22] | can't tell | −0.50 | −0.36 | 8 | train, drawdown, random |
| 80 | 1 | #92 | `pl_factor_momentum_timed` | portfolio-learning | M6 | -0.05 | −0.39 [−0.70, −0.16] | worse | −0.52 | −0.09 | 58 | train, random |
| 81 | 1 | #59 | `sc_same_month_seasonal` | seasonality-calendar | M1 | -0.06 | −0.39 [−0.78, −0.10] | worse | −0.55 | −0.31 | 22 | train, random |
| 82 | 1 | #7 | `mom_regime_filtered` | regime switching | M1 | -0.10 | −0.44 [−1.18, +0.23] | can't tell | −0.52 | +0.19 | 0 | random |
| 83 | 1 | #57 | `lv_amihud_illiquidity_tilt` | liquidity-volume | M3 | -0.13 | −0.47 [−0.90, −0.13] | worse | −0.52 | −0.08 | 28 | train, random |
| 84 | 1 | #60 | `sc_same_month_seasonal_aligned` | seasonality-calendar | M1 | -0.14 | −0.48 [−0.91, −0.14] | worse | −0.69 | −0.21 | 12 | train, random |
| 85 | 1 | #99 | `rv_minvar_closedform` | range-variance | M1 | -0.26 | −0.60 [−1.31, +0.00] | can't tell | −0.64 | −0.33 | 0 | train, random |

### B. The 27 confined strategies

These could only pick from today's surviving large caps, so every number below is
survivorship-biased. They are ranked among themselves only. Tiers and mechanisms are left out
because the confidence set is not meaningful for a hindsight-limited list.

| rank | # | strategy | family | v3 Sharpe | skill [90% CI] | vs basket | skill @2× cost | train skill | random %ile | gates failed |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | #79 | `pl_union_region_relative_illiq` | portfolio-learning | 0.68 | +0.34 [+0.08, +0.59] | better | +0.24 | −0.09 | 100 | train |
| 2 | #71 | `pl_fixed_share_tails` | portfolio-learning | 0.62 | +0.28 [+0.03, +0.52] | better | +0.18 | −0.09 | 100 | train |
| 3 | #68 | `pl_maxleg_signal_blend` | portfolio-learning | 0.61 | +0.28 [−0.07, +0.58] | can't tell | +0.14 | −0.09 | 100 | train |
| 4 | #77 | `pl_zeroleg_all_placebo` | portfolio-learning | 0.60 | +0.27 [+0.02, +0.48] | better | +0.18 | −0.18 | 100 | train |
| 5 | #87 | `sc_seasonal_depth_narrow` | seasonality-calendar | 0.60 | +0.26 [−0.11, +0.64] | can't tell | +0.12 | −0.02 | 100 | train |
| 6 | #76 | `pl_3leg_ladder_rung` | portfolio-learning | 0.55 | +0.21 [−0.13, +0.49] | can't tell | +0.12 | +0.00 | 100 | train |
| 7 | #58 | `ll_group_lastmonth_lead` | lead-lag-spillover | 0.55 | +0.21 [−0.16, +0.52] | can't tell | +0.09 | −0.04 | 100 | train |
| 8 | #69 | `pl_maxleg_rank_control` | portfolio-learning | 0.55 | +0.21 [−0.16, +0.54] | can't tell | +0.07 | −0.09 | 100 | train |
| 9 | #23 | `mom_multihorizon_zscore_sectorneutral` | cross-sectional momentum | 0.53 | +0.19 [−0.38, +0.63] | can't tell | +0.14 | +0.07 | 92 | passes all |
| 10 | #72 | `sc_seasonal_matched_control` | seasonality-calendar | 0.52 | +0.18 [−0.10, +0.48] | can't tell | +0.04 | −0.04 | 100 | train |
| 11 | #70 | `pl_second_best_leg` | portfolio-learning | 0.50 | +0.16 [−0.11, +0.42] | can't tell | +0.03 | −0.05 | 100 | train |
| 12 | #83 | `pl_signal_intersection` | portfolio-learning | 0.46 | +0.12 [−0.33, +0.60] | can't tell | +0.14 | −0.19 | 68 | train, drawdown, random |
| 13 | #62 | `ll_group_laggard_diffusion` | lead-lag-spillover | 0.44 | +0.10 [−0.26, +0.41] | can't tell | −0.06 | −0.11 | 100 | train |
| 14 | #88 | `sc_seasonal_depth_wide` | seasonality-calendar | 0.37 | +0.03 [−0.21, +0.28] | can't tell | −0.10 | −0.11 | 100 | train |
| 15 | #97 | `lv_illiq_evar_signflip` | liquidity-volume | 0.35 | +0.01 [−0.31, +0.31] | can't tell | +0.00 | +0.03 | 12 | drawdown, random |
| 16 | #67 | `pl_integrated_signal_blend` | portfolio-learning | 0.30 | −0.04 [−0.28, +0.18] | can't tell | −0.15 | −0.05 | 100 | train |
| 17 | #98 | `pt_mom_evar_arbrisk` | price-trend | 0.19 | −0.14 [−0.69, +0.27] | can't tell | −0.17 | −0.01 | 20 | train, random |
| 18 | #103 | `pt_mom_seasonal_deferral` | price-trend | 0.19 | −0.14 [−0.68, +0.26] | can't tell | −0.17 | −0.00 | 20 | train, random |
| 19 | #89 | `lv_illiq_stocks_only` | liquidity-volume | 0.17 | −0.17 [−0.46, +0.07] | can't tell | −0.20 | +0.05 | 12 | drawdown, random |
| 20 | #104 | `pt_mom_id_z` | price-trend | 0.16 | −0.18 [−0.73, +0.23] | can't tell | −0.20 | −0.01 | 6 | train, random |
| 21 | #82 | `lv_illiq_region_wide30` | liquidity-volume | 0.16 | −0.18 [−0.48, +0.06] | can't tell | −0.22 | +0.03 | 24 | random |
| 22 | #78 | `lv_illiq_region_relative` | liquidity-volume | 0.11 | −0.23 [−0.57, +0.05] | can't tell | −0.27 | +0.03 | 14 | random |
| 23 | #84 | `pl_intersection_fixed_breadth` | portfolio-learning | 0.10 | −0.24 [−0.74, +0.16] | can't tell | −0.33 | +0.02 | 6 | random |
| 24 | #80 | `lv_illiq_region_tail10` | liquidity-volume | 0.06 | −0.27 [−0.62, +0.03] | can't tell | −0.32 | +0.01 | 24 | drawdown, random |
| 25 | #81 | `lv_illiq_region_rankweight` | liquidity-volume | 0.04 | −0.30 [−0.62, −0.03] | worse | −0.35 | +0.01 | 16 | drawdown, random |
| 26 | #90 | `sl_ppp_walkforward` | statistical-learning | 0.10 | −0.24 [−0.37, −0.11] | worse | −0.39 | −0.23 | 2 | train, random |
| 27 | #96 | `lv_illiq_evar_riskcost` | liquidity-volume | -0.10 | −0.44 [−0.76, −0.20] | worse | −0.48 | +0.11 | 0 | random |

### C. Reference rows

The 8 ported v1 champions and the 3 sanity strategies are not trials. Their numbers are in the
"Ported v1 champions" and "Sanity checks" tables above.

