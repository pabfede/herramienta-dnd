from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class NpcBase(BaseModel):
    model_config = camel_model_config

    name: str
    description: str | None = None
    custom_fields: dict = {}


class NpcCreate(NpcBase):
    pass


class NpcUpdate(BaseModel):
    model_config = camel_model_config

    name: str | None = None
    description: str | None = None
    custom_fields: dict | None = None


class NpcRead(NpcBase):
    id: str
    created_at: datetime
    updated_at: datetime
