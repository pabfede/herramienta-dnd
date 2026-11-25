from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.db import engine_for, list_campaign_ids
from app.errors import CampaignNotFoundError


def get_campaign_session(campaign_id: str) -> Generator[Session, None, None]:
    if campaign_id not in list_campaign_ids():
        raise CampaignNotFoundError(campaign_id)
    session = sessionmaker(bind=engine_for(campaign_id))()
    try:
        yield session
    finally:
        session.close()
