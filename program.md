# Research Program

This file is the human-edited "program" that steers the autonomous research org
(autoresearch-style). Agents read this file and `CLAUDE.md` at the start of every
session. Edit this file to change the research agenda; do not edit the engine.

## Mission

Find robust, cost-aware, long-only daily-rebalanced portfolio strategies on a global
stock + ETF universe that beat the current champion out-of-sample, while honestly
accounting for multiple-testing (deflated Sharpe) and data limitations.

## Objective and promotion rule (owned by `engine/protocol.py` — do not reinterpret)

- Objective: **net Sharpe on the validation split (2018-01-01 → 2023-12-31)**, after
  costs, deflated by the total number of trials ever recorded in `experiments/trials.jsonl`.
- A candidate is promoted to champion only if `run_experiment.py` says `PROMOTE`:
  it must beat the champion's validation Sharpe, have deflated-Sharpe probability ≥ 0.95,
  pass all hard gates (drawdown, turnover, concentration, causality check), and pass
  the train-split sanity check.
- The **holdout split (2024-01-01 →)** is evaluated only at promotion time, automatically,
  and every touch is journaled. Never run anything on holdout manually.

## Experiment budget

- Nightly autonomous session: **up to 8 experiments** (one candidate file each), then write
  the session summary in the journal and stop.
- Prefer few well-motivated hypotheses over parameter-sweep spam. Every trial permanently
  raises the deflated-Sharpe bar for all future candidates — wasteful trials have a real cost.

## Strategy families to explore (in rough priority order)

1. **Cross-sectional momentum** (3–12 month lookbacks, skip-month, volatility scaling)
2. **Time-series momentum / trend following** on ETFs with regime filters (e.g., 200d MA)
3. **Volatility targeting / risk parity** across asset-class ETFs
4. **Short-term mean reversion** (careful: turnover gate bites here)
5. **Low-volatility / quality tilts** within the stock universe
6. **Regime switching** (risk-on/risk-off via trend, drawdown, or vol signals)
7. **Combinations** of promoted or near-miss ideas (ensembles of decorrelated signals)

## Constraints and known caveats (repeat these in your reasoning)

- Long-only, max 25% per position, gross leverage ≤ 1.0, costs 15 bps per side (10 cost + 5 slippage).
- Universe is **current** constituents → survivorship bias inflates stock-picking results;
  ETF-level strategies suffer least. Treat single-stock alpha with extra skepticism.
- Free daily data: no intraday, no fundamentals yet, corporate actions as adjusted closes.
- Non-USD instruments are converted to USD; FX moves are part of returns (unhedged).

## Reporting

- Weekly report in `reports/YYYY-WW.md`: champion metric trend, promotions/retirements,
  top learnings, notable failures. Keep it readable for a human skimming on a phone.

## Future upgrades (do not start without human approval)

- Paid point-in-time data (survivorship-bias-free), fundamentals, intraday bars.
- Paper-trading bridge (e.g., Alpaca paper) — human-driven; agents never execute trades.
