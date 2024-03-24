from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import sys
import os


class Settings(BaseSettings):
    NGROK_TOKEN: str = "_"
    NGROK_URL: str = "_"
    TELEGRAM_TOKEN: str = "_"
    UVICORN_HOST: str = "_"
    UVICORN_PORT: int = 8000
    ADMIN_USER_ID: str = Field(alias="USER_ID")
    HF_TOKEN: str = "_"
    PYTHONPATH: str = "_"
    LOGGER_PATH: str = "_"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: int = -1
    DB_NAME: str = "postgres"
    DB_DEFAULT_NAME: str = "postgres"
    DB_TABLE_NAME: str = '_'

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8",
                                      extra="allow")

    @property
    def url_for_webhook(self):
        return (
            "https://api.telegram.org/"
            f"bot{self.TELEGRAM_TOKEN}/"
            f"setWebhook?url={self.NGROK_URL}/"
        )

    @property
    def url_for_send_message(self):
        return (
            "https://api.telegram.org/"
            f"bot{self.TELEGRAM_TOKEN}/"
            f"sendMessage"
        )

    @property
    def url_for_ngrok(self):
        return (f"{self.NGROK_URL}")

    @property
    def url_for_db(self):
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()

sys.path.insert(0, os.path.abspath(settings.PYTHONPATH))
