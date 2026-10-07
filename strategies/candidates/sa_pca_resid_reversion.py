"""Does removing FIVE principal components beat removing one market factor?

THE PAIR THIS FILE COMPLETES. `pt_resid_reversal_band` reverts the 21-day return
measured against the equal-weight eligible pool -- a single, equally-weighted
factor. This file reverts the 21-day return measured against the **five leading
principal components** of the trailing 252-day standardised return matrix,
re-estimated from scratch at every rebalance date on the names eligible that day,
and is otherwise byte-identical in construction: same horizon, same band (ranks
31-120 of the sort), same equal weight, same monthly grid. The pair was declared a
designed pair on one mechanism in the session's pre-registration, not two
independent bets, and the two scores correlate **+0.847** cross-sectionally on the
train split. The one variable between them is how much of the comovement is removed
before the residual is reverted.

WHY THE QUESTION IS WORTH A TRIAL RATHER THAN A NOTE. The free screens measure the
extra factor removal twice, and it wins on both readings while the risk shape stays
put (train split only; journal F3, F6, F7):

    reading                                      market residual   5-PC residual
    cross-sectional IC vs forward 21d return    +0.0282 (t 3.07)  +0.0278 (t 5.17)
    band 31-90, excess over pool, bps/month       +28.1 (t 2.82)    +32.2 (t 4.30)
    band 31-120, excess over pool, bps/month      +27.0 (t 3.28)    +23.9 (t 4.20)
    band 31-120, train mdd                           -65.1%           -66.3%

The IC magnitudes are the same to three decimals and the **t nearly doubles**, which
is the signature of a score whose cross-sectional dispersion is being cleaned rather
than enlarged: removing the market, region and sector-like comovement that the five
leading components carry leaves a residual whose reversion is less contaminated by
whichever factor happened to move in a given month. That is a claim about stability,
and stability is what `experiments/learnings.md` records this lab repeatedly losing
when it mistook one for the other -- three separate scores in the v1 history turned
out to be "reversal in costume", i.e. a factor move wearing a stock-specific label.
Here the direction is reversed: the question is whether a score that is *already*
reversal gets better when the factor moves are taken out properly.

HOW THE ABSENCE OF THE SHORT LEG IS HANDLED, which `program.md` requires a
`statistical-arbitrage` candidate to state. A residual-reversion signal is naturally
two-sided: names whose residual fell are cheap, names whose residual rose are rich.
Long-only, **only the cheap side is tradeable and the rich side is simply not held**
-- it is not shorted, and it is not used to fund the long leg either. The book is
therefore a long-only slice of one tail of the residual distribution and carries the
pool's full market exposure; the statistical-arbitrage content is in the selection
only, which is exactly the quantity the random-selection null gate measures. Two
consequences are accepted in advance: the book inherits the pool's drawdown (F7
measures the equal-weight eligible pool at -64.8% on train and no band width gets
materially below it), and roughly half of the signal's theoretical information is
discarded unused.

WHY FIVE COMPONENTS AND A 252-DAY WINDOW. Five because the panel spans 15 regions
and two instrument types and the leading components of a global daily return matrix
are the ones the residual must not contain; 252 days because the band screens and the
IC screens were both run at that window and changing it here would confound the one
variable the pair is testing. No component count other than five was scored, so this
is not a sweep -- it is the pair's partner at the pair's settings.

DETERMINISM AND COST. The factor basis comes from `numpy.linalg.eigh` on the
252 x 252 Gram matrix of the standardised block, then the right singular vectors by
back-projection; the residual uses the orthogonal projector `V V'`, which is
invariant to eigenvector sign, so there is no non-determinism for the causality
check to read as a peek. Estimation uses only the names eligible on the rebalance
date, so hiding later rows -- and with them the columns that become eligible later --
cannot change the basis. Build cost is 2.7 s over 251 train month-ends, about 4 s per
`generate_weights` call on the full window, well inside the ~60 s budget.

FALSIFIER. If this lands at or below `pt_resid_reversal_band` on validation Sharpe,
the near-doubling of the IC's t-statistic and the +4.1 bps/month of extra train
excess were a train-split artifact, and the lab should stop treating factor removal
as an improvement to a reversal score on this panel. If it also fails the drawdown
gate, the +0.847 correlation was the whole story and the pair is one trial's worth of
information, not two.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "sa_pca_resid_reversion",
    "family": "statistical-arbitrage",
    "track": "scout",
    "hypothesis": (
        "Reverting the 21-day return measured against the five leading "
        "principal components of the trailing 252-day standardised return "
        "matrix, re-estimated at every month-end on that day's eligible names, "
        "beats the same band of the same sort taken against the single "
        "equal-weight pool factor on validation Sharpe, because on the train "
        "split the five-component residual leaves the IC's magnitude unchanged "
        "(+0.0278 vs +0.0282) while nearly doubling its t-statistic (+5.17 vs "
        "+3.07) and raises the band's excess over the pool from +28.1 to +32.2 "
        "bps/month at t = +4.30 vs +2.82 with the risk shape unchanged; "
        "landing at or below the market-residual version says the extra factor "
        "removal is a train-split artifact and that the two scores' +0.847 "
        "cross-sectional correlation was the whole story."
    ),
}

HORIZON = 21
WINDOW = 252
N_PC = 5
BAND_LO = 30
BAND_HI = 120
MIN_NAMES = 150
MIN_COVERAGE = 0.8


def _factor_residual_score(block: np.ndarray, recent: np.ndarray) -> np.ndarray:
    """Cumulative `recent` return with its projection on the `N_PC` leading
    components of `block` removed, negated so that a fallen residual scores high."""
    mu, sigma = block.mean(axis=0), block.std(axis=0) + 1e-12
    standardized = (block - mu) / sigma
    _, vectors = np.linalg.eigh(standardized @ standardized.T)
    loadings = standardized.T @ vectors[:, -N_PC:]
    loadings /= np.linalg.norm(loadings, axis=0, keepdims=True) + 1e-12
    recent_z = (recent - mu) / sigma
    residual = recent_z - (recent_z @ loadings) @ loadings.T
    return -residual.sum(axis=0)


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)
    returns = prices.pct_change(fill_method=None)

    rows = {}
    for dt in rebalance_dates:
        if dt not in returns.index:
            continue
        end = returns.index.get_loc(dt)
        if end < WINDOW:
            continue
        block = returns.iloc[end - WINDOW + 1 : end + 1]
        covered = block.notna().sum(axis=0).to_numpy() > WINDOW * MIN_COVERAGE
        ok = elig.loc[dt].to_numpy() & covered
        if ok.sum() < MIN_NAMES:
            continue
        ids = prices.columns[ok]
        score = pd.Series(
            _factor_residual_score(
                np.nan_to_num(block[ids].to_numpy()),
                np.nan_to_num(returns.iloc[end - HORIZON + 1 : end + 1][ids].to_numpy()),
            ),
            index=ids,
        )
        ranked = score.nlargest(min(BAND_HI, len(score))).index
        picked = ranked[BAND_LO:]
        if len(picked) == 0:
            continue
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
