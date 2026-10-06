"""Holdings-only diagnostic for the re-scoring correction: share of each book's
validation-window stock weight that sits on the 98 legacy (today's-survivor)
stocks, under the re-scoring's masked view (V2m). Reads prices to 2023-12-31
only; scores no returns; records nothing."""
import json, sys, time
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engine import data, protocol

names = sys.argv[1:]
out_path = Path(__file__).with_name("legacy_share.jsonl")
prices = data.load_prices(universe="pit", start=protocol.PIT_PRICE_START)
aux = data.load_panels(universe="pit", start=protocol.PIT_PRICE_START)
setup = protocol.setup_v2(prices, aux)
setup.mask_strategy_view = True
visible, elig = protocol.visible_frame(prices, "2023-12-31", setup)
legacy = {i for i, t in data.instrument_types("legacy").items() if t == "stock"}
types = setup.types
stocks = [c for c in visible.columns if types.get(c) == "stock"]
val_elig = elig.loc["2018-01-01":"2023-12-31", stocks]
base = float((val_elig[[c for c in stocks if c in legacy]].sum(axis=1) / val_elig.sum(axis=1)).mean())
print("base rate: legacy share of eligible stocks over validation", round(base, 4), flush=True)
for name in names:
    t0 = time.time()
    path = Path(name) if name.endswith(".py") else protocol.ROOT / "strategies" / "candidates" / f"{name}.py"
    mod, _ = protocol.load_strategy(path.resolve())
    try:
        w = protocol.call_strategy(*protocol._strategy_view(mod.generate_weights, visible, aux, elig, setup))
    except Exception as e:  # record and move on; one candidate must not stop the sweep
        rec = {"name": name, "error": f"{type(e).__name__}: {e}"[:200]}
        print(json.dumps(rec), flush=True)
        with open(out_path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        continue
    w = w.sort_index()
    w = w[~w.index.duplicated(keep="last")]
    w = w.reindex(columns=visible.columns).fillna(0.0).abs()
    w = w.loc["2018-01-01":"2023-12-31"]
    ok = elig.reindex(index=w.index).fillna(False).astype(bool)
    w = w.where(ok, 0.0)                                 # what the engine would keep
    sw = w[stocks]
    tot = sw.sum(axis=1)
    rows = tot > 1e-9
    share = float((sw[[c for c in stocks if c in legacy]].sum(axis=1)[rows] / tot[rows]).mean()) if rows.any() else None
    stock_w = float((tot / w.sum(axis=1).replace(0, float("nan"))).mean())
    rec = {"name": name, "legacy_share_of_stock_weight": None if share is None else round(share, 4),
           "stock_share_of_book": round(stock_w, 4), "base_rate": round(base, 4),
           "secs": round(time.time() - t0, 1)}
    print(json.dumps(rec), flush=True)
    with open(out_path, "a") as f:
        f.write(json.dumps(rec) + "\n")
