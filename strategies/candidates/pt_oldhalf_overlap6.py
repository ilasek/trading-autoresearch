"""A third selection rule: the old-half reversal held in six overlapping sleeves.

THE CLAIM IN ONE LINE. `learnings.md` (2026-10-25/26) measures the binding
constraint on this panel as TURNOVER rather than selection, and (2026-10-26/27)
records that the lab owns exactly two selection rules -- hard top-K, which is
expensive, and banded top-K, which a paired validation trial refused -- so that
"the search for a positive-selection score that is naturally cheap to hold has
no target". This candidate does not look for another score. It adds the third
rule: the family lead's own score and own top-100 pick, held in six overlapping
monthly sleeves, one reformed each month and carried six months as shares. The
emitted row is the drifted book plus the reformed sixth, so only that sixth
trades.

WHY IT SHOULD WORK, AND WHY THE ARGUMENT IS NOT A TRAIN SCREEN. `corr(train
skill, validation skill)` over fifteen v3 trials is -0.074, so no train
*selection* number is evidence here and none is offered as such. The claim rests
on two things a train run can establish without claiming transfer:

  (i) the score cannot notice the delay. It is a 60-month mean of monthly
      returns ALREADY lagged 60 months, so a five-month-old pick is reading a
      window shifted by one twelfth of its own length, about content five to ten
      years old either way. Tonight's F2 confirms it directly: averaged over
      every calendar phase, the GROSS (zero-cost) train skill of the identical
      book is +0.0450 / +0.0460 / +0.0430 at holding periods of 1 / 3 / 6 months
      and only falls at 12 (+0.0278). Flat to six months, so six is the corner
      of the flat region and was fixed there before any overlapping book ran.

  (ii) the cost saving is arithmetic, not a forecast. Over the same sweep the
      cost term is -0.0190 / -0.0073 / -0.0012 / +0.0028 and engine-counted
      churn 2.36x / 1.48x / 1.04x / 0.73x. Fewer trading events cost less money;
      that is not a property of 2018-2023 that may fail to hold.

TONIGHT'S FREE SCREENS (train 1997-2017 only, through `protocol.evaluate_split`
with the v3 execution model -- the instrument validated 2026-10-25/26, which
reproduces this score's recorded train skill +0.026 to three decimals on its
hold-1 row below. No validation, holdout, forward or incubation number was read.
Journal F1-F7 of 2026-10-27/28.)

*F1/F2 -- the single-phase grid is a lottery, and that is why this book averages
the phase away rather than picking one.* Reforming every `hold` months at
calendar offset `phase`, all `hold` phases priced (gross = zero-cost skill):

    hold   gross mean   sd across phases   min      max      cost      turn
     1      +0.0450          --          +0.0450  +0.0450   -0.0190    2.36
     3      +0.0460        0.0171        +0.0320  +0.0650   -0.0073    1.48
     6      +0.0430        0.0273        +0.0180  +0.0900   -0.0012    1.04
    12      +0.0278        0.0179        -0.0000  +0.0580   +0.0028    0.73

The phase spread at hold 6 (sd 0.0273) is LARGER than the whole cost saving
(0.0178), so any one coarse grid buys the saving and a coin flip with it. A
plain semiannual (Jun/Dec) book reads gross +0.060 -- one draw of six, and the
2026-10-26/27 phase-6 anti-candidate is the standing warning against taking it.

*F3/F4 -- which channel pays, decomposed on train.* SYNC re-forms all six
sleeves every month (same names, same breadth, drift undone); OVERLAP reforms
one and lets the rest drift:

    book                        gross    cost     net     turn    pos   97-08   09-17
    hold-1  (= trial #12)      +0.045  -0.019  +0.026    2.36   140.4  +0.051  -0.020
    sync/H6                    +0.055  -0.007  +0.048    1.44   164.4  +0.057  +0.030
    overlap/H6                 +0.063  -0.005  +0.058    1.30   164.4  +0.062  +0.053

So about two thirds of the gain (+0.022 of +0.032) is the weight smoothing that
averaging six lagged picks produces -- a name enters at 1/600 and grows to 6/600
over six months instead of jumping to 1/100 -- and one third (+0.010) is the
drift. Both show up in turnover as well as in gross, and the smoothing half is
NOT a retention band: it re-times nothing, it changes what the target vector is.
`pt_oldhalf_sync6` ships alongside this file as the paired control, so the
decomposition is tested on validation rather than asserted from the table above.

*F5 -- the operator is not a free lunch and does not reach the risk axis.*
Applied to three slow risk scores it collapses the gross term instead of
preserving it, which is what (i) above predicts for a score whose content is not
five years old:

    score          hold1 gross -> overlap gross    hold1 net -> overlap net   volratio
    lowvol126           +0.057 -> +0.010               +0.009 -> -0.006         0.72
    lowvol504           +0.034 -> -0.010               +0.016 -> -0.013         0.74
    lowbeta252          (see journal F5)               -0.00x -> -0.022         0.69

All three also sit at a volatility ratio near 0.70, the de-risking construction
trial #1 closed. **No non-price-trend object cleared the standing screen
tonight, so no trial was bought outside this family.**

WHAT ARGUES AGAINST THE BOOK.
 (i) This is mechanism M3 again, not a new one: the score, the quota, K and the
     availability rule are trial #12's, and the honest description is the lab's
     one positive object traded under a cheaper rule. M3's validation readings
     are -0.006, -0.055, +0.070, +0.021 and +0.088.
 (ii) The parent score's within-region IC alternates sign across five-year
     buckets of the decision date (2026-10-25/26 F12), and much of the train
     result sits in the 2000-2004 rebound.
 (iii) 2009-2017 is +0.053 here against trial #12's -0.020, which is the first
     time the half of train nearest validation has agreed -- but that sub-period
     is the lab's WORST predictor of validation skill (-0.355 over fifteen
     trials), so it is reported, not leant on.
 (iv) Holding six months means a sleeve can carry a name that leaves its index
     inside the holding period. Those names are pruned at every month-end (the
     protocol's own instruction is to hold only names eligible on the rebalance
     date), and the shipped book was re-screened with the pruning in place
     rather than without it.

*F6 -- the null FOR THE OPERATOR, and it is the most important row in this file.*
Six random AR(1) scores at this score's own measured month-to-month Spearman rank
persistence (phi = **0.9803**), masked to its own scorable set, pushed through
the identical hold-1 and overlap constructions:

    book            net skill                    gross skill                turn
    null hold-1    -0.0377 (sd 0.0294, max -0.0010)  -0.0167 (sd 0.0295)    2.67
    null overlap   -0.0210 (sd 0.0151, max -0.0080)  -0.0158 (sd 0.0153)    1.34
    null DELTA     +0.0167 (sd 0.0153, min -0.0070, max +0.0410)

Read it both ways, because both readings matter:
 (a) **The LEVEL separates the book from the null decisively.** +0.058 against a
     null mean of -0.0210 at sd 0.0151 is **z +5.2** on net and +5.2 on gross,
     and the book churns 1.31x against the random scores' 1.34x. Consistent with
     the 2026-10-26/27 F13 null on the hold-1 version (z +5.9 / +5.7).
 (b) **The DELTA does not.** The operator hands a *meaningless* score +0.0167 of
     net skill, against this book's +0.032, which is **z +1.0**. So the gain is
     mechanical: it is the cost saving any score gets for trading less, not a
     selection effect this score has and others do not. **That is the claim, not
     a hole in it.** The hypothesis is explicitly that an ARITHMETIC channel
     transfers where selection channels have not; a null confirming the channel
     is arithmetic is the null agreeing with the hypothesis. What this rules out
     is the reading that the operator found something in the score.

*F7 -- the shipped file's own screen, pruning included.* `skill +0.058, gross
+0.063, cost -0.005, turn 1.31x, pos 164.3, volratio 0.972, skill at 2x costs
+0.053, 1997-2008 +0.061, 2009-2017 +0.053`. The pruning is free (unpruned:
+0.058 at 1.30x), and the 2026-10-26/27 method rule is satisfied -- this sheet
is the book that ships, not an algebraically-equivalent relative of it.

PRE-REGISTERED TURNOVER, as a range with the wider split's churn in it: train
comes in at 1.31x, and this lab's validation churn has run 29-49% above its
train figure on the last four trials of this mechanism, so **1.5-2.2x** is the
predicted band.
"""

