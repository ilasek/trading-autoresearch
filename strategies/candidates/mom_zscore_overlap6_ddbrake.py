"""Drawdown-state brake on the champion's overlapping-tranche book.

WHY THIS, AND WHY NOW. A returns-only diagnostic on the champion's recorded
validation series (trial #35, no re-backtest) showed that the daily vol-spike
trim it carries is a *fast-crash* detector, not a loss-avoider: the 21d/252d
vol ratio crosses 1.6 on 44 days in 2020 (+132%, the best year) and on 0 days
in 2021 and 2023, but on only 7 days in 2018 (-5.9%) and 13 in 2022 (-8.9%) —
the two years the strategy actually loses money. Both loss regimes are slow
grinds (2018-10 -> 2019-01, and 2022-04 -> 2023-04) in which dispersion never
spikes, so a ratio-of-vols trigger structurally cannot see them. The book
spends 16 days below -25% drawdown in the whole validation window and every
one of them falls in those two years.

THE MECHANISM. Add a second, path-dependent state variable the vol trigger
does not carry: the book's own equity drawdown. Track the pre-trim book's
gross equity, and brake exposure when it falls far below its running peak,
releasing only after it has substantially recovered — a hysteresis band, the
same device the membership buffer already uses (enter top-15, hold to top-25).

Enter at -20%, release at -10%. These are set from the *shape* of the
drawdown-episode distribution, not tuned against performance: of 55 distinct
episodes in validation, 12 reach -5%, 6 reach -10% and only 4 reach -20%, so
-20% is where routine noise ends, and -10% is the level the book has recovered
past in every episode that later resumed. Deliberately NOT set to -25%, which
the diagnostic shows would isolate exactly the two loss years — that number
would be fitted to the window, not chosen from it. They will not be swept.

ONE CHANGE ONLY. Signal, buffer, magnitude weighting, tranche structure and
the vol-spike trim are byte-identical to the champion. The two overlays are
combined with min(), not by multiplying, so the deepest de-risking this
candidate can reach is 0.6x — exactly the champion's. The trial therefore
tests *when* to de-risk, holding *how much* fixed; a multiplicative
combination would confound the two.

WHAT WOULD FALSIFY IT. The brake also arms during drawdowns that preceded
strong rebounds — the diagnostic shows -20% was breached in 2020 (before a
+132% year) and 2021 (+17.5%) as well. If selling a fifth of the way down and
buying back after a recovery costs more in those years than it saves in 2018
and 2022, validation Sharpe lands at or below the champion's 1.107. That is
the null this trial exists to test, and it is the *a priori* likely one: this
repo has refuted three de-risking overlays already, and drawdown control on a
mean-reverting equity book is a known way to sell bottoms.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_ddbrake",
    "family": "regime switching",
    "hypothesis": (
        "Adding a hysteresis drawdown brake on the book's own equity (cut "
        "exposure to 0.6x when the pre-trim book is more than 20% below its "
        "running peak, restore when it recovers to within 10%), combined with "
        "the existing daily vol-spike trim by min() so peak de-risking is "
        "unchanged, raises validation Sharpe above the champion's 1.107 net "
        "of 15 bps costs, because the vol-ratio trigger it already carries "
        "fires in the strategy's best year and is nearly blind in both years "
        "it loses money, where the losses are slow grinds without a "
        "dispersion spike."
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

DD_ENTER = -0.20   # arm the brake below this drawdown
DD_EXIT = -0.10    # release it once recovered above this


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

    # ---- overlay 1: the champion's daily vol-spike trim, unchanged ----
    vol_scale = pd.Series(1.0, index=all_dates)
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
        scale_series = scale_series.where(vol_long > 0, 1.0).fillna(1.0)
        vol_scale.iloc[start_pos:end_pos] = scale_series.iloc[start_pos:end_pos].to_numpy()

    # ---- overlay 2: drawdown brake on the pre-trim book's own equity ----
    # The state variable ignores both overlays' own scaling, so the brake reads
    # the underlying basket's drawdown rather than one it partly caused.
    book_ret = pd.Series(0.0, index=all_dates)
    for start_pos, end_pos, norm in base_periods:
        names = [n for n in norm.index if n in prices.columns]
        seg = prices.iloc[start_pos:end_pos][names]
        if len(seg) < 2:
            continue
        # weights set on start_pos earn from the next day, matching the engine's lag
        day_rets = seg.pct_change().iloc[1:]
        contrib = day_rets.mul(norm.reindex(day_rets.columns), axis=1).sum(axis=1, min_count=1)
        book_ret.loc[contrib.index] = contrib.fillna(0.0).to_numpy()

    equity = (1.0 + book_ret).cumprod()
    drawdown = equity / equity.cummax() - 1.0

    brake_scale = pd.Series(1.0, index=all_dates)
    braked = False
    scales = []
    for value in drawdown.to_numpy():
        if braked:
            if value >= DD_EXIT:
                braked = False
        elif value <= DD_ENTER:
            braked = True
        scales.append(TRIM_SCALE if braked else 1.0)
    brake_scale.iloc[:] = scales

    combined = pd.concat([vol_scale, brake_scale], axis=1).min(axis=1)

    # ---- emit rows only where the effective scale moves, as the champion does ----
    last_scale = 1.0
    for start_pos, end_pos, norm in base_periods:
        day_scales = combined.iloc[start_pos:end_pos]
        for dt2, scale in day_scales.items():
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
