---
title: "Cross-Sectional and Time-Series Tests of Return Predictability: What Is the Difference?"
authors: Goyal, Jegadeesh
year: 2018
venue: Review of Financial Studies 31(5), 1784–1824 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhx131
citations: 137 (OpenAlex, checked 2026-08-17; not indexed in Semantic Scholar under this DOI)
sample_period: US stocks 1946–2013; 55 futures markets 1985–2013
markets: CRSP US common stocks (non-micro-cap, above the 20th NYSE size percentile); 55 futures contracts spanning equities, bonds, commodities and currencies
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This source answers the open question `SUMMARY.md` flagged last session — *why does the
time-series momentum literature discard signal magnitude while this lab's largest single gain
came from magnitude weighting?* — and it answers it by exhibiting the exact algebraic
difference between the two families.

**The difference between a time-series and a cross-sectional strategy is a benchmark, and the
benchmark is worth a portfolio.**

- A **cross-sectional (CS)** rule ranks each asset's past return *against the cross-sectional
  mean*: long the ones above, short the ones below. Because the comparison point is the mean
  of the same set, the long and short sides are equal by construction and the strategy is
  **zero net investment**.
- A **time-series (TS)** rule compares each asset's past return *against zero* (i.e. against
  its own excess-return sign): long if positive, short if negative. Nothing forces the two
  sides to balance, so the strategy carries a **time-varying net long position** in risky
  assets.

Write `NetLong_t = Σ_i w^TS_{i,t−1}`. Then a TS strategy is, exactly,

```
TS  ≈  CS  +  NetLong_t × (equal-weighted index return)
```

and the extra term — the authors call it the time-varying investment in the market, TVM —
decomposes cleanly into two economically different pieces:

```
TVM  =  E[NetLong] × E[R̄]        ← "risk premium": just being net long, on average
      + cov(NetLong_t, R̄_t)      ← "market timing": being more long before up-markets
```

