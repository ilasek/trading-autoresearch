"""Two LINEAR SPANS of a name's own price path, each priced walk-forward.

WHY A SPAN RATHER THAN A SCORE. `experiments/learnings.md` records this lab
refuting one functional of the own price path at a time: the mean (12-1
momentum, 21-day reversal, the decade halves), the dispersion (Garman-Klass
range vol, idiosyncratic vol), the third moment (coskewness, own skewness
through the lottery object), the maximum (52-week-high proximity, MAX), the
sign count (information discreteness), the within-day location (CLV) and the
session split (overnight drift). Each closure is one direction in a space.
A walk-forward cross-sectional regression over a whole FAMILY of path
functionals prices the entire linear span at once: if the span is empty, every
remaining direction inside it is closed by one trial rather than by twenty.

This is also the open cell of `statistical-learning`'s charter question.
`learnings.md` (2026-10-17/18) answered that question -- "which feature groups
carry signal" -- with *none of them, linear or nonlinear*, but it answered it
for ONE feature group: seven characteristic features, under ridge and under
gradient boosting. Its own words name what is left: "the uncovered cell (small
neural nets) is a third estimator over the same null features." A different
FEATURE FAMILY under the same validated estimator is the other uncovered cell,
and it is the one the entry's own diagnosis ("it is the features") points at.

THE TWO FAMILIES, AND WHY THEY ARE A MATCHED PAIR ACROSS THE CATEGORY PRIOR.
`research/SUMMARY.md`'s `p0` subsection (2026-11-06) is the only non-circular
ordering instrument this lab has left: every pre-trial statistic it owns
refuses usefully and qualifies not at all (2026-11-06/07), so the literature's
per-category replication rate is what remains. The two categories reachable
from daily OHLCV sit at opposite ends of it -- Hou-Xue-Zhang replicate
**momentum at 63.2%** and **trading frictions at about 4%** (102 of 106
variables failing), which `SUMMARY.md` turns into `p0 ~ 0.25-0.55` against
`0.02-0.06`. Almost every v3 trial so far has been frictions-shaped.

So the two families below are built to be identical in every respect except
which of those two categories their features live in:

  TREND  (momentum-shaped)      f_L = log(MA_L(P) / P)  for L in 5..504 days
         Han-Zhou-Zhu's moving-average-to-price ratios: the term structure of
         a name's own trend, one feature per horizon, signs learned rather
         than assumed. Nests short-horizon reversal (L=5,21), 12-1 momentum
         (L=252) and the start of the long-horizon reversal window (L=504) in
         one object, which is exactly the reconciliation a single-horizon sort
         cannot express. Every single horizon in it has been refuted here on
         its own; the span has not.

  MICRO  (frictions-shaped)     rho_k = corr(r_t, r_{t-k}) for k in 1..6
         The term structure of a name's own return autocorrelation over a
         504-day window lagged 21 days. Unit-free by construction, so it
         carries neither the volatility level nor the back-adjustment
         contaminant of the 2026-10-18 / 2026-10-22 engine issues (a
         correlation of two returns of the same name cannot hold a
         multiplicative adjustment factor). `rho_1` nests Roll's implied
         effective spread -- the frictions axis this lab has closed on the
         Amihud LEVEL and the share-turnover TREND but never on the serial
         -correlation form -- and `rho_2..rho_6` are the slow-diffusion half,
         which no object in the v3 record touches.

THE COLUMN AXIS, AND IT IS WHY EVERY `.where(elig)` BELOW COMES BEFORE ITS
RANK. `features.xs_rank` is row-wise, so it is causal in the TIME axis and
**not** in the COLUMN axis. `protocol.visible_frame` drops columns that have
not yet been eligible, so a frame truncated by 63 days holds fewer names and
every rank in every earlier row shifts with its denominator -- the leak that
cost trial `sl_ridge_six_features` on 2026-10-07 and this file's own first run
on 2026-11-07. The fix recorded there is the one used here: **mask to the
eligible names BEFORE ranking, not after**, so a row's rank denominator is the
pool the book could actually have bought from.

Both families have exactly SIX features, both need 504 days of a name's own
history and nothing more, both are cross-sectionally ranked row-wise over the
ELIGIBLE names only, both are fitted by the same closed-form ridge
at the same monthly grid against the same cross-sectional rank of the forward
one-month return, and both are then poured into the one construction the v3
board is built on. The pair is therefore the first PAIRED test of the category
prior itself, and it is not a same-score pair (2026-11-06/07's anti-candidate):
the two feature sets share no member and no window convention.

#388's FORECAST FLOOR, and the accompaniment it demands. `research/SUMMARY.md`
`#388` is a construction default -- "floor the predicted excess return at
zero", the long-only constraint imposed on the forecast rather than on the
weight -- and it comes with a mandatory report: the fraction of dates on which
the restriction is ACTIVE. It is imposed here by setting the score to NaN
wherever the walk-forward forecast is not strictly positive, so a name the
model expects to be a below-median performer cannot be bought however high it
ranks among its peers. `active_share_of_dates` returns the diagnostic.

WHAT THIS FILE DOES NOT DO. It introduces no new construction node. The book
is `strategies/lib/third_moment.moment_book`, byte-identical to the one that
priced trials #24 and #25, because 2026-11-06/07 measured same-score pairs at
active-return rho +0.909 and ruled that trials are to be spent on scores
rather than on construction nodes. The only thing new here is the score.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

# Pre-registered and not swept. Six features per family so the two are matched
# on parameter count; 504 days of required history so they are matched on the
# price-history-length confound (`learnings.md`, 2026-10-26/27) as well.
TREND_SCALES = (5, 21, 63, 126, 252, 504)
MICRO_LAGS = (1, 2, 3, 4, 5, 6)
MICRO_WINDOW = 504
MICRO_LAG = 21
HORIZON = 21
# The engine fills a row emitted on date `d` at each name's NEXT REAL close, so
# the return a book actually earns from a decision at `d` is `P[d+1+h]/P[d+1]`
# and not `P[d+h]/P[d]`. A learner trained on the latter is trained on one day
# of return it cannot collect -- which is harmless for a 756-day score and is
# the entire quantity for a 5-day one. The target below is the tradeable one,
# and `FILL_LAG` is the protocol's own convention rather than a knob.
FILL_LAG = 1
RIDGE_ALPHA = 10.0
# ~24 monthly cross-sections before the model is allowed to speak. The train
# split opens with only one index eligible (~500 names), so 12000 rows is two
# years of monthly panels there and less than one year later on.
MIN_TRAIN_ROWS = 12000


# ---------------------------------------------------------------------------
# Feature families
# ---------------------------------------------------------------------------

def _elig_frame(prices: pd.DataFrame, eligible) -> pd.DataFrame:
    if eligible is None:
        return pd.DataFrame(True, index=prices.index, columns=prices.columns)
    return (eligible.reindex(index=prices.index, columns=prices.columns)
            .fillna(False).astype(bool))


def _masked_rank(frame: pd.DataFrame, elig: pd.DataFrame) -> pd.DataFrame:
    """Row-wise rank over the ELIGIBLE names only (see the header's column-axis
    note), centred on zero."""
    return F.xs_rank(frame.where(elig)) - 0.5


def trend_features(prices: pd.DataFrame, aux: dict | None = None,
                   eligible=None) -> dict[str, pd.DataFrame]:
    """`log(MA_L / P)` at six horizons, ranked over the eligible names."""
    elig = _elig_frame(prices, eligible)
    px = prices.ffill()
    out: dict[str, pd.DataFrame] = {}
    for L in TREND_SCALES:
        ma = px.rolling(L, min_periods=L).mean()
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.log(ma.where(ma > 0) / px.where(px > 0))
        out[f"ma{L:04d}"] = _masked_rank(ratio, elig)
    return out


def micro_features(prices: pd.DataFrame, aux: dict | None = None,
                   eligible=None) -> dict[str, pd.DataFrame]:
    """Own-return autocorrelation at lags 1-6, cross-sectionally ranked.

    Returns are masked to days the name actually PRINTED (`volume` is not
    forward-filled, so a NaN there is a closed listing market). Without the
    mask a run of forward-filled holiday zeros would put the listing calendar
    into `rho_1`, which `learnings.md` (2026-09-28) records as the panel's
    `%zero` artifact; with it, every pair `(r_t, r_{t-k})` entering the
    estimate is a pair of real prints.
    """
    elig = _elig_frame(prices, eligible)
    r = prices.pct_change(fill_method=None)
    if aux is not None and "volume" in aux:
        printed = aux["volume"].reindex(index=r.index, columns=r.columns).notna()
        r = r.where(printed)
    w, mp = MICRO_WINDOW, MICRO_WINDOW // 2
    m = r.rolling(w, min_periods=mp).mean()
    v = r.rolling(w, min_periods=mp).var(ddof=0)
    out: dict[str, pd.DataFrame] = {}
    for k in MICRO_LAGS:
        prod = (r * r.shift(k)).rolling(w, min_periods=mp).mean()
        with np.errstate(divide="ignore", invalid="ignore"):
            rho = (prod - m * m) / v.where(v > 0)
        out[f"rho{k}"] = _masked_rank(rho.shift(MICRO_LAG).clip(-1.0, 1.0), elig)
    return out


FAMILIES = {"trend": trend_features, "micro": micro_features}


# ---------------------------------------------------------------------------
# The walk-forward score, with #388's floor
# ---------------------------------------------------------------------------

def tradeable_rank_target(prices: pd.DataFrame, eligible=None, horizon: int = HORIZON,
                          fill_lag: int = FILL_LAG) -> pd.DataFrame:
    """Rank, over the ELIGIBLE names and centred on zero, of the forward return
    measured FROM THE FILL. `walkforward.rank_target` measures from the decision
    date, which includes the one close the v3 execution model gives away, and
    ranks over the frame's whole column set, which is the column-axis leak."""
    fwd = prices.shift(-(horizon + fill_lag)) / prices.shift(-fill_lag) - 1.0
    return _masked_rank(fwd, _elig_frame(prices, eligible))


