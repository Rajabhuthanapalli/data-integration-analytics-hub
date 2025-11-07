import pandas as pd

SUPPORTED = {"USD","EUR","GBP","INR"}

def normalize_currency(orders: pd.DataFrame, fx_rates: dict, base_currency: str="USD") -> pd.DataFrame:
    """
    Convert each row's currency to USD using fx_rates.
    If base_currency == USD, rates[currency] = currency per 1 USD.
    So USD = amount / rates[currency] (except USD where rate≈1).
    """
    rates = fx_rates.get("rates", {}) or {}
    out = orders.copy()

    def to_usd(row):
        cur = str(row["currency"]).upper()
        amt = float(row["amount"])
        if cur == base_currency:
            return amt
        if cur not in SUPPORTED:
            return None
        r = rates.get(cur)
        if r is None or r == 0:
            return None
        return amt / float(r)

    out["currency"] = out["currency"].str.upper()
    out["amount_usd"] = out.apply(to_usd, axis=1)
    out = out.dropna(subset=["amount_usd"])
    out["amount_usd"] = out["amount_usd"].round(2)
    return out

def make_dimensions(df: pd.DataFrame):
    # dim_date
    dim_date = df[["order_date"]].drop_duplicates().reset_index(drop=True)
    dim_date["date_key"] = dim_date["order_date"].dt.strftime("%Y%m%d").astype(int)
    dim_date = dim_date[["date_key","order_date"]]

    # dim_customer
    dim_customer = df[["customer_id","region"]].drop_duplicates().reset_index(drop=True)

    # fact_orders
    fact_orders = df.copy()
    fact_orders["date_key"] = fact_orders["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact_orders = fact_orders[[
        "order_id","customer_id","date_key","currency","amount","amount_usd"
    ]]

    return dim_customer, dim_date, fact_orders
