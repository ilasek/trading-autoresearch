#!/usr/bin/env python
"""Incremental data refresh — run daily by GitHub Actions, never by research agents.

Fetches only bars newer than what the store holds. Primary backend: batched
Yahoo (yfinance) requests. --source stooq uses per-series Stooq CSVs instead
(may be blocked by Stooq's browser check on some networks). Idempotent: reruns
are no-ops.

What is refreshed: every series of the legacy universe (data/universe.yaml),
plus the point-in-time universe's *live* series — ETFs, FX, and stocks with an
open membership spell. A stock that has left every tracked index is frozen:
its history stays (held positions stay valued, its past eligibility stands) but
it is no longer re-fetched, so the store stops churning on names no strategy
can buy. Writes go to the store's month files, so a refresh rewrites only the
current month.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data, membership

CHUNK = 50


def live_series() -> list[dict]:
    """Legacy series + the PIT universe's live ones, de-duplicated by id."""
    specs = {s["id"]: s for s in data.all_series("legacy")}
    if data.UNIVERSE_PIT_FILE.exists():
        iv = membership.load_intervals()
        open_ids = set(iv.loc[iv["end"].isna(), "id"])
        for s in data.all_series("pit"):
            if s["type"] != "stock" or s["id"] in open_ids:
                specs.setdefault(s["id"], s)
    return list(specs.values())


def stale_series(max_age_bdays: int) -> list[tuple[dict, pd.Timestamp]]:
    today = pd.Timestamp.today().normalize()
    out = []
    for spec in live_series():
        last = data.last_date(spec["id"])
        if last is None:
            print(f"  WARN {spec['id']}: not in store (run seed_data.py / build_membership.py); skipping")
            continue
        if len(pd.bdate_range(last, today)) - 1 > max_age_bdays:
            out.append((spec, last))
    return out


def refresh_yahoo(stale: list[tuple[dict, pd.Timestamp]]) -> int:
    updated = 0
    for i in range(0, len(stale), CHUNK):
        chunk = stale[i: i + CHUNK]
        since = min(last for _, last in chunk) + pd.Timedelta(days=1)
        by_yahoo = {spec["yahoo"]: (spec, last) for spec, last in chunk}
        try:
            frames = data.fetch_yahoo_batch(list(by_yahoo), start=since.strftime("%Y-%m-%d"))
        except Exception as e:  # noqa: BLE001 — one bad batch must not stop the refresh
            print(f"  WARN batch {i // CHUNK}: {type(e).__name__}: {e}")
            continue
        new_rows = {}
        for ysym, (spec, last) in by_yahoo.items():
            df = frames.get(ysym)
            if df is None:
                # Usually a delisting. Keep the history; report it so the
                # membership update (or a human) can confirm.
                print(f"  WARN {spec['id']}: Yahoo returned no data for {ysym}")
                continue
            new = df[df.index > last]
            if len(new):
                new_rows[spec["id"]] = new
        data.write_many(new_rows)
        updated += len(new_rows)
        for sid, new in new_rows.items():
            print(f"  ok {sid}: +{len(new)} rows through {new.index[-1].date()}")
    return updated


def refresh_stooq(stale: list[tuple[dict, pd.Timestamp]]) -> int:
    updated = 0
    new_rows = {}
    for spec, last in stale:
        try:
            df = data.fetch_stooq(spec["stooq"], start=(last + pd.Timedelta(days=1)).strftime("%Y-%m-%d"))
        except data.RateLimitError as e:
            print(f"STOP (stooq): {e}")
            break
        except Exception as e:
            print(f"  WARN {spec['id']}: {type(e).__name__}: {e}")
            continue
        new = df[df.index > last]
        if len(new):
            new_rows[spec["id"]] = new
            updated += 1
            print(f"  ok {spec['id']}: +{len(new)} rows through {new.index[-1].date()}")
    data.write_many(new_rows)
    return updated


def report_stopped(max_gap_bdays: int = 10) -> None:
    """Live series whose last bar is well behind the store's newest bar."""
    lasts = {s["id"]: data.last_date(s["id"]) for s in live_series()}
    lasts = {k: v for k, v in lasts.items() if v is not None}
    if not lasts:
        return
    newest = max(lasts.values())
    stopped = sorted(k for k, v in lasts.items() if len(pd.bdate_range(v, newest)) - 1 > max_gap_bdays)
    if stopped:
        print(f"  {len(stopped)} live series stopped updating (> {max_gap_bdays} bdays behind): "
              + ", ".join(stopped[:30]) + (" …" if len(stopped) > 30 else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-bdays", type=int, default=0,
                    help="refresh series more than N business days behind today")
    ap.add_argument("--source", choices=["yahoo", "stooq"], default="yahoo")
    args = ap.parse_args()

    stale = stale_series(args.max_age_bdays)
    print(f"{len(stale)} series need refresh")
    if stale:
        if args.source == "stooq":
            stale = [(s, last) for s, last in stale if s.get("stooq")]
        updated = (refresh_yahoo if args.source == "yahoo" else refresh_stooq)(stale)
        print(f"Done. updated={updated}/{len(stale)}")
    report_stopped()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
