"""A no-trade band on position *sizes*, completing the hysteresis idea that
membership buffering only half-implemented.

Background. The single most productive mechanism ever found in this repo was
hysteresis on basket *membership* (`mom_12m_buffered`, trial #17): replacing a
hard top-15 cutoff with hold-25/enter-15 improved Sharpe and cut turnover at the
same time — the only free lunch recorded here. Every subsequent improvement has
been built on that basket.

But the buffer only governs *who is in the basket*. Once a name is in, its
target weight is recomputed from scratch every month off a continuous composite
z-score, and the engine trades all the way to that new number. That is where the
cost is actually going: the best challenger (trial #28) turns over 7.3x per year
while typically holding ~18 names it mostly keeps for many months. Twelve
membership rebalances a year cannot account for 7.3x — most of that turnover is
*re-sizing names we are keeping anyway*, chasing small month-to-month wiggles in
a noisy score. At 15 bps per side that is roughly 2.2% of annual return burned,
against a strategy earning ~27%.

The fix is the standard result for portfolio choice under proportional
transaction costs (Constantinides 1986; Garleanu & Pedersen 2013): the optimal
policy is *not* to track the target continuously. It is to define a no-trade
region around the target and leave the position completely alone while it stays
inside — because near the optimum the utility surface is flat, so the benefit of
closing a small gap is second-order while the cost of trading is first-order.
Applied here: if a held name's newly-computed target weight differs from what we
already own by less than a quarter of the position, do not trade it at all.

This is a different mechanism from everything already refuted:
- It is not the membership buffer (trial #17), which decides *who* is held. This
  decides *how much*, for names whose membership is not in question.
- It is not weight-spread dampening (trial #22, refuted), which shrank the
  *dispersion* of the target weights toward equal-weight and cost Sharpe. This
  leaves every target exactly where the magnitude-weighting puts it and changes
  only the willingness to pay to get there. The refuted idea altered where the
  portfolio wants to be; this one alters how eagerly it chases it.
- It is not an exposure overlay (the vol-spike trim family). Gross exposure is
  unchanged; only the churn between names is.

Membership changes are always executed in full — a name entering the basket goes
straight to its target and a name leaving goes straight to zero. The band applies
only to retained names. After banding, the vector is renormalized to full
investment, which nudges every weight by a common factor of well under 1%; that
is a negligible amount of turnover and keeps gross exposure at the same 1.0 the
comparison basket runs at.

The 25% relative band is the one new constant, chosen a priori as "a quarter of
the position is a material drift" rather than fitted. It will not be swept: if
the mechanism works the finding is that no-trade bands help, and if it fails the
finding is that this basket's month-to-month re-sizing is real signal rather than
noise. Either way the answer does not live in the third decimal of the band.

Everything else is held byte-for-byte identical to
`mom_zscore_narrow_daily_volspike_trim` (trial #28, val Sharpe 1.07,
maxDD -30.3%, DSR 0.9326): universe, composite 6-1/12-1 total-return z-score,
hold-25/enter-15 buffer, magnitude weighting, 0.25 cap, and the daily-evaluated
binary vol-spike trim.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_notrade_band",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Leaving a retained name's position untouched when its newly-computed "
        "target weight is within 25% of the weight already held — a no-trade "
        "band on size, on top of the existing hold-25/enter-15 band on "
        "membership — raises validation Sharpe above 1.07 net of 15 bps costs, "
        "because most of the basket's 7.3x annual turnover is re-sizing names "
        "it keeps anyway, and paying 30 bps round-trip to chase second-order "
        "wiggles in a noisy score costs more than the tracking error it avoids."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

NOTRADE_BAND = 0.25   # relative to the weight currently held

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
    """Hold the existing position for any name whose target has moved less than
    NOTRADE_BAND of what is already held; trade the rest to target. Names not
    previously held (current 0) always trade in full."""
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
    current = pd.Series(dtype=float)   # last executed base weights

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
