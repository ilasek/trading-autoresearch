"""Does HOW a formation-period return was assembled condition the incumbent's
own continuation score?

THIS CANDIDATE WAS FULLY SPECIFIED BEFORE ITS NUMBERS EXISTED. Every constant
below, the base construction, the family, the track, the run order, the window
rule, the term's sign and both branches of the falsifier are transcribed
verbatim from `experiments/journal.md`'s `## Pre-registration — 2026-09-28
(nightly)`, written before the first screen was run. The one specification
choice left open there — whether the term is type-demeaned — was decided by
F3's pre-registered threshold and not by taste; see below.

WHAT LICENSES IT. `research/SUMMARY.md` #168, written against this lab's own
2026-09-27 next-ideas item 2. That item is a constraint rather than an idea:
the seat holds **61.41%** of its gross in ten of ~48 names and **1.43%** in the
ten smallest, so an overlay acting on membership at rank 15-25 moves ~1.4% of
gross and cannot resolve — trial #103 measured exactly that at `rho` 0.9984.
What is wanted is a *score* change that reorders the top ten weights, and
Da-Gurun-Warachka's frog-in-the-pan is the only such object on the board:
a conditioner *on* `PRET` rather than a substitute for it.

THE MECHANISM, IN ONE LINE. A cumulative return delivered as many small
same-signed daily moves attracts less attention than the identical return
delivered in a few large jumps, so it is absorbed more slowly and continues
further.

THREE GATES, ALL FREE, ALL RUN BEFORE THIS FILE EXISTED.
  F1 (`SUMMARY.md` #165). This panel is forward-filled across foreign holidays,
    so an exact zero daily return can be a calendar artifact. Median `%zero` on
    train is **0.0441** overall, **0.0458** (etf) / **0.0427** (stock), worst
    regional cohort **0.108** (AU, n=2) — under the 0.20 kill line. `ID_Z`'s
    denominator `[%neg + %pos]` removes the zeros exactly, which is why it is
    the variant used here and raw `ID` is not.
  F2, the deciding gate. `learnings.md` [2026-09-01]'s standing
    reversal-in-costume screen, read **within the winner tail** as the source's
    own gate (ii) requires. Median across 215 train month-ends of `|spearman|`
    between `ID_Z` and the top-25 band names' scores: **0.164** (12-1 momentum),
    **0.187** (trailing 252d), **0.161** (21d reversal), **0.170** (trailing
    63d) — all far under the 0.60 line fixed in advance. Two riders worth more
    than the pass itself. The whole-cross-section reading is roughly twice as
    correlated (0.357 / 0.310), so **the conditioning is what makes the object
    orthogonal**, which is the source's own simulated prediction that `ID`
    carries nothing where `PRET` is near zero, observed here rather than
    quoted. And this is the first score in four adjacent veins to survive that
    screen: reference point, salience and 52-week-high proximity all died on it.
  F3, a specification branch with both arms named in advance. Rank-AUC of
    `ID_Z` separating the 42 ETFs from the single names: median **0.387**.
    Under the pre-registered 0.80 line (the seat's `E/Var` term read 0.815 and
    was therefore type-demeaned), **so this term enters RAW.** Recorded as an
    honest caveat rather than a clean pass: 0.387 is a real separation in the
    direction mechanics predict — a basket's daily return is an average and
    therefore smoother, so ETFs read as more continuous — and it is roughly a
    third of the way to the line. The branch was fixed before the number was
    seen and is not revisited now that it has been.

THE CHANGE, AND IT IS ONE CHANGE. The seated champion `pt_mom_evar_arbrisk`,
reproduced byte-for-byte in every node — the same four lookbacks
(252/189/126/63) over the same 21-day skip, the same hold-25/enter-15 band per
leg, the same `c - c.min() + FLOOR` magnitude weighting, the same equal average
across legs, the same six-tranche formation overlap, the same 25% cap, the same
daily vol-spike trim and the same `E/Var` constants — with the per-leg score
changed from `zscore(mom) + zscore(-E/Var)` to
`zscore(mom) + zscore(-E/Var) + zscore(-ID_Z)`. Nothing else is touched.

`ID_Z`, AND ITS ONE TRANSCRIPTION CHOICE. `ID_Z = sgn(PRET) * [%neg - %pos] /
[%neg + %pos]`, one pass over daily closes, trivially causal. Low `ID_Z` is the
continuous-information name, so the term is negated to make higher better.
**The window is each leg's own formation window** — `lookback + skip` back to
`skip`, exactly the span its own `PRET` measures — rather than a fixed 252 days.
This is the mechanism-faithful reading (a leg's conditioner has no business
reading a window its own score does not) and it is also the choice with **zero**
new constants, where a fixed 252 would introduce one that merely coincides with
the longest leg. `research/SUMMARY.md` #1's parameter-count triage rule, which
`learnings.md` [2026-09-24] records as transferring, decides it that way.
ANTI-CANDIDATE, FIXED IN ADVANCE: the fixed-252 variant is a second value of the
same knob and must not be run later as a "repair". Nor may `ID_MAG`'s
5/15..1/15 quintile weights be swept — their own authors call the scheme
arbitrary (`SUMMARY.md` #169(d)).

COUNTED NaN-TOLERANTLY, DELIBERATELY. `%pos` and `%neg` count only the
observations that exist, so a foreign holiday neither votes nor restricts the
pool. The strict alternative — `dropna(how="any")` over the window — is the
exact shape of the `dropna` filter that cost this repo four trials on the trim
overlay (`learnings.md`, trials #37-#40), and the habit that episode left
behind is to check what a component's code actually reads: measured over the
validation month-ends, the eligible pool is **unchanged to within one
instrument** by adding this term.

THE FORM IS THE POINT. The term enters the per-leg score *before* the
magnitude-weighting step, so it can reorder the ten weights that carry 61.41% of
gross. `SUMMARY.md` #169(a) makes the alternatives standing anti-candidates: as
a membership filter, a band-margin tiebreak or a tail overlay this lands in the
1.4%-of-gross channel trial #103 already measured at `d = -0.011`.

EQUAL WEIGHTS BETWEEN THE THREE TERMS ARE LOAD-BEARING AND ARE NOT A KNOB.
`learnings.md`'s horizon-leg finding — equal weights are the right ones and
estimating them is the mistake three separate literatures warn against — is a
`price-trend` constant measured on this construction, so it applies directly.

WHAT WOULD FALSIFY IT, BOTH BRANCHES FIXED IN ADVANCE. Validation Sharpe at or
below **1.269** says frog-in-the-pan conditioning is absent on this universe's
incumbent score, closing `SUMMARY.md` #168 and making it the fourth adjacent
vein closed after reference point [2026-09-19], salience [2026-09-20] and
52-week-high proximity [2026-09-27]. Above 1.269 it goes to the deflated-Sharpe
bar and the holdout veto on its own merits.

STATED IN ADVANCE AGAINST THE OBJECTIVE. The number to read is the paired `t`
under `metrics.sharpe_diff_se`, not the Sharpe difference. At the `rho` 0.95-0.99
a one-term score change sits at, the required-gain table asks **+0.138 to
+0.310** and the family's resolution floor is 0.03-0.08, while the seat's entire
cost channel is worth **+0.0249**. The honest prior is a point estimate inside
±0.05 that this split cannot resolve; tonight's contribution is the sign and the
closure, not a level. Source provenance, stated because it discounts the prior:
Tier A, `validation_overlap: false`, `published_post_2018: false`, and
`SUMMARY.md` records **no independent replication located**.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import groups as G

STRATEGY = {
    "name": "pt_mom_id_z",
    "family": "price-trend",
    "track": "challenge",
    "hypothesis": (
        "Adding zscore(-ID_Z) — the sign-only information-discreteness of each "
        "leg's own formation window, sgn(PRET)*[%neg-%pos]/[%neg+%pos] — as a "
        "third term to the seated champion pt_mom_evar_arbrisk's per-leg score, "
        "leaving every other node byte-identical, raises validation Sharpe "
        "above 1.269, because a formation-period return assembled from many "
        "small same-signed daily moves is absorbed more slowly than an "
        "identical cumulative return delivered in a few large jumps, so "
        "continuation persists further where the information arrived "
        "continuously."
    ),
}

# --- transcribed from the seated champion, unchanged ---
LOOKBACKS = (252, 189, 126, 63)
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

EVAR_WINDOW = 250
EVAR_LAG = 20
EVAR_K = 4
MIN_TYPE = 4


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def _demean_by(score: pd.Series, mapping: dict, min_size: int) -> pd.Series:
    labels = pd.Series({name: mapping.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= min_size).dropna()


def _hedgeable_fraction(window: np.ndarray, names: list) -> pd.Series:
    """E/Var = corr(name, its top-K substitute basket)^2, in closed form."""
    v = window - window.mean(axis=0)
    sd = v.std(axis=0, ddof=1)
    ok = sd > 0
    if ok.sum() <= EVAR_K + 1:
        return pd.Series(dtype=float)
    v, sd = v[:, ok], sd[ok]
    cols = [n for n, keep in zip(names, ok) if keep]
    n = len(cols)

    corr = (v.T @ v) / (len(v) - 1) / np.outer(sd, sd)
    np.fill_diagonal(corr, -np.inf)
    top = np.argpartition(-corr, EVAR_K - 1, axis=1)[:, :EVAR_K]

    sel = np.zeros((n, n))
    sel[np.arange(n)[:, None], top] = 1.0 / EVAR_K
    baskets = v @ sel.T
    b_sd = baskets.std(axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        rho = (v * baskets).sum(axis=0) / (len(v) - 1) / (sd * b_sd)
    return pd.Series(np.square(np.clip(rho, -1.0, 1.0)), index=cols).replace(
        [np.inf, -np.inf], np.nan
    ).dropna()


def _id_z(window: np.ndarray, names: list, pret: pd.Series) -> pd.Series:
    """Sign-only information discreteness over one leg's formation window.

    `%zero` is excluded by construction: the denominator counts only strictly
    signed days, which is the variant of Da-Gurun-Warachka's measure that is
    invariant to this panel's forward-filled foreign holidays. Counting is
    NaN-tolerant so a holiday neither votes nor restricts the pool.
    """
    pos = np.nansum(window > 0, axis=0).astype(float)
    neg = np.nansum(window < 0, axis=0).astype(float)
    den = pos + neg
    ok = den > 0
    if not ok.any():
        return pd.Series(dtype=float)
    cols = [n for n, keep in zip(names, ok) if keep]
    raw = pd.Series((neg[ok] - pos[ok]) / den[ok], index=cols)
    signs = np.sign(pret.reindex(raw.index))
    return (raw * signs).dropna()


def _leg_target(score: pd.Series, held: set) -> tuple:
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

    ret_values = prices.pct_change(fill_method=None).to_numpy()
    all_names = list(prices.columns)
    positions = {dt: i for i, dt in enumerate(all_dates)}

    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < max_lb + SKIP + 1:
            continue

        moms = {lb: _momentum(hist, lb) for lb in LOOKBACKS}
        common = None
        for m in moms.values():
            common = m.index if common is None else common.intersection(m.index)

        pos_dt = positions[dt]
        end = pos_dt - EVAR_LAG + 1
        start = end - EVAR_WINDOW
        if start < 1:
            continue
        block = ret_values[start:end]
        finite = np.isfinite(block).all(axis=0)
        if finite.sum() <= EVAR_K + 1:
            continue
        evar = _hedgeable_fraction(
            block[:, finite], [n for n, keep in zip(all_names, finite) if keep]
        )
        if evar.empty:
            continue
        # low E/Var = least hedgeable = costliest to arbitrage, so negate.
        risk_score = _demean_by(-evar, G.TYPE_OF, MIN_TYPE)

        # ID_Z per leg, over exactly the span that leg's own PRET measures.
        idz = {}
        for lb in LOOKBACKS:
            lo = pos_dt - (lb + SKIP) + 1
            if lo < 1:
                break
            idz[lb] = _id_z(ret_values[lo:pos_dt - SKIP + 1], all_names, moms[lb])
        if len(idz) < len(LOOKBACKS):
            continue

        common = common.intersection(risk_score.index)
        for lb in LOOKBACKS:
            common = common.intersection(idz[lb].index)
        if len(common) < CORE_N:
            continue

        z_risk = _zscore(risk_score[common])
        leg_targets = []
        for lb in LOOKBACKS:
            # low ID_Z = continuous information = the side the mechanism favours.
            score = _zscore(moms[lb][common]) + z_risk + _zscore(-idz[lb][common])
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
