#!/usr/bin/env python
"""One-off (idempotent) migration of the price store to monthly partitions.

Old layout: data/store/<id>.parquet, one file per series with its full history,
rewritten whole by every daily refresh. New layout: data/store/<YYYY>/<YYYY-MM>.parquet,
one long-format file per calendar month (see engine/data.py "Store I/O").

Any flat <id>.parquet still present is folded into the month files and then
deleted, so re-running after a merge that brought in new flat files (e.g. from
a refresh bot still on the old layout) finishes the job.

    python scripts/migrate_store_partitioned.py            # migrate + verify
    python scripts/migrate_store_partitioned.py --check    # verify only
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data


def flat_files() -> list[Path]:
    return sorted(data.STORE.glob("*.parquet"))


def read_flat(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify only; change nothing")
    args = ap.parse_args()

    files = flat_files()
    print(f"{len(files)} flat series files to migrate")
    if not files:
        return 0
    frames = {f.stem: read_flat(f) for f in files}
    if not args.check:
        data.write_many(frames)

    bad = []
    for sid, old in frames.items():
        new = data.load_ohlcv(sid)
        if new is None:
            bad.append(f"{sid}: missing after migration")
            continue
        new = new.loc[new.index.isin(old.index)]
        try:
            pd.testing.assert_frame_equal(
                old[data.OHLCV_COLS].astype(float), new[data.OHLCV_COLS],
                check_names=False, check_index_type=False, check_freq=False,
            )
        except AssertionError as e:
            bad.append(f"{sid}: {str(e).splitlines()[0]}")
    if bad:
        print("MISMATCH — flat files kept:\n  " + "\n  ".join(bad[:20]))
        return 1
    print(f"verified {len(frames)} series identical in the partitioned store")
    if not args.check:
        for f in files:
            f.unlink()
        print(f"removed {len(files)} flat files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
