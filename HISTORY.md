# Project History & Design Decisions

This is the narrative record of how the lab was built, what it found, and why the
protocol looks the way it does. `experiments/journal.md` is the append-only ledger
of every trial; `experiments/learnings.md` is the distilled research findings;
`reports/` are the weekly human-readable summaries. This file is the layer above
all three: the story of the system itself, not of any one strategy.

For the current agenda see `program.md`. For the rules agents operate under see
`CLAUDE.md`. Nothing here overrides either.

## What this is

An autonomous strategy-research lab, in the spirit of
[karpathy/autoresearch](https://github.com/karpathy/autoresearch): an AI agent runs a
hypothesize → implement → backtest → keep-or-discard → journal loop, nightly and
mostly unattended, against a frozen evaluation protocol it cannot edit. The frozen
protocol is the point — the interesting engineering problem here isn't the momentum
signal, it's building a research environment where an agent motivated to find
promotable strategies still can't quietly loosen the bar that judges them.

## Origins — 2026-08-02

The system was bootstrapped in one commit
([`639ad64`](https://github.com/ilasek/trading-autoresearch/commit/639ad64)):
data loader, vectorized backtest engine, metrics (including deflated Sharpe),
the fixed protocol, CI, and three inaugural trials. The founding design decisions,
all still standing:

| Decision | What it means | Why |
|---|---|---|
| **Frozen `engine/`, CI-enforced** | Research agents can propose strategies but cannot touch the code that scores them. `protect-engine.yml` fails any commit touching `engine/`, `scripts/`, `tests/`, `program.md`, `CLAUDE.md`, or `data/universe.yaml` unless the commit message contains `[engine-maintenance]` — reserved for human-reviewed changes. | An agent under pressure to find a promotable strategy has a standing incentive to loosen the thing that judges it. Removing its ability to do so, rather than trusting it not to, is the load-bearing design choice of the whole project. |
| **Three-way walk-forward split** | train (→2017-12-31) / validation (2018-01-01→2023-12-31) / holdout (2024-01-01→, locked). | Validation is where research happens and gets fitted against, however indirectly, across many trials. Holdout exists only to catch that fitting after the fact. |
| **Holdout touched exactly once, automatically** | `evaluate_split(..., "holdout")` is only ever called from inside `promote()`, itself only reachable from a PROMOTE verdict. No manual backtest on 2024+ data is possible without editing the frozen engine. | The instant a holdout number is seen and rejected, it stops being a holdout — the next attempt is implicitly fit to it. Locking the mechanism, not just the policy, is what makes "never touch the holdout" enforceable rather than aspirational. |
| **Deflated Sharpe as the sole promotion objective** | Validation net Sharpe must beat the champion, and pass Bailey & López de Prado's probabilistic Sharpe test against the expected maximum Sharpe of every trial ever recorded — `DSR ≥ 0.95`. | With one validation window and unbounded trials, "beats the champion" alone is a p-hacking machine — someone will eventually get lucky. Deflating by trial count makes the multiple-testing cost explicit and rising, rather than invisible. |
| **Causality (no-lookahead) check** | Every candidate is re-run on truncated price histories; if its holdings for shared dates differ, it's rejected as peeking. | Catches accidental lookahead (e.g. computing a signal on `.mean()` over the full frame) that a human reviewer would likely miss and that would otherwise silently inflate every metric downstream. |
| **Hard gates** (drawdown, turnover, concentration, min positions/active days) | Checked before DSR is even computed. | Sanity floor independent of the Sharpe optimization — a strategy can't buy a high Sharpe with 90% drawdown or by holding one stock. |
| **Append-only trial ledger** | `experiments/trials.jsonl` is written only by `run_experiment.py`; the file permission table in `CLAUDE.md` forbids hand-editing it. | The deflator's honesty depends entirely on the recorded trial count being the true trial count. A ledger that can be quietly edited is a ledger that can be quietly gamed. |
| **Yahoo-first free data, committed to the repo** | `data/store/` is Parquet, refreshed by a daily GitHub Actions cron; research sessions never fetch data live. | Keeps backtests fully offline and reproducible commit-to-commit; the cost is survivorship bias (today's constituents only) and no fundamentals/intraday — treated as a permanent, explicitly documented caveat rather than something to work around. |

`mom_12m_baseline` (classic 12-1 cross-sectional momentum) was the first and, at
bootstrap, only trial — promoted automatically since no champion yet existed.
Validation Sharpe 0.865.

## Research timeline

### Week 1 (Aug 2–8): the momentum ladder begins

29 trials across 5 nightly sessions, all REJECT or GATE_FAIL after the bootstrap
promotion. The shape that would define the rest of the project's research showed up
immediately: successive refinements to the *same* momentum idea — buffered basket
membership, then rank-weighting, then z-score magnitude-weighting, then a
daily-reacting volatility-spike trim — climbed validation Sharpe from 0.865 to 1.07
in clean, well-motivated steps, while the deflated-Sharpe bar rose to meet each gain
almost exactly. By trial #28 (`mom_zscore_narrow_daily_volspike_trim`), DSR reached
0.9326 — the closest miss yet, on every axis (Sharpe, drawdown, *and* DSR)
simultaneously better than the champion. See `experiments/learnings.md` for the
full mechanism-by-mechanism account; it's substantial and worth reading directly
rather than re-summarizing here.

Two negative-space decisions from this week turned out to matter as much as the
positive findings: sessions on 08-07 and 08-11 explicitly ran *fewer* than their
8-trial budget when no remaining hypothesis had a strong rationale, on the reasoning
that a low-conviction trial permanently raises the bar for everyone after it for a
result nobody expects to promote. This restraint is now house doctrine (see
`program.md`'s "prefer few well-motivated hypotheses" instruction) and shows up
repeatedly in later sessions.

### Week 2 (Aug 9–15): the split-brain incident

An operational failure, not a research one, but the most consequential thing to
happen to the protocol's integrity before the DSR fix below. The nightly scheduled
trigger had an outcome-branch setting that pushed each night's work to a fresh
per-run branch (`claude/keen-einstein-*`) instead of `main`. Four consecutive
sessions (08-12 through 08-15) each started from `main`'s tip, ran real trials,
and never merged — so each session's deflated-Sharpe bar was computed from `main`'s
31 recorded trials while the true attempted count silently grew to 50. None of the
four could see the others' work either: residual momentum was independently
re-tested three times across three different nights.

The best result of the entire project to date was sitting on one of those orphaned
branches: overlapping formation tranches (`mom_zscore_overlap6_daily_trim`,
validation Sharpe 1.107, turnover cut to a third) — found on 08-15 and invisible to
`main` for a full day.

This was caught and fixed on 08-16, documented in full in the journal's
`## Protocol issue — 2026-08-16` entry (worth reading directly — it's an unusually
clear postmortem). The resolution:

- The four orphaned sessions were preserved as annotated git tags
  (`archive/nightly-2026-08-12` … `-15`) rather than imported — importing would
  have meant hand-editing `trials.jsonl`, which the file-permission table forbids
  even to fix a real bug.
- Every number from those sessions was declared **unusable as-is**: each was
  deflated against a stale, understated trial count and therefore overstated. Any
  finding worth keeping had to be re-run through `run_experiment.py` against
  `main`'s real history before being treated as established.
- The overlapping-tranches result was re-run verbatim that same night (trial #32
  on `main`) and reproduced to the decimal — validation Sharpe 1.11, DSR 0.9341,
  still short of 0.95, but the highest DSR ever legitimately recorded on `main`.
- The weekly report for that week (`reports/2026-W33.md`) had already been written
  from the incomplete picture and calmly amended with a full correction section
  rather than rewritten — the append-only discipline applied to prose, not just to
  the trial ledger.

The same night's session also traced *why* the overlap mechanism worked, and got
it right on the second attempt: not "a cheaper implementation of the same signal"
(the original hypothesis) but that ~20% of book weight sits on names the current
month's signal has already rejected — pruning that stranded capital costs Sharpe,
drawdown, and turnover simultaneously, because it collapses the six formation
tranches back onto near-identical name sets and destroys the temporal breadth that
no single-date selection rule can reproduce. That correction is itself a good
example of the lab's standard for a finding: mechanism explained, alternative
explanation tested and refuted, not just a Sharpe number reported.

### 2026-08-16: the deflated-Sharpe audit and fix

With `main`'s history back to 34 real trials and the best challenger sitting at
0.9341 — tantalizingly below 0.95 — the human operator asked a pointed question:
does DSR over-penalize potentially winning variants, and does it favor the
incumbent simply because it was tested first? An audit of the trial record (not
guesswork — the actual numbers were pulled and recomputed) found the answer was
yes, for two separable reasons, and both were fixed by hand in
[PR #1](https://github.com/ilasek/trading-autoresearch/pull/1), reviewed and merged
under `[engine-maintenance]`:

**1. The incumbent held a seat it never earned.** `run_trial`'s bootstrap branch
(`if not CHAMPION_FILE.exists(): promote()`) computed the DSR but never checked it
before promoting. `mom_12m_baseline` was seated on day one at DSR 0.9312 — below
the very bar it went on to impose on all 33 challengers after it — and was never
re-deflated as the trial count grew. Recomputed against the full 34-trial pool it
scored 0.8129, while the best challenger, at +28% validation Sharpe, was being
rejected at a *higher* DSR than the champion had ever posted. Fix: the bootstrap
path now enforces the same threshold, and every comparison re-deflates the
incumbent against exactly the bar the challenger faces. A champion that can no
longer clear 0.95 is marked **provisional** and can be displaced by a candidate
that beats it on both validation Sharpe and DSR, even below 0.95; a champion that
does clear 0.95 can only be displaced by another that also does.

**2. Near-duplicate trials were deflated as if independent.** Bailey & López de
Prado's expected-maximum-Sharpe benchmark assumes independent trials. 23 of the 34
recorded trials were one idea, tuned across successive variants — the entire ladder
from `mom_12m_baseline` through `overlap6` described above. Counting each as an
independent shot at a high Sharpe inflates the benchmark, and does so
asymmetrically: a failed *off-family* idea widens the cross-trial Sharpe dispersion
and raises the bar for everyone, while another near-duplicate of the incumbent
barely moves it — the opposite of the incentive the lab wants. Fix:
`effective_n_trials` clusters trials by the correlation of their validation return
series (single-linkage, ρ ≥ 0.95) and passes the cluster count, not the raw count,
to `deflated_sharpe`. The dispersion term still uses every trial — only the count
is corrected. Per-trial validation returns are now stored in
`experiments/trial_returns/`, named by timestamp so `trials.jsonl` stays untouched;
`scripts/backfill_trial_returns.py` reconstructed all 33 recoverable historical
trials with **zero Sharpe drift**, confirming the committed price store reproduces
every past backtest exactly. Result: 34 trials turned out to be worth 11 effective
ones.

Both fixes are stated as a **discontinuity, not a silent revision**: DSR values
recorded before this change are explicitly flagged as incomparable to those after
it, in both the journal and the PR description, rather than treated as if the bar
had always worked this way.

`mom_zscore_overlap6_daily_trim` was then run for real through
`run_experiment.py` as trial #35. It cleared the corrected bar outright — DSR
0.9621 against 11 effective trials — and **promoted**, becoming the second champion
in the project's history:

| split | Sharpe | ann. return | max drawdown |
|---|---|---|---|
| train | +0.98 | +19.4% | −56.5% |
| validation | +1.11 | +26.9% | −29.1% |
| **holdout** | **+1.22** | **+32.7%** | −23.3% |

The holdout — evaluated exactly once, automatically, as the mechanism guarantees —
came out *better* than validation, the opposite of the overfitting signature that
would have cast doubt on the promotion.

One honest tradeoff was written into the record alongside the fix, not glossed
over: within-family tuning is now nearly free in deflation terms, since a 24th
momentum variant just joins an existing cluster. That's the intended correction —
redundant trials were never truly extra shots on goal — but it does remove
deflation as a brake on within-family overfitting specifically. What still holds
that line is the raw-Sharpe-beats-incumbent requirement and the fixed validation
window; the holdout remains the backstop.

## Design decision log

Chronological list of decisions that shaped the protocol or the operating rules,
for quick reference. Each links to where the reasoning is spelled out in full.

1. **Frozen engine, CI-enforced, `[engine-maintenance]` escape hatch for reviewed
   changes** — bootstrap, `639ad64`. See "Origins" above.
2. **Deflated Sharpe (Bailey & López de Prado) as the sole promotion metric, with
   an explicit 0.95 probability bar** — bootstrap, `engine/metrics.py`,
   `engine/protocol.py`.
3. **Holdout evaluated exactly once, mechanically, only at promotion** —
   bootstrap, `protocol.promote()`.
4. **Prefer few well-motivated trials over parameter sweeps** — codified in
   `program.md` after week 1 showed the pattern paying off; a wasted trial's cost
   is permanent (it raises the bar for every future candidate).
5. **Nightly runs must land on `main`, not per-run branches** — forced by the
   2026-08-12..15 split-brain incident; see `## Protocol issue — 2026-08-16` in
   the journal for the full incident report and the archive-tag preservation
   mechanism used to avoid touching the frozen trial ledger even while fixing it.
6. **Deflate against effective (correlation-clustered) trial count, and re-deflate
   the incumbent at the same bar on every comparison** — 2026-08-16,
   [PR #1](https://github.com/ilasek/trading-autoresearch/pull/1), see above.
   Introduced the "provisional champion" concept and per-trial return storage
   (`experiments/trial_returns/`).
7. **External-research learning agent, quarantined in `research/`** — 2026-08-17.
   A second nightly cloud routine scans public literature (papers, credible
   practitioner research) and distills findings into `research/notes/` +
   `research/SUMMARY.md`, which the strategy session now reads as idea input
   (CLAUDE.md step 1, wired via `[engine-maintenance]`). Its output is kept out
   of `experiments/learnings.md` so "verified on this repo's data" and "read in
   the literature" never blur. Source soundness is scored (citations, venue tier,
   replication status, sample robustness, cost-awareness). Lookahead policy:
   mechanisms only, no period-specific performance figures, an absolute ban on
   post-2023 information, and per-source `sample_period` /
   `validation_overlap` / `published_post_2018` tags so the strategy agent can
   discount hypotheses implicitly pre-fit to its validation window. Residual
   risk accepted knowingly: publication selection can still softly contaminate
   hypothesis *choice* (the causality check only catches code-level peeking, and
   the trial counter cannot see out-of-band screening) — the holdout remains the
   backstop. Rules live in `research/README.md`; the agent never backtests and
   never touches the trial ledger.

## Current state (as of 2026-08-16)

- **Champion:** `mom_zscore_overlap6_daily_trim` — cross-sectional momentum,
  z-score magnitude-weighted, six overlapping monthly formation tranches, daily
  volatility-spike exposure trim. Validation Sharpe 1.11, holdout Sharpe 1.22.
  Promoted at trial #35, DSR 0.9621 (11 effective trials).
- **Trial ledger:** 35 trials recorded on `main`; 11 effective after clustering.
  19 additional trials exist only as archived, explicitly-invalid tags
  (`archive/nightly-2026-08-12` … `-15`) — never merged, never counted, preserved
  for provenance only.
- **Retired champion:** `mom_12m_baseline` (bootstrap, val Sharpe 0.865),
  archived at `strategies/archive/20260816-203332_mom_12m_baseline.py`.
- **Closed research directions** (see `experiments/learnings.md` for full detail
  on each): low-volatility/inverse-vol tilts and weighting, external
  trend/regime-based de-risking overlays, standalone diversified ETF sleeves,
  52-week-high proximity as a signal substitute, residual momentum, tranche-K
  sweeping, sector-neutral scoring on the current best challenger.
- **Open directions:** a genuinely decorrelated (not just widened) source of
  formation-date breadth beyond the six-tranche overlap; whether the
  within-family-tuning-is-nearly-free tradeoff from the DSR fix needs a
  complementary safeguard once the current champion's own family gets tuned
  further.
