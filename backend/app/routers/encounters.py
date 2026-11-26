from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.encounter import Encounter
from app.routers.deps import get_campaign_session
from app.schemas.encounter import (
    EncounterCreate,
    EncounterGenerate,
    EncounterRead,
    EncounterUpdate,
)
from app.services import encounter_service, entity_service

router = APIRouter(prefix="/api/campaigns/{campaign_id}/encounters", tags=["encounters"])


@router.get("", response_model=list[EncounterRead])
def list_encounters(session: Session = Depends(get_campaign_session)) -> list[EncounterRead]:
    return entity_service.list_entities(session, Encounter)


@router.post("", response_model=EncounterRead, status_code=201)
def create_encounter(
    data: EncounterCreate, session: Session = Depends(get_campaign_session)
) -> EncounterRead:
    return entity_service.create_entity(session, Encounter, data.model_dump())


@router.post("/generate", response_model=EncounterRead, status_code=201)
def generate_encounter(
    data: EncounterGenerate, session: Session = Depends(get_campaign_session)
) -> EncounterRead:
    combatants = encounter_service.generate_encounter(session, data.size, data.faction)
    return entity_service.create_entity(
        session,
        Encounter,
        {
            "name": "Generated Encounter",
            "description": None,
            "custom_fields": {},
            "combatants": combatants,
            "notes": None,
        },
    )


@router.get("/{encounter_id}", response_model=EncounterRead)
def get_encounter(
    encounter_id: str, session: Session = Depends(get_campaign_session)
) -> EncounterRead:
    return entity_service.get_entity(session, Encounter, encounter_id)


@router.patch("/{encounter_id}", response_model=EncounterRead)
def update_encounter(
    encounter_id: str, data: EncounterUpdate, session: Session = Depends(get_campaign_session)
) -> EncounterRead:
    changes = data.model_dump(exclude_unset=True)
    return entity_service.update_entity(session, Encounter, encounter_id, changes)


@router.delete("/{encounter_id}", status_code=204)
def delete_encounter(encounter_id: str, session: Session = Depends(get_campaign_session)) -> None:
    entity_service.delete_entity(session, Encounter, encounter_id)
