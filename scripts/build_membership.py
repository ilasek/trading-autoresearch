#!/usr/bin/env python
"""Build and evolve the point-in-time (PIT) universe.

    python scripts/build_membership.py --bootstrap   # rebuild spells from the change logs
    python scripts/build_membership.py               # weekly: diff today's constituents

A data/engine-maintenance tool (like seed_data.py): it fetches from Wikipedia
and Yahoo. Research sessions never run it.

Outputs (all committed):
    data/membership/intervals.csv   (index, id, start, end) membership spells, ids as in the store
    data/membership/unpriced.csv    members Yahoo has no prices for (retried monthly)
    data/membership/suspect.csv     spells dropped because the priced series is not the member's
    data/membership/coverage.csv    per month-end and index: members, priced members, share priced
    data/universe_pit.yaml          every priced ever-member + the ETFs + FX

Sources (data/membership/sources/, provenance in each file's header):
    S&P 500        fja05680/sp500 daily membership since 1996, then Wikipedia's list
    DAX, CAC 40, FTSE 100, SMI, AEX, Euro Stoxx 50
                   change logs from 2009, vendored from ilasek/trading-agent
    Nikkei 225, Hang Seng
                   change logs from 2009, scripts/build_asia_changelogs.py
    ETFs           the legacy universe's ETFs: eligible from their first price

Before an index's log is trusted (1996 for the S&P 500, 2009 for the rest) it
has no members: the universe shrinks rather than borrowing today's list. The
weekly mode never deletes anything; a name that leaves an index has its spell
closed and keeps its price series.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
import time
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import data  # noqa: E402
from engine.membership import (  # noqa: E402
    INTERVAL_COLS, MEMBERSHIP_DIR, Event, apply_snapshot, intervals_from_events,
    load_intervals, membership_mask, save_intervals, yahoo_to_id,
)

SOURCES = MEMBERSHIP_DIR / "sources"
OVERRIDES_FILE = MEMBERSHIP_DIR / "overrides.yaml"
UNPRICED_FILE = MEMBERSHIP_DIR / "unpriced.csv"
SUSPECT_FILE = MEMBERSHIP_DIR / "suspect.csv"
COVERAGE_FILE = MEMBERSHIP_DIR / "coverage.csv"
SP500_HISTORY = SOURCES / "sp500_ticker_start_end.csv"

LOG_COMPLETE_FROM = pd.Timestamp("2009-01-01")   # the non-US change logs
LOG_INDICES = ("dax", "cac40", "ftse100", "smi", "aex", "sx5e", "n225", "hsi")
#: New names are stored from here: the S&P history starts 1996-01-02 and a
#: 12-month lookback needs the year before.
PRICE_HISTORY_START = "1995-01-01"
UNPRICED_RETRY_DAYS = 30
#: A spell whose priced series starts this long after the spell does is not the
#: member's price history (the ticker was reassigned to a later listing).
REUSE_TOLERANCE_DAYS = 30
COVERAGE_START = "1996-01-31"
#: Price-quality rules for the (mostly dead) names Yahoo still serves: a daily
#: move beyond these is not a market move but a unit change, a re-listing
#: spliced onto an old series, or junk.
IMPOSSIBLE_UP, IMPOSSIBLE_DOWN = 5.0, -0.9
JUNK_MOVE, JUNK_DAYS = 0.5, 10
QUALITY_FILE = MEMBERSHIP_DIR / "price_quality.csv"
FETCH_CHUNK = 40
FETCH_PAUSE = 3.0

UA = {"User-Agent": "trading-autoresearch membership builder (ivo.lasek@gmail.com)"}

# Yahoo suffix -> (quote currency, region)
SUFFIX = {
    "": ("USD", "US"), ".DE": ("EUR", "DE"), ".PA": ("EUR", "FR"), ".AS": ("EUR", "NL"),
    ".BR": ("EUR", "BE"), ".MI": ("EUR", "IT"), ".MC": ("EUR", "ES"), ".HE": ("EUR", "FI"),
    ".IR": ("EUR", "IE"), ".L": ("GBX", "UK"), ".SW": ("CHF", "CH"), ".CO": ("DKK", "DK"),
    ".T": ("JPY", "JP"), ".HK": ("HKD", "HK"),
}
FX_EXTRA = {"CHF": {"id": "FX_USDCHF", "stooq": "usdchf", "yahoo": "CHF=X", "invert": True}}


def split_suffix(symbol: str) -> tuple[str, str]:
    for suf in sorted(SUFFIX, key=len, reverse=True):
        if suf and symbol.endswith(suf):
            return symbol[: -len(suf)], suf
    return symbol, ""


# ---------------------------------------------------------------------------
# Current constituents (Wikipedia). Each returns {yahoo symbol: name}.
# ---------------------------------------------------------------------------

def _html(url: str) -> str:
    import requests

    for attempt in range(5):
        r = requests.get(url, headers=UA, timeout=30)
        if r.status_code != 429:   # Wikipedia rate limit: wait as told, then retry
            break
        time.sleep(min(int(r.headers.get("retry-after", 10)), 60) + attempt)
    r.raise_for_status()
    return re.sub(r'(colspan|rowspan)="(\d+)[^"]*"', r'\1="\2"', r.text)


def _tables(url: str) -> list[pd.DataFrame]:
    return pd.read_html(io.StringIO(_html(url)))


def _find(tables: list[pd.DataFrame], *cols: str) -> pd.DataFrame:
    for t in tables:
        names = [str(c[0] if isinstance(c, tuple) else c).strip() for c in t.columns]
        if all(c in names for c in cols):
            t = t.copy()
            t.columns = names
            return t
    raise LookupError(f"no table with columns {cols}")


def _clean(s: object) -> str:
    return str(s).strip().split("[")[0].strip().rstrip(".")


def _valid(sym: str) -> bool:
    base = sym.split(".")[0].lower()
    return bool(base) and base not in ("nan", "none", "-")


def current_sp500() -> dict[str, str]:
    t = _find(_tables("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"), "Symbol", "Security")
    return {_clean(r.Symbol).replace(".", "-"): _clean(r.Security) for r in t.itertuples()}


def current_dax() -> dict[str, str]:
    t = _find(_tables("https://en.wikipedia.org/wiki/DAX"), "Ticker", "Company")
    return {_clean(r.Ticker): _clean(r.Company) for r in t.itertuples()}


def current_cac40() -> dict[str, str]:
    t = _find(_tables("https://fr.wikipedia.org/wiki/CAC_40"), "Société", "Mnémo")
    return {f"{_clean(m)}.PA": _clean(n) for n, m in zip(t["Société"], t["Mnémo"])}


def current_ftse100() -> dict[str, str]:
    t = _find(_tables("https://en.wikipedia.org/wiki/FTSE_100_Index"), "Company", "Ticker")
    return {f"{_clean(r.Ticker).replace('.', '-')}.L": _clean(r.Company) for r in t.itertuples()}


def current_smi() -> dict[str, str]:
    t = _find(_tables("https://en.wikipedia.org/wiki/Swiss_Market_Index"), "Name", "Ticker")
    return {f"{_clean(r.Ticker)}.SW": _clean(r.Name) for r in t.itertuples()}


#: Euronext Amsterdam codes whose Yahoo symbol is not "<code>.AS".
AEX_YAHOO = {"RDSA": "SHELL.AS", "EXOR": "EXO.AS", "WDP": "WDP.BR"}


def current_aex() -> dict[str, str]:
    # The Dutch article is kept current; the English table missed the
    # September 2025 expansion to 30 names.
    t = _find(_tables("https://nl.wikipedia.org/wiki/AEX"), "Company", "Ticker symbol")
    out = {}
    for name, code in zip(t["Company"], t["Ticker symbol"]):
        code = _clean(code)
        out[AEX_YAHOO.get(code, f"{code}.AS")] = _clean(name)
    return out


def current_sx5e() -> dict[str, str]:
    t = _find(_tables("https://en.wikipedia.org/wiki/Euro_Stoxx_50"), "Ticker", "Main listing", "Name")
    return {_clean(r.Ticker): _clean(r.Name) for r in t.itertuples()}


def current_n225() -> dict[str, str]:
    import requests

    from build_asia_changelogs import N225_TITLE, n225_members

    r = requests.get("https://ja.wikipedia.org/w/api.php", params=dict(
        action="query", prop="revisions", titles=N225_TITLE, rvprop="content",
        rvslots="main", format="json", formatversion=2), headers=UA, timeout=60).json()
    text = r["query"]["pages"][0]["revisions"][0]["slots"]["main"]["content"]
    return {f"{code}.T": name for name, code in n225_members(text).items() if code}


def current_hsi() -> dict[str, str]:
    t = _find(_tables("https://zh.wikipedia.org/wiki/%E6%81%92%E7%94%9F%E6%8C%87%E6%95%B8"),
              "股份代號", "名稱")
    out = {}
    for code, name in zip(t["股份代號"], t["名稱"]):
        code = str(code).strip()
        if code.isdigit():
            out[f"{int(code):04d}.HK"] = _clean(name)
    return out


FETCHERS = {
    "sp500": current_sp500, "dax": current_dax, "cac40": current_cac40,
    "ftse100": current_ftse100, "smi": current_smi, "aex": current_aex,
    "sx5e": current_sx5e, "n225": current_n225, "hsi": current_hsi,
}


# ---------------------------------------------------------------------------
# Historical sources
# ---------------------------------------------------------------------------

def load_overrides() -> dict:
    with open(OVERRIDES_FILE) as f:
        return yaml.safe_load(f) or {}


def read_events(path: Path) -> tuple[list[Event], dict[str, str]]:
    df = pd.read_csv(path, comment="#", dtype={"symbol": str})
    events = [Event(pd.Timestamp(r.date), r.action.strip(), r.symbol.strip()) for r in df.itertuples()]
    names = {r.symbol.strip(): str(r.name).replace(" (approximate)", "") for r in df.itertuples()}
    return events, names


def merge_spells(df: pd.DataFrame) -> pd.DataFrame:
    """Merge overlapping or touching spells of one (index, id)."""
    out = []
    far = pd.Timestamp("2262-01-01")
    for (idx, sym), g in df.sort_values("start").groupby(["index", "id"], sort=False):
        cur_s, cur_e = None, None
        for r in g.itertuples(index=False):
            e = far if pd.isna(r.end) else r.end
            if cur_s is None:
                cur_s, cur_e = r.start, e
            elif r.start <= cur_e:
                cur_e = max(cur_e, e)
            else:
                out.append((idx, sym, cur_s, cur_e))
                cur_s, cur_e = r.start, e
        out.append((idx, sym, cur_s, cur_e))
    res = pd.DataFrame(out, columns=INTERVAL_COLS)
    res.loc[res["end"] == far, "end"] = pd.NaT
    return res


def sp500_history(renames: dict[str, str]) -> pd.DataFrame:
    df = pd.read_csv(SP500_HISTORY)
    df["symbol"] = df["ticker"].str.strip().str.replace(".", "-", regex=False)
    df["symbol"] = df["symbol"].map(lambda s: renames.get(s, s))
    df["start"] = pd.to_datetime(df["start_date"])
    df["end"] = pd.to_datetime(df["end_date"])   # exclusive: the successor starts that day
    df["index"] = "sp500"
    df["id"] = df["symbol"]
    return merge_spells(df[INTERVAL_COLS])


def _to_ids(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["id"] = df["id"].map(yahoo_to_id)
    return df


def bootstrap(today: pd.Timestamp) -> tuple[pd.DataFrame, dict[str, str], list[str]]:
    """Spells from the historical sources, synced to today's lists.

    Intervals are built in Yahoo symbols and converted to store ids at the end;
    the returned `names` maps Yahoo symbol -> company name."""
    ov = load_overrides()
    renames = {k.replace(".", "-"): v for k, v in (ov.get("sp500_renames") or {}).items()}
    drop = set(ov.get("drop_symbols") or [])
    warnings: list[str] = []
    names: dict[str, str] = {}
    parts = []

    current = {}
    for k, f in FETCHERS.items():
        current[k] = {s: n for s, n in f().items() if _valid(s)}
        names.update(current[k])

    sp = sp500_history(renames)
    cur_sp = {renames.get(s, s) for s in current["sp500"]}
    sp, added, removed = apply_snapshot(sp, "sp500", cur_sp, today)
    if added or removed:
        warnings.append(f"sp500: synced to today's list (+{len(added)} -{len(removed)})")
    parts.append(sp)

    for idx in LOG_INDICES:
        events, ev_names = read_events(SOURCES / f"{idx}_changes.csv")
        for k, v in ev_names.items():
            names.setdefault(k, v)
        df, w = intervals_from_events(idx, events, set(current[idx]), LOG_COMPLETE_FROM, today)
        warnings += w
        parts.append(df)

    iv = pd.concat(parts, ignore_index=True)
    iv = iv[~iv["id"].isin(drop)]
    return _to_ids(iv), names, warnings


def evolve(iv: pd.DataFrame, today: pd.Timestamp) -> tuple[pd.DataFrame, dict[str, str], list[str]]:
    """Weekly: apply today's constituent lists. A fetch that fails or returns a
    list far smaller than the open spells is skipped, never applied — a broken
    page must not close every spell of an index."""
    ov = load_overrides()
    renames = {k.replace(".", "-"): v for k, v in (ov.get("sp500_renames") or {}).items()}
    drop = set(ov.get("drop_symbols") or [])
    names: dict[str, str] = {}
    log: list[str] = []
    for idx, fetch in FETCHERS.items():
        try:
            members = fetch()
        except Exception as e:  # network / layout change
            log.append(f"{idx}: fetch failed ({type(e).__name__}: {e}); left unchanged")
            continue
        members = {s: n for s, n in members.items() if _valid(s)}
        if idx == "sp500":
            members = {renames.get(s, s): n for s, n in members.items()}
        members = {s: n for s, n in members.items() if s not in drop}
        n_open = int(((iv["index"] == idx) & iv["end"].isna()).sum())
        if len(members) < max(15, 0.8 * n_open):
            log.append(f"{idx}: fetched {len(members)} names vs {n_open} open spells; left unchanged")
            continue
        names.update(members)
        ids = {yahoo_to_id(s) for s in members}
        iv, added, removed = apply_snapshot(iv, idx, ids, today)
        if added or removed:
            log.append(f"{idx}: +{added} -{removed}")
    return iv, names, log


# ---------------------------------------------------------------------------
# Prices, suspects, universe file, coverage
# ---------------------------------------------------------------------------

def fetch_missing_prices(symbols: dict[str, str], today: pd.Timestamp) -> set[str]:
    """Fetch every id (-> Yahoo symbol) not yet in the store. Returns the ids
    Yahoo has no prices for. Known-unpriced ids are retried every
    UNPRICED_RETRY_DAYS."""
    unpriced = pd.read_csv(UNPRICED_FILE, parse_dates=["checked"]) if UNPRICED_FILE.exists() \
        else pd.DataFrame(columns=["id", "yahoo", "checked"])
    recent = set(unpriced.loc[unpriced["checked"] > today - pd.Timedelta(days=UNPRICED_RETRY_DAYS), "id"])
    stored = set(data.store_ids())
    todo = [i for i in symbols if i not in stored and i not in recent]
    print(f"fetching prices for {len(todo)} ids ...", flush=True)
    pending: dict[str, pd.DataFrame] = {}
    for n in range(0, len(todo), FETCH_CHUNK):
        chunk = todo[n: n + FETCH_CHUNK]
        by_yahoo = {symbols[i]: i for i in chunk}
        try:
            got = data.fetch_yahoo_batch(list(by_yahoo), start=PRICE_HISTORY_START)
        except Exception as e:  # noqa: BLE001 — one bad batch must not stop the build
            print(f"  WARN batch {n // FETCH_CHUNK}: {type(e).__name__}: {e}", flush=True)
            time.sleep(30)
            continue
        frames = {by_yahoo[y]: df for y, df in got.items() if df["close"].notna().sum() > 20}
        pending.update(frames)
        print(f"  {n + len(chunk)}/{len(todo)}: {len(frames)} priced", flush=True)
        # every month file is rewritten on a write, so batch several chunks
        if len(pending) >= 300 or n + FETCH_CHUNK >= len(todo):
            data.write_many(pending, replace=True)
            pending = {}
        time.sleep(FETCH_PAUSE)
    if pending:
        data.write_many(pending, replace=True)
    stored = set(data.store_ids())
    still = {i for i in symbols if i not in stored}
    keep = unpriced[unpriced["id"].isin(still) & unpriced["id"].isin(recent)]
    fresh = pd.DataFrame({"id": sorted(still - set(keep["id"]))})
    fresh["yahoo"] = fresh["id"].map(symbols)
    fresh["checked"] = today
    out = pd.concat([keep, fresh]).sort_values("id")
    out["checked"] = pd.to_datetime(out["checked"]).dt.strftime("%Y-%m-%d")
    out.to_csv(UNPRICED_FILE, index=False)
    return still


def drop_reused_tickers(iv: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop spells whose priced series cannot be the member's own.

    Yahoo serves a ticker's CURRENT holder. When an old member's ticker now
    belongs to a company that listed later, the series starts after the spell
    did; a member must have been listed when it joined, so such a spell is
    dropped rather than letting the newcomer's prices stand in for it. Spells
    starting at a log's trust date are exempt (the member joined earlier), as
    are spells whose series simply starts late within a long spell for a name
    Yahoo only covers partially — those are flagged only when the gap exceeds
    REUSE_TOLERANCE_DAYS."""
    first = {i: data.load_ohlcv(i)["close"].first_valid_index() for i in set(iv["id"]) if data.load_ohlcv(i) is not None}
    trust = {"sp500": pd.Timestamp("1996-01-02")}
    bad, trimmed = [], []
    iv = iv.copy()
    for k, r in iv.iterrows():
        f = first.get(r["id"])
        if f is None:
            continue
        exempt = r["start"] <= trust.get(r["index"], LOG_COMPLETE_FROM)
        if exempt or f <= r["start"] + pd.Timedelta(days=REUSE_TOLERANCE_DAYS):
            continue
        if pd.isna(r["end"]):
            # A current member whose Yahoo history starts late (a renamed or
            # re-formed company now holding the ticker): it is the member now,
            # so keep the spell from its first price rather than dropping it.
            trimmed.append((k, r["start"]))
            iv.loc[k, "start"] = f
        else:
            bad.append(k)
    suspect = iv.loc[bad + [k for k, _ in trimmed]].copy()
    suspect["first_price"] = suspect["id"].map(first)
    suspect["action"] = ["dropped"] * len(bad) + ["start moved to first price"] * len(trimmed)
    for k, start in trimmed:
        suspect.loc[k, "start"] = start
    return iv.drop(index=bad), suspect


