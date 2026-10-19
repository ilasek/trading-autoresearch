#!/usr/bin/env python
"""Weekly leaderboard: every evaluated strategy ranked with error bars, plus
the top strategies against the S&P 500 — a ready-to-paste report section.

    python scripts/weekly_board.py --out /tmp/board.md --chart reports/charts/2026-W43-vs-sp500.svg
    python scripts/weekly_board.py --top 4          # how many strategies the chart shows

Everything comes from stored **validation** returns (2018–2023); nothing is
re-run and no split is read:

- v3 trials: `experiments/trial_returns/` (as `scripts/rank_trials.py`);
- v1/v2 trials: their protocol-v3 re-scoring, `experiments/protocol_v3/`
  (`scripts/rescore_protocol_v3.py`), so every trial is scored under the same
  execution, costs and cash rate on the same days.

Trials the re-scoring flagged `confined` (restricted to the legacy names, which
are known survivors) are listed apart: their edge is survivorship, and ranking
them with the rest would push every honest trial out of tier 1.

The chart takes the best trial of each of the top `--top` mechanisms (trials
whose active returns correlate >= 0.5 are one bet; five momentum variants on
one chart would be one line drawn five times) and plots growth of $1 over
validation against SPY (total return, no costs) and the equal-weight eligible
pool the skill numbers are measured against. SPY is cut at the validation end.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import data, metrics, protocol, ranking  # noqa: E402

RESCORE = ROOT / "experiments" / "protocol_v3"
SUMMARIES = ROOT / "reports" / "strategy-summaries.md"
REPORTS = ROOT / "reports"
VAL_START, VAL_END = protocol.SPLITS_V3["validation"]
BENCH = "SPY"


def label(version: int, j: int) -> str:
    """How the lab writes a trial's number: v1 trials bare, later ones prefixed."""
    return str(j) if version == 1 else f"v{version}-{j}"


def load_summaries() -> dict[tuple[str, str], str]:
    """{(label, name): plain-English line} from `reports/strategy-summaries.md`."""
    out = {}
    if not SUMMARIES.exists():
        return out
    for line in SUMMARIES.read_text().splitlines():
        m = re.match(r"\|\s*([\w, -]+?)\s*\|\s*`([^`]+)`\s*\|[^|]*\|\s*(.+?)\s*\|\s*$", line)
        if m:
            for lab in m.group(1).split(","):  # "32, 35": one row for identical trials
                out[(lab.strip(), m.group(2))] = m.group(3)
    return out


def collect() -> tuple[pd.DataFrame, pd.Series, pd.Series, dict, list]:
    """(validation returns by trial, pool, rf, meta, unscored trials)."""
    rescore = {}
    if (RESCORE / "rescore.jsonl").exists():
        for line in (RESCORE / "rescore.jsonl").read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                rescore[row["key"]] = row
    summaries = load_summaries()
    rets, meta, unscored = {}, {}, []
    pool = rf = None
    counters: dict[int, int] = {}
    for rec in protocol.recorded_trials(all_versions=True):
        v = protocol.record_version(rec)
        counters[v] = counters.get(v, 0) + 1
        j = counters[v]
        lab, name = label(v, j), rec.get("name", "")
        row = rescore.get(f"v{v}_t{j:03d}", {})
        frame = None
        if v == protocol.PROTOCOL_VERSION:
            frame = protocol.load_trial_frame(rec.get("ts", ""), name)
            if frame is not None and {"pool", "rf"} <= set(frame):
                pool, rf = frame["pool"], frame["rf"]
        else:
            path = RESCORE / "returns" / f"v{v}_t{j:03d}_validation.parquet"
            frame = pd.read_parquet(path) if path.exists() else None
        if frame is None or len(frame) < 100:
            unscored.append((lab, name, rec.get("family"), rec.get("verdict")))
            continue
        rets[lab] = frame["ret"]
        meta[lab] = {"name": name, "version": v, "family": rec.get("family"),
                     "verdict": rec.get("verdict"), "confined": bool(row.get("confined")),
                     "summary": summaries.get((lab, name), "—")}
    if pool is None:
        raise SystemExit("no protocol-v3 trial with a stored pool and cash rate")
    return pd.DataFrame(rets), pool, rf, meta, unscored


def vs_pool(r) -> str:
    if r.skill_lo > 0:
        return "better"
    if r.skill_hi < 0:
        return "worse"
    return "can't tell"


def table_md(table: pd.DataFrame, meta: dict, tiers: bool) -> list[str]:
    head = "| # | tier | trial | strategy | family | verdict | mech. | val Sharpe | skill [90% CI] | vs pool | what it does |"
    if not tiers:
        head = head.replace(" tier |", "").replace(" mech. |", "")
    lines = [head, "|" + "---|" * (head.count("|") - 1)]
    for i, (lab, r) in enumerate(table.iterrows(), 1):
        m = meta[lab]
        cells = [str(i), str(int(r.tier)), lab, f"`{m['name']}`", m["family"] or "—",
                 f"{m['verdict']} (v{m['version']})", f"M{int(r.mechanism)}", f"{r.sharpe:+.2f}",
                 f"{r.skill:+.2f} [{r.skill_lo:+.2f}, {r.skill_hi:+.2f}]", vs_pool(r), m["summary"]]
        if not tiers:
            del cells[6], cells[1]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def spy_returns(index: pd.DatetimeIndex) -> pd.Series:
    """SPY daily returns on the strategies' calendar, validation window only."""
    close = data.load_ohlcv(BENCH)["close"].loc[:VAL_END].dropna()
    days = close.index.union(index)
    px = close.reindex(days).ffill()
    return px.pct_change().reindex(index).fillna(0.0)


