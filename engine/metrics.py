"""Performance metrics, including deflated Sharpe (Bailey & López de Prado)."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def ann_return(returns: pd.Series) -> float:
    if len(returns) == 0:
        return 0.0
    growth = float((1 + returns).prod())
    if growth <= 0:
        return -1.0
    return growth ** (TRADING_DAYS / len(returns)) - 1


def ann_vol(returns: pd.Series) -> float:
    return float(returns.std(ddof=1) * math.sqrt(TRADING_DAYS)) if len(returns) > 2 else 0.0


def sharpe(returns: pd.Series) -> float:
    vol = ann_vol(returns)
    if vol == 0:
        return 0.0
    return float(returns.mean() * TRADING_DAYS / vol)


def sortino(returns: pd.Series) -> float:
    downside = returns[returns < 0]
    if len(downside) < 2:
        return 0.0
    dvol = float(downside.std(ddof=1) * math.sqrt(TRADING_DAYS))
    if dvol == 0:
        return 0.0
    return float(returns.mean() * TRADING_DAYS / dvol)


def max_drawdown(returns: pd.Series) -> float:
    """Most negative peak-to-trough drawdown of the equity curve (<= 0)."""
    equity = (1 + returns).cumprod()
    peak = equity.cummax()
    return float((equity / peak - 1).min()) if len(equity) else 0.0


def _norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _norm_ppf(p: float) -> float:
    # Acklam's rational approximation; plenty accurate for our use.
    if not 0 < p < 1:
        raise ValueError("p must be in (0,1)")
    a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
         1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
    b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
         6.680131188771972e01, -1.328068155288572e01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
         -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
         3.754408661907416e00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def probabilistic_sharpe(returns: pd.Series, sr_benchmark_daily: float) -> float:
    """PSR: probability the true (daily) Sharpe exceeds the benchmark, accounting
    for sample length, skew and kurtosis (Bailey & López de Prado 2012)."""
    n = len(returns)
    if n < 30:
        return 0.0
    sr = returns.mean() / returns.std(ddof=1) if returns.std(ddof=1) > 0 else 0.0
    skew = float(returns.skew())
    kurt = float(returns.kurtosis()) + 3.0  # pandas gives excess kurtosis
    denom = math.sqrt(max(1e-12, 1 - skew * sr + (kurt - 1) / 4 * sr**2))
    z = (sr - sr_benchmark_daily) * math.sqrt(n - 1) / denom
    return _norm_cdf(z)


def expected_max_sharpe(var_trial_sharpes: float, n_trials: float) -> float:
    """E[max Sharpe] under the null, for `n_trials` *independent* trials drawn
    from a distribution with variance `var_trial_sharpes` (Bailey & López de
    Prado 2014, eq. 3). Grows like sqrt(2 ln N) — slowly, but without bound."""
    n = max(2.0, float(n_trials))
    var = max(float(var_trial_sharpes), 1e-8)
    gamma = 0.5772156649015329
    return math.sqrt(var) * (
        (1 - gamma) * _norm_ppf(1 - 1.0 / n) + gamma * _norm_ppf(1 - 1.0 / (n * math.e))
    )


def deflated_sharpe(
    returns: pd.Series,
    trial_sharpes_daily: list[float],
    n_effective: float | None = None,
) -> float:
    """DSR: PSR against the expected max Sharpe among all trials ever attempted.

    trial_sharpes_daily: daily-frequency Sharpe ratios of every recorded trial
    (including this one). More trials -> higher benchmark -> harder to pass.

    n_effective: the number of *independent* trials the recorded ones are worth.
    Bailey & López de Prado's E[max SR] assumes independent draws; a search that
    tests many near-duplicate variants of one idea does not get that many
    independent shots at a high Sharpe, and scoring it at the raw trial count
    over-deflates. Pass an effective count (see `protocol.effective_n_trials`)
    to correct for that. Defaults to the raw count, which is the conservative
    (harder-to-pass) choice. The dispersion term still uses every recorded
    trial: a wide search genuinely makes an extreme maximum more likely, and
    only the count is affected by redundancy.
    """
    n_trials = len(trial_sharpes_daily) if n_effective is None else n_effective
    var = (
        float(np.var(trial_sharpes_daily, ddof=1))
        if len(trial_sharpes_daily) > 2
        else 0.25 / TRADING_DAYS
    )
    return probabilistic_sharpe(returns, expected_max_sharpe(var, n_trials))


def sharpe_diff_se(
    returns_a: pd.Series,
    returns_b: pd.Series,
    min_overlap: int = 30,
) -> tuple[float, float]:
    """SE of the *annualized* Sharpe difference between two strategies, and the
    correlation of their daily returns. Memmel's (2003) correction to the
    Jobson-Korkie (1981) test.

    Both series are aligned on the intersection of their dates, so the estimate
    is *paired*: the two strategies see the same days and their common market
    exposure cancels. That is what makes it useful here — a single strategy's
    own Sharpe carries a standard error several times larger than the error on
    a difference between two highly correlated ones, and the difference is the
    quantity a promotion decision actually turns on.

        Var(s_a - s_b) = (1/T) [ 2(1 - rho) + 0.5(s_a^2 + s_b^2 - 2 s_a s_b rho^2) ]

    with s_* the *daily* Sharpe ratios; the result is scaled by sqrt(252) to
    annualize. The (1 - rho) term dominates in practice, so near-identical
    constructions are resolvable to a much finer margin than distinct ones.

    Assumes i.i.d. bivariate normal returns, so under fat tails and volatility
    clustering it is liberal: treat it as a *floor* on the error bar, never as
    a significance test in its own right.

    Returns (se, rho). Degenerate comparisons — too little overlap, or either
    series flat — return (inf, nan), which makes every t-statistic zero and so
    decides nothing.
    """
    joined = pd.concat([returns_a, returns_b], axis=1, join="inner").dropna()
    n = len(joined)
    if n < min_overlap:
        return float("inf"), float("nan")

    a = joined.iloc[:, 0].to_numpy(dtype=float)
    b = joined.iloc[:, 1].to_numpy(dtype=float)
    sd_a, sd_b = a.std(ddof=1), b.std(ddof=1)
    if sd_a <= 0 or sd_b <= 0:
        return float("inf"), float("nan")

    rho = float(np.corrcoef(a, b)[0, 1])
    if not np.isfinite(rho):
        return float("inf"), float("nan")

    s_a = float(a.mean() / sd_a)  # daily Sharpe
    s_b = float(b.mean() / sd_b)
    var = (
        2.0 * (1.0 - rho)
        + 0.5 * (s_a**2 + s_b**2 - 2.0 * s_a * s_b * rho**2)
    ) / n
    var = max(var, 0.0)
    return math.sqrt(var) * math.sqrt(TRADING_DAYS), rho


def summary(returns: pd.Series) -> dict:
    return {
        "ann_return": round(ann_return(returns), 4),
        "ann_vol": round(ann_vol(returns), 4),
        "sharpe": round(sharpe(returns), 3),
        "sortino": round(sortino(returns), 3),
        "max_drawdown": round(max_drawdown(returns), 4),
        "n_days": int(len(returns)),
    }
