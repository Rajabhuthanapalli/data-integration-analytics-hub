from sqlalchemy import create_engine
import os

def init_db(db_url: str | None = None):
    db_url = db_url or os.getenv("DATABASE_URL", "sqlite:///./diah.db")
    engine = create_engine(db_url, future=True)
    return engine
