from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.base import EntityMixin


class Encounter(Base, EntityMixin):
    __tablename__ = "encounter"

    combatants: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
