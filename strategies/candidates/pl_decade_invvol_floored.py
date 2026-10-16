"""Risk weighting inside an already-selected slice, with the weight vector kept
permutation-mild so the gain is not handed back to the candidate's own null.

THE CLAIM IN ONE LINE. v3's random-selection null copies a candidate's weight
*vector* onto region-matched replacement names, so a vector fitted to the names
actually held is destroyed in the replicas -- but a vector with a heavy TAIL also
widens the null's dispersion, and the gate sits at the null's 90th percentile, not
its median. Flooring the inverse-volatility weights at the slice's own bottom
quintile keeps the whole of the risk-weighting gain while leaving the vector mild
enough that the null's dispersion stays at the equal-weight floor -- which is the
only way the gain reaches the gate.

WHY THIS RE-OPENS A LINE `learnings.md` CLOSED, AND WHAT IS DIFFERENT. The
2026-10-13 entry concludes "THE WHOLE WEIGHTING AXIS IS DEAD", measured on four
books over the *whole pool*: equal weight restored monthly (+0.524), held from one
start (+0.569), restored annually (+0.456) and a FIXED UNEQUAL vector restored
monthly (+0.529, i.e. +0.10%/yr against equal weight, t +0.56). Every one of those
is a vector chosen without reference to the names it lands on. None of them tests a
vector *fitted to the held names' trailing risk inside a selected slice*, which is
the object research `#260` proposes and the object measured below. The refusal
stands exactly where it was measured -- on the pool, with an unfitted vector -- and
this candidate is the case it did not cover.

TONIGHT'S FREE SCREENS (train 1997-2017 only, 216-264 monthly decision rows; no
validation, holdout, forward or incubation number was read, and no portfolio
outside this sheet was scored. Journal F4, F6, F7, F8 of 2026-10-15/16.)

*F4 -- risk weighting raises skill and pays for it in null dispersion.* Same 100
names every month, only the weight vector changing; null = 40 region-matched
replicas of each book, train:

    weight vector inside the slice      sr     skill   null med   null sd   sel    margin
    equal weight [baseline]           +0.628   +0.104    +0.514    0.0213  +0.114   +0.096
    1/sigma (126d close-to-close)     +0.644   +0.120    +0.499    0.0375  +0.144   +0.100
    1/sigma^2                         +0.665   +0.141    +0.514    0.0584  +0.151   +0.088

Skill rises monotonically and the *margin over the gate* does not: the null median
does drop for 1/sigma, so the permutation really cannot imitate the fit, but the
dispersion rises faster than the selection term and the p90 gate eats the gain.
Read alone this table declines `#260`.

*F8 -- what the dispersion actually responds to is the vector's TAIL.* Unfloored
1/sigma puts 9.4% of the book in its largest name on average and leaves 33.4
effective names (1/HHI) out of 100; its entire skill advantage sits in one train
sub-period (+0.189 in 1997-2008 against +0.001 in 2009-2017). Flooring sigma at the
slice's own 20th percentile:

    book                         sr    skill   97-08   09-17   1/HHI   maxw    null sd   sel    margin
    equal weight [baseline]    +0.628  +0.104  +0.103  +0.023   107.1  0.0093   0.0213  +0.114  +0.096
    1/sigma unfloored          +0.644  +0.120  +0.189  +0.001    33.4  0.0943   0.0375  +0.144  +0.100
    1/sigma floored at p20     +0.644  +0.120  +0.136  +0.034   100.0  0.0123   0.0210  +0.137  +0.121  <- run

The floor keeps the full +0.120 of skill, restores effective breadth to the book's
own size, balances the sub-periods, holds the null's dispersion at the equal-weight
floor (0.0210 against 0.0213) and so converts the skill gain into **+0.121 of gate
margin against the baseline's +0.096** -- the first construction in six v3 trials
to improve the margin on the gate that has decided all five recorded ones. Book
volatility 17.05% against the pool's 18.1%, beta 0.909.

The floor was tested at exactly one value, the quintile, chosen a priori as a
breadth guard rather than searched; "no floor" and "p20" are the whole of the two
cells, as the 10- and 20-year windows were for the score underneath.

*The staleness explanation for the unfloored tail was checked and is WRONG.* A
natural reading of 1/sigma's concentration is that a carried close reads as a zero
return and deflates sigma, so 1/sigma is partly 1/(print coverage). Recomputing
sigma on printing days only (`volume` is not forward-filled, so a NaN is a
non-print) reproduces the naive book to three decimals, because print coverage of
the eligible names is 1.00/0.97/0.97 in 1997/2008/2017. The tail is real dispersion
in trailing volatility, not a data artifact.

THE SCORE UNDERNEATH IS A RECORDED LEAD, NOT A NEW SEARCH. It is the ten-year mean
monthly return of `pt_decade_reversal_peer_neutral` (trial #5, GATE_FAIL at the
75th null percentile, validation skill -0.006 -- the only positive validation
selection term v3 has recorded), unchanged: same window, same peer quotas, same
K=100, and its band grid and both windows stay declined on the measurements already
in journal F4 of 2026-10-14. Nothing here is a parameter of that score. What is
being tested is the allocation step on top of it, which is what
`portfolio-learning` is for.

ONE CORRECTION TO THE SCORE'S OWN RECORD, APPLIED HERE (journal F3, tonight). The
score needs 60 monthly observations, so it forms no book until 2000 -- and the
recorded trial was therefore scored **in cash for the first three years of train,
against a fully-invested pool**. That cost it 0.071 of train skill (+0.033 as run;
+0.115 scored from its own first row) and it is 80% of the -0.090 "geography" term
the last session read off its null median. This file holds the equal-weight
eligible pool on dates where fewer than 50 names have a score, which is causal,
costs nothing, and restores train skill to +0.104 before any weighting. It cannot
touch validation: the score is formed on every date in 2018-2023, so the warm-up
branch never fires there.

PRE-REGISTERED PREDICTION, AND IT IS NOT THAT THIS PASSES. The validation null's
dispersion runs 2.3-2.5x train's across the five recorded v3 trials (sd 0.045-0.062
against 0.021-0.024 at the same K), because a Sharpe over six years carries more
sampling error than one over twenty-one; the validation hurdle 1.28*sd is therefore
~0.070 where train's is ~0.027. The baseline's validation selection term was
+0.034. If the floored vector's +20% train improvement in the selection term
carries, this book lands near +0.041 -- a **higher null percentile than the
baseline's 75% and still short of the 90% gate.** The outcome that would refute the
mechanism outright is a percentile at or below 75%; the outcome that would make it
the leg research `#250`'s blend has been starved of is one above 90%.

Pre-registered turnover, as a range with the wider split's churn in it: the
baseline charged 2.0x on train and 2.7x on validation, and the floored vector adds
only drift correction on the same names, so 1.5-4.5x annualised.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
MONTHS = 120
MIN_MONTHS = 60
VOL_WINDOW = 126
VOL_MIN = 80
FLOOR_Q = 0.20
MIN_SCORED = 50

STRATEGY = {
    "name": "pl_decade_invvol_floored",
    "family": "portfolio-learning",
    "hypothesis": (
        "Weighting an already-selected slice -- the 100 eligible names with the lowest "
        "trailing ten-year mean monthly return, quota-allocated across trailing-calendar "
        "peer groups -- inversely to 126-day volatility floored at the slice's own 20th "
        "percentile earns a higher validation null percentile than the equal-weight "
        "version of the same slice (75%), because v3's null copies the weight vector onto "
        "permuted names and so cannot inherit a fit to the names actually held, while a "
        "floored vector stays mild enough (100 effective names, 1.2% largest weight) that "
        "the null's dispersion stays at the equal-weight floor instead of widening with it "
        "as the unfloored vector's does (0.0210 against 0.0375 on train)."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Monthly. The K lowest ten-year mean monthly returns, quota-allocated
    across trailing-calendar peer groups, weighted by 1/sigma with sigma floored
    at the slice's 20th percentile. Before the score exists, the equal-weight
    eligible pool."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    decade = mret.rolling(MONTHS, min_periods=MIN_MONTHS).mean()
    score = (-decade).reindex(prices.index, method="ffill")
    vol = prices.pct_change(fill_method=None).rolling(
        VOL_WINDOW, min_periods=VOL_MIN).std()

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    for date in month_ends:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 20:
            continue
        pool = pd.Series(1.0 / len(names), index=names)
        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < MIN_SCORED:
            rows[date] = pool                      # hold the pool until the score exists
            continue
        groups = calendar_peers(volume, date, names)
        picked = peer_quota_select(sc, groups, min(K, len(sc)))
        if len(picked) < 20:
            rows[date] = pool
            continue
        sig = vol.loc[date].reindex(picked)
        sig = sig.fillna(sig.median())
        if not sig.notna().any() or float(sig.max()) <= 0:
            rows[date] = pd.Series(1.0 / len(picked), index=picked)
            continue
        sig = sig.clip(lower=float(sig.quantile(FLOOR_Q)))
        w = 1.0 / sig
        rows[date] = w / w.sum()

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
