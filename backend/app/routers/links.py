from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.routers.deps import get_campaign_session
from app.schemas.link import LinkCreate, LinkRead
from app.services import link_service

router = APIRouter(prefix="/api/campaigns/{campaign_id}/links", tags=["links"])


@router.get("", response_model=list[LinkRead])
def list_links(
    entity_kind: str,
    entity_id: str,
    session: Session = Depends(get_campaign_session),
) -> list[LinkRead]:
    return link_service.links_for(session, entity_kind, entity_id)


@router.post("", response_model=LinkRead, status_code=201)
def create_link(data: LinkCreate, session: Session = Depends(get_campaign_session)) -> LinkRead:
    return link_service.create_link(
        session, data.kind_a, data.id_a, data.kind_b, data.id_b, data.relation
    )


@router.delete("/{link_id}", status_code=204)
def delete_link(link_id: str, session: Session = Depends(get_campaign_session)) -> None:
    link_service.delete_link(session, link_id)