def price_quality(ids: list[str], protected: set[str]) -> dict[str, pd.Timestamp | None]:
    """{id: valid_from} for series that need it; valid_from None = unusable.

    A series with more than JUNK_DAYS daily moves beyond +-JUNK_MOVE is junk
    and dropped. Otherwise, a non-positive close or a single-day move beyond
    IMPOSSIBLE_UP / IMPOSSIBLE_DOWN marks everything up to it unusable; the
    series is kept from the next day if at least a year remains. Legacy
    instruments (`protected`) are exempt so the v1 universe is unchanged."""
    out: dict[str, pd.Timestamp | None] = {}
    rows = []
    for sid in ids:
        if sid in protected:
            continue
        df = data.load_ohlcv(sid)
        if df is None:
            continue
        c = df["close"].dropna()
        r = c.pct_change()
        junk = int((r.abs() > JUNK_MOVE).sum())
        bad = c.index[(c <= 0).to_numpy() | (r > IMPOSSIBLE_UP).to_numpy() | (r < IMPOSSIBLE_DOWN).to_numpy()]
        if junk > JUNK_DAYS:
            # junk is usually an early stretch of alternating units; keep what
            # follows the last junk move if a clean year or more remains
            last = r.index[(r.abs() > JUNK_MOVE).to_numpy()][-1]
            cut = c.index[c.index > last]
            if len(cut) < 252:
                out[sid] = None
                rows.append((sid, "dropped", "", f"{junk} daily moves beyond {JUNK_MOVE:.0%}"))
            else:
                out[sid] = cut[0]
                rows.append((sid, "trimmed", str(cut[0].date()),
                             f"{junk} daily moves beyond {JUNK_MOVE:.0%}, the last on {last.date()}"))
        elif len(bad):
            cut = c.index[c.index > bad[-1]]
            if len(cut) < 252:
                out[sid] = None
                rows.append((sid, "dropped", str(bad[-1].date()), "impossible tick, < 1y after it"))
            else:
                out[sid] = cut[0]
                rows.append((sid, "trimmed", str(cut[0].date()), f"impossible tick on {bad[-1].date()}"))
    pd.DataFrame(rows, columns=["id", "action", "valid_from", "reason"]).to_csv(QUALITY_FILE, index=False)
    return out


