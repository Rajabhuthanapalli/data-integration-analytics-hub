import pandas as pd

SUPPORTED = {"USD","EUR","GBP","INR"}

def normalize_currency(orders: pd.DataFrame, fx_rates: dict, base_currency: str="USD") -> pd.DataFrame:
    rates = fx_rates.get("rates", {})
    # If base is USD, amount_usd = amount / rate[currency]? No:
    # API base=USD means rates[currency] = currency per 1 USD.
    # To convert X currency -> USD: USD = amount / rates[currency]
    # For base != USD adjust accordingly later.
    def to_usd(row):
        cur = row["currency"]
        amt = row["amount"]
        if cur == base_currency:
            return float(amt)
        if cur not in SUPPORTED:  # keep simple for Day 1
            return None
        r = rates.get(cur)
        if not r or r == 0:
            return None
        return float(amt) / float(r)
    out = orders.copy()
    out["amount_usd"] = out.apply(to_usd, axis=1)
    out = out.dropna(subset=["amount_usd"])
    out["amount_usd"] = out["amount_usd"].round(2)
    return out

def make_dimensions(df: pd.DataFrame):
    # Very light dims for Day 1
    dim_customer = df[["customer_id","region"]].drop_duplicates().reset_index(drop=True)
    dim_date = df[["order_date"]].drop_duplicates().reset_index(drop=True)
    dim_date["date_key"] = dim_date["order_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date = dim_date[["date_key","order_date"]]
    # Fact
    fact_orders = df.copy()
    fact_orders["date_key"] = fact_orders["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact_orders = fact_orders[["order_id","customer_id","date_key","currency","amount","amount_usd"]]
    return dim_customer, dim_date, fact_orders
