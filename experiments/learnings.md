# Distilled Learnings

Read this before proposing any hypothesis. Add to it when a pattern repeats
across experiments; prune entries that later evidence contradicts.

## Data & methodology caveats (permanent)

- **Survivorship bias**: the universe is today's constituents. Single-stock alpha
  (especially momentum/quality tilts on stocks) will look better than it was.
  ETF-level strategies are the most trustworthy results in this repo.
- **Free daily data**: Yahoo-adjusted closes; no intraday, no fundamentals, no
  point-in-time constituents. Costs are modeled at 15 bps/side — strategies whose
  edge dies below ~30 bps round-trip are not robust here.
- **Every trial raises the bar**: the deflated-Sharpe benchmark grows with the
  trial count in `experiments/trials.jsonl`. Sweeping parameters wastes shared budget —
  test ideas, not knobs.

## Strategy learnings (append below)

- **De-risking overlays on momentum reliably backfire out-of-sample.** Three distinct
  attempts to fix the champion's 2008-09 momentum-crash drawdown — inverse-vol basket
  weighting + vol targeting, per-asset 200dma trend filtering on an ETF sleeve, and a
  binary SPY-trend regime switch — all cut the *train-period* drawdown substantially
  but lost more validation Sharpe than they saved (0.71, 0.51, 0.51 vs champion's
  0.86), mostly via diluted upside or whipsaw turnover. Any future crash-mitigation
  idea should be judged on its own out-of-sample turnover/whipsaw cost, not just its
  in-sample crash-period behavior.
- **Standalone diversified ETF sleeves cap out well below the champion.** Static
  equal-weight (0.49 Sharpe) and true inverse-vol risk parity (0.35 Sharpe) on the
  same ~10-asset global sleeve both underperform — risk-weighting even did *worse*
  than capital-weighting here, because it overweights low-return bond legs. This is
  now a fairly well-established floor: pure asset-class diversification without a
  return/momentum signal is not competitive on this universe.
- **Blending beats switching.** The one near-miss so far: holding the ETF sleeve
  *alongside* momentum (80/20 capital blend, always on) came within 0.015 Sharpe of
  the champion while also improving both train and validation max drawdown — better
  than any gate/switch/reweight attempt. Combination-family ideas that keep both
  legs always-on and let low correlation do the work look more promising than
  regime-timing the allocation.
- **Low-vol stock tilt is refuted, standalone and as a within-momentum filter.**
  Bottom-quintile trailing-vol stocks alone (val Sharpe 0.69) and lowest-vol names
  *within* the top-momentum quintile (val Sharpe 0.64, worse than either alone) both
  underperform the champion. The double-sort mechanism actively hurts: filtering a
  high-momentum pool by low vol discards the pool's strongest compounders (the
  highest-conviction, often higher-vol names) in favor of the weakest names that
  barely qualified. Treat the whole low-vol family as closed on this universe absent
  a genuinely different vol construction (e.g. sector-neutralized, not raw trailing).
