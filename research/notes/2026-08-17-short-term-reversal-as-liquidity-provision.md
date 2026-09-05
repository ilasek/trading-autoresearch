---
title: "Evaporating Liquidity" (primary) with "Fads, Martingales, and Market Efficiency" and "When Are Contrarian Profits Due to Stock Market Overreaction?"
authors: Nagel (2012); Lehmann (1990); Lo, MacKinlay (1990)
year: 2012, 1990, 1990
venue: Review of Financial Studies 25(7), 2005–2039 (venue tier 1); Quarterly Journal of Economics 105(1), 1–28 (venue tier 1); Review of Financial Studies 3(2), 175–205 (venue tier 1)
url: https://doi.org/10.1093/rfs/hhs066 ; https://doi.org/10.2307/2937816 ; https://doi.org/10.1093/rfs/3.2.175
citations: Nagel (2012) 468 (Semantic Scholar, checked 2026-08-17); Lehmann (1990) 1621 (OpenAlex, checked 2026-08-17); Lo–MacKinlay (1990) 1891 (Semantic Scholar, checked 2026-08-17)
sample_period: Nagel 1998–2010 (start set at 1998 deliberately, to exclude the Nasdaq order-handling-rule change); Lehmann and Lo–MacKinlay use CRSP weekly data ending in the mid-1980s
markets: US equities (CRSP), individual stocks and value-weighted industry portfolios
tier: A
validation_overlap: false
published_post_2018: false
---

## Mechanism

This is the first dedicated source for `program.md` family 4, and its central contribution is
to say **what the short-term reversal premium is payment for** — which turns out to settle the
implementability question at the mechanism level rather than by turnover arithmetic.

**Reversal profits are the market-making spread, viewed from the other side.** When a large
uninformed order arrives, the market-making sector absorbs it and demands compensation for
taking the resulting inventory. The price moves away from fundamentals to induce that
absorption and reverts as the inventory is worked off. A contrarian strategy that buys
whatever fell over the last few days and sells whatever rose is, mechanically, supplying that
absorption capacity. So the return to a short-horizon reversal strategy is a **proxy for the
return to liquidity provision**, and it is priced accordingly.

Two consequences follow directly, and they are the reason this note matters more than a
generic "reversal exists" finding:

1. **The premium is strongly time-varying and predictable by market stress.** The expected
   return to reversal strategies rises sharply and predictably with the VIX, and it rises
   *faster than the strategy's volatility does*, so conditional Sharpe ratios rise with stress
   too. The interpretation is a supply story rather than a demand story: in turmoil,
   intermediaries are capital-constrained and less willing to warehouse inventory, so the
   price of liquidity goes up. This is what "liquidity evaporates" actually means in the
   paper's reading — not that trading stops, but that the required return for providing
   liquidity spikes.
2. **The effect is not confined to individual stocks.** A reversal strategy built from
   long-short positions in **value-weighted industry portfolios** — which earns essentially
   nothing unconditionally — also earns high returns and high Sharpe ratios when the VIX is
   high. That says liquidity providers are compensated for absorbing *common, industry-level*
   order imbalances, not only idiosyncratic single-stock ones. It is the one part of the
   result that speaks to an ETF-scale universe.

Nagel also documents that the premium is largest among small, illiquid, high-volatility
stocks, but is present even among the largest, most liquid, lowest-volatility names — a
pervasive phenomenon with a strong illiquidity gradient.

**Lo–MacKinlay supply the necessary correction to the naive story.** Contrarian profits do
*not* require overreaction, and are not mostly own-stock mean reversion. Even with temporally
independent individual security returns, a contrarian portfolio rule can earn positive
expected profits through **cross-autocovariances** — lead-lag relations where some stocks'
returns predict others'. Their evidence points against overreaction as the primary source and
documents important lead-lag structure. The practical import: the reversal signal is only
partly a statement about the stock you are trading; a large part of what a contrarian book
harvests is cross-sectional lead-lag, which is a different object with different capacity and
different decay.

