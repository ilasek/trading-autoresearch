"""Decomposition, not a challenger: horizon averaging with the date overlap
switched off.

WHY THIS IS WORTH A TRIAL EVEN THOUGH IT CANNOT WIN. Trials #41 and #42
established that averaging several lookback-length vintages as portfolios
raises Sharpe, breadth and drawdown together, on top of the six-tranche date
overlap. What they cannot tell apart is whether the two kinds of vintage
diversity are **complements** (each supplying decorrelation the other cannot)
or **substitutes** (one general mechanism — average over decorrelated
vintages of any kind — reachable by either route). That distinction decides
where a future session should look, and it is not answerable from the two
results already recorded, because both carry both mechanisms at once.

This candidate therefore removes exactly one of them: four quarterly lookback
windows (12-1, 9-1, 6-1, 3-1), each with its own buffer chain and its own
magnitude-weighted target, averaged at equal weight — and then **no date
tranching at all** (N_TRANCHES = 1, the whole book reformed every month).
Everything else is trial #42 unchanged: same skip, same hold-25/enter-15
band, same weighting, same daily vol-spike trim.

THE COMPARATOR IS ALREADY ON RECORD, WHICH IS WHY THIS COSTS ONE TRIAL AND
NOT TWO. `mom_zscore_narrow_daily_volspike_trim` (trial #28) is precisely
this construction with one composite score instead of four averaged
portfolios: K = 1, same band, same weighting, same trim — validation Sharpe
1.066, maxDD -30.3%, turnover 7.3x. So the 2x2 completes itself:

    date overlap x horizon averaging   val Sharpe
    no  x no    (#28)                    1.066
    yes x no    (#35, champion until tonight)  1.107
    yes x yes   (#42, champion)           1.120
    no  x yes   (this trial)              ?

STATED PLAINLY: THIS IS NOT EXPECTED TO PROMOTE. The date overlap is worth
roughly 0.04 of Sharpe and cuts turnover from 7.3x to 3.0x; removing it
should cost most of that back. The trial is spent on the shape of the answer,
not on the number. `learnings.md` records that the repo's most useful results
have come from exactly this shape — bracketing a mechanism against its own
controls (the five-way trim-universe comparison, the concentration-vs-trim
additivity check) — and it is the honest way to find out whether tonight's
promotions rest on one mechanism or two.

WHAT EACH OUTCOME MEANS. If validation Sharpe lands near #28's 1.066, horizon
averaging does nothing without the date overlap: the two are complements and
the date overlap is the load-bearing one. If it lands materially above 1.066
— toward 1.10 — then length diversity substitutes for date diversity, the two
are two routes to one mechanism, and the general statement in `learnings.md`
should be widened from "decorrelated formation *dates*" to "decorrelated
vintages of any kind". If it lands at or above #42's 1.120, tonight's reading
is wrong in an interesting way and the date overlap is redundant once enough
horizons are averaged.

CAVEATS. (a) Turnover will be high (#28 ran 7.3x); the gate's ceiling is 50x,
so this is a cost drag, not a gate risk. (b) As in #41 and #42, the book's
name count changes, which perturbs the `held ∩ legacy-cohort` intersection
that trials #37-#40 showed carries ~0.026 of Sharpe as sampling luck — so
differences smaller than that are not evidence. Here that matters less than
usual: the effect being measured is expected to be ~0.05, not ~0.005.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_hzn_avg4_k1",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Averaging four quarterly lookback-length vintages (12-1, 9-1, 6-1, "
        "3-1) as separate buffered magnitude-weighted portfolios while "
        "removing the six-tranche date overlap entirely (whole book reformed "
        "monthly), with band, weighting and daily vol-spike trim otherwise "
        "identical to trial #42, lands validation Sharpe materially above the "
        "1.066 of the same construction with a single composite score and no "
        "overlap (trial #28) net of 15 bps costs, because length-vintage and "
        "date-vintage diversity are substitutable routes to one mechanism "
        "rather than complements; landing at or below 1.066 falsifies that "
        "and shows horizon averaging only works on top of the date overlap."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 1  # <- the single change under test: date overlap switched off

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
