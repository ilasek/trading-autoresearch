"""Is there an illiquidity premium left inside a universe of survivors?

WHY THIS FAMILY. `liquidity-volume` has never been scouted here for a single
mechanical reason: until 2026-08-29 strategies received closing prices only, so
no measure with volume in it was expressible. Amihud's ILLIQ — mean of
|daily return| / dollar volume traded, the average price impact of a dollar —
is the canonical daily-data liquidity measure precisely because it needs
nothing but prices and volumes, and it is therefore the first thing worth
asking of the newly available panel.

THE MECHANISM. A name that moves a lot per dollar traded is expensive to get
out of, and an investor who has to hold it demands compensation for that. The
claim is a risk premium, not a behavioural effect, which matters here: risk
premia are the kind that survive publication, and this one has been in the
literature long enough that a decayed or absent result is itself informative.

WHAT IT DOES. One sort, nothing else. At each month-end, rank every instrument
by log Amihud illiquidity measured over the trailing quarter, hold the 20 most
illiquid at equal weight, with a hold-30 / enter-20 band so that a name drifting
around the cutoff does not churn the book. Equal weight, not magnitude weight:
the size of an illiquidity score is not a forecast of return strength, and the
magnitude-weighting result this lab established is a finding about momentum
scores, which `CLAUDE.md` now explicitly forbids carrying into a new family by
analogy.

WHAT WOULD FALSIFY IT. A validation Sharpe at or below the 0.49 equal-weight
global sleeve floor. And the honest prior is that it might well fail: this
universe is ~140 large, heavily traded, currently-listed global names, which is
the part of the cross-section where the illiquidity premium is documented to be
weakest — the effect is concentrated in the small and genuinely illiquid tail
that a survivorship-selected mega-cap universe does not contain. A null here
would say something specific and useful — that the premium is not reachable on
this universe — rather than that the measure is wrong.

CAVEATS RECORDED IN ADVANCE. (a) Volume is not forward-filled, so a foreign
holiday leaves a NaN; the rolling mean skips it, which slightly thins the
estimate for non-US names. (b) Amihud is mechanically inverse to size, so this
is partly a small-cap tilt inside a large-cap universe, and survivorship bias
flatters exactly the smaller survivors. (c) Volume history is thinner before the
2000s for the non-US listings, so the train split leans US.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_amihud_illiquidity_tilt",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Holding the 20 most illiquid instruments by trailing-quarter Amihud ILLIQ, "
        "equal-weighted with a hold-30/enter-20 band and rebalanced monthly, earns a "
        "validation Sharpe above the 0.49 equal-weight floor net of 15 bps costs — "
        "i.e. an illiquidity premium is present and harvestable even within a universe "
        "of large, currently-listed survivors."
    ),
}

ILLIQ_WINDOW = 63     # one quarter
CORE_N = 20
BAND_N = 30
WARMUP = 6


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = illiq.loc[:dt].iloc[-1].dropna()
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        # Hysteresis: keep a name while it stays inside the wider band, enter
        # only on the tighter one. Cuts churn without changing what is being
        # measured.
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