def write_universe(iv: pd.DataFrame, names: dict[str, str], unpriced: set[str],
                   yahoo_of: dict[str, str], quality: dict | None = None) -> int:
    legacy = data.load_universe("legacy")
    fx = dict(legacy["fx"])
    fx.update(FX_EXTRA)
    rows = []
    quality = quality or {}
    for sid, g in iv.groupby("id"):
        if sid in unpriced or (sid in quality and quality[sid] is None):
            continue
        ysym = yahoo_of[sid]
        _, suf = split_suffix(ysym)
        ccy, region = SUFFIX[suf]
        row = {
            "id": sid, "yahoo": ysym, "name": names.get(ysym) or sid, "type": "stock",
            "region": region, "currency": ccy, "indices": sorted(set(g["index"])),
        }
        if quality.get(sid) is not None:
            row["valid_from"] = quality[sid].strftime("%Y-%m-%d")
        rows.append(row)
    for inst in legacy["instruments"]:
        if inst["type"] == "etf":
            rows.append({k: inst[k] for k in ("id", "yahoo", "name", "type", "region", "currency")}
                        | {"indices": []})
    header = (
        "# Point-in-time selection universe (protocol v2). GENERATED by\n"
        "# scripts/build_membership.py — edit data/membership/sources/ or overrides.yaml\n"
        "# instead. Stocks: every priced name that was ever a member of a tracked index;\n"
        "# WHEN each one is eligible is decided by data/membership/intervals.csv, not by\n"
        "# presence here. ETFs: the legacy universe's ETFs, eligible from their first\n"
        "# price. currency is the Yahoo quote currency (GBX = pence).\n"
    )
    body = yaml.safe_dump({"fx": fx, "instruments": rows}, sort_keys=False, allow_unicode=True,
                          width=200, default_flow_style=None)
    data.UNIVERSE_PIT_FILE.write_text(header + body)
    return len(rows)


