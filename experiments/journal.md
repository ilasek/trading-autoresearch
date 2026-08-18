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


## Protocol issue — 2026-08-16 — split-brain trial history (off-branch trials)

Recorded by the weekly reporting agent, not by `run_experiment.py`. No trial
record was added, altered, or removed in writing this entry; `trials.jsonl`
remains exactly as `run_experiment.py` last wrote it (31 records).

**What happened.** From 2026-08-12 to 2026-08-15 the nightly routine pushed its
work to per-run branches (`claude/keen-einstein-*`) instead of `main`, due to an
outcome-branch setting on the scheduled trigger. Each night therefore started
from `main` at that day's data-refresh commit and could not see any prior
night's work. Four sessions ran **19 trials** in total, every one of them
independently numbered from #32 onward. None were merged into `main`.

**Consequence for the DSR gate.** `engine/protocol.py:past_trial_sharpes()`
derives the deflated-Sharpe benchmark from every `validation.sharpe_daily`
record in `trials.jsonl`. All four sessions computed their bar from 31 trials
(annualised sr_max 0.4863) when the true attempted history was 50 trials
(0.5012). Every DSR recorded in those off-branch sessions is therefore measured
against too low a benchmark and is **overstated**. The size of the error is not
recoverable from these files alone: DSR is `probabilistic_sharpe(returns,
sr_max)` and needs each candidate's daily return series, which only
`run_experiment.py` can regenerate.

**Consequence for this repo's own trial count.** `main`'s `trials.jsonl` records
31 trials. The true number of candidate strategies actually evaluated to date is
**50**. Future challengers evaluated on `main` are consequently judged against a
bar that is understated. This is a known, deliberate state: importing the 19
records would have required hand-editing a file that CLAUDE.md freezes to
`run_experiment.py`, so they were archived instead (below).

