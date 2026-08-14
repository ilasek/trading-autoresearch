"""Continuous daily vol-targeting of the basket's exposure, replacing the
binary vol-spike trim of `mom_zscore_narrow_daily_volspike_trim` (trial #28).

Background. Trial #28 is the repo's strongest challenger (val Sharpe 1.07,
maxDD -30.3%, DSR 0.9326). Its de-risking overlay is a *step function*: the
basket's own trailing 21d realized vol is compared to its 252d realized vol,
and if the ratio exceeds 1.6 the whole book is scaled to 0.6x, otherwise 1.0x.
Two things were established about it: the cadence must be daily (a monthly
check was a no-op, trial #25), and redirecting the freed capital into TLT/GLD
instead of cash does not help (trial #29). Both of those are closed.

What is *not* closed is the functional form. A binary step wastes information
twice over: it does nothing at all for a 1.5x vol expansion, and it does no
more for a 3.0x expansion than for a 1.6x one. The volatility-managed-portfolio
literature (Moreira & Muir 2017) scales exposure *proportionally* to inverse
realized variance/vol rather than by a threshold, and reports that most of the
benefit comes from the proportional response, not from a regime call.

This candidate changes exactly one thing versus trial #28: the exposure scalar
becomes `min(1, sigma_252 / sigma_21)` instead of `1.6-threshold -> 0.6`.
Everything else — universe, composite 6-1/12-1 z-score signal, hold-25/enter-15
buffer, magnitude weighting, 0.25 cap, the vol estimator itself (equal-weighted
daily returns of the currently held names), and the daily evaluation cadence —
is held byte-for-byte identical.

Note the design deliberately introduces **no new constants**: the continuous
rule passes almost exactly through the binary rule's own operating point (at a
ratio of 1.6 it produces 0.625x, versus the binary 0.6x), so this is a clean
functional-form test rather than a re-tuned threshold. The cap at 1.0 is forced
by the engine's `max_leverage = 1.0`; unlike the literature we cannot lever *up*
in calm regimes, so only the de-risking half of vol-targeting is available here.

The cost side is the real risk and is the point of measuring it: a proportional
scalar moves a little every single day, so the whole book gets nudged daily at
15 bps per side, whereas the step function only trades on threshold crossings.
If the continuous version loses, turnover is the expected culprit, and that is
itself a useful result about proportional overlays in a 15 bps world.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_continuous_voltarget",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Replacing the binary vol-spike exposure trim (21d/252d realized-vol "
        "ratio > 1.6 -> 0.6x) with a continuous proportional scalar "
        "min(1, sigma_252/sigma_21) on the identical narrow hold-25/enter-15 "
        "buffered composite-z-score basket raises validation Sharpe above the "
        "binary version's 1.07, net of 15 bps costs, because a proportional "
        "response uses the magnitude of the vol expansion instead of "
        "discarding it at a threshold."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

VOL_SHORT = 21
VOL_LONG = 252


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
    base_periods = []  # (start_idx_pos, end_idx_pos_exclusive, norm)

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
        # Proportional de-risking only: cap at 1.0 (no leverage available).
        scale_series = (vol_long / vol_short).clip(upper=1.0)
        scale_series = scale_series.where(vol_long > 0, 1.0)

        day_scales = scale_series.iloc[start_pos:end_pos]
        for dt2, scale in day_scales.items():
            if pd.isna(scale):
                scale = 1.0
            w_full = pd.Series(0.0, index=prices.columns)
            w_full[norm.index] = norm * scale
            rows[dt2] = w_full

    return pd.DataFrame.from_dict(rows, orient="index")
