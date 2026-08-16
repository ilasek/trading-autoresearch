"""Overlapping tranches (K = 6) with signal-conditional tranche membership.

WHAT THE OVERLAP CURRENTLY DOES. Each month a formation writes a frozen
target-weight vector, and the live book is the equal average of the six most
recent such vectors (trial #32, val Sharpe 1.11, maxDD -29.1%, turnover
3.0x). Those vectors are frozen *completely*: a tranche formed five months
ago keeps its full 1/6 of capital on exactly the names it bought, even if
every one of them has since fallen out of the strategy's own buffered
`held` set.

HOW MUCH CAPITAL THAT STRANDS. Measured directly on the weight matrix
(holdings only, no returns scored, not a backtest), averaged over months:

                        weight on names outside the current held-set
    train (1962-2017)                 10.7%   (max 58.2%)
    validation (2018-2023)            20.6%   (max 55.2%)

So across the validation window roughly **one fifth of the book, on
average, is committed to names the strategy's current signal has already
rejected** — not names it is merely lukewarm on, but names outside even the
tolerant hold-25 buffer band (19.3% by that stricter measure). The
weight-weighted average current rank of the book is 17.2 against a
hold-25/enter-15 rule.

THE CHANGE. Tranche *lifetime* stops being unconditional. At each rebalance
every live tranche is masked to the names currently in `held` and
renormalised, so a tranche keeps its 1/6 of capital but may only deploy it
into names the signal still endorses. A tranche whose picks all survive is
untouched; one whose picks have decayed is pruned early rather than riding
out its full six months. This is explicitly *not* a K sweep — nominal
tranche lifetime stays at six months, and the mechanism, signal, buffer,
weighting and daily vol-spike trim are all unchanged. It changes only
whether a tranche's capital stays on names the current signal rejects.

WHY IT MIGHT FAIL, AND THE HONEST TENSION. Trial #32 established that
holding capital on formation signals up to six months stale cost *zero*
return in aggregate (ann_ret 26.9%, identical at K = 3 and K = 6 in the
archived work). One reading of that is that the staleness tax is real but
was outweighed by cost savings — which this change should recover. The
competing reading is that there is no staleness tax at all, because the
decayed names are exactly where short-horizon rebound accrues; on that
reading pruning them is selling losers at the bottom and will cost return
outright. Two further forces push against the change: pruning must be paid
for in turnover (the 3.0x base will rise), and a pruned book is a narrower,
more concentrated book — tonight's trial #33 showed that on this base a
~30% rise in HHI is worth roughly 2 points of drawdown. There is also a
conceptual argument against: the hold-25 buffer exists precisely because
hard membership cutoffs manufacture turnover without signal, and pruning
reintroduces a cutoff by the back door.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below trial #32's 1.11 means
the stranded capital is not a drag and the whole staleness axis closes with
it — a decisive read either way, since the diagnostic above shows the
quantity of capital involved is far too large for a null to be a
measurement-scale artifact.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_live_tranche",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Masking each live formation tranche to the names still in the "
        "current buffered held-set and renormalising it — so a tranche keeps "
        "its 1/6 of capital but cannot hold names the signal has since "
        "rejected — raises validation Sharpe above the 1.11 of the "
        "otherwise-identical six-tranche basket (trial #32), net of 15 bps "
        "costs, because roughly a fifth of that basket's book weight sits on "
        "decayed names whose momentum edge has already expired."
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

        # Signal-conditional tranche lifetime: each live tranche keeps its
        # 1/N of capital, but only on names the signal currently endorses.
        # Renormalising per tranche preserves the equal capital split, so
        # the average of the tranches still sums to 1.
        live = []
        for t in recent_targets:
            kept = t[[n for n in t.index if n in held]]
            total = kept.sum()
            live.append(kept / total if total > 0 else t)

        blended = pd.concat(live, axis=1).fillna(0.0).mean(axis=1)
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
