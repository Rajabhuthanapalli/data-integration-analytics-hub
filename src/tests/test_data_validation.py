import pandas as pd
from src.data_validation import DataValidator

def test_data_validation():
    data = {
        "order_id": [1, 2, 2, 4],
        "amount": [100, 200, -50, 300],
        "currency": ["USD", "USD", None, "EUR"]
    }
    df = pd.DataFrame(data)
    validator = DataValidator(df)
    result = validator.run_all_validations(numeric_cols=["amount"])
    
    assert "currency" in result["null_values"]
    assert result["duplicates"] == 1
    assert "amount" in result["negative_values"]
