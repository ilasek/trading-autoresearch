"""A parametric portfolio policy: the first book here that ranks nothing.

WHY THIS FILE EXISTS. Every strategy this repo has ever run does the same two
things — compute a cross-sectional score, then hold a band of its top names.
`learnings.md`'s house-construction table (2026-09-10) makes that explicit, and
the one node it refuses to give a single value to is exactly the band, because
the right band is where that score's marginal rank slices go flat and that is a
property of the score. `research/SUMMARY.md` #98 supplies the alternative shape:

    w[i,t] = 1/N_t + (1/N_t) * theta' xhat[i,t]          (Brandt-Santa-Clara-Valkanov)
    w      = max(0, w) / sum(max(0, w))                  (long-only, as the source gives it)

There is no ranking and no band. Every name in the pool gets a weight that is
affine in its standardized characteristics; the long-only clip is what decides
membership, so **breadth is chosen by the policy's own utility rather than
inherited from another book's machinery**. Parameter count grows with the number
of characteristics, not with the number of assets: three characteristics over
~68 names is a three-parameter model, which is as close to `CLAUDE.md`'s "prefer
few features and a penalised linear model first" as a learned construction gets.

THE NODES, all pre-committed in the journal before anything was scored
(`## Pre-registration — 2026-09-11`):

  characteristics  the champion's four-horizon momentum z-score; region-relative
                   Amihud ILLIQ (the seated `liquidity-volume` lead's score);
                   same-minus-other-calendar-month seasonal (the seated
                   `seasonality-calendar` lead's score). Three scores the lab
                   already owns, each cross-sectionally z-scored.
  pool             the `common` intersection of the three eligibilities — the
                   house default. ~68 of 140 names.
  grid             house default: last TRADING day of each month, warmup 6.
  utility          quadratic, gamma = 5, fixed before anything was fitted.
  horizon          21 days.
  estimation       walk-forward, refit every rebalance, on rows whose forward
                   target was already realized; 60 month-ends minimum.

WHY QUADRATIC UTILITY, AND WHY IT IS NOT A SHORTCUT. Under `U(r) = r - (g/2)r^2`
the average utility of the UNCONSTRAINED policy is quadratic in theta, so the fit
is a closed-form 3x3 linear solve:

    r_p(t) = rbar(t) + theta' g(t),   g(t) = (1/N_t) sum_i xhat[i,t] R[i,t->t+h]
    theta* = (gamma E[g g'])^-1 (E[g] - gamma E[g rbar])

No optimizer, therefore no iteration counts, no restarts and no floating-point
non-determinism — which matters because `causality_check` compares holdings at
1e-6 and reads non-determinism as a peek. The long-only clip is applied AFTER the
fit, exactly as the source writes it.

THE TWO RIDERS #98 CALLS MANDATORY, BOTH HONOURED.
(a) The source fits theta once over its whole sample; applied here as written it
    would fail the causality check outright. theta is refit walk-forward, and the
    training set at date `d` is the rebalance dates `t` with `t + 21 <= d` in
    trading-day positions — the same rule `strategies/lib/walkforward.py` uses,
    which is the causality rule and the embargo in one line. That set does not
    depend on anything after `d`, so holdings are bit-identical on a truncated
    history.
(b) The source's low turnover rests on a constant theta and must not be
    inherited. Measured here rather than assumed: **13.2x annual L1 on train**,
    ~2.0%/yr of drag at 15 bps a side. It is stated in the hypothesis and in the
    journal, not discovered afterwards.

THE FREE SCREEN (train, forward 21d, book excess over its own scoreable pool
WEIGHTED BY THE BOOK'S OWN WEIGHTS per 2026-09-10, one common 334-date sample,
churn and the book's trailing-volatility percentile beside every arm):

    arm                                        names   excess %/yr     t    volpct   churn
    PPP, walk-forward theta (3 chars)           41.4      +10.70     +6.83   0.581   13.2x
    band on the SAME theta'x, magnitude wt      41.2       +7.46     +7.24   0.547   10.6x
    PPP, hand-set theta=(1,0,0)  [#98's ctl]    61.3       +1.92     +1.42   0.545    3.6x
    PPP, theta=(0,0,0)  [= equal weight]        68.2        0.00     +0.65   0.510    0.1x
    [ctl] PPP on a PLACEBO characteristic       66.2       -0.32     -0.74   0.509    7.6x

#98's own decision rule is what licenses the trial: it says to hand-set theta
first and, if the hand-set version carries the result, not to spend one. It does
not — the paired difference is +8.78%/yr at t = +5.21. The placebo arm reads
-0.32%/yr, so the harness has no free lunch in it. And the volpct column is the
warning: at 0.581 against the equal-weight pool's 0.510 the policy buys its mean
partly with variance, which is precisely the half an excess screen cannot see
(2026-09-10, the lesson from `lv_illiq_stocks_only`).

PRE-REGISTERED: validation **0.95, range 0.75-1.15** — deliberately well below
what +10.70%/yr would imply, because the over-prediction rule is the default
again since 2026-09-06 and because 13.2x churn costs ~2.0%/yr against the seated
`liquidity-volume` lead's 0.14%/yr. **No drawdown call is made**: the
risk-contribution statistic is blind to everything that is not cross-sectional
and contemporaneous and its K=6 scatter is +-1.2pp, so a call here would be
unfalsifiable rather than small (2026-09-09).

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sl_ppp_walkforward",
    "family": "statistical-learning",
    "track": "scout",
    "hypothesis": (
        "A parametric portfolio policy — weights affine in three standardized "
        "characteristics (the champion's four-horizon momentum, region-relative Amihud "
        "ILLIQ, and the same-minus-other-month seasonal), `w = 1/N + (1/N) theta'xhat` "
        "clipped long-only, with theta refit walk-forward at every month-end by maximizing "
        "average quadratic utility (gamma = 5) of the unconstrained policy's realized "
        "return — scores near 0.95 on validation (range 0.75-1.15), because it is the first "
        "construction in this repo that ranks nothing and holds no band, and on a free train "
        "screen at one common 334-date sample it carries +10.70%/yr of own-weight book excess "
        "over its scoreable pool (t = +6.83) against +7.46%/yr for rank-and-band on the "
        "identical theta'x composite at matched breadth (41.4 against 41.2 names), +1.92%/yr "
        "for #98's own hand-set theta=(1,0,0) control (t = +1.42, so the control does not "
        "carry the result and the estimation is what is being tested), and -0.32%/yr for the "
        "same policy driven by a placebo characteristic that reads no market data. The point "
        "estimate sits far below what that screen implies because the standing "
        "over-prediction rule is the default again since 2026-09-06, and because the policy's "
        "measured 13.2x annual train churn costs ~2.0%/yr against the seated liquidity lead's "
        "0.14%/yr, and because the book's trailing-volatility percentile of 0.581 against the "
        "equal-weight pool's 0.510 says it buys part of its mean with variance an excess "
        "screen structurally cannot price. Above ~1.0 says the policy shape beats the "
        "rank-and-band house default outside `price-trend` and the band node has a "
        "utility-chosen alternative; below 0.75 says the shape does not survive the variance "
        "its tilt buys, and the screen is the over-prediction rule arriving on a construction "
        "rather than on a score."
    ),
}

ILLIQ_WINDOW = 63      # one quarter, as the seated `liquidity-volume` lead
HORIZON = 21           # the policy's target horizon, in trading days
GAMMA = 5.0            # quadratic-utility risk aversion, fixed before any fit
RIDGE = 1e-6           # numerical floor on the 3x3 solve, not a tuned shrinkage
MIN_FIT_DATES = 60     # month-ends of realized targets before theta is fitted at all
MIN_POOL = 20          # a cross-section below this is not standardized against
WARMUP = 6
MIN_REGION = 4         # a region below this cannot supply a peer mean
MAX_WEIGHT = 0.25      # the engine's own cap; applied here so it never has to bind

CHARS = ("mom", "illiq_rr", "seasonal")


def _region_relative(frame: pd.DataFrame) -> pd.DataFrame:
    """Each name's score minus the mean over its own region, dropping names whose
    region has fewer than `MIN_REGION` instruments scoreable on that date.

    `groups.REGION_OF` is static instrument metadata from `data/universe.yaml` —
    no dates, no prices, nothing estimated from returns. Same helper as the
    seated `liquidity-volume` lead.
    """
    out = pd.DataFrame(np.nan, index=frame.index, columns=frame.columns)
    labels = pd.Series({c: G.REGION_OF.get(c) for c in frame.columns})
    for _, members in labels.groupby(labels).groups.items():
        sub = frame[list(members)]
        n = sub.notna().sum(axis=1)
        out[list(members)] = sub.sub(sub.mean(axis=1), axis=0).where(n >= MIN_REGION, axis=0)
    return out


def _characteristics(prices: pd.DataFrame, aux: dict) -> dict[str, pd.DataFrame]:
    """The three scores, each cross-sectionally standardized. All causal."""
    mom = sum(
        F.xs_zscore(F.trailing_return(prices, lb, skip=21)) for lb in (252, 189, 126, 63)
    ) / 4.0
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)
    # `signal_blend.seasonal_score`, not `features.seasonal_same_month_return`:
    # the latter still carries the MonthEnd/MonthBegin alignment bug trials
    # #59/#60 measured and may not be edited.
    seasonal = SB.seasonal_score(prices).reindex(prices.index).ffill()
    return {
        "mom": F.xs_zscore(mom),
        "illiq_rr": F.xs_zscore(_region_relative(illiq)),
        "seasonal": F.xs_zscore(seasonal),
    }


def _solve(g: np.ndarray, rbar: np.ndarray) -> np.ndarray:
    """theta* = (gamma E[g g'])^-1 (E[g] - gamma E[g rbar]).

    The stationary point of average quadratic utility of `rbar + theta'g`. Closed
    form, so the fit is deterministic to machine precision.
    """
    k = g.shape[1]
    a = GAMMA * (g.T @ g) / len(g) + RIDGE * np.eye(k)
    b = g.mean(axis=0) - GAMMA * (g * rbar[:, None]).mean(axis=0)
    return np.linalg.solve(a, b)


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    chars = _characteristics(prices, aux)
    forward = prices.shift(-HORIZON) / prices - 1.0
    pos = {d: i for i, d in enumerate(prices.index)}

    # One pass over the grid: the pool, the standardized characteristic matrix,
    # and (where the forward target exists in the visible frame) the
    # characteristic-managed portfolio returns `g` that the fit consumes.
    grid: list[pd.Timestamp] = []
    xmat: dict[pd.Timestamp, pd.DataFrame] = {}
    g_rows: dict[pd.Timestamp, np.ndarray] = {}
    rbars: dict[pd.Timestamp, float] = {}

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        cols = []
        for key in CHARS:
            hist = chars[key].loc[:dt]
            if hist.empty:
                break
            cols.append(hist.iloc[-1].rename(key))
        if len(cols) < len(CHARS):
            continue
        x = pd.concat(cols, axis=1).dropna()
        if len(x) < MIN_POOL:
            continue
        grid.append(dt)
        xmat[dt] = x

        fwd = forward.loc[dt].reindex(x.index) if dt in forward.index else None
        if fwd is not None and fwd.notna().sum() >= MIN_POOL:
            ok = fwd.notna()
            xd, rd = x[ok], fwd[ok]
            n = len(xd)
            g_rows[dt] = (xd.to_numpy(dtype=float) * rd.to_numpy()[:, None]).sum(axis=0) / n
            rbars[dt] = float(rd.mean())

    if not grid:
        return pd.DataFrame(columns=prices.columns, dtype=float)

    fit_dates = [d for d in grid if d in g_rows]
    fit_pos = np.array([pos[d] for d in fit_dates])
    g_all = np.array([g_rows[d] for d in fit_dates])
    rbar_all = np.array([rbars[d] for d in fit_dates])

    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in grid:
        # Rows whose forward target was already realized at `dt`. Independent of
        # anything after `dt`, so truncating the history cannot move a holding.
        usable = fit_pos + HORIZON <= pos[dt]
        if usable.sum() < MIN_FIT_DATES:
            continue
        theta = _solve(g_all[usable], rbar_all[usable])

        x = xmat[dt]
        n = len(x)
        w = 1.0 / n + (x.to_numpy(dtype=float) @ theta) / n
        w = np.clip(w, 0.0, None)
        total = w.sum()
        if total <= 0:
            continue
        held = pd.Series(w / total, index=x.index)
        held = held[held > 0]

        # The engine caps at 25% anyway; capping here keeps the emitted vector and
        # the traded vector the same object, so the diagnostics read what trades.
        # Water-filling: pin the binding names at the cap and rescale the rest to
        # fill what is left, repeating until nothing binds.
        for _ in range(len(held)):
            over = held > MAX_WEIGHT + 1e-12
            if not over.any():
                break
            free = held[~over]
            room = 1.0 - MAX_WEIGHT * int(over.sum())
            if room <= 0 or free.sum() <= 0:
                held = pd.Series(1.0 / len(held), index=held.index)
                break
            held[over] = MAX_WEIGHT
            held[~over] = free * room / free.sum()
        rows[dt] = held

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
