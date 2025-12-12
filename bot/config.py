from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./books.db"

settings = Settings()
channels_id = []
