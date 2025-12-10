from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url = "sqlite + aiosqlite:///./books.db"

settings = Settings()