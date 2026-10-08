"""Protocol v3's execution model, cost model, statistics and ranking.

The load-bearing test is `test_fill_waits_for_the_next_real_print`: on a
calendar that is the union of time zones, the legacy model lets a strategy buy
a Tokyo stock at Tokyo's close using a US close ~15 hours later. That is
look-ahead the causality check cannot see (it truncates rows; this lives
inside one row), and it turns a pure lead-lag artifact into a Sharpe of ~7.6.
"""

import numpy as np
import pandas as pd
import pytest

from engine import benchmarks, metrics, ranking
from engine.backtest import ExecutionModel, decision_targets, run_backtest, simulate
from engine.costs import CostModel, liquidity_bps, tax_tables


def lead_lag_market(n=2000, seed=0):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2010-01-01", periods=n)
    us = rng.normal(0, 0.01, n)
    jp = np.r_[0, 0.8 * us[:-1]] + rng.normal(0, 0.006, n)   # Tokyo reacts a session later
    return pd.DataFrame({"US": 100 * np.cumprod(1 + us), "JP": 100 * np.cumprod(1 + jp)}, index=idx)


def ann_sharpe(r):
    return float(r.mean() / r.std() * np.sqrt(252))


FREE = ExecutionModel(costs=CostModel(flat_bps=0.0, taxes=False))


def test_fill_waits_for_the_next_real_print():
    px = lead_lag_market()
    signal = (px["US"].pct_change() > 0).astype(float)      # known only at the US close
    w = pd.DataFrame({"US": 0.0, "JP": signal}, index=px.index)
    legacy = run_backtest(w, px, cost_bps=0.0, slippage_bps=0.0)
    v3 = run_backtest(w, px, execution=FREE)
    assert ann_sharpe(legacy.returns) > 3.0                  # the artifact
    assert abs(ann_sharpe(v3.returns)) < 1.0                 # gone


def test_a_holiday_delays_the_fill_instead_of_using_a_stale_price():
    px = lead_lag_market(n=60)
    traded = pd.DataFrame(True, index=px.index, columns=px.columns)
    d = px.index[10]
    traded.loc[px.index[11], "JP"] = False                   # Tokyo closed the day after
    w = pd.DataFrame({"US": [0.5], "JP": [0.5]}, index=[d])
    res = run_backtest(w, px, execution=ExecutionModel(traded=traded, costs=CostModel(flat_bps=0.0)))
    held = res.weights
    # US fills at the row-11 close and is held from row 12; JP waits for row 12's print
    assert held.loc[px.index[11]].abs().sum() == 0.0
    assert held.loc[px.index[12], "US"] > 0 and held.loc[px.index[12], "JP"] == 0.0
    assert held.loc[px.index[13], "JP"] > 0


def test_holdings_drift_and_rebalancing_is_charged():
    px = lead_lag_market(n=500)
    ex = ExecutionModel(costs=CostModel(flat_bps=15.0, taxes=False))
    once = run_backtest(pd.DataFrame({"US": [0.5], "JP": [0.5]}, index=px.index[:1]), px, execution=ex)
    daily = run_backtest(pd.DataFrame(0.5, index=px.index, columns=px.columns), px, execution=ex)
    # emitted once: weights wander with prices and nothing is traded after entry
    assert once.weights["US"].iloc[100:].std() > 1e-3
    assert once.turnover.iloc[5:].sum() == pytest.approx(0.0)
    # emitted daily: the book is pulled back to 50/50 every day, and pays for it
    assert daily.turnover.iloc[5:].sum() > 0.1
    assert daily.costs.sum() > once.costs.sum()


def test_cash_earns_the_risk_free_rate_and_sharpe_is_on_excess():
    px = lead_lag_market(n=300)
    rf = pd.Series(0.04 / 252, index=px.index)
    empty = pd.DataFrame(0.0, index=px.index[:1], columns=px.columns)
    res = run_backtest(empty, px, execution=ExecutionModel(rf=rf))
    assert res.returns.iloc[1:].to_numpy() == pytest.approx(0.04 / 252)
    assert metrics.sharpe(res.returns, rf) == 0.0            # cash is not a 30-Sharpe strategy


