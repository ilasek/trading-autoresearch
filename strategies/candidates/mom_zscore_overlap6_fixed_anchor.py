"""Overlapping tranches (K = 6) with a membership-independent weight anchor.

The repo's two strongest mechanisms were found in two different off-branch
sessions that could not see each other, and have never been run together:

  1. **Fixed anchor** (archived 2026-08-14, that session's trial #35). Every
     magnitude-weighted candidate since trial #20 sized positions off
     `composite - composite[held].min() + FLOOR`, anchoring the entire weight
     vector to the weakest *currently held* name — precisely the name the
     hold-25/enter-15 buffer swaps most often. Every swap therefore rescaled
     every weight in the book even when no name's own signal had moved. That
     session's weight-matrix decomposition measured the artifact directly:
     re-sizing turnover fell from 4.67x to 2.30x per year when the min-shift
     was replaced by a fixed floor. It also found the min-shift had been a
     hidden *concentration amplifier*, not the compressor it looked like —
     the subtracted minimum is usually negative (a decayed buffer member),
     and subtracting a negative inflates the top-to-bottom weight spread by
     an amount that drifts month to month with how badly the worst held name
     had decayed.
  2. **Overlapping formation tranches** (archived 2026-08-15; verified on
     `main` tonight as trial #32 — val Sharpe 1.11, maxDD -29.1%, turnover
     3.0x). Reform 1/6 of capital per month and hold each tranche six months.

These are orthogonal: the anchor governs *how* weights are computed within
one formation, the overlap governs *when* capital commits to a formation.
Tonight's trial #32 carries the min-shift anchor untouched, so the artifact
identified in (1) is still live inside every one of its six tranches.

WHY THIS IS A GENUINE TENSION, NOT A STACK-THE-WINS SWEEP. The two
mechanisms overlap in their *effects* even though their causes are
independent, and they could plausibly cancel:

- Both reduce turnover, so the anchor fix's headline benefit may already
  have been harvested — averaging six formation vectors mechanically damps
  any single formation's rescaling, since a spurious rescale in one tranche
  is diluted 6:1. If so the fix is a no-op here and this trial says so.
- Both reduce concentration (the anchor fix cut mean top weight 0.194 →
  0.143 on its own; averaging six tranches spreads the book across ~34
  names). Stacking them could push the book past the point where
  magnitude-weighting still pays — the repo's equal → rank → magnitude
  ladder says tilting capital *toward* the strongest names is where the
  Sharpe came from, and over-diluting would give that back.
- Against both: the artifact is *noise*, not signal. Removing a source of
  signal-independent weight movement should compound with, not substitute
  for, a mechanism that lowers cost. And the 08-15 session showed this
  basket's residual drawdown is driven by effective *weight* concentration
  rather than name count — the anchor fix attacks exactly that, and did cut
  maxDD to the repo's best-ever -28.2% when tested standalone.

Note this is not the retired "re-tilt concentration" lever, which the
2026-08-14 session closed in both directions. Concentration is not a free
parameter here: it is whatever the stable, membership-independent transform
produces. Nothing else is touched.

SINGLE VARIABLE. Identical to tonight's trial #32 in signal (12-1 and 6-1
composite z-score), buffer (hold-25 / enter-15), tranche count (K = 6),
cap, and the daily vol-spike trim. The only edit is the two lines computing
`raw`. The archived fixed-anchor candidate also carried a 25% no-trade band;
that is deliberately *excluded* here to keep this a one-variable test — the
band was reported as underdelivering against its own premise, and at 3.0x
turnover it has little left to save.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below trial #32's 1.11 with
no improvement in maxDD would mean the overlap has already absorbed
whatever the anchor fix was worth, retiring the anchor axis on this base.
A Sharpe fall with a *further* drop in concentration would instead mean the
two de-concentration effects compounded past the useful point.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_fixed_anchor",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Sizing each formation tranche by the composite z-score floored at a "
        "fixed constant, instead of by the score minus the weakest currently "
        "held member's score, raises validation Sharpe above the 1.11 of the "
        "otherwise-identical six-tranche basket (trial #32) and lowers its "
        "-29.1% maxDD, net of 15 bps costs, because the min-shift anchor "
        "rescales every weight in the book whenever the buffer swaps its "
        "weakest member — signal-independent movement that averaging six "
        "tranches damps but does not remove."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05          # membership-independent floor, replaces the min-shift

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

        # Fixed anchor: a name's weight depends on its own score only, never
        # on which other names happen to be in the basket this month.
        raw = composite[list(held)].clip(lower=FLOOR)
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
