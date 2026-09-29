"""Point-in-time membership: spells from change logs, snapshots, the mask, and
the change logs themselves (replayed index sizes)."""

import json
import re

import pandas as pd
import pytest

from engine.membership import (
    Event, apply_snapshot, eligibility, intervals_from_events, liquidity_mask,
    load_intervals, membership_mask, yahoo_to_id,
)

T = pd.Timestamp
COMPLETE = T("2009-01-01")
SNAP = T("2026-09-24")


def spells(df, sym):
    return [(r.start, None if pd.isna(r.end) else r.end) for r in df[df.id == sym].itertuples()]


def test_join_leave_and_complete_from():
    events = [
        Event(T("2019-03-18"), "in", "NEW"),        # joined 2019
        Event(T("2015-06-22"), "out", "OLD"),       # left 2015, no recorded entry
        Event(T("2012-09-24"), "out", "BACK"),      # left, came back
        Event(T("2021-09-20"), "in", "BACK"),
        Event(T("2005-01-01"), "in", "ANCIENT"),    # before the log is trusted: ignored
    ]
    df, warnings = intervals_from_events("x", events, {"NEW", "BACK", "STAY"}, COMPLETE, SNAP)
    assert spells(df, "NEW") == [(T("2019-03-18"), None)]
    assert spells(df, "OLD") == [(COMPLETE, T("2015-06-22"))]
    assert spells(df, "BACK") == [(COMPLETE, T("2012-09-24")), (T("2021-09-20"), None)]
    # a current member with no event has been in since the log became complete
    assert spells(df, "STAY") == [(COMPLETE, None)]
    assert spells(df, "ANCIENT") == []
    assert warnings == []


def test_log_disagreeing_with_snapshot_is_reported():
    events = [Event(T("2022-12-19"), "in", "GONE")]           # exit never recorded
    df, warnings = intervals_from_events("x", events, set(), COMPLETE, SNAP)
    assert spells(df, "GONE") == [(T("2022-12-19"), SNAP)]
    assert len(warnings) == 1 and "GONE" in warnings[0]


def test_snapshot_opens_and_closes_without_deleting():
    df, _ = intervals_from_events("x", [], {"A", "B"}, COMPLETE, SNAP)
    df2, added, removed = apply_snapshot(df, "x", {"B", "C"}, T("2026-10-05"))
    assert added == ["C"] and removed == ["A"]
    assert spells(df2, "A") == [(COMPLETE, T("2026-10-05"))]
    assert spells(df2, "C") == [(T("2026-10-05"), None)]
    assert spells(df2, "B") == [(COMPLETE, None)]


def test_mask_is_point_in_time():
    events = [Event(T("2019-03-18"), "in", "NEW"), Event(T("2015-06-22"), "out", "OLD")]
    df, _ = intervals_from_events("x", events, {"NEW"}, COMPLETE, SNAP)
    dates = pd.bdate_range("2014-01-01", "2020-12-31")
    m = membership_mask(df, dates, ["NEW", "OLD", "NONE"])
    assert not m.loc["2018-12-31", "NEW"] and m.loc["2019-03-18", "NEW"]
    assert m.loc["2015-06-19", "OLD"] and not m.loc["2015-06-22", "OLD"]   # end is exclusive
    assert not m["NONE"].any()


def test_yahoo_to_id_matches_legacy_ids():
    assert yahoo_to_id("SAP.DE") == "SAP_DE"
    assert yahoo_to_id("AZN.L") == "AZN_UK"
    assert yahoo_to_id("7203.T") == "7203_JP"
    assert yahoo_to_id("0700.HK") == "0700_HK"
    assert yahoo_to_id("BRK-B") == "BRK-B"


def test_eligibility_combines_membership_liquidity_and_type():
    dates = pd.bdate_range("2019-01-01", "2019-12-31")
    prices = pd.DataFrame(10.0, index=dates, columns=["S", "THIN", "E", "X"])
    prices.loc[:"2019-02-28", "E"] = float("nan")          # ETF launches in March
    volume = pd.DataFrame(1e6, index=dates, columns=prices.columns)   # $10M/day
    volume["THIN"] = 1e3                                                # $10k/day
    iv = pd.DataFrame({"index": "x", "id": ["S", "THIN"], "start": [T("2019-06-03")] * 2,
                       "end": [pd.NaT] * 2})
    types = {"S": "stock", "THIN": "stock", "E": "etf"}   # X: unknown type
    el = eligibility(prices, volume, types, iv)
    assert not el.loc["2019-05-31", "S"] and el.loc["2019-06-03", "S"]
    assert not el["THIN"].any()                        # member but illiquid
    assert not el.loc["2019-02-28", "E"] and el.loc["2019-03-01", "E"]
    assert not el["X"].any()


