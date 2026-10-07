"""Does removing FIVE principal components beat removing one market factor?

THE PAIR THIS FILE COMPLETES, AND WHY ITS ANCHOR MOVED BEFORE IT RAN. This file
reverts the 21-day return measured against the **five leading principal components**
of the trailing 252-day standardised return matrix, re-estimated from scratch at
every rebalance date on the names eligible that day. Its partner,
`pt_resid_reversal_v2`, reverts the same 21-day return against a single
equally-weighted pool factor, and is otherwise identical: same horizon, same **top
30** of the sort, same equal weight, same monthly grid. The two scores correlate
**+0.847** cross-sectionally on the train split and were declared a designed pair on
one mechanism, not two independent bets.

**The anchor was going to be ranks 31-120 and the lab just found out it must not be.**
Trial #2 (`pt_resid_reversal_band`) took that band on the market-residual score
because seven train slices said the extreme tail was risk without signal. On
validation:

    trial                      train sharpe  train mdd   val sharpe  val mdd  null pctile  IR vs pool
    #1 top 30                     +0.44       -78.6%       +0.54     -54.1%      98%         +0.41
    #2 ranks 31-120               +0.55       -62.1%       +0.38     -43.1%      81%         -0.04

The band did exactly what the train screens promised on the axis they measured --
drawdown -54.1% -> -43.1%, clearing the gate -- and **inverted the selection content
it was supposed to protect**: 0.54 -> 0.379, from the 98th percentile of the null to
the 81st, from +0.41 of information ratio over the pool to -0.04. So
`learnings.md` [2026-08-30]'s "the book buys the extreme tail, not the quintile mean"
is right and the train screen that contradicted it was wrong, and the configuration
this question has to be asked at is the top 30.

WHY THE QUESTION IS WORTH A TRIAL RATHER THAN A NOTE. The free screens measure the
extra factor removal twice and it wins on both (train split only; journal F3, F6, F7):

    reading                                      market residual   5-PC residual
    cross-sectional IC vs forward 21d return    +0.0282 (t 3.07)  +0.0278 (t 5.17)
    band 31-90, excess over pool, bps/month       +28.1 (t 2.82)    +32.2 (t 4.30)

The IC magnitudes are the same to three decimals and the **t nearly doubles**, which
is the signature of a score whose cross-sectional dispersion is being cleaned rather
than enlarged. That reading is now explicitly on probation: those are train numbers,
and trial #2 is the fourth consecutive reading in which a train advantage outside the
incumbent's family anti-predicted the validation ordering (`learnings.md` [2026-08-30],
three for three before tonight, two of them designed pairs; this pair makes four, and
it is a designed pair too). **So the train screens are the REASON this is tested and
are being treated as evidence against the hypothesis, not for it.**

THE MECHANISM-LEVEL REASON TO EXPECT SOMETHING ANYWAY, which is independent of the
train screens and is what actually justifies the trial. The market-residual sort's
top 30 are the names that fell most against a single equal-weight average, so that
tail is loaded with names whose *region or sector* fell -- a factor move wearing a
stock-specific label, which is the thing `learnings.md` records three v1 scores
turning out to be. Removing five components takes those out of the tail by
construction and leaves names whose *own* move was extreme. If the reversion premium
is price pressure on individual names, that substitution should raise the selection
content; if it is a factor-level overreaction, it should destroy it. Either answer is
worth the trial, and the two are distinguishable in one number.

PRE-REGISTERED TRAIN-AS-PREDICTION ENTRY, which `learnings.md` [2026-08-30] asks every
scout to record: train Sharpe is predicted at **+0.45 to +0.60** (trial #1 scored
+0.438 at top 30 and the 5-PC score's train excess is higher), and the anti-prediction
rule therefore predicts validation **below** trial #1's +0.54. The hypothesis below
predicts the opposite. The pair is the fifth reading either way.

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
are the ones the residual must not contain; 252 days because every screen this
session ran was run at that window and changing it here would confound the one
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

FALSIFIER, AND THE DRAWDOWN RISK ACCEPTED IN ADVANCE. If this lands at or below
`pt_resid_reversal_v2`'s +0.54 and 98th null percentile, the near-doubling of the
IC's t-statistic was a train-split artifact, factor removal is not an improvement to
a reversal score on this panel, and the +0.847 correlation was the whole story -- the
pair is then one trial's worth of information, not two. Trial #1 was killed by the
drawdown gate at -54.1% and this file deliberately returns to its book size, so a
drawdown failure is a live and accepted risk: the number that answers the question is
the validation Sharpe and the null percentile, both of which are recorded even on a
GATE_FAIL. A candidate that clears -45% *as well* would say the 5-PC residual
de-concentrates the crash exposure of the tail, which no screen tonight measured.
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
        "beats the same top-30 book taken against the single equal-weight "
        "pool factor (trial #1: validation 0.54 at the 98th percentile of its "
        "null, IR vs pool +0.41) on validation Sharpe, because the top 30 of a "
        "single-factor residual sort is loaded with names whose region or "
        "sector fell rather than names whose own move was extreme, and "
        "removing five components substitutes the second population for the "
        "first; landing at or below +0.54 says the reversion premium on this "
        "panel is factor-level overreaction rather than price pressure on "
        "individual names, that the five-component residual's near-doubled "
        "train IC t-statistic (+5.17 vs +3.07) was a train-split artifact, and "
        "that the two scores' +0.847 cross-sectional correlation was the whole "
        "story. Train Sharpe is predicted at +0.45 to +0.60."
    ),
}

HORIZON = 21
WINDOW = 252
N_PC = 5
BAND_LO = 0
BAND_HI = 30
MIN_NAMES = 50
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
