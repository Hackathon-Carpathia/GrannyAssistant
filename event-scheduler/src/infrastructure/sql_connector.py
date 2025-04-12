from dataclasses import dataclass, field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


Base = declarative_base()

@dataclass
class DatabaseConnector:
    db_url: str = "sqlite:///./car_ratings.db"
    _engine: any = field(init=False, repr=False)
    _session_factory: any = field(init=False, repr=False)
    _base = Base

    def __post_init__(self):
        self._engine = create_engine(
            self.db_url,
            connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {}
        )
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

    def get_session(self) -> Session:
        return self._session_factory()

    def create_all(self):
        self._base.metadata.create_all(bind=self._engine)