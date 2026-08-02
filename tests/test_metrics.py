import numpy as np
import pandas as pd
import pytest

from engine import metrics


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
