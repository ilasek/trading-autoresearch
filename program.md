# Research Program

This file is the human-edited "program" that steers the autonomous research org
(autoresearch-style). Agents read this file and `CLAUDE.md` at the start of every
session. Edit this file to change the research agenda; do not edit the engine.

## Mission

Find robust, cost-aware, long-only daily-rebalanced portfolio strategies on a global
stock + ETF universe that beat the current champion out-of-sample, while honestly
accounting for multiple-testing (deflated Sharpe) and data limitations.

**Breadth is part of the mission, not a detour from it.** The lab spent its first 55
trials inside one family and mapped it to exhaustion; `experiments/learnings.md` now
puts the gain a decorrelated challenger would need at +0.438 Sharpe, which nothing in
that family can supply. A search that only deepens the incumbent has stopped searching.
The two tracks below exist so that a genuinely different mechanism — a learned model, a
liquidity signal, a seasonal effect — can be tested, recorded and built on without
weakening a single gate.

## Objective and promotion rule (owned by `engine/protocol.py` — do not reinterpret)

- Objective: **net Sharpe on the validation split (2018-01-01 → 2023-12-31)**, after
  costs, deflated by the total number of trials ever recorded in `experiments/trials.jsonl`.
- Only a `challenge` candidate can move the champion. `FAMILY_LEAD` and `SCOUT`
  verdicts record a family's best result and never touch the seat or the holdout.
- A candidate is promoted to champion only if `run_experiment.py` says `PROMOTE`:
  it must beat the champion's validation Sharpe, have deflated-Sharpe probability ≥ 0.95,
  pass all hard gates (drawdown, turnover, concentration, causality check), pass
  the train-split sanity check, and **clear the holdout veto** below.
- **The holdout veto.** A candidate that has won everything above is still refused the
  seat if it is worse than the incumbent on the **holdout split (2024-01-01 →)** by more
  than `HOLDOUT_VETO_T` = 2.0 paired standard errors (Memmel's correction to
  Jobson-Korkie, `metrics.sharpe_diff_se`). Such a trial is recorded as `HOLDOUT_VETO`:
  it still counts against the deflated-Sharpe bar, and the champion does not move.
  - The veto is **one-sided**. Holdout is never scored, ranked, or maximized — it can
    only ever say no. A candidate that ties or wins on holdout is promoted on its
    validation case alone, so the burden of proof stays on the challenger.
  - The gate runs **last**, so it reads the holdout only for candidates that would have
    been promoted outright before it existed. The number of candidate holdout reads is
    therefore unchanged by its introduction.
  - Why it exists: between trials #43 and #51 four consecutive promotions raised
    validation Sharpe 1.120 → 1.229 while holdout Sharpe fell 1.377 → 0.691. No promotion
    in this repo's history has ever cleared |t| = 2 on validation, while five of six
    superseded champions beat the incumbent on holdout at |t| > 2. The gate was breaking
    ties on the split with no resolving power.
- Holdout is read **only** by that gate, automatically, and every read is journaled.
  Never run anything on holdout manually.
- **A trial that reaches the holdout gate ends the session** — whether it promoted or was
  vetoed. Once a session has seen a holdout number, every later candidate it designs is
  holdout-informed. This rations the one split that is not yet spent.

## Experiment budget

- Nightly autonomous session: **up to 8 experiments** (one candidate file each), then write
  the session summary in the journal and stop. See the budget allocation below: the 8 are
  not free to spend all in one family.
- Prefer few well-motivated hypotheses over parameter-sweep spam. Every trial permanently
  raises the deflated-Sharpe bar for all future candidates — wasteful trials have a real cost.

## The two tracks

Every candidate declares a track in its `STRATEGY` dict. The default is
`challenge`, so nothing written before this existed changed meaning.

- **`"track": "scout"` — breadth.** Explores a family the lab has not established.
  Runs the same causality check, the same splits and the same hard gates, and counts
  as a full trial in the deflator. It never compares against the champion, so it
  never reaches the holdout gate: **a scouting session spends no holdout look and
  never has to stop early.** Its verdict is `FAMILY_LEAD` when it is the best result
  yet recorded in its family, else `SCOUT`. Both are results, not failures.
- **`"track": "challenge"` — depth.** Competes for the champion seat under exactly
  the promotion rule above. Unchanged in every respect.

`experiments/leaderboard.json` (engine-written after every trial) holds each family's
best validation result and its **return correlation to the seated champion**. That
correlation is the input a challenger needs: a decorrelated leg is worth more in a
blend than a better-correlated one, and the required-gain table in
`experiments/learnings.md` is read off it.

**How a scouted family reaches the seat.** Not by out-scoring the champion alone —
nothing outside `price-trend` plausibly will. A `challenge` candidate blends the
incumbent with one or more decorrelated family leads (`strategies/lib/blend.py`) and
competes normally. That is what "drill into a promising family on a parallel track"
means here: scout to find a lead, then deepen it, then argue the blend from the
leaderboard's rho — never from hope, because naive dilution is already priced and
already loses.

