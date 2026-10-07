import json

import numpy as np
import pandas as pd
import pytest

from engine import protocol


@pytest.fixture
def prices():
    """Synthetic global market 2010-2025: random walks with mild drift."""
    rng = np.random.default_rng(42)
    idx = pd.bdate_range("2010-01-04", "2025-06-30")
    n = len(idx)
    n_assets = 8
    drift = rng.uniform(0.0001, 0.0005, n_assets)
    rets = rng.normal(drift, 0.012, size=(n, n_assets))
    px = 100 * np.exp(np.cumsum(rets, axis=0))
    return pd.DataFrame(px, index=idx, columns=[f"A{i}" for i in range(n_assets)])


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    """Redirect all protocol state files into a temp dir.

    Pins the default protocol to v1: these synthetic prices have no membership
    data, and the gates, holdout veto and tracks under test are shared by both
    versions. v2 tests build their own `Setup` (see `_v2_setup`)."""
    monkeypatch.setattr(protocol, "PROTOCOL_VERSION", 1)
    monkeypatch.setattr(protocol, "ROOT", tmp_path)
    monkeypatch.setattr(protocol, "CHAMPION_FILE", tmp_path / "strategies" / "champion.py")
    monkeypatch.setattr(protocol, "CHAMPION_CARD", tmp_path / "strategies" / "champion_card.json")
    monkeypatch.setattr(protocol, "ARCHIVE_DIR", tmp_path / "strategies" / "archive")
    monkeypatch.setattr(protocol, "TRIALS_FILE", tmp_path / "experiments" / "trials.jsonl")
    monkeypatch.setattr(
        protocol, "LEADERBOARD_FILE", tmp_path / "experiments" / "leaderboard.json"
    )
    (tmp_path / "strategies" / "candidates").mkdir(parents=True)
    return tmp_path


CAUSAL_STRATEGY = '''
import pandas as pd
STRATEGY = {"name": "equal_weight_monthly", "family": "baseline",
            "hypothesis": "Equal weight everything, rebalanced monthly."}
def generate_weights(prices):
    monthly = prices.resample("ME").last().index
    monthly = monthly.intersection(prices.index).union(prices.index[:1])
    w = pd.DataFrame(1.0 / prices.shape[1], index=monthly, columns=prices.columns)
    return w
'''

PEEKING_STRATEGY = '''
import numpy as np
import pandas as pd
STRATEGY = {"name": "peeker", "family": "bug",
            "hypothesis": "Cheat by weighting on full-sample means (lookahead)."}
def generate_weights(prices):
    score = prices.pct_change().mean().clip(lower=0)   # uses the entire future
    row = score / score.sum()
    w = pd.DataFrame(np.tile(row.values, (len(prices.index), 1)),
                     index=prices.index, columns=prices.columns)
    return w
'''


SPARSE_REBALANCE_STRATEGY = '''
import pandas as pd
STRATEGY = {"name": "sparse_monthly", "family": "baseline",
            "hypothesis": "Causal, rebalances on each month's last observed trading day."}
def generate_weights(prices):
    # groupby-tail(1) makes the final row a partial-month rebalance whose date
    # moves with truncation — causal, but a raw-frame diff would flag it.
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    return pd.DataFrame(1.0 / prices.shape[1], index=rebal, columns=prices.columns)
'''


# Both holdout fixtures below beat the equal-weight champion on validation by the
# same tilt, and differ only in what they do after the holdout starts. Tilting by
# calendar date is causal — the rule reads the date, never a future price — so
# both pass the causality check and reach the holdout gate.
_HOLDOUT_TILT = '''
import pandas as pd
STRATEGY = {{"name": "{name}", "family": "baseline",
            "hypothesis": "{hypothesis}"}}
def generate_weights(prices):
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    w = pd.DataFrame(1.0 / prices.shape[1], index=rebal, columns=prices.columns)
    val = (w.index >= "2018-01-01") & (w.index <= "2023-12-31")
    w.loc[val] = w.loc[val] * 0.90
    w.loc[val, "A5"] += 0.10          # A5 is the strongest asset in validation
    hold = w.index >= "2024-01-01"
    w.loc[hold] = w.loc[hold] * (1 - {tilt})
    w.loc[hold, "{asset}"] += {tilt}
    return w
'''

# A2 is the only asset with a negative holdout Sharpe: this wins validation and
# then falls apart on the split the old gate could not see.
HOLDOUT_DEGRADER_STRATEGY = _HOLDOUT_TILT.format(
    name="holdout_degrader", asset="A2", tilt=0.75,
    hypothesis="Wins validation, collapses on holdout.",
)

