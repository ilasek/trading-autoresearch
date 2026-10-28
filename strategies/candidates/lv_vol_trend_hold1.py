"""A multi-year FALLING-TURNOVER trend, as a plain monthly top-K book.

THE CLAIM IN ONE LINE. `liquidity-volume` is recorded as a null on this panel
(`learnings.md`, 2026-10-24/25), but every reading that closed it was of a
liquidity *level* -- Amihud illiquidity, dollar volume, the region-relative
restatement of the same. The *trend* in a name's own share turnover over
multiple years has never been priced here, and it is the instrument Datar-Naik-
Radcliffe's low-turnover premium actually names: a name whose turnover is
falling is becoming less liquid, and a less liquid name must offer more return.

THE SCORE. For each (recent, older) month-pair in `{(24,24), (24,36), (24,60),
(36,36), (36,60), (60,60)}`, the log ratio of the name's mean daily share volume
over the last `recent` months to its mean over the `older` months before that,
normal-scored across the names eligible on the decision date and averaged over
the six pairs. Negated: the book buys falling turnover. Pre-signed from the
published direction BEFORE anything was run; the negation invariant below is
what tests that, and it passes by a distance.

WHY SHARE COUNTS AND NOT DOLLAR VOLUME. The store holds back-adjusted bars, so
the price level and the volume level embed future corporate actions (the
2026-10-22 engine issue), and the standing rule is that a candidate may use
ratios and trends of the stored panels and not their levels. A ratio of two
share-volume means for one name is scale-free in share counts, so the
contaminant cannot enter by construction; measured, this score's rank rho to the
log price level is **+0.070**, i.e. the leak-predicted IC contribution is about
-0.006 and of the wrong sign to flatter it. Dollar volume would have carried the
dividend half of the same contaminant, as the `lv_*` lineage did.

WHY THE KNOB IS AVERAGED AND NOT CHOSEN. Tonight's F4 priced all nine
(recent, older) pairs over {12,24,36,60} before any one was read, per the
2026-10-27/28 phase-lottery rule. The three pairs with a 12-month recent window
read -0.051 / -0.013 / +0.016 and the six with a recent window of 24 months or
more read +0.015 to +0.034 (sd 0.0066, every cell positive). The 12-month cells
were excluded **a priori** by the sleeve operator's own stated precondition --
the score's content must be older than the holding period -- not by their
scores; and the six survivors are averaged rather than picked, so the shipped
file contains no window choice to have got lucky on. (Unpredicted and flagged
as such: the average scores above every individual cell, which is what one
expects if the cells share content and differ by independent boundary noise, but
it was not forecast.)

THE TRAIN SHEET (train 1997-2017 only, through the engine's own backtest with
`setup.execution` -- the instrument validated 2026-10-25/26 and re-confirmed
tonight at `pt_oldhalf_overlap6` +0.0580 against its recorded +0.058 and
`pt_decade_old_half_depth_neutral` +0.0256 against +0.026. No validation,
holdout, forward or incubation number was read. Journal F1-F9 of 2026-10-28/29.)

    book                  net     gross    cost    2x cost  turn   pos    97-08   09-17
    hold-1   [this file] +0.0504 +0.0622 -0.0118  +0.0386   1.81   102.0  +0.030  +0.122
    overlap/H6 [control] +0.0415 +0.0437 -0.0022  +0.0393   1.07   120.0  +0.025  +0.079

Positive in BOTH train sub-periods and at 2x liquidity costs. Volatility ratio
to the pool 0.96, so this is not the de-risking construction trial #1 closed
(that column sits at 0.71-0.77) -- though the negated book reads 1.16, so the
falling-turnover side is the lower-volatility side and that is a caveat, not a
clean bill.

THE MATCHED NULL, AND WHICH READING THE HYPOTHESIS RESTS ON. Six random AR(1)
scores at this score's own month-to-month Spearman rank persistence
(**phi = 0.9953**), masked to its own scorable set, pushed through the identical
constructions:

    book            null net skill (sd)    this book     z
    hold-1         -0.0220 (0.0172)        +0.0504     +4.21
    overlap/H6     -0.0161 (0.0194)        +0.0415     +2.97
    operator delta +0.0059 (0.0098)        -0.0089     -1.51

**The hypothesis rests on the LEVEL, and it is pre-registered as such.** The
delta is the operator's, not the score's, and it is the paired control's
business rather than this file's.

RELABELLING CONTROLS (rank rho, train month-ends, eligible names only). Nothing
here is a refuted object in costume, and the two largest numbers are NEGATIVE
against the lab's one positive mechanism:

    M3's old half -0.164 | decade mean -0.204 | -vol126 +0.134 | mom 12-1 +0.049
    amihud126 -0.089 | log price level +0.070 | history depth +0.049

Run the refuted objects through this construction (the 2026-10-25/26 rule), and
this score is a better *selector* rather than only a cheaper book: gross skill
+0.011 (-vol126), -0.010 (mom 12-1), +0.038 (amihud126), +0.007 (decade
skewness) against this file's +0.062.

WHAT ARGUES AGAINST IT.
 (i) Every number above is a TRAIN number, and this lab has nine recorded
     instances of a train *selection* term failing to transfer, with
     `corr(train skill, validation skill)` at -0.074 over seventeen v3 trials.
     The one quantity measured to transfer is a cost term, and this file's claim
     is a selection claim. It should be read as a reason to spend a trial, not
     as a result.
 (ii) The 2009-2017 sub-period (+0.122) is the strongest half, and that
     sub-period is the lab's WORST predictor of validation skill (-0.355 over
     fifteen trials). Reported, not leant on.
 (iii) `liquidity-volume`'s family lead is at validation skill -0.052 and the
     family was closed on measurement. A new instrument inside a closed family
     carries the family's prior, and the honest expectation is about zero.
 (iv) 1.81x churn is above the pool's 0.89x, and the cost schedule has eaten a
     positive selection term on six of sixteen objects this lab has priced.

PRE-REGISTERED TURNOVER: train comes in at 1.81x, and this lab's validation
churn has run 29-49% above its train figure on the last four trials, so
**2.3-2.7x** is the predicted band.
"""

