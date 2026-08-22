"""The champion's second concentration channel, never isolated — and the trial
that adjudicates a constant this repo has used to net out confounds three times.

TWO CHANNELS, ONE MEASURED. The champion's final weight for a name is
`mean_k w_{i,k}` over four horizon legs, with `w_{i,k} = 0` where leg k does not
hold i. That is a product of two distinct concentration mechanisms:

    (agreement)  how many of the four legs picked the name at all, and
    (magnitude)  how strongly the legs that did pick it sized it.

Trial #52 deleted the second last night and lost **0.206** of validation Sharpe —
2.5x what the same deletion was worth on the single-leg base of trials #18-#21,
which is the opposite of what the buffer result (#51) predicted by analogy, and
the reason this file exists: if four-leg averaging *amplifies* a concentration
channel rather than absorbing it, then the channel that only exists because there
are four legs has never been looked at. Agreement is that channel. It is
load-bearing by construction — a name all four legs hold receives four times the
base weight of a name one leg holds — and the measured distribution is not a
formality:

    names held by 1 leg   8.45      names held by 3 legs   4.68
    names held by 2 legs  5.54      names held by 4 legs   6.61

DELETING IT EXACTLY, WITH NO KNOB. Weight each name by the mean of its leg
weights taken over **only the legs that hold it**,

    w_i  ∝  (Σ_k w_{i,k}) / |{k : i ∈ leg k}|

so every leg's own magnitude sizing survives untouched, the union membership is
unchanged, and the four-way agreement premium is removed. There is no second
value of this to try.

PRE-TRIAL DIAGNOSTIC (holdings only, prices truncated 2023-12-31, no returns
scored, trial count untouched):

                          champion    this file
    avg positions           30.30       30.30      <- bit-identical, breadth fixed
    HHI                    0.0943      0.0699      (-26%)
    top weight              0.200       0.158
    ann turnover            8.22x       9.18x      (+12%)
    effective risk bets      5.99        7.73      (+29%)
    N_cond (Meucci)          5.63        5.60      (-0.6%)
    mean weight overlap             0.8176

WHY THIS IS WORTH A TRIAL AND IS NOT KNOB-TURNING: the two available calibrations
of this repo's most-quoted rule of thumb disagree by a factor of four about this
exact change, and the constant is load-bearing.

  - `learnings.md` prices de-concentration at **~0.02 Sharpe per ~30% of HHI**
    whenever the flatness does not arrive from a decorrelated vintage. At -26%
    HHI that is -0.017, and with the turnover rise (+0.96x, ~0.006) the standing
    constant predicts **1.206**.
  - Trial #52 is the only calibration ever measured on *this* base: -55% of HHI
    cost 0.206 of Sharpe. Scaled to -26% that is -0.097, predicting **1.132**.

That constant was used to net out the concentration confound in the
pre-registrations of #50 and #51, and to kill the fixed-anchor idea for free
without a trial. If it is four times too small, three past readings were wrong in
the same direction and the repo should stop quoting it. **Pre-registered point
estimate: 1.13**, the figure derived from this base rather than from the old one.

  - near 1.13 -> the standing constant understates the cost of de-concentration
    on this base by ~4x, and #52's loss was mostly the concentration channel.
  - near 1.21 -> the standing constant is right, and the corollary is the more
    interesting one: #52's 0.206 then cannot be attributed to concentration at
    all, so magnitude weighting carries real cross-sectional signal rather than a
    concentration tilt — the square-root-dampening finding re-established at a
    different point and on the current base.
  - at or above 1.229 -> the agreement premium is not earning its seat, and the
    four-leg construction's value is breadth-from-disagreement rather than
    weight-from-agreement, which would refine `learnings.md`'s #41/#42 entry.

SECOND PRE-REGISTERED FALSIFIER — a quantitative replication of the referee #52
settled. Last night the Herfindahl-over-marginal-risk-contributions count and the
Meucci conditional count disagreed maximally (+195% against -2.6%) and validation
maxDD moved -29.6% -> **-24.3%**, the repo's best ever: the contribution count was
right and the Meucci count was wrong. Here they disagree again in the same
direction but at a seventh of the size (+29% against -0.6%). If the contribution
count is measuring something real and roughly linearly, maxDD should land near
**-28.8%** (29/195 of last night's 5.3pp gain). Landing there replicates the
statistic quantitatively rather than only in sign; landing at or worse than the
champion's -29.6% says last night's agreement was a coincidence of a very large
effect and the statistic should not be trusted at the effect sizes this repo
actually works at.

WHAT THIS FILE DOES NOT DO. It tunes nothing. Signal, four horizon windows,
skip-month, hard top-15 membership per leg, the within-leg magnitude transform
and its FLOOR, single-tranche formation, cohort trim and both trim constants are
inherited untouched. Only the cross-leg aggregation rule changes, and it changes
by deletion rather than by re-parameterisation.
"""

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_noagree",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Deleting the cross-leg agreement premium from the champion — weighting "
        "each name by the mean of its leg weights taken over only the legs that "
        "hold it, so a name all four horizon legs pick no longer receives four "
        "times the base weight of a name one leg picks, with membership "
        "(30.30 average positions, bit-identical), signal, skip-month, the "
        "within-leg magnitude transform, single-tranche formation, cohort trim "
        "and both trim constants otherwise untouched — lands validation Sharpe "
        "near 1.13 net of 15 bps costs. That figure is trial #52's calibration "
        "of de-concentration on this base (-55% HHI cost 0.206 Sharpe, scaled to "
        "this change's -26% HHI) plus a ~0.006 turnover cost; the standing "
        "constant in learnings.md (~0.02 Sharpe per 30% HHI) instead predicts "
        "1.206, and the two disagree by a factor of four about the same change, "
        "so the trial adjudicates a constant used to net out confounds in the "
        "pre-registrations of #50 and #51 and to kill the fixed-anchor idea for "
        "free. Landing near 1.21 rather than 1.13 says the constant is right and "
        "that #52's loss was therefore not concentration but real signal in the "
        "magnitude transform. Second falsifier on the unscored axis: effective "
        "risk bets rise 5.99 -> 7.73 (+29%) against the Meucci count's -0.6%, a "
        "seventh of the disagreement #52 resolved in the contribution count's "
        "favour, so validation maxDD should land near -28.8% if that statistic "
        "is roughly linear rather than only directionally right."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
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


def _leg_target(score: pd.Series) -> pd.Series:
    """Unchanged from the champion: the current top CORE_N, magnitude-weighted."""
    ranked = score.sort_values(ascending=False)
    held = list(ranked.index[:CORE_N])
    c_held = score[held]
    raw = c_held - c_held.min() + FLOOR
    return raw / raw.sum()


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
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
            leg_targets.append(_leg_target(score))

        legs = pd.concat(leg_targets, axis=1).fillna(0.0)
        # The champion divides by the number of legs (a plain mean), which pays a
        # name for being picked by many. Divide by the number of legs that
        # actually hold it instead: the agreement premium is removed and each
        # leg's own magnitude sizing is preserved.
        n_holding = (legs > 0).sum(axis=1)
        target = legs.sum(axis=1) / n_holding.replace(0, np.nan)
        target = target.fillna(0.0)
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
