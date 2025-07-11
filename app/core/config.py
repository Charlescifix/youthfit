from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        # This resolves .env relative to the project root
        env_file = str(Path(__file__).resolve().parent.parent.parent / ".env")

settings = Settings()
