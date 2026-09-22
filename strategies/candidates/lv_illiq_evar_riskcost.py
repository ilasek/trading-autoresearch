"""Are the trading-cost and risk-cost limits to arbitrage two channels or one?

WHERE THIS COMES FROM AND WHAT WAS PAID BEFORE IT. `research/SUMMARY.md` #137,
tonight's highest-ranked book, gated behind two preconditions that were fixed in
the journal before anything was computed and then measured free (no trial, no
returns scored, train only):

  (a) PRECONDITION — 42 of 140 instruments are ETFs, i.e. baskets, and should be
      the easiest things here to hedge with other baskets. Measured: ETF mean
      `E/Var` 0.741 against single-name 0.430, Cohen's d +1.59, rank-AUC 0.815
      over 133 quarters. PASS, and sharply.
  (b) ARTIFACT SCREEN — the entire claim to novelty is that this is not the
      volatility level, which on this universe is the survivorship artifact.
      Measured on train: `|spearman(E/Var, 21d Garman-Klass vol)| = 0.148` and
      `|spearman(E/Var, rank 12-1)| = 0.015`, against a threshold of 0.50 fixed
      in advance. PASS. For contrast the 250-day realized-vol level comes in at
      0.238, so the ratio is the part that escapes the artifact, as the source
      says it should be.

WHAT `E/Var` IS. Wurgler-Zhuravskaya's arbitrage risk is the residual variance
`A` of a name against its best substitute basket; the hedgeable fraction
`E/Var = 1 - A/Var` is the part of its variance a substitute basket does span.
With a single equal-weight basket regressor this is exactly the regression `R^2`,
so it is computed here in closed form as `corr(name, basket)^2` — dimensionless
in volatility by construction, which is the whole point. Substitutes are the
`K = 4` names with highest trailing correlation over a 250-day window ending
`LAG = 20` days before the measurement date (the source's own `[-365, -20]`
template, and a causality convenience here). Closes only, so no foreign-holiday
volume NaN.

THE HYPOTHESIS, AND WHY IT IS A CONDITIONING VARIABLE RATHER THAN A NEW SCORE.
`#137` forbids a standalone sort: the source makes no claim about average
returns, only about price response to flow, and a candidate claiming otherwise
claims more than the paper does. So the base score here is the family's seated
lead — `lv_illiq_region_wide30`, region-relative Amihud illiquidity — reproduced
bit-identically (same 63-day window, same hold-45/enter-30 band, same region
operator with `MIN_REGION = 4`, same equal weighting, same month-end grid), and
`E/Var` enters only as a second standardized term. Amihud illiquidity is the
*trading*-cost limit to arbitrage: what it costs to move the price. `E/Var` is
the *risk*-cost limit: what cannot be hedged while you wait. Wurgler-Zhuravskaya's
claim is precisely that the second is distinct from and not subsumed by the
first. If it is, adding it should improve the family lead; if the two are one
channel wearing two hats, it should not.

THE IDENTIFICATION PROBLEM, AND HOW IT IS HANDLED RATHER THAN NOTED. Gate (a)
succeeded, and its success *is* the confound: low `E/Var` means "single stock"
far more than it means anything else, and single stocks are where this universe's
survivorship bias is worst. A raw low-`E/Var` tilt would therefore be a
stock-versus-ETF tilt in disguise and would be unidentified in exactly the sense
`#138` warns about. So `E/Var` is demeaned **within instrument type** (ETF
against ETFs, stock against stocks) before it is standardized, which removes the
ETF/stock axis — the survivorship axis — by construction. This is the same
operator the family's own one measurement win used (`lv_illiq_region_relative`,
a region demean); the type demean is its analogue on the axis this particular
variable loads on. `groups.TYPE_OF` is static metadata from `data/universe.yaml`
— no dates, no prices, nothing estimated from returns.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below the family lead's 0.942
says the risk-cost channel adds nothing the trading-cost channel does not already
carry on this universe — which would be a genuine result about the two proxies
being one object here, and it would close `#137` rather than leave it open. A
materially *worse* number says the type-demeaned hedgeable fraction is actively
mis-signed here, and the direction would then be worth one line in `learnings.md`
and nothing more.

WHAT IS NOT CLAIMED. Nothing about average returns as such; nothing about the
level of arbitrage risk, which the source itself says is near-collinear with
total variance and which gate (b)'s contrast number supports. And this is a
scout: it never compares against the champion and never reaches the holdout.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_evar_riskcost",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Adding a type-demeaned hedgeable-fraction term (-E/Var, the residual "
        "share of a name's variance against its 4 most-correlated substitutes "
        "over a 250-day window lagged 20 days) to the seated family lead's "
        "region-relative Amihud score — window, band, weighting, pool, region "
        "operator and rebalance grid otherwise bit-identical to "
        "lv_illiq_region_wide30 — beats that lead's 0.942 validation Sharpe, "
        "because Amihud measures the trading cost of arbitrage and E/Var "
        "measures its risk cost, and Wurgler-Zhuravskaya's claim is that the "
        "second is a distinct limit rather than a restatement of the first."
    ),
}

# --- transcribed from the seated family lead, unchanged ---
ILLIQ_WINDOW = 63
CORE_N = 30
BAND_N = 45
WARMUP = 6
MIN_REGION = 4

# --- the one new object, with the source's own window template ---
EVAR_WINDOW = 250
EVAR_LAG = 20
EVAR_K = 4
MIN_TYPE = 4          # a type below this cannot supply a peer mean


def _demean_by(score: pd.Series, mapping: dict[str, str], min_size: int) -> pd.Series:
    """Each name's score minus the mean of its own group, dropping names whose
    group is too small to supply a peer mean. `mapping` is static instrument
    metadata, so this reads only the cross-section it is handed."""
    labels = pd.Series({name: mapping.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= min_size).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    sd = s.std(ddof=0)
    return (s - s.mean()) / sd if sd > 0 else s * 0.0


def _hedgeable_fraction(window: np.ndarray, names: list[str]) -> pd.Series:
    """E/Var = corr(name, its top-K substitute basket)^2, in closed form.

    With one equal-weight basket regressor the regression R^2 *is* the squared
    correlation, so no least-squares fit is needed and nothing is estimated that
    a correlation matrix does not already contain."""
    v = window - window.mean(axis=0)
    sd = v.std(axis=0, ddof=1)
    ok = sd > 0
    if ok.sum() <= EVAR_K + 1:
        return pd.Series(dtype=float)
    v, sd = v[:, ok], sd[ok]
    cols = [n for n, keep in zip(names, ok) if keep]
    n = len(cols)

    corr = (v.T @ v) / (len(v) - 1) / np.outer(sd, sd)
    np.fill_diagonal(corr, -np.inf)
    top = np.argpartition(-corr, EVAR_K - 1, axis=1)[:, :EVAR_K]

    sel = np.zeros((n, n))
    sel[np.arange(n)[:, None], top] = 1.0 / EVAR_K
    baskets = v @ sel.T                       # column j is name j's substitute basket
    b_sd = baskets.std(axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        rho = (v * baskets).sum(axis=0) / (len(v) - 1) / (sd * b_sd)
    return pd.Series(np.square(np.clip(rho, -1.0, 1.0)), index=cols).replace(
        [np.inf, -np.inf], np.nan
    ).dropna()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)
    rets = prices.pct_change(fill_method=None)
    ret_values = rets.to_numpy()
    all_names = list(prices.columns)
    positions = {dt: i for i, dt in enumerate(prices.index)}

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        end = positions[dt] - EVAR_LAG + 1
        start = end - EVAR_WINDOW
        if start < 1:
            continue
        block = ret_values[start:end]
        finite = np.isfinite(block).all(axis=0)
        if finite.sum() < BAND_N:
            continue
        evar = _hedgeable_fraction(
            block[:, finite], [n for n, keep in zip(all_names, finite) if keep]
        )
        if evar.empty:
            continue

        illiq_score = _demean_by(
            illiq.loc[:dt].iloc[-1].dropna(), G.REGION_OF, MIN_REGION
        )
        # low E/Var = hard to hedge = costly to arbitrage, so the sign is negated.
        risk_score = _demean_by(-evar, G.TYPE_OF, MIN_TYPE)

        common = illiq_score.index.intersection(risk_score.index)
        if len(common) < BAND_N:
            continue
        score = _zscore(illiq_score[common]) + _zscore(risk_score[common])

        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
