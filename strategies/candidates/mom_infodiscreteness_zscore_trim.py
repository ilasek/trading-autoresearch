"""Information-discreteness ("frog in the pan") as a third scoring dimension.

Base mechanism is byte-identical to `mom_zscore_narrow_daily_volspike_trim`
(trial #28, the repo's strongest challenger: val Sharpe 1.07, maxDD -30.3%):
hold-25/enter-15 buffer, magnitude weighting by composite z-score, 25% cap,
daily-reacting basket-own vol-spike exposure trim, monthly rebalance. The only
change is that the composite gains a third z-scored term.

Da, Gurun & Warachka (2014) document that momentum formed by a steady drip of
small same-signed moves ("continuous information") continues far more
reliably than momentum formed by a few large jumps ("discrete information"),
because gradual information diffuses under investor inattention while jumps
are news the market has already priced. Their measure is

    ID = sign(PRET) * (%neg - %pos)

over the formation window; low ID = continuous. This candidate adds the
continuity score -ID as a third equally-weighted composite term alongside the
252d and 126d return z-scores, so it shifts both basket membership and
magnitude weights toward gradual-information winners.

Why this is a different axis from the two residual-momentum trials just run
(#32, #33): ID is computed purely from the *sign pattern* of daily returns —
it never divides by volatility and never regresses out a common factor. Trial
#32 showed idiosyncratic-vol normalization is a drawdown lever that costs too
much return; trial #33 showed removing market beta from the score is mildly
negative on every axis. ID is orthogonal to both: a high-volatility name that
ground steadily upward scores well, and a low-volatility name that gapped once
scores badly, which is the reverse of what a risk-normalized score does.

Falsifiable: if information discreteness carries no independent signal on this
universe — or is merely another smoothness-preferring proxy that acts like the
vol denominator did — validation Sharpe lands at or below 1.07, and in the
latter case with the same signature of lower return alongside lower maxDD.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_infodiscreteness_zscore_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Adding a third equally-weighted composite term for information "
        "continuity (-ID, where ID = sign(formation return) * (%neg - %pos) "
        "of daily returns over the 252d formation window, skipping the most "
        "recent month) to the buffered magnitude-weighted momentum basket "
        "raises validation Sharpe above the 1.07 of the otherwise identical "
        "two-term version, net of 15 bps costs, because momentum built from "
        "gradual same-signed drift continues more reliably than momentum "
        "built from a few large jumps that the market has already priced."
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
    """-ID = sign(PRET) * (%pos - %neg) over the formation window."""
    px = hist.iloc[-(lookback + SKIP) - 1 : len(hist) - SKIP]
    px = px.dropna(axis=1, how="any")
    if px.shape[1] < 2 or len(px) < lookback:
        return pd.Series(dtype=float)

    rets = px.pct_change().iloc[1:]
    n = len(rets)
    pct_pos = (rets > 0).sum() / n
    pct_neg = (rets < 0).sum() / n
    pret = px.iloc[-1] / px.iloc[0] - 1
    return np.sign(pret) * (pct_pos - pct_neg)


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
