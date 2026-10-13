# Protocol v3 re-scoring — every strategy, with the T-bill rate (2026-10-13)

> **What this is.** A re-scoring, not new research. Every strategy the lab has recorded was re-run
> under **protocol v3**: 104 under v1, 6 under v2 (5 scored), and 2 under v3. The eight ported v1
> champions and three sanity strategies were re-run too.
> It supersedes the W41 re-scoring (`reports/2026-W41.md`), which ran before the cash-rate series
> was in the store and so paid 0% on cash and measured Sharpe on raw returns. This run uses the
> stored 13-week T-bill rate (`RATE_US3M`, 1.82%/yr on average over validation) and today's
> membership store, after PR #9.
>
> Train and validation only: **no holdout data was read**, and nothing was added to
> `experiments/trials.jsonl`, so no deflated bar moved.
> - Harness: `scripts/rescore_protocol_v3.py`, unchanged; 122 rows, 0 errors.
> - Raw rows: `experiments/protocol_v3/rescore.jsonl`.
> - Validation returns: `experiments/protocol_v3/returns/`.
> - **Check:** the two v3 trials reproduce their recorded validation Sharpe and skill exactly
>   (0.304 / −0.033 and 0.218 / −0.119).

**TL;DR.** The T-bill rate changes the levels and not the verdict. **No unconfined strategy shows
skill it can prove.** "Skill" means Sharpe minus that of an equal-weight basket of every eligible
stock, both measured in excess of T-bills.

- **The basket's Sharpe fell from 0.45 to 0.34.** Its own excess return is paying for cash now,
  and it is less volatile than most of the books measured against it. That lifted the median
  trial's skill by +0.04. The lift is not evidence of skill.
- **Unconfined trials (84).** None has a 90% skill interval above zero. 39 have positive point
  skill. The best is +0.16, with an interval about ±0.6 wide. The best deflated-skill
  probability is **0.26** against a bar of **0.95**.
- **All 84 sit in tier 1.** The data cannot separate any of them from the best. 61 of them are
  one mechanism (momentum).
- **Train gate.** Only **4** unconfined trials beat the basket on train (1997–2017). All four are
  ETF allocation books, and all four have negative validation skill. **No unconfined
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
  - train skill not above zero: 98 of 111 scored trials;
  - not beating 90% of random books built like it: 73;
  - validation drawdown worse than −45%: 22;
  - one trial each for too few positions and too much turnover.
- **One real trial clears every gate:** #23, which is confined.
- **The v1 record still does not predict v3.** Rank agreement between v1's recorded validation
  Sharpe and v3 is +0.46. The median recorded Sharpe was 0.87; under v3 it is 0.33.

## Strategy leaderboard (v3, unconfined, with error bars)

**Every one of the 84 unconfined trials is in tier 1.** The 10% model confidence set cannot
separate any of them from the best, so the order below is not evidence. Ranking comes from
`engine.ranking.rank_table` over the re-scored validation returns, the same method as
`scripts/rank_trials.py`.

**Column notes:**
- "Mech." groups trials whose returns in excess of the basket correlate at 0.5 or more; trials
  in one mechanism are one bet.
- "DSR" is the deflated-skill probability. It is illustrative: it uses the re-scored skills and
  standard errors against the v3 deflator, with 111 recorded trials across all versions and
  **38 effective**. A seat needs 0.95.
- "Random %ile" is where the trial's Sharpe sits among random books built like it (50 draws).

**The 15 unconfined trials with the highest skill:**

| tier | # | strategy | family | skill [90% CI] | skill @2× cost | train skill | random %ile | DSR | mech. | what it does |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 33 | `mom_zscore_overlap6_fixed_anchor` | cross-sectional momentum | +0.16 [−0.44, +0.65] | +0.14 | −0.07 | 96 | 0.22 | M1 | Recent winners, one-sixth of the book rebuilt each month, sizing each stock against a fixed yardstick. |
| 1 | 39 | `mom_zscore_overlap6_market_trim` | regime switching | +0.16 [−0.55, +0.76] | +0.14 | −0.02 | 90 | 0.26 | M1 | The six-month blend, with the safety cut-back triggered by the whole market's swings. |
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
| regime switching | 5 | +0.10 | +0.16 | 0.43 | 1.05 | M1 |
| cross-sectional momentum | 33 | +0.04 | +0.16 | 0.38 | 1.05 | M1 |
| price-trend | 7 | +0.02 | +0.06 | 0.35 | 0.65 | M1, M2 |
| liquidity-volume | 4 | −0.00 | +0.01 | 0.33 | 0.68 | M2, M3, M7 |
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

**15 family labels, 8 mechanisms.**
- **M1** (momentum, plus the ETF and blend books that move with it) holds 61 trials, with median
  skill +0.00.
- **M2** (short-term and residual reversal) holds 15, with median skill −0.01.
- **The other six** mechanisms hold one or two trials each. Their best skill is +0.00 (#94's overnight-sentiment
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
   an interval above zero. The best deflated-skill probability is 0.26 against 0.95, with 38
   effective trials searched in this window.
2. **Train skill is the binding constraint, not validation.** 98 of 111 trials fail the train
   gate. The four unconfined trials that pass it are ETF allocation books, and all four lose to
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