# A3 is the strongest asset in holdout: the same validation win, but the two
# splits now agree, so the gate has no grounds to refuse it.
HOLDOUT_AGREEING_STRATEGY = _HOLDOUT_TILT.format(
    name="holdout_agreeing", asset="A3", tilt=0.25,
    hypothesis="Wins validation without giving up holdout.",
)


def write_candidate(sandbox, code, name):
    p = sandbox / "strategies" / "candidates" / f"{name}.py"
    p.write_text(code)
    return p


def test_split_windows_do_not_overlap(prices):
    def gen(p):
        return pd.DataFrame(1.0 / p.shape[1], index=p.index[:1], columns=p.columns)
    train = protocol.evaluate_split(gen, prices, "train")
    val = protocol.evaluate_split(gen, prices, "validation")
    r_train, r_val = train["_returns"], val["_returns"]
    assert r_train.index.max() <= pd.Timestamp("2017-12-31")
    assert r_val.index.min() >= pd.Timestamp("2018-01-01")
    assert r_val.index.max() <= pd.Timestamp("2023-12-31")


def test_causality_check_passes_causal_and_catches_peeker(prices, sandbox):
    causal_path = write_candidate(sandbox, CAUSAL_STRATEGY, "causal")
    peek_path = write_candidate(sandbox, PEEKING_STRATEGY, "peeker")
    causal_mod, _ = protocol.load_strategy(causal_path)
    peek_mod, _ = protocol.load_strategy(peek_path)
    assert protocol.causality_check(causal_mod.generate_weights, prices) is None
    assert protocol.causality_check(peek_mod.generate_weights, prices) is not None


def test_causality_check_tolerates_truncation_shifted_rebalances(prices, sandbox):
    path = write_candidate(sandbox, SPARSE_REBALANCE_STRATEGY, "sparse")
    mod, _ = protocol.load_strategy(path)
    assert protocol.causality_check(mod.generate_weights, prices) is None


def test_bootstrap_promotes_first_passing_candidate(prices, sandbox):
    path = write_candidate(sandbox, CAUSAL_STRATEGY, "baseline")
    result = protocol.run_trial(path, prices)
    assert result.verdict == "PROMOTE"
    assert protocol.CHAMPION_FILE.exists()
    card = json.loads(protocol.CHAMPION_CARD.read_text())
    assert card["holdout"] is not None            # holdout evaluated exactly at promotion
    assert protocol.TRIALS_FILE.exists()


def test_peeker_gets_gate_failed_and_recorded(prices, sandbox):
    path = write_candidate(sandbox, PEEKING_STRATEGY, "peeker")
    result = protocol.run_trial(path, prices)
    assert result.verdict == "GATE_FAIL"
    assert "causality" in result.reasons[0]
    lines = protocol.TRIALS_FILE.read_text().strip().splitlines()
    assert len(lines) == 1


def test_identical_candidate_cannot_beat_champion(prices, sandbox):
    protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "baseline"), prices)
    result = protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "copycat"), prices)
    assert result.verdict == "REJECT"
    # Trial count grows regardless of verdict — the multiple-testing bar rises.
    assert len(protocol.TRIALS_FILE.read_text().strip().splitlines()) == 2


def test_holdout_veto_blocks_a_candidate_that_wins_validation(prices, sandbox):
    """The failure mode the gate exists for: validation says yes, holdout says no."""
    protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "baseline"), prices)
    champion_before = protocol.CHAMPION_FILE.read_text()

    result = protocol.run_trial(
        write_candidate(sandbox, HOLDOUT_DEGRADER_STRATEGY, "degrader"), prices
    )

    assert result.verdict == "HOLDOUT_VETO"
    # It really did win the old gate's only contest — that is the point.
    assert result.validation["sharpe"] > result.champion_val_sharpe
    assert result.dsr >= protocol.DSR_THRESHOLD
    # And it was refused on a resolvable holdout loss, not on a rounding error.
    assert result.holdout_t < -protocol.HOLDOUT_VETO_T
    assert result.holdout_delta < 0
    assert "holdout veto" in result.reasons[0]

    # The seat does not move, and the trial still counts against the DSR bar.
    assert protocol.CHAMPION_FILE.read_text() == champion_before
    assert len(protocol.TRIALS_FILE.read_text().strip().splitlines()) == 2
    record = json.loads(protocol.TRIALS_FILE.read_text().strip().splitlines()[-1])
    assert record["verdict"] == "HOLDOUT_VETO"
    assert record["holdout"] is not None          # every holdout read leaves a trail


def test_holdout_gate_promotes_when_the_splits_agree(prices, sandbox):
    """The veto is one-sided: it refuses losses, it does not demand holdout gains."""
    protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "baseline"), prices)

    result = protocol.run_trial(
        write_candidate(sandbox, HOLDOUT_AGREEING_STRATEGY, "agreeing"), prices
    )

    assert result.verdict == "PROMOTE"
    assert result.holdout_t > -protocol.HOLDOUT_VETO_T
    card = json.loads(protocol.CHAMPION_CARD.read_text())
    assert card["name"] == "holdout_agreeing"
    assert card["holdout_gate"]["t"] == result.holdout_t


