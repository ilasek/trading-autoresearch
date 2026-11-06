"""Asymmetric comovement: downside CORRELATION, and coskewness.

Two objects, both computable from daily closes alone, both never sorted on in
this repo before 2026-11-06, and both chosen because they are **unit-free** --
which, on this panel, is a design requirement rather than an aesthetic.

WHY UNIT-FREE IS THE DESIGN. `experiments/learnings.md` records two separate
reasons a scale-carrying score is refused here. (i) Every object this lab has
screened that cleared |t| = 2 in bps carried a volatility ratio at least 0.14
away from 1.00, and its Sharpe skill was inside the noise floor or negative
(2026-10-20/21, eight paired observations); the risk axis is worth nothing in
Sharpe (2026-10-09/10) while a book MORE volatile than the pool is refused by
the drawdown gate (2026-11-05/06, twice), so the gate set admits only a narrow
band around volatility parity. (ii) The stored price and volume LEVELS embed
future corporate actions (2026-10-18 / 2026-10-22 engine issues), and a ratio
of same-window second and third moments cannot carry a per-name multiplicative
adjustment constant. Both statistics below divide their scale out by
construction rather than by a post-hoc control, which is research `#406`'s
"design the confound out" applied to the one confound this panel is known to
have.

--------------------------------------------------------------------------
DOWNSIDE CORRELATION  `rho_minus`
--------------------------------------------------------------------------
    rho_minus(i) = corr(r_i, r_m)  over the days in the window on which r_m
                   was below its own window mean.

Ang-Chen-Xing's disappointment-aversion story is about downside BETA,
`beta_minus = Cov(r_i, r_m | r_m < mu) / Var(r_m | r_m < mu)`. Research note
`#116` records that sort as REFUTED and says exactly why, through the identity

    beta_minus = rho_minus * sigma_minus_i / sigma_minus_m,

i.e. a high downside beta comes either from high downside CORRELATION, which is
the priced content, or from the name's own downside VOLATILITY, which carries
the opposite-signed volatility effect and dominates the extreme bucket. The
note's words: *"the raw beta_minus sort is a refuted construction and must not
be proposed here; what has never been measured is the correlation with the
volatility term divided out."* `rho_minus` is that object and nothing else:
`sigma_minus_i` is divided out, `sigma_minus_m` is common to every name on a
date and therefore drops out of any cross-sectional rank.

The pre-signed direction is LOW `rho_minus` held long -- a name that comoves
LESS with the market when the market falls is the one that does not fail you
when diversification is worth most, and disappointment aversion says that
service is paid for.

--------------------------------------------------------------------------
COSKEWNESS  `beta_skd`
--------------------------------------------------------------------------
    beta_skd(i) = E[e_i * e_m^2] / sqrt( E[e_i^2] * E[e_m^2] )

with `e_i` the market-model residual of name i and `e_m` the demeaned market
return, both over the same window (research `#118`; Harvey-Siddique). Unit-free
by construction, and built from residuals orthogonal to the market, so it is
not the beta axis the lab closed from the selection side on 2026-10-20/21.

Extend utility to the third moment and an asset that makes a diversified
portfolio's distribution more left-skewed must be PAID for, so the premium on
coskewness is NEGATIVE and the tradeable long bucket is the most-negative third.
The pre-signed direction is therefore LOW `beta_skd` held long.

THE ESTIMATION WINDOW IS THE LIVE DISAGREEMENT, AND THE NOTE RESOLVES IT ONE
WAY. `#118` records Hou-Xue-Zhang reading coskewness as right-signed but
insignificant while others recover it, and the most parsimonious reconciliation
in the note is that HXZ estimate the third moment from ONE MONTH of daily
returns, where Harvey-Siddique are explicit that odd moments are not persistent
and that noise in a third moment is amplified by a cube rather than a square.
This module therefore uses a LONG window (756 trading days ~ 36 months, the
short end of Harvey-Siddique's own 36-72 month grid) and a 21-day lag, which is
also the window every other score on this lab's v3 board uses.

HONEST CAVEAT, CARRIED BECAUSE IT CUTS AGAINST THE EXERCISE. `#118`'s most
transferable remark is Harvey-Siddique's own: *the highest-Sharpe styles often
have the most negative skew, which is part of why their Sharpe ratios are
high.* The lab's objective IS Sharpe, and Sharpe does not penalise left skew.
So a book that buys the most-negative-coskewness names is, by the mechanism's
own logic, buying a skew risk premium, and a positive skill reading would be
partly compensation rather than selection. Any candidate using this score must
report its own realised skewness beside its Sharpe and say so.

CAUSALITY. Every value is computed from a window that ENDS `lag` trading days
before the row it is published on, and published on a month-end grid that is
then forward-filled to daily. Nothing indexes past the row it is asked about.

NOTE ON THE FILE-PERMISSION RULE: `strategies/lib/` may gain new files but no
existing one may ever be edited, because a promoted candidate keeps importing
it. This file is therefore frozen from the moment it is committed.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

WINDOW = 756       # ~36 months, the short end of Harvey-Siddique's own grid
LAG = 21           # trading days between the end of the window and the row
MIN_OBS = 400      # usable market days required in the full window
MIN_DOWN = 133     # usable market days required in the r_m < mu sub-window


def _nanmean(a: np.ndarray, axis: int = 0) -> np.ndarray:
    with np.errstate(invalid="ignore"):
        return np.nanmean(a, axis=axis)


def market_return(prices: pd.DataFrame, eligible: pd.DataFrame | None) -> pd.Series:
    """The equal-weight eligible panel's daily return -- the same basket the
    protocol benchmarks against, computed from the frames a candidate is given.
    Uses only same-day and earlier closes."""
    r = prices.pct_change(fill_method=None)
    if eligible is not None:
        mask = eligible.reindex(index=r.index, columns=r.columns).fillna(False).to_numpy()
        r = r.where(mask)
    return r.mean(axis=1, skipna=True)


def moment_scores(prices: pd.DataFrame, eligible: pd.DataFrame | None = None,
                  window: int = WINDOW, lag: int = LAG,
                  min_obs: int = MIN_OBS, min_down: int = MIN_DOWN):
    """`(rho_minus, beta_skd)` as daily frames, each published on month-ends
    from a window ending `lag` trading days earlier and forward-filled."""
    r = prices.pct_change(fill_method=None)
    rm = market_return(prices, eligible)
    R, M = r.to_numpy(), rm.to_numpy()
    pos = {d: i for i, d in enumerate(r.index)}

    out_rho: dict = {}
    out_skd: dict = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        end = pos[date] - lag
        if end < window:
            continue
        sl = slice(end - window, end)
        X, m = R[sl], M[sl]
        ok = np.isfinite(m)
        if ok.sum() < min_obs:
            continue

        # ---- coskewness over the whole window ----
        mm, Xm = m[ok], X[ok]
        em = mm - mm.mean()
        vm = float((em * em).mean())
        valid = np.isfinite(Xm)
        n = valid.sum(axis=0)
        Xf = np.where(valid, Xm, np.nan)
        xbar = _nanmean(Xf)
        b = _nanmean((Xf - xbar) * em[:, None]) / vm if vm > 0 else np.full(Xf.shape[1], np.nan)
        e = Xf - xbar - b * em[:, None]
        den = np.sqrt(_nanmean(e * e) * vm)
        with np.errstate(invalid="ignore", divide="ignore"):
            out_skd[date] = np.where((n >= min_obs) & (den > 0),
                                     _nanmean(e * (em * em)[:, None]) / den, np.nan)

        # ---- downside correlation over the r_m < mu sub-window ----
        dn = ok & (m < m[ok].mean())
        if dn.sum() < min_down:
            continue
        md, Xd = m[dn], X[dn]
        vd = np.isfinite(Xd)
        nd = vd.sum(axis=0)
        Xdf = np.where(vd, Xd, np.nan)
        xb = _nanmean(Xdf)
        emd = md - md.mean()
        sx = np.sqrt(_nanmean((Xdf - xb) ** 2))
        sm = float(np.sqrt((emd * emd).mean()))
        with np.errstate(invalid="ignore", divide="ignore"):
            out_rho[date] = np.where((nd >= min_down) & (sx > 0) & (sm > 0),
                                     _nanmean((Xdf - xb) * emd[:, None]) / sx / sm, np.nan)

    cols = prices.columns

    def _frame(d):
        if not d:
            return pd.DataFrame(index=prices.index, columns=cols, dtype=float)
        return pd.DataFrame(d, index=cols).T.sort_index().reindex(prices.index, method="ffill")

    return _frame(out_rho), _frame(out_skd)


def downside_correlation_score(prices, aux=None, eligible=None, window: int = WINDOW,
                               lag: int = LAG, sign: float = 1.0) -> pd.DataFrame:
    """Minus `rho_minus`: HIGH where a name comoves LEAST with the market on the
    market's down days, with its own downside volatility divided out."""
    rho, _ = moment_scores(prices, eligible, window=window, lag=lag)
    return sign * (-rho)