- **Inverse-vol / risk-weighting between sleeves of unequal diversification always
  favors the more-diversified (lower-return) leg.** Confirmed twice now:
  `risk_parity_multi_asset` (inverse-vol across a 10-ETF sleeve underweighted the
  return-carrying equity/EM/commodity legs, 0.35 Sharpe) and `mom_etf_volweighted_blend`
  (inverse-vol weighting between the 15-stock momentum basket and the 10-ETF sleeve
  handed the ETF sleeve the majority of capital on average — not just during
  turbulence — cutting the fixed-80/20 blend's 0.85 Sharpe down to 0.76). A
  concentrated basket is structurally higher-vol than a diversified one almost
  regardless of its return quality, so naive inverse-vol comparison between sleeves
  of different concentration is not a sound weighting mechanism here. Fixed-ratio
  blending remains the better mechanism than any vol-based reweighting tried so far.
- **Buffered momentum (hysteresis band on basket membership) is the strongest lead
  in the repo, superseding the momentum+reversal blend below.** Replacing the
  champion's hard top-15 monthly cutoff with an asymmetric buffer (hold while
  ranked in the top 25, enter only in the top 15 — standard practice for cutting
  momentum-strategy turnover) beat the champion outright on *both* axes at once:
  validation Sharpe 0.90 vs 0.865, and turnover 4.4x vs the champion's own 5.8x
  (`mom_12m_buffered`, trial #17). It was still REJECTed only on the deflated-Sharpe
  bar (0.9019 < 0.95), but by a smaller margin than any prior challenger. Two
  follow-ups the same night both did *worse* than this standalone version: adding
  the short-term-reversal leg back (`mom_str_reversal_buffered`, 0.88 val Sharpe)
  and blending in the diversified ETF sleeve (`mom_buffered_etf_blend`, 0.88 val
  Sharpe) — both diluted capital away from the buffered leg for a smaller gain than
  it cost. This reframes the earlier momentum+reversal blend finding below: most of
  its apparent edge over plain momentum likely came from indirectly absorbing some
  of momentum's own turnover-inefficiency, not from real diversification benefit —
  once that inefficiency is fixed directly via buffering, the reversal leg actively
  subtracts value. Future sessions should treat unblended buffered momentum as the
  candidate to beat, not a base to blend further; any new idea should be judged
  against its 0.90 validation Sharpe, not the champion's 0.865.
- **[Superseded by the finding above, kept for context] Momentum + short-term
  reversal blend** — two independent constructions (two-basket 80/20 blend and a
  composite z-score) both landed at validation Sharpe ~0.87, the first candidates
  to beat the champion's raw validation Sharpe, both REJECTed only on the DSR bar.
  Do not pursue further variants of this specific blend — the buffered-momentum
  finding above suggests its edge was mostly a turnover-inefficiency artifact.
- **The DSR multiple-testing bar effectively requires one large single-step jump,
  not several trials of incremental gains.** Across trials #14-18, validation Sharpe
  climbed from 0.865 (champion) to 0.87, 0.87, 0.88, 0.90, 0.88 while DSR probability
  moved only 0.9043 → 0.9004 → 0.9004 → 0.9019 → 0.8905 — each additional trial's
  own bar-raising effect roughly cancels a modest Sharpe improvement. A candidate
  needs to clear the champion by significantly more than ~0.035 Sharpe (the biggest
  gap achieved so far) to have a real shot at PROMOTE at the current trial count;
  don't expect a string of small refinements to eventually cross 0.95.
- **Capital dilution has a roughly constant Sharpe cost regardless of the base
  leg's quality.** Blending 20% capital into the ~0.5-Sharpe diversified ETF sleeve
  cost about the same ballpark of Sharpe whether the other 80% was plain momentum
  (`mom_etf_blend`: 0.865 → 0.85) or buffered momentum (`mom_buffered_etf_blend`:
  0.90 → 0.88) — the dilution tax doesn't shrink as the diluted leg improves, so
  blending becomes relatively less attractive the better the core signal gets.
- **Within-basket weighting scheme, not just membership/buffering, is a major
  untapped lever — and the direction matters.** Three trials in one session,
  each isolating a single change on top of `mom_12m_buffered`'s identical
  basket membership, climbed validation Sharpe 0.90 → 0.93 → 0.98 → 1.03:
  equal-weight → linear rank-weight → z-score-magnitude-weight → z-score-
  magnitude-weight on a 6-1/12-1 composite signal. Each step tilts *more*
  capital toward the strongest-momentum names in the held basket — the
  mirror image of the refuted low-vol/inverse-vol findings above, which
  tilted capital *away* from them. DSR probability climbed alongside it
  (0.9019 → 0.9083 → 0.9252 → 0.9333, the best-ever DSR in the repo) but the
  per-trial DSR gain shrank on the last step even as the Sharpe gain didn't,
  and validation maxDD widened in lockstep with each step (-30.2% → -32.4% →
  -36.0%, closing in on the -45% gate) — a real risk cost, not a free lunch.
  A follow-up square-root dampening of the weight spread (same basket, same
  ranking, only less concentrated) tested whether trading some Sharpe for
  lower variance would raise DSR further — it did not: Sharpe fell to 0.98
  and DSR *dropped* to 0.9155, worse than the undamped version. This settles
  that the magnitude-weighting gain is closer to real signal than to a
  variance/convexity artifact of concentration, at least in the direction
  and strengths tested. `mom_multihorizon_zscore_buffered` (val Sharpe 1.03,
  DSR 0.9333, trial #21, unpromoted) is the strongest challenger ever
  recorded here. Future sessions should not further escalate concentration
  on this same signal (a fourth horizon, a steeper transform) without a new
  rationale — that's now a well-explored, partially-refuted direction
  (escalation works, dampening doesn't) — but a structurally different idea
  building on undamped magnitude-weighting, or simply patience for the DSR
  bar to become clearable, are both reasonable next steps.
- **The best challenger's rising validation maxDD is not a diversification
  problem — it survives both sector-neutral scoring and much wider basket
  breadth unchanged, closing that whole axis.** Following up on the
  drawdown-widening concern above, one session tested two structurally
  distinct diversification fixes on `mom_multihorizon_zscore_buffered`
  (val Sharpe 1.03, maxDD -36.0%) without touching its weighting mechanism:
  neutralizing the composite z-score within coarse sector/asset-class groups
  cost far more Sharpe (1.03 → 0.87) than the drawdown it saved (-36.0% →
  -32.3%) and even raised turnover (7.0x → 7.8x); separately, widening the
  basket from hold-25/enter-15 to hold-35/enter-20 left maxDD essentially
  unchanged (-35.6%) while matching Sharpe (1.03) and cutting turnover
  (7.0x → 6.5x). Both results point the same direction: the basket's
  drawdown growth is not caused by too few names or excess sector
  concentration — global top-momentum names already span sectors reasonably
  well, and adding more of them doesn't dilute the risk either. The driver
  is more likely inherent to the magnitude-weighting mechanism itself (or
  the underlying momentum signal's tail behavior in a crash), not basket
  composition. Treat the sector/breadth axis as closed for this specific
  problem; a future attempt at trimming this basket's drawdown should act on
  the signal or time dimension instead (e.g. a regime-conditional trim that
  only engages during identifiable extreme periods, distinct from the
  already-refuted always-on de-risking overlays). Basket breadth (35/20)
  itself is still a free upgrade over the narrower 25/15 version — same
  Sharpe, lower turnover — worth adopting as the base for any future variant
  of this basket even though it didn't solve the drawdown question.
