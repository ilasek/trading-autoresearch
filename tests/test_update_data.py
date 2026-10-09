"""The data refresh keeps one adjustment basis per series.

Yahoo adjusts old bars for every new dividend and split; the store keeps rows
as fetched. Without a basis check, a 2:1 split after a series' last stored row
reads as a -50% day and a dividend disappears from the total return.
"""

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_spec = importlib.util.spec_from_file_location(
    "update_data", Path(__file__).resolve().parent.parent / "scripts" / "update_data.py")
update_data = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(update_data)


def bars(closes, idx, volume=1e6):
    c = pd.Series(closes, index=idx, dtype=float)
    return pd.DataFrame({"open": c, "high": c * 1.01, "low": c * 0.99, "close": c,
                         "volume": float(volume)}, index=idx)


def test_a_split_after_the_last_stored_row_is_spliced_on_the_stored_basis(monkeypatch):
    idx = pd.bdate_range("2026-08-03", periods=30)
    raw = np.linspace(100, 110, 30)
    split_day = 20
    raw[split_day:] = raw[split_day:] / 2                     # 2:1 split: the raw price halves
    stored = bars(raw[:split_day], idx[:split_day])           # stored before the split
    # Yahoo after the split: history divided by 2, volume doubled, new rows raw
    fetched = bars(np.r_[raw[:split_day] / 2, raw[split_day:]], idx, volume=2e6)
    monkeypatch.setattr(update_data.data, "load_ohlcv", lambda sid: stored)
    new = update_data.new_rows_for({"id": "X", "type": "stock"}, idx[split_day - 1], fetched)
    spliced = pd.concat([stored["close"], new["close"]])
    assert spliced.pct_change().min() > -0.01                 # no fake -50% day
    assert new["volume"].iloc[0] == pytest.approx(1e6)       # shares back on the stored basis


def test_a_dividend_is_kept_in_the_total_return(monkeypatch):
    idx = pd.bdate_range("2026-08-03", periods=20)
    stored = bars(np.full(10, 100.0), idx[:10])
    # ex-date at row 10: price drops by the 2.0 dividend; Yahoo scales history by 0.98
    fetched = bars(np.r_[np.full(10, 98.0), np.full(10, 98.0)], idx)
    monkeypatch.setattr(update_data.data, "load_ohlcv", lambda sid: stored)
    new = update_data.new_rows_for({"id": "X", "type": "stock"}, idx[9], fetched)
    assert new["close"].iloc[0] / stored["close"].iloc[-1] - 1 == pytest.approx(0.0, abs=1e-12)


def test_rates_and_fx_are_never_rescaled(monkeypatch):
    idx = pd.bdate_range("2026-08-03", periods=10)
    stored = bars(np.full(5, 5.0), idx[:5])
    fetched = bars(np.full(10, 4.0), idx)                     # yields simply moved
    monkeypatch.setattr(update_data.data, "load_ohlcv", lambda sid: stored)
    new = update_data.new_rows_for({"id": "RATE_US3M", "type": "rate"}, idx[4], fetched)
    assert (new["close"] == 4.0).all()


def test_verify_repairs_a_break_spliced_in_by_an_old_refresh():
    idx = pd.bdate_range("2026-06-01", periods=60)
    true = np.linspace(100, 120, 60)
    fetched = bars(true / 2, idx)                             # today's fully adjusted view
    stored_close = true.copy()
    stored_close[40:] = true[40:] / 2                         # an old refresh appended raw rows
    stored = bars(stored_close, idx)
    fixed, drift = update_data.repair_window(stored, fetched, idx[0])
    assert drift > 0.4
    repaired = stored["close"].copy()
    repaired.loc[fixed.index] = fixed["close"]
    assert repaired.pct_change().dropna().abs().max() < 0.01  # one basis again
    assert repaired.iloc[0] == pytest.approx(stored["close"].iloc[0])


def test_verify_leaves_a_consistent_series_alone():
    idx = pd.bdate_range("2026-06-01", periods=60)
    true = np.linspace(100, 120, 60)
    fixed, drift = update_data.repair_window(bars(true, idx), bars(true * 0.97, idx), idx[0])
    assert fixed is None and drift < 1e-9


def test_jump_warnings_flag_big_moves():
    idx = pd.bdate_range("2026-08-03", periods=5)
    stored = bars([100.0], idx[:1])
    new = bars([101.0, 50.0, 51.0, 52.0], idx[1:])
    lines = update_data.jump_warnings("X", stored, new)
    assert len(lines) == 1 and "-50%" in lines[0]


# --- 2026-10-09 refresh failure ------------------------------------------------

def _yf_like(tickers, **kw):
    """What yfinance >= 0.2.48 returns: (Ticker, Price) MultiIndex columns,
    even for a single ticker."""
    idx = pd.bdate_range("2026-09-01", periods=5)
    frames = {t: pd.DataFrame({"Open": 4.0 + i, "High": 4.1 + i, "Low": 3.9 + i, "Close": 4.0 + i,
                               "Volume": 1e3}, index=idx) for i, t in enumerate(tickers)}
    return pd.concat(frames.values(), axis=1, keys=frames.keys(), names=["Ticker", "Price"])


def test_single_symbol_fetch_handles_multiindex_columns(monkeypatch):
    import sys
    import types
    monkeypatch.setitem(sys.modules, "yfinance", types.SimpleNamespace(download=_yf_like))
    one = update_data.data.fetch_yahoo_batch(["^IRX"])
    assert list(one["^IRX"].columns) == update_data.data.OHLCV_COLS
    assert (one["^IRX"]["close"] == 4.0).all()
    many = update_data.data.fetch_yahoo_batch(["AAA", "BBB"])
    assert (many["BBB"]["close"] == 5.0).all()


def test_write_many_refuses_a_multiindex_frame(tmp_path, monkeypatch):
    monkeypatch.setattr(update_data.data, "STORE", tmp_path)
    bad = _yf_like(["^IRX"])
    with pytest.raises(ValueError, match="MultiIndex"):
        update_data.data.write_many({"RATE_US3M": bad})


def test_a_volume_revision_alone_is_not_an_adjustment(monkeypatch):
    idx = pd.bdate_range("2026-10-01", periods=8)
    stored = bars(np.full(5, 100.0), idx[:5], volume=1e6)
    fetched = bars(np.full(8, 100.0), idx, volume=1e10)      # Yahoo restated recent volumes
    monkeypatch.setattr(update_data.data, "load_ohlcv", lambda sid: stored)
    new = update_data.new_rows_for({"id": "X", "type": "stock"}, idx[4], fetched)
    assert (new["volume"] == 1e10).all() and (new["close"] == 100.0).all()
