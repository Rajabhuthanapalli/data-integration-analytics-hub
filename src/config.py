from pydantic import BaseModel
from dotenv import load_dotenv
import yaml
from pathlib import Path

load_dotenv()

class DBConfig(BaseModel):
    url: str

class SourcesConfig(BaseModel):
    orders_csv: str

class FXConfig(BaseModel):
    base_url: str
    base_currency: str

class Settings(BaseModel):
    database: DBConfig
    sources: SourcesConfig
    fx_api: FXConfig

def get_settings() -> Settings:
    cfg_path = Path("config/settings.yaml")
    with cfg_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Settings(**raw)