def coskewness_score(prices, aux=None, eligible=None, window: int = WINDOW,
                     lag: int = LAG, sign: float = 1.0) -> pd.DataFrame:
    """Minus `beta_skd`: HIGH where a name's coskewness with the market is most
    NEGATIVE -- the bucket Harvey-Siddique's negative premium says is paid."""
    _, skd = moment_scores(prices, eligible, window=window, lag=lag)
    return sign * (-skd)


# ---------------------------------------------------------------------------
# The book
# ---------------------------------------------------------------------------
# The construction is the one `strategies/lib/session_split.py` documents, node
# for node -- `calendar_peers` cells crossed with a tercile of a second
# characteristic, `peer_quota_select` at K=100, six overlapping monthly sleeves
# with one reformed each month-end, ineligible names pruned at every month-end.
# It is reproduced here rather than imported with a different score because
# `session_split.py` is already the source of recorded trials and must not change.
#
# The ONE node that is new is `cells`. `"mom"` crosses the peer group with a
# 12-1 momentum tercile, which is what every sleeve book on this board has used.
# `"vol"` crosses it with a trailing-volatility tercile instead, which is
# research `#406`'s "design the confound out rather than regress it out":
# pre-sort on volatility, then sort on the signal WITHIN tercile, so the book's
# volatility profile matches the panel's by construction rather than by
# assumption. `experiments/learnings.md` holds the volatility level to be this
# universe's own artifact and the de-risking axis to be closed, so for a score
# that selects on comovement this is the node that decides whether the claim is
# a comovement claim at all.

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select  # noqa: E402

