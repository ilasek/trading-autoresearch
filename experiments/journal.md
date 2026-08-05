# Experiment Journal

Append-only. Newest entries last.

## 2026-08-02T19:15:57+00:00 — mom_12m_baseline — **PROMOTE**
- Candidate: `strategies/candidates/mom_12m_baseline.py` (family: cross-sectional momentum, trial #1)
- Hypothesis: Instruments with the highest 12-month return (skipping the most recent month) continue to outperform over the next month, net of 15 bps costs.
- Verdict: PROMOTE — bootstrap: no champion exists; gates passed
- Train: sharpe +0.95, ann_ret +16.9%, maxDD -50.7%, turnover 3.3x
- Validation: sharpe +0.86, ann_ret +18.2%, maxDD -29.9%, turnover 5.8x
- Holdout: sharpe +1.14, ann_ret +28.2%, maxDD -24.1%, turnover 5.5x
- Deflated Sharpe prob: 0.9312 (bar from 1 trials)
- Lesson: Vanilla 12-1 momentum on this universe is a strong bar (val Sharpe 0.86), but
  remember it's stock-heavy and survivorship-inflated; the -51% train maxDD (2008-09
  momentum crash) is the known weakness for challengers to attack.

## 2026-08-02T19:16:16+00:00 — gtaa_trend_etf — **GATE_FAIL**
- Candidate: `strategies/candidates/gtaa_trend_etf.py` (family: time-series momentum / trend following, trial #0)
- Hypothesis: Holding a diversified ETF sleeve only while each ETF trades above its 200-day moving average (parking de-risked sleeves in 7-10y Treasuries) beats cross-sectional stock momentum on risk-adjusted returns.
- Verdict: GATE_FAIL — avg positions 3.84 < 4.0
- Train: sharpe +0.38, ann_ret +2.0%, maxDD -18.8%, turnover 0.5x
- Validation: sharpe +0.35, ann_ret +2.5%, maxDD -15.2%, turnover 3.0x
- Lesson: Risk-off designs that consolidate everything into one safe asset violate the
  min-positions gate by construction. Spread the defensive sleeve (e.g. IEF+SHY+GLD)
  or keep partial risk exposure. Also: first version crashed on truncated history —
  always derive sleeve availability per-date, never from `dropna().index[0]`.

## 2026-08-02T19:16:48+00:00 — ew_global_etf — **REJECT**
- Candidate: `strategies/candidates/ew_global_etf.py` (family: volatility targeting / risk parity, trial #3)
- Hypothesis: A static equal-weight basket of global equity, bond, real-asset and EM ETFs achieves a better net Sharpe than cross-sectional momentum simply by avoiding momentum crashes and churn.
- Verdict: REJECT — validation sharpe 0.492 <= champion 0.865
- Train: sharpe +0.42, ann_ret +2.1%, maxDD -32.2%, turnover 0.0x
- Validation: sharpe +0.49, ann_ret +4.5%, maxDD -19.6%, turnover 0.0x
- Deflated Sharpe prob: 0.7417 (bar from 3 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Static diversification alone (val Sharpe 0.49) explains roughly half of the
  champion's 0.86 — the momentum overlay is doing real work. Useful floor: any
  candidate below ~0.5 validation Sharpe is not even beating "buy everything".

## 2026-08-02T19:23:01+00:00 — mom_invvol_target — **REJECT**
- Candidate: `strategies/candidates/mom_invvol_target.py` (family: cross-sectional momentum, trial #4)
- Hypothesis: Inverse-volatility basket weighting plus a portfolio-level volatility target (scaling down only) on top of 12-1 momentum reduces the champion's momentum-crash drawdown while keeping validation Sharpe at or above the champion's, net of 15 bps costs.
- Verdict: REJECT — validation sharpe 0.706 <= champion 0.865
- Train: sharpe +0.97, ann_ret +12.1%, maxDD -41.6%, turnover 3.7x
- Validation: sharpe +0.71, ann_ret +10.7%, maxDD -24.3%, turnover 6.1x
- Deflated Sharpe prob: 0.8739 (bar from 4 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Vol management cut train maxDD (-50.7% -> -41.6%) but cost too much upside
  (val Sharpe 0.86 -> 0.71, ann_ret 18.2% -> 10.7%): inverse-vol weighting tilts the
  basket away from the highest-momentum (often highest-vol) names precisely when
  they're compounding hardest, and the vol-target scale-down clips winning runs, not
  just crash periods. Refining the momentum crash weakness needs a smarter trigger
  (e.g. a drawdown or correlation-based signal) rather than blanket vol-scaling —
  or accept the crash risk as the cost of the return premium.

## 2026-08-02T19:23:42+00:00 — gtaa_trend_diversified — **REJECT**
- Candidate: `strategies/candidates/gtaa_trend_diversified.py` (family: time-series momentum / trend following, trial #5)
- Hypothesis: An equal-weight multi-asset-class ETF sleeve that de-risks each asset individually below its 200-day moving average, parking de-risked capital across a diversified bond basket instead of one instrument, beats cross-sectional stock momentum on risk-adjusted terms while satisfying the diversification gate.
- Verdict: REJECT — validation sharpe 0.505 <= champion 0.865
- Train: sharpe +0.51, ann_ret +2.1%, maxDD -15.6%, turnover 0.7x
- Validation: sharpe +0.51, ann_ret +3.5%, maxDD -16.0%, turnover 3.8x
- Deflated Sharpe prob: 0.7426 (bar from 5 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Spreading the defensive sleeve across 4 bonds fixed the gate failure (avg_pos
  8.7 in validation, was 3.84) but the underlying idea is still weak: 0.51 Sharpe is
  right at the "barely beats buy-everything" floor seen with `ew_global_etf` (0.49).
  Per-asset 200dma trend filtering on this 8-asset sleeve mostly just de-risks bond/gold
  legs that were already low-vol, while adding whipsaw turnover (3.8x) for little
  return. ETF-level absolute-momentum/trend filters need a stronger asset set or a
  slower/confirming signal to earn their turnover cost here — plain 200dma alone is
  now a refuted knob for this family, not just the single-defensive-asset bug.

## 2026-08-02T19:24:35+00:00 — lowvol_equity_tilt — **REJECT**
- Candidate: `strategies/candidates/lowvol_equity_tilt.py` (family: low-volatility / quality tilts, trial #6)
- Hypothesis: Stocks with the lowest trailing 126-day realized volatility outperform the champion's high-momentum basket on a risk-adjusted (Sharpe) basis, net of 15 bps costs, because low-vol names carry less drawdown risk per unit of turnover.
- Verdict: REJECT — validation sharpe 0.685 <= champion 0.865
- Train: sharpe +0.83, ann_ret +9.5%, maxDD -42.5%, turnover 1.3x
- Validation: sharpe +0.69, ann_ret +8.7%, maxDD -29.5%, turnover 3.1x
- Deflated Sharpe prob: 0.8571 (bar from 6 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Low-vol stocks still drew a -42.5% train maxDD (barely better than the
  champion's -50.7%) and clearly lower validation Sharpe (0.69 vs 0.86) — on this
  survivorship-biased large-cap universe the "safety" of low realized vol didn't
  translate into a better risk-adjusted return, likely because low-vol names are
  concentrated in a handful of sectors (staples/utilities/telecom) rather than truly
  diversified, and because survivorship bias already strips out the low-vol names
  that failed (delisted/acquired). Plain low-vol stock selection is now a refuted
  standalone signal here; if revisited, it should be combined with a return/quality
  filter rather than used alone.

## 2026-08-02T19:25:26+00:00 — mom_regime_filtered — **REJECT**
- Candidate: `strategies/candidates/mom_regime_filtered.py` (family: regime switching, trial #7)
- Hypothesis: Switching fully out of 12-1 cross-sectional momentum into a diversified bond sleeve whenever SPY is below its 200-day moving average reduces the champion's momentum-crash drawdown while keeping validation Sharpe at or above the champion's, net of costs.
- Verdict: REJECT — validation sharpe 0.511 <= champion 0.865
- Train: sharpe +0.84, ann_ret +9.7%, maxDD -24.3%, turnover 2.3x
- Validation: sharpe +0.51, ann_ret +7.7%, maxDD -30.1%, turnover 8.6x
- Deflated Sharpe prob: 0.7492 (bar from 7 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: The regime filter did what it promised in-sample (train maxDD -50.7% ->
  -24.3%, the 2008-09 crash largely avoided) but failed out-of-sample: validation
  maxDD (-30.1%) was actually *worse* than the champion's (-29.9%), and turnover
  nearly doubled (8.6x vs 5.8x) from whipsawing in/out around the 200dma during
  choppy 2018-2023 markets (2018 Q4, 2020 COVID V-shape, 2022). A binary SPY-trend
  switch trades train-period crash protection for validation-period whipsaw cost —
  third rejected attempt at fixing the momentum-crash weakness (after inverse-vol
  scaling and ETF-level trend); the pattern across all three is that de-risking
  overlays reliably cut the *in-sample* 2008 drawdown but reliably lose more Sharpe
  than they save once applied out-of-sample. Future attempts should backtest the
  overlay's own turnover/whipsaw cost before combining with momentum, not just its
  crash-period behavior.

## 2026-08-02T19:26:18+00:00 — risk_parity_multi_asset — **REJECT**
- Candidate: `strategies/candidates/risk_parity_multi_asset.py` (family: volatility targeting / risk parity, trial #8)
- Hypothesis: Inverse-volatility weighting across a diversified asset-class ETF sleeve, scaled to a 10% annualized vol target, achieves a better net Sharpe than the champion by balancing risk contribution rather than capital across uncorrelated asset classes.
- Verdict: REJECT — validation sharpe 0.353 <= champion 0.865
- Train: sharpe +0.52, ann_ret +1.8%, maxDD -23.3%, turnover 0.3x
- Validation: sharpe +0.35, ann_ret +2.5%, maxDD -18.6%, turnover 1.1x
- Deflated Sharpe prob: 0.5875 (bar from 8 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Inverse-vol weighting (true risk parity) scored worse than the earlier
  static equal-weight basket (val Sharpe 0.35 vs 0.49) on essentially the same ETF
  set. Vol-weighting overweights the lowest-vol legs (short bonds, IG credit),
  under-allocating to the equity/EM/commodity sleeves that actually carry the return
  premium; the 10% vol target then scales the whole low-return blend down further.
  Confirms the `ew_global_etf` floor from a different angle: on this asset set,
  neither capital-weighting nor risk-weighting alone beats ~0.5 Sharpe — the gap to
  the champion is a real cross-sectional-momentum edge, not a diversification
  artifact. Vol targeting/risk parity as tested here (naive inverse-vol, no
  momentum/carry overlay) is now refuted for this universe; a future attempt should
  overlay a return signal rather than rely on risk-weighting alone.

## 2026-08-02T19:27:12+00:00 — mom_etf_blend — **REJECT**
- Candidate: `strategies/candidates/mom_etf_blend.py` (family: combinations, trial #9)
- Hypothesis: An 80/20 capital blend of 12-1 cross-sectional momentum with a static diversified ETF sleeve improves the champion's Sharpe and/or drawdown net of costs, because the low-turnover ETF sleeve is only weakly correlated with momentum's crash periods even though it has a much lower standalone Sharpe.
- Verdict: REJECT — validation sharpe 0.85 <= champion 0.865
- Train: sharpe +0.94, ann_ret +14.4%, maxDD -46.8%, turnover 2.6x
- Validation: sharpe +0.85, ann_ret +15.7%, maxDD -27.8%, turnover 4.7x
- Deflated Sharpe prob: 0.9124 (bar from 9 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Closest miss of the session — a near-tie with the champion on Sharpe (0.85 vs
  0.865) while also improving validation maxDD (-27.8% vs -29.9%) and train maxDD
  (-46.8% vs -50.7%). This is the first evidence in the repo that the ETF sleeve helps
  when *blended alongside* momentum rather than substituting for it or gating it on/off
  — consistent with the pattern from the three failed de-risking attempts (they all
  hurt more than they helped) and the two failed standalone-sleeve attempts (too weak
  alone to carry a portfolio). Deliberately NOT chasing this by sweeping the 80/20
  blend ratio this session (that's a knob, not an idea, and every trial raises the
  DSR bar for everyone). Worth one focused follow-up next session with a distinct
  rationale for the blend weight (e.g. inverse-vol-weighted blend of the two sleeves'
  own realized vols, not a fixed 80/20), not a parameter grid.


## Session summary — 2026-08-02 (nightly)

- Experiments run: 6 (mom_invvol_target, gtaa_trend_diversified, lowvol_equity_tilt,
  mom_regime_filtered, risk_parity_multi_asset, mom_etf_blend). Verdicts: 6 REJECT, 0
  PROMOTE, 0 GATE_FAIL. Champion unchanged: `mom_12m_baseline` (validation Sharpe 0.865).
- Best finding: `mom_etf_blend` (80% momentum / 20% static diversified ETF sleeve,
  always-on blend) — validation Sharpe 0.85 vs champion 0.865, with better train and
  validation max drawdown than the champion. Closest challenger yet; not promoted
  because it must strictly beat the champion, but the "blend, don't switch" mechanism
  is new evidence worth building on.
- Pattern across the session: every attempt to fix the champion's momentum-crash
  drawdown by *modifying or gating* the momentum sleeve (vol scaling, ETF trend
  filter, SPY-regime switch) reduced validation Sharpe more than it reduced drawdown.
  Every attempt at a *standalone* diversified ETF sleeve (equal-weight, risk parity)
  topped out around 0.35-0.71 Sharpe. Only an always-on capital *blend* of the two
  legs came close. Distilled into experiments/learnings.md.
- Ideas for next session:
  1. Follow up on `mom_etf_blend` with a principled (non-swept) blend-weighting
     rule — e.g. inverse-vol-weighted combination of the momentum and ETF sleeves'
     own trailing realized vols — rather than a fixed 80/20 split.
  2. Short-term mean reversion (family #4, untested this session) — watch the
     turnover gate (50x annual cap) closely given the champion's already-high 5.8x.
  3. A quality/return overlay on top of low-vol stock selection, since low-vol alone
     is now refuted standalone.
- No engine issues encountered; `pytest tests/` green (16 passed) before the session.
## 2026-08-04T01:13:11+00:00 — mom_etf_volweighted_blend — **REJECT**
- Candidate: `strategies/candidates/mom_etf_volweighted_blend.py` (family: combinations, trial #10)
- Hypothesis: Blending 12-1 cross-sectional momentum with a static diversified ETF sleeve, weighted inversely by each sleeve's own trailing 126-day realized volatility rather than a fixed 80/20 split, improves on the champion's validation Sharpe and/or drawdown net of costs, because it organically shifts capital toward the ETF sleeve exactly when momentum is turbulent.
- Verdict: REJECT — validation sharpe 0.757 <= champion 0.865
- Train: sharpe +0.64, ann_ret +5.3%, maxDD -39.0%, turnover 1.1x
- Validation: sharpe +0.76, ann_ret +9.1%, maxDD -21.9%, turnover 2.2x
- Deflated Sharpe prob: 0.8662 (bar from 10 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Inverse-vol sleeve weighting is a worse mechanism than the fixed 80/20 split
  (0.76 vs 0.85 validation Sharpe), not better — avg_positions jumped from 14.6 to
  24.7, meaning the scheme handed the ETF sleeve the majority of capital on average,
  not just during momentum turbulence. The flaw: a 15-stock momentum basket is
  structurally higher-vol than a 10-ETF diversified basket almost always, just from
  differences in diversification, so naive inverse-vol comparison between sleeves of
  different concentration systematically favors the more-diversified (lower-return)
  leg — the same failure mode already seen in `risk_parity_multi_asset` overweighting
  low-vol bond legs. This refutes vol-based *sleeve-level* reweighting as a family for
  this pairing; the fixed 80/20 (or a rule anchored to a target *momentum* weight with
  only a small vol-conditioned adjustment band) remains the better mechanism so far. A
  future blend attempt should keep momentum's weight close to fixed and only lean
  modestly toward the ETF sleeve, not let vol ratios set the split freely.

## 2026-08-04T01:14:36+00:00 — str_reversal_stocks — **GATE_FAIL**
- Candidate: `strategies/candidates/str_reversal_stocks.py` (family: short-term mean reversion, trial #0)
- Hypothesis: Stocks with the worst trailing 5-trading-day return outperform over the next week as the move mean-reverts, producing a better net Sharpe than the champion's 12-1 momentum, net of 15 bps costs, on a weekly-rebalanced long-only basket.
- Verdict: GATE_FAIL — annual turnover 83.94 > 50.0
- Train: sharpe +0.92, ann_ret +17.4%, maxDD -53.3%, turnover 51.5x
- Validation: sharpe +0.38, ann_ret +6.4%, maxDD -39.7%, turnover 83.9x
- Lesson: A fully-rebalanced bottom-N-by-1-week-return basket is turnover-toxic by
  construction — a 5-day reversal ranking reshuffles most of its members every week,
  so weekly full rebalance alone (before even weighing signal quality) blew the 50x
  gate 1.7x over. Also notable: validation Sharpe (0.38) was far below train (0.92),
  suggesting a fair amount of the train-period edge is a costs/turnover artifact that
  the gate is correctly protecting against, not a real anomaly at this frequency. GATE_FAIL
  doesn't cost a trial (n_trials stayed at #0), so a structurally different version —
  slower signal (~1-month lookback, matching the literature's dominant short-term
  reversal horizon) on the champion's monthly cadence — is worth one follow-up rather
  than abandoning the family, since that changes the mechanism (not just a knob) and
  should cut turnover by roughly the same 4x the rebalance frequency dropped.

## 2026-08-04T01:16:01+00:00 — str_reversal_monthly — **REJECT**
- Candidate: `strategies/candidates/str_reversal_monthly.py` (family: short-term mean reversion, trial #12)
- Hypothesis: Stocks with the worst trailing 1-month (21-trading-day) return outperform over the next month as the move mean-reverts, producing a better net Sharpe than the champion's 12-1 momentum, net of 15 bps costs, on a monthly-rebalanced long-only basket.
- Verdict: REJECT — validation sharpe 0.82 <= champion 0.865
- Train: sharpe +0.75, ann_ret +13.4%, maxDD -62.3%, turnover 11.5x
- Validation: sharpe +0.82, ann_ret +17.9%, maxDD -35.5%, turnover 19.4x
- Deflated Sharpe prob: 0.8895 (bar from 12 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Moving to monthly cadence fixed the turnover gate cleanly (83.9x -> 19.4x,
  well inside the 50x cap) and got closer to the champion than the weekly version
  (0.82 vs 0.38 validation Sharpe) — second-closest miss in the repo so far after
  `mom_etf_blend` (0.85). But it came with a materially worse drawdown profile than
  momentum on both splits (train maxDD -62.3% vs champion's -50.7%, validation -35.5%
  vs -29.9%): buying last month's biggest losers means concentrating in names that are
  falling for a real reason often enough (earnings misses, guidance cuts) that the
  "reversal" is really tail risk, not just overreaction, on a survivorship-biased
  large-cap universe. Short-term reversal on this universe is a real but second-tier
  signal — weaker and riskier than 12-1 momentum standalone. Given it's the second
  reasonably-close standalone family after momentum, it could be worth a future
  decorrelation check against momentum's own return stream (not a blend attempt this
  session — that's the next session's call) before writing off the family entirely.

## 2026-08-04T01:17:02+00:00 — mom_lowvol_doublesort — **REJECT**
- Candidate: `strategies/candidates/mom_lowvol_doublesort.py` (family: low-volatility / quality tilts, trial #13)
- Hypothesis: Among stocks in the top momentum quintile (12-1 return), those with the lowest trailing 126-day realized volatility produce a better net Sharpe than the champion's plain top-N momentum selection, because low-vol acts as a quality filter that avoids the most crash-prone high-momentum names.
- Verdict: REJECT — validation sharpe 0.642 <= champion 0.865
- Train: sharpe +0.91, ann_ret +15.8%, maxDD -50.4%, turnover 3.4x
- Validation: sharpe +0.64, ann_ret +10.9%, maxDD -28.4%, turnover 6.8x
- Deflated Sharpe prob: 0.7864 (bar from 13 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Filtering to lowest-vol names *within* the top-momentum quintile scored
  worse (0.64) than either the plain champion (0.86) or standalone low-vol selection
  (0.69) — refuting the learnings.md hypothesis that low-vol needed a return overlay
  to work here, at least via this mechanism. Drawdown barely moved either (train
  -50.4% vs champion's -50.7%). Likely explanation: within an already-high-momentum
  pool, the lowest-vol subset is picking the *weakest* momentum names that barely
  qualified for the quintile (steady, low-vol grinders) rather than the strongest
  compounders, so the double sort discards exactly the return magnitude that made
  the pool worth trading in the first place, while inheriting the pool's timing
  risk anyway. Low-vol is now refuted both standalone and as a within-momentum
  quality filter on this universe — treat the whole low-vol family as closed absent
  a genuinely new mechanism (e.g. sector-neutralized vol, not raw trailing vol).

## 2026-08-04T01:18:28+00:00 — mom_str_reversal_blend — **REJECT**
- Candidate: `strategies/candidates/mom_str_reversal_blend.py` (family: combinations, trial #14)
- Hypothesis: An 80/20 capital blend of 12-1 cross-sectional momentum with monthly (21-day) short-term reversal improves the champion's validation Sharpe and/or drawdown net of costs, because the two signals select on disjoint, structurally anti-correlated return horizons of the same stock universe.
- Verdict: REJECT — deflated sharpe prob 0.9043 < 0.95 (bar set by 14 total trials)
- Train: sharpe +0.94, ann_ret +16.3%, maxDD -50.5%, turnover 4.7x
- Validation: sharpe +0.87, ann_ret +17.8%, maxDD -30.7%, turnover 8.3x
- Deflated Sharpe prob: 0.9043 (bar from 14 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **First candidate in the repo's history to actually beat the champion's raw
  validation Sharpe** (0.87 vs 0.865), and it also improved train drawdown slightly
  (-50.5% vs -50.7%) — rejected only on the deflated-Sharpe multiple-testing bar
  (0.9043 < 0.95 required at 14 accumulated trials), not on the head-to-head
  comparison. This validates the session's mechanism reasoning: blending momentum
  with a *structurally* anti-correlated signal (opposite horizon, same universe)
  beats every prior blend attempt, including the previous-best `mom_etf_blend`
  (0.85) and the failed inverse-vol sleeve weighting (0.76 in this session). The
  catch is real, though, not a technicality: this is trial #14, and every rejected
  trial this session and last has raised the bar the next genuinely good idea must
  clear — a strategy this close needs either a materially larger raw edge or fewer
  accumulated trials to ever clear 0.95 DSR probability. This is the strongest lead
  yet for a future promotion; it should NOT be re-run with swept weights (e.g.
  70/30, 90/10) since that spends trials cheaply for a knob, but a *replication*
  attempt with a distinctly different construction of the same "opposite horizon"
  idea (e.g. composite z-score ranking instead of two separate baskets, which
  might reduce turnover from 8.3x and improve the Sharpe enough to clear the bar
  outright) would be a well-motivated next trial.

## 2026-08-04T01:19:34+00:00 — mom_str_reversal_composite — **REJECT**
- Candidate: `strategies/candidates/mom_str_reversal_composite.py` (family: combinations, trial #15)
- Hypothesis: Ranking stocks on a single composite z-score of 12-1 momentum (80% weight) and negative 1-month return (20% weight) and holding the top 15 achieves a better net validation Sharpe than both the champion and the two-basket `mom_str_reversal_blend`, because a single ranked list has lower name turnover than reconciling two separate baskets.
- Verdict: REJECT — deflated sharpe prob 0.9004 < 0.95 (bar set by 15 total trials)
- Train: sharpe +0.95, ann_ret +17.0%, maxDD -51.9%, turnover 5.0x
- Validation: sharpe +0.87, ann_ret +18.0%, maxDD -28.7%, turnover 9.0x
- Deflated Sharpe prob: 0.9004 (bar from 15 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: The turnover hypothesis was wrong: a single composite-ranked basket had
  *higher* validation turnover than the two-basket blend (9.0x vs 8.3x), not lower
  — ranking 15 names by a blended z-score every month reshuffles membership just as
  much as running two separate top-15 lists, because the composite score itself is
  more volatile month-to-month than either raw signal (z-scoring amplifies small
  cross-sectional differences near the selection boundary). Sharpe and drawdown both
  landed in the same range as `mom_str_reversal_blend` (0.87 val Sharpe, still short
  of the DSR bar which is now higher at 15 trials: 0.9004 vs 0.9043). Net effect:
  two independent constructions of "momentum + short-term reversal" both land at
  ~0.87 validation Sharpe, which is good evidence the ~0.87 edge is a real property
  of combining the two signals rather than a construction artifact — but also that
  neither construction is enough of a jump over the champion to clear a rising
  multiple-testing bar. Stopping this specific idea here rather than trying a third
  construction: two consistent, non-clearing results is enough signal without
  spending a third trial's worth of DSR bar on the same underlying edge.



## Session summary — 2026-08-04 (nightly)

- Housekeeping: session started with local `main` pointed at a stale ref (8 commits
  behind origin); fetched and fast-forwarded before starting — no lost work, just a
  stale local branch pointer. Engine tests green (16 passed) before the session; data
  store fresh through 2026-08-03 (cron working).
- Experiments run: 6 (mom_etf_volweighted_blend, str_reversal_stocks, str_reversal_monthly,
  mom_lowvol_doublesort, mom_str_reversal_blend, mom_str_reversal_composite). Verdicts:
  5 REJECT, 1 GATE_FAIL (str_reversal_stocks, turnover — free retry, didn't cost a trial).
  Champion unchanged: `mom_12m_baseline` (validation Sharpe 0.865). No promotion.
- Best finding: `mom_str_reversal_blend` and its composite-ranking variant
  `mom_str_reversal_composite` — both an 80/20 (or z-score-weighted) combination of
  12-1 momentum with monthly short-term reversal reached validation Sharpe ~0.87,
  **the first candidates in this repo's history to beat the champion's raw validation
  Sharpe**. Both were rejected only on the deflated-Sharpe multiple-testing bar
  (~0.90 vs 0.95 required), not on the head-to-head comparison — a genuine near-miss,
  not a refutation. Full reasoning distilled into `experiments/learnings.md`.
- Other patterns confirmed this session: inverse-vol/risk-weighting between sleeves of
  unequal diversification always favors the more-diversified leg (now confirmed twice);
  low-vol stock selection is refuted both standalone and as a within-momentum filter;
  short-term (1-month) reversal is a real but riskier second-tier standalone signal
  (val Sharpe 0.82, worse drawdown than momentum).
- Ideas for next session:
  1. One more, genuinely different construction of the momentum+reversal combination
     specifically aimed at cutting turnover (currently 8-9x vs champion's 5.8x) —
     e.g. a no-trade/hysteresis band on basket membership — since the raw edge is
     already established twice and turnover reduction could clear the DSR bar outright
     rather than needing dumb luck on trial count.
  2. Sector-neutralized (rather than raw trailing) volatility as a genuinely different
     mechanism, if the low-vol family is ever revisited — raw trailing vol is now
     closed on this universe.
  3. Family #3 (vol targeting/risk parity) and #6 (regime switching) are both now
     refuted in every form tried (naive and momentum-combined); no further standalone
     attempts recommended without a fundamentally new signal, not a reweighting scheme.
- No engine issues encountered this session.
## 2026-08-05T01:08:29+00:00 — mom_str_reversal_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_str_reversal_buffered.py` (family: combinations, trial #16)
- Hypothesis: Applying an asymmetric buffer band (hold while ranked in the top/bottom 25, enter only when ranked in the top/bottom 15) to each leg of the 80/20 momentum + monthly-reversal blend cuts turnover well below the ~8-9x seen in the unbuffered blend while keeping validation Sharpe within reach of the champion, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.9004 < 0.95 (bar set by 16 total trials)
- Train: sharpe +0.92, ann_ret +15.2%, maxDD -51.3%, turnover 2.9x
- Validation: sharpe +0.88, ann_ret +17.3%, maxDD -30.9%, turnover 6.5x
- Deflated Sharpe prob: 0.9004 (bar from 16 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: The buffer/hysteresis mechanism did exactly what it was designed to do —
  turnover fell from 8.3-9.0x (both prior unbuffered constructions) to 6.5x, much
  closer to the champion's 5.8x — and validation Sharpe ticked up to a new high for
  the family (0.88 vs 0.87 twice before). But the DSR probability barely moved
  (0.9004, same as trial #15) because it's now trial #16: the bar-raising effect of
  one more accumulated trial almost exactly offset the Sharpe gain. This is the
  clearest evidence yet that this specific momentum+reversal edge is structurally
  capped a hair below the 0.95 DSR bar as currently implemented — three independent
  constructions (two-basket blend, composite z-score, buffered blend) have now
  converged on validation Sharpe 0.87-0.88 while trial count climbs in lockstep.
  Any further refinement of *this* idea should be assumed to face the same
  offsetting effect unless it produces a materially larger jump (e.g. +0.03-0.05
  Sharpe in one step), not another incremental turnover/construction tweak. Treat
  this family as very likely closed for future sessions absent a fundamentally
  different signal to add to the blend, not another reweighting of the same two.

## 2026-08-05T01:09:48+00:00 — mom_12m_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_12m_buffered.py` (family: cross-sectional momentum, trial #17)
- Hypothesis: Replacing the champion's hard top-15 monthly cutoff with an asymmetric buffer band (hold while ranked in the top 25, enter only when ranked in the top 15) reduces annual turnover below the champion's 5.8x while keeping validation Sharpe at or above the champion's, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.9019 < 0.95 (bar set by 17 total trials)
- Train: sharpe +0.91, ann_ret +15.3%, maxDD -51.6%, turnover 1.9x
- Validation: sharpe +0.90, ann_ret +18.3%, maxDD -30.2%, turnover 4.4x
- Deflated Sharpe prob: 0.9019 (bar from 17 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Best challenger in the repo's history, by a clear margin.** Applying the
  buffer mechanism to the champion's own signal in isolation (no reversal leg, no
  blend) beat the champion outright on both axes at once: validation Sharpe 0.90 vs
  0.865 (a +0.035 raw edge, larger than any prior challenger's), *and* turnover 4.4x
  vs the champion's own 5.8x (lower, not just lower-than-other-challengers). This
  confirms the mechanism-isolation reasoning: the buffer wasn't just riding along
  with the reversal leg in `mom_str_reversal_buffered` — most of that trial's
  turnover reduction and Sharpe gain came from the buffer itself. Still REJECTed
  purely on the DSR bar (0.9019 < 0.95 at 17 trials), and the trial-count pattern
  from the previous entry repeats: DSR barely moved versus trial #16 (0.9004) despite
  a much bigger Sharpe jump, because one more accumulated trial ate most of the gain.
  Structural read for future sessions: this repo's DSR bar effectively requires a
  large single-step improvement to ever clear 0.95, not several trials of steady
  incremental gains — each trial's own bar-raising effect roughly cancels a modest
  improvement. This is the strongest lead ever recorded here; a future session
  combining this buffered-momentum leg with the already-validated ETF-sleeve blend
  (drawdown dampening) or another structurally distinct add-on is the natural next
  step, not another cutoff-threshold tweak on the buffer bands themselves (that
  would be a swept knob).

## 2026-08-05T01:11:04+00:00 — mom_buffered_etf_blend — **REJECT**
- Candidate: `strategies/candidates/mom_buffered_etf_blend.py` (family: combinations, trial #18)
- Hypothesis: An 80/20 capital blend of the buffered-momentum leg (top-15 core / top-25 hold band) with the static diversified ETF sleeve improves the champion's validation Sharpe and drawdown simultaneously, net of 15 bps costs, by combining the buffered leg's lower turnover and higher raw Sharpe with the ETF sleeve's drawdown-dampening effect.
- Verdict: REJECT — deflated sharpe prob 0.8905 < 0.95 (bar set by 18 total trials)
- Train: sharpe +0.90, ann_ret +13.1%, maxDD -47.9%, turnover 1.5x
- Validation: sharpe +0.88, ann_ret +15.7%, maxDD -28.1%, turnover 3.5x
- Deflated Sharpe prob: 0.8905 (bar from 18 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: Stacking the ETF blend on top of the buffered leg gave back most of the
  standalone buffered momentum's gain: validation Sharpe fell from 0.90
  (`mom_12m_buffered`) to 0.88, and DSR fell too (0.8905 vs 0.9019) because the
  Sharpe drop outweighed only a modest drawdown improvement (validation maxDD
  -28.1% vs buffered-alone's -30.2%, a smaller gain than the ~2pp improvement
  `mom_etf_blend` got over plain momentum). Same mechanism as the original
  `mom_etf_blend` finding (20% capital parked in a ~0.5 Sharpe sleeve costs raw
  Sharpe to buy a drawdown improvement), just applied to a stronger base leg — the
  dilution tax scales with what's being diluted, so blending doesn't get more
  attractive as the momentum leg improves; it's roughly a constant cost. Confirms
  `mom_12m_buffered` (trial #17, standalone, unblended) remains the best finding
  in the repo. Future attempts to build on it should leave the buffered leg
  unblended — every regime/switch/blend overlay tried on any momentum leg so far
  has independently failed for the same reason (whipsaw or diluted upside), so a
  capital-diluting addition should be treated as a high bar to clear, not a
  default next step.

## Session summary — 2026-08-05 (nightly)

- Housekeeping: local `main` ref was stale at session start (pointed at the
  bootstrap commit, 15 commits behind `origin/main`) — a `git fetch` + branch reset
  fixed it before starting; no lost work, `origin/main` on GitHub already had the
  full history. Engine tests green (16 passed) before the session; data store fresh
  through 2026-08-04 (cron working).
- Experiments run: 3 (mom_str_reversal_buffered, mom_12m_buffered,
  mom_buffered_etf_blend). Verdicts: 3 REJECT, 0 PROMOTE, 0 GATE_FAIL. Champion
  unchanged: `mom_12m_baseline` (validation Sharpe 0.865). Ran fewer than the 8-trial
  budget deliberately — the second trial's result was strong and specific enough
  (see below) that further variants would have been incremental knob-turning rather
  than new information, and every trial permanently raises the DSR bar.
- Best finding, and the best in the repo's history: `mom_12m_buffered` — replacing
  the champion's hard top-15 monthly cutoff with an asymmetric buffer/hysteresis
  band (hold while ranked in the top 25, enter only in the top 15) beat the champion
  outright on both Sharpe (0.90 vs 0.865) *and* turnover (4.4x vs 5.8x) at once —
  the first challenger to ever be strictly better on both axes simultaneously.
  REJECTed only on the DSR multiple-testing bar (0.9019 < 0.95 at trial #17), by the
  smallest margin of any rejected trial so far.
- Two same-night follow-ups both confirmed the buffered leg is best left unblended:
  adding the short-term-reversal leg back (`mom_str_reversal_buffered`, val Sharpe
  0.88) and blending in the diversified ETF sleeve (`mom_buffered_etf_blend`, val
  Sharpe 0.88) each diluted capital away from the buffered momentum leg for a
  smaller gain than it cost. This reframes last session's "momentum + reversal
  blend" near-miss (~0.87 val Sharpe) as likely having absorbed some of plain
  momentum's own turnover-inefficiency rather than reflecting a real
  diversification benefit — full reasoning in `experiments/learnings.md`, which now
  treats unblended buffered momentum (0.90 val Sharpe) as the bar for future ideas
  to clear, not the champion's 0.865.
- Structural pattern across trials #14-18: validation Sharpe climbed from 0.865 to
  as high as 0.90, but DSR probability barely moved (0.90-0.90) because each
  additional trial's own bar-raising effect roughly cancels a modest Sharpe gain.
  Distilled into learnings.md: clearing 0.95 DSR at this trial count needs one large
  single-step jump, not a string of incremental refinements.
- Ideas for next session:
  1. A genuinely different mechanism to add to buffered momentum that doesn't
     dilute capital away from it (e.g. a signal that only ever *adds* exposure
     rather than reallocating from the momentum leg) — every capital-diluting
     addition tried so far (reversal blend, ETF blend, vol scaling, regime switch)
     has cost more Sharpe than it bought, on any base leg.
  2. If revisiting regime/trend switching (now refuted 3x for plain momentum),
     note the buffer mechanism validated tonight targets whipsaw specifically, but
     learnings.md's read is that diluted upside during choppy-but-ultimately-up
     markets — not just whipsaw turnover — was the dominant failure mode, so
     hysteresis alone may not be a strong enough "specific reason" to retry it;
     weigh carefully before spending a trial there.
  3. Family #3 (vol targeting/risk parity) and #6 (regime switching) remain fully
     refuted; sector-neutralized vol (family #5 follow-up) is not currently
     testable — `data/universe.yaml` has no sector/industry field.
- No engine issues encountered this session.

