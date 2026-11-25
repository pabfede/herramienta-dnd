from app.db import Base
from app.models.base import EntityMixin


class Campaign(Base, EntityMixin):
    """Self-describing metadata row stored inside the campaign's own .db file."""

    __tablename__ = "campaign"
