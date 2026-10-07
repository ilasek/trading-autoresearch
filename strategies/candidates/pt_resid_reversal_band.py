"""The extreme tail of the reversal sort is where the RISK is, not the SIGNAL.

WHAT TRIAL #1 ESTABLISHED. `pt_resid_reversal_v2` (top 30 of the 21-day
market-residual sort, equal weight, monthly) scored validation **0.54 at the 98th
percentile of its own random-selection null** (null median +0.30, 90% +0.44;
equal-weight eligible pool +0.51, IR vs pool +0.41) and was then **killed by the
drawdown gate at -54.1% against -45%**. So the mechanism has content on the
point-in-time panel and the book, not the score, is what failed. The pre-registered
expectation for that trial was a coin flip on the null gate and it cleared it by
eight percentiles; nothing in this file revisits the score's existence.

WHAT THE FOLLOW-UP SCREENS SAID (train split only, gross of costs, monthly grid --
a risk-shape diagnostic, deliberately not comparable to an engine Sharpe; journal
F5-F7). Slices of the same sort, excess over the equal-weight eligible pool on the
same grid:

    slice                            excess (bps/mo)    t      sd    train mdd
    top 30      (= trial #1)             +14.0       +0.61    747    -84.0%
    top 60                               +26.4       +1.74    638    -77.1%
    top 100                              +22.0       +1.96    588    -73.2%
    ranks  31-90                         +28.1       +2.82    544    -68.3%
    ranks  31-120                        +27.0       +3.28    525    -65.1%
    ranks  31-180                        +16.1       +2.45    498    -62.1%
    ranks  61-180                        +10.0       +1.47    490    -61.1%
    equal-weight pool (reference)          --          --     485    -64.8%

**Dropping the 30 most extreme losers DOUBLES the excess and halves the gap to the
pool's own risk.** That is the opposite of what `learnings.md` [2026-08-30] records
for this mechanism under v1 -- "the book buys the extreme tail, not the quintile
mean" -- and it is the reason this file exists rather than a wider top-N. The
reading that fits all seven rows: the extreme tail of a 21-day loser sort mixes
price pressure, which mean-reverts, with information, which does not, and on a
point-in-time panel the informational share of that tail is large enough to pay for
the pressure. Brown-Keim-Kleidon's first a-priori objection to tax-loss selling
(`research/notes/2026-10-07-tax-year-end-alignment-and-the-australian-test.md`) is
the same argument from the literature's side: realization is not a demand shift
unless the name is genuinely hard to substitute, and buyers who can tell a forced
seller from bad news will not pay the pressure price.

TWO DE-RISKERS THAT TURNED OUT TO BE SUBSTITUTES, NOT COMPLEMENTS, AND THE COMBINATION
IS RECORDED AS A KILL. F4 found reversal stronger in LOW idiosyncratic volatility
(+0.0322, t = +3.27) than in high (+0.0243, t = +2.45), which looked like a second,
independent way to cut the drawdown. Combining the two destroys the signal: ranks
31-90 within the low-idio-vol half is +12.7 (t = +1.21) and within the low-idio-vol
third is **+0.5 (t = +0.04)**, against +28.1 for the band alone. The extreme-loser
tail IS largely the high-idio-vol population, so the band already does the vol
de-risking, and doing both removes the names that carry the effect. Only the band is
used here.

WHY THE BAND IS 31-120 AND NOT THE BEST CELL. The selection rule was fixed before
F7 was read: take the narrowest band whose train drawdown is near the pool's own
floor, not the highest-excess cell. The floor is real and is the main thing F7
measured -- **no band width gets materially below the equal-weight pool's -64.8%**,
so the drawdown that killed trial #1 is market beta plus an extreme-tail premium,
and only the second part is removable. 31-120 is the narrowest band at that floor
(-65.1%), it has the steadiest excess of the seven slices (t = +3.28 against +2.82
for 31-90), and the same band is used by this trial's `statistical-arbitrage`
partner so the pair stays a one-variable comparison.

FALSIFIER. Trial #1's validation drawdown was 0.69x its train drawdown. At that
ratio this book lands near -45% and the gate is a coin flip again; the claim being
tested is that the -54.1% was an extreme-tail effect rather than the pool's beta, so
a validation drawdown that does NOT improve materially on -54.1% falsifies the whole
reading above, whatever the Sharpe does. Conversely a drawdown near the pool's with
the null percentile held near trial #1's would say the tail was pure cost.
"""

from __future__ import annotations

import pandas as pd

STRATEGY = {
    "name": "pt_resid_reversal_band",
    "family": "price-trend",
    "track": "scout",
    "hypothesis": (
        "Dropping the 30 most extreme losers from the 21-day market-residual "
        "reversal sort and holding ranks 31-120 equal-weight monthly clears "
        "the -45% validation drawdown gate that killed the top-30 book at "
        "-54.1% while keeping its selection content, because on the train "
        "split the same slice earns +27.0 bps/month over the equal-weight "
        "eligible pool at t = +3.28 against the top-30's +14.0 at t = +0.61 "
        "and carries a -65.1% drawdown against its -84.0%, i.e. the extreme "
        "tail of a loser sort is where the risk is and not where the signal "
        "is; a validation drawdown that fails to improve materially on -54.1% "
        "falsifies that reading and says the drawdown is the pool's beta "
        "rather than the tail's."
    ),
}

HORIZON = 21
BAND_LO = 30       # names 1..30 of the sort are dropped
BAND_HI = 120      # ... and 31..120 are held
MIN_NAMES = 150


def generate_weights(prices: pd.DataFrame, aux: dict, eligible: pd.DataFrame = None) -> pd.DataFrame:
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    if eligible is None:
        eligible = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    elig = eligible.reindex(index=prices.index, columns=prices.columns).fillna(False)

    horizon_return = prices / prices.shift(HORIZON) - 1.0

    rows = {}
    for dt in rebalance_dates:
        if dt not in horizon_return.index:
            continue
        r = horizon_return.loc[dt]
        ok = elig.loc[dt].to_numpy() & r.notna().to_numpy()
        if ok.sum() < MIN_NAMES:
            continue
        r = r[ok]
        score = -(r - r.mean())          # revert the move against the eligible pool
        ranked = score.nlargest(min(BAND_HI, len(score))).index
        picked = ranked[BAND_LO:]
        if len(picked) == 0:
            continue
        w = pd.Series(0.0, index=prices.columns)
        w[picked] = 1.0 / len(picked)
        rows[dt] = w

    if not rows:
        return pd.DataFrame(0.0, index=prices.index[:1], columns=prices.columns)
    return pd.DataFrame(rows).T.sort_index()
