"""Extra candidate legs for the union-of-tails books (`portfolio-learning`).

WHY A NEW FILE. `strategies/lib/signal_blend.py` holds the four legs that trials
#67-#72 were measured against and may not be edited (`CLAUDE.md`: a promoted
candidate keeps importing it). The legs below are new inputs, so they live here
and the existing four keep their exact recorded meaning.

------------------------------------------------------------------------------
`standardized_unexplained_volume` — and the bug it exists to fix
------------------------------------------------------------------------------
`research/SUMMARY.md` #62 proposes standardized unexplained volume as a union
leg, and the 2026-09-01 session screened it to this recipe:

    "log volume on a constant plus |positive| and |negative| returns as separate
     regressors over 21 days, residual sum standardized, minimum 15 valid
     observations"

**Read literally that recipe is identically zero.** An OLS fit that includes an
intercept has residual sum exactly zero on the sample it was fitted to, so
regressing over one 21-day window and then summing that same window's residuals
returns 0 for every name on every date. Measured directly: over 416 name-dates
the largest |sum of residuals| is 1.6e-11 and the mean is 2.4e-13, i.e. the
accumulated rounding error of the linear solve. Ranking that rounding error
cross-sectionally is what produced the screen's IC of +0.0101 at 21 days, and it
is also why the object measured as "the most orthogonal signal ever measured
against these legs" (|rho| 0.002-0.107): **a signal with no content is orthogonal
to everything by construction.**

The literature's construction (Garfinkel-Sokobin; Bali-Peng-Shen-Tang) uses two
*disjoint* windows, which is what makes the residual sum informative:

  - an **estimation** window (here t-63 .. t-11, 53 trading days) that fits
    `log volume ~ 1 + |return|_+ + |return|_-`;
  - an **event** window (here t-10 .. t, 11 trading days) whose residuals are
    taken against the estimation window's coefficients and summed;
  - the sum standardized by the estimation residual standard deviation times
    sqrt(event length), so it is a t-like quantity.

That is the version implemented below. It is causal (every window ends at or
before the row it is published on), fitted per name rather than cross-
sectionally, and estimates nothing that is carried across dates.

IMPLEMENTATION NOTE. The rolling OLS is solved from rolling cross-moments rather
than by looping over (name, date): the protocol calls `generate_weights` about
seven times per trial and a Python loop over 140 names x 14k rows is far outside
`CLAUDE.md`'s ~60s budget. The normal equations are 3x3 and are solved in closed
form, so the result is deterministic — the causality check compares holdings at
1e-6 and any non-determinism reads as a peek.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

EST_WINDOW = 53          # estimation window length, ending EVENT_WINDOW days back
EVENT_WINDOW = 11        # event window length, ending at the row
MIN_EST = 40             # usable estimation observations required
MIN_EVENT = 8            # usable event observations required
SIGMA_FLOOR = 1e-3       # log-volume units; guards a degenerate estimation fit


def _roll(frame: pd.DataFrame, window: int, minp: int) -> pd.DataFrame:
    return frame.rolling(window, min_periods=minp).sum()


def standardized_unexplained_volume(
    volume: pd.DataFrame,
    prices: pd.DataFrame,
    est_window: int = EST_WINDOW,
    event_window: int = EVENT_WINDOW,
    min_est: int = MIN_EST,
    min_event: int = MIN_EVENT,
) -> pd.DataFrame:
    """Standardized unexplained volume, two-window construction.

    Positive values mean the last `event_window` days traded more volume than the
    name's own recent return-magnitude/volume relation predicts.

    `volume` is a share count and is NOT forward-filled by the loader, so foreign
    holidays are NaN; those rows are dropped from both windows by the masked
    rolling sums rather than imputed.
    """
    logv = np.log(volume.where(volume > 0))
    ret = prices.pct_change(fill_method=None)
    pos = ret.clip(lower=0.0)
    neg = (-ret).clip(lower=0.0)

    # A row is usable only where every regressor and the response are finite.
    ok = logv.notna() & pos.notna() & neg.notna()
    y = logv.where(ok)
    p = pos.where(ok)
    n = neg.where(ok)
    one = ok.astype(float)

    # --- estimation window: rolling cross-moments, shifted off the event window
    lag = event_window
    S = {}
    for key, frame in (
        ("1", one), ("p", p), ("n", n), ("y", y),
        ("pp", p * p), ("nn", n * n), ("pn", p * n),
        ("py", p * y), ("ny", n * y), ("yy", y * y),
    ):
        S[key] = _roll(frame, est_window, min_est).shift(lag)

    cnt = S["1"].to_numpy()
    with np.errstate(invalid="ignore", divide="ignore"):
        # Normal equations X'X b = X'y for X = [1, p, n].
        a11, a12, a13 = cnt, S["p"].to_numpy(), S["n"].to_numpy()
        a22, a23, a33 = S["pp"].to_numpy(), S["pn"].to_numpy(), S["nn"].to_numpy()
        b1, b2, b3 = S["y"].to_numpy(), S["py"].to_numpy(), S["ny"].to_numpy()

        # Cofactor expansion of the symmetric 3x3.
        c11 = a22 * a33 - a23 * a23
        c12 = a13 * a23 - a12 * a33
        c13 = a12 * a23 - a13 * a22
        det = a11 * c11 + a12 * c12 + a13 * c13

        c22 = a11 * a33 - a13 * a13
        c23 = a13 * a12 - a11 * a23
        c33 = a11 * a22 - a12 * a12

        beta0 = (c11 * b1 + c12 * b2 + c13 * b3) / det
        beta1 = (c12 * b1 + c22 * b2 + c23 * b3) / det
        beta2 = (c13 * b1 + c23 * b2 + c33 * b3) / det

        # Estimation residual variance: (y'y - b'X'y) / (n - 3).
        rss = S["yy"].to_numpy() - (beta0 * b1 + beta1 * b2 + beta2 * b3)
        dof = cnt - 3.0
        sigma = np.sqrt(np.maximum(rss, 0.0) / np.where(dof > 0, dof, np.nan))

    # --- event window: residual sum against those coefficients
    e1 = _roll(one, event_window, min_event).to_numpy()
    ep = _roll(p, event_window, min_event).to_numpy()
    en = _roll(n, event_window, min_event).to_numpy()
    ey = _roll(y, event_window, min_event).to_numpy()

    with np.errstate(invalid="ignore", divide="ignore"):
        resid_sum = ey - (beta0 * e1 + beta1 * ep + beta2 * en)
        suv = resid_sum / (sigma * np.sqrt(np.where(e1 > 0, e1, np.nan)))

    # A near-perfect estimation fit drives `sigma` to zero and the ratio to
    # infinity. That is a data pathology (a stretch of near-constant reported
    # volume), not a large volume surprise, and because the union books select
    # on within-leg ORDERING a single such cell would take a slot outright.
    # `SIGMA_FLOOR` is a units floor on log-volume dispersion, not a tuned
    # threshold: residual noise below 0.1% of log volume is not real data.
    bad = (
        ~np.isfinite(suv)
        | ~np.isfinite(det)
        | (np.abs(det) < 1e-12)
        | (cnt < min_est)
        | (e1 < min_event)
        | ~(sigma > SIGMA_FLOOR)
    )
    suv = np.where(bad, np.nan, suv)
    return pd.DataFrame(suv, index=prices.index, columns=prices.columns)


# ---------------------------------------------------------------------------
# The fixed-quota union book, factored out so a designed pair is bit-identical
# ---------------------------------------------------------------------------
CORE_N = 20
BAND_N = 30
WARMUP = 60


def fixed_quota_union(
    prices: pd.DataFrame,
    legs: dict[str, pd.DataFrame],
    core_n: int = CORE_N,
    band_n: int = BAND_N,
    warmup: int = WARMUP,
    min_names: int = 20,
) -> pd.DataFrame:
    """Trial #71's book, generalised to any number of legs.

    Each leg is z-scored within its own cross-section, the frame is restricted to
    the instruments *every* leg can score (so no name enters on a partial set of
    legs), and the book holds the union of each leg's own top `core_n / n_legs`
    names under a hysteresis band of each leg's top `band_n / n_legs`. Equal
    weight, monthly.

    The per-leg quota is fixed by name count and never varies by date, which is
    what makes the book invariant to any strictly monotone per-leg transform:
    only the WITHIN-leg ordering is ever read, and every monotone transform
    agrees on that. `learnings.md` (2026-09-01) verified that invariance by
    rebuilding #71 under percentile ranks and under exp(z) — bit-identical on
    every date. Reads only rows at or before each rebalance date.
    """
    from strategies.lib import walkforward as W

    names = list(legs)
    per_core = core_n // len(names)
    per_band = band_n // len(names)

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=warmup):
        zs: dict[str, pd.Series] = {}
        common: pd.Index | None = None
        usable = True
        for nm in names:
            sub = legs[nm].loc[:dt]
            if sub.empty:
                usable = False
                break
            row = sub.iloc[-1].dropna()
            if len(row) < min_names:
                usable = False
                break
            sd = row.std(ddof=0)
            if not sd > 0:
                usable = False
                break
            z = (row - row.mean()) / sd
            zs[nm] = z
            common = z.index if common is None else common.intersection(z.index)

        if not usable or common is None or len(common) < band_n:
            continue

        core: set[str] = set()
        band: set[str] = set()
        for nm in names:
            ordered = zs[nm].reindex(common).sort_values(ascending=False)
            core |= set(ordered.index[:per_core])
            band |= set(ordered.index[:per_band])

        held = (held & band) | core
        picks = sorted(held)
        rows[dt] = pd.Series(1.0 / len(picks), index=picks)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
