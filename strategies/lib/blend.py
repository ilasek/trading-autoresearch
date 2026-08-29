"""Combine several strategies' weight frames into one book.

This is the sanctioned route from a scouted family lead to the champion seat: a
`challenge` candidate blends the incumbent with a decorrelated family lead and
competes under the unchanged promotion rule. Read
`experiments/leaderboard.json` for each family's lead and its correlation to the
champion before proposing one — `experiments/learnings.md` has priced naive
dilution repeatedly, and a blend that is not argued from decorrelation is a
known loser.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent


def strategy_weights(path: str | Path, prices: pd.DataFrame, aux: dict | None = None):
    """Weights from another strategy file, called under its own contract.

    `path` is relative to the repo root. The module is loaded fresh each call so
    that no state leaks between legs of a blend."""
    path = ROOT / path
    spec = importlib.util.spec_from_file_location(f"_blend_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import inspect

    params = [
        p for p in inspect.signature(mod.generate_weights).parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    if len(params) >= 2:
        return mod.generate_weights(prices, {k: v.reindex(prices.index) for k, v in (aux or {}).items()})
    return mod.generate_weights(prices)


def blend(frames: list[pd.DataFrame], weights: list[float]) -> pd.DataFrame:
    """Capital-weighted combination of weight frames.

    Each leg is forward-filled onto the union of all legs' rebalance dates
    first, so a monthly leg and a weekly leg combine at the cadence of the
    faster one rather than the slower one silently dropping rows. Fixed ratios
    only: every vol- or risk-based reweighting between sleeves tried in this
    repo has lost, and the reason is on record (unequal component Sharpe)."""
    if len(frames) != len(weights):
        raise ValueError("frames and weights must be the same length")
    total = float(sum(weights))
    if total <= 0:
        raise ValueError("blend weights must sum to a positive number")
    index = frames[0].index
    for f in frames[1:]:
        index = index.union(f.index)
    out = None
    for frame, w in zip(frames, weights):
        aligned = frame.reindex(index).ffill().fillna(0.0) * (w / total)
        out = aligned if out is None else out.add(aligned, fill_value=0.0)
    return out
