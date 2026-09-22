"""The sign falsifier for trial #96: does the arbitrage-risk term carry direction?

WHY THIS EXISTS. Trial #96 (`lv_illiq_evar_riskcost`, validation 1.053) took the
seated `liquidity-volume` lead's region-relative Amihud score and added one term:
the type-demeaned negative hedgeable fraction, `-E/Var`. It beat the lead by
+0.111 and it rests on a mechanism claim — low `E/Var` means hard to hedge, which
means costly to arbitrage, which means mispricing persists, which is what an
illiquidity book is trying to hold.

There is a duller explanation, and it is the one that has to be ruled out before
#96 means anything: **any** second standardized term added to a one-term score
may improve it simply by spreading ties and reducing the sort's noise, in which
case the arbitrage story is decoration on a mechanical effect.

THE TEST. This file is #96 with **the sign of the `E/Var` term reversed** and
nothing else changed — same 63-day Amihud window, same hold-45/enter-30 band,
same region operator with `MIN_REGION = 4`, same type demean, same equal
weighting, same month-end grid, same 250-day/lag-20/K-4 `E/Var` computed by the
same code path. The book now tilts toward names that are **easy** to hedge, i.e.
cheap to arbitrage, which is the opposite of what the mechanism predicts should
pay.

THE READING, FIXED IN THE JOURNAL BEFORE THIS RAN. Materially **below** the 0.942
seated lead means the term carries direction and #96's mechanism claim survives.
**At or above 0.942** means both signs improve the lead, the gain is the added
dispersion rather than arbitrage risk, and **#96 must be read down to "a second
term helps" regardless of its Sharpe.** Both branches are stated in advance so
neither can be chosen afterwards.

WHY THIS FALSIFIER AND NOT THE LEVEL-VERSUS-RATIO ABLATION. Replacing `E/Var`
with total variance would test the source's other claim, but a variance **level**
on this universe is the survivorship artifact, so a good score there would seat a
knowingly-artifactual book at the top of a non-`price-trend` family — exactly what
`SUMMARY.md` #137 warns against. The reversed term is the same dimensionless
ratio, so anti-candidates #134 and #138 are untouched whichever way this lands.
"""


from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_evar_signflip",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Reversing the sign of trial #96's type-demeaned hedgeable-fraction "
        "term — so the book tilts toward names that are EASY to hedge, and "
        "therefore cheap to arbitrage — while holding the window, band, pool, "
        "weighting, region operator, type demean and rebalance grid "
        "bit-identical, scores materially below the seated family lead's "
        "0.942, because if the arbitrage-risk mechanism is what #96 measured "
        "then the term must carry direction, and if instead both signs improve "
        "the lead then #96's gain was the added dispersion of a second term "
        "rather than arbitrage risk at all."
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
        # SIGN REVERSED against #96: this tilts toward names that are EASY
        # to hedge. The whole point of the file is that this should lose.
        risk_score = _demean_by(evar, G.TYPE_OF, MIN_TYPE)

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