def test_series_ending_while_held_is_exited_and_haircut_stress_books_a_loss():
    px = lead_lag_market(n=300)
    px.loc[px.index[150]:, "JP"] = np.nan                    # JP's series ends
    w = pd.DataFrame({"US": [0.5], "JP": [0.5]}, index=px.index[:1])
    base = run_backtest(w, px, execution=ExecutionModel(costs=CostModel(flat_bps=0.0)))
    hit = run_backtest(w, px, execution=ExecutionModel(costs=CostModel(flat_bps=0.0),
                                                       delist_haircut=0.30))
    day = px.index[150]
    assert base.delisted.loc[day] > 0.1                      # the drifted JP weight
    assert base.weights.loc[px.index[151], "JP"] == 0.0
    assert hit.returns.loc[day] == pytest.approx(
        base.returns.loc[day] - 0.30 * base.delisted.loc[day], abs=1e-3)


def test_decision_targets_match_the_legacy_sanitizer_on_emitted_rows():
    px = lead_lag_market(n=100)
    w = pd.DataFrame({"US": [0.9, np.nan], "JP": [0.9, 0.2]}, index=px.index[[5, 50]])
    t = decision_targets(w, px, 0.25, 1.0, False)
    assert t.loc[px.index[5]].tolist() == [0.25, 0.25]       # capped
    assert t.loc[px.index[50], "US"] == 0.25                  # NaN carries the last instruction


def test_cost_model_tiers_and_taxes():
    assert liquidity_bps(np.array([2e8, 5e7, 1e7, 1e6, np.nan])).tolist() == [15, 20, 30, 40, 30]
    idx = pd.bdate_range("2020-01-01", "2024-12-31")
    regions, buy, sell = tax_tables(idx)
    uk, hk = regions.index("UK"), regions.index("HK")
    assert buy[0, uk] == 50 and sell[0, uk] == 0                     # UK stamp duty on purchases
    assert buy[idx.get_loc(pd.Timestamp("2022-06-01")), hk] == 13    # HK 0.13% in 2021-23
    model = CostModel(regions={"A": "UK", "B": "US"}).prepare(idx, pd.Index(["A", "B"]))
    # no liquidity panel: the flat 15 bps on both, plus 50 bps stamp duty on the UK purchase
    cost = model.trade_cost(0, np.array([0, 1]), np.array([0.1, 0.1]))
    assert cost == pytest.approx((0.1 * 15 + 0.1 * 15 + 0.1 * 50) / 1e4)
    assert model.trade_cost(0, np.array([0]), np.array([-0.1])) == pytest.approx(0.1 * 15 / 1e4)
    adv = pd.DataFrame({"A": 2e8, "B": 1e6}, index=idx)
    liquid = CostModel(adv=adv, regions={"A": "UK", "B": "US"}, taxes=False).prepare(
        idx, pd.Index(["A", "B"]))
    assert liquid.trade_cost(0, np.array([0, 1]), np.array([0.1, 0.1])) == \
        pytest.approx((0.1 * 15 + 0.1 * 40) / 1e4)


def test_stationary_bootstrap_is_deterministic_and_in_range():
    a = metrics.stationary_bootstrap_indices(500, n_boot=50, seed=1)
    b = metrics.stationary_bootstrap_indices(500, n_boot=50, seed=1)
    assert a.shape == (50, 500) and np.array_equal(a, b)
    assert a.min() >= 0 and a.max() < 500
    # blocks: most consecutive indices advance by one
    assert (np.diff(a, axis=1) == 1).mean() > 0.9


def test_deflated_skill_is_centred_on_the_pool_not_on_zero():
    # a book with no skill (skill 0) can never look better than a coin flip,
    # however high its raw Sharpe; real skill well above the luck benchmark can
    for n in (2, 10, 50):
        assert metrics.deflated_skill(0.0, 0.25, [0.0, 0.1, -0.1, 0.05], n) < 0.5
    trials = [0.0, 0.1, -0.1, 0.05, 0.2, -0.05, 0.15, 1.5]
    assert metrics.deflated_skill(1.5, 0.25, trials, 10) > 0.95
    # more effective trials -> a higher bar
    assert (metrics.deflated_skill(0.8, 0.25, [0.0, 0.3, -0.2, 0.8], 50)
            < metrics.deflated_skill(0.8, 0.25, [0.0, 0.3, -0.2, 0.8], 5))


def test_paired_bootstrap_resolves_a_drag_and_not_noise():
    rng = np.random.default_rng(3)
    idx = pd.bdate_range("2018-01-01", periods=1500)
    base = pd.Series(rng.normal(0.0004, 0.01, len(idx)), index=idx)
    dragged = base - 0.0004                                   # same book, 10%/yr worse
    out = metrics.sharpe_diff_bootstrap(base, dragged)
    assert out["lo"] > 0 and out["rho"] > 0.99
    other = pd.Series(rng.normal(0.0004, 0.01, len(idx)), index=idx)
    noisy = metrics.sharpe_diff_bootstrap(base, other)
    assert noisy["lo"] < 0 < noisy["hi"]