The empirical core of the paper is that for US stocks, **the entire performance gap between TS
and CS strategies is this TVM term**. Once a CS strategy is given the same net long position
(the authors' "CS TVM" construction), CS and TS excess returns are generally about equal
across ranking/holding horizons from 1 to 60 months. The TS approach is not better at picking
assets; it is a CS strategy plus a market exposure.

**Which piece of TVM dominates depends on horizon, and this is the part that matters most
here.** At long ranking periods — the 12-month horizon this repo's champion uses — the net
long position is large and *virtually all of the TVM return comes from the static risk-premium
component*, i.e. from simply being invested. The market-timing covariance term is the larger
share only at short ranking horizons, and its statistical support is weaker throughout.

**The one substantive thing the TS approach does differently is a failure, not a feature.**
The authors' own summary: the only real difference they find is that **the TS approach misses
short-horizon return reversals** entirely. Cross-sectionally, a 1-month-ranked, 1-month-held
strategy earns *negative* momentum returns (i.e. reversal is real and cross-sectional); the
corresponding TS strategy shows positive returns — but only because the net-long term masks
the reversal. Measuring against zero instead of against the cross-section destroys the signal.

**On heterogeneous multi-asset sets, cross-sectional wins outright.** Applying the same
comparison to 55 futures markets across four asset classes, the authors show the standard
comparison in the TS literature is not like-for-like: an inverse-volatility-scaled TS strategy
takes far larger gross positions than an equal-weighted CS strategy (roughly $3.28 long and
$1.73 short for a 12-month-ranked scaled TS book, versus $1 long and $1 short for the
equal-weighted CS book) *and* carries a large positive net long. When the CS strategy is
scaled the same way, **the scaled CS strategy significantly outperforms the scaled TS
strategy**. Their stated reasons are differences in the asset-class composition of the two
books and CS's better ability to identify over- and under-valued bonds.

## Construction recipe

The comparison is the recipe, and all four constructions are worth having written down
because they differ only in the benchmark and the scaling:

- **Unscaled TS**: `w_i ∝ sign(R_{i,t−1})`, long side = equal-weighted portfolio of assets
  with positive ranking-period excess return, short side = the rest. Net investment floats.
- **Unscaled CS**: identical, except the threshold is the **cross-sectional mean** of
  ranking-period returns rather than zero. Net investment is zero by construction.
- **Scaled TS** (the time-series-momentum literature's standard): position in asset `i` is
  `sign(R_{i,t−1}) × 40% / σ_{i,t−1}`, averaged over `N` assets. `σ_{i,t−1}` is an
  exponentially weighted average of lagged squared daily returns with the weight centre of
  mass at 60 days, annualized. The 40% numerator is chosen because it is "similar to the risk
  of an average individual stock". Gross exposure therefore floats with the cross-section's
  volatilities and always exceeds $2 in their sample.
- **Scaled CS**: same cross-sectional mean threshold, then each asset weighted inversely
  proportional to `σ_{i,t−1}`, matched to the scaled TS book's gross exposure so the
  comparison is like-for-like.
- **CS TVM** (the diagnostic construction): CS plus a position in the equal-weighted index
  equal to the dollar difference between the TS book's long and short sides each month. This
  is the object to compare a TS strategy against — not raw CS.

Ranking and holding periods are swept jointly from 1 to 60 months in the US stock tests; the
notation `J × K` means J-month ranking, K-month holding.

## Robustness evidence (qualitative only)

- Multi-decade US sample (roughly seven decades of CRSP), restricted to non-micro-cap stocks
  so the result is not an illiquidity artifact — directly relevant to a large-cap universe.
- Independent multi-asset sample of 55 futures markets across four asset classes, ~three
  decades, constructed comparably to the canonical time-series-momentum dataset.
- The decomposition itself is an accounting identity plus a standard-error derivation
  (supplied in the appendix), so the *structural* claim — TS = CS + net long — cannot decay.
  What could decay is the empirical claim that the residual difference is economically nil.
- Methodology honesty is high: the paper's whole point is that a widely cited comparison was
  mis-specified, and it is careful to state the conditions under which each conclusion holds.
  It is a replication-style challenge from a tier-1 venue, published after the result it
  challenges.
- Note the direction of the disagreement in the literature: this paper does *not* say
  time-series momentum is absent. It says the *comparison* favouring TS over CS was
  confounded. That is a narrower and better-supported claim than the one in the
  Huang–Li–Wang–Zhou replication, and the two are complementary rather than duplicative.

## Implementability here

**This is the strongest reason yet recorded for the lab's cross-sectional construction, and it
converts one of the lab's own inferences into something with a source behind it — but not
all of it.**

1. **It answers the flagged open question, with one caveat.** `SUMMARY.md` recorded the lab's
   inference that magnitudes are incomparable across heterogeneous assets in a time-series
   setting but comparable cross-sectionally within one universe. This source supports the
   *conclusion* — on a heterogeneous multi-asset set, like-for-like scaled CS beats scaled TS
   — but attributes it to asset-class composition and bond selection rather than to magnitude
   comparability as such. So: the direction of the lab's inference is now corroborated by a
   tier-1 source, the *stated reason* is still the lab's. Do not cite this paper as proof of
   the magnitude-comparability story; cite it for the ranking, and for the structural fact
   that TS's benchmark (zero) carries a market bet that CS's benchmark (the cross-sectional
   mean) does not. **Nobody should "correct" the champion's magnitude weighting by citing
   MOP's sign-only rule** — that rule is answering a different question, against a different
   benchmark.

2. **A fifth, and possibly decisive, obstacle for long-only trend overlays.** The existing
   family-2 note lists four (long-short evidence, multi-asset diversification, intrinsic
   inverse-vol sizing, one-sided vol targeting). This source adds a cleaner one. A long-only
   trend overlay — "hold the asset if its own trailing return is positive, else hold cash" —
   *is* a time-series rule whose net long position varies between 0 and 1. Against a
   fully-invested cross-sectional book, which holds net long ≡ 1 always, the overlay cannot
   capture the risk-premium half of TVM; it can only **give some of it up**. Everything it
   could add is the market-timing covariance term — the smaller, statistically weaker piece,
   and the one that shrinks at exactly the 12-month ranking horizon this repo uses. That is a
   mechanism-level prediction that a long-only trend overlay should cost return and add little,
   which is precisely what the lab measured three times (200dma filter, SPY-trend switch,
   drawdown brake). Recorded as the sharpest statement of the anti-candidate.

3. **The reversal finding cuts the same way as the skip-month convention.** Because the TS
   benchmark is zero, a TS rule cannot see short-horizon reversal at all; cross-sectionally it
   is clearly present at the 1-month ranking horizon. Combined with the liquidity-provision
   note, this makes the champion's skip-month a doubly-supported choice: the recent month
   carries a real, cross-sectionally-measurable reversal whose economics are inventory
   absorption rather than mispricing.

4. **What is *not* portable.** Every construction here is long-short and several use leverage
   above 1. Nothing in this paper can be built as-is. Its value is entirely as a triage and
   interpretation tool: **before crediting any signal rule, ask what its benchmark is —
   zero or the cross-sectional mean — and if it is zero, decompose the resulting net-long
   drift out before comparing it to anything.** A long-only book's constant full investment is
   itself a permanent "net long" the literature's TS strategies are partly being paid for.

## Related

- `2026-08-17-time-series-momentum-evidence-and-replication.md` — the four existing obstacles
  to family 2; this note supplies a fifth and independent one, from a different angle
  (portfolio accounting rather than replication statistics).
- `2026-08-17-short-term-reversal-as-liquidity-provision.md` — the reversal that the TS
  approach cannot see; that note supplies its economics.
- `2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the CS construction whose overlapping
  tranche scheme the champion uses; same author lineage.
- `2026-08-17-momentum-horizon-echo.md` — skip-month convention, now supported from a third
  direction.
