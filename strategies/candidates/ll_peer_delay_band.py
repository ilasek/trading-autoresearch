"""Within-region information diffusion: the share of a name's weekly response
to its own most-correlated peers that arrives one week late.

Hypothesis (pre-registered, see the journal entry for this trial): the 100
eligible names whose weekly return loads most heavily on the ONE-WEEK-LAGGED
return of their own most-correlated same-calendar-peer-group basket, relative
to the contemporaneous loading, earn positive validation skill over the
equal-weight eligible pool, because Hong-Stein gradual information diffusion
says a name that prices its peer group's information late is a name whose
investor recognition is limited, and Hou-Moskowitz read that lag share as a
priced premium. Pre-signed direction: HIGH lag share earns MORE.

Why this family and why this object. `lead-lag-spillover` is the one family in
`program.md` with no recorded trial under any protocol version, and `CLAUDE.md`'s
budget rule requires at least one trial in such a family while one remains. The
family's cross-region half is structurally unreachable under v3 (the
random-selection null is region-matched, so a region-allocation edge is matched
move-for-move by its own replicas and cannot move the percentile off ~50%,
`experiments/learnings.md` 2026-10-13). This candidate is therefore in the only
reachable half: selection WITHIN a region, on a variable measured on OTHER names.

What the screen said, and it argues AGAINST this book on arithmetic. Thirteen
within-region spillover objects were screened free on train tonight (journal
F1-F5), region-matched, top and bottom 100, forward 63 days, 249 month-ends.
Not one has a positive region-matched excess in its pre-signed direction. This
object's own sheet, in the exact construction below:

    cal-peer delay, top 100, region-matched     -8.3 bps/63d  (t -0.86)
    1997-2008 / 2009-2017                       +8.4/+0.73   -31.2/-1.89
    whole-pool reading                           -4.6 bps/63d  (t -0.46)
    one-way name churn, band B=200               2.72x/yr  (5.74x unbanded)
    median scored names per date                 325 of ~500 eligible
    rho to own 21-day return / 126-day vol       -0.005 / +0.035
    rho to the market-lag price delay already
      nulled here (learnings 2026-10-14)         +0.441

So the expected verdict is a loss, and it is written down before the run: at
~21.7 bps a side on 2.72x one-way churn the book pays about 118 bps/yr against
a gross prize of about -33 bps/yr. The trial is spent anyway, for three stated
reasons and no others. (i) The budget rule is a rule, and two previous sessions
deferred it to the human owner without a ruling. (ii) This is the most
orthogonal score the lab has measured under v3 -- rank rho -0.005 to 21-day
return and +0.035 to trailing volatility -- and the lab's standing diagnosis of
its own board is that every new score turns out to be a refuted one in costume;
this one is not, and that is worth a recorded number. (iii) The lab's own
seven-trial calibration (learnings 2026-10-16/17) is that train skill and the
validation null percentile are uncorrelated (Spearman -0.571, n 7, slope SE
larger than the slope), so a weak train screen is not evidence either way --
a train screen may refute but may not qualify, and the refutation here is the
cost arithmetic rather than the excess, which the band has already minimised.

Two things deliberately NOT done. The bottom side of this sort reads +9.1 bps
(t +1.24) and is not traded: the literature signs the top, and choosing a sign
because the number came out that way is what `experiments/learnings.md` refuses
for the illiquid half (2026-10-13). And the 52-week estimation window reads
+3.6 bps where the 104-week window reads -8.3; the 104-week window is taken
because it is Hou-Moskowitz's own specification, not because of its number.

Pre-registered turnover, as a range with the wider split's churn in it: the
engine's metric counts both sides and validation name churn has run up to 68%
above train's, so 4.5-9.5x annualised is the predicted band.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
BAND = 200
NPEER = 10
CORR_WINDOW = 252
N_WEEKS = 104
MIN_WEEKS = 60
MIN_NAMES = 50

STRATEGY = {
    "name": "ll_peer_delay_band",
    "family": "lead-lag-spillover",
    "hypothesis": (
        "Selecting the 100 eligible names with the highest share of their weekly return "
        "response that arrives one week after their own most-correlated same-peer-group "
        "basket moves -- entries quota-allocated across trailing-trading-calendar peer "
        "groups so the book's geography matches the pool's, with a top-200 retention band "
        "-- earns positive validation skill over the equal-weight eligible pool, because "
        "gradual information diffusion predicts that a name which prices its peers' "
        "information late is compensated for limited investor recognition. Train screen "
        "reads -8.3 bps/63d region-matched (t -0.86), so a loss is the expected verdict; "
        "the score's rank correlation is -0.005 to 21-day return and +0.035 to trailing "
        "volatility, making it the most orthogonal object the lab has measured under v3."
    ),
    "track": "scout",
}


def _lag_share(weekly: np.ndarray, peer: np.ndarray) -> np.ndarray:
    """Per column: |b_lag| / (|b_contemp| + |b_lag|) from regressing a name's
    weekly return on the contemporaneous and one-week-lagged peer basket."""
    y, x0, x1 = weekly[1:], peer[1:], peer[:-1]
    out = np.full(weekly.shape[1], np.nan)
    ones = np.ones(len(y))
    for j in range(weekly.shape[1]):
        if not np.isfinite(x0[:, j]).all():
            continue
        design = np.column_stack([ones, x0[:, j], x1[:, j]])
        beta = np.linalg.lstsq(design, y[:, j], rcond=None)[0]
        denom = abs(beta[1]) + abs(beta[2])
        if denom > 1e-12:
            out[j] = abs(beta[2]) / denom
    return out


def generate_weights(prices, aux, eligible=None):
    """Monthly, equal-weight over the K highest peer-lag shares, quota-allocated
    across trailing-calendar peer groups, with a top-BAND retention band. The
    equal-weight eligible pool is emitted on month-ends where the score does not
    exist yet, so the book is never scored in cash against a fully-invested
    benchmark (`experiments/learnings.md`, 2026-10-15/16)."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    rets = prices.pct_change(fill_method=None)
    weekly_all = np.log(prices / prices.shift(5)).replace([np.inf, -np.inf], np.nan)

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows: dict = {}
    held: set = set()
    for date in month_ends:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < MIN_NAMES:
            continue
        pool = pd.Series(1.0 / len(names), index=names)

        # Peer groups from the trailing trading calendar, over the eligible
        # names only -- never the whole visible frame, whose column count
        # differs between the truncated and untruncated causality runs.
        groups = calendar_peers(volume, date, names)
        if groups.empty:
            rows[date] = pool
            continue
        window = rets.loc[:date, groups.index].iloc[-CORR_WINDOW:]
        good = groups.index[window.notna().sum().to_numpy() >= 150]
        if len(good) < MIN_NAMES:
            rows[date] = pool
            continue

        # Within-group correlation neighbours. Standardise on the window, then
        # mask every cross-group pair out before taking neighbours, so no
        # cross-region relationship can enter the basket.
        z = rets.loc[:date, good].iloc[-CORR_WINDOW:].fillna(0.0)
        z = ((z - z.mean()) / z.std(ddof=0).replace(0, np.nan)).fillna(0.0).to_numpy()
        corr = (z.T @ z) / z.shape[0]
        np.fill_diagonal(corr, -np.inf)
        label = groups.reindex(good).to_numpy()
        corr = np.where(label[:, None] == label[None, :], corr, -np.inf)
        order = np.argsort(-corr, axis=1)[:, :NPEER]
        ok = np.isfinite(np.take_along_axis(corr, order, axis=1))

        weekly = weekly_all.loc[:date, good].iloc[-5 * N_WEEKS::5].fillna(0.0).to_numpy()
        if weekly.shape[0] < MIN_WEEKS:
            rows[date] = pool
            continue
        basket = np.full_like(weekly, np.nan)
        for j in range(weekly.shape[1]):
            peers = order[j][ok[j]]
            if len(peers) >= 3:
                basket[:, j] = weekly[:, peers].mean(axis=1)

        score = pd.Series(_lag_share(weekly, basket), index=good).dropna()
        if len(score) < MIN_NAMES:
            rows[date] = pool
            continue

        # Retention band: a held name keeps its seat while it is inside the top
        # BAND of the current score, which is the long-only discrete form of the
        # proportional-cost no-trade band (learnings, 2026-10-10).
        ranked = score.rank(ascending=False)
        keep = [n for n in held if n in ranked.index and ranked[n] <= BAND]
        priority = score.copy()
        if keep:
            priority[keep] = priority.max() + 1.0
        picked = peer_quota_select(priority, groups.reindex(score.index), K)
        if len(picked) < 20:
            rows[date] = pool
            continue
        held = set(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
