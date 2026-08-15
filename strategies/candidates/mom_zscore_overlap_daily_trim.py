"""Overlapping formation tranches on top of the best challenger.

Every candidate in this repo's momentum line reforms 100% of capital on a
single monthly date, so the whole portfolio is exposed to the luck of *which*
month-end it happens to rank on. The classic Jegadeesh-Titman overlapping-
portfolio construction removes that dependence: 1/K of capital is reformed
each month and held for K months, so the live portfolio is at all times the
average of the K most recent formations.

With K = 3 this is exactly equivalent to averaging the three most recent
monthly target-weight vectors, which is how it is implemented here. Nothing
else changes: same 12-1/6-1 composite z-score, same hold-25/enter-15 buffer
(one shared buffer state, so the underlying selection process is untouched),
same magnitude weighting, same daily-reacting vol-spike trim.

Two reasons to expect this to help rather than merely smooth:

1. Turnover. Every real gain in this repo has come from spending less on
   trading the same signal (buffering: 5.8x -> 4.4x; widened breadth: 7.0x
   -> 6.5x at equal Sharpe). Overlapping tranches cut turnover structurally
   — only a third of the book can turn over in any month — without changing
   what the signal says.
2. Formation-date variance. Averaging three independent formation dates
   lowers the variance of the realised weight vector around the signal's
   own intent, which is the kind of improvement the deflated-Sharpe bar
   rewards (higher Sharpe through lower noise, not through more risk).

The known risk is that averaging three ranked snapshots dilutes the
magnitude weighting that drove this line's gains — a real possibility, and
the point of the test. This is temporal dilution of the *same* signal,
which is distinct from the already-refuted capital dilution into a weaker
second leg.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap_daily_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Holding the best challenger's basket as three overlapping monthly "
        "tranches (portfolio = average of the three most recent monthly "
        "target-weight vectors, i.e. a 3-month holding period with 1/3 of "
        "capital reformed each month), with signal, buffer, weighting and "
        "daily vol-spike trim otherwise identical, raises validation Sharpe "
        "above 1.07 and cuts turnover below 7.0x, net of 15 bps costs, "
        "because it removes single-formation-date luck and structurally "
        "limits how much of the book can turn over per month."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 3

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


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    recent_targets = []  # up to N_TRANCHES most recent monthly target vectors
    base_periods = []  # (start_idx_pos, end_idx_pos_exclusive, blended norm)

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
        target = raw / raw.sum()

        recent_targets.append(target)
        if len(recent_targets) > N_TRANCHES:
            recent_targets.pop(0)

        # Live book = average of the most recent formations (each sums to 1,
        # so the average does too).
        blended = pd.concat(recent_targets, axis=1).fillna(0.0).mean(axis=1)
        norm = blended / blended.sum()
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
