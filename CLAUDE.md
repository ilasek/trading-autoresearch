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
| `strategies/lib/` | **add new files freely**; never edit an existing one (a promoted candidate becomes the champion and keeps importing it — editing in place would silently change an already-measured strategy). CI enforces this. |
| `experiments/journal.md`, `experiments/learnings.md` | append/edit |
| `reports/` | create weekly reports |
| `research/` | written by the nightly learning agent (rules in `research/README.md`); strategy sessions read-only |
| `engine/`, `scripts/`, `tests/`, `data/`, `program.md`, `CLAUDE.md` | **frozen — never edit** (CI enforces `engine/`) |
| `strategies/champion.py`, `experiments/trials.jsonl`, `experiments/leaderboard.json` | written only by `run_experiment.py`, never by hand |

## The experiment loop (repeat up to the budget in program.md)

1. **Read first**: `experiments/learnings.md`, the last ~20 entries of
   `experiments/journal.md`, the champion's result card
   (`strategies/champion_card.json`), `experiments/leaderboard.json` (which families
   have been tried, how far each got, how correlated each lead is to the champion),
   and `research/SUMMARY.md` (external-research findings, if present). Then read
   `program.md`'s budget allocation and plan the session's mix of families **before**
   writing the first hypothesis — deciding family-by-family as you go is how a session
   ends up entirely inside the incumbent's family. Do not re-test ideas already refuted unless you have a
   specific reason, which you must state. External findings are literature-derived, not
   verified here: treat `validation_overlap`/`published_post_2018` flags as a discount
   on novelty, and never import performance expectations from them into hypotheses.
2. **Hypothesize**: one sentence, falsifiable, written before you code.
3. **Implement**: one file in `strategies/candidates/<slug>.py` implementing the strategy
   contract (below). Keep it small and readable.
4. **Run**: `.venv/bin/python scripts/run_experiment.py strategies/candidates/<slug>.py`
   The script evaluates train + validation, applies gates, records the trial, and appends a
   journal entry. A candidate that wins validation and clears the deflated-Sharpe bar then
   faces the **holdout veto** (see `program.md`): the holdout is read, and the seat is
   refused if the candidate is worse than the incumbent there by more than 2 paired
   standard errors. On `PROMOTE` the champion is updated.
5. **Verdict handling**:
   - `PROMOTE` → `git add -A && git commit -m "promote: <slug> (<val_sharpe> vs <old>)"`
   - `HOLDOUT_VETO` → the candidate won validation but the holdout refused it. Keep the
     candidate file — it is a result, not a failure — and commit with
     `git commit -m "trial: <slug> HOLDOUT_VETO"`. Record the gate's `t` in the journal
     lesson line; a repeated pattern of vetoes in one family is itself a finding.
   - `FAMILY_LEAD` → a scout set the best result yet in its family. Keep the candidate
     file — it is the family's lead and the thing a later ensemble challenger builds on —
     and commit with `git commit -m "scout: <slug> FAMILY_LEAD (<val_sharpe>)"`. The
     session continues: no holdout was read.
   - `SCOUT` → a scout that did not lead its family. Still a result about the family;
     record what it rules out. Commit `git commit -m "scout: <slug> SCOUT"`.
   - `REJECT`/`GATE_FAIL` → keep the journal/trials changes, delete or keep the candidate
     file as you judge useful, commit with `git commit -m "trial: <slug> REJECT"`.
     Never delete or rewrite journal/trials history.
6. **Learn**: append one lesson line to the journal entry; when a pattern repeats across
   experiments, distill it into `experiments/learnings.md` (and prune stale learnings).

**Stop the session the moment a trial reaches the holdout gate** — on `PROMOTE` or
`HOLDOUT_VETO` alike. You have now seen a holdout number, so every later candidate you
design tonight would be holdout-informed. Write the session summary and stop, even with
budget left.

At session end: write a short session summary block in the journal (experiments run,
verdicts, best finding, next ideas) and push: `git push origin main`.

## Strategy contract

A candidate file must define:

```python
STRATEGY = {
    "name": "twelve_month_momentum",
    "family": "price-trend",                    # a family slug from program.md
    "hypothesis": "One falsifiable sentence.",
    "track": "challenge",                       # or "scout"; defaults to "challenge"
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

### The optional second argument

Declaring a second positional parameter gets you the rest of the daily bar:

```python
def generate_weights(prices, aux):
    """aux: {"open", "high", "low", "volume", "dollar_volume"} — wide frames on
    exactly the same index and columns as `prices`, truncated to the same visible
    window. Volume is a share count in native units and is NOT forward-filled, so
    expect NaN on foreign holidays; `dollar_volume` is close_usd * volume."""
```

Both contracts are supported forever; the one-argument form means "closes only".
`strategies/lib/features.py` has causal helpers for both (range volatility, Amihud
illiquidity, volume shocks, cross-sectional normalisation, long-only weighting).

### Machine-learning candidates

- **Fit walk-forward or not at all.** A model fitted once over the whole visible
  window and applied backwards is the classic lookahead, and `causality_check` is
  built to catch it: it recomputes weights with the tail hidden and fails anything
  whose holdings move. `strategies/lib/walkforward.py` does the bookkeeping —
  a training row is released only once its forward-return target was realized.
- **Be deterministic.** Fix `random_state`, keep estimators single-threaded. The
  causality check compares holdings at 1e-6; non-determinism reads as a peek.
- **Watch the clock.** The protocol calls `generate_weights` about seven times per
  trial (three truncated causality runs, three splits, the champion). The current
  champion takes ~12s; keep a candidate under ~60s per call. If a model is too
  expensive to refit at every month-end, give it fewer rebalance dates rather than a
  cached fit nobody can audit.
- **Prefer few features and a penalised linear model first.** This universe is 140
  instruments; a heavy learner mostly fits noise, and the literature's own finding is
  that the dominant signals are few.

## Hard rules

- **Never touch the holdout split.** No manual backtests on 2024+ data, no "just checking".
  The holdout veto inside `run_experiment.py` is the *only* permitted read, and reaching
  it ends the session. The veto does not make the split a free resource — it is the one
  split not yet spent, and it is spent one look at a time.
- **Never edit the engine, protocol thresholds, or trials.jsonl.** If you believe the
  engine has a bug, write it up in the journal under `## Engine issue` and stop that
  experiment; a human reviews engine changes.
- **A scout never reaches the holdout.** The scout track skips the champion comparison
  entirely, so `holdout_gate` is unreachable from it and a scouting session does not have
  to stop. Do not try to read holdout "just to see how a family did" — that is the same
  rule as always, and the scout track is not a loophole in it.
- **Spend the budget across families.** `program.md` sets the allocation: at most 2
  trials in `price-trend`, at most 2 in any one family until four families have leads,
  at least one in a family with no trials at all. This is a rule, not advice.
- **The learnings file is mostly about one family.** Almost everything in
  `experiments/learnings.md` was measured on `price-trend` constructions. Do not carry
  its constants (the de-concentration price, the required-gain table, the risk-bet
  calibration) into a new family by analogy — re-measure them there or say you have not.
- **Every strategy run goes through `run_experiment.py`** so the trial count (and thus
  the deflated-Sharpe bar) stays honest. No ad-hoc backtests of candidate ideas.
- **No trading, no orders, no broker APIs.** Research only.
- Report failures plainly. A well-documented negative result is a success of the system.
