"""The volatility LEVEL in the same cheap harness — the control vol-of-vol needs.

WHY THIS FILE EXISTS. `rv_volofvol_neutral_band` ran tonight and came in at
validation skill **-0.191** at the 14th percentile of its null, on 4.5x
validation churn against a pre-registered 0.6-1.8x. Two readings of that are
consistent with the number and they imply opposite things about where this lab
should look next:

  (a) the SCORE is the problem -- volatility instability is not priced here, as
      the volatility level is not; or
  (b) the HARNESS is the problem -- K = 100 with a peer quota, a 200-name band
      and monthly rebalancing cannot clear this panel's null gate whatever score
      is poured into it, and 4.5x churn is paying ~50 bps/yr for the privilege.

Nothing in trial one separates them, because it has no partner. This file is the
partner: the same K, the same calendar-peer quota, the same 200-name retention
band, the same monthly grid, the same pool-during-warm-up rule, the same
eligibility masking -- with the score replaced by the plain trailing 126-day
volatility level, low held.

ONE HONEST DIFFERENCE, STATED RATHER THAN SMOOTHED. This is not a
one-operator pair. Trial one's quota cells are (peer group x volatility
tercile), and a volatility-LEVEL score inside a volatility-tercile quota is
degenerate -- it would rank names by volatility within terciles of volatility,
where the dispersion has been removed on purpose. So the tercile cell is dropped
here and the quota is on the peer group alone. The pair therefore differs in the
score AND in the tercile neutralisation, and the two trials together bracket the
question rather than resolving it to one operator. Said plainly because the
2026-10-15/16 entry's cleanest result came from a pair that really did differ in
one operator, and this one does not.

WHY RE-MEASURE AN OBJECT THE RECORD CALLS A NULL, AND THE SPECIFIC REASON
`CLAUDE.md` REQUIRES. `learnings.md` closes the low-volatility anomaly on this
panel (2026-10-09/10, "Sharpe is flat in beta", since reproduced six times) and
trial #1 `pt_lowvol_gk_quarterly` measured skill -0.03. But #1 is not the control
for tonight's book: it was a QUARTERLY book on a GARMAN-KLASS estimator with no
peer quota, no retention band and K drawn differently. The comparison this file
makes is to tonight's harness, not to the low-volatility literature, and the
quantity of interest is the DIFFERENCE between the two trials rather than either
level. A re-test whose purpose is to calibrate a harness is not a re-test of a
refuted hypothesis.

THE SIGN is low volatility held, fixed from the same mechanism as #1 and not
re-derived.

WHAT THE PAIR CAN AND CANNOT SETTLE. If this book lands near -0.19 as well, the
harness is the binding term and the lab's whole current construction corner --
K = 100, peer quota, band, monthly -- is what needs re-pricing, which would be a
statement about the lab rather than about volatility. If it lands materially
above -0.19, vol-of-vol is specifically bad and the instability axis closes. If
it lands materially below, the tercile neutralisation was doing real work and
that operator is worth carrying. All three readings are results; none of them is
a reason to run a third variant tonight, because a third would be the "keep
trying treatments until one reads" failure the record names.

NO TRAIN NUMBER IS OFFERED AS EVIDENCE, for the reason in trial one's file:
corr(train skill, validation skill) is -0.08 over 27 recorded trials, so a train
sheet cannot qualify a candidate, and the 2026-10-16/17 rule permits a train
screen to refute but not to qualify.

PRE-REGISTERED TURNOVER, carried unrevised from tonight's pre-registration so
the record shows whether the range was right: **0.5-2.0x** one-way per year. A
volatility-level ranking is far more rank-persistent than tonight's demeaned
vol-of-vol, so the band should bite here where it did not there. Flagged rather
than silently widened: trial one's validation churn ran 73% above its train
figure, so the top of this range is probably optimistic, and that is exactly the
kind of thing a pre-registered range exists to expose.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.features import realized_vol

K = 100
BAND = 200
VOL_WINDOW = 126

STRATEGY = {
    "name": "pt_lowvol126_quota_band",
    "family": "price-trend",
    "hypothesis": (
        "Holding the 100 eligible names with the LOWEST trailing 126-day close-to-close "
        "volatility, quota-allocated across trailing-trading-calendar peer groups, "
        "monthly with a 200-name retention band, earns validation skill materially "
        "different from the -0.191 that tonight's vol-of-vol book earned in the same "
        "harness -- which would attribute that result to the score rather than to the "
        "construction; and if instead it lands near -0.191, the binding term is the "
        "harness this lab has standardised on rather than either volatility statistic."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Low trailing volatility, calendar-peer quota'd, monthly with a retention band.
    Trial one's harness with the score replaced and the volatility-tercile cell dropped.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    level = realized_vol(prices, VOL_WINDOW)

    held: list[str] = []
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        score = (-level.loc[date].reindex(names)).dropna()
        if len(score) < 60:
            # Warm-up: hold the pool rather than cash (2026-10-15/16). Once a book
            # exists, emit nothing and let it drift rather than trade on no score.
            if not held:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, score.index).dropna()
        if len(groups) < 50:
            continue
        score = score.reindex(groups.index).dropna()

        rank = score.rank(ascending=False, method="first")
        inband = [n for n in held if n in rank.index and rank[n] <= BAND]
        keep = list(rank.reindex(inband).sort_values().index)
        if len(keep) >= K:
            picked = pd.Index(keep[:K])
        else:
            rest = score.drop(index=keep, errors="ignore")
            add = peer_quota_select(rest, groups.reindex(rest.index).dropna(), K - len(keep))
            picked = pd.Index(keep).append(pd.Index(add))
        if len(picked) < 20:
            continue

        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
