"""The closed-form long-only minimum-variance book, as the control that a
hand-built co-movement score would have had to beat.

TRANSCRIBED FROM TONIGHT'S PRE-REGISTRATION (`## Pre-registration — 2026-09-24`),
entry **T2**, written before any number was computed. Every constant below is
either transcribed from the seated champion or forced by the algebra; nothing
was chosen after a measurement.

WHY IT IS RUN AT ALL, GIVEN THAT ITS PARTNER WAS KILLED FOR FREE TONIGHT.
`research/SUMMARY.md` #146 proposed two objects: a hand-built market-correlation
leg (T1) and this closed form as its natural control. T1 was **not built** — the
pre-registered third orthogonality gate returned `|spearman(mc, beta-hat)| =
0.675` against a 0.50 bar, so a direct co-movement score on this universe is a
low-beta bet in costume. T2's own claim is independent of that score and is the
one thing the kill does not settle: Clarke-de Silva-Thorley derive that a
long-only *variance objective* excludes most of the universe **by itself**, with
systematic risk deciding who is in the book and idiosyncratic risk deciding only
how much. This repo has refuted a volatility-*level* tilt (`lowvol_equity_tilt`,
0.685) and an inverse-vol sleeve (0.35), but it has never run the actual
closed-form composition, and without it the `range-variance` family has no
parameter-free floor to price anything against.

THE CONSTRUCTION, AND IT HAS NO FREE PARAMETERS TO SWEEP. Single-factor risk
model on the equal-weight universe return. For each name, `beta_i` and residual
variance `s2_i = var(r_i) - beta_i^2 * var(r_m)`. The long-only minimum-variance
solution is

    w_i  proportional to  (1/s2_i) * (1 - beta_i/beta_L)   for beta_i < beta_L,
    w_i  = 0                                               otherwise,

and `beta_L` is not a knob: substituting the solution back into its own
first-order conditions gives `beta_L = (C + 1/var(r_m)) / B` with
`B = sum(beta_i/s2_i)` and `C = sum(beta_i^2/s2_i)` over the surviving long set,
so it is found by iterating to a fixed point. That is `O(n)` per pass, needs no
matrix inversion, and estimates one number per name -- which is exactly why it
passes `research/SUMMARY.md` #1's parameter-count triage where a covariance
objective does not.

THE TWO CONSTANTS THAT ARE NOT FORCED ARE TRANSCRIBED, NOT CHOSEN. The 250-day
estimation window and the 20-day lag are the seated champion's `E/Var`
constants, taken verbatim so that this book and the seated term see exactly the
same information. They are not to be swept here or later.

WHY `range-variance` AND WHY SCOUT. `program.md` names "correlation regimes"
under `range-variance` and nowhere else, and this is a variance objective. It is
a **scout** because it is aimed squarely at the variance channel, and
`research/SUMMARY.md` #142 forbids building for that channel and expecting this
repo's Sharpe gate to reward it. A scout never reaches the holdout.

WHAT WOULD FALSIFY IT, BOTH BRANCHES FIXED IN ADVANCE. A validation Sharpe at or
below the `range-variance` family lead of **0.494** says a parameter-free
variance objective does not even beat the family's existing vol-of-vol book, and
the low-risk vein on this universe is closed at the family level rather than at
the level of any one construction. Above it, the family has its first floor that
is not a hand-built score, and any future low-risk proposal must clear it.

WHAT IS NOT CLAIMED. Nothing about the mean. `research/SUMMARY.md` #147 forbids
importing the low-correlation cross-section's expected spread onto a universe of
~145 large global survivors, and the number that matters here is the *position
count* -- CdST predict the threshold sits inside the lowest-beta quintile -- at
least as much as the Sharpe.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "rv_minvar_closedform",
    "family": "range-variance",
    "track": "scout",
    "hypothesis": (
        "The Clarke-de Silva-Thorley closed-form long-only minimum-variance "
        "book — w_i proportional to (1/s2_i)(1 - beta_i/beta_L) for "
        "beta_i < beta_L and zero otherwise, under a single-factor model on "
        "the equal-weight universe return estimated over the seated term's "
        "own 250-day window lagged 20 days, with beta_L fixed by its own "
        "first-order conditions and no free parameter anywhere — reaches a "
        "validation Sharpe above the range-variance family lead of 0.494 "
        "while holding fewer than a quintile of the universe, because a "
        "long-only variance objective excludes most names by itself."
    ),
}

# transcribed from the seated champion's E/Var term, not chosen here
WINDOW = 250
LAG = 20

MAX_WEIGHT = 0.25
MIN_NAMES = 8
MAX_PASSES = 50


def _min_variance_weights(block: np.ndarray, names: list[str]) -> pd.Series:
    """Long-only minimum-variance weights under a single-factor model.

    `block` is a (window x n) array of daily simple returns, all finite. The
    market is the equal-weight mean of the same block, so nothing outside the
    visible window is used.
    """
    mkt = block.mean(axis=1)
    var_m = mkt.var(ddof=1)
    if not np.isfinite(var_m) or var_m <= 0:
        return pd.Series(dtype=float)

    centred = block - block.mean(axis=0)
    m_centred = mkt - mkt.mean()
    cov = (centred * m_centred[:, None]).sum(axis=0) / (len(block) - 1)
    beta = cov / var_m
    total_var = centred.var(axis=0, ddof=1)
    resid_var = total_var - np.square(beta) * var_m

    # a residual variance at or below zero is an estimation artifact, not an
    # arbitrage; such a name is simply not eligible.
    ok = np.isfinite(beta) & np.isfinite(resid_var) & (resid_var > 0)
    if ok.sum() < MIN_NAMES:
        return pd.Series(dtype=float)

    beta, resid_var = beta[ok], resid_var[ok]
    cols = [n for n, keep in zip(names, ok) if keep]

    # beta_L is a fixed point, not a parameter: iterate the long set until it
    # stops changing. Starting from every eligible name, the set only shrinks.
    live = np.ones(len(cols), dtype=bool)
    beta_l = np.nan
    for _ in range(MAX_PASSES):
        inv = 1.0 / resid_var[live]
        b_sum = float((beta[live] * inv).sum())
        c_sum = float((np.square(beta[live]) * inv).sum())
        if b_sum <= 0:
            return pd.Series(dtype=float)
        beta_l = (c_sum + 1.0 / var_m) / b_sum
        nxt = live & (beta < beta_l)
        if nxt.sum() < MIN_NAMES:
            break
        if np.array_equal(nxt, live):
            break
        live = nxt

    if not np.isfinite(beta_l) or live.sum() < MIN_NAMES:
        return pd.Series(dtype=float)

    raw = np.zeros(len(cols))
    raw[live] = (1.0 / resid_var[live]) * (1.0 - beta[live] / beta_l)
    raw = np.clip(raw, 0.0, None)
    if raw.sum() <= 0:
        return pd.Series(dtype=float)

    w = pd.Series(raw / raw.sum(), index=cols)
    w = w[w > 0]
    if (w > MAX_WEIGHT).any():
        w = w.clip(upper=MAX_WEIGHT)
        w = w / w.sum()
    return w


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    all_names = list(prices.columns)
    positions = {dt: i for i, dt in enumerate(prices.index)}
    ret_values = prices.pct_change(fill_method=None).to_numpy()

    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in rebalance_dates:
        end = positions[dt] - LAG + 1
        start = end - WINDOW
        if start < 1:
            continue
        block = ret_values[start:end]
        finite = np.isfinite(block).all(axis=0)
        if finite.sum() < MIN_NAMES:
            continue
        w = _min_variance_weights(
            block[:, finite], [n for n, keep in zip(all_names, finite) if keep]
        )
        if w.empty:
            continue
        full = pd.Series(0.0, index=prices.columns)
        full[w.index] = w
        rows[dt] = full

    return pd.DataFrame.from_dict(rows, orient="index")
