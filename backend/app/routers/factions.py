from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.faction import Faction
from app.routers.deps import get_campaign_session
from app.schemas.faction import FactionCreate, FactionRead, FactionUpdate
from app.services import entity_service

router = APIRouter(prefix="/api/campaigns/{campaign_id}/factions", tags=["factions"])


@router.get("", response_model=list[FactionRead])
def list_factions(session: Session = Depends(get_campaign_session)) -> list[FactionRead]:
    return entity_service.list_entities(session, Faction)


@router.post("", response_model=FactionRead, status_code=201)
def create_faction(
    data: FactionCreate, session: Session = Depends(get_campaign_session)
) -> FactionRead:
    return entity_service.create_entity(session, Faction, data.model_dump())


@router.get("/{faction_id}", response_model=FactionRead)
def get_faction(faction_id: str, session: Session = Depends(get_campaign_session)) -> FactionRead:
    return entity_service.get_entity(session, Faction, faction_id)


@router.patch("/{faction_id}", response_model=FactionRead)
def update_faction(
    faction_id: str, data: FactionUpdate, session: Session = Depends(get_campaign_session)
) -> FactionRead:
    changes = data.model_dump(exclude_unset=True)
    return entity_service.update_entity(session, Faction, faction_id, changes)


@router.delete("/{faction_id}", status_code=204)
def delete_faction(faction_id: str, session: Session = Depends(get_campaign_session)) -> None:
    entity_service.delete_entity(session, Faction, faction_id)
