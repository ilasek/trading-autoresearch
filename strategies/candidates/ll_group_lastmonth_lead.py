"""Does last month continue at the group level while it reverses at the name level?

WHY THIS FAMILY. `lead-lag-spillover` has never been scouted here and is the
family `program.md` calls best suited to this universe: 140 instruments across
15 regions with 42 ETFs, so groups are numerous, populated and economically
meaningful. It is also the only untried family whose mechanism has no overlap
with anything the lab has already measured.

THE MECHANISM, AND WHY IT IS NOT MOMENTUM. Gradual information diffusion says a
shock that lands on a group is absorbed by the whole group with a lag: the group
aggregate moves first and the individual members finish adjusting later. The
sharpest testable consequence of that on this repo's data is a *sign
disagreement about the most recent month*. At the individual-name level the last
month is the month every momentum construction in this lab deliberately skips,
because at that horizon a name's own move reverses — the champion's four legs are
all `N-1` and `learnings.md` records the skip-month as load-bearing. The
diffusion claim is that the same month, measured on the *group*, continues
instead. Same window, same data, opposite prediction, and the two are
distinguishable in one trial.

WHAT IT DOES. At each month-end, take every instrument's trailing 21-day return
and reduce it to a group score: the **median** member return of each of the 12
sector-ish groups with at least four members (`strategies/lib/groups.py`). Rank
the groups, hold every member of the top 3, one third of capital per group and
equal weight within it, with a hold-top-5 / enter-top-3 hysteresis band on group
membership. Capital is allocated per group rather than per name so that a 21-name
group and a 5-name group are the same size bet; the alternative makes this a
test of "is tech big" rather than of a lead-lag.

WHY MEDIAN RATHER THAN MEAN. A group's score should describe the group, not its
largest mover. The median also bounds the contamination this design cannot
remove entirely: an instrument's own return is one of the observations forming
its own group's score. With a median over 5-21 members that contribution is
close to nil, and where it survives it points the *wrong* way for the
hypothesis — a name held because its own last month was strong is being held on
exactly the own-name signal the skip-month says reverses. Any measured edge is
therefore group-level in origin or it is not there at all.

WHAT WOULD FALSIFY IT. A validation Sharpe at or below the 0.49 equal-weight
global sleeve floor. Two more specific outcomes are worth reading off the same
run. If the book earns *negative* group-level continuation — i.e. it loses — the
lab has learned that the last month reverses at the group level too, which
closes the diffusion story on this universe rather than merely failing to
support it. And if it wins, its correlation to the champion is the number that
matters, because a signal built entirely from the window the champion discards
should be genuinely decorrelated; `learnings.md`'s standing blend table says a
leg at rho ~0.6 needs validation Sharpe ~0.9 before a blend is worth a trial.

CAVEATS RECORDED IN ADVANCE. (a) Holding whole groups means 3 of 12 buckets, so
the book is deliberately concentrated in sector space even though it holds ~30
names; expect a higher drawdown than a diversified sleeve. (b) The group map is
current metadata on a survivorship-selected universe — the same standing caveat
as every result here, neither better nor worse. (c) Two groups are ETF baskets
(`broad_market_etf`, `bonds`), so in a month when everything else falls the book
can rotate into bonds; that is a real property of a rank-based rotation and not
a regime overlay, but it will show up as a low-beta stretch if it happens.
(d) Rotating up to 3 of 12 groups a month is not cheap; the band exists to hold
turnover down and the realised figure is part of the result.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "ll_group_lastmonth_lead",
    "family": "lead-lag-spillover",
    "track": "scout",
    "hypothesis": (
        "The most recent month, which reverses at the individual-name level and is "
        "therefore skipped by every momentum construction in this repo, *continues* at "
        "the group level: holding all members of the three sector groups with the "
        "highest median trailing 21-day return, one third of capital per group and "
        "rebalanced monthly with a top-3-enter / top-5-hold band, earns a validation "
        "Sharpe above the 0.49 equal-weight floor net of 15 bps costs."
    ),
}

LOOKBACK = 21          # the month the name-level signal throws away
ENTER_TOP = 3
HOLD_TOP = 5
MIN_GROUP = 4
WARMUP = 2


_MEMBERS = G.group_members(G.SECTOR_OF, min_size=MIN_GROUP)


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK + 2:
            continue
        ret = hist.iloc[-1] / hist.iloc[-1 - LOOKBACK] - 1.0

        scores: dict[str, float] = {}
        live: dict[str, list[str]] = {}
        for group, members in _MEMBERS.items():
            present = [m for m in members if m in ret.index and pd.notna(ret[m])]
            if len(present) < MIN_GROUP:
                continue
            scores[group] = float(ret[present].median())
            live[group] = present
        if len(scores) < HOLD_TOP:
            continue

        ranked = sorted(scores, key=scores.get, reverse=True)
        enter = set(ranked[:ENTER_TOP])
        band = set(ranked[:HOLD_TOP])
        # Hysteresis on *group* membership: a group leaves only when it drops
        # out of the wider band, so a group hovering around rank 3 does not
        # rotate the whole sleeve every month.
        held = (held & band) | enter

        chosen = [g for g in held if g in live]
        if not chosen:
            continue
        per_group = 1.0 / len(chosen)
        w: dict[str, float] = {}
        for group in chosen:
            names = live[group]
            for name in names:
                w[name] = w.get(name, 0.0) + per_group / len(names)
        rows[dt] = pd.Series(w)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
