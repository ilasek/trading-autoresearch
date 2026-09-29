"""Can a seasonal signal pay for RE-TIMING the incumbent's existing trades,
rather than for running a book of its own?

THIS CANDIDATE WAS FULLY SPECIFIED BEFORE ITS NUMBERS EXISTED. Every constant
below, the base construction, the family, the track, the run order and both
branches of the falsifier are transcribed verbatim from
`experiments/journal.md`'s `## Pre-registration — 2026-09-27 (nightly)`, which
was committed before the first screen ran. The two screens that gated it (F1's
deferral census, F2's band-margin IC) had their kill lines fixed in that same
entry. Nothing here was chosen after a measurement tonight.

WHAT LICENSES IT. `research/SUMMARY.md` #49, the research folder's one *build*,
carried unspent for THIRTY sessions and the only item on its list that is not
gated behind a screen which has since failed. It is the source authors' own
recommendation rather than an inference drawn from them: Heston-Sadka decline to
recommend trading their seasonal signal because doing so "requires rebalancing
the entire portfolio every month", and observe instead that "it is relatively
simple to postpone the sale or purchase of a particular stock if it has a large
positive or negative expected return over the next month". That adds no
turnover; it re-times turnover the incumbent was already paying for, and
`experiments/learnings.md` records cost as this lab's live axis. The seat runs
3.01x validation turnover, which is the base the overlay sits on.

WHY IT IS `price-trend` AND WHY IT IS A CHALLENGER. It modifies the incumbent,
so it is `price-trend` whatever the overlay signal's provenance, and it counts
against that family's cap of two. Because it can reach the holdout gate it is
run last in its session; nothing is designed after it.

THE CHANGE, AND IT IS ONE FUNCTION. `pt_mom_evar_arbrisk` is reproduced
byte-for-byte in every node -- the same four lookbacks (252/189/126/63) over the
same 21-day skip, the same `zscore(momentum) + zscore(type-demeaned -E/Var)`
per-leg score with the same `E/Var` constants (250-day window, 20-day lag,
K = 4, MIN_TYPE = 4), the same hold-25/enter-15 band, the same
`c - c.min() + FLOOR` magnitude weighting, the same equal average across legs,
the same six-tranche formation overlap, the same 25% cap and the same daily
vol-spike trim -- with the per-leg membership rule alone replaced. No `E/Var`
knob and no momentum knob is moved.

THE OVERLAY. Per leg, per rebalance date, with `base_held` the set the
champion's rule returns and `prev` that leg's own holdings last month:

    sells = prev - base_held        buys = base_held - prev

    defer a SELL: a name in `sells` is RETAINED this month if its seasonal
    score is in the TOP DEFER_Q of the date's cross-section, and it was not
    already deferred last month.

    defer a BUY: a name in `buys` is SKIPPED this month if its seasonal score
    is in the BOTTOM DEFER_Q of the date's cross-section, and it was not
    already skipped last month.

`MAX_DEFER = 1` -- a name may be deferred at most one consecutive month per leg.
That cap is what makes this a POSTPONEMENT rather than a different band: without
it a seasonally-strong name could be retained indefinitely and the overlay would
quietly become a second score.

`DEFER_Q = 0.10`, READ OFF AN EXISTING MEASUREMENT RATHER THAN SWEPT.
`learnings.md` [2026-09-01] profiles this exact score on train deciles: flat
across deciles 1-9 (-3.1% to +1.0%/yr) and +10.59%/yr at t = +4.16 in decile 10.
The decile is the score's own measured step, not a chosen quantile. No other
value will be tried, in this session or a later one.

THE ASYMMETRY IS THE POINT, AND ITS TWO ARMS ARE NOT EQUALLY BACKED. The sell
arm sits on the +10.59%/yr top decile and is where any gain must come from. The
bottom decile's -3.1%/yr is inside the flat region, so the buy arm was
pre-registered as a breadth neutraliser expected to contribute approximately
nothing. F1 measured it contributing 341 of 724 deferrals -- 47%, nearly half
the weight movement -- so THAT PREDICTION IS ALREADY WRONG and any gain here
must be attributed to the asymmetric pair of arms, not to the top decile alone.
This is recorded before the trial runs, not after it.

WHAT THE GATING SCREENS RETURNED (train, holdings only, no returns scored; both
kill lines were fixed in the pre-registration). F1: the overlay defers 0.1013 of
the base book's monthly membership trades (floor 0.05) and moves a mean 0.0403
of gross (floor 0.02), with breadth neutral to 0.02 of a position (25.36 against
25.34) and 229 of 534 months byte-identical to the base book -- idle most of the
time, occasionally moving an eighth of the book, which is the shape of a
re-timing rule rather than of a second score. F2: the seasonal score's IC among
names ranked 15-25 by the champion's own per-leg score -- the exact population
whose hold/drop decision this overlay changes -- is +0.0510 at t = +2.69 over
412 train dates, against a placebo-hash control at +0.0025 (t = +0.14). The sign
was declared positive in advance.

WHAT WOULD FALSIFY IT, BOTH BRANCHES FIXED IN ADVANCE. Validation Sharpe at or
below 1.269 says a seasonal signal cannot pay for re-timing a momentum book's
existing trades on this universe, which retires `SUMMARY.md` #49 after thirty
sessions on a measured result rather than on neglect. Above 1.269 it goes to the
deflated-Sharpe bar and the holdout veto on its own merits. An annual turnover
ABOVE 3.01 would mean the implementation is not a deferral and is a bug, not a
finding -- it is a correctness check on this file, not a branch of the
hypothesis.

STATED IN ADVANCE AGAINST THE OBJECTIVE. A one-node change to the champion sits
at `rho` ~ 0.99, where `learnings.md`'s required-gain table asks +0.138 and this
family's resolution floor is 0.03-0.08. The number to read is the paired `t`
under `metrics.sharpe_diff_se`, not the Sharpe difference on its own.
`learnings.md` [2026-09-10] is on record that changing 42% of a book's NAMES
moved its returns only to `rho` = 0.9908, so a few deferred names per leg per
month is a small prior and not a promising one.

ANTI-CANDIDATES ATTACHED. No second `DEFER_Q`. No `MAX_DEFER` other than 1. No
second auxiliary signal -- the 5-day reversal score carries this repo's largest
IC at t = +10.59 and is the obvious substitute, but substituting it would be
choosing the overlay signal off the lab's own table rather than off #49's
source, and `learnings.md` [2026-09-25] already carries a standing
anti-candidate against reading that IC as a licence. No widening of the
champion's 15/25 band to "make room" for deferred names: that is a band knob,
and the band is the one node this repo has measured as construction-specific.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import groups as G
from strategies.lib import signal_blend as SB

STRATEGY = {
    "name": "pt_mom_seasonal_deferral",
    "family": "price-trend",
    "track": "challenge",
    "hypothesis": (
        "Deferring by exactly one month those membership trades the seated "
        "champion was going to make anyway — retaining a name it would sell "
        "when that name's same-calendar-month seasonal score is in the top "
        "decile of the date's cross-section, and skipping a name it would buy "
        "when that score is in the bottom decile, each name deferrable at most "
        "one consecutive month, with every other node of pt_mom_evar_arbrisk "
        "byte-identical — raises validation Sharpe above 1.269 while lowering "
        "annual turnover below 3.01, because the overlay adds no trade by "
        "construction and Heston-Sadka's own recommendation is that a seasonal "
        "signal is worth using to re-time an existing rebalance rather than to "
        "run a book."
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

# --- the overlay, and these are the only new constants in the file ---
DEFER_Q = 0.10      # the seasonal score's own measured decile step
MAX_DEFER = 1       # one consecutive month; a postponement, not a band
MIN_SEASONAL = 20   # names needed before a decile cut means anything


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


def _deferral_sets(seasonal_row: pd.Series, pool) -> tuple[set, set]:
    """The date's top and bottom `DEFER_Q` of the seasonal cross-section,
    restricted to the scoreable pool. Empty on a date too thin for a decile cut,
    which makes the overlay a no-op there rather than an arbitrary one."""
    if seasonal_row is None:
        return set(), set()
    s = seasonal_row.dropna()
    s = s[s.index.isin(pool)]
    if len(s) < MIN_SEASONAL:
        return set(), set()
    hi, lo = s.quantile(1.0 - DEFER_Q), s.quantile(DEFER_Q)
    return set(s[s >= hi].index), set(s[s <= lo].index)


def _leg_target(
    score: pd.Series, held: set, top_seasonal: set, bot_seasonal: set,
    deferred_sells: set, skipped_buys: set,
) -> tuple:
    """The champion's membership rule, then the deferral overlay on top of it.

    The champion's two lines are reproduced exactly and their result is
    `base_held`; everything after them is the overlay, and it can only ever
    remove a trade the base rule had already decided to make.
    """
    ranked = score.sort_values(ascending=False)
    core = set(ranked.index[:CORE_N])
    band = set(ranked.index[:BAND_N])
    base_held = (held & band) | core

    sells = held - base_held
    buys = base_held - held
    # MAX_DEFER = 1: a name deferred last month is not deferrable this month.
    defer_s = {n for n in sells if n in top_seasonal and n not in deferred_sells}
    skip_b = {n for n in buys if n in bot_seasonal and n not in skipped_buys}
    new_held = (base_held | defer_s) - skip_b

    c_held = score[list(new_held)]
    raw = c_held - c_held.min() + FLOOR
    return raw / raw.sum(), new_held, defer_s, skip_b


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    seasonal = SB.seasonal_score(prices)

    rows = {}
    held = {lb: set() for lb in LOOKBACKS}
    deferred_sells = {lb: set() for lb in LOOKBACKS}
    skipped_buys = {lb: set() for lb in LOOKBACKS}
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

        end = positions[dt] - EVAR_LAG + 1
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
        risk_score = _demean_by(-evar, G.TYPE_OF, MIN_TYPE)

        common = common.intersection(risk_score.index)
        if len(common) < CORE_N:
            continue

        seasonal_row = seasonal.loc[dt] if dt in seasonal.index else None
        top_seasonal, bot_seasonal = _deferral_sets(seasonal_row, common)

        z_risk = _zscore(risk_score[common])
        leg_targets = []
        for lb in LOOKBACKS:
            score = _zscore(moms[lb][common]) + z_risk
            t, held[lb], deferred_sells[lb], skipped_buys[lb] = _leg_target(
                score, held[lb], top_seasonal, bot_seasonal,
                deferred_sells[lb], skipped_buys[lb],
            )
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
