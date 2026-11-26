import uuid

from sqlalchemy.orm import sessionmaker

from app.db import clear_engine_cache, db_path, engine_for, list_campaign_ids
from app.errors import CampaignNotFoundError
from app.models.campaign import Campaign
from app.models.system import System
from app.repositories.base import BaseRepository
from app.schemas.campaign import CampaignCreate, CampaignUpdate

_DEFAULT_SYSTEM_NAME = "D&D 5e"


def list_campaigns() -> list[Campaign]:
    campaigns = []
    for campaign_id in list_campaign_ids():
        campaign = get_campaign(campaign_id)
        if campaign is not None:
            campaigns.append(campaign)
    return campaigns


def get_campaign(campaign_id: str) -> Campaign | None:
    if campaign_id not in list_campaign_ids():
        return None
    session = sessionmaker(bind=engine_for(campaign_id))()
    try:
        repo = BaseRepository(session, Campaign)
        rows = repo.list()
        return rows[0] if rows else None
    finally:
        session.close()


def create_campaign(data: CampaignCreate) -> Campaign:
    campaign_id = str(uuid.uuid4())
    path = db_path(campaign_id)
    try:
        session = sessionmaker(bind=engine_for(campaign_id))()
        try:
            campaign = Campaign(
                id=campaign_id,
                name=data.name,
                description=data.description,
                custom_fields=data.custom_fields,
            )
            session.add(campaign)
            session.add(System(name=_DEFAULT_SYSTEM_NAME, config={}))
            session.commit()
            session.refresh(campaign)
            return campaign
        finally:
            session.close()
    except Exception:
        clear_engine_cache(campaign_id)
        if path.exists():
            path.unlink()
        raise


def update_campaign(campaign_id: str, data: CampaignUpdate) -> Campaign:
    if campaign_id not in list_campaign_ids():
        raise CampaignNotFoundError(campaign_id)
    session = sessionmaker(bind=engine_for(campaign_id))()
    try:
        repo = BaseRepository(session, Campaign)
        rows = repo.list()
        if not rows:
            raise CampaignNotFoundError(campaign_id)
        changes = data.model_dump(exclude_unset=True)
        return repo.update(rows[0], changes)
    finally:
        session.close()


def delete_campaign(campaign_id: str) -> None:
    if campaign_id not in list_campaign_ids():
        raise CampaignNotFoundError(campaign_id)
    clear_engine_cache(campaign_id)
    path = db_path(campaign_id)
    if path.exists():
        path.unlink()


def require_campaign(campaign_id: str) -> None:
    if campaign_id not in list_campaign_ids():
        raise CampaignNotFoundError(campaign_id)
