from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class LocationBase(BaseModel):
    model_config = camel_model_config

    name: str
    description: str | None = None
    custom_fields: dict = {}


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    model_config = camel_model_config

    name: str | None = None
    description: str | None = None
    custom_fields: dict | None = None


class LocationRead(LocationBase):
    id: str
    created_at: datetime
    updated_at: datetime
