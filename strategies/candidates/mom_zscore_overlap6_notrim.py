"""Ablation: the champion with its daily vol-spike trim removed entirely.

WHY THIS IS WORTH A TRIAL. Tonight's trial #37 re-specified the trim's
realized-vol trigger to measure the basket it actually de-risks (the champion's
version qualifies names on a complete history back to 1962, admitting a mean of
3 of 34 held names and 11% of book weight). Correcting it *lowered* validation
Sharpe, 1.107 -> 1.050, and cost return in all six validation years. That
leaves an uncomfortable possibility the repo cannot answer from the trials it
has on `main`: that the trim contributes nothing on this base when specified
correctly, and that the champion's margin over an untrimmed book rests on a
degenerate 3-name universe rather than on crash detection.

The archived 2026-08-15 session ran this exact ablation and recorded validation
Sharpe 1.062, but the `## Protocol issue — 2026-08-16` entry is explicit that no
number from those sessions may be treated as established until re-run through
`run_experiment.py` against `main`'s own trial history — the same reason trial
#32 was re-run before anything was built on it. This is that re-run, and it is
the control the trim's whole line has never had on `main`.

THE CHANGE. Signal, buffer, magnitude weighting, six-tranche overlap and
MAX_WEIGHT are byte-identical to the champion. The daily exposure scalar is
deleted, so the book is the plain monthly-rebalanced average of the six most
recent formations and holds no cash.

WHAT EACH OUTCOME MEANS. This candidate is not expected to PROMOTE — it should
land below the champion's 1.107. The question is *where*:
  - near 1.05, i.e. next to the correctly-specified trim of trial #37, means
    the trim mechanism is worth approximately nothing on this base and the
    champion's edge over it is an artifact of the degenerate universe;
  - materially below 1.05 means the trim earns its keep even though the
    correctly-specified version does not, which would be a strange result
    worth stating plainly rather than explaining away.
Either way the answer bounds how much of the champion's validation Sharpe is
attributable to a component the repo has been citing as one of its strongest
mechanisms.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_zscore_overlap6_notrim",
    "family": "cross-sectional momentum",
    "hypothesis": (
        "Removing the daily vol-spike trim from the champion entirely leaves "
        "validation Sharpe at or near the 1.050 of the correctly-specified "
        "trim (trial #37) rather than materially below it, net of 15 bps "
        "costs, because the trim's apparent contribution to the champion's "
        "1.107 comes from a degenerate trigger universe — a mean of 3 of 34 "
        "held names — rather than from detecting turbulence in the book."
    ),
}

LOOKBACK_LONG = 252
LOOKBACK_SHORT = 126
SKIP = 21
CORE_N = 15
BAND_N = 25
MAX_WEIGHT = 0.25
FLOOR = 0.05

N_TRANCHES = 6


def _momentum(hist: pd.DataFrame, lookback: int) -> pd.Series:
    past = hist.iloc[-(lookback + SKIP) - 1]
    recent = hist.iloc[-SKIP - 1]
    return (recent / past - 1).dropna()


def _zscore(s: pd.Series) -> pd.Series:
    mu, sigma = s.mean(), s.std(ddof=0)
    return (s - mu) / sigma if sigma > 0 else s * 0.0


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    recent_targets = []

    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK_LONG + SKIP + 1:
            continue
        mom_long = _momentum(hist, LOOKBACK_LONG)
        mom_short = _momentum(hist, LOOKBACK_SHORT)
        common = mom_long.index.intersection(mom_short.index)
        if len(common) < CORE_N:
            continue

        composite = _zscore(mom_long[common]) + _zscore(mom_short[common])
        ranked = composite.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core

        c_held = composite[list(held)]
        raw = c_held - c_held.min() + FLOOR
        target = raw / raw.sum()

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

    return pd.DataFrame.from_dict(rows, orient="index")
