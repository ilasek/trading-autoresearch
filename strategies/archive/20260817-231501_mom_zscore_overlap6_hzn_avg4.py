"""Does the *width* of the lookback bracket matter, or only that there is more
than one?

WHAT TRIAL #41 LEFT OPEN. Averaging the two horizon legs as portfolios rather
than as scores was promoted, but its two lookbacks (252 and 126) were
inherited from the champion, not chosen — they are the bracket the repo
happened to already have. The averaging-over-estimation-windows method that
motivated it (`research/SUMMARY.md` candidate #7) does not average two
windows; it averages a model over a *range* of window lengths precisely
because the bias-variance optimum is unknown and estimating it from a short
noisy sample is the mistake that whole literature warns against. So the open
question after #41 is whether the gain is about horizon diversity as such —
in which case a wider bracket should extend it — or specifically about those
two windows, in which case widening should do nothing or hurt.

THE CHANGE, AND IT IS ONE CHANGE. Four evenly spaced quarterly windows —
3-1, 6-1, 9-1, 12-1 (63/126/189/252 trading days, all skipping the same 21
days) — each with its own buffer chain, own held-set and own
magnitude-weighted target, averaged at equal weight into the month's target.
Everything else is trial #41 exactly: same skip, same hold-25/enter-15 band,
same `c - c.min() + FLOOR` weighting, same six-tranche date overlap, same
daily vol-spike trim, same equal weighting between legs.

WHY THIS IS A BOUNDED ARGUMENT AND NOT A PARAMETER SWEEP. `learnings.md`
forbids sweeping knobs, and `research/SUMMARY.md` candidate #12 gives the
form a legitimate depth argument must take: two bounds and no scan. The same
discipline applies here, and both bounds come from outside the data. At the
short end, the skip-month is load-bearing (both echo-literature sources agree
the most recent month carries reversal, not continuation) — 3-1 is the
shortest window that still clears it with a full quarter of formation signal
behind it. At the long end, 12-1 is where the momentum literature's formation
window ends and post-formation reversal begins. Four evenly spaced windows
fill that interval; nothing is chosen by performance, and no alternative
bracket will be tried in this session, because comparing brackets *is* the
sweep the manual forbids.

WHY IT IS NOT A SIGNAL-DEFINITION IDEA. `learnings.md` closes "find a better
score" as heavily explored and low-yield. This does not look for a better
score — it declines to pick one. The 3-1 and 9-1 windows are not proposed as
improvements on 12-1; they are additional equally-weighted estimates of the
same quantity, which is the case forecast-combination theory endorses and the
case #41 passed.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below trial #41's 1.112. Two
distinguishable failure modes, and the diagnostics will tell them apart: if
the wider bracket simply de-concentrates further (average positions climbing
well past #41's 47) while Sharpe slips, the gain in #41 was breadth bought at
the usual concentration price rather than horizon diversity; if Sharpe falls
sharply, the short windows are carrying reversal the skip-month does not
fully remove and horizon diversity has a floor.

CAVEATS RECORDED IN ADVANCE. (a) As in #41, widening the book perturbs the
`held ∩ legacy-cohort` intersection that trials #37-#40 showed carries ~0.026
of the champion's Sharpe as sampling luck, so a small difference either way
is not clean evidence. (b) #41 itself was promoted on a 0.005 validation
margin; the bar this candidate must clear is therefore itself uncertain, and
the comparison worth reading is the *direction and size* of the move, not
whether it crosses.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_hzn_avg4",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Widening the averaged lookback bracket from two windows (12-1, 6-1) "
        "to four evenly spaced quarterly windows (12-1, 9-1, 6-1, 3-1), each "
        "forming its own buffered magnitude-weighted portfolio averaged at "
        "equal weight, with the six-tranche date overlap, band, weighting and "
        "daily vol-spike trim otherwise identical to trial #41, raises "
        "validation Sharpe above that candidate's 1.112 net of 15 bps costs, "
        "because the gain from portfolio-level horizon averaging is horizon "
        "diversity as such — bracketing an unknown bias-variance optimum "
        "rather than estimating it — and not a property of the particular two "
        "windows the repo inherited."
    ),
}

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
