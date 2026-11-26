"""THE LAST OBJECT ON THE BOARD CARRYING THE ETF CONFOUND -- discharged on the fifth night it
has been carried on a handover, with the one trial that can discharge it.

THE STANDING RIDER. The 2026-11-22 session found that the panel's 42 ETFs against ~1,400
stocks (5.5% of a median train month-end) are matched by `random_null_v3` on TYPE but, inside
the ETF type, matched on nothing -- so a book overweight in ETFs has a fifth of its replicas
drawn as random (mostly equity) ETFs while it bought the quietest funds on the panel. The one
paired instance it ran:

    book                           quota cells   cand    null med  geography  selection  pctile  ETF share
    pt_lowvol126_quota_band (#30)  peer          +0.196   +0.346     +0.006     -0.150      0%     20.8%
    pt_lowvol126_typequota (#31)   peer x type   +0.237   +0.331     -0.009     -0.094      6%     ~5.0%

Matching the asset class moved the selection term **+0.056** and took geography to -0.009, the
cleanest benchmark alignment recorded under v3 -- and it is inside the error bars, so one paired
instance puts the channel at about a third of that book's deficit rather than measuring it.
That entry closed with a free ETF census naming **exactly two** recorded objects that carry the
confound, both low-volatility books: `#30` at 20.8%, discharged the same night, and
**`#1 pt_lowvol_gk_quarterly` at 24.7%, the highest ETF share in the record**, which has been
carried on the handover of 2026-11-22, 11-23, 11-24 and 11-25 as "one `price-trend` trial
discharges it" and deferred four times for better uses of the budget. Tonight the budget is
there and the night's main thread is closed, so it is discharged.

WHAT THIS FILE CHANGES, AND IT IS ONE NODE. `#1` selects the 100 eligible names with the lowest
trailing 252-day Garman-Klass range volatility at quarter-ends, equal weight, with NO quota of
any kind -- a pure `nsmallest`. This file allots the same 100 slots across INSTRUMENT TYPE
cells in proportion to each type's share of the scorable set, which is the minimal change that
makes the book's asset-class mix match the pool's. The volatility estimator, the 252-day
window, the 80% coverage filter, the 150-name minimum, the quarterly grid, K = 100 and the
equal weighting are unchanged. Note it deliberately does NOT add the peer quota as well: `#1`
never had one, and adding two nodes at once would make the result unreadable. The geography
term is left unmatched and will be read, not fixed.

FREE PRE-TRIAL SCREEN, 83 train quarter-ends, measured before this file was written. No train
signal statistic (no IC, no train skill, no forward return) was computed.

    quantity                              #1 (no quota)    THIS FILE (type quota)
    ETF share of holdings                     24.7%               6.8%
    mean book size                            100.0               100.0
    holdings replaced per quarter             12.5%               14.3%
    top-100 Jaccard, the two books                     0.710
    rank persistence phi of -GK vol across quarter-ends        +0.967

6.8% against the panel's 5.5% is a near-exact match and reproduces `#31`'s ~5.0%. Jaccard
0.710 is what makes this a trial rather than a relabelling (the 0.90 bar is not approached):
the quota displaces 29% of the book, which is what cutting the ETF sleeve from a quarter to a
fifteenth of it costs. Turnover is essentially unchanged, so no cost story can confound the
reading -- this is the cleanest single-node benchmark-matching test available on this board.

PRE-REGISTERED PREDICTIONS, written before the run.
 - The SELECTION term (candidate Sharpe minus its null median) moves **0 to +0.08**, centred on
   the +0.056 the one recorded paired instance gave, and the GEOGRAPHY term (null median minus
   pool) moves toward zero by less than that, since no peer quota is added.
 - The book **STILL LOSES**: validation skill stays negative and the null percentile stays
   below the 90% gate. None of the six measurements behind "Sharpe is flat in beta on this
   panel" (2026-10-09/10 onward) is withdrawn by this file; the rider was only ever on their
   MAGNITUDE, because each was taken on a book whose ETF share nobody had measured.
 - CHURN: train **0.3-0.9x**, validation **0.4-1.3x** one-way (`#1` ran at ~0.51x; the
   replacement rate rises 12.5% -> 14.3% per quarter, so a touch more).
 - `#1`'s recorded v3 validation skill is **-0.03**. If this file lands materially ABOVE zero
   the finding is that the record's whole low-volatility literature on this panel was measured
   through an asset-class mismatch, which would be the largest methodological correction of the
   v3 era. I do not predict it, and the prediction above is that it does not happen.
 - REFUSAL, pre-committed: whatever this reads, the low-volatility axis is NOT re-opened with a
   third quota, a different window or a different volatility estimator. This trial exists to
   discharge a stated rider with a yes or a no, and the rider is discharged either way.

WHAT ARGUES AGAINST THE BOOK.
 (i) Reading instrument type is not hindsight -- type is static, survivorship-free and the
     protocol's own matching axis -- but it IS a second use of the same axis the null matches
     on, so the gain it buys is benchmark ALIGNMENT and not new signal. Nothing here makes the
     low-volatility sort a better predictor; it makes the comparison fair.
 (ii) `#1` is a v3 trial whose own stated case was that 0.51x turnover puts it beyond the cost
     model's reach. That case survives this change and so does its weakness: a book that almost
     never trades cannot earn its skill from selection timing, only from the level of the
     characteristic, and "the whole risk axis is worth nothing under this protocol"
     (2026-10-17/18) is the record's verdict on that level.
 (iii) The quota is allotted on type only, so the book's GEOGRAPHY is still chosen by the score.
     The 2026-10-15/16 and 2026-10-19/20 entries both warn that this leaves a region and FX bet
     inside the skill statistic. Fixing it would need the peer quota too, and that is the second
     node this file deliberately does not add.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib import features as F
from strategies.lib.calendar_peers import peer_quota_select

STRATEGY = {
    "name": "pt_lowvol_gk_typequota",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "Allotting pt_lowvol_gk_quarterly's 100 slots across INSTRUMENT TYPE cells in "
        "proportion to each type's share of the scorable set -- the one node that takes its "
        "ETF share from 24.7%, the highest in the record, to 6.8% against the panel's own "
        "5.5%, while leaving the Garman-Klass estimator, the 252-day window, the quarterly "
        "grid, K and the equal weighting byte-identical and the turnover within 2 percentage "
        "points of replacement per quarter -- moves that book's SELECTION term (its Sharpe "
        "minus its own null median) by 0 to +0.08, because `random_null_v3` matches type but "
        "matches nothing inside the ETF type, so a book holding a quarter of its weight in the "
        "quietest funds on the panel is compared against replicas drawn as random equity ETFs; "
        "and the book nevertheless still loses, with validation skill negative and a null "
        "percentile below the 90% gate, so that none of the six measurements behind 'Sharpe is "
        "flat in beta on this panel' is withdrawn and only their magnitude carries the rider."
    ),
}

VOL_WINDOW = 252
TOP_N = 100
MIN_NAMES = 150
MIN_COVERAGE = 0.8


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="QE")).tail(1).index

    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)
    kinds = data.instrument_types("pit")

    vol = F.garman_klass_vol(aux["open"], aux["high"], aux["low"], prices, window=VOL_WINDOW)
    covered = prices.notna().rolling(VOL_WINDOW, min_periods=1).mean()

    rows = {}
    for dt in rebalance_dates:
        if dt not in vol.index:
            continue
        v = vol.loc[dt].where(elig.loc[dt] & (covered.loc[dt] > MIN_COVERAGE))
        v = v[v > 0].dropna()
        if len(v) < MIN_NAMES:
            continue
        # Lowest volatility, allotted across instrument-type cells in proportion to each
        # type's share of the scorable set. `peer_quota_select` takes the HIGHEST scores,
        # so the score handed to it is the negated volatility.
        cells = pd.Series([str(kinds.get(n, "stock")) for n in v.index], index=v.index)
        picked = peer_quota_select(-v, cells, min(TOP_N, len(v)))
        if len(picked) < 20:
            continue
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
