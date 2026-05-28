from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Dime US Market Coach"
    api_mode: str = "mock"
    market_data_provider: str = os.environ.get("MARKET_DATA_PROVIDER", "mock")
    default_currency: str = "THB"
    assumed_usd_thb: float = 36.5


settings = Settings()