**Lehmann established the base result** — winners and losers over one week reverse the next in
a way that yields apparent arbitrage profits, and (his claim) profits that persist after
correcting for bid-ask spreads and plausible transaction costs of that era. This sits in
tension with the liquidity-provision reading and the tension is worth stating plainly rather
than smoothing over; see *Robustness* below.

## Construction recipe

The canonical constructions across these sources share one shape: **zero-cost, cross-sectional,
weights proportional to the negative of the recent return measured relative to a benchmark,
rebalanced at the signal's own (very short) horizon.**

Nagel's daily version, stated precisely because it is the one with the mechanism attached:

- Each day `t`, form five separate reversal strategies, indexed by lag `k = 1..5`. Strategy
  `k` weights each stock proportional to the **negative of its market-adjusted return on day
  `t−k`**.
- Scale weights so each strategy is $1 long and $1 short (zero net investment). The headline
  series is the equal-weighted average of the five.
- Rebalance **daily**. Returns are computed from daily closing transaction prices; a
  quote-midpoint version is also constructed, and both are predictable with the VIX, though
  the transaction-price version more strongly so.
- Optionally hedge conditional market-factor exposure — this barely moves mean return but
  meaningfully lowers volatility, i.e. market beta is a large share of an unhedged reversal
  book's variance.
- The aggregated variant replaces individual stocks with **value-weighted industry portfolios**
  as the basis assets, same weighting rule.

Lehmann's version is the same shape at **weekly** horizon: rank on the past week's return
relative to the cross-sectional mean, weight against it, hold one week.

The conditioning variable, if the time-variation is to be exploited: **VIX**, used as a
predictor of next-period reversal returns, not as a filter on the cross-section. Nagel is
explicit that VIX is unlikely to be the state variable itself — it proxies for
intermediary risk-bearing capacity and public liquidity demand, which are hard to observe
separately.

## Robustness evidence (qualitative only)

- **Replication and pedigree.** All three are tier-1 peer-reviewed with citation counts in the
  hundreds to near two thousand. Short-term reversal is one of the least contested anomalies
  in the literature at the *statistical* level; the entire live debate is about whether it is
  net of costs an anomaly at all or simply the market-making margin.
- **Sample honesty in the primary source.** Nagel sets his sample start deliberately to exclude
  a known institutional break in Nasdaq order-handling rules that sharply changed spreads, and
  carries an explicit control for the later decimalization change. That is unusually careful
  treatment of microstructure regime shifts, and it is a reminder that this effect's magnitude
  is a function of the trading regime in a way momentum's is not.
- **Downside behaviour.** Reversal returns in the primary source are positively skewed, and the
  well-known August-2007 quant-crisis episode — in which a similar strategy lost sharply and
  transiently — is characterised as exceptional rather than typical. So the risk story for this
  family is *not* fat left tails in normal times; it is that the losses arrive concentrated in
  exactly the episodes when the strategy's leverage is largest.
- **The honesty caveat that dominates everything else.** The primary source's headline returns
  are explicitly **before the costs of carrying out the trades**. For a strategy that
  rebalances a full long-short book daily, that is not a minor omission — it is the whole
  question, and the paper does not claim otherwise. Its contribution is the *economics* of the
  premium, not a net-of-cost investability claim.
- **The Lehmann tension, recorded not resolved.** Lehmann's abstract claims profits survive
  bid-ask corrections and plausible costs; the liquidity-provision mechanism implies the
  profit *is* the spread. These are reconcilable — a weekly rebalance trades far less than a
  daily one, and his sample sits in a pre-decimalization, wide-spread era whose gross reversal
  magnitudes were correspondingly larger — but the reconciliation is inference, not something
  any source read here states. Lehmann's full text was not machine-readable in this session;
  the claims attributed to it come from its published abstract and from the primary source's
  description of the standard construction, and should be treated as second-hand.

## Implementability here

