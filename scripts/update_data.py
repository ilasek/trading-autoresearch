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

Adjusted prices and corporate actions. Yahoo serves dividend- and split-adjusted
bars, adjusted *as of the day they are fetched*. The store keeps old rows as
they were fetched, so a dividend or split that happens after a series' last
stored row would otherwise splice two bases together: a 2:1 split reads as a
-50% day and a dividend vanishes from the total return. Two defences:

- every refresh re-fetches a short overlap (`OVERLAP_DAYS`) and puts the new
  rows on the stored basis: it multiplies their prices by the stored/fetched
  close ratio on the latest overlapping rows (and volumes by the volume ratio,
  for splits), so returns across the event are total returns;
- `--verify-days N` re-fetches the last N days of every live stock and ETF and
  repairs any stored stretch whose stored/fetched ratio is not constant (a break
  an earlier refresh spliced in). The data-refresh workflow runs it weekly.

Also seeds the cash-rate series (`data.RATE_SERIES`, ^IRX) on first run, and
prints a WARN line for any new daily move beyond `JUMP_WARN` for a human to
check.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data, membership

CHUNK = 50
OVERLAP_DAYS = 10          # calendar days re-fetched before each series' last stored row
ADJ_TOL = 1e-4             # stored/fetched ratio further from 1 than this = an adjustment
# A basis change this large is a split or consolidation, not a dividend; only
# then is volume rescaled, by the inverse of the price ratio (Yahoo restates
# share counts on splits only). Measured volume ratios are NOT used: Yahoo
# revises the latest days' volumes on its own, and on 2026-10-09 that read as
# x0.0001 "adjustments" on LSE names whose prices had not moved at all.
SPLIT_RATIO = 1.25
VERIFY_TOL = 1e-3          # verify mode: ratio drift beyond this inside the window = a break
JUMP_WARN = 0.40           # flag new daily moves beyond +-40% for a human to check
ADJUSTED_TYPES = ("stock", "etf")
PRICE_COLS = ["open", "high", "low", "close"]


def _ratio(num: pd.Series, den: pd.Series) -> pd.Series:
    r = (num / den).replace([float("inf"), float("-inf")], float("nan")).dropna()
    return r[r > 0]


def volume_ratio_for(price_ratio: float) -> float:
    """Share-count rescale implied by a price-basis change: 1/price_ratio for a
    split or consolidation (so close x volume is unchanged), 1 for a dividend."""
    return 1.0 / price_ratio if max(price_ratio, 1.0 / price_ratio) >= SPLIT_RATIO else 1.0


def adjustment_ratios(stored: pd.DataFrame, fetched: pd.DataFrame, last: pd.Timestamp,
                      n: int = 3) -> tuple[float, float] | None:
    """(price, volume) ratios that put fetched rows on the stored basis, from
    the latest `n` rows both hold at or before `last`; None when they share no
    row. A price ratio away from 1 means Yahoo re-adjusted the old rows for an
    event after `last`; the volume ratio follows from it (`volume_ratio_for`)."""
    common = stored.index.intersection(fetched.index)
    common = common[common <= last][-n:]
    if not len(common):
        return None
    pr = _ratio(stored.loc[common, "close"], fetched.loc[common, "close"])
    if not len(pr):
        return None
    price_ratio = float(pr.median())
    return price_ratio, volume_ratio_for(price_ratio)


def on_stored_basis(rows: pd.DataFrame, price_ratio: float, volume_ratio: float) -> pd.DataFrame:
    out = rows.copy()
    out[PRICE_COLS] = out[PRICE_COLS] * price_ratio
    out["volume"] = out["volume"] * volume_ratio
    return out


def jump_warnings(sid: str, stored: pd.DataFrame | None, new: pd.DataFrame) -> list[str]:
    closes = new["close"]
    if stored is not None and len(stored):
        closes = pd.concat([stored["close"].iloc[-1:], closes])
    r = closes.pct_change().dropna()
    return [f"  WARN {sid}: {d.date()} close moved {v:+.0%} — check for an unadjusted "
            f"corporate action or a bad tick" for d, v in r[r.abs() > JUMP_WARN].items()]


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
            if spec.get("type") == "rate":
                out.append((spec, None))       # seeded here: full history
                continue
            print(f"  WARN {spec['id']}: not in store (run seed_data.py / build_membership.py); skipping")
            continue
        if len(pd.bdate_range(last, today)) - 1 > max_age_bdays:
            out.append((spec, last))
    return out


def new_rows_for(spec: dict, last: pd.Timestamp | None, fetched: pd.DataFrame) -> pd.DataFrame:
    """The rows of `fetched` to append for one series, on the stored basis."""
    if last is None:
        return fetched                           # first fetch: the whole history, one basis
    new = fetched[fetched.index > last]
    if not len(new) or spec.get("type") not in ADJUSTED_TYPES:
        return new
    stored = data.load_ohlcv(spec["id"])
    ratios = adjustment_ratios(stored, fetched, last) if stored is not None else None
    if ratios is None:
        print(f"  WARN {spec['id']}: no overlap with stored rows; appended without basis check")
        return new
    price_ratio, volume_ratio = ratios
    if abs(price_ratio - 1) > ADJ_TOL:
        kind = "a split" if volume_ratio != 1.0 else "a dividend"
        print(f"  adj {spec['id']}: new rows rescaled onto the stored basis (price x{price_ratio:.6f}, "
              f"volume x{volume_ratio:.4f}) — {kind} since the last refresh")
        new = on_stored_basis(new, price_ratio, volume_ratio)
    return new


