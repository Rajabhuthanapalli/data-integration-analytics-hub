from src.config import get_settings
from src.transform import normalize_currency, make_dimensions
from src.ingest_api import fetch_fx_rates
from src.load import init_db, upsert_replace
from src.utils.data_quality import run_basic_suite, save_quality_report
import pandas as pd

def main():
    cfg = get_settings()
    engine = init_db(cfg.database.url)

    df = pd.read_csv(cfg.sources.orders_csv, parse_dates=["order_date"])
    fx = fetch_fx_rates(cfg.fx_api.base_url, cfg.fx_api.base_currency)
    df = normalize_currency(df, fx, base_currency=cfg.fx_api.base_currency)
    _, _, fact_orders = make_dimensions(df)

    # --- Run data validation suite ---
    results = run_basic_suite(fact_orders)
    save_quality_report(results, "data/reports/data_quality.json")

    print("=== Data Quality Validation Summary ===")
    for r in results:
        print(f"{r['expectation']} → {r['status']}")
    if not all(r["status"] == "passed" for r in results):
        raise ValueError("❌ Data quality validation failed, review report.")
    
    # --- Load clean data ---
    upsert_replace(fact_orders, "fact_orders", engine)
    print("✅ Data loaded successfully after validation.")

if __name__ == "__main__":
    main()
