"""Bagging on the axis Breiman actually used: perturb which instruments the
selection sees.

WHY THIS IS THE LAST UNTRIED MEMBER OF THE FAMILY. The repo's strongest
mechanisms are all averages over vintages of one selection procedure, and
`research/SUMMARY.md` now names the mechanism: Breiman's aggregation result,
where the gain equals the base procedure's *instability* — the variance of the
fit across perturbed training sets — and where the canonical unstable procedure
is **subset selection**, "the variables competing for inclusion". That is
literally the champion's buffered top-N membership rule. The lab has perturbed
two things: the formation *date* (trial #32) and the lookback *length* (#41,
#42). It has never perturbed the thing Breiman perturbs — **the data the
procedure is fitted on**. On a cross-sectional selection problem the analogue
of resampling the training set is resampling the *instruments*.

THE CONSTRUCTION. Three deterministic leave-one-third-out folds, assigned by
column position mod 3, so every instrument is present in exactly two of three
folds and none is systematically under-represented. The champion's entire
construction — four horizon legs, per-leg buffer chains, magnitude weighting,
single-tranche formation, market-level cohort trim, both constants — is run
independently inside each fold, and the three resulting *portfolios* are
averaged at equal weight. Nothing is estimated: the fold assignment is fixed,
the weights across folds are equal, and no covariance, correlation or return
forecast is computed anywhere.

IT PASSES EVERY FREE SCREEN THE REPO AND THE RESEARCH FOLDER HAVE ACCUMULATED.
(1) Noisily-estimated parameters: zero. (2) Are the components estimates of the
same quantity, or different return streams? The same — one signal, one
construction, three data draws; this is the case forecast-combination theory
endorses, not the capital-dilution case it forbids. (3) Is the per-component
output nonlinear in the data? Yes, and maximally so: the buffered top-N
threshold is the canonical unstable procedure, so averaging portfolios is not
the portfolio of averaged scores. (4) Which `IR = mean(IC)/sqrt(σ_IC² + φ/N)`
term does it move? It lowers `σ_IC` by averaging weakly-correlated draws — and,
stated against itself, it also *lowers* `mean(IC)`, because each fold picks its
top 15 from ~93 instruments rather than 140 and therefore holds a strictly
weaker selection. That trade is the trial. (5) Group neutralisation: not
applicable, no group constraint is imposed.

PRE-TRIAL DIAGNOSTIC (holdings only, no returns scored, prices truncated at
2023-12-31, 72 validation months, trial count untouched):

    fold-to-fold weight overlap        0.428 / 0.423 / 0.483
    bagged vs champion overlap                         0.851
    L1 disagreement vs champion   core (top-10) 0.140, fringe 0.159
    avg positions                              35.1 -> 53.3
    mean top weight                          0.1717 -> 0.1205
    mean weight HHI                          0.0753 -> 0.0482
    monthly target turnover                   0.303 -> 0.280
    top-name RISK share                      0.3094 -> 0.2252
    effective bets by weight / by risk    13.3 / 6.0 -> 20.7 / 9.9

Two readings, both of which had to hold before this file was written. First,
the folds genuinely disagree: 0.43-0.48 pairwise, against 0.645 for date
vintages and 0.963 for the buffer-band vintages this same diagnostic run killed
for free tonight. Second — and this is the criterion tonight's rejected trial
established — the disagreement is in the **core**, not the fringe: 0.140 of L1
distance sits in the champion's own top-10 names against 0.159 across all the
rest. A name absent from a fold cannot be selected in it, so subsampling
re-draws the whole held-set rather than shuffling a low-weight tail, which is
exactly what perturbing a threshold on one ranking failed to do.

THE HONEST PRIOR IS NOT FAVOURABLE, AND IS STATED BEFORE THE RUN. Three things
argue against. (a) `learnings.md` has priced de-concentration at roughly -0.02
Sharpe every time the extra flatness did not arrive from a decorrelated vintage,
and weight HHI falls 36% here. (b) Each fold selects from two-thirds of the
universe, a direct `mean(IC)` loss with no offsetting term of its own. (c)
Buja-Stuetzle's counterweight, recorded in `research/SUMMARY.md`: squared
plug-in bias *always* rises under aggregation, variance only *usually* falls,
and bagging a procedure that is not unstable enough is mildly harmful rather
than neutral. The case for spending the trial is that (b) and (c) are exactly
what cannot be settled on paper, while everything that can be settled on paper
has been.

WHAT WOULD FALSIFY IT, ON TWO AXES RATHER THAN ONE. The hypothesis is that
validation Sharpe lands at or above the champion's 1.201; landing materially
below it says the smaller selection pool's bias exceeds the aggregation gain,
Buja-Stuetzle's crossover binds, and the subsample axis closes. Independently
of the gate, this is the first mechanism the repo has measured that nearly
halves top-name risk share (30.9% -> 22.5%, effective risk bets 6.0 -> 9.9),
where sector-neutral scoring and basket-breadth widening both failed to move
validation maxDD at all. So if maxDD does *not* improve materially on -28.7%,
that falsifies the standing `learnings.md` conjecture that the drawdown is
inherent to the magnitude-weighting mechanism, and points instead at the
underlying signal's tail behaviour. Both answers are recorded either way.

COMMITMENTS. One fold count is tried and no ladder follows: three folds is the
coarsest partition that keeps each pool large enough for a top-15 cut to remain
a top-16% selection, and `research/SUMMARY.md` records that replicate counts
saturate fast (most of Breiman's gain by ~10, nothing after ~25), so a deeper
stack would have to pre-register a small effect. A caveat that must travel with
the result: the fold partition is one arbitrary draw, so a small Sharpe gap
should be read with the same timing-luck discipline the folder applies to
rebalance dates.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_subsample_bag3",
    "family": "combinations",
    "hypothesis": (
        "Running the champion's entire construction independently inside three "
        "deterministic leave-one-third-out instrument folds and averaging the "
        "three portfolios at equal weight — four horizon legs, buffers, "
        "magnitude weighting, single-tranche formation, market-level cohort "
        "trim and both constants unchanged within each fold — lands validation "
        "Sharpe at or above the champion's 1.201 net of 15 bps costs, because "
        "buffered top-N membership is the canonical unstable procedure whose "
        "aggregation gain equals its instability, and perturbing which "
        "instruments the selection sees re-draws the held-set in its core "
        "(fold-to-fold weight overlap 0.43-0.48, core L1 disagreement 0.140 "
        "against 0.159 in the whole fringe) rather than shuffling a low-weight "
        "tail; landing materially below 1.201 shows the bias from each fold "
        "picking its top 15 out of ~93 instruments rather than 140 exceeds the "
        "variance reduction, and closes the subsample-vintage axis."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_FOLDS = 3

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
    all_dates = prices.index
    max_lb = max(LOOKBACKS)

    # Deterministic folds: every instrument sits in exactly N_FOLDS - 1 of them.
    folds = [
        [c for k, c in enumerate(prices.columns) if k % N_FOLDS != f]
        for f in range(N_FOLDS)
    ]
    held = {(f, lb): set() for f in range(N_FOLDS) for lb in LOOKBACKS}

    rows = {}
    base_periods = []
    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < max_lb + SKIP + 1:
            continue

        fold_targets = []
        for f in range(N_FOLDS):
            sub = hist[folds[f]]
            moms = {lb: _momentum(sub, lb) for lb in LOOKBACKS}
            common = None
            for m in moms.values():
                common = m.index if common is None else common.intersection(m.index)
            if len(common) < CORE_N:
                continue
            leg_targets = []
            for lb in LOOKBACKS:
                score = _zscore(moms[lb][common])
                t, held[(f, lb)] = _leg_target(score, held[(f, lb)])
                leg_targets.append(t)
            ft = pd.concat(leg_targets, axis=1).fillna(0.0).mean(axis=1)
            fold_targets.append(ft / ft.sum())

        if not fold_targets:
            continue

        blended = pd.concat(fold_targets, axis=1).fillna(0.0).mean(axis=1)
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
        # Market-level trigger, copied verbatim from the champion.
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
