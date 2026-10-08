"""Where the residual-reversion premium lives: a price-impact tilt on the lead.

THE LEAD THIS CONDITIONS. `sa_pca_resid_reversion` (trial #3) is the session's and
the v2 board's best recorded result: validation Sharpe **0.597 at the 99th percentile
of its own random-selection null** (median +0.28, 90% +0.41), information ratio over
the equal-weight eligible pool +0.35, validation drawdown -40.1%, train +0.544. It
reverts the 21-day return measured against the five leading principal components of
the trailing 252-day standardised return matrix, holds the top 30, equal weight,
monthly.

THE QUESTION, AND WHY IT IS A `liquidity-volume` QUESTION RATHER THAN A SECOND
STAT-ARB TRIAL. If the premium is **price pressure** -- a forced or impatient seller
pushing a name below value and the price recovering when the pressure lifts -- then it
must be larger where a given flow moves the price more, i.e. where Amihud price impact
per dollar traded is high. If it is factor-level or informational overreaction, price
impact is irrelevant to it. The two readings are distinguishable, and the distinction
is the literature's own: Brown-Keim-Kleidon's first a-priori objection to tax-loss
selling (`research/notes/2026-10-07-tax-year-end-alignment-and-the-australian-test.md`)
is that **realization is not a demand shift unless the name is genuinely hard to
substitute** -- if close substitutes exist the demand curve is horizontal and
even heavy one-sided selling moves no price at all. Price impact is the measurable
version of "hard to substitute", and the paper's own test of its hypothesis is to look
for the effect where the mechanism requires it to be rather than where it is
convenient.

WHAT THE SCREENS ALREADY SETTLED, INCLUDING ONE FREE KILL THAT MATTERS HERE. The
standalone illiquidity premium on this panel is **a flat null**: Amihud at a 126-day
window scores IC -0.0024 (t = -0.29) against the forward 21-day return over 251 train
month-ends, and +0.0024 the other way (journal F3). So no trial is spent on an
illiquidity sort, and -- more important for this file -- the tilt below cannot be
smuggling in a level effect, because there is no level effect to smuggle. Its
decorrelation from both reversal scores is clean (+0.002 and +0.014).

WHAT THIS FILE'S CONDITIONER MEASURES ON TRAIN (journal F8; 251 month-ends, top-30
slice, excess over the equal-weight eligible pool on the same grid):

    score                                    IC        t   | top30 excess   t    rho to lead
    pca_rev (the lead)                    +0.0278   +5.17  |    +7.2     +0.61     1.000
    z(pca_rev) + 0.5 z(illiq)   <- this   +0.0248   +4.12  |   +24.2     +1.84     +0.912
    pca_rev * illiq rank                  +0.0267   +5.19  |   +28.0     +1.93     +0.929
    pca_rev / parkinson vol               +0.0295   +5.62  |   +15.2     +1.28     +0.980
    pca_rev / residual std                +0.0276   +5.16  |    +9.0     +0.77     +0.993

**The tilt LOWERS the cross-sectional IC and roughly QUADRUPLES the tail excess**,
which is the signature of a conditioner that relocates the premium into the slice a
top-30 book actually buys rather than one that adds cross-sectional information. That
is the axis trial #2 proved matters here: ranks 31-120 of the market-residual sort
earned +27.0 bps/month on train at t = +3.28 and delivered -0.04 of information ratio
on validation, while the top 30's +14.0 at t = +0.61 delivered +0.41. The tail is
where this mechanism's premium lives, so a conditioner should be judged on the tail
and this one is.

TWO THINGS RECORDED AGAINST THIS CANDIDATE BEFORE IT RUNS.

*(a) The same table kills the `range-variance` candidate this session would otherwise
have run, and the kill is free.* Dividing the residual by Parkinson range volatility
or by its own residual standard deviation are the two obvious range-variance
conditioners on the lead. They score **rho +0.980 and +0.993 to the lead** -- they are
the lead wearing a different label, a fourth instance of this repo's recurring "the
score turned out to be reversal in costume" finding, caught before a trial rather than
after one. Standardising a residual by its own scale barely reorders a cross-section
in which the residual is already standardised.

*(b) This candidate is at rho +0.912 to the lead too, which is lower but not low.*
It is a refinement of trial #3, not an independent mechanism, and the `liquidity-volume`
family lead it may set should be read that way: the deflator will likely cluster the
two return series, which makes the trial cheap and also means it buys the lab no
breadth. Stated here so the leaderboard's `rho` is not read as a surprise later.

WHY THE ADDITIVE z-SCORE FORM AND NOT THE PRODUCT. The product scored marginally
higher on the tail (+28.0 vs +24.2) and the additive form is taken anyway, for two
reasons. It is this repo's standing score idiom -- the v1 champion's own score was
`zscore(momentum) + zscore(type-demeaned -E/Var)` -- and it is monotone and
interpretable, where a product of a signed score by a rank in [0,1] reorders the
negative half perversely and would have to be explained every time it was read. And
the anti-prediction rule (`learnings.md` [2026-08-30], four-for-five after tonight)
says the highest train cell is the wrong thing to pick. The 0.5 coefficient is the
only one screened; no sweep was run and none should be.

PRE-REGISTERED TRAIN-AS-PREDICTION ENTRY: train Sharpe predicted at **+0.45 to +0.65**,
a shade above the lead's +0.544 since the tilt raises the train tail excess. By the
anti-prediction rule that is itself a bearish signal for validation, and it is recorded
as such rather than quietly left out.

FALSIFIER. Beating +0.597 says the residual-reversion premium is price pressure and
larger where a dollar moves the price more. Landing between the null's 90% quantile and
+0.597 says the tilt moved the book without moving the premium -- four times the train
tail excess for nothing -- and that the F8 tail column is as misleading as trial #2's
F5 excess column was. Landing below the null's 90% quantile says a conditioner at rho
+0.912 can still destroy the lead, which would make the lead's own construction more
fragile than its 99th percentile suggests.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F

STRATEGY = {
    "name": "lv_resid_rev_illiq_tilt",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Adding half a cross-sectional z-score of log Amihud price impact "
        "(126-day window) to the z-scored five-component residual reversion "
        "score, and holding the top 30 equal-weight monthly exactly as "
        "sa_pca_resid_reversion does, beats that lead's validation Sharpe of "
        "0.597 (99th percentile of its null), because the residual-reversion "
        "premium is price pressure and must therefore be larger where a given "
        "flow moves the price more -- on the train split the tilt roughly "
        "quadruples the top-30 excess over the eligible pool (+7.2 to +24.2 "
        "bps/month, t +0.61 to +1.84) while LOWERING the cross-sectional IC "
        "(+0.0278 to +0.0248), the signature of a conditioner that relocates "
        "the premium into the slice the book buys, and the standalone "
        "illiquidity premium is a flat null here (-0.0024, t -0.29) so no "
        "level effect is being smuggled in; landing at or below 0.597 says the "
        "tilt moved the book without moving the premium."
    ),
}

HORIZON = 21
WINDOW = 252
N_PC = 5
ILLIQ_WINDOW = 126
TILT = 0.5
TOP_N = 30
MIN_NAMES = 50
MIN_COVERAGE = 0.8


def _factor_residual_score(block: np.ndarray, recent: np.ndarray) -> np.ndarray:
    """Cumulative `recent` return with its projection on the `N_PC` leading
    components of `block` removed, negated so a fallen residual scores high.
    Identical to `sa_pca_resid_reversion`'s, deliberately."""
    mu, sigma = block.mean(axis=0), block.std(axis=0) + 1e-12
    standardized = (block - mu) / sigma
    _, vectors = np.linalg.eigh(standardized @ standardized.T)
    loadings = standardized.T @ vectors[:, -N_PC:]
    loadings /= np.linalg.norm(loadings, axis=0, keepdims=True) + 1e-12
    recent_z = (recent - mu) / sigma
    residual = recent_z - (recent_z @ loadings) @ loadings.T
    return -residual.sum(axis=0)


