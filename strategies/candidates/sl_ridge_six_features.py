"""Do the six screened feature groups combine to more than their best member?

THE QUESTION `program.md` ASKS OF THIS FAMILY, VERBATIM: "the interesting
question is not 'does ML beat momentum' but which feature groups carry signal
once costs and the skip-month are respected." This session's free screens put
six causal feature groups on the point-in-time panel and measured each one's
cross-sectional IC against the forward 21-day return over 251 train month-ends
(journal F2, F3):

    feature        IC        t      what it is
    rev21       +0.0282   +3.07   negative 21-day return against the eligible pool
    mom12_1     +0.0128   +0.96   252-day return, 21-day skip
    lowidio     +0.0088   +0.78   negative 63-day idiosyncratic volatility
    illiq       -0.0024   -0.29   log Amihud price impact, 126-day window
    volshock    +0.0012   +0.21   negative log volume against its 63-day median
    seas        -0.0142   -2.01   mean return in the same calendar month, 20 years

and their pairwise cross-sectional rank correlations, which are what makes the
combination a real question rather than a restatement of its largest term:

                 mom12_1  lowidio   illiq  volshock   seas   rev21
    rev21           0.02     0.02    0.01     -0.04  -0.03    1.00
    mom12_1         1.00     0.08      --     -0.01   0.00    0.02
    lowidio         0.08     1.00      --     -0.07  -0.05    0.02
    seas            0.00    -0.05      --      0.01   1.00   -0.03

**Every off-diagonal entry is inside ±0.08.** Six nearly orthogonal predictors is
the textbook case where a penalised linear combination beats its best member, and
`program.md`'s own guidance -- "prefer few features and a penalised linear model
first ... a heavy learner mostly fits noise, and the literature's own finding is
that the dominant signals are few" -- names exactly this construction as the first
thing to try. It has never been tried here: `statistical-learning` has no v2 trial,
and the v1 reading (`learnings.md` [2026-08-29], "a penalised linear combiner on a
140-name monthly panel ...") was measured on 140 survivors with a different feature
set and is v1 knowledge like everything else in that file.

WHAT WOULD MAKE THE ANSWER NO, AND IT IS THE LIKELIER OUTCOME. Five of the six
features are individually indistinguishable from zero and one of them (`seas`) is
significantly negative, i.e. the opposite sign to the one v1 traded it in. A ridge
fitted on a cross-sectional rank target will put most of its weight on `rev21`
because that is where the fit is, and the book will then be a noisier
`pt_resid_reversal_band` -- five features' worth of estimation error added to one
feature's worth of signal. That is the specific failure this trial is designed to
detect, and it is why the comparison is against `pt_resid_reversal_band` and not
against the pool.

CONSTRUCTION, HELD FIXED TO THE PAIR'S SETTINGS SO THE COMPARISON IS ONE VARIABLE.
Same 21-day horizon, same monthly grid, same band (ranks 31-120 of the predicted
score), same equal weight as `pt_resid_reversal_band` and `sa_pca_resid_reversion`.
The only change is that the score is a fitted combination rather than one feature.
Features are cross-sectionally z-scored on each date and winsorised at ±3 sd so the
ridge sees comparable scales and is not dragged by one fat tail; the target is the
cross-sectional *rank* of the forward 21-day return (`walkforward.rank_target`),
because this panel's return distribution is heavy enough that a raw-return target
would be fitted to a handful of moves.

CAUSALITY. `walkforward.walk_forward_scores` does the bookkeeping: a training row
for prediction date `d` is a past rebalance date `t` with `t + 21 <= d`, so no
target is read before it was realized, and the model is refitted at every
rebalance rather than cached. Ridge is closed-form, single-threaded and seedless,
so there is no non-determinism for the 1e-6 holdings comparison to read as a peek.
Every feature that needs a cross-sectional aggregate -- the pool residual and the
idiosyncratic-volatility residual -- takes it over the *eligible* names only, never
over whatever columns happen to be present, because the column set itself shrinks
when the causality check hides the tail and a pool mean taken over all columns would
move with it.

FALSIFIER. If this lands at or below `pt_resid_reversal_band` on validation Sharpe,
the five auxiliary feature groups cost more in estimation error than they carry in
signal on this panel, and the lab should stop proposing combinations of nulls.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sl_ridge_six_features",
    "family": "statistical-learning",
    "track": "scout",
    "hypothesis": (
        "A ridge (alpha 10) refitted at every month-end on realized "
        "cross-sectional rank targets, over six causal feature groups whose "
        "pairwise rank correlations are all inside +/-0.08 (21-day pool "
        "residual, 12-1 momentum, negative idiosyncratic vol, log Amihud "
        "illiquidity, negative volume shock, same-calendar-month seasonal), "
        "beats the best single feature's book (pt_resid_reversal_band) on "
        "validation Sharpe at the same band, weighting and grid, because six "
        "nearly orthogonal predictors is the case where a penalised linear "
        "combination beats its largest term; landing at or below it shows the "
        "five auxiliary groups -- five of which are individually "
        "indistinguishable from zero on the train split -- cost more in "
        "estimation error than they carry in signal on this panel."
    ),
}

HORIZON = 21
ALPHA = 10.0
BAND_LO = 30
BAND_HI = 120
MIN_NAMES = 150
WARMUP = 300          # month-end rows skipped before the first possible fit


def _panels(prices: pd.DataFrame, aux: dict, elig: pd.DataFrame) -> dict:
    returns = prices.pct_change(fill_method=None)
    pool = returns.where(elig).mean(axis=1)

    horizon_return = prices / prices.shift(HORIZON) - 1.0
    rev21 = -(horizon_return.sub(horizon_return.where(elig).mean(axis=1), axis=0))
    idio = returns.sub(pool, axis=0).rolling(63, min_periods=40).std()

    raw = {
        "rev21": rev21,
        "mom12_1": F.trailing_return(prices, 252, skip=HORIZON),
        "lowidio": -idio,
        "illiq": F.amihud_illiquidity(prices, aux["dollar_volume"], window=126),
        "volshock": -F.volume_shock(aux["volume"], window=63),
        "seas": F.seasonal_same_month_return(prices, years=20),
    }
    return {k: F.winsorize(F.xs_zscore(v.where(elig)), 3.0) for k, v in raw.items()}


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)

    panels = _panels(prices, aux, elig)
    target = W.rank_target(prices, HORIZON).where(elig)
    dates = W.rebalance_dates(prices, warmup=WARMUP)

    scores = W.walk_forward_scores(
        panels, target, dates, HORIZON, W.ridge_fit_predict(ALPHA), min_train_rows=2000
    )

    rows = {}
    for dt, row in scores.iterrows():
        s = row[elig.loc[dt].to_numpy() & row.notna().to_numpy()]
        if len(s) < MIN_NAMES:
            continue
        picked = s.nlargest(min(BAND_HI, len(s))).index[BAND_LO:]
        if len(picked) == 0:
            continue
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
