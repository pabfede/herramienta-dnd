from pydantic import BaseModel

from app.schemas._util import camel_model_config


class SystemRead(BaseModel):
    model_config = camel_model_config

    id: str
    name: str
    config: dict
