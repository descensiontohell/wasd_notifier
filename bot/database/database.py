from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from bot.config import config


class Database:
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.new_session: Optional[sessionmaker] = None
        self.connect()

    def connect(self):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{config.user}:{config.password}@{config.host}/{config.database}"
        )
        self.new_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)


db = Database()
