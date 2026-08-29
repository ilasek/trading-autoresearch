"""The scout track, the auxiliary OHLCV panels, and the family leaderboard.

The load-bearing test here is `test_peeking_through_aux_is_caught`: the aux
panels are a second channel into a strategy, and if the protocol ever handed
one over untruncated, the causality check would be watching the wrong frame and
every learned candidate's backtest would be worthless.
"""

import json

import numpy as np
import pandas as pd
import pytest

from engine import protocol
from tests.test_protocol import prices, sandbox  # noqa: F401  (fixtures)


@pytest.fixture
def panels(prices):  # noqa: F811
    """Aux panels shaped like `data.load_panels()` output."""
    rng = np.random.default_rng(7)
    shape = prices.shape
    return {
        "high": prices * (1 + rng.uniform(0.0, 0.02, shape)),
        "low": prices * (1 - rng.uniform(0.0, 0.02, shape)),
        "open": prices.shift(1).fillna(prices.iloc[0]),
        "volume": pd.DataFrame(
            rng.lognormal(12, 0.6, shape), index=prices.index, columns=prices.columns
        ),
    }


def write(sandbox, name, source):  # noqa: F811
    path = sandbox / "strategies" / "candidates" / f"{name}.py"
    path.write_text(source)
    return path


ONE_ARG = '''
import pandas as pd
STRATEGY = {"name": "one_arg", "family": "baseline", "hypothesis": "Equal weight."}
def generate_weights(prices):
    dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    return pd.DataFrame(1.0 / prices.shape[1], index=dates, columns=prices.columns)
'''

TWO_ARG = '''
import pandas as pd
STRATEGY = {"name": "two_arg", "family": "liquidity-volume", "track": "scout",
            "hypothesis": "Tilt toward names with heavy trailing volume."}
def generate_weights(prices, aux):
    assert set(aux) >= {"high", "low", "volume"}, "aux panels missing"
    assert aux["volume"].index.equals(prices.index), "aux outran the visible prices"
    dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    score = aux["volume"].rolling(63, min_periods=20).mean()
    rows = {}
    for dt in dates:
        s = score.loc[:dt].iloc[-1].dropna()
        if len(s) < 4:
            continue
        top = s.nlargest(4)
        rows[dt] = pd.Series(1.0 / len(top), index=top.index)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
'''

# Reads the LAST row of the volume panel it was handed, at every rebalance date.
# Causal on the full frame only if the panel stops where the prices do; if the
# protocol leaked an untruncated panel this would silently see the future.
PEEKING_AUX = '''
import pandas as pd
STRATEGY = {"name": "peek_aux", "family": "liquidity-volume", "track": "scout",
            "hypothesis": "Deliberately peeks through the aux panel."}
def generate_weights(prices, aux):
    vol = aux["volume"]
    dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    final = vol.iloc[-1]                      # the end of whatever it was given
    rows = {}
    for dt in dates:
        top = final.nlargest(4)
        rows[dt] = pd.Series(1.0 / len(top), index=top.index)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
'''

SCOUT_EW = '''
import pandas as pd
STRATEGY = {"name": "scout_ew", "family": "seasonality-calendar", "track": "scout",
            "hypothesis": "Equal weight, scouted."}
def generate_weights(prices):
    dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    return pd.DataFrame(1.0 / prices.shape[1], index=dates, columns=prices.columns)
'''


def test_one_arg_strategy_still_runs_unchanged(sandbox, prices, panels):  # noqa: F811
    """The original single-argument contract is untouched by the aux channel."""
    path = write(sandbox, "one_arg", ONE_ARG)
    with_aux = protocol.run_trial(path, prices, panels)
    without = protocol.run_trial(path, prices)
    assert with_aux.validation["sharpe"] == without.validation["sharpe"]


def test_two_arg_strategy_receives_aligned_panels(sandbox, prices, panels):  # noqa: F811
    path = write(sandbox, "two_arg", TWO_ARG)
    result = protocol.run_trial(path, prices, panels)
    assert result.verdict in ("FAMILY_LEAD", "SCOUT", "GATE_FAIL")
    assert "causality" not in " ".join(result.reasons)


def test_peeking_through_aux_is_caught(sandbox, prices, panels):  # noqa: F811
    path = write(sandbox, "peek_aux", PEEKING_AUX)
    result = protocol.run_trial(path, prices, panels)
    assert result.verdict == "GATE_FAIL"
    assert result.reasons[0].startswith("causality:")


def test_slice_panels_matches_the_visible_window(prices, panels):  # noqa: F811
    from engine import data

    visible = prices.loc[:"2020-12-31"]
    sliced = data.slice_panels(panels, visible.index)
    assert set(sliced) == set(panels)
    for frame in sliced.values():
        assert frame.index.equals(visible.index)


def test_scout_never_reads_holdout_or_touches_the_champion(sandbox, prices, panels):  # noqa: F811
    """A scout trial is recorded, deflated and gated like any other — but the
    champion seat and the holdout split are unreachable from it."""
    champion = sandbox / "strategies" / "champion.py"
    champion.write_text(ONE_ARG)
    (sandbox / "strategies" / "champion_card.json").write_text(
        json.dumps({"name": "one_arg"})
    )
    before = champion.read_text()

    result = protocol.run_trial(write(sandbox, "scout_ew", SCOUT_EW), prices, panels)

    assert result.track == "scout"
    assert result.verdict in ("FAMILY_LEAD", "SCOUT")
    assert result.holdout is None
    assert result.holdout_t is None
    assert result.champion_val_sharpe is None
    assert champion.read_text() == before
    assert result.dsr is not None and result.n_trials >= 1


def test_family_lead_only_on_a_within_family_best(sandbox, prices, panels):  # noqa: F811
    first = protocol.run_trial(write(sandbox, "scout_ew", SCOUT_EW), prices, panels)
    assert first.verdict == "FAMILY_LEAD"
    assert first.family_best_sharpe is None

    again = protocol.run_trial(write(sandbox, "scout_ew2", SCOUT_EW), prices, panels)
    assert again.verdict == "SCOUT"
    assert again.family_best_sharpe == first.validation["sharpe"]


def test_leaderboard_records_one_row_per_family(sandbox, prices, panels):  # noqa: F811
    protocol.run_trial(write(sandbox, "scout_ew", SCOUT_EW), prices, panels)
    protocol.run_trial(write(sandbox, "two_arg", TWO_ARG), prices, panels)

    board = json.loads(protocol.LEADERBOARD_FILE.read_text())
    assert "seasonality-calendar" in board["families"]
    row = board["families"]["seasonality-calendar"]
    assert row["track"] == "scout"
    assert row["validation"]["sharpe"] is not None


def test_unknown_track_is_rejected(sandbox, prices):  # noqa: F811
    path = write(sandbox, "bad_track", ONE_ARG.replace(
        '"family": "baseline"', '"family": "baseline", "track": "freestyle"'))
    with pytest.raises(ValueError, match="track"):
        protocol.load_strategy(path)
