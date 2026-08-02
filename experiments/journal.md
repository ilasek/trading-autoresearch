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