def test_confidence_set_drops_the_clearly_worse_and_keeps_the_indistinguishable():
    rng = np.random.default_rng(5)
    idx = pd.bdate_range("2018-01-01", periods=1500)
    common = rng.normal(0.0004, 0.01, len(idx))
    frame = pd.DataFrame({
        "a": common + rng.normal(0, 0.002, len(idx)),
        "b": common + rng.normal(0, 0.002, len(idx)),        # a twin of a
        "worse": common - 0.0008 + rng.normal(0, 0.002, len(idx)),
    }, index=idx)
    pool = pd.Series(common, index=idx)
    table = ranking.rank_table(frame, pool, n_boot=400)
    assert set(table.index[table["in_mcs"]]) == {"a", "b"}
    assert table.loc["worse", "tier"] == 3
    assert table["p_best"].sum() == pytest.approx(1.0)


def test_mechanism_clusters_use_active_returns():
    rng = np.random.default_rng(9)
    idx = pd.bdate_range("2018-01-01", periods=1000)
    mkt = rng.normal(0, 0.01, len(idx))
    sig1, sig2 = rng.normal(0, 0.003, len(idx)), rng.normal(0, 0.003, len(idx))
    active = pd.DataFrame({"rev_a": sig1, "rev_b": sig1 + rng.normal(0, 0.001, len(idx)),
                           "mom": sig2}, index=idx)
    raw = active.add(mkt, axis=0)
    assert raw.corr().min().min() > 0.7                      # everything looks alike raw
    c = ranking.mechanism_clusters(active)
    assert c["rev_a"] == c["rev_b"] != c["mom"]


def region_market(n=600, seed=2):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2018-01-01", periods=n)
    cols = [f"US{i}" for i in range(10)] + [f"JP{i}" for i in range(10)]
    px = pd.DataFrame(100 * np.exp(np.cumsum(rng.normal(0.0003, 0.012, (n, 20)), axis=0)),
                      index=idx, columns=cols)
    types = {c: "stock" for c in cols}
    regions = {c: c[:2] for c in cols}
    return px, types, regions


def test_v3_null_is_deterministic_and_region_matched():
    px, types, regions = region_market()
    elig = pd.DataFrame(True, index=px.index, columns=px.columns)
    rebal = px.groupby(pd.Grouper(freq="ME")).tail(1).index
    targets = pd.DataFrame(0.0, index=rebal, columns=px.columns)
    targets[["JP0", "JP1", "JP2", "JP3"]] = 0.25             # an all-Japan book
    window = (px.index[100], px.index[-1])
    a, _ = benchmarks.random_null_v3(targets, px, elig, types, regions, FREE, window, 15, seed=1)
    b, _ = benchmarks.random_null_v3(targets, px, elig, types, regions, FREE, window, 15, seed=1)
    assert np.array_equal(a, b)
    # replicas never hold a US name: make the US names explode and nothing changes
    px_bad = px.copy()
    px_bad.loc[:, [c for c in px.columns if c.startswith("US")]] *= \
        np.linspace(1, 50, len(px))[:, None]
    c, _ = benchmarks.random_null_v3(targets, px_bad, elig, types, regions, FREE, window, 15, seed=1)
    assert np.allclose(a, c)


def test_v3_equal_weight_pool_uses_only_eligible_names():
    px, _, _ = region_market(n=300)
    elig = pd.DataFrame(True, index=px.index, columns=px.columns)
    elig["US0"] = False
    bad = px.copy()
    bad["US0"] *= np.linspace(1, 50, len(px))
    pd.testing.assert_series_equal(benchmarks.equal_weight_v3(px, elig, FREE),
                                   benchmarks.equal_weight_v3(bad, elig, FREE))


def test_simulate_from_a_start_takes_the_instruction_in_force():
    px = lead_lag_market(n=300)
    targets = pd.DataFrame({"US": [1.0], "JP": [0.0]}, index=px.index[:1])
    t = decision_targets(targets, px, 1.0, 1.0, False)
    res = simulate(t, px, FREE, start=px.index[100])
    assert res.weights.loc[px.index[102], "US"] > 0.99
