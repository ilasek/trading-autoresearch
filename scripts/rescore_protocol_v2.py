#!/usr/bin/env python
"""Re-score every recorded trial under protocol v1 (as of today) and protocol v2.

    python scripts/rescore_protocol_v2.py                     # all trials, train + validation
    python scripts/rescore_protocol_v2.py --only 1,35,98      # a subset (trial numbers, 1-based)
    python scripts/rescore_protocol_v2.py --champions-holdout # ALSO holdout, champions only

An engine-maintenance measurement, not research: it runs no candidate through
`run_trial`, appends nothing to `experiments/trials.jsonl`, and so raises no
one's deflated-Sharpe bar. Its output is a comparison of the two protocols.

Each trial's candidate is rebuilt exactly as it was run: the `strategies/`
tree (candidate plus `strategies/lib`) is taken from the commit that appended
the trial's record, not from today's working tree.

Variants (see reports/protocol-v2-survivorship.md):
    V1   legacy universe (today's ~140 constituents), protocol v1 splits and
         gates — a re-run today, to separate data drift from protocol change
    U    point-in-time universe file, but every *current* index member
         eligible for its whole price history — the widened, still
         survivorship-biased pool
    V2m  protocol v2 for code written before it: the strategy sees each name's
         prices only while it is eligible (so it cannot rank non-members), the
         backtest uses true prices. Conservative for new index joiners, which
         become rankable only once their lookback fills with in-index prices.
    V2   protocol v2 exactly as a new candidate faces it: true prices plus the
         `eligible` panel. Meaningful only for code that uses `eligible` — the
         sanity strategies and the ported champions (experiments/protocol_v2/
         ported/); unported code ranks non-members and the engine turns that
         weight into cash.

For every variant the validation split also gets the survivorship-matched
benchmarks (random-selection null, equal-weight eligible pool); for V1 the
pool is "every legacy name with a price".

Holdout is read only with --champions-holdout, and then only for trials that
were promoted (their holdout was already read at promotion). No other trial's
holdout is ever evaluated.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import multiprocessing as mp
import subprocess
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import benchmarks, data, membership, metrics, protocol  # noqa: E402

OUT = ROOT / "experiments" / "protocol_v2"
SRC_CACHE = ROOT / ".cache" / "rescore_src"
SANITY_DIR = OUT / "sanity"
PORTED_DIR = OUT / "ported"
VARIANTS = ("V1", "U", "V2m")

_CTX: dict = {}


# ---------------------------------------------------------------------------
# Sources as they were run
# ---------------------------------------------------------------------------

def trial_records() -> list[tuple[int, dict]]:
    recs = protocol.recorded_trials()
    return [(i + 1, r) for i, r in enumerate(recs)]


def commit_for(rec: dict) -> str | None:
    ts = rec.get("ts", "")[:19]
    out = subprocess.run(
        ["git", "log", "--reverse", "--format=%H", f"-S{ts}", "--", "experiments/trials.jsonl"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    return out[0] if out else None


def materialize(sha: str) -> Path:
    tree = SRC_CACHE / sha
    if not (tree / "data" / "universe.yaml").exists():
        tree.mkdir(parents=True, exist_ok=True)
        archive = subprocess.run(["git", "archive", sha, "strategies", "data/universe.yaml"], cwd=ROOT,
                                 capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", str(tree)], input=archive, check=True)
    return tree


def load_module(path: Path, tree: Path | None):
    """Import a strategy file with `strategies.*` resolved against `tree` (the
    commit's own strategies/ package), never against today's."""
    for name in [m for m in sys.modules if m == "strategies" or m.startswith("strategies.")]:
        del sys.modules[name]
    base = str(tree or ROOT)
    sys.path[:] = [p for p in sys.path if not p.startswith(str(SRC_CACHE))]
    sys.path.insert(0, base)
    spec = importlib.util.spec_from_file_location(f"cand_{abs(hash(str(path)))}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    _patch_groups()
    return mod


def _patch_groups() -> None:
    """strategies.lib.groups labels instruments from data/universe.yaml; give
    it the PIT universe's types and regions too, so a type- or region-demeaned
    signal scores the new names instead of silently dropping them. (Sector
    labels exist only for the legacy names: SECTOR_OF is left as it was.)"""
    g = sys.modules.get("strategies.lib.groups")
    if g is None:
        return
    for inst in data.load_universe("pit")["instruments"]:
        if hasattr(g, "TYPE_OF"):
            g.TYPE_OF.setdefault(inst["id"], inst["type"])
        if hasattr(g, "REGION_OF"):
            g.REGION_OF.setdefault(inst["id"], inst["region"])


# ---------------------------------------------------------------------------
# Evaluation contexts
# ---------------------------------------------------------------------------

def todays_members_intervals() -> pd.DataFrame:
    iv = membership.load_intervals()
    live = sorted(set(iv.loc[iv["end"].isna(), "id"]))
    return pd.DataFrame({"index": "today", "id": live, "start": pd.Timestamp("1900-01-01"),
                         "end": pd.NaT})


def _masked(setup: protocol.Setup) -> protocol.Setup:
    setup.mask_strategy_view = True
    return setup


def build_context() -> dict:
    t = time.time()
    legacy_px = data.load_prices(universe="legacy")
    legacy_aux = data.load_panels(universe="legacy")
    pit_px = data.load_prices(universe="pit", start=protocol.PIT_PRICE_START)
    pit_aux = data.load_panels(universe="pit", start=protocol.PIT_PRICE_START)
    ctx = {
        "V1": (protocol.setup_v1(), legacy_px, legacy_aux),
        "U": (protocol.setup_v2(pit_px, pit_aux, intervals=todays_members_intervals()), pit_px, pit_aux),
        "V2": (protocol.setup_v2(pit_px, pit_aux), pit_px, pit_aux),
        "V2m": (_masked(protocol.setup_v2(pit_px, pit_aux)), pit_px, pit_aux),
        "legacy_types": data.instrument_types("legacy"),
    }
    print(f"context built in {time.time() - t:.0f}s: legacy {legacy_px.shape}, pit {pit_px.shape}",
          flush=True)
    return ctx


def _metrics(d: dict) -> dict:
    return {k: v for k, v in d.items() if not k.startswith("_")}


def _bench(val: dict, setup: protocol.Setup, legacy_types: dict, draws: int) -> dict:
    """Random-selection null + equal-weight pool on the validation split."""
    held, visible, window = val["_held"], val["_visible"], val["_returns"]
    if setup.pit:
        elig, types = val["_eligible"], setup.types
    else:
        types = legacy_types
        known = pd.Index([c for c in visible.columns if types.get(c) in ("stock", "etf")])
        elig = visible.notna() & visible.columns.isin(known)
    sharpes, _ = benchmarks.random_null(held, visible, elig, types, n_draws=draws,
                                        seed=protocol.NULL_SEED)
    out = benchmarks.null_summary(metrics.sharpe(window), sharpes)
    ew = benchmarks.equal_weight(visible, elig, str(window.index[0].date()),
                                 str(window.index[-1].date()))
    out["ew_sharpe"] = round(metrics.sharpe(ew), 3)
    out["ir_vs_ew"] = round(metrics.sharpe(window - ew.reindex(window.index).fillna(0.0)), 3)
    # the null's pool: names on offer on a typical validation day
    out["pool_median"] = int(elig.reindex(window.index).sum(axis=1).median())
    return out


def score(gw, variant: str, holdout: bool, draws: int) -> tuple[dict, dict]:
    setup, px, aux = _CTX[variant]
    t = time.time()
    tr = protocol.evaluate_split(gw, px, "train", aux, setup)
    va = protocol.evaluate_split(gw, px, "validation", aux, setup)
    row = {
        "train": _metrics(tr), "validation": _metrics(va),
        "gate_fails": protocol.apply_gates(tr, va, protocol.GATES),
        "bench": _bench(va, setup, _CTX["legacy_types"], draws),
    }
    rets = {"validation": va["_returns"]}
    if holdout:
        ho = protocol.evaluate_split(gw, px, "holdout", aux, setup)
        row["holdout"] = _metrics(ho)
        rets["holdout"] = ho["_returns"]
    # stock share of validation holdings: how exposed the book is to the bias
    held = va["_held"]
    types = setup.types if setup.pit else _CTX["legacy_types"]
    stock_cols = [c for c in held.columns if types.get(c) == "stock"]
    gross = held.abs().sum(axis=1).sum()
    row["stock_share"] = round(float(held[stock_cols].abs().sum(axis=1).sum() / gross), 4) if gross else 0.0
    row["seconds"] = round(time.time() - t, 1)
    return row, rets


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def run_task(task: dict) -> list[dict]:
    rows = []
    try:
        if task["kind"] == "trial":
            tree = materialize(task["sha"])
            path = tree / task["candidate"]
        else:
            tree = materialize(task["sha"]) if task.get("sha") else None
            path = Path(task["path"])
        mod = load_module(path, tree)
    except Exception as e:  # noqa: BLE001
        return [{**task["meta"], "variant": v, "error": f"load: {type(e).__name__}: {e}"}
                for v in task["variants"]]
    for v in task["variants"]:
        try:
            row, rets = score(mod.generate_weights, v, task["holdout"], task["draws"])
            for split, r in rets.items():
                p = OUT / "returns" / f"{task['meta']['key']}_{v}_{split}.parquet"
                p.parent.mkdir(parents=True, exist_ok=True)
                r.rename("ret").to_frame().to_parquet(p)
            rows.append({**task["meta"], "variant": v, **row})
        except Exception as e:  # noqa: BLE001
            rows.append({**task["meta"], "variant": v,
                         "error": f"{type(e).__name__}: {e}",
                         "trace": traceback.format_exc()[-1500:]})
        print(f"  done {task['meta']['key']} {v}", flush=True)
    return rows


def build_tasks(args) -> list[dict]:
    tasks = []
    only = {int(x) for x in args.only.split(",")} if args.only else None
    variants = tuple(args.variants.split(","))
    if not args.skip_trials:
        for n, rec in trial_records():
            if only and n not in only:
                continue
            sha = commit_for(rec)
            meta = {
                "key": f"t{n:03d}", "trial": n, "name": rec.get("name"),
                "family": rec.get("family"), "track": rec.get("track", "challenge"),
                "recorded_verdict": rec.get("verdict"),
                "recorded_train_sharpe": (rec.get("train") or {}).get("sharpe"),
                "recorded_val_sharpe": (rec.get("validation") or {}).get("sharpe"),
                "recorded_holdout_sharpe": (rec.get("holdout") or {}).get("sharpe"),
                "commit": sha, "candidate": rec.get("candidate"),
            }
            if sha is None:
                tasks.append({"kind": "missing", "meta": meta, "variants": variants})
                continue
            tasks.append({
                "kind": "trial", "sha": sha, "candidate": rec["candidate"], "meta": meta,
                "variants": variants, "draws": args.draws,
                "holdout": args.champions_holdout and rec.get("verdict") == "PROMOTE",
            })
    records = dict(trial_records())
    for d, kind in ((SANITY_DIR, "sanity"), (PORTED_DIR, "ported")):
        if args.skip_extra or not d.exists():
            continue
        for path in sorted(d.glob("*.py")):
            meta = {"key": f"{kind}_{path.stem}", "trial": None, "name": path.stem, "kind": kind}
            sha = None
            if kind == "ported":
                meta["ports_trial"] = int(path.stem.split("_")[0][1:])
                sha = commit_for(records[meta["ports_trial"]])   # its strategies/lib as run
            extra_variants = tuple(dict.fromkeys(variants + ("V2",)))
            tasks.append({
                "kind": kind, "path": str(path), "sha": sha, "meta": meta, "variants": extra_variants,
                "draws": args.draws,
                "holdout": args.champions_holdout and kind == "ported",
            })
    return tasks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated trial numbers (1-based)")
    ap.add_argument("--variants", default=",".join(VARIANTS))
    ap.add_argument("--draws", type=int, default=protocol.NULL_DRAWS)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--champions-holdout", action="store_true",
                    help="also score holdout, for promoted trials (and their ports) only")
    ap.add_argument("--skip-trials", action="store_true")
    ap.add_argument("--skip-extra", action="store_true", help="skip sanity and ported strategies")
    ap.add_argument("--out", default=str(OUT / "rescore.jsonl"))
    args = ap.parse_args()

    tasks = build_tasks(args)
    print(f"{len(tasks)} tasks", flush=True)
    global _CTX
    _CTX = build_context()
    rows: list[dict] = []
    for t in tasks:
        if t["kind"] == "missing":
            rows += [{**t["meta"], "variant": v, "error": "no commit found for the trial record"}
                     for v in t["variants"]]
    work = [t for t in tasks if t["kind"] != "missing"]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "a") as f:
        for r in rows:
            f.write(json.dumps(r, default=str) + "\n")
        if args.workers <= 1:
            for t in work:
                for r in run_task(t):
                    f.write(json.dumps(r, default=str) + "\n")
                    f.flush()
        else:
            ctx = mp.get_context("fork")
            with ctx.Pool(args.workers, maxtasksperchild=4) as pool:
                for res in pool.imap_unordered(run_task, work):
                    for r in res:
                        f.write(json.dumps(r, default=str) + "\n")
                    f.flush()
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
