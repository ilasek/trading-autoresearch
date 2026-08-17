---
title: "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency"
authors: Jegadeesh, Titman
year: 1993
venue: Journal of Finance (venue tier 1)
url: https://doi.org/10.1111/j.1540-6261.1993.tb04702.x
citations: 12208 (SciSpace, checked 2026-08-17)
sample_period: 1965–1989
markets: US (NYSE + AMEX, CRSP)
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

Relative past return over an intermediate horizon (3–12 months) predicts relative future
return over a comparable horizon. The paper's own tests rule out the two mechanical
explanations available at the time: the profits are not compensation for systematic risk
(they survive beta and size controls) and are not an artifact of lead–lag cross-serial
correlation in reaction to common factors. What remains is under-reaction to firm-specific
information — prices adjust to news gradually rather than instantly, so the ranking of
recent relative performance carries information about the not-yet-completed adjustment.

The economically important qualifier the paper itself supplies: **the effect is not
permanent.** A meaningful part of the abnormal return earned in the first year after
formation dissipates over the following two years. This is a delayed-adjustment story with
an overshoot component, not a persistent risk premium — which bounds how long a position
formed on a momentum signal can usefully be held before it starts collecting the reversal.

## Construction recipe

- **Universe/sort**: each month, rank all eligible names on cumulative return over the past
  J months; form decile portfolios; hold the top decile (long side) — the paper's headline
  strategy is winners-minus-losers, but the winner decile is the piece a long-only book uses.
- **Weighting**: equal-weighted within decile.
- **Formation/holding grid**: J and K each drawn from {3, 6, 9, 12} months. Every one of the
  combinations tested produced positive average returns — the effect is not a knife-edge of
  one lookback. The strongest combination in their grid used a 12-month formation with a
  short (3-month) holding period.
- **Skip period**: the original paper inserts a **1-week** gap between the end of formation
  and the start of holding, to avoid contaminating the momentum signal with short-horizon
  bid–ask bounce and reversal. (The 1-month skip that is now the field convention — the
  "12-1" construction — is a later hardening of the same idea; the rationale is identical,
  the length differs.)
- **Overlapping portfolios — the piece that matters most here.** For a K-month holding
  period they do not reform the whole book each month. They hold, simultaneously, the
  portfolios formed in the current month **and in each of the previous K−1 months**, so the
  live book is an average of K formation vintages and only **1/K of capital is recommitted
  per month**. Their stated motive is statistical: overlapping vintages yield many more
  monthly observations than disjoint K-month periods, raising the power of the test.

## Robustness evidence (qualitative only)

- Positive across the entire 4×4 formation/holding grid, not a single tuned pair.
- Survives controls for beta, firm size, and the authors' own transaction-cost treatment.
- Momentum is among the most replicated cross-sectional effects in the literature; it is one
  of the anomalies that clears the bar in the large-scale replication audits (it is not
  among the majority of published anomalies that fail to replicate), and the effect has been
  documented out-of-sample across many national equity markets and in later decades than the
  original sample. See `2026-08-17-mclean-pontiff-publication-decay.md` for the general
  post-publication decay discount that nonetheless applies.
- The post-first-year reversal is itself a replicated feature, not a sample quirk.

## Implementability here

**Directly relevant, because this repo's strongest recorded mechanism is this paper's
sampling scheme re-purposed.** The champion holds K = 6 overlapping monthly formation
tranches and recommits ~1/6 of capital per month — structurally identical to Jegadeesh and
Titman's overlapping-portfolio construction with K = 6.

Three things follow that are worth writing down:

1. **The literature's framing understates what the lab found.** In the paper, overlapping
   vintages are a *statistical estimator* — a way to get more observations out of the same
   history. They are not presented as a portfolio improvement, and the paper does not claim
   the overlapped book earns more than a single-vintage book. The lab's own result (the
   overlap raises return, not merely lowers cost, and pruning stale names *hurts*) is
   therefore a finding **beyond** this source, not an import from it. Do not cite this paper
   as literature support for the temporal-breadth explanation; it supports only the
   construction, not the economic claim.
2. **A principled bound on tranche count, without sweeping K.** The learnings file
   explicitly forbids sweeping K as knob-tuning. This paper supplies a mechanism-level
   ceiling instead: because momentum profits partially *reverse* over the two years after
   formation, tranche lifetime that extends well past ~12 months stops holding a decayed
   signal and starts holding an actively reversing one. K = 6 sits comfortably inside that
   bound; K in the high teens or beyond would not, and that is a reason, not a sweep.
3. **Long-only caveat.** The paper's headline object is winners-minus-losers. Everything the
   long side of the decile sort earns is available here; nothing that comes from the loser
   leg is. Any figure or claim about WML should be assumed not to transfer.

Pitfalls specific to this repo: the decile sort assumes a broad cross-section — on a
~145-instrument universe a "decile" is ~14 names, so the paper's breakpoints translate to
roughly the basket size already in use, and finer sorts would be noise. Equal weighting
within the basket is the paper's construction and is *not* what the champion does (it
magnitude-weights); the lab has already established magnitude-weighting is the better of
the two here, so treat the paper's equal weighting as the baseline it superseded, not as a
recommendation.

## Related

- `2026-08-17-momentum-horizon-echo.md` — which slice of the formation window carries the
  information, and why the answer differs between US-only and global universes.
- `2026-08-17-momentum-crash-risk-management.md` — the tail-risk properties of this signal
  and why the standard fixes are long-short-specific.
- `experiments/learnings.md`: "Overlapping formation tranches are the strongest mechanism in
  the repo" and "Holding names the current signal has already rejected is the overlap's
  active ingredient" — both consistent with, but not derivable from, this source.
