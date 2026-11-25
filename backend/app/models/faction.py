from app.db import Base
from app.models.base import EntityMixin


class Faction(Base, EntityMixin):
    __tablename__ = "faction"
