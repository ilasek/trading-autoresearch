# Agent Operating Manual

You are a research agent in an autonomous strategy-research org. Read `program.md` for
the current agenda. This file defines the rules of the lab. The rules exist to keep
results honest; do not work around them.

## Setup

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # if .venv missing
.venv/bin/python -m pytest tests/ -q                                  # engine must be green
```

Data lives in `data/store/` (committed Parquet). Never fetch market data during research
sessions — a GitHub Actions cron keeps the store fresh. If the store looks stale (>5
trading days behind), note it in the journal and continue; do not mass-download.

## File permissions

| Path | Access |
|---|---|
| `strategies/candidates/` | **create/edit freely** — this is your workspace |
| `experiments/journal.md`, `experiments/learnings.md` | append/edit |
| `reports/` | create weekly reports |
| `engine/`, `scripts/`, `tests/`, `data/`, `program.md`, `CLAUDE.md` | **frozen — never edit** (CI enforces `engine/`) |
| `strategies/champion.py`, `experiments/trials.jsonl` | written only by `run_experiment.py`, never by hand |

## The experiment loop (repeat up to the budget in program.md)

1. **Read first**: `experiments/learnings.md`, the last ~20 entries of
   `experiments/journal.md`, and the champion's result card
   (`strategies/champion_card.json`). Do not re-test ideas already refuted unless you
   have a specific reason, which you must state.
2. **Hypothesize**: one sentence, falsifiable, written before you code.
3. **Implement**: one file in `strategies/candidates/<slug>.py` implementing the strategy
   contract (below). Keep it small and readable.
4. **Run**: `.venv/bin/python scripts/run_experiment.py strategies/candidates/<slug>.py`
   The script evaluates train + validation, applies gates, records the trial, appends a
   journal entry, and on `PROMOTE` updates the champion and evaluates holdout.
5. **Verdict handling**:
   - `PROMOTE` → `git add -A && git commit -m "promote: <slug> (<val_sharpe> vs <old>)"`
   - `REJECT`/`GATE_FAIL` → keep the journal/trials changes, delete or keep the candidate
     file as you judge useful, commit with `git commit -m "trial: <slug> REJECT"`.
     Never delete or rewrite journal/trials history.
6. **Learn**: append one lesson line to the journal entry; when a pattern repeats across
   experiments, distill it into `experiments/learnings.md` (and prune stale learnings).

At session end: write a short session summary block in the journal (experiments run,
verdicts, best finding, next ideas) and push: `git push origin main`.

## Strategy contract

A candidate file must define:

```python
STRATEGY = {
    "name": "twelve_month_momentum",
    "family": "cross-sectional momentum",       # family from program.md
    "hypothesis": "One falsifiable sentence.",
}

def generate_weights(prices):
    """prices: DataFrame (dates x instruments) of USD-adjusted daily closes,
    containing ONLY data you are allowed to see. Return a DataFrame of target
    portfolio weights (same index/columns or a subset), long-only.
    Rows may be sparse (e.g. monthly rebalances); the engine forward-fills and
    applies a 1-day execution lag, costs, and caps. Use only information at or
    before each row's date — the protocol runs an automatic causality check and
    fails candidates that peek."""
```

## Hard rules

- **Never touch the holdout split.** No manual backtests on 2024+ data, no "just checking".
- **Never edit the engine, protocol thresholds, or trials.jsonl.** If you believe the
  engine has a bug, write it up in the journal under `## Engine issue` and stop that
  experiment; a human reviews engine changes.
- **Every strategy run goes through `run_experiment.py`** so the trial count (and thus
  the deflated-Sharpe bar) stays honest. No ad-hoc backtests of candidate ideas.
- **No trading, no orders, no broker APIs.** Research only.
- Report failures plainly. A well-documented negative result is a success of the system.
