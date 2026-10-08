"""Daily backtest engine: the legacy vectorized model and the v3 execution model.

Legacy model (protocol v1/v2; `run_backtest` without an `execution`), unchanged
so every recorded v1/v2 number reproduces:
- weights decided on row t earn the return from close t to close t+1, i.e. the
  book trades at the same close its signal was computed from;
- target weights are held constant every day (an implicit free daily rebalance);
- costs are charged only on changes of the target, at one flat rate.

Execution model (protocol v3; `run_backtest(..., execution=ExecutionModel(...))`),
built because each legacy convention flatters a strategy:
- **Fill at the next real print.** A decision emitted on row d is filled, name by
  name, at the first close strictly after row d on which that name actually
  traded (`traded`, not a forward-filled holiday price). On a calendar that is
  the union of exchanges, row d's information includes the US close, which is
  ~15 hours *after* the Tokyo close of the same date; trading Tokyo at that
  close would be look-ahead the causality check cannot see. Filling at the next
  real print is causal in every time zone and removes same-close bid-ask bounce.
- **Holdings drift.** Between the rows a strategy emits, positions are held as
  shares: weights move with prices. An emitted row is a rebalance instruction
  and its trades — including those that undo drift — are charged.
- **Costs per name** from `costs.CostModel`: a liquidity tier plus the listing
  market's transaction tax.
- **Cash earns the risk-free rate** (`rf`, daily simple return per row).
- **Series that end while held** are exited at the last price, as before; the
  `delist_haircut` stress instead books that exit at a loss.

Guarantees in both models: long-only by default, per-position cap and gross
leverage cap at decision time (scaled down, never up), no weight on a name
without a price.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from .costs import CostModel


@dataclass
class BacktestResult:
    returns: pd.Series          # net daily portfolio returns
    gross_returns: pd.Series    # before costs
    equity: pd.Series           # cumulative net growth of $1
    weights: pd.DataFrame       # effective weights actually held during each row
    turnover: pd.Series         # daily sum |Δw| traded
    costs: pd.Series            # daily cost drag
    delisted: pd.Series | None = None   # weight force-exited because its series ended
    targets: pd.DataFrame | None = None  # v3: sanitized decision rows (what was ordered)

    @property
    def ann_turnover(self) -> float:
        return float(self.turnover.mean() * 252)

    def avg_positions(self) -> float:
        return float((self.weights.abs() > 1e-6).sum(axis=1).mean())


@dataclass
class ExecutionModel:
    """How decisions become trades under protocol v3 (see the module docstring).

    Every field is optional so synthetic tests can build one: `traded=None`
    treats every priced row as a real print, `rf=None` pays 0 on cash, and
    `costs=None` charges the legacy flat rate."""
    traded: pd.DataFrame | None = None      # dates x columns, bool: a real print that day
    rf: pd.Series | None = None             # daily simple return on cash, by row
    costs: CostModel | None = None
    delist_haircut: float = 0.0             # stress: loss booked on a forced exit

    def stressed(self, cost_multiplier: float = 1.0, delist_haircut: float | None = None):
        costs = (self.costs or CostModel()).stressed(cost_multiplier)
        return replace(self, costs=costs,
                       delist_haircut=self.delist_haircut if delist_haircut is None else delist_haircut)


def sanitize_weights(
    weights: pd.DataFrame,
    prices: pd.DataFrame,
    max_weight: float,
    max_leverage: float,
    allow_short: bool,
    eligible: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Validate and normalize raw strategy weights onto the price calendar.

    `eligible` (dates x instruments, bool; protocol v2) is the point-in-time
    universe. On every row the strategy emitted — a rebalance — weight on a
    name that is not eligible that day is set to zero before forward-filling:
    a name can only be bought while it is in the universe, and a held name is
    kept only until the next rebalance after it leaves. Rows the strategy did
    not emit are untouched, so an index exit between rebalances does not force
    a sale the strategy never decided."""
    if not isinstance(weights, pd.DataFrame):
        raise TypeError("generate_weights must return a DataFrame")
    unknown = weights.columns.difference(prices.columns)
    if len(unknown):
        raise ValueError(f"weights reference unknown instruments: {list(unknown)[:5]}")
    future = weights.index.difference(prices.index)
    if len(future):
        raise ValueError(
            f"weights contain dates outside the price calendar (first: {future[0]})"
        )
    w = weights.reindex(index=prices.index, columns=prices.columns)
    if eligible is not None:
        rows = weights.index
        ok = eligible.reindex(index=rows, columns=prices.columns).fillna(False).astype(bool)
        w.loc[rows] = w.loc[rows].where(ok, 0.0)
    w = w.ffill().fillna(0.0)
    if not allow_short:
        w = w.clip(lower=0.0)
    w = w.clip(lower=-max_weight, upper=max_weight)
    # Zero out weight wherever there is no price (instrument not yet listed/delisted).
    w = w.where(prices.notna(), 0.0)
    gross = w.abs().sum(axis=1)
    scale = np.where(gross > max_leverage, max_leverage / gross.replace(0, np.nan), 1.0)
    w = w.mul(pd.Series(scale, index=w.index).fillna(1.0), axis=0)
    return w


