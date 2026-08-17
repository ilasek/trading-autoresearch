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
  naive construction is closed. **Update (2026-08-16): the archived sessions
  closed this direction much harder — see the off-branch note below. After
  52-week-high proximity, residual momentum (twice), and information
  discreteness all landed at or below the base construction, treat "find a
  better score" as heavily explored and low-yield; the open axes are
  portfolio construction and rebalance mechanics, not signal definition.**

- **NOTE ON PROVENANCE: several of the strongest results below were first
  found in the four off-branch sessions of 2026-08-12..15 (see the
  `## Protocol issue — 2026-08-16` journal entry, and the `archive/nightly-*`
  annotated tags).** Those sessions' DSR numbers are invalid — each was
  computed against a 31-trial bar its own session could not know was stale.
  Their *mechanisms* are still real findings, but no number from them may be
  quoted as established until re-run through `run_experiment.py` on `main`.
  One such re-run has now been done (overlapping tranches, trial #32, below);
  the rest have not. Also note the standing bias in the other direction:
  `main`'s recorded trial count understates the true number of candidate
  strategies attempted across all sessions (34 recorded vs 53 attempted as
  of tonight), so every DSR scored on `main` is somewhat *generous* relative
  to the real multiple-testing burden. A borderline PROMOTE should be read
  with that in mind.

- **Overlapping formation tranches are the strongest mechanism in the repo,
  and the reason they work is not the one they were found for.** Instead of
  reforming the whole book each month, hold K = 6 overlapping tranches: the
  live book is the average of the six most recent monthly target-weight
  vectors, so only ~1/6 of capital is recommitted per month. Signal, buffer,
  magnitude weighting and daily vol-spike trim all untouched — only *when*
  capital commits changes. Verified on `main` (trial #32): validation Sharpe
  **1.11**, ann_ret 26.9%, maxDD -29.1%, turnover **3.0x** (versus the
  identical non-overlapping basket's 1.066 / -30.3% / 7.3x), DSR **0.9341** —
  the highest deflated-Sharpe probability ever recorded on `main`, and rising
  despite the extra trials in the deflator, which is the signature the gate
  needs. Higher return at less than half the turnover means **cost drag, not
  signal decay, was the binding constraint on this whole line.** The original
  framing — "a cheaper implementation of the same signal" — is now known to be
  wrong, see the next entry.

- **Holding names the current signal has already rejected is the overlap's
  active ingredient, not a tolerated side-effect.** A diagnostic on the
  weight matrix showed 20.6% of average validation book weight (max 55%)
  sits on names outside the current buffered held-set entirely. Pruning that
  stranded capital — masking each live tranche to the current held-set and
  renormalising, so tranche lifetime becomes conditional on the signal still
  endorsing its picks — cost on every axis at once: Sharpe 1.11 → 1.02,
  maxDD -29.1% → -30.9%, turnover 3.0x → 4.6x, and average positions
  collapsed 34.2 → 18.6. Pruning reverts the six tranches onto near-identical
  name sets, destroying the **temporal breadth** that no contemporaneous
  selection rule can reproduce, because every contemporaneous rule picks from
  a single month's ranking. This also explains why six-month-stale signals
  cost zero return: there is no staleness tax, so a pruning rule had nothing
  to win. Closes the tranche-lifetime axis in the conditional direction, and
  closes a loop with two earlier results — nominal breadth widening was a
  no-op on maxDD, and halving per-tranche size gave the drawdown gain back.
  **Breadth only pays when it comes from decorrelated formation dates, not
  from more names chosen at one date.** Do not sweep K; that is knob-tuning.

- **An artifact fix's value is a property of the base, not of the fix.** Every
  magnitude-weighted candidate since trial #20 sized positions off
  `composite - composite[held].min() + FLOOR`, anchoring the whole weight
  vector to the weakest *currently held* name — the one the buffer swaps most
  often — so every swap rescaled every weight even when no name's own signal
  moved. On the non-overlapping basket, replacing it with a fixed floor
  halved re-sizing turnover (4.67x → 2.30x). On the overlapping basket
  (trial #33) the *same two lines* moved re-sizing turnover only 2.36x →
  2.12x, because averaging six formations already damps any one formation's
  spurious rescale ~6:1. What was left was pure de-concentration (mean top
  weight 0.188 → 0.136, HHI 0.0831 → 0.0579 at identical name count), which
  bought the repo's best-ever validation maxDD **-26.9%** for ~0.02 of Sharpe
  (1.11 → 1.09, DSR 0.9341 → 0.9277). Since the gate scores Sharpe and not
  drawdown, trial #32 remains the challenger to beat — but read #32 and #33
  as one strategy at two points on a risk/return dial, not as rivals. General
  lesson: before generalising an artifact-removal result, ask how much of the
  artifact the rest of the construction has already neutralised.

- **Cheap holdings-only diagnostics keep killing ideas before they cost a
  trial — use them.** Computing statistics on the weight matrix (top weight,
  HHI, position counts, entry/exit vs re-sizing turnover decomposition,
  weight sitting outside the current held-set) or on a trigger's firing dates
  scores no returns and is not a backtest, so it does not touch the trial
  count. It has now pre-empted several trials: an inter-signal ensemble
  (rank correlation 0.89 between candidate scores), a convex-transform
  exponent fixed against a concentration target rather than tuned against
  performance, and — tonight — re-specifying the vol-spike trim to measure
  the *actual book-weighted* basket vol instead of the equal-weighted proxy
  the code uses. That last looked like a real mis-specification but the two
  definitions disagree on **1 of 1562 validation days**: the 21d/252d vol
  *ratio* is largely insensitive to weighting within one correlated basket.
  Diagnose first; spend the trial only on what survives.

- **A headline mechanism in this repo was mis-specified, and finding out cost
  four trials: the champion's daily "vol-spike trim" does not measure its own
  basket.** The filter is `prices.iloc[:end_pos][names].dropna(axis=1,
  how="any")`, and since the store starts in 1962 it admits only instruments
  with a complete ~60-year history — a mean of **3 of 34 held names, 11% of book
  weight**, zero in some months. The eleven that can ever qualify (JNJ, PG, XOM,
  CVX, KO, MRK, DIS, IBM, CAT, GE, HON) are old-economy defensives, roughly the
  opposite style to the momentum book. Bracketing it against every deliberate
  specification plus the control: held-basket trigger 1.050, whole-market
  trigger 1.055, **no trim at all 1.062**, whole legacy cohort 1.081, champion's
  accidental `held ∩ cohort` 1.107. Three consequences. (a) The
  correctly-specified basket-own trim is *worse than deleting the overlay*, so
  "the basket's own realized vol" as a mechanism is refuted, not merely
  mis-measured. (b) What is real is a **defensive-cohort stress overlay**: the
  cohort trigger reproduces the champion's maxDD exactly (-29.1% vs the control's
  -30.3%) and the ordering basket < market < none < cohort is monotone in how
  style-orthogonal the trigger is to a momentum book — a momentum basket's vol
  rises in melt-ups as readily as in crashes (the champion's trigger fires 44
  days in 2020, its +132% year, and near-zero in both loss years), so measuring
  the thing you are de-risking is precisely the wrong signal. Worth about +0.019
  Sharpe and -1.2pp drawdown. (c) The remaining **0.026 of the champion's Sharpe
  requires sampling that cohort through basket membership and has no mechanism —
  treat it as sampling luck.** The champion keeps its seat (it won the gate
  honestly, and its holdout — 1.22 Sharpe, -23.3% maxDD — is the repo's best
  number), but its margin over the plain untrimmed six-tranche book is only
  partly explained. Do not build on the trim without re-reading trials #37-#40.
  General lesson: **before crediting a component, check what its code actually
  reads.** This one survived ~20 trials and several write-ups describing it in
  terms its implementation never matched.

- **Drawdown-state braking is refuted, and the failure mode is the mirror of the
  cadence lesson.** A hysteresis brake on the book's own equity (cut to 0.6x
  below -20% from peak, release above -10%) was aimed at the one gap the
  vol-spike trigger structurally cannot see — both loss years, 2018 and 2022, are
  slow grinds without a dispersion spike — and it made **2022 worse, -8.9% ->
  -17.4%**, cost -13.3% in 2019 and -10.7% in 2021, and widened validation maxDD
  to -33.3% while improving train maxDD (-56.5% -> -46.5%), the same
  in-sample-crash-fix signature as the three earlier de-risking overlays. The
  mechanism: it armed in the 2018-10 selloff and, because release requires
  recovery to within 10% of peak, was still de-risked into the start of a +50%
  year. Earlier lesson: a trigger must react faster than the strategy's rebalance
  cadence. **New complement: a release rule slower than the recovery costs more
  than the trigger ever saves.** Drawdown depth is a lagging state variable — by
  the time it is deep enough to be outside routine noise (4 of 55 validation
  episodes reach -20%), it mostly describes what already happened. Closed for any
  threshold; different thresholds are the only knob and would be tuning a refuted
  mechanism.

- **Turnover reduction is now a spent lever on the overlapping-tranche base.**
  At 3.0x annual turnover and 15 bps/side the champion's entire cost drag is
  0.45%/yr ≈ 0.019 Sharpe, so even eliminating trading altogether could not close
  the gap to a materially better strategy. This retires a whole class of ideas
  (no-trade bands, weight-change thresholds, cheaper rebalance mechanics) that
  were worth testing when the same signal ran at 7.3x. It also reframes the
  overlap finding once more: at 7.3x -> 3.0x the saving was ~0.65%/yr, but the
  overlap gained far more than that in return, so cost was never the main story
  there either — temporal breadth was.

- **The validation window is not a homogeneous sample, and every Sharpe quoted
  here inherits that.** The champion's validation P&L by year: 2018 -5.9%, 2019
  +50.3%, 2020 **+132.2%**, 2021 +17.5%, 2022 -8.9%, 2023 +24.5%. One year is
  most of the result. Combined with the post-2026-08-16 protocol (trial
  clustering makes within-family tuning nearly free in deflation terms, so DSR no
  longer brakes a ladder of momentum variants), the practical position is that
  **the only real check left is the holdout**, and a challenger that beats 1.107
  by a small margin should be assumed to have beaten it in 2020 until shown
  otherwise.

- **Lookback *length* is a second axis of vintage diversity, roughly independent
  of formation *date*, and it is the answer to the standing "what supplies
  decorrelated vintages without being a K sweep" question.** The champion had
  been collapsing its two lookbacks into one score (`z(12-1) + z(6-1)`) before
  selecting anything, which discards the fact that the two windows disagree about
  *which names to hold* and keeps only their agreement about ranking. Giving each
  window its own buffer chain, held-set and magnitude-weighted target and
  averaging the resulting *portfolios* at equal weight moved the whole profile:
  two windows (#41) then four quarterly windows 12-1/9-1/6-1/3-1 (#42) gave
  validation Sharpe 1.107 -> 1.112 -> 1.120, validation maxDD -29.1% -> -28.5% ->
  -27.8%, holdout Sharpe 1.22 -> 1.32 -> 1.38, holdout maxDD -23.3% -> -22.1% ->
  -20.1%, turnover 3.0x -> 3.2x -> 3.1x, positions 34 -> 47 -> 63. Monotone on
  every axis, with the largest moves on the axes the gate does not score. Two
  things this settles. (a) The **concentration price is not a law of
  de-concentration** — every previous step down that dial cost ~0.02 of Sharpe,
  but breadth arriving from a decorrelated vintage costs nothing, which is the
  pruning result one axis over. (b) The pre-trial diagnostic gate worked as
  intended: the two legs rank-correlate 0.66 (0.69 in validation) and their
  portfolios share only 0.60 of weight (0.47 in validation), well clear of the
  0.89 that killed the earlier inter-signal ensemble for free. **Equal weights
  between legs are load-bearing** — "weight the better window more" is the
  estimated-weight mistake three separate literatures warn against. Do not
  compare further brackets: the interval is bounded on both ends (skip-month
  below, post-formation reversal above) and scanning it is the sweep the manual
  forbids. What remains genuinely open, for a session with its own rationale, is
  whether the windows should fill that interval *evenly*.

- **The validation split and the holdout can disagree about the sign of a
  mechanism, and the gate only reads the one that was wrong. Treat a large
  validation jump inside this family as evidence of overfitting until the holdout
  agrees.** Trial #43 switched the six-tranche date overlap off while keeping the
  four-horizon averaging, and produced the biggest validation jump ever recorded
  here — **1.120 -> 1.187**, DSR 0.9747, a clean PROMOTE — while the holdout
  **collapsed 1.38 -> 0.88** (ann_ret 34.9% -> 22.6%, maxDD -20.1% -> -27.4%).
  Costs do not explain it: turnover 2.8x -> 8.0x is worth ~1.5pp/yr at 15 bps
  against a 12.3pp gap in annual return. So the decomposition is answered, just
  not on the gate's axis: **date-vintage and length-vintage diversity are
  complements, not substitutes** — length alone (holdout 0.88) is worse than date
  alone (holdout 1.22), and the two together (holdout 1.38) beat both. The
  general rule to carry: within this heavily-explored family the validation
  window is a *weak* discriminator, and its failure mode is legible — it rewards
  concentrated, fast-rotating books (35 positions at 7.4x turnover beat 63 at
  3.1x) in a six-year sample whose P&L is dominated by 2019-2020. **Corollary for
  session design: once a session has seen a holdout number, every later candidate
  it designs is holdout-informed. Stop the session rather than spend the
  remaining budget.** Corollary for reading tonight's other two promotions: their
  validation margins (0.005, 0.008) were inside the noise both candidates
  pre-registered; what corroborates them is the monotone holdout, not the gate.

- **Standing protocol concern, raised 2026-08-17, for human attention.** Promotion
  scores validation Sharpe only, and the holdout is evaluated *after* the decision
  is made, so the gate structurally cannot see a validation/holdout disagreement —
  and on trial #43 it installed as champion a strategy materially worse
  out-of-sample than the one it displaced, by following `program.md` exactly.
  Nothing frozen was touched and this is not an engine bug; it is the stated
  objective working as specified on a case where the specification does not serve
  the mission. Two aggravating factors, both already on record: DSR clustering
  removed deflation as a brake on within-family laddering, and every promotion
  spends one more look at the holdout (three tonight). `mom_zscore_overlap6_hzn_avg4`
  (#42 — validation 1.120, holdout 1.38, maxDD -20.1%, turnover 2.8x) is the
  candidate a human would most plausibly reinstate.