def write_coverage(iv: pd.DataFrame, today: pd.Timestamp, unusable: set[str] = frozenset()) -> pd.DataFrame:
    """Per month-end and index: members, members with a price in the last 10
    days, and the share priced. The unpriced share is the survivorship bias
    this universe cannot remove: members Yahoo no longer serves."""
    dates = pd.date_range(COVERAGE_START, today, freq="ME")
    ids = sorted(set(iv["id"]))
    priced = pd.DataFrame(False, index=dates, columns=ids)
    for s in ids:
        df = data.load_ohlcv(s)
        if df is None or df.empty or s in unusable:
            continue
        c = df["close"].dropna()
        pos = c.index.searchsorted(dates, side="right") - 1
        last = pd.DatetimeIndex([c.index[p] if p >= 0 else pd.NaT for p in pos])
        priced[s] = (pos >= 0) & ((dates - last).days <= 10)
    rows = []
    for idx, g in iv.groupby("index"):
        m = membership_mask(g, dates, ids)
        members = m.sum(axis=1)
        have = (m & priced).sum(axis=1)
        rows.append(pd.DataFrame({"index": idx, "members": members, "priced": have}))
    m = membership_mask(iv, dates, ids)
    rows.append(pd.DataFrame({"index": "all", "members": m.sum(axis=1), "priced": (m & priced).sum(axis=1)}))
    cov = pd.concat(rows)
    cov = cov[cov["members"] > 0]
    cov["share_priced"] = (cov["priced"] / cov["members"]).round(4)
    cov.index.name = "date"
    cov = cov.reset_index().sort_values(["date", "index"])
    cov.to_csv(COVERAGE_FILE, index=False, date_format="%Y-%m-%d")
    return cov


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bootstrap", action="store_true", help="rebuild intervals from the historical sources")
    ap.add_argument("--no-prices", action="store_true", help="skip fetching prices for new ids")
    ap.add_argument("--as-of", help="date to stamp changes with (default today)")
    args = ap.parse_args()
    today = pd.Timestamp(args.as_of).normalize() if args.as_of else pd.Timestamp.today().normalize()

    if args.bootstrap:
        iv, names, log = bootstrap(today)
    else:
        iv = load_intervals()
        if iv.empty:
            raise SystemExit("no intervals yet; run with --bootstrap first")
        prev = yaml.safe_load(data.UNIVERSE_PIT_FILE.read_text()) if data.UNIVERSE_PIT_FILE.exists() else {}
        iv, names, log = evolve(iv, today)
        names.update({i["yahoo"]: i["name"] for i in (prev or {}).get("instruments", [])})
    for line in log:
        print(line)
    iv = iv.drop_duplicates().reset_index(drop=True)

    # id -> Yahoo symbol: every name we have seen under its Yahoo symbol
    yahoo_of = {yahoo_to_id(s): s for s in names}
    if data.UNIVERSE_PIT_FILE.exists():
        prev = yaml.safe_load(data.UNIVERSE_PIT_FILE.read_text()) or {}
        yahoo_of.update({i["id"]: i["yahoo"] for i in prev.get("instruments", [])})
    for sid in set(iv["id"]) - set(yahoo_of):
        yahoo_of[sid] = sid   # plain US ticker: id == symbol
    ids = {sid: yahoo_of[sid] for sid in sorted(set(iv["id"]))}
    fx_ids = {spec["id"]: spec["yahoo"] for spec in FX_EXTRA.values()}

    if args.no_prices:
        stored = set(data.store_ids())
        unpriced = {i for i in ids if i not in stored}
    else:
        unpriced = fetch_missing_prices({**ids, **fx_ids}, today)

    iv, suspect = drop_reused_tickers(iv)
    suspect.to_csv(SUSPECT_FILE, index=False, date_format="%Y-%m-%d")
    save_intervals(iv)
    legacy_ids = {i["id"] for i in data.load_universe("legacy")["instruments"]}
    quality = price_quality(sorted(set(iv["id"]) - unpriced), legacy_ids)
    unusable = {k for k, v in quality.items() if v is None}
    n = write_universe(iv, names, unpriced, yahoo_of, quality)
    cov = write_coverage(iv, today, unusable)
    print(f"intervals: {len(iv)} spells over {iv['id'].nunique()} ids; universe: {n} instruments; "
          f"unpriced: {len(unpriced - set(fx_ids))}; suspect spells dropped: {len(suspect)}")
    allc = cov[cov["index"] == "all"].set_index("date")
    print(allc.groupby(pd.to_datetime(allc.index).year).last().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
