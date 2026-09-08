"""The same question as #85, with the breadth control actually working.

WHY THIS FILE EXISTS. #85 (`pt_depth_vs_vintage_breadth`) asked whether the
champion's breadth is bought by the DEPTH of one fresh ranking or by the TIMING
of six formation-date tranches, and it pinned its band on the **train** split:
41.59 names against the champion's 41.36, a 0.6% match. On validation the match
broke — **49.22 against 62.71, a 21% shortfall** — so the designed comparison did
not happen and #85's 1.166 is a reading at the wrong breadth.

The cause was my own error and it is worth stating because it is the general
rule, not an accident. #85's file argued "a single sort's book size is `m` and
does not depend on pool size, so the match carries to validation". The champion
is **not a single sort**: it is a union of four horizon legs across six date
tranches, and the union of a set operator grows with the pool, which goes 55 ->
126 names between the early train years and validation. So the incumbent
broadened and this book did not. 2026-09-06 already wrote the rule — "any
non-linear set operator must have its breadth pinned by construction" — and #85
applied it to the wrong side of the comparison: it checked that the *candidate*
would not de-broaden and never asked whether the *incumbent* would broaden.

This file changes exactly one expression: `CORE_N` 22 -> 30 (band ratio held at
the champion's 25/15 = 1.667, so `BAND_N` 37 -> 50). Nothing else moves.

BREADTH PINNED ON THE SPLIT THAT MATTERS, holdings-only, pre-registered. The
profiler used below reproduces the engine's champion `avg_positions` to 0.03
names (62.71 against the champion card's 62.69), so it can be trusted to pin a
band without scoring anything:

    core/band     15/25 K=6     22/37       26/43   28/47   30/50   32/53   34/57
                  (champion)    (#85)
    train  names     41.36      41.59       46.15   48.41   51.76   54.10   57.19
    VALID  names     62.71      49.22       56.04   59.53   62.50   65.68   69.39
    valid  HHI      0.0618     0.0529      0.0453  0.0420  0.0392  0.0367  0.0344

`30/50` gives **62.50 against 62.71, a 0.3% match**. That is the pin.

THE AXIS THAT STILL CANNOT BE MATCHED, AND WHY IT IS NOT A FIXABLE DEFECT. HHI
is 0.0392 against the champion's 0.0618, -37%. Breadth and concentration are
linked through the operator here — averaging six tranches piles weight onto the
names that repeat across them, so at any matched name count the vintage book is
the more concentrated one — and matching HHI instead would unmatch breadth. The
hypothesis is about breadth, so breadth is what is pinned, and the residual is
reported rather than corrected. One mitigating measurement from #85's
post-mortem: the *top* of the two books is far more alike than HHI suggests —
on validation month-ends **72.5% (champion) and 70.1% (#85) of capital sits in
the top 15 names**, so the HHI gap is a tail effect, not a different core.

WHAT #85 ESTABLISHED THAT THIS FILE BUILDS ON. Its "below 1.00" branch was
refuted decisively, and with the two K=1 books already on the board the depth
axis is now three points, monotone in breadth:

    K=1 book                         names   validation
    mom_hzn_avg4_nobuffer             30.3      1.229
    mom_hzn_avg4_k1_cohort_trim       35.1      1.201
    #85 pt_depth_vs_vintage_breadth   49.2      1.166
    THIS FILE                         62.5         ?
    champion (K=6)                    62.7      1.120

The slope is about **-0.033 of Sharpe per 10 names** and it is remarkably linear
over a 1.6x breadth span.

PRE-REGISTERED POINT ESTIMATE: **1.12**, read off that slope
(1.166 - 0.033 * (62.5-49.2)/10 = 1.122) and landing, by arithmetic rather than
by intention, within 0.002 of the champion's 1.120. I am recording that
coincidence in advance so it cannot be claimed afterwards.

BRANCHES NAMED IN ADVANCE. The paired `SE` against the seat at the `rho` #85
recorded (0.9497) is about 0.127, so "indistinguishable" means roughly +/-0.06
of one SE-scaled half-width; I am naming +/-0.06 around the champion.
  * **1.06 to 1.18** — depth and timing buy the *same* breadth. The overlap is
    then a breadth-generating device and nothing more, and the journal's
    "breadth is justified by timing" reading is **not** supported: what the
    six-tranche structure supplies is names, not better names. It would also
    corroborate the K=1 slope out of sample of its own fit.
  * **Below 1.06** — breadth bought by depth really is worse, the overlap earns
    its keep as a breadth mechanism, and the three-point slope over-predicted
    at the wide end.
  * **Above 1.18** — depth beats timing at matched breadth, so the overlap is a
    cost at every breadth on this split and its only remaining defence is the
    holdout behaviour that caused the human rollback. That would be the reading
    most worth putting in front of a human, and the one I least expect.

SECOND PRE-REGISTRATION, per the standing instruction. #85 read **under**
(train 0.939 -> validation 1.166), taking the record to n = 27. This book scores
on the same month-ends and the same history requirement, so it is admissible
too; I am predicting **under** again, because every K=1 momentum book on this
board has read under.

SCOUT, for the same three reasons as #85, the third still load-bearing: the four
promotions after trial #42 each raised validation Sharpe while holdout Sharpe
fell 1.377 -> 0.691, and the human rolled the seat back to K=6 for exactly that
reason. A K=1 `price-trend` challenger is a candidate on the path that rollback
rejected, and running one on the challenge track would risk spending a holdout
look to re-learn what the champion card already records. This is the session's
second and last `price-trend` trial; the cap is 2.
"""

from __future__ import annotations

import pandas as pd

STRATEGY = {
    "name": "pt_depth_breadth_pinned",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "Repeating #85's depth control with its band pinned on the split that matters — "
        "CORE_N/BAND_N 22/37 -> 30/50, the single expression that changes, giving 62.50 "
        "names against the champion's 62.71 on a profiler that reproduces the engine's "
        "champion avg_positions to 0.03 names, where #85 matched on train (41.59 vs "
        "41.36) and missed on validation (49.22 vs 62.71) — scores near 1.12, "
        "indistinguishable from the champion's 1.120, because the three recorded K=1 "
        "books fall monotonically in breadth (30.3 names 1.229, 35.1 names 1.201, 49.2 "
        "names 1.166, about -0.033 of Sharpe per 10 names) and that slope extrapolates "
        "to 1.122 at 62.5 names. Landing between 1.06 and 1.18 says depth and timing buy "
        "the SAME breadth, so the six-tranche overlap supplies names rather than better "
        "names and the journal's 'breadth is justified by timing' reading is not "
        "supported; below 1.06 says depth-bought breadth is genuinely worse and the "
        "overlap earns its keep; above 1.18 says the overlap is a cost at every breadth "
        "on this split and its only defence is the holdout behaviour behind the human "
        "rollback. HHI stays unmatched at 0.0392 against 0.0618 because breadth and "
        "concentration are linked through the operator and cannot both be pinned, though "
        "#85's post-mortem shows the two books' cores are alike (72.5% vs 70.1% of "
        "capital in the top 15 names) and the HHI gap is a tail effect."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 30            # #85 used 22; pinned here to the champion's VALIDATION breadth
BAND_N = 50            # band ratio held at the champion's 25/15 = 1.667
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 1         # champion 6 — the axis under test

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
