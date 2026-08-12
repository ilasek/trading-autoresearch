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
  composition. Basket breadth (35/20) itself is still a free upgrade over
  the narrower 25/15 version — same Sharpe, lower turnover.
- **[Superseded below] A time-dimension de-risking lever finally solved the
  maxDD problem the sector/breadth axis couldn't — but only once cadence was
  fixed.** A basket-own realized-vol-spike trigger (trailing 21d vs 252d
  realized vol of the basket's own held names, ratio > 1.6 → cut exposure to
  0.6x) is mechanistically distinct from every previously-refuted de-risking
  overlay (those all used an *external* trend signal — 200dma, SPY-trend —
  which whipsawed because trend reversals are frequent in calm markets).
  Evaluated only at the monthly rebalance, it was a near no-op: it fired in
  just 19 of 513 months of history and only twice in the whole 2018-2023
  validation window, leaving maxDD identical to the untrimmed basket
  (-35.6%) because by month-end most of a fast crash (e.g. 2020-03) had
  already happened. Re-evaluating the *identical* trigger daily instead —
  composition/selection/weighting all still monthly, only the exposure
  scalar reacts faster — fixed this completely: validation Sharpe rose to
  1.05-1.07 (new best-ever, beating the untrimmed 1.03) *and* maxDD fell to
  -29.5%/-30.3%, better than the untrimmed basket's -35.6% *and* better than
  the champion's own -29.9%. This is the first mechanism in the repo to
  improve Sharpe and drawdown simultaneously, on both the widebreadth
  (20/35) and narrower (15/25) basket variants — confirming concentration
  level and the trim are independent, additive levers. **General lesson for
  any future overlay/regime idea: evaluate whether the trigger needs to
  react faster than the strategy's own rebalance cadence before concluding
  a mechanism doesn't work — a monthly-only check can make a genuinely
  sound crash-detection signal look like a no-op purely from reaction
  lag, distinct from the whipsaw failure mode of the earlier de-risking
  attempts.** One follow-up refuted: redirecting the trimmed capital into a
  fixed 50/50 TLT/GLD hedge instead of leaving it as cash made no
  improvement (same Sharpe, slightly worse maxDD and turnover) — cash is a
  cleaner, cost-free ballast for this trigger; bonds/gold were not reliably
  diversifying during the exact spike windows it fires on (e.g. the
  liquidity-driven 2020-03 selloff briefly hit most assets at once). The
  narrow-basket + daily-trim combination
  (`mom_zscore_narrow_daily_volspike_trim`, val Sharpe 1.07, maxDD -30.3%,
  DSR 0.9326) is the strongest challenger in the repo's history on every
  axis — Sharpe, drawdown, and DSR — future sessions should treat it as the
  new bar, not the champion's 0.865 or the earlier 1.03 escalation line.
- **The daily vol-spike trim's benefit is specific to the magnitude-weighted
  basket, not a general property of concentrated momentum baskets.** Applying
  the identical daily-reacting trim mechanism to the plain equal-weight
  buffered 12-1 basket (`mom_12m_daily_volspike_trim`) was a near no-op —
  Sharpe, maxDD, and turnover all landed within rounding of the untrimmed
  `mom_12m_buffered` numbers, because that basket's own realized vol rarely
  crosses the 1.6x spike threshold in the first place. The trim only earns
  its keep on baskets concentrated enough (via magnitude-weighting) to
  actually be vol-spiky. Future de-risking-overlay ideas should keep
  targeting the magnitude-weighted basket specifically.
- **A structurally different price-based signal (52-week-high proximity)
  was tried and refuted, closing that specific avenue.** Swapping the
  composite return-magnitude z-score for a composite z-score of nearness-
  to-52-week-high (same buffer/weighting mechanism otherwise) collapsed
  validation Sharpe to 0.35 and more than doubled turnover (7.0x -> 14.6x).
  The bounded (0,1] ratio clusters many names near 1.0 in bull markets, so
  small price wiggles flip buffer-band membership far more often than an
  unbounded z-scored return does — the mechanism that works well for return
  magnitude does not transfer to this alternative momentum proxy without
  first fixing the turnover blow-up (not attempted; would need a distinct
  rationale, e.g. a much wider band, not a parameter sweep). The "genuinely
  new signal source" direction remains open in principle but this specific
  naive construction is closed.
