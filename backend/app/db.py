from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


_engine_cache: dict[str, Engine] = {}


def db_path(campaign_id: str):
    return get_settings().data_dir_resolved / f"{campaign_id}.db"


def engine_for(campaign_id: str) -> Engine:
    if campaign_id not in _engine_cache:
        path = db_path(campaign_id)
        _engine_cache[campaign_id] = create_engine(
            f"sqlite:///{path}", connect_args={"check_same_thread": False}
        )
    return _engine_cache[campaign_id]


def clear_engine_cache(campaign_id: str) -> None:
    """Dispose and evict a cached engine before deleting the .db file (Windows locks it)."""
    engine = _engine_cache.pop(campaign_id, None)
    if engine is not None:
        engine.dispose()


def list_campaign_ids() -> list[str]:
    data_dir = get_settings().data_dir_resolved
    return sorted(p.stem for p in data_dir.glob("*.db"))


def session_for(campaign_id: str) -> Generator[Session, None, None]:
    engine = engine_for(campaign_id)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
