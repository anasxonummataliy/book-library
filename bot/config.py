import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class SQLiteConfig:
    DB_PATH: str = field(default_factory=lambda: os.getenv("DB_PATH", "data/books.db"))

    @property
    def db_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.DB_PATH}"


@dataclass
class BotConfig:
    TOKEN: str = field(default_factory=lambda: os.getenv("TOKEN", ""))
    ADMINS: list[int] = field(
        default_factory=lambda: [
            int(a.strip())
            for a in os.getenv("ADMINS", "").split(",")
            if a.strip().isdigit()
        ]
    )

    @property
    def ADMIN(self) -> int:
        """Birinchi (asosiy) adminni qaytaradi"""
        return self.ADMINS[0] if self.ADMINS else 0
    

@dataclass
class Configuration:
    db: SQLiteConfig = field(default_factory=SQLiteConfig)
    bot: BotConfig = field(default_factory=BotConfig)


conf = Configuration()
