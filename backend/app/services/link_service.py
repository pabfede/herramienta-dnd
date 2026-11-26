from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.errors import DuplicateLinkError, NotFoundError
from app.models.faction import Faction
from app.models.link import Link
from app.models.location import Location
from app.models.npc import Npc
from app.services import entity_service

KIND_MODELS: dict[str, type] = {
    "npc": Npc,
    "location": Location,
    "faction": Faction,
}

# reverse lookup used by entity_service to know which deletes need link cascade
MODEL_KINDS: dict[type, str] = {model: kind for kind, model in KIND_MODELS.items()}


def _canonical_pair(
    kind_a: str, id_a: str, kind_b: str, id_b: str
) -> tuple[str, str, str, str]:
    if (kind_a, id_a) <= (kind_b, id_b):
        return kind_a, id_a, kind_b, id_b
    return kind_b, id_b, kind_a, id_a


def create_link(
    session: Session, kind_a: str, id_a: str, kind_b: str, id_b: str, relation: str | None = None
) -> Link:
    for kind, entity_id in ((kind_a, id_a), (kind_b, id_b)):
        if kind not in KIND_MODELS:
            raise NotFoundError(kind, entity_id)
        entity_service.get_entity(session, KIND_MODELS[kind], entity_id)

    kind_a, id_a, kind_b, id_b = _canonical_pair(kind_a, id_a, kind_b, id_b)
    if kind_a == kind_b and id_a == id_b:
        raise DuplicateLinkError(kind_a, id_a, kind_b, id_b)

    existing = session.scalars(
        select(Link).where(
            Link.kind_a == kind_a,
            Link.id_a == id_a,
            Link.kind_b == kind_b,
            Link.id_b == id_b,
        )
    ).first()
    if existing is not None:
        raise DuplicateLinkError(kind_a, id_a, kind_b, id_b)

    link = Link(kind_a=kind_a, id_a=id_a, kind_b=kind_b, id_b=id_b, relation=relation)
    session.add(link)
    session.commit()
    session.refresh(link)
    return link


def links_for(session: Session, kind: str, entity_id: str) -> list[Link]:
    return list(
        session.scalars(
            select(Link).where(
                or_(
                    and_(Link.kind_a == kind, Link.id_a == entity_id),
                    and_(Link.kind_b == kind, Link.id_b == entity_id),
                )
            )
        )
    )


def delete_link(session: Session, link_id: str) -> None:
    link = session.get(Link, link_id)
    if link is None:
        raise NotFoundError("Link", link_id)
    session.delete(link)
    session.commit()


def delete_links_for(session: Session, kind: str, entity_id: str) -> None:
    for link in links_for(session, kind, entity_id):
        session.delete(link)
    session.commit()