**Duplicated work caused by the split.** Residual momentum was tested four times
across three nights (#32 on 08-12; #32 and #33 on 08-13; #33 on 08-14).
Volatility targeting was tested twice (08-12 #35, 08-14 #32). Each session
recorded its result as novel because it could not see the others.

**Unresolved finding worth knowing about.** The 2026-08-14 session (trial #35,
`mom_zscore_fixed_anchor`) reported that roughly half the re-sizing turnover in
every magnitude-weighted candidate since trial #20 came from the weight vector
being anchored to the swapped-out marginal member rather than from any change in
signal. If that holds, it affects **trial #28**
(`mom_zscore_narrow_daily_volspike_trim`), which is `main`'s current best
challenger — in the direction of *understating* it (the anchor-fixed variant
recorded val Sharpe 1.085, maxDD -28.2%, turnover 5.75x, versus #28's 1.066 /
-30.3% / 7.31x). This has NOT been verified on `main` and must be re-run through
`run_experiment.py` before it is treated as established.

**Where the data went.** The four sessions are preserved in full as archive
branches, not merged and not part of `main`'s history:

  - `archive/nightly-2026-08-12` (4 trials, was `claude/keen-einstein-qlglzr`)
  - `archive/nightly-2026-08-13` (5 trials, was `claude/keen-einstein-05sf9e`)
  - `archive/nightly-2026-08-14` (5 trials, was `claude/keen-einstein-xclptt`)
  - `archive/nightly-2026-08-15` (5 trials, was `claude/keen-einstein-2j8t6q`)

Annotated tags were the intended archive format; the session's git credentials
reject `refs/tags/*` pushes (HTTP 403), so branch refs under `archive/` were used
instead. Ref deletion is likewise rejected, so the original
`claude/keen-einstein-*` branches must be deleted manually via the GitHub UI.

**Do not treat any DSR value from those archive branches as valid, and do not
promote any strategy on the basis of them.** Any idea from those sessions worth
pursuing must be re-run through `run_experiment.py` against `main`'s trial
history so it is scored on an honest bar.

### Correction (2026-08-16, same day) — archives live in TAGS, not branches

The paragraph above ("Where the data went") described the archives as branch
refs and reported that `refs/tags/*` pushes were rejected. That was true of the
reporting agent's own credentials but is no longer the state of the repo: the
repository owner pushed annotated tags from a session with full credentials, and
subsequently removed the archive branches. Superseding record:

The four off-branch sessions are preserved as **annotated tags**:

  - `archive/nightly-2026-08-12` -> 623dc427 (4 trials, was claude/keen-einstein-qlglzr)
  - `archive/nightly-2026-08-13` -> 2d3abaa8 (5 trials, was claude/keen-einstein-05sf9e)
  - `archive/nightly-2026-08-14` -> ea22d7e4 (5 trials, was claude/keen-einstein-xclptt)
  - `archive/nightly-2026-08-15` -> 0cc89937 (5 trials, was claude/keen-einstein-2j8t6q)

Verified: tag objects are annotated (not lightweight), peeled targets match the
commits above, and each tag's tree carries its session's full `trials.jsonl`
(35/36/36/36 records) and `journal.md`. Inspect without checking out, e.g.:

    git show archive/nightly-2026-08-14:experiments/journal.md
    git show archive/nightly-2026-08-14:experiments/trials.jsonl

Tags are the durable form here: branch-cleanup automation targets branches, and
a fresh clone fetches tags by default. Nothing on `main` references these
commits, so this journal entry is the only pointer to them — do not remove it.

Everything else in the protocol issue entry above stands unchanged: those trials
are NOT part of `main`'s history, `main`'s recorded count of 31 understates the
true attempted count of 50, and no strategy may be promoted on the DSR values
recorded in those sessions without re-running it through `run_experiment.py`.
## 2026-08-16T17:55:39+00:00 — mom_zscore_overlap6_daily_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_daily_trim.py` (family: cross-sectional momentum, trial #32)
- Hypothesis: Holding six overlapping monthly formation tranches (portfolio = average of the six most recent monthly target-weight vectors, 1/6 of capital reformed each month), with signal, buffer, magnitude weighting and daily vol-spike trim otherwise identical to trial #28, raises validation Sharpe above that basket's 1.066 and cuts its 7.3x turnover below 4x, net of 15 bps costs, because the turnover and effective-breadth benefits of overlapping formation dates outweigh the decay of a 12-1 momentum signal held six months.
- Verdict: REJECT — deflated sharpe prob 0.9341 < 0.95 (bar set by 32 total trials)
- Train: sharpe +0.98, ann_ret +19.4%, maxDD -56.5%, turnover 2.0x
- Validation: sharpe +1.11, ann_ret +26.9%, maxDD -29.1%, turnover 3.0x
- Deflated Sharpe prob: 0.9341 (bar from 32 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Verification re-run — the archived overlapping-tranche result reproduces on `main` to the decimal, and is now the best challenger `main` has ever recorded on every axis at once.** Validation Sharpe 1.11, ann_ret 26.9%, maxDD -29.1%, turnover 3.0x — identical to the 2026-08-15 off-branch session's numbers for the same (byte-identical) code, which is the expected result given the same data store and engine, and confirms nothing in that session's environment was inflating it. What was *not* transferable is the DSR: measured here against `main`'s honest history it is **0.9341 at 32 trials**, versus the 0.9311 the archived session reported against its own 35-trial bar. That is now the highest deflated-Sharpe probability ever recorded on `main` (previous best 0.9333, trial #21), and it beats trial #28's 0.9326 while sitting two trials further into the deflator — the Sharpe gain outran the bar-raising, which is the signature the gate needs. Note the honest caveat from the protocol-issue entry still applies in the *other* direction: `main`'s 32-trial bar understates the true 51 candidate strategies now attempted across all sessions, so this 0.9341 is itself generous relative to the real multiple-testing burden. Mechanically the finding stands as the archived session described it: the overlap converts the same signal into a far cheaper implementation (turnover 7.3x → 3.0x versus trial #28's identical basket) at *higher* return, meaning cost drag, not signal decay, was the binding constraint on this line. Establishing this on `main` was the necessary precondition for tonight's real work — every subsequent idea should be built and judged against 1.11 / -29.1% / 3.0x, not against trial #28's 1.066 or the champion's 0.865.

## 2026-08-16T17:57:34+00:00 — mom_zscore_overlap6_fixed_anchor — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_fixed_anchor.py` (family: cross-sectional momentum, trial #33)
- Hypothesis: Sizing each formation tranche by the composite z-score floored at a fixed constant, instead of by the score minus the weakest currently held member's score, raises validation Sharpe above the 1.11 of the otherwise-identical six-tranche basket (trial #32) and lowers its -29.1% maxDD, net of 15 bps costs, because the min-shift anchor rescales every weight in the book whenever the buffer swaps its weakest member — signal-independent movement that averaging six tranches damps but does not remove.
- Verdict: REJECT — deflated sharpe prob 0.9277 < 0.95 (bar set by 33 total trials)
- Train: sharpe +0.97, ann_ret +19.6%, maxDD -56.9%, turnover 2.2x
- Validation: sharpe +1.09, ann_ret +24.4%, maxDD -26.9%, turnover 2.9x
- Deflated Sharpe prob: 0.9277 (bar from 33 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Half-confirmed, and the half that failed is the informative one: the overlap had already absorbed most of the anchor artifact, so what remains of the fix on this base is essentially pure de-concentration — which buys the best drawdown in the repo's history at the cost of ~0.02 Sharpe.** New best-ever validation maxDD **-26.9%** (previous best -28.2%, and better than tonight's trial #32 at -29.1% and the champion's own -29.9%), with turnover also marginally lower (2.9x vs 3.0x). But validation Sharpe fell 1.11 → 1.09 and ann_ret 26.9% → 24.4%, so DSR dropped to 0.9277 from 0.9341. A holdings-only weight-matrix diagnostic over the validation window (no returns scored, not a backtest) explains both halves cleanly and confirms the "could cancel" branch written into the candidate's docstring *before* the run: (a) re-sizing turnover fell only 2.36x → 2.12x, a ~10% reduction, versus the ~50% reduction (4.67x → 2.30x) the identical fix produced on the non-overlapping basket — averaging six formation vectors dilutes any single formation's spurious rescale roughly 6:1, so the artifact was already mostly damped and there was little cost left to save; (b) at an identical 34.2 average positions, mean top weight fell 0.188 → 0.136 and HHI 0.0831 → 0.0579, a ~30% de-concentration. So on the overlapping base the anchor fix is no longer a turnover fix at all — it is a concentration change wearing a turnover fix's clothes, and it lands exactly where the 2026-08-14 session's retired-concentration finding predicts: less concentration, less drawdown, slightly less Sharpe. **Actionable consequence: the anchor axis is now closed on the overlapping base** (the artifact it targets is pre-harvested by the overlap), and the two candidates should be read as one strategy at two points on a risk/return dial rather than as rival ideas — trial #32 for Sharpe and DSR, trial #33 for drawdown. Since the DSR gate scores Sharpe and not drawdown, **trial #32 (1.11 / 0.9341) remains the challenger to beat**, and future work should build on its min-shift form despite this one's better risk profile. Broader methodological point, and a caution against generalising artifact-removal results: an artifact fix's value is not a property of the fix alone but of how much of the artifact the rest of the construction has already neutralised — the same two lines of code were worth a halving of re-sizing turnover on one base and almost nothing on another.

## 2026-08-16T18:03:13+00:00 — mom_zscore_overlap6_live_tranche — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_live_tranche.py` (family: cross-sectional momentum, trial #34)
- Hypothesis: Masking each live formation tranche to the names still in the current buffered held-set and renormalising it — so a tranche keeps its 1/6 of capital but cannot hold names the signal has since rejected — raises validation Sharpe above the 1.11 of the otherwise-identical six-tranche basket (trial #32), net of 15 bps costs, because roughly a fifth of that basket's book weight sits on decayed names whose momentum edge has already expired.
- Verdict: REJECT — deflated sharpe prob 0.8995 < 0.95 (bar set by 34 total trials)
- Train: sharpe +0.96, ann_ret +19.3%, maxDD -50.0%, turnover 2.6x
- Validation: sharpe +1.02, ann_ret +25.7%, maxDD -30.9%, turnover 4.6x
- Deflated Sharpe prob: 0.8995 (bar from 34 trials)
- Champion validation sharpe at the time: +0.86
- Lesson: **Refuted, and the refutation rewrites what the overlap mechanism actually is: the "stranded" capital is not a drag on the strategy, it *is* the strategy.** Pruning decayed names cost on every axis at once — validation Sharpe 1.11 → 1.02, maxDD -29.1% → -30.9%, turnover 3.0x → 4.6x — so the pre-registered falsification condition is met decisively, and the quantity involved (20.6% of average book weight, per the holdings-only diagnostic run before the trial) was far too large for this to be a measurement-scale null. The mechanism is visible in one number that was not part of the hypothesis: **average positions fell 34.2 → 18.6**. Masking each tranche to the current buffered held-set collapses the six tranches back onto near-identical name sets, so the book reverts to roughly the single-formation basket, and the overlap's *effective breadth* — which the archived 2026-08-15 decomposition identified as the source of its drawdown benefit specifically (as opposed to its turnover benefit, which is temporal) — is destroyed. The pruning then charges 1.6x of extra annual turnover for the privilege. **The correct reading of overlapping tranches is therefore not "a cheaper implementation of the same signal", which is how the archived session framed it and how tonight's trial #32 write-up repeated it. Holding names the current signal has already rejected is not a tolerated side-effect of committing capital slowly — it is the mechanism's active ingredient**, supplying temporal breadth that no contemporaneous selection rule can produce, because every contemporaneous rule by construction picks from one month's ranking. This also explains the otherwise-puzzling archived finding that six-month-stale signals cost zero return: there is no staleness tax to recover, so there was never anything for a pruning rule to win. **The staleness/tranche-lifetime axis is now closed in the conditional direction**, and it closes a loop with two prior results that pointed the same way from the other side: nominal basket-breadth widening was a no-op on maxDD (trial #30-era), and halving per-tranche size gave the drawdown gain straight back — breadth only pays when it comes from *decorrelated formation dates*, not from more names chosen at one date. Trial #32 (val Sharpe 1.11, maxDD -29.1%, DSR 0.9341) remains the challenger to beat.



## Session summary — 2026-08-16 (nightly)

- Housekeeping: the session started on a per-run branch
  (`claude/epic-mendel-g4bmnj`) with local `main` 12 commits behind
  `origin/main`. The branch held no commits of its own — it pointed at
  `origin/main`'s tip — so `git checkout main && git reset --hard
  origin/main` corrected it with nothing lost, and all of tonight's work was
  committed and pushed on `main`, per CLAUDE.md and the integrity check.
  `git branch -r --no-merged origin/main` was clean: no unlanded remote
  work. Engine tests green (16 passed). Data store fresh through 2026-08-14
  (cron working, one trading day behind).
- **Recovering the off-branch sessions was the main event.** The
  `## Protocol issue — 2026-08-16` entry above records that 19 trials from
  2026-08-12..15 never reached `main` and that none of their numbers may be
  treated as established. Those four sessions were read in full from the
  `archive/nightly-*` tags before any code was written tonight — both to
  avoid re-testing the 19 ideas they already refuted (which shaped every
  decision below) and to identify which of their findings were worth the
  cost of re-establishing honestly.
- Experiments run: 3 of the 8-trial budget (#32 `mom_zscore_overlap6_daily_trim`,
  #33 `mom_zscore_overlap6_fixed_anchor`, #34 `mom_zscore_overlap6_live_tranche`).
  Verdicts: 3 REJECT, 0 PROMOTE, 0 GATE_FAIL. Champion unchanged:
  `mom_12m_baseline` (validation Sharpe 0.865).
- **Best finding, and the best result ever recorded on `main`:** trial #32,
  the overlapping-tranche construction, re-run verbatim from the archive —
  **validation Sharpe 1.11, ann_ret 26.9%, maxDD -29.1%, turnover 3.0x,
  DSR 0.9341.** It reproduced the archived numbers to the decimal, which
  confirms nothing in that session's environment was inflating them, and its
  DSR — the one number that could not transfer, since it depends on trial
  history — is the highest ever recorded here, beating trial #21's 0.9333 and
  trial #28's 0.9326 while sitting further into the deflator. Still short of
  the 0.95 PROMOTE bar.
- Second finding: trial #33 produced the repo's best-ever validation
  drawdown, **-26.9%**, for about 0.02 of Sharpe. Since the gate scores
  Sharpe and not drawdown it is not the challenger to beat, but #32 and #33
  are best read as one strategy at two points on a risk/return dial.
- Key new patterns this session (all distilled into `experiments/learnings.md`):
  1. **The overlap mechanism's explanation was wrong, and the correction is
     the session's most useful output.** It is not "a cheaper implementation
     of the same signal". Holding names the current signal has already
     rejected — 20.6% of average book weight — is the active ingredient.
     Pruning them cost Sharpe, drawdown *and* turnover at once, and dropped
     average positions 34.2 → 18.6: the six tranches collapse onto
     near-identical name sets, destroying temporal breadth that no
     contemporaneous selection rule can reproduce. Breadth pays only when it
     comes from decorrelated formation dates, not from more names picked at
     one date — which closes a loop with two earlier no-op breadth results.
  2. **An artifact fix's value is a property of the base, not the fix.** The
     min-shift anchor fix halved re-sizing turnover on the non-overlapping
     basket but moved it only ~10% here, because averaging six formations
     already damps a single formation's spurious rescale ~6:1. What remained
     was pure de-concentration (HHI -30%), which is why it bought drawdown
     and gave back Sharpe.
  3. Holdings-only diagnostics remain the cheapest tool in the lab — see
     below.
- Why 3 trials and not 8. Two further ideas were **killed without spending a
  trial**, which is why the budget was not exhausted:
  (a) Re-specifying the daily vol-spike trim to measure the *actual
  book-weighted* basket vol rather than the equal-weighted proxy the code
  uses. This looked like a genuine mis-specification of the kind that paid
  off in trial #33, but a trigger-firing diagnostic showed the two
  definitions disagree on **1 of 1562 validation days** — the 21d/252d vol
  ratio is nearly insensitive to weighting within one correlated basket.
  (b) Diversifying the month-end formation phase, to test whether the 1.11
  is timing luck. Reading the archive showed this was already answered
  (2026-08-13, weekly-staggered formation dates: Sharpe 1.05 vs 1.07, inside
  noise) — the result is not a timing-luck artifact, and re-running it here
  would have burned a trial to learn nothing.
  Beyond those, the well-motivated hypothesis space is genuinely thin: the
  archived sessions closed signal definition hard (52-week-high proximity,
  residual momentum twice, information discreteness — all at or below the
  base), and concentration, trim cadence/threshold/redirect, sector
  neutrality, capital blending and K-sweeping are all explicitly closed.
  Forcing a fourth trial would have permanently raised the DSR bar for a
  hypothesis none of tonight's evidence supports. This matches the
  2026-08-07, 08-11 and 08-14 precedents and the program's explicit
  quality-over-quantity instruction.
- **Distance to promotion, and a caveat that cuts against us.** The best
  challenger is at 1.11 with DSR 0.9341; the 2026-08-14 arithmetic put the
  Sharpe needed to clear 0.95 at roughly 1.17-1.20, and nothing tonight
  closes that gap. Note also the standing bias flagged in the protocol-issue
  entry: `main` has now recorded 34 trials, but the true number of candidate
  strategies attempted across all sessions is 53 (31 + tonight's 3, plus the
  19 archived). Every DSR scored on
  `main` is therefore *generous* relative to the real multiple-testing
  burden, and a borderline PROMOTE should be read with that in mind. This is
  a known, deliberate state — importing the archived records would mean
  hand-editing a file CLAUDE.md freezes to `run_experiment.py`.
- Ideas for next session:
  1. The highest-value direction follows from tonight's correction: if
     temporal breadth from decorrelated formation dates is the active
     ingredient, the open question is what else supplies decorrelated
     formation dates *without* being a K sweep. Formations one month apart
     share 11/12 of their 12-1 lookback window, so the six tranches are far
     from independent — a construction that genuinely decorrelates them
     (rather than spacing them further apart, which is knob-tuning) is a
     distinct idea with its own rationale.
  2. Do not build further on the anchor axis (closed on this base tonight),
     the tranche-lifetime axis (closed tonight), or any signal-definition
     idea (heavily explored, low-yield, four refutations).
  3. If no strong hypothesis is available, patience is a legitimate move:
     the challenger's DSR has now risen three times in a row across
     bar-raising trials, which no other line in this repo has done.
- No engine issues encountered this session.

## 2026-08-16 — Protocol change (human-directed) — **[engine-maintenance]**

Not an experiment. No trial recorded, no candidate run, holdout untouched.
Two defects in how the deflated-Sharpe gate was applied, found by auditing the
trial record, fixed on the human's instruction.

**Defect 1 — the incumbent held a seat it never earned.** `run_trial` computed
the DSR and then the bootstrap branch (`if not CHAMPION_FILE.exists()`) promoted
regardless. `mom_12m_baseline` was seated at DSR 0.9312, below the 0.95 bar it
then imposed on all 33 challengers after it, and was never re-deflated as the
trial count grew. Judged against the pool as it stands it scores 0.8129 raw.
Meanwhile `mom_zscore_overlap6_daily_trim`, at +28% validation Sharpe (1.107 vs
0.865), was rejected at 0.9341 — a higher DSR than the champion ever posted.

Fixes: the bootstrap path now enforces the same threshold (no champion is seated
until one is earned), and every comparison re-deflates the incumbent against
exactly the bar the challenger faces. A champion that can no longer clear the
threshold is **provisional**: it can be displaced by a candidate that beats it on
both validation Sharpe and DSR, even below 0.95. A champion that does clear the
threshold can only be displaced by another that also clears it. `champion_dsr`
is now recorded on every trial, and the champion card carries `dsr_at_promotion`
and a `provisional` flag.

**Defect 2 — near-duplicate trials were deflated as independent ones.** Bailey &
López de Prado's E[max SR] assumes independent trials. `effective_n_trials` now
clusters trials by the correlation of their validation returns (single linkage,
rho >= 0.95) and passes the cluster count to `deflated_sharpe`. Per-trial
validation returns are stored in `experiments/trial_returns/` under a filename
derived from the trial's timestamp and name, so `trials.jsonl` is never
rewritten. `scripts/backfill_trial_returns.py` reconstructed 33 of 34 historical
trials with zero Sharpe drift; `mom_zscore_daily_volspike_trim`'s candidate file
was deleted earlier, so it has no returns and keeps counting on its own. Trials
without stored returns always count independently — the conservative default.
The dispersion term still uses every recorded trial; only the count is corrected.

**Result: 34 trials are worth 11 effective ones.** 23 of them — the entire ladder
from `mom_12m_baseline` through `overlap6` — are one cluster. The expected-max
bar drops from 0.503 to 0.384 annualized. Champion 0.8129 -> 0.8810 (still
provisional); best challenger 0.9317 -> 0.9626 (clears 0.95 outright).

**Honest caveat.** Within-family tuning is now nearly free in deflation terms:
the 24th momentum variant joins an existing cluster and barely moves the bar.
That is the intended correction — redundant trials were never extra shots on
goal — but it removes deflation as a brake on within-family overfitting. What
still holds the line is that a challenger must beat the incumbent's raw
validation Sharpe, and that the validation window is fixed, so a ladder of tweaks
climbing it is still fitting one sample. The holdout remains the only real check.

**DSR values recorded before this entry are not comparable to those after it.**
Trials 1-34 were deflated at the raw trial count with no incumbent re-deflation.
Nothing in `trials.jsonl` was altered.

- Lesson: a multiple-testing correction is only as honest as its independence
  assumption and its treatment of the incumbent. This repo had 34 trials on
  paper, 11 real ones, and a champion exempt from its own bar.
## 2026-08-16T20:32:35+00:00 — mom_zscore_overlap6_daily_trim — **PROMOTE**
- Candidate: `strategies/candidates/mom_zscore_overlap6_daily_trim.py` (family: cross-sectional momentum, trial #35)
- Hypothesis: Holding six overlapping monthly formation tranches (portfolio = average of the six most recent monthly target-weight vectors, 1/6 of capital reformed each month), with signal, buffer, magnitude weighting and daily vol-spike trim otherwise identical to trial #28, raises validation Sharpe above that basket's 1.066 and cuts its 7.3x turnover below 4x, net of 15 bps costs, because the turnover and effective-breadth benefits of overlapping formation dates outweigh the decay of a 12-1 momentum signal held six months.
- Verdict: PROMOTE — beats champion (1.107 > 0.865) with DSR 0.9621 (35 trials, 11 effective after clustering at rho 0.95)
- Train: sharpe +0.98, ann_ret +19.4%, maxDD -56.5%, turnover 2.0x
- Validation: sharpe +1.11, ann_ret +26.9%, maxDD -29.1%, turnover 3.0x
- Holdout: sharpe +1.22, ann_ret +32.7%, maxDD -23.3%, turnover 3.7x
- Deflated Sharpe prob: 0.9621 (bar from 35 trials, 11 effective)
- Champion validation sharpe at the time: +0.86
- Champion re-deflated at the same bar: 0.8798 — **provisional seat**
- Lesson: **The strategy did not change; the bar did — and this is the first champion in this repo to have actually earned its seat.** The code promoted here is byte-identical to trial #32, which was REJECTed nine hours earlier at DSR 0.9341 on the same data. What moved was the protocol: clustering near-duplicate trials before deflating cut 35 recorded trials to 11 effective ones, and re-deflating the incumbent at the challenger's own bar exposed `mom_12m_baseline` as holding a seat it could no longer win (0.8798, provisional). Two things are worth carrying forward. First, the holdout — touched here for the first time since the baseline was seated — is the strongest evidence in the repo that the overlapping-tranche mechanism is not a validation-window artifact: Sharpe 1.22, ann_ret 32.7%, maxDD -23.3% on 2024+, *better* than validation on all three axes, which is the reverse of the usual out-of-sample decay. Second, the caveat in the protocol-change entry binds hard from here on: clustering makes within-family tuning nearly free in deflation terms, so DSR is no longer a brake on a ladder of momentum variants climbing one fixed validation window. The champion's raw validation Sharpe, not its DSR, is now the binding constraint on every challenger, and the holdout is the only remaining real check. _(Filled in by the second 2026-08-16 session; the promoting run left this line blank.)_

## 2026-08-16T23:11:49+00:00 — mom_zscore_overlap6_ddbrake — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_ddbrake.py` (family: regime switching, trial #36)
- Hypothesis: Adding a hysteresis drawdown brake on the book's own equity (cut exposure to 0.6x when the pre-trim book is more than 20% below its running peak, restore when it recovers to within 10%), combined with the existing daily vol-spike trim by min() so peak de-risking is unchanged, raises validation Sharpe above the champion's 1.107 net of 15 bps costs, because the vol-ratio trigger it already carries fires in the strategy's best year and is nearly blind in both years it loses money, where the losses are slow grinds without a dispersion spike.
- Verdict: REJECT — validation sharpe 0.989 <= champion 1.107
- Train: sharpe +0.99, ann_ret +17.5%, maxDD -46.5%, turnover 1.9x
- Validation: sharpe +0.99, ann_ret +21.4%, maxDD -33.3%, turnover 3.4x
- Deflated Sharpe prob: 0.9313 (bar from 36 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.9627
- Lesson: **Refuted decisively, and in the most informative way available: the brake made the exact regime it was built for worse.** It was motivated by a returns-only diagnostic showing the champion's vol-spike trigger fires on 44 days in 2020 (+132%, its best year) and on 0 days in 2021 and 2023, but only 7 days in 2018 and 13 in 2022 — the two years the book loses money, both slow grinds without a dispersion spike. The brake was aimed squarely at that gap and **2022 went from -8.9% to -17.4%**. The full year decomposition against the champion: 2018 +1.0%, 2019 **-13.3%**, 2020 0.0%, 2021 -10.7%, 2022 **-8.6%**, 2023 0.0% — one small win, three large losses, and validation maxDD *widened* -29.1% -> -33.3% even though train maxDD improved -56.5% -> -46.5%, the exact in-sample-crash-fix-that-does-not-transfer signature `learnings.md` already records for three earlier de-risking overlays. The mechanism of the failure is visible in 2019: the brake armed in the 2018-10 selloff and, because it only releases once the book recovers to within 10% of its peak, was still de-risked through the start of a +50% year. **This is the mirror image of the cadence lesson the daily vol-spike trim taught: that one said a trigger must react faster than the strategy's rebalance; this one says a release rule slower than the recovery costs more than the trigger ever saves.** Drawdown depth is a lagging state variable — by the time it crosses a threshold deep enough to be outside routine noise (only 4 of 55 validation episodes reach -20%), the information is mostly about what already happened. The drawdown-brake axis is closed; do not retry it with different thresholds, which is the only knob left and would be tuning a refuted mechanism.

## 2026-08-16T23:16:35+00:00 — mom_zscore_overlap6_trim_universe — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_trim_universe.py` (family: cross-sectional momentum, trial #37)
- Hypothesis: Computing the daily vol-spike trim's realized-vol trigger over the names actually held — qualifying them on a trailing 283-day window instead of a complete history back to 1962, which currently admits a mean of 3 of 34 held names and 11% of book weight — raises validation Sharpe above the champion's 1.107 net of 15 bps costs, because the trigger then measures the turbulence of the book it de-risks rather than that of an incidental handful of long-listed instruments.
- Verdict: REJECT — validation sharpe 1.05 <= champion 1.107
- Train: sharpe +0.97, ann_ret +19.3%, maxDD -57.6%, turnover 2.1x
- Validation: sharpe +1.05, ann_ret +24.7%, maxDD -30.8%, turnover 4.5x
- Deflated Sharpe prob: 0.95 (bar from 37 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.9629
- Lesson: **The champion's daily vol-spike trim does not measure its own basket, and never has.** Every candidate in this line since trial #22 computes the trigger as `prices.iloc[:end_pos][names].dropna(axis=1, how='any')` — and because the price store starts in 1962, that filter keeps only instruments with a complete ~60-year history. A holdings-only diagnostic over the champion's own formations (weights only, nothing scored) shows the consequence: across the 72 validation-window formations the book holds a mean of 34.1 names of which a mean of **3.0** survive the filter — **11% of book weight**, and zero in some months, which disables the trim outright. The eleven instruments that can ever qualify are JNJ, PG, XOM, CVX, KO, MRK, DIS, IBM, CAT, GE and HON: old-economy large-cap defensives and industrials, close to the opposite style to a high-momentum growth book. Pointing the trigger at the names actually held (and, in passing, making it strictly causal — the original reads one rebalance into the future to decide the trigger's membership) **lowered** validation Sharpe 1.107 -> 1.050 and cost return in all six validation years: 2018 -2.4%, 2019 -3.2%, 2020 -2.9%, 2021 -1.0%, 2022 -3.7%. Note what this is *not*: `learnings.md` records a prior session killing a trim re-specification by diagnostic, but that one compared book-weighted against equal-weighted vol *of this same 3-name subset* and correctly found the ratio insensitive to weighting. The universe, not the weighting, was the defect — a reminder that a cheap diagnostic only closes the question it actually asked.

## 2026-08-16T23:18:20+00:00 — mom_zscore_overlap6_notrim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_notrim.py` (family: cross-sectional momentum, trial #38)
- Hypothesis: Removing the daily vol-spike trim from the champion entirely leaves validation Sharpe at or near the 1.050 of the correctly-specified trim (trial #37) rather than materially below it, net of 15 bps costs, because the trim's apparent contribution to the champion's 1.107 comes from a degenerate trigger universe — a mean of 3 of 34 held names — rather than from detecting turbulence in the book.
- Verdict: REJECT — validation sharpe 1.062 <= champion 1.107
- Train: sharpe +0.94, ann_ret +19.4%, maxDD -56.1%, turnover 1.6x
- Validation: sharpe +1.06, ann_ret +26.9%, maxDD -30.3%, turnover 2.6x
- Deflated Sharpe prob: 0.9527 (bar from 38 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.963
- Lesson: **The control this line never had on `main`, and it reproduces the archived number to the decimal (1.062).** With the trim deleted the book keeps the champion's ann_ret (26.9%, identical) and gives up 0.045 of Sharpe and 1.2pp of drawdown (-30.3% vs -29.1%) while *lowering* turnover 3.0x -> 2.6x. Set against trial #37 this is the uncomfortable result of the session so far: **the correctly-specified basket-own trim (1.050) is worse than no trim at all (1.062)**, so the mechanism as the repo has described it is not merely mis-measured, it is value-destroying when measured properly, and the champion's margin comes from the mis-specification rather than from crash detection. This also re-establishes the honest baseline for the whole overlapping-tranche line: an untrimmed six-tranche book at 1.062 / -30.3% / 2.6x is the simplest thing in the repo that gets most of the way to the champion, and it is fully explained — no accidental universe anywhere in it.

## 2026-08-16T23:20:31+00:00 — mom_zscore_overlap6_market_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_market_trim.py` (family: regime switching, trial #39)
- Hypothesis: Driving the daily exposure trim from a deliberately specified market-wide vol-spike trigger — the equal-weighted 21d/252d realized vol ratio of every instrument with a complete trailing 283-day history, held or not — raises validation Sharpe above the champion's 1.107 net of 15 bps costs, because the champion's trigger already reads a style-orthogonal set of long-listed defensives rather than its own basket, and specifying that on purpose replaces an incidental 3-name sample with the full cross-section of the same signal.
- Verdict: REJECT — validation sharpe 1.055 <= champion 1.107
- Train: sharpe +0.97, ann_ret +19.3%, maxDD -56.8%, turnover 2.1x
- Validation: sharpe +1.05, ann_ret +25.1%, maxDD -30.6%, turnover 3.5x
- Deflated Sharpe prob: 0.9516 (bar from 39 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.9632
- Lesson: **Not the market either — the deliberate market-wide trigger lands at the no-trim control.** Replacing the incidental legacy sample with the equal-weighted vol ratio of every instrument listed for the trailing 283 days (the whole cross-section, held or not, no tickers hard-coded, strictly causal) gave 1.055 against the 1.062 of deleting the trim entirely, and a slightly worse drawdown (-30.6% vs -30.3%). So the style-orthogonality reading in this candidate's docstring — 'the trigger works because it reads defensives rather than the book' — is *not* confirmed in its general form: diluting those defensives into 140 instruments destroys the effect just as thoroughly as dropping them did in trial #37. After three deliberate specifications (basket 1.050, market 1.055, none 1.062) every intentional version of this overlay sits within 0.012 Sharpe of doing nothing, while the accident is worth 0.045. That narrows the question to a single remaining degree of freedom rather than answering it: the champion conditions on **basket membership ∩ legacy cohort**, and neither term on its own reproduces anything.

## 2026-08-16T23:22:24+00:00 — mom_zscore_overlap6_legacy_trim — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_overlap6_legacy_trim.py` (family: regime switching, trial #40)
- Hypothesis: Driving the daily exposure trim from the realized vol of the whole long-listed cohort — every instrument with a complete history from the store's start to the formation date, held or not, rather than only the ~3 of them the momentum screen happens to hold — reproduces or beats the champion's 1.107 validation Sharpe net of 15 bps costs, because the signal doing the work is those defensives' turbulence and not the incidental intersection with basket membership.
- Verdict: REJECT — validation sharpe 1.081 <= champion 1.107
- Train: sharpe +0.98, ann_ret +19.4%, maxDD -58.9%, turnover 2.1x
- Validation: sharpe +1.08, ann_ret +25.7%, maxDD -29.1%, turnover 3.6x
- Deflated Sharpe prob: 0.9578 (bar from 40 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.9632
- Lesson: **Roughly 40% of the trim's credit is a real, specifiable signal and the rest needs an intersection with no mechanism behind it — and the drawdown benefit is entirely the real half.** Driving the trim from the whole long-listed cohort (the champion's own filter with the basket intersection deleted) gives 1.081, and the five-way comparison now brackets the component completely:
    | trim trigger universe | val Sharpe | maxDD | turnover |
    |---|---|---|---|
    | held ∩ legacy cohort (champion) | 1.107 | -29.1% | 3.0x |
    | legacy cohort, whole (#40) | 1.081 | -29.1% | 3.6x |
    | none — control (#38) | 1.062 | -30.3% | 2.6x |
    | whole market (#39) | 1.055 | -30.6% | 3.5x |
    | the actual held basket (#37) | 1.050 | -30.8% | 4.5x |
  Two readings, and both matter. **The mechanistic half:** the cohort trigger reproduces the champion's validation maxDD to the decimal (-29.1%), so the entire 1.2pp drawdown benefit over the untrimmed control is attributable to the long-listed defensives' volatility and needs nothing accidental to explain it. The ordering basket (1.050) < market (1.055) < none (1.062) < cohort (1.081) is monotone in how style-orthogonal the trigger is to a momentum book, which is a coherent mechanism and not a random scatter: a momentum book's own vol rises in melt-ups as readily as in crashes, the market's vol is a blend, and a defensive cohort is turbulent mainly in genuine systemic stress. **The luck half:** the remaining 0.026 of Sharpe requires sampling that cohort *through* month-to-month basket membership — a 3-name subset chosen by which defensives a momentum screen happens to hold — and no mechanism reads that way. The honest conclusion is that the champion's 1.107 contains roughly 0.026 of Sharpe that is sampling luck inside a 6-year window, and that the repo should stop describing the daily vol-spike trim as 'the basket's own realized vol'; it is a defensive-cohort stress overlay worth about +0.019 Sharpe and -1.2pp of drawdown when specified deliberately. The champion keeps its seat — it won the gate honestly and its holdout is the repo's best number — but its margin over the simple untrimmed book is now only partly explained, which is exactly the thing a future session should not build on top of without re-reading this entry.


## Session summary — 2026-08-16 (nightly, second session)

- Housekeeping: started on a per-run branch (`claude/epic-mendel-91epxp`) that
  pointed at `origin/main` with no commits of its own, so `git checkout main &&
  git reset --hard origin/main` corrected it with nothing lost; all of tonight's
  work is on `main`. `git branch -r --no-merged origin/main` clean — no unlanded
  remote work. Engine tests green (16 passed). Data store fresh through
  2026-08-14. Also filled in the Lesson line for trial #35, which the promoting
  run left blank.
- Experiments run: 5 of the 8-trial budget (#36 `..._ddbrake`, #37
  `..._trim_universe`, #38 `..._notrim`, #39 `..._market_trim`, #40
  `..._legacy_trim`). Verdicts: 5 REJECT, 0 PROMOTE, 0 GATE_FAIL. Champion
  unchanged: `mom_zscore_overlap6_daily_trim` (validation Sharpe 1.107).
- **The session's finding is about the champion itself, and it is not
  flattering.** The daily vol-spike trim the repo has been citing as one of its
  strongest mechanisms — "the basket's own realized vol", the first thing here
  ever to improve Sharpe and drawdown at once — does not measure the basket. Its
  availability filter runs `dropna(how='any')` over a price prefix that starts in
  1962, so only instruments with a complete ~60-year history qualify: a mean of
  **3 of the 34 names held, 11% of book weight**, zero in some months. The eleven
  instruments that can ever qualify are JNJ, PG, XOM, CVX, KO, MRK, DIS, IBM,
  CAT, GE, HON — old-economy defensives, close to the opposite style to the
  momentum book they are trimming.
- Four trials bracketed what that accident is worth, against every deliberate
  specification of the overlay plus the control of deleting it:

  | trim trigger universe | val Sharpe | maxDD | turnover |
  |---|---|---|---|
  | held ∩ legacy cohort (champion) | 1.107 | -29.1% | 3.0x |
  | legacy cohort, whole (#40) | 1.081 | -29.1% | 3.6x |
  | none — control (#38) | 1.062 | -30.3% | 2.6x |
  | whole market (#39) | 1.055 | -30.6% | 3.5x |
  | the actual held basket (#37) | 1.050 | -30.8% | 4.5x |

  Reading, in two halves. **Real:** the cohort trigger reproduces the champion's
  validation maxDD exactly (-29.1%), so the whole drawdown benefit over the
  untrimmed control is attributable to long-listed defensives' volatility, and
  the ordering basket < market < none < cohort is monotone in style-orthogonality
  — a coherent mechanism, worth about +0.019 Sharpe and -1.2pp drawdown when
  specified on purpose. **Luck:** the remaining 0.026 of Sharpe requires sampling
  that cohort *through* month-to-month basket membership, and no mechanism reads
  that way. Also established: the correctly-specified basket-own trim (1.050) is
  worse than no trim at all (1.062).
- Second finding: a hysteresis drawdown brake on the book's own equity (#36) was
  refuted hard, making the exact regime it targeted worse (2022 -8.9% -> -17.4%)
  and widening validation maxDD to -33.3% while improving train maxDD — the
  familiar signature of an in-sample crash fix that does not transfer. The
  mechanism of its failure is the complement of the cadence lesson the vol-spike
  trim taught: a *release* rule slower than the recovery costs more than the
  trigger saves (it was still de-risked into the start of a +50% 2019).
- Two candidate ideas were killed by diagnostic without spending a trial: a
  no-trade band on weights (arithmetic — at 3.0x turnover the champion's entire
  cost drag is 0.45%/yr ≈ 0.019 Sharpe, so turnover reduction is now a spent
  lever on this base, which is also why the archived `mom_zscore_notrade_band`
  result should not be revisited), and finer-cadence formation dates (the trim
  loop is O(prefix x periods), and weekly formation would have required changing
  the trim's implementation, confounding the cadence test with tonight's subject).
- Why 5 and not 8: after #40 the trim question was answered in both directions
  and no remaining hypothesis was better motivated than the ones already
  refuted. Forcing more trials would have been sweeping the trigger definition,
  which is the knob-tuning the program explicitly warns against.
- Ideas for next session:
  1. **The champion's docstring and `learnings.md` now overstate its trim.** A
     future session that wants a *fully explained* strategy should consider that
     `mom_zscore_overlap6_notrim` (1.062 / -30.3% / 2.6x) and
     `mom_zscore_overlap6_legacy_trim` (1.081 / -29.1% / 3.6x) contain no
     accidental component. Neither can displace the champion under the gate,
     which scores validation Sharpe only — that is a limitation of the gate, not
     evidence that they are worse strategies.
  2. Untouched and still open: what supplies *decorrelated formation dates*
     without being a K sweep (last session's idea #1, not attempted tonight).
  3. Closed tonight: drawdown-state braking (any threshold), trim-trigger
     universe (all four specifications tested).
  4. Standing caution, unchanged: the validation window's P&L is dominated by
     2019-2020 (+50%, +132%) with losses in 2018 and 2022, and DSR clustering has
     removed deflation as a brake on within-family tuning. The holdout is the only
     real check left.
- No engine issues encountered this session.

## Research session — 2026-08-17 (learning agent): 4 notes added, see research/SUMMARY.md

## Research session — 2026-08-17 (learning agent): 3 notes added, see research/SUMMARY.md

## Research session — 2026-08-17 (learning agent): 4 notes added, see research/SUMMARY.md

## Research session — 2026-08-17 (learning agent): 3 notes added, see research/SUMMARY.md
## 2026-08-17T23:08:54+00:00 — mom_zscore_overlap6_hzn_avg — **PROMOTE**
- Candidate: `strategies/candidates/mom_zscore_overlap6_hzn_avg.py` (family: cross-sectional momentum, trial #41)
- Hypothesis: Averaging the 12-1 and 6-1 momentum legs as separate buffered, magnitude-weighted target portfolios — rather than summing their z-scores into one score before selecting a single basket — with the six-tranche date overlap, buffer band, weighting and daily vol-spike trim otherwise identical to the champion, raises validation Sharpe above the champion's 1.107 net of 15 bps costs, because the two lookback windows are decorrelated estimates of the same quantity (rank correlation 0.66, portfolio weight overlap 0.60) and averaging them at the portfolio level supplies a second axis of vintage diversity that date-spacing alone cannot, whereas score-level compositing discards it by collapsing to one basket.
- Verdict: PROMOTE — beats champion (1.112 > 1.107) with DSR 0.9638 (41 trials, 11 effective after clustering at rho 0.95)
- Train: sharpe +0.96, ann_ret +18.7%, maxDD -57.2%, turnover 2.0x
- Validation: sharpe +1.11, ann_ret +26.1%, maxDD -28.5%, turnover 3.2x
- Holdout: sharpe +1.32, ann_ret +34.1%, maxDD -22.1%, turnover 3.3x
- Deflated Sharpe prob: 0.9638 (bar from 41 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.9631
- Lesson: **A promotion that the validation split did not really earn, and a holdout that says the mechanism is nonetheless real.** The gate fired on a validation margin of **0.005** (1.112 vs 1.107) — an order of magnitude smaller than the ~0.026 of Sharpe that trials #37-#40 attributed to sampling luck in the trim's `held ∩ legacy-cohort` intersection, which this candidate necessarily perturbs by widening the book from ~34 to ~47 names. That confound was written into the candidate's docstring *before* the run, and it binds: on validation alone this result is a coin flip, and `research/SUMMARY.md`'s rebalance-timing-luck note says the same thing from the other side (a single backtest of a discretely rebalanced strategy is one draw, so gaps this small are not evidence). What is *not* inside that noise is the holdout: **1.32 Sharpe, +34.1% ann_ret, maxDD -22.1%** against the outgoing champion's 1.22 / +32.7% / -23.3% — better on all three axes, on the one split neither candidate was tuned against, and the second consecutive time this line's holdout has come in *above* its validation rather than decaying. Two further readings. (a) The change is squarely on the axis the repo has established as its only live one: it moves nothing about the signal, only *where the averaging happens* — two lookback windows now produce two buffered, magnitude-weighted portfolios that are averaged, instead of two z-scores summed into one score that produces one portfolio. Score-level compositing is a lossy collapse: it discards the fact that the two windows disagree about *which names to hold* (weight overlap 0.60 full-sample, 0.47 in validation) and keeps only their agreement about ranking. (b) It also answers the journal's standing open question — *what supplies decorrelated formation vintages without being a K sweep* — in the affirmative, with **lookback length** as the second axis, exactly as `research/SUMMARY.md` candidate #7 predicted from the averaging-over-estimation-windows literature. Date diversity and length diversity are close to independent: the champion's date-tranches already overlap only 0.35 of weight at lag 5 in validation, and this adds a dimension orthogonal to that. **The honest summary is that the mechanism is corroborated by breadth (avg positions 34 -> 47), by drawdown (-29.1% -> -28.5% validation, -23.3% -> -22.1% holdout) and by the holdout Sharpe, and is *not* corroborated by the validation Sharpe the gate actually scores.** Read the next two trials in this session as the real test of whether the axis has anything more in it.

## 2026-08-17T23:11:19+00:00 — mom_zscore_overlap6_hzn_avg4 — **PROMOTE**
- Candidate: `strategies/candidates/mom_zscore_overlap6_hzn_avg4.py` (family: cross-sectional momentum, trial #42)
- Hypothesis: Widening the averaged lookback bracket from two windows (12-1, 6-1) to four evenly spaced quarterly windows (12-1, 9-1, 6-1, 3-1), each forming its own buffered magnitude-weighted portfolio averaged at equal weight, with the six-tranche date overlap, band, weighting and daily vol-spike trim otherwise identical to trial #41, raises validation Sharpe above that candidate's 1.112 net of 15 bps costs, because the gain from portfolio-level horizon averaging is horizon diversity as such — bracketing an unknown bias-variance optimum rather than estimating it — and not a property of the particular two windows the repo inherited.
- Verdict: PROMOTE — beats champion (1.12 > 1.112) with DSR 0.9652 (42 trials, 11 effective after clustering at rho 0.95)
- Train: sharpe +0.97, ann_ret +18.6%, maxDD -57.2%, turnover 2.0x
- Validation: sharpe +1.12, ann_ret +25.7%, maxDD -27.8%, turnover 3.1x
- Holdout: sharpe +1.38, ann_ret +34.9%, maxDD -20.1%, turnover 2.8x
- Deflated Sharpe prob: 0.9652 (bar from 42 trials, 11 effective)
- Champion validation sharpe at the time: +1.11
- Champion re-deflated at the same bar: 0.9636
- Lesson: **Bracket width is the live variable, and validation Sharpe is the *least* informative axis on which it moves.** Doubling the number of averaged lookback windows from two to four moved validation Sharpe 1.112 -> 1.120 (+0.008, again inside the noise both #41 and this candidate pre-registered), but every other axis moved in the same direction and by margins that are not noise: validation maxDD **-28.5% -> -27.8%** (the best drawdown ever recorded on a promoted strategy here, beating the -26.9% of the unpromoted `..._fixed_anchor` only in the sense that this one also carries the Sharpe), turnover **3.2x -> 3.1x**, average positions 47 -> 63, and holdout **1.32 -> 1.38 Sharpe with maxDD -22.1% -> -20.1% at 2.8x turnover**. Read the three-point sequence rather than any single comparison — one window bracket -> two -> four gives validation Sharpe 1.107 / 1.112 / 1.120, validation maxDD -29.1% / -28.5% / -27.8%, holdout Sharpe 1.22 / 1.32 / 1.38, holdout maxDD -23.3% / -22.1% / -20.1%. Monotone on all four, and the two axes moving *most* are the ones the gate does not score. So the answer to what #41 left open is that **the gain is horizon diversity as such, not a property of the two windows the repo inherited** — and the falsification test written into this candidate's docstring resolved in the informative direction: breadth rose steeply (47 -> 63 positions) *without* the concentration price `learnings.md` has attached to every previous de-concentration step, which cost ~0.02 of Sharpe each time. That price was real when de-concentration came from spreading capital across more names picked at one date; it does not appear when the extra names arrive from a genuinely decorrelated vintage. This is the same law as the pruning result, one axis over. **Two disciplines this result must not be allowed to break.** First, the docstring committed in advance to trying no other bracket this session, and that commitment holds: comparing a fifth or a sixth window is the sweep the manual forbids, and the bounds argument (skip-month at the short end, post-formation reversal at the long end) already fixes the interval — what is *not* fixed, and is a legitimate question for a later session with its own rationale, is whether the windows should fill that interval evenly. Second and more serious: **two promotions in one session means the holdout has now been touched twice tonight, and a ladder of small validation wins is spending the only real check the repo has left.** Trial #43 must be motivated without reference to any holdout number above.

## 2026-08-17T23:14:02+00:00 — mom_zscore_hzn_avg4_k1 — **PROMOTE**
- Candidate: `strategies/candidates/mom_zscore_hzn_avg4_k1.py` (family: cross-sectional momentum, trial #43)
- Hypothesis: Averaging four quarterly lookback-length vintages (12-1, 9-1, 6-1, 3-1) as separate buffered magnitude-weighted portfolios while removing the six-tranche date overlap entirely (whole book reformed monthly), with band, weighting and daily vol-spike trim otherwise identical to trial #42, lands validation Sharpe materially above the 1.066 of the same construction with a single composite score and no overlap (trial #28) net of 15 bps costs, because length-vintage and date-vintage diversity are substitutable routes to one mechanism rather than complements; landing at or below 1.066 falsifies that and shows horizon averaging only works on top of the date overlap.
- Verdict: PROMOTE — beats champion (1.187 > 1.12) with DSR 0.9747 (43 trials, 11 effective after clustering at rho 0.95)
- Train: sharpe +0.94, ann_ret +18.1%, maxDD -54.1%, turnover 4.5x
- Validation: sharpe +1.19, ann_ret +28.7%, maxDD -29.0%, turnover 7.4x
- Holdout: sharpe +0.88, ann_ret +22.6%, maxDD -27.4%, turnover 8.0x
- Deflated Sharpe prob: 0.9747 (bar from 43 trials, 11 effective)
- Champion validation sharpe at the time: +1.12
- Champion re-deflated at the same bar: 0.9645
- Lesson: **The validation split and the holdout disagree about the sign of the date overlap, and the gate scores only the one that is wrong. This is the most important result of the session and it is a warning, not a discovery.** Switching the six-tranche date overlap off — keeping the four-horizon portfolio averaging from #42 and changing nothing else — produced the largest single validation jump ever recorded here, **1.120 -> 1.187** (+0.067, more than ten times the margin of either promotion earlier tonight), the best DSR on record at 0.9747, and the gate duly promoted it. On the holdout the same change is a **collapse: 1.38 -> 0.88 Sharpe, ann_ret 34.9% -> 22.6%, maxDD -20.1% -> -27.4%**. The third outcome enumerated in this candidate's docstring — "the date overlap is redundant once enough horizons are averaged" — is what validation says, and it is wrong. **Costs do not explain it.** Turnover rises 2.8x -> 8.0x on holdout, worth at most ~1.5pp/yr of drag at 15 bps/side, against a 12.3pp gap in annual return. The date overlap earns return out-of-sample, which is exactly what `learnings.md` already concluded from the other direction ("cost drag was never the main story there either — temporal breadth was") and what the pruning diagnostic showed. So the decomposition question this trial was spent on *is* answered, just not on the axis the gate reads: **date-vintage and length-vintage diversity are complements, not substitutes.** Length diversity alone (this trial, holdout 0.88) is worse than date diversity alone (#35, holdout 1.22); the two together (#42, holdout 1.38) beat both. What the validation window sees instead is a concentrated, fast-rotating book — 35 positions at 7.4x turnover against #42's 63 at 3.1x — being rewarded in a six-year sample whose P&L is dominated by 2019-2020, precisely the standing caution in `learnings.md`. **Three consequences, and the third is a request for human attention.** (1) Tonight's earlier promotions are re-read, not retracted: their validation margins were noise (0.005, 0.008) while their holdout gains were large and monotone (1.22 -> 1.32 -> 1.38), and this trial supplies the contrast case that makes that pattern legible — within this family, validation Sharpe is a poor discriminator and the holdout is doing the real work. (2) The session stops here rather than spending its remaining four trials: the holdout numbers above are now known, so any further candidate designed tonight would be holdout-informed, and the one protection the repo has left would be gone. Stopping is the only way to keep it. (3) **The protocol has just installed as champion a strategy that is materially worse out-of-sample than the one it displaced, and it did so by following `program.md` exactly** — the objective is validation Sharpe, the holdout is evaluated only after the decision is made, and nothing in the gate can see the disagreement. That is not an engine bug and nothing frozen was touched; it is the stated objective working as specified, on a case where the specification does not serve the mission. Flagged for human review in the session summary below. `mom_zscore_overlap6_hzn_avg4` (#42, validation 1.120, holdout 1.38, maxDD -20.1%, turnover 2.8x) is on record should a human wish to reinstate it.


## Session summary — 2026-08-17 (nightly)

- Housekeeping: the session started on a per-run branch (`main-b713x5`) pointing at
  `origin/main` with no commits of its own, so `git checkout main && git reset --hard
  origin/main` corrected it with nothing lost; all of tonight's work is on `main`.
  `git branch -r --no-merged origin/main` clean — no unlanded remote work, so no
  repeat of the 2026-08-16 split-brain. Engine tests green (16 passed). Data store
  fresh through 2026-08-17.
- Experiments run: **3 of the 8-trial budget** (#41 `..._hzn_avg`, #42 `..._hzn_avg4`,
  #43 `..._hzn_avg4_k1`). Verdicts: **3 PROMOTE, 0 REJECT, 0 GATE_FAIL** — the first
  session here to promote at all since the protocol change, and the only one ever to
  promote three times.
- One trial was killed by diagnostic before it was written (holdings only, no returns
  scored, prices truncated at 2023-12-31, no trial count touched): the two horizon
  legs' rank correlation of 0.66 was checked against the 0.89 that killed an earlier
  inter-signal ensemble. It *passed*, which is what licensed #41 — the same diagnostic
  would have killed it for free had it come back near 0.89.

### The finding, and it cuts both ways

**Lookback length is a second axis of vintage diversity, roughly independent of
formation date.** The champion had been collapsing its two lookbacks into a single
score before selecting anything, which throws away the two windows' disagreement about
*which names to hold*. Giving each window its own buffer chain, held-set and
magnitude-weighted target and averaging the resulting *portfolios* at equal weight:

| # | construction | val Sharpe | val maxDD | turnover | positions | holdout Sharpe | holdout maxDD |
|---|---|---|---|---|---|---|---|
| 35 | 1 composite score, 6 date tranches | 1.107 | -29.1% | 3.0x | 34 | 1.22 | -23.3% |
| 41 | 2 horizon portfolios, 6 date tranches | 1.112 | -28.5% | 3.2x | 47 | 1.32 | -22.1% |
| 42 | 4 horizon portfolios, 6 date tranches | 1.120 | -27.8% | 3.1x | 63 | **1.38** | **-20.1%** |
| 43 | 4 horizon portfolios, **no** date tranches | **1.187** | -29.0% | 7.4x | 35 | **0.88** | -27.4% |

Rows 35→41→42 are monotone on every axis, and the axes moving *most* are the ones the
gate does not score. This also retires a supposed law: every previous de-concentration
step cost ~0.02 of Sharpe, but breadth arriving from a decorrelated vintage costs
nothing — the pruning result one axis over. It answers the journal's standing open
question (*what supplies decorrelated formation vintages without being a K sweep*) and
matches `research/SUMMARY.md` candidate #7, which predicted exactly this from the
averaging-over-estimation-windows literature (Pesaran–Timmermann). **Idea provenance:
#41 and #42 came from `research/SUMMARY.md`; #43 was the lab's own decomposition.**

**Row 43 is the warning, and it is the more important half.** Switching the date
overlap off produced the largest validation jump ever recorded here (+0.067, ten times
either promotion above it) and the best DSR on record — and the holdout collapsed from
1.38 to 0.88. Costs do not explain it (turnover 2.8x → 8.0x is worth ~1.5pp/yr at 15
bps against a 12.3pp gap in annual return). So the decomposition *is* answered, off the
gate's axis: **date-vintage and length-vintage diversity are complements, not
substitutes** — length alone (0.88) is worse than date alone (1.22), and the two
together (1.38) beat both. What validation rewarded instead is a concentrated,
fast-rotating book (35 positions at 7.4x against 63 at 3.1x) in a six-year sample whose
P&L is dominated by 2019–2020.

### Why the session stopped at 3 of 8

The holdout numbers above are now known to this session. Any further candidate designed
tonight would be holdout-informed, and the repo's only remaining real check would be
gone. Stopping is the only way to keep it. This is a new stopping rule, distinct from
the "no well-motivated hypothesis left" reason used on 2026-08-07, 08-11, 08-14 and
08-16 — and it is now recorded in `learnings.md` as a rule for session design.

### ⚠ Protocol concern — for human review, no frozen file touched

**The gate promoted a strategy that is materially worse out-of-sample than the one it
displaced, by following `program.md` exactly.** Promotion scores validation Sharpe only;
the holdout is evaluated *after* the decision, so nothing in the gate can see a
validation/holdout disagreement. Two aggravating factors already on record: DSR
clustering removed deflation as a brake on within-family laddering (2026-08-16 protocol
change, its own "honest caveat"), and **every promotion spends one more look at the
holdout — three tonight alone**, which is the fastest this repo has ever consumed it.
This is not an engine bug and no threshold, engine file or trial record was edited; it
is the stated objective working as specified on a case where the specification does not
serve the mission in `program.md` ("beat the current champion out-of-sample"). Recorded
here rather than acted on, per CLAUDE.md. `mom_zscore_overlap6_hzn_avg4` (#42 —
validation 1.120, holdout 1.38, maxDD -20.1%, turnover 2.8x) is the candidate a human
would most plausibly reinstate; its file is intact in `strategies/candidates/`.

### Ideas for next session

1. **Do not open with a challenger.** The live champion (#43) is the weakest holdout
   performer of tonight's four rows, and the strongest one (#42) lost to it on the only
   axis the gate reads. Until a human rules on the protocol concern above, the useful
   work is diagnostic, not competitive.
2. Closed tonight: whether length and date vintage diversity substitute for each other
   (they do not — complements), and whether horizon averaging's gain belongs to the two
   inherited windows (it does not — it is horizon diversity as such).
3. Deliberately *not* attempted, and still open with its own rationale required:
   whether the averaged windows should fill the 3-1..12-1 interval **evenly**. Comparing
   further brackets is the sweep the manual forbids; a principled non-uniform spacing
   argument is not. Both #42's docstring and this entry commit to that boundary.
4. From `research/SUMMARY.md`, still untouched and still free: the closed-form
   weight-vector triage for any proposed trend/MA signal (candidate #3), and the
   noisily-estimated-parameter count as a pre-trial screen on any weighting proposal
   (candidate #1). Both cost no trial.
5. Standing caution, now with a worked example: within this family a *large* validation
   jump is evidence of overfitting, not of progress, until the holdout agrees.
- No engine issues encountered this session.

## Research session — 2026-08-18 (learning agent): 3 notes added, see research/SUMMARY.md
## 2026-08-18T23:10:57+00:00 — mom_zscore_hzn_geom4_k1 — **REJECT**
- Candidate: `strategies/candidates/mom_zscore_hzn_geom4_k1.py` (family: cross-sectional momentum, trial #44)
- Hypothesis: Spacing the four averaged lookback windows geometrically between the same endpoints (252, 159, 100, 63 trading days, adjacent ratios all 4**(1/3)) instead of evenly (252, 189, 126, 63), with bracket endpoints, window count, skip, band, weighting, per-leg buffers, single-tranche formation and daily vol-spike trim otherwise identical to the champion, raises validation Sharpe above the champion's 1.187 net of 15 bps costs, because redundancy between two nested formation windows is governed by the ratio of their lengths rather than their difference — uniform spacing therefore samples the long end of the bracket roughly twice as densely and leaves the legs non-exchangeable (adjacent-pair weight overlap 0.641/0.580/0.469), which is the exact condition under which the equal weights the construction already uses are the wrong ones; landing at or below 1.187 falsifies that and shows interior spacing is not a live variable.
- Verdict: REJECT — validation sharpe 1.166 <= champion 1.187
- Train: sharpe +0.94, ann_ret +18.0%, maxDD -56.0%, turnover 4.7x
- Validation: sharpe +1.17, ann_ret +28.0%, maxDD -29.7%, turnover 7.8x
- Deflated Sharpe prob: 0.9713 (bar from 44 trials, 11 effective)
- Champion validation sharpe at the time: +1.19
- Champion re-deflated at the same bar: 0.9744
- Lesson: **Interior spacing of the averaged lookback windows is not a live variable — the last explicitly-open axis of the horizon-averaging family closes negative, and it closes cleanly because the mechanism was measured before the trial rather than inferred from the Sharpe afterwards.** The pre-trial holdings-only diagnostic (72 validation months, no returns scored, prices truncated at 2023-12-31, trial count untouched) confirmed the argument's premise exactly: geometric spacing all but restores exchangeability between the four legs, with the dispersion of adjacent-pair weight overlap falling **12x, 0.0711 -> 0.0060** (`[0.641, 0.580, 0.469]` -> `[0.557, 0.543, 0.546]`), and it does so *without* changing breadth (union name count 35.1 -> 35.6). That second half matters: it rules out in advance the confound that has explained several previous results here — this could not be a de-concentration effect wearing another name, because there was no de-concentration to have. So the premise was true and the conclusion still did not follow. Validation Sharpe went **1.187 -> 1.166**, with maxDD -29.0% -> -29.7%, turnover 7.4x -> 7.8x and positions 35.1 -> 35.6: every axis moved by less than the repo's own noise floor for this family, and the two that the gate does not score moved in the same (slightly worse) direction as the one it does, so there is no risk/return-dial reading to rescue it. **The substantive finding is that equal weighting across the horizon legs is robust to the legs not being exchangeable.** The theory says equal weights are optimal for a combination when the components have equal variance and equal pairwise correlation; the champion violates the second condition systematically (uniform spacing bunches the length *ratios* at the long end, since two nested formation windows of length L1 < L2 share exactly L1/L2 of their data, so redundancy is a ratio and not a difference); and repairing the violation with a zero-estimated-parameter rule bought nothing. That is a stronger version of the `learnings.md` entry it tests: equal weights between legs are not merely load-bearing against the *estimated*-weight mistake, they are also insensitive to the one deviation from their optimality condition that can be corrected for free. Which in turn says the horizon-averaging gain of trials #41/#42 is coarse — it comes from having several windows at all, not from where inside the bracket they sit — consistent with #42's own finding that the gain is horizon diversity as such rather than a property of the particular windows. **Two disciplines carried forward.** (a) The docstring committed in advance to trying exactly one alternative spacing and no ladder, and that commitment holds: there is no third non-arbitrary rule, and a third spacing would be the sweep the manual forbids. The interval is now pinned at both ends (skip-month, post-formation reversal), at its width (#42), and now in its interior — the bracket is finished. (b) The effect was pre-registered as small on the strength of the diagnostic's *level* reading (mean pairwise overlap moved only -0.011 even as its dispersion collapsed), and it came in small; the diagnostic predicted the magnitude of this trial's outcome correctly and the only thing the trial added was the sign. That is an argument for spending more of these sessions on diagnostics and fewer on trials, not fewer diagnostics.

## 2026-08-18T23:15:13+00:00 — mom_hzn_avg4_k1_cohort_trim — **PROMOTE**
- Candidate: `strategies/candidates/mom_hzn_avg4_k1_cohort_trim.py` (family: regime switching, trial #45)
- Hypothesis: Driving the champion's daily exposure trim from the realized vol of the whole full-history legacy cohort rather than from its accidental intersection with the held basket — four horizon legs, buffers, magnitude weighting, single-tranche formation, SPIKE_RATIO 1.6 and TRIM_SCALE 0.6 otherwise identical to the champion — lands validation Sharpe at or above the champion's 1.187 net of 15 bps costs, because trials #37-#40 attributed the intersection's residual +0.026 on the six-tranche base to sampling luck in which three defensives the momentum screen happened to hold, and champion #43 re-draws that held-set from an entirely different selection process (no date overlap, four independent horizon legs), so a genuinely lucky residual should not survive the re-draw; landing materially below 1.187 falsifies the sampling-luck attribution and shows the membership filter is systematic.
- Verdict: PROMOTE — beats champion (1.201 > 1.187) with DSR 0.9762 (45 trials, 11 effective after clustering at rho 0.95)
- Train: sharpe +0.94, ann_ret +18.2%, maxDD -56.7%, turnover 4.6x
- Validation: sharpe +1.20, ann_ret +28.6%, maxDD -28.7%, turnover 7.9x
- Holdout: sharpe +0.81, ann_ret +20.6%, maxDD -27.4%, turnover 8.0x
- Deflated Sharpe prob: 0.9762 (bar from 45 trials, 11 effective)
- Champion validation sharpe at the time: +1.19
- Champion re-deflated at the same bar: 0.9739
- Lesson: **The sampling-luck attribution in `learnings.md` is now tested rather than asserted, and it holds — a residual that was worth +0.026 on one book is worth -0.014 on a re-drawn one, which is what luck does under re-draw.** Trials #37-#40 found the champion's daily trim was reading `held ∩ full-history-cohort` rather than its own basket, bracketed every deliberate specification (held basket 1.050 < market 1.055 < no trim 1.062 < whole cohort 1.081 < the accident 1.107), credited the monotone ordering in style-orthogonality as the mechanism, and then wrote off the remaining +0.026 as "sampling luck" in which three defensives the momentum screen happened to hold. That clause was an attribution made on one book over one window. Champion #43 re-drew the held-set from a structurally different selection process — date overlap gone, four independent horizon legs, and per tonight's diagnostic a trigger sample of **6.5 names / 20.7% of book weight** against the 3 names / 11% the accident was characterised on — and on that re-draw the ordering **reverses**: the deliberate whole-cohort trigger comes in at 1.201 against the accident's 1.187. A systematic edge does not change sign when the sample is re-drawn; a lucky one does. The clause stands, and the repo now owns a champion whose overlay is *specified* — the equal-weighted realized vol of every instrument with a complete price history to the formation date, a stated style-orthogonal defensive-cohort stress signal — instead of one that was an artifact of a `dropna` filter nobody had read. That epistemic upgrade is the real product of this trial; the Sharpe move is not. **How the +0.014 was earned, and why it is not a return story.** Validation ann_ret actually *fell* 28.75% → 28.59% while ann_vol fell 0.2367 → 0.2319: the deliberate trigger fires on 99 validation days against the accident's 65 (they disagree on 40 of 1412, asymmetrically — the accident is very nearly a strict subset), so the book is de-risked more often and Sharpe rises through the denominator. That is exactly what a working de-risking overlay is supposed to look like, and it is the first time in this repo one has been observed doing it on the specification it claims to use. The pre-trial diagnostic also called the shape of this in advance: the 37 extra de-risking days land almost entirely in 2018 (22), 2020 (8) and 2022 (8) — the window's two loss years and its +132% year — so the two specifications pull opposite ways and the small net margin is the residue of a large offsetting trade, not a uniform improvement. **The part that should worry a reader more than the promotion pleases them.** Holdout fell 0.875 → 0.813 (ann_ret 22.6% → 20.6%, maxDD identical at -27.4%): the extra trimming bought no drawdown out-of-sample and cost return. Set that beside the last two promotions and the sequence is #42 val 1.120 / holdout 1.38 → #43 val 1.187 / holdout 0.875 → #45 val 1.201 / holdout 0.813. **Validation monotone up, holdout monotone down, three promotions running.** Last session raised the protocol concern on a single case; it is now a trend, and the trend is the textbook signature of a gate optimising a statistic that has stopped tracking the objective `program.md` states ("beat the current champion out-of-sample"). Nothing frozen was touched and this is not an engine bug — see the session summary, where it is escalated. **Session discipline applied:** this trial's holdout number is now known to the session, so per the stopping rule recorded in `learnings.md` on 2026-08-17 the session ends here rather than spending its remaining six trials on candidates that would be holdout-informed. **The trim axis is closed either way** — six trials have now been spent on it, the mechanism is identified, the accident is retired, and the two constants (1.6, 0.6) remain inherited and untuned; any further work on it would be knob-turning on a solved question.


## Session summary — 2026-08-18 (nightly)

- Integrity check clean. Session opened on the per-run branch `main-p76jo3` pointing
  at exactly `origin/main` (`a5daec1`) with no commits of its own, and
  `git branch -r --no-merged origin/main` returned nothing — every remote branch
  (`claude/remote-learning-egress-access-33q7fy`, `deflated-sharpe-effective-trials`,
  `main-b713x5`) is an ancestor of `origin/main`, so there is no unlanded work and no
  repeat of the 2026-08-16 split-brain. Engine tests green (16 passed). Data store
  fresh through 2026-08-18.
- Experiments run: **2 of the 8-trial budget** (#44 `mom_zscore_hzn_geom4_k1`,
  #45 `mom_hzn_avg4_k1_cohort_trim`). Verdicts: **1 REJECT, 1 PROMOTE, 0 GATE_FAIL**.
- **Three ideas were resolved without spending a trial**, which is why the budget was
  not exhausted. All were holdings-only diagnostics — weight matrices and trigger
  firing dates, prices truncated at 2023-12-31, no returns scored, trial count
  untouched.

### The two trials

**#44 — interior spacing of the horizon bracket. REJECT, and it closes the axis.**
The one question #42 and the 2026-08-17 summary both left explicitly open was whether
the four averaged windows should fill the 3-1..12-1 interval *evenly*; both committed
that a principled non-uniform argument would be legitimate where another bracket
comparison would not. The argument: two nested formation windows of length L1 < L2
share exactly L1/L2 of their data, so redundancy is a **ratio, not a difference**, and
the uniform 63/126/189/252 bracket has adjacent ratios 2.00/1.50/1.33 — it samples the
long end twice as densely and leaves the legs non-exchangeable, which is exactly when
the equal weights the construction already uses stop being the right ones. Geometric
spacing between the same endpoints (252/159/100/63, all ratios 4^(1/3)) repairs that at
zero estimated parameters.

The pre-trial diagnostic confirmed the premise and, unusually, the effect size:

| | uniform (champion) | geometric |
|---|---|---|
| adjacent-pair weight overlap | 0.641 / 0.580 / 0.469 | 0.557 / 0.543 / 0.546 |
| dispersion of those | 0.0711 | **0.0060** |
| mean pairwise weight overlap | 0.4748 | 0.4639 |
| mean union name count | 35.1 | 35.6 |

Exchangeability essentially restored (12x less dispersion) with breadth untouched — so
this could not be a de-concentration effect wearing another name, the confound that has
explained several earlier results here. The premise was true and the conclusion still
did not follow: validation Sharpe **1.187 → 1.166**, maxDD -29.0% → -29.7%, turnover
7.4x → 7.8x. All inside the family's noise, all in the same slightly-worse direction.
**Finding: equal weighting between horizon legs is robust to the legs not being
exchangeable**, which is a stronger claim than the "equal weights are load-bearing"
entry it tests, and it means the #41/#42 gain is coarse — it comes from having several
windows at all, not from where inside the bracket they sit. The bracket is now pinned at
its ends, its width and its interior. No third spacing will be proposed; there is no
third non-arbitrary rule.

**#45 — re-testing the repo's own "sampling luck" attribution. PROMOTE.**
Trials #37-#40 found the champion's daily trim reads `held ∩ full-history-cohort`
rather than its own basket, credited the cohort's style-orthogonality as the mechanism
(held basket 1.050 < market 1.055 < no trim 1.062 < whole cohort 1.081 < the accident
1.107), and wrote the residual +0.026 off as luck in which three defensives the screen
happened to hold. That was an attribution, never a measurement. Champion #43 re-drew
the held-set from a different selection process, so it could finally be tested — and
this is an out-of-sample test of *a claim the repo had already made*, not another
challenger. Diagnostic first, to avoid the no-op trap that killed the book-weighted-vol
re-specification last session: the two triggers fire on 65 vs 99 validation days and
disagree on **40 of 1412**, asymmetrically (the accident is nearly a strict subset),
with the disagreement concentrated in 2018 (22 days), 2020 (8) and 2022 (8) — the
window's two loss years and its +132% year, pulling opposite ways.

Result: the ordering **reverses** on the re-drawn book — deliberate whole-cohort
**1.201** against the accident's 1.187. A systematic edge does not change sign under
re-draw; a lucky one does. The clause stands, now measured, and the repo's one
surviving overlay is finally **specified** rather than an artifact of a `dropna` filter
nobody had read for ~20 trials. Note how it wins: validation ann_ret *fell* (28.75% →
28.59%) while ann_vol fell more (0.2367 → 0.2319) — Sharpe rose through the
denominator, which is what a de-risking overlay is supposed to do and the first time
one has been seen here doing it on the specification it claims to use. **The trim axis
is closed**: six trials, mechanism identified, accident retired, constants untuned.

### Three trials not spent

1. **Min-shift → fixed weight anchor on the champion's base.** `learnings.md` left this
   open (closed on the six-tranche base only) and the champion is now non-overlapping,
   where the same fix once halved re-sizing turnover. Diagnostic: re-sizing turnover
   -22% (between the -51% on the single-score non-overlapping base and the -10% on the
   six-tranche one, exactly as ~1/N damping predicts for four legs), worth ~0.014
   Sharpe in saved cost — against **-27% HHI at unchanged breadth** (35.1 → 35.1
   positions), which this repo has priced at ~0.02 Sharpe every time the extra flatness
   did not arrive from a decorrelated vintage. Predicted net negative. Not spent.
2. **Risk- or variance-weighting between the horizon legs.** Killed by
   `research/SUMMARY.md` screen #1 (count the noisily-estimated parameters) plus the
   2026-08-18 ERC theorem note: weighting legs by realized vol estimates something, and
   ERC is maximum-Sharpe only under constant correlation *and* equal component Sharpes.
3. **Disjoint rather than nested formation windows** (3-1, 6-4, 9-7, 12-10) as a way to
   force leg decorrelation. This is a signal-definition change, not a construction one,
   and it is the intermediate-horizon echo — which `research/SUMMARY.md` records as not
   surviving outside the US and a low prior on this global universe. Not spent.

### ⚠ Protocol concern — escalated from "a case" to "a trend". For human review.

Last session flagged that the gate cannot see a validation/holdout disagreement. It is
now three promotions running:

| # | validation Sharpe | holdout Sharpe | holdout ann_ret | holdout maxDD |
|---|---|---|---|---|
| 42 | 1.120 | **1.38** | 34.9% | -20.1% |
| 43 | 1.187 | 0.875 | 22.6% | -27.4% |
| 45 | 1.201 | 0.813 | 20.6% | -27.4% |

**Validation monotone up, holdout monotone down.** Each step followed `program.md`
exactly; no frozen file, threshold or trial record was touched, and this is not an
engine bug. It is the signature of a gate optimising a statistic that has stopped
tracking the mission it proxies. Aggravating factors, all on record: DSR clustering
removed deflation as a brake on within-family laddering (11 effective trials against 45
recorded); `main`'s trial count understates the candidates actually attempted; and
**every promotion spends one more look at the holdout — four since 2026-08-17.**
`mom_zscore_overlap6_hzn_avg4` (#42) remains the candidate a human would most plausibly
reinstate; its file is intact. The two levers that would fix this — scoring something
other than raw validation Sharpe, or rationing holdout looks — both live in frozen
files, so this is recorded rather than acted on, per CLAUDE.md.

### Why the session stopped at 2 of 8

The stopping rule recorded in `learnings.md` on 2026-08-17: once a session has seen a
holdout number, every later candidate it designs is holdout-informed. #45's promotion
put three holdout numbers in front of this session, including the trend above. Stopping
is the only way to keep the repo's last real check intact.

### Ideas for next session

1. **Prefer diagnostics to challengers in this family until a human rules on the
   protocol concern.** Tonight is the argument for it: two diagnostics predicted both
   trials' magnitudes correctly and the trials supplied only the sign, while a third
   diagnostic killed an idea outright for free. That is a better yield per unit of
   permanently-raised DSR bar than any challenger has produced since #42.
2. Closed tonight and not to be reopened: interior spacing of the horizon bracket
   (negative), the weight-anchor axis on the non-overlapping base (negative by
   diagnostic), and the trim axis in full (mechanism identified, accident retired).
3. Still open, from `research/SUMMARY.md`, and still free: the closed-form weight-vector
   triage for any proposed trend/MA signal (candidate #3), and the risk-contribution
   vector `x_i · ∂_i σ(x)` as a holdings-only statistic (candidate #21) — the latter
   would answer directly how much of the champion's variance its top name explains,
   which the existing top-weight/HHI statistics only proxy, and it bears on the
   drawdown story the sector/breadth axis failed to explain. **Idea provenance: both
   from `research/SUMMARY.md`; #44 and #45 were the lab's own, following up the
   2026-08-17 session's explicitly-listed open questions.**
4. `research/SUMMARY.md` reports the literature has now closed six directions and
   opened one, with eleven screens against a single live build, and says the marginal
   value of another family survey is low. Read together with point 1, the honest
   position is that this repo's remaining upside is in **methodology and in the
   protocol question above**, not in another candidate.
- No engine issues encountered this session.
