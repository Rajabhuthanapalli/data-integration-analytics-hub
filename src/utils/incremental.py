from pathlib import Path
import pandas as pd
from datetime import datetime

def read_watermark(path: str) -> datetime | None:
    p = Path(path)
    if not p.exists():
        return None
    txt = p.read_text().strip()
    try:
        return datetime.fromisoformat(txt)
    except Exception:
        return None

def write_watermark(path: str, value: datetime):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(value.isoformat())

def filter_incremental(df: pd.DataFrame, column: str, last_value: datetime | None):
    if last_value is None:
        return df
    mask = df[column] > last_value
    return df.loc[mask].copy()
