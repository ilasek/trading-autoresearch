"""Protocol v3 end to end: skill-based deflation counted across versions, the
train-skill gate, the holdout veto against the pool (including for a
version's first champion), holdout numbers kept out of what strategy sessions
read, forward incubation, and mechanism-aware leaderboard rows."""

import json

import numpy as np
import pandas as pd
import pytest

from engine import protocol
from engine.backtest import ExecutionModel
from engine.costs import CostModel
from tests.test_protocol import prices, sandbox  # noqa: F401  (fixtures)


@pytest.fixture
def market():
    """Eight names on one market factor with very different idiosyncratic
    drifts; in the holdout the four weakest (A0-A3) slide."""
    rng = np.random.default_rng(11)
    idx = pd.bdate_range("2012-01-02", "2025-06-30")
    mkt = rng.normal(0.0003, 0.01, len(idx))[:, None]
    mu = np.tile(np.linspace(0.0, 0.003, 8), (len(idx), 1))
    mu[idx >= "2024-01-01", :4] = -0.003
    rets = mkt + rng.normal(mu, 0.006)
    return pd.DataFrame(100 * np.exp(np.cumsum(rets, axis=0)), index=idx,
                        columns=[f"A{i}" for i in range(8)])


def v3_setup(px, rf_annual=0.02):
    types = {c: "stock" for c in px.columns}
    regions = {c: ("US" if i % 2 else "JP") for i, c in enumerate(px.columns)}
    eligible = pd.DataFrame(True, index=px.index, columns=px.columns)
    rf = pd.Series(rf_annual / 252, index=px.index)
    ex = ExecutionModel(rf=rf, costs=CostModel(flat_bps=15.0, regions=regions))
    return protocol.Setup(version=3, splits=protocol.SPLITS_V3, gates=protocol.GATES_V3,
                          universe="legacy", eligible=eligible, types=types, regions=regions,
                          execution=ex)


@pytest.fixture
def v3(sandbox, monkeypatch):  # noqa: F811
    monkeypatch.setattr(protocol, "NULL_DRAWS", 40)
    return sandbox


def write(sandbox, name, src):  # noqa: F811
    p = sandbox / "strategies" / "candidates" / f"{name}.py"
    p.write_text(src)
    return p


EQUAL_WEIGHT = '''
import pandas as pd
STRATEGY = {"name": "ew", "family": "baseline", "track": "scout", "hypothesis": "The pool itself."}
def generate_weights(prices, eligible=None):
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    e = eligible.loc[rebal].astype(float)
    return e.div(e.sum(axis=1), axis=0).fillna(0.0)
'''

# The four highest-drift names, chosen causally from trailing 252-day returns.
TOP4 = '''
import pandas as pd
STRATEGY = {{"name": "{name}", "family": "{family}", "track": "{track}",
            "hypothesis": "Trailing winners keep winning on this synthetic panel."}}
def generate_weights(prices, eligible=None):
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    trail = prices.pct_change(252, fill_method=None)
    rows = {{}}
    for d in rebal:
        s = trail.loc[d].where(eligible.loc[d]).dropna()
        if len(s) < 4:
            continue
        w = pd.Series(0.0, index=prices.columns)
        w[s.nlargest(4).index] = 0.25
        rows[d] = w
    return pd.DataFrame(rows).T
'''

# TOP4 until the holdout starts, then the four weakest names (by date: causal).
DEGRADER = TOP4.replace('    return pd.DataFrame(rows).T', '''    w = pd.DataFrame(rows).T
    late = w.index >= "2024-01-01"
    w.loc[late] = 0.0
    w.loc[late, ["A0", "A1", "A2", "A3"]] = 0.25
    return w''')


def test_v3_trial_records_skill_stresses_and_pool(market, v3):
    setup = v3_setup(market)
    r = protocol.run_trial(write(v3, "top4", TOP4.format(name="top4", family="trend", track="scout")),
                           market, setup=setup)
    assert r.protocol_version == 3
    v = r.validation
    for key in ("skill", "pool_sharpe", "skill_cost2x", "skill_delist30", "ir_vs_pool"):
        assert key in v
    assert v["skill_cost2x"] <= v["skill"] + 1e-9            # doubling costs cannot help
    assert r.skill_ci90 is not None and r.skill_ci90[0] < r.skill < r.skill_ci90[1]
    assert "skill_2009_2017" in r.train                      # a train sub-period
    frame = protocol.load_trial_frame(r.ts, r.name)
    assert set(frame.columns) == {"ret", "pool", "rf"}


