import numpy as np
import pandas as pd
import pytest

from engine.backtest import run_backtest, sanitize_weights


def make_prices(n_days=300, n_assets=4, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2020-01-01", periods=n_days)
    rets = rng.normal(0.0003, 0.01, size=(n_days, n_assets))
    prices = 100 * np.exp(np.cumsum(rets, axis=0))
    return pd.DataFrame(prices, index=idx, columns=[f"A{i}" for i in range(n_assets)])


def test_execution_lag_prevents_same_day_capture():
    # Asset A0 jumps +50% on day 10. A strategy that "knows" this and buys on day 10
    # must not capture the jump: weights at t are applied to returns from t+1.
    prices = make_prices()
    jump_day = prices.index[10]
    prices.loc[jump_day:, "A0"] *= 1.5
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    weights.loc[jump_day, "A0"] = 0.25
    res = run_backtest(weights, prices)
    assert res.gross_returns.loc[jump_day] == 0.0  # nothing held during the jump


def test_costs_charged_on_turnover():
    prices = make_prices()
    weights = pd.DataFrame(0.10, index=prices.index, columns=prices.columns)
    res = run_backtest(weights, prices, cost_bps=10, slippage_bps=5)
    # Entering 4 x 10% on the first effective day costs 0.40 * 15bps, then zero.
    entry_day = res.turnover[res.turnover > 0].index[0]
    assert res.turnover.loc[entry_day] == pytest.approx(0.40)
    assert res.costs.loc[entry_day] == pytest.approx(0.40 * 15 / 1e4)
    assert res.turnover.drop(entry_day).sum() == pytest.approx(0.0)


def test_leverage_scaled_down_and_shorts_clipped():
    prices = make_prices()
    weights = pd.DataFrame(0.5, index=prices.index, columns=prices.columns)  # gross 2.0
    weights.iloc[:, 0] = -0.5  # short attempt
    w = sanitize_weights(weights, prices, max_weight=0.25, max_leverage=1.0, allow_short=False)
    assert (w >= 0).all().all()
    assert (w.abs().sum(axis=1) <= 1.0 + 1e-9).all()
    assert (w <= 0.25 + 1e-9).all().all()


def test_unknown_instrument_and_future_dates_rejected():
    prices = make_prices()
    bad_col = pd.DataFrame(0.1, index=prices.index, columns=["NOPE"])
    with pytest.raises(ValueError, match="unknown instruments"):
        sanitize_weights(bad_col, prices, 0.25, 1.0, False)
    future_idx = prices.index.shift(10, freq="B")
    bad_dates = pd.DataFrame(0.1, index=future_idx, columns=prices.columns)
    with pytest.raises(ValueError, match="outside the price calendar"):
        sanitize_weights(bad_dates, prices, 0.25, 1.0, False)


def test_no_weight_on_unlisted_instrument():
    prices = make_prices()
    prices.iloc[:50, 1] = np.nan  # A1 lists late
    weights = pd.DataFrame(0.2, index=prices.index, columns=prices.columns)
    res = run_backtest(weights, prices)
    assert res.weights.iloc[:50]["A1"].abs().sum() == 0.0
