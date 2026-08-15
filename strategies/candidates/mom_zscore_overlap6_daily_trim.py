"""Extend the holding period of the overlapping-tranche construction from
three months to six.

`mom_zscore_overlap_daily_trim` (trial #33) established overlapping formation
tranches as the strongest mechanism in the repo — val Sharpe 1.08, maxDD
-28.5%, turnover 4.2x, all best-ever. Trial #34 then decomposed *why*: the
turnover benefit is temporal (it survives any basket size), while the
drawdown benefit comes from the wider effective book that overlapping
formation dates produce. Both halves of that mechanism point the same way if
K is raised further.

This is the one follow-up needed to establish the lever's direction rather
than leave a newly-found mechanism uncharacterised at an arbitrary K. It is
a genuine tension, not a sweep, because the two effects pull against each
other:

- With K = 6, only a sixth of the book can turn over per month and the
  effective book widens further, extending both of the benefits measured at
  K = 3.
- But five sixths of capital then sits on formation signals up to six months
  stale. Cross-sectional momentum on a 12-1 formation window has limited
  persistence; the classic literature holds it for 3-6 months precisely
  because the edge decays inside that range. If decay dominates, Sharpe
  should fall clearly at K = 6.

Whichever way it lands settles whether the next session should push this
lever further or treat K = 3 as near the optimum. Everything else — signal,
buffer, magnitude weighting, daily vol-spike trim — is identical to trial #33.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_daily_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Extending the overlapping-tranche holding period from three months "
        "to six (portfolio = average of the six most recent monthly target- "
        "weight vectors, 1/6 of capital reformed each month), with signal, "
        "buffer, weighting and daily vol-spike trim otherwise identical to "
        "trial #33, raises validation Sharpe above that version's 1.08 and "
        "cuts turnover below 4.2x, net of 15 bps costs, because the turnover "
        "and effective-breadth benefits of overlapping formation dates "
        "outweigh the decay of a 12-1 momentum signal held six months."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 6

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
