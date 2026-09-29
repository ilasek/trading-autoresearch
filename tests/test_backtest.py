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


# --- protocol v2: the point-in-time universe is enforced by the engine -------

def test_never_eligible_name_gets_no_weight():
    prices = make_prices()
    weights = pd.DataFrame(0.25, index=prices.index[::21], columns=prices.columns)
    eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    eligible["A0"] = False
    res = run_backtest(weights, prices, eligible=eligible)
    assert (res.weights["A0"] == 0).all()
    assert (res.weights["A1"].iloc[5:] > 0).all()


def test_late_joiner_is_bought_only_after_joining_and_held_to_next_rebalance():
    prices = make_prices()
    rebal = prices.index[::21]
    weights = pd.DataFrame(0.25, index=rebal, columns=prices.columns)
    eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    join, leave = rebal[3], prices.index[100]           # leaves between rebalances
    eligible.loc[: join - pd.Timedelta(days=1), "A0"] = False
    eligible.loc[leave:, "A0"] = False
    w = sanitize_weights(weights, prices, 0.25, 1.0, False, eligible)
    assert (w.loc[: join - pd.Timedelta(days=1), "A0"] == 0).all()
    assert w.loc[join, "A0"] == 0.25
    next_rebal = rebal[rebal >= leave][0]
    assert (w.loc[leave: next_rebal - pd.Timedelta(days=1), "A0"] == 0.25).all()
    assert (w.loc[next_rebal:, "A0"] == 0).all()


def test_position_in_a_series_that_ends_exits_at_last_price():
    """A delisted series (NaN after its last bar) is exited at its last price:
    no return on the missing days, and the exit is charged as turnover."""
    prices = make_prices()
    last = prices.index[150]
    prices.loc[prices.index > last, "A0"] = np.nan
    weights = pd.DataFrame(0.25, index=prices.index[:1], columns=prices.columns)
    res = run_backtest(weights, prices, cost_bps=10.0, slippage_bps=5.0)
    after = prices.index[prices.index > last]
    assert (res.weights.loc[after[1]:, "A0"] == 0).all()
    assert res.turnover.loc[after[1]] == pytest.approx(0.25)
    assert np.isfinite(res.returns).all()