K = 100
HOLD = 6
CELL_BINS = 3
VOL_WINDOW = 126


def _cell_values(prices: pd.DataFrame, cells: str) -> pd.DataFrame:
    if cells == "mom":
        return prices.pct_change(252, fill_method=None).shift(21)
    if cells == "vol":
        r = prices.pct_change(fill_method=None)
        return r.rolling(VOL_WINDOW, min_periods=VOL_WINDOW // 2).std().shift(LAG)
    raise ValueError(cells)


def moment_book(prices, aux, eligible=None, score_fn=None, cells: str = "mom",
                k: int = K, hold: int = HOLD, window: int = WINDOW,
                sign: float = 1.0) -> pd.DataFrame:
    score_fn = score_fn or downside_correlation_score
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    volume = aux["volume"]
    px = prices.ffill()
    score = score_fn(prices, aux, eligible=elig, window=window, sign=sign)
    cell_vals = _cell_values(prices, cells)

    sleeves: dict[int, pd.Series] = {}
    formed: set[int] = set()
    rows: dict = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue
        if sleeves:
            ok = set(names)
            sleeves = {s: sh[[n in ok for n in sh.index]] for s, sh in sleeves.items()}
            sleeves = {s: sh for s, sh in sleeves.items() if len(sh)}
        p = px.loc[date]
        vals = {s: float((sh * p.reindex(sh.index)).fillna(0.0).sum())
                for s, sh in sleeves.items()}
        value = float(sum(vals.values()))

        sc = score.loc[date].reindex(names)
        sc = sc[np.isfinite(sc)].dropna()
        picked = None
        if len(sc) >= 50:
            groups = calendar_peers(volume, date, sc.index).dropna()
            if len(groups) >= 50:
                sc = sc.reindex(groups.index)
                cv = cell_vals.loc[date].reindex(groups.index)
                try:
                    bins = pd.qcut(cv.rank(method="first"), CELL_BINS, labels=False)
                except ValueError:
                    bins = pd.Series(0, index=cv.index)
                cell = groups.astype(str) + "|" + bins.fillna(0).astype(int).astype(str)
                cand = peer_quota_select(sc, cell, k)
                if len(cand) >= 20:
                    picked = cand

        if picked is None:
            # Hold the equal-weight eligible pool until the score exists: causal,
            # free, and worth ~0.07 of train skill (`learnings.md`, 2026-10-16).
            if value == 0.0:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        sleeve = (date.year * 12 + date.month - 1) % hold
        if value == 0.0:
            target = 1.0
        elif sleeve not in formed:
            target = value / hold
            sleeves = {s: sh * ((value - target) / value) for s, sh in sleeves.items()}
        else:
            target = vals.get(sleeve, 0.0)

        pp = p.reindex(picked)
        pp = pp[pp > 0].dropna()
        if len(pp) < 20 or target <= 0:
            continue
        sleeves[sleeve] = (target / len(pp)) / pp
        formed.add(sleeve)

        held = pd.Series(0.0, index=prices.columns, dtype=float)
        for sh in sleeves.values():
            held = held.add((sh * p.reindex(sh.index)).reindex(prices.columns).fillna(0.0),
                            fill_value=0.0)
        total = float(held.sum())
        if total > 0:
            rows[date] = held[held > 1e-12] / total

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0).sort_index()
