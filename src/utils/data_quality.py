import pandas as pd

def expect_non_null(df: pd.DataFrame, columns: list[str]) -> dict:
    res = {c: int(df[c].isna().sum()) for c in columns}
    passed = all(v == 0 for v in res.values())
    return {"expectation": "non_null", "result": res, "status": "passed" if passed else "failed"}

def expect_unique(df: pd.DataFrame, column: str) -> dict:
    dups = df.duplicated(subset=[column]).sum()
    return {"expectation": f"unique_{column}", "duplicates": int(dups), "status": "passed" if dups == 0 else "failed"}

def expect_positive(df: pd.DataFrame, column: str) -> dict:
    neg = (df[column] < 0).sum()
    return {"expectation": f"positive_{column}", "negatives": int(neg), "status": "passed" if neg == 0 else "failed"}

def run_basic_suite(df: pd.DataFrame) -> list[dict]:
    checks = []
    checks.append(expect_non_null(df, ["order_id", "customer_id", "currency", "amount_usd"]))
    checks.append(expect_unique(df, "order_id"))
    checks.append(expect_positive(df, "amount_usd"))
    return checks