def test_holdout_is_not_read_before_the_gate(prices, sandbox):
    """The gate runs last, so it reads no holdout the old protocol would not have.

    A candidate rejected on validation Sharpe never reaches it, and one that
    fails a hard gate never even gets scored.
    """
    protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "baseline"), prices)

    rejected = protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "copycat"), prices)
    assert rejected.verdict == "REJECT"
    assert rejected.holdout is None
    assert rejected.holdout_t is None

    gate_failed = protocol.run_trial(write_candidate(sandbox, PEEKING_STRATEGY, "peeker"), prices)
    assert gate_failed.verdict == "GATE_FAIL"
    assert gate_failed.holdout is None

    holdouts = [
        json.loads(line)["holdout"]
        for line in protocol.TRIALS_FILE.read_text().strip().splitlines()
    ]
    assert [h is not None for h in holdouts] == [True, False, False]


# --- protocol v2 --------------------------------------------------------------

def _v2_setup(prices, eligible):
    types = {c: "stock" for c in prices.columns}
    return protocol.Setup(version=2, splits=protocol.SPLITS_V2, gates=protocol.GATES_V2,
                          universe="legacy", eligible=eligible, types=types)


LATE_JOINER_PEEKER = '''
import pandas as pd
STRATEGY = {"name": "future_member", "family": "bug",
            "hypothesis": "Buy whatever column exists, including names that join later."}
def generate_weights(prices):
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    # a column's presence is the leak: A7 only joins the universe in 2020
    return pd.DataFrame(1.0 if "A7" in prices.columns else 0.0, index=rebal, columns=["A0"]) \\
        .reindex(columns=prices.columns, fill_value=0.0).clip(upper=0.25) \\
        .assign(A1=0.25, A2=0.25, A3=0.25)
'''

ELIGIBLE_AWARE = '''
import pandas as pd
STRATEGY = {"name": "eligible_equal_weight", "family": "baseline",
            "hypothesis": "Equal weight the eligible names, monthly."}
def generate_weights(prices, eligible=None):
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    e = eligible.loc[rebal].astype(float)
    return e.div(e.sum(axis=1), axis=0).fillna(0.0)
'''


def test_v2_hides_columns_until_they_are_eligible(prices):
    eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    eligible.loc[:"2019-12-31", "A7"] = False
    setup = _v2_setup(prices, eligible)
    seen = []

    def gen(p, eligible=None):
        seen.append(("A7" in p.columns, eligible is not None and eligible.shape == p.shape))
        return pd.DataFrame(1.0 / p.shape[1], index=p.index[:1], columns=p.columns)

    protocol.evaluate_split(gen, prices, "train", setup=setup)
    protocol.evaluate_split(gen, prices, "validation", setup=setup)
    assert seen == [(False, True), (True, True)]


def test_v2_causality_catches_universe_lookahead(prices):
    eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    eligible.loc[:"2020-12-31", "A7"] = False
    setup = _v2_setup(prices, eligible)
    ns: dict = {}
    exec(LATE_JOINER_PEEKER, ns)
    assert protocol.causality_check(ns["generate_weights"], prices, setup=setup) is not None
    ns = {}
    exec(ELIGIBLE_AWARE, ns)
    assert protocol.causality_check(ns["generate_weights"], prices, setup=setup) is None


def test_v2_static_check_refuses_reading_membership(sandbox):
    path = write_candidate(sandbox, "from engine.membership import load_intervals\n", "sneaky")
    assert protocol.static_check(path) is not None
    path = write_candidate(sandbox, CAUSAL_STRATEGY, "honest")
    assert protocol.static_check(path) is None


def test_v2_trial_records_null_and_benchmarks(prices, sandbox, monkeypatch):
    monkeypatch.setattr(protocol, "NULL_DRAWS", 40)
    eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    setup = _v2_setup(prices, eligible)
    path = write_candidate(sandbox, ELIGIBLE_AWARE, "eligible_equal_weight")
    r = protocol.run_trial(path, prices, setup=setup)
    rec = json.loads((sandbox / "experiments" / "trials.jsonl").read_text().splitlines()[-1])
    assert rec["protocol_version"] == 2
    assert set(rec["null"]) >= {"null_p50", "null_p90", "null_pctile"}
    # equal-weighting every eligible name IS the equal-weight benchmark: no
    # selection, so it cannot clear the random-selection null's 90% quantile
    assert r.verdict == "GATE_FAIL"
    assert any("random-selection null" in x for x in r.reasons)
    assert rec["ir_vs_ew"] == pytest.approx(0.0, abs=0.3)


