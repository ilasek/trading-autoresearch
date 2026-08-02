"""Data layer: Parquet store loader + throttled Stooq/Yahoo fetchers.

Research code must only use the loaders (load_universe, load_prices). The fetchers
are for scripts/seed_data.py and scripts/update_data.py — never call them from a
strategy or during an experiment.
"""

from __future__ import annotations

import io
import time
from pathlib import Path

import pandas as pd
import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "data" / "store"
UNIVERSE_FILE = ROOT / "data" / "universe.yaml"

OHLCV_COLS = ["open", "high", "low", "close", "volume"]

_STOOQ_URL = "https://stooq.com/q/d/l/?s={symbol}&i=d"
_MIN_REQUEST_INTERVAL = 1.2  # seconds between Stooq requests
_last_request_ts = 0.0


class RateLimitError(RuntimeError):
    """Raised when a data provider signals we exceeded its limits."""


# ---------------------------------------------------------------------------
# Universe
# ---------------------------------------------------------------------------

def load_universe() -> dict:
    """Full parsed universe.yaml: {'fx': {...}, 'instruments': [...]}."""
    with open(UNIVERSE_FILE) as f:
        return yaml.safe_load(f)


def instruments(types: tuple[str, ...] = ("stock", "etf")) -> list[dict]:
    return [i for i in load_universe()["instruments"] if i["type"] in types]


def all_series() -> list[dict]:
    """Every series we store: instruments plus FX pairs."""
    uni = load_universe()
    fx = [dict(v, type="fx", currency="USD") for v in uni["fx"].values()]
    return uni["instruments"] + fx


# ---------------------------------------------------------------------------
# Store I/O
# ---------------------------------------------------------------------------

def store_path(series_id: str) -> Path:
    return STORE / f"{series_id}.parquet"


def load_ohlcv(series_id: str) -> pd.DataFrame | None:
    """One series as a date-indexed OHLCV frame, or None if not in the store."""
    path = store_path(series_id)
    if not path.exists():
        return None
    df = pd.read_parquet(path)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def write_ohlcv(series_id: str, df: pd.DataFrame) -> None:
    """Merge new rows into the store (idempotent: dedupes on date, keeps latest)."""
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    existing = load_ohlcv(series_id)
    if existing is not None:
        df = pd.concat([existing, df])
    df = df[~df.index.duplicated(keep="last")].sort_index()
    STORE.mkdir(parents=True, exist_ok=True)
    df.to_parquet(store_path(series_id))


def last_date(series_id: str) -> pd.Timestamp | None:
    df = load_ohlcv(series_id)
    return None if df is None or df.empty else df.index[-1]


# ---------------------------------------------------------------------------
# Research loader
# ---------------------------------------------------------------------------

def _fx_to_usd(currency: str, universe: dict) -> pd.Series:
    """Multiplicative series converting one unit of `currency` to USD."""
    if currency == "USD":
        raise ValueError("no FX needed for USD")
    scale = 1.0
    if currency == "GBX":  # LSE pence
        currency, scale = "GBP", 0.01
    spec = universe["fx"][currency]
    df = load_ohlcv(spec["id"])
    if df is None:
        raise FileNotFoundError(
            f"FX series {spec['id']} missing from store; run scripts/seed_data.py"
        )
    rate = df["close"]
    if spec.get("invert"):
        rate = 1.0 / rate
    return rate * scale


def load_prices(
    types: tuple[str, ...] = ("stock", "etf"),
    currency: str = "USD",
    field: str = "close",
) -> pd.DataFrame:
    """Wide frame (dates x instrument ids) of daily prices converted to USD.

    Instruments missing from the store are skipped with a warning column count
    difference; NaN before an instrument's first bar is expected and strategies
    must handle it.
    """
    if currency != "USD":
        raise ValueError("only USD target currency is supported")
    universe = load_universe()
    cols: dict[str, pd.Series] = {}
    fx_cache: dict[str, pd.Series] = {}
    for inst in universe["instruments"]:
        if inst["type"] not in types:
            continue
        df = load_ohlcv(inst["id"])
        if df is None or df.empty:
            continue
        series = df[field].astype(float)
        cur = inst["currency"]
        if cur != "USD":
            if cur not in fx_cache:
                fx_cache[cur] = _fx_to_usd(cur, universe)
            fx = fx_cache[cur].reindex(series.index).ffill()
            series = series * fx
        cols[inst["id"]] = series
    if not cols:
        raise FileNotFoundError("data store is empty; run scripts/seed_data.py")
    prices = pd.DataFrame(cols).sort_index()
    # Drop weekend/garbage rows where nearly nothing traded.
    prices = prices.dropna(how="all")
    # The index is the union of all exchange calendars, so every column has
    # holes on foreign holidays. Forward-fill briefly so rolling windows and
    # returns behave; the cap keeps genuinely dead series NaN (and the engine
    # zeroes weights on NaN prices).
    prices = prices.ffill(limit=10)
    return prices


