"""Overlapping formation tranches (K = 6) on the buffered composite-z-score
basket — re-run on `main` to establish the archived result honestly.

PROVENANCE. This construction was developed on 2026-08-15 in a session whose
work never reached `main` (see the `## Protocol issue — 2026-08-16` journal
entry). That session reported it as the strongest result in the repo's
history on Sharpe, turnover and DSR at once — val Sharpe 1.11, maxDD -29.1%,
turnover 3.0x — but scored it against a 35-trial bar derived from a
trials.jsonl that `main` has never seen. The protocol entry is explicit that
no such number may be treated as established, and that any idea worth
pursuing from those sessions must be re-run through `run_experiment.py`
against `main`'s own trial history. That is the sole purpose of this file:
the code below is byte-identical to the archived candidate
(`archive/nightly-2026-08-15:strategies/candidates/mom_zscore_overlap6_daily_trim.py`),
so this trial measures the same strategy against `main`'s honest bar.

THE MECHANISM. Instead of reforming the whole book at each monthly
rebalance, hold six overlapping tranches: the live portfolio is the average
of the six most recent monthly target-weight vectors, so only ~1/6 of
capital is recommitted each month. Signal (12-1 and 6-1 composite z-score),
buffer (hold-25 / enter-15), magnitude weighting and the daily vol-spike
trim are all untouched — only *when* capital commits to the signal changes.
This is temporal dilution into the same signal, categorically unlike the
capital dilution into a weaker second leg that `learnings.md` refutes.

WHAT WOULD FALSIFY IT. If the archived 1.11 was an artifact of that
session's environment rather than the mechanism, validation Sharpe here
lands near the min-shift basket it was built on (`mom_zscore_narrow_daily_
volspike_trim`, trial #28, val Sharpe 1.066) rather than clearly above it,
and turnover fails to collapse from that basket's 7.3x toward 3x.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_daily_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Holding six overlapping monthly formation tranches (portfolio = "
        "average of the six most recent monthly target-weight vectors, 1/6 "
        "of capital reformed each month), with signal, buffer, magnitude "
        "weighting and daily vol-spike trim otherwise identical to trial "
        "#28, raises validation Sharpe above that basket's 1.066 and cuts "
        "its 7.3x turnover below 4x, net of 15 bps costs, because the "
        "turnover and effective-breadth benefits of overlapping formation "
        "dates outweigh the decay of a 12-1 momentum signal held six months."
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
