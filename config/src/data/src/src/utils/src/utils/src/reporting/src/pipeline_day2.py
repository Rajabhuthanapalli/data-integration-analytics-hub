from pathlib import Path
import pandas as pd
from src.config import get_settings
from src.ingest_csv import read_orders_csv
from src.utils.validation import validate_and_clean
from src.reporting.quick_profile import write_profile_md

def main():
    cfg = get_settings()

    # 1) Read
    raw_df = read_orders_csv(cfg.sources.orders_csv)

    # 2) Validate / Clean
    clean_df, dq = validate_and_clean(
        raw_df,
        required_columns=cfg.validation.required_columns,
        allowed_currencies=cfg.validation.allowed_currencies,
        min_amount=cfg.validation.min_amount,
    )

    # 3) Output folders
    processed_dir = Path(cfg.outputs.processed_dir)
    reports_dir = Path(cfg.outputs.reports_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 4) Save cleaned dataset
    clean_csv = processed_dir / "orders_clean.csv"
    clean_df.to_csv(clean_csv, index=False)

    # 5) Write small markdown profile
    profile_path = reports_dir / "orders_profile.md"
    write_profile_md(clean_df, str(profile_path), title="Orders (Clean) Profile")

    # 6) Console summary (for CI/logs)
    print("=== Day 2 Ingestion Report ===")
    for k, v in dq.items():
        print(f"{k}: {v}")
    print(f"\nSaved cleaned data -> {clean_csv.resolve()}")
    print(f"Saved profile      -> {profile_path.resolve()}")

if __name__ == "__main__":
    main()
