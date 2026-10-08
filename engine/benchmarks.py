"""Survivorship-matched benchmarks for protocol v2 (and v3, below).

Both benchmarks pick from exactly the pool the candidate could pick from on
each date — the point-in-time eligible, priced names. The survivorship bias
that pool still carries (members Yahoo no longer prices are absent from it) is
*not* neutral between the two, contrary to what this module used to claim: the
missing members are disproportionately names that fell hard and then failed,
and a strategy that deliberately buys recent losers would have held them far
more often than a random draw does. So the comparison flatters loser-buying
books (reversal, deep value) relative to the null. Protocol v3 reports a
delisting-haircut stress for exactly this reason; read it next to the null.

- `equal_weight`: every eligible name, equal weight, rebalanced at month-ends.
- `random_null`: the candidate's own portfolio construction with its choices
  randomised. Each draw keeps the candidate's holdings schedule (the dates its
  set of names changes), its weight vector, gross exposure, stock/ETF mix and
  thus its turnover in names, but every name the candidate *enters* is replaced
  by a name drawn uniformly from the same type's eligible, unused names on that
  date, and held for exactly as long as the candidate held its name. The
  distribution of the draws' Sharpe ratios is what "picking at random, built
  exactly like this" earns on the same pool (cf. Daniel, Sornette & Woehrmann
  on constrained random portfolios as the null for look-ahead-biased
  universes; research/notes/2026-08-26-look-ahead-benchmark-bias-index-constituents.md).

Both use the engine's cost model and the same daily return convention as
`engine.backtest.run_backtest`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import metrics


def _returns(held: pd.DataFrame, prices: pd.DataFrame, cost_bps: float, slippage_bps: float) -> pd.Series:
    """Net daily returns of `held` (weights already in force on each day,
    i.e. lagged), mirroring run_backtest's arithmetic."""
    rets = prices.pct_change(fill_method=None).fillna(0.0).reindex(index=held.index, columns=held.columns)
    gross = (held * rets.fillna(0.0)).sum(axis=1)
    turnover = held.diff().abs().sum(axis=1).fillna(0.0)
    return gross - turnover * (cost_bps + slippage_bps) / 1e4


