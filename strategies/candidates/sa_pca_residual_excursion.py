"""Does a *conditional* PCA-residual excursion pay where an unconditional
residual sort did not?

WHY THIS FAMILY, AND WHY AGAIN. `statistical-arbitrage` has no recorded trial.
It was declined on 2026-08-29 on a free train screen: raw 5-day reversal IC
+0.0455, one-factor residual +0.0375, PCA k=3 +0.0331, PCA k=5 +0.0336 — i.e.
residualising made the signal monotonically worse, so the family's premise
looked dead. `research/SUMMARY.md` #55 says that screen tested the wrong region.
Its source's structural finding is that the factor count has an **interior
optimum**: one factor is the *worst* configuration (leftover common variation
means slow measured reversion and inflated residual volatility), and a very
high variance target loses too (the residual is real but smaller than costs).
k in {1, 3, 5} sits entirely inside the region the source also found worst.

THE PREMISE, MEASURED BEFORE THIS FILE WAS WRITTEN (train split only, no returns
scored). Bracketing the source's stated ~55% variance target against 40% and 75%,
21-day forward returns, monthly formation dates, 300 months:

    variance target   #factors   IC (t)          Q5-universe (t)
    0.40              3.0        +0.0341 (4.27)  +3.19%/yr (2.27)
    0.55              7.0        +0.0402 (5.60)  +6.14%/yr (4.18)
    0.75              20.3       +0.0350 (5.11)  +4.59%/yr (3.48)

The interior optimum replicates, and it is at the value the source pre-specifies.
Two controls matter more than the level. Running the **identical OU machinery on
total returns with no factor removal** gives IC +0.0399 / Q5-uni +4.11%/yr, so
residualisation is worth about +2%/yr of Q5 spread rather than nothing. And the
plain **cumulative 60-day total return** — the thing this could trivially be in
costume — is a clean null (IC -0.0009, t=-0.07; Q5-Q1 -5.94%/yr). So the OU
standardisation, not a 3-month reversal, is what is being measured.

WHAT IT DOES. At each month-end: PCA the 252-day correlation matrix of daily
returns, take enough eigenportfolios (weighted 1/sigma_i) to explain 55% of
variance, regress every name on them, cumulate the residual over the last 60
days, and fit an OU process to that cumulative residual. A name is *admissible*
only if its estimated reversion is fast enough to complete inside the estimation
window (kappa > 252/30, i.e. tau < 30 trading days) — a falsifiable
admissibility condition nothing in this lab's reversal work has used. Among
admissible names, open a long when the s-score s = (X - m)/sigma_eq falls below
-1.25 and close it when s rises above -0.50; both thresholds are the source's
own, not tuned here. Equal weight over whatever is open, fully invested.

Measured on train, holdings-only: mean 10.2 names (min 4, max 32), annual
turnover 17.9x. That is expensive — ~2.7%/yr at 15 bps a side — and it is
pre-registered as the main thing that could sink an otherwise real signal. The
conditional bucket's gross train edge is +7.56%/yr over the universe (t = 3.29)
at s < -1.25, so roughly 4.9%/yr should survive costs *if* the train reading
transfers.

WHAT WOULD FALSIFY IT. A validation Sharpe at or below the 0.49 equal-weight
global sleeve floor. Pre-registered expectation: 0.55-0.80 — a floor-clearing
family lead, not a challenger. Nothing here is argued as a decorrelation play:
per `SUMMARY.md` #54, a long-only book at gross <= 1.0 holds only the cheap side
of the residual and keeps the market exposure it cannot short away, so this
answers a *selection* question only.

CAVEATS RECORDED IN ADVANCE. (a) 55% was bracketed on train against 40% and 75%
and won; it is the source's pre-specified value rather than a swept one, but it
is still a train-informed choice and is stated as such. (b) The eligible set at
each date is names with a complete 252-day return history, which thins the early
train split toward US listings. (c) A minimum of 8 admissible names is held when
the excursion condition qualifies fewer, so the book never collapses to one name
and quietly becomes a de-risking overlay; measured, this backstop leaves mean
positions at 10.2 against 9.7 without it and turnover essentially unchanged.
(d) Equal weight throughout: magnitude weighting is a `price-trend` finding and
`CLAUDE.md` forbids carrying it into a new family by analogy.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import walkforward as W

STRATEGY = {
    "name": "sa_pca_residual_excursion",
    "family": "statistical-arbitrage",
    "track": "scout",
    "hypothesis": (
        "Selecting names by a conditional OU excursion of their PCA residual — "
        "factor count fixed by a 55% explained-variance target, admissibility "
        "gated on estimated reversion speed (kappa > 252/30), long opened at "
        "s < -1.25 and closed at s > -0.50, equal-weighted and rebalanced "
        "monthly — earns a validation Sharpe above the 0.49 equal-weight floor "
        "net of 15 bps costs, i.e. the residual-reversion premise survives once "
        "the factor count is out of the region the lab's earlier k in {1,3,5} "
        "screen tested and the trade is conditioned on an excursion rather than "
        "measured as an unconditional cross-sectional IC."
    ),
}

PCA_WIN = 252          # source's estimation window for the factors
OU_WIN = 60            # source's estimation window for the residual process
VAR_TARGET = 0.55      # source's stated optimum; bracketed on train vs 0.40/0.75
MAX_FACTORS = 30
KAPPA_MIN = 252.0 / (OU_WIN / 2.0)   # tau shorter than half the OU window
OPEN_S = -1.25         # source's entry threshold
CLOSE_S = -0.50        # source's exit threshold
MIN_NAMES = 8
WARMUP = 13


def _scores(window: pd.DataFrame) -> pd.DataFrame | None:
    """s-score and kappa for every name with a complete window. Uses only the
    rows handed in, so nothing after the formation date can be read."""
    window = window.dropna(axis=1, how="any")
    if window.shape[1] < 40 or len(window) < PCA_WIN - 5:
        return None
    sd = window.std(ddof=1)
    sd = sd[sd > 0]
    if len(sd) < 40:
        return None
    window = window[sd.index]
    z = (window - window.mean()) / sd
    corr = np.corrcoef(z.values, rowvar=False)
    if not np.isfinite(corr).all():
        return None
    eigval, eigvec = np.linalg.eigh(corr)
    order = np.argsort(eigval)[::-1]
    eigval, eigvec = eigval[order], eigvec[:, order]
    k = int(np.searchsorted(np.cumsum(eigval) / eigval.sum(), VAR_TARGET) + 1)
    k = max(1, min(k, MAX_FACTORS))

    # Eigenportfolio returns: the j-th loading divided by the name's own vol,
    # which is the source's construction (equal risk contribution per name).
    factors = window.values @ (eigvec[:, :k] / sd.values[:, None])
    design = np.column_stack([np.ones(len(factors)), factors])
    beta, *_ = np.linalg.lstsq(design, window.values, rcond=None)
    resid = window.values - design @ beta

    cum = np.cumsum(resid[-OU_WIN:], axis=0)
    x0, x1 = cum[:-1], cum[1:]
    m0, m1 = x0.mean(0), x1.mean(0)
    denom = ((x0 - m0) ** 2).sum(0)
    with np.errstate(all="ignore"):
        b = np.where(denom > 0, ((x0 - m0) * (x1 - m1)).sum(0) / denom, np.nan)
        a = m1 - b * m0
        ok = (b > 1e-6) & (b < 0.9999)
        var_xi = ((x1 - (a + b * x0)) ** 2).sum(0) / (len(x0) - 2)
        sigma_eq = np.sqrt(var_xi / (1.0 - b ** 2))
        s = np.where(ok & (sigma_eq > 0), (cum[-1] - a / (1.0 - b)) / sigma_eq, np.nan)
        kappa = np.where(ok, -np.log(b) * 252.0, np.nan)
    return pd.DataFrame({"s": s, "kappa": kappa}, index=window.columns)


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    returns = prices.pct_change()
    positions = {d: i for i, d in enumerate(prices.index)}
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        i = positions[dt]
        if i < PCA_WIN + 5:
            continue
        panel = _scores(returns.iloc[i - PCA_WIN + 1 : i + 1])
        if panel is None:
            continue
        admissible = panel[panel["kappa"] > KAPPA_MIN]["s"].dropna()
        if admissible.empty:
            continue
        keep = {n for n in held if n in admissible.index and admissible[n] < CLOSE_S}
        held = keep | set(admissible.index[admissible < OPEN_S])
        if len(held) < MIN_NAMES:
            # Backstop: top up with the deepest admissible excursions so the book
            # never shrinks into an accidental cash overlay.
            for name in admissible.sort_values().index:
                if len(held) >= MIN_NAMES:
                    break
                held.add(name)
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
