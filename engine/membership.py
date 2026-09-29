"""Point-in-time index membership: which instruments were eligible on a date.

A backtest that picks from today's constituents buys the survivors, the names
that grew into the index, and never holds the ones that shrank out of it.
Membership intervals undo that: a stock is a candidate on date t only if it
belonged to one of the tracked indices on t.

Intervals live in data/membership/intervals.csv, one row per (index, id,
membership spell): `start` inclusive, `end` exclusive, `end` blank while still
a member. `id` is the store / price-column id (see `yahoo_to_id`).
scripts/build_membership.py writes and evolves the file; research code only
reads it, and only through the protocol, never from a strategy.

Ported from ilasek/trading-agent (engine/membership.py), keyed by this repo's
instrument ids instead of Yahoo symbols.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MEMBERSHIP_DIR = ROOT / "data" / "membership"
INTERVALS_FILE = MEMBERSHIP_DIR / "intervals.csv"
INTERVAL_COLS = ["index", "id", "start", "end"]

# Liquidity floor applied on top of membership: trailing median USD traded
# value. Causal: rolling over past rows only.
ADV_WINDOW = 63
ADV_MIN_PERIODS = 40
MIN_ADV_USD = 5e6

# Yahoo suffix -> id suffix. Kept identical to the ids data/universe.yaml has
# always used, so a legacy instrument and its point-in-time twin share one
# store series.
_ID_SUFFIX = {".L": "_UK", ".T": "_JP"}


def yahoo_to_id(symbol: str) -> str:
    """Store / column id for a Yahoo symbol: `SAP.DE` -> `SAP_DE`,
    `AZN.L` -> `AZN_UK`, `7203.T` -> `7203_JP`, `0700.HK` -> `0700_HK`."""
    for suf, rep in _ID_SUFFIX.items():
        if symbol.endswith(suf):
            return symbol[: -len(suf)] + rep
    return symbol.replace(".", "_")


@dataclass(frozen=True)
class Event:
    date: pd.Timestamp
    action: str   # "in" | "out"
    symbol: str


def load_intervals(path: Path = INTERVALS_FILE) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=INTERVAL_COLS)
    df = pd.read_csv(path, dtype={"index": str, "id": str})
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])  # NaT = still a member
    return df


def save_intervals(df: pd.DataFrame, path: Path = INTERVALS_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df[INTERVAL_COLS].copy()
    out = out.sort_values(["index", "id", "start"]).reset_index(drop=True)
    out["start"] = pd.to_datetime(out["start"]).dt.strftime("%Y-%m-%d")
    out["end"] = pd.to_datetime(out["end"]).dt.strftime("%Y-%m-%d").fillna("")
    out.to_csv(path, index=False)


def intervals_from_events(
    index: str,
    events: list[Event],
    current: set[str],
    complete_from: pd.Timestamp,
    snapshot: pd.Timestamp,
) -> tuple[pd.DataFrame, list[str]]:
    """Rebuild membership spells from a dated change log plus today's members.

    `complete_from` is the date from which the change log is trusted to be
    complete. A name that leaves with no recorded entry was a member from at
    least `complete_from`; a current member with no recorded entry has been one
    since `complete_from` too. Membership before `complete_from` is unknown, so
    no spell starts earlier: the universe shrinks instead of borrowing today's
    list.

    Returns (intervals, warnings). Warnings flag log/snapshot disagreements: a
    name the log says joined but that is not a member at `snapshot` with no
    recorded exit is closed at `snapshot` and reported.
    """
    rows: list[dict] = []
    warnings: list[str] = []
    by_sym: dict[str, list[Event]] = {}
    for e in sorted(events, key=lambda e: (e.date, e.action == "in")):
        if e.date < complete_from:
            continue
        by_sym.setdefault(e.symbol, []).append(e)

    for sym in sorted(set(by_sym) | current):
        evs = by_sym.get(sym, [])
        start: pd.Timestamp | None = None
        # A first event of "out" (or no event, for a current member) means the
        # name was already in when the log became trustworthy.
        if not evs or evs[0].action == "out":
            start = complete_from
        for e in evs:
            if e.action == "in":
                if start is None:
                    start = e.date
                # a repeated "in" while already in is a no-op
            else:
                if start is not None and e.date > start:
                    rows.append({"index": index, "id": sym, "start": start, "end": e.date})
                start = None
        if start is not None:
            if sym in current:
                rows.append({"index": index, "id": sym, "start": start, "end": pd.NaT})
            else:
                warnings.append(f"{index}: {sym} joined {start.date()} with no recorded exit and is "
                                f"not a member at {snapshot.date()}; closed at {snapshot.date()}")
                rows.append({"index": index, "id": sym, "start": start, "end": snapshot})
        elif sym in current:
            warnings.append(f"{index}: {sym} is a member at {snapshot.date()} but the log's last event "
                            f"is an exit; opened at {snapshot.date()}")
            rows.append({"index": index, "id": sym, "start": snapshot, "end": pd.NaT})
    df = pd.DataFrame(rows, columns=INTERVAL_COLS)
    return df, warnings


def apply_snapshot(
    intervals: pd.DataFrame, index: str, current: set[str], date: pd.Timestamp,
) -> tuple[pd.DataFrame, list[str], list[str]]:
    """Evolve one index's spells to match a fresh constituent list.

    Names that appeared get a spell opened on `date`; names that disappeared
    have their open spell closed on `date`. Nothing is ever deleted, so a name
    that left stays priced and its history stays eligible where it was.
    Returns (intervals, added, removed)."""
    df = intervals.copy()
    mine = df["index"] == index
    open_mask = mine & df["end"].isna()
    open_ids = set(df.loc[open_mask, "id"])
    added = sorted(current - open_ids)
    removed = sorted(open_ids - current)
    if removed:
        df.loc[open_mask & df["id"].isin(removed), "end"] = date
    if added:
        new = pd.DataFrame({"index": index, "id": added, "start": date, "end": pd.NaT})
        df = pd.concat([df, new], ignore_index=True)
    return df, added, removed


def membership_mask(
    intervals: pd.DataFrame, dates: pd.DatetimeIndex, ids: list[str],
) -> pd.DataFrame:
    """Boolean panel (dates x ids): True where the id belonged to any tracked
    index on that date. Ids without intervals are all False."""
    mask = np.zeros((len(dates), len(ids)), dtype=bool)
    col = {s: i for i, s in enumerate(ids)}
    d = dates.values
    for r in intervals.itertuples(index=False):
        j = col.get(r.id)
        if j is None:
            continue
        lo = np.searchsorted(d, np.datetime64(r.start), side="left")
        hi = len(d) if pd.isna(r.end) else np.searchsorted(d, np.datetime64(r.end), side="left")
        if hi > lo:
            mask[lo:hi, j] = True
    return pd.DataFrame(mask, index=dates, columns=ids)


def liquidity_mask(prices: pd.DataFrame, volume: pd.DataFrame) -> pd.DataFrame:
    """True where the trailing median USD traded value clears MIN_ADV_USD.

    `prices` is USD closes, `volume` the native share count aligned to it.
    Rolling over past rows only, so the mask at t uses data up to t. A column
    with no volume at all (some FX-quoted lines) is judged on price presence
    alone rather than excluded: missing volume is a data gap, not illiquidity."""
    vol = volume.reindex(index=prices.index, columns=prices.columns)
    traded = vol * prices
    adv = traded.rolling(ADV_WINDOW, min_periods=ADV_MIN_PERIODS).median()
    ok = adv >= MIN_ADV_USD
    no_volume = vol.notna().sum() == 0
    if no_volume.any():
        ok.loc[:, no_volume] = prices.loc[:, no_volume].notna()
    return ok.fillna(False).astype(bool)


def eligibility(
    prices: pd.DataFrame,
    volume: pd.DataFrame | None,
    types: dict[str, str],
    intervals: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Point-in-time eligibility panel (dates x columns of `prices`).

    - stock: a member of a tracked index on that date AND above the
      liquidity floor (when `volume` is given) AND priced.
    - etf: eligible whenever priced. An ETF has no prices before launch, so
      this is point-in-time by construction.
    - anything else (or unknown): never eligible.

    Every input is at or before the row's date, so the panel is causal and can
    be truncated with the prices it accompanies."""
    iv = load_intervals() if intervals is None else intervals
    cols = list(prices.columns)
    stocks = [c for c in cols if types.get(c) == "stock"]
    etfs = [c for c in cols if types.get(c) == "etf"]
    elig = pd.DataFrame(False, index=prices.index, columns=cols)
    if stocks:
        member = membership_mask(iv, prices.index, stocks)
        if volume is not None:
            member &= liquidity_mask(prices[stocks], volume[stocks])
        elig[stocks] = member
    if etfs:
        elig[etfs] = True
    return elig & prices.notna()
