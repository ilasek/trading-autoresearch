"""The control that isolates the champion's trim to one degree of freedom.

WHERE THE INVESTIGATION STANDS. The champion's daily trim reads the realized
vol of the held names that have a complete price history back to the store's
1962 start — a mean of 3 of 34 held names, 11% of book weight, drawn from the
eleven old-economy large caps that are the only instruments able to qualify
(JNJ, PG, XOM, CVX, KO, MRK, DIS, IBM, CAT, GE, HON). Tonight bounded what that
is worth against every deliberate specification of the mechanism it was
believed to be:

    champion — held names ∩ full-history cohort   1.107   (the accident)
    trigger on the real held basket        (#37)  1.050
    trim deleted                           (#38)  1.062
    trigger on the whole market            (#39)  1.055

Every intentional trigger collapses to the no-trim control. Only the accident
is worth anything, which leaves exactly one untested degree of freedom: the
champion's trigger conditions on **basket membership ∩ legacy cohort**, and
neither term alone reproduces it — the market test above dilutes the legacy
names into 140, and the basket test drops them.

THE CHANGE, AND IT IS THE ONLY ONE. This candidate removes the intersection
with the held basket and keeps the cohort: the trigger is the equal-weighted
realized vol of every instrument with a complete history from the start of the
price store to the formation date, whether or not the strategy holds it. That
is the champion's own filter with one term deleted. No tickers are hard-coded
and no future information is read — completeness is evaluated on the trailing
prefix only, so the cohort is whatever the store's own start date implies at
each formation. Signal, buffer, magnitude weighting, six-tranche overlap,
SPIKE_RATIO 1.6, TRIM_SCALE 0.6 and daily evaluation are byte-identical to the
champion.

WHY THE ANSWER MATTERS MORE THAN THE VERDICT. This trial is diagnostic, and
either result is worth having:

  - Landing near 1.107 means the long-listed defensive cohort's volatility is
    a genuine style-orthogonal stress signal for a momentum book, which the
    repo found by accident and can now state deliberately. It would also mean
    the champion is doing something real, just not the thing its docstring
    claims.
  - Landing near 1.06, with the no-trim control, means the effect survives
    only when the cohort is sampled *through* basket membership — three names
    varying month to month by which defensives the momentum screen happens to
    hold. There is no mechanism that reads that way, and the honest conclusion
    would be that the champion's +0.045 Sharpe over an untrimmed book is
    sampling luck inside a 6-year window, and that the repo should stop citing
    the daily vol-spike trim as one of its established mechanisms.

WHAT WOULD FALSIFY THE HYPOTHESIS AS WRITTEN. Validation Sharpe at or below
1.062 — the no-trim control — falsifies the "legacy cohort carries a real
stress signal" reading and forces the sampling-luck conclusion.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_legacy_trim",
    "family": "regime switching",
    "hypothesis": (
        "Driving the daily exposure trim from the realized vol of the whole "
        "long-listed cohort — every instrument with a complete history from "
        "the store's start to the formation date, held or not, rather than "
        "only the ~3 of them the momentum screen happens to hold — reproduces "
        "or beats the champion's 1.107 validation Sharpe net of 15 bps costs, "
        "because the signal doing the work is those defensives' turbulence "
        "and not the incidental intersection with basket membership."
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
        # The champion's own filter with the basket intersection removed:
        # everything listed for the entire prefix as of the formation date.
        cohort = prices.iloc[:start_pos + 1].dropna(axis=1, how="any").columns
        if len(cohort) == 0:
            continue
        sub = prices.iloc[:end_pos][cohort]
        rets = sub.pct_change()
        cohort_ret = rets.mean(axis=1)
        vol_short = cohort_ret.rolling(VOL_SHORT).std(ddof=0)
        vol_long = cohort_ret.rolling(VOL_LONG).std(ddof=0)
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
