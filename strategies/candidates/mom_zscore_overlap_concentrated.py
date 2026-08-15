"""Restore per-tranche conviction now that overlapping tranches have created
breadth headroom.

`mom_zscore_overlap_daily_trim` (trial #33) is the repo's strongest result:
val Sharpe 1.08, maxDD -28.5%, turnover 4.2x. But it bought its drawdown and
turnover improvements partly by widening the *effective* book — average
positions rose from 15 to 25.5, because three overlapping 15-name tranches
rarely agree on the same 15 names.

The repo's clearest positive finding before this was that tilting more
capital toward the strongest-momentum names raises Sharpe (equal-weight ->
rank-weight -> magnitude-weight: 0.90 -> 0.93 -> 0.98 -> 1.03), and the only
thing that stopped that escalation was validation maxDD widening toward the
-45% gate (-30.2% -> -32.4% -> -36.0%). Overlap has now pushed maxDD back
down to -28.5%, i.e. it has bought back all the risk budget that escalation
had spent — a new rationale for revisiting concentration, rather than a
blind re-sweep of a parameter.

This candidate halves the per-tranche basket (core 15 -> 8, band 25 -> 14)
and changes nothing else. The choice is not arbitrary: three overlapping
8-name tranches should produce an effective book of roughly 15-20 names,
i.e. approximately the book-level breadth of the pre-overlap best challenger
`mom_zscore_narrow_daily_volspike_trim`. The test is therefore whether
per-tranche conviction and temporal diversification are independent additive
levers — the same question the vol-trim work answered affirmatively for
concentration and the trim.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap_concentrated",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Halving the per-tranche basket (hold-14/enter-8 instead of "
        "hold-25/enter-15) inside the three-tranche overlapping construction, "
        "with signal, weighting and daily vol-spike trim unchanged, raises "
        "validation Sharpe above the overlap version's 1.08 while keeping "
        "maxDD better than -33%, net of 15 bps costs, because overlap "
        "restores at book level the diversification that per-tranche "
        "concentration gives up."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 8
BAND_N = 14
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
    recent_targets = []
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
        target = raw / raw.sum()

        recent_targets.append(target)
        if len(recent_targets) > N_TRANCHES:
            recent_targets.pop(0)

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
