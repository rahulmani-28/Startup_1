from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    mongodb_uri: str = Field(alias="MONGODB_URI")
    database_name: str = Field(alias="DATABASE_NAME", default="travel_buddy")
    app_name: str = Field(alias="APP_NAME", default="Travel Buddy (Chariot Testing) Backend")
    cors_origins: str = Field(alias="CORS_ORIGINS", default="*")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()  # type: ignore[arg-type]


