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
- **[PARTLY RETRACTED 2026-08-19 — see the risk-contribution entry near the end
  of this file. The two experiments below moved *weight* diversification and
  left *risk* diversification untouched, which is why they were no-ops; the
  axis was not closed, it was mis-measured.]** **The best challenger's rising
  validation maxDD is not a diversification
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
- **[Pruned 2026-08-20 to its transferable content; the specific numbers below were
  superseded by the trim-axis entry further down, which found this mechanism was
  mis-specified.] Cadence is a property of an overlay to check before judging it.** A
  vol-spike exposure trigger evaluated only at the monthly rebalance looked like a
  near-no-op (19 firings in 513 months); the *identical* trigger re-evaluated daily,
  with composition/selection/weighting still monthly and only the exposure scalar
  reacting faster, moved both Sharpe and drawdown. **General lesson for any future
  overlay or regime idea: check whether the trigger needs to react faster than the
  strategy's own rebalance cadence before concluding the mechanism does not work — a
  monthly-only check can make a sound crash-detection signal look dead purely from
  reaction lag, which is a different failure mode from the whipsaw that sank the
  earlier trend-based overlays.** Its complement is recorded further down under the
  refuted drawdown brake: a release rule slower than the recovery costs more than the
  trigger ever saves. One follow-up refuted at the time and not worth revisiting:
  redirecting trimmed capital into a fixed TLT/GLD hedge rather than cash gained
  nothing, because those legs were not reliably diversifying in the exact windows the
  trigger fires on.
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
  **the only real check left is the holdout**.
  **The "assume it beat 2020" clause is retracted 2026-08-20, having finally been
  measured rather than assumed.** A free decomposition of every recorded trial's
  stored validation return series (`experiments/trial_returns/`, no strategy
  re-run, no new backtest, trial count untouched) puts `corr(validation Sharpe,
  2020 return)` at **+0.892** across all recorded trials and `corr(validation
  Sharpe, mean of the other five years)` at **+0.891** — indistinguishable. And
  the repo's biggest single validation jump, #42 -> #43 (1.120 -> 1.187), has
  **2020 essentially unchanged** (126.9% vs 128.6%): its gain is 2018 (-5.7 ->
  +2.2) and 2023 (28.4 -> 41.0). So the ladder is not a 2020 artifact, and the
  validation/holdout disagreement #43 opened is not explained by 2020 either —
  which makes the ⚠ protocol concern at the end of this file *harder* to dismiss,
  not easier. What the table does show is a sharper pattern: **the years that
  discriminate inside this family are the rotation years, 2018 and 2023**, and
  every construction that slows the core allocation's response to the current
  signal gives ground there specifically. Decompose before attributing any gap in
  this family to one year; the tooling is `experiments/trial_returns/` and it is
  free.

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

- **The horizon-averaging bracket is finished on all three of its axes, and the last
  one closed negative.** #42 pinned the *width* (four windows, ends fixed by the
  skip-month below and post-formation reversal above); trial #44 pinned the
  *interior*. The argument for interior spacing was sound and its premise was
  verified before the trial: two nested formation windows of length L1 < L2 share
  exactly L1/L2 of their data, so redundancy is a **ratio, not a difference**, and
  the uniform 63/126/189/252 bracket has adjacent ratios 2.00/1.50/1.33 — it samples
  the long end roughly twice as densely and leaves the legs non-exchangeable, which
  is precisely the condition under which the equal weights the construction already
  uses are the wrong ones. Geometric spacing between the *same* endpoints
  (252/159/100/63, all ratios 4^(1/3)) fixes that for free — a holdings-only
  diagnostic put the dispersion of adjacent-pair weight overlap down **12x, 0.0711 →
  0.0060**, with breadth untouched (35.1 → 35.6 names), which rules out the
  de-concentration confound that has explained several earlier results. And it bought
  nothing: validation Sharpe 1.187 → 1.166, maxDD -29.0% → -29.7%, turnover 7.4x →
  7.8x, all inside the family's noise and all in the same slightly-worse direction,
  so there is no risk/return-dial reading to rescue it. **The substantive finding is
  the stronger claim about equal weighting:** equal weights between horizon legs are
  not merely load-bearing against the *estimated*-weight mistake, they are also
  insensitive to the one deviation from their optimality condition that can be
  corrected at zero estimated parameters. Which means the #41/#42 gain is **coarse** —
  it comes from having several windows at all, not from where inside the bracket they
  sit. Do not propose a third spacing; there is no third non-arbitrary rule, and it
  would be the sweep the manual forbids.

- **"Sampling luck" is a testable attribution, and the way to test it is to re-draw
  the sample rather than to argue about it.** Trials #37-#40 found the champion's
  daily trim was reading `held ∩ full-history-cohort` rather than its own basket,
  established the mechanism from a monotone ordering in style-orthogonality (held
  basket 1.050 < market 1.055 < no trim 1.062 < whole cohort 1.081 < the accident
  1.107), and wrote off the accident's residual +0.026 as luck in which three
  defensives the momentum screen happened to hold. Trial #45 tested that: champion
  #43 had re-drawn the held-set from a different selection process (no date overlap,
  four independent horizon legs; trigger sample 6.5 names / 20.7% of book weight
  against the 3 / 11% the accident was characterised on), and on the re-draw the
  ordering **reverses** — deliberate whole-cohort 1.201 against the accident's 1.187.
  A systematic edge does not change sign under re-draw; a lucky one does. Two
  consequences. (a) The clause stands, now measured. (b) The repo's one surviving
  overlay is finally **specified** rather than accidental: the equal-weighted realized
  vol of every instrument with a complete price history to the formation date, a
  stated style-orthogonal defensive-cohort stress signal, replacing an artifact of a
  `dropna` filter nobody had read for ~20 trials. Note *how* it earns its keep —
  validation ann_ret **fell** (28.75% → 28.59%) while ann_vol fell more (0.2367 →
  0.2319), because the deliberate trigger fires 99 validation days to the accident's
  65 and the accident is nearly a strict subset. Sharpe rose through the denominator,
  which is what a de-risking overlay is supposed to do and the first time one has been
  observed here doing it on the specification it claims to use. **The trim axis is now
  closed** — six trials, mechanism identified, accident retired, the two constants
  (1.6, 0.6) still inherited and untuned. Further work on it is knob-turning.

- **Generalise the pre-trial diagnostic habit into a rule: measure the mechanism's
  premise first, and pre-register the effect size the measurement implies.** Both of
  tonight's trials were preceded by a holdings-only diagnostic and both diagnostics
  were quantitatively right about what followed — the spacing diagnostic said the
  *level* of redundancy barely moved (-0.011 mean overlap) even as its dispersion
  collapsed, and the trial duly returned a null; the trim diagnostic said the two
  specifications disagree on 40 of 1412 validation days concentrated in 2018/2020/2022,
  and the trial duly returned a small net margin that was the residue of a large
  offsetting trade. In both cases **the trial supplied only the sign.** A third idea —
  replacing the min-shift weight anchor with a fixed floor on the champion's base —
  was killed outright for free: the diagnostic put re-sizing turnover at -22% (between
  the -51% recorded on the single-score non-overlapping base and the -10% on the
  six-tranche base, exactly as the ~1/N damping story predicts for four legs) worth
  ~0.014 Sharpe in saved cost, against a **-27% HHI de-concentration at unchanged
  breadth** (35.1 → 35.1 positions), which this repo has priced at ~0.02 Sharpe every
  time the extra flatness did not come from a decorrelated vintage. Predicted net
  negative, trial not spent. Diagnose first; spend the trial only on the sign, and only
  when the sign matters.

- **[NUMBERS RE-BASELINED 2026-08-26. The champion changed today — the human's
  `## Engine change` journal entry rolled the seat back to #42
  `mom_zscore_overlap6_hzn_avg4`, validation 1.120, K=6. Every concentration and
  risk figure in the entry below, and in every entry between 2026-08-21 and
  2026-08-24 phrased as "on this base", describes the **retired** K=1 champion
  `mom_hzn_avg4_nobuffer`. The mechanisms stand; the levels do not.]** Recomputed
  holdings-only on the reinstated champion (75 sampled validation dates, 252-day
  trailing sample covariance):

      statistic              retired #51   reinstated #42   trial #55 (disjoint)
      positions                 30.3            62.7             80.8
      HHI                      0.0918          0.0612           0.0337
      top weight                0.172           0.156            0.103
      top-name RISK share       0.368           0.323            0.239
      effective WEIGHT bets     13.3*           18.35            31.98
      effective RISK bets        6.0             8.54            13.84

  (*the 13.3/6.0 pair below is quoted for the champion of 2026-08-19.) The
  reinstated book is materially more diversified than six sessions of notes
  describe. The turnover-drag figure for it is already correct in the arithmetic
  correction near the end of this file (3.11x → 0.47%/yr → 0.021 Sharpe).

- **Weight concentration is not risk concentration, and every concentration
  claim in this repo's history was made on the weaker of the two.** The
  risk-contribution vector `x_i · ∂_i σ(x)` — a holdings-only statistic, no
  returns scored — puts the champion's top name at **17.2% of capital but 30.9%
  of variance**, its top five at 48.7% against 63.2%, and its effective bets at
  **13.3 by weight against 6.0 by risk**. The book is less than half as
  diversified as top-weight and HHI had been reporting, because magnitude
  weighting puts the most capital on the names that are simultaneously the most
  volatile and the most correlated with each other. This resolves the standing
  puzzle above: sector-neutral scoring and basket-breadth widening both moved
  weight diversification while leaving risk diversification alone, which is
  exactly why neither moved maxDD. Subsample bagging (trial #47) moved the risk
  axis — top-name risk share 30.9% → 22.5%, effective risk bets 6.0 → 9.9 — and
  validation maxDD moved with it, -28.7% → **-26.9%**, tying the repo's best.
  First time a candidate's drawdown was predicted quantitatively from a
  holdings-only statistic *before* the run. **Compute risk contributions
  alongside HHI for any future concentration or drawdown claim.** The obvious
  fix it invites — capping risk contribution rather than weight — is killed for
  free by screen #1 of `research/SUMMARY.md`: a risk cap needs a covariance
  matrix, the expensive noisily-estimated class refuted twice here and closed
  analytically by the ERC theorem. The diagnostic that reveals the problem does
  not license the fix that would create a worse one.
  **Boundary added 2026-08-20, after the statistic's first miss.** It predicted
  #47's drawdown improvement and #48's non-improvement correctly, then missed #50:
  the risk vector was flat (top-name risk share 0.327 -> 0.317, effective risk bets
  7.7 -> 7.7) while validation maxDD widened -28.7% -> **-33.0%**. The miss has a
  shape. Risk contributions come from a *trailing covariance of a snapshot book*, so
  they are blind to **weight-vector staleness**: when the largest positions are the
  oldest winners, the danger is not that those names co-move, it is that the weight
  vector describes a regime that has ended, and no correlation matrix reports that.
  Keep the diagnostic and the rule — just do not lean on it for a construction whose
  weights carry information from long before the measurement date.

- **A vintage axis is only a vintage axis if its members disagree about
  *membership*; perturbing a threshold re-draws the fringe, perturbing the data
  re-draws the core.** Three candidate averaging axes measured on one night by
  the same holdings-only diagnostic, mean weight overlap against the champion:
  buffer-band vintages (10/18, 15/25, 20/35) **0.963** — killed for free, it
  adds 10.7 names at unchanged HHI and unchanged turnover, i.e. the saturated
  `N` lever, because nested bands off one ranking at one date share their core
  and their average is the middle band plus a low-weight fringe; formation-date
  vintages (K=6) **0.645**; instrument-subsample vintages (three
  leave-one-third-out folds) **0.851** overall but with pairwise fold overlap
  of only **0.43-0.48** and, decisively, **0.140 of L1 disagreement inside the
  champion's own top-10 names against 0.159 across the entire rest of the
  book**. A name absent from a fold cannot be selected in it, so subsampling
  re-draws the held-set where the weight is. Screen any proposed vintage axis
  on core-versus-fringe disagreement before spending a trial — and note the
  measured ordering only says which axes are *live*, not which pay: the 0.645
  axis costs validation Sharpe (below) and the 0.43-0.48 axis costs a little
  too. Live is a precondition, not a prediction.

- **The overlap-versus-no-overlap comparison was confounded, and un-confounding
  it strengthened the finding instead of overturning it — while re-confirming
  the sampling-luck clause a second time, for free.** #42 vs #43 (six-tranche
  date overlap off, four horizon legs fixed) produced the repo's biggest
  validation jump, 1.120 → 1.187, but both sides carried the accidental
  `held ∩ legacy-cohort` trigger, whose sample is a function of book breadth (3
  names / 11% of weight at 62.7 held names, 6.5 / 20.7% at 35.1). The champion's
  whole-cohort trigger is market-level and bit-identical across K, so trial #46
  is the first clean reading: **the gap widens, 0.067 → 0.094** (1.201 vs 1.107).
  #43 stands. The by-product is worth more: laying the four cells out —
  accidental trim K=6 1.120 / K=1 1.187, cohort trim K=6 1.107 / K=1 1.201 — the
  intersection filter is worth **+0.013 on the wide book and −0.014 on the narrow
  one**. #45 re-drew the held-set along the horizon axis and the ordering
  reversed; #46 re-draws it along the K axis and it reverses again, at almost the
  same magnitude, in a trial not designed to ask. **Two independent re-draws, two
  sign flips: the sampling-luck attribution is established, not merely
  surviving.** Note also what the overlap does and does not cost: K=6 wins or
  ties every unscored axis (turnover 3.5x vs 7.9x, maxDD -28.5% vs -28.7%,
  positions 62.7 vs 35.1) and carries DSR 0.9611 on its own; the whole deficit is
  3.4pp of annual return against a cost saving of ~0.66pp/yr, so turnover is
  ruled out as the explanation for the third time on this base.

