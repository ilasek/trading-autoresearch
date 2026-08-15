"""Add a path-continuity ("frog-in-the-pan") axis to the best challenger's
composite score.

`mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07, maxDD
-30.3%, DSR 0.9326) is the strongest challenger in the repo. Its composite
score is built entirely from *return magnitude* (z-scored 12-1 and 6-1
returns), and every escalation along that same axis is now explored
(rank-weighting -> magnitude-weighting -> multi-horizon -> dampening
refuted), while the alternative price-based signal tried last session
(52-week-high proximity) was refuted for turnover reasons.

This candidate keeps the entire mechanism fixed — same 12-1/6-1 horizons,
same hold-25/enter-15 buffer, same magnitude weighting, same daily-reacting
vol-spike trim — and only adds a third z-score to the composite along a
genuinely different information axis: how *smoothly* each name's formation
return was accumulated. Da, Gurun & Warachka (2014) find that momentum
formed from many small same-direction moves (continuous information, which
investors under-react to) persists, while momentum formed from a few large
jumps (discrete information, which gets attention and is priced quickly)
does not.

Information discreteness is ID = sign(PRET) * (%neg - %pos) over the
formation window; low ID means continuous information. The score added here
is the negation, so higher = smoother, and it enters the composite with the
same unit weight as each existing momentum z-score (no tuning knob).

Unlike the refuted low-vol constructions, this does not tilt capital away
from high-magnitude names on a risk axis — a smooth high-return name scores
high on *both* axes; it only breaks ties among names of similar momentum in
favour of the ones whose trend was persistent rather than gap-driven.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_zscore_continuity_daily_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Adding a formation-path continuity z-score (negated information "
        "discreteness: sign(return) * (%up days - %down days) over the 12-1 "
        "window) as a third equal-weight component of the composite score, "
        "with the hold-25/enter-15 buffer, magnitude weighting and daily "
        "vol-spike trim all held fixed, raises validation Sharpe above the "
        "best challenger's 1.07, net of 15 bps costs, because momentum built "
        "from continuous information persists longer than jump-driven "
        "momentum."
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
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _continuity(hist: pd.DataFrame, lookback: int) -> pd.Series:
    """Negated information discreteness over the formation window.

    Uses exactly the same window as `_momentum(hist, lookback)`: from the
    price `lookback + SKIP` days before the last observation up to the
    price `SKIP` days before it.
    """
    window = hist.iloc[-(lookback + SKIP) - 1 : -SKIP]
    rets = window.pct_change().iloc[1:]
    n_valid = rets.notna().sum()
    pct_pos = (rets > 0).sum() / n_valid.replace(0, np.nan)
    pct_neg = (rets < 0).sum() / n_valid.replace(0, np.nan)
    pret = window.iloc[-1] / window.iloc[0] - 1
    return (np.sign(pret) * (pct_pos - pct_neg)).dropna()


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
        cont = _continuity(hist, LOOKBACK_LONG)
        common = mom_long.index.intersection(mom_short.index).intersection(cont.index)
        if len(common) < CORE_N:
            continue

        composite = (
            _zscore(mom_long[common])
            + _zscore(mom_short[common])
            + _zscore(cont[common])
        )
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
