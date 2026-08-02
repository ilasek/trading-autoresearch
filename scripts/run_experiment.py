#!/usr/bin/env python
"""Run one experiment: judge a candidate strategy under the fixed protocol.

This is the ONLY sanctioned way to backtest a candidate. It records the trial
(raising the deflated-Sharpe bar for everyone after), appends a journal entry,
and on PROMOTE swaps in the new champion and evaluates the locked holdout.

Usage: python scripts/run_experiment.py strategies/candidates/<slug>.py
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data, protocol

JOURNAL = protocol.ROOT / "experiments" / "journal.md"


def fmt_split(name: str, m: dict | None) -> str:
    if not m:
        return f"  {name}: n/a"
    return (
        f"  {name}: sharpe {m['sharpe']:+.2f} | ann_ret {m['ann_return']:+.1%} | "
        f"maxDD {m['max_drawdown']:.1%} | turnover {m['ann_turnover']:.1f}x | "
        f"avg_pos {m['avg_positions']:.1f}"
    )


def journal_entry(r: protocol.TrialResult) -> str:
    lines = [
        f"## {r.ts} — {r.name} — **{r.verdict}**",
        f"- Candidate: `{r.candidate}` (family: {r.family}, trial #{r.n_trials})",
        f"- Hypothesis: {r.hypothesis or '_none stated_'}",
        f"- Verdict: {r.verdict} — " + "; ".join(r.reasons),
    ]
    for split in ("train", "validation", "holdout"):
        m = protocol._public(getattr(r, split))
        if m:
            lines.append(
                f"- {split.capitalize()}: sharpe {m['sharpe']:+.2f}, "
                f"ann_ret {m['ann_return']:+.1%}, maxDD {m['max_drawdown']:.1%}, "
                f"turnover {m['ann_turnover']:.1f}x"
            )
    if r.dsr is not None:
        lines.append(f"- Deflated Sharpe prob: {r.dsr} (bar from {r.n_trials} trials)")
    if r.champion_val_sharpe is not None:
        lines.append(f"- Champion validation sharpe at the time: {r.champion_val_sharpe:+.2f}")
    lines.append("- Lesson: _(fill in after reflection)_")
    return "\n".join(lines) + "\n\n"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    candidate = Path(sys.argv[1]).resolve()
    if not candidate.exists():
        print(f"no such candidate: {candidate}")
        return 2

    print(f"Loading price data …")
    prices = data.load_prices()
    print(f"  {prices.shape[1]} instruments, {prices.index[0].date()} → {prices.index[-1].date()}")

    print(f"Running protocol on {candidate.name} …")
    result = protocol.run_trial(candidate, prices)

    print()
    print(f"=== {result.name} [{result.family}] — {result.verdict} ===")
    print("reasons: " + "; ".join(result.reasons))
    print(fmt_split("train     ", protocol._public(result.train)))
    print(fmt_split("validation", protocol._public(result.validation)))
    if result.dsr is not None:
        print(f"  deflated sharpe prob: {result.dsr}  (trial #{result.n_trials})")
    if result.champion_val_sharpe is not None:
        print(f"  champion validation sharpe: {result.champion_val_sharpe:+.2f}")
    if result.holdout:
        print(fmt_split("holdout   ", protocol._public(result.holdout)))
        print("  (holdout evaluated because of promotion — logged)")

    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    if not JOURNAL.exists():
        JOURNAL.write_text("# Experiment Journal\n\nAppend-only. Newest entries last.\n\n")
    with open(JOURNAL, "a") as f:
        f.write(journal_entry(result))
    print(f"\njournal entry appended → {JOURNAL.relative_to(protocol.ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
