from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class LinkCreate(BaseModel):
    model_config = camel_model_config

    kind_a: str
    id_a: str
    kind_b: str
    id_b: str
    relation: str | None = None


class LinkRead(BaseModel):
    model_config = camel_model_config

    id: str
    kind_a: str
    id_a: str
    kind_b: str
    id_b: str
    relation: str | None = None
    created_at: datetime
