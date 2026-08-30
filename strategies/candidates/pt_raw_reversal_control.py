"""The turnover-matched control for `lv_trading_time_reversal`.

WHY THIS EXISTS. `learnings.md` records, from four consecutive trials on
2026-08-29, that "outside `price-trend`, turnover differences dominate every
mechanism comparison the lab tries to run", and prescribes the fix: "Hold
turnover fixed by design, or report the gross decomposition explicitly, or
accept that the trial measured the broker." This file is that design. It is
`lv_trading_time_reversal` with **one expression changed** — the score is the
negative raw 21-day return instead of the negative 21-day sum of
volume-rescaled returns. Same horizon, same 20-enter/30-hold band, same equal
weight, same monthly grid, same universe, same warmup. Measured holdings-only on
the train split before either ran, the two books' annual turnover is 11.93x and
11.80x respectively, so the difference between them is which names they pick and
nothing else.

WHAT THE PAIR ANSWERS. On train, the rescaling was worth +3.35%/yr of Q5-universe
spread at the 21-day horizon (+2.50%/yr, t = 1.27 raw against +5.85%/yr, t = 2.81
rescaled) and it converted a null into a signal. `lv_trading_time_reversal`
subsequently scored validation Sharpe 0.590. The only reading that establishes the
mechanism rather than the horizon is this control's number: if raw 21-day reversal
lands materially below 0.590 the volume rescaling is doing real work out of sample;
if it lands at or above, the train result was the transformation flattering itself
and what the pair actually measured was a 21-day reversal book.

WHAT WOULD FALSIFY THE MECHANISM. This control scoring at or above 0.590.

FAMILY. Raw short-horizon reversal is `price-trend` under `program.md`'s
collapse of the legacy families, and this is one of that family's two permitted
slots for the session. It is filed as a scout: it exists to interpret another
trial, not to compete for the seat, and a 21-day reversal book has no plausible
route to the champion's 1.120.

CAVEAT RECORDED IN ADVANCE. The lab already has `str_reversal_monthly`
(validation 0.820, rho 0.682, 19.45x turnover, 15 names) in the leaderboard's
legacy "short-term mean reversion" slot. That is a *different* construction — a
different name count, no band, and a different reversal window — so it is not a
substitute for this control, and the two numbers should not be differenced.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pt_raw_reversal_control",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "Fading the raw 21-day return on the identical construction as "
        "`lv_trading_time_reversal` (hold 20 names, hold-30/enter-20 band, equal "
        "weight, monthly) scores a validation Sharpe materially below that "
        "candidate's 0.590 — i.e. the volume rescaling, and not the choice of a "
        "monthly horizon or the shared 20/30 book construction, is what produced "
        "its result, the two books having been shown holdings-only to run the "
        "same annual turnover (11.93x against 11.80x on train)."
    ),
}

REVERSAL_WIN = 21
CORE_N = 20
BAND_N = 30
WARMUP = 6


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    score = -(prices / prices.shift(REVERSAL_WIN) - 1.0)
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
