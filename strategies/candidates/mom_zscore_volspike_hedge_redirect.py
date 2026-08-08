"""Redirect trimmed capital into a defensive hedge sleeve instead of idling
it as cash, on top of the repo's best-yet finding.

Trials #27-28 established that a daily-reacting basket-own vol-spike trim
(21d/252d realized-vol ratio > 1.6 -> cut basket exposure to 0.6x) is a
genuinely new, additive lever: applied to either the widebreadth or the
narrower buffered z-score basket it improved validation Sharpe *and* maxDD
simultaneously versus the untrimmed basket — the first mechanism in the
repo's history to do both at once. In both trials, the 0.4x of exposure cut
during a trim was simply left uninvested (implicit cash, since the engine
is long-only with max leverage 1.0).

This candidate holds the winning narrow-basket (15/25) daily trim mechanism
completely fixed and only changes where the freed capital goes: instead of
idling as cash, it is redirected into a small fixed defensive sleeve
(half TLT, half GLD) for exactly as long as the trim is active, so gross
exposure stays near 1.0 throughout rather than dropping to 0.6 during a
spike. This tests a structurally different question from the trim itself
(when to de-risk) — whether de-risked capital is better parked in a
historically low-correlated hedge than left idle, net of 15 bps costs.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_volspike_hedge_redirect",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Redirecting the capital freed by the daily vol-spike trim "
        "(trials #27-28) into a fixed 50/50 TLT/GLD defensive sleeve, "
        "instead of leaving it as idle cash, improves validation Sharpe "
        "over the narrow-basket trimmed version "
        "(`mom_zscore_narrow_daily_volspike_trim`, val Sharpe 1.07) without "
        "materially worsening its maxDD, because bonds and gold have "
        "historically been positively-returning during the momentum "
        "basket's own vol-spike episodes, net of 15 bps costs."
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
HEDGE_ASSETS = ("TLT", "GLD")


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def _with_hedge(norm: pd.Series, scale: float, columns) -> pd.Series:
    w = pd.Series(0.0, index=columns)
    w[norm.index] = norm * scale
    freed = 1.0 - scale
    if freed > 1e-9:
        per_asset = freed / len(HEDGE_ASSETS)
        for asset in HEDGE_ASSETS:
            if asset in w.index:
                w[asset] += per_asset
    return w


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

        rows[dt] = _with_hedge(norm, 1.0, prices.columns)

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
                rows[dt2] = _with_hedge(norm, scale, prices.columns)
                last_scale = scale
                continue
            if scale != last_scale:
                rows[dt2] = _with_hedge(norm, scale, prices.columns)
                last_scale = scale

    return pd.DataFrame.from_dict(rows, orient="index")
