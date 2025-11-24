# src/etl_ingestion.py
import logging
import pandas as pd
from typing import Optional

from src.utils import timer

logger = logging.getLogger(__name__)


def ingest_csv(source_path: str) -> Optional[pandas.DataFrame]:
    """
    Ingest raw CSV data.

    Returns:
        DataFrame if successful, else None.
    """
    with timer(f"Ingestion from {source_path}"):
        try:
            df = pd.read_csv(source_path)
            logger.info(f"Ingested {len(df)} rows from {source_path}.")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {source_path}")
        except Exception as exc:
            logger.exception(f"Unexpected error during ingestion: {exc}")
    return None