- **The DSR bar is now quantified: a candidate needs roughly validation
  Sharpe ≥ 1.17 to reach DSR 0.95 at 35 recorded trials, versus the best
  challenger's 1.07.** Computed directly from the protocol's own formula
  (`metrics.deflated_sharpe` + `probabilistic_sharpe`) rather than inferred
  from past verdicts, holding the validation window at its fixed 1562 days.
  Two consequences worth carrying permanently. (1) The gap that matters is
  ~+0.10 Sharpe over the best challenger, not over the champion's 0.865 —
  and the required level creeps up by roughly +0.01 per additional trial
  recorded, because each trial's Sharpe widens the dispersion term that
  sets the expected-maximum benchmark (`sr_max`, currently ≈0.50
  annualised). Sessions of small refinements make the bar recede about as
  fast as they approach it, which is exactly what trials #14-#35 show. (2)
  Higher moments barely matter: sweeping skew from -0.5 to +0.5 and
  kurtosis from 5 to 8 moves DSR by under 0.01 at these Sharpe levels, so
  there is no point engineering return-shape (smoother equity curves,
  positive-skew overlays) to clear the bar — only raw validation Sharpe
  moves it materially. Any future session should size its ambition against
  the ~1.17 number before spending a trial.
- **Everything that tilts capital or ranking away from the highest
  raw-return, higher-beta names loses on this universe — now five distinct
  refutations, including beta-residualisation.** Inverse-vol basket
  weighting, standalone low-vol tilt, the low-vol double sort, square-root
  dampening of the weight spread, and (newest) replacing total-return
  momentum with market-residual momentum all reduced validation Sharpe;
  every mechanism tilting *toward* those names has gained. Residual
  momentum is the sharpest version of the test because the literature
  (Blitz/Huij/Martens) predicts the opposite: here it cut validation
  ann_return 27.0% -> 22.3% while barely moving vol (25.4% -> 25.0%), so
  Sharpe fell 1.07 -> 0.93 and both validation and train maxDD *worsened*.
  Two reasons, both universe-specific: on a survivorship-biased set of
  today's global mega-caps the beta-loading component is a large part of
  where the realised momentum payoff actually came from, and the "market"
  proxy available here (equal-weight mean of US/JP/HK single stocks plus
  bond, gold and EM ETFs) is too heterogeneous to give clean betas. Treat
  signal-level de-beta / risk-normalisation as closed absent a genuinely
  better market factor — including the residual-vol-normalised (t-stat)
  variant, which sits on the same axis.
- **Monthly selection cadence is a genuine interior optimum, and turnover
  reduction is not a lever on this strategy.** Moving the rebalance grid
  faster (weekly) and slower (quarterly), each as a single change to the
  best challenger, both lost — weekly 0.99 and quarterly 1.01 versus
  monthly's 1.07 — and the two failed by opposite mechanisms, which is what
  makes the optimum real rather than a cost artifact. Weekly *selected
  worse*, not just more expensively: about half its 2.7pp return loss
  survives after netting out the extra turnover, because at weekly
  frequency the ranking near the buffer edges is driven by short-horizon
  price noise that a month-end snapshot averages through. Quarterly did
  deliver its promised cost saving (turnover 7.3x -> 4.2x, worth ~+0.5pp of
  annual return) and still lost 1.6pp of return, i.e. the staleness cost of
  a 3-month-old ranking is about three times the saving — and train maxDD
  blew out from -54.7% to -65.4% because a stale basket rides straight
  through the fast momentum crashes in the pre-2018 history. General form:
  match each mechanism's evaluation cadence to the timescale of the
  phenomenon it measures (fast for a vol-regime break, monthly for a 6-12
  month trend), not to the strategy's rebalance grid in either direction.
  Corollary: the best challenger's ~7.3x turnover costs ~1.1pp of annual
  return, but no turnover-reduction idea that changes effective holdings
  has ever paid for itself here — do not pursue more of them.
- **The exposure-scaling family is capped at about +0.04 Sharpe, whatever
  its functional form.** Textbook continuous constant-volatility targeting
  (25% annualised target, daily, quantised, capped at 1.0 since the engine
  forbids leverage) was finally tested cleanly — the earlier
  `mom_invvol_target` had confounded it with inverse-name-vol weighting at
  monthly cadence — and tied the binary vol-spike trim: validation Sharpe
  1.073 vs 1.066, both up from 1.028 with no overlay at all. They reach the
  same ratio by different routes (the binary trim dodges drawdowns and
  leaves vol at 25.4%; continuous targeting grinds vol to 23.4% and gives
  up return to get there), and continuous costs more turnover (8.1x vs
  7.3x). Once a vol overlay reacts daily, its shape is second-order: do not
  spend further trials on functional-form, threshold or target-level
  variants of exposure scaling.
