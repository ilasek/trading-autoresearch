"""The distributional control for `pl_maxleg_signal_blend` (trial #68).

WHY THIS EXISTS. #68 is now the best non-`price-trend` result the lab has
recorded (validation 1.008, against its four legs' 0.681 / 0.747 / 0.688 / 0.701
and the mean-operator twin's 0.635), and the next session is expected to build a
challenge blend on it — it is the first leg in this repo's history to clear the
solved break-even bar (rho 0.732, k 0.778, needs 0.833, supplies 1.008). Before
that happens, the result should survive the check this repo has twice paid four
trials for skipping: **before crediting a component, check what its code actually
reads.**

THE SPECIFIC WORRY. `max` over z-scores is won by whichever leg has the fattest
right tail, so "max of z" may be partly "prefer the most skewed leg" rather than
"prefer the most convinced leg". That is a property of the *scoring transform*,
not of conviction, and it would not generalise to any other leg set. The legs
here are not distributionally alike: Amihud ILLIQ is a right-skewed ratio, and
the group-lead leg is a group-level value broadcast to members, so it carries
many ties and structurally less cross-sectional dispersion than a name-level
score.

THE CONTROL. Replace the cross-sectional z-score with the cross-sectional
percentile rank, and take the max of that. Ranks are uniform by construction, so
every leg contributes on an identical distribution and no leg can win a name on
skew alone. Everything else is bit-identical to #68: same four legs, same
joint-coverage rule, same core-20 / band-30 equal-weight monthly book, same
warmup, same universe. One expression changed.

MEASURED BEFORE THE RUN, HOLDINGS-ONLY. The screen says the control is neither a
no-op nor a rewrite: holdings overlap with #68's top-20 is **0.845 (train) /
0.815 (validation)**, so it re-draws 16-19% of the book. It does what it is
designed to do — the argmax share per leg goes from #68's uneven **0.247 / 0.226
/ 0.302 / 0.225** (train) and **0.183 / 0.289 / 0.263 / 0.265** (validation) to a
near-exact quarter each, **0.250 / 0.254 / 0.245 / 0.251** and **0.261 / 0.269 /
0.207 / 0.263**. And the artifact hypothesis is only weakly supported to begin
with: per-leg z-skewness is small and does not consistently favour one leg
(illiq +0.49 on train but -0.42 on validation), while the max z reached per leg
runs 1.78-3.71 with the *lowest* belonging to group-lead, which nonetheless has
the *highest* argmax share on train — the opposite of what a pure fat-tail story
predicts.

PRE-REGISTERED, FALSIFIABLE, AND STATED AS A BAND RATHER THAN A POINT. The claim
is that #68's result is a conviction effect and survives the transform: this book
lands **within +/-0.10 of 1.008**. It is falsified by landing **below 0.90**,
which would say the z-transform and not the max operator carried the headline and
that the next session must not build a challenge on it.

BOUNDARY, STATED BECAUSE THE MARGIN WILL NOT SUPPORT MORE. At 0.82-0.85 holdings
overlap these two books will correlate well above 0.95 on returns, so the paired
SE (`0.568*sqrt(1-rho)`) is of order 0.10 and a small gap between them is *not*
resolvable. What this trial can establish is the **direction and rough size** —
whether the effect is intact or gone — and that is what it is being spent on. It
cannot rank the two operators.

SCOUT. It does not compete for the seat and will not reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import signal_blend as SB
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_maxleg_rank_control",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "Taking the maximum of the four family-lead signals' cross-sectional PERCENTILE "
        "RANKS rather than of their z-scores — everything else bit-identical to trial "
        "#68, whose validation Sharpe was 1.008 — lands within 0.10 of that number, "
        "i.e. #68's result is a conviction effect rather than an artifact of the "
        "z-transform favouring whichever leg has the fattest right tail; ranks are "
        "uniform by construction and equalise the per-leg argmax share from #68's "
        "0.18-0.30 to a near-exact quarter each, while re-drawing only 16-19% of the "
        "held book."
    ),
}

CORE_N = 20
BAND_N = 30
WARMUP = 60          # month-ends skipped; the seasonal leg needs the history


def _integrate_max_rank(scores: dict[str, pd.DataFrame], at: pd.Timestamp,
                        min_names: int = 20) -> pd.Series:
    """`pl_maxleg_signal_blend._integrate_max` with the z-score replaced by a
    cross-sectional percentile rank. Reads only rows at or before `at`."""
    ranks: list[pd.Series] = []
    common: pd.Index | None = None
    for panel in scores.values():
        sub = panel.loc[:at]
        if sub.empty:
            return pd.Series(dtype=float)
        row = sub.iloc[-1].dropna()
        if len(row) < min_names:
            return pd.Series(dtype=float)
        r = row.rank(pct=True)
        ranks.append(r)
        common = r.index if common is None else common.intersection(r.index)

    if common is None or len(common) < min_names:
        return pd.Series(dtype=float)
    return pd.concat([r.reindex(common) for r in ranks], axis=1).max(axis=1)


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    legs = {
        "illiq": SB.illiquidity_score(prices, aux["dollar_volume"], 63),
        "seasonal": SB.seasonal_score(prices),
        "group_lead": SB.group_lead_score(prices, 21),
        "reversal": SB.reversal_score(prices, 21),
    }

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = _integrate_max_rank(legs, dt)
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
