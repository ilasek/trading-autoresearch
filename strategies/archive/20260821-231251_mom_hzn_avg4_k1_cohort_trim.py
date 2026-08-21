"""Re-testing a "sampling luck" attribution on an independently re-drawn book.

WHAT TRIALS #37-#40 ESTABLISHED, AND WHAT THEY LEFT AS AN IOU. The champion's
daily vol-spike trim does not measure the basket it de-risks. Its filter,
`prices.iloc[:end_pos][names].dropna(axis=1, how="any")`, admits only names with
a complete history back to the store's 1962 start, so the trigger is driven by
the intersection of the held basket with an eleven-name old-economy cohort
(JNJ, PG, XOM, CVX, KO, MRK, DIS, IBM, CAT, GE, HON). Bracketing every
deliberate specification on the six-tranche base gave

    held basket 1.050  <  whole market 1.055  <  no trim 1.062
                       <  whole legacy cohort 1.081  <  held ∩ cohort 1.107

and the reading recorded in `learnings.md` was: the monotone ordering in
style-orthogonality is the mechanism (a momentum basket's own vol rises in
melt-ups as readily as in crashes, so measuring the thing you are de-risking is
the wrong signal), the deliberate cohort captures it, and **the residual +0.026
between the cohort and the accident "has no mechanism — treat it as sampling
luck."** That last clause is an attribution, not a measurement. It was made on
one book over one window and has never been tested.

WHY IT CAN BE TESTED NOW RATHER THAN ARGUED. Champion #43 carries the identical
accidental trigger onto a structurally different book: the date overlap is gone
and selection now runs through four independent horizon legs, so the monthly
held-set — and therefore the intersection that drives the trigger — has been
**re-drawn from a different process**. If the +0.026 really was luck in the
sampling of three defensives, it should not survive re-drawing; if it
reproduces at a similar size on the new book, then the intersection is doing
something systematic and the sampling-luck attribution in `learnings.md` is
wrong and should be retracted. This is the strongest form of experiment
available here — an out-of-sample test of a *claim the repo has already made*,
rather than another challenger.

PRE-TRIAL DIAGNOSTIC, RUN BEFORE THIS FILE WAS WRITTEN (holdings only, no
returns scored, prices truncated at 2023-12-31, trial count untouched). The
first thing it establishes is that the trial is not a no-op — the trap that
killed the book-weighted-vol re-specification for free last session, where the
two definitions disagreed on 1 of 1562 days. Over the validation window:

    champion (held ∩ cohort) trigger      65 firing days   (4.6%)
    deliberate whole-cohort trigger       99 firing days   (7.0%)
    days the two disagree                 40               (2.83%)
      champion fires, cohort does not      3
      cohort fires, champion does not     37
    disagreement by year   2018: 22, 2019: 2, 2020: 8, 2022: 8

Two things follow. (a) The champion's trigger is very nearly a strict *subset*
of the deliberate one, so this trial asks a clean directional question: is the
accident's edge that it de-risks *less often*? (b) The 37 extra de-risking days
land almost entirely in the three years that decide the result — 2018 and 2022
are the validation window's only loss years and 2020 is the +132% year that
dominates its P&L — so the two specifications are pulled in opposite
directions and the sign is genuinely open. The diagnostic also shows the
accident is far less degenerate on this base than on the one it was
characterised on: it qualifies a mean of **6.5 names and 20.7% of book weight**
here, against the 3 names and 11% recorded for the six-tranche champion, and it
never qualifies zero names in any month.

THE CHANGE, AND IT IS ONE CHANGE. The intersection with the held basket is
deleted from the trigger and the cohort is kept: exposure is scaled by the
equal-weighted realized vol of every instrument with a complete history from
the start of the price store to the formation date, held or not. Completeness
is evaluated on the trailing prefix only, so no ticker is hard-coded and no
future information is read — the cohort is whatever the store's own start date
implies at each formation. Signal, four horizon legs, per-leg buffer chains,
magnitude weighting, N_TRANCHES = 1, SPIKE_RATIO 1.6, TRIM_SCALE 0.6 and daily
evaluation are identical to the champion.

WHAT WOULD FALSIFY IT, AND WHY BOTH ANSWERS ARE WORTH THE TRIAL. The hypothesis
is that the deliberate cohort trigger lands at or above the champion's 1.187,
because the mechanism is the cohort and the intersection was luck. Landing
materially below it falsifies that, and does so informatively: a residual that
reproduces at similar size after the held-set has been re-drawn by an entirely
different selection process is not luck, and `learnings.md` would owe a
retraction of the sampling-luck clause plus a new question — what a
*membership-filtered* defensive cohort knows that the whole cohort does not.
Landing at or above 1.187 confirms the attribution and would additionally give
the repo a champion whose overlay is specified rather than accidental, which is
the state trials #37-#40 said it should be in.

CAVEATS RECORDED IN ADVANCE. (a) `learnings.md` warns not to build on the trim
without re-reading #37-#40; those trials were re-read in full before this file
was written, and this candidate is a re-test of their conclusion rather than a
new overlay idea — no threshold, cadence or scale is being tuned, and the two
constants are inherited untouched. (b) The validation window is a weak
discriminator inside this family and a difference of a few hundredths is inside
its noise; the pre-registered reading is therefore the *direction and size*
relative to the +0.026 the attribution has to explain, not whether the gate
fires. (c) The trim axis is expensive — five trials have now been spent on it —
so this is the last question this session will ask of it either way.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_k1_cohort_trim",
    "family": "regime switching",
    "hypothesis": (
        "Driving the champion's daily exposure trim from the realized vol of "
        "the whole full-history legacy cohort rather than from its accidental "
        "intersection with the held basket — four horizon legs, buffers, "
        "magnitude weighting, single-tranche formation, SPIKE_RATIO 1.6 and "
        "TRIM_SCALE 0.6 otherwise identical to the champion — lands validation "
        "Sharpe at or above the champion's 1.187 net of 15 bps costs, because "
        "trials #37-#40 attributed the intersection's residual +0.026 on the "
        "six-tranche base to sampling luck in which three defensives the "
        "momentum screen happened to hold, and champion #43 re-draws that "
        "held-set from an entirely different selection process (no date "
        "overlap, four independent horizon legs), so a genuinely lucky "
        "residual should not survive the re-draw; landing materially below "
        "1.187 falsifies the sampling-luck attribution and shows the "
        "membership filter is systematic."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
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
        # The champion's own filter with the basket intersection removed:
        # everything listed for the entire prefix as of the formation date.
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
