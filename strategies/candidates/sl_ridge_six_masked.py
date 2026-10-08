"""The same question as trial #4, with trial #4's causality leak located and closed.

WHAT TRIAL #4 WAS AND WHY IT RECORDED NOTHING. `sl_ridge_six_features` asked
`program.md`'s own question of this family -- "which feature groups carry signal
once costs and the skip-month are respected" -- by ridge-combining six causal
features whose pairwise cross-sectional rank correlations are all inside +/-0.08.
It never reached a split: `causality_check` failed it at **max diff 3.33e-02 with
the last 63 days removed**. The trial is spent and counted in the deflator; this
file is a second trial in the same family, run because the leak turned out to be
one line and the question is still unanswered.

WHERE THE LEAK WAS, MEASURED RATHER THAN GUESSED. All six feature panels were
recomputed on the full visible frame and on the 63-day-truncated frame and compared
on the shared rows and columns (journal F9):

    panel        max |diff|        panel        max |diff|
    rev21         1.8e-15          illiq         1.0e-14
    mom12_1       1.8e-15          volshock      1.8e-15
    lowidio       1.6e-13          seas          1.3e-15
    rank_target   3.8e-03   <-- the leak

**Every feature was clean to floating point and the TARGET was not.** The mechanism
is specific and transferable: `walkforward.rank_target` is
`xs_rank(forward_return(prices, h)) - 0.5`, and trial #4 masked it to the eligible
names *after* ranking (`W.rank_target(prices, HORIZON).where(elig)`). `xs_rank`
scales each row's ranks by **the number of non-NaN names in that row**, so with 1246
columns in the full frame and 1239 in the truncated one -- the seven names that only
become eligible inside the hidden tail -- every rank in every row shifts. The target
therefore carried the one thing `protocol.visible_frame` exists to remove: the column
set itself tells the strategy which names join an index later. The fit then moved, and
with it the holdings.

**The fix is to mask before ranking, not after**: rank the forward return over the
eligible names only, so the row's rank denominator is the pool the book could actually
have bought. `strategies/lib/walkforward.py` is not edited -- an existing lib file
never is -- so the target is built inline here, which is also why it is written out
rather than called.

This is worth stating as a general rule because it applies to **any** cross-sectional
normalisation, not just the target: a row-wise rank or z-score is causal in the time
axis and not automatically causal in the *column* axis, and under protocol v2 the
column axis is where the look-ahead lives. `features.xs_zscore` and `features.xs_rank`
are both exposed to it. Trial #4's six feature panels avoided it only because this
file's `_panels` already applied `.where(elig)` *before* normalising.

THE QUESTION, UNCHANGED FROM TRIAL #4. The six features and their train-split ICs
against the forward 21-day return over 251 month-ends (journal F2, F3):

    feature        IC        t      what it is
    rev21       +0.0282   +3.07   negative 21-day return against the eligible pool
    mom12_1     +0.0128   +0.96   252-day return, 21-day skip
    lowidio     +0.0088   +0.78   negative 63-day idiosyncratic volatility
    illiq       -0.0024   -0.29   log Amihud price impact, 126-day window
    volshock    +0.0012   +0.21   negative log volume against its 63-day median
    seas        -0.0142   -2.01   mean return in the same calendar month, 20 years

Five of the six are individually indistinguishable from zero and one is significantly
negative, but every pairwise rank correlation is inside +/-0.08, which is the textbook
case for a penalised linear combination beating its largest term. `program.md` names
this construction as the first thing to try in this family, and the family has no
recorded v2 result.

CONSTRUCTION, held to the session's anchor so the comparison is one variable: 21-day
horizon, monthly grid, **top 30** of the predicted score, equal weight -- identical to
`pt_resid_reversal_v2` (validation 0.54, 98th null percentile) and
`sa_pca_resid_reversion` (validation 0.597, 99th null percentile, the session's lead).
Ridge alpha 10, refitted at every rebalance on realized rank targets only, closed-form
and single-threaded. The band variant is not used: trial #2 showed ranks 31-120 removes
the population the premium lives in (0.54 -> 0.379, 98th percentile -> 81st).

PRE-REGISTERED TRAIN-AS-PREDICTION ENTRY (`learnings.md` [2026-08-30]): train Sharpe
predicted at **+0.40 to +0.60**, the range the two scored top-30 books occupy (+0.438,
+0.544). The anti-prediction rule stands at four-for-five after tonight -- trial #2
confirmed it, trial #3 is its first designed-pair counter-example -- so a train Sharpe
above +0.544 should be read as evidence *against* this candidate's validation case.

FALSIFIER. Beating `sa_pca_resid_reversion`'s +0.597 means the five auxiliary groups
carry signal the lead does not. Landing between +0.54 and +0.597 means they add
nothing the single best feature did not already have. Landing below the
random-selection null's 90% quantile -- which trial #2 did at this horizon on a worse
selection -- means the combination is worse than its own largest term by enough to
erase the mechanism, and the lab should stop proposing combinations of nulls on this
panel whatever their orthogonality.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sl_ridge_six_masked",
    "family": "statistical-learning",
    "track": "scout",
    "hypothesis": (
        "A ridge (alpha 10) refitted at every month-end on realized "
        "cross-sectional rank targets ranked over the ELIGIBLE names only, "
        "over six causal feature groups whose pairwise rank correlations are "
        "all inside +/-0.08 (21-day pool residual, 12-1 momentum, negative "
        "idiosyncratic vol, log Amihud illiquidity, negative volume shock, "
        "same-calendar-month seasonal), beats the session's best single-score "
        "book (sa_pca_resid_reversion, validation 0.597 at the 99th percentile "
        "of its null) on validation Sharpe at the same top-30 selection, "
        "weighting and grid, because six nearly orthogonal predictors is the "
        "case where a penalised linear combination beats its largest term; "
        "landing between +0.54 and +0.597 shows the five auxiliary groups add "
        "nothing the best single feature already had, and landing below the "
        "random-selection null's 90% quantile shows the combination is worse "
        "than its own largest term. Train Sharpe is predicted at +0.40 to "
        "+0.60."
    ),
}

HORIZON = 21
ALPHA = 10.0
TOP_N = 30
MIN_NAMES = 50
WARMUP = 300


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
    # Mask BEFORE normalising: a row-wise rank or z-score whose denominator is the
    # frame's column count is not causal in the column axis (see this file's header).
    return {k: F.winsorize(F.xs_zscore(v.where(elig)), 3.0) for k, v in raw.items()}


def _masked_rank_target(prices: pd.DataFrame, elig: pd.DataFrame) -> pd.DataFrame:
    """`walkforward.rank_target`, ranked over the eligible names only."""
    forward = W.forward_return(prices, HORIZON).where(elig)
    return F.xs_rank(forward) - 0.5


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)

    panels = _panels(prices, aux, elig)
    target = _masked_rank_target(prices, elig)
    dates = W.rebalance_dates(prices, warmup=WARMUP)

    scores = W.walk_forward_scores(
        panels, target, dates, HORIZON, W.ridge_fit_predict(ALPHA), min_train_rows=2000
    )

    rows = {}
    for dt, row in scores.iterrows():
        s = row[elig.loc[dt].to_numpy() & row.notna().to_numpy()]
        if len(s) < MIN_NAMES:
            continue
        picked = s.nlargest(min(TOP_N, len(s))).index
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
