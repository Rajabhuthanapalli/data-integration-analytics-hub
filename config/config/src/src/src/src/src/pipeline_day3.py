from pathlib import Path
import pandas as pd

from src.config import get_settings
from src.ingest_api import fetch_fx_rates
from src.transform import normalize_currency, make_dimensions
from src.load import init_db, upsert_replace

def _load_input(cfg):
    # Prefer Day-2 cleaned file; fallback to raw if missing.
    clean_path = Path(cfg.outputs.processed_dir) / "orders_clean.csv"
    if clean_path.exists():
        df = pd.read_csv(clean_path, parse_dates=["order_date"])
        source = str(clean_path)
    else:
        raw_path = Path(cfg.sources.orders_csv)
        df = pd.read_csv(raw_path, parse_dates=["order_date"])
        source = str(raw_path)
    return df, source

def main():
    cfg = get_settings()

    # 1) Input
    orders_df, src_used = _load_input(cfg)

    # 2) FX rates
    fx = fetch_fx_rates(cfg.fx_api.base_url, cfg.fx_api.base_currency)

    # 3) Normalize to USD
    orders_norm = normalize_currency(orders_df, fx, base_currency=cfg.fx_api.base_currency)

    # 4) Build dims/fact
    dim_customer, dim_date, fact_orders = make_dimensions(orders_norm)

    # 5) Load to SQLite
    engine = init_db(cfg.database.url)
    upsert_replace(dim_customer, "dim_customer", engine)
    upsert_replace(dim_date, "dim_date", engine)
    upsert_replace(fact_orders, "fact_orders", engine)

    # 6) Console summary
    print("=== Day 3 Load Summary ===")
    print(f"Source file used: {src_used}")
    print(f"FX base: {fx.get('base')}  Date: {fx.get('date')}")
    print(f"dim_customer: {len(dim_customer)} rows")
    print(f"dim_date    : {len(dim_date)} rows")
    print(f"fact_orders : {len(fact_orders)} rows")
    print("SQLite DB at:", cfg.database.url)

if __name__ == "__main__":
    main()
