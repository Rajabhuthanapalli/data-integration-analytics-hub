import pandas as pd
from src.utils.validation import validate_and_clean

def test_validate_and_clean_happy_path():
    df = pd.DataFrame({
        "order_id":[1,2],
        "order_date":["2025-11-01","2025-11-02"],
        "customer_id":["C1","C2"],
        "region":["US","EU"],
        "currency":["USD","EUR"],
        "amount":[100.0, 50.0],
    })
    clean, rpt = validate_and_clean(
        df,
        required_columns=["order_id","order_date","customer_id","region","currency","amount"],
        allowed_currencies=["USD","EUR","GBP","INR"],
        min_amount=0.0,
    )
    assert rpt["status"] == "passed"
    assert rpt["missing_columns"] == []
    assert len(clean) == 2
    assert clean["amount"].min() >= 0

def test_validate_and_clean_filters_bad_rows():
    df = pd.DataFrame({
        "order_id":[1,1,3,4],
        "order_date":["2025-11-01","2025-11-01","2025-11-02","2025-11-03"],
        "customer_id":["C1","C1","C3","C4"],
        "region":["US","US","EU","US"],
        "currency":["USD","USD","ABC","USD"],
        "amount":[100.0,-5.0,10.0,20.0],
    })
    clean, rpt = validate_and_clean(
        df,
        required_columns=["order_id","order_date","customer_id","region","currency","amount"],
        allowed_currencies=["USD","EUR","GBP","INR"],
        min_amount=0.0,
    )
    # drops: duplicate, invalid currency, negative amount
    assert rpt["dropped_duplicate_rows"] >= 1
    assert rpt["dropped_invalid_currency_rows"] >= 1
    assert rpt["dropped_invalid_amount_rows"] >= 1
    assert len(clean) >= 1
