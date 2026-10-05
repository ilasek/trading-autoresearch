#!/usr/bin/env python
"""Before/after table for every recorded trial: protocol v1 vs protocol v2.

    python scripts/protocol_v2_comparison.py

Reads experiments/protocol_v2/rescore.jsonl (scripts/rescore_protocol_v2.py)
and writes experiments/protocol_v2/comparison.csv and
reports/protocol-v2-comparison.md. Runs no strategy.

Before = V1: the trial re-run today on the legacy universe under protocol v1
(identical to its recorded result for 103 of 104 trials). After = V2m: the
point-in-time universe under protocol v2, the strategy seeing each name's
prices only while it was an index member. For the eight champions the exact
port (V2p: ranking restricted to eligible names) is shown alongside. Ranks are
by validation Sharpe among all recorded trials, 1 = best.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "experiments" / "protocol_v2"
CSV = OUT / "comparison.csv"
REPORT = ROOT / "reports" / "protocol-v2-comparison.md"
NULL_PASS = 0.90
#: re-scored from a commit whose candidate file already held trial #27's fix
SOURCE_MISMATCH = {26}


def load() -> pd.DataFrame:
    rows = [json.loads(x) for x in (OUT / "rescore.jsonl").read_text().splitlines() if x.strip()]
    return pd.DataFrame(rows).drop_duplicates(["key", "variant"], keep="last")


def metric(frame: pd.DataFrame, split: str, name: str) -> pd.Series:
    return frame[split].map(lambda d: (d or {}).get(name) if isinstance(d, dict) else None)


def build() -> pd.DataFrame:
    df = load()
    trials = df[df["trial"].notna()].copy()
    trials["trial"] = trials["trial"].astype(int)
    out = trials[trials["variant"] == "V1"].set_index("trial")[
        ["name", "family", "track", "recorded_verdict", "recorded_val_sharpe"]].copy()
    for tag, variant in (("before", "V1"), ("widened", "U"), ("after", "V2m")):
        v = trials[trials["variant"] == variant].set_index("trial")
        out[f"{tag}_val_sharpe"] = metric(v, "validation", "sharpe")
        out[f"{tag}_val_cagr"] = metric(v, "validation", "ann_return")
        out[f"{tag}_val_maxdd"] = metric(v, "validation", "max_drawdown")
        out[f"{tag}_train_sharpe"] = metric(v, "train", "sharpe")
        out[f"{tag}_null_pctile"] = metric(v, "bench", "null_pctile")
        out[f"{tag}_ir_vs_ew"] = metric(v, "bench", "ir_vs_ew")
        out[f"{tag}_stock_share"] = v["stock_share"]
    ported = df[df.get("kind").eq("ported") & df["variant"].eq("V2")].copy()
    ported["ports_trial"] = ported["ports_trial"].astype(int)
    ported = ported.set_index("ports_trial")
    out["ported_val_sharpe"] = metric(ported, "validation", "sharpe").reindex(out.index)
    out["ported_null_pctile"] = metric(ported, "bench", "null_pctile").reindex(out.index)

    out["rank_before"] = out["before_val_sharpe"].rank(ascending=False, method="min").astype(int)
    out["rank_after"] = out["after_val_sharpe"].rank(ascending=False, method="min").astype(int)
    out["rank_change"] = out["rank_before"] - out["rank_after"]      # + = moved up
    out["sharpe_change"] = out["after_val_sharpe"] - out["before_val_sharpe"]
    out["null90_before"] = out["before_null_pctile"] >= NULL_PASS
    out["null90_after"] = out["after_null_pctile"] >= NULL_PASS
    out["source_mismatch"] = out.index.isin(SOURCE_MISMATCH)
    out.index.name = "trial"
    return out.sort_values(["rank_after", "trial"])


def f2(x) -> str:
    return "—" if pd.isna(x) else f"{x:+.2f}"


def pc(x) -> str:
    return "—" if pd.isna(x) else f"{x:.0%}"


def arrow(n: int) -> str:
    return "=" if n == 0 else (f"▲{n}" if n > 0 else f"▼{-n}")


def table(rows: pd.DataFrame) -> str:
    head = ("| after | before | Δ rank | # | strategy | family | recorded verdict | val Sharpe before | "
            "val Sharpe after | Δ Sharpe | CAGR before | CAGR after | null %ile before | null %ile after |")
    lines = [head, "|" + "|".join(["---"] * (head.count("|") - 1)) + "|"]
    for t, r in rows.iterrows():
        name = r["name"] + (" †" if r["source_mismatch"] else "")
        if pd.notna(r["ported_val_sharpe"]):
            name += f" (ported {r['ported_val_sharpe']:+.2f})"
        lines.append(
            f"| {r['rank_after']} | {r['rank_before']} | {arrow(int(r['rank_change']))} | {t} | {name} | "
            f"{r['family']} | {r['recorded_verdict']} | {f2(r['before_val_sharpe'])} | "
            f"{f2(r['after_val_sharpe'])} | {f2(r['sharpe_change'])} | {pc(r['before_val_cagr'])} | "
            f"{pc(r['after_val_cagr'])} | {pc(r['before_null_pctile'])} | {pc(r['after_null_pctile'])} |")
    return "\n".join(lines)


def main() -> int:
    t = build()
    t.to_csv(CSV, float_format="%.4f")

    n = len(t)
    rho = t["rank_before"].corr(t["rank_after"], method="spearman")
    top10_before = set(t.nsmallest(10, "rank_before").index)
    top10_after = set(t.nsmallest(10, "rank_after").index)
    risers = t.sort_values("rank_change", ascending=False).head(10)
    fallers = t.sort_values("rank_change").head(10)
    fam = t.groupby("family").agg(
        trials=("name", "size"),
        before=("before_val_sharpe", "median"), after=("after_val_sharpe", "median"),
        rank_before=("rank_before", "median"), rank_after=("rank_after", "median"),
    ).sort_values("rank_after")

    def short(rows):
        lines = ["| # | strategy | family | rank before → after | val Sharpe before → after |",
                 "|---|---|---|---|---|"]
        for i, r in rows.iterrows():
            lines.append(f"| {i} | {r['name']} | {r['family']} | {r['rank_before']} → {r['rank_after']} "
                         f"({arrow(int(r['rank_change']))}) | {f2(r['before_val_sharpe'])} → "
                         f"{f2(r['after_val_sharpe'])} |")
        return "\n".join(lines)

    fam_lines = ["| family | trials | median val Sharpe before → after | median rank before → after |",
                 "|---|---|---|---|"]
    for f, r in fam.iterrows():
        fam_lines.append(f"| {f} | {int(r['trials'])} | {f2(r['before'])} → {f2(r['after'])} | "
                         f"{r['rank_before']:.0f} → {r['rank_after']:.0f} |")

    md = f"""# Protocol v1 vs v2: every trial, before and after

