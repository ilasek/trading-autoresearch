"""The third aggregation operator: an INTERSECTION of two orthogonal scores.

WHY THIS FILE EXISTS IN A FAMILY THIS LAB CLOSED. `portfolio-learning` was closed
on 2026-09-03 on three controls, and the closure is sound for what it tested:
nine trials of *union* books, a placebo partner outscoring a content partner, a
leg measured +0.236 better standalone moving the book -0.003, and the conclusion
that "the union responds to the number of orderings it is handed, not to their
content". Every combiner this lab has ever built is an aggregation over
whole-universe rank scores, and there are exactly two it has used:

    mean   bounded between its components by construction (five vintage axes,
           the 2026-08-30 ensemble arithmetic, #67) -- closed
    max    the union of the legs' tails, escapes the mean's bound (#68/#69)
           -- and then measured inert to leg content (#71..#79) -- closed

An **intersection** is the third, and it has never been built here. The reason to
spend a trial on it is not that it is unbuilt but that **it cannot fail the way
the union failed**: a union adds an ordering, so a content-free partner can still
contribute names and the book stays alive; an intersection can only *cut* the
base book, so a content-free partner must degrade it. The operator carries its own
placebo, which is the falsification `learnings.md` asks for ("run the placebo
before building on a surprise, not after"). It was run first, and it is the
result that motivates the file rather than the headline.

PRE-TRIAL SCREEN, TRAIN SPLIT, HOLDINGS AND TRAIN RETURNS ONLY (no book run, no
holdout). Every arm holds the same ~14 names out of a joint pool averaging 97, so
breadth cannot explain any of it. Forward 21-day excess over the scoreable pool:

    momentum alone, matched size                 +6.47 %/yr  (t = +2.21)
    region-relative ILLIQ alone, matched size    +5.76 %/yr  (t = +3.33)
    INTERSECTION (both legs)                     +7.55 %/yr  (t = +3.68)
    placebo x momentum                           -0.96 %/yr  (t = -0.47)
    placebo x region-relative ILLIQ              +0.92 %/yr  (t = +0.58)
    union of the two top-k tails                 +4.21 %/yr  (t = +2.67)

The placebo is a hash of (rebalance date, ticker) and reads no market data. Both
placebo arms collapse to a null while the intersection beats both its legs, which
is the prediction stated above and the one the union machinery failed. Note the
union arm scoring *below* both its legs at a larger book, consistent with the
2026-08-30 aggregation bound.

Mean cross-sectional `spearman(momentum, region-ILLIQ) = -0.0120`. These two
scores are as close to orthogonal as anything measured in this repo, which is why
their intersection is a different set of names rather than a re-ranking.

WHY THESE TWO LEGS, AND IT IS TONIGHT'S OTHER FREE RESULT. `SUMMARY.md` #83's
monotonicity test was run on the train split before this file (J = 5 fixed in
advance, all-pairs variant, studentized stationary bootstrap resampling the shared
date index, geometric blocks of mean 10 months, B = 1000):

    score                       bin means (%/yr, demeaned)          MR p    Up (p)        Down (p)
    champion 4-horizon mom      +8.02 -0.78 -2.82 -3.96 -0.45       0.698   17.16 (0.002)  2.46 (0.58)
    region-relative ILLIQ       +8.56 +1.00 -2.36 -2.78 -4.41       0.004   24.26 (0.000)  0.00 (0.99)
    same-minus-other month      +6.70 +0.97 -0.95 -3.59 -3.15       0.035   21.04 (0.000)  0.18 (0.97)
    21d reversal                +2.34 -0.18 -0.87 -2.96 +1.67       0.931    7.28 (0.14)   3.84 (0.37)
    Garman-Klass 21d vol level  +5.58 +1.78 +1.59 -1.26 -7.68       0.004   25.57 (0.000)  0.00 (0.99)

The champion's score **is not a ranking of expected return** -- MR does not come
close to rejecting -- while its top bin is +8.02%/yr at t = +3.76. It is a
picker of one corner, which is #83's outcome (b) exactly. The region-relative
`ILLIQ` score is the one perfectly monotone object on the board (Down = 0.00).
So the two legs pay in structurally different ways, and the operator that suits a
corner-picker crossed with a monotone ranking is an intersection: take the corner
the first one identifies, and keep only the part of it the second one ranks high.

The last row is the control that stops any of this being over-read: the **most**
monotone score in the repo is 21-day Garman-Klass volatility, which five sessions
of screens have identified as this universe's survivorship artifact. Monotonicity
is not evidence of content, and no claim below rests on it.

BAND CHOICE, ON A STATED GROUND RATHER THAN ON THE PEAK. Six symmetric bands were
profiled holdings-only. `cover` is train month-ends with a joint pool wide enough
to score, which a band width silently changes (2026-09-04):

    core/band   names    HHI    churn/yr  cover  vol pct   excess %/yr      t
    20/30        7.0   0.2115     7.03     258   0.631      +12.30      +3.72
    25/38       11.5   0.1082     4.83     258    0.593      +9.36      +3.82
    30/45       13.9   0.0812     4.33     225    0.587     +10.46      +4.67   <- this file
    35/52       18.8   0.0596     3.75     224    0.570      +8.04      +4.19
    40/60       24.0   0.0460     3.19     212    0.559      +6.18      +3.69
    50/75       32.1   0.0316     2.73     168    0.540      +5.29      +3.58

30/45 is chosen because each leg then keeps roughly its **top third** of the joint
pool -- the smallest symmetric band that contains momentum's single paying bin
(the top quintile) with margin -- and because it lands the book at ~14 names,
the size at which the screen above was run and passed its placebo. It is also the
peak of the `t` column, and I am disclosing that rather than resting on it: the
excess column is not monotone (10.46 sits above 9.36 at a wider band), so the
column is noisy and no band here is resolvable against its neighbour.

Two controls on the book itself. It sits at the **0.587 percentile of pool
volatility** -- above the median, so this is not the closed low-vol tilt arriving
unlabelled. And churn is 4.33x a year against the ILLIQ leg's 0.93x and the
champion's 3.11x, so the standing turnover confound runs **against** this
candidate, not for it: it pays ~0.65%/yr of cost drag that the leg it must beat
does not.

KNOWN LIMITS, STATED BEFORE THE RESULT. The joint pool needs 45 scoreable names
across both legs, and the momentum leg needs 252+21 days of history while the
region operator drops regions with fewer than 4 members, so only **225 of 666
train month-ends** are scoreable and the first is in the mid-1990s. Train Sharpe
is therefore measured on a very different sample from the champion's and is
**inadmissible to the train-as-prediction record**, per the 2026-09-04 finding
that a band change silently changes the train sample. Validation is unaffected
(the pool is full there), which is why the screen is quoted on train and the
verdict will be read on validation.

PRE-REGISTERED POINT ESTIMATE: **1.00**, against the seated `portfolio-learning`
lead's 1.008 and the ILLIQ leg's 0.942. The falsifying branches, named in advance:

  - **>= 1.12** (the champion's validation Sharpe): the intersection beats both
    legs and every non-`price-trend` result on record, and a genuinely different
    construction becomes worth a challenge. I do not expect this.
  - **1.008 to 1.12**: the operator is real and takes the family lead, but the
    margin over the max operator sits inside the resolution floor and must be
    quoted as a range, not a point (2026-08-31).
  - **0.942 to 1.008**: the intersection lands between its legs and does not beat
    the max operator. The operator is not inert to content -- the placebo already
    established that -- but it buys nothing the union did not.
  - **< 0.942**: the intersection does not beat its own better leg, so the
    concentration cost of a 14-name book eats the joint-tail gain, and the
    intersection joins mean and max as an operator with no headroom on this
    universe. This is the branch that closes `portfolio-learning` for good, on
    all three operators rather than on two.

SCOUT. It does not compete for the seat and cannot reach the holdout, which is
the right track for establishing an operator rather than cashing one.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import groups as G
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "pl_signal_intersection",
    "family": "portfolio-learning",
    "track": "scout",
    "hypothesis": (
        "An intersection of the champion's four-horizon momentum score with the seated "
        "`liquidity-volume` lead's region-relative Amihud ILLIQ score -- each leg keeping its "
        "top third of the joint pool, the overlap held with the family's usual 1.5x buffer -- "
        "scores near 1.00 on validation, above the ILLIQ leg's 0.942 and near the seated "
        "`portfolio-learning` lead's 1.008, because the two scores are cross-sectionally "
        "orthogonal (mean spearman -0.0120) and pay in structurally different ways: "
        "`SUMMARY.md` #83's monotonic-relation test does not reject for momentum (p = 0.698, "
        "Up = 17.16 at p = 0.002), so it picks one corner rather than ranking expected return, "
        "while it rejects for region-relative ILLIQ (p = 0.004, Down = 0.00 exactly), the one "
        "perfectly monotone score in the repo. At a book size matched at ~14 names the "
        "intersection carries +7.55%/yr of train tail excess (t = +3.68) against +6.47 for "
        "momentum alone and +5.76 for ILLIQ alone, while the union of the same two tails "
        "carries only +4.21. Unlike the union operator this lab closed on nine trials, an "
        "intersection cannot be inert to leg content -- a content-free partner can only cut "
        "the base book -- and the built-in placebo confirms it: intersecting either leg with a "
        "hash of (rebalance date, ticker) that reads no market data collapses to -0.96%/yr "
        "(t = -0.47) and +0.92%/yr (t = +0.58). The candidate pays 4.33x annual churn against "
        "the ILLIQ leg's 0.93x, so the standing turnover confound runs against it, and it sits "
        "at the 0.587 percentile of pool volatility, so it is not the closed low-vol tilt in "
        "disguise. Below 0.942 the operator fails to beat its own better leg and "
        "`portfolio-learning` closes on all three aggregation operators rather than two."
    ),
}

MOM_LOOKBACKS = (252, 189, 126, 63)   # the champion's four horizons
SKIP = 21                             # the standard skip-month
ILLIQ_WINDOW = 63                     # one quarter, as the seated liquidity-volume lead
CORE_N = 30                           # each leg's core: ~top third of the joint pool
BAND_N = 45                           # the family's standing 1.5x buffer ratio
WARMUP = 6
MIN_REGION = 4                        # a region below this cannot supply a peer mean


def _region_relative(score: pd.Series) -> pd.Series:
    """Each name's score minus the mean score of its own region, dropping names
    whose region has fewer than `MIN_REGION` instruments scoreable on that date.

    `groups.REGION_OF` is static instrument metadata read from `data/universe.yaml`
    -- no dates, no prices, nothing estimated from returns -- so this reads only
    the cross-section it is handed. Identical to the seated lead's helper.
    """
    labels = pd.Series({name: G.REGION_OF.get(name) for name in score.index})
    grouped = score.groupby(labels)
    demeaned = score - grouped.transform("mean")
    return demeaned.where(grouped.transform("size") >= MIN_REGION).dropna()


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    # Leg 1: the champion's score -- equal average of four cross-sectionally
    # z-scored trailing returns, each ending at the skip-month. Row-wise, so
    # computing it over the whole visible frame is identical to computing it
    # date by date and reads nothing a given row could not see.
    legs = [F.xs_zscore(F.trailing_return(prices, lb, skip=SKIP)) for lb in MOM_LOOKBACKS]
    momentum = sum(legs) / float(len(legs))

    # Leg 2: the seated liquidity-volume lead's score, region-demeaned per date.
    illiq = F.amihud_illiquidity(prices, aux["dollar_volume"], ILLIQ_WINDOW)

    rows: dict[pd.Timestamp, pd.Series] = {}
    held: set[str] = set()

    for dt in W.rebalance_dates(prices, warmup=WARMUP):
        mom = momentum.loc[dt].dropna()
        liq = _region_relative(illiq.loc[:dt].iloc[-1].dropna())
        pool = mom.index.intersection(liq.index)
        if len(pool) < BAND_N:
            continue
        mom_rank = mom.reindex(pool).sort_values(ascending=False).index
        liq_rank = liq.reindex(pool).sort_values(ascending=False).index

        core = set(mom_rank[:CORE_N]) & set(liq_rank[:CORE_N])
        band = set(mom_rank[:BAND_N]) & set(liq_rank[:BAND_N])
        held = (held & band) | core
        if len(held) < 4:
            # Both legs must agree on at least four names for the book to be an
            # intersection at all; on a date where they do not, hold the core
            # alone rather than falling back to a single leg's ranking.
            held = set(core)
            if len(held) < 4:
                continue

        names = sorted(held)
        rows[dt] = pd.Series(1.0 / len(names), index=names)

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
