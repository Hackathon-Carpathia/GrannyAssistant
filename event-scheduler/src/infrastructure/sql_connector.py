from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine
import os
Base = declarative_base()

@dataclass
class DatabaseConnector:
    db_url: str = os.getenv('DB_URL', "sqlite+aiosqlite:///./test.db")
    _engine: AsyncEngine = field(init=False, repr=False)
    _session_factory: async_sessionmaker = field(init=False, repr=False)
    _base = Base

    def __post_init__(self):
        self._engine = create_async_engine(
            self.db_url,
            echo=True,
            future=True,
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def get_session(self) -> AsyncSession:
        return self._session_factory()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(self._base.metadata.create_all)
