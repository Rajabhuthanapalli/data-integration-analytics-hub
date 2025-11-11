from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

from src.config import get_settings
from src.ingest_api import fetch_fx_rates
from src.transform import normalize_currency, make_dimensions
from src.load import init_db, upsert_replace
from src.utils.incremental import read_watermark, write_watermark, filter_incremental
from src.utils.scd2 import upsert_scd2_customers

def main():
    cfg = get_settings()
    engine = init_db(cfg.database.url)

    # --- 1. Read source CSV ---
    df = pd.read_csv(cfg.sources.orders_csv, parse_dates=["order_date"])
    print(f"Raw rows: {len(df)}")

    # --- 2. Incremental filter ---
    watermark = read_watermark(cfg.load.watermark_file)
    inc_df = filter_incremental(df, cfg.load.watermark_column, watermark)
    if inc_df.empty:
        print("No new data to process.")
        return

    latest_ts = inc_df[cfg.load.watermark_column].max()
    print(f"Processing {len(inc_df)} new rows newer than {watermark}")

    # --- 3. FX normalization ---
    fx = fetch_fx_rates(cfg.fx_api.base_url, cfg.fx_api.base_currency)
    inc_df = normalize_currency(inc_df, fx, base_currency=cfg.fx_api.base_currency)

    # --- 4. Dimension + Fact frames ---
    dim_customer, dim_date, fact_orders = make_dimensions(inc_df)

    # --- 5. Load ---
    upsert_scd2_customers(dim_customer, engine)
    upsert_replace(dim_date, "dim_date", engine)
    upsert_replace(fact_orders, "fact_orders", engine)

    # --- 6. Update watermark ---
    write_watermark(cfg.load.watermark_file, latest_ts)

    print(f"Incremental load complete. Watermark set to {latest_ts}")

if __name__ == "__main__":
    main()
