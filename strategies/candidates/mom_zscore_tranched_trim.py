"""Rebalance-timing diversification: four weekly-staggered tranches instead of
one month-end formation date.

Every candidate this repo has ever run forms its basket on the last trading
day of the month and holds until the next month-end. That single arbitrary
formation date injects "rebalance timing luck" (Hoffstein, Faber & Braun 2019):
a portfolio formed on the last day of March and one formed on the second
Friday of April hold the same signal but can differ by several percent of
annual return purely from where their formation dates fell relative to
market swings. On a monthly-rebalanced momentum strategy the dispersion
across formation dates is large, and the reported result is one draw from it.

This candidate is the first attempt in the repo to change *rebalance
mechanics* rather than the signal or an overlay. The signal is left exactly
as in `mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07,
maxDD -30.3% — still the strongest challenger): composite z-score of 252d and
126d returns skipping the most recent month, hold-25/enter-15 buffer,
magnitude weighting, 25% cap, and the daily-reacting basket-own vol-spike
exposure trim.

The portfolio is instead split into four equal sub-portfolios. Sub-portfolio
k rebalances on every fourth weekly grid date (offset k), so each tranche
still holds its names for roughly a month and each keeps its own independent
buffer state; the held portfolio is their average, and only a quarter of
capital reforms in any given week. Turnover per name is therefore unchanged
in character — this is not a faster-rebalancing strategy — but the formation
date is averaged out instead of chosen.

Why this is worth a trial after three consecutive signal-side refutations
(#31 52-week-high, #32/#33 residual momentum, #34 information discreteness):
it adds no new information and cannot dilute the return-magnitude signal that
those trials showed is the actual driver — the same score, buffer and weights
are used, only four times on staggered dates. If timing luck is a material
part of the 1.07, averaging it away should also cut drawdown, since a single
formation date is what concentrates exposure to any one bad entry window.

Falsifiable: if formation-date luck is immaterial at monthly frequency on
this universe, validation Sharpe and maxDD both land within noise of the
single-tranche version's 1.07 / -30.3%, and the extra machinery is not worth
its turnover.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_tranched_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Splitting the buffered magnitude-weighted momentum basket into four "
        "weekly-staggered tranches, each rebalanced every fourth week with "
        "its own buffer state and averaged into one portfolio, raises "
        "validation Sharpe above the 1.07 of the identical single-date "
        "month-end version and reduces its -30.3% maxDD, net of 15 bps costs, "
        "because averaging over formation dates removes rebalance timing "
        "luck rather than changing the signal."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 4

VOL_SHORT = 21
VOL_LONG = 252
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def _tranche_weights(hist: pd.DataFrame, held: set) -> tuple[pd.Series, set] | None:
    """Re-form one tranche at `hist`'s last date. Returns (weights, new held)."""
    if len(hist) < LOOKBACK_LONG + SKIP + 1:
        return None
    mom_long = _momentum(hist, LOOKBACK_LONG)
    mom_short = _momentum(hist, LOOKBACK_SHORT)
    common = mom_long.index.intersection(mom_short.index)
    if len(common) < CORE_N:
        return None

    composite = _zscore(mom_long[common]) + _zscore(mom_short[common])
    ranked = composite.sort_values(ascending=False)
    core = set(ranked.index[:CORE_N])
    band = set(ranked.index[:BAND_N])
    held = (held & band) | core

    c_held = composite[list(held)]
    raw = c_held - c_held.min() + FLOOR
    norm = raw / raw.sum()
    if (norm > MAX_WEIGHT).any():
        norm = norm.clip(upper=MAX_WEIGHT)
        norm = norm / norm.sum()
    return norm, held


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    grid = prices.groupby(pd.Grouper(freq="W")).tail(1).index
    all_dates = prices.index

    rows = {}
    held = [set() for _ in range(N_TRANCHES)]
    tranche_w: list[pd.Series | None] = [None] * N_TRANCHES
    base_periods = []  # (start_pos, end_pos, combined weights)

    for i, dt in enumerate(grid):
        k = i % N_TRANCHES
        out = _tranche_weights(prices.loc[:dt], held[k])
        if out is not None:
            tranche_w[k], held[k] = out

        live = [w for w in tranche_w if w is not None]
        if not live:
            continue

        combined = pd.concat(live, axis=1).fillna(0.0).sum(axis=1) / len(live)
        combined = combined[combined > 0]

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[combined.index] = combined
        rows[dt] = w_full

        start_pos = all_dates.get_loc(dt)
        next_dt = grid[i + 1] if i + 1 < len(grid) else None
        end_pos = all_dates.get_loc(next_dt) if next_dt is not None else len(all_dates)
        base_periods.append((start_pos, end_pos, combined))

    if not base_periods:
        return pd.DataFrame.from_dict(rows, orient="index")

    last_scale = 1.0
    for start_pos, end_pos, norm in base_periods:
        names = list(norm.index)
        sub = prices.iloc[:end_pos][names]
        avail = sub.dropna(axis=1, how="any").columns
        if len(avail) == 0:
            continue
        rets = sub[avail].pct_change()
        basket_ret = rets.mean(axis=1)
        vol_short = basket_ret.rolling(VOL_SHORT).std(ddof=0)
        vol_long = basket_ret.rolling(VOL_LONG).std(ddof=0)
        ratio = vol_short / vol_long
        scale_series = (ratio > SPIKE_RATIO).map({True: TRIM_SCALE, False: 1.0})
        scale_series = scale_series.where(vol_long > 0, 1.0)

        day_scales = scale_series.iloc[start_pos:end_pos]
        for dt2, scale in day_scales.items():
            if pd.isna(scale):
                scale = 1.0
            if dt2 in rows:
                rows[dt2] = rows[dt2] * scale
                last_scale = scale
                continue
            if scale != last_scale:
                w_full = pd.Series(0.0, index=prices.columns)
                w_full[norm.index] = norm * scale
                rows[dt2] = w_full
                last_scale = scale

    return pd.DataFrame.from_dict(rows, orient="index")
