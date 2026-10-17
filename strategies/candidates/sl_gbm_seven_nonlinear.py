"""The same seven features, the same target, the same book — only the learner
changes, from a penalised linear combiner to shallow boosted trees.

WHY THIS IS NOT A RE-RUN OF A REFUTED IDEA, STATED AS `CLAUDE.md` REQUIRES.
Journal F10 of 2026-10-13 answered `statistical-learning`'s charter question for
the *linear* case and declined it for free: a walk-forward ridge (`alpha=10`,
quarterly refit, 63-day horizon) over seven features -- 126-day Amihud, 252-day
return, 21-day return, 126-day volatility, 252-day skewness, dollar-volume trend
and Parkinson/close-to-close -- each z-scored within peer group over the eligible
names and trained on the peer-demeaned forward 63-day return, produced

    rank IC(ridge score, peer-demeaned fwd 63d)   +0.0066  (t +0.28, n 62)
    top-100 region-matched excess                 +18.7 bps/63d (t +0.33)
    bot-100 region-matched excess                 -12.3 bps/63d (t -0.25)

What that measured is that a *monotone linear* combination of seven individually
null features is itself null. `program.md` charters the family as "penalised
linear models, trees, gradient boosting, small neural nets", and the lab has
never run anything but the linear half. The two readings of F10 have not been
separated: either the features carry nothing, or the combiner cannot express
what they carry. This file holds every element of F10 byte-for-byte -- the same
seven features, the same within-peer-group normalisation, the same peer-demeaned
forward 63-day target, the same quarterly grid, the same top-100 peer-quota book
-- and changes exactly one thing, the functional form of the learner. It is the
one-variable experiment that separates the two readings, and either answer closes
something: a null here answers the charter question for the family rather than
for one estimator.

WHY A BOOSTED TREE IS THE RIGHT SECOND LEARNER AND NOT A FISHING LICENCE. The
whole case for machine learning in the cross-section rests on interactions and
thresholds -- "momentum, but only among liquid names", "reversal, but only after
a volume shock" -- which a ridge cannot represent at any penalty. Depth-3 trees
represent three-way interactions and nothing deeper; 100 iterations at learning
rate 0.05 with 200-sample leaves and L2 1.0 is at the penalised end of the
family's capacity range, which is what `CLAUDE.md`'s "a heavy learner mostly fits
noise" asks for. No hyper-parameter was searched: every value is a stock default
or the conservative side of one, fixed before the first run, and the feature set
is inherited rather than chosen. The training window is capped at the most recent
60,000 rows, which is a rolling window in auditable form rather than a cached fit.

TONIGHT'S FREE SCREENS THAT BEAR ON THIS FILE (train 1997-2017 only; journal F1-F6
of 2026-10-17/18. No validation, holdout, forward or incubation number was read.)

*F2 -- the risk axis is worth nothing on this panel, which is why no risk-based
construction sits on top of this score.* Full-pool books through the v3 execution
model, train:

    book                               sr      skill    vol    maxDD   turn
    equal-weight pool [baseline]     +0.5238   +0.000   18.1%  -56.0%  0.89
    1/sigma, whole pool              +0.5193   -0.005   17.0%  -52.0%  0.84
    one-factor minimum variance      +0.5089   -0.015   11.4%  -32.2%  1.76
    two-factor minimum variance      +0.5216   -0.002   11.4%  -33.4%  2.00

A 37% cut in volatility buys **-0.015** of Sharpe. The objective is scale-free in
exactly the quantity a covariance fit improves, so this candidate spends its one
degree of freedom on selection and equal-weights what it picks.

*F5 -- the null's own handicap, measured, and why this book re-forms quarterly
rather than annually.* `benchmarks.random_null_v3` runs its replicas through
`simulate` without the eligibility mask the candidate's own book is run through,
so a replacement keeps its slot after it leaves the index. Over train the
replicas of a full-pool book carry **4.8% of their weight on names that are no
longer members**, and that is worth **+0.018 of Sharpe to the null** (masked
replica median +0.5240 against the candidate's +0.5238 -- the identity the
permutation argument demands -- against +0.5419 as the engine runs them). The
handicap grows with how long a name is held, so a low-turnover construction buys
its cost saving partly out of its own gate margin. Quarterly re-formation with no
retention band is the compromise this file takes.

PRE-REGISTERED PREDICTION, AND IT IS NOT THAT THIS PASSES. F6 of 2026-10-16/17
retired train skill as a qualification signal, so nothing here is offered as one.
The falsifiable claim is the comparison: if the boosted score's rank IC against
the peer-demeaned forward 63-day return is inside noise of F10's +0.0066, then
the seven features carry nothing that *any* of this family's learners can reach,
and `statistical-learning` is answered on measurement rather than by analogy. The
outcome that would make the family live is an IC materially above F10's with a
validation null percentile above 90%. Turnover is pre-registered at 1.5-4x
annualised: a 100-name book re-formed four times a year, plus the equal-weight
pool over the warm-up quarters before the model can be fitted.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
HORIZON = 63
WARMUP = 252
MIN_TRAIN_ROWS = 2000
MAX_TRAIN_ROWS = 60_000
MIN_SCORED = 50

STRATEGY = {
    "name": "sl_gbm_seven_nonlinear",
    "family": "statistical-learning",
    "hypothesis": (
        "Replacing the linear combiner in the lab's own seven-feature walk-forward model "
        "with a depth-3 gradient-boosted tree ensemble -- every other element of the "
        "2026-10-13 F10 construction held fixed, same features, same within-peer-group "
        "normalisation, same peer-demeaned forward 63-day target, same quarterly grid, "
        "same top-100 peer-quota equal-weight book -- raises the model's rank information "
        "coefficient materially above F10's +0.0066 and puts the book above the 90% "
        "quantile of the region-matched random-selection null, because the ridge can "
        "express only a monotone linear combination while the whole case for machine "
        "learning in the cross-section rests on interactions and thresholds."
    ),
    "track": "scout",
}


def _boosted():
    """Deterministic shallow gradient boosting, single-threaded."""
    from sklearn.ensemble import HistGradientBoostingRegressor
    from threadpoolctl import threadpool_limits

    def _fit_predict(x_train, y_train, x_pred):
        model = HistGradientBoostingRegressor(
            max_iter=100, max_depth=3, learning_rate=0.05, min_samples_leaf=200,
            l2_regularization=1.0, early_stopping=False, random_state=0,
        )
        if len(x_train) > MAX_TRAIN_ROWS:          # rolling window, in auditable form
            x_train, y_train = x_train[-MAX_TRAIN_ROWS:], y_train[-MAX_TRAIN_ROWS:]
        with threadpool_limits(limits=1):
            model.fit(x_train, y_train)
            return model.predict(x_pred)

    return _fit_predict


def _raw_features(prices, aux):
    """F10's seven, as raw panels on the price calendar."""
    rets = prices.pct_change(fill_method=None)
    dv = aux["dollar_volume"]
    adv63 = dv.rolling(63, min_periods=21).mean()
    adv252 = dv.rolling(252, min_periods=84).mean()
    pv = F.parkinson_vol(aux["high"], aux["low"], 21)
    cc = F.realized_vol(prices, 21)
    return {
        "amihud126": F.amihud_illiquidity(prices, dv, 126),
        "ret252": F.trailing_return(prices, 252),
        "ret21": F.trailing_return(prices, 21),
        "vol126": F.realized_vol(prices, 126),
        "skew252": rets.rolling(252, min_periods=180).skew(),
        "dvtrend": np.log((adv63 / adv252.where(adv252 > 0)).where(lambda x: x > 0)),
        "pvratio": pv / cc.where(cc > 0),
    }


