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

## Protocol v3 — in force since 2026-10-08

v3 keeps v2's universe, splits, hindsight guard and random-selection null, and changes how
a candidate's returns are produced and judged. The audit that motivated it, and the
re-measurement of the v2 board under it, are in `reports/protocol-v3-methodology.md`. In
one line: v2's numbers were flattered by its execution assumptions, and its ranking looked
sharper than six years of data can make it.

- **Execution** (`engine/backtest.py`, `engine/costs.py`). An emitted row fills, name by
  name, at that name's next *real* close (the old convention filled at the same close the
  signal used — look-ahead on a calendar mixing time zones, and free bid-ask bounce).
  Holdings drift between rebalances and undoing drift is charged. Costs are per name: a
  liquidity tier (15/20/30/40 bps per side by trailing USD volume) plus UK/HK/FR/IT/ES
  transaction taxes. Cash earns the 13-week T-bill rate; every Sharpe is on excess returns.
- **Skill, not Sharpe, is deflated.** The deflated-Sharpe test of v1/v2 asked whether a
  candidate beat the best of N *zero*-Sharpe strategies; a long-only book with no skill
  has the market's Sharpe, so it mostly asked "is this long equity?" (the equal-weight pool
  itself scored 0.81). v3 deflates **skill** — validation Sharpe minus the equal-weight
  eligible pool's on the same days — with a paired block-bootstrap error.
- **The trial count spans every version.** v1's 104 trials and v2's all searched the same
  2018–2023 window. The deflator's effective N clusters every recorded trial of every
  version (109 → 36 effective at cut-over). Only the dispersion term is per-version.
- **Train must show skill.** The train gate is now "train Sharpe above the pool's on the
  same days", not "train Sharpe above zero". 1997–2008 and 2009–2017 are reported apart.
- **Stresses are recorded** with every trial: skill at 2× liquidity costs, and skill when a
  held series that ends is sold 30% below its last price (the delisting bias that remains
  in a Yahoo-priced universe falls hardest on loser-buying books).
- **The null is region-matched** (a random replacement for a stock comes from the same
  listing region) and runs through the same execution model.
- **Holdout hygiene.** The veto now also refuses a candidate that loses to the equal-weight
  pool by more than 2 paired SEs, and applies to a version's first champion too. Holdout
  numbers go only to `experiments/holdout_log.jsonl`; the card, the journal and
  `trials.jsonl` record the verdict. The 2024+ split is **partly spent**: the v2 re-scoring
  read it for the momentum lineage and published the result.
- **Forward incubation.** Every candidate that leads its family or reaches the holdout gate
  is frozen into `strategies/incubating/` and scored by `scripts/incubation_report.py` only
  on trading days after it was registered — the one evidence about current conditions
  that no design decision here has seen. For humans; sessions do not read it.
- **Ranking with error bars.** `scripts/rank_trials.py` ranks recorded trials by skill
  with a 90% interval, P(best), and the model confidence set (tier 1 = cannot be told apart
  from the best). The leaderboard groups family leads into **mechanisms** by the
  correlation of their active returns.
- **The seat starts empty again**, and a v3 trial needs the T-bill series in the store
  (seeded by the data-refresh workflow); `run_experiment.py` stops with an error until it is.

What v3 measured on the v2 board (train + validation, nothing recorded): both v2 family
leads score **zero skill** (−0.01 and +0.00 against a pool at 0.45, 90% intervals about
±0.33), negative skill at 2× costs, and negative train skill in both sub-periods. The v2
"tradeable cross-sectional premium" (`learnings.md`, 2026-10-07) does not survive realistic
execution.

## Protocol v2 — in force 2026-10-06 → 2026-10-08

Every trial now runs under protocol v2 (`PROTOCOL_VERSION = 2` in `engine/protocol.py`).
The re-scoring that motivated the switch is in `reports/protocol-v2-survivorship.md` and
`reports/protocol-v2-comparison.md`: on a point-in-time universe the v1 champion's
validation Sharpe fell from 1.27 to 0.19, and the v1 ranking of all 104 trials agreed with
the v2 ranking at Spearman +0.43 only. What changed:

- **Universe.** ~1,400 stocks that were ever members of nine tracked indices (S&P 500 from
  1996; DAX, CAC 40, FTSE 100, SMI, AEX, Euro Stoxx 50, Nikkei 225, Hang Seng from 2009)
  plus the 42 legacy ETFs. A stock is buyable only on dates it was an index member; the
  engine zeroes weight on anything else. A column appears in `prices` only once the name
  has been eligible. Train starts 1997-01-01; earlier prices are warm-up only.
- **A new hard gate.** Validation Sharpe must beat the 90% quantile of 200 random
  portfolios built exactly like the candidate (same holdings schedule, weights and
  stock/ETF mix) from the same point-in-time pool.
- **The hindsight guard.** A candidate may not name a stock or read the legacy universe,
  in its own source or in any `strategies` module it imports. Its universe comes from the
  `eligible` panel. `strategies/lib/groups.py` maps the 140 legacy names, so anything
  importing it — directly or through `signal_blend.py` / `union_legs.py` — is refused.
- **A fresh history.** The deflated-Sharpe bar, family bests and `leaderboard.json` count
  only v2 trials (the board is rewritten for v2 by the first v2 trial; until then it still
  shows v1). The 104 v1 trials stay in `trials.jsonl`, untouched, as v1 records.
