"""Restore the tested concentration level on top of the stable fixed anchor.

Trial #35 established two things at once. The membership-dependent anchor
(`composite - composite[held].min()`) was manufacturing turnover: removing it
cut re-sizing turnover from 4.32x to 2.30x per year and pulled maxDD to -28.2%,
the best in the repo. But it also *de-concentrated* the book — mean HHI in the
validation era fell from 0.105 to 0.073 — because the subtracted basket minimum
is usually negative (the hold-25 buffer keeps decayed names around), so the
min-shift had been acting as a hidden concentration amplifier rather than the
compressor it looked like. Those two effects cancelled almost exactly: Sharpe
1.085 vs 1.080.

This candidate keeps the stable, membership-independent anchor and restores the
concentration through a convex transform of each name's own score:

    raw = clip(composite, 0.05) ** 1.5

This is not the "escalate concentration further" move earlier learnings warn
against. The target is to *match* a concentration level the repo has already
tested and found good, using mechanics that do not drift. The exponent was
chosen by a weight-matrix diagnostic against that concentration target, not
against any performance number: over the validation era mean HHI is 0.097 at
exponent 1.5 versus the min-shift version's 0.105 (exponent 1.0 gives 0.073 and
exponent 2.0 gives 0.127, bracketing it). The same diagnostic makes the
stability argument concrete — the min-shift's HHI swings between eras (0.094
over all history versus 0.105 recently) while the power transform's ordering is
consistent, which is exactly the month-to-month drift being engineered out.

If the two levers are independent, this should hold trial #35's turnover and
drawdown gains while recovering the Sharpe that de-concentration gave back. If
Sharpe instead lands back at ~1.08 with a worse drawdown, the conclusion is that
the escalation ladder's gains were never about concentration per se but about
the specific, unstable way the min-shift produced it — which would retire the
concentration lever rather than extend it. Both outcomes are worth knowing.

Base is `mom_zscore_fixed_anchor` (trial #35, val Sharpe 1.085, maxDD -28.2%,
turnover 5.75x) with exactly one change, the exponent on the weighting
transform. Signal, horizons, hold-25/enter-15 buffer, 25% no-trade band, 0.25
cap, and the daily vol-spike trim are all unchanged.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_convex_anchor",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Weighting by the composite z-score raised to the power 1.5 off a "
        "fixed floor — restoring the concentration level of the old "
        "membership-anchored formula (validation-era HHI 0.097 vs 0.105) "
        "without its instability — raises validation Sharpe above trial #35's "
        "1.085 while keeping its 5.75x turnover and -28.2% maxDD, because "
        "concentration and anchor stability are independent levers and the "
        "repo's Sharpe gains from concentration were real."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05
EXPONENT = 1.5

NOTRADE_BAND = 0.25

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


def _apply_band(target: pd.Series, current: pd.Series) -> pd.Series:
    if current.empty:
        return target
    held_before = current.reindex(target.index).fillna(0.0)
    drift = (target - held_before).abs()
    inside = (held_before > 0) & (drift <= NOTRADE_BAND * held_before)
    out = target.where(~inside, held_before)
    total = out.sum()
    return out / total if total > 0 else target


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    base_periods = []
    current = pd.Series(dtype=float)

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

        raw = composite[list(held)].clip(lower=FLOOR) ** EXPONENT
        norm = raw / raw.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        norm = _apply_band(norm, current)
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()
        current = norm

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
        sub = prices.iloc[: end_pos][names]
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
