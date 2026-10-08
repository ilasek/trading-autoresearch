# Protocol v3: what the evaluation got wrong, and what changed

_Engine-maintenance report, 2026-10-08. Audit of how a single strategy is judged under
protocol v2, the fixes that became protocol v3, and the re-measurement of the v2 board
under v3. No trial was recorded and no holdout data was read for this report._

## Verdict on v2

v2 was a good **filter** against classic backtest failures: frozen engine, append-only
ledger, causality check, point-in-time universe, hindsight guard, random-selection null.
It was **not** a ranking instrument, and it said almost nothing about current conditions.

## What was wrong, and the fix for each

| # | Problem in v2 | Evidence | v3 fix |
|---|---|---|---|
| 1 | **Rankings are noise.** One six-year validation Sharpe has a 90% interval about ±0.7 wide. | Five v2 trials: every pairwise gap within 1.3 SE; all intervals span ~−0.1 to +1.4. v1 board: observed #1 is #1 in 23% of block-bootstrap resamples; 101 of 103 trials sit in the model confidence set of the best. A hash-of-ticker placebo once ranked 6th of 104. | `engine/ranking.py`, `scripts/rank_trials.py`: skill with a paired block-bootstrap interval, P(best), and the Hansen–Lunde–Nason model confidence set (tier 1). Weekly reports must show tiers, not ordinal ranks. |
| 2 | **The deflated-Sharpe null was zero Sharpe.** A long-only book with no skill earns the market's Sharpe, so DSR mostly tested "is this long equity?". | With 5 effective trials the DSR benchmark was 0.16; centred on the pool (0.51) the expected best of 5 no-skill trials is 0.66 — the v2 lead scored 0.672. The equal-weight pool itself scored DSR 0.81. | `metrics.deflated_skill`: deflate **skill** (Sharpe minus the equal-weight eligible pool's, same days) with a paired bootstrap SE. |
| 3 | **The trial count restarted at zero with each version**, though every version searched the same 2018–2023 window. | 104 v1 trials and a published v2 re-scoring of all of them on that window; v2's deflator counted 5. | The effective N clusters every recorded trial of every version (109 → 36 effective at cut-over). Only the dispersion term stays per-version (scale). |
| 4 | **Same-close fills on a mixed-time-zone calendar.** Weights decided on row t earned close(t)→close(t+1): a Tokyo name was "bought" at Tokyo's close using a US close ~15 h later. The lab's journal dismissed regional lead-lag because "the engine's 1-day lag fills at the t+1 close" — it does not. | Synthetic US→Japan lead-lag rule: Sharpe **+7.62** under v2, **−0.24** with fills at the next real print. | `backtest.simulate`: each name fills at its first *real* close after the decision row (never a forward-filled holiday price). |
| 5 | **Free daily rebalancing.** Target weights were held constant every day; only target changes were charged. | `tests/test_backtest.py::test_costs_charged_on_turnover` asserted zero turnover for a constant-weight book. | Holdings drift as shares; an emitted row is a rebalance and its trades, including undoing drift, are charged. |
| 6 | **One flat 15 bps everywhere.** No stamp duty, no FTT, no liquidity tier — on books selected *for* illiquidity, 71% non-US. | Train split, v2 lead: at 30 bps/side its train IR vs the pool went from +0.03/+0.16 to −0.32/−0.18. | `engine/costs.py`: 15/20/30/40 bps per side by trailing USD volume, plus UK 0.5% on buys, HK both sides, FR/IT/ES on buys; a 2× cost stress is recorded. |
| 7 | **Delisted names silently exit at their last price**, and the null was claimed to share that bias equally. | Unpriced members are disproportionately failures; a loser-buying book meets them far more often than a random draw. | 30% delisting-haircut stress recorded with every trial; the false claim in `benchmarks.py` corrected. (The missing names themselves cannot be priced from free data.) |
| 8 | **Sharpe ignored the risk-free rate; cash earned 0.** | Overstates Sharpe by ~0.1 on 2018–23 rates and ~0.25 at 4–5%. | Cash earns the 13-week T-bill (^IRX, seeded by the data-refresh workflow); every Sharpe is on excess returns. |
| 9 | **The null matched type, not region.** A region/currency tilt counted as stock selection. | — | Replacements for a stock come from the same listing region; the null runs through the same execution model. |
| 10 | **Train was a Sharpe > 0 check.** 21 years of data could not veto a six-year result. | The v2 lead had train Sharpe 0.49/0.93 vs the pool's 0.52/1.00 (1997–2008 / 2009–17). | Gate: train skill > 0. Sub-period skills reported. |
| 11 | **Families were self-declared labels.** | The four v2 "family leads" correlate 0.73–0.94; the four-families rule was met by relabelling one stream. | Leaderboard clusters leads into mechanisms by active-return correlation; the budget rule counts distinct mechanisms. |
| 12 | **Holdout leaked and was unguarded at bootstrap.** Holdout numbers sat in the champion card and journal (required reading); the v2 re-scoring published momentum-lineage holdout results; a version's first champion was promoted with no holdout check. | `engine/protocol.py` bootstrap path; `reports/protocol-v2-*.md`. | Holdout arithmetic only in `experiments/holdout_log.jsonl` (sessions may not read it); veto vs the pool, first champion included. The 2024+ split is declared partly spent. |
| 13 | **Nothing measured current conditions.** Validation ends 2023, scouts never see 2024+. | — | Forward incubation: leads and gate-reaching candidates are frozen and scored only on data after registration (`scripts/incubation_report.py`, weekly in CI). |
| 14 | **The data refresh spliced corporate actions.** Yahoo bars are adjusted as of fetch day; appended rows after a split read as a −50% day, and dividends after the seed vanished from returns. | `scripts/update_data.py` appended rows with no basis check; the quality filter only caught moves beyond −90%. | Overlap re-fetch puts new rows on the stored basis; weekly `--verify-days 120` repairs earlier splices; moves beyond ±40% are flagged. |

