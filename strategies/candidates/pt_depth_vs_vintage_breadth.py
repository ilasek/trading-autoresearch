"""Is the champion's breadth bought by DEPTH or by TIMING? The missing cell.

WHY THIS FILE EXISTS. `experiments/journal.md` has carried the same idea as its
#2 and #3 ranked next-idea for two consecutive sessions and no session has run
it: 2026-09-06 measured that the incumbent's 4-horizon momentum score **fails**
the Patton-Timmermann monotonic-relation test (`p` = 0.698) while its top bin
carries +8.02%/yr at `t` = +3.76 — it picks one corner rather than ranking — yet
the book holds ~62.7 names, about 45% of the universe. The journal's own reading
is that "the incumbent's breadth is justified by timing rather than by its own
current score, and no session has tested that reading directly."

This file tests it directly, and it is the missing cell of a comparison whose
other three cells are already recorded.

THE CONFOUND THIS REMOVES, WHICH IS THE REASON THE EXISTING TRIALS DO NOT ANSWER
IT. Two K=1 books are on the board and both **beat** the champion on validation:
`mom_hzn_avg4_k1_cohort_trim` 1.201 (35.1 names) and `mom_hzn_avg4_nobuffer`
1.229 (30.3 names), against the seat's 1.120 (62.7 names). But both hold
`CORE_N` = 15 / `BAND_N` = 25 — the champion's own narrow band — so switching off
the six-tranche overlap moved **selection and breadth together**, which is
exactly the error 2026-09-06 named ("book size is a property of the operator,
not of the band") and exactly what makes a mechanism question unanswerable. No
K=1 book has ever been run at the champion's breadth. This is that book.

    cell                          K   core/band   names (one profiler)   validation
    champion                      6      15/25          41.36              1.120
    mom_hzn_avg4_k1_cohort_trim   1      15/25          28.89              1.201
    mom_hzn_avg4_nobuffer         1      15/25 (no buf) ~28.9              1.229
    THIS FILE                     1      22/37          41.59                 ?

THE FREE SCREEN THAT MOTIVATES THE POINT ESTIMATE, measured on train before this
file was written — marginal excess of each rank slice of the champion's own
score over its scoreable pool, forward 21 days, 215-299 month-ends, mean pool
96.2:

    slice    1-15     16-30     31-45     46-62
    %/yr    +5.55     -0.34     -0.32     -0.75
    t       +1.94     -0.18     -0.25     -0.55

The score carries **everything in its top ~15 of ~96 and nothing after** — every
marginal slice past the first is negative and none is distinguishable from zero.
Top-5 is +13.39%/yr (`t` = +3.06), top-15 +5.12%, top-62 +0.98% (`t` = +0.88).
So a book that buys its 62 names by reading further down one ranking is filling
~47 of them from slices with negative marginal excess, while the six-tranche
overlap fills the same breadth with six draws from the +5.55%/yr top slice taken
at six different formation dates.

The same screen run on the seated `liquidity-volume` lead's score gives
+7.80 / +2.96 / +1.75 / -0.99 — content out to ~45 names — and on a placebo hash
reading no market data gives +0.98 / -1.17 / +2.09 / -1.90, i.e. no structure.
The placebo is why the momentum profile is read as a shape and not as noise.

BREADTH IS MATCHED BY CONSTRUCTION, HOLDINGS-ONLY, ON TRAIN. The band is the one
number that moves: `CORE_N` 15 -> 22 with the band ratio held at the champion's
25/15 = 1.667, giving 41.59 names against the champion's 41.36 on one consistent
profiler — a 0.6% match. A single sort's book size is `m` and does not depend on
pool size, so unlike 2026-09-06's intersection this band does not de-broaden as
the universe grows, and the match carries to validation.

    core/band    20/33   21/35   22/37   23/38   24/40      champion 15/25 x K=6
    names        38.62   40.29   41.59   42.55   43.88            41.36

THE ONE AXIS THAT DOES NOT MATCH, STATED PLAINLY. HHI is 0.0500 against the
champion's 0.0636, a -21% de-concentration: averaging six tranches piles weight
onto names that repeat across them, and one deep sort spreads more evenly at the
same name count. I am not correcting for it and I am not predicting its sign.
The lab's two concentration brackets point opposite ways — widening was
monotonically *good* in `liquidity-volume` (0.874/0.917/0.942) and every
vintage-averaging axis that lowered HHI *lost* in `price-trend` — and 2026-09-06
concluded the calibration is a property of a construction, not of a family. So
this residual is a caveat on the reading, not a term in it.

EVERYTHING ELSE IS BIT-IDENTICAL TO `strategies/champion.py`: the same four
lookbacks (252, 189, 126, 63) with the same 21-day skip, the same per-leg
cross-sectional z-score, the same hysteresis buffer, the same magnitude
weighting (`score - min + 0.05`, normalised), the same equal-weight average over
the four horizon legs, the same 25% cap and renormalisation, and the same daily
vol-spike trim (21d/252d basket vol ratio > 1.6 -> scale 0.6). `N_TRANCHES` goes
6 -> 1 and `CORE_N`/`BAND_N` go 15/25 -> 22/37. Nothing else is touched.

PRE-REGISTERED POINT ESTIMATE: **0.95**, against the champion's 1.120 and the
narrow K=1 pair's 1.201/1.229. The reasoning: the depth book's mean held name
carries roughly (15*5.55 + 47*(-0.47))/62 ~ +1.0%/yr of pool excess against
+5.55%/yr for a fresh top-15, and the standing rule that a cross-sectional
screen over-predicts the book it motivates by about an order of magnitude cuts
the gap rather than the level.

BOTH BRANCHES ARE NAMED IN ADVANCE AND BOTH ARE INFORMATIVE.
  * **Below ~1.00** — breadth bought by depth is materially worse than breadth
    bought by timing. The overlap is then earning its keep as a *breadth
    mechanism* even though it costs 0.094 against a narrow K=1 book, the
    2026-09-06 monotonic-relation result is cashed at book level rather than at
    screen level, and the incumbent's construction is matched to where its own
    score's content actually lives.
  * **1.00 to 1.12** — the two breadth mechanisms are inside this split's
    resolution floor. The overlap is then a way of getting breadth and not more,
    and the honest statement is that the timing story is unresolvable here.
  * **Above ~1.12** — depth beats vintage at matched breadth, the incumbent's
    stated mechanism is mis-described, and the 0.094 the overlap costs against
    narrow K=1 is not buying breadth quality. That would be the most surprising
    outcome and the one most worth having.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record
its train Sharpe as a prediction of its validation Sharpe. This book scores on
the same month-ends and the same 252+21-day history requirement as the champion,
so unlike the 2026-09-06 pair it **is** admissible to that record.

SCOUT, DELIBERATELY. Three reasons, and the third is the load-bearing one.
(i) The question is about the incumbent's mechanism, not about the seat.
(ii) A scout never reaches the holdout gate, so this cannot end the session.
(iii) The four promotions after trial #42 each raised validation Sharpe while
holdout Sharpe fell 1.377 -> 0.691, and the human rolled the seat back to K=6
for exactly that reason. A K=1 price-trend challenger is a candidate on the path
that rollback rejected; running one on the challenge track would risk spending a
holdout look to re-learn a lesson the champion card already records.
"""