- **The vintage-averaging family is closed for challengers: three live axes, three
  losses, and the third one removes the excuses the first two had.** The lab's
  strongest historical mechanism is averaging one selection procedure over vintages,
  and it now has a complete negative record *on top of the four-horizon single-vintage
  base*: formation-**date** vintages (#46, -0.094), instrument-**subsample** folds
  (#47, -0.021) and rebalance-**phase** vintages (#48, -0.076). Buffer-band vintages
  were killed free earlier (0.963 overlap). The standing account blamed a different
  nuisance for each of the first two — staleness for the date axis (K=6 holds
  six-month-old formations) and pool restriction for the subsample axis (each fold
  picks its top 15 from ~93 instruments, not 140). **Phase has neither**: every
  vintage sees all 140 instruments, runs the champion's cadence, and no tranche is
  ever over one month old. Its nuisance terms were measured at essentially zero before
  the run (HHI -5% ~ 0.003 Sharpe, top-name risk share 0.327 -> 0.325, effective risk
  bets 7.7 -> 7.8, gross exposure identical) and it still cost 0.076 — the cleanest
  reading available, and the largest loss of the three relative to its own excuses.
  **What all three share is a signature, not an excuse: the deficit lands in the
  rotation years.** By the free year decomposition, 2020 is near-untouched in each
  (#48: 126.4% vs the champion's 130.5%) while 2018, 2019, 2022 and 2023 give ground.
  Averaging blurs the core allocation — #48's core-vs-fringe L1 was 0.118 on the
  champion's top-10 against 0.165 on the whole rest, so the top of the book *is*
  re-drawn — and a blurred core tracks a leadership change more slowly than a single
  fresh formation does. That is one mechanism for three nulls and it does not invoke
  staleness, pool size or concentration. Cost is ruled out in all three (turnover
  changes of -55%, +1.8% and -43% across the night, all with the deficit landing in
  return). **Do not propose a fourth vintage axis without a rationale that addresses
  rotation speed specifically**; the screens (overlap, core-vs-fringe) tell you whether
  an axis is *live*, and three live axes have now all lost, so live has been shown to
  be a precondition with no predictive content whatever.
  *Note on scope: none of this overturns #32's original overlap gain, which was
  measured against a materially worse base and whose pruning diagnostic still stands.
  The claim is about marginal value on top of the current four-horizon book.*

- **[MOSTLY RETRACTED 2026-08-21 — the mechanism this entry described does not exist
  in this engine. Corrected text below; the original claim is preserved in the
  2026-08-20 journal entries for #49/#50.]** The entry asserted that "every
  magnitude-weighted book here sets weights once a month and then leaves them alone,
  so the realised weight vector is the formation-date vector tilted by each name's
  trailing 0-21 day return — a momentum tilt applied by omission, inherited by every
  candidate ever run here", and credited that tilt with ~0.09 Sharpe and ~3.7pp/yr.
  **A holdings-only diagnostic (no returns scored, no trial spent) shows there is no
  such tilt.** `sanitize_weights` reindexes the emitted weight rows onto the price
  calendar and *forward-fills them*, so the held weight vector is constant between
  emitted rows and the engine charges turnover only when the emitted target changes:
  it implements a **daily-rebalanced constant-weight book**, not a buy-and-hold one.
  Measured on the champion over the validation split: the held vector changes on **88
  of 1562 days** (exactly the 88 rows the strategy emits), and across the 83
  inter-rebalance gaps the mean L1 change of the held vector is **0.000000**, against
  the **0.0568** that true price drift over the same gaps would produce. Nothing
  drifts; there was never a tilt to harvest, discard or time.
  **What #49 and #50 actually measured, restated.** #49 did not remove a drift — it
  **re-targeted weekly instead of monthly from a fresher composite**, and cost 0.142
  (turnover 7.9x -> 14.8x, ~0.045 Sharpe of it cost). #50 did not "keep" something the
  champion throws away — reading its code, it **introduces** a compounding
  `prev_weight x price growth` tilt of unbounded age that no other candidate here has,
  and cost 0.276. So the two results still bracket the monthly re-target cadence on
  both sides and that conclusion stands, but as a statement about **how often to
  re-target**, not about harvesting a drift at the right horizon.
  **The claimed boundary on the skip-month lesson is withdrawn, and its sign is now
  evidence the other way.** The retracted text said the trailing-month return is
  reversal in *selection* but continuation in *weighting*, "and the second use is free,
  requiring no trade at all". The champion does not make that second use at all, so it
  was never evidence for it; #50 is the only trial that has ever implemented it, and it
  **lost 0.276**. Treat "ride the trailing month in weighting" as refuted rather than
  established, and treat the skip-month as load-bearing in selection with no known
  second use.
  **The general lesson is the one that already cost this repo four trials on the trim,
  recurring: before crediting a component, check what its code actually reads — and
  that now explicitly includes the engine's own conventions, not just the strategy
  file.** Two headline lessons in six days have described mechanisms their
  implementations did not implement. A cheap way to catch the whole class: any claim
  about what happens *between* rebalances can be checked by diffing the sanitized
  weight matrix, which scores no returns and costs nothing.

- **The membership buffer's stated justification is dead on the K=1 base, what it
  actually buys is risk breadth the gate cannot see, and the core-vs-fringe screen
  does not detect that.** The hold-25/enter-15 band has been inherited unexamined
  since trial #17, where it was justified — locally and by `research/SUMMARY.md`
  candidate #9 — as a **cost-mitigation** device, and where it saved 24% of turnover
  on a single-leg equal-weight base. On the four-horizon base it saves **6%**: 0.47x
  of annual turnover, ~**0.003 Sharpe**, because averaging four legs already absorbs
  the churn a band was invented to suppress. Deleting it (#51, `held = core`, a hard
  top-15 per leg) landed validation **1.229** against a pre-registered 1.215 — so the
  band's marginal value on the gate's axis is about **-0.014**, a null, and the whole
  visible move is the concentration confound the diagnostic priced in advance
  (HHI +25.7% ~ +0.017 Sharpe). What the band really carries is **risk breadth**:
  35.1 -> 30.3 names, top-name risk share 0.320 -> 0.368, effective risk bets
  **7.8 -> 6.0**, and validation maxDD duly widened -28.7% -> -29.6% with holdout
  maxDD -27.4% -> -30.5%. That is the risk-contribution diagnostic's second correct
  pre-registered call since its one miss (#50), whose stated shape — blindness to
  weight-vector staleness — correctly did not apply to a monthly-re-targeted book.
  **The transferable boundary is on the core-vs-fringe screen, and it is the same
  shape as the weight-vs-risk distinction already recorded above.** The screen said
  the band is a *fringe* phenomenon (L1 0.063 on the champion's top-10 against 0.127
  on the rest) and that was read as "expect nothing". It was right about *where* the
  change lands and wrong as a proxy for whether it *matters*: 4.8 low-weight names
  carried 1.8 effective risk bets, far more of this book's diversification than their
  4.8/35 share of its weight. **Core-vs-fringe is a weight statistic; pair it with the
  risk-contribution vector before concluding a fringe change is a small change.**
  Practical standing: the band should not be described as a cost device here, and any
  future proposal to reinstate or widen it should be argued on risk breadth.

- **Magnitude weighting decomposes into concentration and information, and more than half
  of it is information. The de-concentration constant this file quotes is ~2.5x too
  small.** Two trials one night apart deleted the champion's two concentration channels
  separately, both with membership held bit-identical at 30.30 names, so each isolates one
  mechanism exactly. **#52** deleted the within-leg magnitude transform (each leg
  equal-weighting its top-15): HHI -55%, cost **0.206** of validation Sharpe. **#53**
  deleted the cross-leg agreement premium (a name all four legs pick no longer receives 4x
  a name one leg picks): HHI -26%, cost **0.043**. Three results follow.
  (a) **Restate the constant.** This file has priced de-concentration at ~0.02 Sharpe per
  30% of HHI; #53 measures **~0.05**. The readings that used the old figure (#50, #51, the
  free kill of the fixed-anchor idea) were understated in the same direction; none is
  overturned, and #51's is strengthened — its concentration tailwind should have been
  ~+0.042 rather than +0.017, making the buffer's marginal value on the gate's axis more
  negative than recorded, not less.
  (b) **The corollary is the finding.** At #53's rate, #52's -55% of HHI should have cost
  0.090; it cost 0.206, so **~0.116 Sharpe of magnitude weighting is not concentration** —
  the ordering and spacing of scores inside a leg's top-15 carries real cross-sectional
  information. This re-establishes the square-root-dampening conclusion on the current base
  by a different method: dampening moved one dial, this decomposes two. What is still open
  is whether the 0.116 is *ordering* or *spacing*; a rank-weighted leg target sits between
  #52 and the champion and would split it, but it is a decomposition and will not promote.
  (c) **"The base has absorbed it" does not generalise across components.** #52 was
  pre-registered at 1.15 on the analogy to #51, where four-leg averaging had shrunk the
  buffer's cost saving from 24% to 6%. It landed 1.023 — the component is worth 2.5x what
  it was worth on the single-leg base of trials #18-#21, not less. The reason is
  structural: a name's weight is (legs holding it)/4 times its within-leg magnitude weight,
  so with four legs the two channels **compound**, where on the old base only one existed.
  #51's absorption was a property of churn damping and has no analogue in a weighting
  transform. Adding legs can amplify a component instead of damping it.

- **The risk-contribution count beat the Meucci count in a designed referee, and now has a
  quantitative calibration rather than only a sign.** `research/SUMMARY.md` candidate
  #23(a) argued that this file's "effective risk bets" — a Herfindahl over *marginal risk
  contributions of correlated assets* — is not a count of anything uncorrelated, and that
  `N_Ent` over the diversification distribution (change basis, then count), reported
  conditionally for a fully-invested long-only book, is the measure that is. #52 is the
  only construction found so far on which the two disagree maximally: effective risk bets
  5.99 -> **17.68** (+195%) against N_cond 5.63 -> **5.49** (-2.6%). Validation maxDD moved
  -29.6% -> **-24.3%**, the best ever recorded here (beating #47's -26.9%). The
  contribution count was right. N_cond *did* correct downward as predicted, and over the
  promotion ladder its correlation with holdout Sharpe (+0.632) beats the contribution
  count's (+0.450) — but on the one case built to separate them as drawdown predictors it
  failed, and it missed again on #53. **Keep computing effective risk bets; do not replace
  them.** #53 then calibrated the statistic: at +29% of effective risk bets (a seventh of
  #52's move) the predicted maxDD was -28.8% by linear scaling and it landed **-29.1%**
  against the champion's -29.6%. Two pre-registered calls at effect sizes a seventh apart,
  both right. It is roughly linear in the range this repo works in.

- **`gamma*`, the excess growth rate, is a null on this universe, and the reason is
  mechanical.** `research/SUMMARY.md` candidate #23(b) proposed measuring
  `gamma*_pi = 1/2 (sum_i pi_i a_ii - pi' a pi)` as "the price of concentration",
  denominated in log growth and therefore on the gate's own axis; it was last session's
  top idea. Measured over validation on every rung of the promotion ladder (holdings-only:
  sanitized weight matrix, 252-day trailing realized covariance, only the excess-growth
  term ever formed — never a portfolio return series): baseline 3.92%, #32 5.20%, #41
  5.34%, #42 5.42%, #43 5.26%, #45 5.26%, #51 5.51%. It is not monotone, does not break at
  #43 where every other ladder statistic does, and its **highest** value belongs to the
  **narrowest** book in the table. `gamma*` is dominated by `sum_i pi_i a_ii`, the weighted
  average variance of what is held, so on a momentum book that concentrates into
  high-volatility winners it *rises* with concentration — confirmed independently by #52,
  where equal weighting cut it 5.51% -> 4.17% while improving every diversification
  measure. **It is not a de-concentration statistic here.** Do not re-run it.

- **A free kill, recorded so it is not rediscovered as an artifact.** All four horizon legs
  select from `common`, the intersection of the instruments eligible for *every* lookback,
  so a 63-day leg cannot pick a name lacking 273 days of history — structurally the same
  shape as the `dropna` artifact that cost four trials on the trim. Over the 72 validation
  month-ends, mean `|common|` is 139.7 against 139.8 for the 63-day leg alone and 139.9
  instruments priced; it binds in 9 of 72 months and costs at most **1 instrument**. A
  no-op. The general habit stands and keeps paying: check what a component's code reads,
  then measure how much it reads differently, *then* decide whether to spend a trial.

- **Magnitude weighting's information is more ordinal than cardinal on the K=1 base, and the
  split does not transfer across leg counts either.** #52 (equal weight) and #53 (no
  cross-leg agreement premium) left one quantity unresolved: whether the ~0.116 Sharpe of
  the within-leg magnitude transform that is *not* concentration is the score's ordering or
  its spacing. #54 split it with linear rank weighting (ordering kept exactly, spacing
  discarded entirely), membership bit-identical at 30.2977 names across all three books:
  equal 1.023 / rank **1.123** / champion 1.229, at HHI 0.0425 / 0.0582 / 0.0918. Netting
  each step's de-concentration at #53's constant leaves **spacing 0.045 and ordering
  0.055-0.072** — 55-62% ordinal, against the **37.5%** the single-leg base of trials
  #18-#21 recorded (equal 0.90 -> rank 0.93 -> magnitude 0.98). The two ordering readings
  differ by 0.017 because HHI ratios compound rather than add across two steps; the residual
  is stated, not allocated. **The general point extends #52 rather than repeating it: the
  old base was borrowed for the *share* this time, not the level, and the share did not
  transfer either — four-leg averaging changes not only how much a component is worth but
  what it is worth it for.** Offered mechanism, untested: the cross-leg average already
  imposes a coarse cardinal spacing (a name's weight is (legs holding it)/4 times its
  within-leg weight, the channel #53 priced at 0.043), so a second cardinal spacing inside
  each leg is partly redundant where the ordinal information is not. The within-leg
  weighting axis is now fully mapped — equal, rank, magnitude, and the refuted square-root
  dampening — and should not be revisited without a new mechanism. A third pre-registered
  call for the risk-contribution count also landed here (predicted validation maxDD -27.1%
  at +92% of effective risk bets, got **-26.7%**), so the statistic is now confirmed at both
  ends of its observed range and at the midpoint.

- **The steps the gate adjudicates are individually unresolvable, and this is now measured
  rather than suspected. Compute the paired-bootstrap SE of a candidate's expected effect
  before spending the trial — it is the cheapest screen in the repo.** Every recorded
  trial's validation return series is stored on the same 1,562 days, so the standard error
  of a *difference* — the quantity the gate actually decides on, and the one
  `research/SUMMARY.md` #26 flags as absent from its source — can be bootstrapped directly
  (stationary block bootstrap on the **paired** series, so cross-candidate correlation is
  preserved; robust to expected block lengths of 1 to 63 days). Two facts follow.
  (a) **The pairing works and the naive objection dies.** A single strategy's own Sharpe
  carries SE 0.39-0.44 here; a difference between consecutive ladder rungs carries
  **0.026-0.15**, 3x to 17x tighter, because consecutive rungs correlate 0.909-0.997 daily.
  "The steps are inside the noise of one Sharpe" was never the right objection.
  (b) **And the steps are still not resolvable.** On that tightest available error, **none
  of the six promotions in this repo's history reaches |t| = 2** — the largest is the first
  (t = 1.62), four of six are below t = 0.55, and `P(step > 0)` for #41 and #42 is 0.58 and
  0.60, a coin flip. End to end the ladder is +0.364 at t = 2.18, so the *cumulative* climb
  is (just) distinguishable from zero while its *increments* are not. **The operational
  rule:** the family's SE floor is ~0.026-0.07 for a near-identical construction
  (correlation > 0.98) and ~0.13-0.17 for a structurally different one (correlation ~0.9);
  a pre-registered effect inside that floor buys a point estimate the data cannot resolve
  while permanently raising the DSR bar for every later candidate. #54 passes the screen
  retrospectively (effect -0.134 against SE 0.064); **#53 and #47 do not** (t = -0.74 and
  -0.86) — their conclusions stand as point estimates but their error bars must now travel
  with them.

- **`eta(q)`, the serial-correlation correction to annualised Sharpe, is not estimable at
  this sample length — and the question behind it has a small, uniform, order-preserving
  answer.** `research/SUMMARY.md` candidate #26 recommended measuring
  `eta(q) = q / sqrt(q + 2*sum_{k=1..q-1}(q-k)*rho_k)`. Computed over all 251 lags on the 52
  stored series it looks decisive (range 11.35-27.32 against `sqrt(252) = 15.87`) and it is
  **entirely noise**: under the null the denominator's sampling SD is
  `2*sqrt(sum_k (q-k)^2 / T) = 116.5` against its own value of 252, and a Monte Carlo on IID
  normal noise of the same length reproduces the whole observed spread (simulated sd 4.47 vs
  observed 3.78) with an *upward* bias in the mean. The bounded-lag version is estimable and
  says: `rho_1` is positive for every book in the magnitude-weighted era (+0.022 to +0.043,
  null SE 0.025), so **current-family Sharpes are overstated by ~2-4%**, and the correction
  **re-orders nothing** (Spearman 0.986 across all 51 distinct trials). The one place it
  bites is the headline — the baseline's `rho_1` is *negative* (-0.043) while the current
  family's is positive, so the ladder's recorded climb of +0.364 becomes **+0.276** under an
  L=1 correction, i.e. **~a quarter of the repo's total recorded progress is an annualisation
  artifact of serial correlation changing sign along the ladder.** Also: Lo's HAC standard
  error for a single strategy (0.41-0.43) is *tighter* than his IID formula (0.51-0.53) on
  these series, so quote the HAC one. **General lesson, and it is the same shape as the two
  headline mis-specifications this repo has already paid for: before adopting an imported
  statistic, check it is estimable on the sample you have — simulate it under its own null,
  which costs nothing.**

- **⚠ Standing protocol concern, raised 2026-08-17, now a FOUR-point trend, and the
  break has been localised to one commit. For human attention — this is the most
  important thing in this file.** Promotion scores validation Sharpe only, and the
  holdout is evaluated *after* the decision is made, so the gate structurally cannot
  see a validation/holdout disagreement. What was one case is now a run:

  | # | promotion | validation Sharpe | holdout Sharpe | holdout ann_ret | holdout maxDD |
  |---|---|---|---|---|---|
  | — | `mom_12m_baseline` | 0.865 | 1.140 | 28.2% | -24.1% |
  | 32 | `mom_zscore_overlap6_daily_trim` | 1.107 | 1.224 | 32.7% | -23.3% |
  | 41 | `mom_zscore_overlap6_hzn_avg` | 1.112 | 1.320 | 34.1% | -22.1% |
  | 42 | `mom_zscore_overlap6_hzn_avg4` | 1.120 | **1.377** | **34.9%** | **-20.1%** |
  | 43 | `mom_zscore_hzn_avg4_k1` | 1.187 | 0.875 | 22.6% | -27.4% |
  | 45 | `mom_hzn_avg4_k1_cohort_trim` | 1.201 | 0.813 | 20.6% | -27.4% |
  | 51 | `mom_hzn_avg4_nobuffer` | 1.229 | **0.691** | 17.5% | -30.5% |

  **Escalation 2026-08-21 — the decisive addition, and it is not the fourth point but
  what the full ladder shows.** Laid out end to end, the two splits agree for the
  first four promotions and then stop: `corr(validation, holdout)` is **+0.822** over
  the K=6 era (n=4, holdout climbing 1.140 -> 1.377) and **-1.000** over the K=1 era
  (n=3, holdout falling 0.875 -> 0.691). The sign of the relationship flips at **one
  identifiable structural change** — trial #43 switching the six-tranche
  formation-date overlap off — and every promotion since has been an increment on
  that base which bought validation with holdout, four times, monotonically, with
  holdout annual return now exactly **halved** (34.9% -> 17.5%) and holdout drawdown
  half again wider (-20.1% -> -30.5%). This is no longer "a run of disagreements"; it
  is a dated regime change in what the gate's axis is measuring.
  **What it does not license.** The gate is not mis-measuring itself: #46 compared
  K=6 against K=1 cleanly on validation and the gap *widened*. The two splits
  genuinely disagree about the overlap, and the gate reads only the one that has been
  wrong every time since.
  **Concrete recommendation for the human, stated plainly because four points is
  enough to stop hedging.** `mom_zscore_overlap6_hzn_avg4` (#42) is the best
  strategy this lab has produced on every axis the mission names — holdout Sharpe
  1.377, holdout return 34.9%, holdout maxDD -20.1%, turnover 2.8x — and it is worse
  than the incumbent only on the one axis the incumbent was selected for. Its file is
  intact in `strategies/candidates/`. Reinstating it, and scoring something other
  than raw validation Sharpe, both require edits to frozen files that no session may
  make.
  The earlier three-point statement of the same concern follows.

  Three consecutive promotions, validation monotone up and holdout monotone down.
  Each step followed `program.md` exactly; nothing frozen was touched and this is not
  an engine bug. It is the textbook signature of a gate optimising a statistic that
  has stopped tracking the mission it was chosen to proxy ("beat the current champion
  out-of-sample"). Three aggravating factors, all on record: DSR clustering removed
  deflation as a brake on within-family laddering (11 effective trials against 45
  recorded); `main`'s recorded trial count understates the true number of candidates
  attempted; and **every promotion spends one more look at the holdout — four since
  2026-08-17.** `mom_zscore_overlap6_hzn_avg4` (#42 — validation 1.120, holdout 1.38,
  maxDD -20.1%, turnover 2.8x) remains the candidate a human would most plausibly
  reinstate, and its file is intact in `strategies/candidates/`. Until a human rules,
  sessions should prefer diagnostic work to challengers in this family — the two
  levers that would fix it (scoring something other than raw validation Sharpe, or
  rationing holdout looks) both live in frozen files.
  **Update 2026-08-19: unchanged at three points — no promotion tonight, so no
  fourth data point and no fifth holdout look was spent.** Both of tonight's
  trials rejected, which is the one outcome that leaves the holdout untouched;
  the count of holdout looks since 2026-08-17 stands at four. Worth recording
  that trial #47 landed 0.021 short of the champion on the gate's axis while
  beating it by 1.8pp on validation drawdown and tying the repo's best — a
  second concrete instance, alongside #32/#33 and #42, of the gate's single axis
  discarding a candidate a human weighing risk would want to see.
  **Update 2026-08-20: still three points, no promotion, no fifth holdout look — and
  one supporting argument has been withdrawn while the concern itself got stronger.**
  Three trials tonight, three REJECTs, so the holdout stayed shut and the count since
  2026-08-17 remains four. The withdrawn argument is the "one year is most of the
  result" reading: measured on the stored trial returns, validation Sharpe tracks the
  2020 return (+0.892) and the mean of the other five years (+0.891) equally well, and
  #43's record jump had 2020 flat. **The concern therefore cannot be waved away as a
  2020 artifact, and it also cannot be explained by one.** What remains is the bare
  fact in the table above: three consecutive promotions, validation monotone up,
  holdout monotone down, decided by a gate that reads only the first column. Still
  awaiting a human; both levers live in frozen files.
  **Update 2026-08-21: four points, and the session that produced the fourth one is
  the clearest illustration of the problem yet.** Trial #51 deleted a component whose
  documented justification a pre-trial diagnostic had just measured at 0.003 Sharpe.
  It cleared every rule in `program.md` — beat the champion, DSR 0.979, all gates —
  and its measured effects were: destroy 1.8 effective risk bets, widen validation
  drawdown, widen holdout drawdown, halve nothing it was supposed to improve, and
  take over half its validation gain from the single melt-up year (2020: 130.5 ->
  142.9). **A correctly-run session, following the manual exactly and diagnosing
  before spending the trial, promoted a strategy it does not believe in, because the
  gate's axis said yes.** The fifth holdout look since 2026-08-17 has now been spent
  (five total). Sessions should continue to prefer diagnostic work; the standing
  advice is now stronger than "prefer" — **in this family, a candidate that clears
  the gate should be treated as evidence about the gate rather than about the
  strategy** until a human rules.
  **Update 2026-08-22: still four points (two REJECTs tonight, no fifth promotion, no
  sixth holdout look), but the concern acquires the thing it has lacked since it was
  raised — a second, larger, already-computed split that agrees with the holdout and
  disagrees with the gate.** Computed from `experiments/trials.jsonl` alone, no strategy
  re-run and no new trial, the promotion ladder on all three splits:

      #    promotion                          train    validation   holdout
      -    mom_12m_baseline                   0.949      0.865       1.140
      32   mom_zscore_overlap6_daily_trim     0.978      1.107       1.224
      41   mom_zscore_overlap6_hzn_avg        0.962      1.112       1.320
      42   mom_zscore_overlap6_hzn_avg4       0.970      1.120       1.377
      43   mom_zscore_hzn_avg4_k1             0.935      1.187       0.875
      45   mom_hzn_avg4_k1_cohort_trim        0.942      1.201       0.813
      51   mom_hzn_avg4_nobuffer              0.931      1.229       0.691

      corr(train,      holdout)  +0.887  (n=7)    magnitude-weighted era (n=6): +0.908
      corr(validation, holdout)  -0.498                                         -0.969
      corr(train,   validation)  -0.297                                         -0.947

  **Why this is stronger than the small-n caveat usually allows.** (i) The train column is
  *not monotone in time* (up to #32, down after #42) and neither is holdout; they share a
  shape, not a trend, and validation is the only monotone column — a correlation driven by
  ladder order could not reproduce a non-monotone shape. (ii) Train is not a selection
  split: `program.md` scores validation Sharpe and train enters only as
  `min_train_sharpe = 0.0`, a floor no candidate has approached, so it is out-of-sample in
  the sense that matters, at 14,261 days against validation's 1,562. (iii) Tonight's #52
  is a prospective instance: best train Sharpe of the recent era (0.951 > the champion's
  0.931), best-ever validation drawdown (-24.3%), rejected by the gate on validation
  Sharpe.
  **Two honest weakenings, stated rather than chosen between.** `corr(train, validation)`
  is -0.947 in the era, so "train predicts holdout" and "validation anti-predicts holdout"
  are close to the same fact stated twice, not two independent findings. And the train
  split has its own severe problems — survivorship bias is worst there (1962-2017 scored
  on today's constituents) and its drawdowns run near -55%, outside the validation gate's
  own -45% limit.
  **What this licenses and what it does not.** It does *not* license a session selecting
  on train, or on any statistic it just discovered correlates with the holdout — that is
  the same error one split over, it is forbidden by `program.md`, and it is exactly the
  failure mode `research/SUMMARY.md` candidate #22 names (a criterion with too little
  curvature picks the high-variance candidate). What it licenses is a sharper
  recommendation to the human: **if a second scored quantity is ever added, the train
  Sharpe is already computed for every trial at zero marginal cost, and its correlation
  with the holdout is the highest of anything measured in this repo.** The standing
  recommendation is otherwise unchanged — `mom_zscore_overlap6_hzn_avg4` (#42) is the best
  strategy this lab has produced on every axis the mission names, it is also top of the
  train column among K=6 books, and its file is intact in `strategies/candidates/`.
  **Update 2026-08-23 — still four points (one REJECT tonight, no fifth promotion, no sixth
  holdout look), and the concern changes in kind rather than in size.** The paired-bootstrap
  standard error recorded above was applied to the comparison this whole concern turns on:
  `mom_zscore_overlap6_hzn_avg4` (#42) against the current champion is **Δ -0.109, SE 0.138,
  t = -0.79, P(#42 better) = 0.21**. On the gate's own split and its own statistic the two
  are **statistically indistinguishable**, and the holdout puts #42 ahead by **0.686**. So
  the claim to a human is no longer only "the gate reads the split that has been wrong every
  time since #43"; it is the stronger and simpler **"the gate broke a tie, and it broke it
  the wrong way."** The same measurement shows no promotion in this repo's history cleared
  |t| = 2 on its own step. If a second scored quantity is ever added, two are now available
  at zero marginal cost: the train Sharpe, and a paired-bootstrap SE of the
  candidate-versus-champion difference, which would let the gate decline to promote on an
  unresolvable margin rather than being obliged to.

- **The family's resolution floor is now measured two independent ways, they agree, and
  every remaining idea in the family sits below it.** (a) *Closed form.* Memmel's correction
  to Jobson–Korkie (`research/SUMMARY.md` #29) gives the paired SE of a Sharpe difference
  before any candidate exists: **`SE ≈ 0.568·sqrt(1−rho)`** on this 1,562-day window — 0.031
  at `rho` = 0.997, 0.057 at 0.99, 0.084 at 0.978, 0.171 at 0.909. Checked against the
  bootstrap recorded on 2026-08-23 it reproduces it closely everywhere and near-exactly on
  the two comparisons that matter (#42-vs-champion: 0.140 closed-form against 0.138
  bootstrapped). **Use it as the pre-trial screen; it needs no series and no resampling, so
  it applies to an idea before the file is written.** Carry it as a *floor*, never as a
  significance test — it assumes i.i.d. bivariate normal returns and is liberal under fat
  tails and volatility clustering. (b) *CSCV/PBO*, the first run here (`research/SUMMARY.md`
  #30), on the 12-member four-horizon family: **PBO 0.454, mean OOS rank of the in-sample
  winner 0.537**, averaged over `S` = 8..16. Calibrated on its own null and on a real
  alternative — 12 series at the family's own vol and `rho`, 40 replicates per point — a true
  advantage of `delta` = 0 gives PBO 0.506/rank 0.495, `delta` = 0.10 gives 0.317/0.623,
  `delta` = 0.30 gives 0.023/0.899. **The observed reading sits between `delta` = 0 and 0.05,
  and the statistic has no power below ~0.10.** Against that, the family's observed validation
  Sharpe spread is **0.304**. Two unrelated methods, one number: **this family cannot resolve
  a Sharpe difference below about 0.08–0.10, and selecting its validation-best member is a
  coin flip on out-of-sample rank.** This is the same conclusion the paired bootstrap reached
  from promotion steps (no promotion clears `|t| = 2`), reached a third way. *Do not re-run
  CSCV here* — it will not move without candidates less correlated than 0.978. *One artifact
  caught and discarded:* the regression of the winner's OOS Sharpe on its IS Sharpe has slope
  −0.98, which looks damning and is not — the same slope appears in the control with a **real**
  edge (−1.00) and in pure noise (−0.78), because conditioning on `argmax` induces it
  mechanically. Simulate under the null before believing any selection-conditional statistic.

- **Averaging pays only when its components disagree, and at `rho` ≈ 0.98 there is nothing
  left to average — the fourth averaging axis, and the first killed without a trial.**
  Formation-date (#46), instrument-subsample (#47) and rebalance-phase (#48) vintages all
  lost on top of the four-horizon base; buffer-band vintages were killed free at 0.963 weight
  overlap. **Cross-specification model averaging** — combining the *distinct constructions*
  the lab has already run rather than vintages of one procedure — is the natural response to
  the PBO finding above (if selection is uninformative, average instead) and it passes
  `research/SUMMARY.md` #2's design test, since these are estimates of the same quantity, not
  different return streams, so the capital-dilution tax does not apply. It dies on arithmetic.
  The average of stored return series *is* the averaged portfolio's return before the cost
  difference, and the combined book trades less than its legs, so the free number is a lower
  bound; best subset of each size, cherry-picked ex-post over all `C(13,k)` subsets and
  therefore an optimistic upper bound on any honest a-priori choice: **2-way 1.216, 3-way
  1.209, 4-way 1.205, 5-way 1.202, 6-way 1.197, all 13 1.150, against the champion's 1.229** —
  every one below, monotone decreasing in leg count. At `rho` = 0.978 across four legs the
  volatility falls ~1% (~0.012 Sharpe) while the pull toward the family mean costs several
  times that. **General form, and it now covers all four axes: the aggregation gain is bounded
  by the components' disagreement, so a family that has converged cannot be rescued by
  combining its members.** Check the correlation before proposing any combination.

- **The skip-month has a second structural consequence, and it is the opposite of the one
  that was retracted: it makes the monthly re-target sign-neutral.** `research/SUMMARY.md`
  #24 argued that a constant-weight re-target is a **contrarian** overlay partially cancelling
  the continuation bet, and named this the membership band's best remaining justification —
  a third one, distinct from the cost claim retired earlier and the risk-breadth claim that
  replaced it. Its premise is holdings-only measurable and it fails. Over the champion's 72
  monthly formation trades in validation (L1 weight units): total trade 0.6508, of which
  entries 0.1132, exits 0.0895, re-sizing of names held through **0.4481**; within that
  re-sizing the **pure drift-reset component is 0.0584 — 9.0% of all trade** — and a sign test
  of the executed re-sizing against the drift it undoes splits **0.2257 with / 0.2224 against,
  a contrarian share of 0.496**. There is no systematic contrarian trade for a band to
  suppress. The mechanism is not luck: the composite deliberately skips the most recent month,
  which is exactly the month whose drift the re-target undoes, so signal and drift are
  near-orthogonal by construction. **This does not revive the retracted "second use" claim** —
  that was about *riding* the trailing month in weighting, which #50 refuted at a cost of
  0.276. The point here is the reverse: the skip-month stops the re-target taking a position
  on that month in either direction. **The membership band now has no live justification of any
  kind on the K=1 base** — cost measured at 0.003, expectation refuted here, risk breadth the
  only surviving one and it is not on the gate's axis. (The band is *present* in the reinstated
  K=6 champion and its marginal value there has never been measured; #51 deleted it on K=1.)

- **[CORRECTION, arithmetic only] "Turnover reduction is a spent lever" was measured on the
  K=6 base and the current champion is not on it.** That entry prices the drag at "0.45%/yr ≈
  0.019 Sharpe" from 3.0x annual turnover. Recomputed: `mom_zscore_overlap6_hzn_avg4` 3.11x →
  0.47%/yr → **0.021** Sharpe, but the champion `mom_hzn_avg4_nobuffer` runs **8.32x → 1.25%/yr
  → 0.051** Sharpe. The champion trades 2.7x more and pays 2.4x the drag. **The conclusion
  survives and its reason changes**: 0.051 is still inside the 0.057 floor at `rho` > 0.99, so
  eliminating trading entirely would buy an unresolvable margin — but the entry should not be
  quoted as "the drag is negligible" for this book, and 0.019 is the wrong number for it.

- **A session may correctly spend zero trials, and the bar for doing so is now a table rather
  than a judgement.** Every idea constructible in this family on 2026-08-24 was screened
  against the closed-form floor before anything was written, and all of them failed: the
  two-speed fresh-core/overlapped-tail book (−0.09..+0.05 against a 0.11 floor), K=6 on the
  no-buffer base (−0.09 against 0.14), a log-return score transform (<0.045 against 0.057,
  since #54 prices all spacing information at 0.045), cross-specification averaging and the
  band's expectation argument (both killed outright by free measurements), and deleting the
  skip-month (large but negative by construction, and advised against by
  `research/SUMMARY.md` #11). **Two rules generalise from that exercise.** (i) The screen is
  cheapest applied to the *idea*, not the candidate — the closed form needs only a guessed
  correlation. (ii) **A rationale that would recover a mechanism the journal records as
  helping the holdout is holdout-informed and must be declined even when it is otherwise the
  best idea available** — the two-speed book was exactly that, and it is the first time the
  post-#43 corollary has bound a session prospectively rather than retrospectively.

- **The two splits have opposite resolving power, and the lab measured this only on the split
  that has none. This is the strongest and narrowest form of the ⚠ concern above; read it
  before the older statements of that concern, which it partly supersedes.** Three sessions
  error-barred *validation* comparisons and none had ever error-barred a *holdout* one. Applying
  the same Memmel/Jobson–Korkie closed form to every predecessor of the current champion — using
  only holdout Sharpe scalars already recorded in `trials.jsonl`, no 2024+ data loaded, no
  strategy re-run, no holdout look spent — gives:

      predecessor                          rho     d_val   t_val    d_hold   t_hold
      mom_12m_baseline                    0.896   -0.364   -1.98    +0.449    +1.60
      mom_zscore_overlap6_daily_trim #32  0.921   -0.122   -0.76    +0.533    +2.20
      mom_zscore_overlap6_hzn_avg   #41   0.928   -0.117   -0.76    +0.629    +2.71
      mom_zscore_overlap6_hzn_avg4  #42   0.939   -0.109   -0.78    +0.686    +3.22
      mom_zscore_hzn_avg4_k1        #43   0.991   -0.042   -0.77    +0.184    +2.24
      mom_hzn_avg4_k1_cohort_trim   #45   0.997   -0.028   -0.93    +0.122    +2.67

  **On validation not one of the six is distinguishable from the champion** (largest |t| = 1.98,
  four below 0.80). **On holdout five of six beat it at |t| > 2**, monotone in date-overlap
  content. The holdout window is *shorter* (683 days vs 1,562, SE inflated 1.51x), so this is
  the harder comparison, not the easier one. For #42 the gap clears |t| = 2 at any `rho` > 0.842
  against a 0.939 anchor, so it does not hinge on the unobservable holdout correlation. Upgrade
  the 2026-08-23 formulation — "the gate broke a tie and broke it the wrong way" — to: **the gate
  broke a tie on the one split with no resolving power, and the split that resolves disagrees
  five times out of six.** Boundaries: holdout `rho` is anchored on the validation value and the
  break-even is reported rather than relied on; the closed form is a *floor* on the error bar, so
  every |t| is an **upper** bound on the evidence; and the largest `t` values belong to the most
  correlated pairs, which is arithmetic, not corroboration.

- **Attenuation is the base case; inversion is the finding — and the split between them is now
  calibrated at p ≈ 0.01 rather than asserted.** `research/SUMMARY.md` #33 says that under any
  positive shrinkage `E(alpha|alpha_hat) = kappa*alpha_hat`, a candidate scoring lower on holdout
  than on validation is *predicted*, so the level drop this repo cited for six sessions carried no
  evidentiary weight. Correct, and the corollary was never tested: does the **shape** survive its
  own null? Two independent nulls, both run before the claim was believed — the discipline adopted
  after the `eta(q)` and CSCV-argmax episodes. (a) *Exchangeable holdout ranks* — validation is
  monotone by construction because the gate promotes only on a validation gain, while holdout is
  never selected on; exact enumeration over all 7! = 5,040 orderings, counting **any** split into
  an increasing prefix ≥3 and a decreasing suffix ≥3 so the post-hoc split point is paid for:
  **50/5040 = 0.0099**. (b) *Shrinkage plus correlated noise*, increments drawn at the closed-form
  paired SE between consecutive rungs, 200k sims: **P(shape) = 0.0163 / 0.0159 / 0.0140 / 0.0105 /
  0.0110 at `kappa` = 0.0 / 0.3 / 0.6 / 0.9 / 1.0.** Two unrelated nulls at p ≈ 0.01, and
  **P(shape) is nearly flat in `kappa`** — shrinkage moves the level and does essentially nothing
  to the shape, which is #33's claim turned into a number. **General rule, the third instance of
  the same habit paying: when an imported interpretation rule tells you half your evidence is the
  base case, calibrate the other half against that base case rather than simply keeping it.**

- **The bar a future candidate must clear is now a table, and its shape is this family's
  epitaph.** Composing #29's closed form with `research/SUMMARY.md` #32 (`MBF = exp(−Z²/2)`; at
  even prior odds a 5% posterior-null target needs `t` = 2.43), the validation Sharpe gain
  required is:

      rho to champion   0.999  0.997  0.990  0.978  0.950  0.939  0.900
      gain needed       0.044  0.076  0.138  0.205  0.310  0.342  0.438

  A candidate earns a *small* required gain only by being nearly identical to the champion — and a
  nearly identical candidate has no mechanism by which to produce even that. Buying a real
  mechanism means decorrelating, and at `rho` ≈ 0.90 the bar is **+0.438**, i.e. 1.229 → 1.667,
  half again above anything recorded here on any split. This is the same conclusion the
  resolution-floor entry above reaches, stated as the quantity a session actually has to
  pre-register against. **Apply this table, not the bare 0.057 floor, before writing any candidate
  file: state the expected `rho`, read off the required gain, compare to the pre-registered
  effect.** Nothing remaining in the four-horizon family clears it at any `rho`.

- **Breadth bought with leg disagreement is half-price — not free, and not full price — and
  the trial that measured it is the first to put two of this file's own calibrated constants
  in direct conflict.** The four horizon legs had always *nested*: every window ends at the
  skip-month, so the 63-day leg's data is a subset of every other leg's. #44 had moved the
  redundancy's *dispersion* (12x) and found a null; the *level* had never been moved. Trial
  #55 moved it to the extreme — four adjacent **disjoint** quarters over the same 12-month
  span, everything else bit-identical to the champion — and the premise was verified first,
  holdings-only: mean pairwise leg weight overlap **0.475 → 0.141**, the largest leg
  disagreement ever measured here (formation-date vintages 0.645, subsample folds 0.43–0.48,
  buffer bands 0.963). Two constants made opposite predictions. *(a)* "Breadth arriving from a
  decorrelated vintage costs nothing" (#41 → #42: 47 → 63 names at rising Sharpe and improving
  drawdown) predicted ≈ 0. *(b)* De-concentration at ≈ 0.05 Sharpe per 30% of HHI (#53)
  predicted **−0.077** on the measured −46% HHI. Observed **−0.037**, almost exactly halfway.
  **Restate (a) as a discount, not an exemption**: the concentration price is real on this
  axis and runs at roughly half rate when the names arrive from legs that disagree. #41/#42's
  "free" reading was the same effect at a far smaller de-concentration with a gain on the
  other side that happened to cover it.
  Three riders. **Live is now a precondition with no predictive content at five axes, not
  three** — this is the fifth live averaging axis to lose, and it is the extreme point of one,
  so the screens (overlap, core-vs-fringe) should be used only to kill, never to promote. The
  move is **de-risking, not dilution**: ann_ret −4.2pp against ann_vol −2.9pp, validation maxDD
  *improving* −27.8% → −27.4%, turnover 3.11x → 2.5x — another risk/return-dial pair like
  #32/#33, and one a human weighing risk might want to see. And a **pre-registration that was
  wrong in a useful way**: turnover was predicted to *rise* (each leg re-forms from a window
  sharing no data with its neighbours) and it *fell*. Leg disagreement damps book-level churn
  rather than adding to it, the same 1/N damping already measured across tranches, now across
  lengths. **Do not reason about a book's turnover from its legs' turnover.**

- **The horizon axis is closed by a bracket rather than an assertion, and the tool that closed
  it is a piece of paper.** `research/SUMMARY.md` #3 — write any trend/MA-type signal as its
  weight vector over past returns — sat unexercised for seven sessions. At *score* level an
  equal average of nested momentum legs **is** a single momentum score with a declining step
  kernel over the 252 days before the skip-month. Quarter weights, and the kernel's mean lag
  in quarters:

      #44 geometric 252/159/100/63   [0.569 0.254 0.114 0.062]   mean lag 1.670   -0.021 (K=1)
      #42 champion  252/189/126/63   [0.521 0.271 0.146 0.062]   mean lag 1.750    best
      #41 two-leg   252/126          [0.375 0.375 0.125 0.125]   mean lag 2.000   -0.008 (K=6)
      #55 disjoint  four quarters    [0.250 0.250 0.250 0.250]   mean lag 2.500   -0.037 (K=6)

  **The champion's kernel is bracketed on both sides** — flatter costs 0.008 and 0.037, more
  recency-tilted costs 0.021. The triage also **retrodicts #44 before any data**: geometric
  spacing moves the mean lag by 0.08 of a quarter, so a null was predictable on paper. Two
  boundaries: the bracket's arms sit on two different bases (K=6, K=1), so it is directional
  rather than paired, and all three margins are inside the family's resolution floor
  (0.03–0.14) — what is established is the *shape*, not any single gap. **Practical rule: any
  future proposal that is a linear filter over past returns — another spacing, another leg
  count, another nesting rule, an exponential or a "new" trend signal — should be written as
  its kernel and compared to the row above before a file is written.** Near-identical mean lag
  ⇒ re-parameterisation ⇒ no trial. Boundary from the source: linear filters only; it says
  nothing about the buffer, the magnitude transform, the tranche overlap or the trim.

- **[RE-FITTED AND PARTLY CORRECTED 2026-08-27 — read the entry below this one first; the
  mechanism asserted here for the miss is refuted, and #55 turns out not to have been a miss.]
  The risk-contribution statistic has a second miss, its slope does not survive a change of
  base, and this is the third instance of one general failure.** Three correct pre-registered
  drawdown calls (#52, #53, #54) and one recorded miss (#50, blamed on weight-vector
  staleness). Trial #55 misses again and **staleness cannot explain it** — #55 re-targets
  monthly exactly as the champion does. Effective risk bets +62% (8.54 → 13.84) predicts
  validation maxDD ≈ **−26.1%** at the recorded linear calibration (5.3pp per +195%); observed
  **−27.4%** against the champion's −27.8%. Sign right, size overstated ~3x. ~~The shape: every
  calibration point was fitted on the K=1 base at ~6 effective risk bets, and the reinstated
  base starts at 8.5 — a book whose drawdowns are already dominated by a factor common to all
  its vintages cannot diversify them away by holding more names, so the marginal drawdown value
  of a risk bet must fall as the count rises.~~ **Refuted 2026-08-27: the K=6 base has books
  down at 6.43 risk bets (8.5 is only where the champion sits), and restricting the K=1 fit to
  the K=6 span makes it *steeper*, not shallower — the level-of-count story predicts the wrong
  sign.** What survives is the instruction that followed it — the slope *is* base-specific and
  has now been re-fitted — and the general failure, now at three instances: #52 showed "the base
  has absorbed it" does not generalise across *components*, #54 showed the ordinal/cardinal
  share did not transfer across *leg counts*, and #55 shows a *calibration* does not transfer
  across *bases*. **A constant measured on one construction is a property of that construction
  until re-measured.**

- **The risk-contribution statistic is blind to every risk axis that is not cross-sectional and
  contemporaneous, and that one fact supplies its base-specific slope, both of its recorded
  "misses", and — for the first time — an error bar.** Re-fitted holdings-only on the eight K=6
  and eight K=1 books that have candidate files (75 sampled validation dates, 252-day trailing
  sample covariance), against recorded validation maxDD:

      base   n   effR span     slope (pp maxDD per risk bet)     r      residual SD
      K=1    8   5.94-17.61            +0.492                 +0.978     0.427 pp
      K=6    8   6.43-13.64            +0.322                 +0.733     0.784 pp
      K=6    5 (unique weight matrices) +0.214                +0.697         —

  The recorded +0.453 is **reproduced on its own base** (+0.492); on the reinstated base it is
  35–55% too steep. **Quote +0.32 for the K=6 base, not +0.45.**
  **The mechanism, and it is structural rather than statistical.** Risk contributions are
  computed on a **normalised, single-date** weight vector, so the statistic can only see risk
  sharing that is cross-sectional and contemporaneous. It is therefore blind to (a) **exposure
  scalars** — every de-risking overlay, i.e. the exact class of change a drawdown diagnostic is
  most often asked about — and (b) **formation-date diversity**, which this file already
  establishes as the date overlap's active ingredient. Both move maxDD. This is why the K=6
  slope is shallower at the same counts (part of a K=6 book's drawdown risk is already
  diversified along a temporal axis one date's covariance cannot report, so contemporaneous
  risk bets buy less on top), and it subsumes the ad-hoc "weight-vector staleness" story
  invented for #50.
  **The error bar, measured directly.** Five of the eight K=6 books are groups sharing a
  **bit-identical normalised weight matrix** — the trim is a pure exposure scalar and the
  diagnostic renormalises — so the statistic cannot distinguish them even in principle:
  #32/#38/#40 all sit at effR 6.4343 with validation maxDD −29.11 / −30.28 / −29.11 (**spread
  1.17pp**), and #42/#46 both at 8.4248 with −27.80 / −28.51 (spread 0.71pp). The K=6 fit's own
  residual SD is **0.784pp, max |residual| 1.207pp** — the regression's scatter *equals* the
  scatter among books it is blind to. **Operational rule: on this base, do not pre-register a
  drawdown call smaller than ~1.2pp; it is unfalsifiable.**
  **Consequence for the record: #55 was not a miss.** Its 1.32pp error (0.76pp at the
  unique-book slope) is inside that floor. The statistic's hit rate is better than the entry
  above records; what was actually missing was never an error bar at all, and this is the
  fourth time in this repo that a component's error bar, once computed, changed the reading of
  its point estimate.

- **`research/SUMMARY.md` #39's volatility-weighted cost multiplier, measured: the flat cost
  model under-charges this repo by ~1.4x, it is monotone in weighting concentration, and it
  changes no verdict.** Turnover-weighted ratio of traded names' 252-day trailing daily
  volatility to the universe median, over the full validation split (holdings-only):
  **champion 1.431**, range 1.221–1.466 across sixteen books, K=6 mean 1.427, K=1 mean 1.331.
  On the champion that turns 0.93%/yr of modelled drag into 1.34%/yr, i.e. **0.018 Sharpe** of
  cost the engine does not charge — against #39's pre-registered "even a 1.5x multiplier stays
  under ~0.03 Sharpe". Confirmed as stated. Two additions. The multiplier is **monotone in
  weighting concentration** (equal 1.221 < rank 1.293 < magnitude 1.367–1.388), which is #39's
  own mechanism observed directly: magnitude weighting tilts further into the high-volatility
  tail a flat bps charge under-prices. And although K=6 books carry the higher *multiplier*,
  the **Sharpe** correction is 2–2.5x larger on K=1 books because they trade 2.7x more — so the
  recorded #51-vs-#42 validation gap of **+0.109 narrows to +0.084** once both pay their true
  volatility-denominated cost. Still positive, still inside the resolution floor, verdict
  unchanged. **Carry the caution #39 attaches: this is a cost account, never an objective** — a
  book can lower it by holding placid names and lose far more on selection, which is the closed
  low-vol family.

- **The champion's construction is now fully mapped on its own base, which changes what the
  lab should ask a human for.** After #55 every component of the reinstated champion has a
  measured marginal value: signal definition, kernel shape, leg count, leg nesting, within-leg
  weighting, cross-leg agreement, membership band, weight anchor, tranche depth, re-target
  cadence, and the trim overlay. Each is at a local optimum or a refuted alternative, and every
  component measured only on the retired K=1 base carries a **negative** recorded sign on
  transfer (equal weighting −0.206, no agreement premium −0.043, rank weighting −0.106, weekly
  re-target −0.142, no re-target −0.276, subsample folds −0.021, phase vintages −0.076,
  geometric spacing −0.021, deliberate cohort trim −0.013 measured on *this* base by #46). The
  single exception with a positive recorded validation sign — deleting the membership band
  (#51, +0.109) — is **declined and should stay declined**: choosing it means reading the
  holdout replay table to pick something the veto will not catch, which is the holdout-informed
  reasoning the post-#43 corollary forbids, and its measured effect is to destroy 1.8 effective
  risk bets. **What is left is an input, not a construction.** `program.md`'s own
  human-approval-gated list names point-in-time survivorship-free constituents, fundamentals and
  intraday bars; `research/SUMMARY.md` #34–#36 (added 2026-08-26) put a magnitude on the first
  for the first time — up to 8%/yr of overstatement for this repo's literal recipe, with return
  up, volatility down and drawdown understated, flattering three of `program.md`'s own gates at
  once. A session that finds itself with budget left and no idea above the floor should say
  this rather than spend a trial re-deriving a recorded negative.

- **Regional neutralisation is closed by a bracket, and the bracket's shape is the general
  lesson: a mechanism can be real, large, and still unreachable.** `research/SUMMARY.md` #40
  was the folder's top-ranked buildable idea and the first grouping ever to pass its own #5
  neutralisation screen — for sectors the lab could name no mechanism and the trial duly lost
  0.16, while for regions the mechanism (large country-specific components in international
  returns) is documented. Its premise verified *stronger* than the note claimed: the champion
  holds **63.1%** North-American stock weight against a **35.8%** eligible-name share, a
  **+27.3pp** overweight swinging **43%–91%** across validation, and the four within-group book
  returns correlate only **0.32–0.61** against the 0.978 at which this family's candidates sit.
  It is by a wide margin the most decorrelated grouping available here. Three free measurements
  then closed it without a trial. *(a)* The candidate (within-group demeaning, everything else
  bit-identical) does work: regional-share standard deviations fall **34–52%**, weight overlap
  0.868, positions 62.7 → 64.3. *(b)* Decomposing the champion's own book as
  `R = Σ_g s_g(t)·r_g(t)` and freezing the group shares at their split means puts the **upper
  bound on the entire mechanism at +0.065** gross Sharpe (ann_vol 22.72% → 21.84%, of which
  +0.046 is the pure variance channel) — already under the twice-measured 0.08–0.10 resolution
  floor and under half the +0.138 the required-gain table demands at `rho` = 0.99; the candidate
  captures 34–52% of it, ≈ +0.03. *(c)* That +0.065 is **not constructible**: freezing at the
  realised split mean fits a parameter to the scoring split (forbidden by #22), and both targets
  needing no fitting lose — eligible-name shares **−0.167**, flat 1/4 per group **−0.083**.
  Two riders. Freezing the shares *raises* annual return 0.42pp, so the pooled sort's regional
  timing is mildly value-destroying and the book is not being paid for the bet — it simply
  cannot shed it more cheaply than it costs, which is the long-only discount (`SUMMARY.md` #4,
  #42) arriving on the variance side. And **live is now a precondition with no predictive
  content at six axes**, this being the extreme point of the strongest one: the #5 screen
  correctly separated a live grouping from a dead one and liveness still did not predict payoff.
  A screen that only ever kills is still worth running; it just may not be upgraded to a
  forecast.

- **The `±1.2pp` unfalsifiability floor bound a session prospectively for the first time, and
  the discipline it enforces is to decline to pre-register rather than to pre-register weakly.**
  Last session established that the risk-contribution statistic's K=6 residual scatter (0.784pp
  SD, 1.207pp max) equals the scatter among books it cannot distinguish even in principle, so a
  drawdown call smaller than ~1.2pp on this base is unfalsifiable. Tonight's candidate moved
  effective risk bets 8.73 → 8.06, predicting **−0.21pp** at the re-fitted +0.322 slope. No call
  was made. The general form, and it is the counterpart to "measure the premise before spending
  the trial": **once a diagnostic has an error bar, an effect inside it is not a small prediction
  but an absent one**, and recording it as a prediction would manufacture a hit or a miss out of
  noise — which is how this same statistic acquired two "misses" that later turned out to be
  inside its own scatter.

- **The only genuinely new signal the research folder has ever supplied is also the one this
  universe flatters most, and the screen that shows it is free.** `research/SUMMARY.md` #41
  (negative past-5-year return as a price-only value proxy) cannot have its *mean* priced
  without a trial, but its holdings can. Built under the champion's own buffer and magnitude
  machinery: weight overlap with the champion **0.054** — the most decorrelated object ever
  measured in this repo, next lowest being #55's disjoint legs at 0.141 — on **18.7** positions,
  **49** distinct names ever held, **59.7%** of book weight in a ten-name repeat cast, and a mean
  daily weight change of 0.008, i.e. it barely trades. The cast, several names held on all 1,562
  validation days: BP, HSBC, Barclays, BAT, Lloyds, Bayer, Deutsche Bank, GE, GSK, BASF, IBM,
  Exxon. Three consequences, converting the folder's three stated caveats into measurements and
  adding a fourth. At 0.054 overlap it is unambiguously a **different return stream**, so #2's
  design test applies and it pays the dilution tax measured here at ~0.015–0.02 Sharpe per 20%
  of capital. It is **near-static**, so it is a standing European-financials-and-energy tilt
  wearing a value label rather than a rotating signal. And that cast is the re-aimed
  survivorship caveat observed directly — every one of those names fell for five years and is in
  today's universe *because it survived* — so the conditioning lands squarely on the one quantity
  the free screen cannot bound. **A holdings-only screen can bound an idea's breadth, its
  concentration and its exposure to a known bias while leaving its sign completely open; say
  which of the three you have bounded before concluding anything.**

- **[PROGRAM CHANGE 2026-08-29 — scope note that applies to this entire file.] Almost
  everything above was measured on one family, and the file does not say so anywhere.** The
  lab's first 55 trials were 34 cross-sectional momentum, 8 combinations of it, 5 regime
  switches over it, and 8 others; all 7 promotions were in it. `program.md` now calls that
  one family, `price-trend`, and caps it at 2 trials a session. **Every calibrated constant
  in this file is a `price-trend` constant** — the ~0.05-Sharpe-per-30%-HHI de-concentration
  price, the required-gain table, the risk-contribution slope, the ±1.2pp unfalsifiability
  floor, the resolution floor `SE ≈ 0.568·sqrt(1−rho)`. The last of those is a property of
  the 1,562-day window and transfers; the rest were fitted on one construction and do not.
  `CLAUDE.md` now forbids carrying them into a new family by analogy. Re-measure, or say you
  have not.

- **Breadth was blocked by three mechanical constraints, not by the deflator, and the
  deflator excuse is now measured and dead.** Sessions had good reason to stay in one family:
  strategies received closing prices only (so every volume, liquidity and range mechanism was
  inexpressible), there was no estimator library (so learned models were unimplementable),
  and the only non-REJECT verdict was PROMOTE (so a 0.7-Sharpe result in a new family was
  indistinguishable in `trials.jsonl` from a broken one). All three are fixed. The fourth
  suspected blocker, the deflated-Sharpe bar, turns out never to have been one: at a
  1.2-Sharpe candidate, DSR runs 0.976 / 0.971 / 0.967 / 0.963 / 0.956 at 12 / 16 / 20 / 25 /
  35 effective trials, so thirteen extra *decorrelated* trials cost ~0.013 of DSR and stay
  clear of 0.95. Observed on the night: two decorrelated scouts moved the effective count
  12 → 13 → 14, one each, against 34 recorded price-trend trials that cluster into far fewer.
  **Exploring is cheap. It always was. What was expensive was having nowhere to record the
  result.**

- **The leaderboard's first act was to kill the idea it was built to enable, for free — and
  the kill is more useful than either trial that produced it.** With two decorrelated legs
  finally on the board (`lv_amihud_illiquidity_tilt`, val 0.681 at rho 0.589;
  `sl_ridge_xs_walkforward`, val 0.601 at rho 0.774), the obvious move is to blend one into
  the champion. Priced on the stored validation return series — no strategy re-run, no trial
  spent — every blend loses:

      leg                          rho     10%      20%      30%
      lv_amihud_illiquidity_tilt  0.589  -0.001   -0.008   -0.023
      sl_ridge_xs_walkforward     0.774  -0.028   -0.061   -0.100

  and a 20% Amihud blend would sit at rho 0.9897 to the champion, needing **+0.140** by the
  required-gain table to be resolvable at all. **A decorrelated leg is not enough; it has to
  be decorrelated *and* good.** The Amihud row shows the exchange rate precisely: at 10%
  weight its decorrelation almost exactly pays for its Sharpe deficit (−0.001), so a leg at
  rho ≈ 0.6 needs validation Sharpe ≈ 0.9 before a blend is worth a trial.
  **[THE "rho 0.6 NEEDS 0.9" TARGET IS SUPERSEDED 2026-08-29 (nightly) — see the blend
  arithmetic entry at the end of this file. Solved rather than eyeballed, break-even at rho
  0.6 is 0.749, not 0.9, and the leg's volatility ratio matters as much as its correlation;
  but the bar that actually matters is +2 SE on the blend's own rho, which needs the leg's
  own Sharpe at 1.34-1.42, i.e. better than the champion. The table below and the standing
  rule are still correct and still worth running.]** **Standing rule:
  run this table for any new leg before writing a blend candidate. It costs nothing and it
  has already saved one trial.** Note what this does *not* say — it prices blends against the
  gate's axis only, and `learnings.md`'s own ⚠ concern is that that axis has been the wrong
  one since #43. A leg whose blend is flat on validation and materially better on turnover
  and drawdown is still a thing a human weighing risk would want to see.

- **First reading on two new families, both first-of-family and both honest floors rather
  than leads worth chasing yet.** `statistical-learning` (ridge over eleven causal
  return/range/liquidity/volume features, refitted monthly walk-forward, val **0.601**) clears
  the 0.49 equal-weight floor and little else, and two things about *how* it fails are more
  informative than the number: 15.4x turnover costs it ~2.3%/yr, roughly a third of its
  margin over the floor, because a monthly rank target re-ranks the whole cross-section and
  nothing in the construction asks it to be stable; and three of its eleven features are the
  champion's own lookbacks, which is why its rho is 0.774 — **feed a learner the incumbent's
  features and it rediscovers the incumbent, worse.** `liquidity-volume` (single sort on
  trailing-quarter Amihud ILLIQ, val **0.681**) is the more interesting of the two despite
  scoring below the champion on every axis the gate reads: **1.0x annual turnover** (0.15%/yr
  of cost drag), the highest train Sharpe on the board at 1.001, and rho 0.589 — the most
  decorrelated non-trivial result the lab has. Neither is a challenger. Both are the first
  entries in families that had none, which is the point of a scout.


- **[Measured 2026-08-29, nightly] The blend arithmetic, done properly, says every resolvable
  champion+leg blend needs a leg better than the champion — which closes the "scout a
  decorrelated family, then blend it in" route as currently framed.** The informal target this
  file carried ("rho ~0.6 needs Sharpe ~0.9") was never solved; solved on the stored validation
  series, break-even for a leg of equal volatility at 20% weight is
  `S_x = S_c[sqrt((1-w)^2 + (wk)^2 + 2w(1-w)*rho*k) - (1-w)]/(wk)`, giving 0.554 / 0.652 /
  0.749 / 0.844 / 0.938 / 1.029 at rho 0.40 / 0.50 / 0.60 / 0.70 / 0.80 / 0.90. Two corrections
  fall out. The old rule was too *pessimistic* at rho 0.6 (0.749, not 0.9), so the Amihud leg is
  0.044 short of break-even rather than 0.22. And it omitted `k`, the leg's volatility ratio,
  which moves the bar as much as correlation does — a low-vol leg is materially cheaper to
  blend. **But break-even is not the bar.** A 20% blend sits at rho 0.987-0.994 to the champion,
  so this file's own resolution floor `SE = 0.568*sqrt(1-rho)` puts one paired SE at 0.044-0.064
  and a two-SE improvement needs the leg's own Sharpe at **1.34-1.42** against the champion's
  1.120. Recorded legs: Amihud 0.681 (needs 1.375), ridge-nontrend 0.634 (1.382), group-lead
  0.688 (1.402), seasonal 0.747 (1.415), short-term reversal 0.820 (1.418). The gap between what
  the promotion gate would *accept* (any margin over break-even) and what would be
  *distinguishable from noise* is roughly a factor of two in required leg Sharpe, which is this
  file's standing ⚠ concern arriving on a new axis. Curiosity, not a proposal: `lowvol_equity_tilt`
  — refuted on its own terms — is the only leg on record whose blend point estimate is positive
  (+0.003 at 10%), purely on low rho and low vol.

- **[Measured 2026-08-29, nightly] Family breadth does not buy portfolio decorrelation on a
  long-only book, and this is now measured rather than assumed.** Five family leads from five
  different mechanisms — illiquidity, a learned non-trend block, group lead-lag, calendar
  seasonality, short-term reversal — correlate **0.75-0.85 with each other** on validation. An
  equal-weight ensemble of all five sits at rho 0.740 to the champion, barely below its best
  single member's 0.698, and blends into the seat at -0.010 / -0.025 / -0.045 at 10/20/30%.
  The reason is structural: every one of them is a long-only book over the same ~140 names and
  carries the same market beta, so mechanism diversity does not become return diversity. The
  scout programme's premise — different families give decorrelated legs — holds against the
  *champion* (rho 0.59-0.75, genuinely lower than `price-trend`'s 0.94-0.95) and fails against
  *each other*. Price that into what the leaderboard can be expected to produce.

- **[Measured 2026-08-29, nightly] Outside `price-trend`, turnover differences dominate every
  mechanism comparison the lab tries to run — four consecutive trials, four times.** #56 → #61:
  removing the incumbent's features and fixing the target horizon and band moved validation
  0.601 → 0.634, but gross of costs the new feature block is *worse* (0.690 vs 0.724); the
  entire net gain is the turnover fix (15.4x → 6.0x, worth ~+0.09) minus a feature-swap loss
  (~-0.05). #59 → #60: a date-alignment fix moved 0.671 → 0.747 and turnover 12.4x → 17.1x.
  #58 → #62: holding the laggard half of each leading group instead of all of it scored 0.665
  vs 0.688 net, but 0.848 vs 0.830 *gross* — the sign flips on 4.5x of extra turnover. The
  general form: the cross-sectional signals available outside the incumbent's family are weak
  enough (Q5-universe spreads of 1-7%/yr, ICs of 0.01-0.04) that a 5-10x turnover difference
  swamps them. **A scout that changes selection and turnover at the same time cannot answer a
  mechanism question.** Hold turnover fixed by design, or report the gross decomposition
  explicitly, or accept that the trial measured the broker.

- **[Measured 2026-08-29, nightly] A penalised linear combiner on a 140-name monthly
  cross-section reproduces its own best input, worse — twice, one level apart.** Fed eleven
  features including the champion's 12-1/6-1/3-1 lookbacks, the ridge came back at rho **0.774**
  to the champion and Sharpe 0.601. Fed a four-feature block with the trend features deliberately
  removed, it came back at rho **0.976** to `lv_amihud_illiquidity_tilt` — an unconditional
  single sort on one of its four inputs — and Sharpe 0.634 against that sort's 0.681. This is the
  reachable version of `SUMMARY.md` #51's warning that estimator ranking is noise at this
  cross-section size. **Design rule: a learned candidate is worth a trial only if its feature
  block contains no single member that already works on its own, or if the model is asked for
  something a sort cannot express** — an interaction, a state-dependence — rather than for a
  better ranking of the same names.

- **[Measured 2026-08-29, nightly] Check date alignment against the *trading* calendar, and treat
  unexpectedly low turnover as a symptom rather than a result.** Rebalance dates in this repo are
  the last *trading* day of each month, which on **29.8%** of train-split months is not the last
  calendar day. On exactly those months `date + MonthEnd(1)` rolls forward only to the calendar
  month-end and returns the month that has just *ended*. Trial #59 carried that error and #60 is
  the identical file with the one expression changed to `MonthBegin(1)`: validation 0.671 →
  **0.747**. The same class of error is live in
  `strategies/lib/features.seasonal_same_month_return`, which averages the month that has just
  ended and is therefore traded one month late — measured on train as a null (Q5-Q1 -0.49%/yr,
  t = -0.17) where the corrected alignment gives +15.7%/yr (t = +5.16). The lib file is left
  untouched per the file-permission rule; candidates should carry their own corrected version.
  The transferable half is the detection story: the bug **lowered** turnover 17.1x → 12.4x,
  because repeating the previous month's target stabilises holdings. A stale-signal bug presents
  as a cheaper book, so any screen that prefers low turnover will prefer the broken version.

- **[Measured 2026-08-29, nightly] Three families were declined on free train-split screens, and
  the screens are worth more than the trials would have been.** *(a)* `range-variance`: GK vol
  compression (Q5-universe -0.79%/yr, t = -0.15), vol-of-vol (-2.21%/yr, t = -1.56), the
  close-to-close/GK variance ratio (+0.07%/yr, t = +0.04) and the range-lottery measure
  (-7.95%/yr, t = -4.30, which is just low-vol) are all null or negative. That also answers
  `SUMMARY.md` #47's open question — **the low-vol refutation was never estimator-limited**: a
  7.4x-efficiency range estimator reproduces it slightly *more* strongly than close-to-close vol
  (t = -4.15 vs -3.25). Incidentally the high-minus-low vol spread of **+19.4%/yr on train** is
  this universe's survivorship bias observed directly, and bounds the order of magnitude by which
  it distorts any vol-sorted result here. *(b)* `statistical-arbitrage`: its premise is that
  removing factor structure improves reversal, and here it does the opposite — raw 5-day reversal
  IC **+0.0455 (t = +4.49)**, one-factor residual +0.0375, PCA k=3 +0.0331, PCA k=5 +0.0336. The
  surviving object is raw 5-10 day reversal, decaying to a null by 21 days, i.e. **the strongest
  signal measurable on this universe sits exactly at the horizon the cost model structurally
  forbids** (#18: the premium pays liquidity *providers*, and a book paying 15 bps a side is on
  the other side of it). *(c)* `liquidity-volume`: `SUMMARY.md` #46 predicted from a tier-1
  commissioned replication that log mean dollar volume would beat Amihud `ILLIQ`. Refuted here —
  `ILLIQ` Q5-universe +1.72%/yr (IC +0.0118), ratio-of-means +1.92%/yr (IC +0.0133), **log ADV
  -0.32%/yr (IC +0.0010, t = +0.11)**, a clean null — while the rank correlations replicate the
  source exactly (0.929 and 0.993), so the disagreement is about which end of a near-identical
  ranking pays, not about the measures. Likely cause: on 140 mega-caps log ADV is a pure size
  ranking with no illiquid tail. #45's confound is settled at the same time: `ILLIQ` **within**
  trailing-volatility terciles gives +2.01%/yr (t = +0.84) against the unconditional +1.72%/yr,
  so the existing scout is not a disguised volatility tilt.

- **[2026-08-29, nightly] `SUMMARY.md` #48's pre-registered screen failed and the session argued
  past it; the trial then confirmed the screen.** Heston-Sadka's identifying claim is a *sign
  disagreement* — annual lags positive, non-annual months negative. Measured on train: annual
  +15.7%/yr (t = +5.16), non-annual **+12.8%/yr (t = +3.70)**, both positive, so the contrast
  that separates a calendar seasonal from persistent cross-sectional mean-return differences is
  absent here. The session ran the trial anyway because orthogonalising the two leaves
  +11.7%/yr (t = +3.97), and bought a floor: validation 0.747 at **rho 0.753 to a momentum
  champion** and 17.1x turnover costing ~2.6%/yr. A calendar effect has no business correlating
  0.75 with a four-horizon trend book. **Treat a failed pre-registered screen as an answer, not
  as a hurdle to argue past** — the supplementary control that justified proceeding was real and
  still did not rescue the identification.

- **[Measured 2026-08-30, nightly] A cross-sectional quintile screen over-predicts the book
  it motivates by roughly an order of magnitude, and the lab has been designing candidates
  on it for two sessions.** The exchange rate is now calibrated on a pair built so that
  nothing else could move: `lv_trading_time_reversal` and `pt_raw_reversal_control` differ in
  one expression, run **16.7x against 17.6x** annual validation turnover at **21.8 against
  21.8** average positions, and the score change was worth **+3.35%/yr of Q5-universe spread
  on train** (a null at t = 1.27 turned into a signal at t = 2.81). It bought **+0.03 of
  train Sharpe and −0.11 of validation Sharpe.** The reason is structural, not statistical:
  a 20-name book with a hold-30/enter-20 band holds a **tail**, not a quintile, and
  re-ranking inside that tail moves the quintile statistic far more than it moves the book.
  Applied prospectively the same night, the discount was right — #66 was pre-registered at
  ~+0.04 by this rate against an observed −0.054, inside the same noise band. **Screen on the
  statistic the trial will be scored on. Use the quintile spread only to kill, never to
  size an expectation** — which is the same standing instruction the overlap and
  core-vs-fringe screens already carry, now with a measured magnitude attached.

- **[Measured 2026-08-30, nightly] Outside the incumbent's family, train advantage has
  anti-predicted validation advantage in every reading the lab has taken — three for three,
  two of them designed pairs. Suggestive, not established, and stated with its own null.**

      reading                        train                      validation
      #63 residual excursion         Q5-uni +6.14%/yr (t=4.18)  0.468, below the 0.49 floor
      #64 vs #65 volume rescaling    +0.030 Sharpe              -0.111 Sharpe
      #66 vs #65 5d vs 21d score     +0.119 Sharpe              -0.054 Sharpe

  From `trials.jsonl` scalars alone (free): `corr(train, validation)` is **+0.697** over the
  57 legacy `price-trend`-lineage trials (p < 0.001) and **−0.322** over the 11 trials since
  the 2026-08-29 program change (spearman −0.400, **p = 0.33**), with the ordering nearly
  inverted inside those 11 — the two highest train Sharpes sit near the bottom on validation
  and the two lowest sit at the top. **Three honest caveats.** (i) Nothing here is
  significant: p = 0.33 on the correlation, and 3-of-3 sign agreement is p = 0.25 two-sided.
  (ii) The legacy +0.697 is partly an artifact of 57 near-identical variants of one
  construction, so the smaller sample is the *cleaner* one, which cuts both ways. (iii) There
  is a mechanism and it is **selection**: all 11 were designed after a train screen, so the
  highest train Sharpes belong to the candidates their screens flattered most, which is what
  screen-overfitting looks like from outside — and it is the reading the entry above
  supports. **The competing reading cannot be adjudicated without the holdout and must not
  be**: this file's ⚠ concern records `corr(train, holdout) = +0.887` on the promotion
  ladder, so if train is the split that tracks the holdout then validation is the split that
  is wrong, and tonight is that concern arriving prospectively on five families it was never
  measured in. **Cheapest way to resolve it: every future scout should record its train
  Sharpe as a pre-registered prediction of its validation Sharpe.** At n ≈ 25 the sign
  becomes readable; it costs nothing but writing the number down.

- **[Measured 2026-08-30, nightly] Signal horizon and rebalance frequency are separate
  choices, and "the strongest signal sits at the horizon the cost model forbids" conflated
  them.** At ~21 trading days of spacing a 5-day, a 10-day and a 21-day lookback are all
  **fully disjoint** from their predecessor, so a monthly book pays the same churn whichever
  it scores on: **11.82x / 11.93x / 11.93x** holdings-only on train at an identical 24.3
  names, and **17.3x against 17.6x** observed on validation. The cost objection therefore
  never applied to a monthly book at all. What survives is a *decay* argument, now with its
  first direct evidence: holding the grid fixed, the 5-day score lost **0.054** of validation
  Sharpe to the 21-day one (0.647 vs 0.701) while winning **0.119** on train. A 5-day
  excursion reverts inside the holding month, so a monthly book collects its front and then
  holds a spent position for three weeks. **Restate the claim as "the 5-10 day reversal
  premium is unreachable on a monthly grid because it decays inside the holding period"** —
  a different mechanism from `SUMMARY.md` #18's liquidity-provision account, and unlike that
  one, measurable here. General form, and it is the fourth instance of this repo's oldest
  habit: **before crediting a constraint, check which quantity it actually binds.**

- **[Measured 2026-08-30, nightly] Reversal, not any of the six new families, is the
  strongest non-incumbent mechanism on this universe — and the IC screen that dismissed it
  was asking the wrong question.** A plain 21-day reversal book (20 names, hold-30/enter-20,
  equal weight, monthly) scores validation **0.701** net of 15 bps at 17.6x turnover, second
  only to `str_reversal_monthly`'s 0.820 — and those two correlate **0.98**, so they are one
  object and their gap is inside the resolution floor. Meanwhile the train cross-sectional
  IC at 21 days is a null (+0.0102, t = +0.97). **A null IC and a 0.70-Sharpe book coexist
  because the book buys the extreme tail, not the quintile mean**, which is the same
  tail-versus-quintile point the calibration entry above makes from the other direction.
  Two riders. Reversal books here are cheap in Sharpe and **expensive in drawdown** —
  validation maxDD −38.1% to −38.5%, train −48% to −57%, against the champion's −27.8%. And
  nothing on this board is blendable into the seat: by this file's own solved break-even
  table a leg needs its own Sharpe at 1.34-1.42, and 0.820 is the best there is.

- **[Measured 2026-08-30, nightly] `portfolio-learning` is closed on arithmetic before its
  first trial, by the same bound that closed cross-specification averaging.** Priced on
  stored validation return series (no strategy re-run, no trial spent) and cherry-picking
  the best subset of each size *ex post* — an optimistic upper bound on any honest a-priori
  choice — equal-weight ensembles of the eight recorded legs give **0.834 / 0.829 / 0.819 /
  0.806 / 0.795 / 0.780 / 0.744** at 2..8 legs, monotone decreasing, against the **best
  single member at 0.820**. The whole ex-post-optimal gain is **+0.014**. The cause is in the
  correlation matrix: the legs correlate **0.68-0.98** with each other, and two pairs are
  effectively one object — `lv_amihud_illiquidity_tilt` with `sl_ridge_nontrend_block` at
  **0.98** (the learned combiner reproducing its own best input, confirming the 2026-08-29
  holdings reading of 0.976 on the return series) and `pt_raw_reversal_control` with
  `str_reversal_monthly` at **0.98**. An allocator over these allocates over one thing. This
  is the aggregation bound already recorded — *the gain is bounded by the components'
  disagreement* — reaching the family `program.md` names as "where scouted leads become a
  challenger", and it agrees with `research/SUMMARY.md`'s own 2026-08-30 downgrade of the
  HRP half.

- **[Measured 2026-08-30, nightly] Three more families declined on free screens, and one of
  the nulls passes its own design test — which makes it the informative kind.** *(a)*
  `lead-lag-spillover`: `SUMMARY.md` #53's `DELAY` (Dimson regression on an equal-weight
  universe return with five leads and five lags) is a monthly null — IC **−0.0016
  (t = −0.18)**, Q5-universe +2.04%/yr — and it **fails screen (iii) of #52**, which requires
  horizon decay: the effect is *larger* at three months (+6.85%/yr, t = +1.95) than at one,
  the signature #52 assigns to a slow-moving risk proxy. It is also computable for a mean of
  only **57 names** per date. *(b)* `range-variance`, now seven screened mechanisms over two
  sessions: close-location value carries the **wrong sign** for its own story (IC −0.0208,
  t = −2.48 at 21 days) and rank-correlates **+0.384** with the trailing 63-day return, i.e.
  reversal in costume; and the overnight/intraday decomposition loses to not decomposing —
  overnight sums give Q5-universe +4.33/+5.59/+4.13%/yr against the plain trailing 63-day
  *total* return's **+7.36%/yr (t = +3.48)**, with IC null throughout. *(c)*
  `liquidity-volume`: #53's relative-volume substitute for the uncomputable turnover sort
  does exactly what it is designed to do — `spearman(rel-volume, log ADV) = **+0.045**`
  against the ≈0.78 the note reports for raw and dollar volume — **and predicts nothing**
  (IC |t| ≤ 1.06 at every horizon). With the 2026-08-29 log-ADV null, that says the family's
  live content is `ILLIQ`'s **price-impact numerator** and not trading activity under any
  normalisation, which answers the Lou–Shu question `SUMMARY.md` flags as its natural
  follow-up without the paper. **A null that passes its own identifying test is worth more
  than one that fails it: it rules out the mechanism, not the measurement.**

- **[PARTLY RETRACTED 2026-09-01 — the mean/max *result* below stands and is strengthened by a
  fourth rung; its *explanation* does not, and the standing pre-trial screen it promotes is
  withdrawn. Read the 2026-09-01 entries at the end of this file before using anything here.
  In short: the "tail depth" the entry credits is measured in each operator's own raw score
  units and is not scale-free; standardized, every one of these books reaches the same
  1.46-1.56 SDs into its own distribution, because they all hold the top ~20 of ~140 names and
  therefore buy the same quantile by construction. `sqrt((1+(n-1)rho)/n)` predicts the
  composite score's *dispersion* ratio, not the depth of the book, and the two coincide only if
  book size is fixed in score units rather than in names.]**
  **[Measured 2026-08-31, nightly] The aggregation bound this file states five times — "the
  gain is bounded by the components' disagreement" — is a property of *averaging* operators,
  not of aggregation, and reading it as the latter cost the lab a family.** Every prior
  aggregation result here used a mean: cross-specification model averaging, the five vintage
  axes, the 2026-08-30 ensemble arithmetic that closed `portfolio-learning`, and #67. A mean
  of `n` scores is bounded between its components by construction; a **max** is not. Over one
  fixed set of four family-lead signals, with the book construction, universe, warmup and
  turnover held bit-identical, the operator is worth more than any mechanism the lab has found
  outside the incumbent's family: mean 0.635 (#67), max-of-rank 0.877 (#69), **max-of-z 1.008
  (#68)**, against the best single leg's 0.747 and legs at 0.681 / 0.747 / 0.688 / 0.701.
  #68 is the **best non-`price-trend` result ever recorded here** (previous best 0.820), at
  validation maxDD **-27.6%**, better than the champion's -27.8%.
  **The mechanism, and it is now closed-form.** These signals pay only in their extreme tails —
  a null 21-day reversal IC (+0.0102, t = +0.97) coexists with a 0.701-Sharpe book — and
  averaging shrinks the tail the book buys. For `n` equicorrelated legs the mean operator's
  tail depth relative to a single leg's own is **`sqrt((1 + (n-1)*rho) / n)`**, verified on two
  leg sets an order of magnitude apart in correlation:

      leg set                    mean pairwise rho   predicted   observed
      four mechanisms (train)          0.054           0.539       0.448
      four mechanisms (validation)     0.070           0.550       0.464
      four horizons   (train)          0.646           0.857       0.873
      four horizons   (validation)     0.669           0.867       0.870

  **Use it as a free pre-trial screen for any aggregation proposal in any family**: state the
  leg correlation, read off the mean operator's tail-depth penalty, and propose a max-type
  operator only when the penalty is large. Near-exact at high correlation; it over-predicts by
  ~0.09 at low correlation, where rank correlation and a top-20 tail mean both depart from its
  linear-correlation assumption — a guide, not a law.
  **Corollary that inverts a standing reading: orthogonality is not free breadth under a mean,
  and it is exactly what makes a max work.** The same |rho| ~ 0.05 across four legs is priced at
  **-0.112** by the mean and **+0.261** by the max, both against the best single leg. It also
  closes the `SUMMARY.md` #60 question properly: the family's 2026-08-30 closure *was* measured
  on a confounded statistic (return-series rho 0.68-0.98 against cross-sectional signal rho
  0.054/0.070, the gap being the common long-only market component), and correcting it reopens
  the family — but not for the reason #60 gave. #60's own rationale, that integration buys names
  "jointly attractive but top-decile on none", is false here: **97.6% / 93.2%** of #67's picks
  sit in some leg's own top-20.

- **[Measured 2026-08-31, nightly] Report a mechanism's effect over the arbitrary implementation
  choices it contains, not at the one that scored best — and run the alternative *before*
  quoting the number.** #68's max-of-z at 1.008 and #69's max-of-rank at 0.877 differ only in a
  scoring transform with no principled basis. Measured: `rho` = **0.9690**, closed-form paired
  SE **0.100**, gap 0.131 at **t = +1.31** — **not distinguishable**, so nothing licenses
  preferring either. What survives is the mean/max distinction (max beats mean by +0.373 and
  **+0.242**, the latter at t = +1.53; both max books beat all four legs); what does not survive
  is the *level*. This matters because the level is what a blend is priced on: at rho 0.73 and
  k 0.78 the solved break-even at 20% weight is 0.833, so **this is the first leg in this repo's
  history to clear its own break-even bar on either reading** — and the 20% blend delta is
  **+0.024 (t = +0.53)** at 1.008 and **+0.003 (t = +0.06)** at 0.877. The leg's entire blend
  value swings from "the first positive row ever recorded" to zero across a coin flip.
  **Quote 0.88-1.01 as a range, never 1.008 as a point.** This repo has three recorded cases of
  a headline turning out to be a property of an incidental implementation detail — the `dropna`
  trim cohort (four trials), the forward-fill weight-drift claim (two trials), the
  `MonthEnd`/`MonthBegin` alignment — every one caught *after* being built on. This is the first
  caught before, and it cost one trial.

- **[2026-08-31, nightly] A session declined a challenge it could have won, and the arithmetic
  for declining is the same table that has been in this file since 2026-08-25.** The new leg
  blends into the seat at 1.144 against the champion's 1.120 at 20% weight — it would have
  beaten the champion on validation, plausibly cleared DSR, **reached the holdout gate, spent
  the one unspent split and ended the session**. At the blend's rho of 0.993 the required-gain
  table demands **+0.076 to +0.138** and the point estimate is **+0.003 to +0.024**, i.e. ~0.5
  paired SE. That is exactly the unresolvable margin the ⚠ standing concern is about, and
  promoting on it would have been the sixth instance of the gate breaking a tie on the split
  with no resolving power. **The productive move on a promising leg is to raise the leg's own
  Sharpe toward the 1.34-1.42 that makes a blend resolvable, not to cash a half-SE win into a
  holdout look.** Recorded as the first time this file's own required-gain table has bound a
  session away from a candidate that would have *promoted*, rather than one that would have
  failed.

- **[Measured 2026-08-31, nightly] Three families closed on free screens, one of them the last
  named `program.md` sub-mechanism with no coverage.** *(a)* **`liquidity-volume`**:
  `SUMMARY.md` #58's constant-Amihud `A_C = mean_d(1/dollar_volume)` was argued to be a
  different cross-sectional object from the volume functionals already screened, because it is a
  mean of reciprocals rather than a function of the mean. On train, **spearman(log `A_C`, -log
  mean dollar volume) = +0.993** — there is no Jensen gap on this universe, and by the note's own
  pre-registered rule the family closes properly, `A_C` inheriting log ADV's measured null. The
  source's corr(`A_C`, `ILLIQ`) ~ 0.90 replicates (0.933). *(b)* **ETF-versus-constituent
  lead-lag**, reachable (9 SPDR sector ETFs + VNQ; 8 groups with >= 4 constituents) and dead: the
  ETF's residual of the existing member-median control is a null at every horizon pair
  (IC -0.0095 / -0.0086 / +0.0057), so the ETF is not a new leader; #59's negative-move asymmetry
  has the right sign but t = 1.43, **fails #52's screen (iii)** (flat from one month to three),
  and sits on the leg long-only cannot reach, while the reachable side is a null at t = +0.07.
  *(c)* **`range-variance`**, declined a third session and now with one cause for all eight
  screened mechanisms: the seven previously screened all sort on a cross-sectional **level**, and
  the level *is* the survivorship artifact (raw GK level IC +0.0766, t = +5.75; the +19.4%/yr
  high-minus-low vol spread on train). A within-name de-levelling — 21-day range vol against the
  name's own 252-day baseline — is a clean null (IC +0.0087 / +0.0132, t = +1.00 / +1.56).
  **Remove the level and nothing is left.** `range-variance` is now the only family with zero
  recorded trials, and no session can honestly propose a candidate there on current evidence —
  flagged for the human against `program.md`'s cold-family allocation rule.

- **[Measured 2026-09-01, nightly] The statistic that explained this lab's best
  non-`price-trend` result does not survive standardisation, and the mechanism it named is not
  identified. This retracts the tail-depth account and the pre-trial screen built on it.** The
  2026-08-31 entries explain the aggregation ladder — max-of-z 1.008, max-of-rank 0.877,
  mean 0.635 — by "these signals pay only in their extreme tails, and a mean shrinks the tail
  the book buys", measured as the held book's mean score **in its own raw units**, and promote
  `sqrt((1+(n-1)rho)/n)` to a standing pre-trial screen. Trial #70 added a fourth rung (the
  k=2 order statistic, 0.753) and a free follow-up measured three candidate depth statistics
  over 325 month-ends:

      operator        Sharpe   (1) own-score   (2) standardized   (3) max-scale
      max (k=1)        1.008       2.136            1.562             2.136
      max-of-rank      0.877       0.977            1.127             2.087
      k=2   (#70)      0.753       1.120            1.524             1.676
      mean  (#67)      0.635       0.651            1.464             1.783

      corr with Sharpe            +0.876           -0.053            +0.845

  Statistic (2) — the book's mean score in **cross-sectional SDs of that operator's own
  score**, i.e. how far into its own distribution the book actually reaches — is **flat at
  1.46-1.56 and correlates -0.053 with Sharpe**. It is flat by construction: every one of these
  books holds the top ~20 of ~140 names, so they buy the **same quantile** and cannot differ in
  tail depth. (1) and (3) track Sharpe only because they are **not scale-free** — the maximum of
  four z-scores has a wider right tail than the second-largest or the mean, so "own-score depth"
  reports the operator's own score *dispersion*. `max-of-rank` settles it: shallowest
  standardized depth of the four, second-best Sharpe. The formula predicts the composite score's
  dispersion ratio, which equals a depth ratio only if book size is held fixed in *score* units
  rather than in *names*, and it never is here. **The ladder is real; the explanation is void.**
  Do not price a construction against the 0.245-Sharpe-per-unit rate read off statistic (1) —
  the narrowing, depth-weighting and leg-count levers the 2026-08-31 session listed were all
  priced that way and their prices are withdrawn.
  **General form, and it is this repo's oldest habit arriving on a descriptive statistic rather
  than on code: before crediting a mechanism, check that the statistic naming it is invariant to
  the thing it is not supposed to measure.** Four prior instances were components whose code did
  not read what they claimed (the `dropna` trim cohort, the forward-fill drift claim, the
  `MonthEnd` alignment, `eta(q)`'s estimability). This is the same failure one level up.

- **[Measured 2026-09-01, nightly] What the max operator buys is the union of the legs' tails,
  and the arbitrary normalisation it needs is removable for free. Better than quoting a
  mechanism's span over its incidental choices is building the object that has no span.** Two
  designed pairs, turnover matched holdings-only in advance, settle what the operator is doing.
  *(a)* Requiring **two** legs to endorse a name (the k=2 order statistic, everything else
  bit-identical, turnover 13.18x against 14.55x) costs **-0.255** (`rho` 0.8999, SE 0.180,
  t = -1.42), so the winner's-curse account is refuted. *(b)* Freezing each leg's contribution
  at a **fixed quota** — hold the union of the top 5 names of each leg, never letting the share
  float — scores **0.958** against 1.008 (`rho` 0.9663, SE 0.104, **t = -0.48**), so the
  date-conditioning (per-leg share sd 0.10-0.18, reaching 0.850 of the book in one month) is
  worth nothing measurable. The union of tails is the whole mechanism.
  **The fixed-quota book is invariant to any strictly monotone per-leg transform** — verified,
  not asserted: rebuilt on percentile ranks and on `exp(z)`, **bit-identical** to the z-scored
  book on every date. That removes the exact arbitrariness #69 could not resolve (max-of-z
  against max-of-rank, `rho` 0.9690, t = +1.31, level swinging 0.877-1.008). The reason is
  structural: a `max` compares **across** legs and therefore needs them on a common scale, and
  there is no principled common scale for an illiquidity ratio, a seasonal mean and a 21-day
  return; a quota only ever ranks **within** a leg, where every monotone transform agrees.
  **Standing rule: when an aggregation rule requires cross-component comparability, the
  normalisation it needs is a free parameter in disguise — prefer the rule that needs none, and
  check invariance by rebuilding the weight matrix under an alternative transform, which costs
  nothing.**

- **[FAILS ITS OWN CONTROL 2026-09-02 — read the union-partner triple near the end of this file
  before using this entry. A placebo partner (a hash of the date and the ticker, reading no market
  data) is maximally independent and maximally insignificant and buys +0.017 against the same
  baseline, so independence is NOT sufficient. The +0.175 gap below is untouched; what dies is the
  per-leg linear reading of it, including the "+0.175/3" arithmetic used to decline a fifth leg.]**
  **[Measured 2026-09-01, nightly] A leg earns its place in a union book by being independent,
  not by being individually significant — which inverts the screen a session would naturally
  apply.** Rebuilding the strongest leg alone under the union's own machinery and its own
  joint-coverage pool (#72) gives **0.782** against the four-leg union's 0.958: gap **+0.175**,
  `rho` 0.9119, SE 0.169, **t = +1.04**, or **+0.13** net of the control's measured cost
  handicap (19.0x against 13.7x turnover). Suggestive, not resolvable — but the direction is
  corroborated by a free train decile screen that points the *opposite* way at leg level:
  `seasonal` decile-10 excess **+10.59%/yr (t = +4.16)** against **+3.37 / +2.85 / +1.90** at
  t = +1.68 / +0.76 / +0.54 for illiquidity, group-lead and reversal, with no leg showing a
  reliable non-monotone shape. **Three legs with no individually significant cross-sectional
  content add ~0.18 to a book built on the one leg that has it.** They add *timing
  independence*, not signal: at cross-sectional |rho| 0.054-0.070 the months in which one leg's
  tail is wrong are unrelated to the months in which the others are, so a 20-name book drawn
  from four near-orthogonal tails carries far less month-specific idiosyncratic risk than a
  20-name book drawn from one. It also explains the turnover direction, which the pre-screen got
  backwards: **the union trades less than any of its legs** (13.7x against 19.0x), the same 1/N
  churn damping already recorded across tranches and across lookback lengths.
  Two riders. The machinery confound this trial existed to remove is worth only **+0.036**
  (t = +0.65), so every earlier leg-versus-union comparison in this family **stands as
  recorded**. And the claim rests on one retrospective reading; the prospective test — adding a
  fifth, maximally orthogonal leg — is a ~0.03 effect against a ~0.10 floor and must be run as a
  **leg-count contrast wide enough to resolve** (2 legs against 4 and 5), not as a single
  marginal addition.

- **[Measured 2026-09-01, nightly] A long-only book whose only alternative is cash can exploit a
  calendar effect only if the complement window's return is at or below zero — which closes the
  whole `calendar` half of `seasonality-calendar` in one screen, on a structural argument rather
  than an empirical one.** The effects are large and highly significant on train: turn-of-month
  (before=1, after=3) runs **+36.9%/yr in-window against +12.6%/yr out, +9.63 bps/day at
  t = +4.38**; Mondays **-10.00 bps/day (t = -4.13)**; Nov-Apr **+6.18 bps/day (t = +3.58)**.
  None is reachable. A hold-in-window/cash-out book trades 24x annually (3.60%/yr of drag) and
  nets Sharpe **+0.32 to +0.63** against buy-and-hold's **+1.05**, because the complement window
  still earns +11% to +14%/yr and sitting it out forgoes more than the concentration gains; and
  `max_leverage = 1.0` means overweighting in-window is not available, so the constraint binds by
  construction, not by parameter choice. **Check the complement window's sign before proposing
  any timing overlay here.** This is the third instance of the standing shape — a mechanism can
  be real, large and significant, and still structurally unreachable on this universe (the
  others: 5-10 day reversal, and regional neutralisation).

- **[Measured 2026-09-01, nightly] `range-variance` is now nine screened mechanisms with one
  cause, including its first *asymmetric* one, and the family should be treated as unreachable on
  this universe rather than unexplored.** `research/SUMMARY.md` #61 supplied the one object there
  that is not a width measure — the lottery/`MAX` upper-tail sort — together with a two-number
  test that decides it either way. Precondition **passes**: `MAX(5)`'s top-decile month-to-month
  stay rate is **0.452** (source ~1/3, random 0.10). The identifying sign test **fails**: on train
  single stocks against the forward 21-day return, `MAX(5)` IC **+0.0167 (t = +1.46)** and
  `MIN(5)` IC **+0.0253 (t = +2.11)** — same sign, which is the source's own criterion for "this
  is volatility", and both *positive*, the opposite of the lottery prediction. `spearman(MAX5,
  21d vol) = +0.872`, and **within trailing-volatility terciles `MAX(5)` is a clean null,
  IC -0.0055 (t = -0.75)**. This also resolves #61's objection to the lab's earlier range-lottery
  reading: the note argued that dismissing a significant, correctly-signed range result as "just
  low-vol" used the very confound `MIN` exists to separate — with the separation run, the
  dismissal was right. **`program.md`'s cold-family allocation rule cannot be honestly satisfied
  here and needs a human**: spending a trial would mean knowingly building on the survivorship
  artifact every screen keeps finding, and permanently raising the DSR bar to satisfy a count.

- **[Measured 2026-09-01, nightly] Two more signals confirmed as reversal in costume, and the
  pattern now has a name.** `research/SUMMARY.md` #64 (52-week-high proximity as an *additional*
  signal rather than a replacement momentum score) has its construction objection genuinely
  disarmed — the bounded-ratio turnover blow-up that sank the lab's earlier refutation cannot bite
  inside a per-leg quota, since only the within-leg ordering is read — and it still fails, on its
  own sign: top-20 **-2.74%/yr (t = -1.56)**, bottom-20 **+4.98%/yr**, IC **-0.0248 (t = -1.75)**,
  with `spearman(wh52, reversal) = -0.436`. **A price level measured against a trailing extreme
  carries the wrong sign for its own story on this universe and turns out to be reversal wearing
  a label** — the second instance after close-location value (2026-08-30, IC -0.0208, rank
  correlation +0.384 with the trailing 63-day return). Screen any such proposal against reversal
  before writing a file. Two smaller results filed at the same time: #65's spline candidate is
  declined because the only leg with content has a **step at the top decile** (+10.59%/yr,
  t = +4.16, flat across deciles 1-9) and a top-quantile cut already is that step; and #62's
  standardized unexplained volume **passes** its pre-registered closure rule
  (`spearman(SUV, log ADV) = +0.110`, `spearman(SUV, |return|) = +0.060` — the first volume object
  here that is not a disguised level, so `liquidity-volume` does **not** close) while **failing**
  screen (iii), its IC growing with horizon (+0.0033 / +0.0101 / **+0.0140** at 5 / 21 / 63 days,
  t = +0.50 / +1.45 / **+2.10**), which is the slow-moving-risk-proxy signature. SUV survives as
  the most orthogonal candidate *union leg* ever measured here (|rho| 0.002-0.107 against all four
  existing legs), not as a sort.
  **[RETRACTED 2026-09-02 — the SUV half of this entry only. The recipe as stated is identically
  zero (an OLS with an intercept has residual sum zero on its own fitting sample; largest
  |sum of residuals| 1.6e-11 over 416 name-dates), so every number quoted for SUV above is the
  rounding error of the linear solve, and the |rho| 0.002-0.107 that made it look like the ideal
  fifth leg is what an object with no content scores against everything by construction. The
  two-window repair in `strategies/lib/union_legs.py` is a real object and is also a null on the
  tail statistic. See the entry near the end of this file. The `A_C` and ETF-lead-lag halves of
  this entry are unaffected.]**

- **[Measured 2026-09-02, nightly] `SUMMARY.md` #62's standardized unexplained volume, as this
  lab implemented it, is identically zero — and the property it was selected for is a
  consequence of that. Fifth instance of the repo's oldest failure mode, and the first caught
  on an object the lab had already written a conclusion about.** The 2026-09-01 screen's recipe
  is "log volume on a constant plus |positive| and |negative| returns as separate regressors
  over 21 days, residual sum standardized". **An OLS containing an intercept has residual sum
  exactly zero on its own fitting sample**, so one window for both the fit and the sum returns 0
  for every name on every date. Measured over 416 name-dates: largest |sum of residuals|
  **1.6e-11**, mean **2.4e-13** — the rounding error of the linear solve. An independent
  reimplementation of the stated recipe reproduces that screen's 21-day IC to four decimals
  (**+0.0102** against **+0.0101**), which is what two implementations of one degenerate formula
  do on the same data. **This retracts the reading that SUV is "the most orthogonal signal ever
  measured against these legs" (|rho| 0.002-0.107): an object with no content is orthogonal to
  everything by construction, so that number was a symptom, not a finding.** The literature's
  construction needs two *disjoint* windows (estimation t-63..t-11, event t-10..t, standardized
  by the estimation residual SD); it is implemented in `strategies/lib/union_legs.py` and is
  well-behaved (median -0.025, quartiles ±1.42, 99.96% inside ±10 once a units floor on the
  estimation residual SD guards a degenerate fit). The repaired object is **also a null** on the
  statistic a book is scored on — top-20 excess +0.09%/yr (t = +0.08), top-10-of-pool
  **-0.77%/yr (t = -0.51)** — so `SUMMARY.md` #62's sort is declined either way, but for the
  right reason now. **The general habit, at its fifth instance and now with a cheap test
  attached: when a screen reports a suspiciously clean orthogonality, print the object's own
  dispersion before believing it.** Prior instances: the `dropna` trim cohort (four trials), the
  forward-fill weight-drift claim (two trials), the `MonthEnd`/`MonthBegin` alignment,
  `eta(q)`'s estimability.

- **[Measured 2026-09-02, nightly] The union book's second slot is indistinguishable from a coin
  flip on both splits, and the standing "legs earn their place by independence" claim does not
  survive its own placebo.** Three two-leg fixed-quota union books, each `seasonal` plus one
  partner, with breadth, churn, warmup, joint pool and machinery matched holdings-only in
  advance (20.1-21.0 names, 13.0-13.4x train turnover, same 350 months):

      arm  partner    partner's own tail        vol/pool   d vs #72    SE      t     train   val
      A    reversal   +2.31%/yr (t=+1.29)         1.230     +0.004   0.1373  +0.03   0.806  0.786
      B    suv        +0.09%/yr (t=+0.08)         1.140     +0.131   0.1360  +0.96   0.810  0.913
      C    placebo    zero by construction        1.005     +0.017   0.1139  +0.15   0.834  0.799

  Arm C's partner is a hash of the rebalance date and the ticker: it reads **no market data at
  all**. **Not one of the three is distinguishable from the single-leg baseline (#72, 0.782), the
  entire spread across all three partners (0.127) sits inside one paired SE (~0.13), and on the
  9.1x longer train split the three span 0.028 — with the coin flip winning it.** The two splits
  also disagree on the ordering (train C > B > A, validation B > C > A), which is this file's ⚠
  standing concern arriving inside one designed family rather than along a promotion ladder.
  **What this refutes and what it leaves standing.** The 2026-09-01 claim that "a leg earns its
  place in a union book by being independent, not by being individually significant" rests on
  #71-vs-#72 at t = +1.04. A placebo partner is maximally independent *and* maximally
  insignificant and buys +0.017, so **independence is not sufficient** and the claim as written
  fails its own control. The 1-leg → 4-leg gap itself (+0.175, t = +1.04) is untouched; what dies
  is the **per-leg linear reading** of it — the gain is not delivered by the first partner and
  must not be priced at +0.175/3, which is exactly the arithmetic the 2026-09-01 session used to
  decline the fifth leg as a "~0.03 effect". If the gap is real it is a **threshold in leg count**,
  not an increment, and it has never been measured at three legs.
  **Two accounts were killed by free diagnostics rather than by trials, in the order they were
  proposed.** *Style tilt in costume*: SUV's picks sit at 1.140x the pool's 21-day volatility
  (above it, not below), pool-average log dollar volume (-0.029), below-pool ETF share (0.127 vs
  0.149) — refuted. *Partner volatility*: it ordered arms A and B correctly and predicted arm C
  highest; C landed **below** B, refuting it one trial after it was proposed.
  **Method, and it is the transferable half: a placebo arm is the cheapest falsification this lab
  has and it had never been run.** It cost one trial and converted a surprising result into one
  draw inside a standard error. Given this file's record of mechanism accounts retracted a session
  or two after being built on, **run the placebo before building on a surprise, not after.**

- **[Measured 2026-09-02, nightly] The cost of a calendar overlay is set by how many times it
  crosses the window boundary, not by how wide the window is — which closes the `calendar` half of
  `seasonality-calendar` a second time, on cost, after its sign condition finally passed.**
  `research/SUMMARY.md` #67 argued the 2026-09-01 structural closure tested the wrong window: its
  complement pooled ordinary mid-month days with the T-8..T-4 window the payment-cycle mechanism
  says is *negative*. Measured on train, equal-weight universe, offsets relative to each month's
  last trading day: **T-8..T-4 runs -0.388 bps/day** (t = -0.22, -0.97%/yr if held always) against
  T-3..T+3 at +12.43 bps/day (t = +8.34) and all other days at +9.02. **So the closure's own
  binding condition — the sat-out window must earn at or below zero — is met, and the note's test
  passes.** The overlay is still unreachable, and the reason generalises. Excluding a 5-day window
  costs **23.8x** of annual turnover, *the same as holding only in-window*, because either way the
  book exits and re-enters once a month: turnover is a property of the **boundary crossings**, not
  of the window's width, and #67's "~12 round trips against 24" is wrong for that reason. Priced:
  gross Sharpe rises **1.050 → 1.216** (the mechanism is real and works gross), and net it falls to
  **0.966**, below buy-and-hold. Decomposed, sitting out T-8..T-4 avoids **+0.230%/yr** of loss
  against **-3.565%/yr** of transition cost, a 15x deficit. **General rule: a monthly calendar
  overlay on this universe must find a window losing more than ~3.6%/yr — about -30 bps/day over
  five days — and the most negative single offset measured here is -1.26 bps/day.** Two riders: the
  window is regime-dependent (US settlement went T+3 → T+2 in 2017 and T+1 in 2024, and the note
  itself warns the predicted day shifts with it), and every neighbouring specification tested
  (T-7..T-4, T-7..T-3, T-8..T-3, T-6..T-4) nets between 0.886 and 0.943, all below buy-and-hold.

- **[Measured 2026-09-02, nightly] The lab's seasonal leg is better identified than the lab
  thought, and the correction comes from running the source's own test rather than the one the lab
  chose.** `SUMMARY.md` #66 says the 2026-08-29 session over-read its Heston-Sadka failure: that
  screen wanted annual lags positive and non-annual *negative*, measured both positive, and
  concluded the identification was absent. Keloharju-Linnainmaa-Nyberg predict exactly that and use
  a different contrast — rank the same assets on same-calendar-month history versus
  other-calendar-month history and check that only the former carries information. Run on train,
  monthly, all 140 instruments: **same-calendar-month mean IC +0.0632 (t = +6.98)** against
  **other-month mean IC +0.0143 (t = +1.49)**; top-20 excess +6.90%/yr (t = +4.73) against
  +4.01%/yr (t = +2.23). **The discriminating test passes.** This matters beyond the seasonal leg,
  because the other-month mean is precisely the "this name has a high unconditional mean return"
  channel that survivorship bias inflates — so the family's strongest object is **not** explained by
  the artifact that closed `range-variance`. Note also that the lab's leg subtracts the other-month
  mean and the raw same-month mean scores slightly higher on both statistics (+0.0632 vs +0.0573,
  +6.90 vs +6.63%/yr); the difference is far inside the resolution floor and is **not** worth a
  trial, but the demeaning should stop being described as adding identification — the free control
  is what supplies it.

- **[Measured 2026-09-02, nightly] `SUMMARY.md` #69's ETF-only seasonal leg — the folder's
  top-ranked source of an orthogonal leg — is dead on this universe, and its own pre-registered
  precondition is what kills it.** The note asks for an annual-lag count first. Measured: ETFs have
  median 16.3 years of history and **only 5 of 42 reach 20 years**; requiring the leg's own 5
  same-month observations leaves **149 of 612 train month-ends** with 20+ ETFs scoreable, the first
  in **2005-08**. And the content is absent where it is computable: ETF-only same-calendar-month
  mean gives **IC -0.0049 (t = -0.19)**, same-minus-other **-0.0005 (t = -0.02)**, top-8 excess
  +1.64%/yr (t = +0.74) — against +0.0632 (t = +6.98) for the same construction on the full
  cross-section. **The source's claim that seasonality strategies on well-diversified
  characteristic portfolios are about as profitable as single-stock ones does not replicate here.**
  Consequence worth carrying: this repo's seasonal effect is a **single-stock** effect, which
  removes the survivorship-relief argument that motivated the ETF version — though the
  other-month control above bounds that worry from the other side.

- **[Measured 2026-09-02, nightly] `range-variance` is declined a fourth session, and for the first
  time on the statistic its own defence rested on.** Three sessions closed the family on ICs and
  quintile spreads. That was open to a real objection the lab itself supplies: `learnings.md`
  (2026-08-30) records that a **null IC and a 0.70-Sharpe book coexist here**, because a 20-of-140
  book buys the tail rather than the quintile mean, so an IC screen cannot close a family whose
  candidate would be a tail book. The one object in the family that is not a cross-sectional level
  — and the level *is* the survivorship artifact — is within-name de-levelled range volatility
  (21-day Garman-Klass against the same name's own 252-day GK baseline), screened in 2026-08-31 as
  an IC null and declined. **Measured tonight on the tail instead: top-20 excess -0.97%/yr
  (t = -0.63) and bottom-20 -0.27%/yr (t = -0.20) — both ends dead, and the top end is the wrong
  sign for a book.** The de-levelling is also only partial: `spearman(DLRV, raw GK level) = +0.563`
  and `spearman(DLRV, 21d reversal) = +0.235`, so more than half of it is still the level artifact
  plus some reversal. **Ten screened mechanisms across five sessions, one identified cause, and the
  last escape hatch closed on its own terms.** The standing recommendation to the human is
  unchanged and now better evidenced: this family is **unreachable on this universe rather than
  unexplored**, and `program.md`'s cold-family allocation rule cannot be honestly satisfied here —
  spending the trial would mean knowingly building on the survivorship artifact and permanently
  raising the DSR bar to satisfy a count.

- **[2026-09-02, nightly] The train-Sharpe-as-prediction sample breaks its streak.** Six
  consecutive non-`price-trend` scouts had under-predicted validation. Tonight's three:
  #73 train 0.806 → val **0.786** (over), #74 0.810 → **0.913** (under), #75 0.834 → **0.799**
  (over). Two of three over-predict, so the level story the last session offered as the competing
  explanation (these books all hold ~20 of ~140 names on a train split with a smaller universe and
  longer survivorship conditioning) no longer accounts for the sample on its own. n = 20 outside
  `price-trend`; still unresolved, still free to keep recording.

- **[Measured 2026-09-03, nightly] `portfolio-learning` is inert to leg quality, on three
  independent controls, and should be closed.** The union leg-count ladder is now complete and
  has an intercept. On validation: **0.759** (four legs replaced by hashes, #77) / 0.782 (one
  leg, #72) / 0.833 (mean of the three 2-leg arms, #73-#75) / **0.889** (three legs, #76) /
  0.958 (four legs, #71) — monotone, R² 0.974, slope +0.0505 per leg, fitted intercept 0.7433
  against a zero-leg rung *pre-registered at 0.75*. The shape survives its hardest control and
  is not an extrapolation artifact. It is still empty, for three reasons that only appear
  together. **(i)** Against the hash book, the seasonal leg — the only leg here with significant
  train content (decile-10 +10.59%/yr, t = +4.16) — is worth **+0.023 (t = +0.13)**, and the
  four-leg headline object is worth **+0.199 (t = +1.11)**. *No rung is individually
  distinguishable from a book that reads no market data.* **(ii)** Train disagrees about the
  shape: 0.471 / 0.577 / 0.814 / 0.696 / 0.678, an inverted U **peaking at two legs**, on a
  split 9.1x longer. **(iii)** #79 swapped in a leg measured **+0.236 better standalone** with
  everything else bit-identical and churn matched in advance, and the book moved **−0.003
  (t = −0.03)**. With the 2026-09-02 placebo partner outscoring a content partner, that is four
  readings agreeing: **the union responds to the number of orderings it is handed, not to their
  content.** The planning corollary is what matters — *no improvement to a leg can reach a union
  book*, so there is no route from the scouting programme to a challenger through this
  construction. Cleanest single comparison: the upgraded leg **alone** scores 0.917 at **1.2x**
  turnover; wrapped in the union, 0.954 at **13.6x** — +0.038 (t = +0.24) bought with ~1.9%/yr
  of costs. Nine trials in this family; stop building union books.

- **[Measured 2026-09-03, nightly] The first leg improvement in this repo that came from a stated
  mechanism rather than from a screened table — and the mechanism is *measurement*, not a
  premium.** `SUMMARY.md` #71's peer-relative scoring benchmark (distinct from the regional
  *weight* neutralisation this file closed by a bracket: that is what the book is exposed to,
  this is what each name's score is measured against) was screened free on all four legs and
  then tested only where it had an argument. `ILLIQ` is |return| / dollar volume, a price-impact
  ratio whose **cross-region level is partly set by the venue** — tick size, lot size,
  settlement, listed float — so region-demeaning should beat sector-demeaning, because venue is
  a regional property and not an industrial one. It does: train IC **+0.0347 (t = +4.47)**
  region against **+0.0145 (t = +1.59)** sector, from an unconditional +0.0186 (t = +1.78).
  Trial #78 scored validation **0.917** against the seated family lead's 0.681 (+0.236,
  `rho` 0.8323, SE 0.2329, t = +1.01) at **1.2x annual turnover** — 0.18%/yr of drag, the
  cheapest book on the board by an order of magnitude — with churn matched holdings-only in
  advance (0.81x against 0.77x), so it provably did not measure the broker.
  **Four free controls, all passed, and they are the reason to believe it rather than the
  score.** Both tails move correctly (top-20 +4.25 → +5.55%/yr, bottom-20 −3.29 → −3.87). The
  same operator on the two **unit-free** legs does nothing or hurts (seasonal +6.73 → +5.03,
  reversal +2.70 → +2.89) — the discriminating prediction of a venue account, which a general
  "peer benchmarks are good" account does not make. It is not size in costume: region-relative
  `ILLIQ` rank-correlates **−0.912** with region-relative log ADV, yet that size sort's own
  top-20 is a null (+0.58%/yr, t = +0.41) — the 2026-08-29 shape again, two near-identical
  rankings disagreeing about which *end* pays, and further confirmation that a 20-of-140 book
  buys a tail rather than a quantile mean. And the account is **bounded**: it does not rescue
  log ADV, because it explains a ratio whose numerator and denominator scale differently by
  venue, not a level.
  **Transferable rule: before neutralising a score against anything, ask whether the thing being
  removed is a unit or a return.** Removing a unit is free measurement hygiene; removing a
  return is removing signal, and this repo has a bracket showing that loses.
  **Also, the standing "a cross-sectional screen over-predicts the book it motivates" rule ran
  backwards here** — the screen's +1.30%/yr of extra tail excess was worth +0.236 of Sharpe, not
  the ≤+0.06 the rule implied, and the trial was pre-registered at 0.72 on that rule. The rule
  was calibrated on a designed `price-trend` pair that changed the *ranking inside a tail*; this
  change moved which names are in the tail at all. Do not apply it to an operator that changes
  the score's scale rather than its ordering within the book.

- **[Measured 2026-09-03, nightly] `research/SUMMARY.md` #70's eigenvalue screen fails its own
  placebo, and the way it fails is the repo's oldest habit arriving on the folder's statistic
  rather than on the lab's.** Fourteen rank-based zero-investment managed portfolios built from
  the lab's own characteristics, PCA'd on the daily covariance. The note's statistic —
  spearman(eigenvalue, |PC mean|) — comes back **+0.776**, which reads as a clean pass. It is
  not one: `|PC mean| = |PC Sharpe| × PC vol`, PC vol spans 17.7% to 0.87%, and shuffling the
  observed Sharpes across PCs with vols held fixed gives a null **mean of +0.584** and
  **p(≥ obs) = 0.124**. The scale-free version is **+0.367**, under the n = 14 critical value.
  What survives is weaker and different: the seven PCs holding 90% of variance carry **0.842**
  of the squared Sharpe against a placebo mean of 0.502 (p = 0.014) — but that is the *bottom*
  seven being quiet, not the top being strong, since the two largest |SR| sit at PC4 and PC6
  (var shares 0.065 and 0.045) while PC1, at 38% of variance, ranks 10th of 14 on |SR|. So
  low-eigenvalue directions are safe to shrink and mean returns do **not** line up with the
  variance ordering; by the note's own decision rule that is a decline, and
  `statistical-learning` gets no trial from it. **Seventh instance of "check that the statistic
  naming a mechanism is invariant to the thing it is not supposed to measure", and the first
  caught on an external proposal before a trial was spent.** The generalisation worth keeping is
  the *method*: when a screen's statistic is a product of the quantity you care about and a
  quantity mechanically tied to the axis, permute the first and hold the second — it costs
  nothing and it is the difference between +0.776 and p = 0.124.

- **[Measured 2026-09-03, nightly] `SUMMARY.md` #72's distance method is declined with its pool
  precondition PASSING and its content precondition failing — which is the informative
  direction.** The note predicted the matching pool would be thin on ~145 names across 15
  regions. It is not: best-partner SSD runs at **0.134** of the median admissible partner's
  within region (0.255 sector, 0.098 universe-wide), and ETFs take 0.396 of best-partner slots
  against a 0.300 universe share — over-represented, not dominant. The mechanism is simply
  absent. Pair-spread z-scores against the forward 21-day return: top-20 excess **−0.6 / +1.0 /
  +0.7 %/yr** (t = −0.49 / +0.64 / +0.45) for region / sector / universe matching, IC
  t = +0.48 / +0.52 / +1.14, and **GGR's own >2-formation-SD divergence trigger** (11-14
  names/date) at −1.8 / −0.5 / +0.8 %/yr (t = −0.73 / −0.26 / +0.38). The sign control fails
  too — within region the **rich** side has the higher forward return. And it is partly the
  incumbent in costume: spearman(−z, 21-day reversal) **+0.307**, spearman(−z, 252-day
  momentum) **−0.304**. Partner stability is 0.420 month-over-month and **0.139**
  year-over-year against ~0.01 for a random draw, so the "partner" is largely refitted each
  year rather than an economic pairing. This is `statistical-arbitrage`'s first genuinely
  *conditional* object, which was the open half of the family's earlier unconditional-IC
  decline; the family is now declined on the test it asked for.

- **[2026-09-03, nightly] The train-Sharpe-as-prediction record, four more readings.** #76 train
  0.696 → val **0.889** (under), #77 0.471 → **0.759** (under), #78 0.917 → **0.917** (exact
  to three decimals, the best reading ever recorded here), #79 0.650 → **0.954** (under). n = 24 outside `price-trend`; three of
  four under-predict again, and the one exception is the only book in the set that is a plain
  single sort rather than a union. That is a hypothesis worth recording rather than a finding:
  the under-prediction may be a property of the union machinery's small early-sample pools
  rather than of the splits. Still free to keep recording.

- **[Measured 2026-09-04, nightly] The concentration axis is now bracketed in a second family,
  and `price-trend`'s constant does not merely fail to transfer — it transfers with the wrong
  sign. This is the strongest form the `CLAUDE.md` scope rule has yet taken.** Three trials on
  one night, each moving the seated `liquidity-volume` lead's concentration and nothing else,
  on validation (the only split on which they are comparable — see the sample caveat below):

      book                            breadth    HHI          validation   t vs seated
      hold-15/enter-10        (#80)     12.4   0.0809 (+103%)    0.874        -0.46
      hold-30/enter-20 rank-wt (#81)    25.2   0.0521 ( +31%)    0.868        -0.96
      hold-30/enter-20 equal (seated)   25.2   0.0398             0.917          —
      hold-45/enter-30        (#82)     36.9   0.0273 ( -31%)    0.942        +0.36

  Monotone in breadth across a 3x span, on both arms, through both channels — cutting names
  and re-weighting at bit-identical membership (#81 returned `avg_pos` 24.3 against the
  seated 24.29, so the isolation held exactly). In `price-trend` every one of those arrows
  points the other way: ordering-only re-weighting is worth **+0.100** (#54) and
  de-concentration is priced at **~0.05 Sharpe per 30% of HHI** (#53). Here re-weighting is
  worth **-0.049** at the same +31% of HHI and de-concentration *gains*.
  **The mechanism, pre-registered and surviving.** A momentum composite's score is a direct
  estimate of expected continuation, so tilting capital up its ranking buys forecast. This
  score's cardinal content is not a forecast: decomposing `log ILLIQ ~ log|r| - log(dv)` on
  train, the denominator alone is a **size ranking this family has measured as a null four
  times** (top-20 +1.94%/yr, t = +1.88) and the numerator alone is the **survivorship-inflated
  volatility level** (+8.53%/yr, t = +3.62) that is the single identified cause behind
  `range-variance`'s eleven closed mechanisms. So the region-relative `ILLIQ` score is
  monotone in tail excess (+4.31 / +5.63 / +7.09 / +9.90 %/yr at top-20 / 15 / 10 / 5) while
  **that extra mean does not survive the variance it costs to reach it.**
  **Read the shape, never the levels.** The four books correlate **0.959-0.992** on validation,
  so by `SE = 0.568*sqrt(1-rho)` no single gap here is resolvable (|t| 0.36-0.96) and the
  +0.025 new lead is a quarter of a standard error. What is established is the ordering across
  a 3x breadth span, not any gap in it. **The axis is closed: no fourth point, in either
  direction.**
  **The transferable consequence is about the other twenty-five books, not this one.**
  `hold-30/enter-20` was adopted by the first non-`price-trend` scout and copied unexamined
  ever since, and it was designed on the **full ~140-name cross-section**, where enter-20 buys
  a top-14% tail. The region operator shrinks its own pool to ~77, so the same band buys the
  top 26% — and the repair that "restores the design quantile" (#80) is the arm that **loses
  worst**. The band is not too narrow relative to the pool; it is too narrow full stop, in the
  one family where that has been tested. Any book here whose operator restricts its pool
  should have its band re-bracketed rather than inherited.

- **[Measured 2026-09-04, nightly] A band-width change silently changes the *train* sample in
  this repo, and every past and future band comparison has to report coverage.** A wider band
  raises the minimum scoreable pool a month must supply, and this universe's pool grows over
  its history, so the three bracket points above run on **546 / 381 / 227** of 666 train
  month-ends, first scoreable in **1972-07 / 1986-04 / 1999-02**. Validation is unaffected
  (72 of 72 for all three), which is why the bracket is quoted on validation alone. Two
  consequences worth carrying. #82's train Sharpe of 0.62 and train maxDD of -46.1% are
  measured on a 1999+ window that excludes most of what the other two books are charged for,
  so **the reading is inadmissible to the train-as-prediction record** (n stays at 26). And a
  band comparison scored on train anywhere in this repo's history is comparing samples, not
  constructions. Sixth instance of this repo's oldest habit — check what a component actually
  reads — and the first to land on a *sample* rather than on a statistic or a line of code.

- **[Measured 2026-09-04, nightly] The lab ran the first control designed to break one of its
  own passing results, and the result survived twice — once against the folder's proposed test
  and once against a sharper one the folder did not propose.** `SUMMARY.md` #76(b) predicted
  that region-demeaning should be nearly inert on a unit-free percent-cost proxy if the
  2026-09-03 venue-unit account of the family lead is right, and should help as much as it
  helped `ILLIQ` if the account is wrong. Measured on train (top-20 excess over the scoreable
  pool): `ILLIQ` **+3.67 -> +4.31 %/yr**, FHT **+1.77 -> +1.00 %/yr**. The operator helps the
  unit-set ratio and *hurts* the unit-free fraction. **The account passes its own falsification.**
  A second, sharper control the folder did not ask for splits the ratio itself. Demeaning only
  the **denominator** (`log dv`, the half whose units the account blames) reproduces **+0.52 of
  the +0.65** total gain; demeaning only the **numerator** (`log|r|`, a return) is worth
  **-0.43**, i.e. the wrong sign. That is this file's own 2026-09-03 rule — *before neutralising
  a score against anything, ask whether the thing being removed is a unit or a return* —
  measured directly on both halves of one object for the first time, rather than inferred from
  which legs the operator helped.
  **A competing account specific to this repo's code was proposed and refuted for free.**
  `load_prices` forward-fills closes across foreign holidays while `load_panels` does not
  forward-fill volume, so the first traded day after a holiday carries a multi-day return
  against a one-day volume — inflating `ILLIQ` in proportion to a name's local holiday density,
  which is a *regional* property that region-demeaning would also remove. Rebuilding `ILLIQ`
  on days where day `t` and day `t-1` both traded gives `spearman(standard, clean) = +0.999`
  and an identical region gain (+0.65 either way). The artifact is real in principle and
  absent in magnitude. **Recording it because a refuted alternative is what makes the surviving
  account worth something** — and because this is the pattern the 2026-09-02 placebo entry asks
  for: run the control before building further, not after.
  **The account is now bounded on three sides and has nothing left to be applied to.** It does
  not rescue log ADV (measured last session), it is inert on unit-free scores (measured
  tonight, twice), and `region` is already the finest venue label `data/universe.yaml` carries
  — 15 regions, each a single country bar the 9-ETF `GLOBAL` bucket — so #76(a)'s "demean
  against listing venue instead" is **not expressible here**. A (region x currency) partition
  is finer but leaves only 7 of 18 cells with 4+ members. The journal's own standing next-idea
  "ask what else carries a venue-set unit" therefore closes: `ILLIQ` is the only ratio in this
  repo whose numerator and denominator scale differently by venue.

- **[Measured 2026-09-04, nightly] Both of the research folder's new liquidity proposals died
  on their own pre-registered preconditions, and the more useful death is the one that took the
  folder's own threshold seriously.** *(a)* **`SUMMARY.md` #74, Corwin-Schultz high-low spread.**
  The note pre-registers the kill: if `spearman(CS_spread, trailing 21-day range volatility)`
  is at or above ~0.7, the variance cancellation failed on this universe and the object is the
  width level again. Measured over 453 train month-ends: **+0.788**. The obvious escape is that
  the failure is an FX artifact — `aux["high"]`/`aux["low"]` *are* USD-converted here, and a
  two-day range absorbs an overnight FX move the one-day terms cancel, mechanically inflating
  `gamma` on the 13 non-USD regions. It is not the escape: restricted to **USD-quoted names
  only**, where no FX enters `gamma` at all, the correlation is **+0.769**. The estimator's
  variance cancellation genuinely fails on this universe. `range-variance` closes on its own
  identified cause for the twelfth screened mechanism, and this time on the folder's top-ranked
  range object with the folder's own number. *(b)* **`SUMMARY.md` #75, FHT.** Its mandatory
  non-trading-day filter is confirmed necessary and prospectively: uncorrected, FHT
  rank-correlates **+0.421** with local holiday density and the filter changes the ranking
  materially (filtered-vs-unfiltered +0.722). Correctly filtered it passes every orthogonality
  precondition — vs 21-day range vol **+0.031**, vs log ADV **-0.234**, vs CS spread **+0.080**
  — with ample dispersion (p90/p10 6.69). It then fails on content: top-20 excess **+1.77%/yr
  (t = +1.62)**, IC **+0.0061 (t = +0.75)**. The decomposition says why, and it is the reason to
  record this rather than just the number: FHT's cross-sectional ranking follows the `Zeros`
  factor at **+0.912** and `sigma` at only **+0.170**, and `Zeros` alone is a clean null
  (+0.25%/yr, t = +0.25) over which **47.8% of name-dates are exact ties at zero**. On 140
  mega-caps a zero-return day is too rare to rank anything. **A proposal can pass every
  orthogonality screen and still be a null, because orthogonality bounds an object's breadth,
  not its sign** — the same distinction this file drew for the value-proxy holdings screen.

- **[2026-09-04, nightly] The blend is declined for the sixth consecutive session, and the new
  lead is the first leg to clear its solved break-even at *every* weight while still being
  half a Sharpe short of resolvability.** `lv_illiq_region_wide30`: `rho` 0.7146, `k` 0.787,
  own Sharpe 0.942 against break-evens of 0.823 / 0.847 / 0.874 / 0.903 at 10/20/30/40%. Blend
  deltas **+0.010 / +0.016 / +0.018 / +0.014** at **t = +0.42 / +0.34 / +0.24 / +0.14**; the
  leg would need its own Sharpe at **1.385-1.470** for a two-SE blend. At 0.93x annual turnover
  it is also the cheapest book ever recorded in this repo (0.14%/yr of drag). The gap between
  what the gate would accept and what is distinguishable from noise is unchanged at roughly a
  factor of 1.5 in required leg Sharpe. Nothing here has moved the standing recommendation.
