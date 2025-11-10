import pandas as pd
from src.transform import normalize_currency

def test_normalize_currency_math_usd_base():
    orders = pd.DataFrame({
        "order_id":[1,2,3],
        "order_date": pd.to_datetime(["2025-11-01","2025-11-01","2025-11-02"]),
        "customer_id":["C1","C2","C3"],
        "region":["US","EU","UK"],
        "currency":["USD","EUR","GBP"],
        "amount":[100.0, 100.0, 100.0],
    })
    # base=USD → rates mean CURRENCY per 1 USD
    fx = {"base":"USD","date":"2025-11-01","rates":{"USD":1.0,"EUR":0.8,"GBP":0.5}}
    # USD value = amount / rate[currency] (except USD itself)
    out = normalize_currency(orders, fx, base_currency="USD")
    # USD row unchanged
    assert float(out.loc[out["currency"]=="USD", "amount_usd"].iloc[0]) == 100.0
    # EUR 100 at rate 0.8 → 100/0.8 = 125 USD
    assert round(float(out.loc[out["currency"]=="EUR","amount_usd"].iloc[0]),2) == 125.00
    # GBP 100 at rate 0.5 → 100/0.5 = 200 USD
    assert round(float(out.loc[out["currency"]=="GBP","amount_usd"].iloc[0]),2) == 200.00