from __future__ import annotations

import pandas as pd

STRATEGY = {
    "name": "pt_depth_vs_vintage_breadth",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "A book that buys the champion's breadth from the DEPTH of one fresh momentum "
        "ranking — K=1 with CORE_N/BAND_N widened 15/25 -> 22/37 so it holds 41.59 names "
        "against the champion's 41.36 on one holdings-only profiler, every other element "
        "of `strategies/champion.py` bit-identical — scores near 0.95 on validation, "
        "materially below the champion's 1.120 and far below the narrow K=1 pair's "
        "1.201/1.229, because the incumbent's score fails the monotonic-relation test "
        "(p = 0.698) and its marginal train excess by rank slice is +5.55%/yr for names "
        "1-15 and then -0.34/-0.32/-0.75%/yr for 16-30/31-45/46-62: the score carries "
        "everything in its top ~15 of a ~96-name pool and nothing after, so ~47 of this "
        "book's 62 names are filled from slices with negative marginal excess while the "
        "six-tranche overlap fills the same breadth with six draws from the top slice at "
        "six different formation dates. This is the missing cell of a comparison whose "
        "other three are recorded — both existing K=1 books hold the champion's narrow "
        "15/25 band, so switching the overlap off moved selection and breadth together. "
        "Below ~1.00 says breadth-by-timing beats breadth-by-depth and the overlap earns "
        "its keep as a breadth mechanism; 1.00-1.12 says the two are inside the "
        "resolution floor and the timing story is unresolvable here; above ~1.12 says "
        "depth wins at matched breadth and the incumbent's mechanism is mis-described."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 22            # champion 15; widened so K=1 reproduces the champion's breadth
BAND_N = 37            # band ratio held at the champion's 25/15 = 1.667
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