from __future__ import annotations

import pandas as pd

from strategies.lib.calendar_peers import calendar_peers, peer_quota_select

K = 100
LAG = 60          # months skipped before the score window starts
SPAN = 60         # length of the score window, in months
MIN_MONTHS = 48   # of SPAN
DEPTH_BINS = 3
HOLD = 6          # sleeves; one is reformed each month and held HOLD months

STRATEGY = {
    "name": "pt_oldhalf_overlap6",
    "family": "price-trend",
    "hypothesis": (
        "Holding trial #12's book -- the 100 eligible names with the lowest mean monthly "
        "return over months -120..-61, quota-allocated across (trailing-trading-calendar "
        "peer group x price-history-depth tercile) cells -- in six overlapping monthly "
        "sleeves, one reformed each month and carried six months as shares, earns higher "
        "validation skill than trial #12's single-sleeve monthly version of the identical "
        "score, because a 60-month mean already lagged 60 months loses no measurable "
        "selection to a five-month-old pick (train gross skill is flat at +0.045/+0.046/"
        "+0.043 across 1-, 3- and 6-month holding periods, averaged over every calendar "
        "phase) while the overlapping rule cuts engine-counted churn from 2.36x to 1.30x "
        "and the cost term from -0.019 to -0.005 -- a saving that is arithmetic rather "
        "than a forecast, which is the one kind of gain this lab has not yet tested for "
        "transfer."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Six overlapping sleeves of the old-half reversal's top-K peer/depth-quota
    pick. One sleeve is reformed each month-end and held six months as shares;
    the emitted row is the whole book's drifted weights, so only the reformed
    sleeve trades. Names that stop being eligible are pruned at every month-end.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    px = prices.ffill()

    # Monthly returns. A value published on a month label uses only returns realized at
    # or before that label; the daily reindex forward-fills, so a decision date reads the
    # latest label at or before it.
    monthly = prices.resample("ME").last()
    mret = monthly.pct_change(fill_method=None)

    # The old half of the decade window: shifted clear of the most recent LAG months.
    old = mret.shift(LAG).rolling(SPAN, min_periods=MIN_MONTHS).mean()
    score = (-old).reindex(prices.index, method="ffill")

    # History depth, as a candidate can count it: months of realized monthly return in
    # the visible window. A function of the window's start, not its end.
    depth = mret.notna().cumsum().reindex(prices.index, method="ffill")

    sleeves: dict[int, pd.Series] = {}   # sleeve -> share counts by name
    formed: set[int] = set()
    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Hold only names that are still eligible: the engine zeroes the rest, so a
        # sleeve carrying a leaver would be asking for a book it does not get.
        if sleeves:
            ok = set(names)
            sleeves = {s: sh[[n in ok for n in sh.index]] for s, sh in sleeves.items()}
            sleeves = {s: sh for s, sh in sleeves.items() if len(sh)}

        p = px.loc[date]
        vals = {s: float((sh * p.reindex(sh.index)).fillna(0.0).sum())
                for s, sh in sleeves.items()}
        value = float(sum(vals.values()))

        # Mask to the eligible names BEFORE anything cross-sectional is taken.
        sc = score.loc[date].reindex(names).dropna()
        picked = None
        if len(sc) >= 50:
            groups = calendar_peers(volume, date, sc.index).dropna()
            if len(groups) >= 50:
                sc = sc.reindex(groups.index)
                dep = depth.loc[date].reindex(groups.index)
                try:
                    bins = pd.qcut(dep.rank(method="first"), DEPTH_BINS, labels=False)
                except ValueError:
                    bins = pd.Series(0, index=dep.index)
                cells = groups.astype(str) + "|" + bins.astype(str)
                cand = peer_quota_select(sc, cells, K)
                if len(cand) >= 20:
                    picked = cand

        if picked is None:
            if value == 0.0:
                # Warm-up: hold the pool rather than cash, so the book is not scored
                # against a fully-invested benchmark while sitting out (2026-10-15/16).
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        # Which sleeve is due. Anchored on the calendar month, not on the position of
        # the date inside the visible window, so truncating the frame cannot move it.
        sleeve = (date.year * 12 + date.month - 1) % HOLD
        if value == 0.0:
            target = 1.0
        elif sleeve not in formed:
            # Ramp-up: the sixth of the book this sleeve will hold comes pro rata out
            # of the sleeves that already exist. Happens once per sleeve.
            target = value / HOLD
            sleeves = {s: sh * ((value - target) / value) for s, sh in sleeves.items()}
        else:
            target = vals.get(sleeve, 0.0)

        pp = p.reindex(picked)
        pp = pp[pp > 0].dropna()
        if len(pp) < 20 or target <= 0:
            continue
        sleeves[sleeve] = (target / len(pp)) / pp
        formed.add(sleeve)

        held = pd.Series(0.0, index=prices.columns, dtype=float)
        for sh in sleeves.values():
            held = held.add((sh * p.reindex(sh.index)).reindex(prices.columns).fillna(0.0),
                            fill_value=0.0)
        total = float(held.sum())
        if total > 0:
            rows[date] = held[held > 1e-12] / total

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
