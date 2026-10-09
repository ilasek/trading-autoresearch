# Strategy summaries

A plain-English line for every strategy the lab has tested, in trial order. The weekly
leaderboards quote these lines. When a new strategy is tested, add its row here: one or two
sentences on what it buys and why, written for a reader with no finance training.

Two phrases recur, because many strategies build on earlier ones:

- **"Recent winners"**: buy the stocks that rose most over the past year, ignoring the
  latest month (which tends to reverse), and refresh the list monthly.
- **"Safety cut-back"**: shrink the whole position to 60% while recent price swings are far
  above normal, and return to full size once they calm down.

| # | strategy | family | what it does |
|---|---|---|---|
| 1 | `mom_12m_baseline` | cross-sectional momentum | Each month, buys the 15 stocks that rose most over the past year (ignoring the latest month), betting that winners keep winning. |
| 2 | `gtaa_trend_etf` | time-series momentum / trend following | Holds a spread of stock, bond and commodity funds, but swaps any fund trading below its 200-day average price into government bonds. |
| 3 | `ew_global_etf` | volatility targeting / risk parity | Holds equal amounts of a fixed set of global stock, bond, commodity and emerging-market funds, and never changes the mix. |
| 4 | `mom_invvol_target` | cross-sectional momentum | Recent winners, but with less money in the jumpiest stocks, and the whole position is scaled down when the portfolio gets too bumpy. |
| 5 | `gtaa_trend_diversified` | time-series momentum / trend following | Equal amounts across many types of fund; any fund below its 200-day average price is swapped into a mix of bond funds. |
| 6 | `lowvol_equity_tilt` | low-volatility / quality tilts | Buys the stocks whose prices have moved around the least over the past six months, betting calm stocks pay more per unit of risk. |
| 7 | `mom_regime_filtered` | regime switching | Recent winners, but moves entirely into bonds whenever the US stock market is below its 200-day average. |
| 8 | `risk_parity_multi_asset` | volatility targeting / risk parity | Spreads money across fund types so each adds about the same amount of risk (less money in the jumpier ones). |
| 9 | `mom_etf_blend` | combinations | 80% in recent winners and 20% in a fixed mix of diversified funds, to soften the winners' sharp crashes. |
| 10 | `mom_etf_volweighted_blend` | combinations | Splits money between recent winners and a fixed fund mix, shifting toward the funds whenever the winners get bumpy. |
| 11 | `str_reversal_stocks` | short-term mean reversion | Each week, buys the stocks that fell most over the past week, betting short-term drops bounce back. |
| 12 | `str_reversal_monthly` | short-term mean reversion | Each month, buys the stocks that fell most over the past month, betting they bounce back. |
| 13 | `mom_lowvol_doublesort` | low-volatility / quality tilts | Among the past year's best performers, buys only the calmest, to avoid the winners most likely to crash. |
| 14 | `mom_str_reversal_blend` | combinations | 80% in last year's biggest winners and 20% in last month's biggest losers: two bets that tend to pay at different times. |
| 15 | `mom_str_reversal_composite` | combinations | Scores each stock mostly on its past-year gain and partly on its last-month drop, and buys the top 15 of that single list. |
| 16 | `mom_str_reversal_buffered` | combinations | The 80/20 winners-plus-bounce-back mix, but a stock already held is kept until it slips well down the ranking, to cut trading. |
| 17 | `mom_12m_buffered` | cross-sectional momentum | Recent winners, but a stock already held is kept until it drops out of the top 25 rather than the top 15, which cuts needless trading. |
| 18 | `mom_buffered_etf_blend` | combinations | 80% in the low-trading winners basket and 20% in a fixed mix of diversified funds. |
| 19 | `mom_rankweighted_buffered` | cross-sectional momentum | The low-trading winners basket, putting more money in the higher-ranked stocks and less in the lower-ranked. |
| 20 | `mom_zscore_weighted_buffered` | cross-sectional momentum | The low-trading winners basket, sizing each stock by how far its gain stands out from the crowd, not just its place in line. |
| 21 | `mom_multihorizon_zscore_buffered` | cross-sectional momentum | Recent winners, sized by how far each stock's gain stands out, judged on 6-month and 12-month gains together so no single time window decides. |
| 22 | `mom_multihorizon_zscore_damped_buffered` | cross-sectional momentum | The two-window winners basket, with the gap between big and small positions softened so no stock takes too large a slice. |
| 23 | `mom_multihorizon_zscore_sectorneutral` | cross-sectional momentum | The two-window winners basket, but compares each stock only with its own industry so no single sector dominates. |
| 24 | `mom_multihorizon_zscore_widebreadth` | cross-sectional momentum | The two-window winners basket, but holding more stocks (about 20–35 instead of 15–25) to spread the risk. |
| 25 | `mom_zscore_volspike_trim` | cross-sectional momentum | The wider winners basket plus the safety cut-back, triggered by the basket's own swings and checked once a month. |
| 26 | `mom_zscore_daily_volspike_trim` | cross-sectional momentum | Recent winners with the safety cut-back checked every day, so it can react to a crash within days instead of weeks. (A bug kept stocks it meant to sell in the book; see #27.) |
| 27 | `mom_zscore_daily_volspike_trim_fixed` | cross-sectional momentum | Recent winners with the safety cut-back checked daily: a corrected re-run of #26, which had a bug. |
| 28 | `mom_zscore_narrow_daily_volspike_trim` | cross-sectional momentum | The daily safety cut-back applied to the narrower 15–25-stock winners basket. |
| 29 | `mom_zscore_volspike_hedge_redirect` | cross-sectional momentum | When the safety cut-back kicks in, the freed money goes into long-term government bonds and gold instead of sitting in cash. |
| 30 | `mom_12m_daily_volspike_trim` | cross-sectional momentum | The plain, equal-sized recent-winners basket with the daily safety cut-back added. |
| 31 | `mom_52wkhigh_zscore_buffered` | cross-sectional momentum | Picks the stocks trading closest to their highest price of the past year, instead of those with the biggest gains. |
| 32, 35 | `mom_zscore_overlap6_daily_trim` | cross-sectional momentum | Recent winners, but only one-sixth of the portfolio is rebuilt each month, so it blends picks from the last six months and trades less. (Run twice; the second run was promoted.) |
| 33 | `mom_zscore_overlap6_fixed_anchor` | cross-sectional momentum | The six-month blend, sizing each stock against a fixed yardstick so positions don't all shift just because the weakest holding changed. |
| 34 | `mom_zscore_overlap6_live_tranche` | cross-sectional momentum | The six-month blend, but older picks that the latest ranking no longer likes are dropped and their money goes to names still in favour. |
| 36 | `mom_zscore_overlap6_ddbrake` | regime switching | Adds a second brake: drop to 60% once the portfolio is 20% below its peak, and return to full size after it recovers to within 10%. |
| 37 | `mom_zscore_overlap6_trim_universe` | cross-sectional momentum | Fixes the safety cut-back to watch the swings of every stock actually held, not just the few with very long price histories. |
| 38 | `mom_zscore_overlap6_notrim` | cross-sectional momentum | The six-month blend with the safety cut-back removed entirely, to test whether it was doing any real work. |
| 39 | `mom_zscore_overlap6_market_trim` | regime switching | Triggers the safety cut-back from the swings of the whole market rather than the portfolio's own. |
| 40 | `mom_zscore_overlap6_legacy_trim` | regime switching | Triggers the safety cut-back from the swings of the long-established stocks, whether held or not. |
| 41 | `mom_zscore_overlap6_hzn_avg` | cross-sectional momentum | Builds two separate winners portfolios, one judged on 12-month gains and one on 6-month gains, and holds half of each. |
| 42 | `mom_zscore_overlap6_hzn_avg4` | cross-sectional momentum | Builds four winners portfolios, judged on gains over 12, 9, 6 and 3 months, and holds a quarter of each, blended over six months, with the safety cut-back. |
| 43 | `mom_zscore_hzn_avg4_k1` | cross-sectional momentum | The four-window winners portfolio, rebuilt in full every month instead of one-sixth at a time. |
| 44 | `mom_zscore_hzn_geom4_k1` | cross-sectional momentum | The four-window portfolio with the windows spaced 12, 7.5, 5 and 3 months, so each is a similar step shorter than the last. |
| 45 | `mom_hzn_avg4_k1_cohort_trim` | regime switching | The four-window portfolio with the safety cut-back driven by the swings of all long-established stocks, not just the few it holds. |
| 46 | `mom_hzn_avg4_k6_cohort_trim` | cross-sectional momentum | Like #45 (four-window winners, market-wide safety cut-back), but with the six-month blending of monthly picks switched back on. |
| 47 | `mom_hzn_avg4_subsample_bag3` | combinations | Runs the four-window strategy three times, each time hiding a different third of the stocks, and holds the average of the three. |
| 48 | `mom_hzn_avg4_phase4` | combinations | Runs the four-window strategy four times, rebalancing on different days of the month (1st, 8th, 15th, 22nd), and holds the average. |
| 49 | `mom_hzn_avg4_weekly_resize` | cross-sectional momentum | Resets position sizes to the latest scores every week, instead of letting them drift with prices for a month. |
| 50 | `mom_hzn_avg4_no_resize` | cross-sectional momentum | Never resizes a stock it already holds; it grows or shrinks with its price, and only new arrivals are sized fresh. |
| 51 | `mom_hzn_avg4_nobuffer` | cross-sectional momentum | Four-window winners, but each of the four portfolios simply holds its current top 15, with no "keep until it drops to 25" rule. |
| 52 | `mom_hzn_avg4_equalweight` | cross-sectional momentum | Four-window winners with equal money in every chosen stock, instead of more money in the strongest. |
| 53 | `mom_hzn_avg4_noagree` | cross-sectional momentum | Four-window winners without the extra money for stocks that several of the four windows pick at once. |
| 54 | `mom_hzn_avg4_rankweight` | cross-sectional momentum | Four-window winners, sized by place in the ranking (1st gets most) rather than by how far each stock stands out. |
| 55 | `mom_hzn_disjoint4_overlap6` | cross-sectional momentum | Judges winners on four separate, non-overlapping quarters of the past year instead of four nested windows. |
| 56 | `sl_ridge_xs_walkforward` | statistical-learning | A simple statistical model, retrained monthly on past data only, combines 11 price and trading-volume clues to pick the 20 stocks it expects to do best next month. |
| 57 | `lv_amihud_illiquidity_tilt` | liquidity-volume | Buys the 20 stocks that are hardest to trade (their price moves most per dollar traded), betting investors are paid extra for holding them. |
| 58 | `ll_group_lastmonth_lead` | lead-lag-spillover | Buys every stock in the three industry groups that rose most last month, betting a whole group's recent rise carries on. |
| 59 | `sc_same_month_seasonal` | seasonality-calendar | Buys the 25 stocks that have historically done best in the calendar month about to start, compared with their other months. |
| 60 | `sc_same_month_seasonal_aligned` | seasonality-calendar | A corrected re-run of the calendar-month idea: the first attempt sometimes looked up the month that had just ended instead of the one about to start. |
| 61 | `sl_ridge_nontrend_block` | statistical-learning | A simple statistical model, retrained monthly on past data only, fed four clues that ignore past-year trends: calendar month, ease of trading, unusual volume and last month's drop. |
| 62 | `ll_group_laggard_diffusion` | lead-lag-spillover | Within the three hottest industry groups, buys only the stocks that haven't caught up yet, betting they follow their group up. |
| 63 | `sa_pca_residual_excursion` | statistical-arbitrage | Buys stocks that have drifted unusually far below where similar stocks say they should be, and sells once they snap back. |
| 64 | `lv_trading_time_reversal` | liquidity-volume | Buys last month's losers, counting price drops on quiet days more heavily than drops on heavy-volume days. |
| 65 | `pt_raw_reversal_control` | price-trend | A comparison test: buys last month's biggest losers with no volume adjustment, to check whether #64's adjustment is what helped. |
| 66 | `pt_fast_reversal_slow_grid` | price-trend | Buys last week's biggest losers, but only trades once a month to keep costs down. |
| 67 | `pl_integrated_signal_blend` | portfolio-learning | Averages four unrelated stock scores (hard to trade, good calendar month, hot industry, last month's drop) and buys the top of the combined list. |
| 68 | `pl_maxleg_signal_blend` | portfolio-learning | Uses the same four scores, but ranks each stock by its single strongest one, so a stock that stands out on any one idea gets bought. |
| 69 | `pl_maxleg_rank_control` | portfolio-learning | Like #68 (buy a stock if any one of four scores is very strong), but comparing ranks rather than raw scores, to check the result isn't a scaling quirk. |
| 70 | `pl_second_best_leg` | portfolio-learning | Ranks each stock by its second-strongest of the four scores, to test whether one standout score is what matters. |
| 71 | `pl_fixed_share_tails` | portfolio-learning | Buys the top 5 stocks from each of the four scores, a fixed quarter of the book per idea. |
| 72 | `sc_seasonal_matched_control` | seasonality-calendar | A comparison test: the calendar-month score alone, built exactly like the four-score books, to see how much the other three add. |
| 73 | `pl_2leg_content_partner` | portfolio-learning | The top 10 by calendar-month score plus the top 10 of last month's losers. |
| 74 | `pl_2leg_null_partner` | portfolio-learning | The top 10 by calendar-month score plus the top 10 by unusual trading volume, a score that predicts nothing on its own. |
| 75 | `pl_2leg_placebo_partner` | portfolio-learning | The top 10 by calendar-month score plus 10 stocks chosen by a fixed random draw, to test whether the second half needs any real idea. |
| 76 | `pl_3leg_ladder_rung` | portfolio-learning | The top 6 stocks from each of three scores: calendar month, hard to trade, and hot industry. |
| 77 | `pl_zeroleg_all_placebo` | portfolio-learning | A comparison test: the four-score book of #71 with every score replaced by a random draw, to measure what the setup earns with no real idea at all. |
| 78 | `lv_illiq_region_relative` | liquidity-volume | Buys the hardest-to-trade stocks, judged against others from the same region so that differences between stock exchanges don't count. |
| 79 | `pl_union_region_relative_illiq` | portfolio-learning | The top 5 stocks from each of four scores (#71), with its hard-to-trade score swapped for the region-adjusted version (#78). |
| 80 | `lv_illiq_region_tail10` | liquidity-volume | The region-adjusted hard-to-trade book, holding only the 10 most extreme stocks instead of 20. |
| 81 | `lv_illiq_region_rankweight` | liquidity-volume | The region-adjusted hard-to-trade book, with more money in the higher-ranked stocks. |
| 82 | `lv_illiq_region_wide30` | liquidity-volume | The region-adjusted hard-to-trade book, holding about 30–45 stocks instead of 20–30 to spread the risk. |
| 83 | `pl_signal_intersection` | portfolio-learning | Buys only stocks that are both recent winners and hard to trade, scoring in the top third on each. |
| 84 | `pl_intersection_fixed_breadth` | portfolio-learning | The winners-and-hard-to-trade overlap, with the cut-offs adjusted so the book always holds about 14 stocks. |
| 85 | `pt_depth_vs_vintage_breadth` | price-trend | Gets the champion's number of holdings by going further down one fresh winners list, instead of blending lists from different months. |
| 86 | `pt_depth_breadth_pinned` | price-trend | Like #85 (one fresh winners list, read deeper), re-tuned so the holding count matches the champion's in the period that is scored. |
| 87 | `sc_seasonal_depth_narrow` | seasonality-calendar | The calendar-month book, holding only the 10–15 strongest stocks instead of 20–30. |
| 88 | `sc_seasonal_depth_wide` | seasonality-calendar | The calendar-month book, holding 30–45 stocks instead of 20–30. |
| 89 | `lv_illiq_stocks_only` | liquidity-volume | The wider hard-to-trade book with funds excluded, because "hard to trade" doesn't mean the same thing for a fund. |
| 90 | `sl_ppp_walkforward` | statistical-learning | Starts with equal money in every stock, then leans toward recent winners, hard-to-trade names and good calendar months, by amounts re-learned each month from past data. |
| 91 | `rv_volofvol_top15` | range-variance | Buys the 15 stocks whose jumpiness itself changes the most from month to month. |
| 92 | `pl_factor_momentum_timed` | portfolio-learning | Holds twelve simple stock-picking styles, but only those that beat the market over the past year. |
| 93 | `pl_factor_momentum_untimed` | portfolio-learning | A comparison test: the same twelve stock-picking styles, all held all the time. |
| 94 | `lv_overnight_sentiment_reversal` | liquidity-volume | Buys stocks with the weakest overnight price moves last month, betting that mood-driven selling unwinds over the following year. |
| 95 | `rv_sleeve_voltarget_phi05` | range-variance | Holds equal amounts of 42 funds, cutting the total stake when markets get jumpy, but adjusting it slowly to avoid costly trading. |
| 96 | `lv_illiq_evar_riskcost` | liquidity-volume | Hard-to-trade stocks, with extra preference for stocks whose moves similar stocks can't easily copy (risky to bet against). |
| 97 | `lv_illiq_evar_signflip` | liquidity-volume | A comparison test: the same, but preferring stocks that are easy to copy, to check that the direction matters. |
| 98 | `pt_mom_evar_arbrisk` | price-trend | Four-window winners, with extra preference for stocks whose moves similar stocks can't easily copy, where trends tend to last longer. |
| 99 | `rv_minvar_closedform` | range-variance | Holds the mix of calm, market-insensitive stocks that a standard formula says gives the smallest swings, with more money in the calmest. |
| 100 | `rv_minvar_equalweight` | range-variance | The same calm, market-insensitive stocks the lowest-swing formula (#99) picks, but with equal money in each. |
| 101 | `ll_peer_momentum` | lead-lag-spillover | Buys stocks whose closest look-alikes rose most last month, betting the stock follows its peers. |
| 102 | `ll_peer_momentum_evargate` | lead-lag-spillover | Follow-your-peers, but only for stocks that really move with their look-alikes. |
| 103 | `pt_mom_seasonal_deferral` | price-trend | The #98 champion, but it delays a sale by a month if the stock usually does well in the coming month, and delays a purchase if it usually does badly. |
| 104 | `pt_mom_id_z` | price-trend | The #98 champion, with extra preference for stocks that climbed in many small steady steps rather than a few big jumps. |

### Protocol v2 trials (numbered within v2)

| # | strategy | family | what it does |
|---|---|---|---|
| v2-1 | `pt_resid_reversal_v2` | price-trend | Buys the 30 stocks that fell furthest behind the average stock over the past month, betting they bounce back; refreshed monthly. |
| v2-2 | `pt_resid_reversal_band` | price-trend | The same bounce-back bet, but skips the 30 most extreme fallers and buys the next 90, hoping for a smoother ride. |
| v2-3 | `sa_pca_resid_reversion` | statistical-arbitrage | Buys the 30 stocks that fell furthest compared with what similar stocks (same region, sector, style) did last month, betting the gap closes. |
| v2-4 | `sl_ridge_six_features` | statistical-learning | A simple learned model that blends six stock measurements to guess next month's winners; thrown out because it accidentally used information from the future. |
| v2-5 | `sl_ridge_six_masked` | statistical-learning | The same learned model with the future-information leak fixed. |
| v2-6 | `lv_resid_rev_illiq_tilt` | liquidity-volume | The look-alike bounce-back bet (v2-3), tilted toward thinly traded stocks, where forced selling is thought to push prices furthest. |
