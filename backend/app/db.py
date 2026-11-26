from collections.abc import Generator
from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from alembic import command
from app.config import get_settings


class Base(DeclarativeBase):
    pass


_engine_cache: dict[str, Engine] = {}
_ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"


def _run_migrations(path: Path) -> None:
    cfg = Config(str(_ALEMBIC_INI))
    cfg.set_main_option("script_location", str(_ALEMBIC_INI.parent / "alembic"))
    cfg.attributes["url"] = f"sqlite:///{path}"
    command.upgrade(cfg, "head")


def db_path(campaign_id: str):
    return get_settings().data_dir_resolved / f"{campaign_id}.db"


def engine_for(campaign_id: str) -> Engine:
    if campaign_id not in _engine_cache:
        path = db_path(campaign_id)
        # shortcut: migrations run on every first-open-per-process, not just on
        # version bump; cheap no-op when already at head, upgrade if it ever
        # costs real latency on large campaign files.
        _run_migrations(path)
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
