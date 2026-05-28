from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Dime US Market Coach"
    api_mode: str = "mock"
    default_currency: str = "THB"
    assumed_usd_thb: float = 36.5


settings = Settings()