def _forecast(prices: pd.DataFrame, aux: dict | None, family: str, eligible=None,
              fill_lag: int = FILL_LAG) -> pd.DataFrame:
    panels = FAMILIES[family](prices, aux, eligible)
    dates = W.rebalance_dates(prices)
    return W.walk_forward_scores(
        panels,
        tradeable_rank_target(prices, eligible, HORIZON, fill_lag),
        dates,
        HORIZON + fill_lag,
        W.ridge_fit_predict(RIDGE_ALPHA),
        min_train_rows=MIN_TRAIN_ROWS,
    )


def learned_score(family: str, floor: bool = True):
    """A `moment_book`-compatible score function for one feature family.

    Signature matches `third_moment.moment_book`'s expectation
    (`score_fn(prices, aux, eligible=, window=, sign=)`); `window` and `sign`
    are accepted and ignored, because this score's windows are the feature
    family's own and its sign is learned.
    """
    def _score(prices, aux=None, eligible=None, window=None, sign: float = 1.0):
        fc = _forecast(prices, aux, family, eligible)
        if floor:
            fc = fc.where(fc > 0.0)             # research `#388`(ii)
        return fc.reindex(index=prices.index, columns=prices.columns)
    return _score


def active_share_of_dates(prices: pd.DataFrame, aux: dict | None, family: str,
                          eligible=None, k: int = 100) -> dict:
    """`#388`'s mandatory accompaniment: how often the floor actually binds.

    A restriction that is never active is not doing any work, and a book that
    is the pool on most dates is mostly the benchmark. Reports, over the
    forecast dates, the share on which fewer than `k` names survive the floor
    and the mean count that does.
    """
    fc = _forecast(prices, aux, family, eligible)
    pos = (fc > 0.0).sum(axis=1)
    return {
        "n_dates": int(len(pos)),
        "mean_positive": round(float(pos.mean()), 1),
        "share_dates_floor_binds": round(float((pos < k).mean()), 4),
        "share_dates_empty": round(float((pos < 20).mean()), 4),
    }
