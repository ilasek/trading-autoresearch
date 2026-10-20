"""The estimation half of `statistical-arbitrage`: the cointegrating slope of a
name's log price on its own peer-group index, at fixed own volatility.

Hypothesis (pre-registered, see the journal entry for this trial): the 100
eligible names with the HIGHEST slope in an Engle-Granger cointegrating
regression of their 504-day log price on their own calendar-peer-group's
equal-weight log-price index -- that slope orthogonalised WITHIN the group
against 126-day realised volatility, so the score is not the refuted low-vol
object -- earn positive validation skill over the equal-weight eligible pool.
Pre-signed direction: HIGH slope earns MORE.

Why this family and why this object. `research/SUMMARY.md`'s own open-questions
entry (2026-10-20) names `statistical-arbitrage`'s ESTIMATION half as the
best-aimed choice left: the family's residual-reversion half has four notes and
a recorded trial, while `Engle-Granger`, `Kalman` and `cointegrat` return
essentially zero across 207 notes, and `program.md`'s charter for the family
asks specifically what survives the long-only constraint. The whole estimation
branch was screened free on train tonight (journal F1-F6) and the branch's own
objects are nulls: the cheap side of the spread, the stationarity t-statistic,
the OU half-life, the spread's amplitude, and the level-by-speed interaction.
This slope is what was left standing when they fell.

What the screen says, in the night's own calibrated units. Tonight's
noisy-oracle block (F7/F8) fixes the exchange rate between a within-region rank
IC against the forward 63-day return and the train skill a K=100 monthly book
earns on it: skill ~= 3.37 * IC, with an uninformative score's skill scattered
at sd ~= 0.025. In those units:

    within-region rank IC (vol-neutral slope)      +0.0328  (t +3.23)
    implied gross train skill, 3.37 * IC           +0.111
    measured gross train skill in the harness      +0.041
    slice volatility ratio to the pool              1.187
    one-way name churn (harness / candidate)        1.03x / 1.39x per yr
    net train skill after ~60 bps/yr               ~+0.008
    noise floor sd of a train skill number          0.025

So the expected verdict is written down before the run: **a dead heat or a
GATE_FAIL**. The gap between the implied +0.111 and the measured +0.041 is the
whole point -- 62% of this score's mean ordering is paid for in volatility,
which is the standing warning of `experiments/learnings.md` (2026-10-13) that a
level premium passes a bps screen and fails a ratio gate.

Three stated reasons the trial is spent anyway, and no others.

(i) **The beta axis has never been tested as a SELECTION under v3.** The
learnings entry "Sharpe is flat in beta on this panel" was measured from a
low-volatility selection (`pt_lowvol_gk_quarterly`) and from covariance
WEIGHTING (2026-10-17/18). A within-group price-level slope at fixed own
volatility is neither, and the orthogonalisation is what separates it from the
refuted object: the raw group-explained share `r2` carries IC +0.0332, and
residualising it on volatility AND this slope collapses it to -0.0028, so the
slope is the axis and `r2` was its costume.

(ii) **It is the only object screened tonight whose mean ordering holds its
sign in both train sub-periods** -- the low side reads -33.5 bps/63d in
1997-2008 and -182.3 in 2009-2017, both region-matched -- against a gate that
is on 1997-2017 as a whole, and against a night in which sub-period sign
inversion refused three separate objects.

(iii) **It is the cheapest book this lab has built.** The candidate's own
construction churns 1.39x one-way on train (the harness's simpler top-100 read
1.03x; the quota and the within-group residual add the difference), a cost bill
of about 60 bps/yr, where the v3 board's trials have run 1.3x to 10.5x. Whether
a nearly-free book can clear the null gate is a question the board has no
observation on.

Two things deliberately NOT done. **No retention band**, though it is the one
construction the lab has measured as paying: the 2026-10-18 engine issue records
that the null's replicas are not held to the eligibility boundary the candidate
is held to, worth +0.005 to +0.017 of Sharpe TO THE NULL and rising with holding
length, so a low-turnover operator buys its cost saving partly out of its own
gate margin -- and this book is already at the cheap end without one. And the
LOW side of the slope sort is not traded even though its region-matched excess
is the larger of the two in magnitude: the literature signs the high side, and
choosing a sign because the number came out that way is what the lab refuses
(2026-10-13).

Pre-registered turnover, as a range with the wider split's churn in it: the
candidate's measured train one-way name churn is 1.39x and the engine's metric
counts both sides, so train should charge ~2.8x; validation name churn has run
68-81% above train's on this panel, and every turnover range this lab has
pre-registered has turned out to be a lower bound, so the predicted band is
**2.5-6.0x annualised**.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.features import realized_vol

K = 100
WINDOW = 504
MIN_OBS = 400
VOL_WINDOW = 126
MIN_NAMES = 60
MIN_GROUP = 5

STRATEGY = {
    "name": "sa_coint_slope_volneutral",
    "family": "statistical-arbitrage",
    "hypothesis": (
        "Selecting the 100 eligible names with the highest slope in an Engle-Granger "
        "cointegrating regression of their 504-day log price on their own calendar-peer-"
        "group equal-weight log-price index, that slope orthogonalised within the group "
        "against 126-day realised volatility so it is not the refuted low-vol object, "
        "earns positive validation skill over the equal-weight eligible pool, because the "
        "estimation half of a cointegrating relationship prices how much of a name's level "
        "is carried by its group and the long-only book can only hold the high-loading "
        "side. Tonight's calibration implies +0.111 of gross train skill from a within-"
        "region rank IC of +0.0328 (t +3.23) and the harness measures +0.041, the gap "
        "being volatility, so a dead heat or a GATE_FAIL is the expected verdict; the "
        "object is traded because the beta axis has never been tested as a selection "
        "under v3, its mean ordering is the only one screened tonight that holds sign in "
        "both train sub-periods, and at 1.03x one-way churn it is the cheapest book the "
        "lab has built."
    ),
    "track": "scout",
}


def _group_slopes(logp: np.ndarray, label: np.ndarray) -> np.ndarray:
    """Per group: OLS slope of each member's log price on the group's
    equal-weight log-price index, over the whole window."""
    out = np.full(logp.shape[1], np.nan)
    for g in np.unique(label):
        idx = np.where(label == g)[0]
        if len(idx) < MIN_GROUP:
            continue
        sub = logp[:, idx]
        b = sub.mean(axis=1)
        bc = b - b.mean()
        den = float(bc @ bc)
        if den <= 1e-12:
            continue
        out[idx] = (bc @ (sub - sub.mean(axis=0))) / den
    return out


def _vol_neutral(score: pd.Series, vol: pd.Series, groups: pd.Series) -> pd.Series:
    """Within each peer group, the residual of rank(score) on rank(vol). The
    orthogonalisation is inside the group because the group is the only region
    proxy a candidate may read, and a cross-group fit would let one market's
    volatility level stand in for another's."""
    out = pd.Series(index=score.index, dtype=float)
    for g, idx in score.groupby(groups.reindex(score.index).to_numpy()).groups.items():
        if len(idx) < MIN_GROUP:
            continue
        y = score.loc[idx].rank().to_numpy()
        x = vol.reindex(idx).rank().to_numpy()
        if not np.isfinite(x).all() or np.nanstd(x) <= 0:
            out.loc[idx] = y - y.mean()
            continue
        design = np.column_stack([np.ones(len(idx)), x])
        beta, *_ = np.linalg.lstsq(design, y, rcond=None)
        out.loc[idx] = y - design @ beta
    return out.dropna()


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K highest volatility-neutral peer-group
    slopes, quota-allocated across peer groups so the book's geography matches
    the pool's. The equal-weight eligible pool is emitted on month-ends where
    the score does not exist yet, so the book is never scored in cash against a
    fully-invested benchmark (`experiments/learnings.md`, 2026-10-15/16)."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    logp = np.log(prices.where(prices > 0))
    vol126 = realized_vol(prices, VOL_WINDOW)

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows: dict = {}
    for date in month_ends:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < MIN_NAMES:
            continue
        pool = pd.Series(1.0 / len(names), index=names)

        # Peer groups from the trailing trading calendar, over the eligible
        # names only -- never the whole visible frame, whose column count
        # differs between the truncated and untruncated causality runs.
        groups = calendar_peers(volume, date, names)
        if groups.empty:
            rows[date] = pool
            continue

        win = logp.loc[:date, groups.index].iloc[-WINDOW:]
        if len(win) < MIN_OBS:
            rows[date] = pool
            continue
        good = groups.index[win.notna().sum().to_numpy() >= MIN_OBS]
        if len(good) < MIN_NAMES:
            rows[date] = pool
            continue
        arr = win[good].ffill().bfill().to_numpy()
        if not np.isfinite(arr).all():
            rows[date] = pool
            continue

        label = pd.factorize(groups.reindex(good))[0]
        slope = pd.Series(_group_slopes(arr, label), index=good).dropna()
        if len(slope) < MIN_NAMES:
            rows[date] = pool
            continue

        score = _vol_neutral(slope, vol126.loc[date].reindex(slope.index), groups)
        if len(score) < MIN_NAMES:
            rows[date] = pool
            continue

        picked = peer_quota_select(score, groups.reindex(score.index), K)
        if len(picked) < 20:
            rows[date] = pool
            continue
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
