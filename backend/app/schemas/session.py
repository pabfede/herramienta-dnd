from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class SessionBase(BaseModel):
    model_config = camel_model_config

    name: str
    description: str | None = None
    custom_fields: dict = {}
    session_date: datetime | None = None
    notes: str | None = None


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    model_config = camel_model_config

    name: str | None = None
    description: str | None = None
    custom_fields: dict | None = None
    session_date: datetime | None = None
    notes: str | None = None


class SessionRead(SessionBase):
    id: str
    created_at: datetime
    updated_at: datetime