## Strategy families to explore

Use these slugs verbatim in `STRATEGY["family"]`; the leaderboard groups on them.

1. **`statistical-learning`** — cross-sectional return prediction with penalised
   linear models, trees, gradient boosting, small neural nets. Walk-forward refit
   only (`strategies/lib/walkforward.py`). The interesting question is not "does ML
   beat momentum" but which feature groups carry signal once costs and the skip-month
   are respected.
2. **`liquidity-volume`** — Amihud illiquidity, volume shocks, turnover trends,
   dollar-volume. Newly reachable: the volume panel is now passed to strategies.
3. **`range-variance`** — Parkinson / Garman-Klass / Rogers-Satchell range volatility,
   HAR-RV forecasting, vol-of-vol, cross-sectional dispersion and correlation regimes.
   Also newly reachable via the high/low panels.
4. **`seasonality-calendar`** — turn-of-month, month-of-year, day-of-week, holiday
   windows, same-calendar-month seasonality. Cheap to test, mechanically unrelated to
   trend, and the turnover gate is the thing to watch.
5. **`lead-lag-spillover`** — ETF versus constituent, region leading region,
   cross-asset (bonds / commodities / FX into equities), network momentum. The
   universe spans 15 regions and 42 ETFs, which is unusually well suited to this.
6. **`statistical-arbitrage`** — PCA or factor residual reversion, cointegration,
   pairs. Long-only is a real constraint: only the cheap side of a residual is
   tradeable here, so say how the short leg's absence is handled.
7. **`portfolio-learning`** — hierarchical risk parity, clustering-based allocation,
   stacking or meta-labelling over family leads, ensembles of decorrelated signals.
   This is where scouted leads become a challenger.
8. **`price-trend`** — **legacy and capped.** Cross-sectional momentum, time-series
   momentum / trend following, vol targeting / risk parity, short-term reversal,
   low-vol / quality, regime switching: the lab's first seven families, collapsed into
   one because they are one exhausted family in practice. 34 of the first 55 trials
   and all 7 promotions are here.

### Budget allocation (per nightly session)

Of the 8 experiments:

- **at most 2** in `price-trend`;
- **at most 2** in any single family, until at least four families have a recorded lead;
- **at least 1** in a family with no recorded trial at all, while any such family remains.

Spending a whole session inside the champion's family is a protocol violation, not a
judgement call. Diagnostic work that scores no returns remains free and unlimited.

### Exploring is cheap — this is measured, not assumed

The standing reason not to explore was the deflated-Sharpe bar. Measured against the
recorded trial history and the champion's stored validation returns, the DSR of a
1.2-Sharpe candidate as the effective trial count grows:

    effective trials    12 (at the time of writing)   16      20      25      35
    DSR at Sharpe 1.2   0.976                         0.971   0.967   0.963   0.956

Thirteen additional *decorrelated* trials cost about 0.013 of DSR probability and stay
clear of the 0.95 threshold. The deflator is not what was stopping exploration; the
"must beat the champion alone" rule was, and the scout track answers it without
touching the rule. Do not use the deflator as a reason to stay in one family.

## Constraints and known caveats (repeat these in your reasoning)

- Long-only, max 25% per position, gross leverage ≤ 1.0, costs 15 bps per side (10 cost + 5 slippage).
- Universe is **current** constituents → survivorship bias inflates stock-picking results;
  ETF-level strategies suffer least. Treat single-stock alpha with extra skepticism.
- Free daily data: no intraday, no fundamentals yet, corporate actions as adjusted closes.
- **Strategies see full daily OHLCV, not just closes.** A candidate declaring
  `generate_weights(prices, aux)` receives `open`, `high`, `low`, `volume` and
  `dollar_volume` panels, aligned to the same index and columns as `prices` and
  truncated to exactly the same visible window. Volume is a share count in native
  units and is not forward-filled — expect NaN on foreign holidays. The one-argument
  contract still works and still means "closes only".
- **scikit-learn and scipy are available.** A learned strategy must be fitted
  walk-forward: a model fitted once over the whole visible window and applied
  backwards fails the causality check, which is the point of the check. Seed every
  estimator and keep it single-threaded; the check compares holdings at 1e-6 and
  floating-point non-determinism reads as a peek.
- Non-USD instruments are converted to USD; FX moves are part of returns (unhedged).

## Reporting

- `experiments/leaderboard.json` is engine-written after every trial. Read it at the
  start of a session: it is the fastest picture of which families have been tried, how
  far each got, and how correlated each lead is with the incumbent.
- Weekly report in `reports/YYYY-WW.md`: champion metric trend, promotions/retirements,
  top learnings, notable failures. Keep it readable for a human skimming on a phone.

## Future upgrades (do not start without human approval)

- Paid point-in-time data (survivorship-bias-free), fundamentals, intraday bars.
- Paper-trading bridge (e.g., Alpaca paper) — human-driven; agents never execute trades.
