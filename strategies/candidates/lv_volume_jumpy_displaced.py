"""THE DISPLACED JUMPY HALF — THE LAST CELL OF THE QUIETNESS (SIDE x WINDOW) DESIGN.

WHAT THE RECORD NOW HOLDS. The share-volume quietness sort has been priced in three of its
four cells, each one node apart, every other node byte-identical:

    cell                                   side     window      val GROSS skill  null %ile
    #50 lv_volume_quiet_alone              quiet    in-window        +0.118          98%
    #51 lv_volume_quiet_displaced          quiet    shift(50)        -0.017          62%
    #52 lv_volume_jumpy_half               jumpy    in-window        -0.135           8%
    THIS FILE                              jumpy    shift(50)           ?              ?

`#52` (run earlier tonight) landed inside the SYMMETRIC-STATE branch it pre-registered:
the complement of `#50`'s book is very nearly its exact mirror (+0.118 against -0.135, mean
-0.009), which refutes the tail-only reading and refutes the window-level reading — a
2018-2023 level effect would have lifted BOTH sides of the sort, and this side is the most
negative object on the board at the 8th percentile of its own matched null.

WHAT IS LEFT UNMEASURED, AND IT IS THE ONLY CELL THAT CAN CLOSE THE DESIGN. Antisymmetry
has been established at the IN-WINDOW position only. If the quietness ordering is a
short-lived STATE, then displacing the window by 50 days should collapse BOTH sides toward
zero, and the jumpy in-window term should come out near -0.15 — an independent second
reading of the +0.135 the quiet side measured. If instead the ordering is a NAME
CHARACTERISTIC, the displaced jumpy arm stays near `#52`'s -0.135, because a 50-day-stale
reading of a quantity whose LEVEL persists at phi +0.709 still selects the same kind of
name. `#51` answered that question on the quiet side alone; one side is a reading and two
sides are a design.

ONE NODE CHANGES FROM #52: `.shift(50)` before the rolling maximum — the identical
displacement `#41` and `#51` used. Nothing else: K = 100, BAND = 200, WINDOW = 50, the
monthly grid, the (calendar peer x instrument type) quota, the equal weighting and the
warm-up branch are byte-identical to `#52`, which is itself byte-identical to `#50` but
for the sign.

FREE PRE-TRIAL SCREEN (train 1997-2017, 252 month-ends; rank and composition statistics
only. **No train Sharpe, train skill or train IC was computed for this object.**) The
displacement is a matched control, so the screens that matter are the ones that must NOT
move, and on the quiet side they moved by at most 0.012:

    quantity                                this arm   #52 in-window   #51 (quiet, displaced)
    rank rho to its own in-window self        +0.269      1.000            +0.269
    month-to-month rank phi                   +0.6249     +0.6252          +0.6249
    rank rho to the 5/45 volume shock         ~+0.04      +0.0435          (mirror of #51)
    rank rho to 126-day volatility            ~+0.04      +0.0420
    coverage of eligible names                 99.7%       99.9%            99.7%
    exit200                                   ~17%        16.9%            21.8%

PRE-REGISTERED PREDICTIONS, written before the run (and the two branches were fixed in
tonight's pre-registration before `#52` was run, as its conditional arm):
 - **(A) SHORT-LIVED STATE**: validation GROSS skill **within 0.05 of zero**, i.e.
   **-0.05 to +0.05**, null percentile **40-75%**. This makes the jumpy in-window term
   -0.15 +- 0.05 against the quiet side's +0.135.
 - **(B) NAME CHARACTERISTIC**: **within 0.05 of #52's -0.135**, i.e. -0.185 to -0.085,
   null percentile **below 40%**.
 - CHURN: the displacement does not change the schedule, so train **4.6x-5.6x** and
   validation **8.4x-9.4x** (`#52` was charged 5.1x / 8.9x; `#51` moved `#50` by 0.07x
   and 0.05x).
 - BILL per 1x within 1 bps of `#52`'s 11.0 bps, since the displacement changes which
   names are held but not the kind of name (`#51` moved `#50`'s by 0.3 bps).
 - TRAIN SKILL is not predicted and was not screened. **The statistic under test is the
   validation GROSS skill and the null percentile. The verdict is not the result.**

WHAT ARGUES AGAINST THE BOOK. It is a control arm, and a control arm's value is entirely
in the difference it licenses: on its own this object is expected to be a null or a loser,
and it is written to make the jumpy side's in-window term measurable rather than to find
an edge. It inherits `#52`'s split-adjustment reservation in the opposite direction — a
50-day-stale window still selects names with a corporate action, just an older one.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
WINDOW = 50
SHIFT = 50          # the identical displacement #41 and #51 used

STRATEGY = {
    "name": "lv_volume_jumpy_displaced",
    "family": "liquidity-volume",
    "hypothesis": (
        "Displacing the jumpy half's scoring window 50 days into the past -- one node "
        "changed from lv_volume_jumpy_half, which is itself lv_volume_quiet_alone with the "
        "sign reversed -- moves validation GROSS skill to within 0.05 of zero if recent "
        "share-volume jumpiness is a SHORT-LIVED STATE, putting the jumpy side's in-window "
        "term at -0.15 +- 0.05 as an independent second reading of the +0.135 the quiet "
        "side measured; and leaves it within 0.05 of the in-window arm's -0.135 if the "
        "ordering instead selects on a persistent NAME CHARACTERISTIC, since the scored "
        "quantity's level persists at phi +0.709 and a stale reading of it would pick the "
        "same kind of name. This is the fourth and last cell of the (side x window) design "
        "whose other three cells are recorded, and the only one that can establish "
        "antisymmetry at both window positions rather than at one."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The 100 jumpiest eligible names by the maximum |d log volume| in a 50-day window
    that ENDED 50 days ago, quota'd across (calendar peer group x instrument type),
    monthly with a top-200 retention band. `lv_volume_jumpy_half` with the window
    displaced and nothing else changed.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    lv = np.log(volume.where(volume > 0))
    # #52's statistic read one window earlier: the displacement is applied to the daily
    # jump series before the rolling maximum, exactly as #41 and #51 do it.
    jumpy = lv.diff().abs().shift(SHIFT).rolling(WINDOW, min_periods=25).max()

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken (the
        # 2026-10-07 column-axis leak).
        score = jumpy.loc[date].reindex(names).dropna()
        if len(score) < 60:
            # Warm-up: hold the pool rather than cash (2026-10-15/16).
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()
        cells = (groups.reindex(score.index).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in score.index],
                             index=score.index))

        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, cells.reindex(rest.index).dropna(), K - len(keep))
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