from __future__ import annotations

from strategies.lib.vol_trend_book import vol_trend_book

K = 100
HOLD = 1          # the one integer that differs from lv_vol_trend_overlap6

STRATEGY = {
    "name": "lv_vol_trend_hold1",
    "family": "liquidity-volume",
    "hypothesis": (
        "The 100 eligible names with the most negative multi-year share-turnover trend -- "
        "the mean, over the six (recent, older) month-pairs whose recent window is at least "
        "24 months, of the within-eligible normal score of log(mean daily share volume over "
        "the last `recent` months / mean over the `older` months before that) -- quota-"
        "allocated across (trailing-trading-calendar peer group x price-history-depth "
        "tercile) cells and re-picked monthly, earns positive validation skill against the "
        "equal-weight eligible pool, because Datar-Naik-Radcliffe's low-turnover premium is a "
        "statement about a name becoming less liquid and the trend in its own share turnover "
        "is that statement's instrument, where every reading that closed `liquidity-volume` "
        "on this panel was of a liquidity LEVEL instead. Train net skill is +0.050 at z +4.21 "
        "against six AR(1) scores matched to this score's own rank persistence (phi 0.9953) "
        "through the identical book, positive in both train sub-periods and at 2x costs, with "
        "rank rho at most 0.21 to every refuted or contaminated object on the board and "
        "NEGATIVE (-0.16, -0.20) to the lab's one positive mechanism."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """The falling-turnover top-K book, re-picked and fully reformed each
    month-end (HOLD = 1 sleeve)."""
    return vol_trend_book(prices, aux, eligible=eligible, k=K, hold=HOLD)