# ---------------------------------------------------------------------------
# The v2 cut-over: hindsight guard, per-version history, re-seating
# ---------------------------------------------------------------------------

HINDSIGHT_LIST = '''
import pandas as pd
STRATEGY = {"name": "hindsight", "family": "bug", "hypothesis": "Hold today's winners."}
WINNERS = ["NVDA", "AAPL", "MSFT"]
def generate_weights(prices):
    return pd.DataFrame(1 / 3, index=prices.index[:1], columns=WINNERS)
'''

CLEAN_WITH_ETF_AND_FREQ = '''
"""Mentions AAPL and data/universe.yaml in a docstring, which is not code."""
import pandas as pd
STRATEGY = {"name": "clean", "family": "baseline",
            "hypothesis": "SPY-relative, monthly; the membership band is prose, not a read."}
def generate_weights(prices):
    rebal = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    monthly = prices.resample("M").last()          # "M" and "MS" are also tickers
    starts = prices.resample("MS").first()
    proxy = prices.get("SPY")
    return pd.DataFrame(1.0 / prices.shape[1], index=rebal, columns=prices.columns)
'''


def test_v2_static_check_refuses_hard_coded_stocks(sandbox):
    msg = protocol.static_check(write_candidate(sandbox, HINDSIGHT_LIST, "hindsight"))
    assert msg is not None and "hindsight" in msg and "NVDA" in msg
    assert protocol.static_check(write_candidate(sandbox, CLEAN_WITH_ETF_AND_FREQ, "clean")) is None


def test_v2_static_check_follows_strategy_imports(sandbox):
    lib = sandbox / "strategies" / "lib"
    lib.mkdir(parents=True)
    (sandbox / "strategies" / "__init__.py").write_text("")
    (lib / "__init__.py").write_text("")
    (lib / "sectors.py").write_text('TECH = ["AAPL", "MSFT"]\n')
    (lib / "wrapper.py").write_text("from strategies.lib import sectors\n")
    path = write_candidate(sandbox, "from strategies.lib import wrapper\n" + CAUSAL_STRATEGY, "indirect")
    msg = protocol.static_check(path)
    assert msg is not None and "strategies/lib/sectors.py" in msg


def test_v2_static_check_refuses_the_legacy_universe(sandbox):
    for i, src in enumerate([
        'from pathlib import Path\nU = Path("data") / "universe.yaml"\n',
        'from engine import data\nNAMES = data.instruments(universe="legacy")\n',
    ]):
        msg = protocol.static_check(write_candidate(sandbox, src + CAUSAL_STRATEGY, f"legacy{i}"))
        assert msg is not None and "legacy universe" in msg


def _record(sandbox, **rec):
    path = sandbox / "experiments" / "trials.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(rec) + "\n")


def test_history_is_kept_per_protocol_version(sandbox):
    _record(sandbox, name="old", family="baseline", ts="2026-01-01T00:00:00+00:00",
            validation={"sharpe": 1.5, "sharpe_daily": 0.09})
    _record(sandbox, name="new", family="baseline", ts="2026-02-01T00:00:00+00:00",
            protocol_version=2, validation={"sharpe": 0.4, "sharpe_daily": 0.03})
    assert [s for s, _ in protocol.past_trials(1)] == [0.09]
    assert [s for s, _ in protocol.past_trials(2)] == [0.03]
    assert protocol.family_best_sharpe("baseline", protocol.recorded_trials(2)) == 0.4
    assert len(protocol.recorded_trials(all_versions=True)) == 2
    board = protocol.write_leaderboard(2)
    assert board["protocol_version"] == 2
    assert board["families"]["baseline"]["name"] == "new"


def test_v1_champion_does_not_hold_the_v2_seat(prices, sandbox, monkeypatch):
    protocol.run_trial(write_candidate(sandbox, CAUSAL_STRATEGY, "baseline"), prices)
    assert protocol.champion_seated(1) and not protocol.champion_seated(2)

    monkeypatch.setattr(protocol, "NULL_DRAWS", 40)
    eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    setup = _v2_setup(prices, eligible)
    result = protocol.run_trial(
        write_candidate(sandbox, HOLDOUT_AGREEING_STRATEGY, "v2_first"), prices, setup=setup)
    # no v2 champion: the candidate is judged by the bootstrap rule, never
    # compared with (or holdout-gated against) the v1 incumbent
    assert result.champion_val_sharpe is None and result.holdout_t is None
    if result.verdict == "PROMOTE":
        assert protocol.champion_seated(2)
        assert any(p.name.endswith("_equal_weight_monthly.py")
                   for p in (sandbox / "strategies" / "archive").iterdir())
    else:
        assert protocol.champion_seated(1)