def equal_weight(
    prices: pd.DataFrame,
    eligible: pd.DataFrame,
    start: str | None,
    end: str | None,
    cost_bps: float = 10.0,
    slippage_bps: float = 5.0,
) -> pd.Series:
    """Daily net returns of an equal-weight portfolio of every eligible name,
    re-formed at each month-end from that day's eligible set, held with a
    one-day lag. Returns the series restricted to [start, end]."""
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    target = elig.loc[month_ends].astype(float)
    target = target.div(target.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    w = target.reindex(prices.index).ffill().fillna(0.0)
    w = w.where(prices.notna(), 0.0)
    held = w.shift(1).fillna(0.0)
    r = _returns(held, prices, cost_bps, slippage_bps)
    return r.loc[start:end]


def random_null(
    held: pd.DataFrame,
    prices: pd.DataFrame,
    eligible: pd.DataFrame,
    types: dict[str, str],
    n_draws: int = 200,
    seed: int = 0,
    cost_bps: float = 10.0,
    slippage_bps: float = 5.0,
) -> tuple[np.ndarray, list[pd.Series]]:
    """Sharpe ratios (annualised) of `n_draws` randomised replicas of `held`.

    `held` is the candidate's lagged daily holdings over the scored window
    (`BacktestResult.weights` restricted to it). A name counts as entered on
    the first day of the window it is held and on every day it goes from
    unheld to held; replicas draw from names eligible on the day *before*
    (the decision day, matching the one-day execution lag).

    Returns (sharpes, return series of the first few draws for inspection)."""
    held = held.fillna(0.0)
    cols = list(held.columns)
    elig = eligible.reindex(index=prices.index, columns=cols).fillna(False).astype(bool)
    decision = elig.shift(1).fillna(False).astype(bool).reindex(held.index).fillna(False)
    h = held.to_numpy()
    on = np.abs(h) > 1e-12
    col_type = np.array([types.get(c, "") for c in cols])
    pool_by_type = {t: np.flatnonzero(col_type == t) for t in set(col_type) if t}
    d_arr = decision.to_numpy()
    rng = np.random.default_rng(seed)

    # Dates where the candidate's set of names changes; weights alone may vary
    # daily in between, and a replica tracks those through its name mapping.
    change = np.ones(len(h), dtype=bool)
    change[1:] = (on[1:] != on[:-1]).any(axis=1)
    change_idx = np.flatnonzero(change)

    sharpes = np.empty(n_draws)
    keep: list[pd.Series] = []
    px = prices.reindex(index=held.index, columns=cols)
    for k in range(n_draws):
        mapping: dict[int, int] = {}          # candidate column -> replica column
        out = np.zeros_like(h)
        for n, i0 in enumerate(change_idx):
            i1 = change_idx[n + 1] if n + 1 < len(change_idx) else len(h)
            now = set(np.flatnonzero(on[i0]))
            for c in list(mapping):
                if c not in now:
                    del mapping[c]
            used = set(mapping.values())
            for c in sorted(now - set(mapping)):
                pool = pool_by_type.get(col_type[c])
                if pool is None or not len(pool):
                    mapping[c] = c
                    continue
                cand = pool[d_arr[i0, pool]]
                cand = cand[~np.isin(cand, list(used))] if used else cand
                pick = int(rng.choice(cand)) if len(cand) else c
                mapping[c] = pick
                used.add(pick)
            src = np.fromiter(mapping.keys(), dtype=int)
            dst = np.fromiter(mapping.values(), dtype=int)
            if len(src):
                out[i0:i1, dst] += h[i0:i1, src]
        replica = pd.DataFrame(out, index=held.index, columns=cols)
        replica = replica.where(px.notna(), 0.0)
        r = _returns(replica, prices, cost_bps, slippage_bps)
        sharpes[k] = metrics.sharpe(r)
        if k < 3:
            keep.append(r)
    return sharpes, keep


# ---------------------------------------------------------------------------
# Protocol v3: the same benchmarks, run through the execution model
# ---------------------------------------------------------------------------
#
# The v2 null replayed the candidate's *lagged daily holdings* with names
# swapped, valued at constant weights. Under v3 holdings drift and fills are
# per-name, so a replica must be built from the candidate's *decisions* (the
# rows it emitted) and run through exactly the same `simulate` call. Two more
# changes: replacements for a stock are drawn from stocks listed in the same
# region (a random book with the candidate's region and currency mix — a
# region/FX tilt is not stock selection), and Sharpe is on excess returns.


def equal_weight_targets(prices: pd.DataFrame, eligible: pd.DataFrame) -> pd.DataFrame:
    """Month-end decision rows: equal weight over every eligible name."""
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    target = elig.loc[month_ends].astype(float)
    return target.div(target.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)


def equal_weight_v3(prices: pd.DataFrame, eligible: pd.DataFrame, execution) -> pd.Series:
    """Daily net returns of the equal-weight eligible pool under `execution`,
    over the whole of `prices` (callers slice the window they score)."""
    from .backtest import simulate
    return simulate(equal_weight_targets(prices, eligible), prices, execution,
                    keep_weights=False).returns


def random_null_v3(
    targets: pd.DataFrame,
    prices: pd.DataFrame,
    eligible: pd.DataFrame,
    types: dict[str, str],
    regions: dict[str, str],
    execution,
    window: tuple[pd.Timestamp, pd.Timestamp],
    n_draws: int = 200,
    seed: int = 0,
    max_leverage: float = 1.0,
) -> tuple[np.ndarray, list[pd.Series]]:
    """Excess-return Sharpe ratios of `n_draws` randomised replicas of the
    candidate's decision rows `targets`, scored on `window` (inclusive).

    Each decision row keeps its weight vector; a name the candidate already
    held at the previous decision keeps its replacement, and every name it
    *enters* is replaced by a name drawn uniformly from the eligible, unused
    names on that decision date with the same type — and, for stocks, the same
    listing region (falling back to any region if that region has none left).
    Replicas start flat on the row before the window and take the instruction
    in force at that point, exactly as the candidate's book is in force."""
    from .backtest import simulate
    lo, hi = pd.Timestamp(window[0]), pd.Timestamp(window[1])
    idx = prices.index
    first = idx[idx >= lo][0]
    pos = idx.get_loc(first)
    sim_start = idx[max(0, pos - 1)]
    tg = targets.loc[(targets.index <= hi)]
    prior = tg.loc[tg.index < sim_start]
    tg = pd.concat([prior.iloc[-1:], tg.loc[tg.index >= sim_start]]) if len(prior) else \
        tg.loc[tg.index >= sim_start]
    cols = list(prices.columns)
    key = np.array([(types.get(c, ""), regions.get(c, "") if types.get(c) == "stock" else "")
                    for c in cols], dtype=object)
    by_type = {t: np.flatnonzero(np.array([types.get(c, "") for c in cols]) == t)
               for t in set(types.get(c, "") for c in cols) if t}
    by_key: dict[tuple, np.ndarray] = {}
    for i, kk in enumerate(map(tuple, key)):
        by_key.setdefault(kk, []).append(i)
    by_key = {k: np.array(v) for k, v in by_key.items()}
    elig = eligible.reindex(index=tg.index, columns=cols).fillna(False).to_numpy(bool)
    tv = tg.reindex(columns=cols).fillna(0.0).to_numpy(dtype=float)
    on = np.abs(tv) > 1e-12
    rng = np.random.default_rng(seed)
    px = prices.loc[prices.index <= hi]
    sharpes = np.empty(n_draws)
    keep: list[pd.Series] = []
    rf = execution.rf
    for k in range(n_draws):
        mapping: dict[int, int] = {}
        out = np.zeros_like(tv)
        for r in range(len(tv)):
            now = set(np.flatnonzero(on[r]))
            for c in list(mapping):
                if c not in now:
                    del mapping[c]
            used = set(mapping.values())
            for c in sorted(now - set(mapping)):
                t = types.get(cols[c], "")
                pick = c
                for pool in (by_key.get(tuple(key[c])), by_type.get(t)):
                    if pool is None or not len(pool):
                        continue
                    cand = pool[elig[r, pool]]
                    if used:
                        cand = cand[~np.isin(cand, list(used))]
                    if len(cand):
                        pick = int(rng.choice(cand))
                        break
                mapping[c] = pick
                used.add(pick)
            for c, d in mapping.items():
                out[r, d] += tv[r, c]
        replica = pd.DataFrame(out, index=tg.index, columns=cols)
        replica = replica.loc[:, (replica.abs() > 0).any(axis=0)]
        res = simulate(replica, px, execution, max_leverage, keep_weights=False, start=sim_start)
        r_win = res.returns.loc[lo:hi]
        sharpes[k] = metrics.sharpe(r_win, rf)
        if k < 3:
            keep.append(r_win)
    return sharpes, keep


def null_summary(candidate_sharpe: float, sharpes: np.ndarray) -> dict:
    """Where the candidate sits in its null distribution."""
    return {
        "null_p50": round(float(np.quantile(sharpes, 0.50)), 3),
        "null_p90": round(float(np.quantile(sharpes, 0.90)), 3),
        "null_p95": round(float(np.quantile(sharpes, 0.95)), 3),
        "null_pctile": round(float((sharpes < candidate_sharpe).mean()), 3),
        "null_draws": int(len(sharpes)),
    }
