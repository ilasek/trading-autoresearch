"""Ten-year reversal, held through a retention band, with the pool held during
the score's warm-up.

Hypothesis (pre-registered, see the journal entry for this trial): adding a
200-name retention band to the ten-year reversal raises its validation skill
above the unbanded trial #5's -0.006, because a band preserves a *mean-reverting*
score's selection while cutting the cost bill it is charged.

Why this is a trial and not a knob. Tonight's free block (F7) split every
screened object's net train skill into SELECTION (gross skill over the gross
pool) and COST (net minus gross), through the engine's own execution model, on
train only. Six of sixteen objects have a POSITIVE selection term and the cost
schedule takes all of it in every one except the lowest-turnover object:

    object (K=100, quota, monthly)   selection    cost    net skill   turn
    decade reversal                    +0.1202  -0.0163    +0.1039   2.20x
    maxret21 low                       +0.0761  -0.2027    -0.1265  12.40x
    lowvol126                          +0.0386  -0.0464    -0.0078   3.06x
    fracpos252                         +0.0092  -0.0577    -0.0485   5.04x
    residrev63                         +0.0048  -0.0959    -0.0910  10.09x
    12-1 momentum                      -0.0067  -0.0600    -0.0667   5.51x

So the binding constraint on this panel is turnover, not selection, and the
operator that addresses it is the band. `experiments/learnings.md` (2026-10-24/25)
bounds where a band pays: on a score whose decayed-but-not-reversed holdings
still earn (mean-reverting) it pays, and on a trend-persistence score it costs.
A ten-year reversal is the former, so the band is predicted to pay here -- and
it does, on train:

    decade reversal, no band                       net +0.1039  turn 2.20x
    decade reversal, band B=200                    net +0.1126  turn 1.13x
      selection +0.1148   cost -0.0022   vol/pool 1.019
      sub-periods 1997-2008 +0.0981 / 2009-2017 +0.0413

Trial #5 declined a band on the ground that its churn was already near the
pool's, so there was "nothing for a band to cut". That reasoning was about cost
and the cost saving is indeed small (0.014); the band is kept here because it
leaves the selection term intact (+0.1148 against +0.1202) while taking the
book to 1.13x -- below the pool's own 0.89x-class churn -- which is what makes
the comparison on validation a comparison of selection rather than of cost.
B=200 is trial #5's own declined-at-B=300 setting stepped back: at B=300 that
book went to 0.14x/yr and this lab's rider says a near-static book's
observations are one draw repeated. 1.13x is not near-static.

The warm-up operator is the standing rule of 2026-10-15/16 ("emit the
equal-weight eligible pool on dates where the score does not yet exist"), which
no trial has yet shipped. On a 120-month score it is worth +0.071 of train
skill (+0.0326 -> +0.1039, reproducing that entry's recorded +0.071 exactly).
It **cannot** change the validation verdict -- the score is formed on every
validation date, so the branch never fires there -- and is included because it
is the honest train number, not because it is expected to buy anything.

Free detectors run before this file was written, all on train:

  negation invariant        decade reversal +0.1126 vs decade MOMENTUM -0.1688
                            -- opposite signs, so the instrument is not
                            manufacturing agreement.
  back-adjustment leak      the score is a mean of monthly RETURNS, so the
                            back-adjustment factor D_i(t) cancels algebraically.
                            Confirmed empirically: across five-year buckets of
                            the decision date the known-contaminated control
                            (log price level) is single-signed at every bucket,
                            while this score's IC ALTERNATES (-0.120, +0.091,
                            +0.010, +0.018, -0.007 at h=63d, targets inside
                            train) -- not the monotone gradient of the leak.
  relabelling rho           +0.232 to -volatility126; trial #5 recorded +0.345
                            to three-year reversal, +0.126 to Amihud, +0.055 to
                            index seasoning, +0.014 to 21-day reversal.
  harness validation        the measurement harness above reproduces trial #5's
                            RECORDED engine figures to four decimals
                            (train_sharpe +0.5564 vs +0.5560, train_skill
                            +0.0326 vs +0.0330).

Two things recorded against the book rather than for it. (i) The score's IC
alternates in sign across five-year buckets and the 2000-2004 bucket (+0.091)
carries much of the train result, which is a value-rebound episode; both
protocol sub-periods are nonetheless positive. (ii) The 2026-10-18 engine issue
-- the random null's replicas are not held to the candidate's eligibility
boundary, worth up to +0.018 of Sharpe to the null and rising with holding
length -- falls hardest on a banded book, so part of this book's gate margin is
paid to that artifact. Both are reasons the validation number may come in below
the train number; neither is a reason not to measure it.

Pre-registered turnover, as a range: train charges 1.13x. The band's saving is
a property of the window (2026-10-19/20) and validation churn has run 68-81%
above train's, and six consecutive trials have had their pre-registration come
in as a lower bound. Predicted range 1.5-4.5x annualised.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100          # names held
BAND = 200       # a held name is kept while its score rank stays inside this
MONTHS = 120
MIN_MONTHS = 60
MIN_SCORED = 50

STRATEGY = {
    "name": "pt_decade_reversal_band_warm",
    "family": "price-trend",
    "hypothesis": (
        "Adding a 200-name retention band to the ten-year reversal -- holding the 100 "
        "eligible names with the lowest trailing ten-year mean monthly return, quota-"
        "allocated across trailing-trading-calendar peer groups, and keeping a held name "
        "while its score rank stays inside the top 200 -- raises validation skill over the "
        "equal-weight eligible pool above the unbanded version's -0.006, because a "
        "train-only decomposition of sixteen objects through the engine's own execution "
        "model shows selection is positive in six of them and the cost schedule takes all "
        "of it in every one except the lowest-turnover book, and a band preserves a "
        "mean-reverting score's selection (+0.1148 against +0.1202 unbanded) while taking "
        "the book from 2.20x to 1.13x annualised turnover."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Monthly. Equal weight over K names chosen by the ten-year reversal with a
    peer-group quota, held through a top-BAND retention band; the equal-weight
    eligible pool on dates where the score does not yet exist."""
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)

    # Monthly returns, then their trailing mean. Every value published on a
    # month label uses only returns realized at or before that label, and the
    # daily reindex forward-fills, so a decision date reads the latest label at
    # or before it. A mean of RATIOS: the store's back-adjustment factor cancels.
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)
    score = (-mret.rolling(MONTHS, min_periods=MIN_MONTHS).mean()).reindex(prices.index, method="ffill")

    month_ends = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows: dict = {}
    held: list | None = None

    for date in month_ends:
        names = prices.columns[elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()]
        if len(names) < MIN_SCORED:
            continue
        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        if len(sc) < MIN_SCORED:
            rows[date] = pd.Series(1.0 / len(names), index=names)   # pool during warm-up
            held = None
            continue

        if held is None:
            picked = peer_quota_select(sc, calendar_peers(volume, date, names), K)
        else:
            rank = sc.rank(ascending=False)
            keep = [n for n in held if n in sc.index and rank[n] <= BAND]
            need = K - len(keep)
            if need > 0:
                rest = sc.drop(index=keep, errors="ignore")
                extra = peer_quota_select(rest, calendar_peers(volume, date, names), need)
                picked = pd.Index(list(keep) + list(extra))
            else:
                picked = pd.Index(sc.reindex(keep).nlargest(K).index)

        if len(picked) < 20:
            rows[date] = pd.Series(1.0 / len(names), index=names)
            held = None
            continue
        held = list(picked)
        rows[date] = pd.Series(1.0 / len(picked), index=picked)

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
