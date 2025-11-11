import pandas as pd
from sqlalchemy import text

def upsert_scd2_customers(new_df: pd.DataFrame, engine):
    """
    Maintain SCD-2 for dim_customer:  columns = [customer_id, region].
    Adds effective_from, effective_to, current_flag.
    """
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id TEXT,
            region TEXT,
            effective_from TEXT,
            effective_to TEXT,
            current_flag INTEGER,
            PRIMARY KEY (customer_id, effective_from)
        );
        """))
        existing = pd.read_sql("SELECT * FROM dim_customer", conn)

        inserts = []
        for _, r in new_df.iterrows():
            cid, reg = r["customer_id"], r["region"]
            match = existing[(existing["customer_id"] == cid) &
                             (existing["current_flag"] == 1)]
            if match.empty:
                inserts.append({
                    "customer_id": cid,
                    "region": reg,
                    "effective_from": pd.Timestamp.utcnow().isoformat(),
                    "effective_to": None,
                    "current_flag": 1
                })
            elif match.iloc[0]["region"] != reg:
                old_row = match.iloc[0]
                conn.execute(text("""
                    UPDATE dim_customer
                       SET effective_to = :now, current_flag = 0
                     WHERE customer_id = :cid AND current_flag = 1
                """), {"now": pd.Timestamp.utcnow().isoformat(), "cid": cid})
                inserts.append({
                    "customer_id": cid,
                    "region": reg,
                    "effective_from": pd.Timestamp.utcnow().isoformat(),
                    "effective_to": None,
                    "current_flag": 1
                })
        if inserts:
            pd.DataFrame(inserts).to_sql("dim_customer", conn, if_exists="append", index=False)
