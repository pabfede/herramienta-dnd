from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.npc import Npc
from app.routers.deps import get_campaign_session
from app.schemas.npc import NpcCreate, NpcRead, NpcUpdate
from app.services import entity_service

router = APIRouter(prefix="/api/campaigns/{campaign_id}/npcs", tags=["npcs"])


@router.get("", response_model=list[NpcRead])
def list_npcs(session: Session = Depends(get_campaign_session)) -> list[NpcRead]:
    return entity_service.list_entities(session, Npc)


@router.post("", response_model=NpcRead, status_code=201)
def create_npc(data: NpcCreate, session: Session = Depends(get_campaign_session)) -> NpcRead:
    return entity_service.create_entity(session, Npc, data.model_dump())


@router.get("/{npc_id}", response_model=NpcRead)
def get_npc(npc_id: str, session: Session = Depends(get_campaign_session)) -> NpcRead:
    return entity_service.get_entity(session, Npc, npc_id)


@router.patch("/{npc_id}", response_model=NpcRead)
def update_npc(
    npc_id: str, data: NpcUpdate, session: Session = Depends(get_campaign_session)
) -> NpcRead:
    changes = data.model_dump(exclude_unset=True)
    return entity_service.update_entity(session, Npc, npc_id, changes)


@router.delete("/{npc_id}", status_code=204)
def delete_npc(npc_id: str, session: Session = Depends(get_campaign_session)) -> None:
    entity_service.delete_entity(session, Npc, npc_id)