def _z(values: pd.Series) -> pd.Series:
    sd = values.std(ddof=0)
    return (values - values.mean()) / sd if sd > 0 else pd.Series(0.0, index=values.index)


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)

    returns = prices.pct_change(fill_method=None)
    # Amihud is a per-column rolling quantity, so it is causal in the time axis;
    # it is z-scored per date below over the eligible names only, never over the
    # frame's column set, which is where protocol v2's look-ahead lives.
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], window=ILLIQ_WINDOW)

    rows = {}
    for dt in rebalance_dates:
        if dt not in returns.index:
            continue
        end = returns.index.get_loc(dt)
        if end < WINDOW:
            continue
        block = returns.iloc[end - WINDOW + 1 : end + 1]
        covered = block.notna().sum(axis=0).to_numpy() > WINDOW * MIN_COVERAGE
        ok = elig.loc[dt].to_numpy() & covered & illiq.loc[dt].notna().to_numpy()
        if ok.sum() < MIN_NAMES:
            continue
        ids = prices.columns[ok]
        residual = pd.Series(
            _factor_residual_score(
                np.nan_to_num(block[ids].to_numpy()),
                np.nan_to_num(returns.iloc[end - HORIZON + 1 : end + 1][ids].to_numpy()),
            ),
            index=ids,
        )
        score = _z(residual) + TILT * _z(illiq.loc[dt, ids])
        picked = score.nlargest(min(TOP_N, len(score))).index
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
