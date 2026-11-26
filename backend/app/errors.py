from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    def __init__(self, entity: str, entity_id: str):
        self.entity = entity
        self.entity_id = entity_id
        super().__init__(f"{entity} {entity_id} not found")


class CampaignNotFoundError(NotFoundError):
    def __init__(self, campaign_id: str):
        super().__init__("Campaign", campaign_id)


class DuplicateLinkError(Exception):
    def __init__(self, kind_a: str, id_a: str, kind_b: str, id_b: str):
        self.kind_a = kind_a
        self.id_a = id_a
        self.kind_b = kind_b
        self.id_b = id_b
        super().__init__(f"Link between {kind_a}:{id_a} and {kind_b}:{id_b} already exists")


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(DuplicateLinkError)
    async def duplicate_link_handler(request: Request, exc: DuplicateLinkError) -> JSONResponse:
        return JSONResponse(status_code=409, content={"detail": str(exc)})
