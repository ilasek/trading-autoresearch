"""Continuous daily volatility targeting of basket exposure, replacing the
binary vol-spike trim.

The best-documented single improvement to momentum in the literature (Barroso &
Santa-Clara 2015, "Momentum has its moments") is scaling exposure inversely to
the strategy's own recent realised volatility, rather than switching on a
threshold. This repo has one prior attempt in that family, `mom_invvol_target`
(trial #4, val Sharpe 0.71), but it is not a clean test of the mechanism: it
combined exposure targeting with inverse-*name*-volatility basket weighting (a
separately refuted mechanism that tilts capital away from the strongest names),
applied it to the plain equal-weight momentum basket, and re-evaluated only at
the monthly rebalance — a cadence later shown (trials #25 vs #27) to make a
sound vol-based overlay behave as a near no-op.

Everything learned since says the clean version deserves one test: the binary
spike trim on this exact basket, re-evaluated daily, is the only mechanism in
the repo's history to improve Sharpe and drawdown at once. A continuous scalar
uses the same daily information but responds proportionally in every vol
regime, not only above a 1.6x spike.

Versus `mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07,
maxDD -30.3%, turnover 7.3x, DSR 0.9326) exactly ONE thing changes: the
exposure scalar. Signal, buffer band, magnitude weighting, cap and monthly
selection cadence are identical.

Two deliberate design choices, both to keep this a mechanism test rather than a
tuned knob: the target is the basket's own long-run realised volatility level
(25% annualised) rather than a fitted number, so the scalar sits near 1.0 in
normal conditions and only de-risks when the basket is unusually volatile; and
the scalar is quantised to 0.05 steps so that ordinary day-to-day vol wobble
does not generate continuous re-trading. The engine forbids leverage, so the
scalar is capped at 1.0 — this is a de-risking-only version of the mechanism,
which is the strictest form of the test.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_daily_voltarget",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Scaling the buffered composite-z-score basket's exposure continuously "
        "and daily toward a 25% annualised volatility target (capped at 1.0, "
        "quantised to 0.05) raises validation Sharpe above the 1.07 of the "
        "otherwise-identical binary vol-spike-trim version, net of 15 bps "
        "costs, because proportional de-risking uses the same daily volatility "
        "information in every regime rather than only above a 1.6x spike "
        "threshold."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

VOL_WINDOW = 21
TARGET_VOL = 0.25          # annualised; the basket's own long-run realised level
MIN_SCALE = 0.3
STEP = 0.05                # quantisation of the exposure scalar


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    base_periods = []

    all_dates = prices.index
    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK_LONG + SKIP + 1:
            continue
        mom_long = _momentum(hist, LOOKBACK_LONG)
        mom_short = _momentum(hist, LOOKBACK_SHORT)
        common = mom_long.index.intersection(mom_short.index)
        if len(common) < CORE_N:
            continue

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

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full

        start_pos = all_dates.get_loc(dt)
        next_dt = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else None
        end_pos = all_dates.get_loc(next_dt) if next_dt is not None else len(all_dates)
        base_periods.append((start_pos, end_pos, norm))

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
        realised = basket_ret.rolling(VOL_WINDOW).std(ddof=0) * (252 ** 0.5)
        scale_series = (TARGET_VOL / realised).clip(upper=1.0, lower=MIN_SCALE)
        scale_series = (scale_series / STEP).round() * STEP
        scale_series = scale_series.where(realised > 0, 1.0)

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