def _check_frame(weights: pd.DataFrame, prices: pd.DataFrame) -> None:
    if not isinstance(weights, pd.DataFrame):
        raise TypeError("generate_weights must return a DataFrame")
    unknown = weights.columns.difference(prices.columns)
    if len(unknown):
        raise ValueError(f"weights reference unknown instruments: {list(unknown)[:5]}")
    future = weights.index.difference(prices.index)
    if len(future):
        raise ValueError(
            f"weights contain dates outside the price calendar (first: {future[0]})"
        )


def decision_targets(
    weights: pd.DataFrame,
    prices: pd.DataFrame,
    max_weight: float,
    max_leverage: float,
    allow_short: bool,
    eligible: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """The rows a strategy emitted, sanitized exactly as `sanitize_weights`
    would sanitize them, but not forward-filled: each row is one rebalance
    instruction. A NaN inside an emitted row carries that name's previous
    instruction, as it does in the legacy model."""
    _check_frame(weights, prices)
    w = weights[~weights.index.duplicated(keep="last")].sort_index()
    w = w.reindex(columns=prices.columns).astype(float)
    if eligible is not None:
        ok = eligible.reindex(index=w.index, columns=prices.columns).fillna(False).astype(bool)
        w = w.where(ok, 0.0)
    w = w.ffill().fillna(0.0)
    if not allow_short:
        w = w.clip(lower=0.0)
    w = w.clip(lower=-max_weight, upper=max_weight)
    w = w.where(prices.reindex(index=w.index).notna(), 0.0)
    gross = w.abs().sum(axis=1)
    scale = np.where(gross > max_leverage, max_leverage / gross.replace(0, np.nan), 1.0)
    return w.mul(pd.Series(scale, index=w.index).fillna(1.0), axis=0)


def simulate(
    targets: pd.DataFrame,
    prices: pd.DataFrame,
    execution: ExecutionModel,
    max_leverage: float = 1.0,
    keep_weights: bool = True,
    start: pd.Timestamp | None = None,
) -> BacktestResult:
    """Run decision rows `targets` through the v3 execution model.

    Row by row: (1) the holdings set at the previous close earn this row's
    return, cash earns `rf`, and a held name whose price has ended is exited at
    its last price (less `delist_haircut`); (2) holdings drift with prices;
    (3) the latest decision emitted on an *earlier* row is filled for every name
    that actually traded on this row, and the fill is charged. Holdings filled
    at this close earn from the next row on.

    `start` (optional) begins the simulation at that row, flat; used by the
    random-selection null to replay only the scored window."""
    idx = prices.index if start is None else prices.index[prices.index >= start]
    active = targets.columns[(targets.abs() > 0).any(axis=0).to_numpy()]
    n, k = len(idx), len(active)
    zeros = pd.Series(0.0, index=idx)
    rf = (execution.rf.reindex(idx).fillna(0.0).to_numpy(dtype=float)
          if execution.rf is not None else np.zeros(n))
    if k == 0:
        net = pd.Series(rf, index=idx)
        return BacktestResult(returns=net, gross_returns=net.copy(), equity=(1 + net).cumprod(),
                              weights=pd.DataFrame(index=idx), turnover=zeros, costs=zeros.copy(),
                              delisted=zeros.copy(), targets=targets)

    px = prices.loc[idx, active]
    alive = px.notna().to_numpy()
    rets = px.pct_change(fill_method=None).to_numpy(dtype=float, copy=True)
    rets[0] = 0.0
    if execution.traded is not None:
        traded = execution.traded.reindex(index=idx, columns=active).fillna(False).to_numpy(bool) & alive
    else:
        traded = alive
    costs = (execution.costs or CostModel()).prepare(idx, active)
    haircut = float(execution.delist_haircut)

    tgt = targets.reindex(columns=active).fillna(0.0)
    tgt = tgt.loc[tgt.index.isin(idx)]
    dec_pos = idx.get_indexer(tgt.index)
    dec_rows = {int(p): i for i, p in enumerate(dec_pos)}
    tvals = tgt.to_numpy(dtype=float)
    if start is not None:
        # the instruction in force when the window opens, emitted before it
        prior = targets.loc[targets.index < idx[0]]
        if len(prior):
            dec_rows.setdefault(-1, len(tvals))
            tvals = np.vstack([tvals, prior.iloc[-1].reindex(active).fillna(0.0).to_numpy()])

    h = np.zeros(k)
    pending = np.zeros(k, dtype=bool)
    ptarget = np.zeros(k)
    held = np.zeros((n, k), dtype=np.float32) if keep_weights else None
    gross = np.zeros(n)
    cost = np.zeros(n)
    turn = np.zeros(n)
    delisted = np.zeros(n)
    if -1 in dec_rows:
        ptarget[:] = tvals[dec_rows[-1]]
        pending[:] = True

    for s in range(n):
        if keep_weights:
            held[s] = h
        cash = 1.0 - h.sum()
        port = cash * rf[s]
        if h.any():
            r = np.where(np.isnan(rets[s]), 0.0, rets[s])
            dead = (h != 0.0) & ~alive[s]
            contrib = h * r
            if dead.any():
                contrib[dead] = -haircut * h[dead]
            port += contrib.sum()
            grown = h * (1.0 + r)
            if dead.any():
                # the series ended: the position is sold at its last price (less
                # the stress haircut), and that sale is charged like any other
                exits = np.flatnonzero(dead)
                proceeds = h[exits] * (1.0 - haircut) / (1.0 + port)
                delisted[s] = h[exits].sum()
                grown[exits] = 0.0
                cost[s] += costs.trade_cost(s, exits, -proceeds)
                turn[s] += proceeds.sum()
            h = grown / (1.0 + port)
        gross[s] = port

        # A decision emitted on row s-1 (or earlier, still unfilled) becomes
        # tradeable at this close.
        d = dec_rows.get(s - 1)
        if d is not None:
            ptarget[:] = tvals[d]
            pending[:] = True
        fill = pending & traded[s]
        if fill.any():
            cols = np.flatnonzero(fill)
            delta = ptarget[cols] - h[cols]
            new = h.copy()
            new[cols] = ptarget[cols]
            over = new.sum() - max_leverage
            buys = cols[delta > 0]
            if over > 1e-12 and len(buys):
                # sells still waiting on a closed market: buy only what fits,
                # and leave the rest of those orders pending
                room = max(0.0, delta[delta > 0].sum() - over) / delta[delta > 0].sum()
                new[buys] = h[buys] + (ptarget[buys] - h[buys]) * room
            delta = new[cols] - h[cols]
            cost[s] += costs.trade_cost(s, cols, delta)
            turn[s] += np.abs(delta).sum()
            h = new
            done = np.abs(ptarget[cols] - h[cols]) <= 1e-12
            pending[cols[done]] = False

    net = pd.Series(gross - cost, index=idx)
    return BacktestResult(
        returns=net,
        gross_returns=pd.Series(gross, index=idx),
        equity=(1.0 + net).cumprod(),
        weights=(pd.DataFrame(held, index=idx, columns=active) if keep_weights
                 else pd.DataFrame(index=idx)),
        turnover=pd.Series(turn, index=idx),
        costs=pd.Series(cost, index=idx),
        delisted=pd.Series(delisted, index=idx),
        targets=targets,
    )


def run_backtest(
    weights: pd.DataFrame,
    prices: pd.DataFrame,
    cost_bps: float = 10.0,
    slippage_bps: float = 5.0,
    max_weight: float = 0.25,
    max_leverage: float = 1.0,
    allow_short: bool = False,
    eligible: pd.DataFrame | None = None,
    execution: ExecutionModel | None = None,
) -> BacktestResult:
    if execution is not None:
        targets = decision_targets(weights, prices, max_weight, max_leverage, allow_short, eligible)
        if execution.costs is None:
            execution = replace(execution, costs=CostModel(flat_bps=cost_bps + slippage_bps))
        return simulate(targets, prices, execution, max_leverage)
    w = sanitize_weights(weights, prices, max_weight, max_leverage, allow_short, eligible)
    # Execution lag: positions held during day t's return were decided at t-1.
    w_eff = w.shift(1).fillna(0.0)
    rets = prices.pct_change(fill_method=None).fillna(0.0)
    gross = (w_eff * rets).sum(axis=1)
    turnover = w_eff.diff().abs().sum(axis=1).fillna(0.0)
    costs = turnover * (cost_bps + slippage_bps) / 1e4
    net = gross - costs
    equity = (1.0 + net).cumprod()
    return BacktestResult(
        returns=net, gross_returns=gross, equity=equity,
        weights=w_eff, turnover=turnover, costs=costs,
    )
