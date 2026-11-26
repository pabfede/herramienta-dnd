import os

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.db import Base
from app.models import campaign, encounter, faction, location, npc, system  # noqa: F401 register tables

config = context.config

# URL is injected at runtime: either by the service (config.attributes["url"]),
# by -x url=... on the CLI, or by the DND_DB_URL env var. No URL is hardcoded.
runtime_url = (
    config.attributes.get("url")
    or context.get_x_argument(as_dictionary=True).get("url")
    or os.environ.get("DND_DB_URL")
)
if runtime_url:
    config.set_main_option("sqlalchemy.url", runtime_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
