"""Trial #49 measured what doing nothing is worth. This asks whether doing less pays more.

WHAT #49 ESTABLISHED, TONIGHT, AND WHY IT MOTIVATES THIS. Every magnitude-weighted book
in this repo sets its weights once a month from a composite that skips the most recent
21 days, then leaves them alone. The realised weight vector on any day is therefore the
formation-date vector tilted by each name's trailing 0-21 day return. #49 deleted that
tilt — same membership (held-set identical on 75 of 75 month-ends), weights recomputed
from the current composite every five trading days — and it cost **0.142 of validation
Sharpe against a pre-registered headwind of 0.035**, leaving ~0.09 Sharpe and ~3.7pp of
annual return attributable to the drift itself, and it lost in **every one of the six
validation years**. The reading recorded there: the trailing-month return is
cross-sectional *reversal* when used to rank the whole universe (which is why the
skip-month is load-bearing in selection) and *continuation* when used to re-weight a
basket whose membership was already chosen on 3-12 month momentum — the same statistic
with opposite signs at two steps.

THE OBVIOUS NEXT QUESTION, AND IT IS NOT A KNOB. If one month of un-re-sized drift is
worth that much, is the monthly re-size itself — the thing that throws the tilt away
twelve times a year — costing the same way? The structural limit of the mechanism is
"never re-score an incumbent": at each monthly rebalance the buffer chains update as
usual and exits are sold and entrants bought, but a name that was held and is still held
keeps its **relative** weight, whatever the market has made of it, instead of being
reset to what its current composite says. Only the scale changes, through renormalisation.
That is one change, it is structural rather than parametric, and there is no second
value of it to try.

It also happens to be the shape `research/SUMMARY.md` says this repo's cost model
selects — under proportional costs the optimal policy "exhibits periods of no trading",
i.e. a no-trade region, and the champion currently applies one to *membership* only
while re-sizing every weight every month regardless. That is a mechanism-shape argument
and nothing more: no performance expectation is imported from it, and per `learnings.md`
the cost lever itself is spent, so this trial is **not** proposed as a cost idea. The
cost saving is a pre-registered tailwind to be netted out.

PRE-TRIAL DIAGNOSTICS (holdings only, prices truncated 2023-12-31, no returns scored):

    positions          35.1 -> 35.1     (membership untouched, same buffer chains)
    HHI                0.0758 -> 0.0846 (+11.5%)
    top weight         0.1720 -> 0.1908 (+10.9%)
    turnover           5.59x  -> 3.82x  (-31.7% on the pre-engine measure)
    top-name RISK share 0.327 -> 0.317  }  the axis #47 showed actually predicts
    effective risk bets  7.7  -> 7.7    }  drawdown: unchanged
    weight overlap vs the champion's book: 0.616 — the largest change of the session

PRE-REGISTERED TAILWIND, ~0.031 SHARPE, AND WHY BOTH TERMS ARE STATED AS TAILWINDS.
Weight concentration rises 11.5%, and this repo has priced concentration on this signal
at ~0.02 Sharpe per 30% of HHI in the *favourable* direction, so ~**+0.008**. Turnover
falls ~0.54pp/yr at the learnings file's 0.15%/yr-per-turn rate against an annual vol
of 0.232, so ~**+0.023**. **The bar is therefore 1.232, not 1.201**: landing between
1.201 and 1.232 would clear the gate on nuisance terms alone and should be read as a
null on the mechanism, and this file is stating that in advance precisely because the
gate cannot. Landing above 1.232 says drift beyond one month keeps paying. Landing
below 1.201 says the mechanism is horizon-limited — continuation over ~a month,
something else over a quarter — which would be the more interesting answer, because it
would put a *length* on the tilt #49 discovered rather than only a sign.

The risk-contribution vector being flat is the second pre-registration: per #47,
validation maxDD tracks the risk axis and not the weight axis, so maxDD is predicted to
land near the champion's -28.7% despite the weight concentration rising. If it widens
materially anyway, the risk-contribution statistic does not capture what drives this
book's drawdowns and `learnings.md` owes an amendment — the same falsifier #48 carried
and passed.

A FREE KILL RECORDED SO IT IS NOT REDISCOVERED AS THE OBVIOUS IMPLEMENTATION. The
natural way to write "trade only for membership changes" is the exact cash-flow rule:
sell the exits, buy the entrants with the proceeds, touch nobody else. Measured, that
rule silently destroys magnitude weighting — HHI **-21.9%**, top-name risk share 0.327
-> **0.182**, effective risk bets 7.7 -> **13.1**, i.e. the book flattens toward equal
weight. The reason is the buffer: with a hold-25/enter-15 band very little capital is
freed in a typical month, so entrants can never be sized on their score, and after a
few years a name's weight reflects the freed capital available on its entry date rather
than its momentum. Since the repo's own ladder puts magnitude weighting ~0.13 Sharpe
above equal weight, that variant is a predictable loss for a reason unrelated to the
question being asked, and it was not built. The version tested here keeps entrants on
the score scale and leaves only incumbents' *relative* weights alone.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_no_resize",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Never re-scoring an incumbent's weight — the four per-horizon buffer chains "
        "update monthly as usual and entrants are sized on the current composite, but "
        "a name held last month and still held keeps its drifted relative weight "
        "instead of being reset, with signal, membership, transform, cohort trim and "
        "both constants otherwise identical — lands validation Sharpe above 1.232 net "
        "of 15 bps costs, because trial #49 measured intra-month drift at ~0.09 Sharpe "
        "and ~3.7pp of annual return in all six validation years, and the monthly "
        "re-size discards that tilt twelve times a year; 1.232 rather than the "
        "champion's 1.201 is the bar because the change carries a pre-registered "
        "tailwind of ~0.031 Sharpe (HHI +11.5% ~ 0.008, turnover -31.7% ~ 0.023), so "
        "landing between 1.201 and 1.232 is a null on the mechanism despite clearing "
        "the gate, and landing below 1.201 shows the drift tilt is horizon-limited to "
        "about a month rather than compounding."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

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
    base_periods = []
    prev_norm = None
    prev_dt = None

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

        if prev_norm is not None:
            gross = prices.loc[dt] / prices.loc[prev_dt]
            drifted = (prev_norm * gross.reindex(prev_norm.index)).dropna()
            drifted = drifted[drifted > 0]
            if len(drifted):
                drifted = drifted / drifted.sum()
                mixed = pd.Series(0.0, index=target.index)
                for name in target.index:
                    # incumbents keep their drifted relative weight; entrants are
                    # sized on the current composite, as the champion sizes everyone.
                    mixed[name] = drifted[name] if name in drifted.index else target[name]
                if mixed.sum() > 0:
                    target = mixed / mixed.sum()

        norm = target
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        prev_norm, prev_dt = norm, dt

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
