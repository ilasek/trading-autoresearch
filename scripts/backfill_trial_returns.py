#!/usr/bin/env python
"""Reconstruct the per-trial validation return series for already-recorded trials.

`protocol.effective_n_trials` measures how redundant the search has been by
correlating trials' validation returns. Trials recorded before those series were
stored have none, and each counts as a fully independent trial — the
conservative default. This script re-runs each recorded candidate through the
same `evaluate_split` the protocol uses and writes the missing Parquet files.

It records no new trials, evaluates no holdout, and never rewrites
`experiments/trials.jsonl` — trial history stays append-only. Candidates whose
source file no longer exists are skipped and keep counting independently.

Usage: python scripts/backfill_trial_returns.py [--force] [--dry-run]
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data, protocol


def main() -> int:
    force = "--force" in sys.argv
    dry_run = "--dry-run" in sys.argv

    if not protocol.TRIALS_FILE.exists():
        print("no trials recorded yet — nothing to backfill")
        return 0

    records = [
        json.loads(line)
        for line in protocol.TRIALS_FILE.read_text().splitlines()
        if line.strip()
    ]

    todo = []
    for rec in records:
        if (rec.get("validation") or {}).get("sharpe_daily") is None:
            continue  # never scored (causality failure) — not part of the trial pool
        path = protocol.returns_path(rec.get("ts", ""), rec.get("name", ""))
        if path.exists() and not force:
            continue
        todo.append(rec)

    print(f"{len(records)} recorded trials, {len(todo)} need returns")
    if not todo:
        return 0
    if dry_run:
        for rec in todo:
            print(f"  would rebuild {rec['name']} from {rec['candidate']}")
        return 0

    print("Loading price data …")
    prices = data.load_prices()
    print(f"  {prices.shape[1]} instruments, {prices.index[0].date()} → {prices.index[-1].date()}")

    written = skipped = failed = 0
    for rec in todo:
        name = rec.get("name", "?")
        candidate = protocol.ROOT / rec["candidate"]
        if not candidate.exists():
            print(f"  SKIP {name}: candidate file {rec['candidate']} no longer exists")
            skipped += 1
            continue
        try:
            mod, _ = protocol.load_strategy(candidate)
            val = protocol.evaluate_split(mod.generate_weights, prices, "validation")
        except Exception as exc:  # noqa: BLE001 - report and continue over the batch
            print(f"  FAIL {name}: {type(exc).__name__}: {exc}")
            failed += 1
            continue

        recorded = float(rec["validation"]["sharpe_daily"])
        rebuilt = float(val["sharpe_daily"])
        drift = abs(rebuilt - recorded)
        out = protocol.store_trial_returns(rec.get("ts", ""), name, val["_returns"])
        # The recorded Sharpe stays authoritative; the rebuilt series is used only
        # for correlation clustering. Drift means the price store changed under a
        # past trial (revised adjusted closes), which is worth knowing about.
        flag = f"   ** sharpe drift {recorded:.6f} -> {rebuilt:.6f}" if drift > 1e-4 else ""
        print(f"  ok   {name} -> {out.relative_to(protocol.ROOT)}{flag}")
        written += 1

    print(f"\nwrote {written}, skipped {skipped}, failed {failed}")

    stored = [r for _, r in protocol.past_trials()]
    n_eff = protocol.effective_n_trials(stored)
    print(
        f"trial pool now {len(stored)} trials -> {n_eff:g} effective "
        f"(clustered at rho {protocol.TRIAL_CLUSTER_RHO})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
