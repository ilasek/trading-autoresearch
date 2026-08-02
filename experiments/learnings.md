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
- **Low-vol stock tilt alone is refuted.** Bottom-quintile trailing-vol stocks (val
  Sharpe 0.69) did not beat momentum and barely improved drawdown; likely needs a
  return/quality overlay to be worth a future trial, not another standalone test.
