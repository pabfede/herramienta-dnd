from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.errors import register_exception_handlers
from app.routers import campaigns, encounters, factions, locations, npcs


def create_app() -> FastAPI:
    app = FastAPI(title="Herramienta DnD", version="0.1.0")

    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(campaigns.router)
    app.include_router(npcs.router)
    app.include_router(locations.router)
    app.include_router(factions.router)
    app.include_router(encounters.router)

    return app


app = create_app()
