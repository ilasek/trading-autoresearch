#!/usr/bin/env python
"""Summarise experiments/protocol_v2/rescore.jsonl into the protocol-v2 report.

    python scripts/protocol_v2_report.py

Writes reports/protocol-v2-survivorship.md and experiments/protocol_v2/summary.json.
Reads only the re-scoring output and the membership files; runs no strategy.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import data, membership  # noqa: E402

OUT = ROOT / "experiments" / "protocol_v2"
REPORT = ROOT / "reports" / "protocol-v2-survivorship.md"
SUMMARY = OUT / "summary.json"
NULL_PASS = 0.90


def load_rows() -> pd.DataFrame:
    rows = [json.loads(line) for line in (OUT / "rescore.jsonl").read_text().splitlines() if line.strip()]
    # a re-run appends; the last row per (key, variant) wins
    df = pd.DataFrame(rows).drop_duplicates(["key", "variant"], keep="last")
    return df


def flat(df: pd.DataFrame) -> pd.DataFrame:
    out = df[["key", "variant", "trial", "name", "family", "track", "kind", "ports_trial",
              "recorded_verdict", "recorded_train_sharpe", "recorded_val_sharpe",
              "recorded_holdout_sharpe", "stock_share", "error"]].copy() \
        if "kind" in df else df.copy()
    for split in ("train", "validation", "holdout"):
        for m in ("sharpe", "ann_return", "max_drawdown", "avg_positions", "ann_turnover"):
            out[f"{split[:3]}_{m}"] = df[split].map(lambda d: (d or {}).get(m) if isinstance(d, dict) else None) \
                if split in df else None
    for m in ("null_p50", "null_p90", "null_pctile", "ew_sharpe", "ir_vs_ew", "pool_median"):
        out[m] = df["bench"].map(lambda d: (d or {}).get(m) if isinstance(d, dict) else None)
    out["gates_ok"] = df["gate_fails"].map(lambda g: isinstance(g, list) and not g)
    out["null_ok"] = out["null_pctile"] >= NULL_PASS
    return out


def f2(x, nd=2):
    return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:+.{nd}f}"


def pct(x):
    return "—" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.0%}"


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in r.values) + " |")
    return "\n".join(lines)


def spearman(a: pd.Series, b: pd.Series) -> float:
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return float("nan")
    return float(a[m].rank().corr(b[m].rank()))


def main() -> int:
    raw = load_rows()
    df = flat(raw)
    trials = df[df["trial"].notna()].copy()
    trials["trial"] = trials["trial"].astype(int)
    wide = trials.pivot_table(index="trial", columns="variant",
                              values=["val_sharpe", "tra_sharpe", "null_pctile", "ir_vs_ew", "stock_share"],
                              aggfunc="first")
    meta = trials.drop_duplicates("trial").set_index("trial")[
        ["name", "family", "track", "recorded_verdict", "recorded_val_sharpe", "recorded_train_sharpe"]]
    errors = trials[trials["error"].notna()][["trial", "name", "variant", "error"]]
    summary: dict = {}

    # ---------------- data coverage
    cov = pd.read_csv(membership.MEMBERSHIP_DIR / "coverage.csv", parse_dates=["date"])
    allc = cov[cov["index"] == "all"].set_index("date")
    yearly = allc.groupby(allc.index.year).last()
    cov_rows = yearly.loc[[y for y in (1996, 1998, 2000, 2003, 2006, 2008, 2009, 2012, 2015, 2017, 2018,
                                       2020, 2023, 2025) if y in yearly.index]]
    by_index = cov[cov["date"].dt.month.eq(12) & cov["date"].dt.year.isin([2009, 2017, 2023])]
    by_index = by_index.pivot_table(index="index", columns=by_index["date"].dt.year, values="share_priced")
    iv = membership.load_intervals()
    uni = data.load_universe("pit")
    n_stocks = sum(1 for i in uni["instruments"] if i["type"] == "stock")
    summary["coverage"] = {int(y): float(r["share_priced"]) for y, r in yearly.iterrows()}

    # ---------------- reproduction (V1 today vs recorded)
    v1 = trials[trials["variant"] == "V1"].set_index("trial")
    drift = (v1["val_sharpe"] - v1["recorded_val_sharpe"]).dropna()
    summary["v1_drift"] = {"n": int(len(drift)), "max_abs": round(float(drift.abs().max()), 4),
                           "exact": int((drift.abs() < 0.0015).sum())}

    # ---------------- sanity
    sanity = df[df["kind"] == "sanity"]
    san_tab = []
    for name, g in sanity.groupby("name"):
        for v in ("V1", "U", "V2", "V2m"):
            r = g[g["variant"] == v]
            if r.empty:
                continue
            r = r.iloc[0]
            san_tab.append({"strategy": name, "variant": v, "train Sharpe": f2(r["tra_sharpe"]),
                            "val Sharpe": f2(r["val_sharpe"]), "null pctile": pct(r["null_pctile"]),
                            "null p90": f2(r["null_p90"]), "EW pool": f2(r["ew_sharpe"]),
                            "IR vs EW": f2(r["ir_vs_ew"]),
                            "passes v2 gates": "yes" if (r["gates_ok"] and r["null_ok"]) else "no"})
    san_df = pd.DataFrame(san_tab)
    summary["sanity"] = san_tab

    # ---------------- champion lineage
    ported = df[df["kind"] == "ported"]
    lineage = []
    for n in sorted(trials.loc[trials["recorded_verdict"] == "PROMOTE", "trial"].unique()):
        rows = trials[trials["trial"] == n].set_index("variant")
        p = ported[(ported["ports_trial"] == n)].set_index("variant")
        def g(frame, v, col):
            return frame.loc[v, col] if v in frame.index else None
        lineage.append({
            "trial": n, "name": meta.loc[n, "name"],
            "rec val": f2(meta.loc[n, "recorded_val_sharpe"]),
            "V1 val": f2(g(rows, "V1", "val_sharpe")), "U val": f2(g(rows, "U", "val_sharpe")),
            "V2m val": f2(g(rows, "V2m", "val_sharpe")), "V2p val": f2(g(p, "V2", "val_sharpe")),
            "V2p null": pct(g(p, "V2", "null_pctile")),
            "V1 hold": f2(g(rows, "V1", "hol_sharpe")), "U hold": f2(g(rows, "U", "hol_sharpe")),
            "V2m hold": f2(g(rows, "V2m", "hol_sharpe")), "V2p hold": f2(g(p, "V2", "hol_sharpe")),
            "V1 train": f2(g(rows, "V1", "tra_sharpe")), "V2p train": f2(g(p, "V2", "tra_sharpe")),
        })
    lin_df = pd.DataFrame(lineage)
    summary["lineage"] = lineage

    # decomposition for the current champion (last PROMOTE)
    champ_n = int(max(trials.loc[trials["recorded_verdict"] == "PROMOTE", "trial"]))
    cr = trials[trials["trial"] == champ_n].set_index("variant")
    cp = ported[ported["ports_trial"] == champ_n].set_index("variant")
    decomp = []
    for label, frame, v in (("legacy list (v1)", cr, "V1"), ("widened, today's members (U)", cr, "U"),
                            ("point-in-time, masked view (V2m)", cr, "V2m"),
                            ("point-in-time, ported (V2p)", cp, "V2")):
        if v not in frame.index:
            continue
        r = frame.loc[v]
        decomp.append({"universe": label, "train Sharpe": f2(r["tra_sharpe"]),
                       "val Sharpe": f2(r["val_sharpe"]), "val CAGR": pct(r["val_ann_return"]),
                       "val maxDD": pct(r["val_max_drawdown"]), "holdout Sharpe": f2(r["hol_sharpe"]),
                       "holdout CAGR": pct(r["hol_ann_return"]), "null pctile": pct(r["null_pctile"]),
                       "IR vs EW": f2(r["ir_vs_ew"])})
    dec_df = pd.DataFrame(decomp)
    summary["decomposition"] = {"trial": champ_n, "rows": decomp}

    # ---------------- all trials
    stats = []
    for v in ("V1", "U", "V2m"):
        t = trials[(trials["variant"] == v) & trials["error"].isna()]
        stats.append({
            "variant": v, "trials scored": len(t),
            "median train Sharpe": f2(t["tra_sharpe"].median()),
            "median val Sharpe": f2(t["val_sharpe"].median()),
            "median train−val gap": f2((t["tra_sharpe"] - t["val_sharpe"]).median()),
            "max val Sharpe": f2(t["val_sharpe"].max()),
            "beat null 80%": int((t["null_pctile"] >= 0.8).sum()),
            "beat null 90%": int((t["null_pctile"] >= 0.9).sum()),
            "beat null 95%": int((t["null_pctile"] >= 0.95).sum()),
            "pass all v2 gates": int((t["gates_ok"] & t["null_ok"]).sum()),
            "median IR vs EW": f2(t["ir_vs_ew"].median()),
        })
    stats_df = pd.DataFrame(stats)
    summary["all_trials"] = stats

    vs = wide["val_sharpe"]
    rho_v1_v2 = spearman(vs.get("V1"), vs.get("V2m"))
    rho_v1_u = spearman(vs.get("V1"), vs.get("U"))
    summary["rank_agreement"] = {"V1_vs_V2m": round(rho_v1_v2, 3), "V1_vs_U": round(rho_v1_u, 3)}

    # null gate verdict flips between V1 and V2m
    npct = wide["null_pctile"]
    flips = pd.DataFrame({"name": meta["name"], "family": meta["family"],
                          "V1 val": vs.get("V1"), "V2m val": vs.get("V2m"),
                          "V1 null": npct.get("V1"), "V2m null": npct.get("V2m")})
    flips["V1 pass"] = flips["V1 null"] >= NULL_PASS
    flips["V2m pass"] = flips["V2m null"] >= NULL_PASS
    changed = flips[flips["V1 pass"] != flips["V2m pass"]]
    summary["null_flips"] = {"v1_only": int((flips["V1 pass"] & ~flips["V2m pass"]).sum()),
                             "v2_only": int((~flips["V1 pass"] & flips["V2m pass"]).sum())}

    # top trials per variant
    top = flips.sort_values("V2m val", ascending=False).head(12).reset_index()
    top_tab = pd.DataFrame({
        "trial": top["trial"], "name": top["name"], "family": top["family"],
        "V1 val": top["V1 val"].map(f2), "V2m val": top["V2m val"].map(f2),
        "V1 null": top["V1 null"].map(pct), "V2m null": top["V2m null"].map(pct)})

    # by family
    fam = flips.groupby("family").agg(n=("name", "size"), v1=("V1 val", "median"), v2=("V2m val", "median"),
                                      v2null=("V2m null", "median")).sort_values("v2", ascending=False)
    fam_tab = pd.DataFrame({"family": fam.index, "trials": fam["n"].values,
                            "median V1 val": fam["v1"].map(f2).values,
                            "median V2m val": fam["v2"].map(f2).values,
                            "median V2m null pctile": fam["v2null"].map(pct).values})
    # exposure: stock share vs Sharpe drop
    ss = wide["stock_share"].get("V1")
    drop = (vs.get("V1") - vs.get("V2m"))
    expo = pd.DataFrame({"stock_share": ss, "drop": drop}).dropna()
    rho_expo = spearman(expo["stock_share"], expo["drop"]) if len(expo) > 3 else float("nan")
    summary["stock_share_vs_drop_spearman"] = round(rho_expo, 3)

    # holdout agreement across the champions
    def agree(val_col, hol_col, frame):
        return spearman(frame[val_col], frame[hol_col])
    ch = pd.DataFrame(lineage).replace("—", np.nan)
    for c in ch.columns:
        if c not in ("trial", "name", "V2p null"):
            ch[c] = pd.to_numeric(ch[c], errors="coerce")
    hold_agree = {v: round(agree(f"{v} val", f"{v} hold", ch), 3) for v in ("V1", "U", "V2m", "V2p")}
    summary["val_holdout_rank_agreement_champions"] = hold_agree

    SUMMARY.write_text(json.dumps(summary, indent=2, default=str) + "\n")

    # ---------------- markdown
    md = [
        "# Protocol v2: survivorship bias, measured and removed",
        "",
        f"_Generated by `scripts/protocol_v2_report.py` from `experiments/protocol_v2/rescore.jsonl` "
        f"({len(trials['trial'].unique())} recorded trials re-scored)._",
        "",
        *([(OUT / "assessment.md").read_text().rstrip(), ""] if (OUT / "assessment.md").exists() else []),
        "## Data: the point-in-time universe",
        "",
        f"- {len(iv)} membership spells over {iv['id'].nunique()} instruments in 9 indices "
        f"(S&P 500 from 1996; DAX, CAC 40, FTSE 100, SMI, AEX, Euro Stoxx 50, Nikkei 225, Hang Seng from 2009).",
        f"- {n_stocks} of them have usable Yahoo prices and form `data/universe_pit.yaml` (plus the legacy ETFs).",
        "- Share of each date's index members that Yahoo can price — the survivorship bias that remains:",
        "",
        md_table(pd.DataFrame({"year-end": cov_rows.index, "members": cov_rows["members"].values,
                               "priced": cov_rows["priced"].values,
                               "share priced": [pct(x) for x in cov_rows["share_priced"].values]})),
        "",
        md_table(by_index.map(pct).reset_index().rename(columns={"index": "index"})),
        "",
        "## Reproduction",
        "",
        f"V1 re-runs today's data through the unchanged v1 protocol: {summary['v1_drift']['exact']} of "
        f"{summary['v1_drift']['n']} trials reproduce their recorded validation Sharpe to ±0.001; the "
        f"largest difference is {summary['v1_drift']['max_abs']:.3f} (see the caveats: a source-recovery "
        f"mismatch, not data drift).",
        "",
        "## Sanity strategies",
        "",
        md_table(san_df) if len(san_df) else "_not run_",
        "",
        f"## The current champion (trial #{champ_n}) by universe",
        "",
        md_table(dec_df),
        "",
        "## Champion lineage",
        "",
        "V2p = the champion with one change: it ranks only point-in-time eligible names "
        "(`experiments/protocol_v2/ported/`). Holdout was read only for these trials, all of "
        "which had it read at promotion.",
        "",
        md_table(lin_df),
        "",
        f"Validation→holdout rank agreement across the champions (Spearman, n={len(lin_df)}): "
        + ", ".join(f"{k} {v:+.2f}" for k, v in hold_agree.items()),
        "",
        "## All trials",
        "",
        md_table(stats_df),
        "",
        f"Rank agreement of validation Sharpe across trials: V1 vs U {rho_v1_u:+.2f}, V1 vs V2m {rho_v1_v2:+.2f}. "
        f"Spearman of a trial's V1 stock share with its V1→V2m Sharpe drop: {rho_expo:+.2f}.",
        "",
        f"Null-gate (90%) verdicts that change between V1 and V2m: {summary['null_flips']['v1_only']} pass only "
        f"under V1, {summary['null_flips']['v2_only']} pass only under V2m.",
        "",
        "### Best trials under V2m",
        "",
        md_table(top_tab),
        "",
        "### By family",
        "",
        md_table(fam_tab),
        "",
    ]
    if len(errors):
        md += ["### Trials that could not be re-scored", "", md_table(errors), ""]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(md) + "\n")
    print(f"wrote {REPORT.relative_to(ROOT)} and {SUMMARY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
