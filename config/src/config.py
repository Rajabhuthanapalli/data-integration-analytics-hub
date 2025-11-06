from pydantic import BaseModel
from pathlib import Path
import yaml

class ValidationConfig(BaseModel):
    required_columns: list[str]
    allowed_currencies: list[str]
    min_amount: float

class SourcesConfig(BaseModel):
    orders_csv: str

class OutputsConfig(BaseModel):
    processed_dir: str
    reports_dir: str

class Settings(BaseModel):
    sources: SourcesConfig
    validation: ValidationConfig
    outputs: OutputsConfig

def get_settings() -> Settings:
    path = Path("config/settings.yaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return Settings(**data)
