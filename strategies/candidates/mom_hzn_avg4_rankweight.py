"""Is the champion's within-leg magnitude weighting ordering, or spacing?

THE QUESTION THIS FILE EXISTS TO SPLIT. Trials #52 and #53 decomposed the
champion's two concentration channels one night apart, with membership held
bit-identical in both, and between them left exactly one quantity unresolved.
#53 deleted the cross-leg agreement premium: HHI -26%, cost 0.043, which
restated this repo's de-concentration constant at **~0.05 Sharpe per 30% of
HHI** (2.5x the ~0.02 `learnings.md` had been quoting). #52 deleted the
within-leg magnitude transform, each leg equal-weighting its top 15: HHI -55%,
cost **0.206**. At #53's rate the -55% should have cost 0.090, so

    ~0.117 Sharpe of the magnitude transform is NOT concentration.

It is real cross-sectional information in the composite z-scores inside a leg's
top-15. What is not known — and what last session's journal named as the one
decomposition it opened and could not close — is whether that 0.117 is the
score's **ordering** (name A ranks above name B) or its **spacing** (by how much
A beats B). Both survive the equal-weight deletion together, because equal
weighting discards both at once.

THE ISOLATING CONSTRUCTION. Linear rank weighting inside each leg: the leg's
top-15 by composite z-score receive raw weights 15, 14, ..., 1, normalised.
Ordering is preserved exactly; spacing is discarded entirely — the gaps between
adjacent z-scores no longer enter the weight at all, only their order does. This
is the repo's own definition of rank weighting, taken unchanged from trial #19
(`mom_rankweighted_buffered`), so the two are comparable. Everything else is
inherited untouched from the champion: the four horizon legs 252/189/126/63, the
skip-month, `held = current top 15` per leg with no membership band, equal-weight
averaging across legs, single-tranche formation, the cohort trim and both trim
constants. One line changes.

The three books therefore sit in a strict nesting:

    equal weight (#52)   neither ordering nor spacing   1.023
    THIS FILE            ordering, no spacing             ?
    champion             ordering and spacing           1.229

PRE-TRIAL DIAGNOSTIC, RUN BEFORE THIS FILE WAS WRITTEN (holdings only: weight
matrices on prices truncated at 2023-12-31, no portfolio return series ever
formed, trial count untouched). It reproduces the repo's recorded figures for
the two known books exactly, which is what licenses reading the third column:

                        positions     HHI    top_w  turnover  top_risk  eff_bets
    champion              30.2977   0.0918   0.197    7.45      0.367      5.99
    #52 equal weight      30.2977   0.0425   0.066    7.16      0.118     17.67
    THIS FILE  rank       30.2977   0.0582   0.109    7.45      0.194     11.49

    membership bit-identical to the champion on every validation day: True
    mean weight overlap vs champion 0.831, vs #52 0.808
    turnover change vs champion: -0.005x annual, i.e. nil

Three readings fix the pre-registration.

(a) **The confound is quantified in advance and it is the whole reason for the
interval.** Rank weighting cuts HHI by 36.6%, which is 68% of the way from the
champion to #52. At #53's restated constant that is a **0.061 Sharpe
de-concentration cost** carried by this file for reasons that have nothing to do
with ordering or spacing.

(b) **The two endpoints of the decomposition, stated before the run.** If the
whole 0.117 is *ordering*, this file keeps it and pays only (a):
**1.229 - 0.061 = 1.168**. If the whole 0.117 is *spacing*, this file loses it
as well: **1.229 - 0.061 - 0.117 = 1.051**. Every outcome inside [1.051, 1.168]
locates the split; the interval is the trial's entire product.

(c) **THE PRE-REGISTERED NUMBER: 1.095.** The only prior on the split fraction is
the single-leg base of trials #18-#21, where the same three weighting schemes ran
on one buffered 12-1 basket: equal 0.90 (`mom_12m_buffered`) -> rank 0.93
(`mom_rankweighted_buffered`) -> magnitude 0.98 (`mom_zscore_weighted_buffered`),
i.e. ordering 0.03 and spacing 0.05, a **37.5 / 62.5** split. Applying that
fraction to tonight's 0.117 gives ordering 0.044 and spacing 0.073, so
1.229 - 0.061 - 0.073 = **1.095**. This prior is used for the *share* only and
not for the level, because #52 established that the old base's *magnitude* is the
one thing that does not transfer — the component is worth 2.5x there what it was
worth here, since with four legs the concentration channels compound where on the
single-leg base only one existed. If the split fraction transfers while the level
does not, 1.095. If it does not transfer either, the endpoints in (b) bound it.

A SECOND PRE-REGISTERED FALSIFIER, ON THE AXIS THE GATE DOES NOT SCORE, AND A
THIRD CALL FOR A STATISTIC THAT NOW HAS A CALIBRATION. Effective risk bets move
5.99 -> 11.49, **+92%**, which sits between #52's +195% and #53's +29% and is
47% of #52's move. #53 established the risk-contribution count is roughly linear
in this range by predicting its own maxDD to 0.3pp from #52's calibration. Linear
scaling of #52's 5.3pp drawdown gain (-29.6% -> -24.3%) by 92/195 predicts
validation maxDD **-27.1%**. Three pre-registered calls at +195%, +92% and +29%
would bracket the statistic across its whole observed range; a miss at the
midpoint after two hits at the ends is the outcome that would falsify linearity
specifically rather than the statistic.

WHAT THIS FILE IS NOT. It is not a challenger and it is not expected to promote:
every reading in (b) is far below the champion's 1.229, and the trial is being
spent to supply a *sign and a location*, which is the standing practice recorded
in `learnings.md` ("diagnose first; spend the trial only on the sign"). It tunes
nothing — no constant is moved, one weighting function is replaced by another
that estimates no parameters, so `research/SUMMARY.md` screen #1 is satisfied by
both sides of the comparison.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_rankweight",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Replacing the champion's within-leg magnitude transform with linear "
        "rank weighting — each horizon leg's top 15 receiving raw weights "
        "15..1 by composite z-score order, so the ordering of scores is kept "
        "exactly and their spacing is discarded entirely, with membership "
        "(30.2977 average positions, bit-identical), the four lookbacks, the "
        "skip-month, cross-leg equal averaging, single-tranche formation, the "
        "cohort trim and both trim constants otherwise untouched — lands "
        "validation Sharpe near 1.095 net of 15 bps costs. That is the "
        "champion's 1.229 less a 0.061 de-concentration cost priced in "
        "advance from a holdings-only diagnostic (HHI -36.6%, at trial #53's "
        "restated constant of ~0.05 Sharpe per 30% of HHI) and less 0.073 for "
        "spacing, being the 62.5% share of the 0.117 of non-concentration "
        "information that the single-leg base of trials #18-#21 attributed to "
        "spacing rather than ordering. The endpoints bound the answer: 1.168 "
        "says the magnitude transform's information is entirely ordering and "
        "its spacing is decoration, 1.051 says it is entirely spacing and "
        "ordering alone buys nothing beyond concentration. Second falsifier "
        "on the unscored axis: effective risk bets rise 5.99 -> 11.49 (+92%), "
        "47% of #52's move, so linear scaling of #52's drawdown gain predicts "
        "validation maxDD -27.1%, a third pre-registered call bracketing the "
        "risk-contribution statistic at the midpoint of its observed range."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
MAX_WEIGHT = 0.25

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
    """Ordering kept, spacing discarded: the leg's top CORE_N by score receive
    raw weights CORE_N..1 in score order, normalised. The champion's version of
    this line is `raw = c_held - c_held.min() + FLOOR`, which is the same
    ordering carrying the score's actual gaps."""
    held = score.sort_values(ascending=False).index[:CORE_N]
    k = len(held)
    raw = pd.Series(range(k, 0, -1), index=held, dtype=float)
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