**Verdict: family 4 should be treated as closed on this repo's constraints, and for a better
reason than the turnover gate.** The lab already knows reversal blends underperform
empirically (`learnings.md`: the momentum+short-term-reversal blend's apparent edge turned out
to be absorbed turnover-inefficiency, and adding the reversal leg back to the buffered basket
actively subtracted value). This source supplies the mechanism for *why*, and it is decisive:

1. **The strategy earns the spread, and this repo pays the spread.** The premium is
   compensation for supplying liquidity. An implementation that rebalances at 15 bps/side of
   modeled cost is, by construction, **demanding** liquidity — taking the losing side of the
   exact trade the premium pays for. This is not a "costs are high, tune the turnover" problem
   that a wider band or a slower rebalance could fix; it is a sign problem. The only
   constructions that harvest it are ones that can post rather than take, which this repo
   structurally cannot model.
2. **The horizon is fundamentally incompatible with the cost model.** The mechanism operates
   at a 1–5 day horizon; inventory reverts over days, and holding longer means holding
   something the signal no longer describes. Daily rebalancing of a full book at 30 bps
   round-trip is not survivable given `learnings.md`'s own accounting (the champion's *entire*
   cost drag at 3.0× turnover is ~0.019 Sharpe; a daily reversal book runs turnover two orders
   of magnitude higher).
3. **Long-only removes most of the object.** All three sources study zero-cost long-short
   books. A long-only reversal tilt keeps only the "buy what fell" leg, which is a large
   market-beta bet with a weak overlay, not liquidity provision.
4. **The one structurally attractive variant is conditional and the lab has ruled out its
   trigger class.** The industry-portfolio version is ETF-scale and therefore the least
   survivorship-contaminated form available here — but it earns nothing unconditionally and
   pays only in high-VIX states. That makes it a **regime overlay**, and the lab's record on
   overlays is four refutations plus one narrow survivor, with two hard cadence lessons (the
   trigger must react faster than the rebalance; the release must not be slower than the
   recovery). A VIX-conditioned reversal sleeve would have to clear both, plus the cost
   problem in (1), and would be trading exactly when spreads are widest — the moment the
   modeled flat 15 bps is least defensible.

**The one genuinely useful transfer is not a strategy but a warning about the champion.**
Lo–MacKinlay's cross-autocovariance result says a portfolio built on recent relative returns
harvests lead-lag structure between names, not only own-stock dynamics. The lab's own skip-month
convention exists because of this family, and both echo-literature sources already agree the
most recent month carries reversal. This source explains the *economics* of why that month is
different: it is contaminated by the inventory-absorption cycle, which is a different
data-generating process from momentum's, operating on the opposite sign. Recorded so nobody
"simplifies" the skip-month away on the grounds that it merely discards information.

## Related

- `2026-08-17-momentum-horizon-echo.md` — the skip-month convention; that note establishes
  *that* the recent month reverses, this one supplies *why*, and the two agree.
- `2026-08-17-cost-mitigation-banding-vs-rebalance-frequency.md` — the cost-mitigation
  techniques enumerated there cannot rescue this family, because the problem is which side of
  the spread the strategy is on, not how often it trades.
- `2026-08-17-cross-sectional-vs-time-series-construction.md` — records the finding that a
  time-series (own-return) rule *misses* short-horizon reversal entirely, which is one more
  reason this effect is inherently cross-sectional.
- **[Added 2026-09-05] `2026-09-05-contrarian-profit-decomposition.md` is now the canonical
  record of Lo–MacKinlay (1990)**, one of this note's three clustered sources. That note carries
  the *identity* — `E[pi(k)] = C_k + O_k − sigma2_mu` — which this note does not, and which is the
  only implementable part of the paper. This note keeps the reversal-family reading and is not
  superseded; go there for the algebra, the asymmetry test, and the survivorship term.
  `2026-09-05-cross-serial-correlation-as-restatement.md` is the rebuttal that must be read with it.
- Contradiction check against `experiments/learnings.md`: no tension. The lab's two reversal
  results (blend superseded, reversal leg subtracts value on the buffered basket) are what this
  mechanism predicts for a cost-paying long-only implementation.
