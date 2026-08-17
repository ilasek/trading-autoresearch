"""Average the two horizon legs as *portfolios* rather than as scores.

THE STANDING QUESTION. `learnings.md` records that the champion's edge comes
from temporal breadth — six overlapping monthly formation vintages of one
signal — and that "breadth only pays when it comes from decorrelated
formation dates, not from more names chosen at one date". The journal's own
open item (2026-08-16, idea #1) sharpens it: formations one month apart share
11/12 of their 12-1 lookback window, so the six vintages are far from
independent, and what *else* supplies decorrelated vintages — without being a
K sweep — is unanswered. `research/SUMMARY.md` candidate #7 names the same
gap from the literature side: the averaging-over-estimation-windows method
(Pesaran-Timmermann) averages a model estimated over different *window
lengths*, whereas the champion averages over *end-dates* at constant length.

THE CHANGE, AND IT IS ONE CHANGE. The champion collapses its two lookbacks
into a single score before selecting anything: `composite = z(12-1) + z(6-1)`,
then one buffer, one held-set, one magnitude-weighted basket. This candidate
keeps every ingredient and moves the averaging one level up — each horizon
gets its own buffer chain, its own held-set and its own magnitude-weighted
target vector, and the month's target is the equal-weighted average of the
two. Nothing else moves: same lookbacks (252/126), same skip (21), same
hold-25/enter-15 band, same `c - c.min() + FLOOR` weighting, same six-tranche
date overlap, same daily vol-spike trim. Equal weights between the legs are
load-bearing, not a default — `research/SUMMARY.md` records that estimating
combination weights is the one move this whole literature warns against.

WHY IT IS NOT THE REFUTED "BLEND IT WITH SOMETHING". The capital-dilution tax
in `learnings.md` was measured blending momentum with a *different, weaker
return stream* (the ~0.5-Sharpe ETF sleeve). The standing design test in
`research/SUMMARY.md` (#2) asks whether the components are estimates of the
same quantity or different return streams: two lookback windows of one
momentum signal are estimates of the same quantity, which is the case
forecast-combination theory endorses and the case six formation vintages
already pass.

PRE-TRIAL DIAGNOSTIC (holdings only, no returns scored, prices truncated at
2023-12-31 — this cost no trial). Over 606 formations: the two legs'
cross-sectional scores rank-correlate 0.66 (0.69 in the validation window),
far below the 0.89 that killed an earlier inter-signal ensemble by diagnostic
alone; as *portfolios* the 12-1 and 6-1 baskets share only 0.60 of weight
(0.47 in validation). The averaged pair overlaps the champion's composite
basket 0.91 (0.85 in validation) and holds 24.6 names per formation against
19.5 — a real change, not a no-op, and not a wholesale one. For scale, the
champion's own date-tranches already overlap 0.51 at lag 5 (0.35 in
validation), so horizon diversity is a roughly independent second axis rather
than a duplicate of the one already exploited.

WHAT WOULD FALSIFY IT. Validation Sharpe lands at or below the champion's
1.107 — meaning score-level compositing already extracts whatever the two
windows jointly know, and portfolio-level averaging only de-concentrates the
book (which `learnings.md` prices at roughly 0.02 of Sharpe per step down the
concentration dial, bought with drawdown).

CAVEAT RECORDED IN ADVANCE. Trials #37-#40 established that the daily
vol-spike trim reads `held ∩ legacy-cohort`, and that roughly 0.026 of the
champion's Sharpe is sampling luck in that intersection. Widening the book
from ~34 to ~42 names perturbs that intersection, so a *small* Sharpe
difference either way is not clean evidence about the mechanism under test.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_hzn_avg",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Averaging the 12-1 and 6-1 momentum legs as separate buffered, "
        "magnitude-weighted target portfolios — rather than summing their "
        "z-scores into one score before selecting a single basket — with the "
        "six-tranche date overlap, buffer band, weighting and daily vol-spike "
        "trim otherwise identical to the champion, raises validation Sharpe "
        "above the champion's 1.107 net of 15 bps costs, because the two "
        "lookback windows are decorrelated estimates of the same quantity "
        "(rank correlation 0.66, portfolio weight overlap 0.60) and averaging "
        "them at the portfolio level supplies a second axis of vintage "
        "diversity that date-spacing alone cannot, whereas score-level "
        "compositing discards it by collapsing to one basket."
    ),
}

LOOKBACKS = (252, 126)
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
    """One horizon leg: buffer its own held-set, magnitude-weight it."""
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
    recent_targets = []  # up to N_TRANCHES most recent monthly target vectors
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

        # One buffered, magnitude-weighted portfolio per lookback window, then
        # average the portfolios at equal weight (never the scores).
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
