import numpy as np
import pandas as pd
import pytest

from engine import metrics


def _paired_series(n_days, rho, sharpe_a_daily, sharpe_b_daily, seed=0):
    """Two return series with *exactly* the requested sample correlation and
    daily Sharpe ratios, so a test can assert on the closed form rather than on
    a lucky draw."""
    rng = np.random.default_rng(seed)
    norm = lambda v: (v - v.mean()) / v.std(ddof=1)
    a = norm(rng.standard_normal(n_days))
    b = rng.standard_normal(n_days)
    b = norm(b - (np.dot(b, a) / np.dot(a, a)) * a)     # exact Gram-Schmidt
    c = norm(rho * a + np.sqrt(1 - rho**2) * b)
    idx = pd.bdate_range("2018-01-01", periods=n_days)
    return (
        pd.Series(a * 0.01 + sharpe_a_daily * 0.01, index=idx),
        pd.Series(c * 0.01 + sharpe_b_daily * 0.01, index=idx),
    )


def test_sharpe_diff_se_reproduces_the_repos_recorded_value():
    """The comparison the holdout gate turns on, against a number this repo
    already published: `mom_zscore_overlap6_hzn_avg4` vs the champion on
    validation — rho 0.939 over 1562 days, paired SE 0.140."""
    a, b = _paired_series(1562, 0.939, 0.077424, 0.070556)
    se, rho = metrics.sharpe_diff_se(a, b)
    assert rho == pytest.approx(0.939, abs=1e-6)
    assert se == pytest.approx(0.140, abs=0.002)


def test_sharpe_diff_se_tightens_as_strategies_correlate():
    """Why the gate pairs at all: near-identical books resolve far finer
    differences than distinct ones do."""
    tight, _ = metrics.sharpe_diff_se(*_paired_series(1562, 0.997, 0.077, 0.070))
    loose, _ = metrics.sharpe_diff_se(*_paired_series(1562, 0.900, 0.077, 0.070))
    assert tight < loose / 3


def test_sharpe_diff_se_refuses_to_resolve_degenerate_comparisons():
    """A degenerate pair must veto nothing: infinite SE drives every t to zero."""
    a, b = _paired_series(400, 0.9, 0.05, 0.05)
    flat = pd.Series(np.zeros(len(a)), index=a.index)
    assert metrics.sharpe_diff_se(a, flat)[0] == float("inf")
    assert metrics.sharpe_diff_se(a.iloc[:10], b.iloc[:10])[0] == float("inf")


def test_max_drawdown_known_case():
    # Equity 1 -> 2 -> 1 -> 3: worst drawdown is -50%.
    rets = pd.Series([1.0, -0.5, 2.0])
    assert metrics.max_drawdown(rets) == pytest.approx(-0.5)


def test_sharpe_positive_for_positive_drift():
    rng = np.random.default_rng(1)
    rets = pd.Series(rng.normal(0.001, 0.01, 2000))
    assert metrics.sharpe(rets) > 1.0
    assert metrics.sortino(rets) > metrics.sharpe(rets) * 0.5


def test_probabilistic_sharpe_monotone_in_benchmark():
    rng = np.random.default_rng(2)
    rets = pd.Series(rng.normal(0.0005, 0.01, 1500))
    assert metrics.probabilistic_sharpe(rets, 0.0) > metrics.probabilistic_sharpe(rets, 0.05)


def test_deflated_sharpe_decreases_with_more_trials():
    rng = np.random.default_rng(3)
    rets = pd.Series(rng.normal(0.0006, 0.01, 1500))
    few = metrics.deflated_sharpe(rets, [0.01, 0.02])
    many_trials = list(rng.normal(0.02, 0.02, 200))
    many = metrics.deflated_sharpe(rets, many_trials)
    assert many < few


def test_norm_ppf_roundtrip():
    for p in (0.01, 0.25, 0.5, 0.9, 0.99):
        assert metrics._norm_cdf(metrics._norm_ppf(p)) == pytest.approx(p, abs=1e-6)
