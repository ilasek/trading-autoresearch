"""Rebalance-phase vintages: the one vintage axis with neither of the two confounds
that explain why the other two cost validation Sharpe.

THE STATE OF THE VINTAGE QUESTION. This repo's strongest mechanism is averaging one
selection procedure over vintages, and three vintage axes have now been measured:

    axis                      mean weight overlap   verdict
    buffer-band vintages            0.963           killed free (fringe only, #46 night)
    formation-DATE vintages (K=6)   0.645           live; costs 0.094 val Sharpe (#46)
    instrument-SUBSAMPLE folds      0.851 / 0.43-0.48 pairwise
                                                    live; costs 0.021 val Sharpe (#47)

Both live axes lost, and `learnings.md` records a specific, *different* reason for
each. The date axis pays a **staleness** price: K=6 holds formations up to six months
old, and #46 showed the whole 3.4pp/yr return gap is return, not cost. The subsample
axis pays a **pool-restriction** price: each fold picks its top 15 out of ~93
instruments instead of 140, and #47's own reading was that the aggregation gain was
"almost exactly large enough to pay for" that bias, leaving the de-concentration tax
as the residual deficit.

Neither reason is a statement about vintage averaging itself. That leaves an obvious
question the lab has never asked: **is there a vintage axis that pays neither price?**

THE AXIS. Rebalance *phase*. Every vintage runs the champion's entire construction on
the full 140-instrument universe at the champion's own monthly cadence and with the
champion's own maximum signal age — the only difference is *where in the month* the
month falls. Four vintages form on the first trading day on or after the 1st, 8th,
15th and 22nd; the book is their equal-weighted average. No fold restricts the pool,
so there is no selection bias; no tranche is ever more than one month old, so there is
no staleness. This is also exactly the object the rebalance-timing-luck literature
describes (`research/SUMMARY.md`, portfolio-construction section): the phase of a
discrete rebalance cycle is uncompensated variance — no phase is better ex ante — and
a single-vintage backtest is one draw from that distribution. The champion is one such
draw. What has never been tested here is whether standing at the centre of that
distribution is worth anything on the gate's own axis.

PRE-TRIAL DIAGNOSTICS (holdings only, prices truncated 2023-12-31, no returns scored,
trial count untouched). Three screens, all run before this file was written.

1. *Is the axis live?* Mean pairwise weight overlap between four phase books of this
   cadence is **0.796** (measured on the quarter-points of each month's trading days,
   an equivalent four-phase scheme), far below the 0.963 that killed buffer-band
   vintages for free and in the same range as the date axis (0.645) and the subsample
   axis. Against the champion's own book this candidate's averaged book overlaps
   **0.859** in composition.
2. *Core or fringe?* The 2026-08-19 screen — a vintage axis is only a vintage axis if
   its members disagree about membership in the **core**, not the fringe. On the same
   measure #47 used, L1 disagreement against the champion's book is **0.118 inside its
   top-10 names** against **0.165** across the entire rest of the book; #47's
   subsample folds, which the lab accepted as core-re-drawing, scored 0.140 against
   0.159. Somewhat weaker than that axis, unambiguously live against the buffer-band
   one. (The top 10 names carry 69.7% of champion weight, so the fringe's larger raw
   number is spread over 25 names holding 30%.)
3. *What does it cost?* This is where the axis differs from every previous one, and it
   is the reason to expect a different answer. Positions rise 35.1 -> 45.7, but the
   book barely de-concentrates: HHI 0.0758 -> 0.0720 (-5%), top weight 0.1720 ->
   0.1693 (-2%). The **risk**-contribution vector — mandatory since #47 for any
   concentration claim — barely moves at all: top-name risk share 0.327 -> 0.325,
   effective bets by risk 7.7 -> 7.8. Turnover falls 2.8%. Mean gross exposure is
   identical at 0.984, so the trim overlay is not doing anything different either.

PRE-REGISTERED EFFECT SIZES. The repo prices de-concentration at ~0.02 Sharpe per ~30%
HHI reduction; at -5% that is **~0.003 Sharpe of tax**, an order of magnitude below the
0.021 that decided #47 and effectively nothing. Cost saving is ~0.02pp/yr, also
nothing. So unlike #46 and #47 this trial is not a risk/return dial: the two nuisance
terms are both near zero and whatever the result is, it is close to a clean reading of
what phase decorrelation is worth. Because the risk axis does not move, maxDD is
predicted **not** to improve — the #47 mechanism is absent here, which is itself the
falsifiable half: if maxDD improves materially anyway, the risk-contribution statistic
does not capture what drives this book's drawdowns and `learnings.md` owes an
amendment.

A FREE BY-PRODUCT, RECORDED BECAUSE IT CORRECTS TONIGHT'S NEWEST RESEARCH SCREEN.
`research/SUMMARY.md` candidate #2's third part (added 2026-08-20) offers a
closed-form, holdings-only prediction of a K-leg combination's turnover:
`sqrt((1+rho(K-1))/K)` in the correlation of the legs' rebalancing trades. Measured
here, rho = 0.083, predicting a ratio of 0.559 — a 44% turnover saving. The realised
ratio is **0.961**. The screen fails because these four legs rebalance on *disjoint
days*: trades that never occur on the same day cannot net, so the measured correlation
is near zero for a reason that has nothing to do with the diversification the formula
prices. The closed form assumes simultaneous rebalancing, and it reads *most*
optimistic exactly where it is *least* applicable. That boundary is worth more than
this trial's headline if the headline is a null.

HYPOTHESIS AND FALSIFICATION. If averaging weakly-correlated vintages of one unstable
selection procedure raises realised net Sharpe on its own — rather than only when it
also buys staleness or breadth — the phase-averaged book beats the champion's 1.201,
because it is the first axis to supply the decorrelation without either price. Landing
at or below 1.201 with the two nuisance terms measured this small says something
stronger than either previous null: that on this validation window the single
concentrated vintage wins regardless of what supplies the decorrelation, which would
make three-for-three and would point the whole vintage story at the window rather than
at the mechanism.

CAVEATS RECORDED IN ADVANCE. (a) This is not a K sweep and does not deepen the tranche
stack: signal age, pool, cadence, buffer, weighting and both trim constants are
untouched, and four phases of a monthly cycle is the natural count, not a tuned one.
(b) Per the timing-luck source, the champion is one draw and this candidate is near the
centre of the same distribution, so a small gap in either direction should be read as
the timing-luck scale itself rather than as evidence — the pre-registered reading is
therefore direction and size against the ~0.003 tax, not whether the gate fires.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_phase4",
    "family": "combinations",
    "hypothesis": (
        "Averaging the champion's entire construction over four rebalance-phase "
        "vintages — formed on the first trading day on or after the 1st, 8th, 15th "
        "and 22nd of each month, every vintage using the full instrument pool at the "
        "champion's own monthly cadence and maximum signal age, with signal, buffers, "
        "magnitude weighting, cohort trim and both constants otherwise identical — "
        "lands validation Sharpe above the champion's 1.201 net of 15 bps costs, "
        "because it is the first vintage axis measured here that supplies genuine "
        "membership decorrelation (mean pairwise weight overlap 0.796, composition "
        "overlap 0.859 against the champion, core-vs-fringe L1 disagreement 0.118 on "
        "its top-10 names against 0.165 on the whole rest) while "
        "paying neither of the prices that explain the other two live axes' losses — "
        "no staleness, since no tranche is over one month old, and no pool "
        "restriction, since no fold is taken — and while barely moving either "
        "concentration statistic (HHI -5%, top-name risk share 0.327 -> 0.325), which "
        "prices the de-concentration tax at ~0.003 Sharpe; landing at or below 1.201 "
        "with those nuisance terms this small shows the concentrated single vintage "
        "wins on this window regardless of what supplies the decorrelation."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

PHASE_DAYS = (1, 8, 15, 22)

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


def _phase_dates(index: pd.DatetimeIndex, day_of_month: int) -> set:
    """First trading day on or after `day_of_month` in each calendar month.

    Anchored to the calendar, not to a month's trading-day count, so the date set
    for any month is fixed once that month's data exists — truncating the tail of
    the price history never moves an earlier phase date.
    """
    out = set()
    for _, grp in index.to_series().groupby(pd.Grouper(freq="ME")):
        eligible = grp.index[grp.index.day >= day_of_month]
        if len(eligible):
            out.add(eligible[0])
    return out


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    phases = [_phase_dates(prices.index, d) for d in PHASE_DAYS]
    all_rebalances = sorted(set().union(*phases))

    held = [{lb: set() for lb in LOOKBACKS} for _ in PHASE_DAYS]
    live = [None] * len(PHASE_DAYS)     # each phase's most recent target

    rows = {}
    base_periods = []
    all_dates = prices.index
    max_lb = max(LOOKBACKS)

    for i, dt in enumerate(all_rebalances):
        hist = prices.loc[:dt]
        if len(hist) < max_lb + SKIP + 1:
            continue

        for p in range(len(PHASE_DAYS)):
            if dt not in phases[p]:
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
                t, held[p][lb] = _leg_target(score, held[p][lb])
                leg_targets.append(t)
            t = pd.concat(leg_targets, axis=1).fillna(0.0).mean(axis=1)
            live[p] = t / t.sum()

        active = [t for t in live if t is not None]
        if not active:
            continue

        blended = pd.concat(active, axis=1).fillna(0.0).mean(axis=1)
        norm = blended / blended.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full

        start_pos = all_dates.get_loc(dt)
        nxt = all_rebalances[i + 1] if i + 1 < len(all_rebalances) else None
        end_pos = all_dates.get_loc(nxt) if nxt is not None else len(all_dates)
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

        for dt2, scale in scale_series.iloc[start_pos:end_pos].items():
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
