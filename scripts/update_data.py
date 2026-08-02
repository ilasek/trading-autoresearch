#!/usr/bin/env python
"""Incremental data refresh — run daily by GitHub Actions, never by research agents.

Fetches only bars newer than what the store holds. Primary backend: one batched
Yahoo (yfinance) request for all stale series. --source stooq uses per-series
Stooq CSVs instead (may be blocked by Stooq's browser check on some networks).
Idempotent: reruns are no-ops.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data


def stale_series(max_age_bdays: int) -> list[tuple[dict, pd.Timestamp]]:
    today = pd.Timestamp.today().normalize()
    out = []
    for spec in data.all_series():
        last = data.last_date(spec["id"])
        if last is None:
            print(f"  WARN {spec['id']}: not in store (run seed_data.py); skipping")
            continue
        if len(pd.bdate_range(last, today)) - 1 > max_age_bdays:
            out.append((spec, last))
    return out


def refresh_yahoo(stale: list[tuple[dict, pd.Timestamp]]) -> int:
    since = min(last for _, last in stale) + pd.Timedelta(days=1)
    by_yahoo = {spec["yahoo"]: (spec, last) for spec, last in stale}
    frames = data.fetch_yahoo_batch(list(by_yahoo), start=since.strftime("%Y-%m-%d"))
    updated = 0
    for ysym, df in frames.items():
        spec, last = by_yahoo[ysym]
        new = df[df.index > last]
        if len(new):
            data.write_ohlcv(spec["id"], new)
            updated += 1
            print(f"  ok {spec['id']}: +{len(new)} rows through {new.index[-1].date()}")
    return updated


def refresh_stooq(stale: list[tuple[dict, pd.Timestamp]]) -> int:
    updated = 0
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
            data.write_ohlcv(spec["id"], new)
            updated += 1
            print(f"  ok {spec['id']}: +{len(new)} rows through {new.index[-1].date()}")
    return updated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-bdays", type=int, default=0,
                    help="refresh series more than N business days behind today")
    ap.add_argument("--source", choices=["yahoo", "stooq"], default="yahoo")
    args = ap.parse_args()

    stale = stale_series(args.max_age_bdays)
    print(f"{len(stale)} series need refresh")
    if not stale:
        return 0
    updated = (refresh_yahoo if args.source == "yahoo" else refresh_stooq)(stale)
    print(f"Done. updated={updated}/{len(stale)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
