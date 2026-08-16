"""Measure the vol-spike trim on the basket it is supposed to be measuring.

THE MIS-SPECIFICATION. Every candidate in this line since trial #22 computes
its "basket's own realized vol" like this:

    sub = prices.iloc[:end_pos][names]              # names = the held basket
    avail = sub.dropna(axis=1, how="any").columns   # <-- over the WHOLE prefix
    basket_ret = sub[avail].pct_change().mean(axis=1)

`prices` starts in 1962, so `dropna(how="any")` over the full prefix keeps only
instruments with a complete ~60-year history. A holdings-only diagnostic over
the champion's own formations (weights only, nothing scored) shows what that
leaves: across the 72 validation-window formations the book holds a mean of
34.1 names, of which a mean of **3.0** survive the filter — **11% of book
weight**, and in some months zero, which disables the trim outright. The
trigger the journal describes as "the basket's own realized vol" is in practice
the equal-weighted vol of whichever handful of pre-1962-listed instruments the
momentum screen happens to hold.

NOT A RE-TEST. `learnings.md` records that a prior session considered
re-specifying this trim and killed it with a diagnostic showing the
book-weighted and equal-weighted definitions disagree on 1 of 1562 days. That
compared two *weightings of this same 3-name subset*, and its conclusion (the
21d/252d ratio is insensitive to weighting within one correlated basket) is not
in dispute here. This candidate changes the *universe*, not the weighting.

THE CHANGE, AND IT IS THE ONLY ONE. The availability filter is applied over a
trailing window ending at the formation date rather than over all history: a
name qualifies if it has complete data over the ~283 trading days the 252/21
rolling statistics actually consume. Everything else — signal, buffer,
magnitude weighting, six-tranche overlap, SPIKE_RATIO 1.6, TRIM_SCALE 0.6,
daily evaluation — is byte-identical to the champion. As a side effect the
filter also becomes strictly causal: the champion's version reads to
`end_pos`, i.e. one rebalance into the future of the period it governs, to
decide which names enter the proxy. (That leak cannot move holdings on shared
dates, which is why the causality check has always passed it, but there is no
reason to keep it once the line is being rewritten.)

WHY IT COULD GO EITHER WAY. Measuring the real basket should make the trigger
fire when the book is actually turbulent instead of when three legacy names
are, and the trim is worth +0.045 validation Sharpe on this base (overlap6
with trim 1.107 vs `mom_zscore_overlap6_notrim` 1.062), so sharpening it has
something real to sharpen. But the opposite is live: last session's returns
diagnostic shows the current trigger fires on 44 days in 2020 (+132%) and near
zero in the two loss years, so whatever it is doing well, it is doing by
*accident* of that odd universe — and a correctly-specified trigger may simply
be a different, no-better one.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below the champion's 1.107.
A specific and instructive failure mode to watch: if Sharpe lands near
`mom_zscore_overlap6_notrim`'s 1.062, the honest reading is that the trim's
entire measured benefit was an artifact of the degenerate universe rather than
a crash-detection mechanism, which would retro-actively weaken the
"daily-cadence vol-spike trim" finding in learnings.md.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_trim_universe",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Computing the daily vol-spike trim's realized-vol trigger over the "
        "names actually held — qualifying them on a trailing 283-day window "
        "instead of a complete history back to 1962, which currently admits a "
        "mean of 3 of 34 held names and 11% of book weight — raises validation "
        "Sharpe above the champion's 1.107 net of 15 bps costs, because the "
        "trigger then measures the turbulence of the book it de-risks rather "
        "than that of an incidental handful of long-listed instruments."
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

# Trailing window the rolling 252/21 statistics consume, plus a small margin.
VOL_WINDOW = VOL_LONG + VOL_SHORT + 10


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
        lo = max(0, start_pos - VOL_WINDOW)
        # Qualify names on data available at formation only — no reading past
        # `start_pos` to decide what the trigger for this period is made of.
        hist_window = prices.iloc[lo:start_pos + 1][names]
        avail = hist_window.dropna(axis=1, how="any").columns
        if len(avail) == 0:
            continue
        sub = prices.iloc[lo:end_pos][avail]
        rets = sub.pct_change()
        basket_ret = rets.mean(axis=1)
        vol_short = basket_ret.rolling(VOL_SHORT).std(ddof=0)
        vol_long = basket_ret.rolling(VOL_LONG).std(ddof=0)
        ratio = vol_short / vol_long
        scale_series = (ratio > SPIKE_RATIO).map({True: TRIM_SCALE, False: 1.0})
        scale_series = scale_series.where(vol_long > 0, 1.0)

        day_scales = scale_series.loc[all_dates[start_pos]:all_dates[end_pos - 1]]
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
