"""Does the overnight component of a return carry a long-horizon reversal this
long-only, close-to-close lab can actually hold?

WHERE THIS COMES FROM. `research/SUMMARY.md` #119-#122 (2026-09-18) opened the
one column of the data panel this lab had used for nineteen days without a note
on it: a daily close-to-close return factors exactly into a close->open
(overnight) and an open->close (intraday) leg. Most of that literature is
unreachable here, and the folder says so plainly — Lou-Polk-Skouras's own advice
to a long-horizon investor is ORDER TIMING (trade at the open or at the close
depending on where your premium accrues), and this engine cannot choose an
execution time. It holds close-to-close and therefore collects the sum, which is
the thing that already nets.

What survives the constraint is one paper and one horizon:
Aboody-Even-Tov-Lehavy-Trueman read the overnight return as a firm-specific
SENTIMENT proxy, and document long-horizon reversal measured on close-to-close
buy-and-hold over a twelve-month holding period. Persistent attention-driven
demand lifts a name overnight; the non-informational part unwinds over the
following year. So the LOW-overnight end is the cheap side, and the cheap side
is the side long-only can hold. Three properties make it reachable where the
rest of the vein is not: the holding period is close-to-close, the long leg
carries the effect on its own, and the long leg loads negatively on momentum.

WHAT THE FREE SCREENS ESTABLISHED BEFORE THIS FILE WAS WRITTEN. All on train,
all in tonight's journal entry with the full search path, because the
vol-neutralisation below was adopted AFTER the unconditional version failed its
own identifying test and that must not be hidden.

  (a) Not trend in costume. Mean spearman(score, 12-1 momentum) = -0.024 — the
      pre-registered kill line was +0.30. Against 21-day reversal it is +0.384,
      well under the 0.98 this repo uses as an identity line, so it is a
      different object from the reversal book already on the board.
  (b) The horizon matters and the source predicts that it should. At a forward
      21 days the HIGH-overnight end earns (continuation); at forward 6 and 12
      months the ranking inverts and the low end earns. The sign flip across
      horizons is the source's own signature, and it is why this book holds for
      twelve months rather than one.
  (c) The identifying test FAILS unconditionally. At the book's own 12-month
      horizon the top band earns +3.96%/yr (t = +3.67) but the bottom band earns
      +8.28%/yr (t = +5.75) — both ends positive, the "short" leg stronger, which
      is the opposite of the source's claim that the long leg carries the effect
      alone. A U-shape in a signed sort is a DISPERSION object.
  (d) And the dispersion object is this universe's identified survivorship
      artifact. spearman(mean |overnight|, 252d realized vol) = +0.706, and the
      plain |overnight| sort's own top-10 earns +9.75%/yr (t = +5.87), larger
      than anything the signed score produces. This is the same cause that has
      closed `range-variance` on fifteen screened mechanisms.
  (e) Inside a single trailing-volatility tercile — the control that family has
      failed ten times — the source's sign returns on BOTH sides in the low and
      mid terciles (low-overnight +0.59, +1.24; high-overnight -0.37, -1.47) and
      only the high-vol tercile keeps the U-shape (+3.66, +6.24). So the signed
      effect is real and small; the U-shape is the artifact sitting on top of it.

HENCE THE ONE DEVIATION FROM THE SOURCE, AND IT IS MEASUREMENT HYGIENE RATHER
THAN A FREE PARAMETER. The score is ranked WITHIN trailing-volatility terciles
and the picks are pooled. `learnings.md`'s standing rule is to ask whether the
thing being removed is a unit or a return: the trailing volatility LEVEL is
neither — it is the documented artifact of a current-constituents universe, in
which the high-volatility names are the survivors (+19.4%/yr high-minus-low vol
spread on train). Removing it is the same move that earned region-relative
`ILLIQ` its seat. The resulting book sits at a volatility percentile of 0.526
against the pool's ~0.51, i.e. it is neutral by construction rather than by luck,
which matters because an excess screen prices a numerator and is blind to a
denominator.

WHY THE BREADTH IS WHAT IT IS, AND IT IS NOT A CHOICE. A twelve-month hold with
monthly formation IS twelve overlapping tranches; that is arithmetic, not a
preference. Measured before this file was written, the book's distinct-name count
runs 28.8 / 49.1 / 65.0 / 78.8 at 1 / 2 / 3 / 4 names per tercile per tranche.
The score's marginal slices go flat after about rank 10 of a ~118-name pool, so
every one of those is past its indicated depth and ONE PER TERCILE IS THE
TIGHTEST THE CONSTRUCTION ALLOWS. It is taken for that reason and not because it
scored best. The folder's preference for overlapping tranches over the source's
December-only rule is honoured — December-only inherits a tax-loss-selling and
turn-of-year confound the paper never disentangles — and the folder's own caveat
is repeated: the overlapping version is UNTESTED IN THE SOURCE.

WHY IT IS A SCOUT AND NOT A CHALLENGER. Not one excess on any screen reaches
|t| = 2 (the book's own train excess over an equal-weight benchmark on the same
grid is +1.99%/yr at t = +1.20). By this file's own solved break-even table
nothing on the blend board is within a third of a standard error of the seat, and
a leg would need its own Sharpe at 1.34-1.42 to make a blend resolvable. This is
a family reading, not a bid for the seat.

WHAT WOULD FALSIFY IT. The folder's discount is explicit and is pre-registered
rather than discovered: the effect is strongest in small, young, unprofitable,
high-volatility names and is insignificant in four of five easiest-to-value
subsamples, and this universe is 140 large, current, surviving names at the easy
end. A STRONG READING HERE IS GROUNDS FOR SUSPICION, NOT CELEBRATION.

Every other node is the house default (`learnings.md` 2026-09-10): last trading
day of each month, all 140 instruments holdable, equal weight within the book, no
group demeaning, and the band set from the score's own profile rather than
inherited.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib import features as F
from strategies.lib import walkforward as W

STRATEGY = {
    "name": "lv_overnight_sentiment_reversal",
    "family": "liquidity-volume",
    "hypothesis": (
        "A long-only book holding the lowest average daily overnight return of the "
        "trailing month, ranked within trailing-volatility terciles so the "
        "survivorship-inflated volatility level is differenced out, held twelve "
        "months as twelve overlapping monthly tranches, beats the 0.49 equal-weight "
        "floor on validation — because the overnight leg carries firm-specific "
        "sentiment whose non-informational part unwinds over the following year, "
        "which is a mechanism orthogonal to the incumbent's trend family "
        "(measured spearman to 12-1 momentum: -0.024)."
    ),
    "track": "scout",
}

FORM = 21          # formation window, in rows of the price calendar
MIN_OBS = 15       # valid overnight observations required inside that window
VOL_WINDOW = 252   # trailing window for the volatility terciles
HOLD = 12          # tranches held, i.e. a twelve-month holding period
PER_TERCILE = 1    # names per volatility tercile per tranche -> 3 per tranche
MIN_POOL = 60      # a date below this cannot support three populated terciles
WARMUP = 6


def _overnight(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    """Average daily overnight return over the trailing `FORM` rows, sign-flipped
    so that a LARGE score means a LOW overnight return, i.e. a held name.

    The decomposition is the imputed one the folder requires, never the direct
    `open_t / close_{t-1}` ratio, which breaks on ex-dates and on any
    adjustment-convention mismatch: the intraday leg is `close/open - 1` from
    same-day prices, and the overnight leg is backed out of the adjusted
    close-to-close return, so the identity `(1+night)(1+day) = 1+r_cc` holds by
    construction. Days the instrument did not trade are masked with the
    non-forward-filled volume panel, per the same rider.

    `min_periods` is set explicitly. Left at its default, `rolling(FORM).mean()`
    requires all `FORM` observations and silently restricts the score to names
    with a complete trading calendar — the `dropna`-cohort artifact that cost
    this repo four trials on the champion's trim. Caught here by a coverage
    check before any number was believed; it moved the scoreable train dates
    from 76 to 226.
    """
    op, vol = aux["open"], aux["volume"]
    traded = vol.notna() & prices.notna() & op.notna()
    r_cc = prices.pct_change(fill_method=None)
    r_day = (prices / op - 1.0).where(traded)
    r_night = ((1.0 + r_cc) / (1.0 + r_day) - 1.0).where(traded & traded.shift(1))
    count = r_night.notna().rolling(FORM).sum()
    avg = r_night.rolling(FORM, min_periods=MIN_OBS).mean()
    return (-avg).where(count >= MIN_OBS)


def _tranche(score_row: pd.Series, vol_row: pd.Series) -> pd.Series | None:
    """One formation date's target: the top `PER_TERCILE` of each trailing-volatility
    tercile of the scoreable pool, equal-weighted. Returns None when the date
    cannot support three populated terciles."""
    names = score_row.dropna().index.intersection(vol_row.dropna().index)
    if len(names) < MIN_POOL:
        return None
    s, v = score_row[names], vol_row[names]
    # `rank(method="first")` before `qcut` so ties break deterministically on a
    # stable column order; the causality check compares holdings at 1e-6 and
    # reads any non-determinism as a peek.
    tercile = pd.qcut(v.rank(method="first"), 3, labels=False)
    picks: list[str] = []
    for t in range(3):
        cell = names[tercile.values == t]
        if len(cell) < 2 * PER_TERCILE:
            return None
        picks += list(s[cell].nlargest(PER_TERCILE).index)
    return pd.Series(1.0 / len(picks), index=picks)


def generate_weights(prices: pd.DataFrame, aux: dict) -> pd.DataFrame:
    score = _overnight(prices, aux)
    vol252 = F.realized_vol(prices, VOL_WINDOW)

    dates = [d for d in W.rebalance_dates(prices, warmup=WARMUP) if d in score.index]
    tranches: dict[pd.Timestamp, pd.Series] = {}
    for d in dates:
        t = _tranche(score.loc[d], vol252.loc[d])
        if t is not None:
            tranches[d] = t

    rows: dict[pd.Timestamp, pd.Series] = {}
    for i, d in enumerate(dates):
        window = [e for e in dates[max(0, i - HOLD + 1): i + 1] if e in tranches]
        if len(window) < HOLD:
            continue          # never hold a partially-formed book
        acc = pd.Series(0.0, index=prices.columns)
        for e in window:
            t = tranches[e]
            acc[t.index] += t.values / HOLD
        total = acc.sum()
        if total > 0:
            rows[d] = acc / total

    if not rows:
        return pd.DataFrame(columns=prices.columns, dtype=float)
    return pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
