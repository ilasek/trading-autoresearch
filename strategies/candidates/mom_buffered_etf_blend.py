"""80/20 capital blend of the buffered-momentum leg with the static
diversified ETF sleeve — stacking two independently-validated improvements.

Two separate, previously-tested mechanisms each improved on some axis of the
plain champion but not simultaneously:
- `mom_12m_buffered` (this session): replacing the champion's hard top-15
  monthly cutoff with an asymmetric buffer band raised validation Sharpe to
  0.90 (vs champion 0.865) *and* cut turnover to 4.4x (vs champion 5.8x) —
  the strongest challenger in the repo's history, rejected only on the DSR
  multiple-testing bar.
- `mom_etf_blend` (prior session): blending the (unbuffered) momentum basket
  80/20 with a static diversified ETF sleeve improved max drawdown on both
  splits (validation -27.8% vs champion -29.9%) at a small Sharpe cost
  (0.85 vs 0.865), because the ETF sleeve is only weakly correlated with
  momentum's crash periods.

Neither mechanism touches the other's failure mode, so this combines them:
swap the plain momentum leg for the buffered one (higher raw Sharpe, lower
turnover) and keep the same 80/20 ETF blend ratio already shown to work. If
the ETF sleeve's drawdown benefit transfers to the buffered leg the way it did
to the plain one, this could combine a Sharpe edge over the champion with a
better drawdown profile than either mom_12m_buffered or mom_etf_blend alone.
"""

import pandas as pd

STRATEGY = {
    "name": "mom_buffered_etf_blend",
    "family": "combinations",
    "hypothesis": (
        "An 80/20 capital blend of the buffered-momentum leg (top-15 core / "
        "top-25 hold band) with the static diversified ETF sleeve improves "
        "the champion's validation Sharpe and drawdown simultaneously, net "
        "of 15 bps costs, by combining the buffered leg's lower turnover and "
        "higher raw Sharpe with the ETF sleeve's drawdown-dampening effect."
    ),
}

LOOKBACK = 252
SKIP = 21
CORE_N = 15
BAND_N = 25
MOM_WEIGHT = 0.8
ETF_SLEEVE = ["SPY", "EFA", "VWO", "VNQ", "DBC", "GLD", "HYG", "TLT", "IEF", "LQD"]
ETF_WEIGHT = 0.2


def generate_weights(prices: pd.DataFrame) -> pd.DataFrame:
    etfs = [c for c in ETF_SLEEVE if c in prices.columns]
    rebalance_dates = prices.groupby(pd.Grouper(freq="ME")).tail(1).index
    rows = {}
    held = set()
    for dt in rebalance_dates:
        hist = prices.loc[:dt]
        if len(hist) < LOOKBACK + SKIP + 1:
            continue
        past = hist.iloc[-(LOOKBACK + SKIP) - 1]
        recent = hist.iloc[-SKIP - 1]
        momentum = (recent / past - 1).dropna()
        if len(momentum) < CORE_N:
            continue

        ranked = momentum.sort_values(ascending=False)
        core = set(ranked.index[:CORE_N])
        band = set(ranked.index[:BAND_N])
        held = (held & band) | core  # both subsets of band, so |held| <= BAND_N

        w = pd.Series(0.0, index=prices.columns)
        w[list(held)] = MOM_WEIGHT / len(held)

        last = hist.iloc[-1]
        avail_etfs = [e for e in etfs if pd.notna(last[e])]
        if avail_etfs:
            per = ETF_WEIGHT / len(avail_etfs)
            for e in avail_etfs:
                w[e] = w.get(e, 0.0) + per
        rows[dt] = w
    return pd.DataFrame.from_dict(rows, orient="index")
