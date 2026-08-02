"""Minimal vectorized daily backtest engine.

Design guarantees (do not weaken):
- Next-day execution: weights decided at date t earn returns from t+1 (shift inside
  the engine), so same-day lookahead is impossible by construction.
- Costs charged on turnover (|Δweight|) at cost_bps + slippage_bps per side.
- Long-only by default, per-position cap, gross leverage cap (scaled down, never up).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class BacktestResult:
    returns: pd.Series          # net daily portfolio returns
    gross_returns: pd.Series    # before costs
    equity: pd.Series           # cumulative net growth of $1
    weights: pd.DataFrame       # effective (sanitized, lagged) weights actually held
    turnover: pd.Series         # daily sum |Δw|
    costs: pd.Series            # daily cost drag

    @property
    def ann_turnover(self) -> float:
        return float(self.turnover.mean() * 252)

    def avg_positions(self) -> float:
        return float((self.weights.abs() > 1e-6).sum(axis=1).mean())


def sanitize_weights(
    weights: pd.DataFrame,
    prices: pd.DataFrame,
    max_weight: float,
    max_leverage: float,
    allow_short: bool,
) -> pd.DataFrame:
    """Validate and normalize raw strategy weights onto the price calendar."""
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


def run_backtest(
    weights: pd.DataFrame,
    prices: pd.DataFrame,
    cost_bps: float = 10.0,
    slippage_bps: float = 5.0,
    max_weight: float = 0.25,
    max_leverage: float = 1.0,
    allow_short: bool = False,
) -> BacktestResult:
    w = sanitize_weights(weights, prices, max_weight, max_leverage, allow_short)
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
