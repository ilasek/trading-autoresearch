"""The sizing ablation of `rv_minvar_closedform`: same long set, equal weight.

TRANSCRIBED FROM `## Pre-registration addendum — 2026-09-24`, entry **T4**,
written before this file existed and before any number from it was computed. One
node changes against T2 and every other node is byte-identical.

THE ONE CHANGE. `rv_minvar_closedform` sizes the surviving set by
`(1/s2_i)(1 - beta_i/beta_L)`. This file keeps the **membership** rule exactly --
the same single-factor model on the equal-weight universe return, the same
250-day window, the same 20-day lag, the same `beta_L = (C + 1/var(r_m))/B`
fixed point iterated over the shrinking long set, the same 25% cap -- and sizes
the survivors **equally**.

WHAT IT MEASURES, AND WHY IT IS A RULE AND NOT A KNOB. The two arms differ by
exactly the quantity `research/SUMMARY.md` #1's triage rule grades: T2 estimates
`n` residual variances and this file estimates **nothing**. `learnings.md`
reproduces both of this repo's weighting verdicts with that rule, and every one
of those measurements was made inside `price-trend`; `CLAUDE.md` forbids
carrying this file's constants into a new family by analogy and requires
re-measuring them there. With membership held fixed, T2 versus T4 is the
cleanest available test of that rule outside the incumbent's family.

WHAT THE NIGHT'S FREE MEASUREMENT ALREADY ESTABLISHED, SO THIS IS NOT ASKED
BLIND. F3's diversification-ratio decomposition of T2, holdings only, 75 sampled
validation dates: `CR` 0.0669 (the most evenly divided risk of the three books
measured), effective risk bets 9.40 (the highest), and volatility-weighted
`rho_bar` **0.2960** (also the highest). T2's 3.34% ex-ante volatility came from
holding low-volatility *names*, not from holding names that replicate each other
less. What it does not say is whether the `1/s2_i` sizing helped or hurt, which
is what this arm isolates.

BRANCHES, FIXED IN ADVANCE. Validation Sharpe **above 0.313** says the triage
rule transfers out of `price-trend` and T2's sizing term was estimation error
rather than its objective being wrong; the gap is then the first price this repo
has put on that rule in a second family. **At or below 0.313** says the rule
takes its first recorded miss and CdST's claim that idiosyncratic risk should
decide position size survives a test designed to break it.

`track: "scout"`, family `range-variance`, and it is not a promotion argument in
either branch: it is aimed at the variance channel and `SUMMARY.md` #142 stands.

ANTI-CANDIDATE ATTACHED. Do **not** add an inverse-*total*-volatility third arm
later. That is the volatility level, which on this universe is the survivorship
artifact, and the family is closed for weighting-scheme work after tonight.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

STRATEGY = {
    "name": "rv_minvar_equalweight",
    "family": "range-variance",
    "track": "scout",
    "hypothesis": (
        "Keeping the closed-form long-only minimum-variance MEMBERSHIP rule "
        "(beta_i < beta_L, with beta_L = (C + 1/var(r_m))/B iterated to its own "
        "fixed point) byte-identical to rv_minvar_closedform and replacing only "
        "its 1/s2_i sizing with equal weight raises validation Sharpe above "
        "that book's 0.313, because the two arms differ by exactly the n "
        "estimated residual variances that SUMMARY.md #1's parameter-count "
        "triage rule says are paid for out-of-sample — a rule this repo has "
        "only ever measured inside price-trend."
    ),
}

# transcribed from rv_minvar_closedform, unchanged
WINDOW = 250
LAG = 20
MAX_WEIGHT = 0.25
MIN_NAMES = 8
MAX_PASSES = 50


def _long_set(block: np.ndarray, names: list[str]) -> pd.Series:
    """Equal weight over the long-only minimum-variance long set.

    Membership is identical to `rv_minvar_closedform._min_variance_weights`;
    only the sizing of the survivors differs.
    """
    mkt = block.mean(axis=1)
    var_m = mkt.var(ddof=1)
    if not np.isfinite(var_m) or var_m <= 0:
        return pd.Series(dtype=float)

    centred = block - block.mean(axis=0)
    m_centred = mkt - mkt.mean()
    cov = (centred * m_centred[:, None]).sum(axis=0) / (len(block) - 1)
    beta = cov / var_m
    total_var = centred.var(axis=0, ddof=1)
    resid_var = total_var - np.square(beta) * var_m

    ok = np.isfinite(beta) & np.isfinite(resid_var) & (resid_var > 0)
    if ok.sum() < MIN_NAMES:
        return pd.Series(dtype=float)
    beta, resid_var = beta[ok], resid_var[ok]
    cols = [n for n, keep in zip(names, ok) if keep]

    live = np.ones(len(cols), dtype=bool)
    beta_l = np.nan
    for _ in range(MAX_PASSES):
        inv = 1.0 / resid_var[live]
        b_sum = float((beta[live] * inv).sum())
        c_sum = float((np.square(beta[live]) * inv).sum())
        if b_sum <= 0:
            return pd.Series(dtype=float)
        beta_l = (c_sum + 1.0 / var_m) / b_sum
        nxt = live & (beta < beta_l)
        if nxt.sum() < MIN_NAMES:
            break
        if np.array_equal(nxt, live):
            break
        live = nxt

    if not np.isfinite(beta_l) or live.sum() < MIN_NAMES:
        return pd.Series(dtype=float)

    # the one change against T2: equal weight, estimating nothing.
    held = [n for n, keep in zip(cols, live) if keep]
    w = pd.Series(1.0 / len(held), index=held)
    if (w > MAX_WEIGHT).any():
        w = w.clip(upper=MAX_WEIGHT)
        w = w / w.sum()
    return w


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    all_names = list(prices.columns)
    positions = {dt: i for i, dt in enumerate(prices.index)}
    ret_values = prices.pct_change(fill_method=None).to_numpy()

    rows: dict[pd.Timestamp, pd.Series] = {}
    for dt in rebalance_dates:
        end = positions[dt] - LAG + 1
        start = end - WINDOW
        if start < 1:
            continue
        block = ret_values[start:end]
        finite = np.isfinite(block).all(axis=0)
        if finite.sum() < MIN_NAMES:
            continue
        w = _long_set(
            block[:, finite], [n for n, keep in zip(all_names, finite) if keep]
        )
        if w.empty:
            continue
        full = pd.Series(0.0, index=prices.columns)
        full[w.index] = w
        rows[dt] = full

    return pd.DataFrame.from_dict(rows, orient="index")
