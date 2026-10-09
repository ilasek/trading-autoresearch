#!/usr/bin/env python
"""Re-score every recorded trial, of every protocol version, under protocol v3.

    python scripts/rescore_protocol_v3.py                  # everything, resumable
    python scripts/rescore_protocol_v3.py --only v1_t098,v2_t006
    python scripts/rescore_protocol_v3.py --draws 50 --workers 3

An engine-maintenance measurement, not research: it runs no candidate through
`run_trial`, appends nothing to `experiments/trials.jsonl`, raises no one's
deflated bar, and **never reads the holdout split** (train and validation only).

Each trial is rebuilt exactly as it was run (its `strategies/` tree from the
commit that recorded it; see `rescore_protocol_v2.py`). Variants:
    V3m  v3 for code written before v2 (all v1 trials): the strategy sees each
         name's prices only while it is eligible, as in the v2 re-scoring's V2m;
         the backtest uses true prices and the v3 execution model.
    V3   v3 exactly as a new candidate faces it: v2 trials, the ported v1
         champions and the sanity strategies, all of which read `eligible`.

27 v1 trials read `strategies/lib/groups.py` and can only rank today's survivors
(`experiments/protocol_v2/legacy_share.jsonl`); they are flagged `confined` and
their numbers are survivorship-biased whatever the protocol.

Output: `experiments/protocol_v3/rescore.jsonl` (one row per task) and
`experiments/protocol_v3/returns/<key>_validation.parquet` (columns ret, pool),
which `ranking.rank_table` reads for the error-barred leaderboard. The cash rate
is used if the store has it; until the data-refresh workflow seeds it, rf = 0
and the rows say so.
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import json
import multiprocessing as mp
import signal
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import benchmarks, data, metrics, protocol  # noqa: E402

_spec = importlib.util.spec_from_file_location("rescore_v2", ROOT / "scripts" / "rescore_protocol_v2.py")
v2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v2)

OUT = ROOT / "experiments" / "protocol_v3"
_CTX: dict = {}


def confined_names() -> set[str]:
    path = ROOT / "experiments" / "protocol_v2" / "legacy_share.jsonl"
    if not path.exists():
        return set()
    rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    return {r["name"] for r in rows if (r.get("legacy_share_of_stock_weight") or 0) >= 0.999}


def build_context() -> dict:
    t = time.time()
    px = data.load_prices(universe="pit", start=protocol.PIT_PRICE_START)
    aux = data.load_panels(universe="pit", start=protocol.PIT_PRICE_START)
    exact = protocol.setup_v3(px, aux, require_rf=False)
    masked = dataclasses.replace(exact, mask_strategy_view=True)   # shares the pool cache
    print(f"context built in {time.time() - t:.0f}s (rf {'stored' if exact.rf is not None else 'missing: 0'})",
          flush=True)
    return {"V3": exact, "V3m": masked, "px": px, "aux": aux}


def _metrics(d: dict) -> dict:
    return {k: v for k, v in d.items() if not k.startswith("_")}


def score(gw, variant: str, draws: int) -> tuple[dict, dict]:
    setup, px, aux = _CTX[variant], _CTX["px"], _CTX["aux"]
    t = time.time()
    tr = protocol.evaluate_split(gw, px, "train", aux, setup)
    va = protocol.evaluate_split(gw, px, "validation", aux, setup)
    gates = protocol.apply_gates(tr, va, setup.gates)
    window = va["_returns"]
    sharpes, _ = benchmarks.random_null_v3(
        va["_targets"], va["_visible"], va["_eligible"], setup.types, setup.regions,
        setup.execution, (window.index[0], window.index[-1]), n_draws=draws,
        seed=protocol.NULL_SEED, max_leverage=protocol.ENGINE_PARAMS["max_leverage"])
    cand = metrics.sharpe(window, setup.rf)
    null = benchmarks.null_summary(cand, sharpes)
    bar = float(np.quantile(sharpes, 0.90))
    if cand <= bar:
        gates.append(f"null: validation sharpe {cand:.3f} <= the null's 90% quantile {bar:.3f}")
    boot = metrics.sharpe_diff_bootstrap(window, va["_pool"], setup.rf)
    row = {
        "train": _metrics(tr), "validation": _metrics(va), "gate_fails": gates,
        "passes_v3_gates": not gates, "null": null,
        "skill_se": round(boot["se"], 4), "skill_ci90": [round(boot["lo"], 3), round(boot["hi"], 3)],
        "rf": "stored" if setup.rf is not None else "missing (0)",
        "seconds": round(time.time() - t, 1),
    }
    return row, {"validation": pd.DataFrame({"ret": window, "pool": va["_pool"]})}


def _init_worker() -> None:
    global _CTX
    _CTX = build_context()


def _alarm(signum, frame):
    raise TimeoutError()


def run_task(task: dict) -> tuple[list[dict], dict]:
    """Score one task in a worker; the parent writes every file."""
    try:
        if task["kind"] == "trial":
            tree = v2.materialize(task["sha"])
            path = tree / task["candidate"]
        else:
            tree = v2.materialize(task["sha"]) if task.get("sha") else None
            path = Path(task["path"])
        mod = v2.load_module(path, tree)
    except Exception as e:  # noqa: BLE001
        return [{**task["meta"], "variant": task["variant"],
                 "error": f"load: {type(e).__name__}: {e}"}], {}
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(task.get("timeout", 0))
    try:
        row, frames = score(mod.generate_weights, task["variant"], task["draws"])
        out = [{**task["meta"], "variant": task["variant"], **row}]
        series = {f"{task['meta']['key']}_{k}.parquet": v for k, v in frames.items()}
    except TimeoutError:
        out, series = [{**task["meta"], "variant": task["variant"],
                        "error": f"timeout after {task['timeout']}s"}], {}
    except Exception as e:  # noqa: BLE001
        out, series = [{**task["meta"], "variant": task["variant"], "error": f"{type(e).__name__}: {e}",
                        "trace": traceback.format_exc()[-1500:]}], {}
    finally:
        signal.alarm(0)
    print(f"  done {task['meta']['key']}", flush=True)
    return out, series


def build_tasks(draws: int, only: set[str] | None) -> list[dict]:
    tasks = []
    confined = confined_names()
    per_version: dict[int, int] = {}
    for rec in protocol.recorded_trials(all_versions=True):
        ver = protocol.record_version(rec)
        per_version[ver] = per_version.get(ver, 0) + 1
        n = per_version[ver]
        key = f"v{ver}_t{n:03d}"
        if (rec.get("validation") or {}).get("sharpe") is None:
            continue                                  # never scored: causality failure
        if only and key not in only:
            continue
        meta = {"key": key, "version": ver, "trial": n, "name": rec.get("name"),
                "family": rec.get("family"), "track": rec.get("track", "challenge"),
                "recorded_verdict": rec.get("verdict"),
                "recorded_val_sharpe": rec["validation"].get("sharpe"),
                "recorded_train_sharpe": (rec.get("train") or {}).get("sharpe"),
                "confined": rec.get("name") in confined, "kind": "trial"}
        sha = v2.commit_for(rec)
        if sha is None:
            tasks.append({"kind": "missing", "meta": meta, "variant": "V3m"})
            continue
        tasks.append({"kind": "trial", "sha": sha, "candidate": rec["candidate"], "meta": meta,
                      "variant": "V3m" if ver == 1 else "V3", "draws": draws})
    v1 = [r for r in protocol.recorded_trials(1)]
    for d, kind in ((v2.SANITY_DIR, "sanity"), (v2.PORTED_DIR, "ported")):
        for path in sorted(d.glob("*.py")) if d.exists() else []:
            key = f"{kind}_{path.stem}"
            if only and key not in only:
                continue
            meta = {"key": key, "name": path.stem, "kind": kind, "family": kind,
                    "confined": path.stem.endswith("pt_mom_evar_arbrisk")}
            sha = None
            if kind == "ported":
                n = int(path.stem.split("_")[0][1:])
                meta["ports_trial"] = n
                sha = v2.commit_for(v1[n - 1])
            tasks.append({"kind": kind, "path": str(path), "sha": sha, "meta": meta,
                          "variant": "V3", "draws": draws})
    return tasks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated keys (v1_t098, v2_t006, sanity_..., ported_...)")
    ap.add_argument("--draws", type=int, default=50, help="random-selection null draws (v3 trials use 200)")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--out", default=str(OUT / "rescore.jsonl"))
    args = ap.parse_args()

    only = set(args.only.split(",")) if args.only else None
    tasks = build_tasks(args.draws, only)
    out = Path(args.out)
    if out.exists():                                  # resumable: skip error-free rows
        done = {r["key"] for r in map(json.loads, out.read_text().splitlines()) if r and not r.get("error")}
        tasks = [t for t in tasks if t["meta"]["key"] not in done]
    for t in tasks:
        t["timeout"] = args.timeout
    for sha in sorted({t["sha"] for t in tasks if t.get("sha")}):
        v2.materialize(sha)
    print(f"{len(tasks)} tasks", flush=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "a") as f:
        for t in [t for t in tasks if t["kind"] == "missing"]:
            f.write(json.dumps({**t["meta"], "variant": t["variant"],
                                "error": "no commit found for the trial record"}) + "\n")
        work = [t for t in tasks if t["kind"] != "missing"]

        def emit(res):
            rows, series = res
            for name, frame in series.items():
                p = OUT / "returns" / name
                p.parent.mkdir(parents=True, exist_ok=True)
                frame.to_parquet(p)
            for r in rows:
                f.write(json.dumps(r, default=str) + "\n")
            f.flush()

        if args.workers <= 1:
            global _CTX
            _CTX = build_context()
            for t in work:
                emit(run_task(t))
        else:
            ctx = mp.get_context("spawn")
            with ctx.Pool(args.workers, initializer=_init_worker) as pool:
                for res in pool.imap_unordered(run_task, work):
                    emit(res)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
