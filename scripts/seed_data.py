#!/usr/bin/env python
"""One-time bulk seed of the Parquet store. Primary backend: Yahoo (yfinance,
batched, full history). Secondary: Stooq (--source stooq) — note Stooq serves a
browser-verification page on some networks, in which case it simply fails.

Resumable: series already in the store are skipped unless --force.

Usage:
    python scripts/seed_data.py                 # seed everything missing via Yahoo
    python scripts/seed_data.py --limit 20      # smoke test
    python scripts/seed_data.py --only SPY,AAPL
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data

CHUNK = 25          # symbols per yfinance batch call
CHUNK_PAUSE = 3.0   # seconds between chunks — keeps us far from Yahoo limits


def seed_yahoo(missing: list[dict]) -> tuple[int, list[str]]:
    fetched, failed = 0, []
    for i in range(0, len(missing), CHUNK):
        chunk = missing[i : i + CHUNK]
        by_yahoo = {s["yahoo"]: s for s in chunk}
        try:
            frames = data.fetch_yahoo_batch(list(by_yahoo))
        except Exception as e:
            print(f"  WARN batch {i//CHUNK}: {type(e).__name__}: {e}")
            failed += [s["id"] for s in chunk]
            time.sleep(30)  # back off hard before the next chunk
            continue
        for spec in chunk:
            df = frames.get(spec["yahoo"])
            if df is None or df.empty:
                print(f"  WARN {spec['id']}: no data from Yahoo ({spec['yahoo']})")
                failed.append(spec["id"])
                continue
            data.write_ohlcv(spec["id"], df)
            fetched += 1
            print(f"  ok {spec['id']}: {len(df)} rows ({df.index[0].date()} → {df.index[-1].date()})")
        if i + CHUNK < len(missing):
            time.sleep(CHUNK_PAUSE)
    return fetched, failed


def seed_stooq(missing: list[dict]) -> tuple[int, list[str]]:
    fetched, failed = 0, []
    for spec in missing:
        try:
            df = data.fetch_stooq(spec["stooq"])
        except data.RateLimitError as e:
            print(f"\nSTOP (stooq): {e}\nRerun with --source yahoo or retry later.")
            break
        except Exception as e:
            print(f"  WARN {spec['id']}: {type(e).__name__}: {e}")
            failed.append(spec["id"])
            continue
        data.write_ohlcv(spec["id"], df)
        fetched += 1
        print(f"  ok {spec['id']}: {len(df)} rows")
    return fetched, failed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--only", type=str, default=None, help="comma-separated series ids")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--source", choices=["yahoo", "stooq"], default="yahoo")
    args = ap.parse_args()

    series = data.all_series()
    if args.only:
        wanted = {s.strip() for s in args.only.split(",")}
        series = [s for s in series if s["id"] in wanted]
    missing = [s for s in series if args.force or data.load_ohlcv(s["id"]) is None]
    skipped = len(series) - len(missing)
    if args.limit is not None:
        missing = missing[: args.limit]

    print(f"Seeding {len(missing)} series via {args.source} (skipping {skipped} already stored)")
    fetched, failed = (seed_yahoo if args.source == "yahoo" else seed_stooq)(missing)

    print(f"\nDone. fetched={fetched} skipped={skipped} failed={len(failed)}")
    if failed:
        print("Failed series (fix symbols or retry): " + ", ".join(failed))
    return 0 if fetched or not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
