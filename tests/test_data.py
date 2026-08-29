"""The auxiliary panels' alignment contract.

`load_panels` promises every frame shares `load_prices()`'s index and column
order. The protocol truncates prices and panels by the same slice and relies on
that promise; without it the causality check compares a strategy against panels
it never actually saw.
"""

import pandas as pd
import pytest

from engine import data

pytestmark = pytest.mark.skipif(
    not (data.STORE.exists() and any(data.STORE.glob("*.parquet"))),
    reason="data store not present",
)


def test_panels_align_to_prices():
    prices = data.load_prices()
    panels = data.load_panels()
    assert set(panels) == {"open", "high", "low", "volume", "dollar_volume"}
    for name, frame in panels.items():
        assert frame.index.equals(prices.index), name
        assert list(frame.columns) == list(prices.columns), name


def test_volume_is_not_forward_filled_or_fx_converted():
    """Volume is a share count. Multiplying it by an FX rate, or filling a
    foreign holiday's missing bar, would corrupt every liquidity measure built
    on it — so it is left alone and callers see the NaN."""
    panels = data.load_panels(fields=("volume",))
    volume = panels["volume"]
    assert volume.isna().any().any()
    raw = data.load_ohlcv("BMW_DE")
    if raw is not None:
        shared = volume.index.intersection(raw.index)[-50:]
        pd.testing.assert_series_equal(
            volume.loc[shared, "BMW_DE"].dropna(),
            raw.loc[shared, "volume"].astype(float).reindex(shared).dropna(),
            check_names=False,
        )


def test_dollar_volume_is_usd_notional():
    prices = data.load_prices()
    panels = data.load_panels()
    expected = panels["volume"] * prices
    pd.testing.assert_frame_equal(panels["dollar_volume"], expected)
