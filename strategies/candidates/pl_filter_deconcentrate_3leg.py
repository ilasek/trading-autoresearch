"""FILTER, THEN DECONCENTRATE -- the one combination operator in this family the lab
has never run (research `#513`).

THE CLAIM IN ONE LINE. Per lead, keep a broad selection on that lead's OWN score; then
inside each selection keep the names with the BEST composite rank across the OTHER
leads; then equal-weight the survivors and blend the legs at equal allocation. The
hypothesis is about the OPERATOR, not about any signal: the three legs are already-
measured objects on this board and two of the three are nulls.

WHY THIS IS NOT ONE MORE ENSEMBLE PROPOSAL, AND THE ARGUMENT IS STRUCTURAL. This lab
has measured the `mean` operator (bounded by its legs), the `max`, the `intersection`,
and equal-weight ensembles of finished RETURN SERIES (monotone decreasing against the
best member). Every one of those is killed in advance by one of two bounds the research
folder uses for exactly that purpose: Breiman's simplex bound, which binds on any
reweighting of finished long-only books, and Novy-Marx's linear-composite equivalence,
which binds on untruncated linear composites. A per-leg selection FILTERED BY THE OTHER
LEADS is neither: the filter is a nonlinearity applied INSIDE each leg, BEFORE portfolio
construction, so it is outside both bounds. `learnings.md`'s own standing rule -- the
value of an aggregation operator is the value of its nonlinearity -- points straight at
it.

WHY THE INFORMATION IS EXPRESSIBLE AS MEMBERSHIP AND NOT AS A WEIGHT. On an equal-
weighted pool every excluded name takes the identical -1/N active weight, so a score's
information enters a long-only book as MEMBERSHIP and not as an ordering of the bad
names (`learnings.md`'s `#375`). The source arrives at the same place from the other
direction: a composite score is an implicit return forecast, reliable for broad groups
and not name by name, so it should make broad distinctions and nothing finer. Both say
the composite decides who is in the book and never touches a weight. Weights here are
therefore maximum deconcentration -- equal, subject to the engine's 25% cap -- and no
score magnitude enters them anywhere.

THE PAIRED CONTROL IS THE POINT OF THE TRIAL. `pl_ownscore_deconcentrate_3leg` is this
file with ONE operator changed: its final 90 names per leg are the 90 DEEPEST on that
leg's own score instead of the 90 best on the other legs' composite. Same legs, same
dates, same breadth, same weighting, same quota. The DIFFERENCE between the two arms is
the value of the filter nonlinearity and nothing else.

THE FREE SCREENS, RUN BEFORE THIS FILE WAS WRITTEN, AND WHAT EACH WAS ALLOWED TO DO.
Research `#514`'s holdings screen and `#515`'s persistence screen, both train-only
(252 month-ends, 1997-2017):

    per-leg Jaccard(filtered, control) selections   0.425      <- the D2 refusal test
    book size, filtered / control                  142 / 202
    dilution pair, mean rank on the other leg       +0.500 .. +0.529
    phi (month-to-month rank persistence)   rev +0.974  mom +0.876  vshock -0.033
    exit-from-top-180 share                 rev 0.3%  mom 3.2%  vshock 47.1%

 (i) The D2 test is the only one that could have refused this file, and it passed:
     the filter moves well over half of each leg's names, so the filtered arm is not
     the control arm relabelled. Had the Jaccard been >= 0.90 only one arm would have
     been run.
 (ii) The dilution pairs come out at the MEDIAN (+0.500 to +0.529), which is NOT what
     was pre-registered: the three legs are nearly ORTHOGONAL in rank, not offsetting.
     Long-horizon reversal and 12-1 momentum were expected to oppose each other and do
     not, on this panel, at these windows. Recorded as a correction to the expectation,
     not as support for the book.
 (iii) `#515`'s band reading: a retention band is inert below phi ~0.97 (2026-11-22),
     which holds for one of three legs only, so NO band is used. The churn forecast
     comes from the same entry's predictor instead.
 (iv) NO TRAIN SKILL, IC, OR SIGNAL STATISTIC WAS COMPUTED OR READ for this book. The
     2026-11-22 rule stands: "a train screen may refute but may not qualify" forbids a
     threshold on a train signal statistic in EITHER direction, and this lab has
     measured corr(train skill, validation skill) at -0.08 over 27 trials.

PRE-REGISTERED TURNOVER, from the 2026-11-22 predictor and written before the trial:
`train one-way churn ~ 1.0 + 0.29 x exit180%` gives 1.1x / 1.9x / 14.7x for the three
legs, and each leg is a third of the book, so **train 2.5-7.0x and validation 3.5-12.0x**
(the registered range, at 1.30-2.00x train). The fast leg carries the bill: the parent
volume-shock book charged ~19 bps per 1x of churn because a volume shock selects exactly
the names the liquidity tiers and the UK/HK/FR/IT/ES taxes punish, so ~100 bps/yr of the
blended book is cost. That is under D3's refusal line, not over it, which is why the file
was written.

WHAT ARGUES AGAINST THE BOOK.
 (i) Two of the three legs are measured NULLS here (12-1 momentum, and the volume shock
     at net skill +0.031), and the third is a board lead whose 90% interval contains
     zero. An operator applied to nulls has to supply the whole of any skill.
 (ii) The filter makes the three legs CONVERGE -- book size falls 202 -> 142 while each
     leg still holds 90 -- which is the source's own structural warning that composite-
     selected names are more correlated with each other than average names, i.e. less
     diversification is available to this arm than to its control. The two arms are
     therefore NOT size-matched, and that is a property of the operator rather than a
     flaw in the pairing: size-matching would have required a second operator change.
 (iii) Requiring all three legs to be defined means requiring ~9 years of monthly
     returns (leg rev needs 108 monthly observations). Price-history depth is a necessary
     condition that carries no information here (2026-11-20), so this is a coverage
     restriction rather than a hidden tilt, but it does mean the book never holds a
     recently-admitted name.
 (iv) Research `#517` is explicit that the mix-versus-composite ranking is NOT settled
     and crosses over in the level of active risk, so no direction was imported from the
     literature. `#514`'s screen reads 0.425 as the low-overlap side, which is the side
     where the composite is predicted to win; that reading is recorded and is not offered
     as evidence.

ONE RECORDED COST OF THIS FILE, STATED BECAUSE IT IS A TRIAL THE BAR NOW CARRIES. The
first version labelled its legs `"R"`, `"M"` and `"V"`, and the hindsight guard refused
it before anything ran: all three single letters are real ticker ids on this panel. The
refusal was recorded as trial #33 (`GATE_FAIL`, nothing scored, no returns stored), so it
counts against the deflated-Sharpe bar for every later candidate. The guard behaved
exactly as designed; the lesson is that a leg label is a string constant and single
letters collide with instrument ids.
"""