def refresh_yahoo(stale: list[tuple[dict, pd.Timestamp | None]]) -> int:
    updated = 0
    # never-stored series (the cash rate on first run) are fetched in full, apart
    known = [(s, last) for s, last in stale if last is not None]
    seeded = [(s, last) for s, last in stale if last is None]
    batches = [known[i: i + CHUNK] for i in range(0, len(known), CHUNK)]
    if seeded:
        batches.append(seeded)
    for i, chunk in enumerate(batches):
        lasts = [last for _, last in chunk if last is not None]
        since = (min(lasts) - pd.Timedelta(days=OVERLAP_DAYS)).strftime("%Y-%m-%d") if lasts else None
        by_yahoo = {spec["yahoo"]: (spec, last) for spec, last in chunk}
        try:
            frames = data.fetch_yahoo_batch(list(by_yahoo), start=since)
        except Exception as e:  # noqa: BLE001 — one bad batch must not stop the refresh
            print(f"  WARN batch {i}: {type(e).__name__}: {e}")
            continue
        new_rows = {}
        for ysym, (spec, last) in by_yahoo.items():
            df = frames.get(ysym)
            if df is None:
                # Usually a delisting. Keep the history; report it so the
                # membership update (or a human) can confirm.
                print(f"  WARN {spec['id']}: Yahoo returned no data for {ysym}")
                continue
            try:
                new = new_rows_for(spec, last, df)
            except Exception as e:  # noqa: BLE001 — one bad series must not stop the refresh
                print(f"::warning::{spec['id']} skipped by the refresh ({type(e).__name__}: {e})")
                continue
            if len(new) and new["close"].notna().any():
                if spec.get("type") in ADJUSTED_TYPES:
                    for line in jump_warnings(spec["id"], data.load_ohlcv(spec["id"]), new):
                        print(line)
                new_rows[spec["id"]] = new
            elif len(new):
                print(f"::warning::{spec['id']}: Yahoo returned {len(new)} rows with no close; not stored")
        try:
            data.write_many(new_rows)
        except Exception as e:  # noqa: BLE001 — keep every other batch's rows
            print(f"::warning::refresh batch {i}: write failed ({type(e).__name__}: {e}); "
                  f"{len(new_rows)} series not updated")
            continue
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


def repair_window(stored: pd.DataFrame, fetched: pd.DataFrame, since: pd.Timestamp
                  ) -> tuple[pd.DataFrame | None, float]:
    """Stored rows from `since` re-derived from a fresh fetch on the stored
    basis, if the stored/fetched ratio drifts inside the window (a spliced
    corporate action); (None, drift) when it is constant. The basis is the
    ratio on the window's first five common rows, so history before the window
    is untouched and the repaired stretch joins it seamlessly."""
    common = stored.index.intersection(fetched.index)
    common = common[common >= since]
    if len(common) < 10:
        return None, 0.0
    q = _ratio(stored.loc[common, "close"], fetched.loc[common, "close"])
    if len(q) < 10:
        return None, 0.0
    ref = float(q.iloc[:5].median())
    drift = float((q / ref - 1).abs().max())
    if drift <= VERIFY_TOL:
        return None, drift
    fixed = on_stored_basis(fetched.loc[fetched.index >= common[0]], ref, volume_ratio_for(ref))
    return fixed, drift


def verify_recent(days: int) -> int:
    """Re-fetch the last `days` of every live stock and ETF and repair breaks."""
    specs = [s for s in live_series() if s.get("type") in ADJUSTED_TYPES and s.get("yahoo")]
    since = pd.Timestamp.today().normalize() - pd.Timedelta(days=days)
    repaired = 0
    for i in range(0, len(specs), CHUNK):
        chunk = specs[i: i + CHUNK]
        by_yahoo = {s["yahoo"]: s for s in chunk}
        try:
            frames = data.fetch_yahoo_batch(list(by_yahoo), start=since.strftime("%Y-%m-%d"))
        except Exception as e:  # noqa: BLE001
            print(f"  WARN verify batch {i // CHUNK}: {type(e).__name__}: {e}")
            continue
        fixes = {}
        for ysym, spec in by_yahoo.items():
            stored, fetched = data.load_ohlcv(spec["id"]), frames.get(ysym)
            if stored is None or fetched is None:
                continue
            fixed, drift = repair_window(stored, fetched, since)
            if fixed is not None:
                fixes[spec["id"]] = fixed
                print(f"  REPAIR {spec['id']}: stored/fetched ratio drifted {drift:.2%} inside the "
                      f"last {days} days (a spliced corporate action); {len(fixed)} rows rewritten "
                      f"on the stored basis")
        data.write_many(fixes)
        repaired += len(fixes)
    print(f"verify: {repaired} series repaired")
    return repaired


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
    ap.add_argument("--verify-days", type=int, default=0,
                    help="also re-fetch the last N days of live stocks/ETFs and repair "
                         "spliced corporate actions (yahoo only)")
    args = ap.parse_args()

    stale = stale_series(args.max_age_bdays)
    print(f"{len(stale)} series need refresh")
    if stale:
        if args.source == "stooq":
            stale = [(s, last) for s, last in stale if s.get("stooq") and last is not None]
        updated = (refresh_yahoo if args.source == "yahoo" else refresh_stooq)(stale)
        print(f"Done. updated={updated}/{len(stale)}")
    if args.verify_days and args.source == "yahoo":
        verify_recent(args.verify_days)
    report_stopped()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
