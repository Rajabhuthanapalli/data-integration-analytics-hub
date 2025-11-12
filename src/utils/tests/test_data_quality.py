import pandas as pd
from src.utils.data_quality import run_basic_suite

def test_run_basic_suite_detects_issues():
    df = pd.DataFrame({
        "order_id": [1, 1, 3],
        "customer_id": ["A", None, "C"],
        "currency": ["USD", "USD", "USD"],
        "amount_usd": [100, -5, 50]
    })
    results = run_basic_suite(df)
    assert any(r["status"] == "failed" for r in results)

def test_run_basic_suite_passes_clean_data():
    df = pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": ["A", "B", "C"],
        "currency": ["USD", "USD", "USD"],
        "amount_usd": [100, 200, 300]
    })
    results = run_basic_suite(df)
    assert all(r["status"] == "passed" for r in results)
