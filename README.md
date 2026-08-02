# trading-autoresearch

Autonomous investment-strategy research, in the spirit of
[karpathy/autoresearch](https://github.com/karpathy/autoresearch): AI agents run a tight
loop — hypothesize → write a candidate strategy → backtest under a **fixed protocol** →
keep-or-discard → journal the learning — continuously and unattended.

**This is a research system, not a trading system.** It never executes trades and its
output is not investment advice. Backtest results on free data (with known survivorship
bias) routinely overstate live performance.

## How it works

- **The repo is the lab.** Market data (Parquet), the frozen backtest engine, strategies,
  the experiment journal, and reports all live in git. Any fresh clone can run the loop.
- **No API calls during research.** Daily bars for a curated global stock+ETF universe are
  stored in `data/store/` and refreshed incrementally by a GitHub Actions cron job.
  Backtests are fully offline, so API rate limits never throttle research.
- **Fixed protocol.** `engine/` is frozen (CI-enforced). Walk-forward splits:
  train (→2017) / validation (2018–2023) / locked holdout (2024→). One objective metric:
  validation net Sharpe, deflated for the number of trials ever attempted. Hard gates on
  drawdown, turnover, and concentration. Automatic causality (no-lookahead) check.
- **Learning loop.** Every trial is appended to `experiments/trials.jsonl` and
  `experiments/journal.md`; distilled insights accumulate in `experiments/learnings.md`,
  which agents read before proposing the next hypothesis.

## Quick start

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/seed_data.py            # one-time bulk data seed
.venv/bin/python scripts/run_experiment.py strategies/candidates/my_idea.py
```

## Key files

| Path | Purpose |
|---|---|
| `program.md` | The research program: agenda, budgets, promotion rules (human-edited) |
| `CLAUDE.md` | Agent operating manual — the loop, file permissions, journaling |
| `engine/` | Frozen: data loader, backtest engine, metrics, protocol |
| `strategies/champion.py` | Current best strategy (promoted only by the protocol) |
| `strategies/candidates/` | Where agents write new strategy ideas |
| `experiments/` | journal.md, learnings.md, trials.jsonl |
| `reports/` | Weekly human-readable reports |
