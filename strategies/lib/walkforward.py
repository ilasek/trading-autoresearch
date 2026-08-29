"""Walk-forward fitting for learned cross-sectional strategies.

The single hard requirement a learned strategy has here is that the model
predicting at date `d` was fitted only on outcomes already realized by `d`.
Fitting once over the whole visible window and applying the fit backwards is
the classic way to produce a spectacular backtest, and `protocol.causality_check`
is built to catch it: it recomputes weights on truncated histories and fails any
strategy whose holdings move when future rows are hidden.

This module does the bookkeeping once so each candidate does not re-derive it:

- rebalance dates are month-ends of the *visible* frame, matching the
  convention every candidate in this repo already uses;
- a training row for prediction date `d` is a past rebalance date `t` whose
  forward-return target had already been observed by `d` (`t + horizon <= d`),
  which is both the causality rule and the embargo;
- fits are deterministic: seed your estimator and keep it single-threaded, or
  floating-point non-determinism will read as a peek at 1e-6.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import features as F


def rebalance_dates(prices: pd.DataFrame, warmup: int = 0) -> pd.DatetimeIndex:
    """Month-end rows of the visible frame, after `warmup` rows of history.

    `groupby(Grouper("ME")).tail(1)` is the repo's standing convention and it
    matters for causality: on a truncated history the only date it shifts is the
    frame's very last row, which the causality check's tail buffer already
    excludes from comparison. A rule that picked, say, the 15th of each month
    would shift a date well inside the compared window and read as a peek.
    """
    dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    return dates[warmup:] if warmup else dates


def forward_return(prices: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Return from each date to `horizon` rows later. Contains the future by
    construction — only ever use it through `walk_forward_scores`, which
    releases a row into training only once it has been realized."""
    return prices.shift(-horizon) / prices - 1.0


def ridge_fit_predict(alpha: float = 10.0):
    """Deterministic ridge learner. Closed-form, single-threaded, no seed to
    forget — the sane default for a first learned candidate on a universe this
    small, where anything heavier is mostly fitting noise."""
    from sklearn.linear_model import Ridge

    def _fit_predict(x_train: np.ndarray, y_train: np.ndarray, x_pred: np.ndarray):
        model = Ridge(alpha=alpha, fit_intercept=True, solver="cholesky")
        model.fit(x_train, y_train)
        return model.predict(x_pred)

    return _fit_predict


def walk_forward_scores(
    feature_panels: dict[str, pd.DataFrame],
    target: pd.DataFrame,
    dates: pd.DatetimeIndex,
    horizon: int,
    fit_predict,
    min_train_rows: int = 500,
) -> pd.DataFrame:
    """Predicted scores (dates x instruments), fitted walk-forward.

    `feature_panels` and `target` are wide frames on the price calendar;
    `target` is a forward-looking quantity (see `forward_return`) and is read
    only for dates whose outcome is already known at the prediction date.

    Returns a sparse frame: one row per date in `dates` that had enough history
    to fit, columns the instruments, values the model's predicted score. Dates
    before the model can be fitted are simply absent.
    """
    names = sorted(feature_panels)
    index = target.index
    pos = {d: i for i, d in enumerate(index)}

    # Feature/target cubes sampled at the rebalance dates only: monthly rows are
    # what the model is asked to predict, and using every day would train it on
    # overlapping targets it would then be scored on.
    usable = [d for d in dates if d in pos]
    x_cube = np.stack(
        [feature_panels[n].reindex(usable).to_numpy(dtype=float) for n in names], axis=-1
    )                                                    # (n_dates, n_inst, n_feat)
    y_mat = target.reindex(usable).to_numpy(dtype=float)  # (n_dates, n_inst)
    date_pos = np.array([pos[d] for d in usable])

    out: dict[pd.Timestamp, pd.Series] = {}
    for i, d in enumerate(usable):
        x_pred = x_cube[i]
        pred_ok = np.isfinite(x_pred).all(axis=1)
        if pred_ok.sum() < 10:
            continue

        # Rows whose forward return was already realized at `d`. This is the
        # causality rule and the embargo in one line.
        train_mask = date_pos + horizon <= date_pos[i]
        if not train_mask.any():
            continue
        xt = x_cube[train_mask].reshape(-1, len(names))
        yt = y_mat[train_mask].reshape(-1)
        rows_ok = np.isfinite(xt).all(axis=1) & np.isfinite(yt)
        if rows_ok.sum() < min_train_rows:
            continue

        # Refit at every rebalance. `fit_predict` fits and predicts in one
        # call, so there is no stale-model path to get wrong; a model too
        # expensive to refit monthly should be given fewer dates, not a cached
        # fit whose training window nobody can see.
        preds = fit_predict(xt[rows_ok], yt[rows_ok], x_pred[pred_ok])
        out[d] = pd.Series(preds, index=target.columns[pred_ok])

    if not out:
        return pd.DataFrame(columns=target.columns, dtype=float)
    return pd.DataFrame(out).T.reindex(columns=target.columns)


def rank_target(prices: pd.DataFrame, horizon: int) -> pd.DataFrame:
    """Cross-sectional rank of the forward return, centred on zero.

    Ranking the target rather than regressing raw forward returns is the usual
    defence against a handful of extreme moves dominating the fit — and this
    universe's return distribution is exactly that heavy (see
    `research/notes/2026-08-26-skewness-and-concentration-of-stock-returns.md`).
    """
    return F.xs_rank(forward_return(prices, horizon)) - 0.5
