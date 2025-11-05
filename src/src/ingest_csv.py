import pandas as pd
from pathlib import Path

def load_orders_csv(path: str) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path, parse_dates=["order_date"])
    # Basic DQ checks
    df = df.dropna(subset=["order_id", "amount"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    return df