_Generated by `scripts/protocol_v2_comparison.py` from `experiments/protocol_v2/rescore.jsonl`;
machine-readable copy in `experiments/protocol_v2/comparison.csv`._

**Before** is protocol v1: the legacy universe of today's ~140 constituents (each trial re-run on
today's data; identical to its recorded result for 103 of {n} trials). **After** is protocol v2: the
point-in-time universe, with the strategy seeing a name's prices only while it was an index member
(V2m). For the eight champions the exact port, which ranks only eligible names, is shown in brackets.
Ranks are by validation Sharpe (2018–2023) among all {n} trials, 1 = best. Δ rank ▲ = moved up.
"Null %ile" is where the validation Sharpe falls among 200 random-selection portfolios built exactly
like the strategy from the same pool; protocol v2 requires ≥ 90%.

## How the order changed

- Spearman rank correlation, before vs after: **{rho:+.2f}**.
- Of the 10 best trials before, **{len(top10_before & top10_after)}** are still in the top 10 after.
- Median validation Sharpe: {f2(t['before_val_sharpe'].median())} before → {f2(t['after_val_sharpe'].median())} after;
  best: {f2(t['before_val_sharpe'].max())} → {f2(t['after_val_sharpe'].max())}.
- Trials at or above the 90% null: {int(t['null90_before'].sum())} before → {int(t['null90_after'].sum())} after.

### Biggest risers

{short(risers)}

### Biggest fallers

{short(fallers)}

### By family

{chr(10).join(fam_lines)}

## All trials, ordered by rank after

{table(t)}

† Trial #26 was rebuilt from a commit whose candidate file already contained trial #27's fix, so its
"before" (1.05) differs from its recorded 1.01.
"""
    REPORT.write_text(md)
    print(f"wrote {REPORT.relative_to(ROOT)} and {CSV.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
