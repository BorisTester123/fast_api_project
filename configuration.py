from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_HOST: str = "Используйте свои данные для подключения"
    DB_PORT: int = "Используйте свои данные для подключения"
    DB_USER: str = "Используйте свои данные для подключения"
    DB_PASS: str = "Используйте свои данные для подключения"
    DB_NAME: str = "Используйте свои данные для подключения"

    @property
    def database_url_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
