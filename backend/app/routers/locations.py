from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.location import Location
from app.routers.deps import get_campaign_session
from app.schemas.location import LocationCreate, LocationRead, LocationUpdate
from app.services import entity_service

router = APIRouter(prefix="/api/campaigns/{campaign_id}/locations", tags=["locations"])


@router.get("", response_model=list[LocationRead])
def list_locations(session: Session = Depends(get_campaign_session)) -> list[LocationRead]:
    return entity_service.list_entities(session, Location)


@router.post("", response_model=LocationRead, status_code=201)
def create_location(
    data: LocationCreate, session: Session = Depends(get_campaign_session)
) -> LocationRead:
    return entity_service.create_entity(session, Location, data.model_dump())


@router.get("/{location_id}", response_model=LocationRead)
def get_location(
    location_id: str, session: Session = Depends(get_campaign_session)
) -> LocationRead:
    return entity_service.get_entity(session, Location, location_id)


@router.patch("/{location_id}", response_model=LocationRead)
def update_location(
    location_id: str, data: LocationUpdate, session: Session = Depends(get_campaign_session)
) -> LocationRead:
    changes = data.model_dump(exclude_unset=True)
    return entity_service.update_entity(session, Location, location_id, changes)


@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: str, session: Session = Depends(get_campaign_session)) -> None:
    entity_service.delete_entity(session, Location, location_id)
