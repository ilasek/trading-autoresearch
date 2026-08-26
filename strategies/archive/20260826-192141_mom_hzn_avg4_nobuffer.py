"""Does the membership buffer still earn its seat on the four-leg base?

WHAT THE BUFFER IS AND WHERE ITS JUSTIFICATION COMES FROM. Every candidate this
repo has run since trial #17 selects through an asymmetric band: a name enters a
leg's basket only in the top CORE_N = 15 but is held while it stays inside the
top BAND_N = 25. It was introduced on a *much* worse base — equal-weight, single
horizon, single formation vintage, no trim — where it beat the then-champion on
both axes at once (validation Sharpe 0.865 -> 0.90, turnover 5.8x -> 4.4x, a 24%
cost saving). `research/SUMMARY.md` candidate #9 endorses it as the literature's
top-ranked construction technique and records it explicitly "so nobody
simplifies it back to a hard top-N cutoff". Both the local result and the
imported endorsement rest on the *same* mechanism: a buy/hold spread suppresses
low-information trades near the cutoff, i.e. **it is a cost-mitigation device.**

WHY THAT JUSTIFICATION NO LONGER SETTLES THE QUESTION HERE. The buffer has never
been re-examined on the base it now sits on. Three things have changed under it:
the book is magnitude-weighted, selection runs through four independent horizon
legs whose averaging already damps any one leg's membership churn, and
`learnings.md` has since retired turnover reduction as a lever on this base.
That is exactly the situation the trim was in for ~20 trials — an inherited
component described in terms its implementation on the current base no longer
matched — and re-reading it cost four trials. `learnings.md`'s own general rule
from that episode is to check what a component actually buys *on the base it is
on*, and its companion rule is that an artifact fix's value is a property of the
base, not of the fix.

PRE-TRIAL DIAGNOSTIC, RUN BEFORE THIS FILE WAS WRITTEN (holdings only: weight
matrices and their trade vectors on prices truncated at 2023-12-31, no returns
scored, trial count untouched). Champion against the identical construction with
the band deleted (`held = core`, a hard top-15 per leg):

                            turnover  positions   HHI    top_w  top_risk  eff_risk_bets
    champion  hold25/enter15   7.87x     35.1    0.0701  0.163   0.320        7.8
    this file hard top-15      8.34x     30.3    0.0881  0.192   0.368        6.0

    mean weight overlap 0.905
    core-vs-fringe L1: top-10 0.063   rest of book 0.127

Three readings, and together they fix the pre-registration.

(a) **The buffer's stated benefit is gone.** It is worth 0.47x of annual turnover
here — 0.070 pp/yr at 15 bps, about **0.003 Sharpe**. On the single-leg base it
saved 24% of turnover; on this one it saves 6%, because averaging four legs
already absorbs most of the churn a band was invented to suppress. Whatever the
buffer is doing for this book, cost mitigation is not it, and the source that
endorses it endorses it for that reason.

(b) **The change is a concentration change, and the confound is quantified in
advance.** HHI +25.7% at 4.8 fewer names. This repo prices de-concentration at
~0.02 Sharpe per ~30% of HHI whenever the flatness does not arrive from a
decorrelated vintage, and the magnitude-weighting ladder ran that dial in the
concentrating direction for gains. So the removal carries a **+0.017 Sharpe
tailwind** that has nothing to do with the buffer.

(c) **The rotation-speed rationale that motivated this trial is measured small,
and recorded as such rather than quietly kept.** The intuition was that a band is
a membership-stickiness device and that `learnings.md`'s three vintage nulls
identify blur in the *core* allocation as what costs return in the rotation
years. The core-vs-fringe screen says the band is largely a **fringe**
phenomenon on this base: 0.063 of L1 disagreement on the champion's top-10
against 0.127 on the whole rest. Removing it re-draws the tail, not the core, so
the rotation-speed benefit should be pre-registered near **zero**, not as the
reason to expect a win.

THE PRE-REGISTERED NUMBER. Netting (a), (b) and (c): **1.215** (1.201 + 0.017
- 0.003). Landing there is a **null on the buffer's marginal value** — it would
say the band neither helps nor hurts once its cost saving is gone, and that the
whole move is the concentration ladder this repo has already climbed. Landing
materially above 1.215 says the band was an active brake worth deleting.
Landing materially **below** 1.201 is the most interesting outcome and the one
this file is really written to test: it would show the buffer is doing real work
on this base through some channel other than cost, at which point the repo would
own a component whose only documented justification is measured at 0.003 Sharpe
and whose actual mechanism is unknown — the trim situation again, found before
twenty trials were built on it rather than after.

A SECOND PRE-REGISTERED FALSIFIER, ON THE AXIS THE GATE DOES NOT SCORE.
Validation maxDD should worsen materially from the champion's -28.7%. Top-name
risk share moves 0.320 -> 0.368 and effective risk *bets* 7.8 -> 6.0, the
largest move on that axis any candidate here has pre-registered, and
`learnings.md`'s one recorded miss of this diagnostic (#50) has a stated shape —
blindness to weight-vector staleness — that does not apply to a book whose
weights are re-targeted every month from a fresh composite. If maxDD does not
worsen, the risk-contribution rule has missed a second time and for a new
reason, which the entry would need to carry.

WHAT THIS FILE DOES NOT DO. It tunes nothing: BAND_N is not moved to some other
value, it is deleted, so the question is about the mechanism's existence on this
base rather than its width. Signal, four horizon legs, skip-month, magnitude
weighting, single-tranche formation, cohort trim and both trim constants are
inherited untouched.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_nobuffer",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Deleting the membership band from the champion — each of the four "
        "horizon legs holding exactly its current top 15 rather than entering "
        "at 15 and holding to 25, with signal, skip-month, magnitude "
        "weighting, single-tranche formation, cohort trim and both trim "
        "constants otherwise identical — lands validation Sharpe at or above "
        "1.215 net of 15 bps costs, because a holdings-only diagnostic prices "
        "the band's entire documented benefit on this base at 0.47x of annual "
        "turnover (~0.003 Sharpe, against the 24% cost saving that justified "
        "it on the single-leg base of trial #17, four-leg averaging having "
        "since absorbed the churn a band was invented to suppress) while the "
        "removal carries a +0.017 Sharpe concentration tailwind (HHI +25.7%) "
        "and a rotation-speed benefit measured near zero (core-vs-fringe L1 "
        "0.063 on the top-10 against 0.127 on the rest, i.e. the band is a "
        "fringe phenomenon here); landing materially below 1.201 shows the "
        "buffer does real work on this base through a channel other than "
        "cost, whose mechanism the repo would then not know."
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
    """The champion's leg target with the hold band deleted: membership is the
    current top CORE_N outright, so nothing is carried between rebalances."""
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
