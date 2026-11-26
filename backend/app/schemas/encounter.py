from datetime import datetime

from pydantic import BaseModel

from app.schemas._util import camel_model_config


class Combatant(BaseModel):
    model_config = camel_model_config

    name: str
    source_id: str | None = None
    initiative: int | None = None


class EncounterBase(BaseModel):
    model_config = camel_model_config

    name: str
    description: str | None = None
    custom_fields: dict = {}
    combatants: list[Combatant] = []
    notes: str | None = None


class EncounterCreate(EncounterBase):
    pass


class EncounterUpdate(BaseModel):
    model_config = camel_model_config

    name: str | None = None
    description: str | None = None
    custom_fields: dict | None = None
    combatants: list[Combatant] | None = None
    notes: str | None = None


class EncounterRead(EncounterBase):
    id: str
    created_at: datetime
    updated_at: datetime


class EncounterGenerate(BaseModel):
    model_config = camel_model_config

    size: int
    faction: str | None = None