def test_v3_train_gate_requires_skill_not_just_a_positive_sharpe(market, v3):
    r = protocol.run_trial(write(v3, "ew", EQUAL_WEIGHT), market, setup=v3_setup(market))
    assert r.train["sharpe"] > 0                             # v2 would have let it through
    assert r.verdict == "GATE_FAIL"
    assert any(x.startswith("train skill") for x in r.reasons)


def test_v3_trial_count_includes_earlier_versions(market, v3):
    setup = v3_setup(market)
    # three v1 records on this validation window, with distinct return series
    rng = np.random.default_rng(0)
    days = market.loc["2018-01-01":"2023-12-31"].index
    for i in range(3):
        ts = f"2026-01-0{i + 1}T00:00:00+00:00"
        protocol.store_trial_returns(ts, f"old{i}", pd.Series(rng.normal(0, 0.01, len(days)), index=days))
        with open(protocol.TRIALS_FILE, "a") as f:
            f.write(json.dumps({"name": f"old{i}", "family": "x", "ts": ts,
                                "validation": {"sharpe": 0.5, "sharpe_daily": 0.03}}) + "\n")
    r = protocol.run_trial(write(v3, "top4", TOP4.format(name="top4", family="trend", track="scout")),
                           market, setup=setup)
    assert r.n_trials == 1                                   # first v3 trial...
    assert r.n_trials_all_versions == 4                      # ...fourth look at the window
    assert r.n_effective_trials == 4


def test_v3_first_champion_faces_the_holdout_veto_against_the_pool(market, v3):
    setup = v3_setup(market)
    r = protocol.run_trial(write(v3, "top4", DEGRADER.format(name="top4", family="trend",
                                                              track="challenge")), market, setup=setup)
    assert r.dsr >= protocol.DSR_THRESHOLD, r.reasons       # it earns a holdout read...
    assert r.verdict == "HOLDOUT_VETO"                       # ...and the holdout refuses it
    assert r.holdout_vetoed_by == ["pool"]
    assert not protocol.CHAMPION_FILE.exists()
    log = [json.loads(x) for x in protocol.holdout_log_file().read_text().splitlines()]
    assert log[-1]["comparisons"]["pool"]["t"] < -protocol.HOLDOUT_VETO_T
    # what strategy sessions read carries the verdict, never the numbers
    rec = json.loads(protocol.TRIALS_FILE.read_text().splitlines()[-1])
    assert rec["holdout"] == {"read": True, "numbers": "experiments/holdout_log.jsonl"}
    assert rec["holdout_t"] is None and rec["champion_holdout_sharpe"] is None
    # and the candidate is frozen for forward scoring
    inc = [json.loads(x) for x in protocol.incubation_file().read_text().splitlines()]
    assert inc[-1]["name"] == "top4" and inc[-1]["data_end"] == "2025-06-30"
    assert (v3 / inc[-1]["frozen_copy"]).read_text() == (v3 / r.candidate).read_text()


def test_v3_promotion_card_has_no_holdout_numbers(market, v3):
    r = protocol.run_trial(write(v3, "top4", TOP4.format(name="top4", family="trend",
                                                          track="challenge")),
                           market, setup=v3_setup(market))
    assert r.verdict == "PROMOTE", r.reasons                 # the splits agree here
    card = json.loads(protocol.CHAMPION_CARD.read_text())
    assert card["holdout"] == {"read": True, "numbers": "experiments/holdout_log.jsonl"}
    assert card["holdout_gate"]["passed"] is True and "t" not in card["holdout_gate"]
    assert card["protocol_version"] == 3 and card["skill"] == r.skill


def test_v3_leaderboard_groups_families_into_mechanisms(market, v3):
    setup = v3_setup(market)
    for name, fam in (("top4_a", "trend"), ("top4_b", "liquidity-volume")):
        protocol.run_trial(write(v3, name, TOP4.format(name=name, family=fam, track="scout")),
                           market, setup=setup)
    board = json.loads(protocol.LEADERBOARD_FILE.read_text())
    fams = board["families"]
    # two labels, one book: one mechanism
    assert fams["trend"]["mechanism"] == fams["liquidity-volume"]["mechanism"]
    assert board["distinct_mechanisms"] == 1
    assert fams["trend"]["skill_ci90"] is not None
