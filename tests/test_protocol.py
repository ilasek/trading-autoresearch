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
    """Redirect all protocol state files into a temp dir."""
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
