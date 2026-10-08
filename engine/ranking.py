"""Ranking with error bars (protocol v3).

A leaderboard sorted by one six-year Sharpe ratio reads like a ranking and is
mostly noise: on the v1 history the observed #1 was still #1 in 23% of
bootstrap resamples, and none of ranks 2-20 could be separated from it. This
module turns a set of validation return series into a ranking that says how
much of its order the data actually supports:

- `skill` (Sharpe minus the equal-weight eligible pool's) with a 90% paired
  stationary-bootstrap interval;
- `p_best`, the share of resamples in which the strategy ranks first;
- the **model confidence set** (Hansen, Lunde & Nason 2011, T_max statistic):
  the strategies that cannot be distinguished from the best at level `alpha`.
  Order *inside* the set is not evidence of anything;
- `mechanism_clusters`: strategies whose *active* returns (minus the pool)
  correlate at or above a threshold are one mechanism, whatever family label
  their authors gave them. Raw returns cannot be used for this: every
  long-only book correlates ~0.8 with every other through the market.

Nothing here reads a split; it works on return series already recorded.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import metrics

MCS_ALPHA = 0.10
MECHANISM_RHO = 0.5


def confidence_set(boots: np.ndarray, observed: np.ndarray, alpha: float = MCS_ALPHA
                   ) -> tuple[np.ndarray, np.ndarray]:
    """Model confidence set on a higher-is-better statistic.

    `boots` (n_boot, k) are bootstrap replicates of the statistic, `observed`
    (k,) its sample value. Returns (in_set bool (k,), mcs_pvalue (k,)): a
    strategy's MCS p-value is the running maximum of the elimination p-values
    up to its own elimination (1.0 for survivors)."""
    k = len(observed)
    alive = np.ones(k, dtype=bool)
    pvals = np.ones(k)
    running = 0.0
    while alive.sum() > 1:
        cols = np.flatnonzero(alive)
        d = observed[cols] - observed[cols].mean()
        db = boots[:, cols] - boots[:, cols].mean(axis=1, keepdims=True)
        sd = db.std(axis=0, ddof=1)
        sd = np.where(sd > 0, sd, np.inf)
        t = d / sd
        stat = np.max(-t)
        null = np.max(-(db - d) / sd, axis=1)
        p = float((null >= stat).mean())
        running = max(running, p)
        if p >= alpha:
            break
        worst = cols[int(np.argmax(-t))]
        alive[worst] = False
        pvals[worst] = running
    return alive, np.where(alive, 1.0, pvals)


def mechanism_clusters(active: pd.DataFrame, rho: float = MECHANISM_RHO) -> dict[str, int]:
    """{column: cluster id}, single linkage on the correlation of active
    returns. Cluster ids are numbered in column order from 1."""
    cols = list(active.columns)
    corr = active.corr().to_numpy() if len(cols) > 1 else np.ones((1, 1))
    parent = list(range(len(cols)))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            if np.isfinite(corr[i, j]) and corr[i, j] >= rho:
                parent[find(i)] = find(j)
    roots: dict[int, int] = {}
    out = {}
    for i, c in enumerate(cols):
        r = find(i)
        roots.setdefault(r, len(roots) + 1)
        out[c] = roots[r]
    return out


def rank_table(returns: pd.DataFrame, pool: pd.Series | None, rf: pd.Series | None = None,
               alpha: float = MCS_ALPHA, n_boot: int = metrics.BOOT_DRAWS,
               mean_block: float = metrics.BOOT_BLOCK, seed: int = metrics.BOOT_SEED,
               mechanism_rho: float = MECHANISM_RHO) -> pd.DataFrame:
    """One row per column of `returns` (validation returns of the strategies
    being ranked, on the same days as `pool`), sorted by skill.

    Columns: sharpe, skill, skill_lo, skill_hi (90%), p_best, in_mcs,
    mcs_pvalue, mechanism, and `tier`: 1 = in the confidence set of the best,
    2 = outside it but skill interval above zero, 3 = neither.

    Without a `pool` (trials recorded before v3 stored one) the table ranks on
    Sharpe alone: no skill columns, mechanisms on raw returns, tier 1 or 3."""
    if pool is None:
        return _rank_sharpe_only(returns, rf, alpha, n_boot, mean_block, seed)
    joined = pd.concat([returns, pool.rename("__pool__")], axis=1, join="inner").dropna()
    ex = joined.apply(lambda s: metrics.excess(s, rf))
    boots = metrics.bootstrap_sharpes(ex, n_boot, mean_block, seed)
    obs = np.array([metrics.sharpe(ex[c]) for c in ex.columns])
    cand_boot, pool_boot = boots[:, :-1], boots[:, -1:]
    cand_obs, pool_obs = obs[:-1], obs[-1]
    skill_boot = cand_boot - pool_boot
    in_set, pv = confidence_set(cand_boot, cand_obs, alpha)
    best = np.argmax(cand_boot, axis=1)
    names = list(returns.columns)
    active = joined[names].sub(joined["__pool__"], axis=0)
    mech = mechanism_clusters(active, mechanism_rho)
    lo = np.quantile(skill_boot, 0.05, axis=0)
    hi = np.quantile(skill_boot, 0.95, axis=0)
    table = pd.DataFrame({
        "sharpe": cand_obs.round(3),
        "skill": (cand_obs - pool_obs).round(3),
        "skill_lo": lo.round(3),
        "skill_hi": hi.round(3),
        "p_best": np.array([(best == i).mean() for i in range(len(names))]).round(3),
        "in_mcs": in_set,
        "mcs_pvalue": pv.round(3),
        "mechanism": [mech[n] for n in names],
    }, index=names)
    table["tier"] = np.where(table["in_mcs"], 1, np.where(table["skill_lo"] > 0, 2, 3))
    table.attrs["pool_sharpe"] = round(float(pool_obs), 3)
    table.attrs["n_days"] = int(len(joined))
    return table.sort_values(["tier", "skill"], ascending=[True, False])


def _rank_sharpe_only(returns, rf, alpha, n_boot, mean_block, seed) -> pd.DataFrame:
    joined = returns.dropna()
    ex = joined.apply(lambda s: metrics.excess(s, rf))
    boots = metrics.bootstrap_sharpes(ex, n_boot, mean_block, seed)
    obs = np.array([metrics.sharpe(ex[c]) for c in ex.columns])
    in_set, pv = confidence_set(boots, obs, alpha)
    best = np.argmax(boots, axis=1)
    names = list(returns.columns)
    table = pd.DataFrame({
        "sharpe": obs.round(3),
        "sharpe_lo": np.quantile(boots, 0.05, axis=0).round(3),
        "sharpe_hi": np.quantile(boots, 0.95, axis=0).round(3),
        "p_best": np.array([(best == i).mean() for i in range(len(names))]).round(3),
        "in_mcs": in_set,
        "mcs_pvalue": pv.round(3),
    }, index=names)
    table["tier"] = np.where(table["in_mcs"], 1, 3)
    table.attrs["n_days"] = int(len(joined))
    return table.sort_values(["tier", "sharpe"], ascending=[True, False])
