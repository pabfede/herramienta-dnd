from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class CampaignBase(BaseModel):
    model_config = camel_model_config

    name: str
    description: str | None = None
    custom_fields: dict = {}


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(BaseModel):
    model_config = camel_model_config

    name: str | None = None
    description: str | None = None
    custom_fields: dict | None = None


class CampaignRead(CampaignBase):
    id: str
    created_at: datetime
    updated_at: datetime
