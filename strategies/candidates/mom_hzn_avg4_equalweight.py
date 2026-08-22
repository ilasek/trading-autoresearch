"""The last unexamined inherited component: does magnitude weighting still earn
its seat on the four-leg base?

WHY THIS COMPONENT AND WHY NOW. `learnings.md` has twice paid for the same
mistake — the daily vol-spike trim survived ~20 trials described in terms its
code never matched (four trials to unwind), and the engine's weight-handling
convention supported a headline lesson that was retracted a night later. The
rule distilled from both is to check what a component actually buys **on the
base it is on**, and its companion is that an artifact fix's value is a property
of the base, not of the fix. Trial #51 applied that rule to the membership
buffer and found its documented justification (cost mitigation, 24% of turnover
on the single-leg base of trial #17) had shrunk to 6% — 0.003 Sharpe — because
four-leg averaging had absorbed the churn a band was invented to suppress.

**Magnitude weighting is the one large inherited component that rule has never
been applied to, and it is the largest of them.** It was measured across trials
#18-#21 on a base that no longer exists in any respect: single formation
vintage, a single composite score, equal-weight membership of 18.6 names, no
cohort trim, no horizon legs. On that base the equal-weight -> rank-weight ->
magnitude-weight ladder ran validation Sharpe 0.90 -> 0.93 -> 0.98, i.e. the
step this file reverses was worth about **+0.08 at fixed signal**. Everything
since has inherited it untouched through eleven promotions and thirty trials.

The reason to expect the base to have absorbed part of it is specific rather
than general. Averaging four horizon legs' *weight vectors* already performs a
form of agreement weighting that did not exist on the single-leg base: a name
selected by all four legs receives four times the capital of a name selected by
one, before any magnitude transform is applied. Magnitude weighting is therefore
no longer the only mechanism tilting capital toward the strongest names, and its
marginal contribution should be smaller than the 0.08 it was measured at. How
much smaller is the question.

PRE-TRIAL DIAGNOSTIC (holdings only, prices truncated 2023-12-31, no returns
scored, trial count untouched). The champion against the identical construction
with each leg equal-weighting its held set:

                          champion    this file
    avg positions           30.30       30.30     <- membership bit-identical
    HHI                    0.0943      0.0425     (-55%)
    top weight              0.200       0.066     (-67%)
    ann turnover            8.22x       7.95x     (-3%)
    gamma* (annualised)     5.51%       4.17%
    effective risk bets      5.99       17.68     (+195%)
    N_cond (Meucci)          5.63        5.49     (-2.6%)
    mean weight overlap             0.6815

Membership is untouched to four decimal places, so this isolates the weighting
transform exactly — the cleanest single-component isolation available on this
base, cleaner than #51's (which moved 4.8 names).

THE PRE-REGISTERED NUMBER, ON THE GATE'S AXIS. Champion 1.229. If magnitude
weighting is worth on this base exactly what it was worth on the single-leg base,
this lands at **1.15**. If four-leg agreement weighting has absorbed half of it,
~1.19. Three readings, fixed in advance:

  - near 1.15  -> the component's value is intact, the axis closes, and the repo
                  keeps it for a reason it has now verified rather than inherited.
  - above 1.19  -> four-leg averaging has absorbed most of it, and this repo owns
                  a concentration device whose gate-axis value is small and whose
                  risk cost is the largest of any component it runs. That is the
                  buffer's situation again, one component over, and it would be
                  found before another thirty trials are built on it.
  - at or above 1.229 -> the last unexamined inherited component is refuted.

THE SECOND PRE-REGISTERED FALSIFIER, AND IT IS WHY THIS TRIAL IS WORTH ITS COST
EVEN IF THE FIRST NUMBER IS DULL. The two risk-breadth statistics this repo runs
**disagree maximally here, and this is the only construction found so far on
which they do**. The Herfindahl-over-marginal-risk-contributions count that
`learnings.md` uses says the equal-weighted book is nearly three times more
diversified (5.99 -> 17.68) and therefore predicts a large improvement in
validation maxDD from the champion's -29.6%. The Meucci conditional
effective-bets count — which changes basis before counting, and which
`research/SUMMARY.md` candidate #23(a) says is the measure that actually counts
uncorrelated sources — says the book is **not more diversified at all**
(5.63 -> 5.49, marginally worse), because flattening weights across thirty names
that all load on the same few principal portfolios adds no independent bets.
Validation maxDD is the referee, and it cannot split the difference:

  - maxDD materially better than -29.6% -> the contribution count is right here
    and Meucci's criticism of it does not bind on this book.
  - maxDD flat or worse despite a 195% move in the contribution count -> the
    contribution count is measuring weight flatness wearing a covariance, and
    `learnings.md` should stop quoting it as a diversification number.

That question is currently load-bearing: the risk-contribution vector is the
statistic this repo used to pre-register #47's and #51's drawdowns, and tonight's
free ladder measurement puts its correlation with holdout Sharpe (+0.450) below
both the Meucci count (+0.632) and simply counting positions (+0.780).

WHAT THIS FILE DOES NOT DO. It tunes nothing. FLOOR is not moved, the transform
is not dampened or steepened — the transform is deleted, so the question is about
the mechanism's existence on this base rather than its strength. Signal, four
horizon windows, skip-month, hard top-15 membership, single-tranche formation,
cohort trim and both trim constants are inherited untouched. Per `learnings.md`
this is explicitly **not** a re-run of the refuted square-root dampening: that
tested an intermediate point on the concentration dial on the single-vintage
single-score base, whereas this deletes the mechanism on the current base, which
is the question dampening could not answer.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_equalweight",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Deleting magnitude weighting from the champion — each of the four "
        "horizon legs equal-weighting its top-15 held set instead of sizing it "
        "by shifted composite z-score, with signal, skip-month, membership, "
        "single-tranche formation, cohort trim and both trim constants "
        "otherwise identical and average positions bit-identical at 30.30 — "
        "lands validation Sharpe near 1.15 net of 15 bps costs, because the "
        "+0.08 that this step was worth across trials #18-#21 was measured on a "
        "base with one formation vintage, one composite score and no horizon "
        "legs, and averaging four legs' weight vectors now performs agreement "
        "weighting independently of any magnitude transform; landing above 1.19 "
        "shows four-leg averaging has absorbed most of the component's value, "
        "leaving a concentration device with a small gate-axis benefit and the "
        "largest risk cost of anything this book runs. Second, independent "
        "falsifier on the unscored axis: the two risk-breadth statistics "
        "disagree maximally here — effective risk bets 5.99 -> 17.68 (+195%) "
        "predicts validation maxDD materially better than the champion's "
        "-29.6%, while the Meucci conditional count 5.63 -> 5.49 (-2.6%) "
        "predicts no improvement — so maxDD adjudicates which of the two this "
        "repo should be quoting as a diversification number."
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
    """The champion's leg target with the magnitude transform deleted: the same
    top CORE_N names, sized equally instead of by shifted z-score."""
    ranked = score.sort_values(ascending=False)
    held = list(ranked.index[:CORE_N])
    return pd.Series(1.0 / len(held), index=held)


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
