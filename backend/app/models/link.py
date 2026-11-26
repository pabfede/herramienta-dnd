import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import _utcnow


class Link(Base):
    __tablename__ = "link"
    __table_args__ = (
        UniqueConstraint("kind_a", "id_a", "kind_b", "id_b", name="uq_link_pair"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kind_a: Mapped[str] = mapped_column(String, nullable=False)
    id_a: Mapped[str] = mapped_column(String, nullable=False)
    kind_b: Mapped[str] = mapped_column(String, nullable=False)
    id_b: Mapped[str] = mapped_column(String, nullable=False)
    relation: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
