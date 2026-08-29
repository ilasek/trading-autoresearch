"""Do groups lead their members, or is the group signal just sector momentum?

WHAT THIS SETTLES. Trial #58 (`ll_group_lastmonth_lead`) held *every* member of
the three sector groups with the strongest median trailing 21-day return and
scored validation 0.688 at rho 0.698, the family's first recorded result. Its
own lesson recorded the ambiguity it could not resolve: a book that holds all of
the three strongest sectors is equally well described as a one-month sector
momentum book, and "the group leads its members" and "sector-level trend at a
one-month horizon simply is not the reversal the name level shows" predict the
same holdings.

They stop predicting the same holdings the moment you look *inside* the chosen
groups, which is what this file does and the only thing it changes. Group
selection is bit-identical to #58 — median member return over the trailing 21
days, top-3 enter, top-5 hold, one third of capital per group. Within each
chosen group it holds only the members whose **own** 21-day return sits in the
bottom half of that group: the laggards.

THE TWO HYPOTHESES NOW DISAGREE, SHARPLY AND IN OPPOSITE DIRECTIONS.
- **Diffusion**: the group aggregate moves first and individual members finish
  adjusting later, so the members that have *not yet* adjusted are the ones with
  the catching-up left to do. Laggards inside leading groups should do at least
  as well as the whole group, and plausibly better.
- **Sector momentum**: there is nothing group-specific about the effect; the
  strong groups are simply where the strong names are, and within a group the
  winners keep winning. Dropping the top half of each leading group should then
  cost most of #58's result.

Because group selection is identical, this is a paired comparison against a
recorded number rather than a fresh sort, and either outcome is informative:
**above 0.688 supports diffusion, materially below it refutes diffusion and
re-labels #58 as a sector-momentum book.** A result close to 0.688 says the
within-group ordering carries nothing either way, which would itself close the
diffusion reading, because diffusion is a claim about *which members* have not
adjusted and a null on that ordering is a null on the claim.

WHAT ELSE THIS RULES OUT, FOR FREE. #58's own-return contamination argument runs
the other way here. In #58 a name could be held partly because its own strong
month lifted its group's median; here the selection is explicitly *against* own
strength, so any edge cannot be own-name momentum leaking through the group
score. It can, however, be one-month own-name reversal — which is a real
alternative reading and is why the result has to be read against #58 rather than
against the 0.49 floor. Measured on the train split tonight, raw one-month
reversal is close to a null on this universe (Q5-Q1 -0.49%/yr, t = -0.13), so
that channel is small, but it is not zero.

CAVEATS RECORDED IN ADVANCE. (a) Holding half of each group roughly halves the
position count against #58's 44, so expect a more concentrated book and a worse
drawdown. (b) Turnover should rise: #58 re-selected only when a group entered or
left the band, whereas here within-group membership can turn over every month
even when the groups do not. #58 already ran 13.8x costing ~2.1%/yr, so if this
lands materially above that, the cost swamps the mechanism test and the verdict
is about execution again — the third time in two sessions, and worth saying so
plainly rather than reading a cost result as a signal result.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "ll_group_laggard_diffusion",
    "family": "lead-lag-spillover",
    "track": "scout",
    "hypothesis": (
        "Holding only the bottom-half performers *within* the same three leading "
        "sector groups that trial #58 selected — group choice bit-identical, one third "
        "of capital per group — scores at or above #58's recorded validation 0.688, "
        "because the members that have not yet adjusted to their group's move are the "
        "ones with the catching-up left to do; a materially lower score instead refutes "
        "the diffusion reading and re-labels #58 as one-month sector momentum."
    ),
}

LOOKBACK = 21
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
        held = (held & set(ranked[:HOLD_TOP])) | set(ranked[:ENTER_TOP])

        chosen = [g for g in held if g in live]
        if not chosen:
            continue
        per_group = 1.0 / len(chosen)
        w: dict[str, float] = {}
        for group in chosen:
            members = ret[live[group]].sort_values()
            # The laggard half: members whose OWN month is weakest inside a group
            # whose median month is among the strongest. This is the only line
            # that differs from trial #58.
            laggards = list(members.index[: max(2, len(members) // 2)])
            for name in laggards:
                w[name] = w.get(name, 0.0) + per_group / len(laggards)
        rows[dt] = pd.Series(w)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