from __future__ import annotations

import pandas as pd

from engine import data
from strategies.lib.calendar_peers import calendar_peers, peer_quota_select
from strategies.lib.lead_scores import leg_scores, pct_rank

BROAD = 150      # the leg's own broad selection
FINAL = 90       # what survives the other leads' composite filter
LEGS = ("rev", "mom", "vshock")

STRATEGY = {
    "name": "pl_filter_deconcentrate_3leg",
    "family": "portfolio-learning",
    "hypothesis": (
        "Blending three legs at equal allocation, where each leg takes the 150 eligible "
        "names with the highest rank on its own score (long-horizon reversal, 12-1 "
        "momentum, split-guarded 5/45 volume shock) and then keeps the 90 of those with "
        "the BEST composite rank across the OTHER two legs, quota-allocated across "
        "(trailing-trading-calendar peer group x instrument type) cells and equal-weighted "
        "within each leg, earns higher validation skill over the equal-weight eligible pool "
        "than the identical book whose final 90 are the 90 deepest on the leg's own score, "
        "because on an equal-weighted long-only pool a score's information enters as "
        "MEMBERSHIP rather than as a weight, and a per-leg selection filtered by the other "
        "leads is a nonlinearity applied inside the leg before portfolio construction -- "
        "the one combination operator that falls outside both Breiman's simplex bound and "
        "Novy-Marx's linear-composite equivalence, the two bounds that kill every ensemble "
        "operator this lab has already measured."
    ),
    "track": "scout",
}


def generate_weights(prices, aux, eligible=None):
    """Three legs, each broad-selected on its own score and then filtered by the other
    two legs' composite rank; equal weights within a leg, equal allocation across legs,
    monthly.
    """
    volume = aux["volume"]
    elig = (eligible if eligible is not None
            else pd.DataFrame(True, index=prices.index, columns=prices.columns))
    elig = elig.reindex(index=prices.index, columns=prices.columns).fillna(False).astype(bool)
    kinds = data.instrument_types("pit")

    scores = leg_scores(prices, volume)

    rows = {}
    for date in prices.groupby(pd.Grouper(freq="ME")).tail(1).index:
        live = elig.loc[date].to_numpy() & prices.loc[date].notna().to_numpy()
        names = prices.columns[live]
        if len(names) < 50:
            continue

        # Mask to the eligible names BEFORE anything cross-sectional is taken, and rank
        # each leg on exactly the names every leg can score, so no leg is ranked on a
        # different population from the composite it is filtered by.
        raw = {leg: scores[leg].loc[date].reindex(names).dropna() for leg in LEGS}
        idx = raw[LEGS[0]].index
        for leg in LEGS[1:]:
            idx = idx.intersection(raw[leg].index)
        if len(idx) < 200:
            if not rows:
                rows[date] = pd.Series(1.0 / len(names), index=names)
            continue

        groups = calendar_peers(volume, date, idx).dropna()
        if len(groups) < 100:
            continue
        idx = idx.intersection(groups.index)
        if len(idx) < 200:
            continue
        rank = {leg: pct_rank(raw[leg].reindex(idx)) for leg in LEGS}
        cells = (groups.reindex(idx).astype(str) + "|"
                 + pd.Series([str(kinds.get(n, "stock")) for n in idx], index=idx))

        book = pd.Series(0.0, index=prices.columns, dtype=float)
        legs_filled = 0
        for leg in LEGS:
            own = rank[leg]
            broad = own.nlargest(min(BROAD, len(own))).index
            others = [o for o in LEGS if o != leg]
            comp = sum(rank[o].reindex(broad) for o in others) / float(len(others))
            comp = comp.dropna()
            if len(comp) < 40:
                continue
            picked = peer_quota_select(comp, cells.reindex(comp.index), FINAL)
            if len(picked) < 20:
                continue
            book = book.add(pd.Series(1.0 / len(picked), index=picked)
                            .reindex(prices.columns).fillna(0.0), fill_value=0.0)
            legs_filled += 1

        if legs_filled == 0:
            continue
        total = float(book.sum())
        if total <= 0:
            continue
        rows[date] = book[book > 1e-12] / total

    if not rows:
        return pd.DataFrame(index=prices.index[:0], columns=prices.columns)
    out = pd.DataFrame(rows).T.reindex(columns=prices.columns).fillna(0.0)
    return out.sort_index()
