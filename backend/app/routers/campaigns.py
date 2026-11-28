from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

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


@router.get("/{campaign_id}/export")
def export_campaign(campaign_id: str):
    path = campaign_service.export_campaign(campaign_id)
    return FileResponse(
        path=path,
        filename=f"{campaign_id}.db",
        media_type="application/octet-stream",
    )


@router.post("/import", response_model=CampaignRead, status_code=201)
async def import_campaign(file: UploadFile = File(...)) -> CampaignRead:
    return await campaign_service.import_campaign(file)