def _demean_in_group(row, groups):
    """Z-score within peer group; groups with too few names are dropped."""
    out = pd.Series(np.nan, index=row.index, dtype=float)
    for g, idx in groups.groupby(groups).groups.items():
        sub = row.reindex(idx).dropna()
        if len(sub) < 10:
            continue
        sd = float(sub.std())
        if not np.isfinite(sd) or sd <= 0:
            continue
        out.loc[sub.index] = ((sub - sub.mean()) / sd).clip(-3.0, 3.0)
    return out


def generate_weights(prices, aux, eligible=None):
    """Quarterly. A boosted tree fitted walk-forward on seven peer-normalised
    features predicts the peer-demeaned forward 63-day return; the book is the
    100 highest predictions, allotted across peer groups in proportion to their
    share of the scored names, equal-weighted. Before the model can be fitted,
    the equal-weight eligible pool."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    raw = _raw_features(prices, aux)
    fwd = W.forward_return(prices, HORIZON)
    month_ends = W.rebalance_dates(prices, warmup=0)
    dates = [d for i, d in enumerate(month_ends) if i % 3 == 2]
    dates = [d for d in dates if prices.index.get_loc(d) >= WARMUP]

    names_at: dict[pd.Timestamp, pd.Index] = {}
    groups_at: dict[pd.Timestamp, pd.Series] = {}
    norm = {k: {} for k in raw}
    target_rows: dict[pd.Timestamp, pd.Series] = {}
    for d in dates:
        names = prices.columns[elig.loc[d].to_numpy() & prices.loc[d].notna().to_numpy()]
        if len(names) < 20:
            continue
        groups = calendar_peers(volume, d, names)
        if groups.empty:
            continue
        names_at[d], groups_at[d] = names, groups
        for k, panel in raw.items():
            norm[k][d] = _demean_in_group(panel.loc[d].reindex(groups.index), groups)
        y = fwd.loc[d].reindex(groups.index)
        target_rows[d] = y - y.groupby(groups).transform("mean")

    if not names_at:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)

    panels = {k: pd.DataFrame(v).T.reindex(index=prices.index, columns=prices.columns)
              for k, v in norm.items()}
    target = pd.DataFrame(target_rows).T.reindex(index=prices.index, columns=prices.columns)
    scores = W.walk_forward_scores(
        panels, target, pd.DatetimeIndex(sorted(names_at)), HORIZON,
        _boosted(), min_train_rows=MIN_TRAIN_ROWS,
    )

    rows = {}
    for d in sorted(names_at):
        names = names_at[d]
        pool = pd.Series(1.0 / len(names), index=names)
        if d not in scores.index:
            rows[d] = pool
            continue
        sc = scores.loc[d].reindex(names).dropna()
        if len(sc) < MIN_SCORED:
            rows[d] = pool
            continue
        picked = peer_quota_select(sc, groups_at[d], min(K, len(sc)))
        if len(picked) < 20:
            rows[d] = pool
            continue
        rows[d] = pd.Series(1.0 / len(picked), index=picked)

    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
