"""Should the four averaged lookback windows fill the 3-1..12-1 interval
*evenly*?

THE ONE QUESTION BOTH #42 AND THE 2026-08-17 SESSION SUMMARY LEFT EXPLICITLY
OPEN. Trial #42's docstring and the session summary that followed it both
closed the bracket-*width* question (comparing a fifth or sixth window is the
sweep the manual forbids; the interval is pinned at both ends by the skip-month
below and post-formation reversal above) while recording one thing as still
live and requiring its own rationale: whether the windows should fill that
fixed interval evenly. This candidate supplies the rationale and spends one
trial on it. It changes no endpoint and adds no window.

THE ARGUMENT, WHICH IS ABOUT REDUNDANCY BEING A RATIO AND NOT A DIFFERENCE.
All four legs end at the same skip point and extend back different distances,
so two legs of length L1 < L2 do not merely resemble each other — the shorter
window's entire formation period is a *subset* of the longer one's. The
fraction of L2's data that L1 also reads is exactly L1/L2. Redundancy between
adjacent legs is therefore governed by the ratio of their lengths, and evenly
spaced windows do not space that ratio evenly: 63/126/189/252 has adjacent
ratios 2.00, 1.50, 1.33, so the long end of the bracket is sampled roughly
twice as densely, in information terms, as the short end. Uniform spacing is
uniform in the wrong coordinate.

WHY THAT MATTERS RATHER THAN BEING A CURIOSITY. The construction averages the
four legs at *equal weight*, and `learnings.md` records that those equal
weights are load-bearing — "weight the better window more" is the
estimated-weight mistake the forecast-combination literature warns against, and
that verdict is not under review here. But equal weighting is the optimal
combination precisely when the components are exchangeable: equal variance and
equal pairwise correlation. Uniform spacing violates the second condition by
construction, and the violation is systematic rather than random — it always
over-weights the long end, because that is where the ratios bunch. Geometric
spacing restores exchangeability without estimating anything from the data,
which keeps the noisily-estimated-parameter count at zero (the screen
`research/SUMMARY.md` candidate #1 asks any weighting proposal to pass) while
letting the equal weights the repo already committed to actually be the right
weights.

THE CHANGE, AND IT IS ONE CHANGE. `LOOKBACKS` goes from (252, 189, 126, 63) to
(252, 159, 100, 63) — the geometric interpolation between the same two
endpoints, adjacent ratios all equal to 4**(1/3) = 1.587. Same bracket, same
number of windows, same skip, same hold-25/enter-15 band, same
`c - c.min() + FLOOR` weighting, same per-leg buffer chains, same equal
weighting between legs, same N_TRANCHES = 1, same daily vol-spike trim.
Nothing is chosen by performance: the interior points are fixed by the
endpoints and the count, exactly as the uniform ones were. This is the only
alternative spacing that will be tried, in this session or as a follow-up
ladder — a third spacing would be the sweep, and there is no third
non-arbitrary rule.

PRE-TRIAL DIAGNOSTIC, RUN BEFORE THIS FILE WAS WRITTEN (holdings only, no
returns scored, prices truncated at 2023-12-31, trial count untouched). Over
the 72 validation months the two spacings give:

    adjacent-pair weight overlap   uniform [0.641, 0.580, 0.469]  sd 0.0711
                                 geometric [0.557, 0.543, 0.546]  sd 0.0060
    mean pairwise weight overlap   0.4748 -> 0.4639
    mean pairwise rank correlation 0.6692 -> 0.6605
    mean union name count          35.1   -> 35.6

So the mechanism is confirmed to exist and confirmed to be *only* what the
argument claims: exchangeability is essentially restored (dispersion of
adjacent overlap falls 12x), while breadth is untouched (35.1 -> 35.6 names),
which rules out the confound that has explained several previous results here —
this cannot be a de-concentration effect wearing another name, because there is
no de-concentration. The honest reading of the same table is that the *level*
of redundancy barely moves (-0.011 mean overlap), so the expected effect is
small, and it is recorded as small in advance rather than discovered to be
small afterwards.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below the champion's 1.187.
Given the pre-registered small effect size, that is the likely outcome, and it
is worth stating what the trial buys in that case: it closes the last axis of
the horizon-averaging family that the previous two sessions deliberately left
open, with a decisive answer — if equalising the redundancy structure of the
legs changes nothing measurable, then interior spacing is not a live variable
and the family's remaining questions are all about what is averaged, not about
where the windows sit. A *large* move in either direction would be the
surprising result and, per `learnings.md`, a large validation jump inside this
family is evidence of overfitting until corroborated, not evidence of progress.

CAVEAT RECORDED IN ADVANCE. The champion was promoted on a validation margin
of +0.067 over trial #42 while its holdout went the other way, and the standing
learnings entry says this window is a weak discriminator inside this family
that rewards concentrated, fast-rotating books. Whatever this trial returns on
validation should be read with that discount; the diagnostic above, not the
Sharpe, is the part of this experiment that is measured rather than sampled.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_hzn_geom4_k1",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Spacing the four averaged lookback windows geometrically between the "
        "same endpoints (252, 159, 100, 63 trading days, adjacent ratios all "
        "4**(1/3)) instead of evenly (252, 189, 126, 63), with bracket "
        "endpoints, window count, skip, band, weighting, per-leg buffers, "
        "single-tranche formation and daily vol-spike trim otherwise identical "
        "to the champion, raises validation Sharpe above the champion's 1.187 "
        "net of 15 bps costs, because redundancy between two nested formation "
        "windows is governed by the ratio of their lengths rather than their "
        "difference — uniform spacing therefore samples the long end of the "
        "bracket roughly twice as densely and leaves the legs non-exchangeable "
        "(adjacent-pair weight overlap 0.641/0.580/0.469), which is the exact "
        "condition under which the equal weights the construction already uses "
        "are the wrong ones; landing at or below 1.187 falsifies that and "
        "shows interior spacing is not a live variable."
    ),
}

LOOKBACKS = (252, 159, 100, 63)  # <- the single change: geometric, not uniform
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 1

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
