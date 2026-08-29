"""Does a learned combination of price, range and volume features beat the
naive single-signal constructions this lab has only ever tested one at a time?

WHY THIS FAMILY, AND WHY FIRST. `statistical-learning` has never been scouted
here — until 2026-08-29 it could not be: strategies received closing prices
only and there was no estimator library. Both changed, so the first question
worth asking is the cheap one: given a handful of causal features drawn from
the whole daily bar, does a penalised linear model fitted walk-forward find a
cross-sectional ranking worth holding?

WHAT IT DOES. Eleven features per name per month-end — four trailing returns
(12-1, 6-1, 3-1 and the un-skipped trailing month, which is reversal not
continuation), two close-to-close volatilities, a Parkinson range volatility,
log Amihud illiquidity, a volume shock against a quarterly median, a
dollar-volume rank, and a market-residual five-day return. Each is
cross-sectionally ranked and centred, so the model sees relative position and
never a raw magnitude whose distribution drifts across sixty years. The target
is the cross-sectional rank of the next month's return. A ridge is refitted at
every month-end on every past month whose forward return had already been
realized at that date, and the fitted model scores the current cross-section.
The top 20 names are held, weighted by predicted score above a fixed floor.

WHY RIDGE AND NOT SOMETHING WITH MORE CAPACITY. The comparative-methods
literature's own finding is that a small set of predictors — variations on
momentum, liquidity and volatility — dominates, and that an unpenalised model
over a wide feature set overfits catastrophically. This universe is 140
instruments; a boosted forest here would mostly fit noise, and if the linear
combination has nothing, capacity is not what was missing. Ridge is also
closed-form and deterministic, which matters because the protocol's causality
check compares holdings at 1e-6.

WHAT WOULD FALSIFY IT. A validation Sharpe at or below the equal-weight global
sleeve's 0.49 — the standing floor for "a construction with no signal in it" in
`experiments/learnings.md` — would say a learned linear combination of these
features adds nothing over the naive constructions already tested. That is a
real answer about the family and the reason this is a scout: it is not trying
to take the champion's seat, it is trying to find out whether there is anything
here at all.

CAVEATS RECORDED IN ADVANCE. (a) Survivorship bias is worst exactly where a
learned model will look — the universe is today's constituents, so any
feature that proxies "survived" gets paid. Read a strong stock-level result
with the scepticism `learnings.md` demands. (b) The features are correlated
with the champion's own signal by construction (three of eleven are its
lookbacks), so a high rho to the incumbent would make this a poor ensemble leg
even if it scores well — the leaderboard reports that number. (c) Monthly
refitting on an expanding window means the early sample is fitted on little
data; the first years of the train split are close to noise.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sl_ridge_xs_walkforward",
    "family": "statistical-learning",
    "track": "scout",
    "hypothesis": (
        "A ridge regression refitted at every month-end on realized outcomes only, "
        "mapping eleven cross-sectionally ranked price, range and volume features to "
        "the rank of next month's return, produces a long-only top-20 book whose "
        "validation Sharpe beats the 0.49 equal-weight floor — i.e. a learned linear "
        "combination of the whole daily bar carries cross-sectional information that "
        "the lab's single-signal constructions have not already extracted."
    ),
}

HORIZON = 21          # one month forward, matching the rebalance cadence
TOP_N = 20
FLOOR = 0.25
ALPHA = 10.0
MIN_TRAIN_ROWS = 2000
WARMUP = 24           # month-ends skipped before the first possible fit


def _feature_panels(prices: pd.DataFrame, aux: dict) -> dict[str, pd.DataFrame]:
    """Eleven causal features, each cross-sectionally ranked and centred.

    Ranking rather than z-scoring is deliberate: this universe's return
    distribution is heavily skewed, and a raw z-score hands the fit to whichever
    handful of names moved most that month."""
    high, low, volume, dv = aux["high"], aux["low"], aux["volume"], aux["dollar_volume"]
    raw = {
        "ret_12_1": F.trailing_return(prices, 252, 21),
        "ret_6_1": F.trailing_return(prices, 126, 21),
        "ret_3_1": F.trailing_return(prices, 63, 21),
        "ret_1_0": F.trailing_return(prices, 21, 0),
        "vol_21": F.realized_vol(prices, 21),
        "vol_252": F.realized_vol(prices, 252),
        "park_21": F.parkinson_vol(high, low, 21),
        "illiq_21": F.amihud_illiquidity(prices, dv, 21),
        "vshock_63": F.volume_shock(volume, 63),
        "dv_rank_63": F.dollar_volume_rank(dv, 63),
        "resid_5": F.market_residual_return(prices, 252, 5),
    }
    return {name: F.xs_rank(frame) - 0.5 for name, frame in raw.items()}


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    dates = W.rebalance_dates(prices, warmup=WARMUP)
    scores = W.walk_forward_scores(
        feature_panels=_feature_panels(prices, aux),
        target=W.rank_target(prices, HORIZON),
        dates=dates,
        horizon=HORIZON,
        fit_predict=W.ridge_fit_predict(ALPHA),
        min_train_rows=MIN_TRAIN_ROWS,
    )
    rows = {}
    for dt, row in scores.iterrows():
        w = F.top_n_weights(row, TOP_N, floor=FLOOR)
        if not w.empty:
            rows[dt] = w
    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
