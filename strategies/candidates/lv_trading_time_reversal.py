"""Does rescaling returns by the volume that produced them move the reversal
premium up to a horizon the cost model can afford?

WHY THIS, AND WHY IT IS A `liquidity-volume` CANDIDATE. The 2026-08-29 session
closed with the sharpest negative result the lab has: raw short-horizon reversal
is "the strongest signal measurable on this universe" (5-day IC +0.0455) and it
"sits exactly at the horizon the cost model structurally forbids", decaying to a
null by 21 days. `research/SUMMARY.md` #56 proposes a transformation rather than
a new sort: replace each return by `R~ = R x <dV>/dV`, where dV is the day's
dollar volume and <dV> a short trailing average. Moves made on heavy volume
shrink; moves made on light volume inflate. Economically: **do not fade a move
that came with heavy trading**, because it is more likely information than an
excursion worth reverting. The active ingredient is entirely the volume panel —
the untransformed version of this signal is a measured null — so the family slug
is `liquidity-volume`, not `price-trend`.

THE PREMISE, MEASURED BEFORE THIS FILE WAS WRITTEN (train split, no returns
scored, 21-day forward returns, ~400 monthly formation dates). Reversal signals,
raw against trading-time-rescaled:

    horizon   raw IC (t)         raw Q5-uni (t)      rescaled IC (t)     rescaled Q5-uni (t)
     5d       +0.0369 (3.86)     +7.23%/yr (3.83)    +0.0441 (4.64)      +8.32%/yr (4.42)
    10d       +0.0328 (3.47)     +5.55%/yr (2.98)    +0.0459 (4.92)      +9.43%/yr (5.01)
    21d       +0.0102 (0.97)     +2.50%/yr (1.27)    +0.0227 (2.23)      +5.85%/yr (2.81)

The 21-day row is the whole point: raw monthly reversal is the null the last
session recorded, and the rescaled version is not. This candidate trades the
21-day horizon precisely because it is the one a monthly book can reach.

THREE CONTROLS RUN FIRST, ALL FREE. (a) *Is it a hidden liquidity tilt?* The
scale factor **on its own** is a null (log mean scale over 5d: IC +0.0034,
t = +0.45; over 21d: +0.0032, t = +0.43), so the interaction carries the signal,
not the level — this is not the Amihud lead in disguise. (b) *Is it a tuned
knob?* No: the clip on the scale factor is not load-bearing (IC +0.0208 / +0.0205
/ +0.0222 / +0.0218 at no clip / 3 / 5 / 10), and the trailing-average window is
flat too (+0.0196 / +0.0222 / +0.0236 at 5 / 10 / 21 days). The source's
un-optimised ~10-day default is kept. (c) *Is the comparison confounded by
turnover?* This is the one that matters most, given that four consecutive trials
on 2026-08-29 had their entire measured difference come from turnover. Measured
holdings-only on the identical 20-enter/30-hold construction: the rescaled book
runs **11.80x** annual turnover and the raw-reversal book **11.93x** — the same
book at the same cost, differing only in which names it picks. **The turnover
axis is held fixed by design here, not argued away afterwards.**

WHAT IT DOES. At each month-end, score every name by the negative of its
trading-time-rescaled 21-day return, hold the 20 highest with a hold-30/enter-20
band, equal weight, fully invested. Nothing else.

WHAT WOULD FALSIFY IT. A validation Sharpe at or below the 0.49 equal-weight
global sleeve floor, or — the more informative failure — a validation Sharpe at
or below the raw-reversal control run immediately after this on the same
construction, which would say the rescaling adds nothing out of sample even
though it adds 3.35%/yr of Q5 spread on train. Pre-registered expectation: 0.6
to 0.9, i.e. a family lead in the range the other scouts occupy, not a
challenger; the required-gain table makes a challenge hopeless at any plausible
rho and this is filed as a scout accordingly.

CAVEATS RECORDED IN ADVANCE. (a) The implementation trap `SUMMARY.md` #56 names
is real and handled: volume is not forward-filled and is NaN on foreign
holidays, so the trailing denominator must *skip* those days rather than read
them as zero volume, or the rescaling explodes exactly where the panel is
thinnest. `min_periods` on the rolling mean and a NaN (not zero) scale on
missing days do that; the rolling sum of rescaled returns likewise skips. (b)
The clip at 5x is a guard against a single near-zero-volume day dominating a
21-day sum, not a tuned parameter — see control (b). (c) Volume history is
thinner before the 2000s for non-US listings, so the train split leans US.
(d) Equal weight: magnitude weighting is a `price-trend` result and `CLAUDE.md`
forbids importing it here by analogy.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_trading_time_reversal",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Rescaling each daily return by the ratio of trailing-average dollar "
        "volume to that day's dollar volume, then fading the 21-day sum of the "
        "rescaled returns (hold 20 names, hold-30/enter-20 band, equal weight, "
        "monthly), earns a validation Sharpe above the 0.49 equal-weight floor "
        "net of 15 bps costs — i.e. down-weighting price moves that arrived on "
        "heavy volume moves part of the reversal premium from the 5-10 day "
        "horizon the cost model forbids up to the monthly horizon it allows, "
        "where the untransformed signal is a measured train-split null."
    ),
}

REVERSAL_WIN = 21
VOL_AVG_WIN = 10        # the source's un-optimised default
SCALE_CAP = 5.0
CORE_N = 20
BAND_N = 30
WARMUP = 6


def _trading_time_score(prices: pd.DataFrame, dollar_volume: pd.DataFrame) -> pd.DataFrame:
    """Negative 21-day sum of volume-rescaled returns. High score = fade this."""
    returns = prices.pct_change()
    avg_dv = dollar_volume.rolling(VOL_AVG_WIN, min_periods=VOL_AVG_WIN // 2).mean()
    with np.errstate(all="ignore"):
        scale = avg_dv / dollar_volume
    # A day the instrument did not trade has NaN volume, hence NaN scale, hence a
    # NaN rescaled return that the rolling sum skips. Reading it as zero volume
    # would divide by zero exactly where the panel is thinnest.
    scale = scale.replace([np.inf, -np.inf], np.nan).clip(upper=SCALE_CAP)
    rescaled = returns * scale
    return -rescaled.rolling(REVERSAL_WIN, min_periods=REVERSAL_WIN // 2).sum()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    score = _trading_time_score(prices, aux["dollar_volume"])
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        row = score.loc[:dt].iloc[-1].dropna()
        if len(row) < BAND_N:
            continue
        ranked = row.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
