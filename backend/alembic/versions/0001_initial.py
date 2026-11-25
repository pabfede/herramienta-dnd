"""initial schema: campaign, npc, location, faction, system

Revision ID: 0001
Revises:
Create Date: 2026-11-25

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _entity_columns() -> list[sa.Column]:
    return [
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("custom_fields", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    ]


def upgrade() -> None:
    op.create_table("campaign", *_entity_columns())
    op.create_table("npc", *_entity_columns())
    op.create_table("location", *_entity_columns())
    op.create_table("faction", *_entity_columns())
    op.create_table(
        "system",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("system")
    op.drop_table("faction")
    op.drop_table("location")
    op.drop_table("npc")
    op.drop_table("campaign")
