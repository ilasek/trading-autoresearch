---
title: "Is Momentum Really Momentum? / Is Momentum an Echo? (paired sources)"
authors: Novy-Marx (2012); Goyal, Wahal (2015)
year: 2012, 2015
venue: Journal of Financial Economics; Journal of Financial and Quantitative Analysis (both venue tier 1)
url: https://www.sciencedirect.com/science/article/abs/pii/S0304405X11001152 ; https://econpapers.repec.org/article/cupjfinqa/v_3a50_3ay_3a2015_3ai_3a06_3ap_3a1237-1267_5f00.htm
citations: Novy-Marx (2012) 450; Goyal–Wahal (2015) 90 (Semantic Scholar, checked 2026-08-17)
sample_period: Novy-Marx US CRSP, ~1927–2010 (approximate; full text not retrievable this session). Goyal–Wahal 37 non-US countries plus the US, ~1980–2011 international (approximate)
markets: Novy-Marx US only; Goyal–Wahal 38 countries incl. developed and emerging, plus pooled regional portfolios
tier: A (both peer-reviewed tier-1; citation counts now verified, so the earlier A− caveat no longer applies)
validation_overlap: false
published_post_2018: false
---

## Mechanism

Both papers ask **which slice of the formation window actually carries the momentum
signal**, and they disagree — which is exactly why they are worth reading together.

**Novy-Marx (2012)**: sorting on returns from month t−12 to t−7 ("intermediate horizon")
predicts future returns better than sorting on t−6 to t−2 ("recent horizon"), and once
intermediate performance is controlled for, recent performance adds little. Predictability
drops off abruptly past 12 months. He labels the shape an *echo* rather than momentum: the
information is not in what just happened but in what happened a while ago, which no standard
under-reaction or risk story predicts. He is explicit that none of the popular
explanations — behavioral or rational — delivers this term structure, i.e. the finding is
presented as an empirical fact in search of a mechanism, not as a mechanism.

**Goyal and Wahal (2015)** test the same term structure outside the US. In 37 non-US
countries there is no robust echo. In portfolios pooling developed and emerging markets, and
in each of three regional groupings (Americas ex-US, Asia, Europe), there is no echo either.
Their diagnosis of the US result: what looks like an echo there is largely a **carryover of
short-term reversal from month t−2** contaminating the recent-horizon leg — i.e. the
recent-horizon portfolio is handicapped by reversal rather than the intermediate-horizon
portfolio being genuinely better informed.

So the honest synthesis is: the echo is a US-specific, specification-sensitive result, and
the mechanism-level claim that survives both papers is the much older and duller one — **a
skip period matters, because the most recent weeks carry reversal, not continuation.**

## Construction recipe

Common scaffolding to both: monthly rebalance, sorts on cumulative return over a *window*
defined by two endpoints rather than a single lookback, value-weighted portfolios in
Novy-Marx, no transaction costs modeled in the headline tests.

- **Intermediate-horizon signal**: cumulative return from t−12 through t−7 (a six-month
  window ending six months before formation).
- **Recent-horizon signal**: cumulative return from t−6 through t−2 (skipping the most
  recent month).
- **Conventional signal for comparison**: t−12 through t−2 (or t−1), i.e. the familiar 12-1.
- Skipping the most recent month is common to all specifications, precisely to avoid
  short-run reversal / microstructure bounce.
- Goyal–Wahal replicate this decomposition country-by-country and then in pooled
  multi-country and regional portfolios — the pooling step is the one that matters for a
  global universe.

## Robustness evidence (qualitative only)

- The echo is **not** robust out of the US: that is the whole content of the second paper,
  and it is a direct, same-methodology, 37-country test — the strongest form of
  out-of-sample challenge available short of a new time period.
- Novy-Marx's own framing concedes there is no theory generating the term structure, which
  is a soundness *weakness* under this repo's rubric (methodology honesty is high, but
  mechanism plausibility is low — an effect with no mechanism and no out-of-sample survival
  is the classic profile of a specification artifact).
- The abrupt drop-off past 12 months is common ground and is consistent with
  Jegadeesh–Titman's post-first-year reversal.
- What both papers agree on and what is well replicated: skip the most recent month.

## Implementability here

**This note's main practical value is that it argues against a tempting candidate.**

The champion scores names on a composite of 6-1 and 12-1 momentum. An obvious-looking next
idea is "Novy-Marx says the recent horizon is noise — replace the composite with a pure
12-7 intermediate-horizon score." Two independent reasons to rank that idea **low**:

1. **This repo's universe is global, and the global evidence says no echo.** The instrument
   set is ~145 global stocks and ETFs — structurally much closer to Goyal–Wahal's pooled
   multi-region portfolios (where the echo vanishes) than to Novy-Marx's US-only CRSP
   cross-section. The applicable prior is therefore "no echo", not "echo".
2. **The lab has already established that re-scoring is a low-yield axis.** `learnings.md`
   records 52-week-high proximity, residual momentum (twice), and information discreteness
   all landing at or below the base construction, and concludes that "find a better score"
   is heavily explored while portfolio construction and rebalance mechanics remain open. A
   12-7 rescore is another draw from the exhausted urn, and now with a literature prior
   pointing the wrong way.

What *does* transfer, and is cheap:

- **The skip is load-bearing and both papers agree on it.** The champion's 6-1/12-1
  composite already skips the most recent month, so this is confirmation that an existing
  choice is well-grounded rather than arbitrary — worth knowing before anyone "simplifies"
  it to 6-0/12-0.
- **A no-cost holdings-only diagnostic before spending a trial**, in the spirit of the
  learnings entry on cheap diagnostics: compute the cross-sectional rank correlation between
  the current composite score and a 12-7 score on the same universe. If it is as high as the
  0.89 that killed the earlier inter-signal ensemble, the idea is dead without a trial. This
  costs no backtest and touches no returns.

Pitfalls: Novy-Marx's portfolios are value-weighted long-short deciles with no costs; the
12-7 window discards the most recent six months entirely, which on a monthly-rebalanced
long-only book means the signal is stale by construction — interacting badly with a
six-tranche overlap that is *already* holding six months of formation vintages. Stacking a
six-month-stale signal on a six-month-deep tranche stack would push effective signal age
toward the 12-month reversal boundary Jegadeesh–Titman warn about.

## Related

- `2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the base construction and the
  post-first-year reversal that bounds total signal age.
- `2026-08-17-mclean-pontiff-publication-decay.md` — why a single-market, mechanism-free,
  much-cited result deserves an extra discount.
- `experiments/learnings.md`: the 52-week-high / residual-momentum / information-discreteness
  cluster, and the "open axes are portfolio construction and rebalance mechanics, not signal
  definition" conclusion — this note supplies literature backing for that conclusion.
