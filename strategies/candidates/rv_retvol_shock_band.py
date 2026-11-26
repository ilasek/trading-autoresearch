"""A THIRD CHANNEL FOR THE BASELINE-PURITY RULE -- and this file is the CONTROL arm, run
first and predicted to be a null.

WHAT THE RECORD ESTABLISHED ON TWO CHANNELS (2026-11-25, six matched books, one node apart):

    channel  arm                        val sharpe  net skill  bill   GROSS skill  null pctile
    volume   jump guard IN window (#32)   +0.368     +0.031   0.180     +0.211         99%
    volume   guard DISPLACED (#41)        +0.250     -0.085   0.186     +0.101         97%
    volume   NO guard (#40)               +0.200     -0.138   0.204     +0.066         95%
    range    median filter IN window(#42) +0.250     -0.084   0.203     +0.119         95%
    range    NO filter (#38)              +0.183     -0.154   0.164     +0.010         79%
    range    filter DISPLACED (#43)       +0.146     -0.190   0.181     -0.009         58%

The IN-WINDOW position carried +0.110 of gross skill on the volume channel and +0.109 on the
range channel. The claim is that a score of the form "recent window minus baseline window" is
corrupted when its BASELINE itself contains a discontinuity -- it is then measuring a decaying
baseline rather than a fresh event -- and that this is a property of shock scores rather than
of share volume or of the intraday range. Two channels is a replication; three would make it
the first construction law this lab has.

THE THIRD CHANNEL, AND WHY IT IS THE ONLY ONE REACHABLE. The two used channels are share
VOLUME (a count) and the INTRADAY RANGE (high/low). The third ratio-only quantity this
protocol passes is the CLOSE-TO-CLOSE return. `dollar_volume` is not available for this
purpose: it is close x volume and so carries the dividend half of the as-of-fetch
back-adjustment factor `D_i(t)` (`learnings.md`, 2026-10-21/22), which is why the recorded
`lv_vol_trend_*` objects cannot host this test. An adjusted-close return is a ratio of two
stored prices inside the visible window, so the split half of `D_i(t)` cancels exactly and the
dividend half IS the distribution, i.e. the return is the total return and nothing spurious
enters. `|r|` is in the same units as `log(high/low)` -- both are log price changes, and
Parkinson's estimator is the statement that one is a rescaling of the other in expectation --
so the operator transplants with no change of units and no new parameter.

WHY THIS ARM IS RUN AND WHAT IT IS FOR. It is the unfiltered CONTROL. The purity term is a
DIFFERENCE of two gross skills, so the third channel cannot be read without the arm that has
no filter on it, exactly as #38 had to be run before #42 and #43 could be read. It is
predicted to be a null.

FREE PRE-TRIAL SCREEN, measured before this file was written. No train signal statistic
(no IC, no train skill, no forward return) was computed for any arm tonight.

    coverage of eligible names        98.7%   (99.7% / 99.7% / 97.2% by decade)
    rank rho to the 5/45 RANGE shock  +0.580
    rank rho to the 5/45 VOLUME shock +0.321
    rank rho to trailing 126d vol     +0.039   -- not a volatility-level sort
    rank rho to 12-1 momentum         +0.025
    rank rho to the board lead        -0.007
    top-100 Jaccard vs the bare range book (#38)   0.407
    phi -0.014, exit200 45.2%, exit100 70.1%, predicted train churn 14.1x
    ETF share of holdings 7.1% (panel is 5.5% of a median train month-end)

Rank rho +0.580 to the range shock is the honest number here: the two are correlated, as two
volatility-expansion measures must be, and 0.407 top-100 overlap is well inside the 0.90
relabelling bar -- but this arm is NOT claimed to be an independent bet from #38, and the
2026-11-25 finding that the bare range and bare volume shocks correlate at +0.638 in ACTIVE
RETURNS while living on different channels says to expect this book's return stream to look
like #38's. That is a reason to run it as a control and not as a candidate.

PRE-REGISTERED PREDICTIONS, written before the run.
 - GROSS skill: a NULL, in [-0.03, +0.05]; null percentile 50-85%. The attention channel was
   already measured null bare on the range panel and nothing predicts it to appear here.
 - NET skill: negative, around -0.15 to -0.25 (bill 0.17-0.27 of Sharpe at this churn).
 - CHURN: train 11-17x, validation 15-30x (predictor 14.1x; the 2026-11-22 rule
   `train one-way churn ~ 1.0 + 0.29 x exit200%` and the 1.30-2.00x validation multiplier).
 - A POSITIVE bare reading would be the surprise, and would say the return channel carries
   something the range channel does not -- which is a finding about the channel, not about
   the purity rule, and would be reported as such.

WHAT ARGUES AGAINST THE BOOK.
 (i) It is a fast book on a panel whose binding constraint is turnover (`learnings.md`,
     2026-10-25/26), so its net skill cannot be competitive and it is a scout by design.
 (ii) A wide absolute return is the short-horizon reversal's conditioning variable with its
     sign thrown away, so if the bare arm reads positive the first alternative explanation is
     reversal and not attention. The displaced-filter arm does not separate those two; only a
     signed control would, and none is run tonight.
 (iii) The 0.580 rank rho to #38 means this is a third CHANNEL and not a third BET. The
     breadth mandate is served by the night's other families, not by this arm.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
FAST = 5            # rows of recent absolute return
SLOW = 45           # rows of baseline, ending FAST+1 rows ago

STRATEGY = {
    "name": "rv_retvol_shock_band",
    "family": "range-variance",
    "hypothesis": (
        "Holding the 100 eligible names with the HIGHEST close-to-close return shock -- mean "
        "|log return| over the last 5 printing days minus the median over the preceding 45, "
        "taken only where both days of the return printed a volume, quota-allocated across "
        "(trailing-trading-calendar peer group x instrument type) cells, monthly with a "
        "200-name retention band -- earns GROSS validation skill within noise of zero and a "
        "null percentile below 85%, i.e. it is a NULL bare, because the Merton-recognition / "
        "Barber-Odean attention channel was already measured null as a bare sort on the "
        "intraday-range channel and the close-to-close channel adds no new mechanism; this "
        "arm exists as the unfiltered control against which the in-window and displaced "
        "baseline-purity filters are differenced on a third data channel."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """High short-window close-to-close return shock, quota'd across (calendar peer group x
    instrument type), monthly with a retention band. `rv_range_shock_band` with one node
    changed: the channel the shock is measured on.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    # A return needs TWO real prints: the close is forward-filled on a 10-day cap, so a
    # holiday would otherwise contribute a zero return and the next day a two-day one.
    printed = volume.notna() & (volume > 0)
    absr = np.log(prices).diff().where(printed & printed.shift(1)).abs()

    fast = absr.rolling(FAST, min_periods=3).mean()
    slow = absr.shift(FAST).rolling(SLOW, min_periods=25).median()
    shock = fast - slow

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        score = shock.loc[date].reindex(names).dropna()
        if len(score) < 60:
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()
        cells = (groups.reindex(score.index).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in score.index],
                             index=score.index))

        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, cells.reindex(rest.index).dropna(), K - len(keep))
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
