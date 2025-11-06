from __future__ import annotations
import pandas as pd
from typing import Tuple, Dict, Any

def validate_and_clean(
    df: pd.DataFrame,
    required_columns: list[str],
    allowed_currencies: list[str],
    min_amount: float,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Apply simple data quality rules and return (clean_df, report)."""
    report: Dict[str, Any] = {}

    # 1) Required columns
    missing = [c for c in required_columns if c not in df.columns]
    report["missing_columns"] = missing
    if missing:
        # If required columns are missing, nothing else to do
        report["status"] = "failed"
        report["reason"] = f"Missing required columns: {missing}"
        return df.head(0), report

    # 2) Coerce dtypes
    raw_len = len(df)
    # order_date as datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    # amount numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # 3) Drop rows with NA in critical fields
    before_na_drop = len(df)
    df = df.dropna(subset=["order_id", "order_date", "customer_id", "currency", "amount"])
    report["dropped_na_rows"] = before_na_drop - len(df)

    # 4) Deduplicate by order_id + customer_id + order_date (conservative)
    before_dupes = len(df)
    df = df.drop_duplicates(subset=["order_id", "customer_id", "order_date"])
    report["dropped_duplicate_rows"] = before_dupes - len(df)

    # 5) Filter invalid currency
    before_currency = len(df)
    df = df[df["currency"].isin(allowed_currencies)]
    report["dropped_invalid_currency_rows"] = before_currency - len(df)

    # 6) Filter invalid amounts (negative or below threshold)
    before_amount = len(df)
    df = df[df["amount"] >= float(min_amount)]
    report["dropped_invalid_amount_rows"] = before_amount - len(df)

    # 7) Basic summary
    report["raw_row_count"] = raw_len
    report["clean_row_count"] = len(df)
    report["kept_rows_pct"] = round(100.0 * (len(df) / raw_len), 2) if raw_len else 0.0
    report["status"] = "passed"

    return df.reset_index(drop=True), report
