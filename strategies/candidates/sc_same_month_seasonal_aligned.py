"""Same-calendar-month seasonality, with the target-month alignment corrected.

WHAT THIS IS AND WHY IT IS A SEPARATE TRIAL. Trial #59
(`sc_same_month_seasonal.py`) implemented the same signal but computed the
month it was predicting as `(rebalance_date + MonthEnd(1)).month`. Rebalance
dates are the last *trading* day of a month, and on **29.8% of train-split
month-ends that is not the last calendar day** — on those months `MonthEnd(1)`
rolls forward only as far as the calendar month-end and returns the month that
has just *ended*. So #59 measured a roughly 70/30 mixture of the intended
signal and the misaligned one, and the misaligned one was separately measured
on the train split as a null (Q5-Q1 -0.49%/yr, t = -0.17, versus +15.7%/yr,
t = +5.16 for the corrected alignment). Its recorded 0.671 is therefore not a
clean reading of the family.

#59's file is deliberately left exactly as it ran: it is the record of what was
measured and `CLAUDE.md` forbids rewriting trial history. This file changes one
expression and nothing else, so the pair is a controlled measurement of what
the alignment is worth **in a costed book** rather than in a quintile spread —
which is a question the lab has never had a clean answer to, and the reason
this correction is worth a trial rather than a footnote.

Everything below is unchanged from #59 and still applies.

WHY THIS TRIAL EXISTS, AND WHY IT ALMOST DID NOT. `research/SUMMARY.md` #48
pre-registered a free screen that was supposed to open or close this family
before a trial was spent: Heston-Sadka's result is a *sign* prediction, so the
cross-sectional winner-minus-loser spread should be **positive** when names are
sorted on their own returns in the annual lags (t-12, t-24, ...) and **negative**
when sorted on the non-annual months of the same intervals. That screen was run
tonight on the train split only. **It failed.** Both sorts are positive and of
similar size — annual lags +15.7%/yr (t = +5.16), non-annual +12.8%/yr
(t = +3.70) — so the contrast that identifies a calendar seasonal, as opposed to
a persistent cross-sectional difference in mean return, is absent on this
universe. Taken literally, #48 says the family closes here.

The trial is run anyway, on one piece of information the pre-registration did
not anticipate and which changes what the failure means. Orthogonalising the
annual-lag score against the same name's long-run mean — score = (average
return in the target calendar month) minus (average return in every other
month) — leaves a top-minus-bottom spread of **+11.7%/yr (t = +3.97)** and a
top-minus-universe spread of +8.8%/yr (t = +4.77). The identifying *contrast*
is gone, but the same-month component is not simply the long-run mean wearing a
calendar label. That is a real disagreement with the source's own identification
strategy and it is worth one scout to price, because pricing it is the only way
to learn whether the surviving component is tradeable net of the turnover the
authors themselves say kills it.

WHAT THE SIGNAL IS. At each month-end, for the calendar month *about to start*,
score each instrument by the mean of its last 20 realised returns in that
calendar month minus the mean of its last 240 returns in other months, using
monthly returns strictly before the current month. Hold the top 25 equal
weighted, with an enter-25 / hold-45 band.

A LIBRARY NOTE, RECORDED BECAUSE IT IS THE REASON THIS FILE DOES NOT USE THE
SHIPPED HELPER. `strategies/lib/features.seasonal_same_month_return` averages
the calendar month **that has just ended** and publishes it on that month-end
row. The engine forward-fills and lags, so that value is held through the
*following* month — it scores month M and is traded in month M+1, one month off
the signal it is named for. Measured on the train split, the shipped alignment
is a null (Q5-Q1 -0.49%/yr, t = -0.17) where the corrected alignment is
+15.7%/yr (t = +5.16). `CLAUDE.md` forbids editing an existing `strategies/lib`
file, correctly, so the correction lives here and the finding is journaled
rather than patched.

WHAT WOULD FALSIFY IT. A validation Sharpe at or below the 0.49 equal-weight
floor. Two failure modes are pre-registered as the most likely, in order.
(a) **Turnover.** The score is recomputed for a different target month every
month, so unlike a momentum sort there is no reason for consecutive months'
selections to overlap; Heston-Sadka draw this distinction themselves and doubt
the round trip is worth paying for. The band is the only defence and it is a
weak one. If validation turnover lands above roughly 12x, the ~1.8%/yr of cost
drag is most of any plausible edge and the family's verdict is about cost, not
about signal. (b) **Survivorship.** A signal built from twenty years of a name's
own history, on a universe defined by who is listed *today*, is the severe case
of the conditioning problem in
`research/notes/2026-08-26-survivorship-conditioning-and-spurious-persistence.md`
— the claim being tested is itself a persistence claim. The orthogonalisation
removes the *level* of a name's long-run mean, which is the part of that bias
most likely to be mechanical, but it does not remove the bias.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sc_same_month_seasonal_aligned",
    "family": "seasonality-calendar",
    "track": "scout",
    "hypothesis": (
        "Scoring each instrument by its average realised return in the calendar month "
        "about to start, minus its average return in all other months, and holding the "
        "top 25 equal-weighted with an enter-25/hold-45 band, earns a validation Sharpe "
        "above the 0.49 equal-weight floor net of 15 bps costs — i.e. the same-calendar-"
        "month component that survives orthogonalisation against a name's long-run mean "
        "is tradeable despite the full monthly re-selection it forces."
    ),
}

ANN_YEARS = 20        # same-month observations averaged
NON_MONTHS = 240      # other-month observations averaged
MIN_SAME = 5          # need at least this many same-month observations
CORE_N = 25
BAND_N = 45


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    # Position of each calendar month in `monthly`, so a daily rebalance date can
    # be mapped to "months strictly before mine".
    month_pos = {p: i for i, p in enumerate(monthly.index.to_period("M"))}

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices):
        i = month_pos.get(dt.to_period("M"))
        if i is None or i < MIN_SAME * 12:
            continue
        past = mret.iloc[:i]                    # strictly before the current month
        # The month being predicted is the one that starts after this rebalance.
        # `MonthBegin(1)`, not `MonthEnd(1)`: rebalance dates are the last
        # *trading* day of a month, which on 29.8% of train-split months is not
        # the last calendar day — and on exactly those months `MonthEnd(1)`
        # rolls forward only to the calendar month-end and returns the month
        # that has just ENDED. That is the bug this file exists to correct.
        target = (dt + pd.offsets.MonthBegin(1)).month

        same = past[past.index.month == target].tail(ANN_YEARS)
        other = past[past.index.month != target].tail(NON_MONTHS)
        if len(same) < MIN_SAME or len(other) < 24:
            continue

        score = (same.mean() - other.mean()).dropna()
        score = score[same.notna().sum() >= MIN_SAME]
        if len(score) < BAND_N:
            continue

        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        # Hysteresis. The signal re-selects from scratch every month by
        # construction, so this band is doing more work here than in any other
        # candidate in the repo — and it is the pre-registered failure mode.
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
