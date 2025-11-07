from sqlalchemy import create_engine, text

def init_db(db_url: str):
    engine = create_engine(db_url, future=True)
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id TEXT PRIMARY KEY,
            region TEXT
        );
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_key INTEGER PRIMARY KEY,
            order_date TEXT
        );
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fact_orders (
            order_id INTEGER PRIMARY KEY,
            customer_id TEXT,
            date_key INTEGER,
            currency TEXT,
            amount REAL,
            amount_usd REAL,
            FOREIGN KEY(customer_id) REFERENCES dim_customer(customer_id),
            FOREIGN KEY(date_key) REFERENCES dim_date(date_key)
        );
        """))
    return engine

def upsert_replace(df, table_name: str, engine):
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
