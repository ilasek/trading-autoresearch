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

## 2026-08-06T01:09:43+00:00 — mom_rankweighted_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_rankweighted_buffered.py` (family: cross-sectional momentum, trial #19)
- Hypothesis: Within the buffered 12-1 momentum basket (hold top 25, enter top 15), weighting held names linearly by momentum rank (more capital to the strongest-ranked names, less to the weakest-ranked) improves validation Sharpe over equal weighting, net of 15 bps costs, because it concentrates capital in the pool's strongest compounders instead of diluting it equally across the full hold band.
- Verdict: REJECT — deflated sharpe prob 0.9083 < 0.95 (bar set by 19 total trials)
- Train: sharpe +0.96, ann_ret +17.8%, maxDD -53.3%, turnover 3.4x
- Validation: sharpe +0.93, ann_ret +21.1%, maxDD -31.6%, turnover 6.0x
- Deflated Sharpe prob: 0.9083 (bar from 19 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **New best-yet result in the repo, and confirms the opposite-direction
  hypothesis cleanly.** Simply rank-weighting the same buffered basket
  (identical universe, lookback, and hold band as `mom_12m_buffered`) instead
  of equal-weighting it lifted validation Sharpe from 0.90 to 0.93 — a +0.065
  edge over the champion, the largest raw gap of any challenger so far — by
  giving more capital to the strongest-ranked names and less to the marginal
  ones near the buffer's edge. This is the mirror image of the refuted
  low-vol/inverse-vol findings: those tilted capital *away* from the
  strongest (often highest-vol) momentum names and lost Sharpe; tilting
  *toward* them gains it. Cost: avg_positions rose 15.0 -> 18.1 and turnover
  6.0x vs 4.4x (rank changes shuffle weights every month even without
  membership churn), still REJECTed only on the DSR bar (0.9083 < 0.95 at
  trial #19) — but DSR moved more than in any prior trial (+0.0064 vs the
  typical near-zero net change), because this is the first challenger whose
  Sharpe jump was large enough to outpace one more trial's bar-raising
  effect, not just offset it. This is now the strategy to beat, and the
  clearest evidence yet that weighting-scheme changes (not just
  membership/buffer changes) are a fruitful, still-open lever on the
  momentum leg. A natural, still-isolated follow-up: a milder or steeper
  rank-weight tilt (e.g. quadratic instead of linear) is a swept knob and
  should be avoided; a genuinely different rank-weighting *basis* (e.g.
  weighting by cross-sectional z-score magnitude instead of ordinal rank,
  which would preserve the info that a runaway winner's momentum lead is
  much larger than a marginal one's) is a distinct enough mechanism to be
  worth one focused trial.

## 2026-08-06T01:10:53+00:00 — mom_zscore_weighted_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_weighted_buffered.py` (family: cross-sectional momentum, trial #20)
- Hypothesis: Within the buffered 12-1 momentum basket (hold top 25, enter top 15), weighting held names by cross-sectional momentum z-score magnitude (rather than ordinal rank) improves validation Sharpe over rank-weighting, net of 15 bps costs, because it gives proportionally more capital to names with an unusually large momentum lead instead of treating all rank gaps as equal.
- Verdict: REJECT — deflated sharpe prob 0.9252 < 0.95 (bar set by 20 total trials)
- Train: sharpe +0.95, ann_ret +19.8%, maxDD -54.9%, turnover 3.6x
- Validation: sharpe +0.98, ann_ret +25.4%, maxDD -32.4%, turnover 6.1x
- Deflated Sharpe prob: 0.9252 (bar from 20 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **New best-yet result again, and DSR moved more than any prior
  trial.** Swapping the weighting basis from ordinal rank to z-score
  magnitude (same buffer band, lookback, universe as
  `mom_rankweighted_buffered`) lifted validation Sharpe again, 0.93 -> 0.98
  (+0.115 over the champion, by far the largest raw gap recorded here), and
  DSR probability rose 0.9083 -> 0.9252 (+0.0169) despite one more
  bar-raising trial — the clearest confirmation yet that magnitude, not just
  order, carries real information: a name with an outsized momentum lead
  over its neighbors deserves outsized capital, not just the next rank
  slot's worth. Cost: validation maxDD widened to -32.4% (vs -30.2% for
  plain buffered, -29.9% champion) and turnover ticked up to 6.1x — expected
  trade-offs of concentrating capital into fewer high-conviction names.
  Extrapolating the last two trials' DSR deltas (+0.0064, then +0.0169) for
  smaller Sharpe jumps than achieved here suggests one more comparably
  well-motivated idea could plausibly cross 0.95, but this is not
  guaranteed — the bar-raising effect could reassert itself as it did at
  trials #14-18. This weighting mechanism (z-score magnitude, not rank) is
  now the base to build on. The natural next lever, not yet touched by any
  weighting-scheme trial, is the *selection* signal itself: everything
  tonight still ranks/weights on raw single-horizon (12-1) momentum.

## 2026-08-06T01:12:19+00:00 — mom_multihorizon_zscore_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_multihorizon_zscore_buffered.py` (family: cross-sectional momentum, trial #21)
- Hypothesis: Ranking and weighting the buffered momentum basket (hold top 25, enter top 15) by a composite of 6-1 and 12-1 momentum z-scores, instead of 12-1 momentum alone, improves validation Sharpe over `mom_zscore_weighted_buffered`, net of 15 bps costs, because averaging two independent lookback horizons reduces horizon-specific noise in which names qualify for the basket.
- Verdict: REJECT — deflated sharpe prob 0.9333 < 0.95 (bar set by 21 total trials)
- Train: sharpe +0.94, ann_ret +19.5%, maxDD -54.5%, turnover 4.1x
- Validation: sharpe +1.03, ann_ret +27.3%, maxDD -36.0%, turnover 7.0x
- Deflated Sharpe prob: 0.9333 (bar from 21 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Third consecutive best-yet result tonight, but the marginal DSR
  gain per trial is now shrinking while risk keeps climbing — a sign this
  specific escalation is nearing its natural limit.** Adding the 6-1 horizon
  to the composite z-score lifted validation Sharpe again (0.98 -> 1.03,
  +0.165 over the champion) and DSR rose 0.9252 -> 0.9333, but the DSR delta
  (+0.0081) was smaller than the previous step's (+0.0169) despite a
  comparable Sharpe jump — the trial-count bar-raising effect is starting to
  bite harder again, consistent with the repo's established pattern
  (learnings.md) that clearing 0.95 needs one big jump, not compounding
  small ones. More concerning: validation maxDD widened again (-32.4% ->
  -36.0%, now closing in on the -45% gate) and turnover rose to 7.0x
  (champion: 5.8x) — each of the three weighting/signal refinements tonight
  has traded some downside risk for the Sharpe gain, and the pattern of
  rising drawdown alongside rising Sharpe suggests the z-score-magnitude
  weighting mechanism is working partly *because* it concentrates into a
  higher-vol, higher-beta tail of the momentum distribution, not purely
  through better name selection. Stopping the "increase conviction
  concentration further" line here rather than testing a fourth escalation
  (e.g. a triple-horizon composite) — that would be sweeping the same knob
  a third time with a visibly shrinking payoff and a visibly growing
  drawdown cost. `mom_multihorizon_zscore_buffered` (val Sharpe 1.03, DSR
  0.9333) is the new bar for future sessions to beat, but the more
  interesting open question for next time is whether *moderating* this
  mechanism's concentration (e.g. a soft cap or square-root dampening on
  the z-score spread, trading a little Sharpe for materially less
  drawdown/turnover) could net a *higher* DSR by reducing return variance
  rather than raising raw Sharpe further — a genuinely different lever
  (risk reduction, not conviction escalation) worth a focused trial.

## 2026-08-06T01:13:35+00:00 — mom_multihorizon_zscore_damped_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_multihorizon_zscore_damped_buffered.py` (family: cross-sectional momentum, trial #22)
- Hypothesis: Applying a square-root dampening transform to the within-basket weight spread of the two-horizon z-score-weighted buffered momentum basket (same selection and ranking as `mom_multihorizon_zscore_buffered`) achieves a higher deflated-Sharpe probability than the undamped version, net of 15 bps costs, because compressing (not eliminating) the tail of the weighting distribution reduces return variance and month-to-month turnover without discarding the magnitude-weighting benefit.
- Verdict: REJECT — deflated sharpe prob 0.9155 < 0.95 (bar set by 22 total trials)
- Train: sharpe +0.94, ann_ret +17.6%, maxDD -52.0%, turnover 3.3x
- Validation: sharpe +0.98, ann_ret +23.2%, maxDD -33.7%, turnover 6.5x
- Deflated Sharpe prob: 0.9155 (bar from 22 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Dampening hypothesis refuted — the raw z-score magnitude is real
  signal, not just a variance-inflating tail.** Square-root-compressing the
  weight spread (identical basket membership to
  `mom_multihorizon_zscore_buffered`) did reduce validation maxDD (-36.0% ->
  -33.7%) and turnover (7.0x -> 6.5x) as intended, but validation Sharpe
  fell more than proportionally (1.03 -> 0.98) and DSR probability actually
  *dropped* (0.9333 -> 0.9155) despite one fewer unit of Sharpe-to-bar
  tension — the risk reduction wasn't nearly enough to offset the return it
  gave up. This settles the question raised in the previous entry: the
  escalating Sharpe gains across tonight's three weighting refinements were
  not primarily a variance/leverage artifact of extreme concentration —
  giving the highest-momentum names proportionally more capital is closer
  to genuine incremental signal than to convexity-driven risk-taking, at
  least at the strengths tested here. `mom_multihorizon_zscore_buffered`
  (undamped, val Sharpe 1.03, DSR 0.9333, trial #21) remains the best
  finding of the night and the bar for future sessions. Do not pursue
  further dampening/moderation variants of this specific mechanism (that
  would be sweeping a knob whose direction is now refuted); a future
  session revisiting this family should either accept the undamped
  magnitude-weighting result as the new incumbent challenger, or bring a
  structurally different idea (not another intensity adjustment on the same
  z-score weighting) if it wants to clear the 0.95 DSR bar.

## Session summary — 2026-08-06 (nightly)

- Housekeeping: local `main` ref was stale at session start (detached HEAD
  pointed at the latest data-refresh commit, 1 commit ahead of where local
  `main` and even the cached `origin/main` ref showed) — a `git fetch` +
  `checkout -B main origin/main` confirmed origin was actually current and
  fixed the local branch pointer before starting; no lost work. Engine tests
  green (16 passed) before the session; data store fresh through 2026-08-05
  (cron working, 1 day behind today).
- Experiments run: 4 (mom_rankweighted_buffered, mom_zscore_weighted_buffered,
  mom_multihorizon_zscore_buffered, mom_multihorizon_zscore_damped_buffered).
  Verdicts: 4 REJECT, 0 PROMOTE, 0 GATE_FAIL. Champion unchanged:
  `mom_12m_baseline` (validation Sharpe 0.865). Ran half the 8-trial budget
  deliberately — three consecutive escalations of the same weighting-scheme
  lever produced diminishing DSR gains and rising drawdown/turnover, and a
  fourth trial (dampening) refuted the obvious next tweak; continuing to
  probe the same lever further would have been knob-sweeping.
- Best finding, and the best in the repo's history by a wide margin:
  `mom_multihorizon_zscore_buffered` — same buffered-momentum basket
  membership as `mom_12m_buffered`, but weighted by the magnitude of a
  composite 6-1/12-1 momentum z-score instead of equal-weighting. Validation
  Sharpe 1.03 vs champion 0.865 (+0.165, the largest gap ever recorded) and
  deflated-Sharpe probability 0.9333 (bar from 21 trials) — the closest any
  candidate has come to the 0.95 PROMOTE threshold. Still REJECTed only on
  the DSR bar, not on the head-to-head Sharpe comparison.
- Key new pattern this session (distilled into `experiments/learnings.md`):
  within-basket *weighting scheme* is as powerful a lever as basket
  membership/buffering was last session, and the direction that works is
  tilting *more* capital toward the strongest-momentum names (opposite of
  every refuted low-vol/inverse-vol attempt). But it's not a free escalation
  — validation maxDD widened from -30.2% to -36.0% across the three
  escalating trials, and a dampening attempt to trade Sharpe for lower
  variance made DSR worse, not better, confirming the magnitude-weighting
  edge is closer to real signal than to a concentration/variance artifact.
- Ideas for next session:
  1. The DSR bar is now within realistic reach (0.9333 at trial #21) —
     a structurally different idea layered on undamped magnitude-weighting
     (not another weighting-intensity tweak, which is now a partially-refuted
     direction) has a real shot at clearing 0.95 outright.
  2. Sanity-check `mom_multihorizon_zscore_buffered`'s validation maxDD
     (-36.0%, still comfortably inside the -45% gate but the closest any
     promising candidate has come to it) before building further on top of
     it — a future escalation that also improves or holds drawdown flat
     would be a stronger candidate than one that only chases Sharpe.
  3. Everything not yet touched by tonight's weighting-scheme work remains
     as summarized in prior sessions: vol targeting/risk parity, regime
     switching, and low-vol tilts are fully refuted; short-term reversal is a
     real but weaker/riskier standalone signal; capital-diluting blends have
     a roughly constant Sharpe tax regardless of the base leg's quality.
- No engine issues encountered this session.

## 2026-08-07T01:09:31+00:00 — mom_multihorizon_zscore_sectorneutral — **REJECT**
- Candidate: `strategies/candidates/mom_multihorizon_zscore_sectorneutral.py` (family: cross-sectional momentum, trial #23)
- Hypothesis: Neutralizing the composite 6-1/12-1 momentum z-score within coarse sector/asset-class groups before ranking and weighting the buffered momentum basket (hold top 25, enter top 15) reduces validation maxDD relative to the globally-ranked `mom_multihorizon_zscore_buffered` (val Sharpe 1.03, maxDD -36.0%), because it prevents a handful of correlated sectors from dominating basket exposure even when name-level diversification looks adequate, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.8664 < 0.95 (bar set by 23 total trials)
- Train: sharpe +0.93, ann_ret +15.9%, maxDD -52.9%, turnover 4.4x
- Validation: sharpe +0.87, ann_ret +17.8%, maxDD -32.3%, turnover 7.8x
- Deflated Sharpe prob: 0.8664 (bar from 23 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Sector-neutralizing the composite z-score is refuted as a risk-reduction lever — it traded away far more Sharpe than the drawdown it saved, and even raised turnover.** Validation maxDD improved only modestly (-36.0% -> -32.3%, well short of eliminating the concentration-driven drawdown growth seen across the weighting-intensity escalation) while Sharpe fell sharply (1.03 -> 0.87, back below the champion) and turnover *rose* (7.0x -> 7.8x) rather than falling — sector rotation at each rebalance apparently churns the basket more than global ranking does, since names now compete only within a shrinking or shifting sector-relative window rather than a stable global ordering. This suggests the drawdown growth in the escalating-weighting trials was not mainly a sector-concentration artifact — global top-momentum names already span multiple sectors more than expected, so forcing sector balance mostly discards genuine cross-sector signal (a stock beating its whole sector matters less than a stock with strong absolute momentum) rather than removing correlated risk. Do not pursue further sector/asset-class-neutral variants of this basket; the maxDD-widening question from last session's learnings should be pursued via a different lever (e.g. basket breadth) rather than sector construction.

## 2026-08-07T01:11:04+00:00 — mom_multihorizon_zscore_widebreadth — **REJECT**
- Candidate: `strategies/candidates/mom_multihorizon_zscore_widebreadth.py` (family: cross-sectional momentum, trial #24)
- Hypothesis: Widening the buffered momentum basket from hold-25/enter-15 to hold-35/enter-20 (same composite 6-1/12-1 z-score ranking and magnitude-weighting as `mom_multihorizon_zscore_buffered`) reduces validation maxDD and turnover versus the narrower basket, at some Sharpe cost, because diluting single-name concentration is a structurally different risk-reduction lever than the (already explored and refuted) options of dampening the weight spread or sector-neutralizing the score, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.9277 < 0.95 (bar set by 24 total trials)
- Train: sharpe +0.91, ann_ret +16.6%, maxDD -53.1%, turnover 3.1x
- Validation: sharpe +1.03, ann_ret +25.9%, maxDD -35.6%, turnover 6.5x
- Deflated Sharpe prob: 0.9277 (bar from 24 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Basket breadth is a nearly-free lever, not a Sharpe-for-risk tradeoff — it didn't reduce maxDD materially, but it matched Sharpe at lower turnover.** Widening hold/enter from 25/15 to 35/20 landed at essentially the same validation Sharpe (1.03 vs 1.03) and almost the same maxDD (-35.6% vs -36.0%, a rounding-level change) as the narrow basket, contrary to the hypothesis that more names would meaningfully dilute concentration risk — so name-count concentration is not the drawdown driver either (confirming this trial's sector-neutral sibling's finding that the risk isn't coming from insufficient diversification breadth or sector balance). The one genuine improvement was turnover (7.0x -> 6.5x), consistent with wider bands reducing membership churn as expected. DSR came in slightly *below* the narrow version's 0.9333 (0.9277) purely because it's now trial #24 instead of #21 — at equal trial count this basket would likely have scored at least as well. Net: breadth widening is a safe, mildly turnover-reducing substitute for the narrow basket with no Sharpe cost, but not a path to clearing the DSR bar on its own since it doesn't touch the actual drawdown driver. Two consecutive trials tonight (sector-neutral, now breadth) have each targeted "reduce concentration risk" and both found the maxDD growth across the earlier weighting-intensity escalation is *not* explained by insufficient diversification along either sector or name-count axes — it is more likely inherent to the magnitude-weighting mechanism itself (concentrating capital into whichever names have the most extreme z-scores, regardless of which names or sectors those are). Future sessions chasing this basket's drawdown should look at signal-level or time-varying levers (e.g. capping the maximum z-score multiple rather than the position weight, or a turnover/whipsaw-safe way to trim only the worst historical drawdown periods) rather than more diversification-axis attempts, which this session has now closed on two fronts.


## Session summary — 2026-08-07 (nightly)

- Housekeeping: local `main` ref was again detached HEAD at session start
  (pointed at the correct latest commit, just not on a branch) — fixed with
  `git checkout -B main origin/main` before starting, no lost work. Engine
  tests green (16 passed). Data store fresh through 2026-08-05 (cron
  working, 2 trading days behind today, well within the 5-day tolerance).
- Experiments run: 2 (mom_multihorizon_zscore_sectorneutral,
  mom_multihorizon_zscore_widebreadth). Verdicts: 2 REJECT, 0 PROMOTE, 0
  GATE_FAIL. Champion unchanged: `mom_12m_baseline` (validation Sharpe
  0.865). Ran a quarter of the 8-trial budget deliberately: both trials
  targeted the specific open question left by last session (is the
  weighting-escalation basket's growing validation maxDD a diversification
  problem, fixable by spreading exposure across sectors or more names?) and
  both answered it cleanly in the negative in one night, closing that
  question on two independent axes. No third hypothesis available tonight
  had a rationale strong enough to avoid re-treading refuted ground (a
  z-score cap/winsorization is a moderation variant of the already-refuted
  dampening idea; a rebalance-frequency change had no clear mechanism tied
  to the actual drawdown driver) — stopped rather than force a weaker trial.
- Best finding remains unchanged from last session:
  `mom_multihorizon_zscore_buffered` (val Sharpe 1.03, DSR 0.9333 at trial
  #21, unpromoted) is still the strongest challenger in the repo. Neither of
  tonight's attempts to reduce its validation maxDD (-36.0%) beat it:
  sector-neutralizing the composite score cost far more Sharpe (1.03 ->
  0.87) than the drawdown it saved (-36.0% -> -32.3%) and even raised
  turnover; widening the basket from 25/15 to 35/20 matched Sharpe (1.03)
  and cut turnover (7.0x -> 6.5x) but left maxDD essentially unchanged
  (-35.6%), landing at a lower DSR (0.9277) purely from the extra trial-
  count tax of running later in the session.
- Key new pattern this session (distilled into `experiments/learnings.md`):
  the growing validation maxDD across the weighting-intensity escalation is
  not a diversification-breadth or sector-concentration artifact — it
  survived both a sector-neutral score construction and a much wider basket
  unchanged. That points toward the magnitude-weighting mechanism itself
  (or the underlying momentum signal's tail behavior) as the actual driver,
  not "too few names/sectors held." Basket breadth (35/20) is a mild,
  Sharpe-free upgrade over the narrower basket (25/15) worth using as the
  base for any future trial on this line, since it holds Sharpe flat while
  cutting turnover.
- Ideas for next session:
  1. The DSR bar (now trial #24) keeps climbing while the best challenger's
     0.93-ish DSR score is now stale (measured at trial #21) — a future
     session should treat ~0.90-0.92 as the realistic bar for a similarly-
     sized Sharpe jump to clear 0.95, given the deflator's growth.
  2. Diversification-axis levers (sector, name-count breadth) are now
     closed for reducing this basket's maxDD. A genuinely different lever
     is needed: something that acts on the *signal* or *time* dimension
     rather than the *cross-sectional composition* dimension — e.g., a
     turnover-aware trim that only engages during identifiably extreme
     drawdown/correlation regimes (distinct from the already-refuted
     always-on de-risking overlays, which hurt in calm periods too), or
     revisiting the composite signal construction itself (e.g. a 3rd
     horizon was explicitly discouraged, but a completely different signal
     source combined via true diversification, not blending/dilution, has
     not been tried).
  3. Everything from prior sessions stands: vol targeting/risk parity,
     regime switching, low-vol tilts, and weight-spread dampening are fully
     refuted; short-term reversal is a real but weaker/riskier standalone
     signal; capital-diluting blends have a roughly constant Sharpe tax
     regardless of the base leg's quality; sector-neutral and basket-
     breadth widening are now refuted/neutral respectively for maxDD
     reduction specifically (breadth remains fine as a turnover-reducing,
     Sharpe-neutral substitute).
- No engine issues encountered this session.
## 2026-08-08T01:07:27+00:00 — mom_zscore_volspike_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_volspike_trim.py` (family: cross-sectional momentum, trial #25)
- Hypothesis: Scaling total exposure down (to 0.6x) only when the momentum basket's own trailing 21-day realized volatility exceeds 1.6x its trailing 252-day realized volatility — leaving exposure at 1.0x otherwise — reduces validation maxDD versus the unscaled `mom_multihorizon_zscore_widebreadth` basket without materially hurting validation Sharpe, net of 15 bps costs, because it targets genuine crash-level vol spikes rather than the frequent trend reversals that made every prior external-trend overlay whipsaw.
- Verdict: REJECT — deflated sharpe prob 0.9174 < 0.95 (bar set by 25 total trials)
- Train: sharpe +0.94, ann_ret +16.8%, maxDD -50.7%, turnover 3.2x
- Validation: sharpe +1.01, ann_ret +24.8%, maxDD -35.6%, turnover 6.6x
- Deflated Sharpe prob: 0.9174 (bar from 25 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **First genuinely different (time-dimension, not composition) risk lever tried, and it didn't move maxDD at all — a diagnostic (not a backtest, just inspecting the weight-generation logic) showed why.** Across the entire 1962-2023 history the trigger (basket's own trailing 21d/252d realized-vol ratio > 1.6) only fired in 19 of 513 months, and only twice inside the whole 2018-2023 validation window: 2018-02 and 2020-03. Validation maxDD came out at -35.6%, identical to the unscaled `mom_multihorizon_zscore_widebreadth` base's -35.6% — the trim simply didn't engage during the drawdown that matters. The mechanism (a basket-own vol-spike trigger, distinct from every prior *external-trend* de-risking overlay) may still be sound, but monthly rebalance cadence makes it structurally too late: by month-end, most of a fast crash (like 2020-03) has already happened, plus the engine's 1-day execution lag. This isolates cadence, not trigger sensitivity, as the likely culprit — worth one direct follow-up (daily re-evaluation of the same trigger, same threshold) before concluding the mechanism itself is refuted.

## 2026-08-08T01:09:12+00:00 — mom_zscore_daily_volspike_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_daily_volspike_trim.py` (family: cross-sectional momentum, trial #26)
- Hypothesis: The same basket-own-vol-spike exposure trim as `mom_zscore_volspike_trim` (21d/252d realized-vol ratio > 1.6 -> 0.6x exposure), re-evaluated daily instead of only at the monthly rebalance, reduces validation maxDD more effectively because it can react to a crash-level vol spike within days rather than waiting up to a month, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.9174 < 0.95 (bar set by 26 total trials)
- Train: sharpe +0.95, ann_ret +15.7%, maxDD -50.8%, turnover 2.1x
- Validation: sharpe +1.01, ann_ret +18.8%, maxDD -30.3%, turnover 2.7x
- Deflated Sharpe prob: 0.9174 (bar from 26 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Implementation bug invalidates this result — do not read anything into these numbers.** The candidate built sparse daily-scale rows directly from the held-names-only `norm` Series instead of zero-filling the full instrument universe first. Since the engine forward-fills sparse rows, any instrument that dropped out of the basket at a later rebalance kept its last nonzero weight forever (NaN in a row does not mean "zero" to a forward-fill) instead of being explicitly zeroed — validation avg_positions came out at 132.1 out of a 140-instrument universe, an unambiguous tell. Turnover (2.7x, "lower" than the base) and maxDD (-30.3%, "better") are both artifacts of this bug, not the daily-cadence mechanism, and should not be compared to prior trials. Caught via a post-hoc diagnostic (inspecting `generate_weights`' output directly, not a second backtest) before drawing any conclusion. Fixed in-place (explicit zero-fill on every emitted row, full-universe columns) and re-run as a fresh trial immediately after — see the next entry for the corrected result. Process lesson: any candidate using sparse/partial-column row construction (as opposed to always emitting a full zero-filled `pd.Series(0.0, index=prices.columns)` per row, the pattern every other candidate in this repo uses) should be visually diff-checked against that pattern before running, since the causality check does not catch this class of bug — it only detects lookahead, not stale forward-filled exposure.

## 2026-08-08T01:12:50+00:00 — mom_zscore_daily_volspike_trim_fixed — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_daily_volspike_trim_fixed.py` (family: cross-sectional momentum, trial #27)
- Hypothesis: The same basket-own-vol-spike exposure trim as `mom_zscore_volspike_trim` (21d/252d realized-vol ratio > 1.6 -> 0.6x exposure), re-evaluated daily instead of only at the monthly rebalance, reduces validation maxDD more effectively because it can react to a crash-level vol spike within days rather than waiting up to a month, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.9302 < 0.95 (bar set by 27 total trials)
- Train: sharpe +0.94, ann_ret +16.4%, maxDD -51.2%, turnover 3.4x
- Validation: sharpe +1.05, ann_ret +24.9%, maxDD -29.5%, turnover 7.0x
- Deflated Sharpe prob: 0.9302 (bar from 27 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **New best-ever result, and the first challenger ever to improve validation Sharpe *and* maxDD at the same time.** Cadence was indeed the problem, not the trigger: re-evaluating the identical basket-own vol-spike trim daily instead of monthly lifted validation Sharpe to 1.05 (previous best: 1.03) while cutting maxDD to -29.5% — better than the unscaled widebreadth base's -35.6% *and* better than the champion's own -29.9%. This directly answers the open question from the last two sessions' learnings (whether the weighting-escalation basket's rising drawdown could be fixed via a time-dimension lever rather than a diversification one): yes, once the trigger reacts fast enough. Turnover rose only modestly (6.5x -> 7.0x) from the occasional extra trim/untrim row, well inside the gate. DSR (0.9302) is still just under the 0.95 bar and, mechanically, slightly below trial #21's stale 0.9333 purely from six more trials' bar-raising — but this is a strictly better risk/return profile than every prior challenger, not just a Sharpe-chasing one. This is now the strategy to beat: `mom_zscore_daily_volspike_trim_fixed`. Natural next step: test whether the same fast-reacting trim generalizes to the narrower, higher-conviction 15/25 basket (`mom_multihorizon_zscore_buffered`, val Sharpe 1.03 alone) rather than only the widebreadth 20/35 one used here.

## 2026-08-08T01:14:48+00:00 — mom_zscore_narrow_daily_volspike_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_narrow_daily_volspike_trim.py` (family: cross-sectional momentum, trial #28)
- Hypothesis: Applying the same daily-reacting basket-own vol-spike exposure trim (21d/252d realized-vol ratio > 1.6 -> 0.6x exposure) to the narrower hold-25/enter-15 buffered z-score basket, instead of the hold-35/enter-20 widebreadth basket used in trial #27, improves validation Sharpe further (starting from a higher base of 1.03 vs 1.03) while still meaningfully reducing that basket's maxDD from -36.0%, net of 15 bps costs, because the trim and the concentration level are independent levers.
- Verdict: REJECT — deflated sharpe prob 0.9326 < 0.95 (bar set by 28 total trials)
- Train: sharpe +0.96, ann_ret +19.3%, maxDD -54.7%, turnover 4.4x
- Validation: sharpe +1.07, ann_ret +27.0%, maxDD -30.3%, turnover 7.3x
- Deflated Sharpe prob: 0.9326 (bar from 28 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Confirms the daily vol-spike trim and basket concentration are independent, additive levers — new best-ever result again.** Applying the identical trim mechanism (proven on the widebreadth basket in trial #27) to the narrower, higher-conviction 15/25 basket lifted validation Sharpe to 1.07 (vs 1.05 on widebreadth, 1.03 untrimmed) while maxDD came in at -30.3% — essentially matching widebreadth+trim's -29.5% and still far better than this basket's own untrimmed -36.0%. DSR (0.9326) edged out trial #27's 0.9302 despite one more trial, the clearest sign yet that this combination (concentration + fast-reacting own-vol trim) carries real incremental signal rather than being a bar-raising coincidence. `mom_zscore_narrow_daily_volspike_trim` is now the strongest challenger in the repo's history on every axis: Sharpe, maxDD, and DSR. Natural next question, tested in the very next trial: does the trimmed capital do better parked as cash (as here) or redirected into an explicit low-correlation hedge?

## 2026-08-08T01:16:47+00:00 — mom_zscore_volspike_hedge_redirect — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_volspike_hedge_redirect.py` (family: cross-sectional momentum, trial #29)
- Hypothesis: Redirecting the capital freed by the daily vol-spike trim (trials #27-28) into a fixed 50/50 TLT/GLD defensive sleeve, instead of leaving it as idle cash, improves validation Sharpe over the narrow-basket trimmed version (`mom_zscore_narrow_daily_volspike_trim`, val Sharpe 1.07) without materially worsening its maxDD, because bonds and gold have historically been positively-returning during the momentum basket's own vol-spike episodes, net of 15 bps costs.
- Verdict: REJECT — deflated sharpe prob 0.9323 < 0.95 (bar set by 29 total trials)
- Train: sharpe +0.96, ann_ret +19.5%, maxDD -54.3%, turnover 4.5x
- Validation: sharpe +1.07, ann_ret +27.3%, maxDD -30.7%, turnover 7.7x
- Deflated Sharpe prob: 0.9323 (bar from 29 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Refuted — parking trimmed capital in TLT/GLD is a wash at best, slightly negative in practice.** Validation Sharpe was unchanged (1.07 vs 1.07) and maxDD came out slightly *worse* (-30.7% vs -30.3% leaving it as cash), with turnover ticking up too (7.3x -> 7.7x) from the extra hedge-entry/exit rows. Bonds and gold were not reliably diversifying during exactly the vol-spike windows this trigger fires on (e.g. 2020-03, where a broad liquidity-driven selloff briefly hit most asset classes at once, including an initial leg down in long bonds) — cash is a cleaner, cost-free ballast than any specific hedge asset pair for this particular trigger. Do not pursue further hedge-asset variants (different bond/commodity mix, partial redirect fraction) of this same idea; the mechanism as tested is closed. `mom_zscore_narrow_daily_volspike_trim` (val Sharpe 1.07, maxDD -30.3%, DSR 0.9326 at trial #28) remains the best finding of the night and the strongest challenger in the repo's history.

## Session summary — 2026-08-08 (nightly)

- Housekeeping: local `main` ref was again detached HEAD at session start
  (pointed at the correct latest commit, just not on a branch) — fixed with
  `git checkout -B main origin/main` before starting, no lost work. Engine
  tests green (16 passed). Data store fresh through 2026-08-07 (cron
  working, 1 trading day behind today).
- Experiments run: 5 (mom_zscore_volspike_trim, mom_zscore_daily_volspike_trim
  [bug, corrected same session], mom_zscore_daily_volspike_trim_fixed,
  mom_zscore_narrow_daily_volspike_trim, mom_zscore_volspike_hedge_redirect).
  Verdicts: 5 REJECT, 0 PROMOTE, 0 GATE_FAIL. Champion unchanged:
  `mom_12m_baseline` (validation Sharpe 0.865). Ran about 5/8 of the budget:
  stopped once the productive line (daily-cadence vol-spike trim) had been
  established, generalized to both basket variants, and its one natural
  follow-up (hedge redirect) cleanly refuted — a further trial along the
  same mechanism would have been knob-sweeping (threshold/scale tuning).
- Process note: trial #26 had an implementation bug (sparse weight rows not
  zero-filled across the full instrument universe, so names dropped from the
  basket kept a stale forward-filled weight — avg_positions read 132/140, an
  unambiguous tell). Caught via a post-hoc diagnostic on the weight matrix
  itself (not a second backtest) before drawing any conclusion, documented
  honestly in that trial's journal entry, fixed, and re-run immediately as
  trial #27 under a new slug. The buggy trial's numbers were left in the
  journal/trials history as recorded (per the never-rewrite-history rule)
  with a clear note not to read anything into them.
- Best finding, and the strongest in the repo's history on every axis
  (Sharpe, drawdown, and DSR): `mom_zscore_narrow_daily_volspike_trim`
  (trial #28) — the narrower 15/25 buffered composite-z-score momentum
  basket (identical to `mom_multihorizon_zscore_buffered`) plus a
  basket-own realized-vol-spike exposure trim (21d/252d vol ratio > 1.6 ->
  0.6x exposure) re-evaluated on every trading day. Validation Sharpe 1.07
  (vs champion 0.865, vs the prior best unprotected basket's 1.03) *and*
  maxDD -30.3% (vs the same unprotected basket's -36.0%, and even better
  than the champion's own -29.9%) — the first challenger ever recorded here
  to improve Sharpe and drawdown at the same time. DSR 0.9326, still short
  of the 0.95 PROMOTE bar but the highest yet recorded, and rising slightly
  despite one more trial's bar-raising effect (unlike most incremental
  improvements in this repo's history).
- Key new pattern this session (distilled into `experiments/learnings.md`):
  the two-session-old open question — whether the weighting-escalation
  basket's rising validation maxDD could be fixed via a signal/time lever
  rather than a diversification one — is answered yes, but only once
  overlay cadence matches the speed of the thing it's trying to catch. The
  identical vol-spike trigger was a near no-op at monthly cadence (fired
  twice in 6 years of validation, no maxDD change) and decisive at daily
  cadence (new best Sharpe and maxDD both). This is a distinct failure mode
  from the earlier-refuted external-trend overlays (which failed from
  whipsaw, not lag) and worth checking for any future regime/overlay idea.
  Redirecting freed capital into a bond/gold hedge instead of cash was
  tested once and cleanly refuted.
- Ideas for next session:
  1. The DSR bar (0.9326 at trial #28, now stale at trial #29) is the
     closest the repo has ever come to 0.95 relative to how large the
     Sharpe/maxDD improvement is — but three consecutive sessions have shown
     the deflator absorbs most of a moderate single-trial gain. A
     structurally different idea layered on
     `mom_zscore_narrow_daily_volspike_trim` (not another trim-mechanism
     tweak — cadence and redirect are both now closed) has the best odds
     yet of clearing 0.95 outright.
  2. The hedge-redirect result suggests the daily-trim's edge is really
     about *timing* exposure reduction, not about what replaces it — a
     future idea should treat "when to de-risk" as solved for this basket
     and look elsewhere (e.g. does the same fast-reacting vol trigger help
     if applied to the champion's own plain 12-1 basket, isolating whether
     the benefit is specific to the magnitude-weighted composite basket or
     general to any concentrated momentum basket).
  3. Everything from prior sessions stands: vol targeting/risk parity,
     regime switching, low-vol tilts, weight-spread dampening, sector-
     neutral scoring, and (as of tonight) monthly-cadence de-risking
     overlays and hedge-asset redirection are all refuted/closed; basket
     breadth widening remains a free, Sharpe-neutral turnover reducer.
- No engine issues encountered this session.

## 2026-08-11T01:07:26+00:00 — mom_12m_daily_volspike_trim — **REJECT**
- Candidate: `strategies/candidates/mom_12m_daily_volspike_trim.py` (family: cross-sectional momentum, trial #30)
- Hypothesis: Applying the same daily-reacting basket-own vol-spike exposure trim (21d/252d realized-vol ratio > 1.6 -> 0.6x exposure) to the plain equal-weight buffered 12-1 basket (the champion's own signal, hold-25/enter-15) improves its validation Sharpe and reduces its maxDD versus the untrimmed champion, net of 15 bps costs, because the trim's benefit comes from reacting to the basket's own vol regime, not from the return-magnitude weighting scheme it was previously tested on.
- Verdict: REJECT — deflated sharpe prob 0.8568 < 0.95 (bar set by 30 total trials)
- Train: sharpe +0.92, ann_ret +15.0%, maxDD -51.6%, turnover 2.4x
- Validation: sharpe +0.90, ann_ret +18.2%, maxDD -30.2%, turnover 4.6x
- Deflated Sharpe prob: 0.8568 (bar from 30 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Refuted — on the plain equal-weight basket the trim is a near no-op, isolating the mechanism as specific to the magnitude-weighted basket, not general to any concentrated momentum basket.** Validation Sharpe (0.90 vs 0.90), maxDD (-30.2% vs -30.2%) and turnover (4.6x vs 4.4x) are all essentially identical to `mom_12m_buffered`'s untrimmed trial #17 numbers — the trim mechanism barely engaged. This makes sense in hindsight: the equal-weight basket's own realized vol is already lower and less spiky than the composite z-score-weighted basket's (which concentrates capital into the most extreme-momentum, typically higher-idiosyncratic-vol names), so the 21d/252d vol-ratio trigger rarely crosses 1.6 for this basket. This answers last session's open question #2 cleanly: the daily vol-spike trim's Sharpe/maxDD improvement is not a generic property of "any concentrated momentum basket + fast vol trim" — it specifically depends on the basket being concentrated/volatile enough (via magnitude-weighting) for the trigger to actually fire during stress. Future de-risking-overlay ideas should keep targeting the magnitude-weighted basket, not the plain equal-weight one; `mom_zscore_narrow_daily_volspike_trim` (val Sharpe 1.07, maxDD -30.3%, DSR 0.9326, trial #28) remains the strongest challenger in the repo.

## 2026-08-11T01:08:54+00:00 — mom_52wkhigh_zscore_buffered — **REJECT**
- Candidate: `strategies/candidates/mom_52wkhigh_zscore_buffered.py` (family: cross-sectional momentum, trial #31)
- Hypothesis: Ranking and magnitude-weighting the buffered basket (hold-25/enter-15) by a composite z-score of nearness-to-52-week-high (252d and 126d trailing windows) instead of trailing total return achieves validation Sharpe competitive with the return-based composite z-score basket (1.03), net of 15 bps costs, because 52-week-high proximity is a documented alternative momentum proxy distinct from return magnitude.
- Verdict: REJECT — validation sharpe 0.355 <= champion 0.865
- Train: sharpe +0.90, ann_ret +12.5%, maxDD -49.3%, turnover 7.4x
- Validation: sharpe +0.35, ann_ret +4.4%, maxDD -28.8%, turnover 14.6x
- Deflated Sharpe prob: 0.3734 (bar from 31 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Clearly refuted, and not close — 52-week-high proximity is a much noisier and more turnover-hungry signal than return magnitude on this universe.** Validation Sharpe fell to 0.35 (vs the return-based composite's 1.03, and below the champion's 0.865) while turnover more than doubled (7.0x -> 14.6x). The likely mechanism: nearness-to-high is a bounded, compressed signal (ratio in (0,1]) that clusters many names near 1.0 during broad bull stretches, so small day-to-day price wiggles flip the ranking of near-tied names in and out of the buffer band far more often than a z-scored *return magnitude*, which spreads names out on an unbounded scale and is naturally stickier. The George & Hwang (2004) effect this was based on is typically documented net of much lower transaction costs and/or with less aggressive rebalancing than this repo's monthly-buffered, magnitude-weighted construction — it does not survive being dropped into this specific high-turnover mechanism. This closes the "genuinely new signal source" direction for now, at least via a naive high-proximity composite; do not retry variants of this specific construction (different lookback windows, single- vs dual-horizon) without addressing the turnover root cause first (e.g. a much wider buffer band or an explicit noise floor on the ratio) — that would need a distinct rationale, not a parameter sweep. `mom_zscore_narrow_daily_volspike_trim` (val Sharpe 1.07, DSR 0.9326, trial #28) remains the strongest challenger in the repo.


## Session summary — 2026-08-11 (nightly)

- Housekeeping: local `main` was on-branch and up to date with `origin/main`
  at session start, no fixup needed. Engine tests green (16 passed). Data
  store fresh through 2026-08-10 (cron working, 1 trading day behind today).
- Experiments run: 2 (mom_12m_daily_volspike_trim, mom_52wkhigh_zscore_buffered).
  Verdicts: 2 REJECT, 0 PROMOTE, 0 GATE_FAIL. Champion unchanged:
  `mom_12m_baseline` (validation Sharpe 0.865). Ran a quarter of the 8-trial
  budget deliberately: both trials targeted specific open questions from
  last session's learnings (does the daily vol-spike trim generalize beyond
  the magnitude-weighted basket? is there a genuinely different price-based
  signal worth trying?) and both answered cleanly in the negative. No third
  hypothesis available tonight had a rationale strong enough to avoid
  re-treading already-refuted ground (blending reversal back into the
  buffered basket, further trim-threshold tuning, and portfolio-level regime
  filtering are all explicitly closed by prior sessions) — stopped rather
  than force a weaker trial, matching the 2026-08-07 session's precedent.
- Best finding remains unchanged: `mom_zscore_narrow_daily_volspike_trim`
  (trial #28, val Sharpe 1.07, maxDD -30.3%, DSR 0.9326) is still the
  strongest challenger in the repo's history, on every axis (Sharpe,
  drawdown, DSR) — unpromoted, short of the 0.95 DSR bar.
- Key new patterns this session (distilled into `experiments/learnings.md`):
  1. The daily vol-spike trim's Sharpe/maxDD improvement is specific to the
     magnitude-weighted basket, not general to any concentrated momentum
     basket — applying it to the plain equal-weight buffered basket was a
     near no-op because that basket's own realized vol rarely crosses the
     spike threshold.
  2. A genuinely different price-based signal (52-week-high proximity,
     replacing return-magnitude in the same composite/buffer/weighting
     mechanism) was tried and clearly refuted — validation Sharpe fell to
     0.35 with turnover more than doubling, because the bounded proximity
     ratio clusters many names near 1.0 and flips buffer-band membership on
     small price wiggles far more than an unbounded z-scored return does.
- Ideas for next session:
  1. The "genuinely different signal" direction is not fully closed — a
     future session could revisit 52-week-high proximity with an explicit
     fix for its turnover blow-up (e.g. a much wider buffer band or a noise
     floor on the ratio), but that needs its own clear rationale, not a
     reflexive parameter sweep.
  2. The DSR bar continues to climb (now trial #31) while the best
     challenger's 0.9326 score is stale (measured at trial #28) — a
     structurally different idea layered on
     `mom_zscore_narrow_daily_volspike_trim` (not another trim/threshold
     tweak, not another signal source in the same weighting mechanism) is
     still the most promising path to clearing 0.95, but no such idea with
     a strong rationale was available tonight.
  3. Everything from prior sessions stands: vol targeting/risk parity,
     regime switching, low-vol tilts, weight-spread dampening, sector-
     neutral scoring, monthly-cadence de-risking overlays, hedge-asset
     redirection, and (as of tonight) the daily vol-spike trim applied
     outside the magnitude-weighted basket and naive 52-week-high proximity
     are all refuted/closed.
- No engine issues encountered this session.
## 2026-08-15T01:06:58+00:00 — mom_zscore_continuity_daily_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_continuity_daily_trim.py` (family: cross-sectional momentum, trial #32)
- Hypothesis: Adding a formation-path continuity z-score (negated information discreteness: sign(return) * (%up days - %down days) over the 12-1 window) as a third equal-weight component of the composite score, with the hold-25/enter-15 buffer, magnitude weighting and daily vol-spike trim all held fixed, raises validation Sharpe above the best challenger's 1.07, net of 15 bps costs, because momentum built from continuous information persists longer than jump-driven momentum.
- Verdict: REJECT — deflated sharpe prob 0.8918 < 0.95 (bar set by 32 total trials)
- Train: sharpe +0.96, ann_ret +18.6%, maxDD -57.7%, turnover 4.8x
- Validation: sharpe +0.99, ann_ret +25.5%, maxDD -35.5%, turnover 7.2x
- Deflated Sharpe prob: 0.8918 (bar from 32 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Refuted — the path-continuity (frog-in-the-pan) axis dilutes the return-magnitude signal rather than sharpening it.** Validation Sharpe fell to 0.99 from the base mechanism's 1.07 and maxDD *widened* to -35.5% from -30.3%, giving back essentially the entire drawdown improvement the daily vol-spike trim had won. Two things are going on. (1) Giving the continuity score a full unit weight alongside the two momentum z-scores hands one third of the ranking signal to an axis that is only weakly related to future return on this universe, so the basket drifts away from the highest-magnitude names — the same directional mistake as the refuted low-vol tilts, arriving by a different route. (2) The maxDD regression is the more diagnostic result: smooth-uptrend names are *by construction* names whose recent path had low daily-return dispersion, so the basket's own realized vol is lower and less spiky, and the 21d/252d trim trigger fires less often — exactly the mechanism identified last session when the same trim was a no-op on the low-vol equal-weight basket. Selecting for path smoothness partially disarms the very overlay that makes the best challenger good. This is a genuinely new lesson: signal changes upstream of the trim are not independent of it, because the trim's usefulness depends on the basket being vol-spiky. Any future signal-side change to this basket should be checked for whether it suppresses trim activity before it is judged on Sharpe alone. Do not retry continuity at a lower composite weight — that would be knob-tuning an axis whose sign of effect is now measured as negative on both Sharpe and drawdown. `mom_zscore_narrow_daily_volspike_trim` (val Sharpe 1.07, maxDD -30.3%, DSR 0.9326, trial #28) remains the strongest challenger.

