"""Remove the membership-dependent anchor from the magnitude-weighting formula.

Background — this is a direct consequence of the turnover decomposition run on
trial #34, not a fresh guess. Every magnitude-weighted candidate in this repo
(trials #20 onward, including the best challengers) sizes positions as:

    raw  = composite - composite[held].min() + 0.05
    w    = raw / raw.sum()

The subtraction of `composite[held].min()` anchors the entire weight vector to
*the score of the weakest name currently in the basket*. That name is, by
construction, the least stable member of the portfolio: the hold-25/enter-15
buffer means the marginal member changes frequently. Every time it does, the
anchor moves, and **every weight in the basket is rescaled — including for names
whose own score and rank did not move at all.**

The decomposition made the cost of this concrete. Of the best challenger's 7.30x
annual validation turnover, 4.67x (64%) is re-sizing names that stay in the
basket, and a 25%-of-position no-trade band caught only 7% of it: the re-sizing
moves are large, not small. Large re-sizing of names whose signal did not change
is exactly the fingerprint of a moving anchor rather than of a moving signal.
At 30 bps round-trip, that turnover is roughly 1.4% of annual return.

The fix is to anchor the weights to something that does not depend on who else
is in the basket. The composite is already a sum of two cross-sectional z-scores,
so it is on a standardized scale with a meaningful, membership-independent zero:
a name at the universe average scores 0, and basket members essentially always
score well above it. Weighting by the score itself, floored at a small constant,
gives each name a weight that depends only on its own score and on the sum — so
a name's weight now moves when *its own* signal moves, and no longer when an
unrelated name at the bottom of the basket is swapped out.

Two independent reasons to expect this to help, pointing the same way:
1. Cost: it removes an artificial source of re-sizing turnover.
2. Signal: dropping the min-shift *widens* the weight spread, tilting more
   capital toward the strongest-scoring names. That is the direction the repo's
   most reliable Sharpe lever has always pointed — equal-weight -> rank-weight ->
   magnitude-weight climbed 0.90 -> 0.93 -> 0.98, and the one attempt to go the
   other way (square-root dampening, trial #22) lost Sharpe *and* DSR. Note this
   is not the "further escalate concentration" move the learnings warn against:
   the escalation here is a side effect of removing a normalization artifact,
   and it comes with a turnover *reduction* rather than the drawdown widening
   that accompanied every earlier escalation step.

Base is `mom_zscore_notrade_band` (trial #34, val Sharpe 1.080, turnover 7.0x),
the current best challenger, with its 25% no-trade band retained — that band's
effect was already measured in isolation, so any change from 1.080 is
attributable to the anchor. Signal, horizons, buffer, cap, and the daily
vol-spike trim are all unchanged.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_fixed_anchor",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Sizing positions by the composite z-score floored at a fixed constant, "
        "instead of by the score minus the weakest current member's score, "
        "raises validation Sharpe above the 1.080 of the otherwise-identical "
        "trial #34 basket and lowers its 7.0x turnover, because anchoring "
        "weights to the marginal member rescales the whole portfolio whenever "
        "that member is swapped — generating large re-sizing trades that carry "
        "no signal."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05          # membership-independent floor, replaces the min-shift

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

        # Fixed anchor: a name's weight depends on its own score only.
        raw = composite[list(held)].clip(lower=FLOOR)
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
