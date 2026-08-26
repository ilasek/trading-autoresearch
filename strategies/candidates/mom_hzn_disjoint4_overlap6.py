"""Do the four horizon legs have to *nest*?

WHAT THE BRACKET WORK LEFT OPEN. Trial #42 (the reinstated champion) fixed the
bracket's *width* — four windows spanning the skip-month to 12 months — and
trial #44 fixed its *interior*, finding geometric spacing a null against uniform
spacing. Both of those moved where the windows' *start* dates sit. Neither
touched the one property all of them share: every leg's window **ends at t-21**,
so the four windows are strictly nested, and the 63-day leg's data is a subset of
every other leg's. #44's own pre-trial diagnostic framed redundancy as the ratio
`L1/L2` of shared data and then moved only its *dispersion* (12x down) while
leaving its *level* almost untouched (-0.011 mean overlap) — and duly returned a
null. The level has never been moved.

THE CHANGE, AND IT IS ONE CHANGE. The four legs cover four **adjacent, disjoint**
quarters ending at t-21 — [t-273, t-210], [t-210, t-147], [t-147, t-84],
[t-84, t-21] — instead of four nested windows all ending at t-21. Total span,
skip-month, per-leg buffer chain, magnitude weighting, equal weighting between
legs, six-tranche date overlap and the daily vol-spike trim are all #42 exactly.
The eligibility pool is bit-identical too: the longest offset is still 273 days,
so `common` is unchanged.

WHY IT IS NOT A SWEEP AND NOT A FOURTH VINTAGE AXIS. Nothing is chosen by
performance: given four legs and a 12-month span pinned at both ends (skip-month
below, post-formation reversal above), "disjoint" is the unique partition — there
is one way to tile an interval with four equal non-overlapping pieces, where
there are infinitely many ways to nest four windows inside it. And it is not a
new averaging axis; it is a re-specification of the length axis the lab already
owns.

THE PREMISE, MEASURED BEFORE THE TRIAL (holdings-only, no returns scored, 72
validation formations). Mean pairwise weight overlap between the four leg
portfolios: **0.475 nested -> 0.141 disjoint**. That is by a wide margin the
largest leg disagreement the lab has ever measured on any averaging axis —
against 0.645 for formation-date vintages, 0.43-0.48 for instrument-subsample
folds and 0.963 for the buffer-band vintages that were killed for free. Book
overlap against the champion is 0.694, and the disagreement is not a fringe
effect: L1 0.244 inside the champion's own top-10 against 0.367 across the whole
rest of the book.

WHY THIS IS WORTH A TRIAL: IT PUTS TWO OF THE LAB'S OWN CALIBRATED CONSTANTS IN
DIRECT CONFLICT, WHICH NOTHING SO FAR HAS DONE.
  (a) *Breadth from a decorrelated vintage is free.* #41 -> #42 went from two
      legs to four, breadth 47 -> 63 names, and validation Sharpe rose (1.112 ->
      1.120) while validation maxDD *improved* (-28.5% -> -27.8%). The recorded
      lesson is explicit: "the concentration price is not a law of
      de-concentration — breadth arriving from a decorrelated vintage costs
      nothing". Disjointness is more of exactly that, and it takes breadth to
      81.1 names.
  (b) *De-concentration costs ~0.05 of Sharpe per 30% of HHI* (#53's measured
      constant, which replaced the older ~0.02 figure). This construction cuts
      book HHI 0.0618 -> 0.0336, i.e. **-46%**, which prices at about **-0.077**.
These two constants have never been asked the same question. On (a) the expected
effect is ~0 to slightly positive; on (b) it is about -0.08. They cannot both be
right here, and the trial supplies only the sign — which is the form
`learnings.md` says a trial should be spent in.

PRE-REGISTERED EFFECT AND THE HONEST BAR. Expected validation Sharpe **1.04 to
1.13** against the champion's 1.120, centred slightly below it: the third force,
not covered by either constant, is that the three far quarters are weaker
standalone selection signals than nested windows that contain the recent quarter
(Goyal-Wahal 2015 find no intermediate-horizon echo outside the US, so this
repo's global pool should read a *declining*, not humped, term structure). At an
expected `rho` near 0.95 the closed-form paired SE is ~0.13, so a promotion-grade
margin is not expected and is not claimed. What is claimed is that the *sign* is
informative and currently unpredictable from the lab's own record.

WHAT WOULD FALSIFY WHICH CLAIM. Sharpe at or above 1.12 with maxDD at or better
than -27.8%: (a) holds and the "breadth from disagreement is free" lesson
generalises past the nested bracket — which would reopen the length axis. Sharpe
near 1.04-1.06: (b) dominates, the de-concentration constant applies to breadth
from decorrelated vintages after all, and the #41/#42 exception was a property of
those particular windows rather than a law. Sharpe well below 1.04: the far
quarters carry little selection signal on this universe and the term structure
is steeper than Goyal-Wahal's flat reading.

CAVEATS RECORDED IN ADVANCE. (a) The daily vol-spike trim is #42's accidental
`held ∩ full-history-cohort` filter, whose sample is a function of book breadth
(trials #37-#40, #45, #46); widening the book to 81 names perturbs it, so a small
difference either way is not clean evidence — the same caveat #42's own file
recorded for the same reason. (b) Turnover should rise: each leg re-forms from a
window that no longer shares data with its neighbours. (c) This is a
signal-*structure* change, not a new score; `learnings.md` closes "find a better
score", and nothing here proposes one.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_disjoint4_overlap6",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Replacing the champion's four nested formation windows (252/189/126/63 "
        "days, all ending at the skip-month) with four adjacent disjoint "
        "quarters spanning the same 12-month bracket — everything else, "
        "including the buffer chain, magnitude weighting, equal leg weighting, "
        "six-tranche date overlap and the daily vol-spike trim, identical to "
        "trial #42 — raises validation Sharpe above 1.120 net of 15 bps costs, "
        "because the gain from portfolio-level horizon averaging is bounded by "
        "how much the legs disagree and disjoint windows raise measured "
        "pairwise leg weight overlap disagreement from 0.475 to 0.141, the "
        "largest on any averaging axis recorded here; it is falsified if the "
        "-46% book HHI that disagreement brings with it costs more than the "
        "disagreement buys, which the lab's de-concentration constant prices at "
        "about -0.077 Sharpe."
    ),
}

SKIP = 21
QUARTER = 63
N_LEGS = 4
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 6

VOL_SHORT = 21
VOL_LONG = 252
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6

# (start_offset, end_offset) in trading days back from the formation date.
# Longest offset is SKIP + N_LEGS*QUARTER = 273, identical to the champion's
# 252 + 21, so the eligibility pool `common` is unchanged.
WINDOWS = tuple(
    (SKIP + (j + 1) * QUARTER, SKIP + j * QUARTER) for j in reversed(range(N_LEGS))
)


def _window_return(hist: pd.DataFrame, start_off: int, end_off: int) -> pd.Series:
    past = hist.iloc[-start_off - 1]
    recent = hist.iloc[-end_off - 1]
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
    held = {w: set() for w in WINDOWS}
    recent_targets = []
    base_periods = []

    all_dates = prices.index
    max_off = max(s for s, _ in WINDOWS)
    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < max_off + 1:
            continue

        moms = {w: _window_return(hist, w[0], w[1]) for w in WINDOWS}
        common = None
        for m in moms.values():
            common = m.index if common is None else common.intersection(m.index)
        if len(common) < CORE_N:
            continue

        leg_targets = []
        for w in WINDOWS:
            score = _zscore(moms[w][common])
            t, held[w] = _leg_target(score, held[w])
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
