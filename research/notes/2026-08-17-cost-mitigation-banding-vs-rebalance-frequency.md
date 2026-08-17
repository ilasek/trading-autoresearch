---
title: "A Taxonomy of Anomalies and Their Trading Costs" + "Comparing Cost-Mitigation Techniques"
authors: Novy-Marx, Velikov
year: 2016, 2019
venue: Review of Financial Studies (venue tier 1); Financial Analysts Journal (venue tier 1 practitioner-academic; 2019 Graham & Dodd Scroll Award)
url: https://academic.oup.com/rfs/article/29/1/104/1844518 ; https://doi.org/10.1080/0015198X.2018.1547057
citations: not verified this session (all scholar APIs and publisher domains egress-blocked; see SUMMARY tooling note)
sample_period: 1963-07 – 2012-12 (RFS paper; the FAJ paper uses the same CRSP/Compustat + TAQ machinery, exact end date not verified)
markets: US equities (CRSP/Compustat universe; TAQ-based effective-spread cost estimates)
tier: A
validation_overlap: false
published_post_2018: mixed — RFS 2016 false, FAJ 2019 true (publication date only; sample is pre-2013)
---

## Mechanism

The object of study is not a signal but the **gap between a strategy's gross and net
performance**, and how construction choices move that gap. Cost drag is turnover × per-trade
cost, so every cost-mitigation technique works by cutting turnover or by cutting the cost of
the trades that remain. The paper's contribution is that these techniques are **not
interchangeable**: they buy the same cost saving at very different prices in signal exposure.

Three techniques are compared:

1. **Restrict the universe to cheap-to-trade securities** — screen out small, illiquid names.
   Cuts the per-trade cost term directly, but discards part of the cross-section, and in the
   US anomaly literature that discarded part is where much of the gross spread lives.
2. **Reduce rebalance frequency / staggered partial rebalancing** — trade the book less often
   (or trade only a slice of it per period). Cuts turnover, at the price of holding a signal
   that is on average staler.
3. **Banding (a "buy/hold spread")** — impose a *stricter* requirement to establish a position
   than to maintain one, so a name is bought only on a strong signal but is kept while its
   signal is merely acceptable. Cuts turnover by suppressing round-trips near the selection
   threshold, where the signal is weakest and the marginal information content of a swap is
   lowest.

The economic argument for banding being the best of the three: the trades it eliminates are
precisely the ones with the least signal content per dollar of cost, whereas frequency
reduction eliminates trades indiscriminately (including high-conviction ones) and the
liquidity screen removes gross return at the source. Stated in the FAJ paper's own terms:
banding yields similar trading-cost reductions to frequency reduction **while maintaining
better exposure to the underlying signal**.

## Construction recipe

- **Banding / buy/hold spread.** Two thresholds instead of one. Enter only if the name ranks
  inside the strict cutoff (say the top X of the score distribution); hold while it ranks
  inside the loose cutoff (top Y, Y > X); exit only when it falls outside Y. Membership
  therefore becomes path-dependent — a name's presence depends on whether it was already
  held — which is the entire point: it is what removes the churn of names oscillating around
  a single cutoff.