def test_liquidity_mask_is_causal():
    dates = pd.bdate_range("2019-01-01", "2019-12-31")
    prices = pd.DataFrame(10.0, index=dates, columns=["A"])
    volume = pd.DataFrame(1e3, index=dates, columns=["A"])
    volume.loc["2019-09-02":, "A"] = 1e7          # becomes liquid in September
    full = liquidity_mask(prices, volume)
    cut = liquidity_mask(prices.loc[:"2019-08-30"], volume.loc[:"2019-08-30"])
    pd.testing.assert_frame_equal(full.loc[:"2019-08-30"], cut)
    assert not full.loc["2019-08-30", "A"]


# ---------------------------------------------------------------------------
# The change logs, replayed from today's members: each index must keep its
# official size on every business day back to 2009 — a missed or misdated
# change shows up as days with one name too many or too few. Exceptions are
# real (spin-offs kept until the next review, takeovers without replacement)
# or the known imprecision of edit-dated changes (Nikkei 225).
# ---------------------------------------------------------------------------

EXPECTED_SIZE = {
    "ftse100": (100, []),
    "sx5e": (50, []),
    "smi": (20, [
        ("2019-04-09", "2019-04-10", 21),   # Alcon in a day before Julius Baer out
        ("2025-06-23", "2025-09-22", 21),   # Amrize spin-off kept until the review
    ]),
    "aex": (25, [
        ("2011-01-31", "2011-03-21", 26),   # Aperam spin-off
        ("2011-05-26", "2011-06-20", 26),   # TNT Express spin-off
        ("2019-03-29", "2019-06-11", 24),   # Gemalto taken over, no replacement
        ("2025-09-22", "2026-04-30", 30),   # expansion to 30
        ("2026-04-30", "2026-06-22", 29),   # JDE Peet's delisted
        ("2026-06-22", "2026-09-25", 30),
    ]),
    "n225": (225, [
        # merger / replacement edits dated a day or a few weeks apart
        ("2010-10-01", "2010-10-04", 226),
        ("2012-10-01", "2012-10-03", 226),
        ("2020-10-01", "2020-10-28", 226),
    ]),
}


def _replay(idx):
    from scripts.build_membership import LOG_COMPLETE_FROM, SOURCES, read_events

    iv = load_intervals()
    events, _ = read_events(SOURCES / f"{idx}_changes.csv")
    events = [Event(e.date, e.action, yahoo_to_id(e.symbol)) for e in events]
    current = set(iv.loc[(iv["index"] == idx) & iv["end"].isna(), "id"])
    df, warnings = intervals_from_events(idx, events, current, LOG_COMPLETE_FROM, SNAP)
    days = pd.bdate_range(LOG_COMPLETE_FROM, SNAP)
    count = membership_mask(df, days, sorted(set(df.id))).sum(axis=1)
    return days, count, warnings


needs_intervals = pytest.mark.skipif(load_intervals().empty, reason="no membership intervals built")


@needs_intervals
@pytest.mark.parametrize("idx", sorted(EXPECTED_SIZE))
def test_change_logs_keep_index_size(idx):
    size, exceptions = EXPECTED_SIZE[idx]
    days, count, warnings = _replay(idx)
    assert warnings == [], (idx, warnings)
    expected = pd.Series(size, index=days)
    for start, end, n in exceptions:
        expected[(days >= T(start)) & (days < T(end))] = n
    wrong = count[count != expected]
    assert wrong.empty, (idx, wrong.head().to_dict())


@needs_intervals
def test_hang_seng_log_matches_published_sizes():
    """The Hang Seng grew from 42 names to 93; its change table records the
    size after every change, which the replay must reproduce exactly."""
    from scripts.build_membership import SOURCES

    header = (SOURCES / "hsi_changes.csv").read_text().split("\ndate,")[0]
    sizes = json.loads(re.search(r"(\[\[.*\]\])", header.replace("\n# ", "")).group(1))
    days, count, warnings = _replay("hsi")
    assert warnings == []
    for date, n in sizes:
        on = days[days >= T(date)][0]
        assert count[on] == n, (date, n, int(count[on]))
