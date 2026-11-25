from app.db import Base
from app.models.base import EntityMixin


class Npc(Base, EntityMixin):
    __tablename__ = "npc"
