import random

from sqlalchemy.orm import Session

from app.models.npc import Npc
from app.services import entity_service


def generate_encounter(session: Session, size: int, faction: str | None) -> list[dict]:
    npcs = entity_service.list_entities(session, Npc)
    if faction:
        # shortcut: faction is a free-text tag on custom_fields, not a real
        # Faction relationship; upgrade once Phase 4 wires NPC-faction links.
        npcs = [npc for npc in npcs if npc.custom_fields.get("faction") == faction]

    if not npcs or size <= 0:
        return []

    pool = random.sample(npcs, size) if len(npcs) >= size else random.choices(npcs, k=size)
    return [
        {"name": npc.name, "source_id": npc.id, "initiative": None}
        for npc in pool
    ]
