"""Restoring the date-overlap axis with the overlay finally held fixed across it.

THE CONFOUND THIS TRIAL EXISTS TO REMOVE. The repo's most consequential single
comparison is #42 vs #43: with four horizon legs in place, switching the
six-tranche date overlap OFF moved validation Sharpe 1.120 -> 1.187, the
biggest validation jump ever recorded here. That comparison is not clean. Both
sides carried the *accidental* trim, whose trigger was
`prices.iloc[:end_pos][names].dropna(axis=1, how="any")` — the intersection of
the **held basket** with the eleven-name full-history legacy cohort. Trials
#37-#40 established that the intersection is what the trigger reads, and
tonight's holdings-only diagnostic puts the two books' breadth at 35.1 (K=1)
against 62.7 (K=6) names. A trigger defined as an intersection with the held
set therefore samples a materially different cohort slice on each side of the
comparison: #45's own diagnostic already recorded the intersection growing from
3 names / 11% of book weight on the six-tranche base to 6.5 names / 20.7% on
the single-tranche one. So #42 vs #43 varied two things at once — the overlap,
and how much defensive-cohort signal the overlay happened to see.

Champion #45 removed the intersection. Its trigger is the equal-weighted
realized vol of every instrument with a complete price history to the formation
date, held or not: a **market-level** quantity that does not depend on the
basket at all, and is therefore bit-identical under K=1 and K=6. That makes the
overlap contrast measurable for the first time with the overlay held fixed.
This trial is that contrast, and it is one change from the champion:
`N_TRANCHES = 1 -> 6`. Signal, four horizon legs, per-leg buffer chains,
magnitude weighting, SPIKE_RATIO 1.6, TRIM_SCALE 0.6, daily evaluation and the
cohort definition are copied verbatim.

K=6 IS RESTORED, NOT SEARCHED. Six is the value established at trial #32 and
carried by #41/#42; it is not a new point scanned tonight, and no other value
is tried in this session or proposed for the next one. `learnings.md` forbids
sweeping K and the external-research folder bounds it on both sides without a
scan (above: momentum reverses past ~12 months of signal age, so a deeper stack
holds a reversing signal; below: a fresh-only window does not minimise forecast
error, which is why pruning tranches to the current held-set lost on every
axis). Six sits inside both with room. The point of this file is the *contrast*
at an already-established setting, not the setting.

PRE-TRIAL DIAGNOSTIC (holdings only, no returns scored, prices truncated at
2023-12-31, trial count untouched). Confirms the trial is not a no-op, which is
the trap that killed the book-weighted-vol re-specification for free:

    weight overlap K=1 vs K=6                0.645   (72 validation months)
    avg positions                     35.1 -> 62.7
    mean top weight                 0.1717 -> 0.1578
    mean HHI                        0.0753 -> 0.0618
    monthly target turnover          0.303 -> 0.109
    K=6 weight outside the current K=1 held-set   mean 0.140, max 0.268

The same diagnostic run killed a separate idea outright — averaging portfolios
formed under several buffer bands (10/18, 15/25, 20/35) overlaps the champion's
single band at 0.963 and adds 10.7 names at unchanged HHI, i.e. more names at
one date rather than decorrelated vintages. The contrast between 0.963 and
0.645 is the whole reason this axis and not that one is worth a trial.

PRE-REGISTERED READING, INCLUDING THE DIRECTION EXPECTED. The hypothesis is
falsifiable in the direction that would embarrass it: I expect K=6 to land
**below** the champion's 1.201 on validation, because `learnings.md` records
that this validation window rewards concentrated, fast-rotating books (its P&L
is dominated by 2019-2020) and the diagnostic above says K=6 is de-concentrated
and trades at a third of the target turnover. What the trial buys is the *size*
of the remaining gap with the overlay finally held fixed. If the gap collapses
from the confounded 0.067 to something inside this family's noise, then most of
#43's record validation jump was the trim sampling a different cohort slice
rather than the overlap axis itself, and the repo's reading of its own biggest
result needs amending. If the gap survives at roughly 0.067, the overlap really
does cost validation Sharpe on its own and #43's finding stands as recorded.
Either answer is worth one trial; only the second is the one the repo currently
believes.

WHAT THIS FILE IS NOT. It is not designed against the holdout. The holdout
numbers for #42, #43 and #45 are in the permanent record and every session
reads them, but they are not the design driver here and no holdout figure is
used to choose K, the bands, the horizons or the trigger — the argument above
runs entirely on the validation-side confound and on holdings statistics. Per
the stopping rule in `learnings.md`, if this trial promotes and thereby exposes
a fresh holdout number, the session ends rather than chaining further
candidates off it.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_k6_cohort_trim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Restoring the six-tranche formation-date overlap on the champion's "
        "four-horizon base — a single change, N_TRANCHES 1 -> 6, with signal, "
        "buffers, magnitude weighting, cohort definition, SPIKE_RATIO 1.6, "
        "TRIM_SCALE 0.6 and daily evaluation identical — closes most of the "
        "0.067 validation-Sharpe gap that trial #43 opened by switching the "
        "overlap off, because that comparison ran with the accidental "
        "held-basket-intersection trigger on both sides and the intersection "
        "samples a materially different cohort slice at 35.1 held names than "
        "at 62.7, whereas the champion's whole-cohort trigger is market-level "
        "and bit-identical across K; a gap that survives at roughly its "
        "original size falsifies that and shows the overlap genuinely costs "
        "validation Sharpe on its own."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
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


def _leg_target(score: pd.Series, held: set) -> tuple[pd.Series, set]:
    ranked = score.sort_values(ascending=False)
    core = set(ranked.index[:CORE_N])
    band = set(ranked.index[:BAND_N])
    held = (held & band) | core
    c_held = score[list(held)]
    raw = c_held - c_held.min() + FLOOR
    return raw / raw.sum(), held


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = {lb: set() for lb in LOOKBACKS}
    recent_targets = []
    base_periods = []

    all_dates = prices.index
    max_lb = max(LOOKBACKS)
    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < max_lb + SKIP + 1:
            continue

        moms = {lb: _momentum(hist, lb) for lb in LOOKBACKS}
        common = None
        for m in moms.values():
            common = m.index if common is None else common.intersection(m.index)
        if len(common) < CORE_N:
            continue

        leg_targets = []
        for lb in LOOKBACKS:
            score = _zscore(moms[lb][common])
            t, held[lb] = _leg_target(score, held[lb])
            leg_targets.append(t)
        target = pd.concat(leg_targets, axis=1).fillna(0.0).mean(axis=1)
        target = target / target.sum()

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
        # Market-level trigger, copied verbatim from the champion: everything
        # listed for the entire prefix as of the formation date, held or not.
        # It does not read the basket, so it is identical under K=1 and K=6 —
        # which is the whole point of this trial.
        cohort = prices.iloc[:start_pos + 1].dropna(axis=1, how="any").columns
        if len(cohort) == 0:
            continue
        rets = prices.iloc[:end_pos][cohort].pct_change()
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
