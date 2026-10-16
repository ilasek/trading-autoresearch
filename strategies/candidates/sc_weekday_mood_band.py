"""A name's OWN weekday mood exposure as a cross-sectional selection score.

THE CLAIM IN ONE LINE. Birru's mechanism -- weekday mood moves the speculative
leg of the cross-section, low on Monday and high into Friday -- replicates on
this panel 7 times out of 7 pre-signed (F1/F1b tonight), but only through
CHARACTERISTIC proxies for speculativeness, every one of which this lab has
already measured as a null. This candidate measures a name's exposure to the
same factor directly from its own returns, which is a different object: the
rank correlation of the resulting score to seven known or refuted scores is at
most +0.126, the lowest relabelling profile anything screened here has had.

WHAT WAS MEASURED FIRST (train 1997-2017 only, journal F1-F5 of 2026-10-16/17;
no validation Sharpe outside this script, and no holdout, forward or
incubation file was opened).

*F1 -- the mechanism is real here, and it was pre-signed.* Daily active return
of a region-quota K=100 book against the equal-weight eligible pool, by
weekday, gross. Birru's prediction is Monday-high / Friday-low for a book whose
long leg is NON-speculative, and the opposite for one whose long leg IS the
speculative side (illiquidity, distress):

    book (long leg)        predicted    all    Mon   rest   Mon-rest      t
    low ivol126            Mon > rest  -0.70  +3.93  -1.85    +5.78    +3.60
    low MAX21              Mon > rest  -0.52  +3.50  -1.52    +5.02    +3.24
    near 52w high          Mon > rest  -1.00  +4.51  -2.37    +6.87    +4.22
    low beta252            Mon > rest  -1.09  +4.11  -2.38    +6.49    +3.20
    low vol126             Mon > rest  -1.01  +4.32  -2.34    +6.66    +3.53
    high amihud126         rest > Mon  +1.26  +0.08  +1.55    -1.48    -1.23
    decade reversal (#5)   rest > Mon  +1.22  -1.11  +1.80    -2.91    -2.24

bps/day, 1085 Mondays. Seven of seven in the predicted direction, six of them
on the lab's own leads or legs, five at |t| > 3. The raw `all` column is
dominated by the books' betas (0.61-0.75 for the defensive five); beta-adjusted
their alpha is +0.22 to +0.83 bps/day, of which Monday alone supplies +3.6 to
+4.6 -- about 85-100% of a week's alpha on 20% of its days.

*F2 -- and that is why it is not a trade.* The only fully-invested way to
harvest a Monday-localised alpha is to rotate, two decision rows a week:

    book                             sr     pool   skill   turn/yr  cost/yr
    Monday rotation (2 rows/wk)    -1.216  +0.524  -1.740   131.69   30.67%
    low-vol book, monthly          +0.503  +0.524  -0.021     3.10    0.77%

Priced through v3's own execution model rather than asserted. The gross prize
was ~300 bps/yr and the bill is 30.67%/yr.

*F3 -- the monthly version of the same idea is plain market beta.* Research
`#265`'s mood beta, built to its own recipe (mood windows = the 2 best and 2
worst months of each COMPLETED year by realized pool return, so no calendar
semantics and no lookahead; a univariate pool loading estimated on mood months
only, 120-month window, min 40 obs) comes out at mean rank correlation +0.966
to all-month beta and +0.453 to trailing vol. Its own discriminating test --
the sign flip an artifact cannot pass -- fails: the high-mood-beta top 100
earns +3.9 bps/21d region-matched in high-mood months and +16.0 in low-mood
months, same sign, both inside noise. `#265` declined before a file existed.

*F4 -- the score this file trades, and its screen.* wd(i,t) = [mean(r_i |
Monday) - mean(r_i | Tue-Fri)] / sd(r_i) over a trailing 252 days. A
Monday-MINUS-rest difference removes the beta LEVEL by construction, which is
what F3's estimator failed to do. Relabelling rank correlations: -vol126
+0.105, -ivol252 +0.082, -beta252 +0.126, -MAX21 +0.088, prox52 +0.016,
amihud126 +0.002, decade_rev +0.029. Slice beta 0.888, slice vol 0.947x the
pool's. Forward region-matched excess of the top 100: +3.3 bps/21d (t +0.40),
-2.8 bps/63d (t -0.22).

**The screen is weak and that is reported, not hidden.** It is also, by this
lab's own repeated measurement, not the quantity that decides the verdict: the
2026-10-14/15 entry records the standing screen passing three consecutive books
validation refused and ordering two of them backwards on one night.

*F5 -- the book itself, on train, with the gate that has actually decided all
six v3 trials.* Standing operators only, none of them a parameter of this score
(calendar-peer quotas, K=100, retention band B=200, equal weight, monthly, hold
the pool until the score exists). 40 region-matched draws:

    book                     npos    sr    pool   skill  nullmed  nullsd   geo    sel  margin  pct  turn
    wd top-100, band 200    100.0 +0.582 +0.524 +0.058   +0.555  0.0298 +0.031 +0.027 -0.002  88%  2.47
    wd top-100, no band     100.0 +0.501 +0.524 -0.023   +0.476  0.0240 -0.047 +0.025 -0.006  88%  5.20
      [band] 1997-2008      100.0 +0.360 +0.300 +0.060       --      --     --     --     --   --  1.46
      [band] 2009-2017      100.0 +1.036 +0.936 +0.100       --      --     --     --     --   --  3.81

The band reproduces its recorded effect exactly (turnover -52%, skill -0.023 ->
+0.058), and the train skill is positive in BOTH sub-periods -- which the
liquidity lead's was not (-0.04 / +0.11). Geography is +0.031, so this is not a
region bet wearing a selection label.

PRE-REGISTERED PREDICTION, AND IT IS THAT THIS FAILS. F10 of 2026-10-15/16
calibrated the gate: the validation null `sd` runs 2.3-2.5x train's at the same
K (0.045-0.062 against 0.021-0.024) purely because six years carry more
sampling error than twenty-one, so the validation hurdle 1.28*sd is ~0.070
against train's ~0.027, and with the measured 3.4x selection decay a candidate
needs a train selection term near **+0.24**. This book's is **+0.027**, a ninth
of that. The prediction is therefore a validation selection term near +0.008,
a null percentile near **55-60%** and a **GATE_FAIL** -- below the board's best
of 80%, so this does not advance research `#250`'s search for a blend leg
either.

WHY RUN IT ANYWAY, STATED PLAINLY. Three things it buys that no screen can.
(i) `seasonality-calendar` has **no recorded trial under any protocol version's
v3 history**, and `day-of-week` is an axis `program.md` charters that this lab
has never scored; tonight is the session that has the mechanism measured.
(ii) The score is the most decorrelated object screened here, so it adds an
independent column to the deflator's clustering rather than another correlated
one. (iii) It is a direct out-of-sample test of F10's bar, which is a
one-night calibration off six trials. **A null percentile above 90% would
refute that calibration**, which is the outcome worth the trial; a percentile
near 55-60% confirms it and closes the last chartered axis of this family with
a scored book instead of a screen.

Pre-registered turnover as a range with the wider split's churn in it: 2.47x
charged on train, and 2018-2023 name churn has run ~68% above train's on this
panel, so **2.0-5.0x annualised**.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

WINDOW = 252
MIN_MONDAYS = 35
MIN_REST = 140
K = 100
BAND = 200
MIN_SCORED = 50

STRATEGY = {
    "name": "sc_weekday_mood_band",
    "family": "seasonality-calendar",
    "hypothesis": (
        "Selecting the 100 eligible names with the highest trailing-252-day weekday mood "
        "exposure -- (mean Monday return minus mean Tuesday-to-Friday return) divided by the "
        "name's own return standard deviation, which is Birru's speculative-leg contrast "
        "measured on the name itself rather than through a characteristic proxy -- "
        "quota-allocated across trailing-calendar peer groups and held through a top-200 "
        "retention band, lands above the 90th percentile of its region-matched null on "
        "validation, because the score's rank correlation to every known or refuted score on "
        "this panel is at most +0.126 and a null that permutes names within region has the "
        "least to imitate in the most decorrelated book; the pre-registered expectation from "
        "F10's calibration is the opposite, a train selection term of +0.027 against a "
        "required +0.24 putting it near the 55-60th percentile."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Monthly. The K highest weekday mood exposures, quota-allocated across
    trailing-calendar peer groups, held through a top-BAND retention buffer,
    equal weight. Before the score exists, the equal-weight eligible pool."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    rets = prices.pct_change(fill_method=None)
    # A 252-day window holds ~50 Mondays and ~200 other days, so the two means
    # need their own min_periods; one threshold cannot serve both frames.
    is_mon = np.repeat((rets.index.dayofweek == 0)[:, None], rets.shape[1], axis=1)
    mon_mask = pd.DataFrame(is_mon, index=rets.index, columns=rets.columns)
    mon = rets.where(mon_mask).rolling(WINDOW, min_periods=MIN_MONDAYS).mean()
    rest = rets.where(~mon_mask).rolling(WINDOW, min_periods=MIN_REST).mean()
    sd = rets.rolling(WINDOW, min_periods=MIN_REST).std()
    score = (mon - rest) / sd.replace(0, np.nan)

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows: dict = {}
    held = pd.Index([])
    for date in month_ends:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < 20:
            continue
        pool = pd.Series(1.0 / len(names), index=names)
        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < MIN_SCORED:
            rows[date] = pool                      # hold the pool until the score exists
            held = pd.Index([])
            continue
        groups = calendar_peers(volume, date, names)
        picked = peer_quota_select(sc, groups, min(K, len(sc)))
        if len(held):
            # Retention band: keep a held name while it is still inside the top BAND.
            rank = sc.rank(ascending=False)
            keep = pd.Index([n for n in held if n in rank.index and rank[n] <= BAND])[:K]
            need = K - len(keep)
            if need > 0:
                held_set = set(keep)
                picked = keep.append(pd.Index([n for n in picked if n not in held_set][:need]))
            else:
                picked = keep
        if len(picked) < 20:
            rows[date] = pool
            held = pd.Index([])
            continue
        held = pd.Index(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