def stats(r: pd.Series, rf: pd.Series) -> dict:
    eq = (1 + r).cumprod()
    years = len(r) / 252
    return {"total": eq.iloc[-1] - 1, "cagr": eq.iloc[-1] ** (1 / years) - 1,
            "vol": r.std(ddof=1) * np.sqrt(252), "sharpe": metrics.sharpe(r, rf),
            "maxdd": float((eq / eq.cummax() - 1).min())}


# Reference palette (categorical slots 1-4, light surface), benchmark in ink.
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]


def chart_svg(lines: list[tuple[str, pd.Series, str, str]], title: str, subtitle: str) -> str:
    """Static SVG line chart: [(label, equity, color, style)], style 'solid'|'bench'|'pool'."""
    title, subtitle = html.escape(title), html.escape(subtitle)
    w, h = 900, 520
    ml, mr, mt, mb = 56, 280, 78, 44
    pw, ph = w - ml - mr, h - mt - mb
    idx = lines[0][1].index
    lo = min(float(s.min()) for _, s, _, _ in lines)
    hi = max(float(s.max()) for _, s, _, _ in lines)
    step = 0.25 if hi - lo < 1.5 else 0.5
    y0, y1 = np.floor(lo / step) * step, np.ceil(hi / step) * step
    t0, t1 = idx[0].value, idx[-1].value
    X = lambda t: ml + (t - t0) / (t1 - t0) * pw  # noqa: E731
    Y = lambda v: mt + (y1 - v) / (y1 - y0) * ph  # noqa: E731
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
           f'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif">',
           f'<rect width="{w}" height="{h}" fill="{SURFACE}"/>',
           f'<text x="{ml}" y="30" font-size="18" font-weight="600" fill="{INK}">{title}</text>',
           f'<text x="{ml}" y="52" font-size="13" fill="{INK2}">{subtitle}</text>']
    for v in np.arange(y0, y1 + 1e-9, step):
        out.append(f'<line x1="{ml}" x2="{ml + pw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<text x="{ml - 8}" y="{Y(v) + 4:.1f}" font-size="12" fill="{INK2}" text-anchor="end">${v:.2f}</text>')
    for yr in range(idx[0].year, idx[-1].year + 1):
        t = pd.Timestamp(f"{yr}-01-01").value
        if t0 <= t <= t1:
            out.append(f'<text x="{X(t):.1f}" y="{mt + ph + 22}" font-size="12" fill="{INK2}" text-anchor="middle">{yr}</text>')
    if y0 <= 1 <= y1:
        out.append(f'<line x1="{ml}" x2="{ml + pw}" y1="{Y(1):.1f}" y2="{Y(1):.1f}" stroke="{MUTED}" stroke-width="1"/>')
    ends = []
    for lab, s, color, style in lines:
        wk = s.resample("W").last().dropna()
        pts = " ".join(f"{X(t.value):.1f},{Y(v):.1f}" for t, v in wk.items())
        width = 2.5 if style == "bench" else 2
        dash = ' stroke-dasharray="6 4"' if style == "pool" else ""
        out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" '
                   f'stroke-linejoin="round" stroke-linecap="round"{dash}/>')
        ends.append([Y(float(s.iloc[-1])), html.escape(lab), color, float(s.iloc[-1])])
        out.append(f'<circle cx="{X(t1):.1f}" cy="{Y(float(s.iloc[-1])):.1f}" r="4" fill="{color}" '
                   f'stroke="{SURFACE}" stroke-width="2"/>')
    # direct labels at the line ends, nudged apart so none collide
    ends.sort(key=lambda e: e[0])
    for k in range(1, len(ends)):
        ends[k][0] = max(ends[k][0], ends[k - 1][0] + 30)
    for k in range(len(ends) - 2, -1, -1):
        ends[k][0] = min(ends[k][0], ends[k + 1][0] - 30)
    for ly, lab, color, v in ends:
        x = ml + pw + 14
        out.append(f'<line x1="{x}" x2="{x + 14}" y1="{ly:.1f}" y2="{ly:.1f}" stroke="{color}" stroke-width="3"/>')
        out.append(f'<text x="{x + 20}" y="{ly - 2:.1f}" font-size="11.5" font-weight="600" fill="{INK}">{lab}</text>')
        out.append(f'<text x="{x + 20}" y="{ly + 12:.1f}" font-size="11" fill="{INK2}">${v:.2f}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=None, help="write the markdown section here (default: stdout)")
    ap.add_argument("--chart", type=Path, default=REPORTS / "charts" / "top-vs-sp500.svg")
    ap.add_argument("--top", type=int, default=4, choices=range(1, len(SERIES) + 1))
    args = ap.parse_args()

    rets, pool, rf, meta, unscored = collect()
    open_ = [c for c in rets if not meta[c]["confined"]]
    conf = [c for c in rets if meta[c]["confined"]]
    table = ranking.rank_table(rets[open_], pool, rf)
    ctable = ranking.rank_table(rets[conf], pool, rf) if conf else None

    # chart: best trial of each of the top mechanisms
    picks = table.sort_values("skill", ascending=False).drop_duplicates("mechanism").head(args.top)
    days = rets.index
    spy = spy_returns(days)
    series = [(f"{lab} {meta[lab]['name']}", rets[lab].fillna(0.0), SERIES[k], "solid")
              for k, lab in enumerate(picks.index)]
    series += [("S&P 500 (SPY)", spy, INK, "bench"), ("Equal-weight pool", pool.reindex(days).fillna(0.0), MUTED, "pool")]
    curves = [(lab.replace(" ", " · ", 1) if s == "solid" else lab, (1 + r).cumprod(), c, s)
              for lab, r, c, s in series]
    args.chart.parent.mkdir(parents=True, exist_ok=True)
    args.chart.write_text(chart_svg(
        curves, "Top strategies vs the S&P 500 — growth of $1",
        f"Validation {days[0]:%b %Y}–{days[-1]:%b %Y}, net of costs. Best trial of each of the top "
        f"{len(picks)} mechanisms; SPY total return, no costs."))

    link = os.path.relpath(args.chart.resolve(), REPORTS)
    n1 = int((table["tier"] == 1).sum())
    md = ["## Strategy leaderboard — every evaluated strategy", "",
          f"_Generated by `scripts/weekly_board.py` from stored validation returns "
          f"({VAL_START[:4]}–{VAL_END[:4]}, {table.attrs['n_days']} days): v3 trials as recorded, v1/v2 trials "
          f"from their protocol-v3 re-scoring. Nothing was re-run; no holdout data was read._", "",
          f"![Top strategies vs the S&P 500]({link})", "",
          "| line | trial | val Sharpe | skill [90% CI] | total return | CAGR | volatility | max drawdown |",
          "|---|---|---|---|---|---|---|---|"]
    for (lab, r, _, style) in series:
        s = stats(r, rf.reindex(days).fillna(0.0))
        if style == "solid":
            t = table.loc[lab.split(" ")[0]]
            name, sk = f"`{lab}` (M{int(t.mechanism)})", f"{t.skill:+.2f} [{t.skill_lo:+.2f}, {t.skill_hi:+.2f}]"
        else:
            name, sk = lab, ("+0.00 (the baseline)" if style == "pool" else "—")
        md.append(f"| {'strategy' if style == 'solid' else 'benchmark'} | {name} | {s['sharpe']:+.2f} | {sk} | "
                  f"{s['total']:+.0%} | {s['cagr']:+.1%} | {s['vol']:.1%} | {s['maxdd']:.0%} |")
    md += ["", "Sharpe is in excess of T-bills. **Skill is Sharpe minus the equal-weight pool's**, the "
           "number every strategy here is judged on; the S&P 500 is shown for orientation, not as the bar.", "",
           "**How to read the ranking.** Sorted by tier, then skill. Tier 1 is the set the data cannot "
           "separate from the best (10% model confidence set) — **order inside tier 1 is not evidence**. "
           "Tier 2 is outside it with a skill interval above zero; tier 3 is everything else. \"vs pool\" "
           "reads the 90% interval: better / worse only when the whole interval is on one side of zero. "
           "\"mech.\" groups trials whose active returns correlate ≥ 0.5 — one mechanism under several "
           "labels is one bet. Verdict is as recorded, under the protocol version shown.", "",
           f"Equal-weight pool validation Sharpe: {table.attrs['pool_sharpe']:+.2f}. "
           f"{n1} of {len(table)} trials are in tier 1.", "",
           f"### A. All {len(table)} ranked trials", ""]
    md += table_md(table, meta, tiers=True)
    if ctable is not None:
        md += ["", f"### B. {len(ctable)} confined trials (survivorship-contaminated — not comparable)", "",
               "These picked only from the legacy names, which are known survivors; their skill is not "
               "evidence of a method. Shown for completeness, sorted by skill, not tiered.", ""]
        md += table_md(ctable.sort_values("skill", ascending=False), meta, tiers=False)
    if unscored:
        md += ["", f"### C. {len(unscored)} trials with no stored validation returns", "",
               "| trial | strategy | family | verdict |", "|---|---|---|---|"]
        md += [f"| {lab} | `{name}` | {fam or '—'} | {ver} |" for lab, name, fam, ver in unscored]
    missing = [f"{lab} `{meta[lab]['name']}`" for lab in rets if meta[lab]["summary"] == "—"]
    if missing:
        md += ["", f"_No plain-English summary yet in `reports/strategy-summaries.md` for: {', '.join(missing)}._"]
    text = "\n".join(md) + "\n"
    if args.out:
        args.out.write_text(text)
        print(f"written → {args.out}; chart → {args.chart}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
