"""lore: session table, link table

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-27

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "session",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("custom_fields", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("session_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
    )

    op.create_table(
        "link",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("kind_a", sa.String(), nullable=False),
        sa.Column("id_a", sa.String(), nullable=False),
        sa.Column("kind_b", sa.String(), nullable=False),
        sa.Column("id_b", sa.String(), nullable=False),
        sa.Column("relation", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("kind_a", "id_a", "kind_b", "id_b", name="uq_link_pair"),
    )


def downgrade() -> None:
    op.drop_table("link")
    op.drop_table("session")