## The v2 board re-measured under v3

Train + validation only, through the v3 engine, nothing recorded, no holdout read. The
T-bill series is not yet in the store, so cash and excess returns use rf = 0 here (this
lowers every Sharpe in the table by roughly 0.1 once seeded; it does not change skill
much, since the pool pays it too).

| v2 trial | v2 val Sharpe | v3 val Sharpe | v3 skill vs pool [90% CI] | skill @2× cost | train skill (97–08 / 09–17) | null pct | v3 gates | v3 DSR |
|---|---|---|---|---|---|---|---|---|
| lv_resid_rev_illiq_tilt | 0.672 | 0.440 | −0.01 [−0.39, +0.30] | −0.28 | −0.25 (−0.22 / −0.34) | 100% | fails train skill | 0.10 |
| sa_pca_resid_reversion | 0.597 | 0.453 | +0.00 [−0.33, +0.28] | −0.22 | −0.31 (−0.29 / −0.37) | 99% | fails train skill | 0.10 |
| pt_resid_reversal_v2 | 0.540 | 0.419 | −0.03 [−0.37, +0.26] | −0.18 | −0.34 (−0.29 / −0.47) | 98% | train skill, drawdown | 0.07 |
| sl_ridge_six_masked | 0.385 | 0.257 | −0.20 [−0.50, +0.09] | −0.32 | −0.64 (−0.47 / −0.96) | 52% | train skill, drawdown, null | 0.01 |
| pt_resid_reversal_band | 0.379 | 0.197 | −0.26 [−0.49, −0.06] | −0.45 | −0.19 (−0.18 / −0.26) | 59% | train skill, null | 0.00 |

Equal-weight eligible pool, validation: 0.452 under v3 (0.508 under v2). Effective trials
across all versions: 36 of 109.

**Reading.** The v2 leads beat *random books built like them* (null percentile 99–100%),
because random books churned 22× a year pay the same heavy costs and earn nothing for it;
but they do **not** beat simply holding the pool, on validation or on 21 years of train,
and they lose to it once costs are doubled. The residual-reversion "premium" of 2026-10-07
was the execution model: same-close fills on the signal's own close, free drift, and a
flat cost on illiquid, stamp-duty-paying names.

## What v3 still does not fix

- **Free data.** Yahoo does not price most delisted members (3–11% over validation, 34–60%
  before 2009); the haircut stress bounds the effect but cannot replace the missing names.
- **Adjusted prices inside liquidity measures.** `dollar_volume` and the ADV floor use
  dividend-back-adjusted closes, a mild look-ahead into eligibility and the illiquidity
  signal. Fixing it needs unadjusted closes in the store.
- **One validation window.** Train now has a veto, but rankings still rest on 2018–2023.
- **The cost tiers are judgement**, documented in `engine/costs.py`; they are deliberately
  never cheaper than v2's 15 bps. The 2× stress is there to show sensitivity.
- **The holdout is partly spent** for the momentum lineage. Forward incubation is the clean
  test of current conditions, and it accrues one day at a time: under ~1 year of forward
  data, read it as anecdote.

## Operational notes

- A v3 trial stops with an error until the T-bill series `RATE_US3M` is in the store. The
  next data-refresh run seeds it (or run the workflow manually).
- The first Monday (or manual) refresh also runs `--verify-days 120`, repairing any
  dividend/split spliced in since the store was seeded in August.
- A v3 trial takes roughly 3–5 minutes on the full panel (the null replays 200 random books
  through the execution model).
