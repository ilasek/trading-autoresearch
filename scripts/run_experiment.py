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
        lines.append(
            f"- Deflated Sharpe prob: {r.dsr} (bar from {r.n_trials} trials, "
            f"{r.n_effective_trials:g} effective)"
        )
    if r.champion_val_sharpe is not None:
        lines.append(f"- Champion validation sharpe at the time: {r.champion_val_sharpe:+.2f}")
    if r.champion_dsr is not None:
        lines.append(
            f"- Champion re-deflated at the same bar: {r.champion_dsr}"
            + (" — **provisional seat**" if r.champion_dsr < protocol.DSR_THRESHOLD else "")
        )
    if r.holdout_t is not None:
        lines.append(
            f"- Holdout gate: candidate {r.holdout['sharpe']:+.2f} vs champion "
            f"{r.champion_holdout_sharpe:+.2f}, delta {r.holdout_delta:+.3f}, "
            f"paired SE {r.holdout_se}, rho {r.holdout_rho}, "
            f"**t {r.holdout_t:+.2f}** (veto below -{protocol.HOLDOUT_VETO_T})"
        )
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
        print(
            f"  deflated sharpe prob: {result.dsr}  (trial #{result.n_trials}, "
            f"{result.n_effective_trials:g} effective)"
        )
    if result.champion_val_sharpe is not None:
        print(f"  champion validation sharpe: {result.champion_val_sharpe:+.2f}")
    if result.champion_dsr is not None:
        flag = " [provisional]" if result.champion_dsr < protocol.DSR_THRESHOLD else ""
        print(f"  champion re-deflated at the same bar: {result.champion_dsr}{flag}")
    if result.holdout:
        print(fmt_split("holdout   ", protocol._public(result.holdout)))
        print("  (holdout read by the holdout gate — logged)")
    if result.holdout_t is not None:
        print(
            f"  holdout gate: champion {result.champion_holdout_sharpe:+.2f}, "
            f"delta {result.holdout_delta:+.3f}, SE {result.holdout_se}, "
            f"rho {result.holdout_rho}, t {result.holdout_t:+.2f} "
            f"(veto below -{protocol.HOLDOUT_VETO_T})"
        )
    if result.verdict == "HOLDOUT_VETO":
        print(
            "  the champion was NOT replaced. This session has now seen a holdout\n"
            "  number: stop here — every later candidate would be holdout-informed."
        )

    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    if not JOURNAL.exists():
        JOURNAL.write_text("# Experiment Journal\n\nAppend-only. Newest entries last.\n\n")
    with open(JOURNAL, "a") as f:
        f.write(journal_entry(result))
    print(f"\njournal entry appended → {JOURNAL.relative_to(protocol.ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
