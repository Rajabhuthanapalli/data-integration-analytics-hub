from src.config import get_settings
from src.ingest_csv import load_orders_csv
from src.ingest_api import fetch_fx_rates
from src.transform import normalize_currency, make_dimensions
from src.load import init_db, upsert_table

def main():
    cfg = get_settings()
    # Extract
    orders = load_orders_csv(cfg.sources.orders_csv)
    fx = fetch_fx_rates(cfg.fx_api.base_url, cfg.fx_api.base_currency)

    # Transform
    orders_norm = normalize_currency(orders, fx, base_currency=cfg.fx_api.base_currency)
    dim_customer, dim_date, fact_orders = make_dimensions(orders_norm)

    # Load
    engine = init_db(cfg.database.url)
    upsert_table(dim_customer, "dim_customer", engine)
    upsert_table(dim_date, "dim_date", engine)
    upsert_table(fact_orders, "fact_orders", engine)
    print("Pipeline run complete. SQLite DB ready at diah.db")

if __name__ == "__main__":
    main()
