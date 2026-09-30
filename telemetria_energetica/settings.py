from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./telemetria.db"

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
