from fastapi import APIRouter

from app.errors import CampaignNotFoundError
from app.schemas.campaign import CampaignCreate, CampaignRead, CampaignUpdate
from app.services import campaign_service

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])


@router.get("", response_model=list[CampaignRead])
def list_campaigns() -> list[CampaignRead]:
    return campaign_service.list_campaigns()


@router.post("", response_model=CampaignRead, status_code=201)
def create_campaign(data: CampaignCreate) -> CampaignRead:
    return campaign_service.create_campaign(data)


@router.get("/{campaign_id}", response_model=CampaignRead)
def get_campaign(campaign_id: str) -> CampaignRead:
    campaign = campaign_service.get_campaign(campaign_id)
    if campaign is None:
        raise CampaignNotFoundError(campaign_id)
    return campaign


@router.patch("/{campaign_id}", response_model=CampaignRead)
def update_campaign(campaign_id: str, data: CampaignUpdate) -> CampaignRead:
    return campaign_service.update_campaign(campaign_id, data)


@router.delete("/{campaign_id}", status_code=204)
def delete_campaign(campaign_id: str) -> None:
    campaign_service.delete_campaign(campaign_id)
