"""The other concentration channel, at bit-identical membership.

WHY THIS FILE EXISTS. Trial #80 (`lv_illiq_region_tail10`) concentrated the
seated `liquidity-volume` lead by **cutting breadth** — 25.2 -> 12.4 names,
HHI +103% — and lost 0.043 of validation Sharpe. That is the family's first
measured concentration price, and it is confounded in a way `price-trend`'s
equivalent measurements are not: #52/#53/#54 concentrated by **re-weighting at
fixed membership**, which is a different channel. This file measures the second
one, and it is the last unexamined inherited choice in this family's
construction.

WHAT IS INHERITED AND NEVER MEASURED. Every non-`price-trend` book in this repo
is **equal-weighted**, across roughly twenty-five trials, adopted by the first
scout and copied since. In `price-trend` that same choice is worth a great deal:
on the four-horizon base, equal 1.023 / rank 1.123 / magnitude 1.229 (#52, #54),
i.e. **+0.100 for ordering alone and +0.206 for ordering plus spacing**.
`CLAUDE.md` forbids carrying that number into a new family by analogy and
requires re-measuring it or saying it has not been measured. This is the
re-measurement.

WHY RANK AND NOT MAGNITUDE. A magnitude transform on a region-demeaned log ratio
needs an additive floor to keep weights positive, and `learnings.md` (2026-09-01)
makes it a standing rule that a normalisation an aggregation rule *requires* is a
free parameter controlling concentration in disguise — prefer the rule that needs
none. A linear rank weight over the held set needs none and is **invariant to
every strictly monotone transform of the score**, which matters here because the
score's units (log dollars of price impact) have no natural scale. It also splits
the question the way the mechanism argument does: rank weighting keeps the
score's **ordering** exactly and discards its **spacing** entirely.

THE MECHANISM ARGUMENT, AND IT PREDICTS THE OPPOSITE SIGN TO `price-trend`.
Tonight's free decomposition measured what this score's cardinal spacing is made
of. Writing `log ILLIQ ~ log|r| - log(dv)` and demeaning each half separately
against region, on train against the forward 21-day return:

    ILLIQ unconditional            top-20 +3.67 %/yr (t=+3.30)   IC +0.0184
    ILLIQ region-demeaned (both)          +4.31     (t=+4.29)       +0.0332
    ILLIQ denominator-demeaned only       +4.19     (t=+4.06)       +0.0301
    ILLIQ numerator-demeaned only         +3.23     (t=+3.08)       +0.0228
    -log ADV (size) alone                 +1.94     (t=+1.88)       +0.0097
    log|r| alone                          +8.53     (t=+3.62)       +0.0377

So the spacing of this score is set by a size ranking this family has measured as
a **null** four separate times and by a volatility level that is this universe's
**survivorship artifact** (+8.46%/yr for a top-20 highest-vol book on train,
which is the single cause behind `range-variance`'s eleven closed mechanisms).
Neither is a forecast of return, so the spacing should carry nothing even if the
ordering does — the opposite of `price-trend`, where the score *is* a direct
estimate of expected continuation and its spacing was measured to carry ~0.116 of
Sharpe on its own.

HOLDINGS-ONLY PROFILE, MATCHED BEFORE THIS FILE WAS WRITTEN. Membership is
bit-identical to the seated lead — same band, same ranking, same dates — so this
isolates the weighting channel exactly, which is the design #52/#53/#54 used:

    weighting    names    HHI               top weight   annual L1 churn
    equal        25.23    0.0398 (  +0.0%)     0.040          0.58x
    rank         25.23    0.0521 ( +30.8%)     0.077          1.43x
    magnitude    25.23    0.0623 ( +56.4%)     0.117          1.50x

    weight overlap, equal vs rank: 0.760
    vol percentile within pool 0.515 -> 0.529 ; log-ADV percentile 0.287 -> 0.216

Two things that follow. The +30.8% of HHI is almost exactly the 30% unit
`learnings.md` quotes its de-concentration constant in, so the transfer test is
unusually direct. And the extra churn is 0.85x of annual turnover — **0.13%/yr**
at 15 bps a side, ~0.013 of Sharpe — so the standing confound in which a 5-10x
turnover difference swamps a non-`price-trend` mechanism is two orders of
magnitude away from biting. The book also stays at its pool's median volatility
(0.515 -> 0.529), so re-weighting is not buying the survivorship artifact either.

PRE-REGISTERED POINT ESTIMATE: **0.94**, against the seated lead's 0.917. Rank
weighting moves roughly 1.8x equal weight onto the top decile of the held set,
whose train excess is +7.09%/yr against the held set's +4.31%/yr, which is worth
about +0.7%/yr of book return, ~+0.037 of Sharpe at this book's volatility,
before the standing discount that a cross-sectional screen over-predicts the book
it motivates, and net of 0.013 of extra cost.

**Stated plainly, because it decides how the result may be read: +0.02 is inside
this family's resolution floor and the trial is NOT powered against it.** At a
weight overlap of 0.760 the paired SE is roughly 0.11 by `SE = 0.568*sqrt(1-rho)`.
What the trial *is* powered against is the hypothesis that actually matters —
that the `price-trend` weighting channel transfers at `price-trend` size. A
+0.100 (rank) or +0.206 (magnitude) effect would be one to two SEs and visible;
a result near 0.917 rules that out and answers `CLAUDE.md`'s re-measurement
instruction with a measurement rather than a disclaimer. Read the sign, never the
level.

SECOND PRE-REGISTRATION, per the standing instruction that every scout record its
train Sharpe as a prediction of its validation Sharpe. n = 25 outside
`price-trend`. Last night's exact reading (0.917 -> 0.917) was hypothesised to
belong to the seated lead being a plain single sort rather than a union book;
trial #80 refuted that prospectively by over-predicting 1.13 -> 0.874 as a plain
single sort. This is the third plain single sort in the set.

SCOUT. It does not compete for the seat and cannot reach the holdout.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_illiq_region_rankweight",
    "family": "liquidity-volume",
    "track": "scout",
    "hypothesis": (
        "Weighting the seated family lead's held set by linear rank of its "
        "region-relative Amihud ILLIQ score instead of equally — membership, band, "
        "window, grid and pool bit-identical to `lv_illiq_region_relative`, so only the "
        "weighting channel moves (25.23 names either way, HHI 0.0398 -> 0.0521, +30.8%, "
        "weight overlap 0.760, annual L1 churn 0.58x -> 1.43x worth 0.13%/yr) — scores "
        "near 0.94 on validation against that lead's 0.917, and in particular does NOT "
        "reproduce the +0.100 that the identical ordering-only re-weighting is worth in "
        "`price-trend` (#54: equal 1.023 / rank 1.123 / magnitude 1.229). The reason is "
        "that this score's cardinal content is a size ranking measured as a null four "
        "times in this family (log ADV alone, top-20 +1.94%/yr, t = +1.88) divided into a "
        "volatility level that is this universe's survivorship artifact (log|r| alone, "
        "+8.53%/yr, t = +3.62), neither of which is a forecast of return, whereas a "
        "momentum composite's spacing is a direct estimate of expected continuation worth "
        "a measured ~0.116. Trial #80 has already shown the breadth-cutting concentration "
        "channel costs -0.043 here; this isolates the re-weighting channel at fixed "
        "membership, which is the channel `price-trend`'s constant was measured on. A "
        "result near 0.917 says the within-leg weighting axis is dead in this family and "
        "that the inherited equal weight was the right default; a result near 1.02 says "
        "the `price-trend` constant transfers and every non-`price-trend` book in this "
        "repo has been leaving that much on the table for twenty-five trials."
    ),
}

ILLIQ_WINDOW = 63     # one quarter, as the seated lead
CORE_N = 20           # band bit-identical to the seated lead
BAND_N = 30
WARMUP = 6
MIN_REGION = 4        # a region below this cannot supply a peer mean


def _region_relative(score: pd.Series) -> pd.Series:
    """Each name's score minus the mean score of its own region, dropping names
    whose region has fewer than `MIN_REGION` instruments scoreable on that date.

    `groups.REGION_OF` is static instrument metadata read from `data/universe.yaml`
    — no dates, no prices, nothing estimated from returns — so this reads only
    the cross-section it is handed. Identical to the seated lead's helper.
    """
    labels = pd.Series({name: G.REGION_OF.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= MIN_REGION).dropna()


def _rank_weights(score: pd.Series, names: list[str]) -> pd.Series:
    """Linear rank weight over the held set: the best-scoring held name gets
    `k` units, the worst gets 1, normalised to sum to one.

    Invariant to any strictly monotone transform of `score` — the whole reason
    this is preferred to a magnitude transform, which would need an additive
    floor that is a concentration parameter in disguise. `method="first"` keeps
    it deterministic under exact ties (the causality check compares holdings at
    1e-6, and a tie broken differently on two runs reads as a peek).
    """
    k = len(names)
    order = score.reindex(names).rank(ascending=False, method="first")
    units = (k + 1.0) - order
    return units / units.sum()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)
    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        score = _region_relative(illiq.loc[:dt].iloc[-1].dropna())
        if len(score) < BAND_N:
            continue
        ranked = score.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core
        names = sorted(held)
        rows[dt] = _rank_weights(ranked, names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
