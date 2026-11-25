from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class FactionBase(BaseModel):
    model_config = camel_model_config

    name: str
    description: str | None = None
    custom_fields: dict = {}


class FactionCreate(FactionBase):
    pass


class FactionUpdate(BaseModel):
    model_config = camel_model_config

    name: str | None = None
    description: str | None = None
    custom_fields: dict | None = None


class FactionRead(FactionBase):
    id: str
    created_at: datetime
    updated_at: datetime
