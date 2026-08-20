"""The champion skips the most recent month in its signal and then rides it in its
weights. This deletes the second half of that sentence.

WHAT THE CODE ACTUALLY DOES, WHICH IS NOT WHAT ANY WRITE-UP HERE HAS SAID. Every
magnitude-weighted candidate in this repo since trial #20 sets its weights once a month
from a composite that deliberately **skips the most recent 21 days** — `learnings.md`
and `research/SUMMARY.md` candidate #11 both record the skip as load-bearing, and both
echo-literature sources agree the omitted month carries reversal rather than
continuation. Between those monthly rebalances the book is never touched: positions
drift with prices. Drift is not neutral. A name that ran hard since formation ends the
month with a larger share of the book, and a name that fell ends with a smaller one —
so the *realised* weight vector on any given day is the formation-date weight vector
tilted by the trailing 0-21 day return. **That is a momentum tilt over exactly the
horizon the signal refuses to use, applied silently, by omission, at the weighting step
rather than the selection step.** No trial here has ever examined it; it is inherited by
every candidate the lab has ever run, including all three of tonight's rejected vintage
axes and the champion.

This is the same class of finding as trials #37-#40 (the trim's `dropna` filter reading
an eleven-name legacy cohort) and `learnings.md`'s distilled rule from them — *before
crediting a component, check what its code actually reads*. Here the component is the
one nobody thought of as a component: the twenty-one days of doing nothing.

THE CHANGE, AND IT IS ONE CHANGE. Membership is untouched — the four per-horizon buffer
chains still update on the champion's monthly schedule, and a pre-trial diagnostic
confirms the held-set is **identical on 75 of 75 month-end snapshots** and average
positions are unchanged at 35.1. The only difference is that the magnitude weights are
recomputed from the *current* composite every five trading days instead of being left to
drift for twenty-one. Signal, lookbacks, skip, buffer widths, transform, FLOOR, cohort
trim, SPIKE_RATIO and TRIM_SCALE are all inherited untouched. Five days is not a tuned
value: it is the coarsest cadence that is materially faster than the 21-day horizon the
tilt operates over, and no other value will be tried this session either way.

WHY THIS IS NOT THE RETIRED COST-MITIGATION CLASS. `learnings.md` retires no-trade
bands, weight-change thresholds and cheaper rebalance mechanics on the grounds that
total cost drag is ~0.019 Sharpe at 3.0x turnover, so nothing can be won there. That
verdict is about ideas whose *purpose* is to trade less. This one trades **more** and
pays for it; the cost term is a pre-registered headwind to be netted out, not the
mechanism. The mechanism is what the book holds.

PRE-TRIAL DIAGNOSTIC AND PRE-REGISTERED HEADWIND (holdings only, prices truncated
2023-12-31, no returns scored, trial count untouched):

    positions        35.1  -> 35.1     (membership identical, 75/75 month-ends)
    HHI              0.0758 -> 0.0687  (-9.4%)
    top weight       0.1720 -> 0.1562  (-9.2%)
    turnover         5.59x  -> 8.81x   (+57.6% on the pre-engine measure)
    weight overlap   0.874 against the champion's own book

Two headwinds follow and both are quantified in advance. The de-concentration is
**-9.4% of HHI**, which this repo has priced at ~0.02 Sharpe per 30%, so ~**0.006**.
The turnover rise is ~0.68pp/yr at the learnings file's 0.15%/yr-per-turn rate against
an annual vol of 0.232, so ~**0.029**. Total pre-registered headwind ~**0.035 Sharpe**.
Note the direction of the concentration move is itself the mechanism showing up in the
holdings: re-sizing *removes* concentration precisely because drift *adds* it, and what
drift adds it adds in proportion to the last month's return.

HYPOTHESIS AND FALSIFICATION, WITH ALL THREE OUTCOMES PRE-READ. If the skip-month
lesson governs weights as well as selection, deleting an unintended 0-21 day momentum
tilt is worth more than 0.035 Sharpe and the candidate beats 1.201. Landing **~0.035
below** says the tilt is worth about nothing — the reversal effect operates on which
names are chosen but not on how a held set is weighted, which would be a real
qualification of a lesson currently stated without that boundary. Landing **materially
further below** says the opposite of the prior: intra-month drift is actively *good*,
"let winners run" beats the skip-month prior at the weighting step, and the champion's
accidental tilt is a component to credit rather than remove — in which case the honest
next question is whether it should be deliberate rather than accidental, and that
question would belong to a session with its own rationale, not to this one.

CAVEAT. A null near -0.035 cannot separate "the tilt is worthless" from "the tilt is
worth roughly what the extra trading costs"; only the size and sign of the miss are
being pre-registered, per `learnings.md`'s rule that the trial supplies the sign.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_hzn_avg4_weekly_resize",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Recomputing the champion's magnitude weights from the current composite "
        "every five trading days instead of letting them drift with prices for "
        "twenty-one — membership, buffer chains, lookbacks, skip-month, transform and "
        "cohort trim all identical, and the held-set verified identical on 75 of 75 "
        "validation month-ends — lands validation Sharpe above the champion's 1.201 "
        "net of 15 bps costs, because leaving weights to drift silently tilts the book "
        "by each name's trailing 0-21 day return, which is exactly the horizon the "
        "signal's skip-month deliberately excludes as carrying reversal rather than "
        "continuation, so the champion skips the recent month in selection and then "
        "rides it in weighting; the change carries a pre-registered headwind of about "
        "0.035 Sharpe (HHI -9.4% ~ 0.006, turnover +57.6% ~ 0.029), so landing about "
        "that far below shows the skip-month lesson does not extend from selection to "
        "weighting, and landing materially further below shows intra-month drift is an "
        "actively useful component rather than an artifact."
    ),
}

LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

RESIZE_EVERY = 5

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


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    all_dates = prices.index
    month_ends = set(prices.groupby(pd.Grouper(freq="ME")).tail(1).index)
    max_lb = max(LOOKBACKS)

    held = {lb: set() for lb in LOOKBACKS}
    rows = {}
    base_periods = []
    pending = []          # (position, date, weights) awaiting its period end

    for i, dt in enumerate(all_dates):
        if i < max_lb + SKIP + 1:
            continue
        is_month = dt in month_ends
        # Position-based cadence: index positions of past dates never move when the
        # tail of the price history is truncated, so this is truncation-stable.
        is_resize = (i % RESIZE_EVERY) == 0
        if not (is_month or is_resize):
            continue

        hist = prices.iloc[:i + 1]
        moms = {lb: _momentum(hist, lb) for lb in LOOKBACKS}
        common = None
        for m in moms.values():
            common = m.index if common is None else common.intersection(m.index)
        if len(common) < CORE_N:
            continue

        leg_targets = []
        for lb in LOOKBACKS:
            score = _zscore(moms[lb][common])
            if is_month:
                ranked = score.sort_values(ascending=False)
                held[lb] = ((held[lb] & set(ranked.index[:BAND_N]))
                            | set(ranked.index[:CORE_N]))
            names = [n for n in held[lb] if n in score.index]
            if not names:
                continue
            c_held = score[names]
            raw = c_held - c_held.min() + FLOOR
            leg_targets.append(raw / raw.sum())
        if not leg_targets:
            continue

        target = pd.concat(leg_targets, axis=1).fillna(0.0).mean(axis=1)
        norm = target / target.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full
        pending.append((i, norm))

    for j, (start_pos, norm) in enumerate(pending):
        end_pos = pending[j + 1][0] if j + 1 < len(pending) else len(all_dates)
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