- **An empty seat.** The v1 champion (`pt_mom_evar_arbrisk`) holds no seat under v2: a
  champion counts only under the protocol version it was promoted in (`protocol_version`
  in its card). Its files stay in place until the first v2 promotion moves them to
  `strategies/archive/`. Under v2 the first `challenge` candidate that passes every gate
  and reaches DSR ≥ 0.95 is promoted by the bootstrap rule (its promotion reads holdout
  once, so it ends the session as usual). After that, the promotion rule below applies.
- **v1 knowledge is a hypothesis, not a result.** `experiments/learnings.md`, every family
  lead and every constant in it were measured on today's survivors. Re-measure before
  relying on any of it; the re-scoring shows v1 rankings largely did not carry over.

## Objective and promotion rule (owned by `engine/protocol.py` — do not reinterpret)

- Objective: **net Sharpe on the validation split (2018-01-01 → 2023-12-31)**, after
  costs and in excess of T-bills; the deflated test (DSR ≥ 0.95) is on its **skill** over
  the equal-weight eligible pool, against the effective number of trials recorded under
  **every** protocol version in `experiments/trials.jsonl` (v3).
- Only a `challenge` candidate can move the champion. `FAMILY_LEAD` and `SCOUT`
  verdicts record a family's best result and never touch the seat or the holdout.
- A candidate is promoted to champion only if `run_experiment.py` says `PROMOTE`:
  it must beat the champion's validation Sharpe, have deflated-Sharpe probability ≥ 0.95,
  pass all hard gates (drawdown, turnover, concentration, causality check, hindsight
  guard, random-selection null), pass
  the train-split sanity check, and **clear the holdout veto** below.
- **The holdout veto.** A candidate that has won everything above is still refused the
  seat if it is worse than the incumbent — or, under v3, than the equal-weight eligible
  pool — on the **holdout split (2024-01-01 →)** by more than `HOLDOUT_VETO_T` = 2.0
  paired standard errors (Memmel's correction to Jobson-Korkie, `metrics.sharpe_diff_se`).
  Such a trial is recorded as `HOLDOUT_VETO`: it still counts against the deflated bar,
  and the champion does not move. Under v3 the first champion of the version faces the
  pool comparison too.
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

**How a scouted family reaches the seat.** (Written under v1; the v2 seat starts empty, so
the first challenger only has to clear the bars, not an incumbent.) Not by out-scoring the
champion alone — under v1 nothing outside `price-trend` plausibly would. A `challenge` candidate blends the
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
8. **`price-trend`** — **legacy and capped** (the cap is kept under v2: the momentum lineage
   is the family the re-scoring hit hardest). Cross-sectional momentum, time-series
   momentum / trend following, vol targeting / risk parity, short-term reversal,
   low-vol / quality, regime switching: the lab's first seven families, collapsed into
   one because they are one exhausted family in practice. 34 of the first 55 trials
   and all 7 promotions are here.

### Budget allocation (per nightly session)

Of the 8 experiments:

- **at most 2** in `price-trend`;
- **at most 2** in any single family, until at least four **distinct mechanisms** have a
  recorded lead (`distinct_mechanisms` in `leaderboard.json`: family leads whose active
  returns correlate at ≥ 0.5 are one mechanism, whatever their slugs — on the first v2
  night four slugs were one residual-reversal stream);
- **at least 1** in a family with no recorded trial at all, while any such family remains.

Spending a whole session inside the champion's family is a protocol violation, not a
judgement call. Diagnostic work that scores no returns remains free and unlimited.

### Exploring is cheap — this is measured, not assumed

(Measured on the v1 trial history and the v1 deflator. **Superseded by v3**: the v3 bar
deflates skill against an effective N that already counts every earlier version's trials
— 36 at cut-over — so it is much higher from the first v3 trial on, and one more
decorrelated trial moves it less than the table below suggests. Re-measure before
quoting it.)

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

- Long-only, max 25% per position, gross leverage ≤ 1.0. Costs (v3): 15–40 bps per side by
  liquidity, plus transaction taxes (UK 0.5% on buys, HK both sides, FR/IT/ES on buys);
  fills at each name's next real close; holdings drift between rebalances.
- Universe is **point-in-time** (protocol v2): survivorship bias is removed from the
  universe, not eliminated. Yahoo prices 89–97% of index members over validation but only
  40–66% over 1996–2008, so train numbers stay optimistic. The guard catches hard-coded
  hindsight; it cannot catch hindsight in a hypothesis — do not design from knowledge of
  which names later won.
- **Use the `eligible` panel.** Declare `eligible=None` as a keyword parameter of
  `generate_weights` to receive it (dates × columns, bool). Ranking names outside it is not
  an error, but the engine zeroes their weight, so the book you meant is not the book that
  is scored.
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
  the strategy leaderboard as of the week's end (from `scripts/rank_trials.py`: the
  confidence-set tier 1 plus every strategy first tested that week, each with its **tier**,
  family, verdict, skill and its 90% interval, mechanism, and a one-line plain-English
  summary of what it does, with no jargon — never an ordinal rank on its own, which reads
  as a precision the data does not have), top learnings, notable failures. Summaries live
  in `reports/strategy-summaries.md`: add a row there for every new strategy and quote it.
  Keep it readable for a human skimming on a phone.
- `reports/incubation.md` (forward results, written weekly by the data-refresh workflow)
  is for the human owner only; strategy sessions never read it.

## Future upgrades (do not start without human approval)

- Paid point-in-time data with full price coverage before 2009, fundamentals, intraday bars.
- Point-in-time sector labels (the legacy `groups.py` sector map covers only 140 names).
- Paper-trading bridge (e.g., Alpaca paper) — human-driven; agents never execute trades.
