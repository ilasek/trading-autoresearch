"""Does the arbitrage-risk channel condition the incumbent's own score, or is it
a `liquidity-volume` object only?

THIS CANDIDATE WAS FULLY SPECIFIED BEFORE ITS NUMBERS EXISTED. Every constant
below, the base construction, the family, the track, the run order and both
branches of the falsifier are transcribed verbatim from
`experiments/journal.md`'s `## Pre-registration for the NEXT session —
2026-09-22`. Nothing was chosen after a measurement tonight.

WHAT LICENSES IT, AND IT IS ONE NUMBER. Trial #96 introduced `E/Var` — the
hedgeable fraction of a name's variance against its four most-correlated
substitutes — and passed two orthogonality gates fixed in the journal before
any book existed: `|spearman(E/Var, 21d Garman-Klass vol)| = 0.148` against the
survivorship artifact, and `|spearman(E/Var, rank 12-1)| = 0.015` against the
*incumbent's own score*. The second number is the one that points here.
Wurgler-Zhuravskaya's mechanism is that mispricing persists where arbitrage is
costly; cross-sectional momentum is a mispricing-continuation signal; so the
interaction the mechanism predicts is with a continuation score specifically,
and a measured rank correlation of 0.015 says the term would be *adding*
information to that score rather than restating it. Trial #96 tested the term
next to a trading-cost proxy (Amihud). It has never been tested next to the
continuation signal its own mechanism names.

THE CHANGE, AND IT IS ONE CHANGE. The seated champion
`mom_zscore_overlap6_hzn_avg4`, reproduced byte-for-byte in every node — the
same four lookbacks (252/189/126/63) over the same 21-day skip, the same
hold-25/enter-15 band per leg, the same `c - c.min() + FLOOR` magnitude
weighting, the same equal average across legs, the same six-tranche formation
overlap, the same 25% cap and the same daily vol-spike trim — with the per-leg
score changed from `zscore(momentum)` to
`zscore(momentum) + zscore(type-demeaned -E/Var)`. Nothing else is touched.

`E/Var` CONSTANTS, TRANSCRIBED AND NOT RE-SWEPT. 250-day window, 20-day lag,
`K = 4` substitutes, equal-weight basket, closed-form `corr^2` (with one
equal-weight basket regressor the regression `R^2` *is* the squared
correlation, so nothing is fitted that a correlation matrix does not already
contain), demeaned within `groups.TYPE_OF` at `MIN_TYPE = 4`. The type demean
is load-bearing rather than cosmetic: `E/Var` separates ETFs from single names
at rank-AUC 0.815, and single names are where this universe's survivorship bias
is worst, so an un-demeaned tilt would be a stock-versus-ETF bet in disguise —
the unidentified shape `research/SUMMARY.md` #138 warns about.

WHY THIS IS `price-trend` AND WHY IT IS A CHALLENGER. It modifies the
incumbent, so it is `price-trend` whatever its new term's provenance, and it
counts against that family's cap of two. Because it can reach the holdout gate
it is run first in its session, before any candidate whose design would
otherwise be holdout-informed.

WHAT WOULD FALSIFY IT, BOTH BRANCHES FIXED IN ADVANCE. Validation Sharpe at or
below the champion's 1.120 says the interaction is absent on the incumbent's
own score and the `E/Var` vein is a `liquidity-volume` object only, which closes
`research/SUMMARY.md` #137 at its most favourable reading. Above 1.120 it goes
to the deflated-Sharpe bar and the holdout veto on its own merits.

STATED IN ADVANCE AGAINST THE OBJECTIVE, SO THE RESULT CANNOT BE READ MORE
GENEROUSLY THAN IT DESERVES. Trial #96's own evidence is that this term's
*gain* does not resolve on this split (t = +0.79 on the `liquidity-volume`
book) while its mis-signed damage does (t = -2.38, trial #97). The honest prior
is therefore a small move the split cannot resolve, and a large one would be
the surprise. The number to read is the paired `t` against the champion under
`metrics.sharpe_diff_se`, not the Sharpe difference on its own; at the
correlation a one-term change to the champion will sit at, `learnings.md`'s
required-gain table asks for +0.044 to +0.138 and the family's resolution floor
is 0.03-0.08.

WHAT IS NOT CLAIMED, AND ONE ANTI-CANDIDATE CARRIED. Nothing about the *level*
of arbitrage risk, which the source itself says is near-collinear with total
variance and which on this universe is the survivorship artifact — the ratio is
the whole novelty, and substituting the level is a standing anti-candidate. No
knob of `E/Var` is swept here and none may be swept later.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import groups as G

STRATEGY = {
    "name": "pt_mom_evar_arbrisk",
    "family": "price-trend",
    "track": "challenge",
    "hypothesis": (
        "Replacing the champion's per-leg score with "
        "zscore(momentum) + zscore(type-demeaned -E/Var) — the hedgeable "
        "fraction of a name's variance against its 4 most-correlated "
        "substitutes over a 250-day window lagged 20 days, demeaned within "
        "instrument type — while leaving every other node of "
        "mom_zscore_overlap6_hzn_avg4 byte-identical, raises validation "
        "Sharpe above 1.120, because momentum is a mispricing-continuation "
        "signal and Wurgler-Zhuravskaya's arbitrage-risk channel says "
        "continuation should persist further where a name's variance is least "
        "hedgeable, a quantity measured at rank correlation 0.015 to the "
        "momentum score and therefore not a restatement of it."
    ),
}

# --- transcribed from the seated champion, unchanged ---
LOOKBACKS = (252, 189, 126, 63)
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 6

VOL_SHORT = 21
VOL_LONG = 252
SPIKE_RATIO = 1.6
TRIM_SCALE = 0.6

# --- transcribed from trial #96, not re-swept ---
EVAR_WINDOW = 250
EVAR_LAG = 20
EVAR_K = 4
MIN_TYPE = 4


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def _demean_by(score: pd.Series, mapping: dict, min_size: int) -> pd.Series:
    """Each name's score minus the mean of its own group, dropping names whose
    group is too small to supply a peer mean. `mapping` is static instrument
    metadata from `data/universe.yaml` — no dates, no prices, nothing estimated
    from returns — so this reads only the cross-section it is handed."""
    labels = pd.Series({name: mapping.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= min_size).dropna()


def _hedgeable_fraction(window: np.ndarray, names: list) -> pd.Series:
    """E/Var = corr(name, its top-K substitute basket)^2, in closed form."""
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


def _leg_target(score: pd.Series, held: set) -> tuple:
    ranked = score.sort_values(ascending=False)
    core = set(ranked.index[:CORE_N])
    band = set(ranked.index[:BAND_N])
    held = (held & band) | core
    c_held = score[list(held)]
    raw = c_held - c_held.min() + FLOOR
    return raw / raw.sum(), held


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = {lb: set() for lb in LOOKBACKS}
    recent_targets = []
    base_periods = []

    all_dates = prices.index
    max_lb = max(LOOKBACKS)

    ret_values = prices.pct_change(fill_method=None).to_numpy()
    all_names = list(prices.columns)
    positions = {dt: i for i, dt in enumerate(all_dates)}

    for i, dt in enumerate(rebalance_dates):
        hist = prices.loc[:dt]
        if len(hist) < max_lb + SKIP + 1:
            continue

        moms = {lb: _momentum(hist, lb) for lb in LOOKBACKS}
        common = None
        for m in moms.values():
            common = m.index if common is None else common.intersection(m.index)

        end = positions[dt] - EVAR_LAG + 1
        start = end - EVAR_WINDOW
        if start < 1:
            continue
        block = ret_values[start:end]
        finite = np.isfinite(block).all(axis=0)
        if finite.sum() <= EVAR_K + 1:
            continue
        evar = _hedgeable_fraction(
            block[:, finite], [n for n, keep in zip(all_names, finite) if keep]
        )
        if evar.empty:
            continue
        # low E/Var = least hedgeable = costliest to arbitrage, so negate.
        risk_score = _demean_by(-evar, G.TYPE_OF, MIN_TYPE)

        common = common.intersection(risk_score.index)
        if len(common) < CORE_N:
            continue

        z_risk = _zscore(risk_score[common])
        leg_targets = []
        for lb in LOOKBACKS:
            score = _zscore(moms[lb][common]) + z_risk
            t, held[lb] = _leg_target(score, held[lb])
            leg_targets.append(t)
        target = pd.concat(leg_targets, axis=1).fillna(0.0).mean(axis=1)
        target = target / target.sum()

        recent_targets.append(target)
        if len(recent_targets) > N_TRANCHES:
            recent_targets.pop(0)

        blended = pd.concat(recent_targets, axis=1).fillna(0.0).mean(axis=1)
        norm = blended / blended.sum()
        if (norm > MAX_WEIGHT).any():
            norm = norm.clip(upper=MAX_WEIGHT)
            norm = norm / norm.sum()

        w_full = pd.Series(0.0, index=prices.columns)
        w_full[norm.index] = norm
        rows[dt] = w_full

        start_pos = all_dates.get_loc(dt)
        next_dt = rebalance_dates[i + 1] if i + 1 < len(rebalance_dates) else None
        end_pos = all_dates.get_loc(next_dt) if next_dt is not None else len(all_dates)
        base_periods.append((start_pos, end_pos, norm))

    if not base_periods:
        return pd.DataFrame.from_dict(rows, orient="index")

    last_scale = 1.0
    for start_pos, end_pos, norm in base_periods:
        names = list(norm.index)
        sub = prices.iloc[:end_pos][names]
        avail = sub.dropna(axis=1, how="any").columns
        if len(avail) == 0:
            continue
        rets = sub[avail].pct_change()
        basket_ret = rets.mean(axis=1)
        vol_short = basket_ret.rolling(VOL_SHORT).std(ddof=0)
        vol_long = basket_ret.rolling(VOL_LONG).std(ddof=0)
        ratio = vol_short / vol_long
        scale_series = (ratio > SPIKE_RATIO).map({True: TRIM_SCALE, False: 1.0})
        scale_series = scale_series.where(vol_long > 0, 1.0)

        day_scales = scale_series.iloc[start_pos:end_pos]
        for dt2, scale in day_scales.items():
            if pd.isna(scale):
                scale = 1.0
            if dt2 in rows:
                rows[dt2] = rows[dt2] * scale
                last_scale = scale
                continue
            if scale != last_scale:
                w_full = pd.Series(0.0, index=prices.columns)
                w_full[norm.index] = norm * scale
                rows[dt2] = w_full
                last_scale = scale

    return pd.DataFrame.from_dict(rows, orient="index")
