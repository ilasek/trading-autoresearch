"""The survivorship-matched benchmarks: deterministic, construction-matched,
and centred on random selection."""

import numpy as np
import pandas as pd

from engine import benchmarks, metrics


def market(n_days=750, n_assets=40, seed=1, dispersion=0.0004):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2018-01-01", periods=n_days)
    drift = rng.normal(0.0003, dispersion, n_assets)
    rets = rng.normal(drift, 0.015, size=(n_days, n_assets))
    px = pd.DataFrame(100 * np.exp(np.cumsum(rets, axis=0)), index=idx,
                      columns=[f"S{i}" for i in range(n_assets)])
    return px, drift


def monthly_book(px, names_by_month):
    rebal = px.groupby(pd.Grouper(freq="ME")).tail(1).index
    w = pd.DataFrame(0.0, index=px.index, columns=px.columns)
    for i, d in enumerate(rebal):
        w.loc[d:, :] = 0.0
        w.loc[d:, names_by_month(i)] = 1.0 / 8
    return w.shift(1).fillna(0.0)


def test_null_is_deterministic_and_matches_construction():
    px, _ = market()
    elig = pd.DataFrame(True, index=px.index, columns=px.columns)
    types = {c: "stock" for c in px.columns}
    rng = np.random.default_rng(7)
    held = monthly_book(px, lambda i: list(rng.choice(px.columns, 8, replace=False)))
    a, reps = benchmarks.random_null(held, px, elig, types, n_draws=20, seed=3)
    b, _ = benchmarks.random_null(held, px, elig, types, n_draws=20, seed=3)
    assert np.array_equal(a, b)
    assert len(reps) == 3


def test_random_selection_sits_mid_distribution_and_skill_does_not():
    # wide cross-sectional drift dispersion, so an oracle's skill is resolvable
    px, drift = market(dispersion=0.0012)
    elig = pd.DataFrame(True, index=px.index, columns=px.columns)
    types = {c: "stock" for c in px.columns}
    best = list(px.columns[np.argsort(drift)[-8:]])     # oracle: highest true drift
    skilled_book = monthly_book(px, lambda i: best)

    def pctile(held):
        r = benchmarks._returns(held, px, 10.0, 5.0)     # same costs as the replicas
        sh, _ = benchmarks.random_null(held, px, elig, types, n_draws=60, seed=5)
        return (sh < metrics.sharpe(r)).mean()

    # any one random book can be lucky (8 names, 3 years: the null is wide);
    # on average random selection must land mid-distribution
    random_pcts = []
    for seed in range(6):
        rng = np.random.default_rng(seed)
        random_pcts.append(pctile(monthly_book(px, lambda i: list(rng.choice(px.columns, 8, replace=False)))))
    assert 0.3 < np.mean(random_pcts) < 0.7
    assert pctile(skilled_book) > 0.95


def test_null_draws_only_from_names_eligible_on_the_decision_day():
    px, _ = market(n_assets=20)
    elig = pd.DataFrame(False, index=px.index, columns=px.columns)
    elig[["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]] = True
    types = {c: "stock" for c in px.columns}
    held = monthly_book(px, lambda i: ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7"])
    # A replica holding an ineligible name would show S10..S19's returns: make
    # those names explode so any such draw is unmistakable.
    px_bad = px.copy()
    px_bad.iloc[:, 10:] *= np.linspace(1, 100, len(px))[:, None]
    a, _ = benchmarks.random_null(held, px, elig, types, n_draws=10, seed=0)
    b, _ = benchmarks.random_null(held, px_bad, elig, types, n_draws=10, seed=0)
    assert np.allclose(a, b)


def test_equal_weight_uses_only_eligible_names():
    px, _ = market(n_assets=10)
    elig = pd.DataFrame(True, index=px.index, columns=px.columns)
    elig["S0"] = False
    px_bad = px.copy()
    px_bad["S0"] = px_bad["S0"] * np.linspace(1, 50, len(px))   # would dominate if held
    r_ok = benchmarks.equal_weight(px, elig, None, None)
    r_bad = benchmarks.equal_weight(px_bad, elig, None, None)
    pd.testing.assert_series_equal(r_ok, r_bad)
