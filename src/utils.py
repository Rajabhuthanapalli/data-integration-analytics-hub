# src/utils.py
import logging
import logging.config
import os
import sqlite3
from contextlib import contextmanager
from time import perf_counter
from typing import Generator, Tuple

LOG_CONFIG_PATH = os.path.join("config", "logging.conf")
DB_PATH = os.path.join("data", "diah.db")


def setup_logging() -> None:
    """Configure logging using logging.conf if available, else basicConfig."""
    if os.path.exists(LOG_CONFIG_PATH):
        logging.config.fileConfig(LOG_CONFIG_PATH, disable_existing_loggers=False)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )


@contextmanager
def timer(operation_name: str) -> Generator[float, None, None]:
    """Context manager to measure execution time."""
    logger = logging.getLogger("timer")
    start = perf_counter()
    logger.info(f"{operation_name} started.")
    try:
        yield
    finally:
        duration = perf_counter() - start
        logger.info(f"{operation_name} completed in {duration:.3f} seconds.")


@contextmanager
def get_db_connection(db_path: str = DB_PATH) -> Generator[sqlite3.Connection, None, None]:
    """Context manager for SQLite connection."""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    finally:
        if conn:
            conn.close()


def ensure_directories() -> None:
    """Create required directories if they don't exist."""
    for folder in ["data", "logs", "reports", "config"]:
        os.makedirs(folder, exist_ok=True)
