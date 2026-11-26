from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DbSession

from app.models.session import Session as SessionModel
from app.routers.deps import get_campaign_session
from app.schemas.session import SessionCreate, SessionRead, SessionUpdate
from app.services import entity_service

router = APIRouter(prefix="/api/campaigns/{campaign_id}/sessions", tags=["sessions"])


@router.get("", response_model=list[SessionRead])
def list_sessions(session: DbSession = Depends(get_campaign_session)) -> list[SessionRead]:
    return entity_service.list_entities(session, SessionModel)


@router.post("", response_model=SessionRead, status_code=201)
def create_session(
    data: SessionCreate, session: DbSession = Depends(get_campaign_session)
) -> SessionRead:
    return entity_service.create_entity(session, SessionModel, data.model_dump())


@router.get("/{session_id}", response_model=SessionRead)
def get_session(
    session_id: str, session: DbSession = Depends(get_campaign_session)
) -> SessionRead:
    return entity_service.get_entity(session, SessionModel, session_id)


@router.patch("/{session_id}", response_model=SessionRead)
def update_session(
    session_id: str, data: SessionUpdate, session: DbSession = Depends(get_campaign_session)
) -> SessionRead:
    changes = data.model_dump(exclude_unset=True)
    return entity_service.update_entity(session, SessionModel, session_id, changes)


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: str, session: DbSession = Depends(get_campaign_session)) -> None:
    entity_service.delete_entity(session, SessionModel, session_id)
