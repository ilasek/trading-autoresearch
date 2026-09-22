"""Does smoothing the *traded exposure* rescue volatility targeting on this universe?

WHY THIS CANDIDATE EXISTS, AND WHY IT WAS SPECIFIED BEFORE TONIGHT. The
2026-09-21 session killed the volatility-*forecasting* vein: HAR(3), HExp and a
pooled cross-instrument panel all beat the repo's 21-day trailing window gross
(+0.096 to +0.126 %/yr, with QLIKE and RMSE agreeing), and all three lost net of
15 bps/side by -2.45 to -3.38 %/yr, on 0 of 132 instruments for the panel,
because a 3-3.7x turnover multiple on the implied exposure is charged against a
gross edge two orders of magnitude smaller. The same session then found the
thing that actually moves the number: smoothing the exposure on the *incumbent*
estimator buys +0.86 %/yr against a best model-choice margin of +0.061 — a 14x
ratio, with all four estimators converging as the smoothing coefficient goes to
zero.

That `phi` grid was run after the session's own numbers were seen, so building a
book on it that night would have been post-hoc. It was pre-registered instead,
completely, with every constant fixed in advance and an explicit instruction not
to re-sweep them. This file honours that: `PHI`, `SIGMA_TARGET`, the estimator
and its window are transcribed, not chosen.

THE CONSTRUCTION. Equal weight across the universe's 42 ETFs, rebalanced
monthly, with gross exposure scaled by `min(1, SIGMA_TARGET / sigma_hat_t)` on
the sleeve's *own* realized variance. This is a time-series scale, never a
cross-sectional sort, so anti-candidate #134 — do not rank names on forecast
volatility — stays untouched: no name is ever preferred to another here. Weight
not allocated is cash, which `engine/backtest.py` holds rather than
renormalising, and which earns 0% rather than the risk-free rate. That drag is
real and no source in this vein models it.

WHY `phi = 0.05` IS STATED AS A KNOWN WEAKNESS RATHER THAN HIDDEN. It is the
2026-09-21 argmax. The defence is that the curve is monotone and flat below 0.10
(2.322 / 2.445 / 2.522 at 0.10 / 0.05 / 0.02), so the choice is not perched on a
spike; and `SIGMA_TARGET = 0.15` is near the sleeve's own historical level, so
`min(1, .)` binds sometimes rather than always or never. Neither is re-swept
tonight, and no second bracket is tried, because comparing brackets is the sweep
the manual forbids.

WHAT IS PREDICTED, AGAINST THE OBJECTIVE THIS ENGINE ACTUALLY SCORES. Harvey et
al. decompose volatility targeting's benefit into a trend-overlap half and an
unconditional half, and say the unconditional half shows up in the *tail*, not
in the Sharpe ratio. The 2026-09-21 session ran the source's own instrument and
found the trend-overlap half absent on this universe: +0.057 and +0.008 against
the +0.20 the reconciliation needed. So the honest prediction, stated here
before the run rather than produced afterwards, is a **mediocre Sharpe with a
thinner left tail**. The engine scores Sharpe. This candidate is therefore
expected to be judged on a statistic it is not optimising, and its max drawdown
is the number worth reading beside the verdict.

WHAT WOULD FALSIFY IT. Validation Sharpe at or below the standing ETF-sleeve
floor — 0.49 static equal-weight, 0.35 true inverse-vol — with no improvement in
max drawdown either. That would say the exposure-smoothing finding does not
survive contact with a traded book at all, rather than merely failing to show up
in the scored statistic. The `range-variance` lead to beat is `rv_volofvol_top15`
at 0.494.

A CAVEAT RECORDED IN ADVANCE. `learnings.md` says three distinct de-risking
overlays on momentum backfired out-of-sample. This is not one of them and must
not be read as a test of them: those scaled a momentum book, this scales a
diversified sleeve whose standalone Sharpe is ~0.49. The overlay question on the
champion is a separate measurement and is kept separate deliberately.
"""

import numpy as np
import pandas as pd

from strategies.lib import groups

STRATEGY = {
    "name": "rv_sleeve_voltarget_phi05",
    "family": "range-variance",
    "hypothesis": (
        "Scaling an equal-weight 42-ETF sleeve's gross exposure by "
        "min(1, 0.15 / sigma_hat) on its own trailing 21-day realized "
        "volatility, with the traded exposure smoothed at phi = 0.05 rather "
        "than traded raw, beats the standing ETF-sleeve floor of 0.49 "
        "(equal-weight) / 0.35 (inverse-vol) on validation Sharpe net of 15 "
        "bps per side, because the 2026-09-21 result was that smoothing the "
        "exposure — not choosing a better variance estimator — is what pays "
        "for itself after costs."
    ),
    "track": "scout",
}

# Every constant below is transcribed from the 2026-09-21 pre-registration and
# is deliberately not re-swept tonight.
SIGMA_TARGET = 0.15
PHI = 0.05
VOL_WINDOW = 21
TRADING_DAYS = 252

MIN_HISTORY = 252      # a name joins the sleeve only with a year of prices behind it
MIN_NAMES = 8          # below this the "sleeve" is not a diversified sleeve

ETFS = tuple(sorted(t for t, kind in groups.TYPE_OF.items() if kind == "etf"))


def _monthly_equal_weights(px: pd.DataFrame) -> pd.DataFrame:
    """Equal weight across the ETFs that are listed and seasoned at each month end."""
    rebalance_dates = px.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    seasoned = px.notna().cumsum()
    for dt in rebalance_dates:
        listed = px.loc[dt].dropna().index
        members = [c for c in listed if seasoned.at[dt, c] >= MIN_HISTORY]
        if len(members) < MIN_NAMES:
            continue
        rows[dt] = pd.Series(1.0 / len(members), index=members)
    if not rows:
        return pd.DataFrame(index=px.index, columns=px.columns, dtype=float)
    base = pd.DataFrame.from_dict(rows, orient="index").reindex(columns=px.columns)
    return base.reindex(px.index).ffill().fillna(0.0)


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ETFS if c in prices.columns]
    px = prices[cols]

    base = _monthly_equal_weights(px)

    # The sleeve's own realized return: yesterday's held weights against today's
    # move, so every input to sigma_hat_t is known at t.
    rets = px.pct_change(fill_method=None)
    sleeve_ret = (base.shift(1) * rets).sum(axis=1, min_count=1)

    sigma_hat = sleeve_ret.rolling(VOL_WINDOW, min_periods=VOL_WINDOW).std(ddof=0) * np.sqrt(
        TRADING_DAYS
    )
    raw_scale = (SIGMA_TARGET / sigma_hat).clip(upper=1.0)
    raw_scale = raw_scale.where(sigma_hat > 0)

    valid = raw_scale.dropna()
    if valid.empty:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    # s_t = PHI * raw_t + (1 - PHI) * s_{t-1}, seeded at the first valid reading.
    scale = valid.ewm(alpha=PHI, adjust=False).mean()

    weights = base.loc[scale.index].mul(scale, axis=0)
    weights = weights.reindex(columns=prices.columns).fillna(0.0)
    return weights.loc[(weights.abs().sum(axis=1) > 0)]
