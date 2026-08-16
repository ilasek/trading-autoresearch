"""Specify the trim's trigger as market-wide stress, instead of leaving it an accident.

WHAT TONIGHT ESTABLISHED FIRST. The champion's daily vol-spike trim does not
measure its own basket. Its availability filter (`dropna(how="any")` over a
price prefix starting in 1962) admits only instruments with a complete ~60-year
history: a mean of 3 of the 34 names held, 11% of book weight, sometimes zero.
The eleven instruments that can ever qualify are JNJ, PG, XOM, CVX, KO, MRK,
DIS, IBM, CAT, GE and HON — old-economy large-cap defensives and industrials,
close to the *opposite* style to a high-momentum growth book. Two trials tonight
bounded what that accident is worth:

    champion, trigger on the ~3 legacy names   val Sharpe 1.107, maxDD -29.1%
    trigger re-specified onto the real basket  val Sharpe 1.050, maxDD -30.8%  (#37)
    trim deleted entirely                      val Sharpe 1.062, maxDD -30.3%  (#38)

So the correctly-specified basket-own trigger is worse than no trim at all,
while the mis-specified one is worth +0.045 Sharpe over deleting it. The
mechanism the journal has been calling "the basket's own realized vol" is
therefore not what is doing the work.

THE HYPOTHESIS THIS TESTS. The reason a defensive-blue-chip trigger beats a
basket-own one is that it is *style-orthogonal*: the momentum book's own vol
rises whenever momentum names get violent, which includes melt-ups — last
session's diagnostic found the current trigger firing on 44 days in 2020, the
strategy's +132% year — whereas long-listed mega-cap defensives only get
turbulent in genuine market-wide stress. If that reading is right, the fix is
not to point the trigger at the basket but to point it deliberately at the
market, and the accident is worth keeping only once it is specified on purpose.

THE CHANGE, AND IT IS THE ONLY ONE. The trigger universe becomes every
instrument with complete data over the trailing ~283 days at the formation date
— the whole investable universe, equal-weighted, held or not. No tickers are
hard-coded: the rule is causal and self-updating, and it uses only past listing
history, so nothing about a name's future is consulted. Signal, buffer,
magnitude weighting, six-tranche overlap, SPIKE_RATIO 1.6, TRIM_SCALE 0.6 and
daily evaluation are byte-identical to the champion. In particular the 1.6
threshold is inherited untouched: a broad basket's vol ratio is smoother than a
3-name one, so this candidate stands or falls on the inherited number, and the
threshold will not be swept to rescue it.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below 1.062, the no-trim
control — that would say a deliberate market-stress trigger adds nothing and
the champion's +0.045 is specific to those particular eleven names, i.e. closer
to luck than to mechanism, and would make the champion's margin over the
untrimmed book something the repo should stop citing as crash detection.
Landing above 1.062 but below the champion's 1.107 is the awkward middle:
market-wide stress is a real signal, but weaker than the accident it replaces.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_market_trim",
    "family": "regime switching",
    "hypothesis": (
        "Driving the daily exposure trim from a deliberately specified "
        "market-wide vol-spike trigger — the equal-weighted 21d/252d realized "
        "vol ratio of every instrument with a complete trailing 283-day "
        "history, held or not — raises validation Sharpe above the champion's "
        "1.107 net of 15 bps costs, because the champion's trigger already "
        "reads a style-orthogonal set of long-listed defensives rather than "
        "its own basket, and specifying that on purpose replaces an incidental "
        "3-name sample with the full cross-section of the same signal."
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
        lo = max(0, start_pos - VOL_WINDOW)
        # Trigger universe: everything listed for the whole trailing window as
        # of the formation date — the market, not the book, and not a name list.
        hist_window = prices.iloc[lo:start_pos + 1]
        avail = hist_window.dropna(axis=1, how="any").columns
        if len(avail) == 0:
            continue
        sub = prices.iloc[lo:end_pos][avail]
        rets = sub.pct_change()
        market_ret = rets.mean(axis=1)
        vol_short = market_ret.rolling(VOL_SHORT).std(ddof=0)
        vol_long = market_ret.rolling(VOL_LONG).std(ddof=0)
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
