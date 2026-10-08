"""Transaction-cost model for protocol v3.

Protocol v1/v2 charged one flat 15 bps per side on every instrument in every
market. That understates the cost of exactly the books a wide global panel
invites: names chosen *for* low liquidity, and markets that tax every purchase.
v3 prices a trade as

    per side:  liquidity tier (commission + half-spread + small-order impact)
               x `multiplier` (the cost-stress knob; 1.0 in the scored run)
    plus:      the listing market's transaction tax, on the side it is levied

Liquidity is the trailing 63-day median USD traded value (`membership.trailing_adv`),
computed from data at or before the fill date. The tiers keep v1/v2's 15 bps
as the floor for the most liquid names, so no trade became cheaper.

Taxes are the statutory rates levied on the buyer (or both sides) by the issuer's
market, applied by listing region. Known simplifications, accepted on purpose:
- region stands in for country of incorporation (a few FTSE 100 members are
  Jersey/Irish-incorporated and pay no UK stamp duty; they are charged it here);
- the FR/ES/IT taxes apply only above a market-capitalisation threshold, which
  every index member in this universe clears;
- Swiss and Belgian levies are charged by domestic intermediaries only and are
  left out, as are exchange/clearing fees (inside the commission tier).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# (min trailing median USD ADV, bps per side). First match wins.
LIQUIDITY_TIERS = ((100e6, 15.0), (25e6, 20.0), (5e6, 30.0), (0.0, 40.0))
# No usable volume history yet (new listing, or a line without volume data).
UNKNOWN_ADV_BPS = 30.0
# The flat legacy rate, used when no liquidity panel is available.
LEGACY_FLAT_BPS = 15.0

# Transaction taxes by listing region: (start, end, buy_bps, sell_bps), inclusive
# dates, None = open. Sources: HMRC SDRT (0.5% since 1986); HK IRD stamp duty
# (0.1% per side from 2001-09-01, 0.13% 2021-08-01..2023-11-16, 0.1% after);
# French TTF (0.2% from 2012-08-01, 0.3% from 2017-01-01, 0.4% from 2025-04-01);
# Italian FTT on regulated markets (0.12% in 2013, 0.1% from 2014); Spanish ITF
# (0.2% from 2021-01-16).
TRANSACTION_TAXES: dict[str, list[tuple[str | None, str | None, float, float]]] = {
    "UK": [(None, None, 50.0, 0.0)],
    "HK": [(None, "2021-07-31", 10.0, 10.0),
           ("2021-08-01", "2023-11-16", 13.0, 13.0),
           ("2023-11-17", None, 10.0, 10.0)],
    "FR": [("2012-08-01", "2016-12-31", 20.0, 0.0),
           ("2017-01-01", "2025-03-31", 30.0, 0.0),
           ("2025-04-01", None, 40.0, 0.0)],
    "IT": [("2013-03-01", "2013-12-31", 12.0, 0.0),
           ("2014-01-01", None, 10.0, 0.0)],
    "ES": [("2021-01-16", None, 20.0, 0.0)],
}


def liquidity_bps(adv: np.ndarray) -> np.ndarray:
    """Per-side bps for an array of trailing ADVs (NaN = unknown)."""
    adv = np.asarray(adv, dtype=float)
    out = np.full(adv.shape, UNKNOWN_ADV_BPS)
    known = np.isfinite(adv)
    assigned = np.zeros(adv.shape, dtype=bool)
    for floor, bps in LIQUIDITY_TIERS:
        hit = known & ~assigned & (adv >= floor)
        out[hit] = bps
        assigned |= hit
    return out


def tax_tables(index: pd.DatetimeIndex) -> tuple[list[str], np.ndarray, np.ndarray]:
    """(regions, buy, sell): buy/sell are len(index) x (len(regions) + 1) bps
    arrays; the last column is the untaxed default."""
    regions = sorted(TRANSACTION_TAXES)
    buy = np.zeros((len(index), len(regions) + 1))
    sell = np.zeros_like(buy)
    dates = index.values
    for j, reg in enumerate(regions):
        for start, end, b, s in TRANSACTION_TAXES[reg]:
            lo = 0 if start is None else np.searchsorted(dates, np.datetime64(start), "left")
            hi = len(dates) if end is None else np.searchsorted(dates, np.datetime64(end), "right")
            buy[lo:hi, j] = b
            sell[lo:hi, j] = s
    return regions, buy, sell


@dataclass
class CostModel:
    """What a fill costs. `adv` None means no liquidity data: every name is
    charged `flat_bps` (the v1/v2 rate unless overridden)."""
    adv: pd.DataFrame | None = None          # dates x columns, trailing median USD ADV
    regions: dict[str, str] = field(default_factory=dict)
    multiplier: float = 1.0                  # stress: scales the liquidity tier, not taxes
    flat_bps: float = LEGACY_FLAT_BPS
    taxes: bool = True

    def stressed(self, multiplier: float) -> "CostModel":
        return CostModel(adv=self.adv, regions=self.regions, multiplier=multiplier,
                         flat_bps=self.flat_bps, taxes=self.taxes)

    def prepare(self, index: pd.DatetimeIndex, columns: pd.Index) -> "PreparedCosts":
        """Arrays aligned to one simulation's rows and (active) columns."""
        if self.adv is not None:
            adv = self.adv.reindex(index=index, columns=columns).to_numpy(dtype=float)
        else:
            adv = None
        regions, buy, sell = tax_tables(index)
        code = {r: i for i, r in enumerate(regions)}
        default = len(regions)
        cols = np.array([code.get(self.regions.get(c, ""), default) for c in columns], dtype=int)
        if not self.taxes:
            buy = np.zeros_like(buy)
            sell = np.zeros_like(sell)
        return PreparedCosts(adv=adv, region_code=cols, buy=buy, sell=sell,
                             multiplier=self.multiplier, flat_bps=self.flat_bps)


@dataclass
class PreparedCosts:
    adv: np.ndarray | None
    region_code: np.ndarray
    buy: np.ndarray
    sell: np.ndarray
    multiplier: float
    flat_bps: float

    def trade_cost(self, row: int, cols: np.ndarray, delta: np.ndarray) -> float:
        """Cost, as a fraction of NAV, of changing weights by `delta` on `cols`
        at simulation row `row`."""
        if self.adv is None:
            side = np.full(len(cols), self.flat_bps)
        else:
            side = liquidity_bps(self.adv[row, cols])
        side = side * self.multiplier
        codes = self.region_code[cols]
        buy_tax = self.buy[row, codes]
        sell_tax = self.sell[row, codes]
        bought = np.clip(delta, 0.0, None)
        sold = np.clip(-delta, 0.0, None)
        bps = (np.abs(delta) * side).sum() + (bought * buy_tax).sum() + (sold * sell_tax).sum()
        return float(bps) / 1e4
