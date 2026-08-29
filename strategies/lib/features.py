"""Causal cross-sectional features from daily OHLCV panels.

Every function takes wide frames (dates x instruments) and returns a frame of
the same shape whose row `t` is computable from data at or before `t`. None of
them centre, scale or rank along the time axis using future rows, which is the
usual way a feature set leaks.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

TRADING_DAYS = 252


# ---------------------------------------------------------------------------
# Return- and volatility-shaped features
# ---------------------------------------------------------------------------

def trailing_return(prices: pd.DataFrame, lookback: int, skip: int = 0) -> pd.DataFrame:
    """Return over `lookback` days ending `skip` days ago.

    `skip` exists because the most recent month carries reversal rather than
    continuation; it is the standard skip-month when set to 21."""
    end = prices.shift(skip)
    return end / end.shift(lookback) - 1.0


def realized_vol(prices: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Annualized close-to-close volatility over a trailing window."""
    rets = prices.pct_change(fill_method=None)
    return rets.rolling(window, min_periods=max(5, window // 2)).std() * np.sqrt(TRADING_DAYS)


def parkinson_vol(high: pd.DataFrame, low: pd.DataFrame, window: int = 21) -> pd.DataFrame:
    """Parkinson's high-low range estimator, annualized.

    Uses the day's range rather than its close-to-close move, so it extracts
    several times more information per observation than `realized_vol` — which
    is the whole reason the high/low panels are worth passing to a strategy."""
    with np.errstate(divide="ignore", invalid="ignore"):
        logs = np.log(high / low) ** 2
    var = logs.rolling(window, min_periods=max(5, window // 2)).mean() / (4.0 * np.log(2.0))
    return np.sqrt(var * TRADING_DAYS)


def garman_klass_vol(
    open_: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, close: pd.DataFrame,
    window: int = 21,
) -> pd.DataFrame:
    """Garman-Klass range estimator, annualized. Adds the open-close move to
    Parkinson's range term."""
    with np.errstate(divide="ignore", invalid="ignore"):
        hl = 0.5 * np.log(high / low) ** 2
        co = (2.0 * np.log(2.0) - 1.0) * np.log(close / open_) ** 2
    var = (hl - co).rolling(window, min_periods=max(5, window // 2)).mean()
    return np.sqrt(var.clip(lower=0.0) * TRADING_DAYS)


# ---------------------------------------------------------------------------
# Liquidity- and volume-shaped features
# ---------------------------------------------------------------------------

def amihud_illiquidity(
    prices: pd.DataFrame, dollar_volume: pd.DataFrame, window: int = 21
) -> pd.DataFrame:
    """Amihud's ILLIQ: mean of |daily return| / dollar volume traded.

    Price impact per dollar traded. Needs only daily prices and volumes, which
    is exactly why it is reachable here when most microstructure measures are
    not. Returned in log form because the raw ratio spans several orders of
    magnitude across a global universe."""
    rets = prices.pct_change(fill_method=None).abs()
    dv = dollar_volume.where(dollar_volume > 0)
    ratio = rets / dv
    illiq = ratio.rolling(window, min_periods=max(5, window // 2)).mean()
    return np.log(illiq.where(illiq > 0))


def volume_shock(volume: pd.DataFrame, window: int = 63) -> pd.DataFrame:
    """Log of today's volume against its trailing median.

    The median, not the mean, because volume is heavy-tailed and one earnings
    day would otherwise set the baseline for a quarter."""
    base = volume.rolling(window, min_periods=max(10, window // 3)).median()
    ratio = volume / base.where(base > 0)
    return np.log(ratio.where(ratio > 0))


def dollar_volume_rank(dollar_volume: pd.DataFrame, window: int = 63) -> pd.DataFrame:
    """Cross-sectional rank of trailing average dollar volume, in [0, 1].

    A size/liquidity control: this universe is survivorship-selected large caps,
    so any liquidity claim needs the size axis held somewhere."""
    avg = dollar_volume.rolling(window, min_periods=max(10, window // 3)).mean()
    return xs_rank(avg)


# ---------------------------------------------------------------------------
# Cross-sectional normalization
# ---------------------------------------------------------------------------

def xs_zscore(frame: pd.DataFrame, min_names: int = 10) -> pd.DataFrame:
    """Z-score each row across instruments. Rows with too few observations are
    blanked rather than scored against a handful of names."""
    mean = frame.mean(axis=1)
    std = frame.std(axis=1, ddof=0)
    z = frame.sub(mean, axis=0).div(std.where(std > 0), axis=0)
    return z.where(frame.notna().sum(axis=1) >= min_names)


def xs_rank(frame: pd.DataFrame, min_names: int = 10) -> pd.DataFrame:
    """Rank each row across instruments, scaled to [0, 1]. Robust to the
    fat tails that make raw z-scores of return features unstable."""
    ranked = frame.rank(axis=1, pct=True)
    return ranked.where(frame.notna().sum(axis=1) >= min_names)


def winsorize(frame: pd.DataFrame, limit: float = 3.0) -> pd.DataFrame:
    """Clip each row to +/- `limit` cross-sectional standard deviations."""
    mean = frame.mean(axis=1)
    std = frame.std(axis=1, ddof=0)
    lo = mean - limit * std
    hi = mean + limit * std
    return frame.clip(lower=lo, upper=hi, axis=0)


# ---------------------------------------------------------------------------
# Market structure
# ---------------------------------------------------------------------------

def market_residual_return(
    prices: pd.DataFrame, window: int = 252, horizon: int = 5
) -> pd.DataFrame:
    """`horizon`-day return with the equal-weighted market's move removed at a
    rolling beta. The residual-reversion family works on this rather than on
    raw returns, because raw short-horizon reversal is mostly a market move."""
    rets = prices.pct_change(fill_method=None)
    market = rets.mean(axis=1)
    min_p = max(60, window // 4)
    cov = rets.rolling(window, min_periods=min_p).cov(market)
    var = market.rolling(window, min_periods=min_p).var()
    beta = cov.div(var.where(var > 0), axis=0)
    resid = rets.sub(beta.mul(market, axis=0))
    return resid.rolling(horizon, min_periods=horizon).sum()


def seasonal_same_month_return(prices: pd.DataFrame, years: int = 20) -> pd.DataFrame:
    """Average return in the *same calendar month* over the past `years`, the
    Heston-Sadka seasonality signal. Strictly backward-looking: the value on a
    date averages only same-month windows that ended before it."""
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    out = pd.DataFrame(np.nan, index=monthly.index, columns=monthly.columns)
    for i, ts in enumerate(monthly.index):
        past = mret.iloc[:i]                      # strictly before this month
        same = past[past.index.month == ts.month]
        if len(same) >= 5:
            out.iloc[i] = same.tail(years).mean()
    # Publish on the month-end date, then hold: the engine forward-fills anyway,
    # and reindexing here keeps the frame on the price calendar.
    return out.reindex(prices.index, method="ffill")


def turn_of_month(index: pd.DatetimeIndex, before: int = 1, after: int = 3) -> pd.Series:
    """Boolean series: is this date within the turn-of-month window?

    True for the last `before` trading days of a month and the first `after` of
    the next, computed from the trading calendar rather than from calendar days.
    """
    frame = pd.Series(index.to_numpy(), index=index)
    period = index.to_period("M")
    pos_in_month = frame.groupby(period).cumcount()
    from_end = frame.groupby(period).cumcount(ascending=False)
    return ((from_end < before) | (pos_in_month < after)).reindex(index)


# ---------------------------------------------------------------------------
# Score -> long-only weights
# ---------------------------------------------------------------------------

def top_n_weights(
    score: pd.Series, n: int, floor: float = 0.25, max_weight: float = 0.25
) -> pd.Series:
    """Long-only weights over the `n` highest scores, proportional to score
    magnitude above a fixed floor.

    The floor is a constant, deliberately: anchoring it to the weakest held
    name (`score - score[held].min()`) rescales every weight whenever
    membership changes, an artifact this repo spent four trials tracing
    (`experiments/learnings.md`, the fixed-anchor entries). Weights are capped
    and renormalized so the engine's own cap never has to bind."""
    valid = score.dropna()
    if valid.empty:
        return pd.Series(dtype=float)
    held = valid.nlargest(min(n, len(valid)))
    spread = held.max() - held.min()
    mag = (held - held.min()) / spread + floor if spread > 0 else pd.Series(1.0, index=held.index)
    w = mag / mag.sum()
    for _ in range(8):                     # cap, redistribute, repeat to a fixed point
        if w.max() <= max_weight + 1e-12:
            break
        w = w.clip(upper=max_weight)
        w = w / w.sum()
    return w