- **Staggered partial rebalancing.** Rather than reforming the whole book on a slower clock,
  reform a fixed fraction of it on the original clock. Their calibration: mid-turnover
  strategies are rebalanced quarterly (the convention used by AQR's momentum indices); for
  high-turnover strategies where the signal decays too fast for a quarterly clock, the
  strategy is run twice as fast with staggered rebalancing at a half-quarterly frequency —
  i.e. cadence is matched to signal persistence, not chosen for its own sake.
- **Liquidity screening.** Restrict to the large/liquid part of the cross-section before
  sorting.
- **Turnover as the design constraint.** Their empirical summary of when cost-aware design can
  rescue an anomaly at all: anomalies with **less than ~50% turnover per month** generally
  generate significant net spreads when designed to mitigate costs; few above that threshold
  do. (Sample-average execution-cost estimates for mid-turnover anomaly strategies land in the
  tens of basis points per trade — a cost level, not a return figure.)

## Robustness evidence (qualitative only)

- Broad rather than deep: the taxonomy paper applies one uniform cost model across a large
  catalogue of published anomalies, so the ranking of techniques is not a single-strategy
  result. That breadth is its main robustness claim.
- Costs are estimated from actual quoted/effective spreads rather than assumed, and the
  authors publish the machinery — this is the methodology-honesty end of the literature, not
  the frictionless end.
- The FAJ companion is peer-reviewed and award-recognised, and its finding (turnover-reducing
  techniques dominate liquidity screening; banding dominates frequency reduction) is a
  comparison run inside one consistent framework rather than assembled across papers.
- Known limits: US-only, one cost regime, and every headline object is a **long-short decile
  spread**. Nothing here is evidence about a long-only book except by inheritance through the
  long leg.

## Implementability here

This is the closest thing in the literature so far to a direct account of the repo's two
live construction mechanisms, and it grades them against each other.

1. **The buffer is the literature's preferred technique, and for the reason the lab observed.**
   The champion's hold-25/enter-15 (and the wider 35/20) band *is* a buy/hold spread. The lab
   found it beat a hard cutoff on both Sharpe and turnover at once; this source supplies the
   mechanism — the suppressed trades are the low-information ones near the cutoff — and the
   comparative claim that this beats simply slowing the clock. Worth recording because it
   means the buffer is not a repo-specific trick.

2. **The liquidity-screen technique is already fully spent here, structurally.** This repo's
   ~145 instruments are large liquid global stocks and ETFs at a flat 15 bps/side. In the
   paper's terms the universe *is* the cheap-to-trade screen, taken to its limit. So of the
   three techniques, one is unavailable (already applied), one is the buffer (applied), and
   one is cadence (applied via monthly formation). There is no fourth lever in this source.
   Combined with the learnings entry that turnover reduction is now a spent lever on the
   overlapping-tranche base (~0.019 Sharpe of total cost drag at 3.0x), **the whole
   cost-mitigation literature should now be read as closed for this repo, not as idea supply.**
   Its remaining value is explanatory, not generative.

3. **Explicit tension worth flagging to the strategy agent.** This source models slower/
   staggered rebalancing as buying cost reduction *at the price of signal staleness* — a real
   tax, which is why it ranks below banding. The lab measured the opposite on its own
   universe: pruning tranches back to names the current signal still endorses cost Sharpe,
   drawdown and turnover simultaneously, and the six-tranche book earns more than the
   single-vintage one, so there was no staleness tax to reclaim. These are not contradictory
   — the paper measures staggering as a *substitute* for a full rebalance (one book, traded
   less), whereas the lab's overlap holds **several formation vintages at once** (one book per
   vintage, averaged), which is a different object: it adds temporal breadth rather than
   merely subtracting trades. Do not let this source's ranking (banding > frequency reduction)
   be read as evidence against the overlap; it is a claim about a different construction.

4. **Turnover-threshold sanity check.** The <50%/month rule of thumb is a useful external
   marker: the champion's ~3.0x annual turnover is far inside it, and even the pre-overlap
   7.3x line was. The repo has never been in the region where this literature says costs kill
   an effect — consistent with the lab's own conclusion that cost was never the binding
   constraint on this line.

Pitfalls: do not import the cost magnitudes (US small-cap-inclusive spreads are much wider
than this universe's), and do not import any net-spread ordering of anomalies — those are
long-short decile results on a cross-section this repo does not have.

## Related

- `2026-08-17-rebalance-timing-luck-tranching.md` — the other half of the rebalance-mechanics
  literature: what staggering across dates does to outcome *dispersion*, as opposed to cost.
- `2026-08-17-jegadeesh-titman-overlapping-momentum.md` — the overlapping-vintage construction
  itself, and why its original motivation was statistical rather than economic.
- `experiments/learnings.md`: "Buffered momentum (hysteresis band on basket membership) is the
  strongest lead in the repo" — this source is its literature grounding; and "Turnover
  reduction is now a spent lever", which this source's technique list corroborates by
  exhaustion.