# ---------------------------------------------------------------------------
# Fetchers (scripts only)
# ---------------------------------------------------------------------------

def _throttle() -> None:
    global _last_request_ts
    wait = _MIN_REQUEST_INTERVAL - (time.monotonic() - _last_request_ts)
    if wait > 0:
        time.sleep(wait)
    _last_request_ts = time.monotonic()


def fetch_stooq(stooq_symbol: str, start: str | None = None, retries: int = 3) -> pd.DataFrame:
    """Full (or from `start`) daily history from Stooq as an OHLCV frame.

    Stooq needs no API key but enforces a daily hits limit per IP; we throttle and
    raise RateLimitError when the limit is hit so callers can stop cleanly.
    """
    url = _STOOQ_URL.format(symbol=stooq_symbol)
    if start:
        url += "&d1=" + pd.Timestamp(start).strftime("%Y%m%d")
    for attempt in range(retries):
        _throttle()
        resp = requests.get(url, timeout=30, headers={"User-Agent": "trading-autoresearch/0.1"})
        text = resp.text
        if "Exceeded the daily hits limit" in text or "przekroczony dzienny limit" in text.lower():
            raise RateLimitError(f"Stooq daily limit hit while fetching {stooq_symbol}")
        if "requires JavaScript to verify your browser" in text:
            # Anti-bot verification page. We do not work around it — callers
            # should switch to the Yahoo backend instead.
            raise RateLimitError(
                f"Stooq is serving a browser-verification page for {stooq_symbol}; "
                "use the Yahoo backend"
            )
        if resp.status_code == 200 and text.startswith("Date,"):
            df = pd.read_csv(io.StringIO(text), parse_dates=["Date"], index_col="Date")
            df.columns = [c.lower() for c in df.columns]
            if "volume" not in df.columns:
                df["volume"] = float("nan")
            return df[OHLCV_COLS]
        if resp.status_code == 200 and text.strip().lower() in ("no data", "brak danych"):
            raise FileNotFoundError(f"Stooq has no data for {stooq_symbol}")
        time.sleep(2.0 * (attempt + 1))
    raise RuntimeError(
        f"Stooq fetch failed for {stooq_symbol}: HTTP {resp.status_code}, body starts "
        f"{text[:80]!r}"
    )


def fetch_yahoo_batch(yahoo_symbols: list[str], start: str | None = None) -> dict[str, pd.DataFrame]:
    """Batched Yahoo download via yfinance (primary backend).

    start=None fetches maximum available history. One yf.download call handles
    many tickers with shared session/throttling. Returns {yahoo_symbol: OHLCV
    frame}; symbols that fail are simply absent.
    """
    import yfinance as yf  # imported lazily; only scripts need it

    kwargs = dict(start=start) if start else dict(period="max")
    raw = yf.download(
        yahoo_symbols, interval="1d", group_by="ticker",
        auto_adjust=True, progress=False, threads=False, **kwargs,
    )
    out: dict[str, pd.DataFrame] = {}
    if raw is None or raw.empty:
        return out
    for sym in yahoo_symbols:
        try:
            df = raw[sym] if len(yahoo_symbols) > 1 else raw
        except KeyError:
            continue
        df = df.dropna(how="all")
        if df.empty:
            continue
        df = df.rename(columns=str.lower)
        for col in OHLCV_COLS:
            if col not in df.columns:
                df[col] = float("nan")
        out[sym] = df[OHLCV_COLS]
    return out
