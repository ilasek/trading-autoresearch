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

- **The membership buffer's stated justification is dead on this base, what it
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
